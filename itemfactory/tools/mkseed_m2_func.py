# itemfactory/tools/mkseed_m2_func.py — m2-1 함수·일차함수 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m2_func.py
#     → seeds/m2-1-func-value.json     (함수와 함숫값: f(p) ± f(q)·a/x + c 의 상수·두 조건→a + b·f(p)→f(q), 4틀)
#     → seeds/m2-1-line-props.json     (일차함수 그래프의 성질: 평행이동→m·평행이동→k·절편 합·평행 조건 k·삼각형 넓이·절편→기울기, 6틀)
#     → seeds/m2-1-line-apply.json     (일차함수의 활용: 물통·양초·기온·점 P 이동 넓이·용수철, 5틀)
#     → seeds/m2-1-line-intersect.json (일차방정식의 그래프: 기울기·절편 합·교점·해 무수히 많음·해 없음·세 직선 한 점·축에 평행, 7틀)
#
# 그래프는 coordplane 의 lines[].points 로 틀 안에서 자른 선분을 그린다(line_clip 파생). 한 직선에 점을 놓는 그림은 점이 직선 위에 있어야
# recheck F4 를 통과하므로 절편·지나는 점만 찍는다.
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import COMMON_APPLY, dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def cplane(xs, ys, points, lines=None, **extra):
    a = {"x": xs, "y": ys, "points": points}
    if lines:
        a["lines"] = lines
    a.update(extra)
    return [{"fn": "coordplane", "args": a}]


def line_clip(pre: str, a: str, b: str, xlo="xlo", xhi="xhi", ylo="ylo", yhi="yhi") -> dict:
    """y = a x + b 를 틀 [xlo,xhi]×[ylo,yhi] 안에서 자른 선분의 끝점 파생 — {pre}xs,{pre}ys,{pre}xe,{pre}ye (a ≠ 0)"""
    return {f"{pre}xa": f"({ylo} - ({b}))/({a})", f"{pre}xb": f"({yhi} - ({b}))/({a})",
            f"{pre}xs": f"max({xlo}, min({pre}xa, {pre}xb))", f"{pre}xe": f"min({xhi}, max({pre}xa, {pre}xb))",
            f"{pre}ys": f"({a})*{pre}xs + ({b})", f"{pre}ye": f"({a})*{pre}xe + ({b})"}


def seg(pre: str, **kw):
    d = {"points": [[f"{{{pre}xs}}", f"{{{pre}ys}}"], [f"{{{pre}xe}}", f"{{{pre}ye}}"]]}
    d.update(kw)
    return d


def _sg(v: int, var: str) -> str:
    a = abs(v)
    if var == "":
        return ("+ " if v > 0 else "− ") + str(a)
    return ("+ " if v > 0 else "− ") + (var if a == 1 else f"{a}{var}")


def sgn_rows(vals, key, var):
    return {"key": key, "rows": {str(v): {f"{key.upper()}S": _sg(v, var)} for v in vals}}


