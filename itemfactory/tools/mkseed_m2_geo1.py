# itemfactory/tools/mkseed_m2_geo1.py — 중2-2 삼각형의 성질 시드 생성기: 이등변삼각형 · 외심 · 내심 (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m2_geo1.py
#     → seeds/m2-2-isosceles.json (5틀) · seeds/m2-2-circumcenter.json (5틀) · seeds/m2-2-incenter.json (6틀)
#
# 유형은 출판사 평가자료 카탈로그(reference/pubs/TYPES.md 5.1·5.3·5.4)에서 골랐다 — 문항 복제 아님.
# 도형은 전부 scene: 각·길이를 좌표로 직접 계산해 실제 크기대로 그린다(외심·내심 좌표는 삼각형 각에서 정확히 계산).
# '주어진 각/구하는 각'이 바뀌는 틀은 표(행)에 꼭짓점 이름을, 파생값에 수치를 두어 라벨 "{gv}°"가 항상 실제 값이 되게 한다.
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402

SCHEMA_ISO = "d9d13b27-3a9a-4e78-ad94-8674c540c5a6"      # 이등변삼각형 두 밑각 크기 (A)
SCHEMA_CIRC = "dffe0bf8-3f6e-4906-a6bd-83bb15cfc294"     # 삼각형 외심에서 중심각과 원주각 관계 (A)
SCHEMA_INC = "d1ef1b08-72be-4657-a5b1-2fa5f50c6b28"      # 삼각형의 내접원과 선분의 길이 (A)

GEO = {"process": "추론", "context": "기하맥락", "points": 4, "time_limit": 80, "traps": ["구하는대상혼동"]}


def tpl(seed_id, no, *bases, **kw):
    t = dict(GEO)
    for b in bases:
        t.update(b)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def scene(pts, segs, marks=None, circles=None, labels=None, nodot=None, shade=None, aspect_min=None):
    a = {"pts": pts, "segs": segs}
    if marks:
        a["marks"] = marks
    if circles:
        a["circles"] = circles
    if labels:
        a["labels"] = labels
    if nodot:
        a["nodot"] = nodot
    if shade:
        a["shade"] = shade
    if aspect_min is not None:
        a["aspect_min"] = aspect_min
    return [{"fn": "scene", "args": a}]


def arc(at, fr, to, label=None, k=None):
    d = {"at": at, "from": fr, "to": to}
    if label is not None:
        d["label"] = label
    if k:
        d["k"] = k
    return d


# ═══════════════════════════════════════════════════════════════════ 1. 이등변삼각형
ISO = dict(prereq=["삼각형의 내각의 합 180°", "이등변삼각형의 두 밑각은 같다"], ops=["각도", "방정식"], tags=["이등변삼각형", "밑각", "꼭지각"])

# A 꼭지각, B·C 밑각. AB = AC = 1 로 두고 그린다.
ISO_PTS = {"A": [0, "{h}"], "B": ["{-w}", 0], "C": ["{w}", 0]}
ISO_DERIVE = {"w": "4*sin(pi*a/360)", "h": "4*cos(pi*a/360)"}


def iso_t1():
    rows = {"apex": {"GQ": "A", "XQ": "B", "isA": 1, "GA": "A", "GF": "B", "GT": "C", "XA": "B", "XF": "A", "XT": "C",
                     "READ": "꼭지각 ∠A가 주어졌으니 두 밑각 ∠B, ∠C가 같다는 것을 쓴다",
                     "F1": "∠B = (180° − ", "F2": "°) ÷ 2", "LAW": "(180° − 꼭지각) ÷ 2"},
            "base": {"GQ": "B", "XQ": "A", "isA": 0, "GA": "B", "GF": "A", "GT": "C", "XA": "A", "XF": "B", "XT": "C",
                     "READ": "밑각 ∠B가 주어졌으니 ∠C = ∠B이고, 꼭지각은 180°에서 두 밑각을 뺀 것이다",
                     "F1": "∠A = 180° − 2 × ", "F2": "°", "LAW": "180° − 2 × 밑각"}}
    return tpl("m2-2-isosceles", 1, ISO,
        title="이등변삼각형 — 꼭지각 ↔ 밑각",
        skill="두 밑각이 같음을 쓰고 내각의 합 180°로 나머지 각 구하기",
        variant_axis={"주어진 것": "꼭지각 / 밑각", "꼭지각": "30°~130° (짝수)"},
        discriminates="AB = AC에서 ∠B = ∠C를 끌어내고, 180°에서 빼는 것을 2로 나누거나 2배하는가",
        qtype="short", difficulty=1, pool_target=300, time_limit=60, process="절차수행",
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "a", "values": {"in": [v for v in range(30, 132, 2) if v != 60]}}],
        table={"key": "w", "rows": rows},
        derive={**ISO_DERIVE, "b": "(180 - a)/2", "gv": "a*isA + (180 - a)/2*(1 - isA)", "ans_v": "(180 - a)/2*isA + a*(1 - isA)"},
        constraints=["ans_v != gv"],
        cost_values=["a", "b", "gv", "ans_v"],
        answer_var="ans_v",
        verify=["a + 2*b == 180", "(isA == 1 and ans == b) or (isA == 0 and ans == a)"],
        question="다음 그림과 같이 [[seg(AB)]] = [[seg(AC)]]인 이등변삼각형 ABC에서 [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(ISO_PTS, [["A", "B"], ["B", "C"], ["C", "A"]],
                     marks={"eq": [[["A", "B"], ["A", "C"]]], "arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="AB = AC이므로 △ABC는 이등변삼각형이고, 이등변삼각형의 두 밑각의 크기는 같다: ∠B = ∠C. {READ}. 삼각형의 세 내각의 합은 180°다.",
        sol1_fig=scene(ISO_PTS, [["A", "B"], ["B", "C"], ["C", "A"]],
                       marks={"eq": [[["A", "B"], ["A", "C"]]], "arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]},
                       labels=[{"at": "B", "text": "{b}°", "dx": 14, "dy": -12, "accent": True, "k": "lbl:b"}, {"at": "C", "text": "{b}°", "dx": -14, "dy": -12, "accent": True, "k": "lbl:c"}]),
        sol1_anim=[[hl("eq:A-B", "eq:A-C", keep=True)], [hl("arc:given", keep=True)], [hl("lbl:b", "lbl:c")]],
        sol2=[
            "AB = AC이므로 ∠B = ∠C (이등변삼각형의 두 밑각)",
            "∠A + ∠B + ∠C = 180°이므로 {F1}{gv}{F2} = {ans_v}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠B = ∠C", "hint": "AB = AC"}, {"text": "{F1}{gv}{F2} = {ans_v}°", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], []],
        sol_check="세 각 {a}° + {b}° + {b}° = 180°로 합이 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="AB = AC이므로 ∠B = ∠C이다. 삼각형의 내각의 합이 180°이므로 {F1}{gv}{F2} = {ans_v}°이다. 따라서 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "밑각 상등", "points": 3, "criterion": "AB = AC이므로 ∠B = ∠C임을 밝혔다.", "partial": "근거 없이 두 각이 같다고만 썼으면 1점."},
            {"element": "내각의 합", "points": 2, "criterion": "세 내각의 합 180°를 써서 {F1}{gv}{F2}{ro(F2)} 나타냈다.", "partial": "180°를 썼으나 식이 틀렸으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": "다른 각을 답했으면 인정하지 않는다."},
        ],
    )


