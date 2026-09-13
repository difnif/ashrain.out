# itemfactory/tools/mkseed_m1_geo3.py — m1-2 잔여 [계획] 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m1_geo3.py
#     → seeds/m1-2-tri-angle-2.json    (삼각형 각 2: 각의 비·이등변 연쇄 3a·내각의 이등분선 90 + A/2, 3틀)
#     → seeds/m1-2-parallel-fold.json  (평행선: 두 번 꺾인 선 · 종이 접기, 2틀)
#     → seeds/m1-2-sector-shade.json   (색칠 부분: 고리 넓이·고리 둘레 a + b·정사각형 − 사분원 p + q·반원 세 개, 4틀)
#     → seeds/m1-2-tri-sides.json      (삼각형 세 변 조건: 자연수 x의 개수·범위 p + q, 2틀)
#     → seeds/m1-2-sphere-apply.json   (구 응용: 원기둥 속 구·쇠구슬 개수·물 높이 상승·반구 물 옮기기, 4틀)
#
# 각은 scene 좌표를 cos·sin 으로 직접 계산해 실제 크기대로 그린다(HANDOFF §1-1). 세 각 ≥ 20° 가독성 규칙.
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


GEO = {"process": "추론", "context": "기하맥락", "ops": ["각도", "방정식"], "traps": ["구하는대상혼동", "조건누락"], "time_limit": 120, "points": 4, "qtype": "short", "pool_target": 300}

