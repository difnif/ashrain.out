# itemfactory/tools/mkseed_m3_quad.py — m3-1 인수분해·이차방정식 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m3_quad.py
#     → seeds/m3-1-factor.json      (인수분해: 완전제곱식 조건·x²+bx+c·acx²+…·공통인수·치환·식의 값·도형, 7틀)
#     → seeds/m3-1-quad-solve.json  (이차방정식 풀이: 인수분해·한 근→상수·제곱근·완전제곱식·근의 공식·중근·근의 개수·잘못 본 방정식, 8틀)
#     → seeds/m3-1-quad-apply.json  (이차방정식 활용: 연속수·두 수·나누어 주기·직사각형·정사각형·길·물체·대각선, 8틀)
#
# 이차식 표기: 이차항 {co(a)}x², 일차항 {sgt(b)}x (± 1 → '+ x'), 상수항 {sgn(c)} (expr.py v1.2 sgt).
# 해가 두 개인 답은 'x = p 또는 x = q' (parse_answer set). 표에 숫자가 박힌 문자열은 {…} 없이 파이썬에서 미리 만든다.
from __future__ import annotations

import os
import sys
from math import gcd, isqrt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from seedlib import COMMON_APPLY, dump, hl, reveal, steps, with_pitfalls  # noqa: E402
from genkit.expr import eul as _eul, ika as _ika  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
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


def _sg(v) -> str:
    return "+" if v > 0 else "−"


def _st(v, var: str = "") -> str:
    """부호 붙은 항 문자열: 3 → '+ 3x', -1 → '− x', 0 → ''"""
    if v == 0:
        return ""
    s = "+ " if v > 0 else "− "
    a = abs(v)
    return s + ("" if (a == 1 and var) else str(a)) + var


def _lin(a, b, var="x") -> str:
    """ax + b → '2x + 3', 'x − 1', '-3x + 2'"""
    lead = ("" if a == 1 else ("-" if a == -1 else str(a))) + var
    return lead + (f" {_st(b)}" if b else "")


def _quad(a, b, c) -> str:
    """ax² + bx + c → '2x² − 3x + 1' (b, c 는 0 이면 생략)"""
    lead = ("" if a == 1 else ("-" if a == -1 else str(a))) + "x²"
    s = lead
    if b:
        s += " " + _st(b, "x")
    if c:
        s += " " + _st(c)
    return s


def _pn(v) -> str:
    return f"({v})" if v < 0 else str(v)


