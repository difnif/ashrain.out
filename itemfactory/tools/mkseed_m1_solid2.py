# itemfactory/tools/mkseed_m1_solid2.py — 입체도형 시드 생성기 2: 다면체 세기 · 각기둥·각뿔 겉넓이·부피 (v1.0 · 2026-09-11)
#
#   python itemfactory/tools/mkseed_m1_solid2.py
#     → seeds/m1-2-polyhedron.json (5틀) · seeds/m1-2-prism-pyramid.json (6틀)
#
# 다면체 세기: n각기둥·n각뿔·n각뿔대의 면·모서리·꼭짓점 (F, E, V) 를 표 행(밑면 수 nb·꼭대기 ap)으로 파생 — F = nb + n, E = n·nb + n, V = n·nb + ap.
# 이름(칠각기둥)은 표 행. 그림 없는 기하 틀이라 audit D3 경고가 난다(예상). 각기둥·각뿔은 solid(triangular_prism·square_pyramid·rectangular_prism)로 그린다.
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, table, with_pitfalls  # noqa: E402

SCHEMA_POLYHEDRON = "0cf606df-5557-4250-982f-90e722513204"   # 다면체의 면·모서리·꼭짓점 개수 활용
SCHEMA_PRISM = "eb9d7ef4-8fc1-427d-8174-3dc798c2d0af"        # 각기둥 부피 응용
SCHEMA_PYRAMID = "e6ce8920-9e27-42fd-b1e7-a2927f088a21"      # 각뿔의 부피

GEO = {"process": "절차수행", "context": "기하맥락", "points": 4, "time_limit": 80, "traps": ["구하는대상혼동", "조건누락"]}


def tpl(seed_id, no, *bases, **kw):
    t = dict(GEO)
    for b in bases:
        t.update(b)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def solid(kind, **args):
    return [{"fn": "solid", "args": {"kind": kind, **args}}]


# ═══════════════════════════════════════════════════════════════════ 1. 다면체 — 면·모서리·꼭짓점
KPRE = {3: "삼", 4: "사", 5: "오", 6: "육", 7: "칠", 8: "팔", 9: "구", 10: "십", 11: "십일", 12: "십이", 13: "십삼", 14: "십사", 15: "십오"}
KINDS = {
    "p": {"KIND": "각기둥", "nb": 2, "ap": 0, "APX": "", "FTXT": "밑면 2개와 옆면(직사각형)", "ETXT": "두 밑면의 모서리와 옆모서리", "VTXT": "두 밑면의 꼭짓점", "BTXT": "두 밑면"},
    "y": {"KIND": "각뿔", "nb": 1, "ap": 1, "APX": " + 꼭대기 1개", "FTXT": "밑면 1개와 옆면(삼각형)", "ETXT": "밑면의 모서리와 옆모서리", "VTXT": "밑면의 꼭짓점과 꼭대기 1개", "BTXT": "밑면"},
    "t": {"KIND": "각뿔대", "nb": 2, "ap": 0, "APX": "", "FTXT": "두 밑면과 옆면(사다리꼴)", "ETXT": "두 밑면의 모서리와 옆모서리", "VTXT": "두 밑면의 꼭짓점", "BTXT": "두 밑면"},
}
N_ROWS = {str(n): {"KPRE": KPRE[n]} for n in KPRE}          # n → 이름 접두(삼·사·…·십이); 이름은 "{KPRE}{KIND}" 로 붙여 쓴다
DIFF_TXT = {("p", "ev"): "n", ("p", "ef"): "2n − 2", ("t", "ev"): "n", ("t", "ef"): "2n − 2", ("y", "ev"): "n − 1", ("y", "ef"): "n − 1"}
ASK = {"f": {"ASK": "면", "aF": 1, "aE": 0, "aV": 0}, "e": {"ASK": "모서리", "aF": 0, "aE": 1, "aV": 0}, "v": {"ASK": "꼭짓점", "aF": 0, "aE": 0, "aV": 1}}
PH = dict(prereq=["각기둥·각뿔·각뿔대의 밑면·옆면", "면·모서리·꼭짓점"], ops=["사칙"], tags=["다면체", "각기둥", "각뿔", "각뿔대"])
DERIVE_FEV = {"F": "nb + n", "E": "n*nb + n", "V": "n*nb + ap"}
SOL1 = "{KPRE}{KIND}은 밑면이 {KPRE}각형인 {KIND}이다. 면은 {FTXT} {n}개, 모서리는 {ETXT}, 꼭짓점은 {VTXT}로 이루어진다. 세는 방법은 공식 암기가 아니라 '밑면 몇 개, 옆면 몇 개'를 그려 보는 것이다."
STEPS_FEV = [
    {"text": "면: 밑면 {nb}개 + 옆면 {n}개 = {F}", "hint": "{FTXT}"},
    {"text": "모서리: 밑면의 모서리 {nb*n}개 + 옆모서리 {n}개 = {E}", "hint": "{ETXT}"},
    {"text": "꼭짓점: 밑면의 꼭짓점 {nb*n}개{APX} = {V}", "hint": "{VTXT}"},
]


