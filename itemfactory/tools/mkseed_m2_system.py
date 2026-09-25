# itemfactory/tools/mkseed_m2_system.py — m2-1 연립방정식 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m2_system.py
#     → seeds/m2-1-sys-solve.json   (연립방정식 풀이: 가감법·대입법·해→상수·해가 같은 두 연립·자연수 해 개수·A=B=C·계수 바꿔 풀기, 7틀)
#     → seeds/m2-1-sys-apply-2.json (연립 활용 2: 걷기·뛰기·일·두 집단 평균·호수 둘레 만남·소금물 농도·입장료, 6틀)
#
# 해(x, y)는 파라미터로 두고 상수항을 역산한다 — 정수 해가 보장되고 검산이 곧 대입이다. 답은 m + n·mn 같은 수치.
from __future__ import annotations

import os
import sys
from fractions import Fraction
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import COMMON_APPLY, dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def _sg(v: int, var: str) -> str:
    """부호 붙은 항 조각(평문): 2 → '+ 2y', -1 → '− y', 0 → ''"""
    if v == 0:
        return ""
    a = abs(v)
    return ("+ " if v > 0 else "− ") + (var if a == 1 else f"{a}{var}")


def sgn_rows(vals, key, var, extra=None):
    rows = {}
    for v in vals:
        r = {f"{key.upper()}S": _sg(v, var)}
        if extra:
            r.update(extra(v))
        rows[str(v)] = r
    return {"key": key, "rows": rows}


BASE = {"process": "절차수행", "context": "무맥락", "time_limit": 120, "points": 4, "qtype": "short", "pool_target": 300}
NZ3 = [-3, -2, -1, 1, 2, 3]
NZ4 = [-4, -3, -2, -1, 1, 2, 3, 4]
NZ5 = [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]
ASKMN_ROWS = {"key": "ask", "rows": {
    "sum": {"ASK": "m + n", "w1": 1, "w2": 1, "wp": 0}, "diff": {"ASK": "m − n", "w1": 1, "w2": -1, "wp": 0}, "prod": {"ASK": "mn", "w1": 0, "w2": 0, "wp": 1}}}
ASKAB_ROWS = {"key": "ask", "rows": {
    "sum": {"ASK": "a + b", "w1": 1, "w2": 1, "wp": 0}, "diff": {"ASK": "a − b", "w1": 1, "w2": -1, "wp": 0}, "prod": {"ASK": "ab", "w1": 0, "w2": 0, "wp": 1}}}

# ═══════════════════════════════════════════════════════════════════ 1. 연립방정식의 풀이
SS = "m2-1-sys-solve"
SS_BASE = {**BASE, "prereq": ["일차방정식", "미지수가 2개인 일차방정식"], "ops": ["연립방정식"], "traps": ["가감법 부호", "대입 시 괄호"], "tags": ["연립방정식의 풀이"]}


