# -*- coding: utf-8 -*-
# esc_sonnet_h1-2_3of7 — 이미지 기준 전사 (84 항목 / 80쪽)
# 문서: 260828_대칭이동 (1 id) + 260828_충분조건과 필요조건 (44 id) + 260828_집합의 연산과 벤 다이어그램 (39 id)
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_3A = ["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄷ", "ㄱ, ㄴ, ㄷ"]

# ================= 260828_대칭이동 =================
add(id="3e0f2891", qtype="choice",
    question=("좌표평면 위에 두 점 [[A(-5, 5)]], [[B(8, 4)]]가 있다.\n"
              "[[x]]축 위의 두 점 P, Q와 직선 [[y = 2]] 위의 점 R에 대하여\n"
              "[[seg(AP) + seg(PR) + seg(RQ) + seg(QB)]]의 최솟값은?"),
    choices=["[[10 sqrt(2)]]", "[[11 sqrt(2)]]", "[[12 sqrt(2)]]", "[[13 sqrt(2)]]", "[[14 sqrt(2)]]"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "좌표평면: 점 A(왼쪽 위), B(오른쪽 위), x축 위의 점 P(원점 왼쪽)·Q(원점 오른쪽), 직선 y=2 위의 점 R, 꺾은선 A-P-R-Q-B"}}],
    difficulty_est=3, confidence=0.8, needs_review="도형 표현 불가: 좌표평면 위 꺾은선 경로 그림",
    note="A를 x축 대칭 A′(−5,−5), B를 x축 대칭 B′(8,−4) 후 y=2 대칭 B″(8,8) → A′B″=13√2 → ④. 빠른정답 3과 불일치.")