def iso_t2():
    # AB = AC, BC = BD (D는 변 AC 위). ∠C = b → ∠BDC = b, ∠DBC = 180 − 2b, ∠ABD = 3b − 180
    rows = {"base-ABD": {"GQ": "C", "XQ": "ABD", "isC": 1, "isABD": 1, "GA": "C", "GF": "B", "GT": "A", "XA": "B", "XF": "A", "XT": "D"},
            "apex-ABD": {"GQ": "A", "XQ": "ABD", "isC": 0, "isABD": 1, "GA": "A", "GF": "B", "GT": "C", "XA": "B", "XF": "A", "XT": "D"},
            "base-DBC": {"GQ": "C", "XQ": "DBC", "isC": 1, "isABD": 0, "GA": "C", "GF": "B", "GT": "A", "XA": "B", "XF": "D", "XT": "C"}}
    pts = {"A": [2, "{ay}"], "B": [0, 0], "C": [4, 0], "D": ["{dx}", "{dy}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["B", "D"]]
    marks = {"eq": [[["A", "B"], ["A", "C"]], [["B", "C"], ["B", "D"]]], "arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-isosceles", 2, ISO,
        title="이등변삼각형 두 개 — AB = AC, BC = BD 연쇄 각",
        skill="이등변삼각형이 두 개 겹친 그림에서 밑각을 차례로 옮겨 각을 구하기",
        variant_axis={"주어진 것": "∠C / ∠A", "구하는 것": "∠ABD / ∠DBC", "∠C": "62°~80°"},
        discriminates="△BCD도 이등변삼각형(BC = BD)임을 읽어 ∠BDC = ∠C를 쓰는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "r", "values": {"in": list(rows)}}, {"name": "b", "values": {"int": [62, 80]}}],
        table={"key": "r", "rows": rows},
        derive={"a": "180 - 2*b", "dbc": "180 - 2*b", "abd": "3*b - 180", "gv": "b*isC + (180 - 2*b)*(1 - isC)", "ans_v": "(3*b - 180)*isABD + (180 - 2*b)*(1 - isABD)",
                "ay": "2*tan(pi*b/180)", "dx": "4 - 8*cos(pi*b/180)*cos(pi*b/180)", "dy": "8*tan(pi*b/180)*cos(pi*b/180)*cos(pi*b/180)"},
        constraints=["ans_v != gv", "ans_v >= 4"],
        cost_values=["b", "a", "dbc", "abd", "ans_v"],
        answer_var="ans_v",
        verify=["abd + dbc == b", "a + 2*b == 180", "(isABD == 1 and ans == abd) or (isABD == 0 and ans == dbc)"],
        question="다음 그림에서 △ABC는 [[seg(AB)]] = [[seg(AC)]]인 이등변삼각형이고, 점 D는 [[seg(BC)]] = [[seg(BD)]]가 되도록 변 AC 위에 잡은 점이다. [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="이등변삼각형이 두 개다. △ABC(AB = AC)에서 ∠ABC = ∠ACB이고, △BCD(BC = BD)에서 ∠BDC = ∠BCD다. 주어진 각에서 ∠C = {b}°를 정하면 △BCD의 두 밑각이 {b}°로 정해지고, ∠DBC는 180°에서 그 둘을 뺀 값, ∠ABD는 ∠ABC에서 ∠DBC를 뺀 값이다.",
        sol1_fig=scene(pts, segs, marks=marks,
                       labels=[{"at": "D", "text": "{b}°", "dx": -16, "dy": 16, "accent": True, "k": "lbl:d"}, {"at": "B", "text": "{b}°", "dx": 22, "dy": -10, "accent": True, "k": "lbl:b"}]),
        sol1_anim=[[hl("eq:A-B", "eq:A-C", "arc:given", keep=True)], [hl("lbl:b", keep=True)], [hl("eq:B-C", "eq:B-D", "lbl:d", keep=True)], [hl("arc:ask")]],
        sol2=[
            "AB = AC이므로 ∠ABC = ∠ACB = {b}° (∠A = 180° − 2 × {b}° = {a}°)",
            "BC = BD이므로 △BCD는 이등변삼각형이고 ∠BDC = ∠BCD = {b}°",
            "△BCD에서 ∠DBC = 180° − {b}° − {b}° = {dbc}°",
            "∠ABD = ∠ABC − ∠DBC = {b}° − {dbc}° = {abd}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠ABC = ∠ACB = {b}°", "hint": "AB = AC"}, {"text": "∠BDC = ∠BCD = {b}°", "hint": "BC = BD"},
                        {"text": "∠DBC = 180° − 2 × {b}° = {dbc}°", "hint": "△BCD의 내각의 합"}, {"text": "∠ABD = {b}° − {dbc}° = {abd}°", "hint": "∠ABC − ∠DBC"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")], []],
        sol_check="△ABD에서 ∠A + ∠ABD + ∠ADB = {a}° + {abd}° + {180 - b}° = 180°(∠ADB는 ∠BDC = {b}°의 보각)로 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="AB = AC이므로 ∠ABC = ∠ACB = {b}°이다. BC = BD이므로 △BCD는 이등변삼각형이고 ∠BDC = ∠BCD = {b}°, ∠DBC = 180° − 2 × {b}° = {dbc}°이다. ∠ABD = ∠ABC − ∠DBC = {b}° − {dbc}° = {abd}°이므로 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "두 이등변삼각형의 밑각", "points": 3, "criterion": "∠ABC = ∠ACB = {b}°와 ∠BDC = ∠BCD = {b}°를 각각의 이등변삼각형에서 밝혔다.", "partial": "한 삼각형의 밑각만 옳게 썼으면 1점."},
            {"element": "각의 계산", "points": 2, "criterion": "∠DBC = 180° − 2 × {b}° = {dbc}°, ∠ABD = {b}° − {dbc}° = {abd}°를 계산했다.", "partial": "∠DBC까지만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": "다른 각을 답했으면 인정하지 않는다."},
        ],
    )


def iso_t3():
    # AB = AC, AD ⊥ BC → BD = CD. BC = 2k, AD = h
    # 표 행은 정적 문자열만 — 수는 v1·v2·v3 로 틀에서 채운다 (행 안의 {k} 등은 채워지지 않는다)
    rows = {"abd": {"Q": "△ABD의 넓이", "isS": 1, "isT": 0, "isB": 0, "U": " cm²", "UA": "cm²", "FORM1": "△ABD = [[frac(1, 2)]] × ", "FORM2": " × ",
                    "STEP1": "△ABD의 넓이 = [[frac(1, 2)]] × BD × AD = [[frac(1, 2)]] × ", "STEP2": " × ", "STEP3": " = ", "STEP4": "(cm²)"},
            "abc": {"Q": "△ABC의 넓이", "isS": 0, "isT": 1, "isB": 0, "U": " cm²", "UA": "cm²", "FORM1": "△ABC = [[frac(1, 2)]] × ", "FORM2": " × ",
                    "STEP1": "△ABC의 넓이 = [[frac(1, 2)]] × BC × AD = [[frac(1, 2)]] × ", "STEP2": " × ", "STEP3": " = ", "STEP4": "(cm²)"},
            "bd": {"Q": "[[seg(BD)]]의 길이", "isS": 0, "isT": 0, "isB": 1, "U": " cm", "UA": "cm", "FORM1": "BD = ", "FORM2": " ÷ ",
                   "STEP1": "BD = BC ÷ 2 = ", "STEP2": " ÷ ", "STEP3": " = ", "STEP4": "(cm)"}}
    pts = {"A": [0, "{h}"], "B": ["{-k}", 0], "C": ["{k}", 0], "D": [0, 0]}
    segs = [["A", "B"], ["C", "A"], ["B", "C"], ["D", "A"]]
    # BC 중점이 D라 선분 라벨이 D 이름과 겹치므로 4분점에, 세로 선분 AD의 라벨은 선 위에 얹히지 않게 오른쪽으로 띄운다
    bclab = [{"at": ["{-k/2}", 0], "text": "{2*k} cm", "dx": 0, "dy": 15, "k": "lbl:bc"}, {"at": [0, "{h/2}"], "text": "{h} cm", "dx": 24, "dy": 4, "k": "lbl:ad"}]
    marks = {"eq": [[["A", "B"], ["A", "C"]]], "right": [["A", "D", "C"]]}
    return tpl("m2-2-isosceles", 3, ISO,
        title="꼭지각의 이등분선(수선) — 밑변의 수직이등분과 넓이",
        skill="이등변삼각형의 꼭짓점에서 밑변에 내린 수선은 밑변을 이등분함을 써서 길이·넓이 구하기",
        variant_axis={"구하는 것": "△ABD 넓이 / △ABC 넓이 / BD", "BC": "6~18", "AD": "4~12"},
        discriminates="AD ⊥ BC이면 BD = CD = BC/2임을 쓰는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70, process="절차수행",
        prereq=["삼각형의 넓이", "이등변삼각형의 꼭지각의 이등분선은 밑변을 수직이등분한다"], ops=["넓이", "사칙"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "k", "values": {"int": [3, 9]}}, {"name": "h", "values": {"int": [4, 12]}}],
        table={"key": "w", "rows": rows},
        derive={"S": "k*h/2", "T": "k*h", "ans_v": "k*h/2*isS + k*h*isT + k*isB", "v1": "k*isS + 2*k*(1 - isS)", "v2": "h*(1 - isB) + 2*isB", "v3": "k*h/2*isS + k*h*isT + k*isB"},
        constraints=["isS == 0 or (k*h) % 2 == 0", "k != h"],
        cost_values=["k", "h", "S", "ans_v"],
        answer_var="ans_v",
        verify=["T == 2*S", "(isS == 1 and ans == S) or (isT == 1 and ans == T) or (isB == 1 and ans == k)"],
        question="다음 그림과 같이 [[seg(AB)]] = [[seg(AC)]]인 이등변삼각형 ABC에서 꼭짓점 A에서 밑변 BC에 내린 수선의 발을 D라고 하자. [[seg(BC)]] = {2*k} cm, [[seg(AD)]] = {h} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks, labels=bclab),
        answer="{ans_v}", answer_alt=["{ans_v}{U}"],
        sol1="이등변삼각형의 꼭짓점 A에서 밑변에 내린 수선 AD는 꼭지각의 이등분선이자 밑변의 수직이등분선이다. 그러므로 BD = CD = BC ÷ 2 = {k} cm이고, AD = {h} cm는 △ABD·△ABC 모두의 높이가 된다.",
        sol1_fig=scene(pts, segs, marks={**marks, "eq": [[["A", "B"], ["A", "C"]], [["B", "D"], ["D", "C"]]]},
                       labels=bclab + [{"at": "D", "text": "{k} cm", "dx": 26, "dy": 14, "accent": True, "k": "lbl:bd"}]),
        sol1_anim=[[hl("right:D", keep=True)], [hl("eq:B-D", "eq:D-C", "lbl:bd", keep=True)], [hl("lbl:ad")]],
        sol2=[
            "AB = AC이고 AD ⊥ BC이므로 AD는 BC를 수직이등분한다: BD = CD = [[frac(1, 2)]] × {2*k} = {k}(cm)",
            "{STEP1}{v1}{STEP2}{v2}{STEP3}{v3}{STEP4}",
            "따라서 {Q}{eun(Q)} {ans_v}{U}",
        ],
        sol2_fig=steps([{"text": "BD = CD = {k} cm", "hint": "수선 = 수직이등분선"}, {"text": "{FORM1}{v1}{FORM2}{v2} = {ans_v}", "hint": "높이 AD = {h}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], []],
        sol_check="△ABD와 △ACD는 합동(RHS)이므로 넓이가 같고, 둘을 합친 △ABC의 넓이 [[frac(1, 2)]] × {2*k} × {h} = {k*h}(cm²)은 △ABD의 넓이 {k*h/2} cm²의 2배다. 답은 {ans_v}{U}다.",
        model_answer="AB = AC인 이등변삼각형에서 꼭짓점 A에서 밑변에 내린 수선은 밑변을 수직이등분하므로 BD = CD = {k} cm이다. {STEP1}{v1}{STEP2}{v2}{STEP3}{v3}{STEP4} 따라서 {Q}{eun(Q)} {ans_v}{U}다.",
        rubric=[
            {"element": "수직이등분", "points": 3, "criterion": "AD가 BC를 수직이등분하므로 BD = CD = {k} cm임을 밝혔다.", "partial": "BD = {k} cm라고만 쓰고 근거가 없으면 1점."},
            {"element": "넓이·길이 계산", "points": 2, "criterion": "{FORM1}{v1}{FORM2}{v2} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "식은 옳고 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v}{U}{eul(UA)} 답했다.", "partial": "단위가 없거나 다른 값을 답했으면 인정하지 않는다."},
        ],
    )


def iso_t4():
    # 접기: AB = AC, 점 A가 점 B에 겹치도록 DE를 접는 선으로 접음 → EA = EB, ∠EBA = ∠A. ∠EBC = t 가 주어짐
    rows = {"C": {"XQ": "C", "isC": 1, "XA": "C", "XF": "A", "XT": "B"},
            "A": {"XQ": "A", "isC": 0, "XA": "A", "XF": "B", "XT": "C"}}
    pts = {"A": [2, "{ay}"], "B": [0, 0], "C": [4, 0], "D": [1, "{ay/2}"], "E": ["{ex}", "{ey}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], {"a": "D", "b": "E", "dash": True}, ["B", "E"]]
    marks = {"eq": [[["A", "B"], ["A", "C"]], [["E", "A"], ["E", "B"]]], "arc": [arc("B", "E", "C", "{t}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-isosceles", 4, ISO,
        title="접은 이등변삼각형 종이 — 겹친 점이 만드는 이등변삼각형",
        skill="접는 선은 수직이등분선(EA = EB)이므로 ∠EBA = ∠A임을 읽고 방정식 세우기",
        variant_axis={"구하는 것": "∠C / ∠A", "∠EBC": "12°~54° (3의 배수)"},
        discriminates="접어서 겹친 두 점의 거리가 같다(EA = EB)는 것을 읽고, 꼭지각을 미지수로 두어 방정식을 세우는가",
        qtype="short", difficulty=4, pool_target=300, time_limit=110,
        prereq=["삼각형의 내각의 합 180°", "이등변삼각형의 두 밑각은 같다", "선분의 수직이등분선 위의 점"], ops=["각도", "방정식"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "t3", "values": {"int": [3, 18]}}],
        table={"key": "w", "rows": rows},
        derive={"t": "3*t3", "a": "60 - 2*t3", "b": "60 + t3", "ans_v": "(60 + t3)*isC + (60 - 2*t3)*(1 - isC)",
                "ay": "2*tan(pi*(60 + t3)/180)", "ex": "2 + 1/cos(pi*(60 - 2*t3)/180)", "ey": "2*tan(pi*(60 + t3)/180)*(1 - 0.5/cos(pi*(60 - 2*t3)/180))"},
        constraints=["ans_v != t"],
        cost_values=["t", "a", "b", "ans_v"],
        answer_var="ans_v",
        verify=["a + 2*b == 180", "b - a == t", "(isC == 1 and ans == b) or (isC == 0 and ans == a)"],
        question="다음 그림과 같이 [[seg(AB)]] = [[seg(AC)]]인 이등변삼각형 모양의 종이 ABC를, 점 A가 점 B에 겹치도록 선분 DE를 접는 선으로 하여 접었다. [[angle(EBC)]] = [[deg({t})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="점 A가 점 B에 겹치도록 접었으므로 접는 선 DE는 AB의 수직이등분선이고, 그 위의 점 E는 두 점 A, B에서 같은 거리에 있다: EA = EB. 그러면 △EAB도 이등변삼각형이라 ∠EBA = ∠A다. 한편 AB = AC이므로 ∠ABC = ∠C이고, ∠EBC = ∠ABC − ∠EBA다. 꼭지각 ∠A를 x로 두면 모든 각이 x로 표현된다.",
        sol1_fig=scene(pts, segs, marks=marks,
                       labels=[{"at": "B", "text": "{a}°", "dx": 30, "dy": -22, "accent": True, "k": "lbl:eba"}, {"at": "C", "text": "{b}°", "dx": -24, "dy": -10, "accent": True, "k": "lbl:c"}]),
        sol1_anim=[[hl("seg:D-E", keep=True)], [hl("eq:E-A", "eq:E-B", keep=True)], [hl("lbl:eba", keep=True)], [hl("lbl:c", "arc:given")]],
        sol2=[
            "접는 선 DE는 AB의 수직이등분선이므로 EA = EB, 따라서 ∠EBA = ∠A",
            "∠A = x라 하면 AB = AC이므로 ∠ABC = ∠C = (180° − x) ÷ 2 = 90° − [[frac(1, 2)]]x",
            "∠EBC = ∠ABC − ∠EBA = (90° − [[frac(1, 2)]]x) − x = 90° − [[frac(3, 2)]]x",
            "90° − [[frac(3, 2)]]x = {t}°이므로 [[frac(3, 2)]]x = {90 - t}°, x = {a}°",
            "∠A = {a}°, ∠C = 90° − [[frac(1, 2)]] × {a}° = {b}°이므로 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠EBA = ∠A = x", "hint": "EA = EB"}, {"text": "∠ABC = ∠C = 90° − [[frac(1, 2)]]x", "hint": "AB = AC"},
                        {"text": "∠EBC = 90° − [[frac(3, 2)]]x = {t}°", "hint": "∠ABC − ∠EBA"}, {"text": "x = {a}°, ∠C = {b}°", "hint": "[[frac(3, 2)]]x = {90 - t}°"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")], []],
        sol_check="∠A = {a}°, ∠B = ∠C = {b}°로 내각의 합이 180°이고, ∠EBA = {a}°, ∠EBC = {b}° − {a}° = {t}°로 조건에 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="접는 선 DE는 AB의 수직이등분선이므로 EA = EB이고 ∠EBA = ∠A이다. ∠A = x라 하면 ∠ABC = ∠C = 90° − [[frac(1, 2)]]x이고 ∠EBC = (90° − [[frac(1, 2)]]x) − x = 90° − [[frac(3, 2)]]x이다. 90° − [[frac(3, 2)]]x = {t}°에서 x = {a}°이므로 ∠A = {a}°, ∠C = {b}°이다. 따라서 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "접은 조건 읽기", "points": 3, "criterion": "EA = EB에서 ∠EBA = ∠A임을 밝혔다.", "partial": "EA = EB만 쓰고 각으로 옮기지 못했으면 1점."},
            {"element": "식 세우기", "points": 2, "criterion": "∠A = x로 두고 90° − [[frac(3, 2)]]x = {t}° 꼴의 방정식을 세웠다.", "partial": "∠ABC = 90° − [[frac(1, 2)]]x까지만 세웠으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": "x의 값만 구하고 묻는 각으로 옮기지 않았으면 인정하지 않는다."},
        ],
    )


def iso_t5():
    # AB = AC, ∠B의 이등분선과 ∠C의 외각의 이등분선의 교점 D → ∠D = ∠A / 2
    rows = {"D": {"GQ": "A", "XQ": "BDC", "isD": 1, "GA": "A", "GF": "B", "GT": "C", "XA": "D", "XF": "B", "XT": "C"},
            "A": {"GQ": "BDC", "XQ": "A", "isD": 0, "GA": "D", "GF": "B", "GT": "C", "XA": "A", "XF": "B", "XT": "C"}}
    pts = {"A": [2, "{ay}"], "B": [0, 0], "C": [4, 0], "D": ["{xd}", "{yd}"], "E": ["{xd + 1}", 0]}
    segs = [["A", "B"], ["A", "C"], ["B", "E"], ["B", "D"], ["C", "D"]]
    marks = {"eq": [[["A", "B"], ["A", "C"]]],
             "arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask"),
                     arc("B", "C", "D", "•", "arc:b1"), arc("B", "D", "A", "•", "arc:b2"), arc("C", "D", "E", "×", "arc:c1"), arc("C", "A", "D", "×", "arc:c2")]}
    return tpl("m2-2-isosceles", 5, ISO,
        title="밑각의 이등분선과 외각의 이등분선이 만나는 각 — ∠D = ∠A ÷ 2",
        skill="외각의 성질(한 외각 = 이웃하지 않는 두 내각의 합)을 두 번 써서 ∠D를 ∠A로 나타내기",
        variant_axis={"구하는 것": "∠D / ∠A", "∠A": "28°~100° (4의 배수)"},
        discriminates="△DBC에서 외각 ∠DCE = ∠DBC + ∠D를 세우고, 이등분된 각을 밑각의 절반으로 옮기는가",
        qtype="short", difficulty=4, pool_target=300, time_limit=120,
        prereq=["삼각형의 외각의 성질", "이등변삼각형의 두 밑각은 같다", "각의 이등분선"], ops=["각도", "방정식"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "a4", "values": {"int": [7, 25]}}],
        table={"key": "w", "rows": rows},
        derive={"a": "4*a4", "b": "90 - 2*a4", "hb": "45 - a4", "ext": "90 + 2*a4", "hext": "45 + a4", "d": "2*a4", "gv": "4*a4*isD + 2*a4*(1 - isD)", "ans_v": "2*a4*isD + 4*a4*(1 - isD)",
                "ay": "2*tan(pi*(90 - 2*a4)/180)", "tq": "tan(pi*(45 - a4)/180)", "xd": "4/(1 - tq*tq)", "yd": "4*tq/(1 - tq*tq)"},
        constraints=["ans_v != gv"],
        cost_values=["a", "b", "hb", "ext", "hext", "d", "ans_v"],
        answer_var="ans_v",
        verify=["a + 2*b == 180", "2*hb == b", "ext + b == 180", "2*hext == ext", "hext == hb + d", "(isD == 1 and ans == d) or (isD == 0 and ans == a)"],
        question="다음 그림에서 △ABC는 [[seg(AB)]] = [[seg(AC)]]인 이등변삼각형이고, 점 D는 [[angle(B)]]의 이등분선과 [[angle(C)]]의 외각 [[angle(ACE)]]의 이등분선의 교점이다. [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="밑각 ∠B = ∠C = {b}°이고 ∠C의 외각 ∠ACE = 180° − {b}° = {ext}°다. 이등분되었으니 ∠DBC = {hb}°, ∠DCE = {hext}°. △DBC에서 ∠DCE는 꼭짓점 C의 외각이므로 ∠DCE = ∠DBC + ∠BDC — 이 관계에서 ∠D가 나온다. 일반적으로 ∠D = ∠A ÷ 2다.",
        sol1_fig=scene(pts, segs, marks=marks,
                       labels=[{"at": "B", "text": "{hb}°", "dx": 34, "dy": -8, "accent": True, "k": "lbl:hb"}, {"at": "C", "text": "{hext}°", "dx": 28, "dy": -12, "accent": True, "k": "lbl:hext"}]),
        sol1_anim=[[hl("eq:A-B", "eq:A-C", keep=True)], [hl("arc:b1", "arc:b2", "lbl:hb", keep=True)], [hl("arc:c1", "arc:c2", "lbl:hext", keep=True)], [hl("arc:ask")]],
        sol2=[
            "AB = AC이므로 ∠ABC = ∠ACB = (180° − {a}°) ÷ 2 = {b}°",
            "∠ACE = 180° − ∠ACB = {ext}°이고, BD, CD가 각을 이등분하므로 ∠DBC = {hb}°, ∠DCE = {hext}°",
            "△DBC에서 외각 ∠DCE = ∠DBC + ∠BDC이므로 ∠BDC = {hext}° − {hb}° = {d}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠ABC = ∠ACB = {b}°", "hint": "(180° − ∠A) ÷ 2"}, {"text": "∠DBC = {hb}°, ∠DCE = {hext}°", "hint": "이등분: 절반씩"},
                        {"text": "∠BDC = {hext}° − {hb}° = {d}°", "hint": "외각 = 두 내각의 합", "marks": [{"on": "{d}°", "note": "= ∠A ÷ 2"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], []],
        sol_check="∠BDC = {d}°는 ∠A = {a}°의 절반이다. 실제로 ∠ACE = ∠A + ∠B이고 절반씩 취하면 ∠DCE = [[frac(1, 2)]]∠A + ∠DBC이므로 ∠D = ∠DCE − ∠DBC = [[frac(1, 2)]]∠A가 되어 어떤 이등변삼각형에서도 성립한다. 답은 [[deg({ans_v})]]다.",
        model_answer="AB = AC이므로 ∠ABC = ∠ACB = {b}°이고, ∠ACE = 180° − {b}° = {ext}°이다. BD, CD가 각각 ∠B, ∠ACE를 이등분하므로 ∠DBC = {hb}°, ∠DCE = {hext}°이다. △DBC에서 외각의 성질에 의해 ∠DCE = ∠DBC + ∠BDC이므로 ∠BDC = {hext}° − {hb}° = {d}°이다. 따라서 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "밑각·외각 구하기", "points": 3, "criterion": "밑각 {b}°와 외각 ∠ACE = {ext}°를 구하고 이등분한 {hb}°, {hext}°를 썼다.", "partial": "밑각까지만 옳으면 1점."},
            {"element": "외각의 성질", "points": 2, "criterion": "△DBC에서 ∠DCE = ∠DBC + ∠BDC를 세웠다.", "partial": "내각의 합으로 돌아가 풀었더라도 옳으면 인정한다. 식이 틀렸으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": "∠A와 ∠D를 바꿔 답했으면 인정하지 않는다."},
        ],
    )


ISO_SEED = {
    "seed_id": "m2-2-isosceles", "category": "도형",
    "title": "이등변삼각형의 성질 — 꼭지각·밑각, 연쇄 각, 수선과 넓이, 접기, 외각 이등분선",
    "unit_id": "m2-2", "concept_ids": ["m2-2-01"],
    "schema_id": SCHEMA_ISO, "schema_name": "이등변삼각형 두 밑각 크기 / 성질의 활용(연쇄·접기·외각 이등분선)",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 5.1)을 참고해 새로 씀. 좌표는 AB = AC = 1(또는 BC = 1)로 두고 각에서 직접 계산 — 접기(t4)의 E는 EA = EB, 외각 이등분선(t5)의 D는 두 이등분선의 교점을 tan 으로 푼 값. t2는 (주어진 각 × 구하는 각) 합성 키.",
    "geometry": True,
    "templates": [iso_t1(), iso_t2(), iso_t3(), iso_t4(), iso_t5()],
}



# ═══════════════════════════════════════════════════════════════════ 2. 삼각형의 외심
CIRC = dict(prereq=["외심: 세 변의 수직이등분선의 교점", "외심에서 세 꼭짓점까지의 거리는 같다 (OA = OB = OC)", "이등변삼각형의 두 밑각은 같다"],
            ops=["각도"], tags=["외심", "외접원"])
R0 = 3   # 외접원 반지름(그림 단위)


def circ_t1():
    # 주어진 꼭짓점 P(A·B·C)와 방향(꼭짓점각 → 중심각 / 중심각 → 꼭짓점각)을 행으로 — 같은 성질을 세 꼭짓점에 돌려 적용.
    # 그림만 다른 s축은 문면 중복(DUP)으로 탈락하므로 행마다 모양 s를 하나씩 붙였다. P는 원 위쪽, Q1·Q2는 아래쪽에 놓는다.
    def row(P, Q1, Q2, fwd, s, ldx, ldy):
        OQ = f"{Q1}O{Q2}"
        slot = {L: ("P" if L == P else "Q1" if L == Q1 else "Q2") for L in "ABC"}
        base = {"P": P, "Q1": Q1, "Q2": Q2, "OQ": OQ, "s": s, "LDX": ldx, "LDY": ldy,
                **{f"{L.lower()}{k}": int(slot[L] == k) for L in "ABC" for k in ("P", "Q1", "Q2")}}
        if fwd:
            return {**base, "GQ": P, "XQ": OQ, "isB": 1, "GA": P, "GF": Q1, "GT": Q2, "XA": "O", "XF": Q1, "XT": Q2,
                    "F1": f"∠{OQ} = 2∠{P} = 2 × ", "F2": "°", "LAW": "중심각은 2배"}
        return {**base, "GQ": OQ, "XQ": P, "isB": 0, "GA": "O", "GF": Q1, "GT": Q2, "XA": P, "XF": Q1, "XT": Q2,
                "F1": f"∠{P} = [[frac(1, 2)]]∠{OQ} = [[frac(1, 2)]] × ", "F2": "°", "LAW": f"∠{P}는 절반"}
    rows = {"A>BOC": row("A", "B", "C", True, 0, 0, 24), "BOC>A": row("A", "B", "C", False, 15, 0, 34),
            "B>AOC": row("B", "A", "C", True, -15, 0, 24), "AOC>B": row("B", "A", "C", False, 0, 0, 34),
            "C>AOB": row("C", "A", "B", True, 15, 0, 24), "AOB>C": row("C", "A", "B", False, -15, 0, 34)}
    # 자리 P = (0, R0), Q1 = (bx, by), Q2 = (cx, cy) — 글자는 행의 자리 플래그(aP, aQ1, …)로 배정
    pts = {"A": ["{bx*aQ1 + cx*aQ2}", "{3*aP + by*aQ1 + cy*aQ2}"], "B": ["{bx*bQ1 + cx*bQ2}", "{3*bP + by*bQ1 + cy*bQ2}"],
           "C": ["{bx*cQ1 + cx*cQ2}", "{3*cP + by*cQ1 + cy*cQ2}"], "O": [0, 0]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["O", "{Q1}"], ["O", "{Q2}"]]
    circles = [{"c": "O", "r": R0}]
    marks = {"arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-circumcenter", 1, CIRC,
        title="외심 — ∠BOC = 2∠A",
        skill="외심 O에 대해 ∠BOC = 2∠A임을 쓰기 (OA = OB = OC인 두 이등변삼각형의 외각; 세 꼭짓점에 돌려 적용)",
        variant_axis={"주어진 것": "꼭짓점각 / 중심각", "꼭짓점": "A·B·C", "각": "20°~80°"},
        discriminates="OA = OB = OC에서 두 이등변삼각형을 읽고 중심각 = 2 × 꼭짓점각으로 옮기는가(2배·절반 방향)",
        qtype="short", difficulty=2, pool_target=300, time_limit=70,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "a", "values": {"int": [20, 80]}}],
        table={"key": "w", "rows": rows},
        derive={"a2": "2*a", "gv": "a*isB + 2*a*(1 - isB)", "ans_v": "2*a*isB + a*(1 - isB)", "hb": "90 - a",
                "bx": "3*cos(pi*(270 - a - s)/180)", "by": "3*sin(pi*(270 - a - s)/180)", "cx": "3*cos(pi*(270 + a - s)/180)", "cy": "3*sin(pi*(270 + a - s)/180)"},
        constraints=["ans_v != gv"],
        cost_values=["a", "a2", "ans_v"],
        answer_var="ans_v",
        verify=["a2 == 2*a", "(isB == 1 and ans == a2) or (isB == 0 and ans == a)"],
        question="다음 그림에서 점 O는 △ABC의 외심이다. [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks, circles=circles),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="점 O는 외심이므로 OA = OB = OC다. 그러면 △O{P}{Q1}, △O{P}{Q2}는 이등변삼각형이라 ∠O{P}{Q1} = ∠O{Q1}{P}, ∠O{P}{Q2} = ∠O{Q2}{P}이고, 각각의 외각을 모으면 ∠{OQ} = 2∠O{P}{Q1} + 2∠O{P}{Q2} = 2∠{P}가 된다. 즉 외심을 중심으로 한 각 ∠{OQ}는 ∠{P}의 2배다.",
        sol1_fig=scene(pts, segs + [{"a": "O", "b": "{P}", "dash": True}], marks={"eq": [[["O", "A"], ["O", "B"], ["O", "C"]]], "arc": marks["arc"]}, circles=circles,
                       labels=[{"at": "{XA}", "text": "{ans_v}°", "dx": "{LDX}", "dy": "{LDY}", "accent": True, "k": "lbl:ans"}]),
        sol1_anim=[[hl("eq:O-A", "eq:O-B", "eq:O-C", "seg:O-{P}", keep=True)], [hl("arc:given", keep=True)], [hl("lbl:ans", "arc:ask")]],
        sol2=[
            "점 O가 외심이므로 OA = OB = OC → △O{P}{Q1}, △O{P}{Q2}는 이등변삼각형",
            "∠O{P}{Q1} = ∠O{Q1}{P}, ∠O{P}{Q2} = ∠O{Q2}{P}이므로 외각의 성질에서 ∠{OQ} = 2(∠O{P}{Q1} + ∠O{P}{Q2}) = 2∠{P}",
            "{F1}{gv}{F2} = {ans_v}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "OA = OB = OC", "hint": "외심"}, {"text": "∠{OQ} = 2∠{P}", "hint": "두 이등변삼각형의 외각"}, {"text": "{F1}{gv}{F2} = {ans_v}°", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="△O{Q1}{Q2}는 O{Q1} = O{Q2}인 이등변삼각형이므로 ∠O{Q1}{Q2} = ∠O{Q2}{Q1} = (180° − {a2}°) ÷ 2 = {hb}°가 되어 ∠{OQ} = {a2}°와 어긋나지 않는다. 답은 [[deg({ans_v})]]다.",
        model_answer="점 O는 △ABC의 외심이므로 OA = OB = OC이고, △O{P}{Q1}와 △O{P}{Q2}는 이등변삼각형이다. 외각의 성질에서 ∠{OQ} = 2∠{P}이므로 {F1}{gv}{F2} = {ans_v}°이다. 따라서 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "외심의 성질", "points": 3, "criterion": "OA = OB = OC임을 밝히고 ∠{OQ} = 2∠{P}의 근거(이등변삼각형·외각)를 썼다.", "partial": "∠{OQ} = 2∠{P}만 쓰고 근거가 없으면 1점."},
            {"element": "각의 계산", "points": 2, "criterion": "{F1}{gv}{F2} = {ans_v}°를 계산했다.", "partial": "2배·절반을 거꾸로 했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": ""},
        ],
    )


