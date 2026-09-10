# itemfactory/tools/mkseed_m1_plane2.py — 평면도형 시드 생성기 2: 정다각형 외각 · 호의 길이 비례 · 선분의 중점 (v1.0 · 2026-09-11)
#
#   python itemfactory/tools/mkseed_m1_plane2.py
#     → seeds/m1-2-polygon-exterior.json (5틀) · seeds/m1-2-arc-ratio.json (5틀) · seeds/m1-2-segment-mid.json (5틀)
#
# 정다각형: 한 외각 = 360/n 이 정수인 n(360의 약수)만 표 행으로. 호의 길이·넓이는 중심각에 비례 — 원 위의 점은 scene 좌표(cos·sin)로 실제로 그린다.
# 선분의 중점: 점을 한 직선(y = 0) 위에 실제 길이로 두고 aspect_min 으로 납작하게 그린다.
from __future__ import annotations

import math
import os
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402

SCHEMA_EXT = "58fa86e8-b3ea-491d-8eab-7f60bbc2ef8f"     # 정다각형의 내각과 외각
SCHEMA_ARC = "ba13e6dc-48aa-4e00-84b8-737982569489"     # 중심각의 크기와 호의 길이 비례
SCHEMA_MID = "4edd7671-5297-4b26-98b4-135ed1b94759"     # 선분의 등분점과 중점 관계

GEO = {"process": "절차수행", "context": "기하맥락", "points": 4, "time_limit": 80, "traps": ["구하는대상혼동", "역연산"]}


def tpl(seed_id, no, *bases, **kw):
    t = dict(GEO)
    for b in bases:
        t.update(b)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def scene(pts, segs, marks=None, circles=None, labels=None, nodot=None, aspect_min=None):
    a = {"pts": pts, "segs": segs}
    if marks:
        a["marks"] = marks
    if circles:
        a["circles"] = circles
    if labels:
        a["labels"] = labels
    if nodot:
        a["nodot"] = nodot
    if aspect_min is not None:
        a["aspect_min"] = aspect_min
    return [{"fn": "scene", "args": a}]


def arc(at, fr, to, label=None):
    d = {"at": at, "from": fr, "to": to}
    if label is not None:
        d["label"] = label
    return d


def polygon(n_expr="{min(n, 12)}"):
    return [{"fn": "polygon", "args": {"n": n_expr}}]


KPRE = {3: "삼", 4: "사", 5: "오", 6: "육", 8: "팔", 9: "구", 10: "십", 12: "십이", 15: "십오", 18: "십팔", 20: "이십", 24: "이십사", 30: "삼십", 36: "삼십육", 40: "사십", 45: "사십오", 60: "육십"}

# ═══════════════════════════════════════════════════════════════════ 1. 정다각형의 외각
EX = dict(prereq=["다각형의 외각의 크기의 합은 360°", "정다각형은 모든 내각(외각)의 크기가 같다", "한 꼭짓점에서 (내각) + (외각) = 180°"], ops=["각도", "방정식"], tags=["정다각형", "외각", "내각"])
N_ROWS = {str(n): {"KPRE": KPRE[n]} for n in KPRE}
ASK_EX = {
    "n": {"ASK": "변의 개수", "aN": 1, "aD": 0, "aI": 0, "aS": 0},
    "d": {"ASK": "대각선의 개수", "aN": 0, "aD": 1, "aI": 0, "aS": 0},
    "i": {"ASK": "한 내각의 크기", "aN": 0, "aD": 0, "aI": 1, "aS": 0},
    "s": {"ASK": "내각의 크기의 합", "aN": 0, "aD": 0, "aI": 0, "aS": 1},
}
DERIVE_N = {"ext": "360/n", "inn": "180 - 360/n", "dg": "n*(n - 3)/2", "sm": "180*(n - 2)"}
ANS_N = "aN*n + aD*n*(n - 3)/2 + aI*(180 - 360/n) + aS*180*(n - 2)"