def ss_t1():
    return tpl(SS, 1, SS_BASE,
        title="가감법으로 연립방정식 풀기 — 해 (m, n)으로 m + n (m − n, mn)",
        skill="한 문자의 계수를 맞추어 두 식을 더하거나 빼서 없애고, 구한 값을 대입해 나머지 문자를 구하기",
        variant_axis={"x의 계수": "2~5", "y의 계수": "±1~±4", "구하는 것": "m + n / m − n / mn"},
        discriminates="계수를 맞추어 곱한 뒤 부호에 맞게 더하거나 빼는가, 구한 값을 대입해 나머지를 구하는가",
        difficulty=2,
        params=[{"name": "a1", "values": {"in": [2, 3, 4]}}, {"name": "b1", "values": {"in": NZ4}}, {"name": "a2", "values": {"in": [2, 3, 5]}}, {"name": "b2", "values": {"in": NZ4}},
                {"name": "x0", "values": {"in": NZ4}}, {"name": "y0", "values": {"in": NZ4}}, {"name": "ask", "values": {"in": ["sum", "diff", "prod"]}}],
        table=[sgn_rows(NZ4, "b1", "y"), sgn_rows(NZ4, "b2", "y"), ASKMN_ROWS],
        derive={"c1": "a1*x0 + b1*y0", "c2": "a2*x0 + b2*y0", "cy": "a2*b1 - a1*b2", "ry": "a2*c1 - a1*c2", "b1y": "b1*y0", "xr": "c1 - b1*y0", "b2y": "b2*y0",
                "ans": "w1*x0 + w2*y0 + wp*x0*y0"},
        constraints=["cy != 0", "c1 != 0", "c2 != 0", "a1 != a2", "ans != 0", "ans not in (a1, a2, abs(b1), abs(b2), c1, c2)", "x0 != y0"],
        cost_values=["a1", "b1", "a2", "b2", "c1", "c2", "cy", "ry", "xr", "x0", "y0", "ans"],
        answer_var="ans",
        verify=["a1*x0 + b1*y0 == c1", "a2*x0 + b2*y0 == c2", "cy*y0 == ry", "ans == w1*x0 + w2*y0 + wp*x0*y0"],
        question="연립방정식 {co(a1)}x {B1S} = {c1}, {co(a2)}x {B2S} = {c2}의 해가 x = m, y = n일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="가감법은 한 문자의 계수의 절댓값을 같게 만든 뒤 두 식을 더하거나 빼서 그 문자를 없애는 방법이다. 첫 식에 {a2}, 둘째 식에 {a1}{eul(a1)} 곱하면 x의 계수가 모두 {a1*a2}{ika(a1*a2)} 되므로 빼서 x를 없앨 수 있다. y를 구한 뒤 한 식에 대입해 x를 구한다.",
        sol2=[
            "{co(a1)}x {B1S} = {c1} … ①, {co(a2)}x {B2S} = {c2} … ②에서 ① × {a2} − ② × {a1}{eul(a1)} 하면 {co(cy)}y = {ry}, y = {y0}",
            "y = {y0}{eul(y0)} ①에 대입하면 {co(a1)}x {sgn(b1y)} = {c1}, {co(a1)}x = {xr}, x = {x0}",
            "따라서 m = {x0}, n = {y0}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(a1)}x {B1S} = {c1}", "hint": "①"},
            {"text": "{co(a2)}x {B2S} = {c2}", "hint": "②"},
            {"text": "{co(cy)}y = {ry}  →  y = {y0}", "hint": "① × {a2} − ② × {a1} — x 소거", "marks": [{"on": "{co(cy)}y = {ry}", "note": "부호 주의"}]},
            {"text": "{co(a1)}x {sgn(b1y)} = {c1}  →  x = {x0}", "hint": "y = {y0} 대입"},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), reveal(1)], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3), hl("hint:3")], [reveal(4)]],
        sol3="x = {x0}, y = {y0}{eul(y0)} ②에 대입하면 {a2} × {pn(x0)} {sgn(b2y)} = {c2}{ro(c2)} 성립한다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["②: {a2} × {pn(x0)} {sgn(b2y)} = {c2} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{co(a1)}x {B1S} = {c1} … ①, {co(a2)}x {B2S} = {c2} … ②에서 ① × {a2} − ② × {a1}{eul(a1)} 하면 {co(cy)}y = {ry}, y = {y0}이다. 이것을 ①에 대입하면 x = {x0}이다. 따라서 m = {x0}, n = {y0}이고 {ASK} = {ans}이다.",
        rubric=[
            {"element": "한 문자 소거", "points": 3, "criterion": "① × {a2} − ② × {a1}{ro(a1)} x를 없애 {co(cy)}y = {ry}{eul(ry)} 얻었다.", "partial": "빼는 식의 부호 실수가 있으면 1점."},
            {"element": "나머지 문자", "points": 2, "criterion": "y = {y0}{eul(y0)} 대입해 x = {x0}{eul(x0)} 구했다.", "partial": "대입 계산 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


B2P = lambda v: {"B2P": ("+ " if v > 0 else "− ") + ("" if abs(v) == 1 else str(abs(v)))}    # noqa: E731 — 대입 시 계수 조각 '+ 2' / '−'


def ss_t2():
    return tpl(SS, 2, SS_BASE,
        title="대입법으로 연립방정식 풀기 — y = px + q를 대입",
        skill="한 식이 y = (x의 식) 꼴이면 다른 식의 y에 그대로 대입(괄호!)해 x의 일차방정식으로 만들기",
        variant_axis={"y = px + q": "p ±1~±3, q ±1~±6", "구하는 것": "m + n / m − n / mn"},
        discriminates="대입할 때 괄호를 써서 계수를 모든 항에 곱하는가, 구한 x를 다시 대입해 y를 구하는가",
        difficulty=2,
        params=[{"name": "p", "values": {"in": NZ3}}, {"name": "q", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}, {"name": "a", "values": {"in": [1, 2, 3, 4, 5]}},
                {"name": "b", "values": {"in": NZ4}}, {"name": "x0", "values": {"in": NZ4}}, {"name": "ask", "values": {"in": ["sum", "diff", "prod"]}}],
        table=[sgn_rows(NZ4, "b2", "y", B2P) | {"key": "b"}, ASKMN_ROWS],
        derive={"y0": "p*x0 + q", "c": "a*x0 + b*(p*x0 + q)", "bp": "b*p", "bq": "b*q", "k": "a + b*p", "r": "a*x0 + b*(p*x0 + q) - b*q",
                "ans": "w1*x0 + w2*(p*x0 + q) + wp*x0*(p*x0 + q)"},
        constraints=["y0 != 0", "k != 0", "abs(bp) >= 2", "c != 0", "ans != 0", "ans not in (p, abs(q), a, abs(b), c)", "x0 != y0", "abs(c) <= 40"],
        cost_values=["p", "q", "a", "b", "c", "bp", "bq", "k", "r", "x0", "y0", "ans"],
        answer_var="ans",
        verify=["y0 == p*x0 + q", "a*x0 + b*y0 == c", "k*x0 == r", "ans == w1*x0 + w2*y0 + wp*x0*y0"],
        question="연립방정식 y = {co(p)}x {sgn(q)}, {co(a)}x {B2S} = {c}의 해가 x = m, y = n일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="한 식이 y = {co(p)}x {sgn(q)}처럼 y에 대해 풀려 있으면 다른 식의 y 자리에 그 식을 통째로 대입한다(대입법). 대입할 때는 반드시 괄호로 묶어 y의 계수 {b}{eul(b)} 모든 항에 곱한다. x를 구한 뒤 y = {co(p)}x {sgn(q)}에 다시 대입해 y를 구한다.",
        sol2=[
            "y = {co(p)}x {sgn(q)} … ①을 {co(a)}x {B2S} = {c} … ②에 대입하면 {co(a)}x {B2P}({co(p)}x {sgn(q)}) = {c}",
            "괄호를 풀면 {co(a)}x {sgn(bp)}x {sgn(bq)} = {c}, 정리하면 {co(k)}x = {r}, x = {x0}",
            "x = {x0}{eul(x0)} ①에 대입하면 y = {p} × {pn(x0)} {sgn(q)} = {y0}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(a)}x {B2P}({co(p)}x {sgn(q)}) = {c}", "hint": "①을 ②의 y에 대입 — 괄호!", "marks": [{"on": "({co(p)}x {sgn(q)})", "note": "괄호로 묶어 대입"}]},
            {"text": "{co(k)}x = {r}  →  x = {x0}", "hint": "괄호 풀고 정리"},
            {"text": "y = {p} × {pn(x0)} {sgn(q)} = {y0}", "hint": "①에 x 대입"},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3)]],
        sol3="x = {x0}, y = {y0}{eul(y0)} ②에 대입하면 {a} × {pn(x0)} {sgn(b*y0)} = {c}{ro(c)} 성립한다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["②: {a} × {pn(x0)} {sgn(b*y0)} = {c} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = {co(p)}x {sgn(q)}{eul(q)} {co(a)}x {B2S} = {c}에 대입하면 {co(a)}x {B2P}({co(p)}x {sgn(q)}) = {c}, {co(k)}x = {r}, x = {x0}이고 y = {y0}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[
            {"element": "대입", "points": 3, "criterion": "y 자리에 {co(p)}x {sgn(q)}{eul(q)} 괄호로 묶어 대입해 {co(a)}x {B2P}({co(p)}x {sgn(q)}) = {c}{eul(c)} 세웠다.", "partial": "괄호 없이 대입해 부호가 어긋났으면 1점."},
            {"element": "x·y 구하기", "points": 2, "criterion": "x = {x0}, y = {y0}{eul(y0)} 구했다.", "partial": "x만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


def _y0_rows():
    vals = [-4, -3, -2, 2, 3, 4]
    return {"key": "yk", "rows": {str(v): {"y0": v, "Y0B": _sg(v, "b"), "Y0A": _sg(-v, "a")} for v in vals}}


def ss_t3():
    return tpl(SS, 3, SS_BASE,
        title="해가 주어진 연립방정식 ax + by = c₁, bx − ay = c₂에서 a + b (a − b, ab)",
        skill="해를 두 식에 대입해 a, b에 대한 연립방정식을 만들고 가감법으로 풀기",
        variant_axis={"해": "x, y ±2~±4", "구하는 것": "a + b / a − b / ab"},
        discriminates="대입한 뒤 a, b가 미지수인 새 연립방정식으로 보고 푸는가, 부호를 바르게 옮기는가",
        difficulty=3,
        params=[{"name": "a", "values": {"in": NZ4}}, {"name": "b", "values": {"in": NZ4}}, {"name": "x0", "values": {"in": [-4, -3, -2, 2, 3, 4]}}, {"name": "yk", "values": {"in": ["-4", "-3", "-2", "2", "3", "4"]}},
                {"name": "ask", "values": {"in": ["sum", "diff", "prod"]}}],
        table=[_y0_rows(), sgn_rows(NZ4, "b", "y"), {"key": "a", "rows": {str(v): {"NAS": _sg(-v, "y")} for v in NZ4}}, ASKAB_ROWS],
        derive={"c1": "a*x0 + b*y0", "c2": "b*x0 - a*y0", "ss": "x0*x0 + y0*y0", "ra": "x0*c1 - y0*c2", "x0a": "x0*a", "rb": "c1 - x0*a",
                "ans": "w1*a + w2*b + wp*a*b"},
        constraints=["c1 != 0", "c2 != 0", "a != b", "ans != 0", "ans not in (c1, c2, x0, y0)", "abs(a) != abs(b)"],
        cost_values=["a", "b", "x0", "y0", "c1", "c2", "ss", "ra", "rb", "ans"],
        answer_var="ans",
        verify=["a*x0 + b*y0 == c1", "b*x0 - a*y0 == c2", "ss*a == ra", "y0*b == rb", "ans == w1*a + w2*b + wp*a*b"],
        question="연립방정식 ax + by = {c1}, bx − ay = {c2}의 해가 x = {x0}, y = {y0}일 때, 상수 a, b에 대하여 {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="해 x = {x0}, y = {y0}{eun(y0)} 두 식을 모두 만족하므로 대입하면 a, b에 대한 두 일차방정식이 생긴다. 이제 a, b를 미지수로 보고 연립방정식을 풀면 된다. 계수가 x, y의 값이므로 부호를 조심해 정리한다.",
        sol2=[
            "x = {x0}, y = {y0}{eul(y0)} 대입하면 {co(x0)}a {Y0B} = {c1} … ①, {co(x0)}b {Y0A} = {c2} … ②",
            "b를 없애기 위해 ① × {pn(x0)} − ② × {pn(y0)}{eul(y0)} 하면 {ss}a = {ra}, a = {a}",
            "a = {a}{eul(a)} ①에 대입하면 {x0a} {Y0B} = {c1}, {co(y0)}b = {rb}, b = {b}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(x0)}a {Y0B} = {c1}  … ①", "hint": "ax + by = {c1}에 대입"},
            {"text": "{co(x0)}b {Y0A} = {c2}  … ②", "hint": "bx − ay = {c2}에 대입"},
            {"text": "{ss}a = {ra}  →  a = {a}", "hint": "(① × {pn(x0)}) − (② × {pn(y0)}) — b 소거", "marks": [{"on": "{ss}a", "note": "{pn(x0)}² + {pn(y0)}²"}]},
            {"text": "{co(y0)}b = {rb}  →  b = {b}", "hint": "①에 a 대입"},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3), hl("hint:3")], [reveal(4)]],
        # 검산은 곱을 계산한 값으로 적는다 — a·b 가 ±1 일 때 '1 × 3'·'-1 × 3' 이 드러나지 않게 (09-25 2차)
        sol3="a = {a}, b = {b}{eul(b)} 넣으면 {co(a)}x {BS} = {c1}, {co(b)}x {NAS} = {c2}이고, x = {x0}, y = {y0}{eul(y0)} 대입하면 {a*x0} {sgn(b*y0)} = {c1}, {b*x0} {sgn(-a*y0)} = {c2}{ro(c2)} 모두 성립한다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["{a*x0} {sgn(b*y0)} = {c1} ✓", "{b*x0} {sgn(-a*y0)} = {c2} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        model_answer="x = {x0}, y = {y0}{eul(y0)} 대입하면 {co(x0)}a {Y0B} = {c1}, {co(x0)}b {Y0A} = {c2}이다. 두 식을 연립하여 풀면 a = {a}, b = {b}이므로 {ASK} = {ans}이다.",
        rubric=[
            {"element": "대입해 식 세우기", "points": 3, "criterion": "해를 대입해 {co(x0)}a {Y0B} = {c1}, {co(x0)}b {Y0A} = {c2}{eul(c2)} 세웠다.", "partial": "한 식만 세웠거나 부호 실수가 있으면 1점."},
            {"element": "a, b 구하기", "points": 2, "criterion": "가감법으로 a = {a}, b = {b}{eul(b)} 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


Q2 = [-4, -3, -2, 2, 3, 4]      # 계수 ±2~±4 (× 1 표기 회피)


def ss_t4():
    return tpl(SS, 4, SS_BASE,
        title="두 연립방정식의 해가 서로 같을 때 상수 a, b — a + b (a − b, ab)",
        skill="a, b가 없는 두 식을 골라 먼저 연립하여 해를 구하고, 그 해를 나머지 식에 대입해 a, b를 구하기",
        variant_axis={"해": "x, y ±1~±4", "구하는 것": "a + b / a − b / ab"},
        discriminates="네 식 중 상수가 없는 두 식을 골라 먼저 푸는 전략을 쓰는가",
        difficulty=3, process="문제해결",
        params=[{"name": "p", "values": {"in": [1, 2, 3]}}, {"name": "q1", "values": {"in": Q2}}, {"name": "r", "values": {"in": [1, 2, 3]}}, {"name": "q2", "values": {"in": Q2}},
                {"name": "q3", "values": {"in": NZ3}}, {"name": "a", "values": {"in": NZ4}}, {"name": "u1", "values": {"in": [1, 2, 3]}}, {"name": "b", "values": {"in": NZ4}},
                {"name": "x0", "values": {"in": NZ4}}, {"name": "y0", "values": {"in": NZ4}}, {"name": "ask", "values": {"in": ["sum", "diff", "prod"]}}],
        table=[sgn_rows(Q2, "q1", "y"), sgn_rows(Q2, "q2", "y"), sgn_rows(NZ3, "q3", "y"), sgn_rows(NZ4, "y0", "b"), sgn_rows(NZ4, "b", "y"), ASKAB_ROWS],
        derive={"s": "p*x0 + q1*y0", "d": "r*x0 + q2*y0", "t": "a*x0 + q3*y0", "u": "u1*x0 + b*y0", "dx": "p*q2 - r*q1", "rx": "s*q2 - d*q1", "px0": "p*x0", "q3y0": "q3*y0", "u1x0": "u1*x0",
                "ans": "w1*a + w2*b + wp*a*b"},
        constraints=["dx != 0", "s != 0", "d != 0", "t != 0", "u != 0", "ans != 0", "ans not in (p, r, s, d, t, u, u1, abs(q1), abs(q2), abs(q3), x0, y0)", "x0 != y0", "a != b", "p*q2 != r*q1"],
        cost_values=["p", "q1", "r", "q2", "s", "d", "dx", "rx", "x0", "y0", "a", "b", "ans"],
        answer_var="ans",
        verify=["p*x0 + q1*y0 == s", "r*x0 + q2*y0 == d", "a*x0 + q3*y0 == t", "u1*x0 + b*y0 == u", "dx*x0 == rx", "ans == w1*a + w2*b + wp*a*b"],
        question="연립방정식 {co(p)}x {Q1S} = {s}, ax {Q3S} = {t}의 해와 연립방정식 {co(r)}x {Q2S} = {d}, {co(u1)}x + by = {u}의 해가 서로 같을 때, 상수 a, b에 대하여 {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 연립방정식의 해가 같으므로, 네 식 가운데 a, b가 없는 {co(p)}x {Q1S} = {s}와 {co(r)}x {Q2S} = {d}{eul(d)} 먼저 연립하면 공통인 해를 구할 수 있다. 그 해를 a가 있는 식과 b가 있는 식에 각각 대입하면 a, b가 정해진다.",
        sol2=[
            "a, b가 없는 {co(p)}x {Q1S} = {s} … ①, {co(r)}x {Q2S} = {d} … ③을 연립: ① × {pn(q2)} − ③ × {pn(q1)}{eul(q1)} 하면 {co(dx)}x = {rx}, x = {x0}",
            "x = {x0}{eul(x0)} ①에 대입하면 {px0} {Q1S} = {s}, y = {y0}",
            "x = {x0}, y = {y0}{eul(y0)} ax {Q3S} = {t}에 대입하면 {co(x0)}a {sgn(q3y0)} = {t}, a = {a}; {co(u1)}x + by = {u}에 대입하면 {u1x0} {Y0S} = {u}, b = {b}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(p)}x {Q1S} = {s},  {co(r)}x {Q2S} = {d}", "hint": "a, b가 없는 두 식부터"},
            {"text": "{co(dx)}x = {rx}  →  x = {x0},  y = {y0}", "hint": "① × {pn(q2)} − ③ × {pn(q1)} 로 y 소거"},
            {"text": "{co(x0)}a {sgn(q3y0)} = {t}  →  a = {a}", "hint": "ax {Q3S} = {t}에 대입"},
            {"text": "{u1x0} {Y0S} = {u}  →  b = {b}", "hint": "{co(u1)}x + by = {u}에 대입"},
            {"text": "{ASK} = {ans}", "marks": [{"on": "{ans}", "note": "a, b 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")], [reveal(4), hl("mark:4-0")]],
        sol3="x = {x0}, y = {y0}{eun(y0)} 네 식 {co(p)}x {Q1S} = {s}, {co(a)}x {Q3S} = {t}, {co(r)}x {Q2S} = {d}, {co(u1)}x {BS} = {u}{eul(u)} 모두 만족한다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["(x, y) = ({x0}, {y0}) → 네 식 모두 성립 ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{co(p)}x {Q1S} = {s}, {co(r)}x {Q2S} = {d}{eul(d)} 연립하여 풀면 x = {x0}, y = {y0}이다. 이것을 ax {Q3S} = {t}, {co(u1)}x + by = {u}에 대입하면 a = {a}, b = {b}이므로 {ASK} = {ans}이다.",
        rubric=[
            {"element": "공통인 해", "points": 3, "criterion": "a, b가 없는 두 식을 연립해 x = {x0}, y = {y0}{eul(y0)} 구했다.", "partial": "가감법 부호 실수면 1점."},
            {"element": "a, b 구하기", "points": 2, "criterion": "해를 대입해 a = {a}, b = {b}{eul(b)} 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


# t5 — 자연수 해의 개수 (표: a, b, c 와 해 목록 미리 계산)
NAT_ROWS = {}
for _a in range(1, 7):
    for _b in range(1, 7):
        if _a == _b:
            continue
        for _c in range(8, 41):
            sols = [(x, (_c - _a * x) // _b) for x in range(1, _c) if _c - _a * x > 0 and (_c - _a * x) % _b == 0]
            if 2 <= len(sols) <= 6 and (_c - _b) // _a <= 8:
                xmax = (_c - _b) // _a
                tab = ", ".join(f"x = {x}일 때 y = {(_c - _a * x) / _b:g}" + ("" if (_c - _a * x) % _b == 0 else "(×)") for x in range(1, xmax + 1))
                NAT_ROWS[f"{_a}-{_b}-{_c}"] = {"a": _a, "b": _b, "c": _c, "CNT": len(sols), "LIST": ", ".join(f"({x}, {y})" for x, y in sols), "XMAX": xmax, "TAB": tab,
                                             "YEXPR": f"y = ({_c} − {'' if _a == 1 else _a}x) ÷ {_b}" if _b > 1 else f"y = {_c} − {'' if _a == 1 else _a}x"}


def ss_t5():
    return tpl(SS, 5, SS_BASE,
        title="x, y가 자연수일 때 일차방정식 ax + by = c의 해의 개수",
        skill="x = 1, 2, 3, …을 차례로 대입해 y가 자연수가 되는 순서쌍만 세기",
        variant_axis={"계수": "1~6", "상수항": "8~40", "해의 개수": "2~6"},
        discriminates="x를 자연수 범위에서 빠짐없이 대입하고 y가 자연수(0 제외)인 것만 세는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(NAT_ROWS)}}],
        table={"key": "f", "rows": NAT_ROWS},
        derive={"ans": "CNT"},
        constraints=["ans not in (a, b, c)"],
        cost_values=["a", "b", "c", "XMAX", "ans"],
        answer_var="ans",
        verify=["ans == CNT", "ans >= 2", "XMAX*a + b <= c"],
        question="x, y가 자연수일 때, 일차방정식 {co(a)}x + {co(b)}y = {c}의 해의 개수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="미지수가 2개인 일차방정식은 해가 무수히 많지만, x, y가 자연수라는 조건이 붙으면 몇 개로 제한된다. {YEXPR}{ro(b)} 고쳐 x = 1, 2, 3, …을 차례로 대입하고 y가 자연수가 되는 경우만 고른다. y가 0이나 음수, 분수가 되면 해가 아니다.",
        sol2=[
            "{YEXPR}이므로 x = 1부터 차례로 대입한다 — y가 자연수여야 하므로 x는 {XMAX} 이하",
            "{TAB}",
            "자연수 해는 (x, y) = {LIST}이므로 {ans}개",
        ],
        sol2_fig=steps([
            {"text": "{YEXPR}", "hint": "y에 대해 정리"},
            {"text": "x = 1, 2, …, {XMAX} 대입", "hint": "y > 0 이려면 x ≤ {XMAX}"},
            {"text": "(x, y) = {LIST}", "hint": "y가 자연수인 것만", "marks": [{"on": "{LIST}", "note": "{ans}개"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="x가 {XMAX}보다 크면 y가 0 이하가 되어 자연수가 아니므로 더 볼 필요가 없다. 찾은 순서쌍 {LIST}{eul(c)} 식에 넣으면 모두 {c}{ika(c)} 된다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["x ≤ {XMAX}까지만 확인", "{LIST} → {ans}개"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{YEXPR}에 x = 1, 2, …을 대입하면 y가 자연수가 되는 해는 (x, y) = {LIST}이다. 따라서 해의 개수는 {ans}이다.",
        rubric=[
            {"element": "대입해 찾기", "points": 3, "criterion": "x = 1부터 차례로 대입해 y가 자연수인 순서쌍 {LIST}{eul(c)} 찾았다.", "partial": "하나를 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "해의 개수 {ans}{eul(ans)} 답했다.", "partial": "y = 0인 경우를 포함해 셌으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def ss_t6():
    return tpl(SS, 6, SS_BASE,
        title="A = B = C 꼴의 방정식 풀기 — 해 (m, n)으로 m + n (m − n, mn)",
        skill="A = B = C를 A = C, B = C의 두 식으로 나누어 연립방정식으로 풀기",
        variant_axis={"계수": "±1~±4", "구하는 것": "m + n / m − n / mn"},
        discriminates="세 식이 같다는 것을 두 개의 등식(A = C, B = C)으로 바꾸어 연립하는가",
        difficulty=3,
        params=[{"name": "p", "values": {"in": NZ3}}, {"name": "q", "values": {"in": Q2}}, {"name": "r", "values": {"in": NZ3}}, {"name": "x0", "values": {"in": NZ4}}, {"name": "y0", "values": {"in": NZ4}},
                {"name": "ask", "values": {"in": ["sum", "diff", "prod"]}}],
        table=[sgn_rows(Q2, "q", "y"), ASKMN_ROWS],
        derive={"t": "p*x0 + q*y0", "s": "(p*x0 + q*y0 - r*x0)/y0", "dx": "p*s - r*q", "rx": "t*s - t*q", "px0": "p*x0",
                "ans": "w1*x0 + w2*y0 + wp*x0*y0"},
        constraints=["s == floor(s)", "abs(s) >= 2", "s != q", "p != r", "t != 0", "dx != 0", "ans != 0", "ans not in (p, r, t, abs(q), abs(s))", "x0 != y0", "abs(t) <= 40"],
        cost_values=["p", "q", "r", "s", "t", "dx", "rx", "x0", "y0", "ans"],
        answer_var="ans",
        verify=["p*x0 + q*y0 == t", "r*x0 + s*y0 == t", "dx*x0 == rx", "ans == w1*x0 + w2*y0 + wp*x0*y0"],
        question="방정식 {co(p)}x {QS} = {co(r)}x {sgn(s)}y = {t}의 해가 x = m, y = n일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="A = B = C 꼴의 방정식은 세 식 가운데 두 개씩 짝지어 A = C, B = C의 연립방정식으로 바꾸어 푼다(어느 두 쌍을 골라도 해는 같다). 여기서는 상수 {t}{ika(t)} 있는 C = {t}{eul(t)} 두 식에 각각 붙이면 계산이 간단하다.",
        sol2=[
            "A = C, B = C로 나누면 {co(p)}x {QS} = {t} … ①, {co(r)}x {sgn(s)}y = {t} … ②",
            "① × {pn(s)} − ② × {pn(q)}{eul(q)} 하면 {co(dx)}x = {rx}, x = {x0}",
            "x = {x0}{eul(x0)} ①에 대입하면 {px0} {QS} = {t}, y = {y0}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(p)}x {QS} = {t}  … ①", "hint": "A = C"},
            {"text": "{co(r)}x {sgn(s)}y = {t}  … ②", "hint": "B = C"},
            {"text": "{co(dx)}x = {rx}  →  x = {x0}", "hint": "① × {pn(s)} − ② × {pn(q)} — y 소거"},
            {"text": "{px0} {QS} = {t}  →  y = {y0}", "hint": "①에 대입"},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), reveal(1), hl("hint:0", "hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")], [reveal(4)]],
        sol3="x = {x0}, y = {y0}{eul(y0)} 세 식에 넣으면 {co(p)}x {QS} = {t}, {co(r)}x {sgn(s)}y = {r} × {pn(x0)} {sgn(s*y0)} = {t}{ro(t)} 셋이 모두 같다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["A = {t}, B = {r} × {pn(x0)} {sgn(s*y0)} = {t}, C = {t} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{co(p)}x {QS} = {t}, {co(r)}x {sgn(s)}y = {t}{eul(t)} 연립하여 풀면 x = {x0}, y = {y0}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[
            {"element": "연립방정식으로 바꾸기", "points": 3, "criterion": "A = C, B = C의 두 식 {co(p)}x {QS} = {t}, {co(r)}x {sgn(s)}y = {t}{eul(t)} 세웠다.", "partial": "A = B 한 식만 세웠으면 인정하지 않는다."},
            {"element": "해 구하기", "points": 2, "criterion": "x = {x0}, y = {y0}{eul(y0)} 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


# t7 — a, b를 바꾸어 놓고 푼 해가 주어질 때 처음 연립방정식의 해 (표: 유효한 조합만)
SWAP_ROWS = {}
for _a in [v for v in range(-5, 6) if v]:
    for _b in [v for v in range(-5, 6) if v]:
        if abs(_a) == abs(_b):
            continue
        for _x in NZ4:
            for _y in NZ4:
                c1, c2 = _a * _x + _b * _y, _b * _x - _a * _y
                dd = _a * _a + _b * _b
                pp, qq = Fraction(_b * c1 + _a * c2, dd), Fraction(_a * c1 - _b * c2, dd)
                if pp.denominator != 1 or qq.denominator != 1 or (pp, qq) == (_x, _y) or 0 in (c1, c2, pp, qq) or abs(c1) > 40 or abs(c2) > 40 or _x == _y:
                    continue
                p, q = int(pp), int(qq)
                SWAP_ROWS[f"{_a}-{_b}-{_x}-{_y}"] = {"a": _a, "b": _b, "x0": _x, "y0": _y, "c1": c1, "c2": c2, "p": p, "q": q, "pq": p * p + q * q,
                                                     "PA": _sg(q, "a"), "PB": _sg(-q, "b"), "QA": _sg(p, "a"), "QB": _sg(p, "b"),
                                                     "ra": q * c1 + p * c2, "CP": "" if p == 1 else ("-" if p == -1 else str(p)),
                                                     "rb": c1 - q * _a, "ax0": _a * _x, "BS": _sg(_b, "y"), "AS": _sg(-_a, "y")}


def ss_t7():
    return tpl(SS, 7, SS_BASE,
        title="a, b를 바꾸어 놓고 푼 해가 주어질 때 처음 연립방정식의 해 — m + n (m − n, mn)",
        skill="바꾸어 놓은 연립방정식에 잘못 구한 해를 대입해 a, b를 구한 뒤 처음 연립방정식을 바르게 풀기",
        variant_axis={"계수": "±1~±5", "구하는 것": "m + n / m − n / mn"},
        discriminates="'바꾸어 놓고 풀었다'를 계수가 바뀐 연립방정식에 주어진 해가 맞는 것으로 해석하는가",
        difficulty=4, process="문제해결",
        params=[{"name": "f", "values": {"in": list(SWAP_ROWS)}}, {"name": "ask", "values": {"in": ["sum", "diff", "prod"]}}],
        table=[{"key": "f", "rows": SWAP_ROWS}, ASKMN_ROWS],
        derive={"ans": "w1*x0 + w2*y0 + wp*x0*y0", "ab2": "a*a + b*b", "rx": "a*c1 + b*c2"},
        constraints=["ans != 0", "ans not in (c1, c2, p, q)"],
        cost_values=["c1", "c2", "p", "q", "a", "b", "x0", "y0", "ans"],
        answer_var="ans",
        verify=["a*x0 + b*y0 == c1", "b*x0 - a*y0 == c2", "b*p + a*q == c1", "a*p - b*q == c2", "pq*a == ra", "ab2*x0 == rx", "ans == w1*x0 + w2*y0 + wp*x0*y0"],
        question="연립방정식 ax + by = {c1}, bx − ay = {c2}에서 a와 b를 서로 바꾸어 놓고 풀었더니 해가 x = {p}, y = {q}이었다. 처음 연립방정식의 해가 x = m, y = n일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="a와 b를 바꾸어 놓은 연립방정식은 bx + ay = {c1}, ax − by = {c2}이고, 잘못 구한 해 x = {p}, y = {q}{eun(q)} 이 바뀐 연립방정식을 만족한다. 대입하면 a, b에 대한 연립방정식이 되어 a, b를 구할 수 있고, 그다음 처음 연립방정식을 바르게 풀면 된다.",
        sol2=[
            "바꾸어 놓은 연립방정식 bx + ay = {c1}, ax − by = {c2}에 x = {p}, y = {q}{eul(q)} 대입: {CP}b {PA} = {c1} … ③, {CP}a {PB} = {c2} … ④",
            "(③ × {pn(q)}) + (④ × {pn(p)})에서 {pq}a = {ra}, a = {a}이고 ③에서 b = {b}",
            "처음 연립방정식은 {co(a)}x {BS} = {c1} … ①, {co(b)}x {AS} = {c2} … ②이고, (① × {pn(a)}) + (② × {pn(b)})에서 {ab2}x = {rx}, x = {x0}, y = {y0}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "bx + ay = {c1},  ax − by = {c2}", "hint": "a, b를 바꾼 연립방정식 — 여기에 ({p}, {q})가 맞는다"},
            {"text": "{CP}b {PA} = {c1},  {CP}a {PB} = {c2}", "hint": "x = {p}, y = {q} 대입"},
            {"text": "{pq}a = {ra}  →  a = {a},  b = {b}", "hint": "(③ × {pn(q)}) + (④ × {pn(p)})"},
            {"text": "{co(a)}x {BS} = {c1},  {co(b)}x {AS} = {c2}", "hint": "처음 연립방정식"},
            {"text": "{ab2}x = {rx}  →  x = {x0},  y = {y0}", "hint": "(① × {pn(a)}) + (② × {pn(b)})", "marks": [{"on": "x = {x0}", "note": "바른 해"}]},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")], [reveal(4), hl("hint:4", "mark:4-0")], [reveal(5)]],
        sol3="a = {a}, b = {b}일 때 처음 연립방정식 {co(a)}x {BS} = {c1}, {co(b)}x {AS} = {c2}에 x = {x0}, y = {y0}{eul(y0)} 넣으면 {ax0} {sgn(b*y0)} = {c1}, {b*x0} {sgn(-a*y0)} = {c2}{ro(c2)} 모두 성립하고, 바꾼 연립방정식에는 ({p}, {q})가 맞는다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["처음: {ax0} {sgn(b*y0)} = {c1} ✓,  {b*x0} {sgn(-a*y0)} = {c2} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="a, b를 바꾼 연립방정식 bx + ay = {c1}, ax − by = {c2}에 x = {p}, y = {q}{eul(q)} 대입하면 {CP}b {PA} = {c1}, {CP}a {PB} = {c2}이고, 이를 풀면 a = {a}, b = {b}이다. 처음 연립방정식 {co(a)}x {BS} = {c1}, {co(b)}x {AS} = {c2}{eul(c2)} 풀면 x = {x0}, y = {y0}이므로 {ASK} = {ans}이다.",
        rubric=[
            {"element": "바꾼 식에 대입", "points": 3, "criterion": "bx + ay = {c1}, ax − by = {c2}에 x = {p}, y = {q}{eul(q)} 대입해 a, b의 연립방정식을 세웠다.", "partial": "처음 식에 그대로 대입했으면 인정하지 않는다."},
            {"element": "a, b 구하기", "points": 2, "criterion": "a = {a}, b = {b}{eul(b)} 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "처음 해와 답", "points": 3, "criterion": "처음 연립방정식을 풀어 x = {x0}, y = {y0}{eul(y0)} 구하고 {ASK} = {ans}{eul(ans)} 답했다.", "partial": "잘못 구한 해 ({p}, {q})로 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


SS_SEED = {
    "seed_id": SS, "category": "연산",
    "title": "연립방정식의 풀이 — 가감법·대입법·해→상수·해가 같은 두 연립·자연수 해·A = B = C·계수 바꿔 풀기",
    "unit_id": "m2-1", "concept_ids": ["m2-1-11", "m2-1-12", "m2-1-13"],
    "schema_id": None, "schema_name": "연립일차방정식의 풀이와 상수 결정",
    "source_item_ids": [],
    "note": "해(x0, y0)와 계수를 파라미터로 두고 상수항을 역산. 계수 ±1 은 표 조각(+ y / − y), '× 1' 표기는 계수 범위 제약으로 회피. 자연수 해·계수 바꿔 풀기는 표에 유효 조합만 미리 계산.",
    "geometry": False,
    "templates": [ss_t1(), ss_t2(), ss_t3(), ss_t4(), ss_t5(), ss_t6(), ss_t7()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 연립방정식의 활용 2
SA = "m2-1-sys-apply-2"
SA_BASE = {**COMMON_APPLY, "ops": ["연립방정식", "사칙"], "prereq": ["연립방정식의 풀이"], "traps": ["단위(시·분)", "미지수 설정"], "tags": ["연립방정식의 활용"], "qtype": "short", "pool_target": 300}
NAME_ROWS = {"key": "nm", "rows": {"1": {"S": "지수"}, "2": {"S": "민준"}, "3": {"S": "서연"}, "4": {"S": "도윤"}, "5": {"S": "하은"}, "6": {"S": "시우"}}}
PLACE_ROWS = {"key": "pl", "rows": {"1": {"PLACE": "학교", "DEST": "학교"}, "2": {"PLACE": "도서관", "DEST": "도서관"}, "3": {"PLACE": "체육관", "DEST": "체육관"}}}
WALK_ASK = {"key": "ask", "rows": {"walk": {"ASKW": "걸은 거리", "iw": 1}, "run": {"ASKW": "뛴 거리", "iw": 0}}}


def sa_t1():
    return tpl(SA, 1, SA_BASE,
        title="걷다가 뛰어서 도착 — 걸은 거리·뛴 거리 (거리 합·시간 합)",
        skill="걸은 거리 x, 뛴 거리 y로 놓고 (거리의 합)·(시간의 합 = 거리 ÷ 속력) 두 식을 세우기",
        variant_axis={"속력": "걷기 시속 3~6 km, 뛰기 시속 6~20 km", "구하는 것": "걸은 거리 / 뛴 거리"},
        discriminates="시간 = 거리 ÷ 속력으로 시간의 합 식을 세우고, 분을 시간(÷60)으로 맞추는가",
        difficulty=3,
        params=[{"name": "nm", "values": {"in": list(NAME_ROWS["rows"])}}, {"name": "pl", "values": {"in": ["1", "2", "3"]}}, {"name": "a", "values": {"in": [3, 4, 5, 6]}}, {"name": "b", "values": {"in": [6, 10, 12, 15, 20]}},
                {"name": "x", "values": {"int": [1, 5]}}, {"name": "y", "values": {"int": [1, 5]}}, {"name": "ask", "values": {"in": ["walk", "run"]}}],
        table=[NAME_ROWS, PLACE_ROWS, WALK_ASK],
        derive={"D": "x + y", "ka": "60/a", "kb": "60/b", "T": "60*x/a + 60*y/b", "kaD": "60/a*(x + y)", "dk": "60/a - 60/b", "ry": "60/a*(x + y) - T", "ans": "iw*x + (1 - iw)*y"},
        constraints=["b > a", "T == floor(T)", "T <= 120", "ans not in (a, b, D, T)", "x != y"],
        cost_values=["a", "b", "D", "T", "ka", "kb", "x", "y", "ans"],
        answer_var="ans",
        verify=["x + y == D", "ka*x + kb*y == T", "dk*y == ry", "ka*a == 60", "kb*b == 60"],
        question="{S}{eun(S)} 집에서 {D} km 떨어진 {DEST}까지 가는데 처음에는 시속 {a} km로 걷다가 도중에 시속 {b} km로 뛰어서 모두 {T}분 만에 도착하였다. {S}{ika(S)} {ASKW}는 몇 km인지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="걸은 거리를 x km, 뛴 거리를 y km라 하면 거리의 합은 {D} km이고, 시간은 (거리) ÷ (속력)이므로 걸은 시간은 [[frac(x, {a})]]시간, 뛴 시간은 [[frac(y, {b})]]시간이다. 전체 시간 {T}분은 [[frac({T}, 60)]]시간으로 바꾸어 시간의 합 식을 세운다. 두 식을 연립해 x, y를 구한다.",
        sol2=[
            "걸은 거리 x km, 뛴 거리 y km: x + y = {D} … ①, [[frac(x, {a})]] + [[frac(y, {b})]] = [[frac({T}, 60)]] … ②",
            "② × 60: {ka}x + {kb}y = {T} … ③, ① × {ka} − ③: {dk}y = {ry}, y = {y}",
            "①에서 x = {D} − {y} = {x}이므로 {ASKW}는 {ans} km",
        ],
        sol2_fig=steps([
            {"text": "x + y = {D}", "hint": "거리의 합"},
            {"text": "[[frac(x, {a})]] + [[frac(y, {b})]] = [[frac({T}, 60)]]", "hint": "시간의 합 — {T}분 = [[frac({T}, 60)]]시간"},
            {"text": "{ka}x + {kb}y = {T}", "hint": "② × 60"},
            {"text": "{dk}y = {ry}  →  y = {y},  x = {x}", "hint": "① × {ka} − ③", "marks": [{"on": "y = {y}", "note": "뛴 거리"}]},
            {"text": "{ASKW} = {ans} km"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3", "mark:3-0")], [reveal(4)]],
        sol3="걸은 {x} km는 시속 {a} km로 {ka*x}분, 뛴 {y} km는 시속 {b} km로 {kb*y}분이 걸려 합이 {T}분이고 거리의 합도 {D} km이다. 따라서 {ASKW}는 {ans} km이다.",
        sol3_fig=steps(["{x} km ÷ 시속 {a} km = {ka*x}분,  {y} km ÷ 시속 {b} km = {kb*y}분", "{ka*x} + {kb*y} = {T}분 ✓,  {x} + {y} = {D} km ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="걸은 거리를 x km, 뛴 거리를 y km라 하면 x + y = {D}, [[frac(x, {a})]] + [[frac(y, {b})]] = [[frac({T}, 60)]]이다. 둘째 식에 60을 곱해 {ka}x + {kb}y = {T}{eul(T)} 얻고 연립하여 풀면 x = {x}, y = {y}이다. 따라서 {ASKW}는 {ans} km이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "x + y = {D}, [[frac(x, {a})]] + [[frac(y, {b})]] = [[frac({T}, 60)]]{eul(T)} 세웠다.", "partial": "분을 시간으로 바꾸지 않았으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "연립하여 x = {x}, y = {y}{eul(y)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKW} {ans} km를 답했다.", "partial": "다른 쪽 거리를 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


# t2 — 일: A 혼자 m일, B 혼자 n일 (표: 두 조합 (p, q), (r, s) 미리 계산)
def _work_rows():
    out = {}
    for m in range(4, 13):
        for n in range(4, 13):
            if m == n:
                continue
            pairs = [(p, q) for q in range(1, n) for p in range(1, m) if p * n + q * m == m * n]
            if len(pairs) < 2:
                continue
            for i in range(len(pairs)):
                for j in range(len(pairs)):
                    if i == j:
                        continue
                    (p, q), (r, s) = pairs[i], pairs[j]
                    for ask, (who, days) in (("A", ("A", m)), ("B", ("B", n))):
                        # A: ① × s − ② × q → (ps − rq)a = s − q ; B: ① × r − ② × p → (qr − sp)b = r − p
                        if ask == "A":
                            dd, num, m1, m2 = p * s - r * q, s - q, s, q
                        else:
                            dd, num, m1, m2 = q * r - s * p, r - p, r, p
                        if dd == 0 or num == 0 or Fraction(num, dd) != Fraction(1, days):
                            continue
                        key = f"{m}-{n}-{p}-{q}-{r}-{s}-{ask}"
                        out[key] = {"m": m, "n": n, "p": p, "q": q, "r": r, "s": s, "WHO": who, "OTHER": "B" if who == "A" else "A", "VAR": "a" if who == "A" else "b",
                                    "DAYS": days, "dd": dd, "num": num, "m1": m1, "m2": m2, "ELIM": f"(① × {m1}) − (② × {m2})",
                                    "OTHERD": n if who == "A" else m}
    return out


WORK_ROWS = _work_rows()


def sa_t2():
    return tpl(SA, 2, SA_BASE,
        title="두 사람이 나누어 한 일 — 혼자 하면 며칠 걸리는가",
        skill="전체 일을 1로 놓고 하루에 하는 일의 양을 미지수로 두어 두 조합의 식을 세우고, 역수로 날수를 구하기",
        variant_axis={"혼자 걸리는 날수": "4~12일", "구하는 사람": "A / B"},
        discriminates="하루 일의 양(1/날수)을 미지수로 두는가, 구한 값의 역수를 날수로 답하는가",
        difficulty=3,
        params=[{"name": "f", "values": {"in": list(WORK_ROWS)}}],
        table={"key": "f", "rows": WORK_ROWS},
        derive={"ans": "DAYS", "val": "1/DAYS"},
        constraints=["ans not in (p, q, r, s)"],
        cost_values=["p", "q", "r", "s", "dd", "num", "ans"],
        answer_var="ans",
        verify=["dd*val == num", "p*val + q/OTHERD == 1 or p/OTHERD + q*val == 1", "ans == DAYS"],
        question="어떤 일을 A가 {p}일 동안 한 다음 B가 {q}일 동안 하면 끝나고, A가 {r}일 동안 한 다음 B가 {s}일 동안 해도 끝난다. 이 일을 {WHO} 혼자 하면 며칠이 걸리는지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="전체 일의 양을 1로 놓고 A, B가 하루에 하는 일의 양을 각각 a, b라 하면, 두 조합은 {co(p)}a + {co(q)}b = 1, {co(r)}a + {co(s)}b = 1의 두 식이 된다. 가감법으로 {VAR}를 구하면 그것이 {WHO}가 하루에 하는 일의 양이고, 혼자 걸리는 날수는 그 역수다.",
        sol2=[
            "A, B가 하루에 하는 일의 양을 각각 a, b라 하면 {co(p)}a + {co(q)}b = 1 … ①, {co(r)}a + {co(s)}b = 1 … ②",
            "{ELIM}에서 {dd}{VAR} = {num}, {VAR} = {val}",
            "{WHO}{eun(WHO)} 하루에 전체의 {val}{eul(ans)} 하므로 혼자 하면 {ans}일이 걸린다",
        ],
        sol2_fig=steps([
            {"text": "{co(p)}a + {co(q)}b = 1", "hint": "① 첫째 조합 (전체 일 = 1)"},
            {"text": "{co(r)}a + {co(s)}b = 1", "hint": "② 둘째 조합"},
            {"text": "{dd}{VAR} = {num}  →  {VAR} = {val}", "hint": "{ELIM}"},
            {"text": "{WHO} 혼자: {ans}일", "hint": "하루 {val} → 역수", "marks": [{"on": "{ans}일", "note": "{val}의 역수"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3", "mark:3-0")]],
        sol3="{WHO}{ika(WHO)} 하루에 {val}, {OTHER}{ika(OTHER)} 하루에 [[frac(1, {OTHERD})]]을 하면 첫째 조합은 {p} × {val_a} + {q} × {val_b} = 1이 되어 맞다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["A: 하루 [[frac(1, {ma})]], B: 하루 [[frac(1, {nb})]]", "{p} × [[frac(1, {ma})]] + {q} × [[frac(1, {nb})]] = 1 ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="A, B가 하루에 하는 일의 양을 각각 a, b라 하면 {co(p)}a + {co(q)}b = 1, {co(r)}a + {co(s)}b = 1이다. {ELIM}에서 {dd}{VAR} = {num}, {VAR} = {val}이므로 {WHO} 혼자 하면 {ans}일이 걸린다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "전체를 1로 놓고 {co(p)}a + {co(q)}b = 1, {co(r)}a + {co(s)}b = 1을 세웠다.", "partial": "한 식만 세웠으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "가감법으로 {VAR} = {val}{eul(ans)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "역수를 취해 {ans}일을 답했다.", "partial": "{val}{eul(ans)} 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def sa_t2_final():
    t = sa_t2()
    t["derive"].update({"ma": "m", "nb": "n", "val_a": "1/m", "val_b": "1/n"})
    return t


ORG_ROWS = {"key": "org", "rows": {"1": {"ORG": "어느 학급", "TEST": "수학 시험"}, "2": {"ORG": "어느 동아리", "TEST": "영어 시험"}, "3": {"ORG": "어느 학원 반", "TEST": "과학 시험"}}}
MF_ASK = {"key": "ask", "rows": {"m": {"ASKW": "남학생", "im": 1}, "f": {"ASKW": "여학생", "im": 0}}}


def sa_t3():
    return tpl(SA, 3, SA_BASE,
        title="전체 평균과 남녀 평균이 주어질 때 남학생(여학생) 수",
        skill="사람 수의 합과 점수의 총합(평균 × 인원) 두 식을 세워 풀기",
        variant_axis={"인원": "20~40명", "평균": "60~90점"},
        discriminates="총점 = 평균 × 인원으로 둘째 식을 세우는가(평균끼리 더하지 않는가)",
        difficulty=3,
        params=[{"name": "org", "values": {"in": ["1", "2", "3"]}}, {"name": "x", "values": {"int": [8, 22]}}, {"name": "y", "values": {"in": [5, 6, 8, 10, 12, 15, 16, 20]}},
                {"name": "a", "values": {"step": [60, 90, 2]}}, {"name": "M", "values": {"int": [65, 85]}}, {"name": "ask", "values": {"in": ["m", "f"]}}],
        table=[ORG_ROWS, MF_ASK],
        derive={"n": "x + y", "Mn": "M*(x + y)", "b": "(M*(x + y) - a*x)/y", "tot": "a*x + b*y", "bma": "b - a", "ry": "M*(x + y) - a*(x + y)", "ans": "im*x + (1 - im)*y"},
        constraints=["b == floor(b)", "b >= 55", "b <= 96", "a != b", "x != y", "n <= 40", "ans not in (n, M, a, b)"],
        cost_values=["n", "M", "a", "b", "Mn", "bma", "ry", "x", "y", "ans"],
        answer_var="ans",
        verify=["x + y == n", "a*x + b*y == M*n", "bma*y == ry"],
        question="{ORG}의 학생 {n}명이 본 {TEST}의 전체 평균은 {M}점이고, 남학생의 평균은 {a}점, 여학생의 평균은 {b}점이었다. {ASKW}은 몇 명인지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="남학생 수를 x명, 여학생 수를 y명이라 하면 인원의 합은 {n}명이다. 평균은 (총점) ÷ (인원)이므로 전체 총점은 {M} × {n} = {Mn}점이고, 이것은 남학생 총점 {a}x와 여학생 총점 {b}y의 합이다. 평균끼리 더하면 안 되고 총점으로 식을 세운다.",
        sol2=[
            "남학생 x명, 여학생 y명: x + y = {n} … ①, {a}x + {b}y = {M} × {n} = {Mn} … ②",
            "② − ① × {a}: {bma}y = {ry}, y = {y}",
            "①에서 x = {n} − {y} = {x}이므로 {ASKW}은 {ans}명",
        ],
        sol2_fig=steps([
            {"text": "x + y = {n}", "hint": "인원의 합"},
            {"text": "{a}x + {b}y = {Mn}", "hint": "총점 = 평균 × 인원 = {M} × {n}"},
            {"text": "{bma}y = {ry}  →  y = {y},  x = {x}", "hint": "② − ① × {a}", "marks": [{"on": "y = {y}", "note": "여학생 수"}]},
            {"text": "{ASKW} = {ans}명"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]],
        sol3="남학생 {x}명의 총점 {a} × {x} = {a*x}점과 여학생 {y}명의 총점 {b} × {y} = {b*y}점을 더하면 {Mn}점이고, {n}명으로 나누면 평균 {M}점이 맞다. 따라서 {ASKW}은 {ans}명이다.",
        sol3_fig=steps(["{a} × {x} + {b} × {y} = {Mn}", "{Mn} ÷ {n} = {M}점 ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="남학생 수를 x명, 여학생 수를 y명이라 하면 x + y = {n}, {a}x + {b}y = {M} × {n} = {Mn}이다. 연립하여 풀면 x = {x}, y = {y}이므로 {ASKW}은 {ans}명이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "x + y = {n}, {a}x + {b}y = {Mn}{eul(Mn)} 세웠다.", "partial": "평균끼리 더해 세웠으면 인정하지 않는다."},
            {"element": "해 구하기", "points": 3, "criterion": "연립하여 x = {x}, y = {y}{eul(y)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKW} {ans}명을 답했다.", "partial": "다른 쪽 인원을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


PAIR_ROWS = {"key": "pr", "rows": {"1": {"S1": "지수", "S2": "민준"}, "2": {"S1": "서연", "S2": "도윤"}, "3": {"S1": "하은", "S2": "시우"}}}
LAKE_ASK = {"key": "ask", "rows": {"fast": {"ASKS": "S1", "ia": 1}, "slow": {"ASKS": "S2", "ia": 0}}}


def sa_t4():
    return tpl(SA, 4, SA_BASE,
        title="호수 둘레를 반대 방향·같은 방향으로 돌아 만나는 시간 — 두 사람의 속력",
        skill="반대 방향이면 속력의 합, 같은 방향이면 속력의 차로 둘레를 나타내는 두 식을 세우기",
        variant_axis={"둘레": "600~3000 m", "구하는 사람": "빠른 쪽 / 느린 쪽"},
        discriminates="반대 방향은 (속력의 합) × 시간 = 둘레, 같은 방향은 (속력의 차) × 시간 = 둘레임을 구별하는가",
        difficulty=3,
        params=[{"name": "pr", "values": {"in": ["1", "2", "3"]}}, {"name": "a", "values": {"step": [60, 120, 10]}}, {"name": "b", "values": {"step": [20, 80, 10]}},
                {"name": "L", "values": {"in": [600, 800, 900, 1000, 1200, 1500, 1800, 2000, 2400, 3000]}}, {"name": "ask", "values": {"in": ["fast", "slow"]}}],
        table=[PAIR_ROWS, LAKE_ASK],
        derive={"t1": "L/(a + b)", "t2": "L/max(a - b, 1)", "sm": "a + b", "df": "a - b", "ans": "ia*a + (1 - ia)*b", "two": "2*a"},
        constraints=["a > b", "t1 == floor(t1)", "t2 == floor(t2)", "t2 <= 60", "t1 >= 3", "ans not in (L, t1, t2)"],
        cost_values=["L", "t1", "t2", "sm", "df", "a", "b", "ans"],
        answer_var="ans",
        verify=["t1*(a + b) == L", "t2*(a - b) == L", "sm + df == two"],
        question="둘레의 길이가 {L} m인 호수의 둘레를 {S1}{wa(S1)} {S2}{ika(S2)} 같은 지점에서 동시에 출발하여 서로 반대 방향으로 돌면 {t1}분 후에 처음으로 만나고, 같은 방향으로 돌면 {t2}분 후에 처음으로 만난다. {S1}{ika(S1)} {S2}보다 빠를 때, {ASKN}의 속력은 분속 몇 m인지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{S1}의 속력을 분속 x m, {S2}의 속력을 분속 y m라 하자. 반대 방향으로 돌면 두 사람이 간 거리의 합이 둘레 {L} m가 될 때 만나므로 {t1}(x + y) = {L}이고, 같은 방향으로 돌면 빠른 사람이 한 바퀴 더 돌아 거리의 차가 {L} m가 될 때 만나므로 {t2}(x − y) = {L}이다.",
        sol2=[
            "{S1} 분속 x m, {S2} 분속 y m: 반대 방향 {t1}(x + y) = {L}에서 x + y = {sm} … ①, 같은 방향 {t2}(x − y) = {L}에서 x − y = {df} … ②",
            "① + ②: 2x = {two}, x = {a}이고 ①에서 y = {sm} − {a} = {b}",
            "따라서 {ASKN}의 속력은 분속 {ans} m",
        ],
        sol2_fig=steps([
            {"text": "{t1}(x + y) = {L}  →  x + y = {sm}", "hint": "반대 방향 — 거리의 합이 둘레"},
            {"text": "{t2}(x − y) = {L}  →  x − y = {df}", "hint": "같은 방향 — 거리의 차가 둘레"},
            {"text": "2x = {two}  →  x = {a},  y = {b}", "hint": "① + ②", "marks": [{"on": "x = {a}", "note": "{S1}"}]},
            {"text": "{ASKN}: 분속 {ans} m"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]],
        sol3="분속 {a} m와 {b} m로 반대 방향으로 {t1}분 가면 {a} × {t1} + {b} × {t1} = {L} m로 한 바퀴가 되고, 같은 방향으로 {t2}분 가면 차가 {a} × {t2} − {b} × {t2} = {L} m로 한 바퀴 차이가 난다. 따라서 {ASKN}의 속력은 분속 {ans} m이다.",
        sol3_fig=steps(["반대: ({a} + {b}) × {t1} = {L} ✓", "같은: ({a} − {b}) × {t2} = {L} ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{S1}의 속력을 분속 x m, {S2}의 속력을 분속 y m라 하면 {t1}(x + y) = {L}, {t2}(x − y) = {L}에서 x + y = {sm}, x − y = {df}이다. 연립하여 풀면 x = {a}, y = {b}이므로 {ASKN}의 속력은 분속 {ans} m이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "{t1}(x + y) = {L}, {t2}(x − y) = {L}{eul(L)} 세웠다.", "partial": "합과 차를 바꾸어 세웠으면 인정하지 않는다."},
            {"element": "해 구하기", "points": 3, "criterion": "x = {a}, y = {b}{eul(b)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKN}의 속력 분속 {ans} m를 답했다.", "partial": "다른 사람의 속력을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def sa_t4_final():
    t = sa_t4()
    # 구하는 사람 이름(ASKN)은 짝 이름표(pr)와 ask 의 조합 — 표 행 문자열로 둘 수 없어 두 표를 합친다
    rows = {}
    for pk, pv in PAIR_ROWS["rows"].items():
        for ak, av in LAKE_ASK["rows"].items():
            rows[f"{pk}-{ak}"] = {**pv, **av, "ASKN": pv["S1"] if av["ia"] == 1 else pv["S2"]}
    t["params"] = [{"name": "pa", "values": {"in": list(rows)}}, {"name": "a", "values": {"step": [60, 120, 10]}}, {"name": "b", "values": {"step": [20, 80, 10]}},
                   {"name": "L", "values": {"in": [600, 800, 900, 1000, 1200, 1500, 1800, 2000, 2400, 3000]}}]
    t["table"] = {"key": "pa", "rows": rows}
    return t


SALT_ASK = {"key": "ask", "rows": {"p": {"ip": 1}, "q": {"ip": 0}}}


def sa_t5():
    return tpl(SA, 5, SA_BASE,
        title="농도가 다른 두 소금물을 섞어 원하는 농도 만들기 — 각각 몇 g",
        skill="소금물의 양의 합과 소금의 양의 합(농도 × 양) 두 식을 세워 풀기",
        variant_axis={"농도": "3~20 %", "전체 양": "200~600 g", "구하는 것": "묽은 쪽 / 진한 쪽"},
        discriminates="소금의 양 = (농도/100) × (소금물의 양)으로 둘째 식을 세우는가",
        difficulty=3,
        params=[{"name": "p", "values": {"in": [3, 4, 5, 6, 8, 10]}}, {"name": "q", "values": {"in": [8, 10, 12, 15, 18, 20]}}, {"name": "x", "values": {"step": [50, 400, 50]}}, {"name": "y", "values": {"step": [50, 400, 50]}},
                {"name": "ask", "values": {"in": ["p", "q"]}}],
        table=SALT_ASK,
        derive={"W": "x + y", "r": "(p*x + q*y)/(x + y)", "rW": "p*x + q*y", "qmp": "q - p", "ry": "p*x + q*y - p*(x + y)", "ASKP": "ip*p + (1 - ip)*q", "ans": "ip*x + (1 - ip)*y"},
        constraints=["q > p", "r == floor(r)", "W <= 600", "x != y", "ans not in (p, q, r, W)"],
        cost_values=["p", "q", "r", "W", "rW", "qmp", "ry", "x", "y", "ans"],
        answer_var="ans",
        verify=["x + y == W", "p*x + q*y == r*W", "qmp*y == ry", "r > p", "r < q"],
        question="{p}%의 소금물과 {q}%의 소금물을 섞어서 {r}%의 소금물 {W} g을 만들려고 한다. {ASKP}%의 소금물은 몇 g 섞어야 하는지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{p}%의 소금물을 x g, {q}%의 소금물을 y g이라 하면 소금물의 양의 합은 {W} g이다. 소금물을 섞어도 소금의 양은 변하지 않으므로, 소금의 양 = (농도) ÷ 100 × (소금물의 양)으로 두 소금물의 소금의 합이 {r}% 소금물 {W} g의 소금의 양과 같다는 식을 세운다.",
        sol2=[
            "{p}% 소금물 x g, {q}% 소금물 y g: x + y = {W} … ①, [[frac({p}, 100)]]x + [[frac({q}, 100)]]y = [[frac({r}, 100)]] × {W} … ②",
            "② × 100: {p}x + {q}y = {rW} … ③, ③ − ① × {p}: {qmp}y = {ry}, y = {y}",
            "①에서 x = {W} − {y} = {x}이므로 {ASKP}%의 소금물은 {ans} g",
        ],
        sol2_fig=steps([
            {"text": "x + y = {W}", "hint": "소금물의 양"},
            {"text": "[[frac({p}, 100)]]x + [[frac({q}, 100)]]y = [[frac({r}, 100)]] × {W}", "hint": "소금의 양 = 농도/100 × 양"},
            {"text": "{p}x + {q}y = {rW}", "hint": "② × 100"},
            {"text": "{qmp}y = {ry}  →  y = {y},  x = {x}", "hint": "③ − ① × {p}", "marks": [{"on": "y = {y}", "note": "{q}% 소금물"}]},
            {"text": "{ASKP}% 소금물: {ans} g"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3", "mark:3-0")], [reveal(4)]],
        sol3="{p}% 소금물 {x} g의 소금은 {dec(p*x/100)} g, {q}% 소금물 {y} g의 소금은 {dec(q*y/100)} g으로 합이 {dec(rW/100)} g이고, 이것은 {r}% 소금물 {W} g의 소금 {dec(rW/100)} g과 같다. 따라서 {ASKP}%의 소금물은 {ans} g이다.",
        sol3_fig=steps(["소금: {dec(p*x/100)} + {dec(q*y/100)} = {dec(rW/100)} g", "{r}% × {W} g = {dec(rW/100)} g ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{p}%의 소금물을 x g, {q}%의 소금물을 y g이라 하면 x + y = {W}, [[frac({p}, 100)]]x + [[frac({q}, 100)]]y = [[frac({r}, 100)]] × {W}이다. 연립하여 풀면 x = {x}, y = {y}이므로 {ASKP}%의 소금물은 {ans} g이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "x + y = {W}와 소금의 양 식 {p}x + {q}y = {rW}{eul(rW)} 세웠다.", "partial": "농도끼리 더해 세웠으면 인정하지 않는다."},
            {"element": "해 구하기", "points": 3, "criterion": "x = {x}, y = {y}{eul(y)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKP}% 소금물 {ans} g을 답했다.", "partial": "다른 소금물의 양을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


VENUE_ROWS = {"key": "vn", "rows": {"1": {"PLACE": "박물관"}, "2": {"PLACE": "놀이공원"}, "3": {"PLACE": "미술관"}, "4": {"PLACE": "동물원"}}}
AC_ASK = {"key": "ask", "rows": {"a": {"ASKW": "어른", "ia": 1}, "c": {"ASKW": "어린이", "ia": 0}}}


def sa_t6():
    return tpl(SA, 6, SA_BASE,
        title="어른·어린이 입장료 — 인원의 합과 금액의 합으로 인원 구하기",
        skill="어른 x명, 어린이 y명으로 놓고 인원의 합·금액의 합 두 식을 세워 가감법으로 풀기",
        variant_axis={"입장료": "어른 3000~8000원, 어린이 1000~4000원", "인원": "6~20명"},
        discriminates="금액 식에서 각 단가에 인원을 곱하는가, 가감법 후 구한 값을 다시 대입하는가",
        difficulty=2,
        params=[{"name": "vn", "values": {"in": ["1", "2", "3", "4"]}}, {"name": "a", "values": {"in": [3000, 4000, 5000, 6000, 8000]}}, {"name": "b", "values": {"in": [1000, 1500, 2000, 2500, 3000, 4000]}},
                {"name": "x", "values": {"int": [2, 10]}}, {"name": "y", "values": {"int": [3, 12]}}, {"name": "ask", "values": {"in": ["a", "c"]}}],
        table=[VENUE_ROWS, AC_ASK],
        derive={"n": "x + y", "T": "a*x + b*y", "amb": "a - b", "rx": "a*x + b*y - b*(x + y)", "ans": "ia*x + (1 - ia)*y"},
        constraints=["a > b", "x != y", "ans not in (n, a, b, T)"],
        cost_values=["a", "b", "n", "T", "amb", "rx", "x", "y", "ans"],
        answer_var="ans",
        verify=["x + y == n", "a*x + b*y == T", "amb*x == rx"],
        question="어느 {PLACE}의 입장료는 어른이 {a}원, 어린이가 {b}원이다. 어른과 어린이를 합하여 {n}명이 입장하는 데 모두 {T}원을 냈다면 {ASKW}는 몇 명인지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="어른 수를 x명, 어린이 수를 y명이라 하면 인원의 합은 {n}명이고, 낸 돈은 어른 입장료 {a}x원과 어린이 입장료 {b}y원의 합 {T}원이다. 두 식을 연립해 가감법으로 푼다.",
        sol2=[
            "어른 x명, 어린이 y명: x + y = {n} … ①, {a}x + {b}y = {T} … ②",
            "② − ① × {b}: {amb}x = {rx}, x = {x}",
            "①에서 y = {n} − {x} = {y}이므로 {ASKW}는 {ans}명",
        ],
        sol2_fig=steps([
            {"text": "x + y = {n}", "hint": "인원의 합"},
            {"text": "{a}x + {b}y = {T}", "hint": "금액의 합"},
            {"text": "{amb}x = {rx}  →  x = {x},  y = {y}", "hint": "② − ① × {b}", "marks": [{"on": "x = {x}", "note": "어른 수"}]},
            {"text": "{ASKW} = {ans}명"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]],
        sol3="어른 {x}명의 입장료 {a} × {x} = {a*x}원과 어린이 {y}명의 입장료 {b} × {y} = {b*y}원을 더하면 {T}원이고 인원도 {n}명이다. 따라서 {ASKW}는 {ans}명이다.",
        sol3_fig=steps(["{a} × {x} + {b} × {y} = {T}원 ✓", "{x} + {y} = {n}명 ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="어른 수를 x명, 어린이 수를 y명이라 하면 x + y = {n}, {a}x + {b}y = {T}이다. 연립하여 풀면 x = {x}, y = {y}이므로 {ASKW}는 {ans}명이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "x + y = {n}, {a}x + {b}y = {T}{eul(T)} 세웠다.", "partial": "단가에 인원을 곱하지 않았으면 인정하지 않는다."},
            {"element": "해 구하기", "points": 3, "criterion": "x = {x}, y = {y}{eul(y)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKW} {ans}명을 답했다.", "partial": "다른 쪽 인원을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


SA_SEED = {
    "seed_id": SA, "category": "활용",
    "title": "연립방정식의 활용 2 — 걷기·뛰기·일·두 집단 평균·호수 둘레 만남·소금물·입장료",
    "unit_id": "m2-1", "concept_ids": ["m2-1-14", "m2-1-15"],
    "schema_id": None, "schema_name": "연립방정식 세우기(문장제) 2",
    "source_item_ids": [],
    "note": "해(x, y)를 파라미터로 두고 조건값(총 시간·평균·농도·만나는 시간)을 역산해 정수 조건으로 거른다. 일 문제는 (m, n)과 두 조합을 표에 미리 계산.",
    "geometry": False,
    "templates": [sa_t1(), sa_t2_final(), sa_t3(), sa_t4_final(), sa_t5(), sa_t6()],
}


if __name__ == "__main__":
    for seed in (SS_SEED, SA_SEED):
        with_pitfalls(seed)
        dump(seed)
