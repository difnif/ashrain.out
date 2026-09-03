# -*- coding: utf-8 -*-
# esc_sonnet_h1-1_4of4 — 이미지 기준 전사 (13 항목 / 13쪽, 미지수가 2개인 연립이차방정식)
# 표기 관행: 연립방정식 중괄호는 두 식을 콤마로 나열(GUIDE §4). 두 연립방정식이 나올 때만 텍스트 중괄호 { }로 묶음.
ITEMS = []
def add(**kw): ITEMS.append(kw)
def dup(ids, **kw):
    for i in ids: ITEMS.append(dict(kw, id=i))

CH_NUM = lambda *v: ["[[%s]]" % x for x in v]

# p41
add(id="13a1369b", qtype="short",
    question=("두 연립방정식 { [[a x - y = 7]], [[x y = 20]] }, { [[x + y = b]], [[pow(x,2) + pow(y,2) = 41]] }의 "
              "공통인 해가 존재할 때, 자연수 [[a]], [[b]]에 대하여 [[a + b]]의 값을 구하시오."),
    choices=None, derived_answer="12", figure=None, difficulty_est=3,
    note="x+y=b, x²+y²=41 → xy=20 ⇒ b=9, (x,y)=(4,5)이면 a=3 → a+b=12 = 빠른정답 ✓. 두 연립의 중괄호는 텍스트 { }로.")

# p42
add(id="caab36fb", qtype="choice",
    question=("연립방정식 [[pow(x,2) + pow(y,2) - 2x - 2y = 8]], [[pow(x,2) - 2 x y + pow(y,2) = 16]]을 만족시키는 "
              "[[x]], [[y]]에 대하여 [[2x + y]]의 최솟값은?"),
    choices=CH_NUM("-3", "-2", "-1", "0", "1"),
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="x−y=±4, (x+y)²−4(x+y)=0 → 해 (2,−2),(−2,2),(4,0),(0,4) → 2x+y 최소 −2 → ②. 빠른정답 29와 불일치(정답표 정렬 오류 의심).")

# p47
add(id="c7759c56", qtype="choice",
    question=("연립방정식 [[x + y + 2 x y = 10]], [[3x + 3y - 2 x y = 6]]의 해를 "
              "[[x = alpha]], [[y = beta]]라 할 때, [[pow(alpha,2) + pow(beta,2)]]의 값은?"),
    choices=CH_NUM("8", "10", "12", "14", "16"),
    derived_answer="②", figure=None, difficulty_est=2,
    note="출처 [2022년 6월 고1 12번 변형]. x+y=4, xy=3 → α²+β²=16−6=10 → ② (빠른정답 없음).")

# p68
add(id="778e65aa", qtype="choice",
    question=("[[x]], [[y]]에 대한 연립방정식 [[x + y = 2a]], [[(x + 3)(y + 3) = 33 + pow(a,2)]]의 해 "
              "중에서 [[x]], [[y]]가 모두 실수인 해가 존재하도록 하는 정수 [[a]]의 최솟값은?"),
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="④", figure=None, difficulty_est=3,
    note="xy=a²−6a+24, 판별식 4a²−4(a²−6a+24)≥0 → a≥4 → ④ (빠른정답 없음).")

# p69
add(id="8d51653d", qtype="choice",
    question=("[[x]], [[y]]에 대한 연립방정식 [[x + y = 2a]], [[(x + 2)(y + 2) = 11 + pow(a,2)]]의 해 "
              "중에서 [[x]], [[y]]가 모두 실수인 해가 존재하도록 하는 정수 [[a]]의 최솟값은?"),
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="②", figure=None, difficulty_est=3, confidence=0.85,
    note="xy=a²−4a+7, 판별식 16a−28≥0 → a≥7/4 → 정수 최솟값 2 → ②. 빠른정답 10과 불일치(선지 범위 밖).")

# p70
add(id="34ccbf08", qtype="choice",
    question=("[[x]], [[y]]에 대한 연립방정식 [[2x + y = 1]], [[pow(x,2) - k y = -6]]이 "
              "오직 한 쌍의 해를 갖도록 하는 양수 [[k]]의 값은?"),
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="②", figure=None, difficulty_est=2,
    note="출처 [2020년 11월 고1 9번/3점]. x²+2kx−k+6=0의 판별식 k²+k−6=0 → k=2 → ② (빠른정답 없음).")

# p73
add(id="df43329f", qtype="choice",
    question=("연립방정식 [[x + y = 4]], [[x y + x + y = k + 4]]가 실근을 갖도록 "
              "하는 실수 [[k]]의 최댓값은?"),
    choices=CH_NUM("1", "2", "3", "4", "5"),
    derived_answer="④", figure=None, difficulty_est=2,
    note="x+y=4, xy=k → 16−4k≥0 → k≤4 → ④ (빠른정답 없음). 원문 '실수k' 띄어쓰기 없음 그대로 의미 유지.")

# p80
add(id="547a6b43", qtype="short",
    question=("연립방정식 [[x + y = 6]], [[2 pow(x,2) + 3 x y + k = 0]]이 실근을 갖도록 하는 "
              "실수 [[k]]의 최솟값을 구하시오."),
    choices=None, derived_answer="-81", figure=None, difficulty_est=2, confidence=0.85,
    note="y=6−x 대입: x²−18x−k=0, 판별식 81+k≥0 → k≥−81 → 최솟값 −81. 빠른정답 'neg 2'와 불일치(옆 문항 p83의 빠른정답이 'neg 81' → 정답표 한 칸 밀림 의심).")

