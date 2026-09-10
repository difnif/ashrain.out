# itemfactory/tools/mkseed_m1_solid.py — 입체도형 시드 생성기: 원기둥 겉넓이 · 원뿔 · 구 (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m1_solid.py
#     → seeds/m1-2-cylinder-surface.json (5틀) · seeds/m1-2-cone.json (5틀) · seeds/m1-2-sphere.json (3틀)
#
# 기하 = 2단 해설(도형 읽기 / 계산·결론, sol_check). π는 기호로 보존([[k * pi]]). 정수 계수가 나오도록 높이는 3의 배수, 구의 반지름은 3의 배수로 생성.
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402

SCHEMA_CYL_SURF = "a8fcf405-db82-4444-ad44-929cb75bc107"   # 원기둥의 겉넓이
SCHEMA_CONE_VOL = "3c211805-73b1-47fc-b0d2-3b7857974ffa"   # 원뿔의 부피
SCHEMA_SPHERE = "dfbbb10f-1413-4586-b2e1-3a1ba7aae7d8"     # 원기둥에 꼭 맞는 구·원뿔 부피 관계

GEO = {"process": "절차수행", "context": "기하맥락", "points": 4, "time_limit": 80, "traps": ["제곱누락", "구하는대상혼동"]}


def tpl(seed_id, no, *bases, **kw):
    t = dict(GEO)
    for b in bases:
        t.update(b)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def solid(kind, **args):
    return [{"fn": "solid", "args": {"kind": kind, **args}}]


PI_FMT = "[[{v} * pi]]"

# ═══════════════════════════════════════════════════════════════════ 1. 원기둥의 겉넓이
CYL = dict(prereq=["원의 넓이 πr²", "원주 2πr", "기둥의 전개도"], ops=["넓이", "지수"], tags=["원기둥", "겉넓이"])