BASE = {"process": "절차수행", "context": "무맥락", "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}
NZ4 = [-4, -3, -2, -1, 1, 2, 3, 4]
NZ6 = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
NZ8 = [-8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8]
FRAME6 = {"xlo": "-6", "xhi": "6", "ylo": "-6", "yhi": "6"}

# ═══════════════════════════════════════════════════════════════════ 1. 함수와 함숫값
FV = "m2-1-func-value"
FV_BASE = {**BASE, "prereq": ["함수의 뜻", "식의 값"], "ops": ["함숫값"], "traps": ["대입 시 부호"], "tags": ["함수", "함숫값"]}
FOP_ROWS = {"key": "op", "rows": {"sum": {"FOP": "+", "s": 1}, "diff": {"FOP": "−", "s": -1}}}


def fv_t1():
    return tpl(FV, 1, FV_BASE,
        title="일차함수 f(x) = ax + b의 함숫값 — f(p) ± f(q)",
        skill="f(p)는 x에 p를 대입한 값임을 알고 두 함숫값을 각각 구해 더하거나 빼기",
        variant_axis={"계수": "a ±1~±4, b ±1~±8", "대입값": "±1~±6"},
        discriminates="f(p)를 x = p일 때의 값으로 읽는가, 음수를 대입할 때 괄호를 쓰는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ4}}, {"name": "b", "values": {"in": NZ8}}, {"name": "p", "values": {"in": NZ6}}, {"name": "q", "values": {"in": NZ6}}, {"name": "op", "values": {"in": ["sum", "diff"]}}],
        table=FOP_ROWS,
        derive={"fp": "a*p + b", "fq": "a*q + b", "ans": "a*p + b + s*(a*q + b)"},
        constraints=["p != q", "ans != 0", "ans not in (a, abs(b), p, q)", "fp != 0", "fq != 0"],
        cost_values=["a", "b", "p", "q", "fp", "fq", "ans"],
        answer_var="ans",
        verify=["ans == fp + s*fq", "fp == a*p + b", "fq == a*q + b"],
        question="함수 f(x) = {co(a)}x {sgn(b)}에 대하여 f({p}) {FOP} f({q})의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="f(p)는 함수 f(x)의 x에 p를 대입해 얻는 함숫값이다. f({p})는 x = {p}를, f({q})는 x = {q}를 각각 대입해 구하고, 두 값을 {FOP} 기호로 계산한다. 음수를 대입할 때는 괄호를 써서 부호 실수를 막는다.",
        sol2=[
            "f({p}) = {a} × {pn(p)} {sgn(b)} = {fp}",
            "f({q}) = {a} × {pn(q)} {sgn(b)} = {fq}",
            "따라서 f({p}) {FOP} f({q}) = {fp} {FOP} {pn(fq)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "f({p}) = {a} × {pn(p)} {sgn(b)} = {fp}", "hint": "x = {p} 대입"},
            {"text": "f({q}) = {a} × {pn(q)} {sgn(b)} = {fq}", "hint": "x = {q} 대입"},
            {"text": "{fp} {FOP} {pn(fq)} = {ans}", "marks": [{"on": "{ans}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="f({p}) = {fp}, f({q}) = {fq}는 각각 x에 {p}, {q}{eul(q)} 넣은 값이 맞고, {fp} {FOP} {pn(fq)} = {ans}이다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["f({p}) = {fp},  f({q}) = {fq}", "{fp} {FOP} {pn(fq)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="f({p}) = {a} × {pn(p)} {sgn(b)} = {fp}, f({q}) = {a} × {pn(q)} {sgn(b)} = {fq}이므로 f({p}) {FOP} f({q}) = {fp} {FOP} {pn(fq)} = {ans}이다.",
        rubric=[
            {"element": "함숫값 구하기", "points": 3, "criterion": "f({p}) = {fp}, f({q}) = {fq}{eul(fq)} 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "f({p}) {FOP} f({q}) = {ans}{eul(ans)} 구했다.", "partial": "뺄셈의 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def fv_t2():
    return tpl(FV, 2, FV_BASE,
        title="f(x) = a/x + c에서 f(p)의 값이 주어질 때 상수 a",
        skill="함숫값 조건 f(p) = v를 식에 대입해 a에 대한 방정식으로 풀기",
        variant_axis={"p": "±1~±6", "c": "±1~±5"},
        discriminates="f(p) = v를 a/p + c = v로 옮기고 분수 방정식을 바르게 푸는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": [-12, -10, -9, -8, -6, -5, -4, -3, -2, 2, 3, 4, 5, 6, 8, 9, 10, 12]}}, {"name": "p", "values": {"in": NZ6}}, {"name": "c", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}}],
        derive={"ap": "a/p", "v": "a/p + c", "vc": "a/p", "ans": "a"},
        constraints=["ap == floor(ap)", "v != 0", "ans not in (p, c, v)", "ans != vc"],
        cost_values=["a", "p", "c", "ap", "v"],
        answer_var="ans",
        verify=["ans/p + c == v", "vc == v - c", "vc*p == ans"],
        question="함수 f(x) = [[frac(a, x)]] {sgn(c)}에서 f({p}) = {v}일 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="f({p})는 x = {p}를 대입한 값이므로 f({p}) = [[frac(a, {p})]] {sgn(c)}이다. 이것이 {v}{wa(v)} 같다는 방정식을 세우고, 상수항을 이항한 뒤 양변에 {p}{eul(p)} 곱해 a를 구한다.",
        sol2=[
            "x = {p}를 대입하면 f({p}) = [[frac(a, {p})]] {sgn(c)} = {v}",
            "{c}{eul(c)} 이항하면 [[frac(a, {p})]] = {v} − {pn(c)} = {vc}",
            "양변에 {p}{eul(p)} 곱하면 a = {vc} × {pn(p)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "[[frac(a, {p})]] {sgn(c)} = {v}", "hint": "f({p}) = {v}"},
            {"text": "[[frac(a, {p})]] = {vc}", "hint": "상수항 이항"},
            {"text": "a = {vc} × {pn(p)} = {ans}", "marks": [{"on": "{ans}", "note": "양변 × {p}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="a = {ans}{eul(ans)} 넣으면 f({p}) = [[frac({ans}, {p})]] {sgn(c)} = {ap} {sgn(c)} = {v}{ro(v)} 조건과 같다. 따라서 a = {ans}이다.",
        sol3_fig=steps(["f({p}) = [[frac({ans}, {p})]] {sgn(c)} = {v} ✓", "a = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="f({p}) = [[frac(a, {p})]] {sgn(c)} = {v}에서 [[frac(a, {p})]] = {vc}이므로 a = {vc} × {pn(p)} = {ans}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "x = {p}를 대입해 [[frac(a, {p})]] {sgn(c)} = {v}{eul(v)} 세웠다.", "partial": "대입 위치가 틀렸으면 인정하지 않는다."},
            {"element": "a 구하기", "points": 2, "criterion": "이항하고 양변에 {p}{eul(p)} 곱해 a = {ans}{eul(ans)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def fv_t3():
    return tpl(FV, 3, FV_BASE,
        title="f(x) = ax + b에서 두 함숫값이 주어질 때 a + b (a − b, ab)",
        skill="두 조건 f(p) = v₁, f(q) = v₂를 대입해 a, b의 연립방정식으로 풀기",
        variant_axis={"계수": "a ±1~±4, b ±1~±6", "대입값": "±1~±5"},
        discriminates="두 조건을 두 식으로 세우고 빼서 a를 먼저 구하는가",
        difficulty=3, process="문제해결",
        params=[{"name": "a", "values": {"in": NZ4}}, {"name": "b", "values": {"in": NZ6}}, {"name": "p", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}}, {"name": "q", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}},
                {"name": "ask", "values": {"in": ["sum", "diff", "prod"]}}],
        table={"key": "ask", "rows": {"sum": {"ASK": "a + b", "w1": 1, "w2": 1, "wp": 0}, "diff": {"ASK": "a − b", "w1": 1, "w2": -1, "wp": 0}, "prod": {"ASK": "ab", "w1": 0, "w2": 0, "wp": 1}}},
        derive={"v1": "a*p + b", "v2": "a*q + b", "dv": "a*q + b - (a*p + b)", "dq": "q - p", "ap": "a*p", "ans": "w1*a + w2*b + wp*a*b"},
        constraints=["p < q", "v1 != 0", "v2 != 0", "ans != 0", "ans not in (p, q, v1, v2)", "a != b"],
        cost_values=["p", "q", "v1", "v2", "dv", "dq", "a", "b", "ans"],
        answer_var="ans",
        verify=["a*p + b == v1", "a*q + b == v2", "dq*a == dv", "ans == w1*a + w2*b + wp*a*b"],
        question="함수 f(x) = ax + b에 대하여 f({p}) = {v1}, f({q}) = {v2}일 때, 상수 a, b에 대하여 {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="f({p}) = {v1}은 x = {p}를 대입하면 {v1}이 된다는 뜻이므로 {co(p)}a + b = {v1}, 마찬가지로 f({q}) = {v2}에서 {co(q)}a + b = {v2}이다. 두 식을 빼면 b가 없어져 a를 구할 수 있고, 다시 대입해 b를 구한다.",
        sol2=[
            "f({p}) = {v1}에서 {co(p)}a + b = {v1} … ①, f({q}) = {v2}에서 {co(q)}a + b = {v2} … ②",
            "② − ①: {dq}a = {dv}, a = {a}",
            "①에 a = {a}{eul(a)} 대입하면 {ap} + b = {v1}, b = {b}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(p)}a + b = {v1}", "hint": "f({p}) = {v1}"},
            {"text": "{co(q)}a + b = {v2}", "hint": "f({q}) = {v2}"},
            {"text": "{dq}a = {dv}  →  a = {a}", "hint": "② − ① — b 소거"},
            {"text": "{ap} + b = {v1}  →  b = {b}", "hint": "①에 대입", "marks": [{"on": "b = {b}", "note": "a 먼저, b 나중"}]},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3", "mark:3-0")], [reveal(4)]],
        sol3="f(x) = {co(a)}x {sgn(b)}이면 f({p}) = {a} × {pn(p)} {sgn(b)} = {v1}, f({q}) = {a} × {pn(q)} {sgn(b)} = {v2}{ro(v2)} 두 조건에 모두 맞다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["f(x) = {co(a)}x {sgn(b)}: f({p}) = {v1} ✓, f({q}) = {v2} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="f({p}) = {v1}, f({q}) = {v2}에서 {co(p)}a + b = {v1}, {co(q)}a + b = {v2}이다. 두 식을 빼면 {dq}a = {dv}, a = {a}이고 b = {b}이므로 {ASK} = {ans}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "두 조건을 {co(p)}a + b = {v1}, {co(q)}a + b = {v2}{ro(v2)} 세웠다.", "partial": "한 식만 세웠으면 1점."},
            {"element": "a, b 구하기", "points": 2, "criterion": "연립하여 a = {a}, b = {b}{eul(b)} 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


def fv_t4():
    return tpl(FV, 4, FV_BASE,
        title="f(x) = ax + b에서 f(p)가 주어질 때 상수 b와 f(q)",
        skill="f(p) = v를 대입해 b를 구하고, 완성된 식에 q를 대입해 f(q)를 구하기",
        variant_axis={"a": "±1~±4", "대입값": "±1~±6"},
        discriminates="b를 구한 뒤 f(q)를 새 식에 대입해 구하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ4}}, {"name": "b", "values": {"in": NZ8}}, {"name": "p", "values": {"in": NZ6}}, {"name": "q", "values": {"in": NZ6}}],
        derive={"v": "a*p + b", "ap": "a*p", "ans": "a*q + b"},
        constraints=["p != q", "v != 0", "ans != 0", "ans not in (a, p, q, v)", "ans != b"],
        cost_values=["a", "p", "v", "b", "q", "ans"],
        answer_var="ans",
        verify=["a*p + b == v", "ans == a*q + b"],
        question="함수 f(x) = {co(a)}x + b에 대하여 f({p}) = {v}일 때, f({q})의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="f({p}) = {v}는 x = {p}를 대입하면 {v}가 된다는 뜻이므로 {a} × {pn(p)} + b = {v}에서 b를 구할 수 있다. 그러면 함수의 식이 완전히 정해지고, 거기에 x = {q}를 대입하면 f({q})가 나온다.",
        sol2=[
            "f({p}) = {v}에서 {a} × {pn(p)} + b = {v}, {ap} + b = {v}, b = {b}",
            "따라서 f(x) = {co(a)}x {sgn(b)}",
            "f({q}) = {a} × {pn(q)} {sgn(b)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{ap} + b = {v}  →  b = {b}", "hint": "f({p}) = {v} 대입"},
            {"text": "f(x) = {co(a)}x {sgn(b)}", "hint": "식 완성"},
            {"text": "f({q}) = {a} × {pn(q)} {sgn(b)} = {ans}", "marks": [{"on": "{ans}", "note": "x = {q} 대입"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="f(x) = {co(a)}x {sgn(b)}에 x = {p}를 넣으면 {ap} {sgn(b)} = {v}{ro(v)} 조건과 같고, x = {q}를 넣으면 {ans}이다. 따라서 f({q}) = {ans}이다.",
        sol3_fig=steps(["f({p}) = {ap} {sgn(b)} = {v} ✓", "f({q}) = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="f({p}) = {v}에서 {ap} + b = {v}, b = {b}이므로 f(x) = {co(a)}x {sgn(b)}이다. 따라서 f({q}) = {a} × {pn(q)} {sgn(b)} = {ans}이다.",
        rubric=[
            {"element": "b 구하기", "points": 3, "criterion": "f({p}) = {v}를 대입해 b = {b}{eul(b)} 구했다.", "partial": "대입은 맞고 계산 실수면 1점."},
            {"element": "f({q}) 구하기", "points": 2, "criterion": "f(x) = {co(a)}x {sgn(b)}에 x = {q}를 대입해 {ans}{eul(ans)} 구했다.", "partial": "b 없이 대입했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


FV_SEED = {
    "seed_id": FV, "category": "연산",
    "title": "함수와 함숫값 — f(p) ± f(q)·a/x + c의 상수·두 조건으로 a, b·f(p)로 b와 f(q)",
    "unit_id": "m2-1", "concept_ids": ["m2-1-16"],
    "schema_id": None, "schema_name": "함숫값과 함수의 식 결정",
    "source_item_ids": [],
    "note": "함숫값은 대입이 전부 — 계수·대입값을 파라미터로 두고 조건값(v)을 역산한다.",
    "geometry": False,
    "templates": [fv_t1(), fv_t2(), fv_t3(), fv_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 일차함수와 그래프의 성질
LP = "m2-1-line-props"
LP_BASE = {**BASE, "prereq": ["일차함수의 뜻", "좌표평면"], "ops": ["일차함수"], "traps": ["평행이동 방향", "절편 혼동"], "tags": ["일차함수", "그래프"]}


def lp_t1():
    return tpl(LP, 1, LP_BASE,
        title="y = ax의 그래프를 y축 방향으로 k만큼 평행이동한 그래프가 지나는 점 (p, m) — m",
        skill="y축 방향으로 k만큼 평행이동하면 y = ax + k가 됨을 알고 점의 x좌표를 대입하기",
        variant_axis={"기울기": "±1~±4", "평행이동": "±1~±6"},
        discriminates="평행이동을 상수항 k의 덧셈으로 나타내는가(기울기를 바꾸지 않는가)",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ4}}, {"name": "k", "values": {"in": NZ6}}, {"name": "p", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}],
        derive={"ap": "a*p", "m": "a*p + k", "ans": "a*p + k", **FRAME6, **line_clip("l", "a", "k")},
        constraints=["ans != 0", "ans not in (a, k, p)", "abs(m) <= 6"],
        cost_values=["a", "k", "p", "ap", "ans"],
        answer_var="ans",
        verify=["ans == a*p + k"],
        question="일차함수 y = {co(a)}x의 그래프를 y축의 방향으로 {k}만큼 평행이동한 그래프가 점 ({p}, m)을 지날 때, m의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="일차함수 y = ax의 그래프를 y축의 방향으로 k만큼 평행이동하면 y = ax + k의 그래프가 된다(기울기는 그대로, y절편만 k만큼 옮겨진다). 평행이동한 그래프의 식에 점의 x좌표 {p}를 대입하면 m이 나온다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "P", "coord": ["{p}", "{m}"]}], [seg("l", label="y = {co(a)}x {sgn(k)}")]),
        sol2=[
            "평행이동한 그래프의 식은 y = {co(a)}x {sgn(k)}",
            "점 ({p}, m)을 지나므로 x = {p}, y = m을 대입하면 m = {a} × {pn(p)} {sgn(k)} = {ap} {sgn(k)}",
            "따라서 m = {ans}",
        ],
        sol2_fig=steps([
            {"text": "y = {co(a)}x  →  y = {co(a)}x {sgn(k)}", "hint": "y축 방향으로 {k}만큼: 상수항 + {pn(k)}"},
            {"text": "m = {a} × {pn(p)} {sgn(k)} = {ans}", "hint": "x = {p} 대입", "marks": [{"on": "{ans}", "note": "기울기는 그대로"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="y = {co(a)}x {sgn(k)}에 x = {p}를 넣으면 y = {ans}이므로 점 ({p}, {ans})는 이 그래프 위에 있다. 평행이동 전 y = {co(a)}x에서는 x = {p}일 때 y = {ap}이고, 여기에 {k}{eul(k)} 더한 값과 같다. 따라서 m = {ans}이다.",
        sol3_fig=steps(["평행이동 전: ({p}, {ap}) → 후: ({p}, {ap} {sgn(k)}) = ({p}, {ans})", "m = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = {co(a)}x의 그래프를 y축의 방향으로 {k}만큼 평행이동한 그래프의 식은 y = {co(a)}x {sgn(k)}이다. x = {p}를 대입하면 m = {a} × {pn(p)} {sgn(k)} = {ans}이다.",
        rubric=[
            {"element": "평행이동한 식", "points": 3, "criterion": "y = {co(a)}x {sgn(k)}{eul(k)} 썼다.", "partial": "기울기에 {k}{eul(k)} 더했으면 인정하지 않는다."},
            {"element": "대입·답", "points": 2, "criterion": "x = {p}를 대입해 m = {ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def lp_t2():
    return tpl(LP, 2, LP_BASE,
        title="y = ax의 그래프를 y축 방향으로 k만큼 평행이동한 그래프가 점 (p, q)를 지날 때 k",
        skill="평행이동한 식 y = ax + k에 점의 좌표를 대입해 k에 대한 방정식으로 풀기",
        variant_axis={"기울기": "±1~±4", "점": "±1~±4"},
        discriminates="평행이동한 식을 y = ax + k로 놓고 점을 대입해 k를 구하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ4}}, {"name": "k", "values": {"in": NZ6}}, {"name": "p", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}],
        derive={"ap": "a*p", "q": "a*p + k", "ans": "k", **FRAME6, **line_clip("l", "a", "k")},
        constraints=["q != 0", "ans not in (a, p, q)", "abs(q) <= 6"],
        cost_values=["a", "p", "q", "ap", "ans"],
        answer_var="ans",
        verify=["a*p + ans == q"],
        question="일차함수 y = {co(a)}x의 그래프를 y축의 방향으로 k만큼 평행이동한 그래프가 점 ({p}, {q})를 지날 때, k의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="y축의 방향으로 k만큼 평행이동한 그래프의 식은 y = {co(a)}x + k이다. 이 그래프가 점 ({p}, {q})를 지나므로 x = {p}, y = {q}를 대입하면 k에 대한 일차방정식이 되어 k를 구할 수 있다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "P", "coord": ["{p}", "{q}"]}], [seg("l", label="y = {co(a)}x {sgn(k)}")]),
        sol2=[
            "평행이동한 그래프의 식은 y = {co(a)}x + k",
            "x = {p}, y = {q}를 대입하면 {q} = {a} × {pn(p)} + k, 즉 {q} = {ap} + k",
            "따라서 k = {q} − {pn(ap)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "y = {co(a)}x + k", "hint": "y축 방향으로 k만큼 평행이동"},
            {"text": "{q} = {ap} + k", "hint": "({p}, {q}) 대입"},
            {"text": "k = {ans}", "marks": [{"on": "{ans}", "note": "{q} − {pn(ap)}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="k = {ans}이면 평행이동한 식은 y = {co(a)}x {sgn(k)}이고, x = {p}를 넣으면 {ap} {sgn(k)} = {q}{ro(q)} 점 ({p}, {q})를 지난다. 따라서 k = {ans}이다.",
        sol3_fig=steps(["y = {co(a)}x {sgn(k)}: x = {p} → y = {q} ✓", "k = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="평행이동한 그래프의 식 y = {co(a)}x + k에 x = {p}, y = {q}를 대입하면 {q} = {ap} + k이므로 k = {ans}이다.",
        rubric=[
            {"element": "평행이동한 식", "points": 2, "criterion": "y = {co(a)}x + k로 놓았다.", "partial": "기울기를 바꾸었으면 인정하지 않는다."},
            {"element": "대입·답", "points": 3, "criterion": "점을 대입해 {q} = {ap} + k에서 k = {ans}{eul(ans)} 구했다.", "partial": "x, y를 바꾸어 대입했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def lp_t3():
    return tpl(LP, 3, LP_BASE,
        title="일차함수 y = ax + b의 x절편 p, y절편 q — p + q (pq)",
        skill="x절편은 y = 0일 때의 x, y절편은 x = 0일 때의 y임을 이용해 구하기",
        variant_axis={"기울기": "±1~±4", "y절편": "±1~±8", "구하는 것": "p + q / pq"},
        discriminates="x절편과 y절편을 혼동하지 않는가, x절편이 분수일 때도 그대로 두는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ4}}, {"name": "b", "values": {"in": NZ8}}, {"name": "ask", "values": {"in": ["sum", "prod"]}}],
        table={"key": "ask", "rows": {"sum": {"ASK": "p + q", "w": 1, "wp": 0}, "prod": {"ASK": "pq", "w": 0, "wp": 1}}},
        derive={"p": "-b/a", "q": "b", "ans": "w*(p + q) + wp*p*q", "xlo": "min(-3, floor(p) - 2)", "xhi": "max(3, ceiling(p) + 2)", "ylo": "min(-3, floor(q) - 2)", "yhi": "max(3, ceiling(q) + 2)", **line_clip("l", "a", "b")},
        constraints=["ans != 0", "ans not in (a, abs(b))", "abs(p) <= 8"],
        cost_values=["a", "b", "p", "q", "ans"],
        answer_var="ans",
        verify=["a*p + b == 0", "q == b", "ans == w*(p + q) + wp*p*q"],
        question="일차함수 y = {co(a)}x {sgn(b)}의 그래프의 x절편을 p, y절편을 q라 할 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="그래프가 x축과 만나는 점의 x좌표가 x절편, y축과 만나는 점의 y좌표가 y절편이다. x축 위의 점은 y = 0이므로 0 = {co(a)}x {sgn(b)}{eul(b)} 풀면 x절편이고, y축 위의 점은 x = 0이므로 y절편은 상수항 {b}이다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "A", "coord": ["{p}", 0]}, {"name": "B", "coord": [0, "{q}"]}], [seg("l")]),
        sol2=[
            "y = 0을 대입하면 0 = {co(a)}x {sgn(b)}, {co(a)}x = {-b}, x = {p}이므로 x절편 p = {p}",
            "x = 0을 대입하면 y = {b}이므로 y절편 q = {q}",
            "따라서 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "0 = {co(a)}x {sgn(b)}  →  p = {p}", "hint": "x절편: y = 0"},
            {"text": "y = {co(a)} × 0 {sgn(b)}  →  q = {q}", "hint": "y절편: x = 0"},
            {"text": "{ASK} = {ans}", "marks": [{"on": "{ans}", "note": "p, q 자리 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="점 ({p}, 0)과 (0, {q})를 식에 넣으면 {a} × {pn(p)} {sgn(b)} = 0, {a} × 0 {sgn(b)} = {q}{ro(q)} 둘 다 그래프 위의 점이다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["({p}, 0): {a} × {pn(p)} {sgn(b)} = 0 ✓", "(0, {q}): y = {q} ✓ → {ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = 0일 때 {co(a)}x {sgn(b)} = 0에서 x = {p}이므로 p = {p}, x = 0일 때 y = {b}이므로 q = {q}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[
            {"element": "x절편", "points": 3, "criterion": "y = 0을 대입해 p = {p}{eul(p)} 구했다.", "partial": "x = 0을 대입했으면 인정하지 않는다."},
            {"element": "y절편·답", "points": 2, "criterion": "q = {q}{eul(q)} 구해 {ASK} = {ans}{eul(ans)} 답했다.", "partial": "p, q를 바꾸어 썼으면 1점."},
        ],
        rubric_total=5,
    )


def lp_t3_final():
    t = lp_t3()
    t["sol2"][0] = "y = 0을 대입하면 0 = {co(a)}x {sgn(b)}, {co(a)}x = {nb}, x = {p}이므로 x절편 p = {p}"
    t["derive"]["nb"] = "-b"
    return t


def lp_t4():
    return tpl(LP, 4, LP_BASE,
        title="두 일차함수의 그래프가 평행할 조건 — 기울기가 같다",
        skill="두 그래프가 평행하면 기울기가 같고 y절편이 다름을 이용해 k를 구하기",
        variant_axis={"기울기": "±1~±5", "k의 계수": "±1~±3"},
        discriminates="평행 조건을 '기울기가 같다'로 쓰는가(y절편이 같다고 하지 않는가)",
        difficulty=2,
        params=[{"name": "b", "values": {"in": NZ6}}, {"name": "c", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "d", "values": {"in": NZ6}}, {"name": "k", "values": {"in": NZ6}}, {"name": "e", "values": {"in": NZ6}}],
        derive={"ck": "c*k", "a": "c*k + d", "ans": "k"},
        constraints=["a != 0", "abs(a) <= 6", "b != e", "ans not in (a, abs(b), c, abs(d), abs(e))"],
        cost_values=["a", "c", "d", "ck", "ans"],
        answer_var="ans",
        verify=["c*ans + d == a"],
        question="두 일차함수 y = {co(a)}x {sgn(b)}{wa(b)} y = ({co(c)}k {sgn(d)})x {sgn(e)}의 그래프가 서로 평행할 때, 상수 k의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 일차함수의 그래프가 서로 평행하려면 기울기가 같고 y절편은 달라야 한다. 두 식의 y절편 {b}{wa(b)} {e}{eun(e)} 이미 다르므로, 기울기 {a}{wa(a)} {co(c)}k {sgn(d)}{ika(d)} 같다는 방정식을 풀면 된다.",
        sol2=[
            "평행하려면 기울기가 같아야 하므로 {co(c)}k {sgn(d)} = {a}",
            "{co(c)}k = {a} − {pn(d)} = {ck}",
            "따라서 k = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(c)}k {sgn(d)} = {a}", "hint": "평행 ⟺ 기울기가 같다"},
            {"text": "{co(c)}k = {ck}  →  k = {ans}", "marks": [{"on": "{ans}", "note": "y절편 {b} ≠ {e} 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="k = {ans}이면 둘째 함수는 y = {co(a)}x {sgn(e)}{ika(e)} 되어 기울기가 {a}{ro(a)} 첫째 함수와 같고 y절편은 {e}{ro(e)} {b}{wa(b)} 다르므로 두 그래프는 평행하다. 따라서 k = {ans}이다.",
        sol3_fig=steps(["k = {ans}: y = {co(a)}x {sgn(e)} — 기울기 {a} 같음, y절편 {e} ≠ {b}", "k = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="두 그래프가 평행하려면 기울기가 같아야 하므로 {co(c)}k {sgn(d)} = {a}, {co(c)}k = {ck}에서 k = {ans}이다.",
        rubric=[
            {"element": "평행 조건", "points": 3, "criterion": "기울기가 같다는 식 {co(c)}k {sgn(d)} = {a}{eul(a)} 세웠다.", "partial": "y절편이 같다는 식을 세웠으면 인정하지 않는다."},
            {"element": "k 구하기", "points": 2, "criterion": "k = {ans}{eul(ans)} 구했다.", "partial": "이항 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def lp_t5():
    return tpl(LP, 5, LP_BASE,
        title="일차함수의 그래프와 x축, y축으로 둘러싸인 삼각형의 넓이",
        skill="x절편과 y절편을 구해 두 절편의 절댓값으로 직각삼각형의 넓이를 구하기",
        variant_axis={"기울기": "±1/1~±4", "y절편": "±2~±8"},
        discriminates="절편에 음수가 있어도 길이는 절댓값으로 잡는가, 1/2을 곱하는가",
        difficulty=3, context="기하맥락",
        params=[{"name": "a", "values": {"in": NZ6}}, {"name": "b", "values": {"in": [v for v in range(-16, 17) if v]}}],
        derive={"p": "-b/a", "q": "b", "ap": "abs(p)", "ab": "abs(b)", "ans": "abs(p)*abs(b)/2", "xlo": "min(-3, floor(p) - 2)", "xhi": "max(3, ceiling(p) + 2)", "ylo": "min(-3, floor(q) - 2)", "yhi": "max(3, ceiling(q) + 2)", **line_clip("l", "a", "b")},
        constraints=["abs(p) <= 8", "ap >= 2", "ans not in (a, abs(b))", "ans != ap"],
        cost_values=["a", "b", "p", "ap", "ab", "ans"],
        answer_var="ans",
        verify=["a*p + b == 0", "2*ans == ap*ab"],
        question="일차함수 y = {co(a)}x {sgn(b)}의 그래프와 x축, y축으로 둘러싸인 삼각형의 넓이를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="그래프가 x축, y축과 만나는 점이 삼각형의 두 꼭짓점이고 원점이 나머지 꼭짓점이다. 이 삼각형은 원점에서 직각인 직각삼각형이므로, 밑변과 높이는 x절편과 y절편의 절댓값이다. 절편이 음수여도 길이는 절댓값으로 잡는다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "A", "coord": ["{p}", 0]}, {"name": "B", "coord": [0, "{b}"]}], [seg("l")]),
        sol2=[
            "x절편: y = 0에서 {co(a)}x {sgn(b)} = 0, x = {p}이므로 A({p}, 0). y절편: x = 0에서 y = {b}이므로 B(0, {b})",
            "삼각형 OAB는 ∠O = 90°인 직각삼각형이고 OA = {ap}, OB = {ab}",
            "넓이 = [[frac(1,2)]] × {ap} × {ab} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "A({p}, 0),  B(0, {b})", "hint": "x절편·y절편"},
            {"text": "OA = {ap},  OB = {ab}", "hint": "길이는 절댓값"},
            {"text": "[[frac(1,2)]] × {ap} × {ab} = {ans}", "marks": [{"on": "{ans}", "note": "직각삼각형 넓이"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="두 절편 {p}, {b}의 절댓값 {ap}, {ab}{ika(ab)} 밑변과 높이이므로 넓이는 {ap} × {ab} ÷ 2 = {ans}이다. 절댓값을 빼먹어 음수가 나오지 않았는지 확인한다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{ap} × {ab} ÷ 2 = {ans}", "넓이 = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x절편은 {p}, y절편은 {b}이므로 삼각형의 밑변과 높이는 각각 {ap}, {ab}이다. 따라서 넓이는 [[frac(1,2)]] × {ap} × {ab} = {ans}이다.",
        rubric=[
            {"element": "절편 구하기", "points": 3, "criterion": "x절편 {p}, y절편 {b}{eul(b)} 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "넓이 구하기", "points": 2, "criterion": "[[frac(1,2)]] × {ap} × {ab} = {ans}{eul(ans)} 구했다.", "partial": "절댓값을 쓰지 않아 부호가 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


def lp_t6():
    return tpl(LP, 6, LP_BASE,
        title="x절편과 y절편이 주어진 일차함수의 그래프의 기울기",
        skill="두 절편으로 두 점 (p, 0), (0, q)를 잡아 기울기 = (y의 증가량)/(x의 증가량)으로 구하기",
        variant_axis={"절편": "±1~±8"},
        discriminates="절편을 점의 좌표로 옮기고 기울기의 부호(오른쪽 위/아래)를 바르게 정하는가",
        difficulty=2,
        params=[{"name": "p", "values": {"in": NZ8}}, {"name": "q", "values": {"in": NZ8}}],
        derive={"ans": "-q/p", "np": "-p", "xlo": "min(-3, floor(p) - 2)", "xhi": "max(3, ceiling(p) + 2)", "ylo": "min(-3, floor(q) - 2)", "yhi": "max(3, ceiling(q) + 2)", **line_clip("l", "-q/p", "q")},
        constraints=["ans not in (p, q)", "abs(p) != abs(q)"],
        cost_values=["p", "q", "ans"],
        answer_var="ans",
        verify=["ans*p + q == 0"],
        question="x절편이 {p}, y절편이 {q}인 일차함수의 그래프의 기울기를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x절편이 {p}이면 그래프는 점 ({p}, 0)을, y절편이 {q}이면 점 (0, {q})를 지난다. 두 점을 알면 기울기는 (y의 증가량) ÷ (x의 증가량)이다. ({p}, 0)에서 (0, {q})로 갈 때 x는 {np}만큼, y는 {q}만큼 변한다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "A", "coord": ["{p}", 0]}, {"name": "B", "coord": [0, "{q}"]}], [seg("l")]),
        sol2=[
            "그래프는 두 점 ({p}, 0), (0, {q})를 지난다",
            "기울기 = [[frac({q} − 0, 0 − {pn(p)})]] = [[frac({q}, {np})]] = {ans}",
        ],
        sol2_fig=steps([
            {"text": "({p}, 0),  (0, {q})", "hint": "절편 → 점"},
            {"text": "기울기 = [[frac({q}, {np})]] = {ans}", "hint": "y의 증가량 ÷ x의 증가량", "marks": [{"on": "{ans}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="기울기가 {ans}이고 y절편이 {q}인 식 y = {co(ans)}x {sgn(q)}에 x = {p}를 넣으면 y = 0이 되어 x절편 {p}{wa(p)} 맞다. 따라서 기울기는 {ans}이다.",
        sol3_fig=steps(["y = {co(ans)}x {sgn(q)}: x = {p} → y = 0 ✓", "기울기 = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="그래프가 두 점 ({p}, 0), (0, {q})를 지나므로 기울기는 [[frac({q} − 0, 0 − {pn(p)})]] = {ans}이다.",
        rubric=[
            {"element": "두 점 잡기", "points": 2, "criterion": "절편으로 두 점 ({p}, 0), (0, {q})를 잡았다.", "partial": "절편을 좌표로 옮기지 못했으면 인정하지 않는다."},
            {"element": "기울기 구하기", "points": 3, "criterion": "[[frac({q}, {np})]] = {ans}{eul(ans)} 구했다.", "partial": "부호가 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


LP_SEED = {
    "seed_id": LP, "category": "연산",
    "title": "일차함수 그래프의 성질 — 평행이동한 그래프의 점·평행이동량·절편의 합·평행 조건·절편 삼각형 넓이·절편으로 기울기",
    "unit_id": "m2-1", "concept_ids": ["m2-1-17", "m2-1-18"],
    "schema_id": None, "schema_name": "일차함수의 그래프(평행이동·절편·기울기·평행)",
    "source_item_ids": [],
    "note": "그래프는 coordplane 선분(line_clip)으로, 찍는 점은 절편·지나는 점만(recheck F4). 분수 절편·기울기는 그대로 둔다.",
    "geometry": False,
    "templates": [lp_t1(), lp_t2(), lp_t3_final(), lp_t4(), lp_t5(), lp_t6()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 일차함수의 활용
LA = "m2-1-line-apply"
LA_BASE = {**COMMON_APPLY, "ops": ["일차함수", "사칙"], "prereq": ["일차함수의 식"], "traps": ["변화율 부호", "단위"], "tags": ["일차함수의 활용"], "qtype": "short", "pool_target": 300}
TANK_ROWS = {"key": "w", "rows": {
    "in": {"ACT": "넣는다", "SG": 1, "DIR": "늘어", "OPW": "+", "WHY": "매분 넣는 양만큼 늘어난다"},
    "out": {"ACT": "뺀다", "SG": -1, "DIR": "줄어", "OPW": "−", "WHY": "매분 빼는 양만큼 줄어든다"},
}}


def la_t1():
    return tpl(LA, 1, LA_BASE,
        title="물통에 물을 넣거나 빼는 상황 — 물의 양이 T L가 되는 시각",
        skill="처음 양과 매분 변화량으로 y = (처음 양) ± (변화량)x의 식을 세우고 y = T를 풀기",
        variant_axis={"처음 양": "20~300 L", "변화량": "2~15 L/분", "넣기 / 빼기": "부호"},
        discriminates="변화량의 부호(넣기 +, 빼기 −)를 식에 반영하고, y = T의 방정식으로 x를 구하는가",
        difficulty=2,
        params=[{"name": "w", "values": {"in": ["in", "out"]}}, {"name": "V0", "values": {"in": [20, 30, 40, 50, 60, 80, 100, 120, 150, 200, 240, 300]}}, {"name": "r", "values": {"in": [2, 3, 4, 5, 6, 8, 10, 12, 15]}}, {"name": "x", "values": {"int": [3, 20]}}],
        table=TANK_ROWS,
        derive={"T": "V0 + SG*r*x", "ans": "x", "diff": "SG*(T - V0)"},
        constraints=["T > 0", "T != V0", "ans not in (V0, r, T)"],
        cost_values=["V0", "r", "T", "diff", "ans"],
        answer_var="ans",
        verify=["V0 + SG*r*ans == T", "diff == r*ans"],
        question="{V0} L의 물이 들어 있는 물통에 매분 {r} L씩 물을 {ACT}. 물을 {ACT.rstrip('다')}기 시작한 지 x분 후 물통에 들어 있는 물의 양을 y L라 할 때, 물의 양이 {T} L가 되는 것은 몇 분 후인지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="물의 양은 처음 {V0} L에서 매분 {r} L씩 {DIR}드니 x분 후에는 {V0} {OPW} {r}x (L)이다. 즉 y = {V0} {OPW} {r}x이고, 이것은 x의 일차함수다. y = {T}를 대입해 x에 대한 일차방정식을 풀면 몇 분 후인지 알 수 있다.",
        sol2=[
            "x분 후 물의 양: y = {V0} {OPW} {r}x",
            "y = {T}이면 {V0} {OPW} {r}x = {T}, {r}x = {diff}",
            "x = {ans}이므로 {ans}분 후",
        ],
        sol2_fig=steps([
            {"text": "y = {V0} {OPW} {r}x", "hint": "{WHY}"},
            {"text": "{V0} {OPW} {r}x = {T}  →  {r}x = {diff}", "hint": "y = {T} 대입"},
            {"text": "x = {ans}", "marks": [{"on": "{ans}", "note": "{diff} ÷ {r}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{ans}분 동안 물이 {r} × {ans} = {r*ans} L {DIR}드니 {V0} {OPW} {r*ans} = {T} L가 맞다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{r} × {ans} = {r*ans} L 변화", "{V0} {OPW} {r*ans} = {T} L ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x분 후 물의 양은 y = {V0} {OPW} {r}x이다. y = {T}를 대입하면 {V0} {OPW} {r}x = {T}에서 x = {ans}이므로 {ans}분 후이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "y = {V0} {OPW} {r}x{eul(r)} 세웠다.", "partial": "변화량의 부호가 틀렸으면 인정하지 않는다."},
            {"element": "방정식 풀기", "points": 3, "criterion": "y = {T}를 대입해 x = {ans}{eul(ans)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}분 후라고 답했다."},
        ],
        rubric_total=8,
    )


def la_t1_final():
    t = la_t1()
    t["question"] = "{V0} L의 물이 들어 있는 물통에 매분 {r} L씩 물을 {ACT}. 물의 양이 변하기 시작한 지 x분 후 물통에 들어 있는 물의 양을 y L라 할 때, 물의 양이 {T} L가 되는 것은 몇 분 후인지 구하시오."
    return t


def la_t2():
    return tpl(LA, 2, LA_BASE,
        title="타는 양초의 길이 — 남은 길이가 R cm가 되는 시각",
        skill="t분마다 d cm씩 짧아지는 것을 1분당 변화량으로 바꾸어 y = L₀ − (d/t)x의 식을 세우기",
        variant_axis={"처음 길이": "15~30 cm", "변화": "t분마다 d cm"},
        discriminates="'t분마다 d cm'를 1분당 d/t cm의 기울기로 바꾸는가",
        difficulty=3,
        params=[{"name": "L0", "values": {"in": [15, 18, 20, 24, 25, 30]}}, {"name": "t", "values": {"in": [2, 3, 4, 5, 6, 10]}}, {"name": "d", "values": {"in": [1, 2, 3, 4]}}, {"name": "x", "values": {"in": [6, 8, 10, 12, 15, 16, 18, 20, 24, 25, 30, 36, 40]}}],
        derive={"k": "d/t", "R": "L0 - d*x/t", "burn": "L0 - R", "ans": "x"},
        constraints=["R == floor(R)", "R >= 1", "R < L0", "ans not in (L0, t, d, R)", "d != t", "ans % t == 0"],
        cost_values=["L0", "t", "d", "k", "R", "burn", "ans"],
        answer_var="ans",
        verify=["L0 - k*ans == R", "k*t == d"],
        question="길이가 {L0} cm인 양초에 불을 붙이면 {t}분마다 {d} cm씩 짧아진다. 불을 붙인 지 x분 후 남은 양초의 길이를 y cm라 할 때, 남은 길이가 {R} cm가 되는 것은 불을 붙인 지 몇 분 후인지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{t}분마다 {d} cm씩 짧아지므로 1분에 {k} cm씩 짧아진다(변화율 = {d} ÷ {t}). 따라서 x분 후 남은 길이는 y = {L0} − {k}x이다. y = {R}를 대입해 x를 구한다.",
        sol2=[
            "1분당 짧아지는 길이는 [[frac({d}, {t})]] = {k} (cm)이므로 y = {L0} − {k}x",
            "y = {R}이면 {L0} − {k}x = {R}, {k}x = {burn}",
            "x = {burn} ÷ {k} = {ans}이므로 {ans}분 후",
        ],
        sol2_fig=steps([
            {"text": "y = {L0} − {k}x", "hint": "1분당 [[frac({d}, {t})]] cm"},
            {"text": "{L0} − {k}x = {R}  →  {k}x = {burn}", "hint": "y = {R} 대입"},
            {"text": "x = {ans}", "marks": [{"on": "{ans}", "note": "{burn} ÷ {k}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{ans}분은 {t}분의 {ans/t}배이므로 짧아진 길이는 {d} × {ans/t} = {burn} cm이고, {L0} − {burn} = {R} cm가 맞다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{ans}분 = {t}분 × {ans/t} → {d} × {ans/t} = {burn} cm 짧아짐", "{L0} − {burn} = {R} cm ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="1분에 {k} cm씩 짧아지므로 y = {L0} − {k}x이다. y = {R}를 대입하면 {L0} − {k}x = {R}에서 x = {ans}이므로 {ans}분 후이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "1분당 변화량 {k}{eul(k)} 구해 y = {L0} − {k}x를 세웠다.", "partial": "{t}분마다를 1분당으로 바꾸지 않았으면 인정하지 않는다."},
            {"element": "방정식 풀기", "points": 3, "criterion": "y = {R}를 대입해 x = {ans}{eul(ans)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}분 후라고 답했다."},
        ],
        rubric_total=8,
    )


def la_t3():
    return tpl(LA, 3, LA_BASE,
        title="높이에 따라 내려가는 기온 — 높이 h km에서의 기온",
        skill="지면의 기온과 1 km당 내려가는 온도로 y = T₀ − dx의 식을 세워 대입하기",
        variant_axis={"지면 기온": "10~30 ℃", "변화율": "1 km당 5~8 ℃"},
        discriminates="내려가는 변화를 음의 기울기로 식에 넣고 대입하는가",
        difficulty=2,
        params=[{"name": "T0", "values": {"in": [10, 12, 14, 15, 16, 18, 20, 22, 24, 25, 28, 30]}}, {"name": "d", "values": {"in": [5, 6, 7, 8]}}, {"name": "h", "values": {"in": [2, 3, 4, 5]}}],
        derive={"dh": "d*h", "ans": "T0 - d*h"},
        constraints=["ans != 0", "ans not in (T0, d, h)"],
        cost_values=["T0", "d", "h", "dh", "ans"],
        answer_var="ans",
        verify=["ans == T0 - dh", "dh == d*h"],
        question="지면의 기온이 {T0} ℃이고, 높이가 1 km 높아질 때마다 기온은 {d} ℃씩 내려간다고 한다. 지면에서 높이가 x km인 곳의 기온을 y ℃라 할 때, 높이가 {h} km인 곳의 기온은 몇 ℃인지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="높이가 1 km 높아질 때마다 {d} ℃씩 내려가므로 x km 높아지면 {d}x ℃만큼 내려간다. 따라서 높이 x km인 곳의 기온은 y = {T0} − {d}x (℃)이고, x = {h}를 대입하면 된다. 내려가는 변화이므로 기울기가 음수다.",
        sol2=[
            "높이 x km에서의 기온: y = {T0} − {d}x",
            "x = {h}를 대입하면 y = {T0} − {d} × {h} = {T0} − {dh}",
            "따라서 {ans} ℃",
        ],
        sol2_fig=steps([
            {"text": "y = {T0} − {d}x", "hint": "1 km당 {d} ℃ 내려감 → 기울기 −{d}"},
            {"text": "y = {T0} − {d} × {h} = {ans}", "hint": "x = {h} 대입", "marks": [{"on": "{ans}", "note": "{T0} − {dh}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="{h} km 높아지면 {d} × {h} = {dh} ℃ 내려가므로 {T0} − {dh} = {ans} ℃가 맞다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{d} × {h} = {dh} ℃ 내려감", "{T0} − {dh} = {ans} ℃"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="높이 x km인 곳의 기온은 y = {T0} − {d}x이므로 x = {h}를 대입하면 y = {T0} − {dh} = {ans}이다. 따라서 {ans} ℃이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "y = {T0} − {d}x{eul(d)} 세웠다.", "partial": "기울기의 부호가 틀렸으면 인정하지 않는다."},
            {"element": "대입·답", "points": 2, "criterion": "x = {h}를 대입해 {ans} ℃를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def la_t4():
    return tpl(LA, 4, LA_BASE,
        title="직사각형의 변 위를 움직이는 점 P — 삼각형의 넓이가 S가 되는 시각",
        skill="x초 후 BP의 길이를 속력 × 시간으로 나타내고 삼각형 넓이를 x의 일차식으로 세우기",
        variant_axis={"변": "AB 4~12 cm, BC 10~20 cm", "속력": "매초 1~3 cm"},
        discriminates="넓이 = (1/2) × AB × BP에서 BP = (속력) × x로 두는가, 1/2을 빠뜨리지 않는가",
        difficulty=3, context="기하맥락",
        params=[{"name": "a", "values": {"in": [4, 5, 6, 8, 10, 12]}}, {"name": "b", "values": {"in": [10, 12, 15, 16, 18, 20]}}, {"name": "v", "values": {"in": [1, 2, 3]}}, {"name": "x", "values": {"int": [2, 10]}}],
        derive={"k": "a*v/2", "BP": "v*x", "S": "a*v*x/2", "ans": "x"},
        constraints=["BP < b", "S == floor(S)", "ans not in (a, b, v, S)"],
        cost_values=["a", "b", "v", "k", "BP", "S", "ans"],
        answer_var="ans",
        verify=["a*BP/2 == S", "BP == v*ans", "k*ans == S"],
        question="다음 그림과 같이 [[seg(AB)]] = {a} cm, [[seg(BC)]] = {b} cm인 직사각형 ABCD에서 점 P는 점 B를 출발하여 [[seg(BC)]]를 따라 점 C까지 매초 {v} cm의 속력으로 움직인다. 점 P가 출발한 지 x초 후 삼각형 ABP의 넓이를 y cm²라 할 때, 넓이가 {S} cm²가 되는 것은 출발한 지 몇 초 후인지 구하시오.",
        figure=[{"fn": "scene", "args": {"pts": {"A": [0, "{a}"], "B": [0, 0], "C": ["{b}", 0], "D": ["{b}", "{a}"], "P": ["{BP}", 0]},
                                          "segs": [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], {"a": "A", "b": "P", "dash": True}],
                                          "nodot": True}}],
        answer="{ans}", answer_alt=[],
        sol1="점 P는 매초 {v} cm씩 움직이므로 x초 후 [[seg(BP)]] = {co(v)}x (cm)이다. 삼각형 ABP는 ∠B = 90°인 직각삼각형이므로 넓이는 [[frac(1,2)]] × [[seg(AB)]] × [[seg(BP)]] = [[frac(1,2)]] × {a} × {co(v)}x이다. 이것을 정리한 일차함수에 y = {S}를 대입해 x를 구한다.",
        sol2=[
            "x초 후 [[seg(BP)]] = {co(v)}x (cm)",
            "y = [[frac(1,2)]] × {a} × {co(v)}x = {k}x",
            "y = {S}이면 {k}x = {S}, x = {ans}이므로 {ans}초 후",
        ],
        sol2_fig=steps([
            {"text": "[[seg(BP)]] = {co(v)}x", "hint": "속력 × 시간"},
            {"text": "y = [[frac(1,2)]] × {a} × {co(v)}x = {k}x", "hint": "직각삼각형 ABP의 넓이"},
            {"text": "{k}x = {S}  →  x = {ans}", "marks": [{"on": "{ans}", "note": "{S} ÷ {k}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{ans}초 후 [[seg(BP)]] = {v} × {ans} = {BP} cm이고 넓이는 [[frac(1,2)]] × {a} × {BP} = {S} cm²로 조건과 같다. [[seg(BP)]] = {BP} cm는 [[seg(BC)]] = {b} cm보다 짧으므로 P는 아직 변 BC 위에 있다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["[[seg(BP)]] = {v} × {ans} = {BP} cm (< {b} cm)", "[[frac(1,2)]] × {a} × {BP} = {S} cm² ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x초 후 [[seg(BP)]] = {co(v)}x이므로 삼각형 ABP의 넓이는 y = [[frac(1,2)]] × {a} × {co(v)}x = {k}x이다. y = {S}를 대입하면 {k}x = {S}에서 x = {ans}이므로 {ans}초 후이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "[[seg(BP)]] = {co(v)}x로 놓고 y = [[frac(1,2)]] × {a} × {co(v)}x = {k}x를 세웠다.", "partial": "2로 나누는 것을 빠뜨렸으면 1점."},
            {"element": "방정식 풀기", "points": 3, "criterion": "y = {S}를 대입해 x = {ans}{eul(ans)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}초 후라고 답했다."},
        ],
        rubric_total=8,
    )


def la_t5():
    return tpl(LA, 5, LA_BASE,
        title="용수철의 길이 — 두 측정값으로 식을 세워 다른 무게에서의 길이",
        skill="추의 무게가 늘 때 길이가 일정하게 늘어나므로 y = ax + b로 놓고 두 측정값으로 a, b를 구하기",
        variant_axis={"처음 길이": "10~30 cm", "10 g당 늘어나는 길이": "1~4 cm"},
        discriminates="두 측정값의 차로 기울기(무게 1 g당 늘어나는 길이)를 구하고 절편을 맞추는가",
        difficulty=3,
        params=[{"name": "L0", "values": {"in": [10, 12, 15, 18, 20, 24, 25, 30]}}, {"name": "k", "values": {"in": [1, 2, 3, 4]}}, {"name": "w1", "values": {"in": [10, 20, 30, 40]}}, {"name": "w2", "values": {"in": [30, 40, 50, 60, 80]}}, {"name": "w3", "values": {"in": [50, 60, 70, 80, 90, 100, 120]}}],
        derive={"L1": "L0 + k*w1/10", "L2": "L0 + k*w2/10", "dL": "k*(w2 - w1)/10", "dw": "w2 - w1", "a": "k/10", "ans": "L0 + k*w3/10"},
        constraints=["w1 < w2", "w3 > w2", "ans not in (L0, w1, w2, w3, L1, L2)"],
        cost_values=["w1", "L1", "w2", "L2", "dL", "dw", "a", "L0", "w3", "ans"],
        answer_var="ans",
        verify=["ans == L0 + a*w3", "a*dw == dL", "L1 == L0 + a*w1", "L2 == L0 + a*w2"],
        question="어떤 용수철에 {w1} g의 추를 매달면 길이가 {L1} cm가 되고, {w2} g의 추를 매달면 길이가 {L2} cm가 된다. 추의 무게에 따라 용수철의 길이가 일정하게 늘어날 때, {w3} g의 추를 매달면 용수철의 길이는 몇 cm가 되는지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="추의 무게 x g에 따라 길이 y cm가 일정하게 늘어나므로 y는 x의 일차함수 y = ax + b이다. 두 측정값 ({w1}, {L1}), ({w2}, {L2})로 기울기 a(1 g당 늘어나는 길이)를 구하고, 한 점을 대입해 b(추가 없을 때의 길이)를 구한 뒤 x = {w3}을 대입한다.",
        sol2=[
            "y = ax + b로 놓으면 기울기 a = [[frac({L2} − {L1}, {w2} − {w1})]] = [[frac({dL}, {dw})]] = {a}",
            "({w1}, {L1})을 대입: {L1} = {a} × {w1} + b, b = {L0}이므로 y = {a}x + {L0}",
            "x = {w3}을 대입하면 y = {a} × {w3} + {L0} = {ans}이므로 {ans} cm",
        ],
        sol2_fig=steps([
            {"text": "a = [[frac({dL}, {dw})]] = {a}", "hint": "무게 1 g당 늘어나는 길이"},
            {"text": "{L1} = {a} × {w1} + b  →  b = {L0}", "hint": "({w1}, {L1}) 대입"},
            {"text": "y = {a}x + {L0}  →  x = {w3}: y = {ans}", "marks": [{"on": "{ans}", "note": "{a} × {w3} + {L0}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="y = {a}x + {L0}에 x = {w2}를 넣으면 {a} × {w2} + {L0} = {L2}{ro(L2)} 둘째 측정값과도 맞다. x = {w3}일 때 {ans} cm이다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["x = {w2}: {a} × {w2} + {L0} = {L2} ✓", "x = {w3}: {ans} cm"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y = ax + b로 놓으면 a = [[frac({dL}, {dw})]] = {a}, b = {L0}이므로 y = {a}x + {L0}이다. x = {w3}을 대입하면 y = {ans}이므로 용수철의 길이는 {ans} cm이다.",
        rubric=[
            {"element": "기울기·식 세우기", "points": 3, "criterion": "두 측정값으로 a = {a}, b = {L0}{eul(L0)} 구해 y = {a}x + {L0}{eul(L0)} 세웠다.", "partial": "기울기만 맞으면 1점."},
            {"element": "대입·계산", "points": 3, "criterion": "x = {w3}을 대입해 {ans}{eul(ans)} 구했다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans} cm를 답했다."},
        ],
        rubric_total=8,
    )


LA_SEED = {
    "seed_id": LA, "category": "활용",
    "title": "일차함수의 활용 — 물통·양초·기온·점 P의 이동과 넓이·용수철",
    "unit_id": "m2-1", "concept_ids": ["m2-1-19", "m2-1-20"],
    "schema_id": None, "schema_name": "일차함수 세우기(문장제)",
    "source_item_ids": [],
    "note": "답(시각·값)을 파라미터로 두고 조건값을 역산. 점 P 틀은 scene 그림(직사각형 + 점 P) — geometry False 로 두어 3단 해설.",
    "geometry": False,
    "templates": [la_t1_final(), la_t2(), la_t3(), la_t4(), la_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 4. 일차함수와 일차방정식의 그래프
LI = "m2-1-line-intersect"
LI_BASE = {**BASE, "prereq": ["일차함수의 그래프", "연립방정식"], "ops": ["일차방정식의 그래프"], "traps": ["부호", "교점 = 연립 해"], "tags": ["일차방정식의 그래프", "연립방정식과 그래프"]}


def li_t1():
    return tpl(LI, 1, LI_BASE,
        title="일차방정식 ax + by + c = 0의 그래프의 기울기 p, y절편 q — p + q (pq)",
        skill="y에 대해 풀어 y = (기울기)x + (y절편) 꼴로 고치기",
        variant_axis={"계수": "a ±1~±6, b ±1~±4, c ±1~±8", "구하는 것": "p + q / pq"},
        discriminates="y에 대해 풀 때 각 항을 b로 나누며 부호를 바르게 처리하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ6}}, {"name": "b", "values": {"in": NZ4}}, {"name": "c", "values": {"in": NZ8}}, {"name": "ask", "values": {"in": ["sum", "prod"]}}],
        table=[sgn_rows(NZ4, "b", "y"), {"key": "ask", "rows": {"sum": {"ASK": "p + q", "w": 1, "wp": 0}, "prod": {"ASK": "pq", "w": 0, "wp": 1}}}],
        derive={"p": "-a/b", "q": "-c/b", "na": "-a", "nc": "-c", "ans": "w*(p + q) + wp*p*q"},
        constraints=["ans != 0", "ans not in (a, abs(b), abs(c))", "abs(b) != 1"],
        cost_values=["a", "b", "c", "p", "q", "ans"],
        answer_var="ans",
        verify=["p*b == -a", "q*b == -c", "ans == w*(p + q) + wp*p*q"],
        question="일차방정식 {co(a)}x {BS} {sgn(c)} = 0의 그래프의 기울기를 p, y절편을 q라 할 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="일차방정식 ax + by + c = 0의 그래프는 y에 대해 풀면 일차함수 y = −[[frac(a, b)]]x − [[frac(c, b)]]의 그래프와 같다. 그래서 y항만 남기고 이항한 뒤 y의 계수 {b}{ro(b)} 나누면 기울기와 y절편이 보인다. 나눌 때 각 항의 부호를 조심한다.",
        sol2=[
            "y항만 남기고 이항하면 {co(b)}y = {co(na)}x {sgn(nc)}",
            "양변을 {b}{ro(b)} 나누면 y = {co(p)}x {sgn(q)}",
            "따라서 p = {p}, q = {q}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(b)}y = {co(na)}x {sgn(nc)}", "hint": "x항·상수항 이항"},
            {"text": "y = {co(p)}x {sgn(q)}", "hint": "양변 ÷ {pn(b)}", "marks": [{"on": "{co(p)}x", "note": "기울기 p"}, {"on": "{sgn(q)}", "note": "y절편 q"}]},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0", "mark:1-1")], [reveal(2)]],
        sol3="y = {co(p)}x {sgn(q)}의 양변에 {b}{eul(b)} 곱하고 정리하면 {co(a)}x {BS} {sgn(c)} = 0으로 돌아오므로 맞다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["y = {co(p)}x {sgn(q)}  ⟺  {co(a)}x {BS} {sgn(c)} = 0 ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{co(a)}x {BS} {sgn(c)} = 0을 y에 대해 풀면 y = {co(p)}x {sgn(q)}이므로 기울기 p = {p}, y절편 q = {q}이고 {ASK} = {ans}이다.",
        rubric=[
            {"element": "y에 대해 풀기", "points": 3, "criterion": "y = {co(p)}x {sgn(q)}{ro(q)} 고쳤다.", "partial": "나눌 때 한 항의 부호만 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "p = {p}, q = {q}에서 {ASK} = {ans}{eul(ans)} 구했다.", "partial": "p, q를 바꾸어 읽었으면 1점."},
        ],
        rubric_total=5,
    )


def li_t2():
    return tpl(LI, 2, LI_BASE,
        title="두 직선의 교점의 좌표 (p, q) — p + q (pq)",
        skill="두 직선의 교점은 두 일차방정식의 연립방정식의 해임을 이용해 풀기",
        variant_axis={"계수": "±1~±4", "구하는 것": "p + q / pq"},
        discriminates="교점을 연립방정식의 해로 구하는가, 가감법의 부호를 지키는가",
        difficulty=3,
        params=[{"name": "a1", "values": {"in": [1, 2, 3]}}, {"name": "b1", "values": {"in": NZ4}}, {"name": "a2", "values": {"in": [1, 2, 3, 4]}}, {"name": "b2", "values": {"in": NZ4}},
                {"name": "x0", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "y0", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "ask", "values": {"in": ["sum", "prod"]}}],
        table=[sgn_rows(NZ4, "b1", "y"), sgn_rows(NZ4, "b2", "y"), {"key": "ask", "rows": {"sum": {"ASK": "p + q", "w": 1, "wp": 0}, "prod": {"ASK": "pq", "w": 0, "wp": 1}}}],
        derive={"c1": "a1*x0 + b1*y0", "c2": "a2*x0 + b2*y0", "det": "a1*b2 - a2*b1", "dx": "a2*b1 - a1*b2", "rx": "b1*c2 - b2*c1", "b1y": "b1*y0", "ans": "w*(x0 + y0) + wp*x0*y0",
                **FRAME6, **line_clip("l", "-a1/b1", "c1/b1"), **line_clip("m", "-a2/b2", "c2/b2")},
        constraints=["det != 0", "c1 != 0", "c2 != 0", "ans != 0", "ans not in (a1, a2, abs(b1), abs(b2), c1, c2)", "x0 != y0", "a1*b2 != a2*b1"],
        cost_values=["a1", "b1", "c1", "a2", "b2", "c2", "dx", "rx", "x0", "y0", "ans"],
        answer_var="ans",
        verify=["a1*x0 + b1*y0 == c1", "a2*x0 + b2*y0 == c2", "dx*y0 == a2*c1 - a1*c2", "ans == w*(x0 + y0) + wp*x0*y0"],
        question="두 직선 {co(a1)}x {B1S} = {c1}, {co(a2)}x {B2S} = {c2}의 교점의 좌표가 (p, q)일 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 직선의 교점은 두 방정식을 동시에 만족하는 점이므로, 교점의 좌표는 연립방정식 {co(a1)}x {B1S} = {c1}, {co(a2)}x {B2S} = {c2}의 해와 같다. 가감법으로 한 문자를 없애 x, y를 구한다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "P", "coord": ["{x0}", "{y0}"]}], [seg("l"), seg("m")]),
        sol2=[
            "교점의 좌표는 연립방정식 {co(a1)}x {B1S} = {c1} … ①, {co(a2)}x {B2S} = {c2} … ②의 해",
            "① × {a2} − ② × {a1}: {co(dx)}y = {a2*c1 - a1*c2}, y = {y0}이고 ①에서 {co(a1)}x {sgn(b1y)} = {c1}, x = {x0}",
            "교점은 ({x0}, {y0})이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(a1)}x {B1S} = {c1},  {co(a2)}x {B2S} = {c2}", "hint": "교점 = 연립방정식의 해"},
            {"text": "{co(dx)}y = {ry}  →  y = {y0}", "hint": "(① × {a2}) − (② × {a1})"},
            {"text": "{co(a1)}x {sgn(b1y)} = {c1}  →  x = {x0}", "hint": "①에 대입"},
            {"text": "교점 ({x0}, {y0}) → {ASK} = {ans}", "marks": [{"on": "({x0}, {y0})", "note": "두 식 모두 만족"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="({x0}, {y0})를 두 식에 넣으면 {a1} × {pn(x0)} {sgn(b1y)} = {c1}, {a2} × {pn(x0)} {sgn(b2*y0)} = {c2}{ro(c2)} 모두 성립하므로 두 직선 위의 점이 맞다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["①: {a1} × {pn(x0)} {sgn(b1y)} = {c1} ✓", "②: {a2} × {pn(x0)} {sgn(b2*y0)} = {c2} ✓ → {ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="교점의 좌표는 연립방정식 {co(a1)}x {B1S} = {c1}, {co(a2)}x {B2S} = {c2}의 해이므로 이를 풀면 x = {x0}, y = {y0}이다. 따라서 p = {x0}, q = {y0}이고 {ASK} = {ans}이다.",
        rubric=[
            {"element": "연립방정식으로 보기", "points": 2, "criterion": "교점의 좌표가 두 방정식의 연립방정식의 해임을 밝혔다.", "partial": "한 식에만 대입해 구하려 했으면 인정하지 않는다."},
            {"element": "해 구하기", "points": 3, "criterion": "x = {x0}, y = {y0}{eul(y0)} 구했다.", "partial": "하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


def li_t2_final():
    t = li_t2()
    t["derive"]["ry"] = "a2*c1 - a1*c2"
    for k in ("sol2", "model_answer"):
        pass
    t["sol2"][1] = "(① × {a2}) − (② × {a1})에서 {co(dx)}y = {ry}, y = {y0}이고 ①에서 {co(a1)}x {sgn(b1y)} = {c1}, x = {x0}"
    t["sol2_fig"][0]["args"]["lines"][1]["text"] = "{co(dx)}y = {ry}  →  y = {y0}"
    t["constraints"] += ["a1 != a2"]
    return t


def li_t3():
    return tpl(LI, 3, LI_BASE,
        title="연립방정식의 해가 무수히 많을 조건 — a + b",
        skill="두 직선이 일치할 때(계수의 비가 모두 같을 때) 해가 무수히 많음을 이용해 a, b를 구하기",
        variant_axis={"배수": "2~4", "계수": "±1~±5"},
        discriminates="해가 무수히 많은 것을 '두 직선이 일치'로 해석해 a, b를 같은 배수로 맞추는가",
        difficulty=3,
        params=[{"name": "p", "values": {"in": [1, 2, 3, 4, 5]}}, {"name": "q", "values": {"in": [-4, -3, -2, 2, 3, 4]}}, {"name": "r", "values": {"in": NZ8}}, {"name": "k", "values": {"in": [2, 3, 4]}}],
        table=[sgn_rows(NZ4, "q", "y")],
        derive={"a": "k*p", "b": "k*r", "kq": "k*q", "ans": "k*p + k*r"},
        constraints=["ans != 0", "ans not in (p, abs(q), r, kq, k)", "a != b"],
        cost_values=["p", "q", "r", "k", "a", "b", "ans"],
        answer_var="ans",
        verify=["a == k*p", "b == k*r", "ans == a + b"],
        question="연립방정식 {co(p)}x {QS} = {r}, ax {sgn(kq)}y = b의 해가 무수히 많을 때, 상수 a, b에 대하여 a + b의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="연립방정식의 해가 무수히 많다는 것은 두 일차방정식의 그래프(직선)가 완전히 겹친다는 뜻이다. 그러려면 한 식이 다른 식의 몇 배가 되어야 한다. y의 계수를 비교하면 {kq}{eun(kq)} {q}의 {k}배이므로 둘째 식은 첫째 식의 {k}배여야 하고, a, b도 각각 {k}배가 된다.",
        sol2=[
            "해가 무수히 많으려면 두 직선이 일치해야 하므로 둘째 식은 첫째 식의 몇 배여야 한다",
            "y의 계수 비교: {kq} ÷ {pn(q)} = {k}이므로 첫째 식 × {k}: {co(a)}x {sgn(kq)}y = {b}",
            "따라서 a = {a}, b = {b}이고 a + b = {ans}",
        ],
        sol2_fig=steps([
            {"text": "해가 무수히 많다 ⟺ 두 직선이 일치", "hint": "한 식이 다른 식의 배수"},
            {"text": "({co(p)}x {QS} = {r}) × {k}  →  {co(a)}x {sgn(kq)}y = {b}", "hint": "y의 계수로 배수 {k} 찾기", "marks": [{"on": "{co(a)}x", "note": "a = {a}"}, {"on": "= {b}", "note": "b = {b}"}]},
            {"text": "a + b = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0", "mark:1-1")], [reveal(2)]],
        sol3="a = {a}, b = {b}이면 둘째 식 {co(a)}x {sgn(kq)}y = {b}의 양변을 {k}{ro(k)} 나누면 첫째 식 {co(p)}x {QS} = {r}{ika(r)} 되어 두 식이 같다. 따라서 a + b = {ans}이다.",
        sol3_fig=steps(["({co(a)}x {sgn(kq)}y = {b}) ÷ {k} = ({co(p)}x {QS} = {r}) ✓", "a + b = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="해가 무수히 많으려면 두 식이 같아야 하므로 둘째 식은 첫째 식의 {k}배이다. 따라서 a = {p} × {k} = {a}, b = {r} × {k} = {b}이고 a + b = {ans}이다.",
        rubric=[
            {"element": "조건 해석", "points": 3, "criterion": "해가 무수히 많으려면 두 식이 일치(배수 관계)해야 함을 밝혔다.", "partial": "'기울기만 같다'고 했으면 1점."},
            {"element": "a, b 구하기", "points": 2, "criterion": "배수 {k}{eul(k)} 찾아 a = {a}, b = {b}{eul(b)} 구했다.", "partial": "하나만 맞으면 1점."},
        ],
        rubric_total=5,
    )


def li_t4():
    return tpl(LI, 4, LI_BASE,
        title="연립방정식의 해가 없을 조건 — 상수 a",
        skill="두 직선이 평행할 때(기울기는 같고 y절편은 다를 때) 해가 없음을 이용해 a를 구하기",
        variant_axis={"배수": "2~4", "계수": "±1~±5"},
        discriminates="해가 없는 것을 '두 직선이 평행'으로 해석해 x, y의 계수의 비만 맞추고 상수항은 다름을 확인하는가",
        difficulty=3,
        params=[{"name": "p", "values": {"in": [1, 2, 3, 4, 5]}}, {"name": "q", "values": {"in": [-4, -3, -2, 2, 3, 4]}}, {"name": "r", "values": {"in": NZ8}}, {"name": "k", "values": {"in": [2, 3, 4]}}, {"name": "bb", "values": {"in": NZ8}}],
        table=[sgn_rows(NZ4, "q", "y")],
        derive={"a": "k*p", "kq": "k*q", "kr": "k*r", "ans": "k*p"},
        constraints=["bb != kr", "ans not in (p, abs(q), r, kq, k, bb)"],
        cost_values=["p", "q", "r", "k", "bb", "a"],
        answer_var="ans",
        verify=["ans == k*p", "kq == k*q", "bb != k*r"],
        question="연립방정식 {co(p)}x {QS} = {r}, ax {sgn(kq)}y = {bb}의 해가 없을 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="연립방정식의 해가 없다는 것은 두 직선이 평행해서 만나지 않는다는 뜻이다. 두 직선이 평행하려면 x, y의 계수의 비가 같고(기울기 같음) 상수항의 비는 달라야 한다(y절편 다름). y의 계수 {kq}{eun(kq)} {q}의 {k}배이므로 a도 {p}의 {k}배여야 하고, 상수항 {bb}{eun(bb)} {r}의 {k}배인 {kr}{wa(kr)} 다르므로 조건에 맞는다.",
        sol2=[
            "해가 없으려면 두 직선이 평행: x, y의 계수의 비는 같고 상수항의 비는 다르다",
            "y의 계수 비교: {kq} ÷ {pn(q)} = {k}이므로 a = {p} × {k} = {a}",
            "상수항: {r} × {k} = {kr} ≠ {bb}이므로 두 직선은 일치하지 않고 평행하다. 따라서 a = {ans}",
        ],
        sol2_fig=steps([
            {"text": "해가 없다 ⟺ 두 직선이 평행", "hint": "계수의 비는 같고 상수항의 비는 다르다"},
            {"text": "a = {p} × {k} = {a}", "hint": "y의 계수로 배수 {k} 찾기", "marks": [{"on": "{a}", "note": "x의 계수도 {k}배"}]},
            {"text": "{r} × {k} = {kr} ≠ {bb} ✓", "hint": "상수항은 달라야 한다(일치 아님)"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")]],
        sol3="a = {a}이면 둘째 식은 {co(a)}x {sgn(kq)}y = {bb}이고, 첫째 식의 {k}배 {co(a)}x {sgn(kq)}y = {kr}{wa(kr)} 좌변은 같고 우변만 다르므로 두 직선은 평행하다 — 해가 없다. 따라서 a = {ans}이다.",
        sol3_fig=steps(["첫째 × {k}: {co(a)}x {sgn(kq)}y = {kr}", "둘째: {co(a)}x {sgn(kq)}y = {bb} — 좌변 같고 우변 다름 → 평행 ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="해가 없으려면 두 직선이 평행해야 하므로 x, y의 계수의 비가 같아야 한다. y의 계수에서 배수가 {k}이므로 a = {p} × {k} = {a}이고, 상수항은 {kr} ≠ {bb}이므로 조건에 맞는다. 따라서 a = {ans}이다.",
        rubric=[
            {"element": "조건 해석", "points": 3, "criterion": "해가 없으려면 두 직선이 평행(계수의 비 같음, 상수항의 비 다름)임을 밝혔다.", "partial": "상수항 조건을 언급하지 않았으면 1점."},
            {"element": "a 구하기", "points": 2, "criterion": "배수 {k}{eul(k)} 찾아 a = {a}{eul(a)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def li_t5():
    return tpl(LI, 5, LI_BASE,
        title="세 직선이 한 점에서 만날 때 상수 a",
        skill="상수가 없는 두 직선의 교점을 먼저 구하고, 그 점이 셋째 직선 위에 있도록 a를 정하기",
        variant_axis={"계수": "±1~±4"},
        discriminates="'세 직선이 한 점에서 만난다'를 두 직선의 교점이 셋째 직선 위에 있는 것으로 옮기는가",
        difficulty=3, process="문제해결",
        params=[{"name": "a1", "values": {"in": [1, 2, 3]}}, {"name": "b1", "values": {"in": NZ4}}, {"name": "a2", "values": {"in": [1, 2, 3, 4]}}, {"name": "b2", "values": {"in": NZ4}},
                {"name": "x0", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "y0", "values": {"in": [-4, -3, -2, -1, 1, 2, 3, 4]}}, {"name": "a", "values": {"in": NZ4}}],
        table=[sgn_rows(NZ4, "b1", "y"), sgn_rows(NZ4, "b2", "y")],
        derive={"c1": "a1*x0 + b1*y0", "c2": "a2*x0 + b2*y0", "det": "a1*b2 - a2*b1", "c3": "a*x0 - y0", "ax0": "a*x0", "ans": "a",
                **FRAME6, **line_clip("l", "-a1/b1", "c1/b1"), **line_clip("m", "-a2/b2", "c2/b2"), **line_clip("n", "a", "-c3")},
        constraints=["det != 0", "c1 != 0", "c2 != 0", "c3 != 0", "ans not in (a1, a2, abs(b1), abs(b2), c1, c2, c3, x0, y0)", "x0 != y0", "a1 != a2", "a1*b2 != a2*b1"],
        cost_values=["a1", "b1", "c1", "a2", "b2", "c2", "x0", "y0", "c3", "a"],
        answer_var="ans",
        verify=["a1*x0 + b1*y0 == c1", "a2*x0 + b2*y0 == c2", "ans*x0 - y0 == c3"],
        question="세 직선 {co(a1)}x {B1S} = {c1}, {co(a2)}x {B2S} = {c2}, ax − y = {c3}이 한 점에서 만날 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="세 직선이 한 점에서 만나면 그 점은 세 방정식을 모두 만족한다. 상수 a가 없는 두 직선의 교점을 연립방정식으로 먼저 구하고, 그 교점의 좌표를 셋째 직선 ax − y = {c3}에 대입해 a를 정한다.",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], [{"name": "P", "coord": ["{x0}", "{y0}"]}], [seg("l"), seg("m"), seg("n", style="dashed")]),
        sol2=[
            "a가 없는 두 직선 {co(a1)}x {B1S} = {c1}, {co(a2)}x {B2S} = {c2}의 교점: 연립하여 풀면 x = {x0}, y = {y0}",
            "이 점 ({x0}, {y0})가 ax − y = {c3} 위에 있어야 하므로 {co(x0)}a − {pn(y0)} = {c3}",
            "{co(x0)}a = {c3} + {pn(y0)} = {ax0}, a = {ans}",
        ],
        sol2_fig=steps([
            {"text": "두 직선의 교점: ({x0}, {y0})", "hint": "a 없는 두 식을 연립"},
            {"text": "{co(x0)}a − {pn(y0)} = {c3}", "hint": "교점을 셋째 직선에 대입"},
            {"text": "{co(x0)}a = {ax0}  →  a = {ans}", "marks": [{"on": "{ans}", "note": "세 직선이 한 점 ({x0}, {y0})를 지난다"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="a = {ans}이면 셋째 직선 {co(a)}x − y = {c3}에 ({x0}, {y0})를 넣으면 {a} × {pn(x0)} − {pn(y0)} = {c3}{ro(c3)} 성립하므로 세 직선은 모두 점 ({x0}, {y0})를 지난다. 따라서 a = {ans}이다.",
        sol3_fig=steps(["{a} × {pn(x0)} − {pn(y0)} = {c3} ✓", "a = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="두 직선 {co(a1)}x {B1S} = {c1}, {co(a2)}x {B2S} = {c2}의 교점은 ({x0}, {y0})이다. 이 점이 ax − y = {c3} 위에 있으므로 {co(x0)}a − {pn(y0)} = {c3}에서 a = {ans}이다.",
        rubric=[
            {"element": "교점 구하기", "points": 3, "criterion": "a가 없는 두 직선을 연립해 교점 ({x0}, {y0})를 구했다.", "partial": "가감법 부호 실수면 1점."},
            {"element": "a 구하기", "points": 2, "criterion": "교점을 ax − y = {c3}에 대입해 a = {ans}{eul(ans)} 구했다.", "partial": "대입 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def li_t6():
    return tpl(LI, 6, LI_BASE,
        title="두 점을 지나는 직선이 y축에 평행할 때 상수 k",
        skill="y축에 평행한 직선은 x = p 꼴이므로 두 점의 x좌표가 같음을 이용하기",
        variant_axis={"계수": "±1~±3", "상수": "±1~±6"},
        discriminates="y축에 평행 ⟺ x좌표가 같다(y좌표가 아님)를 구별하는가",
        difficulty=2,
        params=[{"name": "c1", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "d1", "values": {"in": NZ6}}, {"name": "c2", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "d2", "values": {"in": NZ6}},
                {"name": "e1", "values": {"in": NZ6}}, {"name": "e2", "values": {"in": NZ6}}],
        table=[sgn_rows(NZ6, "d1", ""), sgn_rows(NZ6, "d2", "")],
        derive={"dc": "c1 - c2", "dd": "d2 - d1", "k": "(d2 - d1)/(dc + (dc == 0))", "xk": "c1*k + d1", "ans": "k"},
        constraints=["c1 != c2", "k == floor(k)", "k != 0", "e1 != e2", "ans not in (c1, c2, abs(d1), abs(d2), e1, e2)", "abs(k) <= 8"],
        cost_values=["c1", "d1", "c2", "d2", "dc", "dd", "k", "xk"],
        answer_var="ans",
        verify=["c1*ans + d1 == c2*ans + d2", "xk == c2*ans + d2"],
        question="두 점 ({co(c1)}k {D1S}, {e1}), ({co(c2)}k {D2S}, {e2})를 지나는 직선이 y축에 평행할 때, 상수 k의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="y축에 평행한 직선은 x = p 꼴이고, 그 위의 점은 x좌표가 모두 {xk}처럼 같은 값이다. 그러므로 두 점의 x좌표 {co(c1)}k {D1S}와 {co(c2)}k {D2S}{ika(d2)} 같다는 방정식을 세워 k를 구한다. y좌표가 같은 것은 x축에 평행한 경우이니 헷갈리지 않도록 한다.",
        sol2=[
            "y축에 평행하려면 두 점의 x좌표가 같아야 하므로 {co(c1)}k {D1S} = {co(c2)}k {D2S}",
            "{co(dc)}k = {dd}, k = {ans}",
            "이때 두 점의 x좌표는 {xk}{ro(xk)} 같다",
        ],
        sol2_fig=steps([
            {"text": "{co(c1)}k {D1S} = {co(c2)}k {D2S}", "hint": "y축에 평행 ⟺ x좌표가 같다"},
            {"text": "{co(dc)}k = {dd}  →  k = {ans}", "marks": [{"on": "{ans}", "note": "x좌표 {xk}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="k = {ans}이면 두 점은 ({xk}, {e1}), ({xk}, {e2})가 되어 x좌표가 같으므로 두 점을 지나는 직선은 x = {xk}, 곧 y축에 평행한 직선이다. 따라서 k = {ans}이다.",
        sol3_fig=steps(["({xk}, {e1}), ({xk}, {e2}) → 직선 x = {xk}", "k = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="y축에 평행한 직선 위의 점은 x좌표가 같으므로 {co(c1)}k {D1S} = {co(c2)}k {D2S}에서 {co(dc)}k = {dd}, k = {ans}이다.",
        rubric=[
            {"element": "조건 세우기", "points": 3, "criterion": "x좌표가 같다는 식 {co(c1)}k {D1S} = {co(c2)}k {D2S}{eul(d2)} 세웠다.", "partial": "y좌표가 같다는 식을 세웠으면 인정하지 않는다."},
            {"element": "k 구하기", "points": 2, "criterion": "k = {ans}{eul(ans)} 구했다.", "partial": "이항 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def li_t7():
    return tpl(LI, 7, LI_BASE,
        title="두 점을 지나는 직선이 x축에 평행할 때 상수 k",
        skill="x축에 평행한 직선은 y = q 꼴이므로 두 점의 y좌표가 같음을 이용하기",
        variant_axis={"계수": "±1~±3", "상수": "±1~±6"},
        discriminates="x축에 평행 ⟺ y좌표가 같다(x좌표가 아님)를 구별하는가",
        difficulty=2,
        params=[{"name": "c1", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "d1", "values": {"in": NZ6}}, {"name": "c2", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "d2", "values": {"in": NZ6}},
                {"name": "e1", "values": {"in": NZ6}}, {"name": "e2", "values": {"in": NZ6}}],
        table=[sgn_rows(NZ6, "d1", ""), sgn_rows(NZ6, "d2", "")],
        derive={"dc": "c1 - c2", "dd": "d2 - d1", "k": "(d2 - d1)/(dc + (dc == 0))", "yk": "c1*k + d1", "ans": "k"},
        constraints=["c1 != c2", "k == floor(k)", "k != 0", "e1 != e2", "ans not in (c1, c2, abs(d1), abs(d2), e1, e2)", "abs(k) <= 8"],
        cost_values=["c1", "d1", "c2", "d2", "dc", "dd", "k", "yk"],
        answer_var="ans",
        verify=["c1*ans + d1 == c2*ans + d2", "yk == c2*ans + d2"],
        question="두 점 ({e1}, {co(c1)}k {D1S}), ({e2}, {co(c2)}k {D2S})를 지나는 직선이 x축에 평행할 때, 상수 k의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x축에 평행한 직선은 y = q 꼴이고, 그 위의 점은 y좌표가 모두 같다. 그러므로 두 점의 y좌표 {co(c1)}k {D1S}와 {co(c2)}k {D2S}{ika(d2)} 같다는 방정식을 세워 k를 구한다. x좌표가 같은 것은 y축에 평행한 경우다.",
        sol2=[
            "x축에 평행하려면 두 점의 y좌표가 같아야 하므로 {co(c1)}k {D1S} = {co(c2)}k {D2S}",
            "{co(dc)}k = {dd}, k = {ans}",
            "이때 두 점의 y좌표는 {yk}{ro(yk)} 같다",
        ],
        sol2_fig=steps([
            {"text": "{co(c1)}k {D1S} = {co(c2)}k {D2S}", "hint": "x축에 평행 ⟺ y좌표가 같다"},
            {"text": "{co(dc)}k = {dd}  →  k = {ans}", "marks": [{"on": "{ans}", "note": "y좌표 {yk}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="k = {ans}이면 두 점은 ({e1}, {yk}), ({e2}, {yk})가 되어 y좌표가 같으므로 두 점을 지나는 직선은 y = {yk}, 곧 x축에 평행한 직선이다. 따라서 k = {ans}이다.",
        sol3_fig=steps(["({e1}, {yk}), ({e2}, {yk}) → 직선 y = {yk}", "k = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x축에 평행한 직선 위의 점은 y좌표가 같으므로 {co(c1)}k {D1S} = {co(c2)}k {D2S}에서 {co(dc)}k = {dd}, k = {ans}이다.",
        rubric=[
            {"element": "조건 세우기", "points": 3, "criterion": "y좌표가 같다는 식 {co(c1)}k {D1S} = {co(c2)}k {D2S}{eul(d2)} 세웠다.", "partial": "x좌표가 같다는 식을 세웠으면 인정하지 않는다."},
            {"element": "k 구하기", "points": 2, "criterion": "k = {ans}{eul(ans)} 구했다.", "partial": "이항 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


LI_SEED = {
    "seed_id": LI, "category": "연산",
    "title": "일차방정식의 그래프 — 기울기·절편·두 직선의 교점·해가 무수히 많음·해 없음·세 직선 한 점·축에 평행한 직선",
    "unit_id": "m2-1", "concept_ids": ["m2-1-21", "m2-1-22", "m2-1-23"],
    "schema_id": None, "schema_name": "일차방정식의 그래프와 연립방정식의 해",
    "source_item_ids": [],
    "note": "교점은 해(x0, y0)를 파라미터로 두고 상수항을 역산. 축에 평행 조건은 좌표에 k를 넣은 두 점의 x(y)좌표가 같다는 식.",
    "geometry": False,
    "templates": [li_t1(), li_t2_final(), li_t3(), li_t4(), li_t5(), li_t6(), li_t7()],
}


if __name__ == "__main__":
    for seed in (FV_SEED, LP_SEED, LA_SEED, LI_SEED):
        with_pitfalls(seed)
        dump(seed)