# ═══════════════════════════════════════════════════════════════════ 1. 삼각형의 각 2
TA = "m1-2-tri-angle-2"
TA_BASE = {**GEO, "prereq": ["삼각형의 내각의 합 180°", "삼각형의 외각", "이등변삼각형"], "tags": ["삼각형의 각", "내각과 외각"]}
# 각의 비 (a : b : c) — 합 s 가 180 의 약수가 되게 (한 칸이 정수)
RATIO3 = [(a, b, c) for a in range(1, 8) for b in range(1, 8) for c in range(1, 8) if len({a, b, c}) == 3 and 180 % (a + b + c) == 0 and 180 * min(a, b, c) // (a + b + c) >= 20]
ASK3 = {"A": {"sel": 0, "QWT": "[[angle(A)]]", "QWN": "∠A"}, "B": {"sel": 1, "QWT": "[[angle(B)]]", "QWN": "∠B"}, "C": {"sel": 2, "QWT": "[[angle(C)]]", "QWN": "∠C"}, "max": {"sel": 3, "QWT": "가장 큰 각", "QWN": "가장 큰 각"}}


def ta_t1():
    return tpl(TA, 1, TA_BASE,
        title="세 내각의 비가 주어진 삼각형 — 한 각의 크기",
        skill="세 내각의 합 180°를 비의 합으로 등분해 각 내각을 구하기",
        variant_axis={"구하는 것": "∠A / ∠B / ∠C / 가장 큰 각", "비": "1~7"},
        discriminates="내각의 합 180°를 근거로 비례배분하는가, 묻는 각을 바르게 고르는가",
        difficulty=2,
        params=[{"name": "w", "values": {"in": list(ASK3)}}, {"name": "r3", "values": {"in": [a * 100 + b * 10 + c for a, b, c in RATIO3]}}],
        table={"key": "w", "rows": ASK3},
        derive={"a": "floor(r3/100)", "b": "floor(r3/10) % 10", "c": "r3 % 10", "s": "floor(r3/100) + floor(r3/10) % 10 + r3 % 10", "u": "180/s",
                "A": "180*floor(r3/100)/s", "B": "180*(floor(r3/10) % 10)/s", "C": "180*(r3 % 10)/s",
                "ans_v": "A*(sel == 0) + B*(sel == 1) + C*(sel == 2) + max(A, B, C)*(sel == 3)",
                "cx": "cos(pi*A/180)*sin(pi*B/180)/sin(pi*C/180)", "cy": "sin(pi*A/180)*sin(pi*B/180)/sin(pi*C/180)"},
        constraints=["ans_v != a", "ans_v != b", "ans_v != c", "A >= 20", "B >= 20", "C >= 20", "max(A, B, C) <= 120"],
        cost_values=["a", "b", "c", "s", "u", "ans_v"],
        answer_var="ans_v",
        verify=["A + B + C == 180", "A*b == B*a", "B*c == C*b", "ans == A*(sel == 0) + B*(sel == 1) + C*(sel == 2) + max(A, B, C)*(sel == 3)"],
        question="다음 그림의 [[tri(ABC)]]에서 [[angle(A)]] : [[angle(B)]] : [[angle(C)]] = {a} : {b} : {c}일 때, {QWT}의 크기를 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"A": [0, 0], "B": [1, 0], "C": ["{cx}", "{cy}"]}, "segs": [["A", "B"], ["B", "C"], ["C", "A"]],
                                          "marks": {"arc": [{"at": "A", "from": "B", "to": "C"}, {"at": "B", "from": "C", "to": "A"}, {"at": "C", "from": "A", "to": "B"}]}}}],
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="삼각형의 세 내각의 합은 180°이다. 세 각의 비가 {a} : {b} : {c}이므로 180°를 {a} + {b} + {c} = {s}등분한 한 칸은 180° ÷ {s} = {u}°이고, ∠A는 {a}칸, ∠B는 {b}칸, ∠C는 {c}칸이다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"A": [0, 0], "B": [1, 0], "C": ["{cx}", "{cy}"]}, "segs": [["A", "B"], ["B", "C"], ["C", "A"]],
                                           "marks": {"arc": [{"at": "A", "from": "B", "to": "C", "label": "{A}°"}, {"at": "B", "from": "C", "to": "A", "label": "{B}°"}, {"at": "C", "from": "A", "to": "B", "label": "{C}°"}]}}}],
        sol1_anim=[[hl("arc:A", "arc:B", "arc:C")], [hl("arc:A:lbl", "arc:B:lbl", "arc:C:lbl", keep=True)]],
        sol2=[
            "∠A + ∠B + ∠C = 180° (삼각형의 내각의 합)",
            "∠A : ∠B : ∠C = {a} : {b} : {c}이므로 한 칸은 180° ÷ ({a} + {b} + {c}) = {u}°",
            "∠A = {u}° × {a} = {A}°, ∠B = {u}° × {b} = {B}°, ∠C = {u}° × {c} = {C}°",
            "따라서 {QWN}의 크기는 {ans_v}°",
        ],
        sol2_fig=steps([
            {"text": "∠A + ∠B + ∠C = 180°", "hint": "내각의 합"},
            {"text": "한 칸 = 180° ÷ {s} = {u}°", "hint": "비의 합 {s}", "marks": [{"on": "{u}°", "note": "180÷{s}"}]},
            {"text": "∠A = {A}°,  ∠B = {B}°,  ∠C = {C}°"},
            {"text": "{QWN} = {ans_v}°"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)], [reveal(3)]],
        sol_check="{A}° + {B}° + {C}° = 180°이고 {A} : {B} : {C} = {a} : {b} : {c}로 비도 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="삼각형의 내각의 합은 180°이므로 한 칸은 180° ÷ ({a} + {b} + {c}) = {u}°이고 ∠A = {A}°, ∠B = {B}°, ∠C = {C}°이다. 따라서 {QWN}의 크기는 {ans_v}°다.",
        rubric=[
            {"element": "내각의 합", "points": 2, "criterion": "세 내각의 합이 180°임을 밝혔다.", "partial": "근거 없이 180°만 썼으면 1점."},
            {"element": "비례배분", "points": 3, "criterion": "180°를 {s}등분해 세 각 {A}°, {B}°, {C}°를 구했다.", "partial": "등분 수를 잘못 잡았으면 인정하지 않고, 한 각만 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QWN}의 크기 {ans_v}°를 답했다.", "partial": "다른 각을 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def ta_t2():
    # AB = BC = CD 연쇄: ∠A = a → ∠DCE = 3a (E 는 AC 의 연장선 위)
    return tpl(TA, 2, TA_BASE,
        title="AB = BC = CD인 꺾인 도형 — 외각으로 ∠x = 3a 구하기",
        skill="이등변삼각형의 두 밑각이 같음과 삼각형의 외각은 이웃하지 않는 두 내각의 합임을 두 번 이어 쓰기",
        variant_axis={"∠A": "20°~40°"},
        discriminates="∠BCA = ∠A(이등변), ∠CBD = 2∠A(외각), ∠CDB = ∠CBD(이등변), ∠DCE = ∠A + ∠CDA(외각)의 네 단계를 잇는가",
        difficulty=3,
        params=[{"name": "w", "values": {"in": ["DCE", "CDA"]}}, {"name": "a", "values": {"in": [20, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40]}}],
        table={"key": "w", "rows": {"DCE": {"ASK": "DCE", "isX": 1, "ASKW": "∠DCE"}, "CDA": {"ASK": "CDA", "isX": 0, "ASKW": "∠CDA"}}},
        derive={"x": "3*a", "b2": "2*a", "ans_v": "isX*3*a + (1 - isX)*2*a", "cx": "1 + cos(pi*2*a/180)", "cy": "sin(pi*2*a/180)", "dx": "1 + 2*cos(pi*2*a/180)", "ex": "1.6*(1 + cos(pi*2*a/180))", "ey": "1.6*sin(pi*2*a/180)"},
        constraints=["x != a", "x <= 120"],
        cost_values=["a", "b2", "x", "ans_v"],
        answer_var="ans_v",
        verify=["x == 3*a", "ans == isX*3*a + (1 - isX)*2*a"],
        question="다음 그림에서 [[seg(AB)]] = [[seg(BC)]] = [[seg(CD)]]이고 [[angle(A) = deg({a})]]일 때, [[angle({ASK})]]의 크기를 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"A": [0, 0], "B": [1, 0], "C": ["{cx}", "{cy}"], "D": ["{dx}", 0], "E": ["{ex}", "{ey}"]},
                                          "segs": [["A", "D"], ["A", "E"], ["B", "C"], ["C", "D"]],
                                          "marks": {"eq": [[["A", "B"], ["B", "C"], ["C", "D"]]], "arc": [{"at": "A", "from": "B", "to": "C", "label": "{a}°"}, {"at": "C", "from": "D", "to": "E", "label": "x"}]}}}],
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="AB = BC이므로 △ABC는 이등변삼각형이고 ∠BCA = ∠A = {a}°다. ∠CBD는 △ABC의 외각이므로 ∠CBD = ∠A + ∠BCA = {b2}°다. 다시 BC = CD이므로 △BCD도 이등변삼각형이고 ∠CDB = ∠CBD = {b2}°다. 마지막으로 ∠DCE는 △ACD의 외각이므로 ∠A + ∠CDA = {a}° + {b2}° = {x}°다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"A": [0, 0], "B": [1, 0], "C": ["{cx}", "{cy}"], "D": ["{dx}", 0], "E": ["{ex}", "{ey}"]},
                                           "segs": [["A", "D"], ["A", "E"], ["B", "C"], ["C", "D"]],
                                           "marks": {"eq": [[["A", "B"], ["B", "C"], ["C", "D"]]], "arc": [{"at": "A", "from": "B", "to": "C", "label": "{a}°"}, {"at": "C", "from": "A", "to": "B", "label": "{a}°", "k": "arc:C1"}, {"at": "B", "from": "C", "to": "D", "label": "{b2}°", "k": "arc:B1"}, {"at": "D", "from": "B", "to": "C", "label": "{b2}°", "k": "arc:D1"}, {"at": "C", "from": "D", "to": "E", "label": "x", "k": "arc:C2"}]}}}],
        sol1_anim=[[hl("arc:A", "arc:C1", keep=True)], [hl("arc:B1", keep=True)], [hl("arc:D1", keep=True)], [hl("arc:C2", keep=True)]],
        sol2=[
            "AB = BC이므로 ∠BCA = ∠A = {a}°",
            "∠CBD는 △ABC의 외각이므로 ∠CBD = ∠A + ∠BCA = {a}° + {a}° = {b2}°",
            "BC = CD이므로 ∠CDB = ∠CBD = {b2}°",
            "∠DCE는 △ACD의 외각이므로 ∠DCE = ∠A + ∠CDA = {a}° + {b2}° = {x}°",
            "따라서 {ASKW} = {ans_v}°",
        ],
        sol2_fig=steps([
            {"text": "∠BCA = ∠A = {a}°", "hint": "AB = BC (이등변)"},
            {"text": "∠CBD = {a}° + {a}° = {b2}°", "hint": "△ABC의 외각"},
            {"text": "∠CDB = ∠CBD = {b2}°", "hint": "BC = CD (이등변)"},
            {"text": "∠DCE = {a}° + {b2}° = {x}°", "hint": "△ACD의 외각", "marks": [{"on": "{x}°", "note": "3 × {a}°"}]},
            {"text": "{ASKW} = {ans_v}°"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3", "mark:3-0")], [reveal(4)]],
        sol_check="△ACD에서 ∠A = {a}°, ∠D = {b2}°이므로 ∠ACD = 180° − {a}° − {b2}° = {180 - x}°이고, 평각에서 ∠DCE = 180° − {180 - x}° = {x}°로 같다. 답은 [[deg({ans_v})]]다.",
        model_answer="AB = BC에서 ∠BCA = ∠A = {a}°이고 △ABC의 외각 ∠CBD = {b2}°다. BC = CD에서 ∠CDB = ∠CBD = {b2}°이므로 △ACD의 외각 ∠DCE = ∠A + ∠CDA = {a}° + {b2}° = {x}°다. 따라서 {ASKW} = {ans_v}°다.",
        rubric=[
            {"element": "첫 이등변삼각형과 외각", "points": 3, "criterion": "∠BCA = ∠A = {a}°와 ∠CBD = {b2}°를 근거(이등변·외각)와 함께 구했다.", "partial": "∠CBD = {b2}°만 쓰고 근거를 쓰지 않았으면 1점."},
            {"element": "둘째 이등변삼각형", "points": 2, "criterion": "BC = CD에서 ∠CDB = {b2}°임을 밝혔다.", "partial": "각의 위치를 잘못 잡았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "외각 관계로 {ASKW} = {ans_v}°를 구했다.", "partial": "다른 각(∠ACD 등)을 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


BIS_ROWS = {"fwd": {"GIVEN": "A", "isF": 1, "ASKA": "BDC", "ASKAW": "∠BDC", "S3A": "∠A = ", "S3B": "°이므로 ∠BDC = 90° + ", "S3C": "° ÷ 2 = 90° + ", "S3D": "° = "},
            "rev": {"GIVEN": "BDC", "isF": 0, "ASKA": "A", "ASKAW": "∠A", "S3A": "∠BDC = ", "S3B": "°이므로 ∠A = 2 × (", "S3C": "° − 90°) = 2 × ", "S3D": "° = "}}


def ta_t3():
    # ∠B, ∠C 의 이등분선의 교점 D: ∠BDC = 90° + ∠A/2
    return tpl(TA, 3, TA_BASE,
        title="두 내각의 이등분선이 만나는 각 — ∠BDC = 90° + ∠A/2",
        skill="△DBC의 내각의 합에서 ∠DBC + ∠DCB = (∠B + ∠C)/2 = (180° − ∠A)/2 임을 이용하기",
        variant_axis={"주어진 것": "∠A → ∠BDC / ∠BDC → ∠A", "각": "20°~100°"},
        discriminates="이등분선으로 ∠DBC + ∠DCB = (180° − ∠A) ÷ 2 를 세우는가, 공식을 외워 쓰더라도 근거를 쓰는가",
        difficulty=3,
        params=[{"name": "w", "values": {"in": list(BIS_ROWS)}}, {"name": "a", "values": {"step": [20, 100, 2]}}],
        table={"key": "w", "rows": BIS_ROWS},
        derive={"b": "(180 - a)/2 + 8", "c": "180 - a - b", "d": "90 + a/2", "hb": "b/2", "hc": "c/2", "ans_v": "isF*d + (1 - isF)*a", "gv": "isF*a + (1 - isF)*d", "mid": "isF*a/2 + (1 - isF)*(d - 90)",
                "ax": "cos(pi*b/180)*sin(pi*c/180)/sin(pi*a/180)", "ay": "sin(pi*b/180)*sin(pi*c/180)/sin(pi*a/180)",
                "ca": "sin(pi*b/180)/sin(pi*a/180)", "ab": "sin(pi*c/180)/sin(pi*a/180)",
                "dx": "(ax + ab)/(1 + ca + ab)", "dy": "ay/(1 + ca + ab)"},
        constraints=["c >= 30", "d != a", "ans_v != b", "ans_v != c"],
        cost_values=["a", "d", "ans_v"],
        answer_var="ans_v",
        verify=["d == 90 + a/2", "isF == 0 or ans == d", "isF == 1 or ans == a", "hb + hc + d == 180"],
        question="다음 그림의 [[tri(ABC)]]에서 [[angle(B)]]와 [[angle(C)]]의 이등분선의 교점을 D라 하자. [[angle({GIVEN}) = deg({gv})]]일 때, [[angle({ASKA})]]의 크기를 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"B": [0, 0], "C": [1, 0], "A": ["{ax}", "{ay}"], "D": ["{dx}", "{dy}"]},
                                          "segs": [["A", "B"], ["B", "C"], ["C", "A"], ["B", "D"], ["C", "D"]],
                                          "marks": {"arc": [{"at": "B", "from": "C", "to": "D", "k": "arc:B1"}, {"at": "B", "from": "D", "to": "A", "k": "arc:B2"}, {"at": "C", "from": "A", "to": "D", "k": "arc:C1"}, {"at": "C", "from": "D", "to": "B", "k": "arc:C2"}]}}}],
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="△ABC에서 ∠B + ∠C = 180° − ∠A다. BD, CD가 각각 ∠B, ∠C의 이등분선이므로 ∠DBC = ∠B/2, ∠DCB = ∠C/2이고, 둘을 더하면 (∠B + ∠C)/2 = (180° − ∠A)/2 = 90° − ∠A/2다. △DBC의 내각의 합에서 ∠BDC = 180° − (90° − ∠A/2) = 90° + ∠A/2가 된다. 이 관계로 {GIVEN}에서 {ASKA}를 구한다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"B": [0, 0], "C": [1, 0], "A": ["{ax}", "{ay}"], "D": ["{dx}", "{dy}"]},
                                           "segs": [["A", "B"], ["B", "C"], ["C", "A"], ["B", "D"], ["C", "D"]],
                                           "marks": {"arc": [{"at": "A", "from": "B", "to": "C", "label": "{a}°", "k": "arc:A"}, {"at": "B", "from": "C", "to": "D", "label": "{hb}°", "k": "arc:B1"}, {"at": "C", "from": "D", "to": "B", "label": "{hc}°", "k": "arc:C2"}, {"at": "D", "from": "C", "to": "B", "label": "{d}°", "k": "arc:D"}]}}}],
        sol1_anim=[[hl("arc:A", keep=True)], [hl("arc:B1", "arc:C2", keep=True)], [hl("arc:D", keep=True)]],
        sol2=[
            "∠B + ∠C = 180° − ∠A이고, BD·CD가 이등분선이므로 ∠DBC + ∠DCB = (∠B + ∠C) ÷ 2 = (180° − ∠A) ÷ 2",
            "△DBC에서 ∠BDC = 180° − (∠DBC + ∠DCB) = 180° − (180° − ∠A) ÷ 2 = 90° + ∠A ÷ 2",
            "{S3A}{gv}{S3B}{gv}{S3C}{mid}{S3D}{ans_v}°",
        ],
        sol2_fig=steps([
            {"text": "∠DBC + ∠DCB = (180° − ∠A) ÷ 2", "hint": "이등분선 — 절반씩"},
            {"text": "∠BDC = 90° + ∠A ÷ 2", "hint": "△DBC의 내각의 합", "marks": [{"on": "90°", "note": "180° − 90°"}]},
            {"text": "{S3A}{gv}{S3B}{gv}{S3C}{mid}{S3D}{ans_v}°"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="∠A = {a}°이면 ∠B + ∠C = {180 - a}°, ∠DBC + ∠DCB = {90 - a/2}°이고 △DBC에서 ∠BDC = 180° − {90 - a/2}° = {d}°로 관계가 맞는다. 답은 [[deg({ans_v})]]다.",
        model_answer="∠DBC + ∠DCB = (∠B + ∠C) ÷ 2 = (180° − ∠A) ÷ 2이므로 △DBC에서 ∠BDC = 180° − (180° − ∠A) ÷ 2 = 90° + ∠A ÷ 2다. {S3A}{gv}{S3B}{gv}{S3C}{mid}{S3D}{ans_v}°다.",
        rubric=[
            {"element": "이등분선과 각의 합", "points": 3, "criterion": "∠DBC + ∠DCB = (∠B + ∠C) ÷ 2 = (180° − ∠A) ÷ 2 임을 밝혔다.", "partial": "이등분선을 쓰지 않고 ∠B + ∠C만 썼으면 1점."},
            {"element": "관계식", "points": 2, "criterion": "△DBC의 내각의 합에서 ∠BDC = 90° + ∠A ÷ 2 를 얻었다.", "partial": "공식만 쓰고 유도가 없으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKAW}의 크기 {ans_v}°를 구했다.", "partial": "부호·절반 처리를 잘못했으면 1점."},
        ],
        rubric_total=7,
    )


TA_SEED = {
    "seed_id": TA, "category": "도형",
    "title": "삼각형의 각 2 — 세 각의 비·이등변 연쇄(3a)·두 내각의 이등분선(90° + A/2)",
    "unit_id": "m1-2", "concept_ids": ["m1-2-08"],
    "schema_id": None, "schema_name": "삼각형의 내각·외각의 응용",
    "source_item_ids": [],
    "note": "구조만 차용. 각은 scene 좌표를 삼각비로 계산해 실제 크기대로 그린다(세 각 ≥ 20°). 이등분선 교점은 내심 좌표(변 길이 가중 평균).",
    "geometry": True,
    "templates": [ta_t1(), ta_t2(), ta_t3()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 평행선 — 두 번 꺾인 선·종이 접기
PF = "m1-2-parallel-fold"
PF_BASE = {**GEO, "prereq": ["평행선의 성질(동위각·엇각)", "보조선"], "tags": ["평행선", "엇각", "보조선"]}
# 두 번 꺾인 선: l ∥ m, P(l) → B → C → Q(m). ∠(l, PB) = a, ∠PBC = x = a + β, ∠BCQ = c = β + d, ∠(CQ, m) = d  ⇒  x = a + c − d
UNK_ROWS = {"x": {"U": "x", "ASKA": "PBC", "S_a": 1, "S_x": 0, "S_c": 1, "S_d": 1},
            "a": {"U": "a", "ASKA": "QPB", "S_a": 0, "S_x": 1, "S_c": 1, "S_d": 1},
            "c": {"U": "c", "ASKA": "BCQ", "S_a": 1, "S_x": 1, "S_c": 0, "S_d": 1},
            "d": {"U": "d", "ASKA": "RQC", "S_a": 1, "S_x": 1, "S_c": 1, "S_d": 0}}


def pf_t1():
    return tpl(PF, 1, PF_BASE,
        title="평행선 사이에서 두 번 꺾인 선 — 보조선 두 개로 각 구하기",
        skill="꺾인 점마다 평행한 보조선을 그어 엇각으로 각을 나누고, 같은 쪽 각의 합이 같음(a + c = x + d)을 이용하기",
        variant_axis={"구하는 각": "∠PBC / ∠QPB / ∠BCQ / ∠RQC", "각": "25°~70°"},
        discriminates="두 꺾인 점에 각각 평행한 보조선을 긋고 엇각으로 각을 쪼개는가, 어느 쪽 각을 더하는지 방향을 지키는가",
        difficulty=3,
        params=[{"name": "u", "values": {"in": list(UNK_ROWS)}}, {"name": "a", "values": {"in": [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]}},
                {"name": "bt", "values": {"in": [20, 25, 30, 35, 40, 45, 50, 55]}}, {"name": "d", "values": {"in": [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]}}],
        table={"key": "u", "rows": UNK_ROWS},
        derive={"x": "a + bt", "c": "bt + d", "ans_v": "x*(S_x == 0) + a*(S_a == 0) + c*(S_c == 0) + d*(S_d == 0)",
                "bx": "cos(pi*a/180)/sin(pi*a/180)", "cx": "cos(pi*a/180)/sin(pi*a/180) - cos(pi*bt/180)/sin(pi*bt/180)", "qx": "cos(pi*a/180)/sin(pi*a/180) - cos(pi*bt/180)/sin(pi*bt/180) + cos(pi*d/180)/sin(pi*d/180)",
                "xlo": "min(0, cx) - 0.8", "xhi": "max(bx, qx) + 0.8"},
        constraints=["x <= 120", "c <= 120", "a != d", "a != c", "x != c", "ans_v != a or S_a == 0", "ans_v != x or S_x == 0", "ans_v != c or S_c == 0", "ans_v != d or S_d == 0", "xhi - xlo <= 7"],
        cost_values=["a", "x", "c", "d", "ans_v"],
        answer_var="ans_v",
        verify=["x + d == a + c", "ans == x*(S_x == 0) + a*(S_a == 0) + c*(S_c == 0) + d*(S_d == 0)"],
        question="다음 그림에서 [[par(l, m)]]이고 {G1}, {G2}, {G3}일 때, [[angle({ASKA})]]의 크기를 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"L1": ["{xlo}", 3], "L2": ["{xhi}", 3], "M1": ["{xlo}", 0], "M2": ["{xhi}", 0], "P": [0, 3], "B": ["{bx}", 2], "C": ["{cx}", 1], "Q": ["{qx}", 0], "R": ["{xlo}", 0]},
                                          "nodot": ["L1", "L2", "M1", "M2", "R"], "segs": [["L1", "L2"], ["M1", "M2"], ["P", "B"], ["B", "C"], ["C", "Q"]],
                                          "marks": {"arc": [{"at": "P", "from": "L2", "to": "B", "label": "{LA}", "k": "arc:P"}, {"at": "B", "from": "P", "to": "C", "label": "{LX}", "k": "arc:B"}, {"at": "C", "from": "B", "to": "Q", "label": "{LC}", "k": "arc:C"}, {"at": "Q", "from": "M1", "to": "C", "label": "{LD}", "k": "arc:Q"}]},
                                          "labels": [{"at": ["{xhi}", 3], "text": "l", "dx": 10, "dy": 4}, {"at": ["{xhi}", 0], "text": "m", "dx": 10, "dy": 4}]}}],
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="꺾인 점 B, C를 지나고 l에 평행한 보조선을 각각 그으면, 평행선의 엇각은 같으므로 ∠PBC는 ∠QPB와 같은 {a}°와 나머지 {bt}°로 나뉘고, ∠BCQ는 그 {bt}°와 ∠RQC와 같은 {d}°로 나뉜다. 그래서 ∠QPB + ∠BCQ = ∠PBC + ∠RQC, 곧 {a}° + {c}° = {x}° + {d}°가 성립한다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"L1": ["{xlo}", 3], "L2": ["{xhi}", 3], "M1": ["{xlo}", 0], "M2": ["{xhi}", 0], "P": [0, 3], "B": ["{bx}", 2], "C": ["{cx}", 1], "Q": ["{qx}", 0], "R": ["{xlo}", 0], "B1": ["{xlo}", 2], "B2": ["{xhi}", 2], "C1": ["{xlo}", 1], "C2": ["{xhi}", 1]},
                                           "nodot": ["L1", "L2", "M1", "M2", "R", "B1", "B2", "C1", "C2"], "segs": [["L1", "L2"], ["M1", "M2"], ["P", "B"], ["B", "C"], ["C", "Q"], {"a": "B1", "b": "B2", "style": "dashed"}, {"a": "C1", "b": "C2", "style": "dashed"}],
                                           "marks": {"arc": [{"at": "P", "from": "L2", "to": "B", "label": "{a}°", "k": "arc:P"}, {"at": "B", "from": "P", "to": "B1", "label": "{a}°", "k": "arc:B1"}, {"at": "B", "from": "B1", "to": "C", "k": "arc:B2"}, {"at": "C", "from": "B", "to": "C2", "label": "{bt}°", "k": "arc:C1"}, {"at": "C", "from": "C2", "to": "Q", "label": "{d}°", "k": "arc:C2"}, {"at": "Q", "from": "M1", "to": "C", "label": "{d}°", "k": "arc:Q"}]},
                                           "labels": [{"at": ["{xhi}", 3], "text": "l", "dx": 10, "dy": 4}, {"at": ["{xhi}", 0], "text": "m", "dx": 10, "dy": 4}]}}],
        sol1_anim=[[hl("seg:B1-B2", "seg:C1-C2", keep=True)], [hl("arc:P", "arc:B1")], [hl("arc:B2", "arc:C1")], [hl("arc:C2", "arc:Q")]],
        sol2=[
            "점 B, C를 지나고 l에 평행한 보조선을 긋는다.",
            "엇각이 같으므로 ∠PBC = {a}° + {bt}° = {x}°, ∠BCQ = {bt}° + {d}° = {c}°",
            "따라서 ∠QPB + ∠BCQ = ∠PBC + ∠RQC, 곧 {a}° + {c}° = {x}° + {d}°",
            "구하는 [[angle({ASKA})]] = {ans_v}°",
        ],
        sol2_fig=steps([
            {"text": "B, C를 지나는 평행한 보조선", "hint": "꺾인 점마다 하나씩"},
            {"text": "∠PBC = {a}° + {bt}°,  ∠BCQ = {bt}° + {d}°", "hint": "엇각", "marks": [{"on": "{bt}°", "note": "공통"}]},
            {"text": "{a}° + {c}° = {x}° + {d}°", "hint": "같은 쪽 각의 합"},
            {"text": "[[angle({ASKA})]] = {ans_v}°"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3)]],
        sol_check="{a}° + {c}° = {a + c}°, {x}° + {d}° = {x + d}°로 두 합이 같으므로 네 각이 평행선의 조건을 만족한다. 답은 [[deg({ans_v})]]다.",
        model_answer="점 B, C를 지나고 l에 평행한 보조선을 그으면 엇각에 의해 ∠PBC = {a}° + {bt}° = {x}°, ∠BCQ = {bt}° + {d}° = {c}°이므로 ∠QPB + ∠BCQ = ∠PBC + ∠RQC이다. 따라서 [[angle({ASKA})]] = {ans_v}°다.",
        rubric=[
            {"element": "보조선과 엇각", "points": 3, "criterion": "B, C를 지나는 평행한 보조선을 긋고 엇각이 같음을 이용해 각을 나누었다.", "partial": "보조선을 하나만 그었으면 1점."},
            {"element": "관계식", "points": 2, "criterion": "∠QPB + ∠BCQ = ∠PBC + ∠RQC(또는 각을 쪼갠 등식)를 세웠다.", "partial": "각의 합의 방향을 반대로 했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "[[angle({ASKA})]] = {ans_v}°를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


PF_T1_GIVEN = {
    "x": {"GA1": "[[angle(QPB) = deg({a})]]", "GA2": "[[angle(BCQ) = deg({c})]]", "GA3": "[[angle(RQC) = deg({d})]]", "LAV": "{a}°", "LXV": "x", "LCV": "{c}°", "LDV": "{d}°"},
    "a": {"GA1": "[[angle(PBC) = deg({x})]]", "GA2": "[[angle(BCQ) = deg({c})]]", "GA3": "[[angle(RQC) = deg({d})]]", "LAV": "x", "LXV": "{x}°", "LCV": "{c}°", "LDV": "{d}°"},
    "c": {"GA1": "[[angle(QPB) = deg({a})]]", "GA2": "[[angle(PBC) = deg({x})]]", "GA3": "[[angle(RQC) = deg({d})]]", "LAV": "{a}°", "LXV": "{x}°", "LCV": "x", "LDV": "{d}°"},
    "d": {"GA1": "[[angle(QPB) = deg({a})]]", "GA2": "[[angle(PBC) = deg({x})]]", "GA3": "[[angle(BCQ) = deg({c})]]", "LAV": "{a}°", "LXV": "{x}°", "LCV": "{c}°", "LDV": "x"},
}


def pf_t1_split():
    """미지수 자리마다 문면·라벨이 달라 표 문자열에 {식}을 둘 수 없다 → 미지수별로 틀 4개(t1~t4)."""
    out = []
    for no, (u, g) in enumerate(PF_T1_GIVEN.items(), start=1):
        t = pf_t1()
        t["id"] = f"{PF}-t{no}"
        t["params"] = [p for p in t["params"] if p["name"] != "u"]
        t.pop("table")
        row = UNK_ROWS[u]
        t["derive"] = {**{k: str(v) for k, v in row.items() if k.startswith("S_")}, **t["derive"]}
        t["title"] = t["title"] + f" ({row['ASKA']} 구하기)"
        from seedlib import sub_all
        t = sub_all(t, {"{ASKA}": row["ASKA"], "{G1}": g["GA1"], "{G2}": g["GA2"], "{G3}": g["GA3"], "{LA}": g["LAV"], "{LX}": g["LXV"], "{LC}": g["LCV"], "{LD}": g["LDV"]})
        out.append(t)
    return out


FOLD_ROWS = {"fwd": {"isF": 1}, "rev": {"isF": 0}}


def pf_t5():
    # 폭이 일정한 종이 테이프 접기: 접는 선 EF 와 윗변이 이루는 각 a → 접힌 부분이 아랫변과 이루는 각 x = 180° − 2a
    return tpl(PF, 5, PF_BASE,
        title="폭이 일정한 종이 테이프 접기 — 접은 각과 평행선의 엇각",
        skill="접은 각과 접힌 각이 같음(∠DEF = ∠GEF)과 평행선의 엇각(∠DEF = ∠EFB)을 함께 써서 각 구하기",
        variant_axis={"주어진 것": "접는 선의 각 a → x / x → a", "각": "55°~75°"},
        discriminates="접어 겹친 두 각이 같다는 것과 테이프의 두 변이 평행하다는 것을 모두 근거로 쓰는가",
        difficulty=3,
        params=[{"name": "w", "values": {"in": list(FOLD_ROWS)}}, {"name": "a", "values": {"in": [52, 54, 55, 56, 58, 62, 64, 65, 66, 68, 70, 72, 74, 75]}}],
        table={"key": "w", "rows": FOLD_ROWS},
        derive={"x": "180 - 2*a", "ans_v": "isF*(180 - 2*a) + (1 - isF)*a", "gv": "isF*a + (1 - isF)*(180 - 2*a)",
                "fx": "1.5*cos(pi*a/180)/sin(pi*a/180)", "gx": "1.5*cos(pi*2*a/180)/sin(pi*2*a/180)", "xlo": "min(gx, 0) - 1.2", "xhi": "fx + 1.5"},
        constraints=["x != a", "x >= 30"],
        cost_values=["a", "x", "ans_v"],
        answer_var="ans_v",
        verify=["x == 180 - 2*a", "isF == 0 or ans == x", "isF == 1 or ans == a"],
        question="다음 그림은 폭이 일정한 종이 테이프를 선분 EF를 접는 선으로 하여 접은 것이다. [[angle({GN}) = deg({gv})]]일 때, [[angle({AN})]]의 크기를 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"A": ["{xlo}", 1.5], "D": ["{xhi}", 1.5], "B": ["{xlo}", 0], "C": ["{xhi}", 0], "E": [0, 1.5], "F": ["{fx}", 0], "G": ["{gx}", 0]},
                                          "nodot": ["A", "B", "C", "D"], "segs": [["A", "D"], ["B", "C"], ["E", "F"], ["E", "G"], ["G", "F"]],
                                          "marks": {"arc": [{"at": "E", "from": "D", "to": "F", "label": "{LA}", "k": "arc:E"}, {"at": "G", "from": "C", "to": "E", "label": "{LX}", "k": "arc:G"}]}}}],
        answer="[[deg({ans_v})]]", answer_alt=["{ans_v}°", "{ans_v}"],
        sol1="종이를 접으면 접힌 부분은 원래 부분과 포개지므로 ∠GEF = ∠DEF다. 또 테이프의 두 변 AD, BC는 평행하므로 ∠EFB는 ∠DEF의 엇각으로 같다. 그러면 △EFG에서 ∠GEF + ∠EFG를 180°에서 빼면 ∠EGF, 곧 아랫변과 접힌 변이 이루는 각이 나온다.",
        sol1_fig=[{"fn": "scene", "args": {"pts": {"A": ["{xlo}", 1.5], "D": ["{xhi}", 1.5], "B": ["{xlo}", 0], "C": ["{xhi}", 0], "E": [0, 1.5], "F": ["{fx}", 0], "G": ["{gx}", 0]},
                                           "nodot": ["A", "B", "C", "D"], "segs": [["A", "D"], ["B", "C"], ["E", "F"], ["E", "G"], ["G", "F"]],
                                           "marks": {"arc": [{"at": "E", "from": "D", "to": "F", "label": "{a}°", "k": "arc:E1"}, {"at": "E", "from": "F", "to": "G", "label": "{a}°", "k": "arc:E2"}, {"at": "F", "from": "E", "to": "B", "label": "{a}°", "k": "arc:F"}, {"at": "G", "from": "C", "to": "E", "label": "{x}°", "k": "arc:G"}]}}}],
        sol1_anim=[[hl("arc:E1", "arc:E2", keep=True)], [hl("arc:F", keep=True)], [hl("arc:G", keep=True)]],
        sol2=[
            "접은 각과 접힌 각은 같으므로 ∠GEF = ∠DEF = {a}°",
            "AD ∥ BC이므로 엇각에 의해 ∠EFG = ∠DEF = {a}°",
            "△EFG에서 ∠EGF = 180° − {a}° − {a}° = {x}°",
            "따라서 [[angle({AN})]] = {ans_v}°",
        ],
        sol2_fig=steps([
            {"text": "∠GEF = ∠DEF = {a}°", "hint": "접은 각 = 접힌 각"},
            {"text": "∠EFG = ∠DEF = {a}°", "hint": "AD ∥ BC — 엇각"},
            {"text": "∠EGF = 180° − 2 × {a}° = {x}°", "hint": "삼각형의 내각의 합", "marks": [{"on": "2 × {a}°", "note": "같은 각 두 개"}]},
            {"text": "[[angle({AN})]] = {ans_v}°"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]],
        sol_check="△EFG의 세 각 {a}° + {a}° + {x}° = 180°로 맞고, ∠DEF와 ∠GEF가 같으므로 접었을 때 겹친다. 답은 [[deg({ans_v})]]다.",
        model_answer="접은 각과 접힌 각이 같으므로 ∠GEF = ∠DEF = {a}°이고, AD ∥ BC이므로 엇각 ∠EFG = {a}°다. △EFG에서 ∠EGF = 180° − 2 × {a}° = {x}°이므로 [[angle({AN})]] = {ans_v}°다.",
        rubric=[
            {"element": "접은 각의 성질", "points": 3, "criterion": "접었을 때 겹치는 두 각(∠GEF = ∠DEF)이 같음을 밝혔다.", "partial": "근거 없이 같다고만 썼으면 1점."},
            {"element": "평행선의 엇각", "points": 2, "criterion": "AD ∥ BC에서 엇각 ∠EFG = ∠DEF임을 밝혔다.", "partial": "동위각·엇각의 위치를 잘못 잡았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "삼각형의 내각의 합으로 [[angle({AN})]] = {ans_v}°를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


def pf_t5_split():
    out = []
    for no, (w, gn, an, la, lx) in enumerate([("fwd", "DEF", "EGC", "{a}°", "x"), ("rev", "EGC", "DEF", "x", "{x}°")], start=5):
        t = pf_t5()
        t["id"] = f"{PF}-t{no}"
        t["params"] = [p for p in t["params"] if p["name"] != "w"]
        t.pop("table")
        t["derive"] = {"isF": "1" if w == "fwd" else "0", **t["derive"]}
        from seedlib import sub_all
        t = sub_all(t, {"{GN}": gn, "{AN}": an, "{LA}": la, "{LX}": lx})
        t["title"] = t["title"] + (" (접은 각 → x)" if w == "fwd" else " (x → 접은 각)")
        out.append(t)
    return out


PF_SEED = {
    "seed_id": PF, "category": "도형",
    "title": "평행선의 응용 — 두 번 꺾인 선(보조선 두 개)·종이 테이프 접기",
    "unit_id": "m1-2", "concept_ids": ["m1-2-04"],
    "schema_id": None, "schema_name": "평행선의 성질의 응용(보조선·접기)",
    "source_item_ids": [],
    "note": "구조만 차용. 꺾인 선은 세 각(a, β, d)에서 좌표를 코탄젠트로 계산해 관계 x = a + c − d 가 항상 성립. 미지수 자리별로 틀을 나눴다(문면·라벨이 달라서). 접기는 x = 180° − 2a.",
    "geometry": True,
    "templates": pf_t1_split() + pf_t5_split(),
}


# ═══════════════════════════════════════════════════════════════════ 3. 색칠한 부분의 넓이·둘레 (부채꼴 조합)
SS = "m1-2-sector-shade"
SS_BASE = {**GEO, "process": "절차수행", "ops": ["넓이", "비례"], "prereq": ["부채꼴의 호의 길이와 넓이", "원의 넓이"], "tags": ["부채꼴", "색칠한 부분의 넓이"], "traps": ["구하는대상혼동", "단위"]}
THETAS = [30, 45, 60, 90, 120, 135, 150, 180, 270]


def ss_t1():
    return tpl(SS, 1, SS_BASE,
        title="같은 중심각의 두 부채꼴로 둘러싸인 고리 모양 도형의 넓이",
        skill="큰 부채꼴의 넓이에서 작은 부채꼴의 넓이를 빼기 — πr² × (중심각/360°)",
        variant_axis={"중심각": "30°~270°", "반지름": "1~12"},
        discriminates="두 부채꼴의 넓이를 각각 구해 빼는가(반지름의 차로 계산하지 않는가), 중심각의 비율을 곱하는가",
        difficulty=2,
        params=[{"name": "th", "values": {"in": THETAS}}, {"name": "R", "values": {"int": [3, 16]}}, {"name": "r", "values": {"int": [1, 14]}}],
        derive={"kR": "R*R*th/360", "kr": "r*r*th/360", "k": "(R*R - r*r)*th/360"},
        constraints=["r < R", "r >= 2", "R - r >= 2", "k == floor(k)", "k != R", "k != r", "k != th", "k <= 400"],
        cost_values=["th", "R", "r", "k"],
        answer_var="k",
        verify=["ans*360 == (R*R - r*r)*th"],
        question="중심이 O로 같고 중심각의 크기가 [[deg({th})]]로 같은 두 부채꼴 OAB, OCD의 반지름의 길이가 각각 {R} cm, {r} cm일 때, 두 부채꼴 사이의 고리 모양 도형의 넓이를 구하시오.",
        figure=[{"fn": "sector", "args": {"r": "{R}", "angle": "{th}"}}],
        answer="[[{k} * pi]]", answer_alt=["[[{k} * pi]] cm²"],
        sol1="고리 모양은 큰 부채꼴 OAB에서 작은 부채꼴 OCD를 잘라 낸 것이므로 두 부채꼴의 넓이의 차가 넓이다. 부채꼴의 넓이는 πr² × (중심각/360°)이며, 두 부채꼴의 중심각이 같으므로 비율 [[frac({th},360)]]{eun(360)} 공통이다.",
        sol2=[
            "큰 부채꼴 OAB의 넓이: π × {R}² × [[frac({th},360)]] = {kR}π (cm²)",
            "작은 부채꼴 OCD의 넓이: π × {r}² × [[frac({th},360)]] = {kr}π (cm²)",
            "따라서 고리 모양 도형의 넓이는 {kR}π − {kr}π = {k}π (cm²)",
        ],
        sol2_fig=steps([
            {"text": "큰 부채꼴: π × {R}² × [[frac({th},360)]] = {kR}π", "hint": "πr² × 중심각/360°"},
            {"text": "작은 부채꼴: π × {r}² × [[frac({th},360)]] = {kr}π"},
            {"text": "{kR}π − {kr}π = {k}π", "hint": "큰 것 − 작은 것", "marks": [{"on": "{k}π", "note": "반지름의 차로 계산하지 말 것"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol_check="π({R}² − {r}²) × [[frac({th},360)]] = π × {R*R - r*r} × [[frac({th},360)]] = {k}π로 같다. 답은 [[{k} * pi]] cm²다.",
        model_answer="큰 부채꼴의 넓이는 π × {R}² × [[frac({th},360)]] = {kR}π cm², 작은 부채꼴의 넓이는 π × {r}² × [[frac({th},360)]] = {kr}π cm²이므로 고리 모양 도형의 넓이는 {kR}π − {kr}π = {k}π cm²이다.",
        rubric=[
            {"element": "두 부채꼴의 넓이", "points": 3, "criterion": "두 부채꼴의 넓이 {kR}π, {kr}π를 πr² × (중심각/360°)로 구했다.", "partial": "중심각의 비율을 빠뜨리고 원의 넓이로 계산했으면 인정하지 않고, 하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "큰 것에서 작은 것을 빼 {k}π cm²를 구했다.", "partial": "반지름의 차 {R - r}{ro(R - r)} 부채꼴 넓이를 구했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def ss_t2():
    return tpl(SS, 2, SS_BASE,
        title="고리 모양 도형의 둘레 — (aπ + b) 꼴의 a + b",
        skill="두 호의 길이(2πr × 중심각/360°)와 반지름의 차 두 개를 더해 둘레를 구하기",
        variant_axis={"중심각": "30°~270°", "반지름": "1~12"},
        discriminates="둘레에 두 호뿐 아니라 직선 부분(반지름의 차) 두 개를 포함하는가",
        difficulty=3,
        params=[{"name": "th", "values": {"in": THETAS}}, {"name": "R", "values": {"int": [3, 16]}}, {"name": "r", "values": {"int": [1, 14]}}],
        derive={"aR": "2*R*th/360", "ar": "2*r*th/360", "ka": "2*(R + r)*th/360", "kb": "2*(R - r)", "ans": "ka + kb"},
        constraints=["r < R", "r >= 2", "R - r >= 2", "ka == floor(ka)", "ans != R", "ans != r", "ans != th", "ka != kb", "ans != ka", "ans != kb"],
        cost_values=["th", "R", "r", "ka", "kb", "ans"],
        answer_var="ans",
        verify=["ans == 2*(R + r)*th/360 + 2*(R - r)"],
        question="중심이 O로 같고 중심각의 크기가 [[deg({th})]]로 같은 두 부채꼴 OAB, OCD의 반지름의 길이가 각각 {R} cm, {r} cm이다. 두 부채꼴 사이의 고리 모양 도형의 둘레의 길이가 (aπ + b) cm일 때, a + b의 값을 구하시오. (단, a, b는 자연수)",
        figure=[{"fn": "sector", "args": {"r": "{R}", "angle": "{th}"}}],
        answer="{ans}", answer_alt=[],
        sol1="고리 모양의 둘레는 바깥 호 AB, 안쪽 호 CD, 그리고 두 직선 부분 AC, BD로 이루어진다. 호의 길이는 2πr × (중심각/360°)이고, 직선 부분은 각각 반지름의 차 {R} − {r} = {R - r} cm다. 둘레를 (aπ + b) 꼴로 정리한 뒤 a + b를 구한다.",
        sol2=[
            "바깥 호 AB의 길이: 2π × {R} × [[frac({th},360)]] = {aR}π (cm)",
            "안쪽 호 CD의 길이: 2π × {r} × [[frac({th},360)]] = {ar}π (cm)",
            "직선 부분은 두 개이고 각각 {R} − {r} = {R - r} (cm)이므로 {kb} cm",
            "둘레 = {aR}π + {ar}π + {kb} = {ka}π + {kb} (cm)이므로 a = {ka}, b = {kb}, a + b = {ans}",
        ],
        sol2_fig=steps([
            {"text": "호 AB = {aR}π,  호 CD = {ar}π", "hint": "2πr × 중심각/360°"},
            {"text": "직선 부분 = {R - r} × 2 = {kb}", "hint": "반지름의 차 두 개", "marks": [{"on": "× 2", "note": "빠뜨리기 쉬움"}]},
            {"text": "둘레 = {ka}π + {kb}  →  a + b = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="두 호 {aR}π + {ar}π = {ka}π와 직선 부분 {kb}{ro(kb)} 둘레가 {ka}π + {kb}이고, a = {ka}, b = {kb}이므로 a + b = {ans}이다. 답은 {ans}이다.",
        model_answer="바깥 호는 2π × {R} × [[frac({th},360)]] = {aR}π cm, 안쪽 호는 {ar}π cm, 직선 부분은 ({R} − {r}) × 2 = {kb} cm이므로 둘레는 {ka}π + {kb} cm이다. 따라서 a = {ka}, b = {kb}이고 a + b = {ans}이다.",
        rubric=[
            {"element": "두 호의 길이", "points": 3, "criterion": "두 호의 길이 {aR}π, {ar}π를 2πr × (중심각/360°)로 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "직선 부분", "points": 2, "criterion": "반지름의 차 {R - r} cm 두 개, 곧 {kb} cm를 둘레에 넣었다.", "partial": "하나만 넣었으면 1점, 넣지 않았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "둘레 {ka}π + {kb}에서 a + b = {ans}{eul(ans)} 구했다.", "partial": "a, b를 바꿔 썼거나 더하지 않았으면 1점."},
        ],
        rubric_total=7,
    )


def ss_t3():
    return tpl(SS, 3, SS_BASE,
        title="정사각형에서 사분원을 뺀 부분의 넓이 — (p − qπ) 꼴의 p + q",
        skill="정사각형의 넓이에서 반지름이 한 변인 사분원(중심각 90°)의 넓이를 빼기",
        variant_axis={"한 변": "2~16 (짝수)"},
        discriminates="사분원의 넓이를 πr² × 1/4로 구하는가, 정사각형에서 빼는 것을 (p − qπ) 꼴로 정리하는가",
        difficulty=2,
        params=[{"name": "m", "values": {"int": [1, 8]}}],
        derive={"a": "2*m", "P": "4*m*m", "Q": "m*m", "ans": "5*m*m"},
        constraints=["ans != a", "P != a"],
        cost_values=["a", "P", "Q", "ans"],
        answer_var="ans",
        verify=["ans == a*a + a*a/4", "P == a*a", "4*Q == a*a"],
        question="한 변의 길이가 {a} cm인 정사각형 ABCD에서 꼭짓점 A를 중심으로 하고 반지름의 길이가 {a} cm인 사분원(부채꼴)을 그렸다. 정사각형에서 이 사분원을 뺀 부분의 넓이가 (p − qπ) cm²일 때, p + q의 값을 구하시오. (단, p, q는 자연수)",
        figure=[{"fn": "sector", "args": {"r": "{a}", "angle": 90}}],
        answer="{ans}", answer_alt=[],
        sol1="구하는 넓이는 (정사각형의 넓이) − (사분원의 넓이)다. 사분원은 중심각이 90°인 부채꼴이므로 넓이는 π × {a}² × [[frac(90,360)]] = π × {a}² × [[frac(1,4)]]이다. 두 넓이를 각각 구해 (p − qπ) 꼴로 쓴다.",
        sol2=[
            "정사각형의 넓이: {a} × {a} = {P} (cm²)",
            "사분원의 넓이: π × {a}² × [[frac(1,4)]] = {Q}π (cm²)",
            "따라서 구하는 넓이는 ({P} − {Q}π) cm²이고 p = {P}, q = {Q}, p + q = {ans}",
        ],
        sol2_fig=steps([
            {"text": "정사각형 = {a}² = {P}"},
            {"text": "사분원 = π × {a}² × [[frac(1,4)]] = {Q}π", "hint": "중심각 90° = 원의 1/4", "marks": [{"on": "[[frac(1,4)]]", "note": "90/360"}]},
            {"text": "{P} − {Q}π  →  p + q = {ans}"},
        ]),
        sol2_anim=[[reveal(0)], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="사분원의 넓이 {Q}π(약 {dec(314*Q/100)})는 정사각형의 넓이 {P}보다 작아 뺄 수 있고, p = {P}, q = {Q}이므로 p + q = {ans}이다. 답은 {ans}이다.",
        model_answer="정사각형의 넓이는 {a} × {a} = {P} cm², 사분원의 넓이는 π × {a}² × [[frac(1,4)]] = {Q}π cm²이므로 구하는 넓이는 ({P} − {Q}π) cm²이다. 따라서 p = {P}, q = {Q}이고 p + q = {ans}이다.",
        rubric=[
            {"element": "사분원의 넓이", "points": 3, "criterion": "중심각 90°의 부채꼴 넓이 π × {a}² × [[frac(1,4)]] = {Q}π{eul(Q)} 구했다.", "partial": "[[frac(1,4)]]{eul(4)} 빠뜨렸으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{P} − {Q}π에서 p + q = {ans}{eul(ans)} 구했다.", "partial": "p, q를 구하고 더하지 않았으면 1점."},
        ],
        rubric_total=5,
    )


def ss_t4():
    # 지름 AB 위의 점 C, 세 반원: 색칠 부분(큰 반원 − 두 작은 반원) = π r1 r2
    return tpl(SS, 4, SS_BASE,
        title="지름 위의 점으로 만든 세 반원 — 큰 반원에서 두 반원을 뺀 넓이",
        skill="세 반원의 넓이를 πr² ÷ 2로 각각 구하고 큰 것에서 두 작은 것을 빼기",
        variant_axis={"두 작은 반원의 반지름": "1~9"},
        discriminates="반원의 넓이를 원의 절반으로 구하는가, 지름과 반지름을 혼동하지 않는가",
        difficulty=3,
        params=[{"name": "r1", "values": {"int": [1, 9]}}, {"name": "r2", "values": {"int": [1, 9]}}],
        derive={"d1": "2*r1", "d2": "2*r2", "R": "r1 + r2", "kB": "(r1 + r2)*(r1 + r2)/2", "k1": "r1*r1/2", "k2": "r2*r2/2", "k": "r1*r2"},
        constraints=["r1 < r2", "r1 >= 2", "k != d1", "k != d2", "k != R"],
        cost_values=["d1", "d2", "R", "k"],
        answer_var="k",
        verify=["ans == (R*R - r1*r1 - r2*r2)/2", "ans == r1*r2"],
        question="선분 AB 위의 점 C에 대하여 [[seg(AC)]] = {d1} cm, [[seg(CB)]] = {d2} cm이다. 선분 AB, AC, CB를 각각 지름으로 하는 세 반원을 같은 쪽에 그렸을 때, 큰 반원에서 두 작은 반원을 뺀 부분의 넓이를 구하시오.",
        answer="[[{k} * pi]]", answer_alt=["[[{k} * pi]] cm²"],
        sol1="반원의 넓이는 원의 넓이의 절반 πr² ÷ 2이며, 지름이 주어졌으므로 반지름은 그 절반이다. AB = {d1} + {d2} = {2*R} cm이므로 큰 반원의 반지름은 {R} cm, 두 작은 반원의 반지름은 {r1} cm, {r2} cm다. 큰 반원에서 두 작은 반원을 뺀다.",
        sol2=[
            "AB = {d1} + {d2} = {2*R} (cm)이므로 세 반원의 반지름은 각각 {R} cm, {r1} cm, {r2} cm",
            "큰 반원: π × {R}² ÷ 2 = {kB}π, 작은 반원: π × {r1}² ÷ 2 = {k1}π, π × {r2}² ÷ 2 = {k2}π (cm²)",
            "따라서 구하는 넓이는 {kB}π − {k1}π − {k2}π = {k}π (cm²)",
        ],
        sol2_fig=steps([
            {"text": "반지름: {R}, {r1}, {r2}", "hint": "지름의 절반", "marks": [{"on": "{R}", "note": "({d1}+{d2})÷2"}]},
            {"text": "{kB}π − {k1}π − {k2}π", "hint": "반원 = πr² ÷ 2"},
            {"text": "= {k}π"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol_check="{R}² − {r1}² − {r2}² = {R*R - r1*r1 - r2*r2} = 2 × {r1} × {r2}이므로 넓이는 π × {r1} × {r2} = {k}π로 같다. 답은 [[{k} * pi]] cm²다.",
        model_answer="세 반원의 반지름은 각각 {R} cm, {r1} cm, {r2} cm이므로 넓이는 π × {R}² ÷ 2 − π × {r1}² ÷ 2 − π × {r2}² ÷ 2 = {kB}π − {k1}π − {k2}π = {k}π cm²이다.",
        rubric=[
            {"element": "반지름 읽기", "points": 2, "criterion": "세 반원의 반지름 {R}, {r1}, {r2}{eul(r2)} 지름의 절반으로 구했다.", "partial": "지름을 그대로 반지름으로 썼으면 인정하지 않는다."},
            {"element": "반원의 넓이", "points": 3, "criterion": "세 반원의 넓이 {kB}π, {k1}π, {k2}π를 πr² ÷ 2로 구했다.", "partial": "÷ 2를 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{kB}π − {k1}π − {k2}π = {k}π를 구했다.", "partial": "두 작은 반원 중 하나만 뺐으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


SS_SEED = {
    "seed_id": SS, "category": "도형",
    "title": "색칠한 부분의 넓이·둘레 — 고리 넓이·고리 둘레(a + b)·정사각형 − 사분원(p + q)·세 반원",
    "unit_id": "m1-2", "concept_ids": ["m1-2-11"],
    "schema_id": None, "schema_name": "부채꼴의 넓이·호의 길이의 응용(색칠한 부분)",
    "source_item_ids": [],
    "note": "구조만 차용. 겹친 도형은 렌더러가 그리지 못해 큰 부채꼴 하나만 그리거나 그림 없이 문장으로 둔다. π와 정수가 섞인 답은 a + b 꼴로 수치화.",
    "geometry": True,
    "templates": [ss_t1(), ss_t2(), ss_t3(), ss_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 4. 삼각형의 세 변의 조건
TS = "m1-2-tri-sides"
TS_BASE = {**GEO, "process": "추론", "ops": ["부등식", "개수 세기"], "prereq": ["삼각형의 결정 조건", "삼각형의 세 변의 길이 사이의 관계"], "tags": ["삼각형의 작도", "세 변의 조건"], "traps": ["조건누락"]}


def ts_t1():
    return tpl(TS, 1, TS_BASE,
        title="세 변의 길이가 a, b, x인 삼각형 — 자연수 x의 개수",
        skill="(가장 긴 변) < (나머지 두 변의 합)을 x가 가장 긴 경우와 아닌 경우로 나누어 x의 범위를 구하고 자연수를 세기",
        variant_axis={"두 변": "2~15"},
        discriminates="x가 가장 긴 변인 경우와 아닌 경우를 모두 따져 |a − b| < x < a + b 를 얻는가, 양 끝을 빼고 세는가",
        difficulty=3,
        params=[{"name": "a", "values": {"int": [2, 15]}}, {"name": "b", "values": {"int": [2, 15]}}],
        derive={"lo": "abs(a - b)", "hi": "a + b", "cnt": "2*min(a, b) - 1", "mn": "min(a, b)", "mx": "max(a, b)"},
        constraints=["a != b", "cnt != a", "cnt != b", "cnt >= 3"],
        cost_values=["a", "b", "lo", "hi", "cnt"],
        answer_var="cnt",
        verify=["ans == hi - lo - 1", "ans == 2*mn - 1"],
        question="세 변의 길이가 {a} cm, {b} cm, x cm인 삼각형을 만들 수 있는 자연수 x는 모두 몇 개인지 구하시오.",
        answer="{cnt}", answer_alt=["{cnt}개"],
        sol1="삼각형이 되려면 가장 긴 변의 길이가 나머지 두 변의 길이의 합보다 작아야 한다. 어느 변이 가장 긴지 모르므로 두 경우로 나눈다: x가 가장 긴 변이면 x < {a} + {b}, x가 가장 긴 변이 아니면 (더 긴 변) < x + (짧은 변), 곧 x > {lo}. 두 조건을 합쳐 {lo} < x < {hi}에서 자연수를 센다.",
        sol2=[
            "x가 가장 긴 변일 때: x < {a} + {b} = {hi}",
            "x가 가장 긴 변이 아닐 때: {max(a, b)} < x + {mn}, 곧 x > {lo}",
            "따라서 {lo} < x < {hi}이고, 이를 만족하는 자연수 x는 {lo + 1}, {lo + 2}, …, {hi - 1}",
            "그 개수는 {hi - 1} − {lo + 1} + 1 = {cnt}",
        ],
        sol2_fig=steps([
            {"text": "x < {a} + {b} = {hi}", "hint": "x가 가장 긴 변"},
            {"text": "x > {max(a, b)} − {mn} = {lo}", "hint": "x가 가장 긴 변이 아님"},
            {"text": "{lo} < x < {hi}", "marks": [{"on": "<", "note": "양 끝은 안 됨"}]},
            {"text": "개수: {cnt}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")], [reveal(3)]],
        sol3="x = {lo}이면 {mn} + {lo} = {mx}{ro(mx)} 두 변의 합이 나머지 변과 같아 삼각형이 되지 않고, x = {hi}도 마찬가지이므로 양 끝은 뺀다. {lo + 1}부터 {hi - 1}까지 자연수는 {cnt}개다. 답은 {cnt}개다.",
        model_answer="x가 가장 긴 변이면 x < {a} + {b} = {hi}, 아니면 {max(a, b)} < x + {mn}에서 x > {lo}이다. 따라서 {lo} < x < {hi}이고 자연수 x는 {lo + 1}부터 {hi - 1}까지 {cnt}개다.",
        rubric=[
            {"element": "삼각형의 조건", "points": 3, "criterion": "가장 긴 변이 나머지 두 변의 합보다 작아야 함을 두 경우로 나누어 x < {hi}, x > {lo}를 얻었다.", "partial": "한 경우만 따졌으면 1점."},
            {"element": "범위", "points": 2, "criterion": "{lo} < x < {hi}{ro(hi)} 정리했다.", "partial": "등호를 포함했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "자연수 x의 개수 {cnt}개를 구했다.", "partial": "양 끝을 포함해 셌으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def ts_t2():
    return tpl(TS, 2, TS_BASE,
        title="세 변의 길이가 a, b, x인 삼각형 — x의 범위 p < x < q에서 p + q",
        skill="삼각형의 세 변의 조건에서 x의 범위 |a − b| < x < a + b 를 구하기",
        variant_axis={"두 변": "3~20"},
        discriminates="범위의 아래 끝을 두 변의 차로, 위 끝을 두 변의 합으로 잡는가",
        difficulty=2,
        params=[{"name": "a", "values": {"int": [3, 20]}}, {"name": "b", "values": {"int": [3, 20]}}],
        derive={"p": "abs(a - b)", "q": "a + b", "ans": "abs(a - b) + a + b", "mn": "min(a, b)", "mx": "max(a, b)"},
        constraints=["a != b", "ans != a", "ans != b", "p >= 2"],
        cost_values=["a", "b", "p", "q", "ans"],
        answer_var="ans",
        verify=["ans == 2*max(a, b)", "ans == p + q"],
        question="세 변의 길이가 {a} cm, {b} cm, x cm인 삼각형이 있다. x의 값의 범위가 p < x < q일 때, p + q의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="삼각형의 세 변 사이에는 (가장 긴 변) < (나머지 두 변의 합)이 성립한다. x가 가장 긴 변이면 x < {a} + {b}, 그렇지 않으면 {mx} < x + {mn}이므로 x > {mx} − {mn}이다. 두 조건에서 x의 범위가 나온다.",
        sol2=[
            "x가 가장 긴 변일 때 x < {a} + {b} = {q}",
            "x가 가장 긴 변이 아닐 때 {mx} < x + {mn}, x > {mx} − {mn} = {p}",
            "따라서 {p} < x < {q}이므로 p = {p}, q = {q}, p + q = {ans}",
        ],
        sol2_fig=steps([
            {"text": "x < {a} + {b} = {q}", "hint": "두 변의 합"},
            {"text": "x > {mx} − {mn} = {p}", "hint": "두 변의 차", "marks": [{"on": "{p}", "note": "큰 것 − 작은 것"}]},
            {"text": "p + q = {p} + {q} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="p + q = ({mx} − {mn}) + ({mx} + {mn}) = 2 × {mx} = {ans}로 큰 변의 2배와 같다. 답은 {ans}이다.",
        model_answer="x < {a} + {b} = {q}이고 x > {mx} − {mn} = {p}이므로 {p} < x < {q}이다. 따라서 p + q = {ans}이다.",
        rubric=[
            {"element": "범위 구하기", "points": 3, "criterion": "삼각형의 조건으로 {p} < x < {q}{eul(q)} 얻었다.", "partial": "위 끝만 구했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "p + q = {ans}{eul(ans)} 구했다.", "partial": "p와 q를 바꿔 적었어도 합이 맞으면 2점, 계산 실수면 1점."},
        ],
        rubric_total=5,
    )


TS_SEED = {
    "seed_id": TS, "category": "도형",
    "title": "삼각형의 세 변의 조건 — 자연수 x의 개수·범위 p + q",
    "unit_id": "m1-2", "concept_ids": ["m1-2-05"],
    "schema_id": None, "schema_name": "삼각형의 결정 조건(세 변의 길이)",
    "source_item_ids": [],
    "note": "구조만 차용. 그림 없음(D3 경고). 개수 = 2·min − 1, p + q = 2·max.",
    "geometry": False,
    "templates": [ts_t1(), ts_t2()],
}


# ═══════════════════════════════════════════════════════════════════ 5. 구의 응용
SP = "m1-2-sphere-apply"
SP_BASE = {**GEO, "process": "문제해결", "ops": ["부피", "비례"], "prereq": ["구의 부피", "원기둥의 부피"], "tags": ["구", "부피", "원기둥"], "traps": ["구하는대상혼동", "단위"]}
CY_ASK = {"cyl": {"ASK": "원기둥의 부피", "mul": 3, "WHAT": "원기둥", "REL": "원기둥의 높이는 구의 지름 2r이므로 원기둥의 부피는 πr² × 2r = 2πr³"},
          "gap": {"ASK": "원기둥에서 구를 뺀 빈 공간의 부피", "mul": 1, "WHAT": "빈 공간", "REL": "원기둥의 부피 2πr³에서 구의 부피를 빼면 빈 공간은 2πr³ − [[frac(4,3)]]πr³ = [[frac(2,3)]]πr³"},
          "cone": {"ASK": "원기둥에 꼭 맞게 들어가는 원뿔의 부피", "mul": 1, "WHAT": "원뿔", "REL": "원뿔의 부피는 [[frac(1,3)]] × πr² × 2r = [[frac(2,3)]]πr³"}}


def sp_t1():
    return tpl(SP, 1, SP_BASE,
        title="원기둥에 꼭 맞게 들어 있는 구 — 원기둥·빈 공간·원뿔의 부피",
        skill="구가 원기둥에 꼭 맞으면 원기둥의 밑면 반지름은 r, 높이는 2r임을 이용해 부피를 비교하기 (원뿔 : 구 : 원기둥 = 1 : 2 : 3)",
        variant_axis={"구하는 것": "원기둥 / 빈 공간 / 원뿔", "반지름": "3의 배수"},
        discriminates="원기둥의 높이를 구의 지름으로 잡는가, 구의 부피 공식 4/3 πr³을 정확히 쓰는가",
        difficulty=3,
        params=[{"name": "w", "values": {"in": list(CY_ASK)}}, {"name": "m", "values": {"int": [1, 5]}}],
        table={"key": "w", "rows": CY_ASK},
        derive={"r": "3*m", "h": "6*m", "ks": "4*r*r*r/3", "kc": "2*r*r*r", "kg": "2*r*r*r/3", "k": "mul*2*r*r*r/3"},
        constraints=["k != r", "k != h", "k != ks"],
        cost_values=["r", "ks", "k"],
        answer_var="k",
        verify=["ans*3 == mul*2*r**3", "ks*3 == 4*r**3"],
        question="반지름의 길이가 {r} cm인 구가 원기둥 모양의 통에 꼭 맞게 들어 있다. 이 {ASK}를 구하시오.",
        figure=[{"fn": "solid", "args": {"kind": "cylinder", "radius": "{r} cm", "height": "{h} cm"}}],
        answer="[[{k} * pi]]", answer_alt=["[[{k} * pi]] cm³"],
        sol1="구가 원기둥에 꼭 맞게 들어 있으므로 원기둥의 밑면의 반지름은 구의 반지름 {r} cm와 같고, 높이는 구의 지름 {h} cm다. 구의 부피는 [[frac(4,3)]]πr³ = {ks}π cm³이고, {REL}이다.",
        sol1_fig=[{"fn": "solid", "args": {"kind": "cylinder", "radius": "r = {r}", "height": "2r = {h}"}}],
        sol1_anim=[[hl("radius", "r-lbl")], [hl("height", "h-lbl", keep=True)]],
        sol2=[
            "원기둥의 밑면의 반지름은 {r} cm, 높이는 구의 지름 2 × {r} = {h} (cm)",
            "구의 부피: [[frac(4,3)]] × π × {r}³ = {ks}π (cm³), 원기둥의 부피: π × {r}² × {h} = {kc}π (cm³)",
            "따라서 {ASK}는 {k}π cm³",
        ],
        sol2_fig=steps([
            {"text": "밑면 반지름 {r}, 높이 {h}", "hint": "높이 = 구의 지름", "marks": [{"on": "{h}", "note": "2r"}]},
            {"text": "구 = [[frac(4,3)]]π × {r}³ = {ks}π,  원기둥 = π × {r}² × {h} = {kc}π"},
            {"text": "{ASK} = {k}π"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1)], [reveal(2)]],
        sol_check="원뿔 : 구 : 원기둥 = 1 : 2 : 3이므로 구의 부피 {ks}π에서 원기둥은 그 [[frac(3,2)]]배 {kc}π, 원뿔과 빈 공간은 그 절반 {kg}π다. 답은 [[{k} * pi]] cm³다.",
        model_answer="원기둥의 밑면의 반지름은 {r} cm, 높이는 {h} cm이므로 구의 부피는 {ks}π cm³, 원기둥의 부피는 {kc}π cm³이다. 따라서 {ASK}는 {k}π cm³이다.",
        rubric=[
            {"element": "원기둥의 치수", "points": 2, "criterion": "원기둥의 밑면 반지름 {r} cm, 높이 {h} cm(구의 지름)를 밝혔다.", "partial": "높이를 반지름과 같게 잡았으면 인정하지 않는다."},
            {"element": "부피 계산", "points": 3, "criterion": "구의 부피 {ks}π, 원기둥의 부피 {kc}π를 공식으로 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK} {k}π cm³를 구했다.", "partial": "다른 것의 부피를 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def sp_t2():
    return tpl(SP, 2, SP_BASE,
        title="큰 쇠구슬을 녹여 작은 쇠구슬 만들기 — 개수",
        skill="부피가 보존됨을 이용해 (큰 구의 부피) ÷ (작은 구의 부피) = (반지름의 비)³을 구하기",
        variant_axis={"반지름의 비": "2~5배"},
        discriminates="부피의 비가 반지름의 비의 세제곱임을 쓰는가(제곱·1제곱으로 착각하지 않는가)",
        difficulty=2,
        params=[{"name": "m", "values": {"int": [2, 5]}}, {"name": "r", "values": {"int": [2, 6]}}],
        derive={"R": "m*r", "n": "m*m*m", "kR": "4*R*R*R/3", "kr": "4*r*r*r/3"},
        constraints=["n != R", "n != r", "R <= 24"],
        cost_values=["R", "r", "n"],
        answer_var="n",
        verify=["ans*r**3 == R**3", "ans == m**3"],
        question="반지름의 길이가 {R} cm인 쇠구슬 한 개를 녹여 반지름의 길이가 {r} cm인 쇠구슬을 만들려고 한다. 쇠구슬을 최대 몇 개 만들 수 있는지 구하시오.",
        answer="{n}", answer_alt=["{n}개"],
        sol1="녹여서 다시 만들어도 쇠의 부피는 변하지 않는다. 구의 부피는 [[frac(4,3)]]πr³이므로 큰 구의 부피를 작은 구의 부피로 나누면 개수가 나온다. 반지름이 {m}배이면 부피는 {m}³ = {n}배다.",
        sol2=[
            "큰 쇠구슬의 부피: [[frac(4,3)]] × π × {R}³ (cm³), 작은 쇠구슬 한 개의 부피: [[frac(4,3)]] × π × {r}³ (cm³)",
            "부피가 보존되므로 개수 = [[frac(4,3)]]π × {R}³ ÷ ([[frac(4,3)]]π × {r}³) = ({R} ÷ {r})³ = {m}³",
            "따라서 최대 {n}개를 만들 수 있다.",
        ],
        sol2_fig=steps([
            {"text": "[[frac(4,3)]]π × {R}³ ÷ ([[frac(4,3)]]π × {r}³)", "hint": "부피 보존"},
            {"text": "= ({R} ÷ {r})³ = {m}³", "hint": "반지름의 비의 세제곱", "marks": [{"on": "³", "note": "제곱이 아님"}]},
            {"text": "= {n}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="작은 쇠구슬 {n}개의 부피는 {n} × [[frac(4,3)]]π × {r}³ = [[frac(4,3)]]π × {R}³으로 큰 쇠구슬의 부피와 같다. 답은 {n}개다.",
        model_answer="부피가 보존되므로 개수는 [[frac(4,3)]]π × {R}³ ÷ ([[frac(4,3)]]π × {r}³) = ({R} ÷ {r})³ = {m}³ = {n}이다. 따라서 최대 {n}개다.",
        rubric=[
            {"element": "부피 보존과 식", "points": 3, "criterion": "큰 구의 부피를 작은 구의 부피로 나누는 식을 세웠다.", "partial": "부피 대신 반지름이나 겉넓이의 비로 세웠으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "({R} ÷ {r})³ = {n}개를 구했다.", "partial": "세제곱 계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def sp_t3():
    return tpl(SP, 3, SP_BASE,
        title="원기둥 모양 물통에 쇠구슬을 넣었을 때 높아지는 물의 높이",
        skill="높아진 물의 부피(원기둥 πR²h)가 잠긴 구의 부피와 같음을 이용하기",
        variant_axis={"물통 반지름": "2~12", "구슬 반지름": "3의 배수"},
        discriminates="늘어난 물의 부피를 원기둥 모양으로 보고 구의 부피와 같게 놓는가",
        difficulty=3,
        params=[{"name": "m", "values": {"int": [1, 3]}}, {"name": "R", "values": {"int": [2, 12]}}],
        derive={"r": "3*m", "V": "4*r*r*r/3", "h": "4*r*r*r/(3*R*R)"},
        constraints=["h != R", "h != r", "R >= r", "h != V", "h <= 40"],
        cost_values=["R", "r", "V", "h"],
        answer_var="h",
        verify=["ans*R*R == V", "V*3 == 4*r**3"],
        question="밑면의 반지름의 길이가 {R} cm인 원기둥 모양의 물통에 물이 들어 있다. 이 물통에 반지름의 길이가 {r} cm인 구 모양의 쇠구슬을 완전히 잠기도록 넣었을 때, 물의 높이는 몇 cm 높아지는지 구하시오.",
        figure=[{"fn": "solid", "args": {"kind": "cylinder", "radius": "{R} cm"}}],
        answer="{h}", answer_alt=["{h} cm"],
        sol1="쇠구슬이 완전히 잠기면 밀려 올라간 물의 부피는 쇠구슬의 부피와 같다. 올라간 물은 밑면 반지름 {R} cm, 높이 x cm인 원기둥 모양이므로 π × {R}² × x = (구의 부피)라는 방정식을 세운다.",
        sol1_fig=[{"fn": "vessel", "args": {"kind": "cylinder", "rows": [{"name": "물통", "total": "{2*V + V}", "parts": [{"label": "원래 물", "value": "{2*V}", "kind": "water"}, {"label": "높아진 부피 = 구", "value": "{V}", "kind": "other"}]}]}}],
        sol1_anim=[[hl("part:0-0", "part-lbl:0-0")], [hl("part:0-1", "part-lbl:0-1", keep=True)]],
        sol2=[
            "쇠구슬의 부피: [[frac(4,3)]] × π × {r}³ = {V}π (cm³)",
            "높아진 물의 높이를 x cm라 하면 늘어난 물의 부피는 π × {R}² × x = {R*R}πx (cm³)",
            "{R*R}πx = {V}π이므로 x = {h}",
            "따라서 물의 높이는 {h} cm 높아진다.",
        ],
        sol2_fig=steps([
            {"text": "구의 부피 = [[frac(4,3)]]π × {r}³ = {V}π", "hint": "잠긴 부피"},
            {"text": "π × {R}² × x = {V}π", "hint": "늘어난 물 = 원기둥", "marks": [{"on": "{R}²", "note": "물통의 반지름"}]},
            {"text": "x = {V} ÷ {R*R} = {h}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)], []],
        sol_check="높이가 {h} cm 올라가면 늘어난 부피는 π × {R}² × {h} = {V}π cm³로 쇠구슬의 부피 {V}π cm³와 같다. 답은 {h} cm다.",
        model_answer="쇠구슬의 부피는 [[frac(4,3)]] × π × {r}³ = {V}π cm³이고, 높아진 물의 높이를 x cm라 하면 π × {R}² × x = {V}π이므로 x = {h}이다. 따라서 물의 높이는 {h} cm 높아진다.",
        rubric=[
            {"element": "구의 부피", "points": 2, "criterion": "쇠구슬의 부피 {V}π cm³를 구했다.", "partial": "공식의 계수 [[frac(4,3)]]{eul(3)} 틀렸으면 인정하지 않는다."},
            {"element": "식 세우기", "points": 3, "criterion": "늘어난 물의 부피를 π × {R}² × x로 놓고 구의 부피와 같게 놓았다.", "partial": "쇠구슬의 반지름으로 원기둥을 세웠으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "x = {h} cm를 구했다.", "partial": "π를 약분하지 못해 계산이 틀렸으면 1점."},
        ],
        rubric_total=7,
    )


def sp_t4():
    return tpl(SP, 4, SP_BASE,
        title="반구 모양 그릇의 물을 원기둥 모양 그릇에 옮겨 담은 높이",
        skill="반구의 부피(구의 절반)를 원기둥의 부피 πR²h와 같게 놓아 높이 구하기",
        variant_axis={"반구 반지름": "3의 배수", "원기둥 반지름": "2~12"},
        discriminates="반구의 부피를 구의 절반으로 구하는가, 원기둥의 밑면 반지름을 바르게 쓰는가",
        difficulty=3,
        params=[{"name": "m", "values": {"int": [1, 3]}}, {"name": "R", "values": {"int": [2, 12]}}],
        derive={"r": "3*m", "V": "2*r*r*r/3", "h": "2*r*r*r/(3*R*R)"},
        constraints=["h != R", "h != r", "h != V", "h <= 40"],
        cost_values=["R", "r", "V", "h"],
        answer_var="h",
        verify=["ans*R*R == V", "V*3 == 2*r**3"],
        question="반지름의 길이가 {r} cm인 반구 모양의 그릇에 물을 가득 채운 다음, 이 물을 밑면의 반지름의 길이가 {R} cm인 원기둥 모양의 그릇에 모두 부었다. 원기둥 모양의 그릇에 담긴 물의 높이를 구하시오.",
        figure=[{"fn": "solid", "args": {"kind": "hemisphere", "radius": "{r} cm"}}],
        answer="{h}", answer_alt=["{h} cm"],
        sol1="물의 부피는 옮겨 담아도 변하지 않는다. 반구의 부피는 구의 부피의 절반 [[frac(1,2)]] × [[frac(4,3)]]πr³ = [[frac(2,3)]]πr³이고, 원기둥에 담긴 물의 부피는 π × {R}² × (높이)이므로 두 부피를 같게 놓는다.",
        sol1_fig=[{"fn": "vessel", "args": {"kind": "cylinder", "rows": [{"name": "원기둥 그릇", "total": "{V}", "parts": [{"label": "반구의 물 {V}π", "value": "{V}", "kind": "water"}]}]}}],
        sol1_anim=[[hl("part:0-0", "part-lbl:0-0", keep=True)]],
        sol2=[
            "반구의 부피: [[frac(1,2)]] × [[frac(4,3)]] × π × {r}³ = {V}π (cm³)",
            "원기둥 그릇에 담긴 물의 높이를 x cm라 하면 π × {R}² × x = {V}π",
            "따라서 x = {V} ÷ {R*R} = {h}, 물의 높이는 {h} cm",
        ],
        sol2_fig=steps([
            {"text": "반구 = [[frac(2,3)]]π × {r}³ = {V}π", "hint": "구의 절반", "marks": [{"on": "[[frac(2,3)]]", "note": "4/3의 절반"}]},
            {"text": "π × {R}² × x = {V}π", "hint": "부피 보존"},
            {"text": "x = {h}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol_check="원기둥에 높이 {h} cm로 담긴 물의 부피는 π × {R}² × {h} = {V}π cm³로 반구의 부피와 같다. 답은 {h} cm다.",
        model_answer="반구의 부피는 [[frac(1,2)]] × [[frac(4,3)]] × π × {r}³ = {V}π cm³이고, 원기둥 그릇의 물의 높이를 x cm라 하면 π × {R}² × x = {V}π이므로 x = {h}이다. 따라서 물의 높이는 {h} cm다.",
        rubric=[
            {"element": "반구의 부피", "points": 3, "criterion": "구의 부피의 절반으로 반구의 부피 {V}π cm³를 구했다.", "partial": "구 전체의 부피를 썼으면 인정하지 않는다."},
            {"element": "식 세우기와 답", "points": 2, "criterion": "π × {R}² × x = {V}π를 풀어 x = {h}{eul(h)} 구했다.", "partial": "π를 한쪽에만 두어 계산이 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


SP_SEED = {
    "seed_id": SP, "category": "도형",
    "title": "구의 응용 — 원기둥 속 구·쇠구슬 개수·물 높이 상승·반구 물 옮기기",
    "unit_id": "m1-2", "concept_ids": ["m1-2-16", "m1-2-14"],
    "schema_id": None, "schema_name": "구의 부피의 활용",
    "source_item_ids": [],
    "note": "구조만 차용. 반지름을 3의 배수로 두어 4/3·2/3 계수가 정수가 되게 한다. 물 높이는 vessel 도식(원기둥)으로.",
    "geometry": True,
    "templates": [sp_t1(), sp_t2(), sp_t3(), sp_t4()],
}


if __name__ == "__main__":
    for seed in (TA_SEED, PF_SEED, SS_SEED, TS_SEED, SP_SEED):
        with_pitfalls(seed)
        dump(seed)