BASE = {"process": "절차수행", "context": "무맥락", "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}
SQF = [2, 3, 5, 6, 7, 10, 11, 13, 14, 15, 17, 19, 21, 22, 23]

# ═══════════════════════════════════════════════════════════════════ 1. 인수분해
FA = "m3-1-factor"
FA_BASE = {**BASE, "prereq": ["곱셈 공식", "공통인수"], "ops": ["인수분해"], "traps": ["부호", "공통인수 빠뜨림"], "tags": ["인수분해"]}


# t1 — 완전제곱식이 되는 조건 (□ 채우기)
def _cs_rows():
    out = {}
    for p in (1, 2, 3, 4, 5):
        A = "x" if p == 1 else f"{p}x"
        lead = "" if p == 1 else str(p * p)
        for q in range(1, 10):
            for sg in ("+", "−"):
                sq = f"({A} {sg} {q})²"
                exp = f"{lead}x² {sg} {2 * p * q}x + {q * q}"
                out[f"c{p}-{q}-{sg}"] = {"EXPR": f"{lead}x² {sg} {2 * p * q}x + □", "J": "가", "ASK": "□ 안에 알맞은 수", "ans": q * q, "A": A, "B": str(q), "SQ": sq, "EXP": exp,
                                         "STEP1": f"첫 항 {lead}x² = ({A})², 가운데 항 {2 * p * q}x = 2 × {A} × {q}, 즉 B = {q}이므로 마지막 항은 {q}²",
                                         "STEP2": f"□ = {q}² = {q * q}", "MID": f"2 × {A} × {q} = {2 * p * q}x", "ANS_T": f"{q * q}"}
            out[f"k{p}-{q}"] = {"EXPR": f"{lead}x² + □x + {q * q}", "J": _ika(q * q), "ASK": "□ 안에 알맞은 양수", "ans": 2 * p * q, "A": A, "B": str(q), "SQ": f"({A} + {q})²", "EXP": f"{lead}x² + {2 * p * q}x + {q * q}",
                                "STEP1": f"첫 항 {lead}x² = ({A})², 마지막 항 {q * q} = {q}²이므로 가운데 항은 2 × {A} × {q} = {2 * p * q}x",
                                "STEP2": f"가운데 항 2 × {A} × {q} = {2 * p * q}x이므로 □ = {2 * p * q}", "MID": f"2 × {A} × {q} = {2 * p * q}x", "ANS_T": f"{2 * p * q}"}
    return out


CS_ROWS = _cs_rows()


def fa_t1():
    return tpl(FA, 1, FA_BASE,
        title="완전제곱식이 되도록 □ 채우기 — 상수항 또는 x의 계수",
        skill="A² ± 2AB + B²의 꼴에서 두 항으로 A, B를 정하고 나머지 한 항을 만들기",
        variant_axis={"이차항": "x²·4x²·9x²·16x²·25x²", "B": "1~9", "빈칸": "상수항 / x의 계수(양수)"},
        difficulty=2,
        discriminates="가운데 항이 2AB(2배)임을 알고, 상수항은 B², x의 계수는 2AB로 구분해 채우는가",
        params=[{"name": "f", "values": {"in": list(CS_ROWS)}}],
        table={"key": "f", "rows": CS_ROWS},
        cost_values=["ans"],
        answer_var="ans",
        verify=["ans > 0"],
        question="식 {EXPR}{J} 완전제곱식이 될 때, {ASK}를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="완전제곱식은 (A + B)² = A² + 2AB + B² 또는 (A − B)² = A² − 2AB + B²의 꼴이다. 주어진 두 항에서 A와 B를 정하면 나머지 한 항이 정해진다 — 가운데 항은 AB의 2배, 마지막 항은 B의 제곱이다.",
        sol2=[
            "{STEP1}",
            "{STEP2}",
            "확인: {SQ} = {EXP}",
        ],
        sol2_fig=steps([
            {"text": "A = {A}, B = {B}", "hint": "A² ± 2AB + B²"},
            {"text": "□ = {ANS_T}", "hint": "{MID}", "marks": [{"on": "{ANS_T}", "note": "□"}]},
            {"text": "{SQ} = {EXP}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{SQ}{eul(SQ)} 전개하면 {EXP}{ika(EXP)} 되어 주어진 식과 맞는다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{SQ} = {EXP} ✓", "□ = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{STEP1}이다. 따라서 {STEP2}이고, 이때 주어진 식은 {SQ}{ika(SQ)} 된다.",
        rubric=[
            {"element": "A, B 정하기", "points": 2, "criterion": "A = {A}, B = {B}{ro(B)} 잡았다.", "partial": "B를 제곱수 그대로 두었으면 1점."},
            {"element": "빈칸 구하기", "points": 3, "criterion": "{STEP2}{eul(ans)} 구했다.", "partial": "가운데 항의 2배를 빠뜨렸으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t2 — x² + bx + c = (x + p)(x + q), p > q → p − q
def fa_t2():
    return tpl(FA, 2, FA_BASE,
        title="x² + bx + c의 인수분해 — (x + p)(x + q)에서 p − q",
        skill="곱이 c이고 합이 b인 두 정수를 찾아 (x + p)(x + q)로 인수분해하기",
        variant_axis={"p, q": "−9~9 (0 제외)"},
        difficulty=2,
        discriminates="곱이 c(부호 포함)이고 합이 b인 두 정수를 부호까지 맞게 찾는가",
        params=[{"name": "p", "values": {"in": [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]}}, {"name": "q", "values": {"in": [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]}}],
        derive={"b": "p + q", "c": "p*q", "ans": "p - q"},
        constraints=["p > q", "b != 0", "ans not in (b, c)", "ans != -b", "ans != -c"],
        cost_values=["p", "q", "b", "c", "ans"],
        answer_var="ans",
        verify=["ans == p - q", "b == p + q", "c == p*q"],
        question="x² {sgt(b)}x {sgn(c)}{eul(c)} 인수분해하면 (x + p)(x + q)일 때, 정수 p, q (p > q)에 대하여 p − q의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="(x + p)(x + q) = x² + (p + q)x + pq이므로, 곱이 상수항 {c}{ika(c)} 되고 합이 x의 계수 {b}{ika(b)} 되는 두 정수를 찾는다. 먼저 곱이 {c}인 정수 쌍을 나열하고 그중 합이 {b}인 것을 고른다(부호에 주의).",
        sol2=[
            "곱이 {c}, 합이 {b}인 두 정수: {p}{wa(p)} {q}",
            "x² {sgt(b)}x {sgn(c)} = (x {sgn(p)})(x {sgn(q)})",
            "따라서 p = {p}, q = {q}이고 p − q = {ans}",
        ],
        sol2_fig=steps([
            {"text": "곱 {c}, 합 {b} → {p}, {q}", "hint": "pq = c, p + q = b"},
            {"text": "(x {sgn(p)})(x {sgn(q)})", "hint": "인수분해", "marks": [{"on": "(x {sgn(p)})", "note": "p = {p}"}]},
            {"text": "p − q = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="(x {sgn(p)})(x {sgn(q)})를 전개하면 x² + ({p} {sgn(q)})x + {pn(p)} × {pn(q)} = x² {sgt(b)}x {sgn(c)}{ro(c)} 원래 식과 같다. p > q이므로 p = {p}, q = {q}이고 p − q = {ans}이다.",
        sol3_fig=steps(["전개 확인: x² {sgt(b)}x {sgn(c)} ✓", "p − q = {p} − {pn(q)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="곱이 {c}이고 합이 {b}인 두 정수는 {p}, {q}이므로 x² {sgt(b)}x {sgn(c)} = (x {sgn(p)})(x {sgn(q)})이다. 따라서 p = {p}, q = {q}이고 p − q = {ans}이다.",
        rubric=[
            {"element": "인수분해", "points": 3, "criterion": "(x {sgn(p)})(x {sgn(q)}){ro(q)} 인수분해했다.", "partial": "부호가 틀렸으면 1점."},
            {"element": "p − q", "points": 2, "criterion": "p > q에 맞게 p = {p}, q = {q}{ro(q)} 정해 p − q = {ans}{eul(ans)} 구했다.", "partial": "p, q를 바꿔 −{ans}{ro(ans)} 답했으면 1점."},
        ],
        rubric_total=5,
    )


# t3 — acx² + (ad + bc)x + bd = (ax + b)(cx + d), a, c > 0 → a + b + c + d
def fa_t3():
    return tpl(FA, 3, FA_BASE,
        title="acx² + (ad + bc)x + bd의 인수분해 — (ax + b)(cx + d)에서 a + b + c + d",
        skill="이차항과 상수항을 두 수의 곱으로 나누고 대각선 곱의 합이 x의 계수가 되는 조합 찾기",
        variant_axis={"a, c": "1~3 (둘 다 1은 제외)", "b, d": "±1~±6"},
        difficulty=3,
        discriminates="이차항의 계수가 1이 아닐 때 대각선 곱(ad + bc)으로 x의 계수를 맞추는가",
        params=[{"name": "a", "values": {"int": [1, 3]}}, {"name": "b", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}, {"name": "c", "values": {"int": [1, 3]}}, {"name": "d", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}],
        derive={"A": "a*c", "B": "a*d + b*c", "C": "b*d", "ad": "a*d", "bc": "b*c", "ans": "a + b + c + d"},
        constraints=["A >= 2", "B != 0", "gcd(a, b) == 1", "gcd(c, d) == 1", "ans not in (A, B, C)", "ans != 0", "a <= c"],
        cost_values=["a", "b", "c", "d", "A", "B", "C", "ans"],
        answer_var="ans",
        verify=["ans == a + b + c + d", "A == a*c", "B == ad + bc", "C == b*d"],
        question="{co(A)}x² {sgt(B)}x {sgn(C)}{eul(C)} 인수분해하면 (ax + b)(cx + d)일 때, 정수 a, b, c, d (a, c는 양수)에 대하여 a + b + c + d의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="(ax + b)(cx + d) = acx² + (ad + bc)x + bd이다. 이차항의 계수 {A}{eul(A)} a × c로, 상수항 {C}{eul(C)} b × d로 나누어 놓고, 대각선으로 곱해 더한 ad + bc가 x의 계수 {B}{ika(B)} 되는 조합을 찾는다.",
        sol2=[
            "a × c = {a} × {c} = {A}, b × d = {pn(b)} × {pn(d)} = {C}{ro(C)} 나누어 본다",
            "대각선 곱의 합: {a} × {pn(d)} + {pn(b)} × {c} = {ad} + {pn(bc)} = {B} ✓",
            "따라서 ({co(a)}x {sgn(b)})({co(c)}x {sgn(d)})이고 a + b + c + d = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(a)}x  |  {sgn(b)}", "hint": "이차항 {A} = {a} × {c}"},
            {"text": "{co(c)}x  |  {sgn(d)}", "hint": "상수항 {C} = {pn(b)} × {pn(d)}", "marks": [{"on": "{sgn(d)}", "note": "대각선 합 {B}"}]},
            {"text": "({co(a)}x {sgn(b)})({co(c)}x {sgn(d)}) → {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="({co(a)}x {sgn(b)})({co(c)}x {sgn(d)})를 전개하면 {A}x² + ({ad} {sgn(bc)})x {sgn(C)} = {co(A)}x² {sgt(B)}x {sgn(C)}{ro(C)} 맞다. a, c가 양수이므로 인수의 순서를 바꿔도 합은 같다: a + b + c + d = {ans}.",
        sol3_fig=steps(["전개 확인: {co(A)}x² {sgt(B)}x {sgn(C)} ✓", "{a} + {pn(b)} + {c} + {pn(d)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{co(A)}x² {sgt(B)}x {sgn(C)} = ({co(a)}x {sgn(b)})({co(c)}x {sgn(d)})이므로 a = {a}, b = {b}, c = {c}, d = {d}이고 a + b + c + d = {ans}이다.",
        rubric=[
            {"element": "인수분해", "points": 3, "criterion": "({co(a)}x {sgn(b)})({co(c)}x {sgn(d)}){ro(d)} 인수분해했다.", "partial": "대각선 곱의 합이 맞지 않는 조합을 썼으면 인정하지 않는다."},
            {"element": "합 구하기", "points": 2, "criterion": "a + b + c + d = {ans}{eul(ans)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


# t4 — 공통인수를 먼저 묶는 인수분해: k(x ± m)², k(x + m)(x − m)
def _cf_rows():
    out = {}
    for k in (2, 3, 4, 5):
        for m in range(1, 7):
            for sg in (1, -1):
                b = sg * m
                expr = _quad(k, 2 * k * b, k * m * m)
                inner = _quad(1, 2 * b, m * m)
                fac = f"{k}(x {_st(b)})²"
                out[f"s{k}-{m}-{sg}"] = {"EXPR": expr, "J": _eul(k * m * m), "FORMQ": "a(x + b)²", "FAC": fac, "INNER": inner, "k": k, "m": m, "bb": b, "ans": k + b,
                                         "STEP": f"x² {_st(2 * b, 'x')} + {m * m} = (x {_st(b)})²", "NAME": "완전제곱식", "BT": str(b)}
            expr = f"{k}x² − {k * m * m}"
            out[f"d{k}-{m}"] = {"EXPR": expr, "J": _eul(k * m * m), "FORMQ": "a(x + b)(x − b)", "FAC": f"{k}(x + {m})(x − {m})", "INNER": f"x² − {m * m}", "k": k, "m": m, "bb": m, "ans": k + m,
                                "STEP": f"x² − {m * m} = x² − {m}² = (x + {m})(x − {m})", "NAME": "합차 공식", "BT": str(m)}
    return out


CF_ROWS = _cf_rows()


def fa_t4():
    return tpl(FA, 4, FA_BASE,
        title="공통인수를 묶은 뒤 공식으로 인수분해 — a(x + b)², a(x + b)(x − b)에서 a + b",
        skill="모든 항의 공통인수를 먼저 묶어 내고 괄호 안을 완전제곱식 또는 합차 공식으로 인수분해하기",
        variant_axis={"공통인수": "2~5", "b": "1~6", "형태": "완전제곱 / 합차"},
        difficulty=2,
        discriminates="공통인수를 먼저 묶어 내는가, 그리고 괄호 안의 인수분해 공식을 바르게 고르는가",
        params=[{"name": "f", "values": {"in": list(CF_ROWS)}}],
        table={"key": "f", "rows": CF_ROWS},
        cost_values=["k", "m", "ans"],
        answer_var="ans",
        verify=["ans == k + bb"],
        question="{EXPR}{J} 인수분해하면 {FORMQ}일 때, 정수 a, b (a는 양수)에 대하여 a + b의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="각 항에 공통으로 들어 있는 인수 {k}{eul(k)} 먼저 묶어 내면 {k}({INNER})이 된다. 괄호 안 {INNER}{eun(INNER)} {NAME}으로 인수분해되므로 {FAC}{ika(FAC)} 된다. a는 공통인수, b는 괄호 안의 수이다.",
        sol2=[
            "공통인수 {k}{eul(k)} 묶으면 {k}({INNER})",
            "{STEP}",
            "따라서 {FAC}이고 a = {k}, b = {BT}, a + b = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{k}({INNER})", "hint": "공통인수 {k}"},
            {"text": "{FAC}", "hint": "{NAME}", "marks": [{"on": "{FAC}", "note": "a = {k}, b = {BT}"}]},
            {"text": "a + b = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{FAC}{eul(FAC)} 전개하면 {k} × ({INNER}) = {EXPR}{ro(EXPR)} 원래 식과 같다. 따라서 a + b = {ans}이다.",
        sol3_fig=steps(["{FAC} = {EXPR} ✓", "a + b = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{EXPR} = {k}({INNER}) = {FAC}이므로 a = {k}, b = {BT}이고 a + b = {ans}이다.",
        rubric=[
            {"element": "공통인수", "points": 2, "criterion": "공통인수 {k}{eul(k)} 묶어 {k}({INNER}){eul(INNER)} 얻었다.", "partial": "공통인수를 일부만 묶었으면 1점."},
            {"element": "공식 인수분해", "points": 3, "criterion": "{FAC}{ro(FAC)} 인수분해해 a + b = {ans}{eul(ans)} 구했다.", "partial": "공통인수를 묶지 않고 (kx + …)(…) 꼴로 썼어도 a, b를 바르게 읽었으면 2점."},
        ],
        rubric_total=5,
    )


# t5 — 치환: (x + a)² + b(x + a) + c = (x + p)(x + q) → pq
def fa_t5():
    return tpl(FA, 5, FA_BASE,
        title="공통부분을 치환하는 인수분해 — (x + a)² + b(x + a) + c에서 pq",
        skill="공통부분 x + a를 한 문자 t로 바꿔 t² + bt + c를 인수분해한 뒤 t를 되돌리기",
        variant_axis={"a": "±1~±5", "r, s": "±1~±6"},
        difficulty=3,
        discriminates="치환 후 인수분해하고 t = x + a를 되돌려 (x + p)(x + q) 꼴까지 정리하는가",
        params=[{"name": "a", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}}, {"name": "r", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}, {"name": "s", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}],
        derive={"b": "r + s", "c": "r*s", "p": "a + r", "q": "a + s", "ans": "(a + r)*(a + s)"},
        constraints=["r >= s", "b != 0", "p != 0", "q != 0", "ans not in (a, b, c, r, s)", "ans != 0"],
        cost_values=["a", "r", "s", "b", "c", "p", "q", "ans"],
        answer_var="ans",
        verify=["ans == p*q", "p == a + r", "q == a + s", "b == r + s", "c == r*s"],
        question="(x {sgn(a)})² {sgt(b)}(x {sgn(a)}) {sgn(c)}{eul(c)} 인수분해하면 (x + p)(x + q)일 때, 정수 p, q에 대하여 pq의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x {sgn(a)}{ika(a)} 두 번 나오므로 x {sgn(a)} = t로 놓으면 식은 t² {sgt(b)}t {sgn(c)}{ika(c)} 된다. 곱이 {c}, 합이 {b}인 두 정수 {r}, {s}로 (t {sgn(r)})(t {sgn(s)})로 인수분해한 뒤 t에 x {sgn(a)}{eul(a)} 되돌려 괄호 안을 정리한다.",
        sol2=[
            "x {sgn(a)} = t로 놓으면 t² {sgt(b)}t {sgn(c)} = (t {sgn(r)})(t {sgn(s)})",
            "t = x {sgn(a)}{eul(a)} 되돌리면 (x {sgn(a)} {sgn(r)})(x {sgn(a)} {sgn(s)}) = (x {sgn(p)})(x {sgn(q)})",
            "따라서 p = {p}, q = {q}이고 pq = {ans}",
        ],
        sol2_fig=steps([
            {"text": "t² {sgt(b)}t {sgn(c)} = (t {sgn(r)})(t {sgn(s)})", "hint": "x {sgn(a)} = t"},
            {"text": "(x {sgn(p)})(x {sgn(q)})", "hint": "t를 되돌려 정리", "marks": [{"on": "(x {sgn(p)})", "note": "{pn(a)} {sgn(r)} = {p}"}]},
            {"text": "pq = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="(x {sgn(p)})(x {sgn(q)})에 x = 0을 넣으면 {pn(p)} × {pn(q)} = {ans}이고, 원래 식에 x = 0을 넣으면 {pn(a)}² {sgn(b)} × {pn(a)} {sgn(c)} = {ans}{ro(ans)} 같다. 따라서 pq = {ans}이다.",
        sol3_fig=steps(["x = 0 대입: 두 식 모두 {ans}", "pq = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x {sgn(a)} = t로 놓으면 t² {sgt(b)}t {sgn(c)} = (t {sgn(r)})(t {sgn(s)})이고, t = x {sgn(a)}{eul(a)} 되돌리면 (x {sgn(p)})(x {sgn(q)})이다. 따라서 pq = {ans}이다.",
        rubric=[
            {"element": "치환·인수분해", "points": 2, "criterion": "x {sgn(a)} = t로 놓아 (t {sgn(r)})(t {sgn(s)}){eul(s)} 얻었다.", "partial": "치환 없이 전개해 인수분해했어도 결과가 맞으면 인정한다."},
            {"element": "되돌리기", "points": 3, "criterion": "t를 되돌려 (x {sgn(p)})(x {sgn(q)}){ro(q)} 정리하고 pq = {ans}{eul(ans)} 구했다.", "partial": "괄호 안을 정리하지 않고 (x {sgn(a)} {sgn(r)})… 꼴로 두었으면 2점."},
        ],
        rubric_total=5,
    )


# t6 — 인수분해를 이용한 식의 값: x = c + √a, y = c − √a
def _fv_rows():
    out = {}
    for c in range(1, 6):
        for a in (2, 3, 5, 6, 7, 10, 11, 13):
            xy = c * c - a
            if xy == 0:
                continue
            xpy, xmyk = 2 * c, 2                                   # x + y = 2c, x − y = 2√a
            base = {"c": c, "a": a, "XPY": xpy, "XY": xy}
            out[f"s{c}-{a}"] = {**base, "ASKQ": "x² + 2xy + y²의 값", "FAC": "(x + y)²", "FACV": f"(x + y)² = {xpy}² = {xpy * xpy}", "ans": xpy * xpy, "KIND": "완전제곱식", "USE": "x + y"}
            out[f"d{c}-{a}"] = {**base, "ASKQ": f"x² − y² = k[[sqrt({a})]]일 때, 상수 k의 값", "FAC": "(x + y)(x − y)", "FACV": f"(x + y)(x − y) = {xpy} × 2[[sqrt({a})]] = {2 * xpy}[[sqrt({a})]]", "ans": 2 * xpy, "KIND": "합차 공식", "USE": "x + y, x − y"}
            out[f"m{c}-{a}"] = {**base, "ASKQ": f"x²y − xy² = k[[sqrt({a})]]일 때, 상수 k의 값", "FAC": "xy(x − y)", "FACV": f"xy(x − y) = {_pn(xy)} × 2[[sqrt({a})]] = {2 * xy}[[sqrt({a})]]", "ans": 2 * xy, "KIND": "공통인수 xy", "USE": "xy, x − y"}
    return out


FV_ROWS = _fv_rows()


def fa_t6():
    return tpl(FA, 6, FA_BASE,
        title="인수분해를 이용한 식의 값 — x = c + √a, y = c − √a",
        skill="식을 먼저 인수분해해 x + y, x − y, xy의 값만으로 계산하기",
        variant_axis={"c": "1~5", "a": "2~13", "식": "(x + y)² / (x + y)(x − y) / xy(x − y)"},
        difficulty=3,
        discriminates="무리수를 직접 대입하지 않고 인수분해한 뒤 x + y = 2c, x − y = 2√a, xy = c² − a를 쓰는가",
        params=[{"name": "f", "values": {"in": list(FV_ROWS)}}],
        table={"key": "f", "rows": FV_ROWS},
        constraints=["ans != 0", "ans not in (c, a)"],
        cost_values=["c", "a", "XPY", "XY", "ans"],
        answer_var="ans",
        verify=["XPY == 2*c", "XY == c*c - a"],
        question="x = {c} + [[sqrt({a})]], y = {c} − [[sqrt({a})]]일 때, {ASKQ}을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x, y를 그대로 대입하면 계산이 번거롭다. 먼저 식을 {KIND}로 인수분해하면 {FAC}{ika(FAC)} 되고, x + y = {XPY}, x − y = 2[[sqrt({a})]], xy = {XY}처럼 간단한 값만 필요하다.",
        sol2=[
            "x + y = {XPY}, x − y = 2[[sqrt({a})]], xy = {XY}",
            "인수분해: {FAC}",
            "{FACV}이므로 답은 {ans}",
        ],
        sol2_fig=steps([
            {"text": "x + y = {XPY},  x − y = 2[[sqrt({a})]],  xy = {XY}", "hint": "먼저 준비"},
            {"text": "{FAC}", "hint": "{KIND}", "marks": [{"on": "{FAC}", "note": "{USE} 사용"}]},
            {"text": "{FACV}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="x + y = ({c} + [[sqrt({a})]]) + ({c} − [[sqrt({a})]]) = {XPY}, x − y = 2[[sqrt({a})]], xy = {c}² − ([[sqrt({a})]])² = {XY}{ika(XY)} 맞는지 확인하면 {FACV}이다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["xy = {c}² − {a} = {XY}", "{FACV}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x + y = {XPY}, x − y = 2[[sqrt({a})]], xy = {XY}이고 식을 인수분해하면 {FAC}이므로 {FACV}이다. 따라서 답은 {ans}이다.",
        rubric=[
            {"element": "인수분해·값 준비", "points": 3, "criterion": "{FAC}{ro(FAC)} 인수분해하고 {USE}의 값을 구했다.", "partial": "직접 대입해 바르게 계산했어도 인정한다."},
            {"element": "계산", "points": 2, "criterion": "{ans}{eul(ans)} 구했다.", "partial": "√{a}의 계수와 유리수 부분을 혼동했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t7 — 도형: 넓이 x² + bx + c, 가로 x + p → 세로 x + q
def fa_t7():
    return tpl(FA, 7, {**FA_BASE, "context": "기하맥락", "process": "문제해결"},
        title="넓이가 이차식인 직사각형의 다른 변 — 인수분해",
        skill="넓이 = 가로 × 세로이므로 넓이를 인수분해해 주어진 변을 인수로 갖는 다른 인수 찾기",
        variant_axis={"p, q": "1~9"},
        difficulty=2,
        discriminates="넓이를 인수분해해 두 일차식의 곱으로 보고, 주어진 변이 아닌 나머지 인수를 답하는가",
        params=[{"name": "p", "values": {"int": [1, 9]}}, {"name": "q", "values": {"int": [1, 9]}}],
        derive={"b": "p + q", "c": "p*q"},
        constraints=["p != q"],
        cost_values=["p", "q", "b", "c"],
        verify=["b == p + q", "c == p*q"],
        question="넓이가 x² + {b}x + {c}인 직사각형의 가로의 길이가 x + {p}일 때, 세로의 길이를 x를 사용한 식으로 나타내시오.",
        answer="x + {q}", answer_alt=[],
        sol1="직사각형의 넓이는 (가로) × (세로)이다. 넓이 x² + {b}x + {c}{eul(c)} 인수분해하면 두 일차식의 곱이 되고, 그중 하나가 가로 x + {p}이므로 나머지 인수가 세로의 길이이다. 곱이 {c}, 합이 {b}인 두 수 {p}, {q}를 찾는다.",
        sol2=[
            "x² + {b}x + {c} = (x + {p})(x + {q})",
            "(가로) × (세로) = (x + {p}) × (세로)이므로 세로 = x + {q}",
            "따라서 세로의 길이는 x + {q}",
        ],
        sol2_fig=steps([
            {"text": "x² + {b}x + {c} = (x + {p})(x + {q})", "hint": "곱 {c}, 합 {b}"},
            {"text": "가로 x + {p} → 세로 x + {q}", "hint": "나머지 인수", "marks": [{"on": "x + {q}", "note": "세로"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="(x + {p})(x + {q}) = x² + ({p} + {q})x + {p} × {q} = x² + {b}x + {c}{ro(c)} 넓이와 같다. 따라서 세로의 길이는 x + {q}이다.",
        sol3_fig=steps(["(x + {p})(x + {q}) = x² + {b}x + {c} ✓", "세로 = x + {q}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x² + {b}x + {c} = (x + {p})(x + {q})이고 가로가 x + {p}이므로 세로의 길이는 x + {q}이다.",
        rubric=[
            {"element": "인수분해", "points": 3, "criterion": "넓이를 (x + {p})(x + {q}){ro(q)} 인수분해했다.", "partial": "나눗셈으로 몫 x + {q}{eul(q)} 구했어도 인정한다."},
            {"element": "세로 구하기", "points": 2, "criterion": "세로의 길이 x + {q}{eul(q)} 답했다.", "partial": "가로 x + {p}{eul(p)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


FA_SEED = {
    "seed_id": FA, "category": "연산",
    "title": "인수분해 — 완전제곱식 조건·x² + bx + c·acx² + bx + c·공통인수·치환·식의 값·도형",
    "unit_id": "m3-1", "concept_ids": ["m3-1-11", "m3-1-12", "m3-1-13"],
    "schema_id": None, "schema_name": "인수분해 공식과 활용",
    "source_item_ids": [],
    "note": "인수분해 결과 자체는 답으로 묻지 않고(등가식 채점 문제) p − q·a + b + c + d·pq 같은 수치를 묻는다. 도형 틀만 일차식 답(x + q).",
    "geometry": False,
    "templates": [fa_t1(), fa_t2(), fa_t3(), fa_t4(), fa_t5(), fa_t6(), fa_t7()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 이차방정식의 풀이
QS = "m3-1-quad-solve"
QS_BASE = {**BASE, "prereq": ["인수분해", "제곱근"], "ops": ["이차방정식"], "traps": ["부호", "근 두 개"], "tags": ["이차방정식"]}
NZ9 = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]


# t1 — 인수분해로 풀기: x² + bx + c = 0 → x = q 또는 x = p
def qs_t1():
    return tpl(QS, 1, QS_BASE,
        title="인수분해를 이용한 이차방정식의 풀이 — x² + bx + c = 0",
        skill="좌변을 (x − p)(x − q)로 인수분해하고 AB = 0이면 A = 0 또는 B = 0임을 이용해 두 근 구하기",
        variant_axis={"두 근": "−9~9 (0 제외, 서로 다름)"},
        difficulty=2,
        discriminates="(x − p)(x − q) = 0에서 근이 p, q(부호 반대)임을 알고 두 근을 모두 쓰는가",
        params=[{"name": "p", "values": {"in": NZ9}}, {"name": "q", "values": {"in": NZ9}}],
        derive={"b": "-(p + q)", "c": "p*q", "np": "-p", "nq": "-q"},
        constraints=["p > q", "b != 0", "p not in (b, c)", "q not in (b, c)"],
        cost_values=["p", "q", "b", "c"],
        verify=["b == -(p + q)", "c == p*q"],
        question="이차방정식 x² {sgt(b)}x {sgn(c)} = 0을 푸시오.",
        answer="x = {q} 또는 x = {p}", answer_alt=["x = {p} 또는 x = {q}"],
        sol1="좌변을 인수분해한다: 곱이 {c}이고 합이 {b}인 두 정수 {np}, {nq}{eul(nq)} 찾으면 (x {sgn(np)})(x {sgn(nq)}) = 0이다. 두 식의 곱이 0이면 적어도 하나는 0이므로 x {sgn(np)} = 0 또는 x {sgn(nq)} = 0에서 근을 얻는다 — 괄호 안 부호와 근의 부호가 반대임에 주의한다.",
        sol2=[
            "x² {sgt(b)}x {sgn(c)} = (x {sgn(np)})(x {sgn(nq)}) = 0",
            "x {sgn(np)} = 0 또는 x {sgn(nq)} = 0",
            "따라서 x = {p} 또는 x = {q}",
        ],
        sol2_fig=steps([
            {"text": "(x {sgn(np)})(x {sgn(nq)}) = 0", "hint": "곱 {c}, 합 {b}"},
            {"text": "x {sgn(np)} = 0 또는 x {sgn(nq)} = 0", "hint": "AB = 0 → A = 0 또는 B = 0"},
            {"text": "x = {p} 또는 x = {q}", "marks": [{"on": "x = {p}", "note": "부호 반대"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="x = {p}{eul(p)} 대입하면 {pn(p)}² {sgn(b)} × {pn(p)} {sgn(c)} = 0, x = {q}{eul(q)} 대입해도 0이 되어 두 근 모두 맞다. 따라서 해는 x = {q} 또는 x = {p}이다.",
        sol3_fig=steps(["x = {p}, {q} 대입 → 0 ✓", "x = {q} 또는 x = {p}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x² {sgt(b)}x {sgn(c)} = (x {sgn(np)})(x {sgn(nq)}) = 0이므로 x {sgn(np)} = 0 또는 x {sgn(nq)} = 0이다. 따라서 x = {q} 또는 x = {p}이다.",
        rubric=[
            {"element": "인수분해", "points": 3, "criterion": "좌변을 (x {sgn(np)})(x {sgn(nq)}){ro(nq)} 인수분해했다.", "partial": "부호가 틀렸으면 1점."},
            {"element": "두 근", "points": 2, "criterion": "x = {q} 또는 x = {p}{eul(p)} 모두 구했다.", "partial": "한 근만 썼거나 부호를 반대로 썼으면 1점."},
        ],
        rubric_total=5,
    )


# t2 — 한 근이 주어질 때 상수와 다른 한 근: x² + ax + c = 0, 한 근 p → a, b(다른 근) → ab
def qs_t2():
    return tpl(QS, 2, QS_BASE,
        title="한 근이 주어진 이차방정식 — 상수 a와 다른 한 근 b의 곱",
        skill="주어진 근을 대입해 상수를 구하고, 다시 인수분해해 다른 한 근 찾기",
        variant_axis={"주어진 근": "±1~±9", "다른 근": "±1~±9"},
        difficulty=3,
        discriminates="근을 대입하면 등식이 성립함을 이용해 상수를 구하고, 구한 방정식을 다시 풀어 나머지 근을 찾는가",
        params=[{"name": "p", "values": {"in": NZ9}}, {"name": "q", "values": {"in": NZ9}}],
        derive={"c": "p*q", "A": "-(p + q)", "ans": "-(p + q)*q", "p2": "p*p", "Ap": "-(p + q)*p", "np": "-p", "nq": "-q"},
        constraints=["p != q", "A != 0", "ans not in (p, c)", "ans != 0"],
        cost_values=["p", "q", "c", "A", "ans"],
        answer_var="ans",
        verify=["ans == A*q", "p2 + A*p + c == 0", "q*q + A*q + c == 0"],
        question="이차방정식 x² + ax {sgn(c)} = 0의 한 근이 {p}일 때, 상수 a와 다른 한 근 b에 대하여 ab의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x = {p}{ika(p)} 근이므로 대입하면 등식이 성립한다: {pn(p)}² + {pn(p)}a {sgn(c)} = 0에서 a = {A}. 이제 x² {sgt(A)}x {sgn(c)} = 0을 인수분해해 두 근 {p}, {q}{eul(q)} 얻고, 주어진 근이 아닌 {q}{ika(q)} b이다.",
        sol2=[
            "x = {p} 대입: {p2} + {pn(p)}a {sgn(c)} = 0 → a = {A}",
            "x² {sgt(A)}x {sgn(c)} = (x {sgn(np)})(x {sgn(nq)}) = 0 → x = {p} 또는 x = {q}",
            "따라서 b = {q}, ab = {A} × {pn(q)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{p2} + {pn(p)}a {sgn(c)} = 0 → a = {A}", "hint": "근을 대입"},
            {"text": "(x {sgn(np)})(x {sgn(nq)}) = 0 → b = {q}", "hint": "다시 풀기", "marks": [{"on": "b = {q}", "note": "주어진 근이 아닌 쪽"}]},
            {"text": "ab = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="두 근 {p}, {q}의 합은 −a = {p} {sgn(q)} 이므로 a = {A}, 곱은 {c}{ro(c)} 상수항과 맞는다. 따라서 ab = {A} × {pn(q)} = {ans}이다.",
        sol3_fig=steps(["두 근의 곱 {p} × {pn(q)} = {c} ✓", "ab = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = {p}{eul(p)} 대입하면 {p2} + {pn(p)}a {sgn(c)} = 0이므로 a = {A}이다. x² {sgt(A)}x {sgn(c)} = (x {sgn(np)})(x {sgn(nq)}) = 0에서 다른 한 근은 b = {q}이므로 ab = {ans}이다.",
        rubric=[
            {"element": "상수 구하기", "points": 2, "criterion": "x = {p}{eul(p)} 대입해 a = {A}{eul(A)} 구했다.", "partial": "대입 계산 실수면 1점."},
            {"element": "다른 근·곱", "points": 3, "criterion": "다시 풀어 b = {q}{eul(q)} 구하고 ab = {ans}{eul(ans)} 답했다.", "partial": "주어진 근 {p}{eul(p)} b로 썼으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t3 — 제곱근을 이용한 풀이: A(x − p)² = M → x = p ± √k → p + k
def qs_t3():
    return tpl(QS, 3, QS_BASE,
        title="제곱근을 이용한 이차방정식의 풀이 — a(x − p)² = m의 해가 p ± √k",
        skill="양변을 a로 나누어 (x − p)² = k로 만들고 x − p = ±√k에서 x를 구하기",
        variant_axis={"a": "1~3", "p": "±1~±5", "k": "제곱인수 없는 2~23"},
        difficulty=2,
        discriminates="양변을 먼저 a로 나누는가, ±를 빠뜨리지 않고 p를 이항하는가",
        params=[{"name": "A", "values": {"int": [1, 3]}}, {"name": "p", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}}, {"name": "k", "values": {"in": SQF}}],
        derive={"M": "A*k", "np": "-p", "ans": "p + k"},
        constraints=["ans not in (A, p, k, M)", "ans != 0"],
        cost_values=["A", "p", "k", "M", "ans"],
        answer_var="ans",
        verify=["ans == p + k", "M == A*k"],
        question="이차방정식 {co(A)}(x {sgn(np)})² = {M}의 해가 x = a ± [[sqrt(b)]]일 때, 유리수 a와 가장 작은 자연수 b에 대하여 a + b의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="(x − p)² = k 꼴로 만들면 x − p는 k의 제곱근이므로 x − p = ±√k, 즉 x = p ± √k이다. 먼저 양변을 {A}{ro(A)} 나누어 (x {sgn(np)})² = {k}{eul(k)} 만든 뒤 ±[[sqrt({k})]]를 붙이고 {p}{eul(p)} 이항한다.",
        sol2=[
            "양변을 {A}{ro(A)} 나누면 (x {sgn(np)})² = {k}",
            "x {sgn(np)} = ±[[sqrt({k})]]",
            "x = {p} ± [[sqrt({k})]]이므로 a = {p}, b = {k}, a + b = {ans}",
        ],
        sol2_fig=steps([
            {"text": "(x {sgn(np)})² = {k}", "hint": "양변 ÷ {A}"},
            {"text": "x {sgn(np)} = ±[[sqrt({k})]]", "hint": "제곱근 — ± 둘 다", "marks": [{"on": "±[[sqrt({k})]]", "note": "두 근"}]},
            {"text": "x = {p} ± [[sqrt({k})]] → a + b = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="x = {p} + [[sqrt({k})]]{eul(k)} 넣으면 x {sgn(np)} = [[sqrt({k})]], 제곱하면 {k}, {A}배 하면 {M}{ro(M)} 우변과 같다. {k}에는 제곱인수가 없으므로 b = {k}이고 a + b = {ans}이다.",
        sol3_fig=steps(["{A} × ([[sqrt({k})]])² = {M} ✓", "a + b = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="양변을 {A}{ro(A)} 나누면 (x {sgn(np)})² = {k}이므로 x {sgn(np)} = ±[[sqrt({k})]], 즉 x = {p} ± [[sqrt({k})]]이다. 따라서 a = {p}, b = {k}이고 a + b = {ans}이다.",
        rubric=[
            {"element": "제곱근 취하기", "points": 3, "criterion": "(x {sgn(np)})² = {k}에서 x {sgn(np)} = ±[[sqrt({k})]]{eul(k)} 얻었다.", "partial": "±를 빠뜨렸으면 1점. 양변을 {A}{ro(A)} 나누지 않았으면 인정하지 않는다."},
            {"element": "해·답", "points": 2, "criterion": "x = {p} ± [[sqrt({k})]]{ro(k)} 정리해 a + b = {ans}{eul(ans)} 구했다.", "partial": "이항 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


# t4 — 완전제곱식으로 풀기: x² + 2mx + c = 0 → (x + m)² = D → x = −m ± √D → p + q
def qs_t4():
    return tpl(QS, 4, QS_BASE,
        title="완전제곱식을 이용한 이차방정식의 풀이 — 해가 p ± √q일 때 p + q",
        skill="상수항을 이항하고 (x의 계수의 반)²을 양변에 더해 (x + m)² = D 꼴로 만든 뒤 제곱근 취하기",
        variant_axis={"m": "±1~±6", "D": "제곱인수 없는 2~23"},
        difficulty=3,
        discriminates="양변에 같은 수(x의 계수의 반의 제곱)를 더해 완전제곱식을 만들고, ±√D에서 p, q를 바르게 읽는가",
        params=[{"name": "m", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}, {"name": "D", "values": {"in": SQF}}],
        derive={"b": "2*m", "c": "m*m - D", "m2": "m*m", "nc": "-(m*m - D)", "nm": "-m", "ans": "-m + D"},
        constraints=["c != 0", "ans not in (b, c, D)", "ans != 0"],
        cost_values=["m", "D", "b", "c", "m2", "ans"],
        answer_var="ans",
        verify=["ans == nm + D", "m2 - c == D", "b == 2*m"],
        question="이차방정식 x² {sgt(b)}x {sgn(c)} = 0을 완전제곱식을 이용하여 풀면 x = p ± [[sqrt(q)]]일 때, 유리수 p와 가장 작은 자연수 q에 대하여 p + q의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="좌변을 인수분해할 수 없으면 완전제곱식으로 만든다. 상수항 {c}{eul(c)} 우변으로 넘기고, x의 계수 {b}의 반 {m}{eul(m)} 제곱한 {m2}{eul(m2)} 양변에 더하면 좌변이 (x {sgn(m)})²이 된다. 그다음 제곱근을 취해 x = {nm} ± [[sqrt({D})]]{eul(D)} 얻는다.",
        sol2=[
            "x² {sgt(b)}x = {nc}",
            "양변에 {m2}{eul(m2)} 더하면 (x {sgn(m)})² = {nc} + {m2} = {D}",
            "x {sgn(m)} = ±[[sqrt({D})]]이므로 x = {nm} ± [[sqrt({D})]], p + q = {ans}",
        ],
        sol2_fig=steps([
            {"text": "x² {sgt(b)}x = {nc}", "hint": "상수항 이항"},
            {"text": "(x {sgn(m)})² = {D}", "hint": "양변 + {m2} = ({b} ÷ 2)²", "marks": [{"on": "{D}", "note": "{nc} + {m2}"}]},
            {"text": "x = {nm} ± [[sqrt({D})]] → p + q = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="(x {sgn(m)})² − {D}{eul(D)} 전개하면 x² {sgt(b)}x + {m2} − {D} = x² {sgt(b)}x {sgn(c)}{ro(c)} 원래 식과 같으므로 완전제곱식이 바르게 만들어졌다. 따라서 p = {nm}, q = {D}이고 p + q = {ans}이다.",
        sol3_fig=steps(["(x {sgn(m)})² − {D} = x² {sgt(b)}x {sgn(c)} ✓", "p + q = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x² {sgt(b)}x = {nc}의 양변에 {m2}{eul(m2)} 더하면 (x {sgn(m)})² = {D}이므로 x = {nm} ± [[sqrt({D})]]이다. 따라서 p = {nm}, q = {D}이고 p + q = {ans}이다.",
        rubric=[
            {"element": "완전제곱식 만들기", "points": 3, "criterion": "양변에 {m2}{eul(m2)} 더해 (x {sgn(m)})² = {D}{eul(D)} 얻었다.", "partial": "한쪽에만 더했으면 인정하지 않는다."},
            {"element": "해·답", "points": 2, "criterion": "x = {nm} ± [[sqrt({D})]]{ro(D)} 풀어 p + q = {ans}{eul(ans)} 구했다.", "partial": "±를 빠뜨렸으면 1점."},
        ],
        rubric_total=5,
    )


# t5 — 근의 공식: ax² + bx + c = 0 → 큰 근 (−b + √D)/(2a) → p + q + r (D 제곱인수 없음)
def _qf_rows():
    out = {}
    for a in (1, 2, 3):
        for b in range(-7, 8):
            if b == 0:
                continue
            for c in range(-6, 7):
                if c == 0:
                    continue
                D = b * b - 4 * a * c
                if D <= 1 or sqfree(D)[0] != 1:
                    continue
                if a == 1 and b % 2 == 0:
                    continue                                   # 완전제곱식이 자연스러운 경우는 t4 로
                out[f"{a}-{b}-{c}"] = {"a": a, "b": b, "c": c, "D": D, "nb": -b, "twoa": 2 * a, "b2": b * b, "fac": 4 * a * c, "nfac": -4 * a * c, "ans": -b + D + 2 * a,
                                       "ROOT": f"frac({-b} + sqrt({D}), {2 * a})", "ROOT2": f"frac({-b} − sqrt({D}), {2 * a})", "PM": f"frac(pm({-b}, sqrt({D})), {2 * a})"}
    return out


QF_ROWS = _qf_rows()


def qs_t5():
    return tpl(QS, 5, QS_BASE,
        title="근의 공식 — ax² + bx + c = 0의 큰 근이 (p + √q)/r일 때 p + q + r",
        skill="근의 공식 x = (−b ± √(b² − 4ac))/(2a)에 계수를 부호까지 정확히 대입하기",
        variant_axis={"a": "1~3", "b": "±1~±7", "c": "±1~±6 (판별식 제곱인수 없음)"},
        difficulty=3,
        discriminates="−b와 b² − 4ac의 부호(특히 c가 음수일 때 −4ac가 양수)를 정확히 대입하는가",
        params=[{"name": "f", "values": {"in": list(QF_ROWS)}}],
        table={"key": "f", "rows": QF_ROWS},
        constraints=["ans not in (a, b, c)", "ans != 0"],
        cost_values=["a", "b", "c", "D", "ans"],
        answer_var="ans",
        verify=["ans == nb + D + twoa", "D == b2 - fac"],
        question="이차방정식 {co(a)}x² {sgt(b)}x {sgn(c)} = 0의 두 근 중 큰 근이 [[frac(p + sqrt(q), r)]]일 때, 정수 p, r과 가장 작은 자연수 q에 대하여 p + q + r의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="근의 공식 x = [[frac(pm(-b, sqrt(pow(b,2) − 4*a*c)), 2*a)]]에 a = {a}, b = {b}, c = {c}{eul(c)} 대입한다. b² − 4ac = {b2} {sgn(nfac)} = {D}이고 {D}에는 제곱인수가 없으므로 q = {D}이며, 큰 근은 + 쪽인 [[{ROOT}]]이다.",
        sol2=[
            "a = {a}, b = {b}, c = {c}: b² = {b2}, 4ac = {fac}이므로 b² − 4ac = {b2} {sgn(nfac)} = {D}",
            "x = [[{PM}]]",
            "큰 근 [[{ROOT}]]에서 p = {nb}, q = {D}, r = {twoa}이므로 p + q + r = {ans}",
        ],
        sol2_fig=steps([
            {"text": "b² − 4ac = {b2} {sgn(nfac)} = {D}", "hint": "부호 주의"},
            {"text": "x = [[{PM}]]", "hint": "근의 공식", "marks": [{"on": "[[{PM}]]", "note": "−b = {nb}, 2a = {twoa}"}]},
            {"text": "p + q + r = {nb} + {D} + {twoa} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="분모 r = 2a = {twoa}{eun(twoa)} 양수이므로 √ 앞이 +인 [[{ROOT}]]{ika(twoa)} 큰 근이다. −b = {nb}, 판별식 {D}{eul(D)} 다시 확인하면 p + q + r = {ans}이다.",
        sol3_fig=steps(["큰 근 = [[{ROOT}]]", "p + q + r = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="근의 공식에서 x = [[{PM}]]이므로 큰 근은 [[{ROOT}]]이다. 따라서 p = {nb}, q = {D}, r = {twoa}이고 p + q + r = {ans}이다.",
        rubric=[
            {"element": "근의 공식 대입", "points": 3, "criterion": "b² − 4ac = {D}{eul(D)} 구해 x = [[{PM}]]{eul(twoa)} 얻었다.", "partial": "−4ac의 부호가 틀렸으면 인정하지 않는다."},
            {"element": "큰 근·답", "points": 2, "criterion": "큰 근 [[{ROOT}]]에서 p + q + r = {ans}{eul(ans)} 구했다.", "partial": "작은 근으로 답했으면 1점."},
        ],
        rubric_total=5,
    )


# t6 — 중근 조건 (□ 대신 k)
def _dr_rows():
    out = {}
    for p in (1, 2, 3, 4, 5):
        A = "x" if p == 1 else f"{p}x"
        lead = "" if p == 1 else str(p * p)
        for q in range(1, 10):
            for sg in ("+", "−"):
                out[f"c{p}-{q}-{sg}"] = {"EQ": f"{lead}x² {sg} {2 * p * q}x + k = 0", "ASK": "상수 k", "ans": q * q, "A": A, "B": str(q), "SQ": f"({A} {sg} {q})² = 0",
                                         "STEP": f"{lead}x² {sg} {2 * p * q}x + k = ({A})² {sg} 2 × {A} × {q} + k이므로 k = {q}² = {q * q}", "ROOT": f"x = {'-' if sg == '+' else ''}{q}" if p == 1 else f"x = {'-' if sg == '+' else ''}[[frac({q}, {p})]]"}
            out[f"k{p}-{q}"] = {"EQ": f"{lead}x² + kx + {q * q} = 0", "ASK": "양수 k", "ans": 2 * p * q, "A": A, "B": str(q), "SQ": f"({A} + {q})² = 0",
                                "STEP": f"{lead}x² + kx + {q * q} = ({A})² + kx + {q}²이므로 kx = 2 × {A} × {q} = {2 * p * q}x, 즉 k = {2 * p * q}", "ROOT": f"x = -{q}" if p == 1 else f"x = -[[frac({q}, {p})]]"}
    return out


DR_ROWS = _dr_rows()


def qs_t6():
    return tpl(QS, 6, QS_BASE,
        title="이차방정식이 중근을 가질 조건 — 상수 k",
        skill="중근을 가지려면 좌변이 완전제곱식이어야 함을 이용해 상수 정하기",
        variant_axis={"이차항": "x²·4x²·9x²", "빈 자리": "상수항 / x의 계수(양수)"},
        difficulty=2,
        discriminates="중근 ⇔ (완전제곱식) = 0임을 알고 상수항은 B², x의 계수는 2AB로 맞추는가",
        params=[{"name": "f", "values": {"in": list(DR_ROWS)}}],
        table={"key": "f", "rows": DR_ROWS},
        cost_values=["ans"],
        answer_var="ans",
        verify=["ans > 0"],
        question="이차방정식 {EQ}이 중근을 가질 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="이차방정식이 중근(서로 같은 두 근)을 가지려면 좌변이 완전제곱식 (A ± B)² 꼴이어야 한다. (A ± B)² = A² ± 2AB + B²에서 A = {A}, B = {B}{ro(B)} 놓고 비어 있는 자리를 맞춘다.",
        sol2=[
            "중근 ⇔ 좌변이 완전제곱식",
            "{STEP}",
            "이때 {SQ}에서 중근 {ROOT}",
        ],
        sol2_fig=steps([
            {"text": "A = {A}, B = {B}", "hint": "(A ± B)² = A² ± 2AB + B²"},
            {"text": "k = {ans}", "hint": "완전제곱식 조건", "marks": [{"on": "{ans}", "note": "k"}]},
            {"text": "{SQ}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="k = {ans}{eul(ans)} 넣으면 좌변이 {SQ}의 꼴로 완전제곱식이 되어 근이 {ROOT} 하나(중근)뿐이다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{SQ} → 중근 {ROOT}", "k = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="중근을 가지려면 좌변이 완전제곱식이어야 한다. {STEP}이다.",
        rubric=[
            {"element": "중근 조건", "points": 2, "criterion": "좌변이 완전제곱식이어야 함을 밝혔다.", "partial": "b² − 4ac = 0을 썼어도 인정한다."},
            {"element": "k 구하기", "points": 3, "criterion": "k = {ans}{eul(ans)} 구했다.", "partial": "2AB의 2배를 빠뜨렸으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t7 — 근의 개수에 따른 k 의 범위: ax² + bx + k = 0
CND_ROWS = {
    "two": {"COND": "서로 다른 두 근을 가질", "OP": "<", "DC": "> 0", "NAME": "서로 다른 두 근"},
    "none": {"COND": "근을 갖지 않을", "OP": ">", "DC": "< 0", "NAME": "근 없음"},
    "any": {"COND": "근을 가질", "OP": "≤", "DC": "≥ 0", "NAME": "근 있음(중근 포함)"},
}


def qs_t7():
    return tpl(QS, 7, QS_BASE,
        title="근의 개수에 따른 상수 k의 값의 범위 — ax² + bx + k = 0",
        skill="b² − 4ac의 부호로 근의 개수가 정해짐을 이용해 k의 부등식을 풀기",
        variant_axis={"a": "1~3", "b": "±2am (m = 1~5)", "조건": "서로 다른 두 근 / 근 없음 / 근 있음"},
        difficulty=3,
        discriminates="판별식 b² − 4ak의 부호 조건을 세우고, 4a로 나눌 때 부등호 방향을 지키며, 중근 포함 여부(≤)를 가리는가",
        params=[{"name": "a", "values": {"int": [1, 3]}}, {"name": "m", "values": {"int": [1, 5]}}, {"name": "sg", "values": {"in": [1, -1]}}, {"name": "v", "values": {"in": ["two", "none", "any"]}}],
        table={"key": "v", "rows": CND_ROWS},
        derive={"b": "2*a*m*sg", "b2": "4*a*a*m*m", "foura": "4*a", "T": "a*m*m"},
        constraints=["T != b2"],
        cost_values=["a", "b", "b2", "foura", "T"],
        verify=["b2 == b*b", "foura*T == b2"],
        question="이차방정식 {co(a)}x² {sgt(b)}x + k = 0이 {COND} 때, 상수 k의 값의 범위를 구하시오.",
        answer="k {OP} {T}", answer_alt=[],
        sol1="ax² + bx + c = 0의 근의 개수는 b² − 4ac의 부호로 정해진다: 양수면 서로 다른 두 근, 0이면 중근, 음수면 근이 없다. 여기서는 a = {a}, b = {b}, c = k이므로 b² − 4ac = {b2} − {foura}k이고, 따라서 조건 '{NAME}'에 맞게 {b2} − {foura}k {DC}{eul(DC)} 풀면 된다.",
        sol2=[
            "b² − 4ac = {b2} − {foura}k",
            "{NAME}: {b2} − {foura}k {DC}",
            "{foura}k{ro(foura)} 정리하면 k {OP} {T}",
        ],
        sol2_fig=steps([
            {"text": "{b2} − {foura}k {DC}", "hint": "{NAME}"},
            {"text": "k {OP} {T}", "hint": "{foura}로 나눔 — 부등호 방향", "marks": [{"on": "{OP}", "note": "음수로 나누면 방향 반대"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="k = {T}이면 b² − 4ac = 0이 되어 중근을 갖는 경계이다. 그보다 k가 작으면 b² − 4ac > 0(두 근), 크면 < 0(근 없음)이므로 조건에 맞는 범위는 k {OP} {T}이다.",
        sol3_fig=steps(["경계 k = {T} (중근)", "k {OP} {T}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="b² − 4ac = {b2} − {foura}k이고 {NAME}이려면 {b2} − {foura}k {DC}이어야 하므로 k {OP} {T}이다.",
        rubric=[
            {"element": "판별식 조건", "points": 3, "criterion": "{b2} − {foura}k {DC}{eul(DC)} 세웠다.", "partial": "부등호(등호 포함 여부)가 틀렸으면 1점."},
            {"element": "범위", "points": 2, "criterion": "k {OP} {T}{eul(T)} 구했다.", "partial": "부등호 방향이 반대면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t8 — 잘못 본 방정식
def _wr_rows():
    import itertools
    out = {}
    vals = [v for v in range(-6, 7) if v != 0]
    for r, s in itertools.combinations(vals, 2):        # r < s: 바른 두 근
        S, P = r + s, r * s
        if S == 0:
            continue
        A = [(p, q) for p in range(-9, 10) for q in range(p + 1, 10) if p and q and p + q == S and p * q != P and r not in (p, q) and s not in (p, q)]
        B = [(u, v) for u in range(-9, 10) for v in range(u + 1, 10) if u and v and u * v == P and u + v != S and r not in (u, v) and s not in (u, v)]
        if not A or not B:
            continue
        for i, ((p, q), (u, v)) in enumerate(zip(A[: 2], B[: 2])):
            out[f"{r}_{s}_{i}"] = {"r": r, "s": s, "p": p, "q": q, "u": u, "v": v, "S": S, "P": P, "nS": -S}
    return out


WR_ROWS = _wr_rows()


def qs_t8():
    return tpl(QS, 8, QS_BASE,
        title="잘못 본 이차방정식 — 상수항·x의 계수를 잘못 보고 푼 두 결과로 바른 해 구하기",
        skill="상수항을 잘못 보면 x의 계수(두 근의 합)는 바르고, x의 계수를 잘못 보면 상수항(두 근의 곱)은 바르다는 점을 이용하기",
        variant_axis={"바른 두 근": "−6~6"},
        difficulty=3,
        discriminates="각 사람이 바르게 본 계수가 무엇인지 가려 두 근의 합·곱으로 원래 방정식을 복원하는가",
        params=[{"name": "f", "values": {"in": list(WR_ROWS)}}],
        table={"key": "f", "rows": WR_ROWS},
        derive={"nr": "-r", "ns": "-s"},
        cost_values=["r", "s", "p", "q", "u", "v", "S", "P"],
        verify=["p + q == S", "u*v == P", "r + s == S", "r*s == P"],
        question="이차방정식 x² + mx + n = 0을 푸는데, 지호는 상수항 n을 잘못 보고 풀어 x = {p} 또는 x = {q}를 얻었고, 수아는 x의 계수 m을 잘못 보고 풀어 x = {u} 또는 x = {v}를 얻었다. 이 이차방정식의 바른 해를 구하시오.",
        answer="x = {r} 또는 x = {s}", answer_alt=["x = {s} 또는 x = {r}"],
        sol1="x² + mx + n = (x − α)(x − β) = x² − (α + β)x + αβ이므로 m = −(두 근의 합), n = (두 근의 곱)이다. 지호는 상수항만 잘못 봤으니 지호의 두 근으로 m이, 수아는 x의 계수만 잘못 봤으니 수아의 두 근으로 n이 바르게 정해진다.",
        sol2=[
            "지호(m은 바름): m = −({p} {sgn(q)}) = {nS}",
            "수아(n은 바름): n = {pn(u)} × {pn(v)} = {P}",
            "x² {sgt(nS)}x {sgn(P)} = 0 → (x {sgn(nr)})(x {sgn(ns)}) = 0 → x = {r} 또는 x = {s}",
        ],
        sol2_fig=steps([
            {"text": "m = −({p} {sgn(q)}) = {nS}", "hint": "지호의 근 → 합"},
            {"text": "n = {pn(u)} × {pn(v)} = {P}", "hint": "수아의 근 → 곱"},
            {"text": "x² {sgt(nS)}x {sgn(P)} = 0 → x = {r} 또는 x = {s}", "marks": [{"on": "x = {r} 또는 x = {s}", "note": "바른 해"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="바른 두 근 {r}, {s}의 합 {S}{eun(S)} 지호의 두 근의 합 {p} {sgn(q)} = {S}{wa(S)} 같고, 곱 {P}{eun(P)} 수아의 두 근의 곱 {pn(u)} × {pn(v)} = {P}{wa(P)} 같다. 따라서 바른 해는 x = {r} 또는 x = {s}이다.",
        sol3_fig=steps(["합 {S} ✓, 곱 {P} ✓", "x = {r} 또는 x = {s}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="지호의 두 근에서 m = −({p} {sgn(q)}) = {nS}, 수아의 두 근에서 n = {pn(u)} × {pn(v)} = {P}이므로 원래 방정식은 x² {sgt(nS)}x {sgn(P)} = 0이다. 인수분해하면 (x {sgn(nr)})(x {sgn(ns)}) = 0이므로 x = {r} 또는 x = {s}이다.",
        rubric=[
            {"element": "m, n 복원", "points": 3, "criterion": "m = {nS}, n = {P}{eul(P)} 바르게 정했다.", "partial": "두 사람의 역할을 바꿔 잡았으면 인정하지 않는다."},
            {"element": "바른 해", "points": 2, "criterion": "x² {sgt(nS)}x {sgn(P)} = 0을 풀어 x = {r} 또는 x = {s}{eul(s)} 구했다.", "partial": "한 근만 썼으면 1점."},
        ],
        rubric_total=5,
    )


QS_SEED = {
    "seed_id": QS, "category": "연산",
    "title": "이차방정식의 풀이 — 인수분해·한 근→상수·제곱근·완전제곱식·근의 공식·중근·근의 개수·잘못 본 방정식",
    "unit_id": "m3-1", "concept_ids": ["m3-1-14", "m3-1-15", "m3-1-16", "m3-1-17", "m3-1-18", "m3-1-19"],
    "schema_id": None, "schema_name": "이차방정식의 풀이와 근의 판별",
    "source_item_ids": [],
    "note": "해가 둘인 답은 'x = q 또는 x = p'(set). 근의 공식 틀은 판별식이 제곱인수 없는 경우만 표로 추림. 범위 답은 'k < T' 문자열(answer_var 없음).",
    "geometry": False,
    "templates": [qs_t1(), qs_t2(), qs_t3(), qs_t4(), qs_t5(), qs_t6(), qs_t7(), qs_t8()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 이차방정식의 활용
QA = "m3-1-quad-apply"
QA_BASE = {**BASE, **COMMON_APPLY, "ops": ["이차방정식"], "prereq": ["이차방정식의 풀이", "식 세우기"], "traps": ["조건에 맞지 않는 근 버리기", "미지수 설정"], "tags": ["이차방정식의 활용"], "pool_target": 300}

ASK2_ROWS = {"big": {"ASK": "두 수 중 큰 수", "w": 1}, "small": {"ASK": "두 수 중 작은 수", "w": 0}}


# t1 — 연속한 두 자연수의 제곱의 합
def qa_t1():
    return tpl(QA, 1, QA_BASE,
        title="연속한 두 자연수의 제곱의 합 — 이차방정식 세우기",
        skill="두 수를 x, x + 1로 놓고 x² + (x + 1)² = S를 정리해 풀고 자연수인 근만 택하기",
        variant_axis={"작은 수": "2~60", "구하는 것": "큰 수 / 작은 수"},
        difficulty=2,
        discriminates="두 수를 x, x + 1로 놓고 식을 세워 정리하며, 음수 근을 버리는가",
        params=[{"name": "n", "values": {"int": [2, 60]}}, {"name": "ask", "values": {"in": ["big", "small"]}}],
        table={"key": "ask", "rows": ASK2_ROWS},
        derive={"n1": "n + 1", "S": "n*n + (n + 1)**2", "K": "(S - 1)/2", "n1p": "n + 1", "nn": "-(n + 1)", "ans": "n + w"},
        constraints=["ans not in (S,)"],
        cost_values=["n", "S", "K", "ans"],
        answer_var="ans",
        verify=["S == n*n + n1*n1", "2*K == S - 1", "ans == n + w"],
        question="연속한 두 자연수의 제곱의 합이 {S}일 때, {ASK}를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="작은 수를 x라 하면 큰 수는 x + 1이다. 제곱의 합 x² + (x + 1)² = {S}{eul(S)} 전개해 정리하면 2x² + 2x + 1 − {S} = 0, 양변을 2로 나누면 x² + x − {K} = 0이 되고, 인수분해해 x를 구한다. x는 자연수여야 하므로 음수 근은 버린다.",
        sol2=[
            "x² + (x + 1)² = {S} → 2x² + 2x + 1 = {S} → x² + x − {K} = 0",
            "(x − {n})(x + {n1}) = 0 → x = {n} 또는 x = {nn}",
            "x는 자연수이므로 x = {n}: 두 수는 {n}, {n1}이고 {ASK}는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "x² + (x + 1)² = {S}", "hint": "두 수: x, x + 1"},
            {"text": "x² + x − {K} = 0 → (x − {n})(x + {n1}) = 0", "hint": "정리 후 인수분해", "marks": [{"on": "(x − {n})", "note": "x = {n}"}]},
            {"text": "x = {n} (x = {nn} 버림) → {ASK} {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{n}² + {n1}² = {n*n} + {n1*n1} = {S}{ro(S)} 조건과 맞는다. x = {nn}{eun(nn)} 자연수가 아니므로 버린다. 따라서 {ASK}는 {ans}이다.",
        sol3_fig=steps(["{n}² + {n1}² = {S} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="작은 수를 x라 하면 x² + (x + 1)² = {S}, 즉 x² + x − {K} = 0이므로 (x − {n})(x + {n1}) = 0에서 x = {n} (x > 0). 따라서 두 수는 {n}, {n1}이고 {ASK}는 {ans}이다.",
        rubric=[
            {"element": "식 세우기", "points": 2, "criterion": "x² + (x + 1)² = {S}{eul(S)} 세웠다.", "partial": "두 수를 x, x + 2로 놓았으면 인정하지 않는다."},
            {"element": "풀이·답", "points": 3, "criterion": "x = {n}{eul(n)} 구하고 음수 근을 버려 {ans}{eul(ans)} 답했다.", "partial": "음수 근을 버리지 않고 둘 다 답했으면 2점."},
        ],
        rubric_total=5,
    )


# t2 — 차와 곱이 주어진 두 자연수
def qa_t2():
    return tpl(QA, 2, QA_BASE,
        title="차와 곱이 주어진 두 자연수",
        skill="큰 수를 x, 작은 수를 x − d로 놓고 x(x − d) = P를 풀어 자연수 근 택하기",
        variant_axis={"작은 수": "2~12", "차": "1~9"},
        difficulty=2,
        discriminates="두 수를 x, x − d로 놓아 곱의 식을 세우고, 조건에 맞는 근을 고르는가",
        params=[{"name": "a", "values": {"int": [2, 12]}}, {"name": "d", "values": {"int": [1, 9]}}, {"name": "ask", "values": {"in": ["big", "small"]}}],
        table={"key": "ask", "rows": ASK2_ROWS},
        derive={"b": "a + d", "P": "a*(a + d)", "na": "-a", "nd": "-d", "ans": "a + w*d"},
        constraints=["ans not in (d, P)"],
        cost_values=["a", "d", "b", "P", "ans"],
        answer_var="ans",
        verify=["P == a*b", "b - a == d", "ans == a + w*d"],
        question="차가 {d}이고 곱이 {P}인 두 자연수가 있다. {ASK}를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="큰 수를 x라 하면 작은 수는 x − {d}이다. 곱이 {P}이므로 x(x − {d}) = {P}, 정리하면 x² {sgt(nd)}x − {P} = 0이다. 인수분해하여 x를 구하되, 자연수라는 조건에 맞는 근만 택한다.",
        sol2=[
            "x(x − {d}) = {P} → x² {sgt(nd)}x − {P} = 0",
            "(x − {b})(x + {a}) = 0 → x = {b} 또는 x = {na}",
            "x는 자연수이므로 x = {b}: 두 수는 {b}, {a}이고 {ASK}는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "x(x − {d}) = {P}", "hint": "큰 수 x, 작은 수 x − {d}"},
            {"text": "(x − {b})(x + {a}) = 0", "hint": "x² {sgt(nd)}x − {P} = 0", "marks": [{"on": "(x − {b})", "note": "x = {b}"}]},
            {"text": "x = {b} (x = {na} 버림) → {ASK} {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{b} − {a} = {d}, {b} × {a} = {P}{ro(P)} 두 조건을 모두 만족한다. x = {na}{eun(na)} 자연수가 아니므로 버린다. 따라서 {ASK}는 {ans}이다.",
        sol3_fig=steps(["{b} − {a} = {d} ✓, {b} × {a} = {P} ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="큰 수를 x라 하면 x(x − {d}) = {P}, 즉 x² {sgt(nd)}x − {P} = 0이므로 (x − {b})(x + {a}) = 0에서 x = {b} (x > 0). 따라서 두 수는 {b}, {a}이고 {ASK}는 {ans}이다.",
        rubric=[
            {"element": "식 세우기", "points": 2, "criterion": "x(x − {d}) = {P}{eul(P)} 세웠다.", "partial": "작은 수를 x로 놓아 x(x + {d}) = {P}{eul(P)} 세웠어도 인정한다."},
            {"element": "풀이·답", "points": 3, "criterion": "이차방정식을 풀어 {ans}{eul(ans)} 답했다.", "partial": "음수 근을 버리지 않았으면 2점."},
        ],
        rubric_total=5,
    )


# t3 — 나누어 주기(학생 수)
NAME_ROWS = {
    "candy": {"OBJ": "사탕", "CNT": "개"}, "pencil": {"OBJ": "연필", "CNT": "자루"}, "marble": {"OBJ": "구슬", "CNT": "개"}, "book": {"OBJ": "공책", "CNT": "권"},
}
DIRQ_ROWS = {"less": {"DIR": "적었다", "DIRC": "적어", "SGX": "−", "w": 0}, "more": {"DIR": "많았다", "DIRC": "많아", "SGX": "+", "w": 1}}


def qa_t3():
    return tpl(QA, 3, QA_BASE,
        title="똑같이 나누어 주기 — 한 사람이 받는 개수가 사람 수보다 d만큼 많거나 적을 때",
        skill="사람 수를 x로 놓고 (사람 수) × (한 사람의 개수) = (전체 개수)로 이차방정식 세우기",
        variant_axis={"사람 수": "3~15", "차": "1~6", "많게/적게": "2가지", "물건": "4가지"},
        difficulty=3,
        discriminates="한 사람이 받는 개수를 x ± d로 표현하고 곱이 전체 개수임을 식으로 세우는가",
        params=[{"name": "x0", "values": {"int": [3, 15]}}, {"name": "d", "values": {"int": [1, 6]}}, {"name": "nm", "values": {"in": list(NAME_ROWS)}}, {"name": "dr", "values": {"in": ["less", "more"]}}],
        table=[{"key": "nm", "rows": NAME_ROWS}, {"key": "dr", "rows": DIRQ_ROWS}],
        derive={"each": "x0 + (2*w - 1)*d", "P": "x0*(x0 + (2*w - 1)*d)", "sd": "(2*w - 1)*d", "ans": "x0"},
        constraints=["each >= 2", "ans not in (d, P)"],
        cost_values=["x0", "d", "each", "P", "ans"],
        answer_var="ans",
        verify=["P == x0*each", "ans == x0"],
        question="{OBJ} {P}{CNT}를 학생들에게 남김없이 똑같이 나누어 주었더니 한 학생이 받은 {OBJ}의 수가 학생 수보다 {d}만큼 {DIR}. 학생 수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="학생 수를 x명이라 하면 한 학생이 받는 {OBJ}의 수는 (x {SGX} {d}){CNT}이다. (학생 수) × (한 학생이 받는 수) = (전체 수)이므로 x(x {SGX} {d}) = {P}이고, 이를 풀어 자연수인 x를 택한다.",
        sol2=[
            "x(x {SGX} {d}) = {P} → x² {sgt(sd)}x − {P} = 0",
            "(x − {x0})(x + {each}) = 0 → x = {x0} 또는 x = −{each}",
            "x는 자연수이므로 학생 수는 {x0}명 (한 학생이 {each}{CNT}씩)",
        ],
        sol2_fig=steps([
            {"text": "x(x {SGX} {d}) = {P}", "hint": "학생 수 x, 한 명당 x {SGX} {d}"},
            {"text": "(x − {x0})(x + {each}) = 0 → x = {x0}", "hint": "자연수 근", "marks": [{"on": "x = {x0}", "note": "학생 수"}]},
            {"text": "{x0} × {each} = {P} ✓"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="학생 {x0}명이 {each}{CNT}씩 받으면 {x0} × {each} = {P}{ro(P)} 전체와 같고, {each}{eun(each)} {x0}보다 {d}만큼 {DIRC} 조건에 맞는다. x = −{each}{eun(each)} 학생 수가 될 수 없다. 따라서 학생 수는 {ans}명이다.",
        sol3_fig=steps(["{x0} × {each} = {P} ✓", "학생 수 {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="학생 수를 x라 하면 한 학생이 받는 수는 x {SGX} {d}이므로 x(x {SGX} {d}) = {P}이다. (x − {x0})(x + {each}) = 0에서 x = {x0} (x > 0)이므로 학생 수는 {ans}명이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "x(x {SGX} {d}) = {P}{eul(P)} 세웠다.", "partial": "부호(많게/적게)를 반대로 썼으면 1점."},
            {"element": "풀이·답", "points": 2, "criterion": "x = {x0}{eul(x0)} 구해 학생 수 {ans}{eul(ans)} 답했다.", "partial": "한 학생이 받는 개수를 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t4 — 직사각형: 가로가 세로보다 d 긴, 넓이 P
def qa_t4():
    return tpl(QA, 4, {**QA_BASE, "context": "기하맥락"},
        title="가로가 세로보다 d cm 긴 직사각형의 넓이 — 변의 길이",
        skill="세로를 x로 놓고 x(x + d) = S를 풀어 양수 근 택하기",
        variant_axis={"세로": "2~12", "차": "1~9", "구하는 것": "세로 / 가로"},
        difficulty=2,
        discriminates="변의 길이는 양수라는 조건으로 근을 고르고, 묻는 변(가로/세로)을 구별하는가",
        params=[{"name": "a", "values": {"int": [2, 12]}}, {"name": "d", "values": {"int": [1, 9]}}, {"name": "ask", "values": {"in": ["v", "h"]}}],
        table={"key": "ask", "rows": {"v": {"ASK": "세로의 길이", "w": 0}, "h": {"ASK": "가로의 길이", "w": 1}}},
        derive={"b": "a + d", "S": "a*(a + d)", "nb": "-(a + d)", "ans": "a + w*d"},
        constraints=["ans not in (d, S)"],
        cost_values=["a", "d", "b", "S", "ans"],
        answer_var="ans",
        verify=["S == a*b", "b == a + d"],
        question="가로의 길이가 세로의 길이보다 {d} cm 긴 직사각형의 넓이가 {S} cm²일 때, 이 직사각형의 {ASK}를 구하시오.",
        answer="{ans}", answer_alt=["{ans} cm"],
        sol1="세로의 길이를 x cm라 하면 가로는 (x + {d}) cm이다. 넓이 = 가로 × 세로이므로 x(x + {d}) = {S}, 즉 x² {sgt(d)}x − {S} = 0을 풀고, 길이는 양수이므로 양수 근만 택한다.",
        sol2=[
            "x(x + {d}) = {S} → x² {sgt(d)}x − {S} = 0",
            "(x − {a})(x + {b}) = 0 → x = {a} 또는 x = {nb}",
            "x > 0이므로 세로 {a} cm, 가로 {b} cm → {ASK}는 {ans} cm",
        ],
        sol2_fig=steps([
            {"text": "x(x + {d}) = {S}", "hint": "세로 x, 가로 x + {d}"},
            {"text": "(x − {a})(x + {b}) = 0", "hint": "x² {sgt(d)}x − {S} = 0", "marks": [{"on": "(x − {a})", "note": "x = {a}"}]},
            {"text": "세로 {a}, 가로 {b} → {ASK} {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="세로 {a} cm, 가로 {b} cm이면 {b} − {a} = {d}, {a} × {b} = {S}{ro(S)} 조건과 맞는다. x = {nb}{eun(nb)} 길이가 될 수 없다. 따라서 {ASK}는 {ans} cm이다.",
        sol3_fig=steps(["{a} × {b} = {S} ✓", "{ASK} = {ans} cm"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="세로의 길이를 x cm라 하면 x(x + {d}) = {S}, 즉 x² {sgt(d)}x − {S} = 0이므로 (x − {a})(x + {b}) = 0에서 x = {a} (x > 0). 따라서 세로 {a} cm, 가로 {b} cm이고 {ASK}는 {ans} cm이다.",
        rubric=[
            {"element": "식 세우기", "points": 2, "criterion": "x(x + {d}) = {S}{eul(S)} 세웠다.", "partial": "가로를 x로 놓아 x(x − {d}) = {S}{eul(S)} 세웠어도 인정한다."},
            {"element": "풀이·답", "points": 3, "criterion": "양수 근을 택해 {ASK} {ans} cm를 답했다.", "partial": "가로·세로를 바꿔 답했으면 1점."},
        ],
        rubric_total=5,
    )


# t5 — 정사각형 한 변 늘리기
def qa_t5():
    return tpl(QA, 5, {**QA_BASE, "context": "기하맥락"},
        title="정사각형의 한 변을 늘였을 때의 넓이 — 처음 한 변의 길이",
        skill="처음 한 변을 x로 놓고 (x + d)² = S에서 제곱근을 이용해 양수 근 택하기",
        variant_axis={"처음 한 변": "2~12", "늘인 길이": "1~8"},
        difficulty=2,
        discriminates="(x + d)² = S를 제곱근으로 풀고 x + d > 0인 근만 택하는가",
        params=[{"name": "a", "values": {"int": [2, 12]}}, {"name": "d", "values": {"int": [1, 8]}}],
        derive={"b": "a + d", "S": "(a + d)**2", "nb": "-(a + d)", "nbd": "-(a + d) - d", "ans": "a"},
        constraints=["ans not in (d, S)"],
        cost_values=["a", "d", "b", "S", "ans"],
        answer_var="ans",
        verify=["S == b*b", "b == a + d"],
        question="정사각형의 각 변의 길이를 {d} cm씩 늘였더니 넓이가 {S} cm²인 정사각형이 되었다. 처음 정사각형의 한 변의 길이를 구하시오.",
        answer="{ans}", answer_alt=["{ans} cm"],
        sol1="처음 한 변을 x cm라 하면 늘인 정사각형의 한 변은 (x + {d}) cm이고 넓이는 (x + {d})²이다. (x + {d})² = {S}에서 x + {d}는 {S}의 제곱근이므로 x + {d} = ±{b}이고, 길이는 양수이므로 x + {d} = {b}를 택한다.",
        sol2=[
            "(x + {d})² = {S}",
            "x + {d} = ±[[sqrt({S})]] = ±{b}",
            "x + {d} > 0이므로 x + {d} = {b}, x = {ans}",
        ],
        sol2_fig=steps([
            {"text": "(x + {d})² = {S}", "hint": "늘인 변 x + {d}"},
            {"text": "x + {d} = ±{b}", "hint": "제곱근", "marks": [{"on": "±{b}", "note": "양수만"}]},
            {"text": "x = {b} − {d} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="처음 한 변 {a} cm를 {d} cm 늘이면 {b} cm이고 {b}² = {S}{ro(S)} 조건과 맞는다. x = {nbd}{eun(nbd)} 길이가 될 수 없다. 따라서 처음 한 변의 길이는 {ans} cm이다.",
        sol3_fig=steps(["({a} + {d})² = {b}² = {S} ✓", "처음 한 변 {ans} cm"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="처음 한 변을 x cm라 하면 (x + {d})² = {S}이므로 x + {d} = {b} (x + {d} > 0), 즉 x = {ans}이다. 따라서 처음 한 변의 길이는 {ans} cm이다.",
        rubric=[
            {"element": "식 세우기", "points": 2, "criterion": "(x + {d})² = {S}{eul(S)} 세웠다.", "partial": "전개해 x² + {2*d}x + {d*d} = {S}{ro(S)} 썼어도 인정한다."},
            {"element": "풀이·답", "points": 3, "criterion": "x + {d} = {b}에서 {ans} cm를 구했다.", "partial": "음수 근을 함께 답했으면 2점."},
        ],
        rubric_total=5,
    )


# t6 — 길 내기: (W − x)(H − x) = R
def qa_t6():
    return tpl(QA, 6, {**QA_BASE, "context": "기하맥락"},
        title="직사각형 땅에 폭이 일정한 길을 낼 때 — 길의 폭",
        skill="길을 한쪽으로 몰아 (가로 − x)(세로 − x) = (남은 넓이)로 식을 세우기",
        variant_axis={"폭": "1~5", "가로·세로": "폭 + 3~15"},
        difficulty=3,
        discriminates="가로·세로로 낸 길을 옮겨 붙여 (W − x)(H − x)로 남은 땅을 표현하고, 땅의 크기를 넘는 근을 버리는가",
        params=[{"name": "x0", "values": {"int": [1, 5]}}, {"name": "p", "values": {"int": [3, 15]}}, {"name": "q", "values": {"int": [3, 15]}}],
        derive={"W": "x0 + p", "H": "x0 + q", "R": "p*q", "WH": "(x0 + p) + (x0 + q)", "x2": "x0 + p + q", "K": "(x0 + p)*(x0 + q) - p*q", "ans": "x0"},
        constraints=["p <= q", "ans not in (W, H, R)", "W <= 20", "H <= 20"],
        cost_values=["x0", "W", "H", "R", "WH", "K", "x2", "ans"],
        answer_var="ans",
        verify=["(W - x0)*(H - x0) == R", "x2 == WH - x0", "K == W*H - R"],
        question="가로의 길이가 {W} m, 세로의 길이가 {H} m인 직사각형 모양의 땅에 폭이 일정한 길을 가로와 세로 방향으로 하나씩 내었더니 길을 제외한 땅의 넓이가 {R} m²가 되었다. 길의 폭을 구하시오.",
        answer="{ans}", answer_alt=["{ans} m"],
        sol1="길의 폭을 x m라 하자. 가로·세로 길을 각각 한쪽 가장자리로 옮겨 붙이면 남은 땅은 가로 ({W} − x) m, 세로 ({H} − x) m인 직사각형이 된다. 따라서 ({W} − x)({H} − x) = {R}{eul(R)} 풀고, x는 {W}보다 작은 양수여야 하므로 조건에 맞는 근을 택한다.",
        sol2=[
            "({W} − x)({H} − x) = {R} → x² − {WH}x + {K} = 0",
            "(x − {x0})(x − {x2}) = 0 → x = {x0} 또는 x = {x2}",
            "0 < x < {W}이므로 x = {ans}: 길의 폭은 {ans} m",
        ],
        sol2_fig=steps([
            {"text": "({W} − x)({H} − x) = {R}", "hint": "길을 가장자리로 옮기기"},
            {"text": "x² − {WH}x + {K} = 0 → (x − {x0})(x − {x2}) = 0", "hint": "인수분해", "marks": [{"on": "(x − {x0})", "note": "x = {x0}"}]},
            {"text": "x = {x2}{eun(x2)} 땅보다 큼 → x = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="폭이 {ans} m이면 남은 땅은 ({W} − {x0}) × ({H} − {x0}) = {p} × {q} = {R}{ro(R)} 조건과 맞는다. x = {x2}{eun(x2)} 가로 {W} m보다 커서 길을 낼 수 없다. 따라서 길의 폭은 {ans} m이다.",
        sol3_fig=steps(["{p} × {q} = {R} ✓", "길의 폭 {ans} m"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="길의 폭을 x m라 하면 ({W} − x)({H} − x) = {R}, 즉 x² − {WH}x + {K} = 0이므로 (x − {x0})(x − {x2}) = 0에서 x = {x0} (0 < x < {W}). 따라서 길의 폭은 {ans} m이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "({W} − x)({H} − x) = {R}{eul(R)} 세웠다.", "partial": "길의 넓이를 겹치는 부분 없이 {W}x + {H}x로 놓았으면 인정하지 않는다."},
            {"element": "풀이·답", "points": 2, "criterion": "x = {x0}{eul(x0)} 택해 길의 폭 {ans} m를 답했다.", "partial": "x = {x2}{eul(x2)} 버리지 않았으면 1점."},
        ],
        rubric_total=5,
    )


# t7 — 던져 올린 물체의 높이 h = vt − 5t²
ASKT_ROWS = {"first": {"ASKT": "처음으로", "w": 0}, "second": {"ASKT": "두 번째로", "w": 1}}


def qa_t7():
    return tpl(QA, 7, QA_BASE,
        title="던져 올린 물체의 높이 — 특정 높이가 되는 시각",
        skill="높이 식에 h를 대입해 t에 대한 이차방정식을 세우고 두 근이 각각 올라갈 때·내려올 때임을 해석하기",
        variant_axis={"두 시각": "1~9초", "구하는 것": "처음으로 / 두 번째로"},
        difficulty=3,
        discriminates="두 근이 모두 의미 있음(올라갈 때와 내려올 때)을 알고 묻는 시각을 고르는가",
        params=[{"name": "t1", "values": {"int": [1, 5]}}, {"name": "t2", "values": {"int": [2, 9]}}, {"name": "ask", "values": {"in": ["first", "second"]}}],
        table={"key": "ask", "rows": ASKT_ROWS},
        derive={"v": "5*(t1 + t2)", "Hh": "5*t1*t2", "s": "t1 + t2", "pr": "t1*t2", "ans": "t1 + w*(t2 - t1)"},
        constraints=["t2 > t1", "ans not in (v, Hh)"],
        cost_values=["t1", "t2", "v", "Hh", "ans"],
        answer_var="ans",
        verify=["v == 5*s", "Hh == 5*pr", "v*t1 - 5*t1*t1 == Hh", "v*t2 - 5*t2*t2 == Hh"],
        question="지면에서 초속 {v} m로 똑바로 위로 던져 올린 물체의 t초 후의 높이는 ({v}t − 5t²) m라고 한다. 이 물체의 높이가 {ASKT} {Hh} m가 되는 것은 던진 지 몇 초 후인지 구하시오.",
        answer="{ans}", answer_alt=["{ans}초"],
        sol1="높이가 {Hh} m가 되는 t를 구하려면 {v}t − 5t² = {Hh}{eul(Hh)} 풀면 된다. 정리하면 5t² − {v}t + {Hh} = 0, 양변을 5로 나누어 t² − {s}t + {pr} = 0이고, 두 근 중 작은 것은 올라갈 때, 큰 것은 내려올 때 그 높이를 지나는 시각이다.",
        sol2=[
            "{v}t − 5t² = {Hh} → 5t² − {v}t + {Hh} = 0 → t² − {s}t + {pr} = 0",
            "(t − {t1})(t − {t2}) = 0 → t = {t1} 또는 t = {t2}",
            "처음으로 {Hh} m가 되는 것은 {t1}초 후, 두 번째는 {t2}초 후 → 답 {ans}초",
        ],
        sol2_fig=steps([
            {"text": "t² − {s}t + {pr} = 0", "hint": "h = {Hh} 대입, ÷5"},
            {"text": "(t − {t1})(t − {t2}) = 0", "hint": "두 근 모두 의미 있음", "marks": [{"on": "(t − {t1})", "note": "올라갈 때"}, {"on": "(t − {t2})", "note": "내려올 때"}]},
            {"text": "{ASKT} → {ans}초"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0", "mark:1-1")], [reveal(2)]],
        sol3="t = {t1}일 때 {v} × {t1} − 5 × {t1}² = {Hh}, t = {t2}일 때도 {Hh}{ika(Hh)} 되어 두 시각 모두 높이가 {Hh} m이다. {ASKT} 그 높이가 되는 시각은 {ans}초 후이다.",
        sol3_fig=steps(["t = {t1}, {t2} 모두 h = {Hh} ✓", "{ASKT} → {ans}초"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{v}t − 5t² = {Hh}에서 t² − {s}t + {pr} = 0, (t − {t1})(t − {t2}) = 0이므로 t = {t1} 또는 t = {t2}이다. 따라서 {ASKT} {Hh} m가 되는 것은 {ans}초 후이다.",
        rubric=[
            {"element": "식 세우기·풀기", "points": 3, "criterion": "t² − {s}t + {pr} = 0을 풀어 t = {t1}, {t2}{eul(t2)} 구했다.", "partial": "한 근만 구했으면 1점."},
            {"element": "시각 해석", "points": 2, "criterion": "{ASKT} 그 높이가 되는 시각 {ans}초를 답했다.", "partial": "두 시각을 모두 답했으면 1점."},
        ],
        rubric_total=5,
    )


# t8 — 대각선의 개수 n(n − 3)/2 = D
def qa_t8():
    return tpl(QA, 8, {**QA_BASE, "context": "기하맥락"},
        title="대각선의 개수가 주어진 다각형 — 변의 개수",
        skill="n각형의 대각선의 개수 n(n − 3)/2 = D를 이차방정식으로 풀어 자연수 근 택하기",
        variant_axis={"n": "5~40", "묻는 것": "변의 개수 / 한 꼭짓점에서 그을 수 있는 대각선의 개수 / 내각의 크기의 합"},
        difficulty=2,
        discriminates="대각선 공식을 세우고 2를 곱해 정리한 뒤 n ≥ 3인 근을 고르는가",
        params=[{"name": "n", "values": {"int": [5, 40]}}, {"name": "k", "values": {"in": ["edge", "vert", "angle"]}}],
        table={"key": "k", "rows": {"edge": {"ASK": "변의 개수", "w1": 1, "w2": 0}, "vert": {"ASK": "한 꼭짓점에서 그을 수 있는 대각선의 개수", "w1": 0, "w2": 1}, "angle": {"ASK": "내각의 크기의 합(단위: °)", "w1": 0, "w2": 0}}},
        derive={"D": "n*(n - 3)/2", "D2": "n*(n - 3)", "nn": "-(n - 3)", "n3": "n - 3", "ans": "w1*n + w2*(n - 3) + (1 - w1 - w2)*180*(n - 2)"},
        constraints=["ans != D", "ans != n3 or w2 == 1"],
        cost_values=["n", "D", "D2", "ans"],
        answer_var="ans",
        verify=["2*D == n*(n - 3)", "D2 == 2*D"],
        question="대각선의 총 개수가 {D}인 다각형의 {ASK}를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="n각형의 대각선의 개수는 [[frac(n(n − 3), 2)]]이다. [[frac(n(n − 3), 2)]] = {D}에서 양변에 2를 곱하면 n(n − 3) = {D2}, 즉 n² − 3n − {D2} = 0이다. 인수분해하여 n을 구하고 n ≥ 3인 자연수만 택한다.",
        sol2=[
            "[[frac(n(n − 3), 2)]] = {D} → n(n − 3) = {D2} → n² − 3n − {D2} = 0",
            "(n − {n})(n + {n3}) = 0 → n = {n} 또는 n = {nn}",
            "n은 3 이상의 자연수이므로 n = {n}: {n}각형이고, {ASK}는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "n(n − 3) = {D2}", "hint": "대각선 공식 × 2"},
            {"text": "(n − {n})(n + {n3}) = 0", "hint": "n² − 3n − {D2} = 0", "marks": [{"on": "(n − {n})", "note": "n = {n}"}]},
            {"text": "{n}각형 → {ASK} {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="{n}각형의 대각선의 개수는 {n} × {n3} ÷ 2 = {D}{ro(D)} 조건과 맞는다. n = {nn}{eun(nn)} 다각형이 될 수 없다. {n}각형에서 한 꼭짓점에서 그을 수 있는 대각선은 {n3}개, 내각의 크기의 합은 180° × ({n} − 2)이다. 따라서 {ASK}는 {ans}이다.",
        sol3_fig=steps(["{n} × {n3} ÷ 2 = {D} ✓", "{ASK} {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="n각형의 대각선의 개수는 [[frac(n(n − 3), 2)]]이므로 n(n − 3) = {D2}, 즉 n² − 3n − {D2} = 0에서 (n − {n})(n + {n3}) = 0이므로 n = {n} (n ≥ 3). 따라서 {n}각형이고 {ASK}는 {ans}이다.",
        rubric=[
            {"element": "식 세우기", "points": 2, "criterion": "[[frac(n(n − 3), 2)]] = {D}{eul(D)} 세웠다.", "partial": "2로 나누는 것을 빠뜨렸으면 인정하지 않는다."},
            {"element": "풀이·답", "points": 3, "criterion": "n = {n}{eul(n)} 구해 {ASK} {ans}{eul(ans)} 답했다.", "partial": "음수 근을 버리지 않았으면 2점."},
        ],
        rubric_total=5,
    )


QA_SEED = {
    "seed_id": QA, "category": "활용",
    "title": "이차방정식의 활용 — 연속수·두 수·나누어 주기·직사각형·정사각형·길·물체·대각선",
    "unit_id": "m3-1", "concept_ids": ["m3-1-21"],
    "schema_id": None, "schema_name": "이차방정식의 활용",
    "source_item_ids": [],
    "note": "모든 틀에서 두 근 중 조건(자연수·양수·범위)에 맞는 근을 택하는 단계를 해설과 채점 기준에 넣었다. 물체 틀은 두 근이 모두 의미 있음.",
    "geometry": False,
    "templates": [qa_t1(), qa_t2(), qa_t3(), qa_t4(), qa_t5(), qa_t6(), qa_t7(), qa_t8()],
}


if __name__ == "__main__":
    for seed in (FA_SEED, QS_SEED, QA_SEED):
        with_pitfalls(seed)
        dump(seed)
