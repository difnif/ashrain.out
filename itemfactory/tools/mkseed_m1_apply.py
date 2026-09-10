# itemfactory/tools/mkseed_m1_apply.py — 일차방정식의 활용(m1-1-27) 문장제 시드 생성기 (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m1_apply.py
#     → seeds/m1-1-age.json (나이) · m1-1-consecutive.json (연속하는 수) · m1-1-surplus.json (과부족) · m1-1-purchase.json (두 품목 구매)
#
# 원칙: 조건은 derive 에서 만족하는 꼴로 생성(LOCALGUIDE §3) · 문면에 수치 전부 · 답은 relation+verify 로 재현 ·
#       상황은 그림 하나(표·수직선·막대) · 맥락은 table 파라미터로 변주(요즘 상황) · 채점기준은 활용 표준형 3|3|2 = 8점.
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import COMMON_APPLY, bar, dump, hl, numline, reveal, steps, table, with_pitfalls  # noqa: E402

SCHEMA_AGE = "6576bcea-6568-4bde-8adc-ea440c44a2e0"          # 나이 차이와 배수 관계
SCHEMA_CONSEC = "2f042774-9c12-45bf-be98-06ee850ce27c"       # 연속하는 수 문장제
SCHEMA_SURPLUS = "2820b9fc-b855-4039-8242-0291e86431a1"      # 과부족 문제(배치와 여유인원)
SCHEMA_PURCHASE = "306a40f3-eca2-43df-8cc4-f9a682c99dd0"     # 상품 구입과 거스름돈 구하기

BASE = {**COMMON_APPLY, "prereq": ["일차방정식의 풀이", "문자를 사용한 식"], "traps": ["조건누락", "구하는대상혼동"]}


def tpl(seed_id, no, **kw):
    t = dict(BASE)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


# ═══════════════════════════════════════════════════════════════════ 1. 나이
PAIRS = {
    "1": {"P": "아버지", "C": "아들"},
    "2": {"P": "어머니", "C": "딸"},
    "3": {"P": "이모", "C": "조카"},
    "4": {"P": "삼촌", "C": "조카"},
}
AGE_TABLE = {"key": "c", "rows": PAIRS}
AGE_CPARAM = {"name": "c", "values": {"in": list(PAIRS)}}

AGE_RUBRIC = [
    {"element": "식 세우기", "points": 3, "criterion": "{when} 두 사람의 나이를 각각 문자로 나타내고 배수 관계를 등식 {eq}{ro_eq} 세웠다.", "partial": "두 사람의 나이를 문자로 나타냈으나 등식이 틀렸으면 1점."},
    {"element": "해 구하기", "points": 3, "criterion": "괄호를 풀고 이항하여 {sol}{eul_sol} 바르게 구했다.", "partial": "괄호를 풀어 정리하는 데까지 옳으면 1점."},
    {"element": "답 구하기", "points": 2, "criterion": "구한 값이 문제의 조건에 맞는지 확인하고 답을 {ans}{ro_ans} 썼다.", "partial": "확인 없이 답만 옳게 썼으면 1점."},
]