def circ_t2():
    rows = {"OAB": {"XQ": "OAB", "G1": "OBC", "G2": "OCA", "uA": 1, "uB": 0, "uC": 0, "XA": "A", "XF": "O", "XT": "B", "G1A": "B", "G1F": "O", "G1T": "C", "G2A": "C", "G2F": "O", "G2T": "A"},
            "OBC": {"XQ": "OBC", "G1": "OAB", "G2": "OCA", "uA": 0, "uB": 1, "uC": 0, "XA": "B", "XF": "O", "XT": "C", "G1A": "A", "G1F": "O", "G1T": "B", "G2A": "C", "G2F": "O", "G2T": "A"},
            "OCA": {"XQ": "OCA", "G1": "OAB", "G2": "OBC", "uA": 0, "uB": 0, "uC": 1, "XA": "C", "XF": "O", "XT": "A", "G1A": "A", "G1F": "O", "G1T": "B", "G2A": "B", "G2F": "O", "G2T": "C"}}
    pts = {"A": [0, R0], "B": ["{bx}", "{by}"], "C": ["{cx}", "{cy}"], "O": [0, 0]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["O", "A"], ["O", "B"], ["O", "C"]]
    circles = [{"c": "O", "r": R0}]
    marks = {"arc": [arc("{G1A}", "{G1F}", "{G1T}", "{g1}°", "arc:g1"), arc("{G2A}", "{G2F}", "{G2T}", "{g2}°", "arc:g2"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-circumcenter", 2, CIRC,
        title="외심 — ∠OAB + ∠OBC + ∠OCA = 90°",
        skill="OA = OB = OC인 세 이등변삼각형의 밑각을 모아 세 각의 합이 90°임을 쓰기",
        variant_axis={"구하는 것": "∠OAB / ∠OBC / ∠OCA", "각": "10°~60°"},
        discriminates="세 이등변삼각형의 밑각이 두 번씩 나타나 2(x + y + z) = 180°임을 세우는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "p", "values": {"int": [10, 60]}}, {"name": "q", "values": {"int": [10, 60]}}],
        table={"key": "w", "rows": rows},
        derive={"z": "90 - p - q", "g1": "p*(1 - uA) + q*uA", "g2": "z*(1 - uC) + q*uC", "ans_v": "p*uA + q*uB + z*uC",
                "bx": "3*cos(pi*(270 - 2*p)/180)", "by": "3*sin(pi*(270 - 2*p)/180)", "cx": "3*cos(pi*(90 - 2*p - 2*q)/180)", "cy": "3*sin(pi*(90 - 2*p - 2*q)/180)"},
        constraints=["z >= 10", "ans_v != g1", "ans_v != g2", "g1 != g2"],
        cost_values=["p", "q", "z", "ans_v"],
        answer_var="ans_v",
        verify=["p + q + z == 90", "g1 + g2 + ans == 90"],
        question="다음 그림에서 점 O는 △ABC의 외심이다. [[angle({G1})]] = [[deg({g1})]], [[angle({G2})]] = [[deg({g2})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks, circles=circles),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="점 O는 외심이므로 OA = OB = OC이고, △OAB, △OBC, △OCA는 모두 이등변삼각형이다. 그래서 ∠OAB = ∠OBA, ∠OBC = ∠OCB, ∠OCA = ∠OAC — 세 각 ∠OAB, ∠OBC, ∠OCA가 △ABC의 세 내각 안에 두 번씩 들어 있으므로 그 합은 180° ÷ 2 = 90°다.",
        sol1_fig=scene(pts, segs, marks={"eq": [[["O", "A"], ["O", "B"], ["O", "C"]]], "arc": marks["arc"] + [arc("B", "A", "O", "{p}°", "arc:ba"), arc("C", "B", "O", "{q}°", "arc:cb"), arc("A", "C", "O", "{z}°", "arc:ac")]}, circles=circles),
        sol1_anim=[[hl("eq:O-A", "eq:O-B", "eq:O-C", keep=True)], [hl("arc:g1", "arc:ba", "arc:g2", "arc:cb", "arc:ac", keep=True)], [hl("arc:ask")]],
        sol2=[
            "OA = OB = OC이므로 ∠OAB = ∠OBA, ∠OBC = ∠OCB, ∠OCA = ∠OAC",
            "△ABC의 내각의 합: 2(∠OAB + ∠OBC + ∠OCA) = 180° → ∠OAB + ∠OBC + ∠OCA = 90°",
            "∠{XQ} = 90° − {g1}° − {g2}° = {ans_v}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠OAB = ∠OBA, ∠OBC = ∠OCB, ∠OCA = ∠OAC", "hint": "OA = OB = OC"}, {"text": "∠OAB + ∠OBC + ∠OCA = 90°", "hint": "내각의 합 180°의 절반"},
                        {"text": "∠{XQ} = 90° − {g1}° − {g2}° = {ans_v}°"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)], []],
        sol_check="세 각 {g1}° + {g2}° + {ans_v}° = 90°이고, △ABC의 세 내각은 각각 두 각의 합(∠A = ∠OAB + ∠OCA 등)이 되어 모두 더하면 180°다. 답은 [[deg({ans_v})]]다.",
        model_answer="점 O가 외심이므로 OA = OB = OC이고 ∠OAB = ∠OBA, ∠OBC = ∠OCB, ∠OCA = ∠OAC이다. △ABC의 내각의 합에서 2(∠OAB + ∠OBC + ∠OCA) = 180°이므로 ∠OAB + ∠OBC + ∠OCA = 90°이다. 따라서 ∠{XQ} = 90° − {g1}° − {g2}° = {ans_v}°다.",
        rubric=[
            {"element": "세 이등변삼각형", "points": 3, "criterion": "OA = OB = OC에서 세 쌍의 밑각이 같음을 밝혔다.", "partial": "한 쌍만 밝혔으면 1점."},
            {"element": "합이 90°", "points": 2, "criterion": "2(∠OAB + ∠OBC + ∠OCA) = 180°에서 세 각의 합이 90°임을 세웠다.", "partial": "합이 90°임을 근거 없이 썼으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": ""},
        ],
    )