# ================= 260828_충분조건과 필요조건 =================
# --- 충분조건, 필요조건, 필요충분조건 ---
add(id="ddef7a72", qtype="choice",
    question=("두 실수 [[a]], [[b]]에 대하여 다음 보기 중 조건 [[p]]가 조건 [[q]]이기 위한 필요조건이지만 충분조건이 아닌 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[p]]: [[pow(a,2) + pow(b,2) = 0]], [[q]]: [[a b = 0]]\n"
              "ㄴ. [[p]]: [[(a - b)(b - c) = 0]], [[q]]: [[a = b = c]]\n"
              "ㄷ. [[p]]: [[pow(a,2) - 1 = 0]], [[q]]: [[abs(a) = 1]]\n"
              "ㄹ. [[p]]: [[pow(a,2) - 2a b + pow(b,2) = 0]], [[q]]: [[a = b = 0]]"),
    choices=["ㄱ, ㄴ", "ㄴ, ㄷ", "ㄷ, ㄹ", "ㄴ, ㄹ", "ㄱ, ㄴ, ㄹ"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="q⇒p이고 p⇏q인 것: ㄴ(a=b=c ⇒ (a−b)(b−c)=0), ㄹ(a=b=0 ⇒ a=b) → ④ = 빠른정답 ✓.")

add(id="f38aeed5", qtype="short",
    question=("다음 보기 중 조건 [[p]]가 조건 [[q]]이기 위한 필요조건이고 충분조건은 아닌 것을 있는 대로 고르시오.\n(단, [[a]], [[b]]는 실수이다.)\n<보기>\n"
              "ㄱ. [[p]]: [[union(A, B) = B]], [[q]]: [[subset(A, B)]]\n"
              "ㄴ. [[p]]: [[pow(a,2) + pow(b,2) = 0]], [[q]]: [[a = 0]]이고 [[b = 0]]\n"
              "ㄷ. [[p]]: [[pow(a,2) = pow(b,2)]], [[q]]: [[a = b]]"),
    choices=None, derived_answer="ㄷ", figure=None, difficulty_est=2, confidence=0.9,
    note="ㄱ·ㄴ은 필요충분, ㄷ은 a=b ⇒ a²=b²만 성립 → ㄷ (빠른정답 없음).")

add(id="83fb624f", qtype="choice",
    question="전체집합 [[U]]의 두 부분집합 [[A]], [[B]]에 대하여 두 조건 [[p]], [[q]]가 다음과 같을 때, [[p]]는 [[q]]이기 위한 필요조건이지만 충분조건은 아닌 것은?",
    choices=["[[p]]: [[comp(A) = U]], [[q]]: [[inter(A, comp(B)) = empty]]",
             "[[p]]: [[union(A, B) = A]], [[q]]: [[union(A, comp(B)) = U]]",
             "[[p]]: [[A - B = A]], [[q]]: [[subset(B, comp(A))]]",
             "[[p]]: [[union(comp(A), comp(B)) = empty]], [[q]]: [[comp(A) = empty]]",
             "[[p]]: [[B - comp(A) = empty]], [[q]]: [[A = U - B]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="⑤ p: A∩B=∅, q: A=Bᶜ → q⇒p, p⇏q. ①·④는 p가 충분조건, ②·③은 필요충분 → ⑤ (빠른정답 없음).")

add(id="ad241856", qtype="choice",
    question=("두 조건 [[a]], [[b]]에 대하여 <[[a]], [[b]]>를\n"
              "<[[a]], [[b]]> = 1 ([[a]]가 [[b]]이기 위한 충분조건), 0 ([[a]]가 [[b]]이기 위한 필요충분조건), [[-1]] ([[a]]가 [[b]]이기 위한 필요조건)\n"
              "으로 정의한다. 세 집합 [[A]], [[B]], [[X]]에 대하여 조건 [[p]], [[q]], [[r]]이 다음과 같을 때,\n"
              "[[p]]: [[subset(X, inter(A, B))]]\n[[q]]: [[subset(X, union(A, B))]]\n[[r]]: [[subset(X, A)]] 또는 [[subset(X, B)]]\n"
              "<[[p]], [[q]]> − 2<[[q]], [[r]]> − 3<[[r]], [[p]]>의 값은?"),
    choices=["[[-6]]", "[[-4]]", "[[0]]", "[[4]]", "[[6]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 한계: 경우 나눔(조각적) 정의 ⟨a, b⟩와 꺾쇠 기호를 텍스트로 전사",
    note="출처 [2007년 6월 고1 7번]. p⇒r⇒q: ⟨p,q⟩=1, ⟨q,r⟩=−1, ⟨r,p⟩=−1 → 1+2+3=6 → ⑤ (빠른정답 없음).")

add(id="c72f1d93", qtype="short",
    question="정수 전체의 집합에서 정의된\n두 조건 '[[p]]: [[0 <= a <= 2]]', '[[q]]: [[-8 < 3a - 2 < 7]]'에 대하여\n[[q]]는 [[p]]이기 위한 어떤 조건인지 말하시오.",
    choices=None, derived_answer="필요조건", figure=None, difficulty_est=1, confidence=0.9,
    note="Q: −2<a<3(정수 −1,0,1,2) ⊃ P={0,1,2} → p⇒q → q는 p이기 위한 필요조건. 빠른정답 '충분조건'과 불일치.")

add(id="394b4dfe", qtype="short",
    question="두 집합 [[A]], [[B]]에 대하여 두 조건 [[p]], [[q]]가 '[[p]]: [[inter(A, B) = A]]',\n'[[q]]: [[card(A) > card(B)]]'일 때, [[neg(q)]]는 [[p]]이기 위한 어떤 조건인지 말하시오.",
    choices=None, derived_answer="필요조건", figure=None, difficulty_est=1, confidence=0.9,
    note="p: A⊂B ⇒ n(A)≤n(B)(~q) → ~q는 필요조건 (빠른정답 없음).")

add(id="bad48aa2", qtype="choice",
    question="[[x]], [[y]]가 실수일 때, 다음 중에서 조건 [[p]]가 조건 [[q]]이기 위한 필요충분조건인 것은?",
    choices=["[[p]]: [[x + y >= 2]], [[q]]: [[x >= 1]] 또는 [[y >= 1]]",
             "[[p]]: [[x + y]]는 유리수이다., [[q]]: [[x]], [[y]]는 유리수이다.",
             "[[p]]: [[x y > x + y > 4]], [[q]]: [[x > 2]]이고 [[y > 2]]",
             "[[p]]: [[x y + 1 > x + y > 2]], [[q]]: [[x > 1]]이고 [[y > 1]]",
             "[[p]]: [[x y z = 0]], [[q]]: [[x y = 0]]"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="④ (x−1)(y−1)>0, x+y>2 ⇔ x>1, y>1 → ④ (빠른정답 없음). ②의 '유리수이다.,'는 원문 그대로.")

add(id="94522f93", qtype="choice",
    question=("전체집합 [[U]]의 공집합이 아닌 세 부분집합 [[A]], [[B]], [[C]]에서 두 조건 [[p]], [[q]]에 대하여 [[p]]가 [[q]]이기 위한 필요충분조건인 것만을 보기에서 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[p]]: [[B - A = empty]]\n[[q]]: [[union(A, comp(B)) = U]]\n"
              "ㄴ. [[p]]: [[union(B - A, A - B) = union(A, B)]]\n[[q]]: [[union(comp(A), comp(B)) = U]]\n"
              "ㄷ. [[p]]: [[subset(A, B)]], [[nsubset(B, A)]]\n[[q]]: [[union(comp(A), comp(B)) = comp(A)]]"),
    choices=["ㄱ", "ㄴ", "ㄷ", "ㄱ, ㄴ", "ㄴ, ㄷ"],
    derived_answer="④", figure=None, difficulty_est=3, confidence=0.85,
    note="ㄱ 둘 다 B⊂A, ㄴ 둘 다 A∩B=∅, ㄷ q는 A⊂B(A=B 허용) → ㄱ, ㄴ = ④. 빠른정답 1과 불일치.")

# --- 충분조건, 필요조건, 필요충분조건과 진리집합 ---
add(id="67731d5d", qtype="choice",
    question="전체집합 [[U]]에서 세 조건 [[p]], [[q]], [[r]]를 만족시키는 원소들의 집합을 각각 [[P]], [[Q]], [[R]]라 할 때, 세 집합 [[P]], [[Q]], [[R]] 사이에 아래 그림과 같은 관계가 성립한다. 이때 다음 중 옳은 것은?",
    choices=["[[neg(p)]]는 [[q]]이기 위한 충분조건이다.",
             "[[neg(r)]]는 [[neg(q)]]이기 위한 필요조건이다.",
             "[[p]]는 [[neg(q)]]이기 위한 필요조건이다.",
             "명제 '[[p]]이면 [[neg(r)]]이다.'는 참이다.",
             "명제 '[[neg(r)]]이면 [[p]]이다.'는 거짓이다."],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "벤다이어그램: 전체집합 U 안에 원 P와 원 R가 일부 겹치고, 원 Q는 R 안에 있으며 P와 만나지 않음"}}],
    difficulty_est=2, confidence=0.8, needs_review="도형 표현 불가: 벤다이어그램(포함 관계가 그림에만 있음)",
    note="Q⊂R, P∩Q=∅, P∩R≠∅: ①~④ 거짓, ⑤ Rᶜ⊄P이므로 거짓 명제 → ⑤ = 빠른정답 ✓.")

add(id="65b3eda8", qtype="choice",
    question="전체집합 [[U]]의 두 부분집합 [[P]], [[Q]]에 대하여\n두 조건 [[p]], [[q]]의 진리집합을 각각 [[P]], [[Q]]라 하자.\n[[p]]는 [[neg(q)]]이기 위한 충분조건일 때 다음 중 옳은 것은?",
    choices=["[[subset(P, Q)]]", "[[subset(Q, P)]]", "[[subset(comp(P), Q)]]", "[[inter(P, Q) = empty]]", "[[inter(P, comp(Q)) = Q]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="p⇒~q ⇔ P⊂Qᶜ ⇔ P∩Q=∅ → ④. 빠른정답 '충분'과 불일치(값 아님).")

add(id="55551361", qtype="choice",
    question="전체집합 [[U]]에 대하여 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각 [[P]], [[Q]], [[R]]라고 하자. [[p]]는 [[q]]이기 위한 충분조건, [[neg(r)]]는 [[q]]이기 위한 필요조건일 때, 다음 중 항상 옳은 것은?",
    choices=["[[subset(P, R)]]", "[[subset(comp(P), R)]]", "[[subset(Q, R)]]", "[[inter(P, R) = empty]]", "[[subset(union(P, R), Q)]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="P⊂Q⊂Rᶜ → P∩R=∅ → ④. 빠른정답 2와 불일치.")

add(id="c0ca7d60", qtype="short",
    question="전체집합 [[U]]에 대하여 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각 [[P]], [[Q]], [[R]]라 하자. [[union(P, Q) = Q]], [[Q - R = Q]]일 때, 다음 □ 안에 충분, 필요, 필요충분 중에서 알맞은 것을 써넣으시오.\n[[p]]는 [[neg(r)]]이기 위한 □조건이다.",
    choices=None, derived_answer="충분", figure=None, difficulty_est=1, confidence=0.9,
    note="P⊂Q, Q∩R=∅ → P⊂Rᶜ → p⇒~r → 충분조건. 빠른정답 5와 불일치(값 아님).")

add(id="b823ce21", qtype="choice",
    question="전체집합 [[U]]에 대하여 두 조건 [[p]], [[q]]의 진리집합을 각각 [[P]], [[Q]]라 하자. [[neg(q)]]가 [[p]]이기 위한 필요조건일 때,\n다음 중 옳지 않은 것은?",
    choices=["[[P - Q = P]]", "[[inter(P, Q) = empty]]", "[[inter(P, comp(Q)) = P]]", "[[union(P, Q) = U]]", "[[union(P, comp(Q)) = comp(Q)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="p⇒~q ⇔ P∩Q=∅; ④ P∪Q=U는 성립 안 함 → ④. 빠른정답 1과 불일치.")

add(id="5a43e845", qtype="choice",
    question=("두 조건 [[sub(p,n)]], [[sub(q,n)]] ([[n]] = 1, 2)에 대하여\n"
              "[[sub(P,n)]] = { [[x]] | [[x]]는 [[sub(p,n)]]을 만족한다. },\n"
              "[[sub(Q,n)]] = { [[x]] | [[x]]는 [[sub(q,n)]]을 만족한다. }이고, [[sub(p,1)]]은 [[sub(p,2)]]이기 위한 필요조건, [[sub(q,n)]]은 [[sub(p,n)]]이기 위한 충분조건일 때, 다음 중 옳지 않은 것은?"),
    choices=["[[inter(sub(P,1), sub(P,2)) = sub(P,2)]]",
             "[[inter(sub(P,1), sub(Q,1)) = sub(Q,1)]]",
             "[[union(union(sub(P,1), sub(Q,1)), sub(P,2)) = sub(P,1)]]",
             "[[inter(union(sub(P,1), sub(Q,1)), sub(P,2)) = sub(P,2)]]",
             "[[union(inter(sub(P,1), sub(Q,1)), sub(Q,2)) = sub(Q,1)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="P₂⊂P₁, Q₁⊂P₁, Q₂⊂P₂; ⑤ Q₁∪Q₂는 Q₁이 아닐 수 있음 → ⑤ = 빠른정답 ✓.")

add(id="fde208fa", qtype="choice",
    question=("세 조건 [[p]], [[q]], [[r]]에 대하여 [[p]]는 [[q]]이기 위한 충분조건이고, [[neg(q)]]는 [[neg(r)]]이기 위한 필요조건이다. 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각 [[P]], [[Q]], [[R]]라 할 때,\n"
              "집합 [[inter(comp(union(inter(Q, comp(R)), P)), inter(Q, R))]]를 간단히 한 것은?\n(단, 집합 [[P]], [[Q]], [[R]]는 전체집합 [[U]]의 부분집합이다.)"),
    choices=["[[P]]", "[[Q]]", "[[R]]", "[[Q - P]]", "[[R - Q]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="P⊂Q⊂R → Q∩Rᶜ=∅ → Pᶜ∩Q = Q−P → ④. 빠른정답 2와 불일치.")

add(id="2c3a753b", qtype="choice",
    question=("전체집합 [[U]]에서의 두 조건 [[p]], [[q]]의 진리집합을 각각 [[P]], [[Q]]라고 할 때, [[union(P, comp(Q - P)) = U]]를 만족하는 두 조건 [[p]], [[q]]로 알맞은 것만을 보기에서 있는 대로 고른 것은? (단, [[a]], [[b]], [[c]]는 실수이고 [[P != Q]])\n<보기>\n"
              "ㄱ. [[p]]: [[A - B = empty]], [[q]]: [[A = B]]\n"
              "ㄴ. [[p]]: [[union(A, B) = A]], [[q]]: [[inter(A, B) = B]]\n"
              "ㄷ. [[p]]: [[a b = 0]], [[q]]: [[abs(a) + abs(b) = 0]]\n"
              "ㄹ. [[p]]: [[a > b > 0]], [[q]]: [[0 < frac(1,a) < frac(1,b)]]\n"
              "ㅁ. [[p]]: [[pow(a,2) + pow(b,2) = 0]], [[q]]: [[pow(a,2) - pow(b,2) = 0]]"),
    choices=["ㄱ", "ㄱ, ㄷ", "ㄴ, ㄷ, ㄹ", "ㄱ, ㄴ, ㄹ, ㅁ", "ㄱ, ㄴ, ㄷ, ㄹ, ㅁ"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="조건식 ⇔ Q−P=∅ ⇔ Q⊊P(q⇒p, p⇏q): ㄱ, ㄷ → ② = 빠른정답 ✓.")

add(id="4c80fa95", qtype="choice",
    question="전체집합 [[U]]에 대하여 서로 다른 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각 [[P]], [[Q]], [[R]]라 하고,\n[[r]]는 '[[p]] 이고 [[q]]'이기 위한 충분조건일 때, 다음 중 항상 옳은 것이 아닌 것은?",
    choices=["[[inter(P, R) = R]]", "[[inter(Q, R) = R]]", "[[inter(R, comp(Q)) = empty]]", "[[inter(P, comp(Q)) = empty]]", "[[subset(R, union(P, Q))]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="R⊂P∩Q; ④ P⊂Q는 보장 안 됨 → ④ = 빠른정답 ✓.")

add(id="0aed1259", qtype="short",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 12의 양의 약수 }에 대하여 조건 [[p]]: [[pow(x,2) - 7x + 10 < 0]]의 진리집합을 [[P]], 두 조건 [[q]], [[r]]의 진리집합을 각각 [[Q]], [[R]]이라 하자. "
              "[[p]]는 [[q]]이기 위한 충분조건이고, [[r]]는 [[neg(p)]]이기 위한 필요조건일 때, 두 집합 [[Q]], [[R]]의 순서쌍 [[point(Q, R)]]의 개수를 구하시오."),
    choices=None, derived_answer="64", figure=None, difficulty_est=3, confidence=0.85,
    note="U={1,2,3,4,6,12}, P={3,4}; P⊂Q → 2⁴=16, Pᶜ⊂R → 2²=4 → 64. 빠른정답 4와 불일치.")

add(id="073da342", qtype="choice",
    question="전체집합 [[U]]에 대하여 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각 [[P]], [[Q]], [[R]]라 하자. 이 집합의 포함 관계가 아래 그림과 같을 때, 다음 중 옳은 것은?",
    choices=["[[r]]는 [[p]] 또는 [[q]]이기 위한 필요조건이다.",
             "[[neg(r)]]는 [[neg(p)]] 또는 [[neg(q)]]이기 위한 충분조건이다.",
             "[[r]]는 [[p]]이고 [[q]]이기 위한 충분조건이다.",
             "[[r]]는 [[p]]이고 [[q]]이기 위한 필요충분조건이다.",
             "[[neg(r)]]는 [[p]]이고 [[neg(q)]]이기 위한 충분조건이다."],
    derived_answer="③",
    figure=[{"fn": "unsupported", "args": {"raw": "벤다이어그램: 전체집합 U 안에 두 원 P, Q가 겹치고, 작은 원 R가 P∩Q 부분 안에 들어 있음"}}],
    difficulty_est=2, confidence=0.8, needs_review="도형 표현 불가: 벤다이어그램(포함 관계가 그림에만 있음)",
    note="R⊊P∩Q → r⇒(p이고 q) → ③ = 빠른정답 ✓.")

add(id="3a13f155", qtype="choice",
    question="세 조건 [[p]], [[q]], [[r]]에 대하여 [[q]]는 [[p]]이기 위한 필요조건이고,\n[[r]]는 [[p]]이기 위한 충분조건이다. 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각 [[P]], [[Q]], [[R]]라 할 때, 세 집합 사이의 포함 관계는?",
    choices=["[[P]] ⊂ [[Q]] ⊂ [[R]]", "[[P]] ⊂ [[R]] ⊂ [[Q]]", "[[Q]] ⊂ [[R]] ⊂ [[P]]", "[[R]] ⊂ [[P]] ⊂ [[Q]]", "[[R]] ⊂ [[Q]] ⊂ [[P]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="p⇒q: P⊂Q, r⇒p: R⊂P → R⊂P⊂Q → ④. 빠른정답 2와 불일치. 포함 연쇄는 ⊂를 텍스트로 둠.")

add(id="ab8c6eb4", qtype="choice",
    question="세 조건 [[p]], [[q]], [[r]]에 대하여 [[q]]는 [[neg(p)]]이기 위한\n충분조건이고, [[neg(r)]]는 [[p]]이기 위한 충분조건이다. 세 조건 [[p]], [[q]], [[r]]의 진리집합을 각각 [[P]], [[Q]], [[R]]라 할 때,\n세 집합 사이의 포함 관계는?",
    choices=["[[comp(P)]] ⊂ [[Q]] ⊂ [[R]]", "[[P]] ⊂ [[comp(R)]] ⊂ [[Q]]", "[[Q]] ⊂ [[comp(P)]] ⊂ [[R]]", "[[R]] ⊂ [[comp(P)]] ⊂ [[Q]]", "[[comp(R)]] ⊂ [[Q]] ⊂ [[P]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="Q⊂Pᶜ, Rᶜ⊂P ⇔ Pᶜ⊂R → Q⊂Pᶜ⊂R → ③. 빠른정답 5와 불일치. 포함 연쇄는 ⊂를 텍스트로 둠.")

# --- 충분조건, 필요조건, 필요충분조건을 만족하는 미지수 구하기 ---
add(id="8543bb41", qtype="choice",
    question=("실수 [[x]]에 대한 두 조건\n[[p]]: [[pow(x,2) - 2a x + 25 < 0]], [[q]]: [[pow(x,2) + 4b x + 16 >= 0]]\n"
              "이 있다. 다음 두 문장이 모두 참인 명제가 되도록 하는 정수 [[a]], [[b]]의 순서쌍 [[point(a, b)]]의 개수는?\n"
              "· 모든 실수 [[x]]에 대하여 [[q]]이다.\n· [[neg(q)]]는 [[p]]이기 위한 필요조건이다."),
    choices=["[[45]]", "[[55]]", "[[63]]", "[[77]]", "[[81]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="Q=ℝ ⇒ −2≤b≤2(5개); p⇒~q ⇒ P=∅ ⇒ −5≤a≤5(11개) → 55 → ② = 빠른정답 ✓.")

add(id="96c9e37a", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 30 이하의 자연수 }의\n부분집합 [[A]]가 다음 조건을 만족시킨다.\n"
              "(가) 명제 '모든 [[in(x, U)]]에 대하여\n[[nsubset(set(x, pow(x,2) - 2), A)]]이다.'는 거짓이다.\n"
              "(나) 자연수 [[x]]에 대한 두 조건 [[p]], [[q]]가\n[[p]]: [[x]]는 [[in(frac(1,3) x, A)]]인 30 이하의 자연수이다.\n"
              "[[q]]: [[x]]는 [[in(x, A)]]인 30 이하의 3의 배수이다.\n일 때, [[p]]는 [[q]]이기 위한 필요충분조건이다.\n"
              "[[notin(3, A)]]일 때, 집합 [[A]]의 모든 원소의 합의 최솟값은?"),
    choices=["[[22]]", "[[24]]", "[[26]]", "[[28]]", "[[30]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2025년 3월 고2 20번 변형]. k∈A⇔3k∈A(k≤10); 3∉A→1,9,27∉A; x=2: {2,6,18} 합 26 → ③ = 빠른정답 ✓.")

dup(["1979f246", "ae0b7fcd"], qtype="short",
    question=("두 조건 [[p]], [[q]]가 [[p]]: [[pow(x,2) + 4a x + 32 > 0]],\n[[q]]: [[pow(x,2) + 2b x + 16 <= 0]]일 때, 다음 두 문장이 모두 참인 명제가 되도록 하는 정수 [[a]], [[b]]의 순서쌍 [[point(a, b)]]의 개수를 구하시오.\n"
              "(가) 모든 실수 [[x]]에 대하여 [[p]]이다.\n(나) [[p]]는 [[neg(q)]]이기 위한 충분조건이다."),
    choices=None, derived_answer="35", figure=None, difficulty_est=3, confidence=0.9,
    note="a²<8 → a∈{−2..2}(5개); P=ℝ이므로 Q=∅ → b²<16 → b∈{−3..3}(7개) → 35. 빠른정답 5와 불일치. 같은 이미지에 id 2개.")

add(id="619d4663", qtype="choice",
    question=("실수 [[x]]에 대한 두 조건\n[[p]]: [[pow(x,2) - 2a x + 4 >= 0]], [[q]]: [[pow(x,2) - b x + 9 <= 0]]이 있다.\n"
              "다음 두 문장이 모두 참인 명제가 되도록 하는\n정수 [[a]], [[b]]의 순서쌍 [[point(a, b)]]의 개수는?\n"
              "· 모든 실수 [[x]]에 대하여 [[p]]이다.\n· [[neg(q)]]는 [[p]]이기 위한 필요조건이다."),
    choices=["[[35]]", "[[40]]", "[[45]]", "[[50]]", "[[55]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2022년 3월 고2 17번 변형]. a²≤4 → 5개; Q=∅ → b²<36 → 11개 → 55 → ⑤. 빠른정답 2와 불일치.")

add(id="a545a983", qtype="short",
    question="실수 [[x]]에 대한 두 조건\n[[p]]: [[pow(x,2) - 4x + 3 <= 0]],\n[[q]]: [[x <= a]]\n에 대하여 [[p]]가 [[q]]이기 위한 충분조건이 되도록 하는\n실수 [[a]]의 최솟값을 구하시오.",
    choices=None, derived_answer="3", figure=None, difficulty_est=1, confidence=0.9,
    note="출처 [2018년 9월 고2 이과 25번/3점]. P=[1,3]⊂(−∞,a] → a≥3 → 3. 빠른정답 4와 불일치.")

add(id="b8e2f866", qtype="choice",
    question=("실수 [[x]]에 대한 두 조건\n[[p]]: [[pow(x,2) + 2a x + 1 >= 0]], [[q]]: [[pow(x,2) + 2b x + 9 <= 0]]이 있다.\n"
              "다음 두 문장이 모두 참인 명제가 되도록 하는\n정수 [[a]], [[b]]의 순서쌍 [[point(a, b)]]의 개수는?\n"
              "· 모든 실수 [[x]]에 대하여 [[p]]이다.\n· [[p]]는 [[neg(q)]]이기 위한 충분조건이다."),
    choices=["[[15]]", "[[18]]", "[[21]]", "[[24]]", "[[27]]"],
    derived_answer="①", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2022년 3월 고2 17번/4점]. a²≤1 → 3개; Q=∅ → b²<9 → 5개 → 15 → ①. 빠른정답 35와 불일치.")

add(id="240866bb", qtype="choice",
    question="실수 [[x]]에 대한 두 조건\n[[p]]: [[pow(x - 1, 2) <= 0]],\n[[q]]: [[2 pow(x,2) - (3k + 7) x + 2 = 0]]\n에 대하여 [[p]]가 [[q]]이기 위한 필요조건이 되도록 하는\n모든 정수 [[k]]의 값의 합은?",
    choices=["[[-7]]", "[[-6]]", "[[-5]]", "[[-4]]", "[[-3]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2018년 10월 고3 문과 17번/4점]. Q⊂{1}: k=−1(중근 1) 또는 판별식<0인 k=−3,−2 → 합 −6 → ②. 빠른정답 3과 불일치.")

add(id="df8b63f3", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 20 이하의 자연수 }의\n부분집합 [[A]]가 다음 조건을 만족시킨다.\n"
              "(가) 명제 '모든 [[in(x, U)]]에 대하여\n[[nsubset(set(x, pow(x,2) + 1), A)]]이다.'는 거짓이다.\n"
              "(나) 자연수 [[x]]에 대한 두 조건 [[p]], [[q]]가\n[[p]]: [[x]]는 [[in(frac(1,2) x, A)]]인 20 이하의 자연수이다.\n"
              "[[q]]: [[x]]는 [[in(x, A)]]인 20 이하의 짝수이다.\n일 때, [[p]]는 [[q]]이기 위한 필요충분조건이다.\n"
              "[[notin(1, A)]]일 때, 집합 [[A]]의 모든 원소의 합의 최솟값은?"),
    choices=["[[50]]", "[[53]]", "[[56]]", "[[59]]", "[[62]]"],
    derived_answer="③", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2025년 3월 고2 20번/4점]. k∈A⇔2k∈A; 1∉A→2,4,8,16∉A; x=3: {3,6,12,10,5,20} 합 56 → ③. 빠른정답 1과 불일치.")

add(id="c2a6592b", qtype="short",
    question=("실수 [[x]]에 대하여 두 조건 [[p]]와 [[q]]가 [[p]]: [[a pow(x,2) + 4x - 3 >= 0]],\n[[q]]: [[pow(x,2) + 2b x + 16 > 0]]이다. 다음 두 명제가 모두 거짓이 되도록 하는 정수 [[a]]의 최댓값을 [[M]], 자연수 [[b]]의 최솟값을 [[m]]이라 할 때, [[M + m]]의 값을 구하시오.\n"
              "(가) 어떤 실수 [[x]]에 대하여 [[p]]이다.\n(나) [[neg(p)]]는 [[q]]이기 위한 충분조건이다."),
    choices=None, derived_answer="2", figure=None, difficulty_est=3, confidence=0.9,
    note="(가) 거짓: a<0, 16+12a<0 → M=−2; (나) 거짓: Q≠ℝ → b²≥16 → m=4 → 2 = 빠른정답 ✓.")

add(id="5110c5e6", qtype="short",
    question="두 조건 [[p]]: [[a - 2 < x <= a + 1]], [[q]]: [[x <= -2]] 또는\n[[x >= 5]]에 대하여 [[neg(p)]]는 [[q]]이기 위한 필요조건이 되도록\n하는 모든 정수 [[a]]의 개수를 구하시오.",
    choices=None, derived_answer="4", figure=None, difficulty_est=2, confidence=0.9,
    note="q⇒~p ⇔ P⊂(−2,5): a≥0, a<4 → 0,1,2,3 → 4 = 빠른정답 ✓.")

add(id="9f82f018", qtype="short",
    question="두 조건 [[p]]: [[a - 3 < x <= a + 2]], [[q]]: [[x < 2]] 또는 [[x > 8]]에\n대하여 [[neg(p)]]는 [[q]]이기 위한 필요조건이 되도록 하는 모든\n정수 [[a]]의 개수를 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=2, confidence=0.9,
    note="P⊂[2,8]: a≥5, a≤6 → 2 = 빠른정답 ✓.")

add(id="311f67f7", qtype="choice",
    question=("전체집합 [[U]] = { [[point(x, y)]] | [[x]], [[y]]는 실수 }에 대하여\n두 조건 [[p]], [[q]]가\n"
              "[[p]]: [[abs(x) <= 4]], [[abs(y) <= 2]]\n[[q]]: [[abs(x - a) <= 2]], [[abs(y - b) <= 1]]\n"
              "이다. [[p]]는 [[q]]이기 위한 필요조건이 되도록 하는\n두 실수 [[a]], [[b]]에 대하여 좌표평면에서 점 [[point(a, b)]]가 나타내는\n영역의 넓이는?"),
    choices=["[[4]]", "[[6]]", "[[8]]", "[[10]]", "[[12]]"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.9,
    note="Q⊂P ⇔ |a|≤2, |b|≤1 → 넓이 4×2=8 → ③. 빠른정답 2와 불일치.")

# --- 충분조건, 필요조건, 필요충분조건과 삼단논법 ---
add(id="d0be7cc5", qtype="choice",
    question="세 조건 [[p]], [[q]], [[r]]에 대하여 [[p]]는 [[q]]이기 위한\n충분조건이고, [[neg(q)]]는 [[r]]이기 위한 필요조건일 때,\n다음 명제 중 반드시 참이라고 할 수 없는 것은?",
    choices=["[[imp(p, neg(r))]]", "[[imp(q, neg(r))]]", "[[imp(neg(q), neg(p))]]", "[[imp(r, neg(p))]]", "[[imp(neg(r), q)]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="p⇒q, r⇒~q(q⇒~r): ①~④ 참, ⑤ ~r⇒q는 보장 안 됨 → ⑤. 빠른정답 2와 불일치.")

add(id="21fe2fb6", qtype="choice",
    question="네 조건 [[p]], [[q]], [[r]], [[s]]에 대하여 [[p]]는 [[q]]이기 위한 충분조건,\n[[r]]는 [[q]]이기 위한 필요조건, [[s]]는 [[neg(r)]]이기 위한 충분조건일\n때, 다음 중 옳은 것은?",
    choices=["[[r]] ⇒ [[q]]", "[[q]] ⇒ [[neg(p)]]", "[[s]] ⇒ [[neg(q)]]", "[[neg(s)]] ⇒ [[neg(p)]]", "[[neg(r)]] ⇒ [[p]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="p⇒q⇒r, s⇒~r⇒~q⇒~p → ③. 빠른정답 5와 불일치. ⇒ 기호는 텍스트.")

add(id="f6989e57", qtype="choice",
    question=("세 조건 [[p]], [[q]], [[r]]에 대하여 두 명제 [[imp(p, q)]], [[imp(neg(r), neg(q))]]가\n모두 참일 때, 다음 보기 중 옳은 것만을 있는 대로 고른\n것은?\n<보기>\n"
              "ㄱ. [[q]]는 [[p]]이기 위한 필요조건이다.\nㄴ. [[q]]는 [[r]]이기 위한 충분조건이다.\nㄷ. [[r]]은 [[p]]이기 위한 필요조건이다."),
    choices=CH_3A, derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="p⇒q⇒r → ㄱ, ㄴ, ㄷ 모두 참 → ⑤ = 빠른정답 ✓.")

add(id="2a7a3029", qtype="choice",
    question="세 조건 [[p]], [[q]], [[r]]에 대하여 [[r]]가 [[neg(q)]]이기 위한 충분조건,\n[[q]]가 [[p]]이기 위한 필요조건일 때, 다음 중 반드시 참이라고\n할 수 없는 것은?",
    choices=["[[p]] ⇒ [[q]]", "[[r]] ⇒ [[neg(q)]]", "[[p]] ⇒ [[neg(r)]]", "[[q]] ⇒ [[neg(r)]]", "[[neg(p)]] ⇒ [[r]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="r⇒~q(q⇒~r), p⇒q → p⇒~r; ⑤ ~p⇒r 보장 안 됨 → ⑤ = 빠른정답 ✓. ⇒ 기호는 텍스트.")

add(id="692f92b7", qtype="choice",
    question="세 조건 [[p]], [[q]], [[r]]에 대하여 [[p]]는 [[q]]이기 위한\n충분조건이고 [[neg(q)]]는 [[neg(r)]]이기 위한 필요조건일 때,\n다음 중 옳지 않은 것은?",
    choices=["[[p]] ⇒ [[r]]", "[[q]] ⇒ [[r]]", "[[neg(p)]] ⇒ [[neg(r)]]", "[[neg(q)]] ⇒ [[neg(p)]]", "[[neg(r)]] ⇒ [[neg(p)]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="p⇒q⇒r; ③ ~p⇒~r는 역이므로 보장 안 됨 → ③. 빠른정답 2와 불일치. ⇒ 기호는 텍스트.")

add(id="2bc0b11c", qtype="choice",
    question="[[p]] 는 [[q]] 이기 위한 필요조건, [[p]] 는 [[neg(r)]] 이기 위한\n충분조건일 때, 항상 참인 것은?",
    choices=["[[p]] ⇒ [[q]]", "[[neg(p)]] ⇒ [[r]]", "[[p]] ⇒ [[r]]", "[[r]] ⇒ [[neg(q)]]", "[[neg(r)]] ⇒ [[p]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="q⇒p⇒~r → 대우 r⇒~p⇒~q → ④. 빠른정답 5와 불일치. ⇒ 기호는 텍스트.")

add(id="95a42930", qtype="choice",
    question=("세 조건 [[p]], [[q]], [[r]]에 대하여 두 명제 [[imp(p, neg(q))]], [[imp(neg(r), q)]]가\n모두 참일 때, 다음 보기 중 옳은 것만을 있는 대로 고른\n것은?\n<보기>\n"
              "ㄱ. [[p]]는 [[neg(q)]]이기 위한 충분조건이다.\nㄴ. [[neg(q)]]는 [[r]]이기 위한 필요조건이다.\nㄷ. [[neg(r)]]는 [[neg(p)]]이기 위한 충분조건이다."),
    choices=["ㄱ", "ㄱ, ㄴ", "ㄱ, ㄷ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="p⇒~q, ~r⇒q(~q⇒r): ㄱ✓, ㄴ(r⇒~q) 보장 안 됨, ㄷ ~r⇒q⇒~p ✓ → ③ = 빠른정답 ✓.")

add(id="c7fa806d", qtype="choice",
    question="네 조건 [[p]], [[q]], [[r]], [[s]]에 대하여 [[p]]는 [[q]]이기 위한 필요조건,\n[[r]]은 [[q]]이기 위한 충분조건, [[s]]는 [[neg(r)]]이기 위한 충분조건일\n때, 다음 중 옳은 것은?",
    choices=["[[q]] ⇒ [[r]]", "[[q]] ⇒ [[neg(p)]]", "[[s]] ⇒ [[neg(q)]]", "[[neg(s)]] ⇒ [[neg(p)]]", "[[r]] ⇒ [[p]]"],
    derived_answer="⑤", figure=None, difficulty_est=2, confidence=0.9,
    note="r⇒q⇒p → ⑤ = 빠른정답 ✓. ⇒ 기호는 텍스트.")

add(id="b77ad696", qtype="short",
    question=("두 명제 [[p]] ⇒ [[q]] 와 [[q]] ⇒ [[r]] 가 모두 참이면 명제 [[p]] ⇒ [[r]] 도\n참이 된다. 이 성질을 이용하여 다음을 구하여라.\n"
              "네 조건 [[p]], [[q]], [[r]], [[s]] 에 대하여 [[p]]는 [[r]]이기 위한 충분조건, [[q]]는 [[r]]이기 위한 충분조건, [[s]]는 [[r]]이기 위한 필요조건, [[q]]는 [[s]]이기 위한 필요조건이다.\n"
              "이 때, [[p]] 는 [[q]] 이기 위한 무슨 조건인지 구하여라."),
    choices=None, derived_answer="충분조건", figure=None, difficulty_est=2, confidence=0.85,
    note="p⇒r, q⇒r, r⇒s, s⇒q → q⇔r⇔s, p⇒q → 충분조건. 빠른정답 3과 불일치(값 아님). ⇒ 기호는 텍스트.")

# ================= 260828_집합의 연산과 벤 다이어그램 =================
# --- 합집합과 교집합 ---
add(id="41a954a5", qtype="choice",
    question=("다항식 [[f(x) = (pow(x,2) - 8x + 13)(pow(x,2) + x + 5)]]에\n대하여 두 집합 [[A]], [[B]]를\n"
              "[[A]] = { [[f(n)]] | [[n]]은 20 이하의 자연수 },\n[[B]] = { [[m]] | [[m]]은 100 이하의 소수 }\n라 할 때, [[card(inter(A, B))]]의 값은?"),
    choices=["[[1]]", "[[2]]", "[[3]]", "[[4]]", "[[5]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2018년 3월 고2 이과 18번 변형]. f(2)=11, f(6)=47만 100 이하 소수 → 2 → ② = 빠른정답 ✓(전수 확인).")

add(id="1cee7872", qtype="choice",
    question="두 집합 [[A]], [[B]]에 대하여 [[A]] = { [[x]] | [[x]]는 6의 약수 },\n[[B]] = { [[x]] | [[x]]는 20의 약수 }일 때, [[inter(A, B)]]는?",
    choices=["[[set(1, 2, 3, 10)]]", "[[set(1, 2, 3, 6)]]", "[[set(2, 3, 4, 5)]]", "[[set(1, 2)]]", "[[set(1, 2, 3, 4, 6, 10, 20)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="{1,2,3,6}∩{1,2,4,5,10,20}={1,2} → ④. 빠른정답 15와 불일치.")

# --- 서로소인 집합 ---
dup(["f9ecabd8", "c3693a94"], qtype="choice",
    question=("9 이하의 자연수 [[k]]에 대하여 집합 [[sub(A,k)]]를\n[[sub(A,k)]] = { [[x]] | [[k - 2 <= x <= k + 2]], [[x]]는 실수 }라 하자.\n"
              "다음 보기 중 옳은 것만을 있는 대로 고른 것은?\n<보기>\n"
              "ㄱ. [[inter(inter(sub(A,1), sub(A,3)), sub(A,5)) = set(3)]]\n"
              "ㄴ. 9 이하의 두 자연수 [[l]], [[m]]에 대하여\n[[abs(l - m) > 4]]이면 [[inter(sub(A,l), sub(A,m)) = empty]] 이다.\n"
              "ㄷ. 모든 [[sub(A,k)]]와 서로소가 아니고 원소가 유한개인\n집합 중 원소의 개수가 최소인 집합의 원소의\n개수는 3이다."),
    choices=["ㄱ", "ㄴ", "ㄱ, ㄴ", "ㄴ, ㄷ", "ㄱ, ㄴ, ㄷ"],
    derived_answer="③", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2020년 11월 고1 21번 변형]. ㄱ [−1,3]∩[1,5]∩[3,7]={3} ✓, ㄴ ✓, ㄷ {3, 8}이 모든 A_k와 만나므로 최소 2개 → ✗ → ③. 빠른정답 5와 불일치. 같은 이미지에 id 2개.")

add(id="fe5a9a1e", qtype="short",
    question="집합 [[A]] = { [[x]] | [[x]]는 6 이하의 자연수 }의 부분집합 중에서\n집합 [[B]] = { [[x]] | [[x]]는 15 미만의 소수 }와 서로소인\n집합 [[X]]의 개수를 구하시오.",
    choices=None, derived_answer="8", figure=None, difficulty_est=1, confidence=0.9,
    note="X⊂A−B={1,4,6} → 2³=8 = 빠른정답 ✓.")

# --- 여집합과 차집합 ---
add(id="4109eceb", qtype="short",
    question=("집합 [[P]]에 대하여 P[x]를\n(1) [[in(x, P)]]이면 P[x] = [[set(-x + 1, 0, x - 1)]]\n(2) [[notin(x, P)]]이면 P[x] = [[set(1, x, pow(x,2))]]이라고 정의한다.\n"
              "두 집합 [[A]] = { [[x]] | [[x]]는 소수인 자연수 },\n[[B]] = { [[3x - 1]] | [[x]]는 자연수 }일 때, 집합\n([[A - B]])[2] ∪ ([[B - A]])[8]의 원소의 총합을 구하시오."),
    choices=None, derived_answer="7", figure=None, difficulty_est=3, confidence=0.8,
    needs_review="문법 범위 밖: 집합 기호 P[x](대괄호 표기) 정의를 텍스트로 혼합",
    note="2=3·1−1∈B이므로 2∉A−B → (A−B)[2]={1,2,4}; 8∈B−A → (B−A)[8]={−7,0,7}; 합 7. 빠른정답 2와 불일치.")

# --- 집합의 연산의 성질 ---
add(id="c9b4d4f1", qtype="short",
    question="전체집합 [[U]]의 부분집합 [[X]]에 대하여 □ 안에 알맞은\n집합을 써넣으시오.\n[[union(X, X)]] = □",
    choices=None, derived_answer="X", figure=None, difficulty_est=1, confidence=0.9,
    note="X∪X=X. 빠른정답 7과 불일치(정렬 오류 의심).")

add(id="38c09197", qtype="short",
    question="전체집합 [[U]]의 부분집합 [[P]]에 대하여 □ 안에 알맞은\n집합을 써넣으시오.\n[[inter(U, P)]] = □",
    choices=None, derived_answer="P", figure=None, difficulty_est=1, confidence=0.9,
    note="U∩P=P. 빠른정답 11과 불일치(정렬 오류 의심).")

add(id="117348b3", qtype="short",
    question="전체집합 [[U]]의 부분집합 [[Q]]에 대하여 □ 안에 알맞은\n집합을 써넣으시오.\n[[union(empty, Q)]] = □",
    choices=None, derived_answer="Q", figure=None, difficulty_est=1, confidence=0.9,
    note="∅∪Q=Q. 빠른정답 336과 불일치(정렬 오류 의심).")

add(id="516166cb", qtype="choice",
    question=("집합 [[S = set(a, b, c)]]의 부분집합을 원소로 갖는\n집합 [[X]]가 다음 두 조건을 만족한다.\n"
              "(가) [[in(A, X)]] 이면 [[in(S - A, X)]]\n(나) [[in(A, X)]], [[in(B, X)]]이면 [[in(union(A, B), X)]]\n"
              "이 때, 집합 [[X]]의 개수는? (단, [[X != empty]])"),
    choices=["[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2009년 9월 고1 18번]. 여집합·합집합에 닫힌 비공집합 족: {∅,S}, {∅,{a},{b,c},S}형 3개, P(S) → 5 → ④(전수 확인). 빠른정답 'P'(값 아님).")

add(id="caaf5969", qtype="short",
    question="전체집합 [[U]]의 부분집합 [[X]]에 대하여 □ 안에 알맞은\n집합을 써넣으시오.\n[[inter(U, X)]] = □",
    choices=None, derived_answer="X", figure=None, difficulty_est=1, confidence=0.9,
    note="U∩X=X. 빠른정답 'Q'와 불일치(정렬 오류 의심).")

# --- 집합의 연산을 이용하여 미지수 구하기 ---
add(id="9b8e06c7", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 20 이하의 자연수 }의 두 부분집합\n[[A = set(3, 10, a + 2)]], [[B = set(pow(a,2) - 4a + 2, a + 10)]]\n"
              "에 대하여 [[union(inter(A, comp(B)), inter(comp(A), B)) = set(3, 10, 15)]]일 때,\n상수 [[a]]의 값은?"),
    choices=["[[2]]", "[[3]]", "[[4]]", "[[5]]", "[[6]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="a=5: A={3,10,7}, B={7,15} → 대칭차 {3,10,15} ✓ → ④. 빠른정답 37과 불일치.")

add(id="700dae83", qtype="short",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 자연수 }의 부분집합 [[A]]는 원소의\n개수가 4 이고, 모든 원소의 합이 21이다. 상수 [[k]]에 대하여\n"
              "집합 [[B]] = { [[x + k]] | [[in(x, A)]] }가 다음 조건을 만족시킨다.\n"
              "(가) [[inter(A, B) = set(4, 6)]]\n(나) [[union(A, B)]]의 모든 원소의 합이 40이다.\n집합 [[A]] 의 모든 원소의 곱을 구하시오."),
    choices=None, derived_answer="432", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2016년 6월 고2 이과 26번/4점]. 21+(21+4k)−10=40 → k=2; A⊇{2,4,6}, 합 21 → A={2,4,6,9} → 곱 432. 빠른정답 4와 불일치.")

add(id="eced5948", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 자연수 }의 두 부분집합\n[[A = set(a, b, c)]], [[B = set(sqrt(a), sqrt(b), sqrt(c))]]\n"
              "가 다음 조건을 모두 만족시킬 때, 집합 [[B]]의 모든 원소의\n합의 최댓값은?\n"
              "(가) [[card(inter(A, B)) = 1]]\n(나) [[a < b < c]], [[b + c = 52]]"),
    choices=["[[11]]", "[[12]]", "[[13]]", "[[14]]", "[[15]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="b=16, c=36; a=4일 때 A∩B={4}, B={2,4,6} 합 12(a=1이면 11, a=9는 교집합 없음) → ② = 빠른정답 ✓.")

add(id="b4288acd", qtype="choice",
    question="두 집합 [[A = set(3, 7, a)]], [[B = set(a + 1, 6, 11)]]에 대하여\n[[B - A = set(11)]]일 때, 다음 중 옳지 않은 것은?\n(단, [[a]]는 상수이다.)",
    choices=["[[A = set(3, 6, 7)]]", "[[B = set(6, 7, 11)]]", "[[inter(A, B) = set(6, 7)]]", "[[A - B = set(3, 11)]]", "[[union(A, B) = set(3, 6, 7, 11)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="a=6: A={3,6,7}, B={6,7,11}, A−B={3} → ④ = 빠른정답 ✓.")

add(id="c9026380", qtype="short",
    question=("실수 전체의 집합 [[U]]의 두 부분집합 [[A]], [[B]]에 대하여\n[[card(A) = 5]], [[B]] = { [[frac(x + a, 2)]] | [[in(x, A)]] }이다. 두 집합 [[A]], [[B]]가\n"
              "다음 조건을 만족할 때, 상수 [[a]]의 값을 구하시오.\n"
              "(가) 집합 [[A]]의 모든 원소의 합은 32이다.\n(나) 집합 [[union(A, B)]]의 모든 원소의 합은 57이다.\n(다) [[inter(A, B) = set(11, 15)]]"),
    choices=None, derived_answer="14", figure=None, difficulty_est=3, confidence=0.9,
    note="합(B)=(32+5a)/2; 32+(32+5a)/2−26=57 → a=14 (A={−18,8,11,15,16} 확인). 빠른정답 2와 불일치.")

# --- 집합의 연산과 부분집합의 개수 ---
add(id="5a6eacf3", qtype="short",
    question="전체집합 [[U]] = { [[x]] | [[x]]는 12 이하의 자연수 }의 두 부분집합\n[[A]], [[B]]에 대하여 [[union(A - B, B - A) = set(1, 2, 3, 4, 6)]],\n[[inter(comp(A), comp(B)) = set(5, 7, 9)]]를 만족시키는 집합 [[inter(A, B)]]의 모든\n부분집합의 개수를 구하시오.",
    choices=None, derived_answer="16", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2017년 9월 고1 24번 변형]. A∩B={8,10,11,12} → 2⁴=16 = 빠른정답 ✓.")

add(id="78a3b01d", qtype="choice",
    question="전체집합 [[U]] = { [[x]] | [[x]]는 60 이하의 자연수 }의 두 부분집합\n[[A]] = { [[x]] | [[x]]는 8의 배수 }, [[B]] = { [[x]] | [[x]]는 3의 배수 }가 있다.\n[[union(A, X) = A]]이고 [[inter(B, X) = empty]] 인 집합 [[X]]의 개수는?",
    choices=["[[16]]", "[[24]]", "[[32]]", "[[40]]", "[[48]]"],
    derived_answer="③", figure=None, difficulty_est=2, confidence=0.9,
    note="출처 [2022년 3월 고2 13번 변형]. X⊂A−B, A−B={8,16,32,40,56}(5개) → 2⁵=32 → ③. 빠른정답 14와 불일치.")

add(id="c4287c7d", qtype="short",
    question="전체집합 [[U]] = { [[x]] | [[x]]는 19 이하의 홀수 }의 두 부분집합\n[[A]], [[B]]에 대하여 [[A - B = set(3, 9, 15)]], [[B - A = set(1, 5)]],\n[[comp(union(A, B)) = set(11, 13, 17)]]을 만족시키는 집합 [[A]]의 모든\n부분집합의 개수를 구하시오.",
    choices=None, derived_answer="32", figure=None, difficulty_est=2, confidence=0.9,
    note="A∩B={7,19} → A={3,7,9,15,19}(5개) → 2⁵=32. 빠른정답 16과 불일치.")

dup(["3e83796d", "7f5f57c2"], qtype="short",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 20 이하의 자연수 }의 공집합이\n아닌 서로 다른 두 부분집합 [[A]], [[B]]에 대하여 다음 조건을\n모두 만족시키는 집합 [[B]]의 개수를 구하시오.\n"
              "(가) [[A]] = { [[x]] | [[x]]는 3의 배수 }\n(나) [[subset(union(A, B) - inter(A, B), A - B)]]"),
    choices=None, derived_answer="62", figure=None, difficulty_est=3, confidence=0.9,
    note="(나) ⇔ B−A=∅ ⇔ B⊂A; A 원소 6개, B≠∅, B≠A → 2⁶−2=62. 빠른정답 3과 불일치. 같은 이미지에 id 2개.")

# --- 드모르간의 법칙 ---
add(id="1eec171b", qtype="short",
    question=("전체집합 [[U]]의 두 부분집합 [[A]], [[B]]가 다음 조건을\n만족시킬 때, 집합 [[B]]의 모든 원소의 합을 구하시오.\n"
              "(가) [[A = set(1, 2, 3, 4)]], [[union(comp(A), comp(B)) = set(3, 5, 7)]]\n"
              "(나) [[subset(X, U)]]이고 [[card(X) = 1]]인 모든 집합 [[X]]에\n대하여 집합 [[union(A, X) - B]]의 원소의 개수는\n1이다."),
    choices=None, derived_answer="19", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2021년 3월 고2 28번 변형]. A∩B={1,2,4}, A−B={3}, A∪B=U={1,2,3,4,5,7} → B={1,2,4,5,7} 합 19 = 빠른정답 ✓.")

add(id="d6179c5b", qtype="short",
    question="전체집합 [[U]] = {1, 2, 3, ⋯, 10}의 두 부분집합\n[[A = set(2, 3, 5, 7)]], [[B = set(1, 2, 5, 10)]]에 대하여\n집합 [[inter(union(A, B), comp(union(comp(A), comp(B))))]]의 원소의 개수를 구하시오.",
    choices=None, derived_answer="2", figure=None, difficulty_est=1, confidence=0.9,
    note="(Aᶜ∪Bᶜ)ᶜ=A∩B → (A∪B)∩(A∩B)=A∩B={2,5} → 2. 빠른정답 'U'(값 아님).")

add(id="c611295d", qtype="choice",
    question=("두 자연수 [[k]], [[m]] ([[k >= m]])에 대하여\n전체집합 [[U]] = { [[x]] | [[x]]는 [[k]] 이하의 자연수 }의\n두 부분집합 [[A]] = { [[x]] | [[x]]는 [[m]]의 약수 }, [[B]]가 다음 조건을\n만족시킨다.\n"
              "(가) [[B - A = set(3, 5, 6)]], [[card(union(A, comp(B))) = 9]]\n(나) 집합 [[A]]의 모든 원소의 합과 집합 [[B]]의 모든\n원소의 합은 서로 같다.\n"
              "집합 [[inter(comp(A), comp(B))]]의 모든 원소의 합은?"),
    choices=["[[46]]", "[[47]]", "[[48]]", "[[49]]", "[[50]]"],
    derived_answer="④", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2022년 3월 고2 19번 변형]. k−3=9 → k=12; 합(A−B)=14 → m=8, A={1,2,4,8}, B={1,3,5,6} → 나머지 {7,9,10,11,12} 합 49 → ④. 빠른정답 62와 불일치.")

add(id="242f526f", qtype="choice",
    question="전체집합 [[U]] = { [[x]] | [[x]]는 9 미만의 자연수 }의 두 부분집합\n[[A]] = { [[x]] | [[x]]는 8의 약수 }, [[B]] = { [[x]] | [[x]]는 6의 약수 }에\n대하여 [[inter(comp(A), comp(B))]]은?",
    choices=["[[set(4, 5)]]", "[[set(4, 7)]]", "[[set(5, 6)]]", "[[set(5, 7)]]", "[[set(5, 8)]]"],
    derived_answer="④", figure=None, difficulty_est=1, confidence=0.9,
    note="A∪B={1,2,3,4,6,8} → 여집합 {5,7} → ④. 빠른정답 19와 불일치.")

add(id="9fe460fc", qtype="short",
    question="전체집합 [[U]] = {1, 2, 3, ⋯, 30}의\n두 부분집합 [[A]] = {1, 3, 5, ⋯, 29},\n[[B]] = {2, 4, 6, ⋯, 30}에 대하여 [[union(comp(A), comp(B))]]을 구하시오.",
    choices=None, derived_answer="U", figure=None, difficulty_est=1, confidence=0.9,
    note="A∩B=∅ → (A∩B)ᶜ=U = 빠른정답 ✓.")

add(id="93d1b47a", qtype="choice",
    question="[[U]] = { [[x]] | [[x]]는 10 이하의 자연수 } 의 두 부분집합 [[A]],\n[[B]] 에 대하여\n[[A - B = set(2, 4)]], [[inter(A, B) = set(5)]], [[inter(comp(A), comp(B)) = set(1, 6, 7, 9)]]\n일 때, 집합 [[B]]는?",
    choices=["[[set(3, 5)]]", "[[set(5, 7)]]", "[[set(3, 5, 8)]]", "[[set(3, 5, 10)]]", "[[set(3, 5, 8, 10)]]"],
    derived_answer="⑤", figure=None, difficulty_est=1, confidence=0.9,
    note="B−A=U−{2,4}−{5}−{1,6,7,9}={3,8,10} → B={3,5,8,10} → ⑤. 빠른정답 4와 불일치.")

# --- 집합의 연산 법칙 ---
dup(["33159318", "2ad0a4a9"], qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 10 이하의 자연수 }의\n두 부분집합 [[A = set(1, 3, 5, 7, 9)]], [[B = set(2, 3, 5, 7)]]에\n"
              "대하여 집합 [[U]]의 부분집합 [[X]]가 다음 조건을 만족시킬 때,\n집합 [[X]]의 모든 원소의 합의 최솟값은?\n"
              "(가) [[card(X) = 7]]\n(나) [[A - X = B - X]]\n(다) [[inter(X - A, X - B) != empty]]"),
    choices=["[[26]]", "[[27]]", "[[28]]", "[[29]]", "[[30]]"],
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2021년 11월 고1 20번 변형]. (나)로 1,2,9∈X, (다)로 4,6,8,10 중 하나(4), 나머지 3,5,6 → 합 30 → ⑤(전수 확인). 빠른정답 4와 불일치. 같은 이미지에 id 2개.")

add(id="084d6cb4", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 10 이하의 자연수 }의\n두 부분집합 [[A = set(1, 2, 3, 4, 5)]], [[B = set(3, 4, 5, 6, 7)]]에\n"
              "대하여 집합 [[U]]의 부분집합 [[X]]가 다음 조건을 만족시킬 때,\n집합 [[X]]의 모든 원소의 합의 최솟값은?\n"
              "(가) [[card(X) = 6]]\n(나) [[A - X = B - X]]\n(다) [[inter(X - A, X - B) != empty]]"),
    choices=["[[26]]", "[[27]]", "[[28]]", "[[29]]", "[[30]]"],
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.9,
    note="출처 [2021년 11월 고1 20번/4점]. 1,2,6,7∈X, 8 포함, +3 → 합 27 → ②(전수 확인). 빠른정답 'U'(값 아님).")

add(id="c4ace88a", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 10 미만의 자연수 }의\n세 부분집합 [[A]], [[B]], [[C]]에 대하여\n[[notin(1, A)]], [[C = set(1, 3, 5, 7, 9)]],\n"
              "[[inter(comp(inter(union(B, C), B)), union(inter(B, C), C)) = set(3, 5, 9)]]일 때,\n다음 중 집합 [[inter(inter(A, B), C)]]의 원소가 될 수 있는 것은?"),
    choices=["[[4]]", "[[5]]", "[[6]]", "[[7]]", "[[8]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="식은 Bᶜ∩C=C−B={3,5,9} → B∩C={1,7}, 1∉A → 7 → ④ = 빠른정답 ✓.")

# --- 집합의 연산을 이용한 여러 가지 표현 ---
add(id="12b0e4e0", qtype="choice",
    question="전체집합 [[U]]의 서로 다른 두 부분집합 [[A]], [[B]]에 대하여\n[[subset(comp(B), comp(A))]]일 때, 다음 중 옳지 않은 것은?",
    choices=["[[subset(A, B)]]", "[[inter(A, B) = A]]", "[[union(A, B) = A]]", "[[A - B = empty]]", "[[union(comp(A), B) = U]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="Bᶜ⊂Aᶜ ⇔ A⊂B; A≠B이므로 A∪B=B≠A → ③ = 빠른정답 ✓.")

# --- 집합의 연산 법칙과 포함 관계 ---
add(id="6d653c4b", qtype="choice",
    question="전체집합 [[U]]의 두 부분집합 [[A]], [[B]]에 대하여\n[[union(union(comp(union(A, B)), inter(B, comp(A))), comp(B)) = U]]가 성립할 때,\n다음 중 [[A]], [[B]]의 관계를 옳게 나타낸 것은?",
    choices=["벤다이어그램: [[U]] 안에서 원 [[A]] 안에 원 [[B]]가 들어 있는 그림",
             "벤다이어그램: [[U]] 안에서 원 [[B]] 안에 원 [[A]]가 들어 있는 그림",
             "벤다이어그램: [[U]] 안에서 두 원 [[A]], [[B]]가 일부 겹치는 그림",
             "벤다이어그램: [[U]] 안에서 두 원 [[A]], [[B]]가 서로 떨어져 있는 그림",
             "벤다이어그램: [[U]] 안에서 [[A = B]]인 원 하나인 그림"],
    derived_answer="④",
    figure=[{"fn": "unsupported", "args": {"raw": "선지 ①~⑤가 벤다이어그램: ① A 안에 B ② B 안에 A ③ A, B 일부 겹침 ④ A, B 서로소 ⑤ A=B 원 하나"}}],
    difficulty_est=2, confidence=0.8, needs_review="도형 표현 불가: 선지 5개가 모두 벤다이어그램 그림(텍스트로 서술)",
    note="좌변=(B−A)∪Bᶜ=(A∩B)ᶜ=U → A∩B=∅ → ④(서로소). 빠른정답 1과 불일치.")

add(id="8e3c80c7", qtype="choice",
    question="전체집합 [[U]]의 두 부분집합 [[A]], [[B]]에 대하여\n[[inter(union(comp(A), comp(B)), comp(B - A)) = A]]일 때, 다음 중 옳은 것은?",
    choices=["[[subset(A, B)]]", "[[subset(B, A)]]", "[[inter(A, comp(B)) = B]]", "[[union(A, B) = U]]", "[[inter(A, B) = A]]"],
    derived_answer="④", figure=None, difficulty_est=2, confidence=0.9,
    note="좌변=(A∩B)ᶜ∩(B−A)ᶜ=Bᶜ → Bᶜ=A → A∪B=U → ④ = 빠른정답 ✓.")

add(id="03cc8750", qtype="choice",
    question="서로 다른 두 집합 [[A]], [[B]]에 대하여 [[subset(B, A)]]일 때, 다음 중\n나머지 넷과 다른 하나는?",
    choices=["[[union(A, B)]]", "[[union(A, inter(A, B))]]", "[[inter(union(A, B), B)]]", "[[union(A, inter(B, empty))]]", "[[union(union(A, B), inter(A, B))]]"],
    derived_answer="③", figure=None, difficulty_est=1, confidence=0.9,
    note="①②④⑤=A, ③=B → ③. 빠른정답 1과 불일치.")

# --- 벤다이어그램이 나타내는 집합 ---
add(id="dd32d1e3", qtype="choice",
    question="다음 벤 다이어그램에서 [[A = set(a, b, c, d, e, f)]], [[inter(A, B) = set(a, c, e)]] 가 성립할 때, 다음 중 집합 [[B]] 가 될 수\n있는 것은?",
    choices=["[[set(a, b, c, d, e)]]", "[[set(a, c, d, e, g)]]", "[[set(b, d, e, f, g)]]", "[[set(a, c, d, e, g)]]", "[[set(a, c, e, g, h)]]"],
    derived_answer="⑤",
    figure=[{"fn": "unsupported", "args": {"raw": "벤다이어그램: 두 원 A, B가 겹침. A만의 부분에 b, d, f, 겹치는 부분에 a, c, e, B만의 부분은 비어 있음"}}],
    difficulty_est=1, confidence=0.8, needs_review="도형 표현 불가: 원소가 표시된 벤다이어그램",
    note="B⊇{a,c,e}, b,d,f∉B → ⑤ = 빠른정답 ✓. 선지 ②와 ④가 같은 집합으로 인쇄됨(원문 그대로).")

# --- 배수 또는 약수의 집합의 연산 ---
add(id="21e5b3e9", qtype="choice",
    question=("전체집합 [[U]] = { [[x]] | [[x]]는 20 이하의 자연수 }의 부분집합\n[[sub(A,k)]] = { [[x]] | [[x(y - k) = 30]], [[in(y, U)]] },\n[[B = setb(x, in(frac(30 - x, 5), U))]]\n"
              "에 대하여 [[card(inter(sub(A,k), comp(B))) = 1]]이 되도록 하는\n모든 자연수 [[k]]의 개수는?"),
    choices=["[[3]]", "[[5]]", "[[7]]", "[[9]]", "[[11]]"],
    derived_answer="②", figure=None, difficulty_est=4, confidence=0.85,
    note="출처 [2019년 11월 고1 21번/4점]. B={5,10,15,20}; Bᶜ 쪽 30의 약수 x=2,3,6이 A_k에 들 조건 k≤5,10,15 중 하나만 → 11≤k≤15 → 5개 → ②(전수 확인). 빠른정답 5는 값(선지 ②). x(y−k)는 병치곱이나 파서상 함수 적용으로 읽힘.")

add(id="f48f097f", qtype="short",
    question=("자연수 [[n]]에 대하여 집합 [[sub(A,n)]]이\n[[sub(A,n)]] = { [[x]] | [[x]]는 [[n]]의 양의 배수 }\n"
              "일 때, 다음 조건을 모두 만족시키는 100 이하의 자연수\n[[n]]의 개수를 구하시오.\n"
              "(가) [[inter(sub(A,n), sub(A,4)) = sub(A,4n)]]\n(나) [[subset(sub(A,n) - sub(A,3), sub(A,n) - sub(A,2))]]"),
    choices=None, derived_answer="17", figure=None, difficulty_est=3, confidence=0.9,
    note="(가) gcd(n,4)=1(홀수), (나) 3|n → 100 이하 3의 홀수 배수 17개 = 빠른정답 ✓(전수 확인).")

add(id="8659629a", qtype="short",
    question="전체집합 [[U]] = { [[x]] | [[x]]는 100 이하의 자연수 }의 부분집합\n[[sub(A,k)]] = { [[x]] | [[x = k n + 1]], [[n]]은 정수 }에 대하여\n집합 [[inter(sub(A,3), union(sub(A,5), sub(A,30)))]]의 원소의 개수를 구하시오.\n(단, [[k]]는 자연수)",
    choices=None, derived_answer="7", figure=None, difficulty_est=2, confidence=0.9,
    note="A₃₀⊂A₅ → A₃∩A₅=A₁₅={1,16,31,46,61,76,91} → 7(전수 확인). 빠른정답 4와 불일치.")

add(id="d57fde25", qtype="short",
    question="자연수 [[k]]의 양의 배수의 집합을 [[sub(A,k)]]라 할 때,\n[[union(inter(sub(A,6), sub(A,9)), sub(A,36)) = sub(A,n)]]을 만족시키는 자연수 [[n]]의 값과\n[[subset(union(sub(A,12), sub(A,15)), sub(A,m))]]을 만족시키는 자연수 [[m]]의 최댓값의\n합을 구하시오.",
    choices=None, derived_answer="21", figure=None, difficulty_est=2, confidence=0.9,
    note="A₆∩A₉=A₁₈⊃A₃₆ → n=18; m | gcd(12,15)=3 → m=3 → 21. 빠른정답 2와 불일치.")