def age_t1():
    # x년 후 F + x = k(S + x)  ⇐  S, x, k 로 F 를 생성 (정수해 보장)
    return tpl("m1-1-age", 1,
        title="몇 년 후에 나이가 k배가 되는가",
        skill="x년 후 두 사람의 나이를 (현재 나이 + x)로 놓고 배수 관계로 방정식 세우기",
        variant_axis={"구하는 것": "몇 년 후", "시점": "미래", "맥락": "가족 나이"},
        discriminates="x년 후에는 두 사람 모두 x살씩 많아진다는 것을 식에 반영하는가",
        qtype="short", difficulty=2, pool_target=300, tags=["나이", "일차방정식의 활용"],
        # 나이 차 D = (k−1)(S + x) 를 먼저 뽑는다 (24~45세 차이) → 아이의 그때 나이 B = D/(k−1) → 현재 S = B − x
        params=[AGE_CPARAM, {"name": "k", "values": {"in": [2, 3]}}, {"name": "u", "values": {"int": [0, 12]}}, {"name": "x", "values": {"int": [2, 14]}}],
        table=AGE_TABLE,
        derive={"D": "24 + u*(k - 1)", "B": "(24 + u*(k - 1))/(k - 1)", "S": "(24 + u*(k - 1))/(k - 1) - x", "F": "(24 + u*(k - 1))/(k - 1) - x + 24 + u*(k - 1)",
                "A": "k*((24 + u*(k - 1))/(k - 1))", "R": "k*S - F"},
        constraints=["D <= 45", "S >= 6", "S <= 22", "F <= 62", "x != S", "x != k", "x != F"],
        cost_values=["F", "S", "k", "x", "R", "A"],
        relation="F + X - k*(S + X)", unknown="X", answer_var="x",
        verify=["F + ans == k*(S + ans)", "ans > 0"],
        question="현재 {P}의 나이는 {F}세, {C}의 나이는 {S}세이다. {P}의 나이가 {C}의 나이의 {k}배가 되는 것은 몇 년 후인지 구하시오.",
        answer="{x}", answer_alt=["{x}년 후", "{x}년"],
        sol1="'몇 년 후'를 x년 후라 하면 그때는 두 사람 모두 x살씩 많아진다 — 이것이 핵심이다. x년 후 {P}는 ({F} + x)세, {C}는 ({S} + x)세이고, 그때 {P}의 나이가 {C}의 나이의 {k}배이므로 {F} + x = {k}({S} + x)이다. 현재와 x년 후를 표로 나란히 적어 두면 식이 그대로 읽힌다.",
        sol1_fig=table(["", "현재", "x년 후"], [["{P}", "{F}세", "({F} + x)세"], ["{C}", "{S}세", "({S} + x)세"]]),
        sol2=[
            "{P}의 나이가 {C}의 나이의 {k}배가 되는 때를 x년 후라 하자.",
            "x년 후 {P}의 나이는 ({F} + x)세, {C}의 나이는 ({S} + x)세이다.",
            "그때 {P}의 나이가 {C}의 나이의 {k}배이므로 {F} + x = {k}({S} + x)",
            "괄호를 풀면 {F} + x = {k*S} + {co(k)}x",
            "x는 좌변으로, 상수는 우변으로 이항하면 x − {co(k)}x = {k*S} − {F}, 곧 {co(1-k)}x = {k*S - F}",
            "양변을 {1-k}{ro(1-k)} 나누면 x = {x}",
        ],
        sol2_fig=steps([
            {"text": "{F} + x = {k}({S} + x)", "hint": "x년 후: {P} {F} + x, {C} {S} + x"},
            {"text": "{F} + x = {k*S} + {co(k)}x", "hint": "괄호 풀기 — x에도 {k}를 곱한다", "marks": [{"on": "{k*S}", "note": "{k}×{S}"}]},
            {"text": "{co(1-k)}x = {k*S - F}", "hint": "이항 — 넘기면 부호가 바뀐다"},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{k*S - F}÷({1-k})"}]},
        ]),
        sol2_anim=[[], [], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="{x}년 후 {P}는 {F} + {x} = {A}세, {C}는 {S} + {x} = {B}세이고 {A} = {k} × {B}이므로 {P}의 나이가 {C}의 나이의 {k}배가 맞다. 답은 {x}년 후다.",
        sol3_fig=table(["", "현재", "{x}년 후"], [["{P}", "{F}세", "{A}세"], ["{C}", "{S}세", "{B}세"]], caption="{A} = {k} × {B}"),
        model_answer="구하는 때를 x년 후라 하면 x년 후 {P}의 나이는 ({F} + x)세, {C}의 나이는 ({S} + x)세이다. {P}의 나이가 {C}의 나이의 {k}배이므로 {F} + x = {k}({S} + x)이고, 괄호를 풀어 정리하면 {co(1-k)}x = {k*S - F}에서 x = {x}이다. 실제로 {x}년 후 두 사람의 나이는 {A}세, {B}세로 {k}배가 되므로 답은 {x}년 후다.",
        rubric=[dict(r, criterion=r["criterion"].replace("{when}", "x년 후").replace("{eq}{ro_eq}", "{F} + x = {k}({S} + x)로").replace("{sol}{eul_sol}", "x = {x}를").replace("{ans}{ro_ans}", "{x}년 후로")) for r in AGE_RUBRIC],
        rubric_total=8,
    )


def age_t2():
    # 현재: 합 T, F = k·S + d  ⇐  S, k, d 로 생성
    return tpl("m1-1-age", 2,
        title="나이의 합과 배수 관계로 현재 나이 구하기",
        skill="한 사람의 나이를 x로 놓고 다른 사람의 나이를 x의 식으로 나타내 합 조건으로 방정식 세우기",
        variant_axis={"구하는 것": "현재 나이", "시점": "현재", "맥락": "가족 나이"},
        discriminates="'k배보다 d세 많다'를 kx + d로 옮기고 합 조건을 쓰는가",
        qtype="short", difficulty=2, pool_target=300, tags=["나이", "일차방정식의 활용"],
        params=[AGE_CPARAM, {"name": "k", "values": {"in": [3, 4]}}, {"name": "S", "values": {"int": [7, 16]}}, {"name": "d", "values": {"int": [1, 9]}}],
        table=AGE_TABLE,
        derive={"F": "k*S + d", "T": "k*S + d + S", "D": "k*S + d - S"},
        constraints=["D >= 24", "D <= 45", "S != d", "S != k", "S != T"],
        cost_values=["T", "k", "d", "S", "F"],
        relation="X + (k*X + d) - T", unknown="X", answer_var="S",
        verify=["ans + k*ans + d == T", "k*ans + d - ans >= 24"],
        question="현재 {P}와 {C}의 나이의 합은 {T}세이고, {P}의 나이는 {C}의 나이의 {k}배보다 {d}세 많다. {C}의 현재 나이를 구하시오.",
        answer="{S}", answer_alt=["{S}세", "{S}살"],
        sol1="모르는 것은 두 사람의 나이 두 개지만, 둘 사이의 관계('{k}배보다 {d}세 많다')가 주어져 있으므로 미지수는 하나면 된다. {C}의 나이를 x세로 놓으면 {P}의 나이는 ({k}x + {d})세이고, 두 나이의 합이 {T}세라는 조건에서 방정식이 나온다.",
        sol1_fig=table(["", "나이"], [["{C}", "x세"], ["{P}", "({k}x + {d})세"], ["합", "{T}세"]]),
        sol2=[
            "{C}의 현재 나이를 x세라 하자.",
            "{P}의 나이는 {C}의 나이의 {k}배보다 {d}세 많으므로 ({k}x + {d})세이다.",
            "두 사람의 나이의 합이 {T}세이므로 x + ({k}x + {d}) = {T}",
            "동류항을 모으면 {k+1}x + {d} = {T}",
            "{d}{eul(d)} 이항하면 {k+1}x = {T - d}",
            "양변을 {k+1}{ro(k+1)} 나누면 x = {S}",
        ],
        sol2_fig=steps([
            {"text": "x + ({k}x + {d}) = {T}", "hint": "{C} x세, {P} {k}x + {d}세 — 합이 {T}"},
            {"text": "{k+1}x + {d} = {T}", "hint": "동류항 정리", "marks": [{"on": "{k+1}x", "note": "x + {k}x"}]},
            {"text": "{k+1}x = {T - d}", "hint": "{d}{eul(d)} 이항"},
            {"text": "x = {S}", "marks": [{"on": "{S}", "note": "{T - d}÷{k+1}"}]},
        ]),
        sol2_anim=[[], [], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="{C}가 {S}세이면 {P}는 {k} × {S} + {d} = {F}세이고, 두 나이의 합은 {S} + {F} = {T}세로 조건과 같다. 답은 {S}세다.",
        sol3_fig=table(["", "나이"], [["{C}", "{S}세"], ["{P}", "{F}세"], ["합", "{T}세"]]),
        model_answer="{C}의 현재 나이를 x세라 하면 {P}의 나이는 ({k}x + {d})세이다. 두 사람의 나이의 합이 {T}세이므로 x + ({k}x + {d}) = {T}, 곧 {k+1}x = {T - d}에서 x = {S}이다. 이때 {P}의 나이는 {F}세이고 합이 {T}세이므로 조건에 맞는다. 따라서 {C}의 현재 나이는 {S}세다.",
        rubric=[dict(r, criterion=r["criterion"].replace("{when} ", "").replace("{eq}{ro_eq}", "x + ({k}x + {d}) = {T}로").replace("{sol}{eul_sol}", "x = {S}를").replace("{ans}{ro_ans}", "{S}세로")) for r in AGE_RUBRIC],
        rubric_total=8,
    )


def age_t3():
    # x년 전 F − x = k(S − x)  ⇐  S0(그때 아이 나이), x, k 로 생성
    return tpl("m1-1-age", 3,
        title="몇 년 전에 나이가 k배였는가",
        skill="x년 전 두 사람의 나이를 (현재 나이 − x)로 놓고 배수 관계로 방정식 세우기",
        variant_axis={"구하는 것": "몇 년 전", "시점": "과거", "맥락": "가족 나이"},
        discriminates="'x년 전'을 두 사람 모두에게 −x로 반영하는가",
        qtype="short", difficulty=3, pool_target=300, tags=["나이", "일차방정식의 활용"],
        # (k, 그때 아이 나이 S0) 쌍을 ks = k·100 + S0 로 넘긴다 — 나이 차 (k−1)·S0 가 24~45 인 것만
        params=[AGE_CPARAM, {"name": "ks", "values": {"in": [312, 313, 314, 315, 408, 409, 410, 411, 412, 413, 414, 415, 506, 507, 508, 509, 510, 511, 605, 606, 607, 608, 609, 704, 705, 706, 707]}}, {"name": "x", "values": {"int": [2, 11]}}],
        table=AGE_TABLE,
        derive={"k": "floor(ks/100)", "S0": "ks % 100", "S": "ks % 100 + x", "F": "floor(ks/100)*(ks % 100) + x", "D": "(floor(ks/100) - 1)*(ks % 100)", "A": "floor(ks/100)*(ks % 100)"},
        constraints=["D >= 24", "D <= 45", "F <= 62", "x != S", "x != k", "x != F", "S >= 8"],
        cost_values=["F", "S", "k", "x", "A", "S0"],
        relation="F - X - k*(S - X)", unknown="X", answer_var="x",
        verify=["F - ans == k*(S - ans)", "ans > 0", "ans < S"],
        question="현재 {P}의 나이는 {F}세, {C}의 나이는 {S}세이다. {P}의 나이가 {C}의 나이의 {k}배였던 것은 몇 년 전인지 구하시오.",
        answer="{x}", answer_alt=["{x}년 전", "{x}년"],
        sol1="'몇 년 전'을 x년 전이라 하면 그때는 두 사람 모두 지금보다 x살씩 적었다. x년 전 {P}는 ({F} − x)세, {C}는 ({S} − x)세이고, 그때 {P}의 나이가 {C}의 나이의 {k}배였으므로 {F} − x = {k}({S} − x)이다. '후'면 더하고 '전'이면 빼는 것만 다를 뿐, 두 사람에게 똑같이 적용한다는 점은 같다.",
        sol1_fig=table(["", "x년 전", "현재"], [["{P}", "({F} − x)세", "{F}세"], ["{C}", "({S} − x)세", "{S}세"]]),
        sol2=[
            "{P}의 나이가 {C}의 나이의 {k}배였던 때를 x년 전이라 하자.",
            "x년 전 {P}의 나이는 ({F} − x)세, {C}의 나이는 ({S} − x)세이다.",
            "그때 {P}의 나이가 {C}의 나이의 {k}배였으므로 {F} − x = {k}({S} − x)",
            "괄호를 풀면 {F} − x = {k*S} − {k}x",
            "x를 좌변으로, 상수를 우변으로 이항하면 {k}x − x = {k*S} − {F}, 곧 {k-1}x = {k*S - F}",
            "양변을 {k-1}{ro(k-1)} 나누면 x = {x}",
        ],
        sol2_fig=steps([
            {"text": "{F} − x = {k}({S} − x)", "hint": "x년 전: {P} {F} − x, {C} {S} − x"},
            {"text": "{F} − x = {k*S} − {k}x", "hint": "괄호 풀기 — (−x)에도 {k}를 곱한다", "marks": [{"on": "{k*S}", "note": "{k}×{S}"}]},
            {"text": "{k-1}x = {k*S - F}", "hint": "이항 — 넘기면 부호가 바뀐다"},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{k*S - F}÷{k-1}"}]},
        ]),
        sol2_anim=[[], [], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="{x}년 전 {P}는 {F} − {x} = {A}세, {C}는 {S} − {x} = {S0}세이고 {A} = {k} × {S0}이므로 {k}배가 맞다. 답은 {x}년 전이다.",
        sol3_fig=table(["", "{x}년 전", "현재"], [["{P}", "{A}세", "{F}세"], ["{C}", "{S0}세", "{S}세"]], caption="{A} = {k} × {S0}"),
        model_answer="구하는 때를 x년 전이라 하면 x년 전 {P}의 나이는 ({F} − x)세, {C}의 나이는 ({S} − x)세이다. {P}의 나이가 {C}의 나이의 {k}배였으므로 {F} − x = {k}({S} − x)이고, 괄호를 풀어 정리하면 {k-1}x = {k*S - F}에서 x = {x}이다. 실제로 {x}년 전 두 사람의 나이는 {A}세, {S0}세로 {k}배이므로 답은 {x}년 전이다.",
        rubric=[dict(r, criterion=r["criterion"].replace("{when}", "x년 전").replace("{eq}{ro_eq}", "{F} − x = {k}({S} − x)로").replace("{sol}{eul_sol}", "x = {x}를").replace("{ans}{ro_ans}", "{x}년 전으로")) for r in AGE_RUBRIC],
        rubric_total=8,
    )


AGE_SEED = {
    "seed_id": "m1-1-age", "category": "활용",
    "title": "나이 — 몇 년 후·몇 년 전·현재 나이 (일차방정식의 활용)",
    "unit_id": "m1-1", "concept_ids": ["m1-1-27"],
    "schema_id": SCHEMA_AGE, "schema_name": "나이 차이와 배수 관계",
    "source_item_ids": [],
    "note": "관계식 (현재 ± x) 의 배수 조건만 차용. 정수해가 나오도록 아이의 나이·x·배수 k 로 어른의 나이를 생성한다. 그림은 현재/x년 후 표 하나.",
    "geometry": False,
    "templates": [age_t1(), age_t2(), age_t3()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 연속하는 수
CONSEC_BASE = dict(context="무맥락", tags=["연속하는 수", "일차방정식의 활용"], traps=["구하는대상혼동", "조건누락"])


def consec_t1():
    return tpl("m1-1-consecutive", 1, **CONSEC_BASE,
        title="연속하는 세 자연수의 합 → 가장 큰 수",
        skill="가운데 수를 x로 놓고 세 수를 x − 1, x, x + 1로 나타내기",
        variant_axis={"수의 종류": "자연수", "구하는 것": "가장 큰 수 / 가장 작은 수", "조건": "합"},
        discriminates="연속하는 세 수를 한 미지수로 나타내고, 구하는 것이 x가 아니라 x ± 1임을 챙기는가",
        qtype="short", difficulty=1, pool_target=300,
        params=[{"name": "q", "values": {"in": ["big", "small"]}}, {"name": "m", "values": {"int": [5, 66]}}],
        table={"key": "q", "rows": {"big": {"Q": "가장 큰 수", "E": "x + 1", "o": 1}, "small": {"Q": "가장 작은 수", "E": "x − 1", "o": -1}}},
        derive={"S": "3*m", "L": "m + 1", "a": "m - 1", "ans_v": "m + o"},
        constraints=["S != ans_v"],
        cost_values=["S", "m", "ans_v"],
        relation="(X - o - 1) + (X - o) + (X - o + 1) - S", unknown="X", answer_var="ans_v",
        verify=["3*(ans - o) == S"],
        question="연속하는 세 자연수의 합이 {S}일 때, 세 수 중 {Q}{eul(Q)} 구하시오.",
        answer="{ans_v}", answer_alt=[],
        sol1="연속하는 세 자연수는 1씩 커진다. 가운데 수를 x로 놓으면 세 수는 x − 1, x, x + 1이 되고, 더하면 −1과 +1이 사라져 3x만 남는다 — 가운데를 x로 잡는 이유가 이것이다. 수직선에 세 점을 찍어 두면 '1씩 차이'가 눈에 보인다.",
        sol1_fig=numline("{m - 3}", "{m + 3}", [{"x": "{a}", "label": "x − 1"}, {"x": "{m}", "label": "x"}, {"x": "{L}", "label": "x + 1"}]),
        sol1_anim=[[hl("pt:x", "lbl:x", keep=True)], [hl("pt:x − 1", "lbl:x − 1", "pt:x + 1", "lbl:x + 1")]],
        sol2=[
            "연속하는 세 자연수 중 가운데 수를 x라 하면 세 수는 x − 1, x, x + 1이다.",
            "세 수의 합이 {S}이므로 (x − 1) + x + (x + 1) = {S}",
            "괄호를 풀고 동류항을 모으면 3x = {S}",
            "양변을 3으로 나누면 x = {m}",
            "구하는 것은 {Q}이므로 {E} = {ans_v}",
        ],
        sol2_fig=steps([
            {"text": "(x − 1) + x + (x + 1) = {S}", "hint": "가운데 수를 x로"},
            {"text": "3x = {S}", "hint": "−1과 +1이 사라진다"},
            {"text": "x = {m}", "marks": [{"on": "{m}", "note": "{S}÷3"}]},
            {"text": "{E} = {ans_v}", "hint": "묻는 것은 {Q}"},
        ]),
        sol2_anim=[[], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")], [reveal(3), hl("hint:3")]],
        sol3="세 수는 {a}, {m}, {L}이고 더하면 {a} + {m} + {L} = {S}로 조건과 같다. {Q}{eun(Q)} {ans_v}이다.",
        sol3_fig=numline("{m - 3}", "{m + 3}", [{"x": "{a}", "label": "{a}"}, {"x": "{m}", "label": "{m}"}, {"x": "{L}", "label": "{L}"}]),
        sol3_anim=[[hl("pt:{ans_v}", "lbl:{ans_v}", keep=True)]],
        model_answer="연속하는 세 자연수 중 가운데 수를 x라 하면 세 수는 x − 1, x, x + 1이다. 합이 {S}이므로 (x − 1) + x + (x + 1) = {S}, 곧 3x = {S}에서 x = {m}이다. 따라서 세 수는 {a}, {m}, {L}이고 {Q}{eun(Q)} {ans_v}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "연속하는 세 자연수를 한 문자로 나타내고(x − 1, x, x + 1 또는 x, x + 1, x + 2) 합이 {S}인 등식을 세웠다.", "partial": "세 수를 문자로 나타냈으나 등식이 틀렸으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "동류항을 정리해 x = {m}(또는 놓은 방식에 맞는 값)을 바르게 구했다.", "partial": "동류항 정리까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "구한 x로부터 {Q} {ans_v}{eul(ans_v)} 답으로 썼다.", "partial": "x의 값만 쓰고 {Q}{ro(Q)} 옮기지 않았으면 인정하지 않고, 세 수를 모두 쓰고 {Q}{eul(Q)} 표시하지 않았으면 1점."},
        ],
        rubric_total=8,
    )


def consec_t2():
    # 연속하는 세 홀수: 가운데 m = 2j+1
    return tpl("m1-1-consecutive", 2, **CONSEC_BASE,
        title="연속하는 세 홀수·짝수의 합 → 가장 큰 수·가장 작은 수",
        skill="연속하는 홀수(짝수)는 2씩 커진다 — 가운데 수를 x로 놓고 x − 2, x, x + 2로 나타내기",
        variant_axis={"수의 종류": "홀수 / 짝수", "구하는 것": "가장 큰 수 / 가장 작은 수", "조건": "합"},
        discriminates="연속하는 홀수·짝수의 간격이 1이 아니라 2임을 아는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "q", "values": {"in": ["odd-big", "odd-small", "even-big", "even-small"]}}, {"name": "j", "values": {"int": [3, 60]}}],
        table={"key": "q", "rows": {
            "odd-big": {"K": "홀수", "p": 1, "Q": "가장 큰 수", "E": "x + 2", "o": 2, "EX": "7, 9, 11"},
            "odd-small": {"K": "홀수", "p": 1, "Q": "가장 작은 수", "E": "x − 2", "o": -2, "EX": "7, 9, 11"},
            "even-big": {"K": "짝수", "p": 0, "Q": "가장 큰 수", "E": "x + 2", "o": 2, "EX": "8, 10, 12"},
            "even-small": {"K": "짝수", "p": 0, "Q": "가장 작은 수", "E": "x − 2", "o": -2, "EX": "8, 10, 12"},
        }},
        derive={"m": "2*j + p", "S": "6*j + 3*p", "a": "2*j + p - 2", "L": "2*j + p + 2", "ans_v": "2*j + p + o"},
        constraints=["S != ans_v"],
        cost_values=["S", "m", "ans_v"],
        relation="(X - o - 2) + (X - o) + (X - o + 2) - S", unknown="X", answer_var="ans_v",
        verify=["3*(ans - o) == S", "ans % 2 == p"],
        question="연속하는 세 {K}의 합이 {S}일 때, 세 수 중 {Q}{eul(Q)} 구하시오.",
        answer="{ans_v}", answer_alt=[],
        sol1="연속하는 {K}는 1이 아니라 2씩 커진다(예: {EX}). 가운데 수를 x로 놓으면 세 수는 x − 2, x, x + 2이고, 더하면 −2와 +2가 사라져 3x가 된다. 수직선에 찍어 보면 점 사이의 간격이 2칸임이 보인다.",
        sol1_fig=numline("{m - 4}", "{m + 4}", [{"x": "{a}", "label": "x − 2"}, {"x": "{m}", "label": "x"}, {"x": "{L}", "label": "x + 2"}]),
        sol1_anim=[[hl("pt:x", "lbl:x", keep=True)], [hl("pt:x − 2", "lbl:x − 2", "pt:x + 2", "lbl:x + 2")]],
        sol2=[
            "연속하는 세 {K} 중 가운데 수를 x라 하면 세 수는 x − 2, x, x + 2이다.",
            "세 수의 합이 {S}이므로 (x − 2) + x + (x + 2) = {S}",
            "괄호를 풀고 동류항을 모으면 3x = {S}",
            "양변을 3으로 나누면 x = {m}",
            "구하는 것은 {Q}이므로 {E} = {ans_v}",
        ],
        sol2_fig=steps([
            {"text": "(x − 2) + x + (x + 2) = {S}", "hint": "{K}는 2씩 — 가운데 수를 x로"},
            {"text": "3x = {S}", "hint": "−2와 +2가 사라진다"},
            {"text": "x = {m}", "marks": [{"on": "{m}", "note": "{S}÷3"}]},
            {"text": "{E} = {ans_v}", "hint": "묻는 것은 {Q}"},
        ]),
        sol2_anim=[[], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")], [reveal(3), hl("hint:3")]],
        sol3="세 수는 {a}, {m}, {L}로 모두 {K}이고 더하면 {a} + {m} + {L} = {S}로 조건과 같다. {Q}{eun(Q)} {ans_v}이다.",
        sol3_fig=numline("{m - 4}", "{m + 4}", [{"x": "{a}", "label": "{a}"}, {"x": "{m}", "label": "{m}"}, {"x": "{L}", "label": "{L}"}]),
        sol3_anim=[[hl("pt:{ans_v}", "lbl:{ans_v}", keep=True)]],
        model_answer="연속하는 세 {K} 중 가운데 수를 x라 하면 세 수는 x − 2, x, x + 2이다. 합이 {S}이므로 (x − 2) + x + (x + 2) = {S}, 곧 3x = {S}에서 x = {m}이다. 따라서 세 {K}는 {a}, {m}, {L}이고 {Q}{eun(Q)} {ans_v}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "연속하는 세 {K}를 2씩 차이 나는 꼴(x − 2, x, x + 2 또는 x, x + 2, x + 4)로 나타내고 합이 {S}인 등식을 세웠다.", "partial": "간격을 1로 잘못 놓았으나 합의 등식 구조는 옳으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "동류항을 정리해 x = {m}(또는 놓은 방식에 맞는 값)을 바르게 구했다.", "partial": "동류항 정리까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "구한 x로부터 {Q} {ans_v}{eul(ans_v)} 답으로 썼다.", "partial": "세 수를 모두 구하고 {Q}{eul(Q)} 표시하지 않았으면 1점."},
        ],
        rubric_total=8,
    )


def consec_t3():
    # 가장 큰 수의 k배 = 나머지 두 수의 합 + d  (k=3,4) ⇐ x, k 로 d 생성
    return tpl("m1-1-consecutive", 3, **CONSEC_BASE,
        title="연속하는 세 자연수의 배수·합 관계 → 세 수의 합",
        skill="가장 작은 수를 x로 놓고 x, x + 1, x + 2로 나타내 관계 조건을 식으로 옮기기",
        variant_axis={"수의 종류": "자연수", "구하는 것": "세 수의 합 / 가장 큰 수", "조건": "배수와 합의 관계"},
        discriminates="'A는 B보다 d만큼 크다'를 A = B + d로 옮기고, 구하는 것이 x가 아니라 세 수의 합(가장 큰 수)임을 챙기는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "q", "values": {"in": ["sum", "big"]}}, {"name": "k", "values": {"in": [4, 5]}}, {"name": "x", "values": {"int": [3, 40]}}],
        table={"key": "q", "rows": {
            "sum": {"Q": "세 자연수의 합", "QL": "세 수의 합은 x + (x + 1) + (x + 2) = 3x + 3", "QS": "3x + 3", "QN": "세 수의 합", "oo": 3, "om": 3},
            "big": {"Q": "가장 큰 수", "QL": "가장 큰 수는 x + 2", "QS": "x + 2", "QN": "가장 큰 수", "oo": 2, "om": 1},
        }},
        derive={"d": "(k - 2)*x + 2*k - 1", "S": "3*x + 3", "b": "x + 1", "c": "x + 2", "ans_v": "om*x + oo"},
        constraints=["ans_v != d", "d != x", "d != k", "ans_v != k"],
        cost_values=["k", "d", "x", "ans_v", "2*k"],
        relation="k*((X - oo)/om + 2) - ((X - oo)/om + ((X - oo)/om + 1)) - d", unknown="X", answer_var="ans_v",
        verify=["k*(x + 2) == 2*x + 1 + d", "ans == om*x + oo"],
        question="연속하는 세 자연수가 있다. 가장 큰 수의 {k}배는 나머지 두 수의 합보다 {d}만큼 크다고 한다. 이 {Q}{eul(Q)} 구하시오.",
        answer="{ans_v}", answer_alt=[],
        sol1="세 수를 하나의 문자로 나타내는 것이 먼저다. 가장 작은 수를 x로 놓으면 세 수는 x, x + 1, x + 2이다. 조건 '가장 큰 수의 {k}배는 나머지 두 수의 합보다 {d}만큼 크다'는 (가장 큰 수) × {k} = (나머지 두 수의 합) + {d}, 곧 {k}(x + 2) = x + (x + 1) + {d}로 옮겨진다. 큰 쪽에서 {d}를 빼거나 작은 쪽에 {d}를 더해야 등식이 된다는 점에 주의한다.",
        sol1_fig=numline("{x - 2}", "{x + 4}", [{"x": "{x}", "label": "x"}, {"x": "{b}", "label": "x + 1"}, {"x": "{c}", "label": "x + 2"}]),
        sol1_anim=[[hl("pt:x", "lbl:x", keep=True)], [hl("pt:x + 2", "lbl:x + 2")]],
        sol2=[
            "가장 작은 수를 x라 하면 연속하는 세 자연수는 x, x + 1, x + 2이다.",
            "가장 큰 수의 {k}배는 {k}(x + 2), 나머지 두 수의 합은 x + (x + 1) = 2x + 1이다.",
            "'{d}만큼 크다'이므로 {k}(x + 2) = (2x + 1) + {d}",
            "괄호를 풀면 {k}x + {2*k} = 2x + {d + 1}",
            "이항하여 정리하면 {k}x − 2x = {d + 1} − {2*k}, 곧 {k-2}x = {d + 1 - 2*k}",
            "따라서 x = {x}이고, {QL} = {ans_v}",
        ],
        sol2_fig=steps([
            {"text": "{k}(x + 2) = (2x + 1) + {d}", "hint": "큰 쪽 = 작은 쪽 + {d}"},
            {"text": "{k}x + {2*k} = 2x + {d + 1}", "hint": "괄호 풀기", "marks": [{"on": "{2*k}", "note": "{k}×2"}]},
            {"text": "{k-2}x = {d + 1 - 2*k}", "hint": "이항 — 부호가 바뀐다"},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{d + 1 - 2*k}÷{k-2}"}]},
            {"text": "{QS} = {ans_v}", "hint": "묻는 것은 {QN}"},
        ]),
        sol2_anim=[[], [], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0"), reveal(4), hl("hint:4")]],
        sol3="세 수는 {x}, {b}, {c}이다. 가장 큰 수의 {k}배는 {k} × {c} = {k*c}, 나머지 두 수의 합은 {x} + {b} = {2*x + 1}이고 {k*c} − {2*x + 1} = {d}로 조건과 같다. {QN}{eun(QN)} {ans_v}이다.",
        sol3_fig=numline("{x - 2}", "{x + 4}", [{"x": "{x}", "label": "{x}"}, {"x": "{b}", "label": "{b}"}, {"x": "{c}", "label": "{c}"}]),
        sol3_anim=[[hl("pt:{x}", "lbl:{x}", "pt:{b}", "lbl:{b}", "pt:{c}", "lbl:{c}", keep=True)]],
        model_answer="가장 작은 수를 x라 하면 세 자연수는 x, x + 1, x + 2이다. 가장 큰 수의 {k}배가 나머지 두 수의 합보다 {d}만큼 크므로 {k}(x + 2) = x + (x + 1) + {d}이고, 정리하면 {k-2}x = {d + 1 - 2*k}에서 x = {x}이다. 따라서 세 수는 {x}, {b}, {c}이고 {QN}{eun(QN)} {ans_v}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "세 자연수를 x, x + 1, x + 2로 나타내고 {k}(x + 2) = x + (x + 1) + {d}{eul(d)} 세웠다.", "partial": "세 수를 문자로 나타냈으나 '{d}만큼 크다'의 방향이 틀렸으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "괄호를 풀고 이항하여 x = {x}{eul(x)} 바르게 구했다.", "partial": "괄호를 풀어 정리하는 데까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "세 수 {x}, {b}, {c}로부터 {QN} {ans_v}{eul(ans_v)} 답으로 썼다.", "partial": "x의 값만 쓰고 {QN}{ro(QN)} 옮기지 않았으면 인정하지 않고, 세 수까지 쓰고 {QN}{eul(QN)} 쓰지 않았으면 1점."},
        ],
        rubric_total=8,
    )


CONSEC_SEED = {
    "seed_id": "m1-1-consecutive", "category": "활용",
    "title": "연속하는 수 — 자연수·홀수·배수 관계 (일차방정식의 활용)",
    "unit_id": "m1-1", "concept_ids": ["m1-1-27"],
    "schema_id": SCHEMA_CONSEC, "schema_name": "연속하는 수 문장제",
    "source_item_ids": [],
    "note": "구조(연속 수를 한 문자로 나타내기)만 차용. 합은 3의 배수로, 배수 관계 틀은 d 를 x·k 에서 생성해 정수해를 보장. 그림은 수직선 위 세 점.",
    "geometry": False,
    "templates": [consec_t1(), consec_t2(), consec_t3()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 과부족
SURPLUS_CTX = {
    "1": {"G": "동아리 회원", "I": "기념 스티커", "U": "장", "W": "나누어 주", "V": "동아리 회원들에게 기념 스티커를 나누어 주는데"},
    "2": {"G": "캠핑에 온 친구", "I": "에너지바", "U": "개", "W": "나누어 주", "V": "캠핑에 온 친구들에게 에너지바를 나누어 주는데"},
    "3": {"G": "스터디 모임 회원", "I": "형광펜", "U": "자루", "W": "나누어 주", "V": "스터디 모임 회원들에게 형광펜을 나누어 주는데"},
    "4": {"G": "체험 학습 참가자", "I": "생수", "U": "병", "W": "나누어 주", "V": "체험 학습 참가자들에게 생수를 나누어 주는데"},
}
SURPLUS_TABLE = {"key": "c", "rows": SURPLUS_CTX}
SURPLUS_CPARAM = {"name": "c", "values": {"in": list(SURPLUS_CTX)}}


def surplus_common(no, ask):
    people = ask == "people"
    return tpl("m1-1-surplus", no,
        title="a개씩 주면 남고 c개씩 주면 부족 — " + ("사람 수 구하기" if people else "물건의 개수 구하기"),
        skill="사람 수를 x로 놓고 물건의 개수를 두 가지 방식으로 나타내 같다고 놓기",
        variant_axis={"구하는 것": "사람 수" if people else "물건 수", "과부족 패턴": "남음·부족", "맥락": "나눠 주기"},
        discriminates="'남는다'는 +, '부족하다'는 −로 물건의 총개수를 두 번 나타내는가" + ("" if people else " · 구하는 것이 사람 수가 아니라 물건 수임을 챙기는가"),
        qtype="short", difficulty=2 if people else 3, pool_target=300, tags=["과부족", "일차방정식의 활용"],
        params=[SURPLUS_CPARAM, {"name": "a", "values": {"int": [3, 6]}}, {"name": "g", "values": {"in": [1, 2]}}, {"name": "x", "values": {"int": [5, 16]}}, {"name": "b", "values": {"int": [1, 9]}}],
        table=SURPLUS_TABLE,
        derive={"cc": "a + g", "d": "g*x - b", "N": "a*x + b", "M": "(a + g)*x"},
        constraints=["d >= 1", "d <= 25", "d != b", "x != b", "x != d", "x != a", "x != cc", "N != x", "N != cc"],
        cost_values=["a", "b", "cc", "d", "x", "N"],
        relation="a*X + b - (cc*X - d)" if people else None,
        unknown="X", answer_var="x" if people else "N",
        verify=["a*x + b == N", "cc*x - d == N", "ans == x" if people else "ans == N"],
        question="{V} 한 사람에게 {a}{U}씩 주면 {b}{U}{ika(U)} 남고, {cc}{U}씩 주면 {d}{U}{ika(U)} 부족하다. " + ("{G}는 모두 몇 명인지 구하시오." if people else "{I}는 모두 몇 {U}인지 구하시오."),
        answer="{x}" if people else "{N}", answer_alt=["{x}명"] if people else ["{N}{U}"],
        sol1="{I}의 개수는 변하지 않는다는 것이 핵심이다. {G}의 수를 x명으로 놓으면, {a}{U}씩 주고 {b}{U}{ika(U)} 남았으니 전체는 ({a}x + {b}){U}이고, {cc}{U}씩 주려면 {d}{U}{ika(U)} 부족하니 전체는 ({cc}x − {d}){U}이다. 같은 {I}를 두 가지로 나타냈으므로 두 식은 같다. 막대 두 줄로 그리면 '남음은 더하고 부족은 뺀다'가 보인다.",
        sol1_fig=bar([
            {"name": "{a}{U}씩", "total": "전체 = {a}x + {b}", "parts": [{"label": "{a} × x", "value": "{a*x}"}, {"label": "{b} 남음", "value": "{b}", "fill": True}]},
            {"name": "{cc}{U}씩", "total": "전체 = {cc}x − {d}", "parts": [{"label": "{cc} × x", "value": "{cc*x}", "fill": True}, {"label": "{d} 부족", "value": "{d}"}]},
        ]),
        sol1_anim=[[hl("row:0", "part:0-0", "part-lbl:0-0")], [hl("part:0-1", "part-lbl:0-1", keep=True)], [hl("row:1", "part:1-0", "part-lbl:1-0")], [hl("part:1-1", "part-lbl:1-1", keep=True)]],
        sol2=[
            "{G}의 수를 x명이라 하자.",
            "{a}{U}씩 주면 {b}{U}{ika(U)} 남으므로 {I}의 개수는 ({a}x + {b}){U}",
            "{cc}{U}씩 주면 {d}{U}{ika(U)} 부족하므로 {I}의 개수는 ({cc}x − {d}){U}",
            "{I}의 개수는 같으므로 {a}x + {b} = {cc}x − {d}",
            "이항하여 정리하면 {a}x − {cc}x = −{d} − {b}, 곧 {co(-g)}x = {-(d + b)}",
            "양변을 {-g}{ro(-g)} 나누면 x = {x}",
        ] + ([] if people else ["{I}의 개수는 {a}x + {b} = {a} × {x} + {b} = {N}"]),
        sol2_fig=steps([
            {"text": "{a}x + {b} = {cc}x − {d}", "hint": "남음 +{b} · 부족 −{d}"},
            {"text": "{co(-g)}x = {-(d + b)}", "hint": "이항 — 넘기면 부호가 바뀐다", "marks": [{"on": "{co(-g)}x", "note": "{a}x − {cc}x"}]},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{-(d + b)}÷({-g})"}]},
        ] + ([] if people else [{"text": "{a} × {x} + {b} = {N}", "hint": "묻는 것은 {I}의 개수"}])),
        sol2_anim=[[], [], [], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("mark:2-0")]] + ([] if people else [[reveal(3), hl("hint:3")]]),
        sol3="{G}가 {x}명이면 {I}는 {a} × {x} + {b} = {N}{U}이다. {cc}{U}씩 주려면 {cc} × {x} = {M}{U}가 필요하므로 {M} − {N} = {d}{U}{ika(U)} 부족하다 — 조건과 같다. 답은 " + ("{x}명이다." if people else "{N}{U}이다."),
        sol3_fig=bar([
            {"name": "{a}{U}씩", "total": "{a} × {x} + {b} = {N}", "parts": [{"label": "{a*x}", "value": "{a*x}"}, {"label": "{b}", "value": "{b}", "fill": True}]},
            {"name": "{cc}{U}씩", "total": "{cc} × {x} = {M} = {N} + {d}", "parts": [{"label": "{N}", "value": "{N}", "fill": True}, {"label": "{d}", "value": "{d}"}]},
        ]),
        sol3_anim=[[hl("total:0", "part:0-0", "part:0-1")], [hl("total:1", "part:1-1", "part-lbl:1-1", keep=True)]],
        model_answer="{G}의 수를 x명이라 하면 {a}{U}씩 주고 {b}{U}{ika(U)} 남으므로 {I}는 ({a}x + {b}){U}, {cc}{U}씩 주면 {d}{U}{ika(U)} 부족하므로 {I}는 ({cc}x − {d}){U}이다. {I}의 개수는 같으므로 {a}x + {b} = {cc}x − {d}이고, 정리하면 {co(-g)}x = {-(d + b)}에서 x = {x}이다. " + ("따라서 {G}는 {x}명이다." if people else "따라서 {I}는 {a} × {x} + {b} = {N}{U}이다."),
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "{G}의 수를 x로 놓고 {I}의 개수를 {a}x + {b}, {cc}x − {d}로 두 번 나타내 {a}x + {b} = {cc}x − {d}{eul(d)} 세웠다.", "partial": "한쪽만 옳게 나타냈으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "이항하여 정리하고 x = {x}{eul(x)} 바르게 구했다.", "partial": "이항까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": ("답을 {x}명으로 썼다." if people else "x = {x}{eul(x)} {a}x + {b}에 넣어 {I}의 개수 {N}{U}{eul(U)} 답으로 썼다."), "partial": ("확인 없이 답만 옳게 썼으면 1점." if people else "사람 수 {x}만 쓰고 {I}의 개수로 옮기지 않았으면 인정하지 않는다.")},
        ],
        rubric_total=8,
    )


def surplus_t3():
    # 텐트·스터디룸 배정: a명씩 → b명 남음, c명씩 → 방 d개 남음 ⇒ a r + b = c (r − d)
    return tpl("m1-1-surplus", 3,
        title="a명씩 들어가면 남고 c명씩 들어가면 방이 남음 — 방의 수 구하기",
        skill="방의 수를 x로 놓고 사람 수를 두 가지 방식으로 나타내기 — '방이 남는다'는 (x − d)개 방을 c명씩 채운 것",
        variant_axis={"구하는 것": "방(텐트)의 수", "과부족 패턴": "사람 남음·방 남음", "맥락": "배정"},
        discriminates="'방 d개가 남는다'를 사람 수 c(x − d)로 옮기는가",
        qtype="short", difficulty=3, pool_target=300, tags=["과부족", "일차방정식의 활용"],
        params=[{"name": "c", "values": {"in": ["1", "2", "3"]}}, {"name": "a", "values": {"int": [3, 6]}}, {"name": "g", "values": {"in": [1, 2]}}, {"name": "d", "values": {"in": [1, 2, 3]}}, {"name": "s", "values": {"int": [1, 9]}}],
        table={"key": "c", "rows": {
            "1": {"R": "텐트", "V": "캠핑장에서 텐트에 사람을 배정하는데", "Rj": "텐트가"},
            "2": {"R": "스터디룸", "V": "스터디 카페에서 스터디룸에 학생을 배정하는데", "Rj": "스터디룸이"},
            "3": {"R": "승합차", "V": "수련회에 가려고 승합차에 학생을 태우는데", "Rj": "승합차가"},
        }},
        derive={"cc": "a + g", "b": "s", "r": "(s + (a + g)*d)/g", "N": "a*(s + (a + g)*d)/g + s", "K": "(s + (a + g)*d)/g - d"},
        constraints=["(s + cc*d) % g == 0", "r <= 30", "r != b", "r != a", "r != cc", "r != d", "N != r", "b != d"],
        cost_values=["a", "b", "cc", "d", "r", "N"],
        relation="a*X + b - cc*(X - d)", unknown="X", answer_var="r",
        verify=["a*r + b == N", "cc*(r - d) == N", "ans == r"],
        question="{V} 한 {R}에 {a}명씩 들어가면 {b}명이 남고, {cc}명씩 들어가면 {R} {d}개가 남는다. {R}는 모두 몇 개인지 구하시오.",
        answer="{r}", answer_alt=["{r}개"],
        sol1="사람 수는 변하지 않는다. {R}의 수를 x개로 놓으면, {a}명씩 들어가고 {b}명이 남았으니 사람은 ({a}x + {b})명이다. {cc}명씩 들어가면 {R} {d}개가 남는다는 것은 (x − {d})개의 {R}에 {cc}명씩 꽉 찼다는 뜻이므로 사람은 {cc}(x − {d})명이다. 두 식이 같다고 놓는다.",
        sol1_fig=bar([
            {"name": "{a}명씩", "total": "사람 = {a}x + {b}", "parts": [{"label": "{a} × x", "value": "{a*r}"}, {"label": "{b}명 남음", "value": "{b}", "fill": True}]},
            {"name": "{cc}명씩", "total": "사람 = {cc}(x − {d})", "parts": [{"label": "{cc} × (x − {d})", "value": "{N}", "fill": True}, {"label": "빈 {R} {d}개", "value": "{cc*d}"}]},
        ]),
        sol1_anim=[[hl("row:0", "part:0-0", "part-lbl:0-0")], [hl("part:0-1", "part-lbl:0-1", keep=True)], [hl("row:1", "part:1-0", "part-lbl:1-0")], [hl("part:1-1", "part-lbl:1-1", keep=True)]],
        sol2=[
            "{R}의 수를 x개라 하자.",
            "{a}명씩 들어가면 {b}명이 남으므로 사람 수는 ({a}x + {b})명",
            "{cc}명씩 들어가면 {R} {d}개가 남으므로 사람이 들어간 {R}는 (x − {d})개이고, 사람 수는 {cc}(x − {d})명",
            "사람 수는 같으므로 {a}x + {b} = {cc}(x − {d})",
            "괄호를 풀면 {a}x + {b} = {cc}x − {cc*d}",
            "이항하여 정리하면 {a}x − {cc}x = −{cc*d} − {b}, 곧 {co(-g)}x = {-(cc*d + b)}",
            "양변을 {-g}{ro(-g)} 나누면 x = {r}",
        ],
        sol2_fig=steps([
            {"text": "{a}x + {b} = {cc}(x − {d})", "hint": "{R} {d}개가 남는다 → 채운 {R}는 x − {d}개"},
            {"text": "{a}x + {b} = {cc}x − {cc*d}", "hint": "괄호 풀기 — {d}에도 {cc}를 곱한다", "marks": [{"on": "{cc*d}", "note": "{cc}×{d}={cc*d}"}]},
            {"text": "{co(-g)}x = {-(cc*d + b)}", "hint": "이항 — 부호가 바뀐다"},
            {"text": "x = {r}", "marks": [{"on": "{r}", "note": "{-(cc*d + b)}÷({-g})"}]},
        ]),
        sol2_anim=[[], [], [], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="{R}가 {r}개이면 사람은 {a} × {r} + {b} = {N}명이다. {cc}명씩 들어가면 {N} ÷ {cc} = {K}개의 {R}가 꽉 차고 {r} − {K} = {d}개가 남으므로 조건과 같다. 답은 {r}개다.",
        sol3_fig=bar([
            {"name": "{a}명씩", "total": "{a} × {r} + {b} = {N}명", "parts": [{"label": "{a*r}", "value": "{a*r}"}, {"label": "{b}", "value": "{b}", "fill": True}]},
            {"name": "{cc}명씩", "total": "{cc} × {K} = {N}명 · 빈 {R} {d}개", "parts": [{"label": "{N}", "value": "{N}", "fill": True}, {"label": "{d}개 빔", "value": "{cc*d}"}]},
        ]),
        sol3_anim=[[hl("total:0", "part:0-0", "part:0-1")], [hl("total:1", "part:1-1", "part-lbl:1-1", keep=True)]],
        model_answer="{R}의 수를 x개라 하면 {a}명씩 들어가고 {b}명이 남으므로 사람 수는 ({a}x + {b})명이고, {cc}명씩 들어가면 {R} {d}개가 남으므로 사람 수는 {cc}(x − {d})명이다. 사람 수는 같으므로 {a}x + {b} = {cc}(x − {d}), 곧 {co(-g)}x = {-(cc*d + b)}에서 x = {r}이다. 따라서 {R}는 {r}개다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "{R}의 수를 x로 놓고 사람 수를 {a}x + {b}, {cc}(x − {d})로 두 번 나타내 등식을 세웠다.", "partial": "'{R} {d}개가 남는다'를 (x − {d})로 옮기지 못했으나 나머지는 옳으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "괄호를 풀고 이항하여 x = {r}{eul(r)} 바르게 구했다.", "partial": "괄호를 풀어 정리하는 데까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "답을 {r}개로 쓰고 조건에 맞는지 확인했다.", "partial": "확인 없이 답만 옳게 썼으면 1점."},
        ],
        rubric_total=8,
    )


SURPLUS_SEED = {
    "seed_id": "m1-1-surplus", "category": "활용",
    "title": "과부족 — 남고 부족한 상황에서 사람 수·물건 수·방의 수 (일차방정식의 활용)",
    "unit_id": "m1-1", "concept_ids": ["m1-1-27"],
    "schema_id": SCHEMA_SURPLUS, "schema_name": "과부족 문제(배치와 여유인원)",
    "source_item_ids": [],
    "note": "관계식 ax + b = cx − d, ax + b = c(x − d) 만 차용. 부족한 양 d(또는 남는 사람 b)를 x·간격 g 에서 생성해 정수해를 보장. 맥락은 요즘 상황(동아리 굿즈·캠핑·스터디 카페) 표 변주. 그림은 막대 두 줄.",
    "geometry": False,
    "templates": [surplus_common(1, "people"), surplus_common(2, "items"), surplus_t3()],
}


# ═══════════════════════════════════════════════════════════════════ 4. 두 품목 구매
SHOP_CTX = {
    "1": {"S": "편의점에서", "A": "삼각김밥", "B": "음료수"},
    "2": {"S": "편의점에서", "A": "초코바", "B": "컵라면"},
    "3": {"S": "문구점에서", "A": "볼펜", "B": "노트"},
    "4": {"S": "분식집에서", "A": "떡꼬치", "B": "핫도그"},
    "5": {"S": "카페에서", "A": "쿠키", "B": "머핀"},
}
SHOP_TABLE = {"key": "c", "rows": SHOP_CTX}
SHOP_CPARAM = {"name": "c", "values": {"in": list(SHOP_CTX)}}
PA = {"name": "pa", "values": {"in": [1200, 1500, 1800, 2000]}}
PB = {"name": "pb", "values": {"in": [2500, 3000, 3500]}}


def purchase_t1():
    return tpl("m1-1-purchase", 1,
        title="두 품목을 합하여 n개 — 한 품목의 개수 구하기",
        skill="한 품목의 개수를 x로 놓고 다른 품목을 (n − x)로 나타내 총액으로 방정식 세우기",
        variant_axis={"구하는 것": "한 품목의 개수", "조건": "총 개수·총액", "맥락": "편의점·문구점"},
        discriminates="다른 품목의 개수를 (n − x)로 나타내고 가격 × 개수로 총액을 세우는가",
        qtype="short", difficulty=2, pool_target=300, tags=["물건 구매", "일차방정식의 활용"],
        params=[SHOP_CPARAM, PA, PB, {"name": "x", "values": {"int": [2, 9]}}, {"name": "y", "values": {"int": [2, 9]}}],
        table=SHOP_TABLE,
        derive={"n": "x + y", "T": "pa*x + pb*y", "pbn": "pb*(x + y)", "dp": "pa - pb"},
        constraints=["x != y", "x != n"],
        cost_values=["pa", "pb", "n", "T", "x", "pbn"],
        relation="pa*X + pb*(n - X) - T", unknown="X", answer_var="x",
        verify=["pa*ans + pb*(n - ans) == T", "ans < n"],
        question="{S} 한 개에 {pa}원인 {A}와 한 개에 {pb}원인 {B}를 합하여 {n}개 사고 {T}원을 냈다. {A}는 몇 개 샀는지 구하시오.",
        answer="{x}", answer_alt=["{x}개"],
        sol1="모르는 것은 {A}의 개수와 {B}의 개수 두 가지지만, 합이 {n}개이므로 {A}를 x개 사면 {B}는 ({n} − x)개다. 총액은 (가격) × (개수)를 품목마다 구해 더한 것이므로 {pa}x + {pb}({n} − x) = {T}이다. 막대 하나를 두 칸으로 나누어 각 칸에 가격 × 개수를 적으면 식이 그대로 보인다.",
        sol1_fig=bar([{"name": "총액", "total": "{T}원", "parts": [{"label": "{A} x개", "value": "{pa*x}", "fill": True}, {"label": "{B} ({n} − x)개", "value": "{pb*y}"}]}]),
        sol1_anim=[[hl("part:0-0", "part-lbl:0-0")], [hl("part:0-1", "part-lbl:0-1")], [hl("total:0", keep=True)]],
        sol2=[
            "{A}를 x개 샀다고 하면 {B}는 ({n} − x)개 샀다.",
            "{A}의 값은 {pa}x원, {B}의 값은 {pb}({n} − x)원이다.",
            "총액이 {T}원이므로 {pa}x + {pb}({n} − x) = {T}",
            "괄호를 풀면 {pa}x + {pbn} − {pb}x = {T}",
            "동류항을 정리하면 {co(dp)}x + {pbn} = {T}, 곧 {co(dp)}x = {T - pbn}",
            "양변을 {dp}{ro(dp)} 나누면 x = {x}",
        ],
        sol2_fig=steps([
            {"text": "{pa}x + {pb}({n} − x) = {T}", "hint": "{B}는 {n} − x개"},
            {"text": "{pa}x + {pbn} − {pb}x = {T}", "hint": "괄호 풀기 — x에도 {pb}를 곱한다", "marks": [{"on": "{pbn}", "note": "{pb}×{n}"}]},
            {"text": "{co(dp)}x = {T - pbn}", "hint": "동류항 정리 후 이항"},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{T - pbn}÷({dp})"}]},
        ]),
        sol2_anim=[[], [], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="{A} {x}개는 {pa} × {x} = {pa*x}원, {B} {y}개는 {pb} × {y} = {pb*y}원이고 합은 {pa*x} + {pb*y} = {T}원으로 조건과 같다. 개수도 {x} + {y} = {n}개다. 답은 {x}개다.",
        sol3_fig=bar([{"name": "총액", "total": "{pa*x} + {pb*y} = {T}원", "parts": [{"label": "{A} {x}개", "value": "{pa*x}", "fill": True}, {"label": "{B} {y}개", "value": "{pb*y}"}]}]),
        sol3_anim=[[hl("part:0-0", "part-lbl:0-0", keep=True)], [hl("part:0-1", "part-lbl:0-1")], [hl("total:0")]],
        model_answer="{A}를 x개 샀다고 하면 {B}는 ({n} − x)개이므로 총액에서 {pa}x + {pb}({n} − x) = {T}이다. 괄호를 풀어 정리하면 {co(dp)}x = {T - pbn}에서 x = {x}이다. 실제로 {A} {x}개와 {B} {y}개의 값은 {pa*x} + {pb*y} = {T}원이므로 조건에 맞는다. 따라서 {A}는 {x}개 샀다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "{A}의 개수를 x, {B}의 개수를 {n} − x로 놓고 {pa}x + {pb}({n} − x) = {T}{eul(T)} 세웠다.", "partial": "{B}의 개수를 {n} − x로 나타냈으나 총액 식이 틀렸으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "괄호를 풀고 동류항을 정리해 x = {x}{eul(x)} 바르게 구했다.", "partial": "괄호를 풀어 정리하는 데까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "답을 {A} {x}개로 쓰고 총액이 맞는지 확인했다.", "partial": "확인 없이 답만 옳게 썼으면 1점."},
        ],
        rubric_total=8,
    )


def purchase_t2():
    return tpl("m1-1-purchase", 2,
        title="지불한 돈과 거스름돈 — 다른 품목의 개수 구하기",
        skill="총액 = 낸 돈 − 거스름돈으로 먼저 정리하고, 한 품목을 x로 놓아 방정식 세우기",
        variant_axis={"구하는 것": "다른 품목의 개수", "조건": "총 개수·낸 돈·거스름돈", "맥락": "편의점·문구점"},
        discriminates="거스름돈을 빼서 실제 총액을 구한 뒤 식을 세우는가 · 구한 x가 아니라 묻는 품목의 개수를 답하는가",
        qtype="short", difficulty=3, pool_target=300, tags=["물건 구매", "거스름돈", "일차방정식의 활용"],
        params=[SHOP_CPARAM, PA, PB, {"name": "x", "values": {"int": [2, 9]}}, {"name": "y", "values": {"int": [2, 9]}}],
        table=SHOP_TABLE,
        # 낸 돈 P = 총액을 덮는 가장 작은 만 원 단위(거스름돈 500원 이상 남게) — 3만 원 낸 뒤 거스름돈 5,300원 같은 자연스러운 값
        derive={"n": "x + y", "T": "pa*x + pb*y", "P": "ceiling((pa*x + pb*y + 500)/10000)*10000", "C": "ceiling((pa*x + pb*y + 500)/10000)*10000 - (pa*x + pb*y)", "pbn": "pb*(x + y)", "dp": "pa - pb"},
        constraints=["x != y", "C >= 500", "y != n"],
        cost_values=["pa", "pb", "n", "P", "C", "T", "x", "y"],
        relation="pa*(n - X) + pb*X - T", unknown="X", answer_var="y",
        verify=["pa*(n - ans) + pb*ans == P - C", "ans < n"],
        question="{S} 한 개에 {pa}원인 {A}와 한 개에 {pb}원인 {B}를 합하여 {n}개 사고 {P}원을 냈더니 거스름돈으로 {C}원을 받았다. {B}는 몇 개 샀는지 구하시오.",
        answer="{y}", answer_alt=["{y}개"],
        sol1="먼저 실제로 쓴 돈을 구한다 — 낸 돈 {P}원에서 거스름돈 {C}원을 빼면 총액은 {T}원이다. 그다음은 두 품목 문제와 같다. {A}를 x개 사면 {B}는 ({n} − x)개이고, 가격 × 개수를 더한 것이 {T}원이다. 마지막에 묻는 것이 {B}의 개수라는 점을 잊지 않는다.",
        sol1_fig=bar([{"name": "낸 돈", "total": "{P}원", "parts": [{"label": "{A} x개", "value": "{pa*x}", "fill": True}, {"label": "{B} ({n} − x)개", "value": "{pb*y}"}, {"label": "거스름돈", "value": "{C}"}]}]),
        sol1_anim=[[hl("total:0")], [hl("part:0-2", "part-lbl:0-2", keep=True)], [hl("part:0-0", "part-lbl:0-0")], [hl("part:0-1", "part-lbl:0-1")]],
        sol2=[
            "실제로 쓴 돈은 {P} − {C} = {T}(원)이다.",
            "{A}를 x개 샀다고 하면 {B}는 ({n} − x)개이다.",
            "총액에서 {pa}x + {pb}({n} − x) = {T}",
            "괄호를 풀면 {pa}x + {pbn} − {pb}x = {T}",
            "동류항을 정리하고 이항하면 {co(dp)}x = {T - pbn}",
            "양변을 {dp}{ro(dp)} 나누면 x = {x}",
            "구하는 것은 {B}의 개수이므로 {n} − x = {n} − {x} = {y}",
        ],
        sol2_fig=steps([
            {"text": "{P} − {C} = {T}", "hint": "실제 총액 = 낸 돈 − 거스름돈"},
            {"text": "{pa}x + {pb}({n} − x) = {T}", "hint": "{B}는 {n} − x개"},
            {"text": "{co(dp)}x = {T - pbn}", "hint": "괄호 풀고 정리", "marks": [{"on": "{T - pbn}", "note": "{T} − {pb}×{n}"}]},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{T - pbn}÷({dp})"}]},
            {"text": "{n} − {x} = {y}", "hint": "묻는 것은 {B}의 개수"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [], [reveal(1), hl("hint:1")], [], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3), hl("mark:3-0")], [reveal(4), hl("hint:4")]],
        sol3="{A} {x}개 {pa*x}원, {B} {y}개 {pb*y}원으로 총액은 {T}원이고, {P} − {T} = {C}원이 거스름돈이므로 조건과 같다. 답은 {y}개다.",
        sol3_fig=bar([{"name": "낸 돈", "total": "{P}원", "parts": [{"label": "{A} {x}개", "value": "{pa*x}", "fill": True}, {"label": "{B} {y}개", "value": "{pb*y}"}, {"label": "거스름돈 {C}", "value": "{C}"}]}]),
        sol3_anim=[[hl("part:0-0", "part-lbl:0-0")], [hl("part:0-1", "part-lbl:0-1", keep=True)], [hl("part:0-2", "part-lbl:0-2")]],
        model_answer="실제로 쓴 돈은 {P} − {C} = {T}(원)이다. {A}를 x개 샀다고 하면 {B}는 ({n} − x)개이므로 {pa}x + {pb}({n} − x) = {T}이고, 정리하면 {co(dp)}x = {T - pbn}에서 x = {x}이다. 따라서 {B}는 {n} − {x} = {y}개 샀다. 실제로 {pa*x} + {pb*y} = {T}원이므로 조건에 맞는다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "총액을 {P} − {C} = {T}로 구하고, {A} x개·{B} ({n} − x)개로 놓아 {pa}x + {pb}({n} − x) = {T}{eul(T)} 세웠다.", "partial": "거스름돈을 빼지 않고 {P}{ro(P)} 식을 세웠으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "괄호를 풀고 동류항을 정리해 x = {x}{eul(x)} 바르게 구했다.", "partial": "괄호를 풀어 정리하는 데까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{B}의 개수 {n} − {x} = {y}개를 답으로 썼다.", "partial": "{A}의 개수 {x}{eul(x)} 답으로 썼으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def purchase_t3():
    return tpl("m1-1-purchase", 3,
        title="한 품목을 k개 더 샀을 때 — 개수 구하기",
        skill="적게 산 품목을 x개로 놓고 많이 산 품목을 (x + k)개로 나타내 총액으로 방정식 세우기",
        variant_axis={"구하는 것": "적게 산 품목의 개수", "조건": "개수 차·총액", "맥락": "편의점·문구점"},
        discriminates="'k개 더 샀다'를 (x + k)로 나타내고 각 품목의 값을 가격 × 개수로 세우는가",
        qtype="short", difficulty=2, pool_target=300, tags=["물건 구매", "일차방정식의 활용"],
        params=[SHOP_CPARAM, PA, PB, {"name": "y", "values": {"int": [2, 9]}}, {"name": "k", "values": {"int": [2, 6]}}],
        table=SHOP_TABLE,
        derive={"x": "y + k", "T": "pa*(y + k) + pb*y", "pak": "pa*k", "sp": "pa + pb"},
        constraints=["y != k", "x != k"],
        cost_values=["pa", "pb", "k", "T", "y", "pak"],
        relation="pa*(X + k) + pb*X - T", unknown="X", answer_var="y",
        verify=["pa*(ans + k) + pb*ans == T"],
        question="{S} 한 개에 {pa}원인 {A}를 한 개에 {pb}원인 {B}보다 {k}개 더 사고 모두 {T}원을 냈다. {B}는 몇 개 샀는지 구하시오.",
        answer="{y}", answer_alt=["{y}개"],
        sol1="'{A}를 {B}보다 {k}개 더 샀다'이므로 적게 산 {B}를 x개로 놓으면 {A}는 (x + {k})개다. 품목마다 (가격) × (개수)를 구해 더한 것이 총액 {T}원이다 — {pa}(x + {k}) + {pb}x = {T}. 막대 하나를 두 칸으로 나누어 적어 두면 식이 보인다.",
        sol1_fig=bar([{"name": "총액", "total": "{T}원", "parts": [{"label": "{A} (x + {k})개", "value": "{pa*x}", "fill": True}, {"label": "{B} x개", "value": "{pb*y}"}]}]),
        sol1_anim=[[hl("part:0-1", "part-lbl:0-1")], [hl("part:0-0", "part-lbl:0-0")], [hl("total:0", keep=True)]],
        sol2=[
            "{B}를 x개 샀다고 하면 {A}는 (x + {k})개 샀다.",
            "{A}의 값은 {pa}(x + {k})원, {B}의 값은 {pb}x원이다.",
            "총액이 {T}원이므로 {pa}(x + {k}) + {pb}x = {T}",
            "괄호를 풀면 {pa}x + {pak} + {pb}x = {T}",
            "동류항을 모으고 이항하면 {sp}x = {T - pak}",
            "양변을 {sp}{ro(sp)} 나누면 x = {y}",
        ],
        sol2_fig=steps([
            {"text": "{pa}(x + {k}) + {pb}x = {T}", "hint": "{A}는 x + {k}개"},
            {"text": "{pa}x + {pak} + {pb}x = {T}", "hint": "괄호 풀기", "marks": [{"on": "{pak}", "note": "{pa}×{k}"}]},
            {"text": "{sp}x = {T - pak}", "hint": "동류항 정리 후 이항"},
            {"text": "x = {y}", "marks": [{"on": "{y}", "note": "{T - pak}÷{sp}"}]},
        ]),
        sol2_anim=[[], [], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="{B} {y}개는 {pb} × {y} = {pb*y}원, {A}는 {y} + {k} = {x}개로 {pa} × {x} = {pa*x}원이고 합은 {pa*x} + {pb*y} = {T}원으로 조건과 같다. 답은 {y}개다.",
        sol3_fig=bar([{"name": "총액", "total": "{pa*x} + {pb*y} = {T}원", "parts": [{"label": "{A} {x}개", "value": "{pa*x}", "fill": True}, {"label": "{B} {y}개", "value": "{pb*y}"}]}]),
        sol3_anim=[[hl("part:0-1", "part-lbl:0-1", keep=True)], [hl("part:0-0", "part-lbl:0-0")], [hl("total:0")]],
        model_answer="{B}를 x개 샀다고 하면 {A}는 (x + {k})개이므로 총액에서 {pa}(x + {k}) + {pb}x = {T}이다. 괄호를 풀어 정리하면 {sp}x = {T - pak}에서 x = {y}이다. 실제로 {A} {x}개와 {B} {y}개의 값은 {pa*x} + {pb*y} = {T}원이므로 조건에 맞는다. 따라서 {B}는 {y}개 샀다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "{B}의 개수를 x, {A}의 개수를 x + {k}로 놓고 {pa}(x + {k}) + {pb}x = {T}{eul(T)} 세웠다.", "partial": "'{k}개 더'를 x + {k}로 나타냈으나 총액 식이 틀렸으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "괄호를 풀고 동류항을 정리해 x = {y}{eul(y)} 바르게 구했다.", "partial": "괄호를 풀어 정리하는 데까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "답을 {B} {y}개로 쓰고 총액이 맞는지 확인했다.", "partial": "확인 없이 답만 옳게 썼으면 1점."},
        ],
        rubric_total=8,
    )


PURCHASE_SEED = {
    "seed_id": "m1-1-purchase", "category": "활용",
    "title": "두 품목 구매 — 개수·거스름돈·개수 차 (일차방정식의 활용)",
    "unit_id": "m1-1", "concept_ids": ["m1-1-27"],
    "schema_id": SCHEMA_PURCHASE, "schema_name": "상품 구입과 거스름돈 구하기",
    "source_item_ids": [],
    "note": "관계식 (가격 × 개수)의 합 = 총액 만 차용. 개수 x·y 를 먼저 뽑고 총액을 생성해 정수해를 보장. 맥락(편의점·문구점·분식집·카페)과 가격은 표·파라미터로 변주. 그림은 막대 한 줄.",
    "geometry": False,
    "templates": [purchase_t1(), purchase_t2(), purchase_t3()],
}


if __name__ == "__main__":
    for seed in (AGE_SEED, CONSEC_SEED, SURPLUS_SEED, PURCHASE_SEED):
        with_pitfalls(seed)
        dump(seed)