def ph_t1():
    return tpl("m1-2-polyhedron", 1, PH,
        title="n각기둥·n각뿔·n각뿔대의 면·모서리·꼭짓점의 개수",
        skill="밑면의 변의 개수 n으로 면·모서리·꼭짓점의 개수를 세기 — 밑면 몇 개, 옆면 몇 개인지 그려서 센다",
        variant_axis={"구하는 것": "면·모서리·꼭짓점", "입체": "각기둥·각뿔·각뿔대", "n": "3~12"},
        discriminates="각기둥(밑면 2개)·각뿔(꼭대기 1개)·각뿔대(밑면 2개)의 구조 차이를 세기에 반영하는가",
        qtype="short", difficulty=1, pool_target=300,
        params=[{"name": "n", "values": {"int": [3, 15]}}, {"name": "kd", "values": {"in": list(KINDS)}}, {"name": "ask", "values": {"in": list(ASK)}}],
        table=[{"key": "n", "rows": N_ROWS}, {"key": "kd", "rows": KINDS}, {"key": "ask", "rows": ASK}],
        derive={**DERIVE_FEV, "ans": "aF*(nb + n) + aE*(n*nb + n) + aV*(n*nb + ap)"},
        constraints=[],
        cost_values=["n", "F", "E", "V"],
        relation="X - aF*F - aE*E - aV*V", unknown="X", answer_var="ans",
        verify=["ans == aF*F + aE*E + aV*V", "ans >= 4"],
        question="{KPRE}{KIND}의 {ASK}의 개수를 구하시오.",
        answer="{ans}", answer_alt=["{ans}개"],
        sol1=SOL1,
        sol1_fig=steps(["{KPRE}{KIND} = 밑면이 {KPRE}각형인 {KIND}", "{FTXT}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "면의 개수: 밑면 {nb}개 + 옆면 {n}개 = {F}",
            "모서리의 개수: 밑면의 모서리 {nb*n}개 + 옆모서리 {n}개 = {E}",
            "꼭짓점의 개수: 밑면의 꼭짓점 {nb*n}개{APX} = {V}",
            "따라서 {ASK}의 개수는 {ans}",
        ],
        sol2_fig=steps(STEPS_FEV + [{"text": "{ASK}의 개수 = {ans}", "marks": [{"on": "{ans}", "note": "{ASK}"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol_check="오일러 공식 (꼭짓점) − (모서리) + (면) = {V} − {E} + {F} = 2가 성립하므로 세 개수가 맞다. 답: {ans}",
        model_answer="{KPRE}{KIND}은 밑면이 {KPRE}각형인 {KIND}이므로 면은 밑면 {nb}개와 옆면 {n}개로 {F}개, 모서리는 밑면의 모서리 {nb*n}개와 옆모서리 {n}개로 {E}개, 꼭짓점은 밑면의 꼭짓점 {nb*n}개{APX}로 {V}개이다. 따라서 {ASK}의 개수는 {ans}이다.",
        rubric=[
            {"element": "구조 읽기", "points": 2, "criterion": "{KPRE}{KIND}이 밑면이 {KPRE}각형인 {KIND}임을 밝히고 {BTXT}과 옆면 {n}개로 이루어짐을 적었다.", "partial": "밑면의 변의 개수 {n}만 적었으면 1점."},
            {"element": "개수 세기", "points": 3, "criterion": "{ASK}의 개수를 밑면·옆면(꼭대기) 구조로 세어 {ans}{eul(ans)} 구했다.", "partial": "구조는 맞으나 곱셈·덧셈이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}개로 답했다.", "partial": "다른 요소(면·모서리·꼭짓점)의 개수를 답했으면 인정하지 않는다."},
        ],
    )


GIVEN = {"f": {"GIV": "면", "gF": 1, "gE": 0, "gV": 0}, "e": {"GIV": "모서리", "gF": 0, "gE": 1, "gV": 0}, "v": {"GIV": "꼭짓점", "gF": 0, "gE": 0, "gV": 1}}
ASK2 = {**ASK, "n": {"ASK": "밑면인 다각형의 변", "aF": 0, "aE": 0, "aV": 0}}


def ph_t2():
    return tpl("m1-2-polyhedron", 2, PH,
        title="면(모서리·꼭짓점)의 개수로 n을 찾아 다른 개수 구하기",
        skill="주어진 개수를 n의 식으로 놓아 n을 구한 뒤 구하는 개수를 센다",
        variant_axis={"주어진 것": "면·모서리·꼭짓점", "구하는 것": "변·면·모서리·꼭짓점", "입체": "각기둥·각뿔·각뿔대"},
        discriminates="주어진 개수를 n의 식(n + 2, 3n, 2n …)으로 되돌려 n을 구하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "n", "values": {"int": [3, 15]}}, {"name": "kd", "values": {"in": list(KINDS)}}, {"name": "giv", "values": {"in": list(GIVEN)}}, {"name": "ask", "values": {"in": list(ASK2)}}],
        table=[{"key": "n", "rows": N_ROWS}, {"key": "kd", "rows": KINDS}, {"key": "giv", "rows": GIVEN}, {"key": "ask", "rows": ASK2}],
        derive={**DERIVE_FEV, "gv": "gF*(nb + n) + gE*(n*nb + n) + gV*(n*nb + ap)",
                "ans": "aF*(nb + n) + aE*(n*nb + n) + aV*(n*nb + ap) + (1 - aF - aE - aV)*n"},
        constraints=["gv != ans", "aF*gF + aE*gE + aV*gV == 0"],
        cost_values=["n", "gv", "ans"],
        relation="X - ans", unknown="X", answer_var="ans",
        verify=["gv == gF*F + gE*E + gV*V", "ans != gv"],
        question="{GIV}의 개수가 {gv}인 {KIND}의 {ASK}의 개수를 구하시오.",
        answer="{ans}", answer_alt=["{ans}개"],
        sol1="밑면이 n각형인 {KIND}의 면·모서리·꼭짓점의 개수는 각각 n의 식으로 쓸 수 있다({FTXT} n개 → 면 n + {nb}, 모서리 {co(nb)}n + n, 꼭짓점 {co(nb)}n + {ap}). 주어진 {GIV}의 개수 {gv}{eul(gv)} 그 식과 같다고 놓아 n을 먼저 구한 뒤, 구하는 개수를 센다.",
        sol1_fig=steps(["밑면이 n각형인 {KIND}", "면 = n + {nb},  모서리 = {co(nb)}n + n,  꼭짓점 = {co(nb)}n + {ap}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "밑면을 n각형이라 하면 {GIV}의 개수는 n의 식이고, 이것이 {gv}이므로 n = {n} — 밑면은 {KPRE}각형",
            "즉 이 입체는 {KPRE}{KIND}이다",
            "면: 밑면 {nb}개 + 옆면 {n}개 = {F}, 모서리: {nb*n} + {n} = {E}, 꼭짓점: {nb*n}{APX} = {V}",
            "따라서 {ASK}의 개수는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "{GIV}의 개수 = {gv} → n = {n}", "hint": "n의 식으로 되돌리기", "marks": [{"on": "{n}", "note": "밑면 {KPRE}각형"}]},
            {"text": "{KPRE}{KIND}"},
            {"text": "면 {F} · 모서리 {E} · 꼭짓점 {V}", "hint": "{FTXT}"},
            {"text": "{ASK}의 개수 = {ans}", "marks": [{"on": "{ans}", "note": "{ASK}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1)], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol_check="{KPRE}{KIND}의 {GIV}의 개수를 다시 세면 {gv}{ro(gv)} 문제의 조건과 같다. 답: {ans}",
        model_answer="밑면을 n각형이라 하면 {KIND}의 {GIV}의 개수는 n의 식으로 나타나고, 이것이 {gv}이므로 n = {n}, 즉 {KPRE}{KIND}이다. {KPRE}{KIND}의 면은 {F}개, 모서리는 {E}개, 꼭짓점은 {V}개이므로 {ASK}의 개수는 {ans}이다.",
        rubric=[
            {"element": "n 구하기", "points": 3, "criterion": "{GIV}의 개수를 n의 식으로 놓아 n = {n}({KPRE}{KIND})임을 구했다.", "partial": "식은 세웠으나 n을 잘못 구했으면 1점."},
            {"element": "개수 세기", "points": 2, "criterion": "{KPRE}{KIND}의 {ASK}의 개수를 구조대로 세어 {ans}{eul(ans)} 구했다.", "partial": "구조는 맞으나 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}{ro(ans)} 답했다.", "partial": "n의 값이나 다른 개수를 답했으면 인정하지 않는다."},
        ],
    )


COMBO = {
    "1": {"EXPR": "v + e + f", "cv": 1, "ce": 1, "cf": 1},
    "2": {"EXPR": "v − e + f", "cv": 1, "ce": -1, "cf": 1},
    "3": {"EXPR": "e − v", "cv": -1, "ce": 1, "cf": 0},
    "4": {"EXPR": "e − f", "cv": 0, "ce": 1, "cf": -1},
    "5": {"EXPR": "v + f", "cv": 1, "ce": 0, "cf": 1},
    "6": {"EXPR": "e + f", "cv": 0, "ce": 1, "cf": 1},
}


def ph_t3():
    return tpl("m1-2-polyhedron", 3, PH,
        title="v, e, f 의 식의 값 — 세 개수를 모두 센 뒤 계산",
        skill="꼭짓점 v·모서리 e·면 f를 각각 센 뒤 주어진 식에 대입한다 (v − e + f = 2는 언제나 성립)",
        variant_axis={"구하는 것": "v, e, f의 식", "입체": "각기둥·각뿔·각뿔대", "n": "3~12"},
        discriminates="세 개수를 모두 정확히 세고 식의 순서·부호대로 계산하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "n", "values": {"int": [3, 15]}}, {"name": "kd", "values": {"in": list(KINDS)}}, {"name": "cb", "values": {"in": list(COMBO)}}],
        table=[{"key": "n", "rows": N_ROWS}, {"key": "kd", "rows": KINDS}, {"key": "cb", "rows": COMBO}],
        derive={**DERIVE_FEV, "ans": "cv*(n*nb + ap) + ce*(n*nb + n) + cf*(nb + n)"},
        constraints=["ans > 0"],
        cost_values=["n", "F", "E", "V", "ans"],
        relation="X - cv*V - ce*E - cf*F", unknown="X", answer_var="ans",
        verify=["ans == cv*V + ce*E + cf*F"],
        question="{KPRE}{KIND}의 꼭짓점의 개수를 v, 모서리의 개수를 e, 면의 개수를 f라 할 때, {EXPR}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{KPRE}{KIND}은 밑면이 {KPRE}각형인 {KIND}이다. v, e, f를 하나씩 센다 — 면은 {FTXT} {n}개, 모서리는 {ETXT}, 꼭짓점은 {VTXT}. 세 값을 구한 뒤 {EXPR}에 넣는다.",
        sol1_fig=steps(["{KPRE}{KIND} = 밑면이 {KPRE}각형인 {KIND}", "v, e, f 를 각각 센 뒤 {EXPR}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "꼭짓점: 밑면의 꼭짓점 {nb*n}개{APX} → v = {V}",
            "모서리: 밑면의 모서리 {nb*n}개 + 옆모서리 {n}개 → e = {E}",
            "면: 밑면 {nb}개 + 옆면 {n}개 → f = {F}",
            "따라서 {EXPR} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "v = {V}", "hint": "{VTXT}"},
            {"text": "e = {E}", "hint": "{ETXT}"},
            {"text": "f = {F}", "hint": "{FTXT}"},
            {"text": "{EXPR} = {ans}", "marks": [{"on": "{ans}", "note": "대입"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol_check="v − e + f = {V} − {E} + {F} = 2(오일러 공식)이므로 세 개수가 맞게 세어졌다. 답: {ans}",
        model_answer="{KPRE}{KIND}은 밑면이 {KPRE}각형인 {KIND}이므로 v = {V}, e = {E}, f = {F}이다. 따라서 {EXPR} = {ans}이다.",
        rubric=[
            {"element": "개수 세기", "points": 4, "criterion": "v = {V}, e = {E}, f = {F}를 구조대로 세어 구했다.", "partial": "셋 중 하나가 틀렸으면 2점, 둘 이상 틀렸으면 인정하지 않는다."},
            {"element": "식의 값", "points": 3, "criterion": "{EXPR} = {ans}{eul(ans)} 부호·순서대로 계산했다.", "partial": "세 값은 맞으나 계산이 틀렸으면 1점."},
        ],
    )


ASK3 = {"n": {"ASK": "밑면인 다각형의 변", "aF": 0, "aE": 0, "aV": 0}, "f": ASK["f"], "e": ASK["e"], "v": ASK["v"]}


def ph_t4():
    return tpl("m1-2-polyhedron", 4, PH,
        title="v + e + f 의 값으로 n을 찾아 개수 구하기",
        skill="v + e + f 를 n의 식으로 나타내 방정식을 풀고 n을 구한다",
        variant_axis={"주어진 것": "v + e + f", "구하는 것": "변·면·모서리·꼭짓점", "입체": "각기둥·각뿔·각뿔대"},
        discriminates="세 개수의 합을 n의 일차식으로 세우고 n을 푸는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "n", "values": {"int": [3, 15]}}, {"name": "kd", "values": {"in": list(KINDS)}}, {"name": "ask", "values": {"in": list(ASK3)}}],
        table=[{"key": "n", "rows": N_ROWS}, {"key": "kd", "rows": KINDS}, {"key": "ask", "rows": ASK3}],
        derive={**DERIVE_FEV, "T": "(n*nb + ap) + (n*nb + n) + (nb + n)", "cn": "2*nb + 2", "c0": "ap + nb",
                "ans": "aF*(nb + n) + aE*(n*nb + n) + aV*(n*nb + ap) + (1 - aF - aE - aV)*n"},
        constraints=["ans != T"],
        cost_values=["n", "T", "ans"],
        relation="X - ans", unknown="X", answer_var="ans",
        verify=["T == V + E + F", "T == cn*n + c0"],
        question="어떤 {KIND}의 꼭짓점의 개수를 v, 모서리의 개수를 e, 면의 개수를 f라 하면 v + e + f = {T}이다. 이 {KIND}의 {ASK}의 개수를 구하시오.",
        answer="{ans}", answer_alt=["{ans}개"],
        sol1="밑면을 n각형이라 하면 {KIND}의 꼭짓점은 {co(nb)}n + {ap}, 모서리는 {co(nb)}n + n, 면은 n + {nb}이다. 세 식을 더한 {cn}n + {c0}{ika(c0)} {T}{wa(T)} 같다고 놓으면 n이 나온다. n을 구한 뒤 구하는 개수를 센다.",
        sol1_fig=steps(["v = {co(nb)}n + {ap},  e = {co(nb)}n + n,  f = n + {nb}", "v + e + f = {cn}n + {c0}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "밑면을 n각형이라 하면 v = {co(nb)}n + {ap}, e = {co(nb)}n + n = {nb + 1}n, f = n + {nb}",
            "v + e + f = {cn}n + {c0} = {T}에서 {cn}n = {T - c0}, n = {n}",
            "즉 이 입체는 {KPRE}{KIND}이고, 면 {F}개 · 모서리 {E}개 · 꼭짓점 {V}개",
            "따라서 {ASK}의 개수는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "v + e + f = {cn}n + {c0}", "hint": "세 식의 합"},
            {"text": "{cn}n + {c0} = {T} → n = {n}", "marks": [{"on": "{n}", "note": "{T - c0} ÷ {cn}"}]},
            {"text": "{KPRE}{KIND}: 면 {F} · 모서리 {E} · 꼭짓점 {V}"},
            {"text": "{ASK}의 개수 = {ans}", "marks": [{"on": "{ans}", "note": "{ASK}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)], [reveal(3), hl("mark:3-0")]],
        sol_check="{KPRE}{KIND}에서 v + e + f = {V} + {E} + {F} = {T}{ro(T)} 조건과 같다. 답: {ans}",
        model_answer="밑면을 n각형이라 하면 v = {co(nb)}n + {ap}, e = {nb + 1}n, f = n + {nb}이므로 v + e + f = {cn}n + {c0}이다. {cn}n + {c0} = {T}에서 n = {n}이므로 이 입체는 {KPRE}{KIND}이고, {ASK}의 개수는 {ans}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "v, e, f를 n의 식으로 나타내 v + e + f = {cn}n + {c0}{eul(c0)} 세웠다.", "partial": "셋 중 하나의 식이 틀렸으면 1점."},
            {"element": "n 구하기", "points": 2, "criterion": "{cn}n + {c0} = {T}에서 n = {n}{eul(n)} 구했다.", "partial": "방정식은 맞으나 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{KPRE}{KIND}의 {ASK}의 개수 {ans}{eul(ans)} 답했다.", "partial": "n의 값을 답했으면 인정하지 않는다."},
        ],
    )


DIFF = {"ev": {"D1": "모서리", "D2": "꼭짓점", "d2V": 1, "d2F": 0}, "ef": {"D1": "모서리", "D2": "면", "d2V": 0, "d2F": 1}}
KD_ROWS = {f"{k}-{d}": {**KINDS[k], **DIFF[d], "DTXT": DIFF_TXT[(k, d)]} for k in KINDS for d in DIFF}


def ph_t5():
    return tpl("m1-2-polyhedron", 5, PH,
        title="두 개수의 차로 n을 찾아 개수 구하기",
        skill="(모서리) − (꼭짓점), (모서리) − (면)을 n의 식으로 나타내 n을 구한다",
        variant_axis={"주어진 것": "e − v · e − f", "구하는 것": "변·면·모서리·꼭짓점", "입체": "각기둥·각뿔·각뿔대"},
        discriminates="두 개수의 차를 n의 식으로 세우고 n을 푸는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "n", "values": {"int": [3, 15]}}, {"name": "kd", "values": {"in": list(KD_ROWS)}}, {"name": "ask", "values": {"in": list(ASK3)}}],
        table=[{"key": "n", "rows": N_ROWS}, {"key": "kd", "rows": KD_ROWS}, {"key": "ask", "rows": ASK3}],
        derive={**DERIVE_FEV, "dd": "(n*nb + n) - d2V*(n*nb + ap) - d2F*(nb + n)", "cn": "(nb + 1) - d2V*nb - d2F", "c0": "-d2V*ap - d2F*nb",
                "ans": "aF*(nb + n) + aE*(n*nb + n) + aV*(n*nb + ap) + (1 - aF - aE - aV)*n"},
        constraints=["dd >= 2", "ans != dd", "cn >= 1"],
        cost_values=["n", "dd", "ans"],
        relation="X - ans", unknown="X", answer_var="ans",
        verify=["dd == E - d2V*V - d2F*F", "dd == cn*n + c0"],
        question="어떤 {KIND}의 {D1}의 개수는 {D2}의 개수보다 {dd}만큼 많다. 이 {KIND}의 {ASK}의 개수를 구하시오.",
        answer="{ans}", answer_alt=["{ans}개"],
        sol1="밑면을 n각형이라 하면 {KIND}의 모서리는 {co(nb)}n + n = {nb + 1}n, 꼭짓점은 {co(nb)}n + {ap}, 면은 n + {nb}이다. ({D1}) − ({D2})를 n의 식으로 쓰면 {DTXT}이고, 이것이 {dd}{wa(dd)} 같다고 놓으면 n이 나온다.",
        sol1_fig=steps(["e = {nb + 1}n,  v = {co(nb)}n + {ap},  f = n + {nb}", "({D1}) − ({D2}) = {DTXT}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "밑면을 n각형이라 하면 {D1}의 개수는 {nb + 1}n, {D2}의 개수는 n의 식으로 나타난다",
            "({D1}) − ({D2}) = {DTXT} = {dd}에서 n = {n}",
            "즉 이 입체는 {KPRE}{KIND}이고, 면 {F}개 · 모서리 {E}개 · 꼭짓점 {V}개",
            "따라서 {ASK}의 개수는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "({D1}) − ({D2}) = {DTXT}", "hint": "n의 식으로"},
            {"text": "{DTXT} = {dd} → n = {n}", "marks": [{"on": "{n}", "note": "밑면 {KPRE}각형"}]},
            {"text": "{KPRE}{KIND}: 면 {F} · 모서리 {E} · 꼭짓점 {V}"},
            {"text": "{ASK}의 개수 = {ans}", "marks": [{"on": "{ans}", "note": "{ASK}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)], [reveal(3), hl("mark:3-0")]],
        sol_check="{KPRE}{KIND}에서 ({D1}) − ({D2}) = {dd}{ro(dd)} 조건과 같다. 답: {ans}",
        model_answer="밑면을 n각형이라 하면 {KIND}의 {D1}의 개수는 {nb + 1}n이고, ({D1}) − ({D2}) = {DTXT}이다. 이것이 {dd}이므로 n = {n}, 즉 {KPRE}{KIND}이다. 따라서 {ASK}의 개수는 {ans}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "{D1}·{D2}의 개수를 n의 식으로 나타내 차가 {DTXT}임을 세웠다.", "partial": "둘 중 한 식이 틀렸으면 1점."},
            {"element": "n 구하기", "points": 2, "criterion": "{DTXT} = {dd}에서 n = {n}{eul(n)} 구했다.", "partial": "방정식은 맞으나 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{KPRE}{KIND}의 {ASK}의 개수 {ans}{eul(ans)} 답했다.", "partial": "n의 값을 답했으면 인정하지 않는다."},
        ],
    )


POLY_SEED = {
    "seed_id": "m1-2-polyhedron", "category": "도형",
    "title": "다면체 — 각기둥·각뿔·각뿔대의 면·모서리·꼭짓점",
    "unit_id": "m1-2", "concept_ids": ["m1-2-12"],
    "schema_id": SCHEMA_POLYHEDRON, "schema_name": "다면체의 면·모서리·꼭짓점 개수 활용 / 다면체 모서리 개수 비교",
    "source_item_ids": [],
    "note": "출판사 7.1 유형(n각기둥·뿔·뿔대 면·모서리·꼭짓점 / 역산 / v+e+f / 차) 차용. F = nb + n, E = n·nb + n, V = n·nb + ap 를 표 행(nb·ap)으로 파생. 그림 없는 기하 틀(D3 경고 예상). 정다면체 조건은 개념 판별형이라 제외.",
    "geometry": True,
    "templates": [ph_t1(), ph_t2(), ph_t3(), ph_t4(), ph_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 각기둥·각뿔 — 겉넓이·부피
PP = dict(prereq=["기둥의 부피 = (밑넓이) × (높이)", "뿔의 부피 = (밑넓이) × (높이) ÷ 3", "겉넓이 = (밑넓이) × 2 + (옆넓이)"], ops=["넓이", "부피"], tags=["각기둥", "각뿔", "겉넓이", "부피"])
TRIPLES = {str(i + 1): {"a": a, "b": b, "c": c} for i, (a, b, c) in enumerate([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17), (12, 16, 20), (8, 6, 10), (4, 3, 5), (7, 24, 25), (15, 20, 25), (10, 24, 26), (12, 5, 13), (16, 12, 20), (20, 15, 25)])}


def pp_t1():
    return tpl("m1-2-prism-pyramid", 1, PP,
        title="밑면이 직각삼각형인 삼각기둥의 겉넓이",
        skill="겉넓이 = (밑넓이) × 2 + (옆넓이), 옆넓이 = (밑면의 둘레) × (높이)",
        variant_axis={"구하는 것": "겉넓이", "밑면": "직각삼각형(피타고라스 수 8종)", "높이": "3~15"},
        discriminates="옆면 세 직사각형의 가로가 밑면의 세 변임을 알고 둘레 × 높이로 묶는가, 밑면을 두 개 세는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "tr", "values": {"in": list(TRIPLES)}}, {"name": "h", "values": {"int": [3, 20]}}],
        table={"key": "tr", "rows": TRIPLES},
        derive={"B": "a*b/2", "P": "a + b + c", "L": "(a + b + c)*h", "S": "a*b + (a + b + c)*h"},
        constraints=["h != a", "h != b", "h != c", "S <= 1500"],
        cost_values=["a", "b", "c", "h", "B", "L", "S"],
        relation="X - 2*(a*b/2) - (a + b + c)*h", unknown="X", answer_var="S",
        verify=["ans == 2*B + L"],
        question="다음 그림과 같이 밑면이 빗변의 길이가 {c} cm이고 다른 두 변의 길이가 {a} cm, {b} cm인 직각삼각형이며 높이가 {h} cm인 삼각기둥의 겉넓이를 구하시오.",
        figure=solid("triangular_prism"),
        answer="{S}", answer_alt=["{S} cm²"],
        sol1="삼각기둥을 펼치면 밑면인 직각삼각형 2개와 옆면인 직사각형 3개가 나온다. 세 옆면의 세로는 모두 높이 {h} cm이고 가로는 밑면의 세 변 {a} cm, {b} cm, {c} cm이므로, 옆넓이는 (밑면의 둘레) × (높이)로 한 번에 구한다. 밑넓이는 직각을 낀 두 변으로 {a} × {b} ÷ 2다.",
        sol1_fig=solid("triangular_prism"),
        sol2=[
            "밑넓이: {a} × {b} ÷ 2 = {B} (cm²), 밑면이 2개이므로 {B} × 2 = {2*B} (cm²)",
            "옆넓이: (밑면의 둘레) × (높이) = ({a} + {b} + {c}) × {h} = {P} × {h} = {L} (cm²)",
            "겉넓이 = {2*B} + {L} = {S} (cm²)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 × 2 = ({a} × {b} ÷ 2) × 2 = {2*B}", "hint": "직각을 낀 두 변", "marks": [{"on": "{2*B}", "note": "밑면 2개"}]},
            {"text": "옆넓이 = ({a} + {b} + {c}) × {h} = {L}", "hint": "둘레 × 높이", "marks": [{"on": "{L}", "note": "{P} × {h}"}]},
            {"text": "겉넓이 = {2*B} + {L} = {S} (cm²)"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="밑면을 하나만 세면 {B + L}, 옆면을 하나만 세면 {2*B + a*h}{ika(2*B + a*h)} 나온다 — 모두 답이 아니다. 답: {S} cm²",
        model_answer="삼각기둥의 겉넓이는 (밑넓이) × 2 + (옆넓이)이다. 밑넓이는 {a} × {b} ÷ 2 = {B} (cm²)이고 밑면이 2개이므로 {2*B} (cm²), 옆넓이는 (밑면의 둘레) × (높이) = ({a} + {b} + {c}) × {h} = {L} (cm²)이다. 따라서 겉넓이는 {2*B} + {L} = {S} (cm²)이다.",
        rubric=[
            {"element": "밑넓이", "points": 2, "criterion": "밑넓이 {a} × {b} ÷ 2 = {B}{eul(B)} 구하고 밑면이 2개임을 반영했다.", "partial": "밑넓이는 옳으나 하나만 셌으면 1점."},
            {"element": "옆넓이", "points": 3, "criterion": "옆면이 가로 {a}, {b}, {c}·세로 {h}인 직사각형 3개임을 밝히고 옆넓이 {L}{eul(L)} 구했다.", "partial": "옆면 하나를 빠뜨렸으면 1점."},
            {"element": "겉넓이", "points": 2, "criterion": "{2*B} + {L} = {S} (cm²)로 답했다.", "partial": "더하는 식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


def pp_t2():
    return tpl("m1-2-prism-pyramid", 2, PP,
        title="밑면이 직각삼각형인 삼각기둥의 부피",
        skill="기둥의 부피 = (밑넓이) × (높이) — 밑넓이는 직각을 낀 두 변으로",
        variant_axis={"구하는 것": "부피", "밑면": "직각삼각형", "높이": "3~15"},
        discriminates="밑넓이를 빗변이 아니라 직각을 낀 두 변으로 구하고 높이를 곱하는가",
        qtype="short", difficulty=1, pool_target=300,
        params=[{"name": "tr", "values": {"in": list(TRIPLES)}}, {"name": "h", "values": {"int": [3, 20]}}],
        table={"key": "tr", "rows": TRIPLES},
        derive={"B": "a*b/2", "Vv": "a*b*h/2"},
        constraints=["h != a", "h != b", "h != c", "Vv <= 3000"],
        cost_values=["a", "b", "c", "h", "B", "Vv"],
        relation="X - a*b*h/2", unknown="X", answer_var="Vv",
        verify=["ans == B*h"],
        question="다음 그림과 같이 밑면이 빗변의 길이가 {c} cm이고 다른 두 변의 길이가 {a} cm, {b} cm인 직각삼각형이며 높이가 {h} cm인 삼각기둥의 부피를 구하시오.",
        figure=solid("triangular_prism"),
        answer="{Vv}", answer_alt=["{Vv} cm³"],
        sol1="기둥의 부피는 (밑넓이) × (높이)다. 밑면은 직각삼각형이므로 밑넓이는 직각을 낀 두 변 {a} cm, {b} cm로 {a} × {b} ÷ 2 — 빗변 {c} cm는 넓이 계산에 쓰지 않는다. 여기에 높이 {h} cm를 곱한다.",
        sol1_fig=solid("triangular_prism"),
        sol2=[
            "밑넓이: {a} × {b} ÷ 2 = {B} (cm²)",
            "부피 = (밑넓이) × (높이) = {B} × {h} = {Vv} (cm³)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 = {a} × {b} ÷ 2 = {B}", "hint": "빗변 {c}는 쓰지 않는다"},
            {"text": "부피 = {B} × {h} = {Vv} (cm³)", "marks": [{"on": "{Vv}", "note": "밑넓이 × 높이"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol_check="빗변 {c}{eul(c)} 밑변으로 잘못 쓰면 밑넓이가 달라지고, 2로 나누지 않으면 {2*Vv}{ika(2*Vv)} 된다 — 답이 아니다. 답: {Vv} cm³",
        model_answer="밑면인 직각삼각형의 넓이는 {a} × {b} ÷ 2 = {B} (cm²)이다. 기둥의 부피는 (밑넓이) × (높이)이므로 {B} × {h} = {Vv} (cm³)이다.",
        rubric=[
            {"element": "밑넓이", "points": 3, "criterion": "직각을 낀 두 변으로 밑넓이 {a} × {b} ÷ 2 = {B}{eul(B)} 구했다.", "partial": "2로 나누지 않았으면 1점."},
            {"element": "부피", "points": 2, "criterion": "(밑넓이) × (높이) = {B} × {h} = {Vv} (cm³)로 답했다.", "partial": "식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


BASE3 = {"t": {"BASE": "삼각", "FIG": "triangular_prism"}, "q": {"BASE": "사각", "FIG": "rectangular_prism"}}


def pp_t3():
    return tpl("m1-2-prism-pyramid", 3, PP,
        title="밑넓이와 부피로 각기둥의 높이 구하기",
        skill="(높이) = (부피) ÷ (밑넓이) — 기둥의 부피 공식을 거꾸로",
        variant_axis={"구하는 것": "높이", "밑면": "삼각형·사각형", "제시": "밑넓이·부피"},
        discriminates="부피 공식 (밑넓이) × (높이)를 높이에 대해 거꾸로 푸는가",
        qtype="short", difficulty=1, pool_target=300,
        params=[{"name": "bs", "values": {"in": list(BASE3)}}, {"name": "A", "values": {"int": [6, 40]}}, {"name": "h", "values": {"int": [3, 15]}}],
        table={"key": "bs", "rows": BASE3},
        derive={"Vv": "A*h"},
        constraints=["h != A", "Vv != A", "A % 2 == 0 or A % 3 == 0"],
        cost_values=["A", "h", "Vv"],
        relation="A*X - Vv", unknown="X", answer_var="h",
        verify=["A*ans == Vv"],
        question="밑넓이가 {A} cm²이고 부피가 {Vv} cm³인 {BASE}기둥의 높이를 구하시오.",
        answer="{h}", answer_alt=["{h} cm"],
        sol1="기둥의 부피는 (밑넓이) × (높이)이므로 높이를 h cm라 하면 {A} × h = {Vv}이다. 부피를 밑넓이로 나누면 높이가 나온다 — 밑면이 삼각형이든 사각형이든 밑넓이가 주어졌으니 같은 식이다.",
        sol1_fig=steps(["부피 = 밑넓이 × 높이", "{Vv} = {A} × h"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "높이를 h cm라 하면 (밑넓이) × (높이) = (부피)에서 {A} × h = {Vv}",
            "h = {Vv} ÷ {A} = {h}",
        ],
        sol2_fig=steps([
            {"text": "{A} × h = {Vv}", "hint": "밑넓이 × 높이 = 부피"},
            {"text": "h = {Vv} ÷ {A} = {h}", "marks": [{"on": "{h}", "note": "부피 ÷ 밑넓이"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol_check="높이가 {h} cm이면 부피는 {A} × {h} = {Vv} (cm³)로 조건과 같다. 답: {h} cm",
        model_answer="{BASE}기둥의 높이를 h cm라 하면 (밑넓이) × (높이) = (부피)이므로 {A} × h = {Vv}이다. 따라서 h = {Vv} ÷ {A} = {h}, 즉 높이는 {h} cm이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "기둥의 부피 공식으로 {A} × h = {Vv}{eul(Vv)} 세웠다.", "partial": "부피를 3으로 나누는 등 뿔의 공식을 썼으면 인정하지 않는다."},
            {"element": "높이 구하기", "points": 2, "criterion": "h = {Vv} ÷ {A} = {h} (cm)로 답했다.", "partial": "나눗셈 실수면 1점."},
        ],
    )


def pp_t4():
    return tpl("m1-2-prism-pyramid", 4, PP,
        title="정사각뿔의 겉넓이 — 밑면 + 옆면 삼각형 4개",
        skill="겉넓이 = (밑넓이) + (옆넓이), 옆면은 합동인 이등변삼각형 4개",
        variant_axis={"구하는 것": "겉넓이", "밑면": "정사각형", "옆면": "높이 s인 삼각형"},
        discriminates="옆면 삼각형의 넓이에 ½을 곱하고 4개를 더하는가, 밑면은 하나뿐임을 아는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "a", "values": {"int": [4, 20]}}, {"name": "s", "values": {"int": [5, 24]}}],
        derive={"B": "a*a", "T": "a*s/2", "L": "2*a*s", "S": "a*a + 2*a*s"},
        constraints=["2*s > a", "s != a", "S <= 1500", "T == floor(T)"],
        cost_values=["a", "s", "B", "T", "L", "S"],
        relation="X - a*a - 4*(a*s/2)", unknown="X", answer_var="S",
        verify=["ans == B + 4*T"],
        question="다음 그림과 같이 밑면은 한 변의 길이가 {a} cm인 정사각형이고, 옆면은 모두 높이가 {s} cm인 합동인 이등변삼각형인 사각뿔의 겉넓이를 구하시오.",
        figure=solid("square_pyramid"),
        answer="{S}", answer_alt=["{S} cm²"],
        sol1="사각뿔을 펼치면 밑면인 정사각형 1개와 옆면인 삼각형 4개가 나온다(뿔이므로 밑면은 하나). 옆면 삼각형은 밑변이 {a} cm, 높이가 {s} cm이므로 넓이가 {a} × {s} ÷ 2다. 겉넓이는 (밑넓이) + (옆면 4개의 넓이)다.",
        sol1_fig=solid("square_pyramid"),
        sol2=[
            "밑넓이: {a} × {a} = {B} (cm²)",
            "옆면 한 개: {a} × {s} ÷ 2 = {T} (cm²), 4개이므로 {T} × 4 = {L} (cm²)",
            "겉넓이 = {B} + {L} = {S} (cm²)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 = {a}² = {B}", "hint": "밑면은 하나"},
            {"text": "옆넓이 = ({a} × {s} ÷ 2) × 4 = {L}", "hint": "삼각형 4개", "marks": [{"on": "{L}", "note": "{T} × 4"}]},
            {"text": "겉넓이 = {B} + {L} = {S} (cm²)"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="옆면 삼각형에서 ÷ 2를 빠뜨리면 {B + 2*L}, 밑면을 2개로 세면 {2*B + L}{ika(2*B + L)} 나온다 — 답이 아니다. 답: {S} cm²",
        model_answer="사각뿔의 겉넓이는 (밑넓이) + (옆넓이)이다. 밑넓이는 {a} × {a} = {B} (cm²)이고, 옆면은 밑변 {a} cm·높이 {s} cm인 삼각형 4개이므로 옆넓이는 ({a} × {s} ÷ 2) × 4 = {L} (cm²)이다. 따라서 겉넓이는 {B} + {L} = {S} (cm²)이다.",
        rubric=[
            {"element": "밑넓이", "points": 2, "criterion": "밑넓이 {a} × {a} = {B}{eul(B)} 구했다.", "partial": "밑면을 2개로 셌으면 인정하지 않는다."},
            {"element": "옆넓이", "points": 3, "criterion": "옆면이 삼각형 4개임을 밝히고 ({a} × {s} ÷ 2) × 4 = {L}{eul(L)} 구했다.", "partial": "÷ 2를 빠뜨렸으면 1점."},
            {"element": "겉넓이", "points": 2, "criterion": "{B} + {L} = {S} (cm²)로 답했다.", "partial": "더하는 식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


def pp_t5():
    return tpl("m1-2-prism-pyramid", 5, PP,
        title="정사각뿔대의 부피 — 큰 뿔에서 작은 뿔 빼기",
        skill="(뿔대의 부피) = (큰 뿔의 부피) − (작은 뿔의 부피), 뿔의 부피 = (밑넓이) × (높이) ÷ 3",
        variant_axis={"구하는 것": "뿔대 부피", "닮음비": "1:2·1:3", "높이": "3의 배수"},
        discriminates="뿔대를 두 뿔의 차로 보고 각각 ⅓을 곱해 빼는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "a", "values": {"int": [2, 10]}}, {"name": "k", "values": {"in": [2, 3, 4]}}, {"name": "j", "values": {"int": [1, 6]}}],
        derive={"A": "k*a", "h": "3*j", "H": "3*j*k", "Vb": "(k*a)*(k*a)*(3*j*k)/3", "Vs": "a*a*(3*j)/3", "Vv": "(k*a)*(k*a)*(3*j*k)/3 - a*a*(3*j)/3", "Hf": "3*j*k - 3*j"},
        constraints=["Vv <= 6000", "Vv != Vb", "A != H", "a != h", "A != h"],
        cost_values=["a", "A", "h", "H", "Vb", "Vs", "Vv"],
        relation="X - (A*A*H/3 - a*a*h/3)", unknown="X", answer_var="Vv",
        verify=["ans == Vb - Vs", "H == k*h", "A == k*a"],
        question="밑면은 한 변의 길이가 {A} cm인 정사각형이고 윗면은 한 변의 길이가 {a} cm인 정사각형인 사각뿔대가 있다. 이 사각뿔대는 높이가 {H} cm인 정사각뿔을 밑면에 평행한 평면으로 잘라 높이가 {h} cm인 작은 정사각뿔을 떼어 낸 것이다. 이 사각뿔대의 부피를 구하시오.",
        answer="{Vv}", answer_alt=["{Vv} cm³"],
        sol1="뿔대는 큰 뿔에서 작은 뿔을 잘라 낸 것이므로 (뿔대의 부피) = (큰 뿔의 부피) − (작은 뿔의 부피)다. 큰 뿔은 밑면 한 변 {A} cm·높이 {H} cm, 작은 뿔은 밑면 한 변 {a} cm·높이 {h} cm이고, 뿔의 부피는 (밑넓이) × (높이) ÷ 3이다. 뿔대의 높이 {Hf} cm를 그대로 쓰면 안 된다.",
        sol1_fig=steps(["뿔대 = 큰 뿔 − 작은 뿔", "큰 뿔: 밑면 {A} cm · 높이 {H} cm", "작은 뿔: 밑면 {a} cm · 높이 {h} cm"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "큰 뿔의 부피: {A} × {A} × {H} ÷ 3 = {Vb} (cm³)",
            "작은 뿔의 부피: {a} × {a} × {h} ÷ 3 = {Vs} (cm³)",
            "뿔대의 부피 = {Vb} − {Vs} = {Vv} (cm³)",
        ],
        sol2_fig=steps([
            {"text": "큰 뿔 = {A}² × {H} ÷ 3 = {Vb}", "hint": "밑넓이 × 높이 ÷ 3"},
            {"text": "작은 뿔 = {a}² × {h} ÷ 3 = {Vs}"},
            {"text": "뿔대 = {Vb} − {Vs} = {Vv} (cm³)", "marks": [{"on": "{Vv}", "note": "큰 뿔 − 작은 뿔"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("mark:2-0")]],
        sol_check="두 뿔의 닮음비가 {a} : {A} = 1 : {k}이므로 부피의 비는 1 : {k*k*k}이고, 작은 뿔 {Vs}의 {k*k*k}배가 큰 뿔 {Vb}{ika(Vb)} 맞다. 답: {Vv} cm³",
        model_answer="뿔대의 부피는 큰 뿔의 부피에서 작은 뿔의 부피를 뺀 것이다. 큰 뿔의 부피는 {A} × {A} × {H} ÷ 3 = {Vb} (cm³), 작은 뿔의 부피는 {a} × {a} × {h} ÷ 3 = {Vs} (cm³)이므로 뿔대의 부피는 {Vb} − {Vs} = {Vv} (cm³)이다.",
        rubric=[
            {"element": "방침", "points": 2, "criterion": "뿔대의 부피를 (큰 뿔) − (작은 뿔)로 구한다는 것을 밝혔다.", "partial": "뿔대의 높이 {Hf}{ro(Hf)} 기둥처럼 계산했으면 인정하지 않는다."},
            {"element": "두 뿔의 부피", "points": 3, "criterion": "큰 뿔 {Vb}, 작은 뿔 {Vs}{eul(Vs)} 각각 (밑넓이) × (높이) ÷ 3으로 구했다.", "partial": "한쪽만 옳거나 ÷ 3을 빠뜨렸으면 1점."},
            {"element": "뿔대의 부피", "points": 2, "criterion": "{Vb} − {Vs} = {Vv} (cm³)로 답했다.", "partial": "빼는 식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


def pp_t6():
    return tpl("m1-2-prism-pyramid", 6, PP,
        title="사각뿔 그릇의 물을 직육면체 그릇에 옮겼을 때의 높이",
        skill="물의 부피는 그대로 — (뿔의 부피) = (직육면체 밑넓이) × (물의 높이)",
        variant_axis={"구하는 것": "물의 높이", "그릇": "정사각뿔 → 직육면체", "수치": "정수 높이"},
        discriminates="뿔의 부피에 ⅓을 곱하고, 옮긴 뒤의 부피가 같음을 식으로 세우는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "m", "values": {"int": [2, 6]}}, {"name": "u", "values": {"int": [1, 4]}}, {"name": "v", "values": {"int": [1, 4]}}, {"name": "x", "values": {"int": [2, 15]}}],
        derive={"a": "3*m", "p": "m*u", "q": "m*v", "h": "u*v*x/3", "Vv": "a*a*h/3"},
        constraints=["h == floor(h)", "h >= 3", "h <= 20", "x != h", "x != a", "x != p", "x != q", "p*q != a*a", "p != q or u == v"],
        cost_values=["a", "h", "p", "q", "Vv", "x"],
        relation="p*q*X - a*a*h/3", unknown="X", answer_var="x",
        verify=["p*q*ans == Vv"],
        question="밑면이 한 변의 길이가 {a} cm인 정사각형이고 높이가 {h} cm인 사각뿔 모양의 그릇에 물을 가득 채운 뒤, 이 물을 밑면이 가로 {p} cm, 세로 {q} cm인 직사각형인 직육면체 모양의 빈 그릇에 모두 옮겨 담았다. 옮겨 담은 물의 높이를 구하시오. (단, 그릇의 두께는 생각하지 않는다.)",
        figure=solid("square_pyramid") + solid("rectangular_prism"),
        answer="{x}", answer_alt=["{x} cm"],
        sol1="물을 옮겨도 물의 부피는 변하지 않는다. 사각뿔 그릇에 가득 찬 물의 부피는 (밑넓이) × (높이) ÷ 3 = {a} × {a} × {h} ÷ 3이고, 직육면체 그릇에서는 (밑넓이) × (물의 높이) = {p} × {q} × (높이)다. 두 부피가 같다고 놓는다.",
        sol1_fig=solid("square_pyramid") + solid("rectangular_prism"),
        sol2=[
            "사각뿔 그릇의 물의 부피: {a} × {a} × {h} ÷ 3 = {Vv} (cm³)",
            "옮긴 물의 높이를 x cm라 하면 직육면체 그릇에서 부피는 {p} × {q} × x = {p*q}x (cm³)",
            "{p*q}x = {Vv}이므로 x = {Vv} ÷ {p*q} = {x}",
        ],
        sol2_fig=steps([
            {"text": "뿔의 물 = {a}² × {h} ÷ 3 = {Vv}", "hint": "뿔은 ÷ 3", "marks": [{"on": "{Vv}", "note": "물의 부피"}]},
            {"text": "{p} × {q} × x = {Vv}", "hint": "옮겨도 부피 같음"},
            {"text": "x = {Vv} ÷ {p*q} = {x} (cm)", "marks": [{"on": "{x}", "note": "높이"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="높이가 {x} cm이면 직육면체 그릇의 물의 부피는 {p} × {q} × {x} = {Vv} (cm³)로 뿔 그릇의 물의 부피와 같다. 뿔의 부피에서 ÷ 3을 빠뜨리면 높이가 {3*x} cm로 3배가 된다. 답: {x} cm",
        model_answer="사각뿔 그릇에 가득 찬 물의 부피는 {a} × {a} × {h} ÷ 3 = {Vv} (cm³)이다. 옮겨 담은 물의 높이를 x cm라 하면 직육면체 그릇에서 물의 부피는 {p} × {q} × x (cm³)이고, 옮겨도 부피는 같으므로 {p*q}x = {Vv}, x = {x}이다. 따라서 물의 높이는 {x} cm이다.",
        rubric=[
            {"element": "뿔의 부피", "points": 3, "criterion": "뿔 그릇의 물의 부피 {a} × {a} × {h} ÷ 3 = {Vv}{eul(Vv)} 구했다.", "partial": "÷ 3을 빠뜨렸으면 1점."},
            {"element": "식 세우기", "points": 2, "criterion": "부피가 같음을 이용해 {p} × {q} × x = {Vv}{eul(Vv)} 세웠다.", "partial": "직육면체의 부피 식이 틀렸으면 인정하지 않는다."},
            {"element": "높이 구하기", "points": 2, "criterion": "x = {Vv} ÷ {p*q} = {x} (cm)로 답했다.", "partial": "나눗셈 실수면 1점."},
        ],
    )


PRISM_SEED = {
    "seed_id": "m1-2-prism-pyramid", "category": "도형",
    "title": "각기둥·각뿔 — 삼각기둥 겉넓이·부피, 높이 역산, 정사각뿔 겉넓이, 뿔대 부피, 물 옮겨 담기",
    "unit_id": "m1-2", "concept_ids": ["m1-2-14", "m1-2-15"],
    "schema_id": SCHEMA_PRISM, "schema_name": "각기둥 부피 응용 / 각뿔의 부피 / 뿔대의 부피 / 그릇에 담긴 물의 부피",
    "source_item_ids": [],
    "note": "출판사 7.3~7.4 유형 차용. 밑면 직각삼각형은 피타고라스 수 8종(표), 뿔대는 큰 뿔 − 작은 뿔(닮음비 1:2·1:3, 높이 3의 배수), 물 옮기기는 정수 높이만. 뿔대·높이 역산은 그림 없음(D3 경고 예상). solid 는 치수 라벨이 없으므로 수치는 문면에.",
    "geometry": True,
    "templates": [pp_t1(), pp_t2(), pp_t3(), pp_t4(), pp_t5(), pp_t6()],
}


if __name__ == "__main__":
    with_pitfalls(POLY_SEED)
    dump(POLY_SEED)
    with_pitfalls(PRISM_SEED)
    dump(PRISM_SEED)
