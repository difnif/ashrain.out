# itemfactory/tools/mkseed_m3_trig.py — m3-2 삼각비 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m3_trig.py
#     → seeds/m3-2-trig-basic.json  (삼각비의 뜻·특수각·삼각비 표: 직각삼각형 삼각비·삼각비→삼각비·특수각 계산·특수각 방정식·표 이용, 5틀)
#     → seeds/m3-2-trig-apply.json  (삼각비의 활용: 특수각 변의 길이·높이 측정·삼각형 넓이·두 변 끼인각→대변·사각형 넓이, 5틀)
#
# 무리수 답은 표에서 미리 문자열로 만든다: ANS_T = '[[3*sqrt(3)]]' (answer_var 없음 → 독립 검산은 check_m3str 로 float 비교).
# 유리수 답은 an/ad 파생(Fraction). 도형은 scene — 좌표는 실제 각·길이대로(표에 float).
from __future__ import annotations

import math
import os
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mkseed_m2_geo1 import arc, scene  # noqa: E402
from mkseed_m2_geo2 import lseg  # noqa: E402
from seedlib import COMMON_APPLY, dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def geo(t: dict) -> dict:
    """문항 그림이 있는 틀은 기하(2단 해설: sol3 → sol_check), 없는 틀은 비기하(3단)로 표시."""
    if t.get("figure"):
        t["geometry"] = True
        if "sol3" in t:
            t["sol_check"] = t.pop("sol3")
        t.pop("sol3_fig", None)
        t.pop("sol3_anim", None)
    else:
        t["geometry"] = False
    return t


def sqfree(n: int):
    a, b = 1, n
    p = 2
    while p * p <= b:
        while b % (p * p) == 0:
            b //= p * p
            a *= p
        p += 1
    return a, b


def rad(coef: Fraction, m: int) -> str:
    """coef·√m 의 mathir 본문: (3/2, 2) → 'frac(3*sqrt(2), 2)', (2, 1) → '2', (1/3, 3) → 'frac(sqrt(3), 3)'"""
    coef = Fraction(coef)
    a, b = sqfree(m)
    coef, m = coef * a, b
    if m == 1:
        return str(coef.numerator) if coef.denominator == 1 else f"frac({coef.numerator}, {coef.denominator})"
    num = f"sqrt({m})" if abs(coef.numerator) == 1 else f"{abs(coef.numerator)}*sqrt({m})"
    if coef.numerator < 0:
        num = "-" + num
    return num if coef.denominator == 1 else f"frac({num}, {coef.denominator})"


def mk(coef, m) -> str:
    """답·문면용 마커: 유리수면 마커 없이, 무리수면 [[…]]"""
    s = rad(Fraction(coef), m)
    return f"[[{s}]]" if "sqrt" in s or "frac" in s else s


def val(coef, m) -> float:
    return float(Fraction(coef)) * math.sqrt(m)


def exposed(ans_t: str, *texts: str) -> bool:
    """정수 답이 문면(주어진 값 문자열)에 그대로 나오면 True — audit F1 과 같은 규칙."""
    a = re.sub(r"^\[\[|\]\]$", "", str(ans_t))
    if not re.fullmatch(r"-?\d+", a):
        return False
    return any(re.search(rf"(?<![\d\-\u2212.]){re.escape(a)}(?!\d|\.\d)", t) for t in texts)


# 특수각 삼각비 (coef, radicand)
SPECIAL = {
    ("sin", 30): (Fraction(1, 2), 1), ("cos", 30): (Fraction(1, 2), 3), ("tan", 30): (Fraction(1, 3), 3),
    ("sin", 45): (Fraction(1, 2), 2), ("cos", 45): (Fraction(1, 2), 2), ("tan", 45): (Fraction(1), 1),
    ("sin", 60): (Fraction(1, 2), 3), ("cos", 60): (Fraction(1, 2), 1), ("tan", 60): (Fraction(1), 3),
    ("sin", 0): (Fraction(0), 1), ("cos", 0): (Fraction(1), 1), ("tan", 0): (Fraction(0), 1),
    ("sin", 90): (Fraction(1), 1), ("cos", 90): (Fraction(0), 1),
}


def _sg(v) -> str:
    return "+" if v > 0 else "−"