def ex_t1():
    return tpl("m1-2-polygon-exterior", 1, EX,
        title="정n각형의 한 외각의 크기",
        skill="외각의 크기의 합 360°를 꼭짓점의 수 n으로 나눈다",
        variant_axis={"구하는 것": "한 외각", "n": "360의 약수 17종(그림은 12각형까지)"},
        discriminates="외각의 합이 n과 관계없이 360°임을 알고 n으로 나누는가(내각의 합 180(n−2)와 혼동하지 않는가)",
        qtype="short", difficulty=1, pool_target=300,
        params=[{"name": "n", "values": {"in": list(KPRE)}}],
        table={"key": "n", "rows": N_ROWS},
        derive=DERIVE_N,
        constraints=[],
        cost_values=["n", "ext"],
        relation="X*n - 360", unknown="X", answer_var="ext",
        verify=["ans*n == 360", "ans + inn == 180"],
        question="정{KPRE}각형의 한 외각의 크기를 구하시오.",
        figure=polygon(),
        answer="[[deg({ext})]]", answer_alt=["{ext}"],
        sol1="다각형의 외각의 크기의 합은 꼭짓점의 수와 관계없이 언제나 360°다. 정{KPRE}각형은 {n}개의 외각이 모두 같으므로 360°를 {n}으로 나누면 한 외각이 된다. 내각의 합 180° × ({n} − 2) = {sm}°와 헷갈리지 않는다.",
        sol1_fig=polygon(),
        sol2=[
            "외각의 크기의 합은 360°이고, 정{KPRE}각형의 외각 {n}개는 모두 같다",
            "한 외각 = 360° ÷ {n} = {ext}°",
        ],
        sol2_fig=steps([
            {"text": "외각의 합 = 360°", "hint": "n과 무관"},
            {"text": "한 외각 = 360° ÷ {n} = {ext}°", "marks": [{"on": "{ext}°", "note": "360 ÷ {n}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol_check="한 내각은 180° − {ext}° = {inn}°이고, 내각의 합 {inn}° × {n} = {sm}° = 180° × ({n} − 2)로 맞다. 답: [[deg({ext})]]",
        model_answer="다각형의 외각의 크기의 합은 360°이다. 정{KPRE}각형은 {n}개의 외각의 크기가 모두 같으므로 한 외각의 크기는 360° ÷ {n} = {ext}°이다.",
        rubric=[
            {"element": "외각의 합", "points": 2, "criterion": "외각의 크기의 합이 360°임을 밝혔다.", "partial": "내각의 합 {sm}°로 시작했으면 인정하지 않는다."},
            {"element": "한 외각 구하기", "points": 3, "criterion": "360° ÷ {n} = {ext}°로 구했다.", "partial": "나눗셈 실수면 1점."},
        ],
    )


def ex_t2():
    return tpl("m1-2-polygon-exterior", 2, EX,
        title="한 외각의 크기로 정다각형 정하기 — 변·대각선·내각·내각의 합",
        skill="n = 360 ÷ (한 외각) 으로 정다각형을 정한 뒤 구하는 것을 센다",
        variant_axis={"주어진 것": "한 외각", "구하는 것": "변·대각선·한 내각·내각의 합", "n": "360의 약수 17종"},
        discriminates="외각의 합 360°를 한 외각으로 나누어 n을 되돌리는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "n", "values": {"in": list(KPRE)}}, {"name": "ask", "values": {"in": list(ASK_EX)}}],
        table=[{"key": "n", "rows": N_ROWS}, {"key": "ask", "rows": ASK_EX}],
        derive={**DERIVE_N, "ans": ANS_N},
        constraints=["ans != ext", "n >= 4 or aD == 0"],
        cost_values=["n", "ext", "ans"],
        relation="X - ans", unknown="X", answer_var="ans",
        verify=["ext*n == 360", "ans == aN*n + aD*dg + aI*inn + aS*sm"],
        question="한 외각의 크기가 [[deg({ext})]]인 정다각형의 {ASK}{eul(ASK)} 구하시오.",
        answer="{ans}", answer_alt=["[[deg({ans})]]"],
        sol1="정다각형의 외각은 모두 같고 그 합은 360°이므로, 변의 개수를 n이라 하면 (한 외각) × n = 360°에서 n = 360 ÷ {ext} = {n}이다. 정{KPRE}각형임을 알면 대각선의 개수 n(n − 3)/2, 한 내각 180° − (외각), 내각의 합 180° × (n − 2)는 모두 n에서 나온다.",
        sol1_fig=steps(["(한 외각) × n = 360°", "n = 360 ÷ {ext} = {n}  → 정{KPRE}각형"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "변의 개수를 n이라 하면 외각의 합이 360°이므로 {ext}° × n = 360°, n = {n}",
            "즉 정{KPRE}각형이다 — 대각선 {n} × ({n} − 3) ÷ 2 = {dg}(개), 한 내각 180° − {ext}° = {inn}°, 내각의 합 180° × ({n} − 2) = {sm}°",
            "따라서 {ASK}{eun(ASK)} {ans}",
        ],
        sol2_fig=steps([
            {"text": "{ext}° × n = 360° → n = {n}", "hint": "외각의 합 360°", "marks": [{"on": "{n}", "note": "정{KPRE}각형"}]},
            {"text": "대각선 {dg} · 한 내각 {inn}° · 내각의 합 {sm}°"},
            {"text": "{ASK} = {ans}", "marks": [{"on": "{ans}", "note": "{ASK}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1)], [reveal(2), hl("mark:2-0")]],
        sol_check="정{KPRE}각형의 한 외각은 360° ÷ {n} = {ext}°로 조건과 같다. 답: {ans}",
        model_answer="변의 개수를 n이라 하면 외각의 크기의 합은 360°이므로 {ext}° × n = 360°에서 n = {n}, 즉 정{KPRE}각형이다. 따라서 {ASK}{eun(ASK)} {ans}이다.",
        rubric=[
            {"element": "n 구하기", "points": 3, "criterion": "외각의 합 360°를 이용해 n = 360 ÷ {ext} = {n}{eul(n)} 구했다.", "partial": "식은 옳으나 나눗셈이 틀렸으면 1점."},
            {"element": "구하는 값", "points": 2, "criterion": "정{KPRE}각형의 {ASK}{eul(ASK)} {ans}{ro(ans)} 구했다.", "partial": "n은 맞으나 공식 적용이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}{ro(ans)} 답했다.", "partial": "n의 값 {n}{eul(n)} 답했으면 인정하지 않는다."},
        ],
    )


def _ratio_rows():
    rows = {}
    for n in KPRE:
        ext = Fraction(360, n); inn = 180 - ext
        g = math.gcd(int(inn), int(ext))
        rows[str(n)] = {"KPRE": KPRE[n], "ra": int(inn) // g, "rb": int(ext) // g}
    return rows


RATIO_ROWS = _ratio_rows()
ASK_EX3 = {k: v for k, v in ASK_EX.items() if k != "s"}
ASK_EX3["e"] = {"ASK": "한 외각의 크기", "aN": 0, "aD": 0, "aI": 0, "aS": 0}


def ex_t3():
    return tpl("m1-2-polygon-exterior", 3, EX,
        title="내각과 외각의 크기의 비로 정다각형 정하기",
        skill="(내각) + (외각) = 180° 를 비로 나누어 한 외각을 구하고, n = 360 ÷ (한 외각)",
        variant_axis={"주어진 것": "내각 : 외각", "구하는 것": "변·대각선·한 내각·한 외각", "n": "360의 약수 17종"},
        discriminates="한 꼭짓점에서 내각과 외각의 합이 180°임을 비례배분에 쓰는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "n", "values": {"in": list(KPRE)}}, {"name": "ask", "values": {"in": list(ASK_EX3)}}],
        table=[{"key": "n", "rows": RATIO_ROWS}, {"key": "ask", "rows": ASK_EX3}],
        derive={**DERIVE_N, "ans": ANS_N + " + (1 - aN - aD - aI)*(360/n)"},
        constraints=["n >= 4 or aD == 0", "ans != ra", "ans != rb"],
        cost_values=["n", "ra", "rb", "ext", "ans"],
        relation="X - ans", unknown="X", answer_var="ans",
        verify=["inn*rb == ext*ra", "ext*n == 360"],
        question="한 내각의 크기와 한 외각의 크기의 비가 {ra} : {rb}인 정다각형의 {ASK}{eul(ASK)} 구하시오.",
        answer="{ans}", answer_alt=["[[deg({ans})]]"],
        sol1="한 꼭짓점에서 내각과 외각은 이웃하여 평각을 이루므로 그 합은 180°다. 비가 {ra} : {rb}이므로 한 외각은 180° ÷ ({ra} + {rb}) × {rb} = {ext}°이다. 외각의 합은 360°이므로 n = 360 ÷ {ext} = {n}, 정{KPRE}각형이다.",
        sol1_fig=steps(["(내각) + (외각) = 180°", "외각 = 180° × [[frac({rb}, {ra + rb})]] = {ext}°", "n = 360 ÷ {ext} = {n}"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "(내각) + (외각) = 180°이고 비가 {ra} : {rb}이므로 한 외각 = 180° ÷ {ra + rb} × {rb} = {ext}°",
            "외각의 합이 360°이므로 n = 360 ÷ {ext} = {n} — 정{KPRE}각형",
            "한 내각 180° − {ext}° = {inn}°, 대각선 {n} × ({n} − 3) ÷ 2 = {dg}(개)",
            "따라서 {ASK}{eun(ASK)} {ans}",
        ],
        sol2_fig=steps([
            {"text": "외각 = 180° ÷ {ra + rb} × {rb} = {ext}°", "hint": "합 180°를 비로 나눔", "marks": [{"on": "{ext}°", "note": "외각"}]},
            {"text": "n = 360 ÷ {ext} = {n}", "hint": "외각의 합 360°", "marks": [{"on": "{n}", "note": "정{KPRE}각형"}]},
            {"text": "한 내각 {inn}° · 대각선 {dg}"},
            {"text": "{ASK} = {ans}", "marks": [{"on": "{ans}", "note": "{ASK}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)], [reveal(3), hl("mark:3-0")]],
        sol_check="정{KPRE}각형의 한 내각 {inn}°와 한 외각 {ext}°의 비는 {inn} : {ext} = {ra} : {rb}로 조건과 같다. 답: {ans}",
        model_answer="한 꼭짓점에서 (내각) + (외각) = 180°이고 그 비가 {ra} : {rb}이므로 한 외각은 180° ÷ {ra + rb} × {rb} = {ext}°이다. 외각의 합은 360°이므로 n = 360 ÷ {ext} = {n}, 즉 정{KPRE}각형이다. 따라서 {ASK}{eun(ASK)} {ans}이다.",
        rubric=[
            {"element": "외각 구하기", "points": 3, "criterion": "(내각) + (외각) = 180°를 비 {ra} : {rb}로 나누어 한 외각 {ext}°를 구했다.", "partial": "360°를 비로 나누었으면 인정하지 않고, 비례배분 계산 실수면 1점."},
            {"element": "n 구하기", "points": 2, "criterion": "n = 360 ÷ {ext} = {n}({KPRE}각형)임을 구했다.", "partial": "나눗셈 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK}{eul(ASK)} {ans}{ro(ans)} 답했다.", "partial": "n의 값을 답했으면 인정하지 않는다."},
        ],
    )


def ex_t4():
    return tpl("m1-2-polygon-exterior", 4, EX,
        title="오각형의 외각의 크기의 합으로 x 구하기",
        skill="외각의 크기의 합은 360° — 주어진 네 외각을 더해 360°에서 뺀다",
        variant_axis={"구하는 것": "미지 외각 x", "다각형": "오각형", "각": "5° 단위"},
        discriminates="외각의 합이 360°임을 쓰는가(내각의 합 540°와 혼동하지 않는가)",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "a1", "values": {"step": [40, 110, 5]}}, {"name": "a2", "values": {"step": [40, 110, 5]}}, {"name": "a3", "values": {"step": [40, 110, 5]}}, {"name": "a4", "values": {"step": [40, 110, 5]}}],
        derive={"S4": "a1 + a2 + a3 + a4", "x": "360 - a1 - a2 - a3 - a4"},
        constraints=["x >= 30", "x <= 120", "x != a1", "x != a2", "x != a3", "x != a4", "a1 != a2", "a2 != a3", "a3 != a4", "a1 != a4"],
        cost_values=["a1", "a2", "a3", "a4", "x"],
        relation="X + a1 + a2 + a3 + a4 - 360", unknown="X", answer_var="x",
        verify=["ans + S4 == 360", "ans > 0"],
        question="오각형의 다섯 외각의 크기가 각각 [[deg({a1})]], [[deg({a2})]], [[deg({a3})]], [[deg({a4})]], x°일 때, x의 값을 구하시오.",
        figure=polygon("{5}"),
        answer="{x}", answer_alt=["[[deg({x})]]"],
        sol1="다각형의 외각의 크기의 합은 변의 개수와 관계없이 360°다(오각형의 내각의 합 540°와 다르다). 네 외각을 더한 뒤 360°에서 빼면 x가 나온다.",
        sol1_fig=polygon("{5}"),
        sol2=[
            "오각형의 외각의 크기의 합은 360°이므로 {a1} + {a2} + {a3} + {a4} + x = 360",
            "주어진 네 외각의 합은 {a1} + {a2} + {a3} + {a4} = {S4}",
            "따라서 x = 360 − {S4} = {x}",
        ],
        sol2_fig=steps([
            {"text": "{a1} + {a2} + {a3} + {a4} + x = 360", "hint": "외각의 합 360°"},
            {"text": "{S4} + x = 360"},
            {"text": "x = 360 − {S4} = {x}", "marks": [{"on": "{x}", "note": "360 − {S4}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("mark:2-0")]],
        sol_check="다섯 외각을 더하면 {S4} + {x} = 360으로 외각의 합과 같다. 답: {x}",
        model_answer="다각형의 외각의 크기의 합은 360°이므로 {a1} + {a2} + {a3} + {a4} + x = 360이다. {S4} + x = 360에서 x = {x}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "외각의 합이 360°임을 이용해 {a1} + {a2} + {a3} + {a4} + x = 360을 세웠다.", "partial": "내각의 합 540°로 세웠으면 인정하지 않는다."},
            {"element": "x 구하기", "points": 2, "criterion": "x = 360 − {S4} = {x}{eul(x)} 구했다.", "partial": "덧셈·뺄셈 실수면 1점."},
        ],
    )


INN_ROWS = {str(n): {"KPRE": KPRE[n]} for n in KPRE if n >= 4}     # 한 내각이 정수: 360의 약수 n 전부지만 삼각형(60°)은 외각과 겹쳐 제외
ASK_EX5 = {"n": ASK_EX["n"], "d": ASK_EX["d"], "e": {"ASK": "한 외각의 크기", "aN": 0, "aD": 0, "aI": 0, "aS": 0}}


def ex_t5():
    return tpl("m1-2-polygon-exterior", 5, EX,
        title="한 내각의 크기로 정다각형 정하기 — 외각으로 바꿔서",
        skill="한 외각 = 180° − (한 내각), n = 360 ÷ (한 외각) — 내각의 합 공식보다 빠르다",
        variant_axis={"주어진 것": "한 내각", "구하는 것": "변·대각선·한 외각", "n": "360의 약수(4 이상)"},
        discriminates="내각을 외각으로 바꿔 360°를 나누는 경로를 쓰는가(또는 180(n−2)/n = 내각 방정식을 푸는가)",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "n", "values": {"in": [int(k) for k in INN_ROWS]}}, {"name": "ask", "values": {"in": list(ASK_EX5)}}],
        table=[{"key": "n", "rows": INN_ROWS}, {"key": "ask", "rows": ASK_EX5}],
        derive={**DERIVE_N, "ans": ANS_N + " + (1 - aN - aD - aI)*(360/n)"},
        constraints=["ans != inn"],
        cost_values=["n", "inn", "ext", "ans"],
        relation="X - ans", unknown="X", answer_var="ans",
        verify=["inn + ext == 180", "ext*n == 360"],
        question="한 내각의 크기가 [[deg({inn})]]인 정다각형의 {ASK}{eul(ASK)} 구하시오.",
        answer="{ans}", answer_alt=["[[deg({ans})]]"],
        sol1="한 꼭짓점에서 (내각) + (외각) = 180°이므로 한 외각은 180° − {inn}° = {ext}°다. 외각의 합은 360°이므로 n = 360 ÷ {ext} = {n}, 정{KPRE}각형이다. 내각의 합 공식으로 180(n − 2)/n = {inn}{eul(inn)} 풀어도 같은 n이 나오지만, 외각으로 바꾸는 쪽이 빠르다.",
        sol1_fig=steps(["외각 = 180° − {inn}° = {ext}°", "n = 360 ÷ {ext} = {n}  → 정{KPRE}각형"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "한 외각 = 180° − {inn}° = {ext}°",
            "외각의 합이 360°이므로 n = 360 ÷ {ext} = {n} — 정{KPRE}각형",
            "대각선 {n} × ({n} − 3) ÷ 2 = {dg}(개)",
            "따라서 {ASK}{eun(ASK)} {ans}",
        ],
        sol2_fig=steps([
            {"text": "외각 = 180° − {inn}° = {ext}°", "hint": "내각 + 외각 = 180°", "marks": [{"on": "{ext}°", "note": "외각"}]},
            {"text": "n = 360 ÷ {ext} = {n}", "hint": "외각의 합 360°", "marks": [{"on": "{n}", "note": "정{KPRE}각형"}]},
            {"text": "대각선 {dg}"},
            {"text": "{ASK} = {ans}", "marks": [{"on": "{ans}", "note": "{ASK}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)], [reveal(3), hl("mark:3-0")]],
        sol_check="정{KPRE}각형의 한 내각은 180° × ({n} − 2) ÷ {n} = {inn}°로 조건과 같다. 답: {ans}",
        model_answer="한 외각의 크기는 180° − {inn}° = {ext}°이고, 외각의 합은 360°이므로 n = 360 ÷ {ext} = {n}, 즉 정{KPRE}각형이다. 따라서 {ASK}{eun(ASK)} {ans}이다.",
        rubric=[
            {"element": "외각 구하기", "points": 2, "criterion": "한 외각 180° − {inn}° = {ext}°를 구했다(또는 내각의 합 식을 세웠다).", "partial": "내각·외각의 관계를 잘못 썼으면 인정하지 않는다."},
            {"element": "n 구하기", "points": 3, "criterion": "n = 360 ÷ {ext} = {n}({KPRE}각형)임을 구했다.", "partial": "식은 옳으나 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK}{eul(ASK)} {ans}{ro(ans)} 답했다.", "partial": "n의 값을 답했으면 인정하지 않는다."},
        ],
    )


EXT_SEED = {
    "seed_id": "m1-2-polygon-exterior", "category": "도형",
    "title": "정다각형의 외각 — 한 외각·외각→n·내각:외각 비·외각의 합·내각→n",
    "unit_id": "m1-2", "concept_ids": ["m1-2-09"],
    "schema_id": SCHEMA_EXT, "schema_name": "정다각형의 내각과 외각 / 다각형 외각의 합 응용",
    "source_item_ids": [],
    "note": "출판사 6.3~6.4 유형(정n각형 한 외각·외각→변·대각선·내각:외각 비·외각 합 x·내각→n) 차용. n은 360의 약수 17종(표), 비는 기약 정수비로 굽는다. 기존 m1-2-polygon-angles(내각 합·한 내각)와 겹치지 않게 외각 축만.",
    "geometry": True,
    "templates": [ex_t1(), ex_t2(), ex_t3(), ex_t4(), ex_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 호의 길이와 중심각의 비례
AR = dict(prereq=["한 원에서 호의 길이는 중심각의 크기에 정비례한다", "비례식"], ops=["비례", "각도"], tags=["부채꼴", "호의 길이", "중심각"])
R = 4
LAY = {"1": {"al": 15, "gp": 40}, "2": {"al": 40, "gp": 30}, "3": {"al": 60, "gp": 50}, "4": {"al": 100, "gp": 35}}


def circle_pts(names_angles):
    """이름 → 원 위 좌표(각도식). names_angles = {"A": "al", "B": "al + t1", …} (각도는 도 단위 식)."""
    pts = {"O": [0, 0]}
    for nm, ex in names_angles.items():
        pts[nm] = [f"{{{R}*cos(pi*({ex})/180)}}", f"{{{R}*sin(pi*({ex})/180)}}"]
    return pts


def arc_label(ex_mid, text, k=None):
    d = {"at": [f"{{{R + 0.9}*cos(pi*({ex_mid})/180)}}", f"{{{R + 0.9}*sin(pi*({ex_mid})/180)}}"], "text": text, "accent": True}
    if k:
        d["k"] = k
    return d


TWO_ARCS = dict(A="al", B="al + t1", C="al + t1 + gp", D="al + t1 + gp + t2")
TWO_SEGS = [["O", "A"], ["O", "B"], ["O", "C"], ["O", "D"]]
TWO_CIRC = [{"c": "O", "r": R}]


def ar_t1():
    return tpl("m1-2-arc-ratio", 1, AR,
        title="두 호의 길이와 한 중심각으로 다른 중심각 구하기",
        skill="호의 길이는 중심각에 정비례 — (호 AB) : (호 CD) = ∠AOB : ∠COD 의 비례식",
        variant_axis={"구하는 것": "중심각", "주어진 것": "두 호의 길이·한 중심각", "배치": "4가지"},
        discriminates="비례식을 호의 길이와 중심각을 같은 순서로 세우는가(역비례로 두지 않는가)",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "ly", "values": {"in": list(LAY)}}, {"name": "t1", "values": {"in": [30, 40, 45, 60, 72, 90, 100, 120]}}, {"name": "x", "values": {"in": [20, 30, 40, 45, 50, 60, 75, 80, 90, 100, 120, 135, 150]}}, {"name": "m", "values": {"int": [1, 4]}}],
        table={"key": "ly", "rows": LAY},
        derive={"g": "gcd(t1, x)", "l1": "m*t1/gcd(t1, x)", "l2": "m*x/gcd(t1, x)", "t2": "x"},
        constraints=["x != t1", "al + t1 + gp + x <= 330", "l1 != l2", "x != l1", "x != l2", "l1 != t1", "l2 <= 40", "l1 >= 2"],
        cost_values=["t1", "l1", "l2", "x"],
        relation="X*l1 - t1*l2", unknown="X", answer_var="x",
        verify=["ans*l1 == t1*l2", "ans > 0", "ans < 180"],
        question="다음 그림의 원 O에서 [[arc(AB)]] = {l1} cm, [[arc(CD)]] = {l2} cm이고 [[angle(AOB)]] = [[deg({t1})]]일 때, [[angle(COD)]]의 크기를 구하시오.",
        figure=scene(circle_pts(TWO_ARCS), TWO_SEGS, circles=TWO_CIRC,
                     marks={"arc": [arc("O", "A", "B", "{t1}°"), arc("O", "C", "D", "x")]},
                     labels=[arc_label("al + t1/2", "{l1} cm"), arc_label("al + t1 + gp + t2/2", "{l2} cm")]),
        answer="[[deg({x})]]", answer_alt=["{x}"],
        sol1="한 원에서 부채꼴의 호의 길이는 중심각의 크기에 정비례한다. 호 AB와 호 CD의 길이의 비가 {l1} : {l2}이므로 두 중심각의 비도 {l1} : {l2}다. ∠COD를 x°로 두고 (호의 길이의 비) = (중심각의 비)로 비례식을 세운다 — 순서를 같게 맞추는 것이 핵심이다.",
        sol1_fig=scene(circle_pts(TWO_ARCS), TWO_SEGS, circles=TWO_CIRC,
                       marks={"arc": [arc("O", "A", "B", "{t1}°"), arc("O", "C", "D", "x")]},
                       labels=[arc_label("al + t1/2", "{l1} cm"), arc_label("al + t1 + gp + t2/2", "{l2} cm")]),
        sol1_anim=[[hl("arc:O", "label:0")], [hl("label:1", keep=True)]],
        sol2=[
            "∠COD = x°라 하면 호의 길이는 중심각에 정비례하므로 {l1} : {l2} = {t1} : x",
            "비례식에서 {l1} × x = {l2} × {t1} = {l2*t1}",
            "따라서 x = {dv(l2*t1, l1)}",
        ],
        sol2_fig=steps([
            {"text": "{l1} : {l2} = {t1} : x", "hint": "호 : 호 = 각 : 각 (같은 순서)"},
            {"text": "{co(l1)}x = {l2*t1}", "hint": "외항의 곱 = 내항의 곱"},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{l2*t1} ÷ {l1}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="호 1 cm당 중심각은 {t1} ÷ {l1} = {dec(t1/l1)}°이고, {l2} cm이면 {dec(t1/l1)}° × {l2} = {x}°로 같다. 답: [[deg({x})]]",
        model_answer="한 원에서 호의 길이는 중심각의 크기에 정비례하므로 ∠COD = x°라 하면 {l1} : {l2} = {t1} : x이다. {co(l1)}x = {l2*t1}에서 x = {x}이므로 ∠COD = {x}°이다.",
        rubric=[
            {"element": "비례식 세우기", "points": 3, "criterion": "호의 길이가 중심각에 정비례함을 밝히고 {l1} : {l2} = {t1} : x{eul(x)} 세웠다.", "partial": "비례 관계는 적었으나 순서가 뒤바뀐 비례식은 인정하지 않는다."},
            {"element": "해 구하기", "points": 2, "criterion": "{co(l1)}x = {l2*t1}에서 x = {x}{eul(x)} 구했다.", "partial": "계산 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠COD = {x}°로 답했다.", "partial": "다른 값을 답했으면 인정하지 않는다."},
        ],
    )


def ar_t2():
    return tpl("m1-2-arc-ratio", 2, AR,
        title="한 호의 길이와 두 중심각으로 다른 호의 길이 구하기",
        skill="(호 AB) : (호 CD) = ∠AOB : ∠COD — 호의 길이를 미지수로",
        variant_axis={"구하는 것": "호의 길이", "주어진 것": "한 호의 길이·두 중심각", "배치": "4가지"},
        discriminates="구하는 호의 길이를 미지수로 두고 같은 순서로 비례식을 세우는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "ly", "values": {"in": list(LAY)}}, {"name": "t1", "values": {"in": [30, 40, 45, 60, 72, 90, 100, 120]}}, {"name": "t2", "values": {"in": [20, 30, 40, 45, 50, 60, 75, 80, 90, 100, 120, 135, 150]}}, {"name": "m", "values": {"int": [1, 4]}}],
        table={"key": "ly", "rows": LAY},
        derive={"g": "gcd(t1, t2)", "l1": "m*t1/gcd(t1, t2)", "l2": "m*t2/gcd(t1, t2)"},
        constraints=["t1 != t2", "al + t1 + gp + t2 <= 330", "l1 != l2", "l2 != t1", "l2 != t2", "l1 != t1", "l2 <= 40", "l1 >= 2"],
        cost_values=["t1", "t2", "l1", "l2"],
        relation="X*t1 - l1*t2", unknown="X", answer_var="l2",
        verify=["ans*t1 == l1*t2", "ans > 0"],
        question="다음 그림의 원 O에서 [[arc(AB)]] = {l1} cm이고 [[angle(AOB)]] = [[deg({t1})]], [[angle(COD)]] = [[deg({t2})]]일 때, [[arc(CD)]]의 길이를 구하시오.",
        figure=scene(circle_pts(TWO_ARCS), TWO_SEGS, circles=TWO_CIRC,
                     marks={"arc": [arc("O", "A", "B", "{t1}°"), arc("O", "C", "D", "{t2}°")]},
                     labels=[arc_label("al + t1/2", "{l1} cm"), arc_label("al + t1 + gp + t2/2", "x cm")]),
        answer="{l2}", answer_alt=["{l2} cm"],
        sol1="한 원에서 호의 길이는 중심각의 크기에 정비례한다. 중심각의 비가 {t1} : {t2}이므로 호의 길이의 비도 {t1} : {t2}다. 호 CD의 길이를 x cm로 두고 (호의 길이의 비) = (중심각의 비)로 세운다.",
        sol1_fig=scene(circle_pts(TWO_ARCS), TWO_SEGS, circles=TWO_CIRC,
                       marks={"arc": [arc("O", "A", "B", "{t1}°"), arc("O", "C", "D", "{t2}°")]},
                       labels=[arc_label("al + t1/2", "{l1} cm"), arc_label("al + t1 + gp + t2/2", "x cm")]),
        sol1_anim=[[hl("arc:O", "label:0")], [hl("label:1", keep=True)]],
        sol2=[
            "호 CD의 길이를 x cm라 하면 {l1} : x = {t1} : {t2}",
            "비례식에서 {t1} × x = {l1} × {t2} = {l1*t2}",
            "따라서 x = {dv(l1*t2, t1)}",
        ],
        sol2_fig=steps([
            {"text": "{l1} : x = {t1} : {t2}", "hint": "호 : 호 = 각 : 각"},
            {"text": "{t1}x = {l1*t2}", "hint": "외항의 곱 = 내항의 곱"},
            {"text": "x = {l2}", "marks": [{"on": "{l2}", "note": "{l1*t2} ÷ {t1}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="중심각 1°당 호의 길이는 {l1} ÷ {t1} = {dec(l1/t1)} cm이고, {t2}°이면 {dec(l1/t1)} × {t2} = {l2} (cm)로 같다. 답: {l2} cm",
        model_answer="한 원에서 호의 길이는 중심각의 크기에 정비례하므로 호 CD의 길이를 x cm라 하면 {l1} : x = {t1} : {t2}이다. {t1}x = {l1*t2}에서 x = {l2}이므로 호 CD의 길이는 {l2} cm이다.",
        rubric=[
            {"element": "비례식 세우기", "points": 3, "criterion": "호의 길이가 중심각에 정비례함을 밝히고 {l1} : x = {t1} : {t2}{eul(t2)} 세웠다.", "partial": "순서가 뒤바뀐 비례식은 인정하지 않는다."},
            {"element": "해 구하기", "points": 2, "criterion": "{t1}x = {l1*t2}에서 x = {l2}{eul(l2)} 구했다.", "partial": "계산 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "호 CD의 길이 {l2} cm로 답했다.", "partial": "다른 값을 답했으면 인정하지 않는다."},
        ],
    )


def _diam_rows():
    rows = {}
    for a in range(1, 14):
        for b in range(1, 14):
            if math.gcd(a, b) != 1:
                continue
            t = Fraction(180 * a, a + b)
            if t.denominator == 1 and 18 <= t <= 162:
                rows[f"{a}-{b}"] = {"ra": a, "rb": b}
    return rows


DIAM_ROWS = _diam_rows()
ASK_DIAM = {"1": {"ASKA": "AOC", "wA": 1, "LA": "x", "LB": " "}, "2": {"ASKA": "COB", "wA": 0, "LA": " ", "LB": "x"}}


def ar_t3():
    return tpl("m1-2-arc-ratio", 3, AR,
        title="지름 AB 위의 점 — 호의 길이의 비로 중심각 구하기",
        skill="지름이 만드는 중심각은 180° — 호 AC : 호 CB = ∠AOC : ∠COB 로 180°를 비례배분",
        variant_axis={"구하는 것": "중심각", "주어진 것": "두 호의 비(지름)", "비": "기약 정수비"},
        discriminates="지름의 중심각이 180°임을 알고 비례배분하는가(360°로 배분하지 않는가)",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "rt", "values": {"in": list(DIAM_ROWS)}}, {"name": "ask", "values": {"in": [1, 2]}}],
        table=[{"key": "rt", "rows": DIAM_ROWS}, {"key": "ask", "rows": ASK_DIAM}],
        derive={"x": "180*ra/(ra + rb)", "y": "180*rb/(ra + rb)", "cx": "-4*cos(pi*x/180)", "cy": "4*sin(pi*x/180)", "ans": "wA*180*ra/(ra + rb) + (1 - wA)*180*rb/(ra + rb)", "oth": "180 - ans", "pw": "wA*ra + (1 - wA)*rb"},
        constraints=["x != ra", "x != rb", "x != y"],
        cost_values=["ra", "rb", "ans"],
        relation="X*(ra + rb) - 180*pw", unknown="X", answer_var="ans",
        verify=["ans*(ra + rb) == 180*pw", "x + y == 180"],
        question="다음 그림에서 [[seg(AB)]]는 원 O의 지름이고 [[arc(AC)]] : [[arc(CB)]] = {ra} : {rb}일 때, [[angle({ASKA})]]의 크기를 구하시오.",
        figure=scene({"O": [0, 0], "A": [-4, 0], "B": [4, 0], "C": ["{cx}", "{cy}"]}, [["A", "B"], ["O", "C"]], circles=TWO_CIRC,
                     marks={"arc": [arc("O", "A", "C", "{LA}"), arc("O", "C", "B", "{LB}")]}),
        answer="[[deg({ans})]]", answer_alt=["{ans}"],
        sol1="AB가 지름이므로 호 AC와 호 CB를 합치면 반원이고, 두 호의 중심각을 더하면 ∠AOB = 180°다. 호의 길이는 중심각에 정비례하므로 ∠AOC : ∠COB = {ra} : {rb}이고, 180°를 {ra} : {rb}로 비례배분하면 두 각이 모두 나온다. 360°가 아니라 180°를 나눈다.",
        sol1_fig=scene({"O": [0, 0], "A": [-4, 0], "B": [4, 0], "C": ["{cx}", "{cy}"]}, [["A", "B"], ["O", "C"]], circles=TWO_CIRC,
                       marks={"arc": [arc("O", "A", "C", "x"), arc("O", "C", "B", "{y}°")]}),
        sol1_anim=[[hl("seg:A-B")], [hl("arc:O", keep=True)]],
        sol2=[
            "AB가 지름이므로 ∠AOC + ∠COB = 180°",
            "호의 길이는 중심각에 정비례하므로 ∠AOC : ∠COB = {ra} : {rb}",
            "∠{ASKA} = 180° ÷ ({ra} + {rb}) × {pw} = 180° × [[frac({pw}, {ra + rb})]] = {ans}°",
        ],
        sol2_fig=steps([
            {"text": "∠AOC + ∠COB = 180°", "hint": "지름 → 반원"},
            {"text": "∠AOC : ∠COB = {ra} : {rb}", "hint": "호의 비 = 각의 비"},
            {"text": "∠{ASKA} = 180° ÷ {ra + rb} × {pw} = {ans}°", "marks": [{"on": "{ans}°", "note": "비례배분"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="다른 한 각은 180° − {ans}° = {oth}°이고 {x} : {y} = {ra} : {rb}로 호의 비와 같다. 답: [[deg({ans})]]",
        model_answer="AB가 원 O의 지름이므로 ∠AOC + ∠COB = 180°이다. 한 원에서 호의 길이는 중심각의 크기에 정비례하므로 ∠AOC : ∠COB = {ra} : {rb}이고, 따라서 ∠{ASKA} = 180° ÷ ({ra} + {rb}) × {pw} = {ans}°이다.",
        rubric=[
            {"element": "반원 읽기", "points": 2, "criterion": "AB가 지름이므로 ∠AOC + ∠COB = 180°임을 밝혔다.", "partial": "360°로 두었으면 인정하지 않는다."},
            {"element": "비례배분", "points": 3, "criterion": "호의 비 {ra} : {rb}가 중심각의 비임을 쓰고 180° ÷ {ra + rb} × {pw} = {ans}°를 구했다.", "partial": "비는 세웠으나 배분 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{ASKA} = {ans}°로 답했다.", "partial": "다른 한 각 {oth}°를 답했으면 인정하지 않는다."},
        ],
    )


def _tri_rows():
    rows = {}
    for a in range(1, 10):
        for b in range(a, 10):
            for c in range(b, 10):
                s = a + b + c
                if math.gcd(math.gcd(a, b), c) != 1:
                    continue
                if all(Fraction(360 * v, s).denominator == 1 for v in (a, b, c)) and 360 * a / s >= 24 and 360 * c / s <= 150:
                    for k, (p, q, r) in enumerate([(a, b, c), (b, c, a), (c, a, b)]):
                        rows[f"{a}-{b}-{c}-{k}"] = {"pa": p, "pb": q, "pc": r}
    return rows


TRI_ROWS = _tri_rows()
ASK_TRI = {"1": {"ASKA": "AOB", "w1": 1, "w2": 0, "w3": 0}, "2": {"ASKA": "BOC", "w1": 0, "w2": 1, "w3": 0}, "3": {"ASKA": "COA", "w1": 0, "w2": 0, "w3": 1}}


def ar_t4():
    return tpl("m1-2-arc-ratio", 4, AR,
        title="원 위의 세 점 — 세 호의 길이의 비로 중심각 구하기",
        skill="세 호를 합치면 원 전체(360°) — 호의 비로 360°를 비례배분",
        variant_axis={"구하는 것": "∠AOB·∠BOC·∠COA", "주어진 것": "세 호의 비", "비": "정수비"},
        discriminates="세 호의 중심각의 합이 360°임을 쓰고 구하는 각에 해당하는 항을 고르는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "tr", "values": {"in": list(TRI_ROWS)}}, {"name": "ask", "values": {"in": list(ASK_TRI)}}],
        table=[{"key": "tr", "rows": TRI_ROWS}, {"key": "ask", "rows": ASK_TRI}],
        derive={"ss": "pa + pb + pc", "ta": "360*pa/(pa + pb + pc)", "tb": "360*pb/(pa + pb + pc)", "tc": "360*pc/(pa + pb + pc)",
                "x": "w1*360*pa/(pa + pb + pc) + w2*360*pb/(pa + pb + pc) + w3*360*pc/(pa + pb + pc)", "pw": "w1*pa + w2*pb + w3*pc"},
        constraints=["x != pa", "x != pb", "x != pc"],
        cost_values=["pa", "pb", "pc", "x"],
        relation="X*(pa + pb + pc) - 360*pw", unknown="X", answer_var="x",
        verify=["ans*ss == 360*pw", "ta + tb + tc == 360"],
        question="다음 그림과 같이 원 O 위에 세 점 A, B, C가 있다. [[arc(AB)]] : [[arc(BC)]] : [[arc(CA)]] = {pa} : {pb} : {pc}일 때, [[angle({ASKA})]]의 크기를 구하시오.",
        figure=scene(circle_pts({"A": "20", "B": "20 + ta", "C": "20 + ta + tb"}), [["O", "A"], ["O", "B"], ["O", "C"]], circles=TWO_CIRC,
                     labels=[{"at": [f"{{{R + 0.9}*cos(pi*(20 + ta/2)/180)}}", f"{{{R + 0.9}*sin(pi*(20 + ta/2)/180)}}"], "text": "{pa}", "accent": True},
                             {"at": [f"{{{R + 0.9}*cos(pi*(20 + ta + tb/2)/180)}}", f"{{{R + 0.9}*sin(pi*(20 + ta + tb/2)/180)}}"], "text": "{pb}", "accent": True},
                             {"at": [f"{{{R + 0.9}*cos(pi*(20 + ta + tb + tc/2)/180)}}", f"{{{R + 0.9}*sin(pi*(20 + ta + tb + tc/2)/180)}}"], "text": "{pc}", "accent": True}]),
        answer="[[deg({x})]]", answer_alt=["{x}"],
        sol1="세 호 AB, BC, CA를 합치면 원 전체이므로 세 중심각의 합은 360°다. 호의 길이는 중심각에 정비례하므로 ∠AOB : ∠BOC : ∠COA = {pa} : {pb} : {pc}이고, 360°를 이 비로 나누면 각 중심각이 나온다. 구하는 ∠{ASKA}에 해당하는 항 {pw}{eul(pw)} 고른다.",
        sol1_fig=scene(circle_pts({"A": "20", "B": "20 + ta", "C": "20 + ta + tb"}), [["O", "A"], ["O", "B"], ["O", "C"]], circles=TWO_CIRC,
                       marks={"arc": [arc("O", "A", "B", "{ta}°"), arc("O", "B", "C", "{tb}°"), arc("O", "C", "A", "{tc}°")]}),
        sol1_anim=[[hl("circle:0")], [hl("arc:O", keep=True)]],
        sol2=[
            "세 호의 중심각을 더하면 360°: ∠AOB + ∠BOC + ∠COA = 360°",
            "호의 비가 {pa} : {pb} : {pc}이므로 중심각의 비도 {pa} : {pb} : {pc}",
            "∠{ASKA} = 360° ÷ ({pa} + {pb} + {pc}) × {pw} = 360° × [[frac({pw}, {ss})]] = {x}°",
        ],
        sol2_fig=steps([
            {"text": "∠AOB + ∠BOC + ∠COA = 360°", "hint": "원 한 바퀴"},
            {"text": "∠AOB : ∠BOC : ∠COA = {pa} : {pb} : {pc}", "hint": "호의 비 = 각의 비"},
            {"text": "∠{ASKA} = 360° ÷ {ss} × {pw} = {x}°", "marks": [{"on": "{x}°", "note": "비례배분"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="세 중심각은 {ta}°, {tb}°, {tc}°이고 합이 360°, 비가 {pa} : {pb} : {pc}로 조건과 같다. 답: [[deg({x})]]",
        model_answer="세 호의 중심각의 합은 360°이고, 한 원에서 호의 길이는 중심각의 크기에 정비례하므로 ∠AOB : ∠BOC : ∠COA = {pa} : {pb} : {pc}이다. 따라서 ∠{ASKA} = 360° ÷ ({pa} + {pb} + {pc}) × {pw} = {x}°이다.",
        rubric=[
            {"element": "한 바퀴 읽기", "points": 2, "criterion": "세 중심각의 합이 360°임을 밝혔다.", "partial": "180°로 두었으면 인정하지 않는다."},
            {"element": "비례배분", "points": 3, "criterion": "호의 비가 중심각의 비임을 쓰고 360° ÷ {ss} × {pw} = {x}°를 구했다.", "partial": "다른 호에 해당하는 항으로 배분했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠{ASKA} = {x}°로 답했다.", "partial": "다른 중심각을 답했으면 인정하지 않는다."},
        ],
    )


def ar_t5():
    return tpl("m1-2-arc-ratio", 5, AR,
        title="두 부채꼴의 넓이와 한 중심각으로 다른 중심각 구하기",
        skill="한 원에서 부채꼴의 넓이도 중심각에 정비례 — (넓이) : (넓이) = (각) : (각)",
        variant_axis={"구하는 것": "중심각", "주어진 것": "두 부채꼴의 넓이·한 중심각", "배치": "4가지"},
        discriminates="호의 길이뿐 아니라 넓이도 중심각에 정비례함을 쓰는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "ly", "values": {"in": list(LAY)}}, {"name": "t1", "values": {"in": [30, 40, 45, 60, 72, 90, 100, 120]}}, {"name": "x", "values": {"in": [20, 30, 40, 45, 50, 60, 75, 80, 90, 100, 120, 135, 150]}}, {"name": "m", "values": {"int": [2, 6]}}],
        table={"key": "ly", "rows": LAY},
        derive={"g": "gcd(t1, x)", "s1": "m*t1/gcd(t1, x)", "s2": "m*x/gcd(t1, x)", "t2": "x"},
        constraints=["x != t1", "al + t1 + gp + x <= 330", "s1 != s2", "x != s1", "x != s2", "s1 != t1", "s2 <= 60"],
        cost_values=["t1", "s1", "s2", "x"],
        relation="X*s1 - t1*s2", unknown="X", answer_var="x",
        verify=["ans*s1 == t1*s2", "ans > 0"],
        question="다음 그림의 원 O에서 부채꼴 AOB의 넓이는 {s1} cm², 부채꼴 COD의 넓이는 {s2} cm²이고 [[angle(AOB)]] = [[deg({t1})]]일 때, [[angle(COD)]]의 크기를 구하시오.",
        figure=scene(circle_pts(TWO_ARCS), TWO_SEGS, circles=TWO_CIRC,
                     marks={"arc": [arc("O", "A", "B", "{t1}°"), arc("O", "C", "D", "x")]},
                     labels=[arc_label("al + t1/2", "{s1} cm²"), arc_label("al + t1 + gp + t2/2", "{s2} cm²")]),
        answer="[[deg({x})]]", answer_alt=["{x}"],
        sol1="한 원에서 부채꼴의 넓이는 중심각의 크기에 정비례한다(호의 길이와 같은 성질). 두 부채꼴의 넓이의 비가 {s1} : {s2}이므로 중심각의 비도 {s1} : {s2}이고, ∠COD = x°로 두어 비례식을 세운다.",
        sol1_fig=scene(circle_pts(TWO_ARCS), TWO_SEGS, circles=TWO_CIRC,
                       marks={"arc": [arc("O", "A", "B", "{t1}°"), arc("O", "C", "D", "x")]},
                       labels=[arc_label("al + t1/2", "{s1} cm²"), arc_label("al + t1 + gp + t2/2", "{s2} cm²")]),
        sol1_anim=[[hl("arc:O", "label:0")], [hl("label:1", keep=True)]],
        sol2=[
            "∠COD = x°라 하면 넓이는 중심각에 정비례하므로 {s1} : {s2} = {t1} : x",
            "비례식에서 {s1} × x = {s2} × {t1} = {s2*t1}",
            "따라서 x = {dv(s2*t1, s1)}",
        ],
        sol2_fig=steps([
            {"text": "{s1} : {s2} = {t1} : x", "hint": "넓이 : 넓이 = 각 : 각"},
            {"text": "{co(s1)}x = {s2*t1}", "hint": "외항의 곱 = 내항의 곱"},
            {"text": "x = {x}", "marks": [{"on": "{x}", "note": "{s2*t1} ÷ {s1}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="넓이 1 cm²당 중심각은 {t1} ÷ {s1} = {dec(t1/s1)}°이고, {s2} cm²이면 {dec(t1/s1)}° × {s2} = {x}°로 같다. 답: [[deg({x})]]",
        model_answer="한 원에서 부채꼴의 넓이는 중심각의 크기에 정비례하므로 ∠COD = x°라 하면 {s1} : {s2} = {t1} : x이다. {co(s1)}x = {s2*t1}에서 x = {x}이므로 ∠COD = {x}°이다.",
        rubric=[
            {"element": "비례식 세우기", "points": 3, "criterion": "부채꼴의 넓이가 중심각에 정비례함을 밝히고 {s1} : {s2} = {t1} : x{eul(x)} 세웠다.", "partial": "순서가 뒤바뀐 비례식은 인정하지 않는다."},
            {"element": "해 구하기", "points": 2, "criterion": "{co(s1)}x = {s2*t1}에서 x = {x}{eul(x)} 구했다.", "partial": "계산 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "∠COD = {x}°로 답했다.", "partial": "다른 값을 답했으면 인정하지 않는다."},
        ],
    )


ARC_SEED = {
    "seed_id": "m1-2-arc-ratio", "category": "도형",
    "title": "호의 길이·넓이와 중심각의 비례 — 두 호·한 호·지름·세 점·넓이",
    "unit_id": "m1-2", "concept_ids": ["m1-2-10"],
    "schema_id": SCHEMA_ARC, "schema_name": "중심각의 크기와 호의 길이 비례 / 중심각 비례와 부채꼴 넓이",
    "source_item_ids": [],
    "note": "출판사 6.5 유형(호의 길이 ∝ 중심각 비례식·호 비→중심각·지름 조건·넓이 비례) 차용. 원 위의 점은 반지름 4의 좌표(cos·sin)로 실제로 그리고, 호의 길이·넓이 라벨은 호 바깥 labels, 중심각은 marks.arc. 두 호는 배치 표(시작각·간격) 4가지로 겹치지 않게.",
    "geometry": True,
    "templates": [ar_t1(), ar_t2(), ar_t3(), ar_t4(), ar_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 선분의 중점
SM = dict(prereq=["선분의 중점: 선분을 이등분하는 점", "선분의 길이의 합·차"], ops=["비례", "사칙"], tags=["선분", "중점", "등분점"])


def line_pts(names_x):
    return {nm: [x, 0] for nm, x in names_x.items()}


def seg_lbl(a, b, label):
    return {"a": a, "b": b, "label": label}


MID_ROWS = {   # M = AB 의 중점, N = MB 의 중점(또는 AM 의 중점). AB = 4토막, nx4 = N 의 자리(토막), cf4 = 구하는 선분의 토막 수
    "1": {"SECOND": "MB", "ASKS": "MN", "cf4": 1, "nx4": 3, "STEP": "MN = MB ÷ 2 = (AB ÷ 2) ÷ 2"},
    "2": {"SECOND": "MB", "ASKS": "AN", "cf4": 3, "nx4": 3, "STEP": "AN = AM + MN = AB ÷ 2 + AB ÷ 4"},
    "3": {"SECOND": "AM", "ASKS": "NB", "cf4": 3, "nx4": 1, "STEP": "NB = NM + MB = AB ÷ 4 + AB ÷ 2"},
    "4": {"SECOND": "AM", "ASKS": "AN", "cf4": 1, "nx4": 1, "STEP": "AN = AM ÷ 2 = (AB ÷ 2) ÷ 2"},
    "5": {"SECOND": "MB", "ASKS": "NB", "cf4": 1, "nx4": 3, "STEP": "NB = MB ÷ 2 = (AB ÷ 2) ÷ 2"},
    "6": {"SECOND": "AM", "ASKS": "MN", "cf4": 1, "nx4": 1, "STEP": "MN = AM ÷ 2 = (AB ÷ 2) ÷ 2"},
}


def sm_t1():
    return tpl("m1-2-segment-mid", 1, SM,
        title="중점의 중점 — AB의 길이로 부분 선분 구하기",
        skill="중점은 선분을 반으로 나눈다 — 두 번 반으로 나누면 1/4, 합치면 3/4",
        variant_axis={"구하는 것": "MN·AN·NB", "두 번째 중점": "MB의 중점·AM의 중점", "AB": "4의 배수"},
        discriminates="중점 조건을 길이 관계(½)로 옮기고 두 번 적용하는가, 구하는 선분이 어느 부분들의 합인지 그림에서 읽는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "r", "values": {"in": list(MID_ROWS)}}, {"name": "k", "values": {"int": [2, 12]}}],
        table={"key": "r", "rows": MID_ROWS},
        derive={"L": "4*k", "hL": "2*k", "qL": "k", "ans": "cf4*k", "xn": "nx4*k"},
        constraints=["ans != L", "ans != hL or cf4 == 2"],
        cost_values=["L", "hL", "qL", "ans"],
        relation="X - cf4*L/4", unknown="X", answer_var="ans",
        verify=["4*ans == cf4*L"],
        question="다음 그림에서 점 M은 [[seg(AB)]]의 중점이고 점 N은 [[seg({SECOND})]]의 중점이다. [[seg(AB)]] = {L} cm일 때, [[seg({ASKS})]]의 길이를 구하시오.",
        figure=scene(line_pts({"A": 0, "M": "{hL}", "N": "{xn}", "B": "{L}"}), [["A", "B"]], aspect_min=0.22,
                     labels=[{"at": ["{2*k}", 0], "text": "{L} cm", "dy": 26}]),
        answer="{ans}", answer_alt=["{ans} cm"],
        sol1="점 M이 AB의 중점이므로 AM = MB = AB ÷ 2 = {hL} cm다. 점 N은 {SECOND}의 중점이므로 {SECOND}를 다시 반으로 나누어 {qL} cm짜리 토막이 생긴다. 그림에서 {ASKS}가 어느 토막들로 이루어지는지 읽으면 {STEP}이다.",
        sol1_fig=scene(line_pts({"A": 0, "M": "{hL}", "N": "{xn}", "B": "{L}"}), [seg_lbl("A", "M", "{hL}"), seg_lbl("M", "B", "{hL}")], aspect_min=0.22),
        sol1_anim=[[hl("pt:M", "lbl:M")], [hl("pt:N", "lbl:N", keep=True)]],
        sol2=[
            "M이 AB의 중점이므로 AM = MB = {L} ÷ 2 = {hL} (cm)",
            "N이 {SECOND}의 중점이므로 {SECOND}의 절반은 {hL} ÷ 2 = {qL} (cm)",
            "{STEP} = {ans} (cm)",
        ],
        sol2_fig=steps([
            {"text": "AM = MB = {L} ÷ 2 = {hL}", "hint": "중점 → 절반"},
            {"text": "{SECOND} ÷ 2 = {qL}", "hint": "다시 절반"},
            {"text": "{ASKS} = {ans} (cm)", "marks": [{"on": "{ans}", "note": "[[frac({cf4}, 4)]] × AB"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="AB는 {qL} cm짜리 토막 4개로 나뉘고 {ASKS}는 그중 {cf4}개이므로 {qL} × {cf4} = {ans} (cm)다. 답: {ans} cm",
        model_answer="점 M이 AB의 중점이므로 AM = MB = {L} ÷ 2 = {hL} (cm)이고, 점 N이 {SECOND}의 중점이므로 {SECOND}의 절반은 {qL} cm이다. 따라서 {STEP} = {ans} (cm)이다.",
        rubric=[
            {"element": "첫 중점", "points": 2, "criterion": "M이 중점이므로 AM = MB = {hL} cm임을 구했다.", "partial": "중점의 뜻을 쓰지 않았으면 인정하지 않는다."},
            {"element": "둘째 중점", "points": 2, "criterion": "N이 {SECOND}의 중점이므로 {qL} cm짜리 토막이 생김을 구했다.", "partial": "어느 선분의 중점인지 잘못 읽었으면 인정하지 않는다."},
            {"element": "구하는 선분", "points": 3, "criterion": "{ASKS}가 어느 토막들로 이루어지는지 밝혀 {ans} cm를 구했다.", "partial": "토막 하나를 빠뜨리거나 더했으면 1점."},
        ],
    )


TRI_MID = {   # P, Q 는 AB 의 삼등분점(AP = PQ = QB = 2토막), M 은 표의 선분의 중점. AB = 6토막, mx = M 의 자리(토막), cf6 = 구하는 선분의 토막 수
    "1": {"SECOND": "PQ", "ASKS": "AM", "cf6": 3, "mx": 3, "STEP": "AM = AP + PM = 2토막 + 1토막"},
    "2": {"SECOND": "PQ", "ASKS": "PM", "cf6": 1, "mx": 3, "STEP": "PM = PQ ÷ 2 = 1토막"},
    "3": {"SECOND": "AP", "ASKS": "MB", "cf6": 5, "mx": 1, "STEP": "MB = MP + PQ + QB = 1토막 + 2토막 + 2토막"},
    "4": {"SECOND": "AP", "ASKS": "MQ", "cf6": 3, "mx": 1, "STEP": "MQ = MP + PQ = 1토막 + 2토막"},
    "5": {"SECOND": "QB", "ASKS": "AM", "cf6": 5, "mx": 5, "STEP": "AM = AQ + QM = 4토막 + 1토막"},
    "6": {"SECOND": "QB", "ASKS": "PM", "cf6": 3, "mx": 5, "STEP": "PM = PQ + QM = 2토막 + 1토막"},
}


def sm_t2():
    return tpl("m1-2-segment-mid", 2, SM,
        title="삼등분점과 중점 — AB의 길이로 부분 선분 구하기",
        skill="삼등분점은 선분을 1/3씩, 중점은 1/2 — 토막(AB의 1/6)으로 세면 빠르다",
        variant_axis={"구하는 것": "MB·PM·AM·MQ", "중점": "AQ·PB·PQ의 중점", "AB": "6의 배수"},
        discriminates="삼등분점과 중점의 조건을 함께 길이로 옮기고, 구하는 선분을 토막의 합·차로 읽는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "r", "values": {"in": list(TRI_MID)}}, {"name": "k", "values": {"int": [2, 10]}}],
        table={"key": "r", "rows": TRI_MID},
        derive={"L": "6*k", "tL": "2*k", "sL": "k", "ans": "cf6*k", "xm": "mx*k"},
        constraints=["ans != L", "ans != tL or cf6 == 2"],
        cost_values=["L", "tL", "sL", "ans"],
        relation="X - cf6*L/6", unknown="X", answer_var="ans",
        verify=["6*ans == cf6*L"],
        question="다음 그림에서 두 점 P, Q는 [[seg(AB)]]의 삼등분점이고 점 M은 [[seg({SECOND})]]의 중점이다. [[seg(AB)]] = {L} cm일 때, [[seg({ASKS})]]의 길이를 구하시오.",
        figure=scene(line_pts({"A": 0, "P": "{tL}", "M": "{xm}", "Q": "{2*tL}", "B": "{L}"}), [["A", "B"]], aspect_min=0.22,
                     labels=[{"at": ["{3*k}", 0], "text": "{L} cm", "dy": 26}]),
        answer="{ans}", answer_alt=["{ans} cm"],
        sol1="P, Q가 AB의 삼등분점이므로 AP = PQ = QB = AB ÷ 3 = {tL} cm다. M은 {SECOND}의 중점이므로 {SECOND}를 반으로 나눈다. AB를 {sL} cm짜리 토막 6개로 보면 삼등분점은 2토막마다, 중점은 그 절반 자리에 놓이므로 {ASKS}가 몇 토막인지 세면 된다.",
        sol1_fig=scene(line_pts({"A": 0, "P": "{tL}", "M": "{xm}", "Q": "{2*tL}", "B": "{L}"}), [seg_lbl("A", "P", "{tL}"), seg_lbl("P", "Q", "{tL}"), seg_lbl("Q", "B", "{tL}")], aspect_min=0.22),
        sol1_anim=[[hl("pt:P", "pt:Q", "lbl:P", "lbl:Q")], [hl("pt:M", "lbl:M", keep=True)]],
        sol2=[
            "삼등분점이므로 AP = PQ = QB = {L} ÷ 3 = {tL} (cm)",
            "M은 {SECOND}의 중점이므로 {SECOND}의 절반을 구한다 — AB를 {sL} cm 토막 6개로 나누면 편하다",
            "{STEP}이므로 {ASKS} = {sL} × {cf6} = {ans} (cm)",
        ],
        sol2_fig=steps([
            {"text": "AP = PQ = QB = {tL}", "hint": "삼등분"},
            {"text": "토막 1개 = {sL} cm (AB ÷ 6)", "hint": "중점은 토막의 절반 자리"},
            {"text": "{ASKS} = {sL} × {cf6} = {ans} (cm)", "marks": [{"on": "{ans}", "note": "{cf6}토막"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="AB = {L} cm는 {sL} cm 토막 6개이고 {ASKS}는 그중 {cf6}개이므로 {ans} cm다. 답: {ans} cm",
        model_answer="P, Q가 AB의 삼등분점이므로 AP = PQ = QB = {L} ÷ 3 = {tL} (cm)이다. M이 {SECOND}의 중점이므로 {SECOND}의 절반을 생각하면, AB를 {sL} cm짜리 토막 6개로 나눌 때 {ASKS}는 {cf6}토막이다. 따라서 {ASKS} = {sL} × {cf6} = {ans} (cm)이다.",
        rubric=[
            {"element": "삼등분점", "points": 2, "criterion": "AP = PQ = QB = {tL} cm임을 구했다.", "partial": "2로 나누었으면 인정하지 않는다."},
            {"element": "중점", "points": 2, "criterion": "M이 {SECOND}의 중점임을 길이({SECOND}의 절반)로 옮겼다.", "partial": "어느 선분의 중점인지 잘못 읽었으면 인정하지 않는다."},
            {"element": "구하는 선분", "points": 3, "criterion": "{ASKS}를 토막의 합·차로 읽어 {ans} cm를 구했다.", "partial": "토막 하나를 빠뜨리거나 더했으면 1점."},
        ],
    )


REV_ROWS = {   # 짧은 토막(길이 k)이 주어질 때 — M = AB 중점, N = AM 중점. G1·G2 = 주어진 선분의 양 끝
    "1": {"GIVS": "NM", "G1": "N", "G2": "M", "ASKS": "AB", "cf": 4, "STEP": "AB = 2 × AM = 2 × (2 × NM)"},
    "2": {"GIVS": "NM", "G1": "N", "G2": "M", "ASKS": "NB", "cf": 3, "STEP": "NB = NM + MB = NM + 2 × NM"},
    "3": {"GIVS": "AN", "G1": "A", "G2": "N", "ASKS": "AB", "cf": 4, "STEP": "AB = 2 × AM = 2 × (2 × AN)"},
    "4": {"GIVS": "AN", "G1": "A", "G2": "N", "ASKS": "MB", "cf": 2, "STEP": "MB = AM = 2 × AN"},
    "5": {"GIVS": "AN", "G1": "A", "G2": "N", "ASKS": "NB", "cf": 3, "STEP": "NB = NM + MB = AN + 2 × AN"},
}


def sm_t3():
    return tpl("m1-2-segment-mid", 3, SM,
        title="짧은 토막의 길이로 전체 선분 구하기 — 중점 거꾸로",
        skill="중점 관계를 거꾸로: 절반이 k이면 전체는 2k — 두 번 되돌리면 4k",
        variant_axis={"구하는 것": "AB·NB·MB", "주어진 것": "NM·AN", "토막": "2~15"},
        discriminates="중점 조건을 거꾸로(×2) 적용하는가, 구하는 선분이 토막 몇 개인지 세는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "r", "values": {"in": list(REV_ROWS)}}, {"name": "k", "values": {"int": [2, 15]}}],
        table={"key": "r", "rows": REV_ROWS},
        derive={"ans": "cf*k", "L": "4*k"},
        constraints=["ans != k"],
        cost_values=["k", "ans"],
        relation="X - cf*k", unknown="X", answer_var="ans",
        verify=["ans == cf*k"],
        question="다음 그림에서 점 M은 [[seg(AB)]]의 중점이고 점 N은 [[seg(AM)]]의 중점이다. [[seg({GIVS})]] = {k} cm일 때, [[seg({ASKS})]]의 길이를 구하시오.",
        figure=scene(line_pts({"A": 0, "N": "{k}", "M": "{2*k}", "B": "{4*k}"}), [["A", "B"], {"a": "{G1}", "b": "{G2}", "label": "{k} cm"}], aspect_min=0.22),
        answer="{ans}", answer_alt=["{ans} cm"],
        sol1="N이 AM의 중점이므로 AN = NM = {k} cm이고 AM = 2 × {k} = {2*k} (cm)다. M이 AB의 중점이므로 MB = AM = {2*k} cm, AB = 2 × {2*k} = {4*k} (cm)다. 중점 조건을 거꾸로 두 번 쓰면 AB는 {k} cm짜리 토막 4개다. {ASKS}가 그중 몇 토막인지 센다.",
        sol1_fig=scene(line_pts({"A": 0, "N": "{k}", "M": "{2*k}", "B": "{4*k}"}), [seg_lbl("A", "N", "{k}"), seg_lbl("N", "M", "{k}"), seg_lbl("M", "B", "{2*k}")], aspect_min=0.22),
        sol1_anim=[[hl("pt:N", "lbl:N")], [hl("pt:M", "lbl:M", keep=True)]],
        sol2=[
            "N이 AM의 중점이므로 AN = NM = {k} cm, AM = {k} × 2 = {2*k} (cm)",
            "M이 AB의 중점이므로 MB = AM = {2*k} cm, AB = {2*k} × 2 = {4*k} (cm)",
            "{STEP} = {ans} (cm)",
        ],
        sol2_fig=steps([
            {"text": "AN = NM = {k} → AM = {2*k}", "hint": "중점 거꾸로 ×2"},
            {"text": "MB = AM = {2*k} → AB = {4*k}", "hint": "다시 ×2"},
            {"text": "{ASKS} = {ans} (cm)", "marks": [{"on": "{ans}", "note": "{cf}토막"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="AB = {4*k} cm를 반으로 나누면 AM = {2*k}, 다시 반으로 나누면 AN = {k} cm로 조건과 같다. 답: {ans} cm",
        model_answer="N이 AM의 중점이므로 AM = 2 × {k} = {2*k} (cm)이고, M이 AB의 중점이므로 AB = 2 × {2*k} = {4*k} (cm), MB = {2*k} cm이다. 따라서 {STEP} = {ans} (cm)이다.",
        rubric=[
            {"element": "AM 구하기", "points": 2, "criterion": "N이 AM의 중점이므로 AM = 2 × {k} = {2*k} cm임을 구했다.", "partial": "2로 나누었으면 인정하지 않는다."},
            {"element": "AB 구하기", "points": 2, "criterion": "M이 AB의 중점이므로 AB = 2 × {2*k} = {4*k} cm임을 구했다.", "partial": "한 번만 되돌렸으면 1점."},
            {"element": "구하는 선분", "points": 3, "criterion": "{ASKS}가 토막 {cf}개임을 밝혀 {ans} cm를 구했다.", "partial": "토막 하나를 빠뜨리거나 더했으면 1점."},
        ],
    )


ASK_MN = {"1": {"ASKS": "MN", "isMN": 1}, "2": {"ASKS": "BC", "isMN": 0}}


def sm_t4():
    return tpl("m1-2-segment-mid", 4, SM,
        title="이어진 두 선분의 중점 사이의 거리 — MN = (AB + BC) ÷ 2",
        skill="MN = MB + BN = AB ÷ 2 + BC ÷ 2 = AC ÷ 2",
        variant_axis={"구하는 것": "MN·BC", "주어진 것": "AB·BC 또는 AB·MN", "수치": "짝수"},
        discriminates="MN이 두 선분의 절반의 합임을 그림에서 읽는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "ask", "values": {"in": [1, 2]}}, {"name": "u", "values": {"int": [2, 12]}}, {"name": "v", "values": {"int": [2, 12]}}],
        table={"key": "ask", "rows": ASK_MN},
        derive={"a": "2*u", "b": "2*v", "mn": "u + v", "ans": "isMN*(u + v) + (1 - isMN)*2*v"},
        constraints=["u != v", "ans != a", "ans != b or isMN == 0", "mn != a", "mn != b"],
        cost_values=["a", "b", "mn", "ans"],
        relation="X - ans", unknown="X", answer_var="ans",
        verify=["2*mn == a + b", "ans == isMN*mn + (1 - isMN)*b"],
        question="{Q}",
        figure=scene(line_pts({"A": 0, "M": "{u}", "B": "{a}", "N": "{a + v}", "C": "{a + b}"}), [["A", "C"]], aspect_min=0.22),
        answer="{ans}", answer_alt=["{ans} cm"],
        sol1="세 점 A, B, C가 한 직선 위에 이 순서로 있고 M, N이 각각 AB, BC의 중점이면 MB = AB ÷ 2, BN = BC ÷ 2다. 그림에서 MN = MB + BN이므로 MN은 두 선분의 절반을 더한 것, 곧 AC의 절반이다.",
        sol1_fig=scene(line_pts({"A": 0, "M": "{u}", "B": "{a}", "N": "{a + v}", "C": "{a + b}"}), [seg_lbl("M", "B", "{u}"), seg_lbl("B", "N", "{v}")], aspect_min=0.22),
        sol1_anim=[[hl("pt:M", "lbl:M", "pt:N", "lbl:N")], [hl("seg:M-B", "seg:B-N", keep=True)]],
        sol2=[
            "M이 AB의 중점이므로 MB = {a} ÷ 2 = {u} (cm)",
            "{L2}",
            "{L3}",
        ],
        sol2_fig=steps([
            {"text": "MB = {a} ÷ 2 = {u}", "hint": "중점 → 절반"},
            {"text": "{F2}"},
            {"text": "{F3}", "marks": [{"on": "{ans}", "note": "{ASKS}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("mark:2-0")]],
        sol_check="MN = MB + BN = {u} + {v} = {mn} (cm)이고 AC = {a + b} cm의 절반과 같다. 답: {ans} cm",
        model_answer="{MA}",
        rubric=[
            {"element": "중점 읽기", "points": 3, "criterion": "MB = AB ÷ 2, BN = BC ÷ 2임을 밝혔다.", "partial": "한쪽만 옳으면 1점."},
            {"element": "식 세우기", "points": 2, "criterion": "MN = MB + BN으로 식을 세웠다.", "partial": "MN을 AB 또는 BC의 절반으로 두었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKS} = {ans} cm로 답했다.", "partial": "계산 실수면 1점."},
        ],
    )


def _fix_t4(t):
    """구하는 것(MN / BC)에 따라 문장이 갈리므로 두 틀(t4·t5)로 나눈다."""
    common = "다음 그림과 같이 한 직선 위에 세 점 A, B, C가 이 순서로 있고, 두 점 M, N은 각각 [[seg(AB)]], [[seg(BC)]]의 중점이다. "
    out = []
    for no, ask in ((4, "1"), (5, "2")):
        tt = dict(t)
        tt["id"] = f"m1-2-segment-mid-t{no}"
        tt["params"] = [p for p in t["params"] if p["name"] != "ask"]
        tt.pop("table", None)
        row = ASK_MN[ask]
        tt["derive"] = {"isMN": str(row["isMN"]), **t["derive"]}
        tt["variant_axis"] = {**t["variant_axis"], "구하는 것": row["ASKS"]}
        rep = {"{ASKS}": row["ASKS"]}
        if ask == "1":
            rep.update({"{Q}": common + "[[seg(AB)]] = {a} cm, [[seg(BC)]] = {b} cm일 때, [[seg(MN)]]의 길이를 구하시오.",
                        "{L2}": "N이 BC의 중점이므로 BN = {b} ÷ 2 = {v} (cm)",
                        "{L3}": "MN = MB + BN = {u} + {v} = {mn} (cm)",
                        "{F2}": "BN = {b} ÷ 2 = {v}", "{F3}": "MN = {u} + {v} = {mn}",
                        "{MA}": "M, N이 각각 AB, BC의 중점이므로 MB = {a} ÷ 2 = {u} (cm), BN = {b} ÷ 2 = {v} (cm)이다. 따라서 MN = MB + BN = {u} + {v} = {mn} (cm)이다."})
            tt["title"] = "이어진 두 선분의 중점 사이의 거리 MN 구하기"
        else:
            rep.update({"{Q}": common + "[[seg(AB)]] = {a} cm, [[seg(MN)]] = {mn} cm일 때, [[seg(BC)]]의 길이를 구하시오.",
                        "{L2}": "MN = MB + BN이므로 BN = {mn} − {u} = {v} (cm)",
                        "{L3}": "N이 BC의 중점이므로 BC = 2 × BN = 2 × {v} = {b} (cm)",
                        "{F2}": "BN = MN − MB = {mn} − {u} = {v}", "{F3}": "BC = 2 × {v} = {b}",
                        "{MA}": "M이 AB의 중점이므로 MB = {a} ÷ 2 = {u} (cm)이고, MN = MB + BN에서 BN = {mn} − {u} = {v} (cm)이다. N이 BC의 중점이므로 BC = 2 × {v} = {b} (cm)이다."})
            tt["title"] = "중점 사이의 거리 MN으로 BC 구하기"
            tt["skill"] = "BN = MN − MB 로 되돌린 뒤 BC = 2 × BN"
            tt["difficulty"] = 3
            tt["figure"] = scene(line_pts({"A": 0, "M": "{u}", "B": "{a}", "N": "{a + v}", "C": "{a + b}"}), [["A", "C"]], aspect_min=0.22)
        from seedlib import sub_all
        tt = sub_all(tt, rep)
        out.append(tt)
    return out


MID_SEED = {
    "seed_id": "m1-2-segment-mid", "category": "도형",
    "title": "선분의 중점 — 중점의 중점·삼등분점과 중점·거꾸로·이어진 두 선분의 중점",
    "unit_id": "m1-2", "concept_ids": ["m1-2-01"],
    "schema_id": SCHEMA_MID, "schema_name": "선분의 등분점과 중점 관계 / 중점 연쇄와 선분 길이 관계",
    "source_item_ids": [],
    "note": "출판사 5.1 유형(선분 중점 AM·MN 길이) 차용. 점은 y = 0 위에 실제 길이 좌표로 두고 aspect_min 으로 납작하게. 구하는 선분·둘째 중점의 위치는 표 행(계수 × AB), 거꾸로(토막 → 전체)와 이어진 두 선분(MN = AC/2)도 표로.",
    "geometry": True,
    "templates": [sm_t1(), sm_t2(), sm_t3()] + _fix_t4(sm_t4()),
}


if __name__ == "__main__":
    with_pitfalls(EXT_SEED)
    dump(EXT_SEED)
    with_pitfalls(ARC_SEED)
    dump(ARC_SEED)
    with_pitfalls(MID_SEED)
    dump(MID_SEED)