def cyl_t1():
    return tpl("m1-2-cylinder-surface", 1, CYL,
        title="반지름·높이로 원기둥의 겉넓이 구하기",
        skill="전개도에서 겉넓이 = (밑넓이) × 2 + (옆넓이), 옆넓이의 가로 = 밑면의 원주 2πr",
        variant_axis={"구하는 것": "겉넓이", "제시 방식": "반지름·높이"},
        discriminates="옆면(직사각형)의 가로가 원주 2πr임을 알고, 밑면을 두 개 세는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "r", "values": {"int": [2, 12]}}, {"name": "h", "values": {"int": [3, 20]}}],
        derive={"kb": "r*r", "kl": "2*r*h", "ks": "2*r*r + 2*r*h", "kc": "2*r"},
        constraints=["h != r", "ks <= 800", "ks != kb", "ks != kl"],
        cost_values=["r", "h", "kb", "kl", "ks"],
        relation="X - 2*r*r - 2*r*h", unknown="X", answer_var="ks",
        verify=["ks == 2*kb + kl", "ks > 0"],
        question="다음 그림과 같이 밑면의 반지름의 길이가 {r} cm, 높이가 {h} cm인 원기둥의 겉넓이를 구하시오.",
        figure=solid("cylinder", radius="{r}", height="{h}"),
        answer="[[{ks} * pi]]", answer_alt=["[[{ks} * pi]] cm²"],
        sol1="원기둥을 펼치면 밑면인 원 2개와 옆면인 직사각형 1개가 나온다. 밑면은 반지름 {r} cm인 원이고, 옆면 직사각형의 세로는 높이 {h} cm, 가로는 밑면의 원주 2π × {r} = {kc}π (cm)이다 — 옆면을 말아 붙이면 밑면 둘레와 딱 맞아야 하기 때문이다. 겉넓이는 (밑넓이) × 2 + (옆넓이)다.",
        sol1_fig=solid("cylinder", radius="{r}", height="{h}"),
        sol1_anim=[[hl("top", "base", "radius", "r-lbl")], [hl("height", "h-lbl", keep=True)]],
        sol2=[
            "밑넓이: π × {r}² = {kb}π (cm²), 밑면이 2개이므로 {kb}π × 2 = {2*kb}π (cm²)",
            "옆넓이: (가로) × (세로) = (원주) × (높이) = {kc}π × {h} = {kl}π (cm²)",
            "겉넓이 = (밑넓이) × 2 + (옆넓이) = {2*kb}π + {kl}π = {ks}π (cm²)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 × 2 = π × {r}² × 2 = {2*kb}π", "hint": "밑면은 두 개", "marks": [{"on": "{2*kb}π", "note": "{kb}×2"}]},
            {"text": "옆넓이 = 2π × {r} × {h} = {kl}π", "hint": "가로 = 원주 2πr", "marks": [{"on": "{kl}π", "note": "{kc}×{h}"}]},
            {"text": "겉넓이 = {2*kb}π + {kl}π = {ks}π (cm²)"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="밑면을 하나만 세면 {kb + kl}π, 옆면의 가로를 반지름 {r}로 잘못 잡으면 {kb*2 + r*h}π가 나온다 — 둘 다 답이 아니다. 답은 [[{ks} * pi]] cm²다.",
        model_answer="원기둥의 겉넓이는 (밑넓이) × 2 + (옆넓이)이다. 밑넓이는 π × {r}² = {kb}π (cm²)이고 밑면이 2개이므로 {2*kb}π (cm²), 옆면은 가로가 밑면의 원주 2π × {r} = {kc}π (cm), 세로가 {h} cm인 직사각형이므로 옆넓이는 {kc}π × {h} = {kl}π (cm²)이다. 따라서 겉넓이는 {2*kb}π + {kl}π = {ks}π (cm²)다.",
        rubric=[
            {"element": "밑넓이", "points": 2, "criterion": "밑넓이 π × {r}² = {kb}π를 구하고 밑면이 2개임을 반영했다.", "partial": "밑넓이는 옳으나 하나만 셌으면 1점."},
            {"element": "옆넓이", "points": 3, "criterion": "옆면의 가로가 원주 2π × {r}임을 밝히고 옆넓이 {kl}π를 구했다.", "partial": "옆면이 직사각형임은 밝혔으나 가로를 원주로 잡지 못했으면 1점."},
            {"element": "겉넓이", "points": 2, "criterion": "(밑넓이) × 2 + (옆넓이) = {ks}π (cm²)로 답했다.", "partial": "합하는 식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


def cyl_t2():
    return tpl("m1-2-cylinder-surface", 2, CYL,
        title="겉넓이와 반지름으로 높이 구하기",
        skill="겉넓이 = 2πr² + 2πrh 를 세우고 h에 대한 방정식으로 풀기",
        variant_axis={"구하는 것": "높이", "제시 방식": "겉넓이·반지름"},
        discriminates="겉넓이 식을 바르게 세우고 π를 지운 뒤 h를 역산하는가",
        qtype="short", difficulty=3, pool_target=300, process="추론", ops=["넓이", "방정식"],
        params=[{"name": "r", "values": {"int": [2, 12]}}, {"name": "h", "values": {"int": [3, 20]}}],
        derive={"kb": "r*r", "kl": "2*r*h", "ks": "2*r*r + 2*r*h", "kc": "2*r"},
        constraints=["h != r", "ks <= 800", "ks != h", "kb != h"],
        cost_values=["r", "h", "kb", "kl", "ks"],
        relation="2*r*r + 2*r*X - ks", unknown="X", answer_var="h",
        verify=["2*r*r + 2*r*ans == ks", "ans > 0"],
        question="다음 그림과 같이 밑면의 반지름의 길이가 {r} cm인 원기둥의 겉넓이가 [[{ks} * pi]] cm²일 때, 이 원기둥의 높이를 구하시오.",
        figure=solid("cylinder", radius="{r}", height="h"),
        answer="{h}", answer_alt=["{h} cm"],
        sol1="높이를 h cm로 두고 겉넓이를 h의 식으로 나타낸다. 밑넓이는 π × {r}² = {kb}π (cm²)로 2개, 옆면은 가로 2π × {r} = {kc}π (cm), 세로 h cm인 직사각형이므로 옆넓이는 {kc}πh (cm²)이다. 겉넓이가 {ks}π이므로 {2*kb}π + {kc}πh = {ks}π라는 방정식이 나온다.",
        sol1_fig=solid("cylinder", radius="{r}", height="h"),
        sol1_anim=[[hl("top", "base", "radius", "r-lbl")], [hl("height", "h-lbl", keep=True)]],
        sol2=[
            "높이를 h cm라 하면 (밑넓이) × 2 = π × {r}² × 2 = {2*kb}π (cm²), 옆넓이 = 2π × {r} × h = {kc}πh (cm²)",
            "겉넓이가 {ks}π cm²이므로 {2*kb}π + {kc}πh = {ks}π",
            "양변을 π로 나누면 {2*kb} + {kc}h = {ks}",
            "{2*kb}{eul(2*kb)} 이항하면 {kc}h = {kl}, 따라서 h = {kl} ÷ {kc} = {h}",
        ],
        sol2_fig=steps([
            {"text": "{2*kb}π + {kc}πh = {ks}π", "hint": "밑넓이 × 2 + 옆넓이 = 겉넓이"},
            {"text": "{2*kb} + {kc}h = {ks}", "hint": "양변 ÷ π"},
            {"text": "{kc}h = {kl}", "hint": "{2*kb}{eul(2*kb)} 이항"},
            {"text": "h = {h}", "marks": [{"on": "{h}", "note": "{kl}÷{kc}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2"), reveal(3), hl("mark:3-0")]],
        sol_check="높이 {h} cm로 겉넓이를 다시 구하면 {2*kb}π + 2π × {r} × {h} = {2*kb}π + {kl}π = {ks}π (cm²)로 문제의 값과 같다. 답은 {h} cm다.",
        model_answer="높이를 h cm라 하면 겉넓이는 (밑넓이) × 2 + (옆넓이) = π × {r}² × 2 + 2π × {r} × h = {2*kb}π + {kc}πh (cm²)이다. 이 값이 {ks}π이므로 {2*kb} + {kc}h = {ks}, {kc}h = {kl}에서 h = {h}이다. 따라서 높이는 {h} cm다.",
        rubric=[
            {"element": "겉넓이 식 세우기", "points": 3, "criterion": "높이를 h로 놓고 겉넓이를 {2*kb}π + {kc}πh (= {ks}π)로 나타냈다.", "partial": "밑넓이·옆넓이 중 하나만 옳으면 1점."},
            {"element": "방정식 풀이", "points": 2, "criterion": "π를 지우고 이항하여 {kc}h = {kl}{eul(kl)} 얻었다.", "partial": "π를 지우는 단계까지 옳으면 1점."},
            {"element": "높이 구하기", "points": 2, "criterion": "h = {h}{eul(h)} 구하고 겉넓이가 맞는지 확인했다.", "partial": "확인 없이 답만 옳으면 1점."},
        ],
    )


def cyl_t3():
    return tpl("m1-2-cylinder-surface", 3, CYL,
        title="옆넓이와 높이로 반지름 구하기",
        skill="옆넓이 = (원주) × (높이) = 2πrh 에서 r을 역산하기",
        variant_axis={"구하는 것": "반지름", "제시 방식": "옆넓이·높이"},
        discriminates="옆면 직사각형의 가로가 원주 2πr임을 써서 r을 구하는가",
        qtype="short", difficulty=3, pool_target=300, process="추론", ops=["넓이", "방정식"],
        params=[{"name": "r", "values": {"int": [2, 12]}}, {"name": "h", "values": {"int": [3, 20]}}],
        derive={"kl": "2*r*h", "kc": "2*r", "kh": "2*h"},
        constraints=["h != r", "kl != h", "kl <= 480"],
        cost_values=["r", "h", "kl", "kh"],
        relation="2*X*h - kl", unknown="X", answer_var="r",
        verify=["2*ans*h == kl", "ans > 0"],
        question="다음 그림과 같이 높이가 {h} cm인 원기둥의 옆넓이가 [[{kl} * pi]] cm²일 때, 이 원기둥의 밑면의 반지름의 길이를 구하시오.",
        figure=solid("cylinder", radius="r", height="{h}"),
        answer="{r}", answer_alt=["{r} cm"],
        sol1="옆면을 펼치면 세로가 높이 {h} cm이고 가로가 밑면의 원주인 직사각형이다. 반지름을 r cm로 두면 원주는 2πr (cm)이므로 옆넓이는 2πr × {h} = {kh}πr (cm²)이다. 이것이 {kl}π와 같다는 방정식에서 r을 구한다.",
        sol1_fig=solid("cylinder", radius="r", height="{h}"),
        sol1_anim=[[hl("height", "h-lbl")], [hl("top", "base", "radius", "r-lbl", keep=True)]],
        sol2=[
            "밑면의 반지름을 r cm라 하면 밑면의 원주는 2πr (cm)이다.",
            "옆넓이 = (원주) × (높이) = 2πr × {h} = {kh}πr (cm²)",
            "옆넓이가 {kl}π cm²이므로 {kh}πr = {kl}π, 양변을 π로 나누면 {kh}r = {kl}",
            "양변을 {kh}{ro(kh)} 나누면 r = {r}",
        ],
        sol2_fig=steps([
            {"text": "2πr × {h} = {kl}π", "hint": "옆넓이 = 원주 × 높이"},
            {"text": "{kh}r = {kl}", "hint": "양변 ÷ π"},
            {"text": "r = {r}", "marks": [{"on": "{r}", "note": "{kl}÷{kh}"}]},
        ]),
        sol2_anim=[[], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="반지름 {r} cm이면 원주는 2π × {r} = {kc}π (cm), 옆넓이는 {kc}π × {h} = {kl}π (cm²)로 문제의 값과 같다. 답은 {r} cm다.",
        model_answer="밑면의 반지름을 r cm라 하면 옆넓이는 (원주) × (높이) = 2πr × {h} = {kh}πr (cm²)이다. 이 값이 {kl}π이므로 {kh}r = {kl}에서 r = {r}이다. 따라서 밑면의 반지름의 길이는 {r} cm다.",
        rubric=[
            {"element": "옆넓이 식 세우기", "points": 3, "criterion": "옆면의 가로가 원주 2πr임을 밝히고 옆넓이를 2πr × {h}{ro(h)} 나타냈다.", "partial": "옆면이 직사각형임은 밝혔으나 가로를 원주로 잡지 못했으면 1점."},
            {"element": "방정식 풀이", "points": 2, "criterion": "{kh}πr = {kl}π에서 π를 지우고 r = {r}{eul(r)} 구했다.", "partial": "π를 지우는 단계까지 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "반지름 {r} cm로 옆넓이가 {kl}π가 됨을 확인하고 답을 썼다.", "partial": "확인 없이 답만 옳으면 1점."},
        ],
    )


def cyl_t4():
    return tpl("m1-2-cylinder-surface", 4, CYL,
        title="직육면체의 겉넓이 구하기",
        skill="겉넓이 = 2 × (ab + bc + ca) — 마주 보는 면이 같음을 이용해 세 종류의 면을 두 번씩 세기",
        variant_axis={"구하는 것": "겉넓이", "입체": "직육면체"},
        discriminates="여섯 면을 세 쌍으로 묶어 빠짐없이 세는가",
        qtype="short", difficulty=2, pool_target=300, tags=["직육면체", "겉넓이"], ops=["넓이", "사칙"],
        params=[{"name": "c", "values": {"int": [2, 8]}}, {"name": "db", "values": {"int": [1, 4]}}, {"name": "da", "values": {"int": [1, 5]}}],
        derive={"b": "c + db", "a": "c + db + da", "ab": "(c + db + da)*(c + db)", "bc": "(c + db)*c", "ca": "c*(c + db + da)", "S": "2*((c + db + da)*(c + db) + (c + db)*c + c*(c + db + da))"},
        constraints=["S <= 600"],
        cost_values=["a", "b", "c", "ab", "bc", "ca", "S"],
        relation="X - 2*(a*b + b*c + c*a)", unknown="X", answer_var="S",
        verify=["ans == 2*(ab + bc + ca)"],
        question="가로의 길이가 {a} cm, 세로의 길이가 {b} cm, 높이가 {c} cm인 직육면체의 겉넓이를 구하시오.",
        figure=solid("rectangular_prism"),
        answer="{S}", answer_alt=["{S} cm²"],
        sol1="직육면체의 여섯 면은 마주 보는 면끼리 합동이므로 세 종류의 직사각형이 두 개씩 있다. 가로 × 세로({a} × {b}), 세로 × 높이({b} × {c}), 높이 × 가로({c} × {a}) 세 넓이를 더한 뒤 2배 하면 겉넓이다.",
        sol1_fig=steps(["앞·뒤: {a} × {c} 두 개", "옆: {b} × {c} 두 개", "위·아래: {a} × {b} 두 개"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "세 종류의 면의 넓이: {a} × {b} = {ab}, {b} × {c} = {bc}, {c} × {a} = {ca} (cm²)",
            "세 넓이의 합은 {ab} + {bc} + {ca} = {ab + bc + ca} (cm²)",
            "마주 보는 면이 각각 하나씩 더 있으므로 겉넓이 = 2 × {ab + bc + ca} = {S} (cm²)",
        ],
        sol2_fig=steps([
            {"text": "{a} × {b} + {b} × {c} + {c} × {a} = {ab + bc + ca}", "hint": "세 종류의 면"},
            {"text": "겉넓이 = 2 × {ab + bc + ca} = {S} (cm²)", "hint": "마주 보는 면은 두 개씩"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [], [reveal(1), hl("hint:1")]],
        sol_check="여섯 면을 하나씩 더해 보면 {ab} + {ab} + {bc} + {bc} + {ca} + {ca} = {S} (cm²)로 같다. 세 넓이의 합 {ab + bc + ca}만 답하면 절반이다. 답은 {S} cm²다.",
        model_answer="직육면체의 겉넓이는 2 × (가로 × 세로 + 세로 × 높이 + 높이 × 가로)이다. {a} × {b} = {ab}, {b} × {c} = {bc}, {c} × {a} = {ca}이므로 세 넓이의 합은 {ab + bc + ca} (cm²)이고, 겉넓이는 2 × {ab + bc + ca} = {S} (cm²)다.",
        rubric=[
            {"element": "면 구성", "points": 2, "criterion": "여섯 면이 세 종류의 직사각형 두 개씩임을 밝혔다.", "partial": "세 종류를 나열했으나 두 개씩임을 밝히지 않았으면 1점."},
            {"element": "넓이 계산", "points": 3, "criterion": "{a} × {b}, {b} × {c}, {c} × {a}{eul(a)} 각각 구하고 합 {ab + bc + ca}{eul(ab + bc + ca)} 얻었다.", "partial": "세 넓이 중 하나가 틀렸으면 1점."},
            {"element": "겉넓이", "points": 2, "criterion": "2배 하여 {S} cm²로 답했다.", "partial": "세 넓이의 합만 답했으면 1점."},
        ],
    )


def cyl_t5():
    return tpl("m1-2-cylinder-surface", 5, CYL,
        title="원기둥의 겉넓이 고르기 (5지선다)",
        skill="겉넓이 = 2πr² + 2πrh 를 정확히 세우기",
        variant_axis={"구하는 것": "겉넓이", "제시 방식": "반지름·높이", "출제 형식": "선다형"},
        discriminates="밑면 2개·옆면 가로 = 원주를 모두 반영한 값을 고르는가",
        qtype="choice", difficulty=2, pool_target=300, time_limit=60,
        params=[{"name": "r", "values": {"int": [2, 10]}}, {"name": "h", "values": {"int": [3, 15]}}],
        derive={"kb": "r*r", "kl": "2*r*h", "ks": "2*r*r + 2*r*h", "kc": "2*r"},
        constraints=["h != r", "ks <= 600"],
        cost_values=["r", "h", "kb", "kl", "ks"],
        relation="X - 2*r*r - 2*r*h", unknown="X", answer_var="ks",
        verify=["ks == 2*kb + kl"],
        question="밑면의 반지름의 길이가 {r} cm, 높이가 {h} cm인 원기둥의 겉넓이는?",
        figure=solid("cylinder", radius="{r}", height="{h}"),
        answer="[[{ks} * pi]]", answer_alt=["[[{ks} * pi]] cm²"],
        distractor_fmt=PI_FMT,
        distractors=[
            {"expr": "r*r + 2*r*h", "misconception": "MC-CYL-03"},
            {"expr": "2*r*r + r*h", "misconception": "MC-CYL-04"},
            {"expr": "r*r*h", "misconception": "MC-GEO-04"},
            {"expr": "2*r + 2*r*h", "misconception": "MC-CYL-01"},
            {"expr": "8*r*r + 4*r*h", "misconception": "MC-CYL-02"},
            {"expr": "2*r*r + 2*h", "misconception": "MC-CYL-04"},
            {"expr": "4*r*r + 2*r*h", "misconception": "MC-CALC-01"},
            {"expr": "2*r*r + 4*r*h", "misconception": "MC-CALC-01"},
        ],
        sol1="원기둥의 겉넓이는 (밑넓이) × 2 + (옆넓이)다. 밑면은 반지름 {r} cm인 원 2개, 옆면은 가로가 원주 2π × {r} = {kc}π (cm), 세로가 {h} cm인 직사각형이다.",
        sol1_fig=solid("cylinder", radius="{r}", height="{h}"),
        sol1_anim=[[hl("top", "base", "radius", "r-lbl")], [hl("height", "h-lbl", keep=True)]],
        sol2=[
            "(밑넓이) × 2 = π × {r}² × 2 = {2*kb}π (cm²)",
            "옆넓이 = 2π × {r} × {h} = {kl}π (cm²)",
            "겉넓이 = {2*kb}π + {kl}π = {ks}π (cm²)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 × 2 = {2*kb}π", "hint": "밑면은 두 개"},
            {"text": "옆넓이 = {kc}π × {h} = {kl}π", "hint": "가로 = 원주"},
            {"text": "겉넓이 = {ks}π (cm²)"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol_check="밑면을 하나만 세면 {kb + kl}π, 옆면의 가로를 반지름으로 잡으면 {2*kb + r*h}π가 되어 보기의 다른 값이 나온다. 답은 [[{ks} * pi]] cm²다.",
        model_answer="겉넓이 = (밑넓이) × 2 + (옆넓이) = π × {r}² × 2 + 2π × {r} × {h} = {2*kb}π + {kl}π = {ks}π (cm²)이다.",
        rubric=[
            {"element": "밑넓이", "points": 2, "criterion": "밑넓이 {kb}π를 구하고 밑면이 2개임을 반영했다.", "partial": "밑넓이는 옳으나 하나만 셌으면 1점."},
            {"element": "옆넓이", "points": 3, "criterion": "옆면의 가로가 원주 2π × {r}임을 밝히고 옆넓이 {kl}π를 구했다.", "partial": "가로를 원주로 잡지 못했으면 1점."},
            {"element": "겉넓이", "points": 2, "criterion": "{2*kb}π + {kl}π = {ks}π를 골랐다.", "partial": "식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


CYL_SEED = {
    "seed_id": "m1-2-cylinder-surface", "category": "도형",
    "title": "원기둥·직육면체의 겉넓이 — 구하기·역산·선다형",
    "unit_id": "m1-2", "concept_ids": ["m1-2-14"],
    "schema_id": SCHEMA_CYL_SURF, "schema_name": "원기둥의 겉넓이",
    "source_item_ids": [],
    "note": "관계식 S = 2πr² + 2πrh 와 변주축(구하는 것)만 차용. π는 기호로 보존. 직육면체 틀은 같은 개념(m1-2-14 기둥의 겉넓이)의 각기둥 판.",
    "geometry": True,
    "templates": [cyl_t1(), cyl_t2(), cyl_t3(), cyl_t4(), cyl_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 원뿔·각뿔
CONE = dict(prereq=["원기둥의 부피", "부채꼴의 호의 길이와 넓이"], ops=["부피", "넓이", "지수"], tags=["원뿔", "부피"])
# (r, l) 쌍 — 전개도 부채꼴의 중심각 360·r/l 이 정수인 것 (rl = r·100 + l)
RL_PAIRS = [(1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 5), (2, 9), (3, 4), (3, 5), (3, 8), (3, 10), (4, 5), (4, 9), (5, 6), (5, 8), (5, 9), (5, 12), (7, 8), (7, 9), (7, 10), (7, 12), (9, 10), (11, 12)]


def cone_t1():
    return tpl("m1-2-cone", 1, CONE,
        title="반지름·높이로 원뿔의 부피 구하기",
        skill="뿔의 부피 = (1/3) × (밑넓이) × (높이)",
        variant_axis={"구하는 것": "부피", "제시 방식": "반지름·높이"},
        discriminates="같은 밑면·높이의 기둥 부피의 1/3임을 알고 반지름을 제곱하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "w", "values": {"in": ["rad", "dia"]}}, {"name": "r", "values": {"int": [2, 12]}}, {"name": "k", "values": {"int": [1, 8]}}],
        table={"key": "w", "rows": {"rad": {"GIVEN": "반지름", "isD": 0, "RL": "r"}, "dia": {"GIVEN": "지름", "isD": 1, "RL": "r"}}},
        derive={"h": "3*k", "g": "r*(1 + isD)", "kb": "r*r", "kv": "r*r*k", "kc": "r*r*3*k"},
        constraints=["h != r", "h != g", "kv <= 900", "kv != h", "kv != g"],
        cost_values=["r", "g", "h", "kb", "kc", "kv"],
        relation="3*X - r*r*h", unknown="X", answer_var="kv",
        verify=["3*ans == kb*h", "ans > 0", "g == r*(1 + isD)"],
        question="다음 그림과 같이 밑면의 {GIVEN}의 길이가 {g} cm, 높이가 {h} cm인 원뿔의 부피를 구하시오.",
        figure=solid("cone", radius="{RL}", height="{h}"),
        answer="[[{kv} * pi]]", answer_alt=["[[{kv} * pi]] cm³"],
        sol1="뿔의 부피는 밑면과 높이가 같은 기둥의 부피의 1/3이다 — 그릇에 물을 부어 보면 뿔 세 번이 기둥 한 번과 같다. 주어진 것은 밑면의 {GIVEN} {g} cm이므로 반지름은 {r} cm이고, 밑넓이는 π × {r}² = {kb}π (cm²), 높이는 {h} cm다.",
        sol1_fig=solid("cone", radius="{r}", height="{h}"),
        sol1_anim=[[hl("radius", "r-lbl")], [hl("height", "h-lbl", keep=True)]],
        sol2=[
            "밑면의 반지름은 {r} cm이므로 밑넓이: π × {r}² = {kb}π (cm²)",
            "같은 밑면·높이의 원기둥의 부피: {kb}π × {h} = {kc}π (cm³)",
            "원뿔의 부피는 그 1/3이므로 {kc}π × 1/3 = {kv}π (cm³)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 = π × {r}² = {kb}π", "hint": "{GIVEN} {g} cm → 반지름 {r} cm, 제곱"},
            {"text": "원기둥 부피 = {kb}π × {h} = {kc}π"},
            {"text": "원뿔 부피 = {kc}π × 1/3 = {kv}π (cm³)", "hint": "뿔은 기둥의 1/3", "marks": [{"on": "{kv}π", "note": "{kc}÷3"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol_check="1/3을 빠뜨리면 원기둥의 부피 {kc}π가 나오고, 반지름을 제곱하지 않으면 {r*k}π가 나온다 — 둘 다 답이 아니다. 답은 [[{kv} * pi]] cm³다.",
        model_answer="원뿔의 부피는 (1/3) × (밑넓이) × (높이)이다. 밑면의 반지름은 {r} cm이므로 밑넓이는 π × {r}² = {kb}π (cm²)이고, 부피는 (1/3) × {kb}π × {h} = {kv}π (cm³)다.",
        rubric=[
            {"element": "부피 공식", "points": 2, "criterion": "뿔의 부피 = (1/3) × (밑넓이) × (높이)임을 밝혔다.", "partial": "1/3 없이 기둥의 공식을 썼으면 인정하지 않는다."},
            {"element": "밑넓이", "points": 2, "criterion": "반지름 {r} cm를 확인하고 π × {r}² = {kb}π로 제곱해 구했다.", "partial": "제곱을 빠뜨리거나 지름을 반지름으로 썼으면 인정하지 않는다."},
            {"element": "부피 계산", "points": 3, "criterion": "(1/3) × {kb}π × {h} = {kv}π (cm³)를 바르게 계산했다.", "partial": "식은 옳으나 약분·계산이 틀렸으면 1점."},
        ],
    )


def cone_t2():
    return tpl("m1-2-cone", 2, CONE,
        title="반지름·모선으로 원뿔의 겉넓이 구하기",
        skill="원뿔의 겉넓이 = πr² + πrl (옆넓이는 반지름이 모선인 부채꼴의 넓이 = (1/2) × l × 2πr)",
        variant_axis={"구하는 것": "겉넓이", "제시 방식": "반지름·모선"},
        discriminates="옆넓이를 모선 l로 계산하는가(높이가 아니라), 밑면을 더하는가",
        qtype="short", difficulty=3, pool_target=300, tags=["원뿔", "겉넓이"],
        params=[{"name": "rl", "values": {"in": [r * 100 + l for r, l in RL_PAIRS]}}, {"name": "k", "values": {"int": [1, 3]}}],
        derive={"r": "k*floor(rl/100)", "l": "k*(rl % 100)", "kb": "(k*floor(rl/100))**2", "kl": "k*floor(rl/100)*k*(rl % 100)", "ks": "(k*floor(rl/100))**2 + k*floor(rl/100)*k*(rl % 100)", "th": "360*floor(rl/100)/(rl % 100)"},
        constraints=["ks <= 900", "r >= 2", "ks != l", "ks != r"],
        cost_values=["r", "l", "kb", "kl", "ks"],
        relation="X - r*r - r*l", unknown="X", answer_var="ks",
        verify=["ans == kb + kl", "kl == r*l"],
        question="밑면의 반지름의 길이가 {r} cm, 모선의 길이가 {l} cm인 원뿔의 겉넓이를 구하시오.",
        figure=solid("cone", radius="{r}"),
        answer="[[{ks} * pi]]", answer_alt=["[[{ks} * pi]] cm²"],
        sol1="원뿔을 펼치면 밑면인 원(반지름 {r} cm)과 옆면인 부채꼴이 나온다. 부채꼴의 반지름은 모선의 길이 {l} cm이고, 호의 길이는 밑면의 원주 2π × {r} = {2*r}π (cm)와 같다. 부채꼴의 넓이는 (1/2) × (반지름) × (호의 길이)이므로 옆넓이 = (1/2) × {l} × {2*r}π = π × {r} × {l}이다. 겉넓이 = (밑넓이) + (옆넓이).",
        sol1_fig=[{"fn": "sector", "args": {"r": "{l}", "angle": "{th}"}}, {"fn": "circle", "args": {"r": "{r}"}}],
        sol1_anim=[[hl("radius", "r-lbl")], [hl("arc", keep=True)], [hl("sector")]],
        sol2=[
            "밑넓이: π × {r}² = {kb}π (cm²)",
            "옆넓이: 부채꼴의 넓이 = (1/2) × (모선) × (호의 길이) = (1/2) × {l} × 2π × {r} = π × {r} × {l} = {kl}π (cm²)",
            "겉넓이 = {kb}π + {kl}π = {ks}π (cm²)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 = π × {r}² = {kb}π"},
            {"text": "옆넓이 = π × {r} × {l} = {kl}π", "hint": "πrl — 반지름 × 모선", "marks": [{"on": "{kl}π", "note": "{r}×{l}"}]},
            {"text": "겉넓이 = {kb}π + {kl}π = {ks}π (cm²)"},
        ]),
        sol2_anim=[[reveal(0)], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="옆넓이를 π × {r}² 처럼 반지름만으로 계산하거나 밑면을 빠뜨리면 다른 값이 나온다. 부채꼴의 중심각은 360° × {r}/{l} = {th}°이고 그 넓이는 π × {l}² × {th}/360 = {kl}π로 같다. 답은 [[{ks} * pi]] cm²다.",
        model_answer="원뿔의 겉넓이는 (밑넓이) + (옆넓이)이다. 밑넓이는 π × {r}² = {kb}π (cm²), 옆넓이는 반지름이 모선 {l} cm이고 호의 길이가 밑면의 원주 2π × {r}인 부채꼴의 넓이이므로 (1/2) × {l} × 2π × {r} = {kl}π (cm²)이다. 따라서 겉넓이는 {kb}π + {kl}π = {ks}π (cm²)다.",
        rubric=[
            {"element": "전개도 읽기", "points": 3, "criterion": "옆면이 반지름 {l}(모선), 호의 길이 2π × {r}(밑면의 원주)인 부채꼴임을 밝혔다.", "partial": "부채꼴임은 밝혔으나 호의 길이가 밑면의 원주와 같다는 근거가 없으면 1점."},
            {"element": "옆넓이", "points": 2, "criterion": "(1/2) × {l} × 2π × {r} = {kl}π(또는 π × {r} × {l})를 구했다.", "partial": "모선 대신 다른 길이를 썼으면 인정하지 않는다."},
            {"element": "겉넓이", "points": 2, "criterion": "밑넓이 {kb}π를 더해 {ks}π (cm²)로 답했다.", "partial": "밑넓이를 빠뜨렸으면 1점."},
        ],
    )


def cone_t3():
    return tpl("m1-2-cone", 3, CONE,
        title="원뿔의 전개도에서 부채꼴의 중심각 구하기",
        skill="(부채꼴의 호의 길이) = (밑면의 원주) 로부터 중심각 = 360° × r/l",
        variant_axis={"구하는 것": "중심각", "제시 방식": "반지름·모선"},
        discriminates="옆면 부채꼴의 호의 길이가 밑면의 원주와 같다는 조건을 세우는가",
        qtype="short", difficulty=3, pool_target=300, tags=["원뿔", "전개도", "중심각"], process="추론",
        params=[{"name": "rl", "values": {"in": [r * 100 + l for r, l in RL_PAIRS]}}, {"name": "k", "values": {"int": [1, 4]}}],
        derive={"r": "k*floor(rl/100)", "l": "k*(rl % 100)", "th": "360*floor(rl/100)/(rl % 100)", "kc": "2*k*floor(rl/100)", "kl2": "2*k*(rl % 100)"},
        constraints=["r >= 2", "th != r", "th != l", "l <= 48"],
        cost_values=["r", "l", "th", "kc", "kl2"],
        relation="2*l*X/360 - 2*r", unknown="X", answer_var="th",
        verify=["ans*l == 360*r", "ans < 360"],
        question="밑면의 반지름의 길이가 {r} cm, 모선의 길이가 {l} cm인 원뿔의 전개도에서 옆면인 부채꼴의 중심각의 크기를 구하시오.",
        figure=solid("cone", radius="{r}"),
        answer="[[deg({th})]]", answer_alt=["{th}°", "{th}"],
        sol1="옆면을 펼친 부채꼴은 반지름이 모선 {l} cm이고, 그 호를 말면 밑면의 둘레가 되므로 호의 길이는 밑면의 원주 2π × {r} = {kc}π (cm)와 같다. 중심각을 x°라 하면 호의 길이 = 2π × {l} × x/360이므로 이것을 {kc}π와 같다고 놓는다.",
        sol1_fig=[{"fn": "sector", "args": {"r": "{l}", "angle": "x"}}, {"fn": "circle", "args": {"r": "{r}"}}],
        sol1_anim=[[hl("arc", keep=True)], [hl("angle-lbl")], [hl("radius", "r-lbl")]],
        sol2=[
            "중심각을 x°라 하면 부채꼴의 호의 길이는 2π × {l} × x/360 = {kl2}π × x/360 (cm)",
            "이 호의 길이가 밑면의 원주 2π × {r} = {kc}π (cm)와 같으므로 {kl2}π × x/360 = {kc}π",
            "양변을 π로 나누고 정리하면 x = 360 × {kc}/{kl2} = 360 × {r}/{l} = {th}",
        ],
        sol2_fig=steps([
            {"text": "2π × {l} × x/360 = 2π × {r}", "hint": "호의 길이 = 밑면의 원주"},
            {"text": "x = 360 × {r}/{l}", "hint": "양변 ÷ 2π, × 360, ÷ {l}"},
            {"text": "x = {th}", "marks": [{"on": "{th}", "note": "360×{r}÷{l}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="중심각 {th}°인 반지름 {l} cm 부채꼴의 호의 길이는 2π × {l} × {th}/360 = {kc}π (cm)로 밑면의 원주와 같다. 중심각은 (반지름) : (모선) = {r} : {l}의 비율로 360°를 나눈 것이다. 답은 [[deg({th})]]다.",
        model_answer="옆면인 부채꼴의 반지름은 모선 {l} cm이고 호의 길이는 밑면의 원주 2π × {r} = {kc}π (cm)와 같다. 중심각을 x°라 하면 2π × {l} × x/360 = 2π × {r}에서 x = 360 × {r}/{l} = {th}이다. 따라서 중심각의 크기는 {th}°다.",
        rubric=[
            {"element": "조건 세우기", "points": 3, "criterion": "부채꼴의 호의 길이가 밑면의 원주 2π × {r}{wa(r)} 같음을 밝혔다.", "partial": "호의 길이 공식만 쓰고 밑면의 원주와 같다는 조건이 없으면 1점."},
            {"element": "방정식 풀이", "points": 2, "criterion": "2π × {l} × x/360 = 2π × {r}{eul(r)} 풀어 x = 360 × {r}/{l}{eul(l)} 얻었다.", "partial": "식은 세웠으나 정리가 틀렸으면 1점."},
            {"element": "중심각", "points": 2, "criterion": "중심각 {th}°를 구하고 단위(°)와 함께 썼다.", "partial": "약분·계산 실수면 1점."},
        ],
    )


def cone_t4():
    return tpl("m1-2-cone", 4, CONE,
        title="정사각뿔의 부피 구하기",
        skill="뿔의 부피 = (1/3) × (밑넓이) × (높이), 밑면이 정사각형이면 밑넓이 = a²",
        variant_axis={"구하는 것": "부피", "입체": "정사각뿔"},
        discriminates="밑넓이를 한 변의 제곱으로 구하고 1/3을 곱하는가",
        qtype="short", difficulty=2, pool_target=300, tags=["사각뿔", "부피"],
        params=[{"name": "a", "values": {"int": [2, 14]}}, {"name": "k", "values": {"int": [1, 8]}}],
        derive={"h": "3*k", "kb": "a*a", "kv": "a*a*k", "kc": "a*a*3*k"},
        constraints=["h != a", "kv <= 900", "kv != a", "kv != h"],
        cost_values=["a", "h", "kb", "kc", "kv"],
        relation="3*X - a*a*h", unknown="X", answer_var="kv",
        verify=["3*ans == kb*h"],
        question="밑면이 한 변의 길이가 {a} cm인 정사각형이고 높이가 {h} cm인 사각뿔의 부피를 구하시오.",
        figure=solid("square_pyramid"),
        answer="{kv}", answer_alt=["{kv} cm³"],
        sol1="뿔의 부피는 밑면과 높이가 같은 기둥의 부피의 1/3이다. 밑면은 한 변이 {a} cm인 정사각형이므로 밑넓이는 {a} × {a} = {kb} (cm²)이고, 높이는 {h} cm다.",
        sol1_fig=solid("square_pyramid"),
        sol2=[
            "밑넓이: {a} × {a} = {kb} (cm²)",
            "같은 밑면·높이의 사각기둥의 부피: {kb} × {h} = {kc} (cm³)",
            "사각뿔의 부피는 그 1/3이므로 {kc} × 1/3 = {kv} (cm³)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 = {a}² = {kb}"},
            {"text": "기둥 부피 = {kb} × {h} = {kc}"},
            {"text": "뿔 부피 = {kc} × 1/3 = {kv} (cm³)", "hint": "뿔은 기둥의 1/3", "marks": [{"on": "{kv}", "note": "{kc}÷3"}]},
        ]),
        sol2_anim=[[reveal(0)], [reveal(1)], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol_check="1/3을 빠뜨리면 사각기둥의 부피 {kc} cm³가 나온다. 답은 {kv} cm³다.",
        model_answer="사각뿔의 부피는 (1/3) × (밑넓이) × (높이)이다. 밑넓이는 {a} × {a} = {kb} (cm²)이므로 부피는 (1/3) × {kb} × {h} = {kv} (cm³)다.",
        rubric=[
            {"element": "부피 공식", "points": 2, "criterion": "뿔의 부피 = (1/3) × (밑넓이) × (높이)임을 밝혔다.", "partial": "1/3 없이 기둥의 공식을 썼으면 인정하지 않는다."},
            {"element": "밑넓이", "points": 2, "criterion": "{a} × {a} = {kb}{eul(kb)} 구했다.", "partial": "한 변의 길이를 그대로 넓이로 썼으면 인정하지 않는다."},
            {"element": "부피 계산", "points": 3, "criterion": "(1/3) × {kb} × {h} = {kv} (cm³)를 바르게 계산했다.", "partial": "식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


def cone_t5():
    return tpl("m1-2-cone", 5, CONE,
        title="원뿔의 부피 고르기 (5지선다)",
        skill="뿔의 부피 = (1/3) × πr² × h",
        variant_axis={"구하는 것": "부피", "출제 형식": "선다형"},
        discriminates="1/3과 반지름의 제곱을 모두 반영한 값을 고르는가",
        qtype="choice", difficulty=2, pool_target=300, time_limit=60,
        params=[{"name": "r", "values": {"int": [2, 10]}}, {"name": "k", "values": {"int": [1, 6]}}],
        derive={"h": "3*k", "kb": "r*r", "kv": "r*r*k", "kc": "r*r*3*k"},
        constraints=["h != r", "kv <= 500"],
        cost_values=["r", "h", "kb", "kc", "kv"],
        relation="3*X - r*r*h", unknown="X", answer_var="kv",
        verify=["3*ans == kb*h"],
        question="밑면의 반지름의 길이가 {r} cm, 높이가 {h} cm인 원뿔의 부피는?",
        figure=solid("cone", radius="{r}", height="{h}"),
        answer="[[{kv} * pi]]", answer_alt=["[[{kv} * pi]] cm³"],
        distractor_fmt=PI_FMT,
        distractors=[
            {"expr": "r*r*h", "misconception": "MC-CONE-01"},
            {"expr": "r*k", "misconception": "MC-CYL-01"},
            {"expr": "r*h", "misconception": "MC-CYL-01"},
            {"expr": "4*r*r*k", "misconception": "MC-CYL-02"},
            {"expr": "r*r*h*2/3", "misconception": "MC-CALC-01"},
            {"expr": "r*r + h", "misconception": "MC-GEO-04"},
            {"expr": "r*r*k + r", "misconception": "MC-CALC-01"},
            {"expr": "2*r*h", "misconception": "MC-GEO-04"},
        ],
        sol1="뿔의 부피는 같은 밑면·높이의 기둥의 1/3이다. 밑넓이는 π × {r}² = {kb}π (cm²), 높이는 {h} cm다.",
        sol1_fig=solid("cone", radius="{r}", height="{h}"),
        sol1_anim=[[hl("radius", "r-lbl")], [hl("height", "h-lbl", keep=True)]],
        sol2=[
            "밑넓이: π × {r}² = {kb}π (cm²)",
            "부피 = (1/3) × {kb}π × {h} = {kv}π (cm³)",
        ],
        sol2_fig=steps([
            {"text": "밑넓이 = π × {r}² = {kb}π", "hint": "반지름을 제곱"},
            {"text": "부피 = (1/3) × {kb}π × {h} = {kv}π", "hint": "뿔은 기둥의 1/3", "marks": [{"on": "{kv}π", "note": "{kc}÷3"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol_check="1/3을 빠뜨리면 {kc}π(원기둥의 부피), 반지름을 제곱하지 않으면 {r*k}π가 되어 보기의 다른 값이 나온다. 답은 [[{kv} * pi]] cm³다.",
        model_answer="원뿔의 부피 = (1/3) × (밑넓이) × (높이) = (1/3) × π × {r}² × {h} = {kv}π (cm³)이다.",
        rubric=[
            {"element": "부피 공식", "points": 2, "criterion": "(1/3) × (밑넓이) × (높이)를 썼다.", "partial": "1/3이 없으면 인정하지 않는다."},
            {"element": "밑넓이", "points": 2, "criterion": "π × {r}² = {kb}π를 구했다.", "partial": "제곱을 빠뜨렸으면 인정하지 않는다."},
            {"element": "부피 계산", "points": 3, "criterion": "{kv}π를 골랐다.", "partial": "식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


CONE_SEED = {
    "seed_id": "m1-2-cone", "category": "도형",
    "title": "원뿔·각뿔 — 부피·겉넓이·전개도의 중심각",
    "unit_id": "m1-2", "concept_ids": ["m1-2-15"],
    "schema_id": SCHEMA_CONE_VOL, "schema_name": "원뿔의 부피 / 원뿔의 겉넓이 / 원뿔 전개도 부채꼴 중심각",
    "source_item_ids": [],
    "note": "관계식 V = (1/3)πr²h, S = πr² + πrl, θ = 360·r/l 만 차용. 높이는 3의 배수로 생성해 정수 계수 보장, (r, l)은 중심각이 정수인 쌍만 표로. 전개도 도식은 sector + circle.",
    "geometry": True,
    "templates": [cone_t1(), cone_t2(), cone_t3(), cone_t4(), cone_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 구
SPH = dict(prereq=["원의 넓이", "원기둥의 부피"], ops=["부피", "넓이", "지수"], tags=["구", "겉넓이", "부피"])


def sph_t1():
    return tpl("m1-2-sphere", 1, SPH,
        title="구·반구의 겉넓이 구하기",
        skill="구의 겉넓이 = 4πr², 반구의 겉넓이 = 2πr²(곡면) + πr²(단면)",
        variant_axis={"구하는 것": "겉넓이", "입체": "구 / 반구"},
        discriminates="구의 겉넓이 공식 4πr²을 쓰고, 반구이면 곡면의 절반에 단면인 원을 더하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "w", "values": {"in": ["ball", "half"]}}, {"name": "r", "values": {"int": [2, 16]}}],
        table={"key": "w", "rows": {"ball": {"KIND": "구", "isH": 0, "SK": "sphere"}, "half": {"KIND": "반구", "isH": 1, "SK": "hemisphere"}}},
        derive={"k4": "4*r*r", "k2": "2*r*r", "k1": "r*r", "ks": "4*r*r*(1 - isH) + 3*r*r*isH"},
        constraints=["ks != r", "ks <= 900"],
        cost_values=["r", "k4", "k2", "k1", "ks"],
        answer_var="ks",
        verify=["(isH == 0 and ans == 4*r*r) or (isH == 1 and ans == 3*r*r)"],
        question="반지름의 길이가 {r} cm인 {KIND}의 겉넓이를 구하시오.",
        figure=[{"fn": "solid", "args": {"kind": "{SK}", "radius": "{r}"}}],
        answer="[[{ks} * pi]]", answer_alt=["[[{ks} * pi]] cm²"],
        sol1="구의 겉넓이는 반지름이 같은 원의 넓이의 4배, 곧 4πr²이다. 반구는 구를 반으로 자른 것이므로 곡면의 넓이는 4πr²의 절반 2πr²이고, 잘린 단면인 원(넓이 πr²)이 새로 생긴다 — 반구의 겉넓이는 이 둘의 합이다.",
        sol1_fig=[{"fn": "solid", "args": {"kind": "{SK}", "radius": "{r}"}}],
        sol2=[
            "구의 겉넓이: 4π × {r}² = {k4}π (cm²)",
            "반구라면 곡면은 그 절반 {k2}π (cm²)이고 단면인 원 π × {r}² = {k1}π (cm²)가 더해져 {k2}π + {k1}π = {3*k1}π (cm²)",
            "따라서 {KIND}의 겉넓이는 {ks}π (cm²)이다.",
        ],
        sol2_fig=steps([
            {"text": "구: 4π × {r}² = {k4}π", "hint": "원의 넓이의 4배"},
            {"text": "반구: 2π × {r}² + π × {r}² = {k2}π + {k1}π = {3*k1}π", "hint": "곡면 절반 + 단면 원"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], []],
        sol_check="반구에서 단면인 원을 빠뜨리면 {k2}π, 구인데 반으로 나누면 {k2}π가 나온다. 답은 [[{ks} * pi]] cm²다.",
        model_answer="구의 겉넓이는 4πr²이므로 반지름 {r} cm인 구의 겉넓이는 4π × {r}² = {k4}π (cm²)이고, 반구의 겉넓이는 곡면 2π × {r}² = {k2}π에 단면인 원의 넓이 π × {r}² = {k1}π를 더한 {3*k1}π (cm²)이다. 따라서 {KIND}의 겉넓이는 {ks}π cm²다.",
        rubric=[
            {"element": "공식", "points": 2, "criterion": "구의 겉넓이 = 4πr²임을 밝혔다." , "partial": "πr² 이나 2πr² 처럼 다른 식을 쓰면 인정하지 않는다."},
            {"element": "구성 파악", "points": 3, "criterion": "{KIND}의 겉넓이를 이루는 면(구: 곡면 전체 / 반구: 곡면의 절반 + 단면인 원)을 빠짐없이 밝혔다.", "partial": "반구에서 단면인 원을 빠뜨렸으면 1점."},
            {"element": "겉넓이 계산", "points": 2, "criterion": "{ks}π (cm²)로 바르게 계산했다.", "partial": "식은 옳으나 계산이 틀렸으면 1점."},
        ],
    )


def sph_t2():
    return tpl("m1-2-sphere", 2, SPH,
        title="구·반구의 부피 구하기",
        skill="구의 부피 = (4/3)πr³, 반구의 부피는 그 절반",
        variant_axis={"구하는 것": "부피", "입체": "구 / 반구", "제시 방식": "반지름 / 지름"},
        discriminates="반지름을 세제곱하고 4/3을 곱하는가, 지름이 주어지면 반으로 나누는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "w", "values": {"in": ["ball-r", "half-r", "ball-d", "half-d"]}}, {"name": "m", "values": {"int": [1, 6]}}],
        table={"key": "w", "rows": {
            "ball-r": {"KIND": "구", "isH": 0, "SK": "sphere", "GIVEN": "반지름", "isD": 0},
            "half-r": {"KIND": "반구", "isH": 1, "SK": "hemisphere", "GIVEN": "반지름", "isD": 0},
            "ball-d": {"KIND": "구", "isH": 0, "SK": "sphere", "GIVEN": "지름", "isD": 1},
            "half-d": {"KIND": "반구", "isH": 1, "SK": "hemisphere", "GIVEN": "지름", "isD": 1},
        }},
        derive={"r": "3*m", "g": "3*m*(1 + isD)", "k3": "27*m*m*m", "kv4": "36*m*m*m", "kv": "36*m*m*m*(1 - isH) + 18*m*m*m*isH"},
        constraints=["kv <= 8000", "kv != g"],
        cost_values=["r", "g", "k3", "kv4", "kv"],
        answer_var="kv",
        verify=["3*ans == 4*r*r*r*(1 - isH) + 2*r*r*r*isH", "g == r*(1 + isD)"],
        question="{GIVEN}의 길이가 {g} cm인 {KIND}의 부피를 구하시오.",
        figure=[{"fn": "solid", "args": {"kind": "{SK}", "radius": "r"}}],
        answer="[[{kv} * pi]]", answer_alt=["[[{kv} * pi]] cm³"],
        sol1="구의 부피는 (4/3)πr³이다 — 반지름이 r인 원기둥(높이 2r)에 꼭 맞는 구의 부피가 원기둥의 2/3라는 사실에서 나온다. 반구는 그 절반이다. 주어진 것이 {GIVEN}이므로 먼저 반지름 r = {r} cm를 확인한다. 세제곱한 뒤 4/3배 하는 순서로 처리한다.",
        sol1_fig=[{"fn": "solid", "args": {"kind": "{SK}", "radius": "{r}"}}],
        sol2=[
            "반지름은 r = {r} cm이다. ({GIVEN} {g} cm)",
            "구의 부피: (4/3)π × {r}³ = (4/3)π × {k3} = {kv4}π (cm³)",
            "{KIND}의 부피: {kv}π (cm³)",
        ],
        sol2_fig=steps([
            {"text": "r = {r}", "hint": "{GIVEN} {g} cm에서"},
            {"text": "구의 부피 = (4/3)π × {r}³ = (4/3) × {k3}π = {kv4}π", "hint": "세제곱 먼저, 4/3은 마지막에", "marks": [{"on": "{k3}π", "note": "{r}×{r}×{r}"}]},
            {"text": "{KIND}의 부피 = {kv}π (cm³)"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol_check="4/3 없이 πr³만 구하면 {k3}π, 반지름을 제곱만 하면 {4*r*r}π/3 꼴이 되어 답이 아니다. 답은 [[{kv} * pi]] cm³다.",
        model_answer="{GIVEN}의 길이가 {g} cm이므로 반지름의 길이는 {r} cm이다. 구의 부피는 (4/3)πr³이므로 (4/3)π × {r}³ = {kv4}π (cm³)이고, 반구의 부피는 그 절반 {18*m*m*m}π (cm³)이다. 따라서 {KIND}의 부피는 {kv}π cm³다.",
        rubric=[
            {"element": "반지름과 공식", "points": 2, "criterion": "반지름 r = {r} cm를 확인하고 구의 부피 = (4/3)πr³임을 밝혔다.", "partial": "지름을 반지름으로 썼거나 4/3이 없으면 인정하지 않는다."},
            {"element": "부피 계산", "points": 3, "criterion": "(4/3)π × {r}³ = {kv4}π (cm³)를 바르게 계산했다.", "partial": "세제곱까지 옳고 4/3 곱셈이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{KIND}의 부피 {kv}π (cm³)를 답했다.", "partial": "반구인데 반으로 나누지 않았으면 인정하지 않는다."},
        ],
    )


def sph_t3():
    return tpl("m1-2-sphere", 3, SPH,
        title="원기둥에 꼭 맞는 구의 부피 (원기둥 부피에서 구하기)",
        skill="원기둥에 꼭 맞는 구의 부피는 원기둥 부피의 2/3 (원뿔 : 구 : 원기둥 = 1 : 2 : 3)",
        variant_axis={"구하는 것": "구의 부피", "주어진 정보": "원기둥의 부피", "관계": "1:2:3"},
        discriminates="구가 꼭 맞는 원기둥은 높이가 지름(2r)임을 알고 부피비 2/3을 쓰는가",
        qtype="short", difficulty=3, pool_target=300, process="추론", tags=["구", "원기둥", "부피의 비"],
        params=[{"name": "m", "values": {"int": [4, 60]}}],
        derive={"V": "3*m", "kv": "2*m", "kc": "m"},
        constraints=["kv != V"],
        cost_values=["V", "kv", "kc"],
        relation="3*X - 2*V", unknown="X", answer_var="kv",
        verify=["3*ans == 2*V"],
        question="다음 그림과 같이 구가 원기둥에 꼭 맞게 들어 있다. 원기둥의 부피가 [[{V} * pi]] cm³일 때, 구의 부피를 구하시오.",
        figure=solid("cylinder", radius="r"),
        answer="[[{kv} * pi]]", answer_alt=["[[{kv} * pi]] cm³"],
        sol1="구가 원기둥에 꼭 맞으면 원기둥의 밑면의 반지름은 구의 반지름 r과 같고 높이는 지름 2r이다. 그러면 원기둥의 부피는 πr² × 2r = 2πr³, 구의 부피는 (4/3)πr³이므로 (구) : (원기둥) = (4/3) : 2 = 2 : 3 — 구의 부피는 원기둥 부피의 2/3이다. (원뿔까지 넣으면 1 : 2 : 3.)",
        sol1_fig=steps(["원기둥: πr² × 2r = 2πr³", "구: (4/3)πr³", "원뿔: (1/3)πr² × 2r = (2/3)πr³   → 1 : 2 : 3"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "구의 반지름을 r cm라 하면 원기둥은 밑면의 반지름 r cm, 높이 2r cm이므로 부피는 πr² × 2r = 2πr³ (cm³)",
            "구의 부피는 (4/3)πr³ (cm³)이므로 (구의 부피) = (원기둥의 부피) × 2/3",
            "원기둥의 부피가 {V}π cm³이므로 구의 부피는 {V}π × 2/3 = {kv}π (cm³)",
        ],
        sol2_fig=steps([
            {"text": "원기둥 = 2πr³,  구 = (4/3)πr³", "hint": "높이 = 지름 2r"},
            {"text": "구 = 원기둥 × 2/3", "hint": "(4/3) ÷ 2 = 2/3"},
            {"text": "{V}π × 2/3 = {kv}π (cm³)", "marks": [{"on": "{kv}π", "note": "{V}÷3×2"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol_check="원기둥에 꼭 맞는 원뿔의 부피는 원기둥의 1/3인 {kc}π, 구는 2/3인 {kv}π로 1 : 2 : 3이 맞는다. 답은 [[{kv} * pi]] cm³다.",
        model_answer="구의 반지름을 r cm라 하면 원기둥의 밑면의 반지름은 r cm, 높이는 2r cm이므로 원기둥의 부피는 2πr³ (cm³)이고 구의 부피는 (4/3)πr³ (cm³)이다. 따라서 구의 부피는 원기둥의 부피의 2/3이고, {V}π × 2/3 = {kv}π (cm³)다.",
        rubric=[
            {"element": "원기둥의 치수", "points": 2, "criterion": "구가 꼭 맞으므로 원기둥의 높이가 지름 2r임을 밝혔다.", "partial": "높이를 r로 잡았으면 인정하지 않는다."},
            {"element": "부피의 비", "points": 3, "criterion": "2πr³과 (4/3)πr³을 비교해 구의 부피가 원기둥의 2/3임을 보였다.", "partial": "두 부피는 구했으나 비를 잘못 냈으면 1점."},
            {"element": "구의 부피", "points": 2, "criterion": "{V}π × 2/3 = {kv}π (cm³)를 구했다.", "partial": "비는 옳으나 계산이 틀렸으면 1점."},
        ],
    )


SPHERE_SEED = {
    "seed_id": "m1-2-sphere", "category": "도형",
    "title": "구 — 겉넓이·부피·원기둥에 꼭 맞는 구",
    "unit_id": "m1-2", "concept_ids": ["m1-2-16"],
    "schema_id": SCHEMA_SPHERE, "schema_name": "원기둥에 꼭 맞는 구·원뿔 부피 관계 / 구의 겉넓이와 부피",
    "source_item_ids": [],
    "note": "관계식 S = 4πr², V = (4/3)πr³, 구 : 원기둥 = 2 : 3 만 차용. 반지름은 3의 배수로 생성해 정수 계수 보장. 부피비 틀은 원기둥 부피를 3의 배수로 생성.",
    "geometry": True,
    "templates": [sph_t1(), sph_t2(), sph_t3()],
}


if __name__ == "__main__":
    for seed in (CYL_SEED, CONE_SEED, SPHERE_SEED):
        with_pitfalls(seed)
        dump(seed)