BASE = {"process": "절차수행", "context": "기하맥락", "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}
TRIPLES = [(3, 4, 5), (6, 8, 10), (9, 12, 15), (12, 16, 20), (5, 12, 13), (10, 24, 26), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
PRIM = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]

# ═══════════════════════════════════════════════════════════════════ 1. 삼각비의 뜻·특수각·표
TB = "m3-2-trig-basic"
TB_BASE = {**BASE, "prereq": ["피타고라스 정리", "직각삼각형"], "ops": ["삼각비"], "traps": ["대변·빗변 혼동", "기준각"], "tags": ["삼각비"]}

# ∠C = 90°: BC = a (∠A 의 대변), AC = b (∠A 의 이웃변), AB = c (빗변)
ASK6 = {
    "sinA": ("sin A", "a", "c", "BC", "AB", "∠A의 대변 BC ÷ 빗변 AB"), "cosA": ("cos A", "b", "c", "AC", "AB", "∠A의 이웃변 AC ÷ 빗변 AB"), "tanA": ("tan A", "a", "b", "BC", "AC", "∠A의 대변 BC ÷ 이웃변 AC"),
    "sinB": ("sin B", "b", "c", "AC", "AB", "∠B의 대변 AC ÷ 빗변 AB"), "cosB": ("cos B", "a", "c", "BC", "AB", "∠B의 이웃변 BC ÷ 빗변 AB"), "tanB": ("tan B", "b", "a", "AC", "BC", "∠B의 대변 AC ÷ 이웃변 BC"),
}


def _tb1_rows():
    out = {}
    for (p, q, r) in TRIPLES:
        for a, b in ((p, q), (q, p)):
            c = r
            side = {"a": a, "b": b, "c": c}
            for gk, given in (("legs", ("a", "b")), ("hyp-a", ("a", "c")), ("hyp-b", ("b", "c"))):
                miss = ({"a", "b", "c"} - set(given)).pop()
                segname = {"a": "BC", "b": "AC", "c": "AB"}
                gtxt = ", ".join(f"[[seg({segname[g]})]] = {side[g]}" for g in given)
                if miss == "c":
                    mtxt = f"[[seg(AB)]] = [[sqrt(pow({a},2) + pow({b},2))]] = [[sqrt({a * a + b * b})]] = {c}"
                else:
                    other = "a" if miss == "b" else "b"
                    mtxt = f"[[seg({segname[miss]})]] = [[sqrt(pow({c},2) − pow({side[other]},2))]] = [[sqrt({c * c - side[other] ** 2})]] = {side[miss]}"
                for ak, (F, nk, dk, NS, DS, EXPL) in ASK6.items():
                    f = Fraction(side[nk], side[dk])
                    out[f"{a}-{b}-{gk}-{ak}"] = {"a": a, "b": b, "c": c, "GIVEN": gtxt, "MISS": mtxt, "MISSN": segname[miss], "F": F, "NS": NS, "DS": DS, "EXPL": EXPL,
                                                 "an": f.numerator, "ad": f.denominator, "RAW": f"frac({side[nk]}, {side[dk]})", "nv": side[nk], "dv": side[dk],
                                                 "LA": side["a"] if "a" in given else "", "LB": side["b"] if "b" in given else "", "LC": side["c"] if "c" in given else ""}
    return out


TB1_ROWS = _tb1_rows()
RT_PTS = {"C": [0, 0], "A": ["{b}", 0], "B": [0, "{a}"]}


def tb_t1():
    return tpl(TB, 1, TB_BASE,
        title="직각삼각형에서 삼각비의 값 — 두 변이 주어질 때 sin·cos·tan",
        skill="피타고라스 정리로 나머지 한 변을 구하고 기준각에 대한 대변·이웃변·빗변을 가려 비로 나타내기",
        variant_axis={"세 변": "피타고라스 수 9쌍 × 방향 2", "주어진 두 변": "두 직각변 / 빗변과 한 변", "삼각비": "sin·cos·tan × ∠A·∠B"},
        difficulty=2,
        discriminates="기준각이 바뀌면 대변과 이웃변이 바뀜을 알고, 빗변은 항상 직각의 대변임을 지키는가",
        params=[{"name": "f", "values": {"in": list(TB1_ROWS)}}],
        table={"key": "f", "rows": TB1_ROWS},
        derive={"ans": "an/ad"},
        cost_values=["a", "b", "c", "an", "ad"],
        answer_var="ans",
        verify=["a*a + b*b == c*c", "ans*dv == nv"],
        question="다음 그림과 같이 [[angle(C)]] = [[deg(90)]]인 직각삼각형 ABC에서 {GIVEN}일 때, {F}의 값을 구하시오.",
        figure=scene(RT_PTS, [lseg("C", "A", "{LB}"), lseg("C", "B", "{LA}"), lseg("A", "B", "{LC}")], marks={"right": [["A", "C", "B"]]}),
        answer="{ans}", answer_alt=[],
        sol1="삼각비는 기준각을 정한 뒤 (대변, 이웃변, 빗변)의 비로 정한다: sin = 대변/빗변, cos = 이웃변/빗변, tan = 대변/이웃변. 빗변은 직각 C의 대변 AB이다. 주어지지 않은 변 {MISSN}{eun(MISSN)} 피타고라스 정리로 먼저 구한다.",
        sol1_fig=scene(RT_PTS, [lseg("C", "A", "{b}"), lseg("C", "B", "{a}"), lseg("A", "B", "{c}")], marks={"right": [["A", "C", "B"]]}),
        sol1_anim=[[hl("seglbl:A-B", keep=True)], [hl("seglbl:C-B", "seglbl:C-A")]],
        sol2=[
            "{MISS}",
            "{F} = {EXPL} = [[{RAW}]]",
            "따라서 {F} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{MISS}", "hint": "피타고라스 정리"},
            {"text": "{F} = [[frac({NS}, {DS})]]", "hint": "{EXPL}", "marks": [{"on": "[[frac({NS}, {DS})]]", "note": "기준각 확인"}]},
            {"text": "= [[{RAW}]] = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="세 변 {a}, {b}, {c}에서 {a}² + {b}² = {a*a} + {b*b} = {c*c} = {c}²이므로 직각삼각형이 맞고, {F}는 {EXPL}이므로 [[{RAW}]] = {ans}이다.",
        sol3_fig=steps(["{a}² + {b}² = {c}² ✓", "{F} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="피타고라스 정리에서 {MISS}이다. {F}는 {EXPL}이므로 {F} = [[{RAW}]] = {ans}이다.",
        rubric=[
            {"element": "나머지 변", "points": 2, "criterion": "피타고라스 정리로 {MISSN} = {side_miss}{eul(side_miss)} 구했다.", "partial": "제곱을 빼는 방향을 틀렸으면 인정하지 않는다."},
            {"element": "삼각비", "points": 3, "criterion": "{F} = {EXPL}로 {ans}{eul(ans)} 구했다.", "partial": "대변과 이웃변을 바꿨으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def tb_t1_final():
    t = tb_t1()
    for r in TB1_ROWS.values():
        r["side_miss"] = {"BC": r["a"], "AC": r["b"], "AB": r["c"]}[r["MISSN"]]
    return t


# t2 — 한 삼각비의 값 → 다른 삼각비
def _tb2_rows():
    out = {}
    for (p, q, r) in PRIM:
        for a, b in ((p, q), (q, p)):
            c = r
            given = {"sin": (a, c, f"sin A = [[frac({a}, {c})]]", "대변 BC = {}, 빗변 AB = {}".format(a, c), "AC", f"[[sqrt(pow({c},2) − pow({a},2))]] = [[sqrt({c * c - a * a})]] = {b}"),
                     "cos": (b, c, f"cos A = [[frac({b}, {c})]]", "이웃변 AC = {}, 빗변 AB = {}".format(b, c), "BC", f"[[sqrt(pow({c},2) − pow({b},2))]] = [[sqrt({c * c - b * b})]] = {a}"),
                     "tan": (a, b, f"tan A = [[frac({a}, {b})]]", "대변 BC = {}, 이웃변 AC = {}".format(a, b), "AB", f"[[sqrt(pow({a},2) + pow({b},2))]] = [[sqrt({a * a + b * b})]] = {c}")}
            vals = {"sin A": Fraction(a, c), "cos A": Fraction(b, c), "tan A": Fraction(a, b)}
            for gk, (v1, v2, GT, SET, MISSN, MISS) in given.items():
                others = [k for k in vals if not k.startswith(gk)]
                asks = [(others[0], vals[others[0]]), (others[1], vals[others[1]]), (f"{others[0]} + {others[1]}", vals[others[0]] + vals[others[1]]), (f"{others[0]} × {others[1]}", vals[others[0]] * vals[others[1]])]
                for ak, av in asks:
                    if av == vals[[k for k in vals if k.startswith(gk)][0]]:
                        continue
                    out[f"{a}-{b}-{gk}-{ak}"] = {"a": a, "b": b, "c": c, "GT": GT, "SET": SET, "MISSN": MISSN, "MISS": MISS, "ASK": ak, "an": av.numerator, "ad": av.denominator,
                                                 "V1": f"{others[0]} = [[frac({ {'sin A': a, 'cos A': b, 'tan A': a}[others[0]] }, { {'sin A': c, 'cos A': c, 'tan A': b}[others[0]] })]]",
                                                 "V2": f"{others[1]} = [[frac({ {'sin A': a, 'cos A': b, 'tan A': a}[others[1]] }, { {'sin A': c, 'cos A': c, 'tan A': b}[others[1]] })]]",
                                                 "LA": a, "LB": b, "LC": c}
    return out


TB2_ROWS = _tb2_rows()


def tb_t2():
    return tpl(TB, 2, TB_BASE,
        title="한 삼각비의 값이 주어질 때 다른 삼각비의 값",
        skill="주어진 비로 직각삼각형의 두 변을 정해 그리고 피타고라스 정리로 나머지 변을 구한 뒤 다른 삼각비 읽기",
        variant_axis={"주어진 삼각비": "sin / cos / tan", "구하는 것": "다른 삼각비 하나 / 둘의 합·곱", "세 변": "원시 피타고라스 수 5쌍 × 2"},
        difficulty=3,
        discriminates="비의 값을 실제 변의 길이로 놓고 직각삼각형을 그려 세 번째 변을 구하는가",
        params=[{"name": "f", "values": {"in": list(TB2_ROWS)}}],
        table={"key": "f", "rows": TB2_ROWS},
        derive={"ans": "an/ad"},
        cost_values=["a", "b", "c", "an", "ad"],
        answer_var="ans",
        verify=["a*a + b*b == c*c"],
        question="[[angle(C)]] = [[deg(90)]]인 직각삼각형 ABC에서 {GT}일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{GT}이므로 {SET}인 직각삼각형을 그릴 수 있다(비가 같으면 삼각비도 같다). 피타고라스 정리로 나머지 변 {MISSN} = {MISS}{eul(MISS)} 구하면 세 변이 {a}, {b}, {c}로 정해지고, 나머지 삼각비를 대변·이웃변·빗변의 비로 읽는다.",
        sol1_fig=scene(RT_PTS, [lseg("C", "A", "{LB}"), lseg("C", "B", "{LA}"), lseg("A", "B", "{LC}")], marks={"right": [["A", "C", "B"]]}),
        sol1_anim=[[hl("seglbl:A-B", "seglbl:C-B", "seglbl:C-A")]],
        sol2=[
            "{SET}로 놓으면 {MISSN} = {MISS}",
            "{V1}, {V2}",
            "따라서 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{SET}", "hint": "비를 변의 길이로"},
            {"text": "{MISSN} = {MISS}", "hint": "피타고라스 정리"},
            {"text": "{V1}, {V2} → {ASK} = {ans}", "marks": [{"on": "{ASK} = {ans}", "note": "답"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="세 변 {a}, {b}, {c}는 {a}² + {b}² = {c}²을 만족하므로 직각삼각형이 맞고, 주어진 {GT}에 맞는다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["{a}² + {b}² = {c}² ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{GT}이므로 {SET}인 직각삼각형을 생각하면 {MISSN} = {MISS}이다. 따라서 {V1}, {V2}이고 {ASK} = {ans}이다.",
        rubric=[
            {"element": "변 정하기", "points": 3, "criterion": "{SET}로 놓고 {MISSN} = {MISS}{eul(MISS)} 구했다.", "partial": "빗변을 잘못 잡았으면 인정하지 않는다."},
            {"element": "삼각비 읽기", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다.", "partial": "대변·이웃변을 바꿨으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t3 — 특수각 삼각비의 계산 (유리수 결과)
class RV:
    """Σ coef·√m (m ∈ 제곱인수 없는 수)"""

    def __init__(self, terms=None):
        self.t = {}
        for m, c in (terms or {}).items():
            if c:
                self.t[m] = self.t.get(m, Fraction(0)) + Fraction(c)

    @staticmethod
    def one(coef, m):
        a, b = sqfree(m)
        return RV({b: Fraction(coef) * a})

    def __add__(self, o):
        r = dict(self.t)
        for m, c in o.t.items():
            r[m] = r.get(m, Fraction(0)) + c
        return RV(r)

    def __sub__(self, o):
        return self + RV({m: -c for m, c in o.t.items()})

    def __mul__(self, o):
        r = {}
        for m1, c1 in self.t.items():
            for m2, c2 in o.t.items():
                a, b = sqfree(m1 * m2)
                r[b] = r.get(b, Fraction(0)) + c1 * c2 * a
        return RV(r)

    def inv(self):
        assert len(self.t) == 1
        (m, c), = self.t.items()
        return RV({m: 1 / (c * m)})

    def rational(self):
        return list(self.t) == [1] or not self.t

    def value(self):
        return self.t.get(1, Fraction(0)) if self.rational() else None


def _tb3_rows():
    out = {}
    names = [("sin", 30), ("cos", 30), ("tan", 30), ("sin", 45), ("cos", 45), ("tan", 45), ("sin", 60), ("cos", 60), ("tan", 60), ("sin", 0), ("cos", 0), ("sin", 90), ("cos", 90)]
    ops = {"+": lambda x, y: x + y, "−": lambda x, y: x - y, "×": lambda x, y: x * y, "÷": lambda x, y: x * y.inv()}
    for (f1, t1) in names:
        for (f2, t2) in names:
            if (f1, t1) == (f2, t2):
                continue
            v1 = RV.one(*SPECIAL[(f1, t1)]); v2 = RV.one(*SPECIAL[(f2, t2)])
            for op, fn in ops.items():
                if op == "÷" and (len(v2.t) != 1 or SPECIAL[(f2, t2)][0] == 0):
                    continue
                if op in "×÷" and (t1 in (0, 90) or t2 in (0, 90) or v1.value() == 1 or v2.value() == 1):
                    continue                                    # 0·1 곱셈은 너무 시시함 ('× 1')
                r = fn(v1, v2)
                if not r.rational() or r.value() == 0:
                    continue
                v = r.value()
                m1, m2 = mk(*SPECIAL[(f1, t1)]), mk(*SPECIAL[(f2, t2)])
                out[f"{f1}{t1}{op}{f2}{t2}"] = {"EXPR": f"{f1} {t1}° {op} {f2} {t2}°", "VALS": f"{m1} {op} {m2}", "an": v.numerator, "ad": v.denominator,
                                                 "T1": f"{f1} {t1}° = {m1}", "T2": f"{f2} {t2}° = {m2}"}
    return out


TB3_ROWS = _tb3_rows()


def tb_t3():
    return tpl(TB, 3, TB_BASE,
        title="특수한 각의 삼각비의 값을 이용한 계산",
        skill="30°, 45°, 60°(및 0°, 90°)의 삼각비의 값을 정확히 쓰고 근호가 있는 수를 계산하기",
        variant_axis={"항": "sin·cos·tan × 0°·30°·45°·60°·90°", "연산": "+ − × ÷"},
        difficulty=2,
        discriminates="특수각의 삼각비 값을 정확히 외워 쓰고, √3 × √3 = 3, √2 × √2 = 2 같은 근호 계산을 바르게 하는가",
        params=[{"name": "f", "values": {"in": list(TB3_ROWS)}}],
        table={"key": "f", "rows": TB3_ROWS},
        derive={"ans": "an/ad"},
        cost_values=["an", "ad"],
        answer_var="ans",
        verify=["ad > 0"],
        question="{EXPR}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="특수한 각의 삼각비: sin 30° = cos 60° = [[frac(1,2)]], sin 60° = cos 30° = [[frac(sqrt(3), 2)]], sin 45° = cos 45° = [[frac(sqrt(2), 2)]], tan 30° = [[frac(sqrt(3), 3)]], tan 45° = 1, tan 60° = [[sqrt(3)]] (sin 0° = 0, cos 0° = 1, sin 90° = 1, cos 90° = 0). 각 항을 값으로 바꾼 뒤 계산한다.",
        sol2=[
            "{T1}, {T2}",
            "{EXPR} = {VALS}",
            "= {ans}",
        ],
        sol2_fig=steps([
            {"text": "{T1}", "hint": "특수각의 값"},
            {"text": "{T2}", "hint": "특수각의 값"},
            {"text": "{VALS} = {ans}", "marks": [{"on": "{ans}", "note": "근호 계산 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="근호가 있는 값끼리의 곱·나눗셈은 (√a)² = a를 쓰고, 덧셈·뺄셈은 분모를 맞춘다. 다시 계산해도 {VALS} = {ans}{ika(ans)} 된다.",
        sol3_fig=steps(["{VALS}", "= {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{T1}, {T2}이므로 {EXPR} = {VALS} = {ans}이다.",
        rubric=[
            {"element": "특수각의 값", "points": 3, "criterion": "{T1}, {T2}{eul(T2)} 바르게 썼다.", "partial": "하나만 틀렸으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{ans}{eul(ans)} 구했다.", "partial": "근호 계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t4 — 특수각 삼각비의 방정식: sin x = √3/2 → x (0° < x < 90°), x + s / x − s / 2x 변형
def _tb4_rows():
    out = {}
    base = [(f, t) for (f, t) in SPECIAL if t in (30, 45, 60)]
    for f, t in base:
        V = mk(*SPECIAL[(f, t)])
        forms = [("id", "x", 0, 1, t)]
        for s in (10, 15, 20):
            if t - s > 0:
                forms.append(("plus", f"(x + {s}°)", s, 1, t - s))
            if t + s < 90:
                forms.append(("minus", f"(x − {s}°)", -s, 1, t + s))
        if t % 2 == 0:
            forms.append(("double", "2x", 0, 2, t // 2))
        for kind, arg, s, kmul, x in forms:
            if kind == "id":
                step = f"x = {t}°"
            elif kind == "double":
                step = f"2x = {t}°이므로 x = {x}°"
            else:
                step = f"{arg} = {t}°이므로 x = {t}° {_sg(-s)} {abs(s)}° = {x}°"
            out[f"{f}{t}-{kind}{abs(s)}"] = {"EQ": f"{f} {arg} = {V}", "F": f, "TH": t, "V": V, "ARG": arg, "STEP": step, "ans": x, "ANG": f"{f} {t}° = {V}"}
    return out


TB4_ROWS = _tb4_rows()


def tb_t4():
    return tpl(TB, 4, TB_BASE,
        title="특수한 각의 삼각비를 이용해 x 구하기 — sin x = √3/2, tan (x − 15°) = 1 등",
        skill="삼각비의 값이 어느 특수각의 것인지 알아내고 괄호 안의 식을 그 각과 같다고 놓기",
        variant_axis={"삼각비": "sin·cos·tan", "각": "30°·45°·60°", "변형": "x / x ± s / 2x"},
        difficulty=2,
        discriminates="값으로부터 특수각을 정확히 되찾고, x ± s 나 2x 를 그 각과 같다고 놓아 x를 구하는가",
        params=[{"name": "f", "values": {"in": list(TB4_ROWS)}}],
        table={"key": "f", "rows": TB4_ROWS},
        constraints=["ans > 0", "ans < 90"],
        cost_values=["TH", "ans"],
        answer_var="ans",
        verify=["ans > 0"],
        question="0° < x < 90°일 때, {EQ}를 만족하는 x의 값을 구하시오.",
        answer="[[deg({ans})]]", answer_alt=["{ans}°", "{ans}"],
        sol1="{ANG}이다. 0°와 90° 사이에서 {F}의 값이 이와 같아지는 각은 {TH}° 하나뿐이므로 {ARG} = {TH}°로 놓고 x를 구한다.",
        sol2=[
            "{ANG}",
            "{STEP}",
        ],
        sol2_fig=steps([
            {"text": "{ANG}", "hint": "특수각의 값"},
            {"text": "{STEP}", "hint": "{ARG} = {TH}°", "marks": [{"on": "x = {ans}°", "note": "0° < x < 90° ✓"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="x = {ans}°를 넣으면 {ARG} = {TH}°가 되고 {ANG}이므로 주어진 식이 성립한다. 따라서 x = {ans}°이다.",
        sol3_fig=steps(["x = {ans}° → {ARG} = {TH}° ✓", "x = {ans}°"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{ANG}이므로 {STEP}이다.",
        rubric=[
            {"element": "특수각 찾기", "points": 3, "criterion": "주어진 값이 {F} {TH}°의 값임을 밝혔다.", "partial": "다른 특수각을 골랐으면 인정하지 않는다."},
            {"element": "x 구하기", "points": 2, "criterion": "{ARG} = {TH}°에서 x = {ans}°를 구했다.", "partial": "이항 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


# t5 — 삼각비의 표를 이용한 변의 길이 (소수)
def _tb5_rows():
    out = {}
    for th in range(31, 60):
        s, c, t = (round(math.sin(math.radians(th)), 4), round(math.cos(math.radians(th)), 4), round(math.tan(math.radians(th)), 4))
        out[str(th)] = {"th": th, "S": f"{s:.4f}", "C": f"{c:.4f}", "T": f"{t:.4f}", "s4": round(s * 10000), "c4": round(c * 10000), "t4": round(t * 10000)}
    return out


TB5_ROWS = _tb5_rows()
TB5_ASK = {
    "opp-sin": {"GN": "AB", "XN": "BC", "GT": "빗변 AB", "F": "sin", "REL": "sin {th}° = [[frac(seg(BC), seg(AB))]]", "CALC": "BC = AB × sin {th}°", "w1": 1, "w2": 0, "w3": 0},
    "adj-cos": {"GN": "AB", "XN": "AC", "GT": "빗변 AB", "F": "cos", "REL": "cos {th}° = [[frac(seg(AC), seg(AB))]]", "CALC": "AC = AB × cos {th}°", "w1": 0, "w2": 1, "w3": 0},
    "opp-tan": {"GN": "AC", "XN": "BC", "GT": "이웃변 AC", "F": "tan", "REL": "tan {th}° = [[frac(seg(BC), seg(AC))]]", "CALC": "BC = AC × tan {th}°", "w1": 0, "w2": 0, "w3": 1},
}
for _r in TB5_ASK.values():
    for k in ("REL", "CALC"):
        _r[k] = _r[k].replace("{th}°", "A")


def tb_t5():
    return tpl(TB, 5, TB_BASE,
        title="삼각비의 표를 이용한 변의 길이",
        skill="주어진 각의 삼각비의 값(표)을 읽고 (구하는 변) = (아는 변) × (삼각비)로 계산하기",
        variant_axis={"각": "31°~59°", "아는 변": "빗변 / 이웃변", "구하는 변": "대변 / 이웃변"},
        difficulty=2,
        discriminates="어느 삼각비를 써야 하는지(아는 변·구하는 변의 이름)를 정하고 소수 곱셈을 정확히 하는가",
        params=[{"name": "f", "values": {"in": list(TB5_ROWS)}}, {"name": "h", "values": {"in": [10, 20, 50, 100]}}, {"name": "ask", "values": {"in": list(TB5_ASK)}}],
        table=[{"key": "f", "rows": TB5_ROWS}, {"key": "ask", "rows": TB5_ASK}],
        derive={"ans": "h*(w1*s4 + w2*c4 + w3*t4)/10000", "TV": "(w1*s4 + w2*c4 + w3*t4)/10000"},
        cost_values=["th", "h", "ans"],
        answer_var="ans",
        verify=["ans == h*TV"],
        question="다음 삼각비의 표를 이용하여, [[angle(C)]] = [[deg(90)]], [[angle(A)]] = [[deg({th})]]인 직각삼각형 ABC에서 {GT}의 길이가 {h}일 때 [[seg({XN})]]의 길이를 구하시오. (sin {th}° = {S}, cos {th}° = {C}, tan {th}° = {T})",
        answer="{dec(ans)}", answer_alt=[],
        sol1="∠A = {th}°를 기준각으로 하면 BC는 대변, AC는 이웃변, AB는 빗변이다. 아는 변이 {GT}이고 구하는 변이 {XN}이므로 두 변을 잇는 삼각비 {F} {th}°를 쓴다: {REL}. 표의 값 {F} {th}° = {dec(TV)}{eul(dec(TV))} 넣어 {CALC}로 계산한다.",
        sol2=[
            "{REL}",
            "{CALC} = {h} × {dec(TV)}",
            "= {dec(ans)}",
        ],
        sol2_fig=steps([
            {"text": "{REL}", "hint": "아는 변·구하는 변으로 삼각비 고르기"},
            {"text": "{CALC} = {h} × {dec(TV)}", "hint": "표: {F} {th}° = {dec(TV)}", "marks": [{"on": "{dec(TV)}", "note": "표의 값"}]},
            {"text": "= {dec(ans)}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{XN} = {dec(ans)}{eun(dec(ans))} {GT} {h}에 {F} {th}° = {dec(TV)}{eul(dec(TV))} 곱한 값이다. 소수점 자리를 확인하면 답은 {dec(ans)}이다.",
        sol3_fig=steps(["{h} × {dec(TV)} = {dec(ans)}", "{XN} = {dec(ans)}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{REL}이므로 {CALC} = {h} × {dec(TV)} = {dec(ans)}이다.",
        rubric=[
            {"element": "삼각비 고르기", "points": 3, "criterion": "{REL}{eul(XN)} 세웠다.", "partial": "다른 삼각비를 골랐으면 인정하지 않는다."},
            {"element": "계산", "points": 2, "criterion": "{h} × {dec(TV)} = {dec(ans)}{eul(dec(ans))} 구했다.", "partial": "소수점 자리 실수면 1점."},
        ],
        rubric_total=5,
    )


TB_SEED = {
    "seed_id": TB, "category": "도형",
    "title": "삼각비 — 직각삼각형의 삼각비·삼각비→삼각비·특수각 계산·특수각 방정식·삼각비의 표",
    "unit_id": "m3-2", "concept_ids": ["m3-2-01", "m3-2-02", "m3-2-03"],
    "schema_id": None, "schema_name": "삼각비의 뜻과 특수한 각의 삼각비",
    "source_item_ids": [],
    "note": "피타고라스 수 표(TRIPLES)·특수각 값(SPECIAL, coef·√m)·삼각비 표(31°~59°, 소수 넷째 자리) 를 파이썬에서 미리 계산. 특수각 계산은 유리수 결과만.",
    "geometry": True,
    "templates": [geo(t) for t in (tb_t1_final(), tb_t2(), tb_t3(), tb_t4(), tb_t5())],
}


# ═══════════════════════════════════════════════════════════════════ 2. 삼각비의 활용
TA = "m3-2-trig-apply"
TA_BASE = {**BASE, **COMMON_APPLY, "context": "기하맥락", "ops": ["삼각비"], "prereq": ["특수한 각의 삼각비", "직각삼각형"], "traps": ["기준각 선택", "근호 정리"], "tags": ["삼각비의 활용"], "points": 4, "pool_target": 300}

# ∠B = θ 인 직각삼각형(∠C = 90°): 밑변 BC(이웃변), 높이 AC(대변), 빗변 AB — k 배 (coef, m) 표현
SIDES = {
    30: {"BC": (Fraction(1), 3), "AC": (Fraction(1), 1), "AB": (Fraction(2), 1)},
    60: {"BC": (Fraction(1), 1), "AC": (Fraction(1), 3), "AB": (Fraction(2), 1)},
    45: {"BC": (Fraction(1), 1), "AC": (Fraction(1), 1), "AB": (Fraction(1), 2)},
}
RELS = {
    ("AB", "AC"): ("sin", "AC = AB × sin {th}°", "sin {th}° = [[frac(seg(AC), seg(AB))]]"), ("AB", "BC"): ("cos", "BC = AB × cos {th}°", "cos {th}° = [[frac(seg(BC), seg(AB))]]"),
    ("BC", "AC"): ("tan", "AC = BC × tan {th}°", "tan {th}° = [[frac(seg(AC), seg(BC))]]"), ("AC", "BC"): ("tan", "BC = AC ÷ tan {th}°", "tan {th}° = [[frac(seg(AC), seg(BC))]]"),
    ("AC", "AB"): ("sin", "AB = AC ÷ sin {th}°", "sin {th}° = [[frac(seg(AC), seg(AB))]]"), ("BC", "AB"): ("cos", "AB = BC ÷ cos {th}°", "cos {th}° = [[frac(seg(BC), seg(AB))]]"),
}


def _ta1_rows():
    out = {}
    for th, S in SIDES.items():
        for (G, X), (F, CALC, REL) in RELS.items():
            for k in range(1, 7):
                gc, gm = S[G]; xc, xm = S[X]
                gt, xt = mk(gc * k, gm), mk(xc * k, xm)
                fv = mk(*SPECIAL[(F, th)])
                if fv == "1":
                    continue                                    # tan 45° = 1 은 '÷ 1' 항등 연산
                op = "×" if "×" in CALC else "÷"
                if exposed(xt, gt, str(th)):
                    continue
                out[f"{th}-{G}-{X}-{k}"] = {"th": th, "G": G, "X": X, "GT": gt, "ANS_T": xt, "F": F, "FV": fv, "CALC": CALC.replace("{th}", str(th)), "REL": REL.replace("{th}", str(th)),
                                            "STEP": f"{X} = {gt} {op} {fv} = {xt}", "bx": round(val(*S['BC']) * k, 4), "ay": round(val(*S['AC']) * k, 4),
                                            "LG_BC": gt if G == "BC" else "", "LG_AC": gt if G == "AC" else "", "LG_AB": gt if G == "AB" else "", "ansv": round(val(xc * k, xm), 6)}
    return out


TA1_ROWS = _ta1_rows()
TA1_PTS = {"B": [0, 0], "C": ["{bx}", 0], "A": ["{bx}", "{ay}"]}


def ta_t1():
    return tpl(TA, 1, TA_BASE,
        title="특수한 각을 낀 직각삼각형의 변의 길이",
        skill="아는 변과 구하는 변을 잇는 삼각비를 골라 (구하는 변) = (아는 변) × 또는 ÷ (삼각비의 값)으로 계산하기",
        variant_axis={"각": "30°·45°·60°", "아는 변 → 구하는 변": "6가지", "배율": "1~6"},
        difficulty=2,
        discriminates="곱할지 나눌지(구하는 변이 분자인지 분모인지)를 가리고 분모의 근호를 유리화하는가",
        params=[{"name": "f", "values": {"in": list(TA1_ROWS)}}],
        table={"key": "f", "rows": TA1_ROWS},
        cost_values=["th", "ansv"],
        verify=["ansv > 0"],
        question="다음 그림과 같이 [[angle(C)]] = [[deg(90)]], [[angle(B)]] = [[deg({th})]]인 직각삼각형 ABC에서 [[seg({G})]] = {GT}일 때, [[seg({X})]]의 길이를 구하시오.",
        figure=scene(TA1_PTS, [lseg("B", "C", "{LG_BC}"), lseg("C", "A", "{LG_AC}"), lseg("A", "B", "{LG_AB}")], marks={"right": [["B", "C", "A"]], "arc": [arc("B", "C", "A", "{th}°")]}),
        answer="{ANS_T}", answer_alt=[],
        sol1="∠B = {th}°를 기준각으로 하면 AC는 대변, BC는 이웃변, AB는 빗변이다. 아는 변 {G}{wa(G)} 구하는 변 {X}{eul(X)} 잇는 삼각비는 {F}이므로 {REL}. {F} {th}° = {FV}이므로 {CALC}로 계산하고, 분모에 근호가 남으면 유리화한다.",
        sol1_fig=scene(TA1_PTS, [lseg("B", "C", "{LG_BC}"), lseg("C", "A", "{LG_AC}"), lseg("A", "B", "{LG_AB}")], marks={"right": [["B", "C", "A"]], "arc": [arc("B", "C", "A", "{th}°", "arc:b")]}),
        sol1_anim=[[hl("arc:b", keep=True)], [hl("seg:B-C", "seg:C-A", "seg:A-B")]],
        sol2=[
            "{REL}",
            "{CALC}",
            "{STEP}",
        ],
        sol2_fig=steps([
            {"text": "{REL}", "hint": "기준각 {th}°"},
            {"text": "{CALC}", "hint": "{F} {th}° = {FV}"},
            {"text": "{STEP}", "marks": [{"on": "{ANS_T}", "note": "유리화 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{th}°의 직각삼각형은 세 변의 비가 정해져 있다(30°: 1 : √3 : 2, 45°: 1 : 1 : √2, 60°: √3 : 1 : 2 — 대변 : 이웃변 : 빗변). {G} = {GT}에 맞춰 비를 늘이면 {X} = {ANS_T}이다.",
        sol3_fig=steps(["{th}° 삼각형의 변의 비", "{X} = {ANS_T}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{REL}이므로 {STEP}이다.",
        rubric=[
            {"element": "삼각비 세우기", "points": 3, "criterion": "{REL}{eul(X)} 세웠다.", "partial": "다른 삼각비를 골랐으면 인정하지 않는다."},
            {"element": "계산", "points": 2, "criterion": "{X} = {ANS_T}임을 구했다.", "partial": "유리화하지 않았으면 1점."},
        ],
        rubric_total=5,
    )


# t2 — 높이 측정: 건물(tan) / 사다리(sin)
def _ta2_rows():
    out = {}
    for th in (30, 45, 60):
        tv = SPECIAL[("tan", th)]; sv = SPECIAL[("sin", th)]
        for k in range(2, 13):
            d = k * (3 if th == 30 else 1)                       # 30°: 3k → k√3
            h = mk(tv[0] * d, tv[1])
            if not exposed(h, str(d), str(th)):
              out[f"b{th}-{k}"] = {"KIND": "건물", "th": th, "d": d, "ANS_T": h, "F": "tan", "FV": mk(*tv), "ansv": round(val(tv[0] * d, tv[1]), 6),
                                 "Q": f"지면 위의 한 지점 P에서 건물의 밑 B까지의 거리가 {d} m이고, P에서 건물의 꼭대기 A를 올려다본 각의 크기가 {th}°일 때, 건물의 높이 [[seg(AB)]]를 구하시오.",
                                 "REL": f"tan {th}° = [[frac(seg(AB), seg(PB))]]", "CALC": f"AB = PB × tan {th}° = {d} × {mk(*tv)} = {h}", "SET": "직각삼각형 PBA에서 ∠P = {}°, 이웃변 PB = {} m".format(th, d),
                                 "px": -d, "ay": round(val(tv[0] * d, tv[1]), 4), "N1": "P", "N2": "B", "N3": "A", "LAB": f"{d} m"}
            L = k                                                # 사다리 길이 3~12 m (현실적인 범위)
            hs = mk(sv[0] * L, sv[1])
            if L >= 3 and not exposed(hs, str(L), str(th)):
              out[f"l{th}-{k}"] = {"KIND": "사다리", "th": th, "d": L, "ANS_T": hs, "F": "sin", "FV": mk(*sv), "ansv": round(val(sv[0] * L, sv[1]), 6),
                                 "Q": f"길이가 {L} m인 사다리 PA를 벽에 기대어 놓았더니 사다리가 지면과 이루는 각의 크기가 {th}°였다. 사다리가 벽에 닿은 점 A의 지면으로부터의 높이 [[seg(AB)]]를 구하시오.",
                                 "REL": f"sin {th}° = [[frac(seg(AB), seg(PA))]]", "CALC": f"AB = PA × sin {th}° = {L} × {mk(*sv)} = {hs}", "SET": "직각삼각형 PBA에서 ∠P = {}°, 빗변 PA = {} m".format(th, L),
                                 "px": -round(val(SPECIAL[('cos', th)][0] * L, SPECIAL[('cos', th)][1]), 4), "ay": round(val(sv[0] * L, sv[1]), 4), "N1": "P", "N2": "B", "N3": "A", "LAB": f"{L} m"}
    # 갈래별 계산 부분점수·실수거리 — 유리화가 생기는 것은 tan 30°(1/√3)·sin 45°(1/√2)를 쓸 때뿐
    for r in out.values():
        if (r["KIND"], r["th"]) in (("건물", 30), ("사다리", 45)):
            r["PART"] = "분모의 근호를 유리화하지 않았으면 1점."
            r["PITC"] = "분모의 근호를 유리화하지 않음"
        else:
            r["PART"] = "곱셈 계산 실수면 1점."
            r["PITC"] = "sin 30°와 sin 60°의 값을 바꿔 씀" if r["F"] == "sin" else "tan 30°와 tan 60°의 값을 바꿔 씀"
    return out


TA2_ROWS = _ta2_rows()
TA2_PTS = {"P": ["{px}", 0], "B": [0, 0], "A": [0, "{ay}"]}


def ta_t2():
    return tpl(TA, 2, TA_BASE,
        title="삼각비를 이용한 높이 측정 — 건물의 높이·사다리의 높이",
        skill="상황을 직각삼각형으로 옮겨 아는 변과 구하는 변을 잇는 삼각비로 높이 구하기",
        variant_axis={"상황": "건물(tan) / 사다리(sin)", "각": "30°·45°·60°", "길이": "건물 거리 2~12 배 / 사다리 3~12 m"},
        difficulty=3,
        discriminates="올려다본 각·지면과 이루는 각이 어느 꼭짓점의 각인지 읽고, 거리(이웃변)인지 사다리 길이(빗변)인지 구별하는가",
        params=[{"name": "f", "values": {"in": list(TA2_ROWS)}}],
        table={"key": "f", "rows": TA2_ROWS},
        cost_values=["th", "d", "ansv"],
        verify=["ansv > 0"],
        question="{Q}",
        figure=scene(TA2_PTS, [lseg("P", "B", "{LAB_B}"), ["B", "A"], lseg("A", "P", "{LAB_H}")], marks={"right": [["P", "B", "A"]], "arc": [arc("P", "B", "A", "{th}°")]}),
        answer="{ANS_T}", answer_alt=["{ANS_T} m"],
        sol1="{SET}이고 ∠B = 90°이다. 구하는 높이 AB는 ∠P의 대변이므로, 아는 변이 이웃변이면 tan, 빗변이면 sin을 쓴다: {REL}. 특수각의 값 {F} {th}° = {FV}이므로 이를 넣어 계산한다.",
        sol1_fig=scene(TA2_PTS, [lseg("P", "B", "{LAB_B}"), ["B", "A"], lseg("A", "P", "{LAB_H}")], marks={"right": [["P", "B", "A"]], "arc": [arc("P", "B", "A", "{th}°", "arc:p")]}),
        sol1_anim=[[hl("arc:p", keep=True)], [hl("seg:B-A")]],
        sol2=[
            "{SET}",
            "{REL}",
            "{CALC}",
        ],
        sol2_fig=steps([
            {"text": "{SET}", "hint": "직각삼각형으로 옮기기"},
            {"text": "{REL}", "hint": "AB는 ∠P의 대변"},
            {"text": "{CALC}", "marks": [{"on": "{ANS_T}", "note": "높이"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{th}°의 직각삼각형에서 변의 비(30°: 1 : √3 : 2, 45°: 1 : 1 : √2, 60°: √3 : 1 : 2)로 확인해도 높이는 {ANS_T} m이다. 단위 m를 붙여 답한다.",
        sol3_fig=steps(["{th}° 삼각형의 변의 비로 확인", "AB = {ANS_T} m"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{SET}이므로 {REL}이고, {CALC}이다. 따라서 높이는 {ANS_T} m이다.",
        rubric=[
            {"element": "직각삼각형·삼각비", "points": 3, "criterion": "{REL}의 관계를 세웠다.", "partial": "sin과 tan을 바꿔 썼으면 인정하지 않는다."},
            {"element": "계산", "points": 2, "criterion": "AB = {ANS_T} m를 구했다.", "partial": "{PART}"},
        ],
        rubric_total=5,
    )


def ta_t2_final():
    t = ta_t2()
    for r in TA2_ROWS.values():
        r["LAB_B"] = r["LAB"] if r["KIND"] == "건물" else ""
        r["LAB_H"] = r["LAB"] if r["KIND"] == "사다리" else ""
    return t


# t3 — 삼각형의 넓이 S = ½ab sin C (예각·둔각)
def _ta3_rows():
    out = {}
    for C in (30, 45, 60, 120, 135, 150):
        s = SPECIAL[("sin", 180 - C if C > 90 else C)]
        for a in range(2, 13):
            for b in range(2, 13):
                if a > b or (a * b) % 4:
                    continue
                S = mk(s[0] * a * b / 2, s[1])
                if exposed(S, str(a), str(b), str(C)):
                    continue
                out[f"{C}-{a}-{b}"] = {"C": C, "a": a, "b": b, "ANS_T": S, "SV": mk(*s), "SREF": (f"sin {C}° = sin (180° − {C}°) = sin {180 - C}° = {mk(*s)}" if C > 90 else f"sin {C}° = {mk(*s)}"),
                                       "CALC": f"S = [[frac(1, 2)]] × {a} × {b} × {mk(*s)} = {S}", "ansv": round(val(s[0] * a * b / 2, s[1]), 6),
                                       "ax": round(b * math.cos(math.radians(C)), 4), "ay": round(b * math.sin(math.radians(C)), 4)}
    return out


TA3_ROWS = _ta3_rows()
TA3_PTS = {"C": [0, 0], "B": ["{a}", 0], "A": ["{ax}", "{ay}"]}


def ta_t3():
    return tpl(TA, 3, TA_BASE,
        title="두 변과 그 끼인각으로 삼각형의 넓이 구하기",
        skill="S = ½ × (두 변의 곱) × sin(끼인각)에서 둔각이면 sin(180° − 각)을 쓰기",
        variant_axis={"끼인각": "30°·45°·60°·120°·135°·150°", "두 변": "2~12"},
        difficulty=3,
        discriminates="끼인각이 둔각일 때 sin(180° − C)로 바꾸는가, ½을 빠뜨리지 않는가",
        params=[{"name": "f", "values": {"in": list(TA3_ROWS)}}],
        table={"key": "f", "rows": TA3_ROWS},
        cost_values=["C", "a", "b", "ansv"],
        verify=["ansv > 0"],
        question="다음 그림과 같이 [[seg(BC)]] = {a}, [[seg(CA)]] = {b}, [[angle(C)]] = [[deg({C})]]인 삼각형 ABC의 넓이를 구하시오.",
        figure=scene(TA3_PTS, [lseg("C", "B", "{a}"), lseg("C", "A", "{b}"), ["A", "B"]], marks={"arc": [arc("C", "B", "A", "{C}°")]}),
        answer="{ANS_T}", answer_alt=[],
        sol1="꼭짓점 A에서 변 BC(또는 그 연장선)에 수선 AH를 내리면 높이 AH = CA × sin C이므로 넓이는 S = ½ × BC × CA × sin C이다. {SREF}이므로 이 값을 넣어 계산한다.",
        sol1_fig=scene(TA3_PTS, [lseg("C", "B", "{a}"), lseg("C", "A", "{b}"), ["A", "B"]], marks={"arc": [arc("C", "B", "A", "{C}°", "arc:c")]}),
        sol1_anim=[[hl("arc:c", keep=True)], [hl("seg:C-B", "seg:C-A")]],
        sol2=[
            "S = [[frac(1, 2)]] × BC × CA × sin C",
            "{SREF}",
            "{CALC}",
        ],
        sol2_fig=steps([
            {"text": "S = [[frac(1, 2)]] × BC × CA × sin C", "hint": "높이 = CA × sin C"},
            {"text": "{SREF}", "hint": "특수각의 값", "marks": [{"on": "{SV}", "note": "sin C"}]},
            {"text": "{CALC}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="높이 AH = {b} × {SV}이므로 넓이 ½ × {a} × AH를 계산해도 {ANS_T}이다. 따라서 넓이는 {ANS_T}이다.",
        sol3_fig=steps(["AH = {b} × {SV}", "S = {ANS_T}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{SREF}이므로 {CALC}이다.",
        rubric=[
            {"element": "넓이 공식", "points": 3, "criterion": "S = ½ × {a} × {b} × sin {C}°{eul(C)} 세우고 {SREF}임을 썼다.", "partial": "둔각을 그대로 두어 sin 값을 못 구했으면 1점."},
            {"element": "계산", "points": 2, "criterion": "S = {ANS_T}임을 구했다.", "partial": "½을 빠뜨렸으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t4 — 두 변과 끼인각 → 대변 (수선을 내려 피타고라스)
def _ta4_rows():
    out = {}
    for th in (30, 45, 60):
        c_, s_ = SPECIAL[("cos", th)], SPECIAL[("sin", th)]
        for kc in range(1, 9):
            # AB = c 는 45° 면 k√2, 30°·60° 면 2k (BH·AH 가 k 배)
            if th == 45:
                cc, cm = Fraction(kc), 2
            else:
                cc, cm = Fraction(2 * kc), 1
            bh = (cc * c_[0], cm * c_[1]); ah = (cc * s_[0], cm * s_[1])          # (coef, m)
            bh_v = RV.one(*bh); ah_v = RV.one(*ah)
            if not bh_v.rational() or (list(ah_v.t)[0] not in (1, 3)):
                continue
            BH = bh_v.value()
            for a in range(2, 21):
                if a <= BH:
                    continue
                HC = a - BH
                ac2 = (ah_v * ah_v).value() + HC * HC          # AC² 유리수
                ac2 = Fraction(ac2)
                if ac2.denominator != 1:
                    continue
                q, m = sqfree(int(ac2))
                if m > 30:
                    continue
                AC = mk(Fraction(q), m)
                AHt = mk(*ah)
                if exposed(AC, mk(cc, cm), str(a), str(th)):
                    continue
                out[f"{th}-{kc}-{a}"] = {"th": th, "a": a, "CT": mk(cc, cm), "BH": int(BH), "AH": AHt, "HC": int(HC), "AC2": int(ac2), "ANS_T": AC, "ansv": round(math.sqrt(int(ac2)), 6), "SIMP": (f" = {AC}" if AC != f"[[sqrt({int(ac2)})]]" else ""),
                                         "AH2": int((ah_v * ah_v).value()), "HC2": int(HC * HC), "CV": mk(*c_), "SV": mk(*s_),
                                         "bx": round(float(BH), 4), "ay": round(val(*ah), 4)}
    return out


TA4_ROWS = _ta4_rows()
TA4_PTS = {"B": [0, 0], "C": ["{a}", 0], "A": ["{bx}", "{ay}"], "H": ["{bx}", 0]}
TA4_PTS_Q = {"B": [0, 0], "C": ["{a}", 0], "A": ["{bx}", "{ay}"]}


def ta_t4():
    return tpl(TA, 4, TA_BASE,
        title="두 변과 그 끼인각이 주어진 삼각형의 나머지 한 변 — 수선을 내려 피타고라스",
        skill="한 꼭짓점에서 수선을 내려 특수각 직각삼각형으로 높이와 밑변의 일부를 구하고 나머지 직각삼각형에 피타고라스 정리 쓰기",
        variant_axis={"∠B": "30°·45°·60°", "AB": "특수각에 맞춘 길이(k = 1~8)", "BC": "2~20"},
        difficulty=4,
        discriminates="AH = AB sin B, BH = AB cos B로 나눈 뒤 HC = BC − BH를 쓰는가(BC 전체를 밑변으로 쓰지 않는가)",
        params=[{"name": "f", "values": {"in": list(TA4_ROWS)}}],
        table={"key": "f", "rows": TA4_ROWS},
        constraints=["AC2 != a*a"],
        cost_values=["th", "a", "BH", "HC", "AC2", "ansv"],
        verify=["AH2 + HC2 == AC2"],
        question="다음 그림과 같이 [[seg(AB)]] = {CT}, [[seg(BC)]] = {a}, [[angle(B)]] = [[deg({th})]]인 삼각형 ABC에서 [[seg(AC)]]의 길이를 구하시오.",
        figure=scene(TA4_PTS_Q, [lseg("B", "C", "{a}"), ["C", "A"], lseg("A", "B", "{CT}")], marks={"arc": [arc("B", "C", "A", "{th}°")]}),
        answer="{ANS_T}", answer_alt=[],
        sol1="꼭짓점 A에서 BC에 수선 AH를 내리면 △ABH는 ∠B = {th}°인 직각삼각형이므로 AH = AB × sin {th}° = {AH}, BH = AB × cos {th}° = {BH}이다. 그러면 HC = BC − BH = {a} − {BH} = {HC}이고, 직각삼각형 AHC에서 AC² = AH² + HC²으로 AC를 구한다.",
        sol1_fig=scene(TA4_PTS, [lseg("B", "H", "{BH}"), lseg("H", "C", "{HC}"), ["C", "A"], lseg("A", "B", "{CT}"), lseg("A", "H", "{AH}", dash=True)], marks={"arc": [arc("B", "C", "A", "{th}°")], "right": [["A", "H", "C"]]}),
        sol1_anim=[[hl("seg:A-H", "seglbl:A-H", keep=True)], [hl("seglbl:B-H", "seglbl:H-C", keep=True)], [hl("seg:C-A")]],
        sol2=[
            "AH = {CT} × {SV} = {AH}, BH = {CT} × {CV} = {BH}",
            "HC = BC − BH = {a} − {BH} = {HC}",
            "AC² = AH² + HC² = {AH2} + {HC2} = {AC2}이므로 AC = [[sqrt({AC2})]]{SIMP}",
        ],
        sol2_fig=steps([
            {"text": "AH = {AH}, BH = {BH}", "hint": "△ABH: sin·cos {th}°"},
            {"text": "HC = {a} − {BH} = {HC}", "hint": "BC에서 BH를 뺀다", "marks": [{"on": "{HC}", "note": "HC"}]},
            {"text": "AC = [[sqrt({AC2})]]{SIMP}", "hint": "△AHC 피타고라스"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")]],
        sol3="AC² = {AC2}에서 AC = {ANS_T}이다(제곱인수가 있으면 꺼낸다). HC를 {a}로 잘못 쓰면 AH² + {a}² = {AH2} + {a*a}{ika(a*a)} 되어 틀린다. 따라서 AC = {ANS_T}이다.",
        sol3_fig=steps(["AC² = {AH2} + {HC2} = {AC2}", "AC = {ANS_T}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="A에서 BC에 내린 수선의 발을 H라 하면 AH = {AH}, BH = {BH}이므로 HC = {HC}이다. 따라서 AC² = AH² + HC² = {AC2}이고 AC = [[sqrt({AC2})]]{SIMP}이다.",
        rubric=[
            {"element": "수선·특수각", "points": 3, "criterion": "AH = {AH}, BH = {BH}, HC = {HC}{eul(HC)} 구했다.", "partial": "HC = BC로 두었으면 인정하지 않는다."},
            {"element": "피타고라스·정리", "points": 2, "criterion": "AC = [[sqrt({AC2})]]{SIMP}임을 구했다.", "partial": "제곱인수를 꺼내지 않았으면 1점."},
        ],
        rubric_total=5,
    )


# t5 — 사각형의 넓이: 평행사변형 ab sin θ / 두 대각선 ½pq sin θ
def _ta5_rows():
    out = {}
    for th in (30, 45, 60, 120, 135, 150):
        s = SPECIAL[("sin", 180 - th if th > 90 else th)]
        sref = (f"sin {th}° = sin (180° − {th}°) = sin {180 - th}° = {mk(*s)}" if th > 90 else f"sin {th}° = {mk(*s)}")
        for a in range(2, 11):
            for b in range(a, 11):
                if (a * b) % 2:
                    continue
                S = mk(s[0] * a * b, s[1])
                if not exposed(S, str(a), str(b), str(th)):
                  out[f"p{th}-{a}-{b}"] = {"KIND": "평행사변형", "th": th, "a": a, "b": b, "ANS_T": S, "SV": mk(*s), "SREF": sref, "ansv": round(val(s[0] * a * b, s[1]), 6),
                                         "Q": f"[[seg(AB)]] = {a}, [[seg(AD)]] = {b}, [[angle(A)]] = [[deg({th})]]인 평행사변형 ABCD의 넓이를 구하시오.",
                                         "FORM": "S = AB × AD × sin A", "CALC": f"S = {a} × {b} × {mk(*s)} = {S}", "WHY": "평행사변형은 대각선으로 합동인 두 삼각형으로 나뉘므로 넓이는 △ABD의 2배: 2 × ½ × AB × AD × sin A = AB × AD × sin A"}
                if (a * b) % 4 == 0:
                    S2 = mk(s[0] * a * b / 2, s[1])
                    if exposed(S2, str(a), str(b), str(th)):
                        continue
                    out[f"d{th}-{a}-{b}"] = {"KIND": "두 대각선", "th": th, "a": a, "b": b, "ANS_T": S2, "SV": mk(*s), "SREF": sref, "ansv": round(val(s[0] * a * b / 2, s[1]), 6),
                                             "Q": f"두 대각선의 길이가 {a}, {b}이고 두 대각선이 이루는 각의 크기가 {th}°인 사각형의 넓이를 구하시오.",
                                             "FORM": "S = [[frac(1, 2)]] × (대각선) × (대각선) × sin(끼인각)", "CALC": f"S = [[frac(1, 2)]] × {a} × {b} × {mk(*s)} = {S2}", "WHY": "두 대각선에 평행한 직선으로 사각형을 감싸는 평행사변형을 만들면 그 넓이는 (대각선의 곱) × sin(끼인각)이고 사각형은 그 절반"}
    return out


TA5_ROWS = _ta5_rows()


def ta_t5():
    return tpl(TA, 5, TA_BASE,
        title="사각형의 넓이 — 평행사변형 ab sin θ, 두 대각선 ½pq sin θ",
        skill="평행사변형은 이웃한 두 변과 끼인각으로, 일반 사각형은 두 대각선과 그 사잇각으로 넓이 공식 쓰기",
        variant_axis={"도형": "평행사변형 / 두 대각선", "각": "30°·45°·60°·120°·135°·150°", "길이": "2~10"},
        difficulty=3,
        discriminates="평행사변형에는 ½이 없고 두 대각선 공식에는 ½이 있음을 구별하며, 둔각은 sin(180° − θ)로 바꾸는가",
        params=[{"name": "f", "values": {"in": list(TA5_ROWS)}}],
        table={"key": "f", "rows": TA5_ROWS},
        cost_values=["th", "a", "b", "ansv"],
        verify=["ansv > 0"],
        question="{Q}",
        answer="{ANS_T}", answer_alt=[],
        sol1="{WHY}이다. 따라서 {FORM}. {SREF}이므로 이 값을 넣어 계산한다.",
        sol2=[
            "{FORM}",
            "{SREF}",
            "{CALC}",
        ],
        sol2_fig=steps([
            {"text": "{FORM}", "hint": "{KIND}의 넓이"},
            {"text": "{SREF}", "hint": "특수각의 값", "marks": [{"on": "{SV}", "note": "sin"}]},
            {"text": "{CALC}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{KIND}의 넓이 공식에서 ½의 유무를 확인한다: 평행사변형은 삼각형 두 개(½ × 2 = 1), 두 대각선 공식은 ½이 남는다. 따라서 넓이는 {ANS_T}이다.",
        sol3_fig=steps(["{FORM}", "S = {ANS_T}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{FORM}이고 {SREF}이므로 {CALC}이다.",
        rubric=[
            {"element": "넓이 공식", "points": 3, "criterion": "{FORM}의 식을 세우고 {SREF}임을 썼다.", "partial": "½의 유무를 틀렸으면 1점."},
            {"element": "계산", "points": 2, "criterion": "S = {ANS_T}임을 구했다.", "partial": "근호 정리 실수면 1점."},
        ],
        rubric_total=5,
    )


TA_SEED = {
    "seed_id": TA, "category": "도형",
    "title": "삼각비의 활용 — 특수각 변의 길이·높이 측정·삼각형의 넓이·두 변 끼인각→대변·사각형의 넓이",
    "unit_id": "m3-2", "concept_ids": ["m3-2-04", "m3-2-05"],
    "schema_id": None, "schema_name": "삼각비의 활용 — 길이와 넓이",
    "source_item_ids": [],
    "note": "무리수 답은 표의 ANS_T 문자열(answer_var 없음, 검산은 float). 그림 좌표는 실제 각·길이대로 float 로 미리 계산.",
    "geometry": True,
    "templates": [geo(t) for t in (ta_t1(), ta_t2_final(), ta_t3(), ta_t4(), ta_t5())],
}


if __name__ == "__main__":
    for seed in (TB_SEED, TA_SEED):
        with_pitfalls(seed)
        dump(seed)