def circ_t3():
    # ∠A = 90° 직각삼각형: 외심 O = BC의 중점, 반지름 = BC/2. BC = 2r, AC = m
    rows = {"r": {"Q": "△ABC의 외접원의 반지름의 길이", "isR": 1, "U": " cm", "F1": "R = ", "F2": " ÷ ", "LAW": "빗변의 절반"},
            "aoc": {"Q": "△AOC의 둘레의 길이", "isR": 0, "U": " cm", "F1": "OA + OC + AC = 2 × ", "F2": " + ", "LAW": "OA = OC = R"}}
    pts = {"A": ["{ax}", "{ay}"], "B": ["{-r}", 0], "C": ["{r}", 0], "O": [0, 0]}
    segs = [["A", "B"], ["B", "C"], {"a": "C", "b": "A", "label": "{m} cm"}, ["O", "A"]]
    circles = [{"c": "O", "r": "{r}"}]
    marks = {"right": [["B", "A", "C"]]}
    bclab = [{"at": ["{-r/2}", 0], "text": "{2*r} cm", "dx": 0, "dy": 15, "k": "lbl:bc"}]
    return tpl("m2-2-circumcenter", 3, CIRC,
        title="직각삼각형의 외심 — 빗변의 중점, 반지름 = 빗변 ÷ 2",
        skill="직각삼각형의 외심은 빗변의 중점이므로 외접원의 반지름은 빗변의 절반임을 쓰기",
        variant_axis={"구하는 것": "외접원의 반지름 / △AOC의 둘레", "BC": "6~24", "AC": "3~20"},
        discriminates="외심이 빗변의 중점임을 알고 OA = OB = OC = BC ÷ 2로 옮기는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70, process="절차수행",
        prereq=["직각삼각형의 외심은 빗변의 중점", "외심에서 세 꼭짓점까지의 거리는 같다"], ops=["사칙"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "r", "values": {"int": [3, 12]}}, {"name": "m", "values": {"int": [3, 20]}}],
        table={"key": "w", "rows": rows},
        derive={"d": "2*r", "per": "2*r + m", "ans_v": "r*isR + (2*r + m)*(1 - isR)", "v1": "2*r*isR + r*(1 - isR)", "v2": "2*isR + m*(1 - isR)",
                "ax": "r - m*m/(2*r)", "ay": "sqrt(abs(r*r - (r - m*m/(2*r))*(r - m*m/(2*r))))"},
        constraints=["10*m >= 7*r", "10*m <= 18*r", "m != r", "m != 2*r"],
        cost_values=["d", "m", "r", "ans_v"],
        answer_var="ans_v",
        verify=["d == 2*r", "(isR == 1 and ans == r) or (isR == 0 and ans == 2*r + m)"],
        question="다음 그림과 같이 [[angle(A)]] = [[deg(90)]]인 직각삼각형 ABC에서 점 O는 △ABC의 외심이다. [[seg(BC)]] = {2*r} cm, [[seg(AC)]] = {m} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks, circles=circles, labels=bclab),
        answer="{ans_v}", answer_alt=["{ans_v}{U}"],
        sol1="직각삼각형의 외심은 빗변의 중점이다. 빗변 BC가 외접원의 지름이므로 반지름은 BC ÷ 2 = {r} cm이고, 외심에서 세 꼭짓점까지의 거리가 모두 같아 OA = OB = OC = {r} cm다. AC = {m} cm는 반지름과 무관하다.",
        sol1_fig=scene(pts, segs, marks={"right": [["B", "A", "C"]], "eq": [[["O", "A"], ["O", "B"], ["O", "C"]]]}, circles=circles,
                       labels=bclab + [{"at": "O", "text": "R = {r}", "dx": 22, "dy": -10, "accent": True, "k": "lbl:r"}]),
        sol1_anim=[[hl("right:A", keep=True)], [hl("circle:0", "lbl:bc", keep=True)], [hl("eq:O-A", "eq:O-B", "eq:O-C", "lbl:r")]],
        sol2=[
            "∠A = 90°이므로 △ABC의 외심 O는 빗변 BC의 중점이고, 외접원의 지름은 BC = {2*r} cm",
            "외접원의 반지름 R = [[frac(1, 2)]] × {2*r} = {r}(cm), 따라서 OA = OB = OC = {r} cm",
            "{Q}: {F1}{v1}{F2}{v2} = {ans_v}(cm)",
        ],
        sol2_fig=steps([{"text": "O = BC의 중점, 지름 = {2*r}", "hint": "직각삼각형의 외심"}, {"text": "R = {2*r} ÷ 2 = {r}", "hint": "반지름 = 빗변 ÷ 2"}, {"text": "{Q}: {ans_v}{U}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")]],
        sol_check="OA = OB = OC = {r} cm로 세 꼭짓점이 모두 중심 O에서 같은 거리에 있고, 지름 {2*r} cm는 빗변 BC의 길이와 같다. 답은 {ans_v}{U}다.",
        model_answer="∠A = 90°인 직각삼각형의 외심은 빗변 BC의 중점이므로 외접원의 반지름은 BC ÷ 2 = {r} cm이고 OA = OB = OC = {r} cm이다. 따라서 {Q}{eun(Q)} {ans_v}{U}다.",
        rubric=[
            {"element": "빗변의 중점", "points": 3, "criterion": "직각삼각형의 외심이 빗변의 중점이므로 반지름이 BC ÷ 2 = {r} cm임을 밝혔다.", "partial": "반지름 {r} cm만 쓰고 근거가 없으면 1점."},
            {"element": "길이 계산", "points": 2, "criterion": "OA = OB = OC = {r} cm를 써서 {Q}{eul(Q)} 계산했다.", "partial": "AC를 반지름으로 잘못 썼으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans_v}{U}{eul(U)} 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def circ_t4():
    # 직각인 꼭짓점을 A·B·C로 돌린다(빗변 이름이 문면에 드러나므로 DUP가 아니다). 행마다 모양 s를 하나씩 붙였다.
    rows = {"A": {"RA": "A", "H1": "B", "H2": "C", "HY": "BC", "vA": 1, "vB": 0, "vC": 0, "s": 4, "isS": 1, "Q": "△ABC의 외접원의 넓이", "U": " cm²", "UA": "cm²", "F1": "π × ", "F2": "²", "LAW": "πR²"},
            "B": {"RA": "B", "H1": "C", "H2": "A", "HY": "CA", "vA": 0, "vB": 1, "vC": 0, "s": 6, "isS": 1, "Q": "△ABC의 외접원의 넓이", "U": " cm²", "UA": "cm²", "F1": "π × ", "F2": "²", "LAW": "πR²"},
            "C": {"RA": "C", "H1": "A", "H2": "B", "HY": "AB", "vA": 0, "vB": 0, "vC": 1, "s": 8, "isS": 1, "Q": "△ABC의 외접원의 넓이", "U": " cm²", "UA": "cm²", "F1": "π × ", "F2": "²", "LAW": "πR²"}}
    # 빗변 H1H2는 항상 x축 위 (−r, 0)–(r, 0), 직각 꼭짓점은 원 위 (ax, ay) — 이름만 행에 따라 돈다
    pts = {"A": ["{ax*vA + r*vB - r*vC}", "{ay*vA}"], "B": ["{-r*vA + ax*vB + r*vC}", "{ay*vB}"], "C": ["{r*vA - r*vB + ax*vC}", "{ay*vC}"]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"]]
    circles = [{"c": [0, 0], "r": "{r}"}]
    marks = {"right": [["{H1}", "{RA}", "{H2}"]]}
    bclab = [{"at": ["{-r/2}", 0], "text": "{2*r} cm", "dx": 0, "dy": 15, "k": "lbl:bc"}]
    return tpl("m2-2-circumcenter", 4, CIRC,
        title="직각삼각형의 외접원의 넓이",
        skill="빗변이 지름임을 써서 외접원의 넓이 πR² 구하기 (둘레 2πR은 지름과 계수가 같아 R-05에 걸리므로 넓이만)",
        variant_axis={"구하는 것": "넓이", "빗변": "6~28", "직각 꼭짓점": "A·B·C"},
        discriminates="지름과 반지름을 구별해 R = (빗변) ÷ 2를 쓰는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70, process="절차수행",
        prereq=["직각삼각형의 외심은 빗변의 중점", "원의 넓이 πr²"], ops=["넓이", "사칙"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "r", "values": {"int": [3, 14]}}],
        table={"key": "w", "rows": rows},
        derive={"d": "2*r", "ans_v": "r*r*isS + 2*r*(1 - isS)", "ax": "r*(1 - s*s/50)", "ay": "sqrt(r*r - ax*ax)"},
        constraints=[],
        cost_values=["d", "r", "ans_v"],
        answer_var="ans_v",
        verify=["(isS == 1 and ans == r*r) or (isS == 0 and ans == 2*r)"],
        question="다음 그림과 같이 [[angle({RA})]] = [[deg(90)]]인 직각삼각형 ABC에서 [[seg({HY})]] = {2*r} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks, circles=circles, labels=bclab),
        answer="[[{ans_v}*pi]]", answer_alt=["[[{ans_v}*pi]]{U}", "{ans_v}π{U}"],
        sol1="직각삼각형의 외심은 빗변의 중점이므로 빗변 {HY}는 외접원의 지름이다. 지름이 {2*r} cm이니 반지름은 {r} cm — 원의 넓이는 π × (반지름)²으로 구한다.",
        sol1_fig=scene({**pts, "O": [0, 0]}, segs + [["O", "{RA}"]], marks={"right": [["{H1}", "{RA}", "{H2}"]], "eq": [[["O", "A"], ["O", "B"], ["O", "C"]]]}, circles=[{"c": "O", "r": "{r}"}],
                       labels=bclab + [{"at": "O", "text": "R = {r}", "dx": 22, "dy": -10, "accent": True, "k": "lbl:r"}]),
        sol1_anim=[[hl("right:{RA}", keep=True)], [hl("lbl:bc", "circle:0", keep=True)], [hl("eq:O-A", "eq:O-B", "eq:O-C", "lbl:r")]],
        sol2=[
            "∠{RA} = 90°이므로 외심은 빗변 {HY}의 중점이고, {HY} = {2*r} cm가 외접원의 지름",
            "외접원의 반지름 R = {2*r} ÷ 2 = {r}(cm)",
            "{Q}: {F1}{r}{F2} = {ans_v}π({UA})",
        ],
        sol2_fig=steps([{"text": "지름 = {HY} = {2*r}", "hint": "직각삼각형의 외심 = 빗변의 중점"}, {"text": "R = {r}", "hint": "지름 ÷ 2"}, {"text": "{F1}{r}{F2} = {ans_v}π", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")]],
        sol_check="반지름 {r} cm인 원의 넓이는 {r*r}π cm², 둘레는 {2*r}π cm다. 지름 {2*r} cm를 반지름으로 쓰면 4배·2배로 어긋난다. 답은 [[{ans_v}*pi]]{U}다.",
        model_answer="∠{RA} = 90°인 직각삼각형의 외심은 빗변의 중점이므로 {HY} = {2*r} cm는 외접원의 지름이고 반지름은 {r} cm이다. 따라서 {Q}{eun(Q)} {F1}{r}{F2} = {ans_v}π({UA})이다.",
        rubric=[
            {"element": "지름 = 빗변", "points": 3, "criterion": "외심이 빗변의 중점이므로 {HY}가 지름, 반지름이 {r} cm임을 밝혔다.", "partial": "반지름 {r} cm만 쓰고 근거가 없으면 1점."},
            {"element": "원의 공식", "points": 2, "criterion": "{LAW}에 R = {r}{eul(r)} 넣어 {ans_v}π{eul(UA)} 계산했다.", "partial": "지름을 반지름으로 썼으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans_v}π{U}{eul(UA)} 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


def circ_t5():
    # △OAB 둘레 P, AB = c → R = (P − c)/2 → 외접원 둘레·넓이
    rows = {"circ": {"Q": "△ABC의 외접원의 둘레의 길이", "isS": 0, "U": " cm", "UA": "cm", "F1": "2π × ", "F2": "", "LAW": "2πR"},
            "area": {"Q": "△ABC의 외접원의 넓이", "isS": 1, "U": " cm²", "UA": "cm²", "F1": "π × ", "F2": "²", "LAW": "πR²"}}
    pts = {"A": ["{-c/2}", "{hh}"], "B": ["{c/2}", "{hh}"], "C": ["{cx}", "{cy}"], "O": [0, 0]}
    segs = [{"a": "A", "b": "B", "label": "{c} cm"}, ["B", "C"], ["C", "A"], ["O", "A"], ["O", "B"]]
    circles = [{"c": "O", "r": "{r}"}]
    return tpl("m2-2-circumcenter", 5, CIRC,
        title="△OAB의 둘레 → 외접원의 둘레·넓이",
        skill="OA = OB = R이므로 △OAB의 둘레 = 2R + AB에서 R을 구하고 원의 둘레·넓이로 옮기기",
        variant_axis={"구하는 것": "외접원의 둘레 / 넓이", "R": "3~12", "AB": "3~20"},
        discriminates="△OAB의 둘레에서 AB를 빼고 2로 나누어 R을 얻는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90,
        prereq=["외심에서 세 꼭짓점까지의 거리는 같다", "원의 넓이 πr²·둘레 2πr"], ops=["방정식", "넓이"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "r", "values": {"int": [3, 12]}}, {"name": "c", "values": {"int": [3, 20]}}, {"name": "s", "values": {"in": [-8, 0, 8]}}],
        table={"key": "w", "rows": rows},
        derive={"P": "2*r + c", "ans_v": "r*r*isS + 2*r*(1 - isS)", "hh": "sqrt(abs(r*r - c*c/4))", "cx": "r*cos(pi*(270 + s)/180)", "cy": "r*sin(pi*(270 + s)/180)"},
        constraints=["5*c >= 3*r", "5*c <= 9*r", "c != r", "c != 2*r"],
        cost_values=["P", "c", "r", "ans_v"],
        answer_var="ans_v",
        verify=["P == 2*r + c", "(isS == 1 and ans == r*r) or (isS == 0 and ans == 2*r)"],
        question="다음 그림에서 점 O는 △ABC의 외심이다. [[seg(AB)]] = {c} cm이고 △OAB의 둘레의 길이가 {P} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, circles=circles),
        answer="[[{ans_v}*pi]]", answer_alt=["[[{ans_v}*pi]]{U}", "{ans_v}π{U}"],
        sol1="외심 O에서 세 꼭짓점까지의 거리는 외접원의 반지름 R로 모두 같다: OA = OB = R. 그러므로 △OAB의 둘레 = OA + OB + AB = 2R + {c}이고, 여기서 R이 나온다. 외접원의 둘레는 2πR, 넓이는 πR²다.",
        sol1_fig=scene(pts, segs + [{"a": "O", "b": "C", "dash": True}], marks={"eq": [[["O", "A"], ["O", "B"], ["O", "C"]]]}, circles=circles,
                       labels=[{"at": "O", "text": "R", "dx": -22, "dy": -6, "accent": True, "k": "lbl:r"}]),
        sol1_anim=[[hl("eq:O-A", "eq:O-B", "eq:O-C", "lbl:r", keep=True)], [hl("seg:O-A", "seg:O-B", "seg:A-B", "seglbl:A-B")]],
        sol2=[
            "외접원의 반지름을 R cm라 하면 OA = OB = R (외심의 성질)",
            "△OAB의 둘레: R + R + {c} = {P} → 2R = {2*r}, R = {r}",
            "{Q}: {F1}{r}{F2} = {ans_v}π({UA})",
        ],
        sol2_fig=steps([{"text": "OA = OB = R", "hint": "외심"}, {"text": "2R + {c} = {P} → R = {r}", "hint": "△OAB의 둘레"}, {"text": "{F1}{r}{F2} = {ans_v}π", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")]],
        sol_check="R = {r}이면 △OAB의 둘레는 {r} + {r} + {c} = {P}(cm)로 조건과 맞는다. 답은 [[{ans_v}*pi]]{U}다.",
        model_answer="점 O는 외심이므로 OA = OB = R(외접원의 반지름)이다. △OAB의 둘레가 {P} cm이므로 2R + {c} = {P}, R = {r}이다. 따라서 {Q}{eun(Q)} {F1}{r}{F2} = {ans_v}π({UA})이다.",
        rubric=[
            {"element": "반지름 세우기", "points": 3, "criterion": "OA = OB = R로 두고 2R + {c} = {P}를 세웠다.", "partial": "OA = OB만 쓰고 식을 세우지 못했으면 1점."},
            {"element": "R 구하기", "points": 2, "criterion": "R = {r}{eul(r)} 구했다.", "partial": "AB를 빼지 않고 {P} ÷ 2로 했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans_v}π{U}{eul(UA)} 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


RATIO_C = {}
for _p, _q in [(1, 2), (2, 1), (4, 5), (5, 4), (1, 5), (5, 1), (2, 7), (7, 2), (1, 8), (8, 1), (7, 11), (11, 7), (13, 17), (17, 13), (7, 23), (23, 7),
               (4, 11), (11, 4), (2, 3), (3, 2), (1, 4), (4, 1), (3, 7), (7, 3), (1, 9), (9, 1), (5, 13), (13, 5), (11, 19), (19, 11), (7, 8), (8, 7), (4, 5), (5, 4)]:
    if (180 * _p) % (_p + _q) == 0 and (90 * _p) % (_p + _q) == 0:
        RATIO_C[f"{_p}-{_q}"] = {"p": _p, "q": _q, "aob": 180 * _p // (_p + _q), "aoc": 180 * _q // (_p + _q)}


def circ_t6():
    rows = {"C": {"XQ": "C", "isC": 1, "XA": "C", "XF": "A", "XT": "B"}, "B": {"XQ": "B", "isC": 0, "XA": "B", "XF": "A", "XT": "C"}}
    pts = {"A": ["{ax}", "{ay}"], "B": [-3, 0], "C": [3, 0], "O": [0, 0]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["O", "A"]]
    marks = {"right": [["B", "A", "C"]], "arc": [arc("O", "A", "B", None, "arc:aob"), arc("O", "C", "A", None, "arc:aoc"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-circumcenter", 6, CIRC,
        title="직각삼각형의 외심 — ∠AOB : ∠AOC = p : q → 예각",
        skill="OA = OC인 이등변삼각형의 외각 ∠AOB = 2∠C를 써서 비로 나뉜 각을 예각으로 옮기기",
        variant_axis={"구하는 것": "∠C / ∠B", "비": "정수 답이 되는 17쌍"},
        discriminates="∠AOB가 △AOC의 외각(= 2∠C)임을 읽어 절반을 취하는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "pr", "values": {"in": list(RATIO_C)}}],
        table=[{"key": "w", "rows": rows}, {"key": "pr", "rows": RATIO_C}],
        derive={"cv": "aob/2", "bv": "90 - aob/2", "ans_v": "aob/2*isC + (90 - aob/2)*(1 - isC)", "ax": "-3*cos(pi*aob/180)", "ay": "3*sin(pi*aob/180)"},
        constraints=["aob != 90", "cv == floor(cv)"],
        cost_values=["p", "q", "aob", "aoc", "ans_v"],
        answer_var="ans_v",
        verify=["aob + aoc == 180", "aob*q == aoc*p", "(isC == 1 and 2*ans == aob) or (isC == 0 and 2*ans == aoc)"],
        question="다음 그림에서 △ABC는 [[angle(A)]] = [[deg(90)]]인 직각삼각형이고, 점 O는 [[seg(BC)]]의 중점이다. [[angle(AOB)]] : [[angle(AOC)]] = {p} : {q}일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(pts, segs, marks=marks),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="직각삼각형에서 빗변의 중점 O는 외심이므로 OA = OB = OC다. 그러면 △OAC는 OA = OC인 이등변삼각형이라 ∠OAC = ∠OCA이고, ∠AOB는 △OAC의 외각이므로 ∠AOB = 2∠C다. 마찬가지로 ∠AOC = 2∠B. ∠AOB + ∠AOC = 180°(평각)를 {p} : {q}로 나눈다.",
        sol1_fig=scene(pts, segs, marks={**marks, "eq": [[["O", "A"], ["O", "B"], ["O", "C"]]]},
                       labels=[{"at": "O", "text": "{aob}°", "dx": -22, "dy": -12, "accent": True, "k": "lbl:aob"}, {"at": "O", "text": "{aoc}°", "dx": 22, "dy": -12, "accent": True, "k": "lbl:aoc"}]),
        sol1_anim=[[hl("eq:O-A", "eq:O-B", "eq:O-C", keep=True)], [hl("arc:aob", "arc:aoc", "lbl:aob", "lbl:aoc", keep=True)], [hl("arc:ask")]],
        sol2=[
            "∠AOB + ∠AOC = 180°이고 비가 {p} : {q}이므로 ∠AOB = 180° × [[frac({p}, {p + q})]] = {aob}°, ∠AOC = {aoc}°",
            "점 O는 외심이므로 OA = OC, 즉 △OAC는 이등변삼각형이고 ∠OAC = ∠OCA",
            "∠AOB는 △OAC의 외각이므로 ∠AOB = ∠OAC + ∠OCA = 2∠C → ∠C = {aob}° ÷ 2 = {cv}°",
            "∠B = 90° − ∠C = {bv}°, 따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠AOB = {aob}°, ∠AOC = {aoc}°", "hint": "180°를 {p} : {q}로"}, {"text": "∠AOB = 2∠C", "hint": "△OAC의 외각 (OA = OC)"},
                        {"text": "∠C = {cv}°, ∠B = {bv}°", "hint": "절반, 90°에서 빼기"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="∠AOC = 2∠B = 2 × {bv}° = {aoc}°로 나머지 각과도 맞고, ∠B + ∠C = {bv}° + {cv}° = 90°다. 답은 [[deg({ans_v})]]다.",
        model_answer="∠AOB + ∠AOC = 180°이고 ∠AOB : ∠AOC = {p} : {q}이므로 ∠AOB = {aob}°이다. 점 O는 직각삼각형의 외심이므로 OA = OC이고 ∠OAC = ∠OCA이며, ∠AOB는 △OAC의 외각이므로 ∠AOB = 2∠C, ∠C = {cv}°이다. ∠B = 90° − {cv}° = {bv}°이므로 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "비례배분", "points": 2, "criterion": "180°를 {p} : {q}로 나누어 ∠AOB = {aob}°를 구했다.", "partial": "비의 방향을 바꿨으면 인정하지 않는다."},
            {"element": "외심·외각", "points": 3, "criterion": "OA = OC에서 △OAC가 이등변삼각형이고 ∠AOB = 2∠C임을 밝혔다.", "partial": "OA = OC만 쓰고 외각으로 옮기지 못했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": "∠B와 ∠C를 바꿔 답했으면 인정하지 않는다."},
        ],
    )


CIRC_SEED = {
    "seed_id": "m2-2-circumcenter", "category": "도형",
    "title": "삼각형의 외심 — ∠BOC = 2∠A, 세 각의 합 90°, 직각삼각형의 외접원, △OAB 둘레, 비로 나뉜 각",
    "unit_id": "m2-2", "concept_ids": ["m2-2-02"],
    "schema_id": SCHEMA_CIRC, "schema_name": "삼각형 외심에서 중심각과 원주각 관계 / 직각삼각형의 외접원 / 외심 각 조합",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 5.3)을 참고해 새로 씀. 외접원 반지름 3(그림 단위)으로 두고 꼭짓점을 원 위의 각으로 배치(t1·t2: 내각에서 호의 중심각을 계산해 예각삼각형 보장). t3·t4 직각삼각형은 AC 길이에서 A의 좌표를 정확히 계산. π 답은 [[k*pi]] 마커(t4·t5).",
    "geometry": True,
    "templates": [circ_t1(), circ_t2(), circ_t3(), circ_t4(), circ_t5(), circ_t6()],
}



# ═══════════════════════════════════════════════════════════════════ 3. 삼각형의 내심
INC = dict(prereq=["내심: 세 내각의 이등분선의 교점", "내심에서 세 변까지의 거리는 같다(내접원의 반지름)", "삼각형의 내각의 합 180°"],
           ops=["각도"], tags=["내심", "내접원"])


def inc_geom(Aexpr, Bexpr):
    """각 A, B(도)에서 BC = 4 로 둔 삼각형의 꼭짓점·내심·내접원 반지름 (B = 원점, C = (4, 0))."""
    return {"Ad": Aexpr, "Bd": Bexpr, "Cd": "180 - Ad - Bd",
            "sb": "4*sin(pi*Bd/180)/sin(pi*Ad/180)", "sc": "4*sin(pi*Cd/180)/sin(pi*Ad/180)",
            "ax": "sc*cos(pi*Bd/180)", "ay": "sc*sin(pi*Bd/180)",
            "pp": "4 + sb + sc", "ix": "(4*ax + 4*sc)/pp", "iy": "4*ay/pp", "rr": "iy"}


INC_PTS = {"A": ["{ax}", "{ay}"], "B": [0, 0], "C": [4, 0], "I": ["{ix}", "{iy}"]}
INC_CIRC = [{"c": "I", "r": "{rr}"}]


def inc_t1():
    # 주어진 꼭짓점 P(A·B·C)와 방향(꼭짓점각 → 내심각 / 내심각 → 꼭짓점각)을 행으로 — 같은 성질을 세 꼭짓점에 돌려 적용
    # (그림만 다른 s축은 문면 중복(DUP)으로 탈락하므로 행마다 모양 s를 하나씩 붙였다)
    def row(P, Q1, Q2, fwd, s, ldx, ldy):
        IQ = f"{Q1}I{Q2}"
        base = {"P": P, "Q1": Q1, "Q2": Q2, "IQ": IQ, "vA": int(P == "A"), "vB": int(P == "B"), "vC": int(P == "C"), "s": s, "LDX": ldx, "LDY": ldy}
        if fwd:
            return {**base, "GQ": P, "XQ": IQ, "isB": 1, "GA": P, "GF": Q1, "GT": Q2, "XA": "I", "XF": Q1, "XT": Q2,
                    "F1": f"∠{IQ} = 90° + [[frac(1, 2)]] × ", "F2": "°", "LAW": f"90° + ∠{P}의 절반"}
        return {**base, "GQ": IQ, "XQ": P, "isB": 0, "GA": "I", "GF": Q1, "GT": Q2, "XA": P, "XF": Q1, "XT": Q2,
                "F1": f"∠{P} = 2 × (", "F2": "° − 90°)", "LAW": f"(∠{IQ} − 90°)의 2배"}
    rows = {"A>BIC": row("A", "B", "C", True, 0, 0, 22), "BIC>A": row("A", "B", "C", False, 10, 0, 30),
            "B>AIC": row("B", "A", "C", True, -10, 24, -2), "AIC>B": row("B", "A", "C", False, 0, 28, -8),
            "C>AIB": row("C", "A", "B", True, 10, -24, -2), "AIB>C": row("C", "A", "B", False, -10, -28, -8)}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["I", "{Q1}"], ["I", "{Q2}"]]
    marks = {"arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-incenter", 1, INC,
        title="내심 — ∠BIC = 90° + ∠A ÷ 2",
        skill="IB, IC가 각의 이등분선임을 써서 △IBC의 내각의 합으로 ∠BIC를 ∠A로 나타내기 (세 꼭짓점에 돌려 적용)",
        variant_axis={"주어진 것": "꼭짓점각 / 내심각", "꼭짓점": "A·B·C", "각": "30°~100° (짝수)"},
        discriminates="내심의 성질(각의 이등분선)에서 두 밑각의 절반의 합 = (180° − 꼭짓점각) ÷ 2를 세우는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=80,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "a", "values": {"in": list(range(30, 102, 2))}}],
        table={"key": "w", "rows": rows},
        derive={**inc_geom("a*vA + ((180 - a)/2 + s)*vB + ((180 - a)/2 - s)*vC", "a*vB + ((180 - a)/2 + s)*vC + ((180 - a)/2 - s)*vA"),
                "bic": "90 + a/2", "half": "90 - a/2", "gv": "a*isB + (90 + a/2)*(1 - isB)", "ans_v": "(90 + a/2)*isB + a*(1 - isB)"},
        constraints=["ans_v != gv"],
        cost_values=["a", "bic", "ans_v"],
        answer_var="ans_v",
        verify=["2*bic == 180 + a", "(isB == 1 and ans == bic) or (isB == 0 and ans == a)"],
        question="다음 그림에서 점 I는 △ABC의 내심이다. [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(INC_PTS, segs, marks=marks, circles=INC_CIRC),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="점 I는 내심이므로 I{Q1}, I{Q2}는 각각 ∠{Q1}, ∠{Q2}의 이등분선이다: ∠I{Q1}{Q2} = [[frac(1, 2)]]∠{Q1}, ∠I{Q2}{Q1} = [[frac(1, 2)]]∠{Q2}. △I{Q1}{Q2}의 내각의 합에서 ∠{IQ} = 180° − [[frac(1, 2)]](∠{Q1} + ∠{Q2})이고, ∠{Q1} + ∠{Q2} = 180° − ∠{P}이므로 ∠{IQ} = 90° + [[frac(1, 2)]]∠{P}다.",
        sol1_fig=scene(INC_PTS, segs + [{"a": "I", "b": "{P}", "dash": True}],
                       marks={"arc": marks["arc"] + [arc("{Q1}", "I", "{Q2}", "•", "arc:b1"), arc("{Q1}", "{P}", "I", "•", "arc:b2"), arc("{Q2}", "{P}", "I", "×", "arc:c1"), arc("{Q2}", "I", "{Q1}", "×", "arc:c2")]},
                       circles=INC_CIRC, labels=[{"at": "{XA}", "text": "{ans_v}°", "dx": "{LDX}", "dy": "{LDY}", "accent": True, "k": "lbl:ans"}]),
        sol1_anim=[[hl("arc:b1", "arc:b2", "arc:c1", "arc:c2", keep=True)], [hl("arc:given", keep=True)], [hl("lbl:ans", "arc:ask")]],
        sol2=[
            "점 I는 내심이므로 ∠I{Q1}{Q2} = [[frac(1, 2)]]∠{Q1}, ∠I{Q2}{Q1} = [[frac(1, 2)]]∠{Q2}",
            "△I{Q1}{Q2}에서 ∠{IQ} = 180° − [[frac(1, 2)]](∠{Q1} + ∠{Q2}) = 180° − [[frac(1, 2)]](180° − ∠{P}) = 90° + [[frac(1, 2)]]∠{P}",
            "{F1}{gv}{F2} = {ans_v}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠I{Q1}{Q2} = [[frac(1, 2)]]∠{Q1}, ∠I{Q2}{Q1} = [[frac(1, 2)]]∠{Q2}", "hint": "내심 = 각의 이등분선의 교점"}, {"text": "∠{IQ} = 90° + [[frac(1, 2)]]∠{P}", "hint": "△I{Q1}{Q2}의 내각의 합"},
                        {"text": "{F1}{gv}{F2} = {ans_v}°", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="∠{Q1} + ∠{Q2} = 180° − {a}° = {180 - a}°이고 그 절반 {half}°를 180°에서 빼면 {bic}°다. ∠{P} = {a}°와 ∠{IQ} = {bic}°의 조합이 조건과 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="점 I는 내심이므로 ∠I{Q1}{Q2} = [[frac(1, 2)]]∠{Q1}, ∠I{Q2}{Q1} = [[frac(1, 2)]]∠{Q2}이다. △I{Q1}{Q2}에서 ∠{IQ} = 180° − [[frac(1, 2)]](∠{Q1} + ∠{Q2}) = 180° − [[frac(1, 2)]](180° − ∠{P}) = 90° + [[frac(1, 2)]]∠{P}이므로 {F1}{gv}{F2} = {ans_v}°이다. 따라서 ∠{XQ} = {ans_v}°다.",
        rubric=[
            {"element": "각의 이등분선", "points": 3, "criterion": "내심의 성질에서 ∠I{Q1}{Q2} = [[frac(1, 2)]]∠{Q1}, ∠I{Q2}{Q1} = [[frac(1, 2)]]∠{Q2}임을 밝혔다.", "partial": "한쪽만 썼으면 1점."},
            {"element": "∠{IQ} 식", "points": 2, "criterion": "∠{IQ} = 90° + [[frac(1, 2)]]∠{P}(또는 같은 뜻의 식)를 세웠다.", "partial": "∠{IQ} = 2∠{P} 등 외심의 성질과 혼동했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": ""},
        ],
    )


def inc_t2():
    rows = {"IAB": {"XQ": "IAB", "G1": "IBC", "G2": "ICA", "uA": 1, "uB": 0, "uC": 0, "XA": "A", "XF": "I", "XT": "B", "G1A": "B", "G1F": "I", "G1T": "C", "G2A": "C", "G2F": "I", "G2T": "A"},
            "IBC": {"XQ": "IBC", "G1": "IAB", "G2": "ICA", "uA": 0, "uB": 1, "uC": 0, "XA": "B", "XF": "I", "XT": "C", "G1A": "A", "G1F": "I", "G1T": "B", "G2A": "C", "G2F": "I", "G2T": "A"},
            "ICA": {"XQ": "ICA", "G1": "IAB", "G2": "IBC", "uA": 0, "uB": 0, "uC": 1, "XA": "C", "XF": "I", "XT": "A", "G1A": "A", "G1F": "I", "G1T": "B", "G2A": "B", "G2F": "I", "G2T": "C"}}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], ["I", "A"], ["I", "B"], ["I", "C"]]
    marks = {"arc": [arc("{G1A}", "{G1F}", "{G1T}", "{g1}°", "arc:g1"), arc("{G2A}", "{G2F}", "{G2T}", "{g2}°", "arc:g2"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}
    return tpl("m2-2-incenter", 2, INC,
        title="내심 — ∠IAB + ∠IBC + ∠ICA = 90°",
        skill="세 내각의 절반의 합이 90°임을 써서 나머지 각 구하기",
        variant_axis={"구하는 것": "∠IAB / ∠IBC / ∠ICA", "각": "10°~55°"},
        discriminates="내심이 각의 이등분선의 교점이므로 세 각이 각각 내각의 절반이고 그 합이 90°임을 세우는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90,
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "p", "values": {"int": [10, 55]}}, {"name": "q", "values": {"int": [10, 55]}}],
        table={"key": "w", "rows": rows},
        derive={**inc_geom("2*p", "2*q"), "z": "90 - p - q", "g1": "p*(1 - uA) + q*uA", "g2": "z*(1 - uC) + q*uC", "ans_v": "p*uA + q*uB + z*uC"},
        constraints=["z >= 10", "ans_v != g1", "ans_v != g2", "g1 != g2"],
        cost_values=["p", "q", "z", "ans_v"],
        answer_var="ans_v",
        verify=["p + q + z == 90", "g1 + g2 + ans == 90"],
        question="다음 그림에서 점 I는 △ABC의 내심이다. [[angle({G1})]] = [[deg({g1})]], [[angle({G2})]] = [[deg({g2})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(INC_PTS, segs, marks=marks, circles=INC_CIRC),
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="내심 I는 세 내각의 이등분선의 교점이다. 그래서 ∠IAB = ∠IAC = [[frac(1, 2)]]∠A, ∠IBA = ∠IBC = [[frac(1, 2)]]∠B, ∠ICB = ∠ICA = [[frac(1, 2)]]∠C이고, ∠IAB + ∠IBC + ∠ICA = [[frac(1, 2)]](∠A + ∠B + ∠C) = [[frac(1, 2)]] × 180° = 90°다.",
        sol1_fig=scene(INC_PTS, segs, marks={"arc": marks["arc"] + [arc("A", "C", "I", "{p}°", "arc:a2"), arc("B", "A", "I", "{q}°", "arc:b2"), arc("C", "B", "I", "{z}°", "arc:c2")]}, circles=INC_CIRC),
        sol1_anim=[[hl("arc:g1", "arc:g2", keep=True)], [hl("arc:a2", "arc:b2", "arc:c2", keep=True)], [hl("arc:ask")]],
        sol2=[
            "점 I는 내심이므로 ∠IAB = [[frac(1, 2)]]∠A, ∠IBC = [[frac(1, 2)]]∠B, ∠ICA = [[frac(1, 2)]]∠C",
            "∠IAB + ∠IBC + ∠ICA = [[frac(1, 2)]](∠A + ∠B + ∠C) = [[frac(1, 2)]] × 180° = 90°",
            "∠{XQ} = 90° − {g1}° − {g2}° = {ans_v}°",
            "따라서 ∠{XQ} = {ans_v}°",
        ],
        sol2_fig=steps([{"text": "∠IAB = [[frac(1, 2)]]∠A, ∠IBC = [[frac(1, 2)]]∠B, ∠ICA = [[frac(1, 2)]]∠C", "hint": "내심 = 각의 이등분선의 교점"}, {"text": "∠IAB + ∠IBC + ∠ICA = 90°", "hint": "내각의 합의 절반"},
                        {"text": "∠{XQ} = 90° − {g1}° − {g2}° = {ans_v}°"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)], []],
        sol_check="세 각 {g1}° + {g2}° + {ans_v}° = 90°이고, △ABC의 세 내각은 각각 그 2배인 {2*p}°, {2*q}°, {2*z}°로 합이 180°다. 답은 [[deg({ans_v})]]다.",
        model_answer="점 I는 내심이므로 ∠IAB = [[frac(1, 2)]]∠A, ∠IBC = [[frac(1, 2)]]∠B, ∠ICA = [[frac(1, 2)]]∠C이고, 세 각의 합은 [[frac(1, 2)]] × 180° = 90°이다. 따라서 ∠{XQ} = 90° − {g1}° − {g2}° = {ans_v}°다.",
        rubric=[
            {"element": "각의 이등분선", "points": 3, "criterion": "내심의 성질에서 세 각이 각각 내각의 절반임을 밝혔다.", "partial": "한 각만 밝혔으면 1점."},
            {"element": "합이 90°", "points": 2, "criterion": "세 각의 합이 [[frac(1, 2)]] × 180° = 90°임을 세웠다.", "partial": "합을 180°로 두었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{XQ} = {ans_v}°를 구했다.", "partial": ""},
        ],
    )


INC3_GEOM = inc_geom("52", "60")


def inc_t3():
    rows = {"area": {"Q": "△ABC의 넓이", "U": " cm²", "UA": "cm²", "isA": 1, "isR": 0, "isP": 0, "G1T": "내접원의 반지름의 길이가 ", "G1U": " cm", "G2T": "△ABC의 둘레의 길이가 ", "G2U": " cm",
                     "F1": "△ABC = [[frac(1, 2)]] × r × (둘레) = [[frac(1, 2)]] × ", "F2": " × ", "LAW": "[[frac(1, 2)]] × r × 둘레"},
            "r": {"Q": "내접원의 반지름의 길이", "U": " cm", "UA": "cm", "isA": 0, "isR": 1, "isP": 0, "G1T": "△ABC의 넓이가 ", "G1U": " cm²", "G2T": "△ABC의 둘레의 길이가 ", "G2U": " cm",
                  "F1": "r = 2 × (넓이) ÷ (둘레) = 2 × ", "F2": " ÷ ", "LAW": "넓이 = [[frac(1, 2)]] × r × 둘레"},
            "perim": {"Q": "△ABC의 둘레의 길이", "U": " cm", "UA": "cm", "isA": 0, "isR": 0, "isP": 1, "G1T": "△ABC의 넓이가 ", "G1U": " cm²", "G2T": "내접원의 반지름의 길이가 ", "G2U": " cm",
                      "F1": "(둘레) = 2 × (넓이) ÷ r = 2 × ", "F2": " ÷ ", "LAW": "넓이 = [[frac(1, 2)]] × r × 둘레"}}
    pts = {**INC_PTS, "E": ["{ix}", 0]}
    segs = [["A", "B"], ["B", "C"], ["C", "A"], {"a": "I", "b": "E", "dash": True, "label": "r"}]
    return tpl("m2-2-incenter", 3, INC,
        title="내접원의 반지름과 넓이 — △ABC = ½ × r × (둘레)",
        skill="내심에서 세 변까지의 거리가 r로 같음을 써서 넓이를 r × 둘레 ÷ 2로 나타내기",
        variant_axis={"구하는 것": "넓이 / 반지름 / 둘레", "r": "2~6", "둘레": "20~60"},
        discriminates="△ABC를 △IAB, △IBC, △ICA로 쪼개어 높이가 모두 r임을 쓰는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90, process="문제해결",
        prereq=["내심에서 세 변까지의 거리는 같다(내접원의 반지름)", "삼각형의 넓이"], ops=["넓이", "방정식"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "r", "values": {"int": [2, 6]}}, {"name": "P", "values": {"in": list(range(20, 62, 2))}}],
        table={"key": "w", "rows": rows},
        derive={**INC3_GEOM, "S": "r*P/2", "g1": "r*isA + r*P/2*(1 - isA)", "g2": "P*(isA + isR) + r*isP", "ans_v": "r*P/2*isA + r*isR + P*isP",
                "t1": "(ix*ax + iy*ay)/sc", "dx": "t1*ax/sc", "dy": "t1*ay/sc",
                "t2": "((ix - ax)*(4 - ax) + (iy - ay)*(0 - ay))/sb", "fx": "ax + t2*(4 - ax)/sb", "fy": "ay - t2*ay/sb"},
        constraints=["S != P", "S != r", "P != 2*r"],
        cost_values=["r", "P", "S", "ans_v"],
        answer_var="ans_v",
        verify=["2*S == r*P", "(isA == 1 and ans == S) or (isR == 1 and ans == r) or (isP == 1 and ans == P)"],
        question="다음 그림에서 점 I는 △ABC의 내심이다. {G1T}{g1}{G1U}이고 {G2T}{g2}{G2U}일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, circles=INC_CIRC, nodot=["E"]),
        answer="{ans_v}", answer_alt=["{ans_v}{U}"],
        sol1="내심 I에서 세 변 AB, BC, CA에 내린 수선의 길이는 모두 내접원의 반지름 r로 같다. 그래서 △ABC를 I와 세 꼭짓점을 이어 △IAB, △IBC, △ICA로 나누면 세 삼각형의 높이가 모두 r이고, 넓이의 합은 [[frac(1, 2)]] × r × (AB + BC + CA) = [[frac(1, 2)]] × r × (둘레)다.",
        sol1_fig=scene({**pts, "D": ["{dx}", "{dy}"], "F": ["{fx}", "{fy}"]},
                       [["A", "B"], ["B", "C"], ["C", "A"], {"a": "I", "b": "A", "dash": True}, {"a": "I", "b": "B", "dash": True}, {"a": "I", "b": "C", "dash": True},
                        {"a": "I", "b": "D", "label": "r"}, {"a": "I", "b": "E", "label": "r"}, {"a": "I", "b": "F", "label": "r"}],
                       marks={"right": [["I", "D", "B"], ["I", "E", "C"], ["I", "F", "A"]]}, circles=INC_CIRC, nodot=["D", "E", "F"],
                       shade=[["I", "A", "B"], ["I", "B", "C"], ["I", "C", "A"]]),
        sol1_anim=[[hl("seg:I-D", "seg:I-E", "seg:I-F", "seglbl:I-D", "seglbl:I-E", "seglbl:I-F", keep=True)], [hl("shade:0", "shade:1", "shade:2", "seg:I-A", "seg:I-B", "seg:I-C")]],
        sol2=[
            "내심에서 세 변까지의 거리는 내접원의 반지름 r로 같으므로 △IAB, △IBC, △ICA의 높이는 모두 r",
            "△ABC = △IAB + △IBC + △ICA = [[frac(1, 2)]] × r × (AB + BC + CA) = [[frac(1, 2)]] × r × (둘레)",
            "{F1}{g1}{F2}{g2} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v}{U}",
        ],
        sol2_fig=steps([{"text": "높이가 모두 r인 세 삼각형", "hint": "내심 → 세 변까지의 거리 r"}, {"text": "△ABC = [[frac(1, 2)]] × r × (둘레)", "hint": "{LAW}"}, {"text": "{F1}{g1}{F2}{g2} = {ans_v}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)], []],
        sol_check="r = {r} cm, 둘레 {P} cm이면 넓이는 [[frac(1, 2)]] × {r} × {P} = {S}(cm²)로 세 값이 서로 맞는다. 답은 {ans_v}{U}다.",
        model_answer="내심 I에서 세 변까지의 거리는 내접원의 반지름 r로 같으므로 △ABC = △IAB + △IBC + △ICA = [[frac(1, 2)]] × r × (둘레)이다. {F1}{g1}{F2}{g2} = {ans_v}이므로 {Q}{eun(Q)} {ans_v}{U}다.",
        rubric=[
            {"element": "세 삼각형으로 나누기", "points": 3, "criterion": "△ABC를 세 삼각형으로 나누고 높이가 모두 r임을 밝혔다.", "partial": "공식 [[frac(1, 2)]] × r × (둘레)만 쓰고 근거가 없으면 1점."},
            {"element": "식 세우기·계산", "points": 2, "criterion": "{F1}{g1}{F2}{g2} = {ans_v}{eul(ans_v)} 계산했다.", "partial": "[[frac(1, 2)]]을 빠뜨렸으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans_v}{U}{eul(UA)} 답했다.", "partial": "단위가 없으면 1점."},
        ],
    )


TRIPLES = {"345": {"a0": 3, "b0": 4, "c0": 5}, "51213": {"a0": 5, "b0": 12, "c0": 13}, "81517": {"a0": 8, "b0": 15, "c0": 17}, "72425": {"a0": 7, "b0": 24, "c0": 25}, "435": {"a0": 4, "b0": 3, "c0": 5}, "12513": {"a0": 12, "b0": 5, "c0": 13}}


def inc_t4():
    rows = {"r": {"Q": "내접원의 반지름의 길이", "isR": 1, "isD": 0, "isE": 0, "F1": "r = (BC + CA − AB) ÷ 2 = ", "F2": " ÷ ", "LAW": "r = (a + b − c) ÷ 2"},
            "ad": {"Q": "[[seg(AD)]]의 길이", "isR": 0, "isD": 1, "isE": 0, "F1": "AD = AF = ", "F2": " − ", "LAW": "AF = CA − CF = CA − r"},
            "bd": {"Q": "[[seg(BD)]]의 길이", "isR": 0, "isD": 0, "isE": 1, "F1": "BD = BE = ", "F2": " − ", "LAW": "BE = BC − CE = BC − r"}}
    pts = {"A": [0, "{b}"], "B": ["{a}", 0], "C": [0, 0], "I": ["{r}", "{r}"], "D": ["{dx}", "{dy}"], "E": ["{r}", 0], "F": [0, "{r}"]}
    segs = [{"a": "B", "b": "A", "label": "{c} cm"}, {"a": "C", "b": "B", "label": "{a} cm"}, {"a": "A", "b": "C", "label": "{b} cm"}, {"a": "I", "b": "E", "dash": True}, {"a": "I", "b": "F", "dash": True}]
    marks = {"right": [["A", "C", "B"]]}
    return tpl("m2-2-incenter", 4, INC,
        title="직각삼각형의 내접원 — r = (a + b − c) ÷ 2, 접선의 길이",
        skill="내심에서 두 변에 내린 수선이 정사각형을 만들어 CE = CF = r임을 쓰고, 접선의 길이로 빗변을 나누기",
        variant_axis={"구하는 것": "r / AD / BD", "세 변": "피타고라스 수 6종 × 1~4배"},
        discriminates="∠C = 90°에서 □IECF가 정사각형임을 읽고, 두 접선의 길이가 같음을 써서 AB = (b − r) + (a − r)를 세우는가",
        qtype="short", difficulty=4, pool_target=300, time_limit=110, process="문제해결",
        prereq=["내심에서 세 변까지의 거리는 같다", "원 밖의 한 점에서 그은 두 접선의 길이는 같다", "정사각형의 성질"], ops=["방정식"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "t", "values": {"in": list(TRIPLES)}}, {"name": "k", "values": {"int": [1, 4]}}],
        table=[{"key": "w", "rows": rows}, {"key": "t", "rows": TRIPLES}],
        derive={"a": "k*a0", "b": "k*b0", "c": "k*c0", "r": "(a + b - c)/2", "ad": "b - r", "bd": "a - r", "ans_v": "r*isR + (b - r)*isD + (a - r)*isE",
                "v1": "(a + b - c)*isR + b*isD + a*isE", "v2": "2*isR + r*(1 - isR)",
                "dt": "(r*a - (r - b)*b)/c", "dx": "dt*a/c", "dy": "b - dt*b/c"},
        constraints=["ans_v != a", "ans_v != b", "ans_v != c"],
        cost_values=["a", "b", "c", "r", "ans_v"],
        answer_var="ans_v",
        verify=["a*a + b*b == c*c", "ad + bd == c", "(isR == 1 and ans == r) or (isD == 1 and ans == ad) or (isE == 1 and ans == bd)"],
        question="다음 그림에서 원 I는 [[angle(C)]] = [[deg(90)]]인 직각삼각형 ABC의 내접원이고, 점 D는 내접원과 [[seg(AB)]]의 접점이다. [[seg(BC)]] = {a} cm, [[seg(CA)]] = {b} cm, [[seg(AB)]] = {c} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(pts, segs, marks=marks, circles=[{"c": "I", "r": "{r}"}], nodot=["E", "F"]),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="내접원이 BC, CA와 만나는 점을 E, F라 하면 IE ⊥ BC, IF ⊥ CA이고 IE = IF = r다. ∠C = 90°이므로 □IECF는 네 각이 직각이고 이웃한 두 변이 r로 같은 정사각형 — 따라서 CE = CF = r. 원 밖의 한 점에서 그은 두 접선의 길이는 같으므로 AD = AF = {b} − r, BD = BE = {a} − r이고, 이 둘을 더한 것이 AB = {c}다.",
        sol1_fig=scene(pts, segs + [["I", "D"]], marks={"right": [["A", "C", "B"], ["I", "E", "B"], ["I", "F", "A"]], "eq": [[["C", "E"], ["C", "F"], ["I", "E"], ["I", "F"]], [["A", "D"], ["A", "F"]], [["B", "D"], ["B", "E"]]]},
                       circles=[{"c": "I", "r": "{r}"}], nodot=[],
                       labels=[{"at": "C", "text": "r", "dx": 12, "dy": -12, "accent": True, "k": "lbl:r"}]),
        sol1_anim=[[hl("eq:C-E", "eq:C-F", "eq:I-E", "eq:I-F", "lbl:r", keep=True)], [hl("eq:A-D", "eq:A-F", keep=True)], [hl("eq:B-D", "eq:B-E", keep=True)]],
        sol2=[
            "IE ⊥ BC, IF ⊥ CA, IE = IF = r이고 ∠C = 90°이므로 □IECF는 정사각형: CE = CF = r",
            "두 접선의 길이는 같으므로 AD = AF = {b} − r, BD = BE = {a} − r",
            "AB = AD + BD: ({b} − r) + ({a} − r) = {c} → 2r = {a + b - c}, r = {r}",
            "{F1}{v1}{F2}{v2} = {ans_v}",
            "따라서 {Q}{eun(Q)} {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "CE = CF = r", "hint": "□IECF는 정사각형"}, {"text": "AD = {b} − r, BD = {a} − r", "hint": "접선의 길이"},
                        {"text": "({b} − r) + ({a} − r) = {c} → r = {r}", "hint": "AB = AD + BD"}, {"text": "{F1}{v1}{F2}{v2} = {ans_v}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")], []],
        sol_check="r = {r}이면 AD = {ad}, BD = {bd}로 AD + BD = {c} = AB가 맞고, CE = CF = {r}로 BC = BE + EC = {bd} + {r} = {a}, CA = {ad} + {r} = {b}도 맞는다. 답은 {ans_v} cm다.",
        model_answer="내접원과 BC, CA의 접점을 E, F라 하면 ∠C = 90°이고 IE = IF = r이므로 □IECF는 정사각형이고 CE = CF = r이다. 두 접선의 길이는 같으므로 AD = AF = {b} − r, BD = BE = {a} − r이고, AB = AD + BD에서 ({b} − r) + ({a} − r) = {c}, r = {r}이다. 따라서 {Q}{eun(Q)} {ans_v} cm다.",
        rubric=[
            {"element": "정사각형·접선", "points": 3, "criterion": "CE = CF = r(정사각형)과 AD = AF, BD = BE(접선의 길이)를 밝혔다.", "partial": "둘 중 하나만 밝혔으면 1점."},
            {"element": "방정식", "points": 2, "criterion": "({b} − r) + ({a} − r) = {c}를 세워 r = {r}{eul(r)} 구했다.", "partial": "식은 세웠으나 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm를 답했다.", "partial": "r만 구하고 묻는 길이로 옮기지 않았으면 인정하지 않는다."},
        ],
    )


def tan_geom():
    """접선의 길이 ta·tb·tc(파라미터) → 세 변 a·b·c, 좌표(B 원점, C = (a, 0)), 내심, 접점 D(AB)·E(BC)·F(CA)."""
    return {"a": "tb + tc", "b": "ta + tc", "c": "ta + tb", "P": "a + b + c", "hp": "P/2",
            "ax": "(a*a + c*c - b*b)/(2*a)", "ay": "sqrt(abs(c*c - ax*ax))",
            "ix": "(a*ax + c*a)/P", "iy": "a*ay/P", "rr": "iy",
            "t1": "(ix*ax + iy*ay)/c", "dx": "t1*ax/c", "dy": "t1*ay/c",
            "t2": "((ix - ax)*(a - ax) + (iy - ay)*(0 - ay))/b", "fx": "ax + t2*(a - ax)/b", "fy": "ay - t2*ay/b"}


TAN_PTS = {"A": ["{ax}", "{ay}"], "B": [0, 0], "C": ["{a}", 0], "I": ["{ix}", "{iy}"], "D": ["{dx}", "{dy}"], "E": ["{ix}", 0], "F": ["{fx}", "{fy}"]}


def inc_t5():
    rows = {"AD": {"XS": "AD", "isA": 1, "isB": 0, "isC": 0, "F1": "x = ", "F2": " − ", "SUB": "a"}, "BE": {"XS": "BE", "isA": 0, "isB": 1, "isC": 0, "F1": "y = ", "F2": " − ", "SUB": "b"},
            "CF": {"XS": "CF", "isA": 0, "isB": 0, "isC": 1, "F1": "z = ", "F2": " − ", "SUB": "c"}}
    segs = [["A", "B"], ["B", "C"], ["C", "A"]]
    # 변 길이 라벨은 중점이 아니라 접점(D·E·F)에서 먼 쪽 1/4 지점에, 바깥 법선 방향 20px 띄워 둔다 — 접점 이름과 겹치지 않게
    side_labels = [{"at": ["{ax*(1 - qab)}", "{ay*(1 - qab)}"], "text": "{c} cm", "dx": "{-20*ay/c}", "dy": "{-20*ax/c}", "k": "lbl:ab"},
                   {"at": ["{a*qbc}", 0], "text": "{a} cm", "dx": 0, "dy": 20, "k": "lbl:bc"},
                   {"at": ["{a + qca*(ax - a)}", "{qca*ay}"], "text": "{b} cm", "dx": "{20*ay/b}", "dy": "{-20*(a - ax)/b}", "k": "lbl:ca"}]
    return tpl("m2-2-incenter", 5, INC,
        title="내접원의 접선의 길이 — 세 변에서 접점까지의 길이",
        skill="두 접선의 길이가 같음을 써서 x + y = c, y + z = a, z + x = b를 세우고 풀기",
        variant_axis={"구하는 것": "AD / BE / CF", "접선 길이": "2~7"},
        discriminates="세 쌍의 접선 길이를 미지수로 두고 연립하여 푸는가(세 식의 합 = 둘레)",
        qtype="short", difficulty=4, pool_target=300, time_limit=120, process="문제해결",
        prereq=["원 밖의 한 점에서 그은 두 접선의 길이는 같다", "연립방정식"], ops=["방정식"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "ta", "values": {"int": [2, 7]}}, {"name": "tb", "values": {"int": [2, 7]}}, {"name": "tc", "values": {"int": [2, 7]}}],
        table={"key": "w", "rows": rows},
        derive={**tan_geom(), "ans_v": "ta*isA + tb*isB + tc*isC", "v2": "a*isA + b*isB + c*isC",
                # 접점이 A 쪽(ta < tb)이면 B 쪽 3/4 지점, 아니면 1/4 지점 (같으면 접점이 중점이라 1/4) — 비교식은 곱셈이 안 돼 sign으로
                "qab": "0.25 + 0.25*sign(tb - ta) + 0.25*abs(sign(tb - ta))", "qbc": "0.25 + 0.25*sign(tc - tb) + 0.25*abs(sign(tc - tb))", "qca": "0.25 + 0.25*sign(ta - tc) + 0.25*abs(sign(ta - tc))"},
        constraints=["ta != tb or tb != tc"],
        cost_values=["a", "b", "c", "hp", "ans_v"],
        answer_var="ans_v",
        verify=["a + b + c == 2*hp", "(isA == 1 and ans == hp - a) or (isB == 1 and ans == hp - b) or (isC == 1 and ans == hp - c)"],
        question="다음 그림에서 원 I는 △ABC의 내접원이고, 세 점 D, E, F는 각각 내접원과 세 변 AB, BC, CA의 접점이다. [[seg(AB)]] = {c} cm, [[seg(BC)]] = {a} cm, [[seg(CA)]] = {b} cm일 때, [[seg({XS})]]의 길이를 구하시오.",
        figure=scene(TAN_PTS, segs, circles=[{"c": "I", "r": "{rr}"}], labels=side_labels),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="원 밖의 한 점에서 그 원에 그은 두 접선의 길이는 같다. 그러므로 AD = AF, BD = BE, CE = CF다. 각각을 x, y, z로 두면 세 변이 AB = x + y, BC = y + z, CA = z + x로 나타나고, 세 식을 더하면 2(x + y + z)가 둘레와 같다 — 둘레의 절반에서 한 변을 빼면 그 변과 마주 보는 꼭짓점의 접선의 길이가 나온다.",
        sol1_fig=scene(TAN_PTS, segs + [["I", "D"], ["I", "E"], ["I", "F"]], marks={"eq": [[["A", "D"], ["A", "F"]], [["B", "D"], ["B", "E"]], [["C", "E"], ["C", "F"]]]}, circles=[{"c": "I", "r": "{rr}"}],
                       labels=side_labels + [{"at": "D", "text": "x", "dx": -12, "dy": -8, "accent": True, "k": "lbl:x"}, {"at": "E", "text": "y", "dx": -10, "dy": 14, "accent": True, "k": "lbl:y"}, {"at": "F", "text": "z", "dx": 12, "dy": 10, "accent": True, "k": "lbl:z"}]),
        sol1_anim=[[hl("eq:A-D", "eq:A-F", "lbl:x", keep=True)], [hl("eq:B-D", "eq:B-E", "lbl:y", keep=True)], [hl("eq:C-E", "eq:C-F", "lbl:z", keep=True)]],
        sol2=[
            "AD = AF = x, BD = BE = y, CE = CF = z라 하자 (두 접선의 길이는 같다)",
            "AB = x + y = {c}, BC = y + z = {a}, CA = z + x = {b}",
            "세 식을 더하면 2(x + y + z) = {P}, x + y + z = {hp}",
            "{F1}{hp}{F2}{v2} = {ans_v}",
            "따라서 {XS} = {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AD = AF = x, BD = BE = y, CE = CF = z", "hint": "접선의 길이"}, {"text": "x + y = {c}, y + z = {a}, z + x = {b}", "hint": "세 변"},
                        {"text": "x + y + z = {P} ÷ 2 = {hp}", "hint": "세 식의 합 ÷ 2"}, {"text": "{F1}{hp}{F2}{v2} = {ans_v}", "hint": "합에서 마주 보는 변을 뺀다"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")], []],
        sol_check="x = {ta}, y = {tb}, z = {tc}이면 x + y = {c}, y + z = {a}, z + x = {b}로 세 변이 모두 맞는다. 답은 {ans_v} cm다.",
        model_answer="AD = AF = x, BD = BE = y, CE = CF = z라 하면 x + y = {c}, y + z = {a}, z + x = {b}이다. 세 식을 더하면 x + y + z = {hp}이므로 {F1}{hp}{F2}{v2} = {ans_v}이다. 따라서 {XS} = {ans_v} cm다.",
        rubric=[
            {"element": "접선의 길이", "points": 3, "criterion": "AD = AF, BD = BE, CE = CF를 밝히고 미지수로 두었다.", "partial": "한 쌍만 밝혔으면 1점."},
            {"element": "연립방정식", "points": 2, "criterion": "x + y = {c}, y + z = {a}, z + x = {b}를 세워 풀었다.", "partial": "식은 세웠으나 풀이가 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{XS} = {ans_v} cm를 답했다.", "partial": "다른 접선의 길이를 답했으면 인정하지 않는다."},
        ],
    )


def inc_t6():
    rows = {"perim": {"Q": "△ABC의 둘레의 길이", "isP": 1, "i1": 0, "i2": 0, "i3": 0, "F1": "둘레 = 2 × (", "F2": ")", "LAW": "2(x + y + z)"},
            "AB": {"Q": "[[seg(AB)]]의 길이", "isP": 0, "i1": 1, "i2": 0, "i3": 0, "F1": "AB = AD + DB = ", "F2": "", "LAW": "DB = BE"},
            "BC": {"Q": "[[seg(BC)]]의 길이", "isP": 0, "i1": 0, "i2": 1, "i3": 0, "F1": "BC = BE + EC = ", "F2": "", "LAW": "EC = CF"},
            "CA": {"Q": "[[seg(CA)]]의 길이", "isP": 0, "i1": 0, "i2": 0, "i3": 1, "F1": "CA = CF + FA = ", "F2": "", "LAW": "FA = AD"}}
    segs = [{"a": "A", "b": "D", "label": "{ta} cm"}, ["D", "B"], {"a": "B", "b": "E", "label": "{tb} cm"}, ["E", "C"], {"a": "C", "b": "F", "label": "{tc} cm"}, ["F", "A"]]
    return tpl("m2-2-incenter", 6, INC,
        title="접선의 길이가 주어질 때 — 변의 길이·둘레",
        skill="AF = AD, BD = BE, CE = CF로 각 변을 두 접선의 길이의 합으로 나타내기",
        variant_axis={"구하는 것": "둘레 / AB / BC / CA", "접선 길이": "2~7"},
        discriminates="한 변이 양 끝 꼭짓점의 접선의 길이의 합임을 읽는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=80, process="절차수행",
        prereq=["원 밖의 한 점에서 그은 두 접선의 길이는 같다"], ops=["사칙"],
        params=[{"name": "w", "values": {"in": list(rows)}}, {"name": "ta", "values": {"int": [2, 7]}}, {"name": "tb", "values": {"int": [2, 7]}}, {"name": "tc", "values": {"int": [2, 7]}}],
        table={"key": "w", "rows": rows},
        derive={**tan_geom(), "ans_v": "P*isP + c*i1 + a*i2 + b*i3", "s1": "ta + tb + tc",
                "v1": "s1*isP + ta*i1 + tb*i2 + tc*i3", "v2": "0*isP + tb*i1 + tc*i2 + ta*i3", "MID": "isP*0"},
        constraints=["ta != tb or tb != tc", "ans_v != 2*ta", "ans_v != 2*tb", "ans_v != 2*tc"],
        cost_values=["ta", "tb", "tc", "ans_v"],
        answer_var="ans_v",
        verify=["P == 2*(ta + tb + tc)", "(isP == 1 and ans == P) or (i1 == 1 and ans == c) or (i2 == 1 and ans == a) or (i3 == 1 and ans == b)"],
        question="다음 그림에서 원 I는 △ABC의 내접원이고, 세 점 D, E, F는 각각 내접원과 세 변 AB, BC, CA의 접점이다. [[seg(AD)]] = {ta} cm, [[seg(BE)]] = {tb} cm, [[seg(CF)]] = {tc} cm일 때, {Q}{eul(Q)} 구하시오.",
        figure=scene(TAN_PTS, segs, circles=[{"c": "I", "r": "{rr}"}]),
        answer="{ans_v}", answer_alt=["{ans_v} cm"],
        sol1="원 밖의 한 점에서 그은 두 접선의 길이는 같으므로 AF = AD = {ta}, BD = BE = {tb}, CE = CF = {tc}다. 각 변은 접점에서 두 토막으로 나뉘고, 두 토막은 양 끝 꼭짓점의 접선의 길이다: AB = AD + DB, BC = BE + EC, CA = CF + FA.",
        sol1_fig=scene(TAN_PTS, segs + [["I", "D"], ["I", "E"], ["I", "F"]], marks={"eq": [[["A", "D"], ["A", "F"]], [["B", "D"], ["B", "E"]], [["C", "E"], ["C", "F"]]]}, circles=[{"c": "I", "r": "{rr}"}],
                       labels=[{"at": "F", "text": "{ta}", "dx": 14, "dy": -10, "accent": True, "k": "lbl:fa"}, {"at": "D", "text": "{tb}", "dx": -12, "dy": 10, "accent": True, "k": "lbl:db"}, {"at": "E", "text": "{tc}", "dx": 12, "dy": 14, "accent": True, "k": "lbl:ec"}]),
        sol1_anim=[[hl("eq:A-D", "eq:A-F", "lbl:fa", keep=True)], [hl("eq:B-D", "eq:B-E", "lbl:db", keep=True)], [hl("eq:C-E", "eq:C-F", "lbl:ec", keep=True)]],
        sol2=[
            "두 접선의 길이는 같으므로 AF = AD = {ta}, BD = BE = {tb}, CE = CF = {tc}",
            "AB = AD + DB = {ta} + {tb} = {c}, BC = BE + EC = {tb} + {tc} = {a}, CA = CF + FA = {tc} + {ta} = {b}",
            "둘레 = {c} + {a} + {b} = {P} = 2 × ({ta} + {tb} + {tc})",
            "따라서 {Q}{eun(Q)} {ans_v} cm",
        ],
        sol2_fig=steps([{"text": "AF = {ta}, BD = {tb}, CE = {tc}", "hint": "접선의 길이"}, {"text": "AB = {c}, BC = {a}, CA = {b}", "hint": "두 토막의 합"}, {"text": "둘레 = {P}", "hint": "2 × ({ta} + {tb} + {tc})"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], []],
        sol_check="세 변 {c} + {a} + {b} = {P}이고, 이는 접선의 길이의 합 {ta} + {tb} + {tc} = {s1}의 2배다. 답은 {ans_v} cm다.",
        model_answer="두 접선의 길이는 같으므로 AF = AD = {ta} cm, BD = BE = {tb} cm, CE = CF = {tc} cm이다. 따라서 AB = {c} cm, BC = {a} cm, CA = {b} cm이고 둘레는 {P} cm이다. 그러므로 {Q}{eun(Q)} {ans_v} cm다.",
        rubric=[
            {"element": "접선의 길이", "points": 3, "criterion": "AF = AD, BD = BE, CE = CF를 밝혔다.", "partial": "한 쌍만 밝혔으면 1점."},
            {"element": "변의 길이", "points": 2, "criterion": "각 변을 두 접선의 길이의 합으로 구했다.", "partial": "한 변만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} {ans_v} cm를 답했다.", "partial": "다른 변이나 둘레의 절반을 답했으면 인정하지 않는다."},
        ],
    )


INC_SEED = {
    "seed_id": "m2-2-incenter", "category": "도형",
    "title": "삼각형의 내심 — ∠BIC, 세 각의 합 90°, 넓이와 반지름, 직각삼각형의 내접원, 접선의 길이",
    "unit_id": "m2-2", "concept_ids": ["m2-2-02"],
    "schema_id": SCHEMA_INC, "schema_name": "삼각형의 내접원과 선분의 길이 / 내심 각 / 내접원의 반지름",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(TYPES.md 5.4)을 참고해 새로 씀. 내심 좌표는 변의 길이 가중 평균(aA + bB + cC)/(a + b + c)으로 정확히 계산하고 내접원 반지름 = 내심의 y좌표. 접점 D·F는 내심의 수선의 발(정사영). t4는 피타고라스 수로 세 변을 만들어 r이 정수.",
    "geometry": True,
    "templates": [inc_t1(), inc_t2(), inc_t3(), inc_t4(), inc_t5(), inc_t6()],
}


if __name__ == "__main__":
    for seed in (ISO_SEED, CIRC_SEED, INC_SEED):
        with_pitfalls(seed, strict=False)
        dump(seed)