# p83
add(id="f867ef59", qtype="choice",
    question=("[[x]], [[y]]에 대한 연립방정식 [[x - y = k]], [[x y + 2x + 4 = 0]]이 "
              "오직 한 쌍의 해를 갖도록 하는 모든 실수 [[k]]의 값의 합은?"),
    choices=CH_NUM("-4", "-2", "0", "2", "4"),
    derived_answer="⑤", figure=None, difficulty_est=3, confidence=0.85,
    note="출처 [2017년 3월 고2 문과 11번 변형]. x²+(2−k)x+4=0, 판별식 (2−k)²−16=0 → k=−2, 6 → 합 4 → ⑤. 빠른정답 'neg 81'과 불일치(정답표 밀림 의심).")

# p85 (도형)
_SEMI = ("그림과 같이 직선 위에 [[seg(AB) = {L}]]인 두 점 A, B가 있다. "
         "선분 AB 위의 점 C에 대하여 선분 AC의 중점을 [[sub(P,1)]], "
         "선분 CB의 중점을 [[sub(P,2)]]라 하고 [[sub(P,1)]]C = [[a]], C[[sub(P,2)]] = [[b]]라 하자. "
         "점 [[sub(P,1)]]을 중심으로 하고 반지름의 길이가 [[a + frac({N},2)]]인 "
         "반원 [[sub(O,1)]], 점 [[sub(P,2)]]를 중심으로 하고 반지름의 길이가 [[b + frac({N},2)]]"
         "인 반원 [[sub(O,2)]]를 각각 그린 후, 선분 [[sub(P,1)]][[sub(P,2)]]를 지름으로 하는 "
         "반원을 그린다. 두 반원 [[sub(O,1)]]과 [[sub(O,2)]]의 교점이 "
         "호 [[sub(P,1)]][[sub(P,2)]] 위에 있을 때, [[a b]]의 값은? (단, [[a < b]])")
_SEMI_FIG = lambda L: [{"fn": "unsupported", "args": {"raw": f"직선 위에 왼쪽부터 A, P₁, C, P₂, B(AB={L}); P₁ 중심 반원 O₁, P₂ 중심 반원 O₂(더 큼), 선분 P₁P₂를 지름으로 하는 반원; 세 반원이 한 점에서 만남"}}]
_SEMI_RV = "문법 범위 밖: 첨자 점 라벨 선분(P₁C, CP₂, P₁P₂)의 윗줄 표기 불가 → 텍스트 혼합 / 도형 표현 불가: 반원 3개 복합 도형"
add(id="fdedb1e0", qtype="choice",
    question=_SEMI.format(L="6", N="1"),
    choices=CH_NUM("frac(5,4)", "frac(7,4)", "frac(9,4)", "frac(11,4)", "frac(13,4)"),
    derived_answer="②", figure=_SEMI_FIG("6"), difficulty_est=4, confidence=0.75,
    needs_review=_SEMI_RV,
    note="출처 [2018년 6월 고1 19번/4점]. a+b=3, 교점에서 직각 ⇒ (a+1/2)²+(b+1/2)²=9 → ab=7/4 → ② (빠른정답 없음).")

# p95 (도형)
_ISO = ("다음 그림과 같이 [[seg(AB) = seg(AC)]]인 이등변삼각형 ABC의 "
        "변 BC 위의 한 점 D에 대하여 [[seg(BD) = {p}]], [[seg(CD) = {q}]]이다. "
        "두 선분 AB, AD의 길이가 모두 자연수가 되도록 하는 "
        "모든 삼각형 ABC의 둘레의 길이의 합은?")
_ISO_FIG = lambda p, q: [{"fn": "unsupported", "args": {"raw": f"이등변삼각형 ABC(A 위, B·C 아래), AB=AC 표시(등변 기호), 변 BC 위의 점 D와 선분 AD, BD={p}, DC={q} 점선 표시"}}]
add(id="9c923600", qtype="choice",
    question=_ISO.format(p="28", q="12") + "\n(단, [[seg(AC) - seg(AD) > 3]])",
    choices=CH_NUM("320", "322", "324", "326", "328"),
    derived_answer="①", figure=_ISO_FIG("28", "12"), difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 이등변삼각형+내부 선분 도형(unsupported 초안만 첨부)",
    note="AB²−AD²=BD·CD=336, (AB−AD)(AB+AD)=336, AB−AD>3, 2AB>40 → AB=44,31,25 → 둘레 128+102+90=320 → ①. 빠른정답 92와 불일치.")

# p98 (도형) — p85와 같은 유형(AB=16, 반지름 a+3/2, b+3/2)
add(id="667e05e5", qtype="choice",
    question=_SEMI.format(L="16", N="3"),
    choices=CH_NUM("12", "frac(51,4)", "frac(27,2)", "frac(57,4)", "15"),
    derived_answer="④", figure=_SEMI_FIG("16"), difficulty_est=4, confidence=0.75,
    needs_review=_SEMI_RV,
    note="a+b=8, (a+3/2)²+(b+3/2)²=64 → a²+b²=71/2 → ab=57/4 → ④ (빠른정답 없음).")

# p99 (도형)
add(id="a4c60f56", qtype="choice",
    question=_ISO.format(p="8", q="16"),
    choices=CH_NUM("146", "148", "150", "152", "154"),
    derived_answer="③", figure=_ISO_FIG("8", "16"), difficulty_est=4, confidence=0.8,
    needs_review="도형 표현 불가: 이등변삼각형+내부 선분 도형(unsupported 초안만 첨부)",
    note="AB²−AD²=128, 같은 홀짝 인수쌍 (2,64),(4,32),(8,16) → AB=33,18,12; 2AB>24 → 33,18 → 둘레 90+60=150 → ③. 빠른정답 '12 cm'와 불일치(정답표 밀림 의심).")
