# itemfactory/tools/mkseed_m1_gaps2.py — 문항이 하나도 없던 개념 5개(중1-2 네 개 · 중3-1 하나)의 시드 생성기 (v1.0 · 2026-09-21)
#
#   python itemfactory/tools/mkseed_m1_gaps2.py
#     → seeds/m1-2-congruent.json      (m1-2-06 삼각형의 합동: 대응각(그림 라벨별 t1·t4·t5)·둘레·남은 변, 5틀 · 기하 2단)
#     → seeds/m1-2-revolution.json     (m1-2-13 회전체: 축을 품은 단면·축에 수직인 단면(원기둥 t2·구 t4)·원뿔의 부피, 4틀 · 기하 2단)
#     → seeds/m1-2-stemleaf.json       (m1-2-18 줄기와 잎 그림: 이상인 자료 수·k번째 값·줄기별 개수, 3틀 · 자료맥락)
#     → seeds/m1-2-histogram.json      (m1-2-20 히스토그램·도수분포다각형: 계급값·이상인 도수·넓이, 3틀 · 자료맥락)
#     → seeds/m3-1-quad-build.json     (m3-1-20 이차방정식 구하기: 두 근으로(t1·t4)·중근으로(t2·t5)·잘못 본 문제, 5틀)
#
# 자료(줄기·잎, 히스토그램)는 표(table)에 통째로 굽고 답도 파이썬에서 세어 verify 로 대조한다. 수치는 문면에도 둔다(DUP 방지).
from __future__ import annotations

import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def seed(seed_id, title, cids, note, templates, *, category, schema_name=None, geometry=False):
    return {"seed_id": seed_id, "category": category, "title": title, "unit_id": seed_id[:4], "concept_ids": cids,
            "schema_id": None, "schema_name": schema_name, "source_item_ids": [], "note": note, "geometry": geometry,
            "templates": templates}


# ═══════════════════════════════════════════════════════════════════ 1. 삼각형의 합동 (m1-2-06) — 기하 2단
CG = "m1-2-congruent"
CG_BASE = {"process": "추론", "context": "기하맥락", "ops": ["각도", "사칙"], "traps": ["구하는대상혼동"], "qtype": "short",
           "time_limit": 90, "points": 4, "pool_target": 200, "prereq": ["삼각형의 내각의 합", "합동의 뜻"], "tags": ["합동", "대응각", "대응변"]}

# 주어진 두 각과 묻는 각 — 대응: A↔D, B↔E, C↔F. 묻는 각은 주어지지 않은 세 번째 각의 대응각 (문면에 답이 없다)
# wA·wB: ∠A·∠B 가 x·y·z(남은 각) 중 무엇인지 — 좌표를 각에서 계산해 그림과 문면을 맞춘다 (recheck 의 도형–문면 정합)
CG1_ROWS = {
    "AB_F": {"G1": "A", "G2": "B", "ASK": "F", "CORR": "C", "OTH1": "D", "OTH2": "E", "wAx": 1, "wAy": 0, "wBx": 0, "wBy": 1, "wBz": 0, "wAz": 0},
    "BC_D": {"G1": "B", "G2": "C", "ASK": "D", "CORR": "A", "OTH1": "E", "OTH2": "F", "wAx": 0, "wAy": 0, "wBx": 1, "wBy": 0, "wBz": 0, "wAz": 1},
    "AC_E": {"G1": "A", "G2": "C", "ASK": "E", "CORR": "B", "OTH1": "D", "OTH2": "F", "wAx": 1, "wAy": 0, "wBx": 0, "wBy": 0, "wBz": 1, "wAz": 0},
}


def _cg_scene(labels):
    """△ABC 와 그 합동 △DEF(오른쪽으로 평행이동). labels = {꼭짓점: 각 라벨 문자열} (없으면 표시 안 함)."""
    arcs = []
    for v, f, t in (("A", "B", "C"), ("B", "C", "A"), ("C", "A", "B"), ("D", "E", "F"), ("E", "F", "D"), ("F", "D", "E")):
        if labels.get(v):
            arcs.append({"at": v, "from": f, "to": t, "label": labels[v]})
    # 배치: 삼각형이 높으면(cy ≥ 1.25·AB, s=1) 오른쪽에, 납작하면(s=0) 아래에 — 납작한 삼각형을 옆에 두면 그림이 작아져 각 라벨이 겹친다.
    # 좌표는 AB = 10 (scene 의 최소 여백 0.4 가 단위 크기 그림에서는 너무 커서 삼각형이 작아진다)
    return [{"fn": "scene", "args": {"pts": {"A": [0, 0], "B": [10, 0], "C": ["{X}", "{Y}"], "D": ["{dx}", "{dy}"], "E": ["{dx + 10}", "{dy}"], "F": ["{X + dx}", "{Y + dy}"]},
                                     "segs": [["A", "B"], ["B", "C"], ["A", "C"], ["D", "E"], ["E", "F"], ["D", "F"]],
                                     "marks": {"arc": arcs}}}]


CG1_LABELS = {"AB_F": {"A": "{x}°", "B": "{y}°", "F": "?"}, "BC_D": {"B": "{x}°", "C": "{y}°", "D": "?"}, "AC_E": {"A": "{x}°", "C": "{y}°", "E": "?"}}


def cg_t1(key="AB_F", no=1):
    return tpl(CG, no, CG_BASE,
        title="합동인 두 삼각형의 대응각 — 세 번째 각을 내각의 합으로 구해 옮기기",
        skill="△ABC ≡ △DEF 에서 대응각의 크기가 같음을 알고, 주어지지 않은 각을 내각의 합 180°로 구한 뒤 대응각으로 옮기기",
        variant_axis={"주어진 각": "∠A·∠B / ∠B·∠C / ∠A·∠C", "묻는 각": "∠F / ∠D / ∠E"},
        discriminates="꼭짓점의 순서로 대응각을 바르게 찾고(A↔D, B↔E, C↔F), 없는 각은 180°에서 두 각을 빼서 구하는가",
        difficulty=2,
        params=[{"name": "k", "values": {"in": [key]}}, {"name": "i", "values": {"int": [5, 21]}}, {"name": "j", "values": {"int": [5, 21]}}],
        table={"key": "k", "rows": CG1_ROWS},
        derive={"x": "5*i", "y": "5*j", "z": "180 - 5*i - 5*j",
                "aA": "wAx*5*i + wAy*5*j + wAz*(180 - 5*i - 5*j)", "aB": "wBx*5*i + wBy*5*j + wBz*(180 - 5*i - 5*j)",
                "aC": "180 - (wAx*5*i + wAy*5*j + wAz*(180 - 5*i - 5*j)) - (wBx*5*i + wBy*5*j + wBz*(180 - 5*i - 5*j))",
                "bl": "sin(aB*pi/180)/sin(aC*pi/180)", "cx": "bl*cos(aA*pi/180)", "cy": "bl*sin(aA*pi/180)",
                "X": "10*cx", "Y": "10*cy", "s": "min(1, floor(cy/1.25))", "dx": "15*s", "dy": "-(10*cy + 4)*(1 - s)",
                },
        # 세 각 모두 25°~105° — 한 각이 너무 크면 삼각형이 납작해져 그림의 각 라벨이 겹친다
        constraints=["z != x", "z != y", "x != y", "aA >= 25", "aB >= 25", "aC >= 25", "aA <= 105", "aB <= 105", "aC <= 105"],
        cost_values=["x", "y", "z"],
        answer_var="z",
        verify=["x + y + ans == 180", "ans > 0", "aA + aB + aC == 180"],
        question="다음 그림에서 △ABC ≡ △DEF이고 ∠{G1} = [[deg({x})]], ∠{G2} = [[deg({y})]]일 때, ∠{ASK}의 크기를 구하시오.",
        figure=_cg_scene(CG1_LABELS[key]),
        answer="[[deg({z})]]", answer_alt=["{z}"],
        sol1="합동인 두 도형은 대응하는 각의 크기가 서로 같다. △ABC ≡ △DEF에서 꼭짓점 순서대로 A↔D, B↔E, C↔F가 대응하므로 ∠{ASK}는 ∠{CORR}{wa(CORR)} 같다. ∠{CORR}{eun(CORR)} 주어지지 않았으니 삼각형의 세 내각의 합이 180°임을 써서 먼저 구한다.",
        sol1_fig=_cg_scene(CG1_LABELS[key]),
        sol1_anim=[[hl("arc:{CORR}", "arc:{ASK}")]],
        sol2=["∠{CORR} = 180° − ∠{G1} − ∠{G2} = 180° − [[deg({x})]] − [[deg({y})]] = [[deg({z})]]", "대응각이므로 ∠{ASK} = ∠{CORR} = [[deg({z})]]"],
        sol2_fig=steps([{"text": "∠{CORR} = 180° − {x}° − {y}° = {z}°", "hint": "세 내각의 합 180°"},
                        {"text": "∠{ASK} = ∠{CORR} = {z}°", "hint": "A↔D, B↔E, C↔F", "marks": [{"on": "∠{ASK}", "note": "대응각은 순서로 찾는다"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol_check="△DEF의 세 각 ∠{OTH1}, ∠{OTH2}, ∠{ASK}도 대응각이므로 {x}°, {y}°, {z}°이고 합이 180°다. 답은 [[deg({z})]]다.",
        model_answer="∠{CORR} = 180° − {x}° − {y}° = {z}°이고, △ABC ≡ △DEF에서 ∠{ASK}의 대응각은 ∠{CORR}이므로 ∠{ASK} = {z}°이다.",
        rubric=[
            {"element": "남은 각 구하기", "points": 2, "criterion": "내각의 합을 써서 ∠{CORR} = {z}°를 구했다.", "partial": "계산 실수면 1점."},
            {"element": "대응각 찾기", "points": 3, "criterion": "꼭짓점 순서로 ∠{ASK}의 대응각이 ∠{CORR}임을 밝혔다.", "partial": "다른 각과 대응시켰으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{ASK} = {z}°를 답했다.", "partial": "주어진 각을 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


CG2_ROWS = {"ab_bc_df": {"S1": "AB", "S2": "BC", "S3": "DF", "S3C": "AC"}, "ab_ca_ef": {"S1": "AB", "S2": "CA", "S3": "EF", "S3C": "BC"}, "bc_ca_de": {"S1": "BC", "S2": "CA", "S3": "DE", "S3C": "AB"}}


def cg_t2():
    return tpl(CG, 2, CG_BASE,
        title="합동인 두 삼각형에서 대응변을 찾아 둘레 구하기",
        skill="△ABC ≡ △DEF 에서 다른 삼각형의 변이 어느 변과 대응하는지 찾아 둘레의 길이를 구하기",
        variant_axis={"주어진 변": "두 변은 △ABC, 한 변은 △DEF", "대응": "DF↔AC / EF↔BC / DE↔AB"},
        discriminates="꼭짓점 순서로 대응변을 찾아(DF↔AC, EF↔BC, DE↔AB) 둘레에 넣는가",
        ops=["사칙"], difficulty=2,
        params=[{"name": "k", "values": {"in": list(CG2_ROWS)}}, {"name": "a", "values": {"int": [3, 12]}}, {"name": "b", "values": {"int": [3, 12]}}, {"name": "c", "values": {"int": [3, 12]}}],
        table={"key": "k", "rows": CG2_ROWS},
        derive={"P": "a + b + c"},
        constraints=["a + b > c", "b + c > a", "c + a > b", "P != a", "P != b", "P != c", "a != b", "b != c", "a != c"],
        cost_values=["a", "b", "c", "P"],
        answer_var="P",
        verify=["ans == a + b + c", "a + b > c"],
        question="△ABC ≡ △DEF이고 {S1} = {a} cm, {S2} = {b} cm, {S3} = {c} cm일 때, △ABC의 둘레의 길이를 구하시오.",
        answer="{P}", answer_alt=["{P} cm", "{P}cm"],
        sol1="합동인 두 삼각형은 대응하는 변의 길이가 같다. △ABC ≡ △DEF에서 A↔D, B↔E, C↔F이므로 {S3}{eun(S3)} △ABC의 {S3C}{wa(S3C)} 대응한다. 그러면 △ABC의 세 변을 모두 알 수 있다.",
        sol2=["{S3C} = {S3} = {c} cm (대응변)", "둘레 = {S1} + {S2} + {S3C} = {a} + {b} + {c} = {P} (cm)"],
        sol2_fig=steps([{"text": "{S3C} = {S3} = {c}", "hint": "A↔D, B↔E, C↔F", "marks": [{"on": "{S3C}", "note": "글자 순서로 대응변"}]},
                        {"text": "{a} + {b} + {c} = {P}", "hint": "세 변의 합"}]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")]],
        sol_check="△DEF의 둘레도 대응변의 합이라 {P} cm로 같다. 답은 {P} cm다.",
        model_answer="△ABC ≡ △DEF에서 {S3C}의 대응변은 {S3}이므로 {S3C} = {c} cm이다. 따라서 △ABC의 둘레는 {a} + {b} + {c} = {P} (cm)이다.",
        rubric=[
            {"element": "대응변 찾기", "points": 3, "criterion": "{S3C} = {S3} = {c} cm임을 밝혔다.", "partial": "다른 변과 대응시켰으면 인정하지 않는다."},
            {"element": "둘레 구하기", "points": 2, "criterion": "{a} + {b} + {c} = {P} (cm)를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def cg_t3():
    return tpl(CG, 3, CG_BASE,
        title="둘레가 주어진 합동인 삼각형에서 남은 한 변의 길이 구하기",
        skill="합동인 두 삼각형의 둘레가 같음을 이용해 알려지지 않은 변의 길이를 구하기",
        variant_axis={"둘레": "12~40 cm", "주어진 두 변": "3~15 cm"},
        discriminates="합동이면 둘레가 같음을 근거로 세우고, 둘레에서 두 변을 빼서 남은 변을 구하는가",
        ops=["사칙"], difficulty=2,
        params=[{"name": "a", "values": {"int": [3, 15]}}, {"name": "b", "values": {"int": [3, 15]}}, {"name": "c", "values": {"int": [3, 15]}}],
        # 삼각형 부등식(세 변 모두)은 constraints 에서 거르고 verify 에서 가장 긴 변 기준으로 한 번 더 확인 — [검산]이 늘 참이 되게
        derive={"P": "a + b + c", "L": "max(a, b, c)", "R": "a + b + c - max(a, b, c)"},
        constraints=["a + b > c", "b + c > a", "c + a > b", "a != b", "b != c", "a != c", "c != P - a", "c != P - b"],
        cost_values=["a", "b", "P", "c"],
        answer_var="c",
        verify=["a + b + ans == P", "ans > 0", "a + b > ans", "b + ans > a", "ans + a > b", "L < R", "2*L < P"],
        question="△ABC ≡ △DEF이고 △DEF의 둘레의 길이가 {P} cm이다. AB = {a} cm, BC = {b} cm일 때, AC의 길이를 구하시오.",
        answer="{c}", answer_alt=["{c} cm", "{c}cm"],
        sol1="합동인 두 삼각형은 대응변의 길이가 모두 같으므로 둘레도 같다. 따라서 △ABC의 둘레도 {P} cm이고, 여기서 아는 두 변을 빼면 AC가 나온다.",
        sol2=["△ABC의 둘레 = △DEF의 둘레 = {P} cm", "AC = {P} − {a} − {b} = {c} (cm)"],
        sol2_fig=steps([{"text": "둘레(△ABC) = 둘레(△DEF) = {P}", "hint": "합동 → 대응변이 모두 같다"},
                        {"text": "AC = {P} − {a} − {b} = {c}", "marks": [{"on": "{c}", "note": "두 변을 모두 뺀다"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol_check="{a} + {b} + {c} = {P}{ro(P)} 둘레와 맞고, 가장 긴 변 {L} cm가 나머지 두 변의 합 {R} cm보다 짧아 세 변 {a} cm, {b} cm, {c} cm로 삼각형이 만들어진다. 답은 {c} cm다.",
        model_answer="합동인 두 삼각형은 둘레가 같으므로 △ABC의 둘레는 {P} cm이다. 따라서 AC = {P} − {a} − {b} = {c} (cm)이다.",
        rubric=[
            {"element": "둘레가 같음", "points": 3, "criterion": "합동이므로 △ABC의 둘레도 {P} cm임을 밝혔다.", "partial": "근거 없이 값만 썼으면 1점."},
            {"element": "남은 변 구하기", "points": 2, "criterion": "AC = {P} − {a} − {b} = {c} (cm)를 구했다.", "partial": "한 변만 뺐으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# ═══════════════════════════════════════════════════════════════════ 2. 회전체 (m1-2-13) — 기하 2단
RV = "m1-2-revolution"
RV_BASE = {"process": "추론", "context": "기하맥락", "ops": ["넓이"], "traps": ["구하는대상혼동"], "qtype": "short",
           "time_limit": 90, "points": 4, "pool_target": 200, "prereq": ["원기둥·원뿔·구", "직사각형·삼각형의 넓이"], "tags": ["회전체", "단면"]}
RV1_ROWS = {"cyl": {"KIND": "cylinder", "KW": "원기둥", "SEC": "직사각형", "f": 2, "FORM": "(2 × 반지름) × 높이", "DIV": "", "PIT2": "직사각형의 넓이(지름 × 높이)를 계산하다 곱셈 실수", "SRC": "가로가 지름 2r, 세로가 높이 h"},
            "cone": {"KIND": "cone", "KW": "원뿔", "SEC": "이등변삼각형", "f": 1, "FORM": "(2 × 반지름) × 높이 ÷ 2", "DIV": " ÷ 2", "PIT2": "이등변삼각형의 넓이에서 ÷ 2를 빠뜨림", "SRC": "밑변이 지름 2r, 높이가 h"}}


def rv_t1():
    return tpl(RV, 1, RV_BASE,
        title="회전축을 포함하는 평면으로 자른 단면의 넓이 — 원기둥은 직사각형, 원뿔은 이등변삼각형",
        skill="회전체를 회전축을 품은 평면으로 자르면 원기둥은 직사각형, 원뿔은 이등변삼각형이 됨을 알고 그 넓이를 구하기 (지름을 써야 함)",
        variant_axis={"입체": "원기둥 / 원뿔", "반지름": "2~9", "높이": "3~12"},
        discriminates="단면의 가로(밑변)가 반지름이 아니라 지름 2r 임을 아는가",
        difficulty=2,
        params=[{"name": "k", "values": {"in": list(RV1_ROWS)}}, {"name": "r", "values": {"int": [2, 9]}}, {"name": "h", "values": {"int": [3, 12]}}],
        table={"key": "k", "rows": RV1_ROWS},
        derive={"d": "2*r", "S": "f*r*h", "wrong": "f*r*h/2"},
        constraints=["S != r", "S != h", "S != d", "r != h"],
        cost_values=["r", "h", "S"],
        answer_var="S",
        verify=["ans == f*r*h", "d == 2*r"],
        question="밑면의 반지름의 길이가 {r} cm, 높이가 {h} cm인 {KW}{eul(KW)} 회전축을 포함하는 평면으로 자를 때 생기는 단면의 넓이를 구하시오.",
        figure=[{"fn": "solid", "args": {"kind": "{KIND}", "radius": "{r}", "height": "{h}"}}],
        answer="{S}", answer_alt=["{S} cm²", "{S}cm²"],
        sol1="{KW}{eun(KW)} 회전축을 품은 평면으로 자르면 단면은 {SEC}이다. {SRC}이므로 가로(밑변)에는 반지름이 아니라 지름을 써야 한다.",
        sol1_fig=[{"fn": "solid", "args": {"kind": "{KIND}", "radius": "{r}", "height": "{h}"}}],
        sol1_anim=[[hl("radius", "r-lbl")], [hl("height", "h-lbl", keep=True)]],
        sol2=["단면의 밑변(가로) = 지름 = 2 × {r} = {d} (cm), 높이 = {h} cm", "단면({SEC})의 넓이 = {FORM} = {d} × {h}{DIV} = {S} (cm²)"],
        sol2_fig=steps([{"text": "가로(밑변) = 2 × {r} = {d}", "hint": "지름!", "marks": [{"on": "{d}", "note": "반지름 {r}{ika(r)} 아니다"}]},
                        {"text": "넓이 = {d} × {h}{DIV} = {S}", "hint": "{FORM}"}]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")]],
        sol_check="반지름을 그대로 쓰면 {wrong} cm²가 나오는데 이는 단면의 절반이다. 답은 {S} cm²다.",
        model_answer="{KW}{eul(KW)} 회전축을 포함하는 평면으로 자른 단면은 {SEC}이고, 그 가로(밑변)는 지름 {d} cm, 높이는 {h} cm이다. 따라서 넓이는 {FORM} = {d} × {h}{DIV} = {S} (cm²)이다.",
        rubric=[
            {"element": "단면의 모양", "points": 2, "criterion": "단면이 {SEC}임을 밝혔다.", "partial": "모양을 잘못 썼으면 인정하지 않는다."},
            {"element": "단면의 치수", "points": 3, "criterion": "가로(밑변)가 지름 {d} cm, 높이가 {h} cm임을 썼다.", "partial": "반지름을 그대로 썼으면 인정하지 않는다."},
            {"element": "넓이 구하기", "points": 2, "criterion": "넓이 {S} cm²를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


RV2_ROWS = {"cyl": {"KIND": "cylinder", "KW": "원기둥", "PL": "회전축에 수직인 평면", "HAS_H": 1},
            "sph": {"KIND": "sphere", "KW": "구", "PL": "중심을 지나는 평면", "HAS_H": 0}}


def rv_t2():
    return tpl(RV, 2, RV_BASE,
        title="회전축에 수직인 평면(구는 중심을 지나는 평면)으로 자른 단면 — 원의 넓이",
        skill="원기둥을 축에 수직으로, 구를 중심을 지나게 자르면 단면이 반지름이 같은 원임을 알고 넓이 πr²을 구하기",
        variant_axis={"입체": "원기둥 / 구", "반지름": "2~12"},
        discriminates="단면이 원임을 알고 넓이에 π와 반지름의 제곱을 쓰는가 (원주 2πr 과 혼동하지 않는가)",
        difficulty=2, traps=["제곱누락"],
        params=[{"name": "k", "values": {"in": list(RV2_ROWS)}}, {"name": "r", "values": {"int": [2, 12]}}, {"name": "h", "values": {"int": [4, 12]}}],
        table={"key": "k", "rows": RV2_ROWS},
        derive={"k2": "r*r", "wrong": "2*r"},
        constraints=["k2 != r", "(HAS_H == 0) or (h != r)", "(HAS_H == 1) or (h == 4)"],
        cost_values=["r", "k2"],
        answer_var="k2",
        verify=["ans == r*r", "ans > wrong or r == 2"],
        question=None,   # rv_t2_split — 원기둥(높이 있음)·구
        answer="[[{k2} * pi]]", answer_alt=["[[{k2} * pi]] cm²", "{k2}π"],
        sol1="{KW}{eul(KW)} {PL}으로 자르면 단면은 반지름의 길이가 {r} cm인 원이다. 원의 넓이는 π × (반지름)²이다.",
        sol1_fig=[{"fn": "solid", "args": {"kind": "{KIND}", "radius": "{r}", "height": "{h}"}}],
        sol1_anim=[[hl("radius", "r-lbl")]],
        sol2=["단면은 반지름이 {r} cm인 원", "넓이 = π × {r}² = {k2}π (cm²)"],
        sol2_fig=steps([{"text": "단면 = 반지름 {r}인 원", "hint": "{PL}"}, {"text": "π × {r}² = {k2}π", "marks": [{"on": "{r}²", "note": "제곱을 빠뜨리지 말 것"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol_check="원주 2π × {r} = {wrong}π와 혼동하기 쉽다. 넓이는 π × {r} × {r} = {k2}π (cm²)다.",
        model_answer="{KW}{eul(KW)} {PL}으로 자른 단면은 반지름의 길이가 {r} cm인 원이므로 넓이는 π × {r}² = {k2}π (cm²)이다.",
        rubric=[
            {"element": "단면의 모양", "points": 2, "criterion": "단면이 반지름 {r} cm인 원임을 밝혔다.", "partial": "모양만 맞고 반지름을 잘못 썼으면 1점."},
            {"element": "넓이 구하기", "points": 3, "criterion": "π × {r}² = {k2}π (cm²)를 구했다.", "partial": "제곱을 빠뜨렸으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def rv_t2_split(t):
    out = []
    for no, key, q in ((2, "cyl", "밑면의 반지름의 길이가 {r} cm, 높이가 {h} cm인 원기둥을 회전축에 수직인 평면으로 자를 때 생기는 단면의 넓이를 구하시오."),
                       (4, "sph", "반지름의 길이가 {r} cm인 구를 중심을 지나는 평면으로 자를 때 생기는 단면의 넓이를 구하시오.")):
        u = dict(t)
        u["id"] = f"{RV}-t{no}"
        u["params"] = [p for p in t["params"] if p["name"] != "k"] + [{"name": "k", "values": {"in": [key]}}]
        u["question"] = q
        u["title"] = t["title"] + (" (원기둥)" if key == "cyl" else " (구)")
        if key == "sph":
            u["figure"] = None
            u["sol1_fig"] = [{"fn": "solid", "args": {"kind": "sphere", "radius": "{r}"}}]
        else:
            u["figure"] = [{"fn": "solid", "args": {"kind": "cylinder", "radius": "{r}", "height": "{h}"}}]
        out.append(u)
    return out


def rv_t3():
    return tpl(RV, 3, RV_BASE,
        title="직각삼각형을 한 바퀴 돌려 만든 회전체(원뿔)의 부피",
        skill="직각삼각형을 직각을 낀 한 변을 축으로 회전시키면 원뿔이 생김을 알고, 밑면의 반지름과 높이를 찾아 부피 (1/3)πr²h 를 구하기",
        variant_axis={"밑변(반지름)": "2~9", "높이": "3~12"},
        discriminates="회전축이 된 변이 높이, 다른 변이 밑면의 반지름이 됨을 알고 1/3 을 빠뜨리지 않는가",
        ops=["부피"], difficulty=3, points=5, prereq=["원뿔의 부피", "회전체"],
        params=[{"name": "r", "values": {"int": [2, 9]}}, {"name": "h", "values": {"int": [3, 12]}}],
        derive={"kv": "r*r*h/3", "kc": "r*r*h"},
        constraints=["(r*r*h) % 3 == 0", "kv != r", "kv != h", "r != h"],
        cost_values=["r", "h", "kv"],
        answer_var="kv",
        verify=["3*ans == r*r*h", "ans > 0"],
        question="∠B = 90°이고 AB = {h} cm, BC = {r} cm인 직각삼각형 ABC를 변 AB를 회전축으로 하여 한 바퀴 돌릴 때 생기는 회전체의 부피를 구하시오.",
        answer="[[{kv} * pi]]", answer_alt=["[[{kv} * pi]] cm³", "{kv}π"],
        sol1="직각삼각형을 직각을 낀 변 AB를 축으로 돌리면 원뿔이 된다. 축이 된 AB가 원뿔의 높이, 축과 수직인 BC가 밑면의 반지름이다.",
        sol1_fig=[{"fn": "solid", "args": {"kind": "cone", "radius": "{r}", "height": "{h}"}}],
        sol1_anim=[[hl("radius", "r-lbl")], [hl("height", "h-lbl", keep=True)]],
        sol2=["회전체 = 밑면의 반지름 {r} cm, 높이 {h} cm인 원뿔", "부피 = [[frac(1,3)]] × π × {r}² × {h} = {kv}π (cm³)"],
        sol2_fig=steps([{"text": "반지름 = BC = {r}, 높이 = AB = {h}", "hint": "축이 된 변이 높이"},
                        {"text": "[[frac(1,3)]] × π × {r}² × {h} = {kv}π", "marks": [{"on": "[[frac(1,3)]]", "note": "뿔은 1/3"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol_check="1/3을 빠뜨리면 원기둥의 부피 {kc}π가 나온다 — 답이 아니다. 답은 {kv}π cm³다.",
        model_answer="변 AB를 축으로 돌리면 밑면의 반지름이 {r} cm, 높이가 {h} cm인 원뿔이 생기므로 부피는 [[frac(1,3)]] × π × {r}² × {h} = {kv}π (cm³)이다.",
        rubric=[
            {"element": "회전체 파악", "points": 3, "criterion": "원뿔이 생기고 반지름이 {r} cm, 높이가 {h} cm임을 밝혔다.", "partial": "반지름과 높이를 바꿔 썼으면 인정하지 않는다."},
            {"element": "부피 구하기", "points": 2, "criterion": "[[frac(1,3)]] × π × {r}² × {h} = {kv}π (cm³)를 구했다.", "partial": "1/3을 빠뜨렸으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# ═══════════════════════════════════════════════════════════════════ 3. 줄기와 잎 그림 (m1-2-18) — 자료맥락 3단
SL = "m1-2-stemleaf"
SL_BASE = {"process": "문제해결", "context": "자료맥락", "ops": ["통계"], "traps": ["조건누락"], "qtype": "short",
           "time_limit": 90, "points": 4, "pool_target": 200, "prereq": ["자료의 정리"], "tags": ["줄기와 잎 그림", "자료"]}
SL_CTX = [("수학 점수", "점"), ("윗몸일으키기 기록", "회"), ("몸무게", "kg"), ("하루 독서 시간", "분"), ("줄넘기 기록", "회")]


def _sl_rows():
    rnd = random.Random(1818)
    rows = {}
    i = 0
    while len(rows) < 120:
        ctx, unit = rnd.choice(SL_CTX)
        s0 = rnd.choice([1, 2, 3, 4, 5, 6])
        nst = rnd.choice([3, 4])
        stems = list(range(s0, s0 + nst))
        leaves = []
        for st in stems:
            k = rnd.choice([1, 2, 2, 3, 3, 4, 5])
            leaves.append(sorted(rnd.sample(range(0, 10), k)))
        vals = sorted(10 * st + lf for st, ls in zip(stems, leaves) for lf in ls)
        N = len(vals)
        if N < 8:
            continue
        note = f"{stems[0]}|{leaves[0][0]}{'은' if str(leaves[0][0])[-1] in '013678' else '는'} {vals[0]}{unit}"
        # ① X 이상인 자료 수 — X 는 십의 자리 경계가 아닌 값(줄기 중간)
        X = rnd.choice([10 * st + rnd.choice([3, 5, 7]) for st in stems[1:]]) if nst >= 2 else 10 * stems[0] + 5
        cntX = sum(1 for v in vals if v >= X)
        # ② k 번째로 큰 값
        k = rnd.choice([2, 3, 4])
        kth = vals[-k]
        # ③ 잎이 가장 많은 줄기의 자료 수 (유일할 때만)
        counts = [len(ls) for ls in leaves]
        mx = max(counts)
        big_stem = stems[counts.index(mx)] if counts.count(mx) == 1 else None
        i += 1
        rows[f"D{i}"] = {"CTX": ctx, "U": unit, "N": N, "STEMS": stems, "LEAVES": leaves, "NOTE": note, "X": X, "CNTX": cntX, "K": k, "KTH": kth,
                         "BIGS": big_stem if big_stem is not None else -1, "BIGN": mx, "MAXV": vals[-1], "MINV": vals[0], "RNG": vals[-1] - vals[0],
                         "LTOP": ", ".join(str(v) for v in vals[-4:][::-1])}
    return rows


# 단위 표기(09-25 3차): 단위 기호 cm·kg 는 수와 띄어 쓴다(UU). 단위 뒤 조사는 읽는 소리(UR) 기준 — 'cm'는 센티미터, 'kg'는 킬로그램.
UNIT_UU = {"cm": " cm", "kg": " kg"}
UNIT_UR = {"점": "점", "회": "회", "분": "분", "초": "초", "cm": "센티미터", "kg": "킬로그램"}


def _sl_weight_rows(rows):
    """t1·t3 용 — 몸무게 행을 중학생 범위(35~74 kg)의 자료로 같은 자리(행 키)에 다시 넣는다 (09-25 3차: 줄기 1~3 = 10~39 kg 학생이 있었다).
    X(기준값)·CNTX·BIGS 도 새 자료로 다시 구하고, t1·t3 가 모두 성립하도록(잎이 가장 많은 줄기가 하나, 기준 이상이 1명 이상·전원 아님) 고른다.
    K 는 그대로 둔다(t2 는 _sl2_rows 에서 따로 몸무게를 뽑는다)."""
    rnd = random.Random(1821)
    out = {}
    seen1, seen3 = set(), set()                  # 발문이 겹치면 DUP 로 떨어진다 — t1 발문(N, X)·t3 발문(N, BIGS)이 몸무게 행끼리 겹치지 않게
    for key, r in rows.items():
        if r["CTX"] != "몸무게":
            out[key] = r
            continue
        for _ in range(100000):
            nst = rnd.choice([3, 4])
            s0 = rnd.choice([3, 4]) if nst == 4 else rnd.choice([3, 4, 5])
            stems = list(range(s0, s0 + nst))
            heavy = rnd.choice(stems + [st for st in stems if st in (4, 5)])     # 잎이 가장 많은 줄기 — 40·50 kg대가 더 자주
            leaves = []
            for st in stems:
                pool = range(5, 10) if st == 3 else (range(0, 5) if st == 7 else range(0, 10))
                k = rnd.choice([4, 5]) if st == heavy else rnd.choice([1, 2, 2, 3])
                leaves.append(sorted(rnd.sample(list(pool), min(k, len(pool)))))
            vals = sorted(10 * st + lf for st, ls in zip(stems, leaves) for lf in ls)
            counts = [len(ls) for ls in leaves]
            mx = max(counts)
            X = 10 * rnd.choice(stems[1:]) + rnd.choice([3, 5, 7])
            cntX = sum(1 for v in vals if v >= X)
            if len(vals) < 8 or counts.count(mx) != 1 or not (1 <= cntX < len(vals)) or cntX == X or mx == stems[counts.index(mx)]:
                continue
            if (len(vals), X) in seen1 or (len(vals), stems[counts.index(mx)]) in seen3:
                continue
            seen1.add((len(vals), X)); seen3.add((len(vals), stems[counts.index(mx)]))
            break
        else:
            raise SystemExit(f"_sl_weight_rows: {key} 몸무게 자료를 만들지 못함")
        note = f"{stems[0]}|{leaves[0][0]}{'은' if str(leaves[0][0])[-1] in '013678' else '는'} {vals[0]}{r['U']}"
        out[key] = dict(r, N=len(vals), STEMS=stems, LEAVES=leaves, NOTE=note, X=X, CNTX=cntX, KTH=vals[-r["K"]],
                        BIGS=stems[counts.index(mx)], BIGN=mx, MAXV=vals[-1], MINV=vals[0], RNG=vals[-1] - vals[0],
                        LTOP=", ".join(str(v) for v in vals[-4:][::-1]))
    for r in out.values():                       # 표기 칸 — 그림 메모도 '39 kg'
        r["NOTE"] = re.sub(r"(\d)(cm|kg)$", r"\1 \2", r["NOTE"])
        r["UU"], r["UR"] = UNIT_UU.get(r["U"], r["U"]), UNIT_UR[r["U"]]
    return out


SL_ROWS = _sl_weight_rows(_sl_rows())
SL_FIG = [{"fn": "stemleaf", "args": {"stems": "{STEMS}", "leaves": "{LEAVES}", "note": "{NOTE}"}}]


def _sl_vals(r):
    return sorted(10 * st + lf for st, ls in zip(r["STEMS"], r["LEAVES"]) for lf in ls)


def _sl1_rows():
    """t1 전용 — 기준 이상인 값 전부를 그림 순서(위 줄부터, 왼쪽부터 = 작은 값부터)로 적은 GEX 를 더한다 (09-25: [확인]의 나열이 그림과 반대이고 모자랐다)."""
    out = {}
    for k, r in SL_ROWS.items():
        ge = [v for v in _sl_vals(r) if v >= r["X"]]
        out[k] = dict(r, GEX=", ".join(str(v) for v in ge))
    return out


# 몸무게 — 중학생 현실 범위(35~74 kg)에서 다시 뽑는다. 줄기 3~7 중 3~4개, 가운데 줄기(40·50 kg대)에 잎이 더 몰리게.
def _sl2_weight_row(rnd, r):
    while True:
        nst = rnd.choice([3, 4])
        s0 = rnd.choice([3, 4]) if nst == 4 else rnd.choice([3, 4, 5])
        stems = list(range(s0, s0 + nst))
        leaves = []
        for st in stems:
            pool = range(5, 10) if st == 3 else (range(0, 5) if st == 7 else range(0, 10))
            k = rnd.choice([2, 3, 3, 4, 5]) if st in (4, 5) else rnd.choice([1, 2, 2, 3])
            leaves.append(sorted(rnd.sample(list(pool), min(k, len(pool)))))
        vals = sorted(10 * st + lf for st, ls in zip(stems, leaves) for lf in ls)
        N, K = len(vals), r["K"]
        if N < 8 or vals[-K] in (N, K):
            continue
        note = f"{stems[0]}|{leaves[0][0]}{'은' if str(leaves[0][0])[-1] in '013678' else '는'} {vals[0]}{r['U']}"
        return dict(r, N=N, STEMS=stems, LEAVES=leaves, NOTE=note, KTH=vals[-K], MAXV=vals[-1], MINV=vals[0], RNG=vals[-1] - vals[0],
                    LTOP=", ".join(str(v) for v in vals[-4:][::-1]))


def _sl2_rows():
    """t2 전용 — 몸무게 행만 현실 범위로 다시 뽑고(나머지 행은 SL_ROWS 그대로), K 번째보다 큰 값 목록 GT 를 더한다."""
    rnd = random.Random(1819)
    out = {}
    for k, r in SL_ROWS.items():
        if r["CTX"] == "몸무게":
            r = _sl2_weight_row(rnd, r)
        vals = _sl_vals(r)
        row = {f: r[f] for f in ("CTX", "U", "N", "STEMS", "LEAVES", "NOTE", "K", "KTH", "MAXV", "MINV", "LTOP")}
        row["NOTE"] = re.sub(r"(\d)kg$", r"\1 kg", row["NOTE"])   # 단위 기호(kg)는 수와 띄어 쓴다 — '58 kg' (점·회·분은 붙여 씀)
        row["UU"] = " kg" if r["U"] == "kg" else r["U"]   # t2 가 쓰는 칸만 (몸무게 행의 X·BIGS 등 옛 값이 남지 않게)
        out[k] = dict(row, GT=", ".join(str(v) for v in vals[-1:-r["K"]:-1]))
    return out


SL1_ROWS = _sl1_rows()
SL2_ROWS = _sl2_rows()


def sl_t1():
    return tpl(SL, 1, SL_BASE,
        title="줄기와 잎 그림에서 어떤 값 이상인 자료의 개수 세기",
        skill="줄기와 잎 그림에서 각 자료의 값을 읽어(줄기 = 십의 자리, 잎 = 일의 자리) 기준 이상인 자료의 개수를 세기",
        variant_axis={"자료": "점수·기록·몸무게·시간", "기준값": "줄기 중간 값"},
        discriminates="줄기와 잎을 합쳐 값을 읽고, 기준 줄기에서는 잎을 하나하나 비교해 세는가",
        difficulty=2,
        params=[{"name": "k", "values": {"in": list(SL_ROWS)}}],
        table={"key": "k", "rows": SL1_ROWS},
        derive={"ansv": "CNTX"},
        constraints=["CNTX >= 1", "CNTX != N", "CNTX != X"],
        cost_values=["N", "X", "CNTX"],
        answer_var="ansv",
        verify=["ans == CNTX", "ans <= N", "MAXV >= X"],
        question="다음은 학생 {N}명의 {CTX}{eul(CTX)} 조사하여 나타낸 줄기와 잎 그림이다. {CTX}{ika(CTX)} {X}{UU} 이상인 학생은 모두 몇 명인지 구하시오.",
        figure=SL_FIG,
        answer="{ansv}", answer_alt=["{ansv}명"],
        sol1="줄기와 잎 그림에서 한 자료의 값은 (줄기)(잎)으로 읽는다 — {NOTE}. 기준 {X}{UU} 이상인 것을 셀 때는 줄기가 더 큰 줄의 잎은 모두 세고, 기준과 줄기가 같은 줄에서는 잎을 하나씩 비교한다.",
        sol2=["줄기가 {X}{UU}의 십의 자리보다 큰 줄의 잎은 모두 {X}{UU} 이상이다", "줄기가 같은 줄에서는 일의 자리(잎)가 기준 이상인 것만 센다", "세어 보면 {X}{UU} 이상인 학생은 {CNTX}명"],
        sol2_fig=steps([{"text": "큰 줄기의 잎: 모두 포함", "hint": "줄기 = 십의 자리"}, {"text": "같은 줄기: 잎 ≥ 기준의 일의 자리", "marks": [{"on": "잎", "note": "'이상'은 같은 값 포함"}]}, {"text": "합: {CNTX}명"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)]],
        sol3="그림의 위 줄부터 왼쪽에서 오른쪽으로(작은 값부터) {X}{UU} 이상인 자료를 모두 적으면 {GEX}의 {CNTX}개다. 따라서 전체 {N}명 중 {CNTX}명이 조건에 맞다.",
        sol3_fig=steps(["{X}{UU} 이상: {GEX}", "전체 {N}명 중 {CNTX}명"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="줄기와 잎 그림에서 {X}{UU} 이상인 값을 세면 {CNTX}개이다. 따라서 {CNTX}명이다.",
        rubric=[
            {"element": "자료 값 읽기", "points": 3, "criterion": "줄기와 잎을 합쳐 값을 읽고 {X}{UU} 이상인 것을 골랐다.", "partial": "같은 줄기의 잎 비교를 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{CNTX}명을 답했다.", "partial": "하나 차이면 1점."},
        ],
        rubric_total=5,
    )


def sl_t2():
    return tpl(SL, 2, SL_BASE,
        title="줄기와 잎 그림에서 k번째로 큰 값 찾기",
        skill="줄기와 잎 그림이 이미 크기순으로 정리되어 있음을 이용해 큰 쪽에서 k번째 값을 읽기",
        variant_axis={"k": "2·3·4", "자료": "점수·기록·몸무게·시간"},
        discriminates="잎이 줄기마다 크기순이며 마지막 줄기의 끝이 가장 큰 값임을 알고, 줄을 넘어가며 거꾸로 세는가",
        difficulty=2,
        params=[{"name": "k", "values": {"in": list(SL2_ROWS)}}],
        table={"key": "k", "rows": SL2_ROWS},
        derive={"ansv": "KTH"},
        constraints=["KTH != N", "KTH != K", "KTH != MAXV", "N != 2*K"],   # N = 2K 이면 작은 쪽 K번째가 큰 쪽 K+1번째와 같아 채점 판정(불인정·1점)이 겹친다
        cost_values=["N", "K", "KTH"],
        answer_var="ansv",
        verify=["ans == KTH", "ans < MAXV", "ans > MINV"],
        question="다음은 학생 {N}명의 {CTX}{eul(CTX)} 조사하여 나타낸 줄기와 잎 그림이다. {CTX}{ika(CTX)} {K}번째로 높은(큰) 학생의 {CTX}{eul(CTX)} 구하시오.",
        figure=SL_FIG,
        answer="{ansv}", answer_alt=["{ansv}{U}", "{ansv} {U}"],
        sol1="줄기와 잎 그림은 줄기가 아래로 갈수록 크고 잎도 왼쪽부터 작은 순서로 적혀 있다. 그러므로 가장 큰 값은 마지막 줄기의 맨 오른쪽 잎이고, 거기서부터 왼쪽으로, 잎이 다 떨어지면 윗줄기의 맨 오른쪽으로 옮겨 가며 세면 된다.",
        sol2=["가장 큰 값은 {MAXV}{UU}", "큰 쪽에서 차례로 읽으면 {LTOP}, …", "따라서 {K}번째로 큰 값은 {KTH}{UU}"],
        sol2_fig=steps([{"text": "1번째: {MAXV}", "hint": "마지막 줄기의 맨 오른쪽 잎"}, {"text": "큰 쪽부터: {LTOP}", "marks": [{"on": "{KTH}", "note": "{K}번째"}]}, {"text": "답: {KTH}{UU}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)]],
        sol3="{KTH}{UU}보다 큰 값은 {GT}의 {K - 1}개뿐이므로, 큰 쪽에서 {K}번째 값은 {KTH}{UU}이다.",
        sol3_fig=steps(["{KTH}보다 큰 값: {GT} → {K - 1}개"]),
        sol3_anim=[[reveal(0)]],
        model_answer="줄기와 잎 그림에서 큰 값부터 차례로 읽으면 {LTOP}, …이므로 {K}번째로 큰 값은 {KTH}{UU}이다.",
        rubric=[
            {"element": "큰 값부터 읽기", "points": 3, "criterion": "마지막 줄기의 오른쪽 잎부터 거꾸로 읽어 순서를 매겼다.", "partial": "줄기를 넘어갈 때 순서를 잘못 이었으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{K}번째로 큰 값이 {KTH}{UU}임을 답했다.", "partial": "큰 쪽에서 센 순위가 하나 어긋난 값을 답했으면 1점."},
        ],
        rubric_total=5,
    )


def sl_t3():
    return tpl(SL, 3, SL_BASE,
        title="줄기와 잎 그림에서 잎이 가장 많은 줄기와 그 줄의 자료 수",
        skill="줄기마다 잎의 개수를 세어 가장 많은 줄기를 찾고, 그 줄기가 뜻하는 값의 범위를 말하기",
        variant_axis={"줄기 수": "3~4", "자료": "점수·기록·몸무게·시간"},
        discriminates="잎의 개수가 곧 그 범위의 자료 수임을 알고 줄기별로 정확히 세는가",
        difficulty=1,
        params=[{"name": "k", "values": {"in": list(SL_ROWS)}}],
        table={"key": "k", "rows": SL_ROWS},
        derive={"ansv": "BIGN", "lo": "10*BIGS", "hi": "10*BIGS + 9"},
        constraints=["BIGS >= 0", "BIGN != N", "BIGN != BIGS"],
        cost_values=["N", "BIGN"],
        answer_var="ansv",
        verify=["ans == BIGN", "ans <= N"],
        question="다음은 학생 {N}명의 {CTX}{eul(CTX)} 조사하여 나타낸 줄기와 잎 그림이다. 잎이 가장 많은 줄기는 {BIGS}이다. 이 줄기에 속하는 학생, 즉 {CTX}{ika(CTX)} {lo}{UU} 이상 {hi}{UU} 이하인 학생은 몇 명인지 구하시오.",
        figure=SL_FIG,
        answer="{ansv}", answer_alt=["{ansv}명"],
        sol1="줄기와 잎 그림에서 한 줄기의 잎 하나가 자료 하나다. 그러므로 줄기 {BIGS}에 적힌 잎의 개수가 곧 {lo}{UU} 이상 {hi}{UU} 이하인 학생 수다.",
        sol2=["줄기 {BIGS}의 잎을 센다", "잎이 {BIGN}개이므로 학생은 {BIGN}명"],
        sol2_fig=steps([{"text": "줄기 {BIGS} → 값 {lo}~{hi}", "hint": "줄기 = 십의 자리"}, {"text": "잎의 개수 = {BIGN}", "marks": [{"on": "{BIGN}", "note": "잎 하나 = 학생 한 명"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="다른 줄기의 잎은 모두 {BIGN}개보다 적으므로 줄기 {BIGS}{ika(BIGS)} 잎이 가장 많은 줄기가 맞고, 그 학생 수는 {BIGN}명이다.",
        sol3_fig=steps(["줄기 {BIGS}: {BIGN}명 (가장 많음)"]),
        sol3_anim=[[reveal(0)]],
        model_answer="줄기 {BIGS}의 잎은 {BIGN}개이므로 {lo}{UU} 이상 {hi}{UU} 이하인 학생은 {BIGN}명이다.",
        rubric=[
            {"element": "줄기의 뜻", "points": 2, "criterion": "줄기 {BIGS}{ika(BIGS)} {lo}~{hi}{UU}{eul(UR)} 뜻함을 밝혔다.", "partial": "범위를 잘못 썼으면 인정하지 않는다."},
            {"element": "잎 세기", "points": 3, "criterion": "잎의 개수 {BIGN}개를 세어 {BIGN}명으로 답했다.", "partial": "하나 차이면 1점."},
        ],
        rubric_total=5,
    )


# ═══════════════════════════════════════════════════════════════════ 4. 히스토그램과 도수분포다각형 (m1-2-20) — 자료맥락 3단
HG = "m1-2-histogram"
HG_BASE = {"process": "문제해결", "context": "자료맥락", "ops": ["통계", "사칙"], "traps": ["구하는대상혼동"], "qtype": "short",
           "time_limit": 90, "points": 4, "pool_target": 200, "prereq": ["도수분포표", "계급·계급값"], "tags": ["히스토그램", "도수분포다각형"]}
HG_CTX = [("수학 점수", "점", 50, 10), ("키", "cm", 140, 5), ("100 m 달리기 기록", "초", 14, 2), ("하루 운동 시간", "분", 20, 10), ("몸무게", "kg", 40, 5)]


def _hg_rows():
    rnd = random.Random(2020)
    rows = {}
    i = 0
    while len(rows) < 120:
        ctx, unit, base0, cw = rnd.choice(HG_CTX)
        s0 = base0 + cw * rnd.choice([0, 1, 2])
        f = [rnd.choice([2, 3, 4, 5, 6, 7, 8, 9, 10, 12]) for _ in range(5)]
        if f.count(max(f)) != 1:
            continue
        N = sum(f)
        bins = [f"{s0 + cw*j}~{s0 + cw*(j+1)}" for j in range(5)]
        j = f.index(max(f))
        mid = Fraction(2 * s0 + cw * (2 * j + 1), 2)
        X = s0 + cw * rnd.choice([2, 3])
        jx = (X - s0) // cw
        cntX = sum(f[jx:])
        i += 1
        rows[f"H{i}"] = {"CTX": ctx, "U": unit, "S0": s0, "CW": cw, "N": N, "BINS": bins, "F": f, "F1": f[0], "F2": f[1], "F3": f[2], "F4": f[3], "F5": f[4],
                         "JMAX": j, "LOMAX": s0 + cw * j, "HIMAX": s0 + cw * (j + 1), "MIDn": mid.numerator, "MIDd": mid.denominator,
                         "X": X, "CNTX": cntX, "AREA": cw * N, "FMAX": max(f)}
    return rows


HG_ROWS = _hg_rows()
for _r in HG_ROWS.values():                   # 표기 칸(09-25 3차) — UU: cm·kg 는 띄어 씀, UR: 단위 뒤 조사용 읽는 소리, SC: 점수(100점 상한) 표시
    _r["UU"], _r["UR"], _r["SC"] = UNIT_UU.get(_r["U"], _r["U"]), UNIT_UR[_r["U"]], int(_r["CTX"] == "수학 점수")
HG_FIG = [{"fn": "hist", "args": {"bins": "{BINS}", "counts": "{F}", "labels": "도수(명)"}}]


def _hg2_rows():
    """t2 전용 — 기준 이상·미만 계급을 도수와 함께 적은 칸(GEB·GESUM·LTB·LTSUM)을 더한다 (09-25: [전개]가 그림 없이 따라갈 수 없었다).
    현실 범위(09-25 2차): 수학 점수는 100점에서 끝나게 내리고, 100 m 달리기는 계급의 크기 1초로 13~20초 안에,
    몸무게는 35·40 kg 에서 시작해 가운데 계급(45~55 kg)에 도수가 몰리게(큰 도수를 가운데로) 다시 놓는다.
    기준값은 원래처럼 3·4번째 계급의 시작값. t2 가 쓰는 칸만 남긴다."""
    out = {}
    for n, (k, r) in enumerate(HG_ROWS.items()):
        s0, cw, f = r["S0"], r["CW"], list(r["F"])
        jx = (r["X"] - s0) // cw
        if r["CTX"] == "수학 점수":
            s0 = min(s0, 100 - 5 * cw)
        elif r["CTX"] == "100 m 달리기 기록":
            s0, cw = 13 + n % 3, 1
        elif r["CTX"] == "몸무게":
            s0 = 35 if n % 2 else 40
            order = [2, 1, 3, 0, 4] if n % 2 else [2, 3, 1, 4, 0]
            hump = [0] * 5
            for pos, c in zip(order, sorted(f, reverse=True)):
                hump[pos] = c
            f = hump
        bins = [f"{s0 + cw*i}~{s0 + cw*(i+1)}" for i in range(5)]
        lab = [f"{b}{r['UU']} {c}명" for b, c in zip(bins, f)]
        out[k] = {"CTX": r["CTX"], "U": r["U"], "UU": r["UU"], "UR": r["UR"], "S0": s0, "CW": cw, "N": sum(f), "BINS": bins, "F": f,
                  "F1": f[0], "F2": f[1], "F3": f[2], "F4": f[3], "F5": f[4], "X": s0 + cw * jx, "CNTX": sum(f[jx:]),
                  "GEB": ", ".join(lab[jx:]), "GESUM": " + ".join(str(c) for c in f[jx:]),
                  "LTB": ", ".join(lab[:jx]), "LTSUM": " + ".join(str(c) for c in f[:jx])}
    return out


HG2_ROWS = _hg2_rows()


def hg_t1():
    return tpl(HG, 1, HG_BASE,
        title="히스토그램에서 도수가 가장 큰 계급의 계급값 구하기",
        skill="히스토그램의 가장 높은 직사각형에서 계급을 읽고, 계급값 = (양 끝 값의 합) ÷ 2 로 구하기",
        variant_axis={"자료": "점수·키·기록·시간·몸무게", "계급의 크기": "2·5·10"},
        discriminates="도수(높이)가 가장 큰 계급을 고르고, 계급값을 계급의 한가운데 값으로 구하는가 (도수를 답하지 않는가)",
        difficulty=2,
        params=[{"name": "k", "values": {"in": list(HG_ROWS)}}],
        table={"key": "k", "rows": HG_ROWS},
        derive={"ansv": "MIDn/MIDd"},
        constraints=["FMAX >= 1", "SC == 0 or S0 + 5*CW <= 100"],   # 수학 점수 계급이 100점을 넘는 행은 뺀다 (09-25 3차)
        cost_values=["N", "CW", "ansv"],
        answer_var="ansv",
        verify=["2*ans == LOMAX + HIMAX", "LOMAX < ans", "ans < HIMAX"],
        question="다음은 학생 {N}명의 {CTX}{eul(CTX)} 조사하여 나타낸 히스토그램이다. 도수가 가장 큰 계급의 계급값을 구하시오.",
        figure=HG_FIG,
        answer="{dec(ansv)}", answer_alt=["{dec(ansv)}{U}", "{dec(ansv)} {U}"],
        sol1="히스토그램에서 직사각형의 높이가 도수이므로 가장 높은 직사각형이 도수가 가장 큰 계급이다. 계급값은 그 계급의 양 끝 값을 더해 2로 나눈 한가운데 값이다.",
        sol2=["가장 높은 직사각형의 계급: {LOMAX}{UU} 이상 {HIMAX}{UU} 미만 (도수 {FMAX}명)", "계급값 = ({LOMAX} + {HIMAX}) ÷ 2 = {dec(ansv)} ({U})"],
        sol2_fig=steps([{"text": "도수 최대: {LOMAX} ~ {HIMAX} ({FMAX}명)", "hint": "가장 높은 직사각형"}, {"text": "({LOMAX} + {HIMAX}) ÷ 2 = {dec(ansv)}", "marks": [{"on": "{dec(ansv)}", "note": "도수 {FMAX}{eul(FMAX)} 답하지 말 것"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="계급값 {dec(ansv)}{UU}{eun(UR)} {LOMAX}{UU}{wa(UR)} {HIMAX}{UU}의 한가운데이므로 계급 안에 있다. 답은 {dec(ansv)}{UU}{ida(UR)}.",
        sol3_fig=steps(["{LOMAX} < {dec(ansv)} < {HIMAX}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="도수가 가장 큰 계급은 {LOMAX}{UU} 이상 {HIMAX}{UU} 미만이므로 계급값은 ({LOMAX} + {HIMAX}) ÷ 2 = {dec(ansv)} ({U})이다.",
        rubric=[
            {"element": "계급 찾기", "points": 2, "criterion": "가장 높은 직사각형의 계급 {LOMAX}~{HIMAX}{UU}{eul(UR)} 골랐다.", "partial": "다른 계급을 골랐으면 인정하지 않는다."},
            {"element": "계급값 구하기", "points": 3, "criterion": "({LOMAX} + {HIMAX}) ÷ 2 = {dec(ansv)}{eul(ansv)} 구했다.", "partial": "계급의 크기나 도수를 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def hg_t2():
    return tpl(HG, 2, HG_BASE,
        title="히스토그램에서 어떤 값 이상인 학생 수 구하기",
        skill="히스토그램에서 기준 이상인 계급들의 도수를 모두 더하기",
        variant_axis={"기준": "3·4번째 계급의 시작값", "자료": "점수·키·기록·시간·몸무게"},
        discriminates="기준이 계급의 경계일 때 그 계급부터 오른쪽 계급의 도수를 빠짐없이 더하는가",
        difficulty=2,
        params=[{"name": "k", "values": {"in": list(HG2_ROWS)}}],
        table={"key": "k", "rows": HG2_ROWS},
        derive={"ansv": "CNTX"},
        constraints=["CNTX >= 1", "CNTX != N", "CNTX != X"],
        cost_values=["N", "X", "CNTX"],
        answer_var="ansv",
        verify=["ans == CNTX", "ans < N", "F1 + F2 + F3 + F4 + F5 == N"],
        question="다음은 학생 {N}명의 {CTX}{eul(CTX)} 조사하여 나타낸 히스토그램이다. {CTX}{ika(CTX)} {X}{UU} 이상인 학생은 모두 몇 명인지 구하시오.",
        figure=HG_FIG,
        answer="{ansv}", answer_alt=["{ansv}명"],
        sol1="히스토그램의 각 직사각형의 높이가 그 계급의 도수(학생 수)다. {X}{UU} 이상인 학생은 {X}{UU}에서 시작하는 계급부터 오른쪽 계급들의 도수를 모두 더하면 된다.",
        sol2=["{X}{UU} 이상인 계급과 그 도수(직사각형의 높이)를 읽으면 {GEB}", "이 도수를 모두 더하면 {GESUM} = {CNTX} (명)"],
        sol2_fig=steps([{"text": "{GEB}", "hint": "{X}{UU}에서 시작하는 계급부터 (경계값은 그 계급에 포함)"}, {"text": "{GESUM} = {CNTX}", "marks": [{"on": "{CNTX}", "note": "전체 {N}명 중"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="나머지 {X}{UU} 미만인 계급은 {LTB}이므로 {LTSUM} = {N - CNTX} (명)이다. {CNTX} + {N - CNTX} = {N}{ro(N)} 전체 학생 수와 맞다. 답은 {CNTX}명이다.",
        sol3_fig=steps(["{X}{UU} 미만: {LTSUM} = {N - CNTX}", "{CNTX} + {N - CNTX} = {N}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{X}{UU} 이상인 계급의 도수는 {GEB}이므로 모두 더하면 {GESUM} = {CNTX} (명)이다.",
        rubric=[
            {"element": "계급 고르기", "points": 2, "criterion": "{X}{UU} 이상인 계급들을 빠짐없이 골랐다.", "partial": "경계 계급을 빠뜨렸으면 1점."},
            {"element": "도수 더하기", "points": 3, "criterion": "도수의 합 {CNTX}명을 구했다.", "partial": "덧셈 실수면 1점."},
        ],
        rubric_total=5,
    )


def hg_t3():
    return tpl(HG, 3, HG_BASE,
        title="히스토그램의 직사각형의 넓이의 합(도수분포다각형과 가로축 사이의 넓이) = 계급의 크기 × 도수의 총합",
        skill="히스토그램에서 직사각형의 넓이의 합이 (계급의 크기) × (도수의 총합)이고, 도수분포다각형과 가로축으로 둘러싸인 넓이와 같음을 알고 구하기",
        variant_axis={"묻는 것": "직사각형의 넓이의 합 / 도수분포다각형 아래 넓이", "계급의 크기": "2·5·10"},
        discriminates="넓이의 합을 계급의 크기와 도수의 총합의 곱으로 구하는가 (도수의 합만 답하지 않는가)",
        difficulty=3, points=5,
        params=[{"name": "q", "values": {"in": ["hist", "poly"]}}, {"name": "k", "values": {"in": list(HG_ROWS)}}],
        table=[{"key": "q", "rows": {"hist": {"QW": "히스토그램의 각 직사각형의 넓이의 합"}, "poly": {"QW": "이 히스토그램에서 만든 도수분포다각형과 가로축으로 둘러싸인 부분의 넓이"}}}, {"key": "k", "rows": HG_ROWS}],
        derive={"ansv": "AREA"},
        constraints=["AREA != N", "AREA != CW", "SC == 0 or S0 + 5*CW <= 100"],   # 수학 점수 계급이 100점을 넘는 행은 뺀다 (09-25 3차, t1 과 같은 기준)
        cost_values=["N", "CW", "AREA"],
        answer_var="ansv",
        verify=["ans == CW*N", "F1 + F2 + F3 + F4 + F5 == N"],
        question="다음은 학생 {N}명의 {CTX}{eul(CTX)} 조사하여 나타낸 히스토그램이다. 계급의 크기가 {CW}{UU}일 때, {QW}{eul(QW)} 구하시오.",
        figure=HG_FIG,
        answer="{ansv}", answer_alt=[],
        sol1="히스토그램의 직사각형은 가로가 계급의 크기, 세로가 도수이므로 넓이는 (계급의 크기) × (도수)다. 모든 직사각형의 넓이를 더하면 (계급의 크기) × (도수의 총합)이 되고, 도수분포다각형과 가로축으로 둘러싸인 넓이도 이와 같다.",
        sol2=["직사각형 하나의 넓이 = (계급의 크기) × (도수)", "넓이의 합 = (계급의 크기) × (도수의 총합) = {CW} × {N} = {AREA}"],
        sol2_fig=steps([{"text": "넓이 = {CW} × (도수)", "hint": "가로는 모두 {CW}"}, {"text": "{CW} × ({F1} + {F2} + {F3} + {F4} + {F5}) = {CW} × {N} = {AREA}", "marks": [{"on": "{AREA}", "note": "도수분포다각형 아래 넓이와 같다"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="직사각형을 하나씩 계산해 더해도 {CW} × {F1} + {CW} × {F2} + … = {AREA}{ro(AREA)} 같다. 답은 {AREA}{ida(AREA)}.",
        sol3_fig=steps(["{CW} × ({F1} + {F2} + {F3} + {F4} + {F5}) = {AREA}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="직사각형의 넓이의 합은 (계급의 크기) × (도수의 총합) = {CW} × {N} = {AREA}이고, 도수분포다각형과 가로축으로 둘러싸인 부분의 넓이도 이와 같다.",
        rubric=[
            {"element": "넓이의 구조", "points": 3, "criterion": "넓이의 합이 (계급의 크기) × (도수의 총합)임을 밝혔다.", "partial": "직사각형 하나의 넓이만 구했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{CW} × {N} = {AREA}{eul(AREA)} 구했다.", "partial": "도수의 총합 {N}{eul(N)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# ═══════════════════════════════════════════════════════════════════ 5. 이차방정식 구하기 (m3-1-20) — 3단
QB = "m3-1-quad-build"
QB_BASE = {"process": "절차수행", "context": "무맥락", "ops": ["방정식", "인수분해"], "traps": ["부호"], "qtype": "short",
           "time_limit": 90, "points": 4, "pool_target": 300, "prereq": ["인수분해", "이차방정식의 해"], "tags": ["이차방정식", "두 근"]}


def qb_t1():
    return tpl(QB, 1, QB_BASE,
        title="두 근이 주어진 이차방정식 만들기 — a(x − p)(x − q) = 0 을 전개해 계수 읽기",
        skill="두 근 p, q 와 x² 의 계수 a 가 주어진 이차방정식을 a(x − p)(x − q) = 0 으로 세우고 전개하여 ax² + bx + c = 0 의 b, c 를 구하기",
        variant_axis={"구하는 것": "b / c / b + c", "x² 의 계수": "1~3", "두 근": "−6~6"},
        discriminates="근이 p 이면 인수가 (x − p) 임을 알고(부호), 전개할 때 a 를 모든 항에 곱하는가",
        difficulty=2,
        params=[{"name": "q1", "values": {"in": ["b", "c", "bc"]}}, {"name": "a", "values": {"int": [1, 3]}}, {"name": "p", "values": {"int": [-6, 6]}}, {"name": "q", "values": {"int": [-6, 6]}}],
        table={"key": "q1", "rows": {"b": {"QT": "b", "w1": 1, "w2": 0}, "c": {"QT": "c", "w1": 0, "w2": 1}, "bc": {"QT": "b + c", "w1": 1, "w2": 1}}},
        derive={"b": "-a*(p + q)", "c": "a*p*q", "ans": "w1*(-a*(p + q)) + w2*(a*p*q)", "s": "p + q", "m": "p*q"},
        constraints=["p < q", "p != 0", "q != 0", "ans != p", "ans != q", "ans != a", "ans != 0"],
        cost_values=["a", "p", "q", "ans"],
        answer_var="ans",
        verify=["a*p*p + b*p + c == 0", "a*q*q + b*q + c == 0", "ans == w1*b + w2*c"],
        question="두 근이 {p}, {q}이고 x²의 계수가 {a}인 이차방정식을 {a}x² + bx + c = 0 꼴로 나타낼 때, {QT}의 값을 구하시오." if False else None,   # a=1 일 때 "1x²" 을 피하려 qb_t1_fix
        answer="{ans}", answer_alt=[],
        sol1="두 근이 p, q 이고 x²의 계수가 a 인 이차방정식은 a(x − p)(x − q) = 0 이다. 근이 {p}이면 인수는 (x − {pn(p)}) 이므로 부호에 주의해 인수를 만든 뒤 전개하여 계수를 읽는다.",
        # 전개 줄에 x² − (합)x + (곱) 을 그대로 쓰면 합·곱이 ±1 일 때 '1x'·'× 1' 이 나온다 → 합·곱은 말로, 식은 정리된 꼴로
        sol2=["{co(a)}(x − {pn(p)})(x − {pn(q)}) = 0", "두 근의 합은 {s}, 두 근의 곱은 {m}이므로 전개하면 {co(a)}x² {sgt(b)}x {sgn(c)} = 0", "따라서 b = {b}, c = {c}이고 {QT} = {ans}"],
        sol2_fig=steps([{"text": "{co(a)}(x − {pn(p)})(x − {pn(q)}) = 0", "hint": "근 p → 인수 (x − p)", "marks": [{"on": "{pn(p)}", "note": "음수 근이면 부호가 바뀐다"}]},
                        {"text": "{co(a)}x² {sgt(b)}x {sgn(c)} = 0", "hint": "a 를 모든 항에 곱한다"},
                        {"text": "b = {b}, c = {c} → {QT} = {ans}"}]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="x = {p}{eul(p)} 대입하면 인수 (x − {pn(p)})가 0이 되어 좌변 전체가 0이고, x = {q}{eul(q)} 대입해도 마찬가지다. 답은 {ans}이다.",
        sol3_fig=steps(["x = {p} 대입 → 0  ✓", "x = {q} 대입 → 0  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="두 근이 {p}, {q}이고 x²의 계수가 {a}이므로 {co(a)}(x − {pn(p)})(x − {pn(q)}) = 0, 전개하면 {co(a)}x² {sgt(b)}x {sgn(c)} = 0이다. 따라서 b = {b}, c = {c}이고 {QT} = {ans}이다.",
        rubric=[
            {"element": "인수 만들기", "points": 3, "criterion": "{co(a)}(x − {pn(p)})(x − {pn(q)}) = 0 꼴로 세웠다.", "partial": "근의 부호를 바꿔 인수를 만들었으면 인정하지 않는다."},
            {"element": "전개", "points": 2, "criterion": "{co(a)}x² {sgt(b)}x {sgn(c)} = 0으로 전개했다.", "partial": "a 를 한 항에만 곱했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 구했다.", "partial": "다른 계수를 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def qb_t1_split(t):
    """x² 의 계수 1 은 '1x²' 이 아니라 'x²' 로 써야 한다 → a=1 틀과 a≥2 틀을 나눈다."""
    out = []
    for no, avals, q in ((1, [1], "두 근이 {p}, {q}이고 x²의 계수가 1인 이차방정식을 x² + bx + c = 0 꼴로 나타낼 때, {QT}의 값을 구하시오."),
                         (4, [2, 3], "두 근이 {p}, {q}이고 x²의 계수가 {a}인 이차방정식을 {a}x² + bx + c = 0 꼴로 나타낼 때, {QT}의 값을 구하시오.")):
        u = dict(t)
        u["id"] = f"{QB}-t{no}"
        u["params"] = [p for p in t["params"] if p["name"] != "a"] + [{"name": "a", "values": {"in": avals}}]
        u["question"] = q
        u["title"] = t["title"] + (" (x² 의 계수 1)" if no == 1 else " (x² 의 계수 2·3)")
        if no == 4:
            _qb_t4_distribute(u)
        out.append(u)
    return out


def _qb_t4_distribute(u):
    """t4 (a = 2·3) — 이 틀이 재려는 'a 를 모든 항에 곱하기'를 해설에 드러낸다 (09-25 스크리닝):
    (x − p)(x − q) 를 먼저 x² − (합)x + (곱) 으로 정리하고, a(…) = ax² + bx + c 로 a 를 세 항에 나눠 곱하는 줄을 따로 둔다.
    x 의 계수는 {sgt()} 로 써서 합이 ±1 이어도 '1x' 가 나오지 않고, a × (계수) 곱셈은 쓰지 않아 '× 1' 도 없다.
    합이 0 이면 괄호 안이 'x² + 0x − …' 가 되므로 그 조합은 뺀다."""
    u["derive"] = dict(u["derive"], nb="-(p + q)")
    u["constraints"] = u["constraints"] + ["p + q != 0"]
    u["verify"] = u["verify"] + ["a*nb == b", "a*m == c"]
    u["sol1"] = ("두 근이 p, q이고 x²의 계수가 a인 이차방정식은 a(x − p)(x − q) = 0이다. 근이 {p}이면 인수는 (x − {pn(p)})이므로 부호에 주의해 인수를 만든다. "
                 "전개할 때는 괄호 두 개를 먼저 곱해 정리한 뒤, 앞의 {a}{eul(a)} x² 항만이 아니라 x 항과 상수항에도 모두 곱해야 한다.")
    u["sol2"] = ["{a}(x − {pn(p)})(x − {pn(q)}) = 0",
                 "괄호 두 개를 먼저 곱하면 (x − {pn(p)})(x − {pn(q)}) = x² {sgt(nb)}x {sgn(m)} (두 근의 합 {s}, 곱 {m})",
                 "{a}{eul(a)} 세 항에 모두 곱하면 {a}(x² {sgt(nb)}x {sgn(m)}) = {a}x² {sgt(b)}x {sgn(c)} = 0",
                 "{a}x² + bx + c = 0과 비교하면 b = {b}, c = {c}이므로 구하는 {QT}의 값은 {ans}"]
    u["sol2_fig"] = steps([{"text": "{a}(x − {pn(p)})(x − {pn(q)}) = 0", "hint": "근 p → 인수 (x − p)", "marks": [{"on": "(x − {pn(p)})", "note": "x에서 근 {p}{eul(p)} 뺀다"}]},
                           {"text": "(x − {pn(p)})(x − {pn(q)}) = x² {sgt(nb)}x {sgn(m)}", "hint": "합 {s}, 곱 {m}"},
                           {"text": "{a}(x² {sgt(nb)}x {sgn(m)}) = {a}x² {sgt(b)}x {sgn(c)}", "hint": "{a}{eul(a)} 모든 항에 곱한다", "marks": [{"on": "{a}x²", "note": "x 항·상수항에도 {a}배"}]},
                           {"text": "b = {b}, c = {c} → {QT}의 값 {ans}"}])
    u["sol2_anim"] = [[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]]
    # 괄호 뒤 조사는 괄호 안 마지막 수(근)의 소리로 — '(x − (-6))이' / '(x − 5)가'
    u["sol3"] = "x = {p}{eul(p)} 대입하면 인수 (x − {pn(p)}){ika(p)} 0이 되어 좌변 전체가 0이고, x = {q}{eul(q)} 대입해도 마찬가지다. 답은 {ans}이다."
    u["model_answer"] = ("두 근이 {p}, {q}이고 x²의 계수가 {a}이므로 {a}(x − {pn(p)})(x − {pn(q)}) = 0이다. (x − {pn(p)})(x − {pn(q)}) = x² {sgt(nb)}x {sgn(m)}이고, "
                         "{a}{eul(a)} 모든 항에 곱하면 {a}x² {sgt(b)}x {sgn(c)} = 0이다. 따라서 b = {b}, c = {c}이므로 구하는 {QT}의 값은 {ans}이다.")
    u["rubric"] = [
        {"element": "인수 만들기", "points": 3, "criterion": "{a}(x − {pn(p)})(x − {pn(q)}) = 0 꼴로 세웠다.", "partial": "근 p의 인수를 (x + p)로 썼으면 인정하지 않는다."},
        {"element": "전개", "points": 2, "criterion": "{a}(x² {sgt(nb)}x {sgn(m)}) = {a}x² {sgt(b)}x {sgn(c)} = 0으로 {a}{eul(a)} 모든 항에 곱해 전개했다.", "partial": "a를 한 항에만 곱했으면 1점."},
        {"element": "답 구하기", "points": 2, "criterion": "{QT}의 값 {ans}{eul(ans)} 구했다.", "partial": "다른 계수를 답했으면 인정하지 않는다."},
    ]


def qb_t2():
    return tpl(QB, 2, QB_BASE,
        title="중근이 주어진 이차방정식 만들기 — a(x − p)² = 0",
        skill="중근 x = p 를 갖고 x² 의 계수가 a 인 이차방정식이 a(x − p)² = 0 임을 알고 전개하여 상수항(또는 x 의 계수)을 구하기",
        variant_axis={"구하는 것": "c / b", "x² 의 계수": "1~3", "중근": "−7~7"},
        discriminates="중근은 (x − p)² 으로 인수가 두 번 겹침을 알고 완전제곱식을 바르게 전개하는가",
        difficulty=2,
        params=[{"name": "q1", "values": {"in": ["c", "b"]}}, {"name": "a", "values": {"int": [1, 3]}}, {"name": "p", "values": {"int": [-7, 7]}}],
        table={"key": "q1", "rows": {"c": {"QT": "c", "w1": 0, "w2": 1}, "b": {"QT": "b", "w1": 1, "w2": 0}}},
        derive={"b": "-2*a*p", "c": "a*p*p", "ans": "w1*(-2*a*p) + w2*(a*p*p)", "p2": "p*p"},
        constraints=["p != 0", "ans != p", "ans != a", "abs(p) != 1"],
        cost_values=["a", "p", "ans"],
        answer_var="ans",
        verify=["a*p*p + b*p + c == 0", "b*b == 4*a*c", "ans == w1*b + w2*c"],
        question=None,   # qb_t2_split
        answer="{ans}", answer_alt=[],
        sol1="중근 x = p 를 갖는 이차방정식은 (x − p)² 을 인수로 갖는다. 따라서 x²의 계수가 a 이면 a(x − p)² = 0 이고, 완전제곱식을 전개하면 b 와 c 가 나온다.",
        sol2=["{co(a)}(x − {pn(p)})² = 0", "전개하면 {co(a)}(x² − 2 × {pn(p)}x + {pn(p)}²) = 0, 즉 {co(a)}x² {sgt(b)}x {sgn(c)} = 0", "따라서 b = {b}, c = {c}이고 {QT} = {ans}"],
        sol2_fig=steps([{"text": "{co(a)}(x − {pn(p)})² = 0", "hint": "중근 → 같은 인수 두 번"},
                        {"text": "(x − p)² = x² − 2px + p²", "hint": "완전제곱식", "marks": [{"on": "2px", "note": "가운데 항은 2배"}]},
                        {"text": "{co(a)}x² {sgt(b)}x {sgn(c)} = 0 → {QT} = {ans}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="중근을 가지므로 b² − 4ac = 0이 되어야 하는데, 실제로 b² − 4ac = {b*b} − {4*a*c} = 0이다. 답은 {ans}이다.",
        sol3_fig=steps(["b² − 4ac = {b*b} − {4*a*c} = 0  ✓"]),
        sol3_anim=[[reveal(0)]],
        model_answer="중근이 {p}이고 x²의 계수가 {a}이므로 {co(a)}(x − {pn(p)})² = 0, 전개하면 {co(a)}x² {sgt(b)}x {sgn(c)} = 0이다. 따라서 {QT} = {ans}이다.",
        rubric=[
            {"element": "완전제곱 꼴 세우기", "points": 3, "criterion": "{co(a)}(x − {pn(p)})² = 0 으로 세웠다.", "partial": "(x − p) 를 한 번만 썼으면 인정하지 않는다."},
            {"element": "전개", "points": 2, "criterion": "{co(a)}x² {sgt(b)}x {sgn(c)} = 0 으로 전개했다.", "partial": "가운데 항의 2배를 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 구했다.", "partial": "다른 계수를 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def qb_t2_split(t):
    out = []
    for no, avals, q in ((2, [1], "x = {p}{eul(p)} 중근으로 갖고 x²의 계수가 1인 이차방정식을 x² + bx + c = 0 꼴로 나타낼 때, {QT}의 값을 구하시오."),
                         (5, [2, 3], "x = {p}{eul(p)} 중근으로 갖고 x²의 계수가 {a}인 이차방정식을 {a}x² + bx + c = 0 꼴로 나타낼 때, {QT}의 값을 구하시오.")):
        u = dict(t)
        u["id"] = f"{QB}-t{no}"
        u["params"] = [p for p in t["params"] if p["name"] != "a"] + [{"name": "a", "values": {"in": avals}}]
        u["question"] = q
        u["title"] = t["title"] + (" (x² 의 계수 1)" if no == 2 else " (x² 의 계수 2·3)")
        if no == 2:   # 계수 1 이면 전개식에 괄호가 필요 없다
            u["sol2"] = [x.replace("{co(a)}(x² − 2 × {pn(p)}x + {pn(p)}²) = 0", "x² − 2 × {pn(p)}x + {pn(p)}² = 0") for x in t["sol2"]]
        out.append(u)
    return out


def _qb3_rows():
    """옳은 두 근 r < s (정수) — 민수는 x 의 계수를 잘못 봐서 상수항 rs 는 맞게 보고 두 근 p1·q1 (p1·q1 = rs),
    지연이는 상수항을 잘못 봐서 x 의 계수는 맞게 보고 두 근 p2·q2 (p2 + q2 = r + s). 잘못 본 근은 옳은 근과 달라야 한다."""
    rows = {}
    for r in range(-6, 7):
        for s in range(r + 1, 8):
            if r == 0 or s == 0:
                continue
            prod, ssum = r * s, r + s
            # p1·q1 = prod, {p1,q1} != {r,s}
            for p1 in range(-12, 13):
                if p1 == 0 or prod % p1:
                    continue
                q1 = prod // p1
                if p1 >= q1 or {p1, q1} == {r, s}:
                    continue
                # p2 + q2 = ssum, {p2,q2} != {r,s}, p2 < q2
                for p2 in range(-9, 10):
                    q2 = ssum - p2
                    if p2 >= q2 or {p2, q2} == {r, s} or {p2, q2} == {p1, q1}:
                        continue
                    if s in (p1, q1, p2, q2):            # 답이 문면의 수와 같으면 뺀다 (R-05)
                        continue
                    key = f"{r}|{s}|{p1}|{q1}|{p2}|{q2}"
                    rows[key] = {"r": r, "s": s, "p1": p1, "q1": q1, "p2": p2, "q2": q2, "bb": -ssum, "cc": prod}
    # 너무 많으면 고르게 솎는다
    keys = list(rows)
    rnd = random.Random(3130)
    rnd.shuffle(keys)
    return {k: rows[k] for k in sorted(keys[:400])}


QB3_ROWS = _qb3_rows()


def qb_t3():
    return tpl(QB, 3, QB_BASE,
        title="계수를 잘못 보고 푼 두 사람의 근에서 원래 이차방정식의 옳은 근 구하기",
        skill="x 의 계수를 잘못 본 사람의 두 근에서는 상수항이, 상수항을 잘못 본 사람의 두 근에서는 x 의 계수가 맞음을 이용해 원래 방정식을 세우고 풀기",
        variant_axis={"옳은 두 근": "−6~7 (정수)", "잘못 본 근": "곱·합이 같은 다른 짝"},
        discriminates="누가 무엇을 맞게 보았는지 가려내어(잘못 본 것의 반대 계수가 맞다) 원래 방정식을 복원하는가",
        difficulty=4, time_limit=150, points=5, process="문제해결",
        params=[{"name": "k", "values": {"in": list(QB3_ROWS)}}],
        table={"key": "k", "rows": QB3_ROWS},
        derive={"ans": "s"},
        constraints=["r < s"],
        cost_values=["p1", "q1", "p2", "q2", "ans"],
        answer_var="ans",
        verify=["ans*ans + bb*ans + cc == 0", "r*r + bb*r + cc == 0", "p1*q1 == cc", "p2 + q2 == -bb"],
        question="이차방정식 x² + bx + c = 0을 푸는데, 민수는 x의 계수를 잘못 보고 풀어 두 근 {p1}, {q1}을 얻었고, 지연이는 상수항을 잘못 보고 풀어 두 근 {p2}, {q2}를 얻었다. 이 이차방정식의 옳은 두 근 중 큰 근을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x의 계수를 잘못 본 민수는 상수항 c는 맞게 보았으므로 민수의 두 근의 곱이 c다. 상수항을 잘못 본 지연이는 x의 계수 b는 맞게 보았으므로 지연이의 두 근의 합이 −b다. 이렇게 b, c를 복원해 원래 방정식을 풀면 된다.",
        sol2=["민수: (x − {pn(p1)})(x − {pn(q1)}) = 0 → 상수항 c = {pn(p1)} × {pn(q1)} = {cc}", "지연: (x − {pn(p2)})(x − {pn(q2)}) = 0 → x의 계수 b = −({pn(p2)} + {pn(q2)}) = {bb}",
              "원래 방정식 x² {sgt(bb)}x {sgn(cc)} = 0 → (x − {pn(r)})(x − {pn(s)}) = 0 → x = {r} 또는 x = {s}, 큰 근은 {s}"],
        sol2_fig=steps([{"text": "c = {pn(p1)} × {pn(q1)} = {cc}", "hint": "x 의 계수를 잘못 봄 → 상수항은 맞음"},
                        {"text": "b = −({pn(p2)} + {pn(q2)}) = {bb}", "hint": "상수항을 잘못 봄 → x 의 계수는 맞음", "marks": [{"on": "−", "note": "합의 부호를 바꾼다"}]},
                        {"text": "x² {sgt(bb)}x {sgn(cc)} = 0 → x = {r}, {s}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="옳은 두 근 {r}, {s}의 합은 {r + s}, 곱은 {cc}이므로 지연이의 두 근의 합 {p2} + {pn(q2)} = {r + s}, 민수의 두 근의 곱 {p1} × {pn(q1)} = {cc}{wa(cc)} 각각 같다. 큰 근은 {s}이다.",
        sol3_fig=steps(["합: {p2} + {pn(q2)} = {r} + {pn(s)} = {r + s}", "곱: {p1} × {pn(q1)} = {r} × {pn(s)} = {cc}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="민수는 상수항을 맞게 보았으므로 c = {pn(p1)} × {pn(q1)} = {cc}이고, 지연이는 x의 계수를 맞게 보았으므로 b = −({pn(p2)} + {pn(q2)}) = {bb}이다. 따라서 원래 방정식은 x² {sgt(bb)}x {sgn(cc)} = 0이고 (x − {pn(r)})(x − {pn(s)}) = 0에서 옳은 두 근은 {r}, {s}이므로 큰 근은 {s}이다.",
        rubric=[
            {"element": "상수항 복원", "points": 3, "criterion": "민수의 두 근의 곱으로 c = {cc}{eul(cc)} 구했다.", "partial": "누구의 근을 써야 하는지 바꿨으면 인정하지 않는다."},
            {"element": "x 의 계수 복원", "points": 3, "criterion": "지연이의 두 근의 합으로 b = {bb}{eul(bb)} 구했다.", "partial": "합의 부호를 바꾸지 않았으면 1점."},
            {"element": "옳은 근 구하기", "points": 2, "criterion": "x² {sgt(bb)}x {sgn(cc)} = 0을 풀어 큰 근 {s}{eul(s)} 구했다.", "partial": "작은 근을 답했으면 1점."},
        ],
        rubric_total=8,
    )


# ═══════════════════════════════════════════════════════════════════ 생성
def main():
    out = []
    out.append(seed(CG, "삼각형의 합동 — 대응각·둘레·남은 변", ["m1-2-06"], "합동인 두 삼각형의 대응 관계(A↔D, B↔E, C↔F)를 꼭짓점 순서로 읽는 훈련. 답이 문면의 각·변과 겹치지 않는 축만 골랐다. 대응각 틀은 그림 라벨이 달라 변주별로 t1·t4·t5.", [cg_t1("AB_F", 1), cg_t1("BC_D", 4), cg_t1("AC_E", 5), cg_t2(), cg_t3()], category="도형", schema_name="삼각형의 합동 — 대응각·대응변", geometry=True))
    out.append(seed(RV, "회전체 — 단면·회전체의 부피", ["m1-2-13"], "회전축을 품은 단면(직사각형·이등변삼각형), 축에 수직인 단면(원), 직각삼각형의 회전체(원뿔). 원뿔 부피는 회전체 개념과 잇는 자리.", [rv_t1()] + rv_t2_split(rv_t2()) + [rv_t3()], category="도형", schema_name="회전체의 단면", geometry=True))
    out.append(seed(SL, "줄기와 잎 그림 — 이상인 자료 수·k번째 값·줄기별 개수", ["m1-2-18"], "자료를 표에 통째로 굽고(stems·leaves) 답도 파이썬에서 세었다. 문면에 N·기준값·k 를 두어 그림만 다른 문항이 겹치지 않게.", [sl_t1(), sl_t2(), sl_t3()], category="활용", schema_name="줄기와 잎 그림 읽기"))
    out.append(seed(HG, "히스토그램·도수분포다각형 — 계급값·이상인 도수·넓이", ["m1-2-20"], "5계급 히스토그램(hist 도식). 도수는 그림에서 읽고 문면에는 N·계급의 크기·기준값을 둔다.", [hg_t1(), hg_t2(), hg_t3()], category="활용", schema_name="히스토그램 읽기"))
    out.append(seed(QB, "이차방정식 구하기 — 두 근·중근·잘못 본 문제", ["m3-1-20"], "a(x−p)(x−q)=0 전개, a(x−p)²=0 전개, 계수를 잘못 본 두 사람의 근에서 복원(고전 유형). x² 계수 1 은 문면에서 '1x²' 이 되지 않게 틀을 나눴다.",
                    qb_t1_split(qb_t1()) + qb_t2_split(qb_t2()) + [qb_t3()], category="연산", schema_name="두 근으로 이차방정식 만들기"))
    for s in out:
        dump(with_pitfalls(s))


if __name__ == "__main__":
    main()
