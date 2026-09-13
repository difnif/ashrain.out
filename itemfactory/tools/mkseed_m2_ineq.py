# itemfactory/tools/mkseed_m2_ineq.py — m2-1 부등식 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m2_ineq.py
#     → seeds/m2-1-ineq-property.json (부등식의 성질: 식의 값 범위 m+n·정수 개수·최댓값→상수·분수 계수, 4틀)
#     → seeds/m2-1-ineq-solve-2.json  (일차부등식 풀이 2: 분수 계수·소수 계수·자연수 해 개수→a 범위·해→상수(분수)·해가 같은 두 부등식, 5틀)
#     → seeds/m2-1-ineq-apply.json    (부등식 활용: 평균 점수·두 품목 최대 개수·상점 다녀오기·삼각형 넓이 범위·엘리베이터, 5틀)
#
# 부등호 방향(뒤집힘)은 파생값이 아니라 표 행이 정한다 — m2-1-ineq-solve 와 같은 방식. 해가 문자열인 틀(x > 3, 2 ≤ a < 3)은
# recheck.py 가 발문을 되읽어 대조한다.
from __future__ import annotations

import os
import sys
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import COMMON_APPLY, dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


BASE = {"process": "절차수행", "context": "무맥락", "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}
NZ6 = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
OPS4 = {"gt": (">", "<"), "ge": ("≥", "≤"), "lt": ("<", ">"), "le": ("≤", "≥")}      # 부등호 → 뒤집은 부등호


def sgn_rows(vals, key, var):
    """부호 붙은 항 조각(평문): 2 → '+ 2y', -1 → '− y'"""
    def f(v):
        a = abs(v)
        return ("+ " if v > 0 else "− ") + (var if a == 1 else f"{a}{var}")
    return {"key": key, "rows": {str(v): {f"{key.upper()}S": f(v)} for v in vals}}


# ═══════════════════════════════════════════════════════════════════ 1. 부등식의 성질
IP = "m2-1-ineq-property"
IP_BASE = {**BASE, "prereq": ["부등식의 뜻", "일차식의 값"], "ops": ["부등식의 성질"], "traps": ["음수 곱셈 시 방향"], "tags": ["부등식의 성질"]}

# x 범위 꼴(4) × x 계수 부호(2) — 결과 범위의 부등호와 정수 개수 보정(adj)
_XF = {"le_lt": ("≤", "<"), "lt_le": ("<", "≤"), "le_le": ("≤", "≤"), "lt_lt": ("<", "<")}
RANGE_ROWS = {}
for _k, (_xl, _xr) in _XF.items():
    for _sg, _s in (("p", 1), ("n", -1)):
        opl, opr = ((_xl, _xr) if _s > 0 else ({"<": "<", "≤": "≤"}[_xr], {"<": "<", "≤": "≤"}[_xl]))
        RANGE_ROWS[f"{_k}_{_sg}"] = {"XL": _xl, "XR": _xr, "OPL": opl, "OPR": opr, "s": _s,
                                     "FLIP": " (음수를 곱하므로 부등호의 방향이 바뀐다)" if _s < 0 else "",
                                     "SGW": "음수" if _s < 0 else "양수",
                                     "adj": 1 if _k == "le_le" else (-1 if _k == "lt_lt" else 0),
                                     "dl": 1 if opl == "<" else 0, "dr": 1 if opr == "<" else 0}
ASKMN_ROWS = {"key": "ask", "rows": {"sum": {"ASK": "m + n", "t": 1}, "diff": {"ASK": "n − m", "t": -1}}}


def ip_t1():
    return tpl(IP, 1, IP_BASE,
        title="x의 범위가 주어질 때 px + q의 값의 범위 — m + n (n − m)",
        skill="x의 범위의 각 변에 x의 계수를 곱하고(음수면 부등호 방향 반전) 상수를 더해 식의 값의 범위 구하기",
        variant_axis={"x의 범위 꼴": "≤·< 조합 4가지", "계수": "±2~±5", "구하는 것": "m + n / n − m"},
        discriminates="음수를 곱할 때 부등호의 방향을 바꾸고 끝점을 서로 바꾸어 놓는가, 등호의 위치를 그대로 따라가는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(RANGE_ROWS)}}, {"name": "a", "values": {"int": [-5, 3]}}, {"name": "b", "values": {"int": [-2, 6]}},
                {"name": "pp", "values": {"int": [2, 5]}}, {"name": "q", "values": {"in": NZ6}}, {"name": "ask", "values": {"in": ["sum", "diff"]}}],
        table=[{"key": "f", "rows": RANGE_ROWS}, ASKMN_ROWS],
        derive={"p": "s*pp", "lo": "(a*(1 + s) + b*(1 - s))/2", "hi": "(b*(1 + s) + a*(1 - s))/2", "LO": "s*pp*lo", "HI": "s*pp*hi",
                "m": "s*pp*lo + q", "n": "s*pp*hi + q", "ea": "s*pp*a + q", "eb": "s*pp*b + q", "ans": "n + t*m"},
        constraints=["a < b", "ans != 0", "ans not in (a, b, p, abs(q))", "abs(m) <= 40", "abs(n) <= 40", "m != 0", "n != 0"],
        cost_values=["a", "b", "p", "q", "LO", "HI", "m", "n", "ans"],
        answer_var="ans",
        verify=["ans == n + t*m", "m < n", "m == min(ea, eb)", "n == max(ea, eb)"],
        question="{a} {XL} x {XR} {b}일 때, {co(p)}x {sgn(q)}의 값의 범위가 m {OPL} {co(p)}x {sgn(q)} {OPR} n이다. 이때 {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="부등식의 각 변에 같은 양수를 곱하거나 같은 수를 더해도 부등호의 방향은 그대로이고, 음수를 곱하면 방향이 바뀐다. x의 범위 {a} {XL} x {XR} {b}의 각 변에 x의 계수 {p}{eul(p)} 곱한 다음 {q}{eul(q)} 더하면 {co(p)}x {sgn(q)}의 범위가 된다. 등호(≤)는 원래 붙어 있던 끝을 그대로 따라간다.",
        sol2=[
            "각 변에 {p}{eul(p)} 곱하면 {LO} {OPL} {co(p)}x {OPR} {HI}{FLIP}",
            "각 변에 {q}{eul(q)} 더하면 {m} {OPL} {co(p)}x {sgn(q)} {OPR} {n}",
            "따라서 m = {m}, n = {n}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{a} {XL} x {XR} {b}", "hint": "x의 범위"},
            {"text": "{LO} {OPL} {co(p)}x {OPR} {HI}", "hint": "각 변 × {p}{FLIP}"},
            {"text": "{m} {OPL} {co(p)}x {sgn(q)} {OPR} {n}", "hint": "각 변 + {pn(q)}", "marks": [{"on": "{m}", "note": "m"}, {"on": "{n}", "note": "n"}]},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0", "mark:2-1")], [reveal(3)]],
        sol3="끝점을 대입해 보면 x = {a}일 때 {co(p)}x {sgn(q)} = {ea}, x = {b}일 때 {eb}이므로 작은 값 {m}이 m, 큰 값 {n}이 n이다. 계수가 {SGW}이므로 부등호 방향도 맞다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["x = {a} → {ea},  x = {b} → {eb}", "m = {m}, n = {n} → {ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{a} {XL} x {XR} {b}의 각 변에 {p}{eul(p)} 곱하면 {LO} {OPL} {co(p)}x {OPR} {HI}이고, 각 변에 {q}{eul(q)} 더하면 {m} {OPL} {co(p)}x {sgn(q)} {OPR} {n}이다. 따라서 m = {m}, n = {n}이고 {ASK} = {ans}이다.",
        rubric=[
            {"element": "계수 곱하기", "points": 3, "criterion": "각 변에 {p}{eul(p)} 곱해 {LO} {OPL} {co(p)}x {OPR} {HI}{eul(HI)} 얻었다(음수이면 방향을 바꾸었다).", "partial": "음수를 곱하며 방향을 바꾸지 않았으면 인정하지 않는다."},
            {"element": "상수 더하기", "points": 2, "criterion": "각 변에 {q}{eul(q)} 더해 {m} {OPL} {co(p)}x {sgn(q)} {OPR} {n}{eul(n)} 얻었다.", "partial": "한 변에만 더했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "m = {m}, n = {n}에서 {ASK} = {ans}{eul(ans)} 구했다.", "partial": "m, n을 바꾸어 읽었으면 1점."},
        ],
        rubric_total=7,
    )


def ip_t2():
    return tpl(IP, 2, IP_BASE,
        title="x의 범위가 주어질 때 px + q의 값이 될 수 있는 정수의 개수",
        skill="식의 값의 범위를 구한 뒤 경계의 포함 여부(등호)에 맞게 정수를 세기",
        variant_axis={"x의 범위 꼴": "≤·< 조합 4가지", "계수": "±2~±5"},
        discriminates="범위를 바르게 구한 뒤 등호가 붙은 끝은 포함하고 붙지 않은 끝은 제외하며 세는가",
        difficulty=3,
        params=[{"name": "f", "values": {"in": list(RANGE_ROWS)}}, {"name": "a", "values": {"int": [-4, 2]}}, {"name": "b", "values": {"int": [-1, 5]}},
                {"name": "pp", "values": {"int": [2, 4]}}, {"name": "q", "values": {"in": NZ6}}],
        table={"key": "f", "rows": RANGE_ROWS},
        derive={"p": "s*pp", "lo": "(a*(1 + s) + b*(1 - s))/2", "hi": "(b*(1 + s) + a*(1 - s))/2", "LO": "s*pp*lo", "HI": "s*pp*hi",
                "m": "s*pp*lo + q", "n": "s*pp*hi + q", "FIRST": "s*pp*lo + q + dl", "LAST": "s*pp*hi + q - dr", "ans": "n - m + adj"},
        constraints=["a < b", "ans >= 3", "ans not in (a, b, p, abs(q))", "abs(m) <= 30", "abs(n) <= 30"],
        cost_values=["a", "b", "p", "q", "m", "n", "ans"],
        answer_var="ans",
        verify=["ans == LAST - FIRST + 1", "m < n", "FIRST >= m", "LAST <= n"],
        question="{a} {XL} x {XR} {b}일 때, {co(p)}x {sgn(q)}의 값이 될 수 있는 정수의 개수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="먼저 x의 범위의 각 변에 {p}{eul(p)} 곱하고 {q}{eul(q)} 더해 {co(p)}x {sgn(q)}의 값의 범위를 구한다(음수를 곱하면 부등호 방향이 바뀐다). 그다음 그 범위에 들어가는 정수를 센다 — 등호가 있는 끝은 포함하고, 등호가 없는 끝은 뺀다.",
        sol2=[
            "각 변에 {p}{eul(p)} 곱하면 {LO} {OPL} {co(p)}x {OPR} {HI}{FLIP}",
            "각 변에 {q}{eul(q)} 더하면 {m} {OPL} {co(p)}x {sgn(q)} {OPR} {n}",
            "이 범위의 정수는 {FIRST}, …, {LAST}이므로 {ans}개",
        ],
        sol2_fig=steps([
            {"text": "{LO} {OPL} {co(p)}x {OPR} {HI}", "hint": "각 변 × {p}{FLIP}"},
            {"text": "{m} {OPL} {co(p)}x {sgn(q)} {OPR} {n}", "hint": "각 변 + {pn(q)}"},
            {"text": "정수: {FIRST}, …, {LAST} → {ans}개", "marks": [{"on": "{FIRST}, …, {LAST}", "note": "등호 없는 끝은 제외"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{FIRST}부터 {LAST}까지의 정수는 {LAST} − {pn(FIRST)} + 1 = {ans}개다. 끝점 {m}, {n}의 포함 여부를 등호로 다시 확인하면 답은 {ans}이다.",
        sol3_fig=steps(["{LAST} − {pn(FIRST)} + 1 = {ans}", "정수의 개수 = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{a} {XL} x {XR} {b}의 각 변에 {p}{eul(p)} 곱하고 {q}{eul(q)} 더하면 {m} {OPL} {co(p)}x {sgn(q)} {OPR} {n}이다. 이 범위의 정수는 {FIRST}, …, {LAST}의 {ans}개이다.",
        rubric=[
            {"element": "식의 값의 범위", "points": 3, "criterion": "{m} {OPL} {co(p)}x {sgn(q)} {OPR} {n}{eul(n)} 구했다.", "partial": "음수를 곱하며 방향을 바꾸지 않았으면 인정하지 않는다."},
            {"element": "정수 세기", "points": 2, "criterion": "등호 유무에 맞게 {FIRST}부터 {LAST}까지 {ans}개를 셌다.", "partial": "끝점 하나의 포함 여부를 틀려 1개 차이면 1점."},
        ],
        rubric_total=5,
    )


EXT_ROWS = {"key": "w", "rows": {
    "maxp": {"MX": "최댓값", "s": 1, "ia": 0, "SGW": "양수", "WHY": "x가 클수록 값이 커지므로 오른쪽 끝에서 최댓값"},
    "minp": {"MX": "최솟값", "s": 1, "ia": 1, "SGW": "양수", "WHY": "x가 작을수록 값이 작아지므로 왼쪽 끝에서 최솟값"},
    "maxn": {"MX": "최댓값", "s": -1, "ia": 1, "SGW": "음수", "WHY": "x가 작을수록 값이 커지므로 왼쪽 끝에서 최댓값"},
    "minn": {"MX": "최솟값", "s": -1, "ia": 0, "SGW": "음수", "WHY": "x가 클수록 값이 작아지므로 오른쪽 끝에서 최솟값"},
}}


def ip_t3():
    return tpl(IP, 3, IP_BASE,
        title="x의 범위에서 px + k의 최댓값(최솟값)이 주어질 때 상수 k",
        skill="x의 계수의 부호로 최댓값·최솟값이 생기는 끝점을 정하고 대입해 k를 구하기",
        variant_axis={"계수 부호": "양 / 음", "구하는 것": "최댓값 / 최솟값 조건"},
        discriminates="계수가 음수이면 최댓값이 x의 가장 작은 값에서 생김을 아는가",
        difficulty=3,
        params=[{"name": "w", "values": {"in": list(EXT_ROWS["rows"])}}, {"name": "a", "values": {"int": [-4, 2]}}, {"name": "b", "values": {"int": [-1, 5]}},
                {"name": "pp", "values": {"int": [2, 5]}}, {"name": "V", "values": {"int": [-9, 12]}}],
        table=EXT_ROWS,
        derive={"p": "s*pp", "xe": "a*ia + b*(1 - ia)", "pxe": "s*pp*(a*ia + b*(1 - ia))", "k": "V - s*pp*(a*ia + b*(1 - ia))", "ea": "s*pp*a + k", "eb": "s*pp*b + k", "ans": "k"},
        constraints=["a < b", "k != 0", "ans not in (a, b, p, V)", "abs(k) <= 30"],
        cost_values=["a", "b", "p", "V", "pxe", "k"],
        answer_var="ans",
        verify=["ans == V - p*xe", "ia*(a - xe) == 0", "(1 - ia)*(b - xe) == 0", "max(ea, eb) == V or min(ea, eb) == V"],
        question="{a} ≤ x ≤ {b}일 때, {co(p)}x + k의 {MX}이 {V}이다. 상수 k의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="x의 계수가 양수이면 x가 클수록 식의 값이 커지고, 음수이면 x가 클수록 식의 값이 작아진다. 그래서 {co(p)}x + k의 최댓값과 최솟값은 x의 범위의 양 끝 {a}, {b} 중 한쪽에서 생긴다. 계수 {p}의 부호로 어느 끝인지 정한 뒤 대입해 k를 구한다.",
        sol2=[
            "x의 계수 {p}{eun(p)} {SGW}이므로 {MX}은 x = {xe}일 때 생긴다",
            "x = {xe}{eul(xe)} 대입하면 {p} × {pn(xe)} + k = {V}, 즉 {pxe} + k = {V}",
            "따라서 k = {V} − {pn(pxe)} = {k}",
        ],
        sol2_fig=steps([
            {"text": "계수 {p}{eun(p)} {SGW} → {MX}은 x = {xe}에서", "hint": "{WHY}"},
            {"text": "{p} × {pn(xe)} + k = {V}", "hint": "대입"},
            {"text": "k = {V} − {pn(pxe)} = {k}", "marks": [{"on": "{k}", "note": "다른 끝을 쓰면 틀림"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="k = {k}{ro(k)} 놓고 양 끝을 대입하면 x = {a}일 때 {ea}, x = {b}일 때 {eb}이므로 {MX}은 {V}{ika(V)} 맞다. 따라서 k = {k}이다.",
        sol3_fig=steps(["x = {a} → {ea},  x = {b} → {eb}", "{MX} = {V} ✓ → k = {k}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x의 계수 {p}{ika(p)} {SGW}이므로 {co(p)}x + k의 {MX}은 x = {xe}일 때이고, {p} × {pn(xe)} + k = {V}에서 k = {k}이다.",
        rubric=[
            {"element": "끝점 정하기", "points": 3, "criterion": "계수의 부호를 근거로 {MX}이 x = {xe}에서 생김을 밝혔다.", "partial": "근거 없이 끝점만 맞게 골랐으면 1점."},
            {"element": "대입·계산", "points": 2, "criterion": "{p} × {pn(xe)} + k = {V}에서 k = {k}{eul(k)} 구했다.", "partial": "부호 실수 하나면 1점."},
        ],
        rubric_total=5,
    )


XF_ROWS = {"key": "f", "rows": {k: {"XL": xl, "XR": xr} for k, (xl, xr) in _XF.items()}}


def ip_t4():
    return tpl(IP, 4, IP_BASE,
        title="x의 범위가 주어질 때 x/d + q의 값의 범위 — 분수 계수",
        skill="각 변을 같은 양수로 나누고 상수를 더해 분수 계수 식의 값의 범위를 구하기",
        variant_axis={"분모": "2~5", "x의 범위 꼴": "≤·< 조합 4가지"},
        discriminates="각 변을 나눌 때 끝점이 분수가 되어도 그대로 두고 상수를 더하는가, 부등호 방향을 유지하는가",
        difficulty=3,
        params=[{"name": "f", "values": {"in": list(_XF)}}, {"name": "a", "values": {"int": [-9, 3]}}, {"name": "b", "values": {"int": [-2, 9]}},
                {"name": "d", "values": {"int": [2, 5]}}, {"name": "q", "values": {"in": NZ6}}, {"name": "ask", "values": {"in": ["sum", "diff"]}}],
        table=[XF_ROWS, ASKMN_ROWS],
        derive={"LO": "a/d", "HI": "b/d", "m": "a/d + q", "n": "b/d + q", "ans": "n + t*m"},
        constraints=["a < b", "ans != 0", "ans not in (a, b, d, abs(q))", "a % d != 0 or b % d != 0"],
        cost_values=["a", "b", "d", "q", "LO", "HI", "m", "n", "ans"],
        answer_var="ans",
        verify=["ans == n + t*m", "m < n", "m*d == a + q*d", "n*d == b + q*d"],
        question="{a} {XL} x {XR} {b}일 때, [[frac(x, {d})]] {sgn(q)}의 값의 범위가 m {XL} [[frac(x, {d})]] {sgn(q)} {XR} n이다. 이때 {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="[[frac(x, {d})]]{eun(d)} x를 {d}{ro(d)} 나눈 것이므로 x의 범위의 각 변을 {d}{ro(d)} 나눈다. 양수로 나누므로 부등호의 방향은 그대로이고, 끝점이 분수가 되어도 약분만 하고 그대로 둔다. 그다음 각 변에 {q}{eul(q)} 더한다.",
        sol2=[
            "각 변을 {d}{ro(d)} 나누면 {LO} {XL} [[frac(x, {d})]] {XR} {HI}",
            "각 변에 {q}{eul(q)} 더하면 {m} {XL} [[frac(x, {d})]] {sgn(q)} {XR} {n}",
            "따라서 m = {m}, n = {n}이므로 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{LO} {XL} [[frac(x, {d})]] {XR} {HI}", "hint": "각 변 ÷ {d} — 방향 그대로"},
            {"text": "{m} {XL} [[frac(x, {d})]] {sgn(q)} {XR} {n}", "hint": "각 변 + {pn(q)} → m, n"},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="끝점을 대입해 보면 x = {a}일 때 [[frac(x, {d})]] {sgn(q)} = {m}, x = {b}일 때 {n}이 되어 m, n이 맞다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["x = {a} → {m},  x = {b} → {n}", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{a} {XL} x {XR} {b}의 각 변을 {d}{ro(d)} 나누면 {LO} {XL} [[frac(x, {d})]] {XR} {HI}이고, 각 변에 {q}{eul(q)} 더하면 {m} {XL} [[frac(x, {d})]] {sgn(q)} {XR} {n}이다. 따라서 m = {m}, n = {n}이고 {ASK} = {ans}이다.",
        rubric=[
            {"element": "나누기", "points": 3, "criterion": "각 변을 {d}{ro(d)} 나누어 {LO} {XL} [[frac(x, {d})]] {XR} {HI}{eul(HI)} 얻었다.", "partial": "분모를 곱했거나 방향을 바꾸었으면 인정하지 않는다."},
            {"element": "상수 더하기", "points": 2, "criterion": "각 변에 {q}{eul(q)} 더해 {m} {XL} [[frac(x, {d})]] {sgn(q)} {XR} {n}{eul(n)} 얻었다.", "partial": "한 변에만 더했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "m = {m}, n = {n}에서 {ASK} = {ans}{eul(ans)} 구했다.", "partial": "약분하지 않았으면 1점."},
        ],
        rubric_total=7,
    )


IP_SEED = {
    "seed_id": IP, "category": "연산",
    "title": "부등식의 성질 — 식의 값의 범위(m + n·정수의 개수·최댓값 조건·분수 계수)",
    "unit_id": "m2-1", "concept_ids": ["m2-1-07"],
    "schema_id": None, "schema_name": "부등식의 성질과 식의 값의 범위",
    "source_item_ids": [],
    "note": "결과 범위의 부등호는 표 행(x 범위 꼴 × 계수 부호)이 정한다. 계수가 음수이면 끝점이 서로 바뀐다(lo·hi 파생).",
    "geometry": False,
    "templates": [ip_t1(), ip_t2(), ip_t3(), ip_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 일차부등식의 풀이 2
IS = "m2-1-ineq-solve-2"
IS_BASE = {**BASE, "prereq": ["일차부등식의 풀이", "분수의 계산"], "ops": ["일차부등식"], "traps": ["음수로 나눌 때 방향", "통분"], "tags": ["일차부등식"]}


def _ro(n: int) -> str:
    return "으로" if str(abs(n))[-1] in "036" else "로"


def _sign_text(K: int) -> str:
    if K > 0:
        return f"정리한 x의 계수 {K}{'은' if str(K)[-1] in '013678' else '는'} 양수이므로 나눌 때 부등호의 방향은 그대로다."
    return f"정리한 x의 계수 {K}{'은' if str(-K)[-1] in '013678' else '는'} 음수이므로 나눌 때 부등호의 방향이 바뀐다."


def _div_text(K: int) -> str:
    if K == 1:
        return "x의 계수가 1이므로 그대로"
    if K == -1:
        return "양변을 −1로 나누면 부등호의 방향이 바뀌어"
    if K > 0:
        return f"양변을 {K}{_ro(K)} 나누면"
    return f"양변을 음수 {K}{_ro(K)} 나누면 부등호의 방향이 바뀌어"


# t1 — 분수 계수: (x + a)/m − (x + b)/n OP c  (m ≠ n, 순서에 따라 x의 계수 부호가 정해진다)
FR_ROWS = {}
for _m, _n in [(2, 3), (3, 2), (2, 4), (4, 2), (2, 5), (5, 2), (2, 6), (6, 2), (3, 4), (4, 3), (3, 5), (5, 3), (3, 6), (6, 3), (4, 5), (5, 4), (4, 6), (6, 4), (5, 6), (6, 5)]:
    _L = _m * _n // gcd(_m, _n)
    _K = _L // _m - _L // _n
    for _ok, (_op, _opf) in OPS4.items():
        FR_ROWS[f"{_m}-{_n}-{_ok}"] = {"m": _m, "n": _n, "L": _L, "fm": _L // _m, "fn": _L // _n, "K": _K, "OP": _op, "FOP": _opf if _K < 0 else _op,
                                       "DIVT": _div_text(_K), "FLIPW": "바뀐다" if _K < 0 else "그대로다", "SIGNW": _sign_text(_K)}


def is_t1():
    return tpl(IS, 1, IS_BASE,
        title="분수 계수 일차부등식 (x + a)/m − (x + b)/n ▷ c 풀기",
        skill="분모의 최소공배수를 양변에 곱해 정수 계수로 만든 뒤 풀고, x의 계수가 음수이면 방향을 바꾸기",
        variant_axis={"분모": "2~6의 서로 다른 쌍(순서 포함)", "부등호": "<, >, ≤, ≥"},
        discriminates="최소공배수를 상수항에도 곱하는가, 빼는 분수의 분자를 괄호로 묶어 부호를 바꾸는가, 음수 계수로 나눌 때 방향을 바꾸는가",
        difficulty=3,
        params=[{"name": "f", "values": {"in": list(FR_ROWS)}}, {"name": "a", "values": {"in": NZ6}}, {"name": "b", "values": {"in": NZ6}}, {"name": "x0", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}],
        table={"key": "f", "rows": FR_ROWS},
        derive={"fma": "fm*a", "fnb": "fn*b", "nfnb": "-fn*b", "cst": "fm*a - fn*b", "c": "(K*x0 + fm*a - fn*b)/L", "cL": "K*x0 + fm*a - fn*b", "rhs": "K*x0"},
        constraints=["c == floor(c)", "c != 0", "a != b", "abs(c) <= 12", "abs(rhs) <= 40"],
        cost_values=["a", "b", "c", "L", "fma", "fnb", "K", "rhs", "x0"],
        verify=["cL == c*L", "rhs == cL - cst", "K*x0 == rhs", "fm*m == L", "fn*n == L"],
        question="일차부등식 [[frac(x {sgn(a)}, {m})]] − [[frac(x {sgn(b)}, {n})]] {OP} {c}{eul(c)} 푸시오.",
        answer="x {FOP} {x0}", answer_alt=[],
        sol1="분모가 있는 부등식은 양변에 분모의 최소공배수 {L}{eul(L)} 곱해 정수 계수로 고친다. 이때 우변의 상수 {c}에도 {L}{eul(L)} 곱해야 하고, 빼는 분수의 분자 (x {sgn(b)})는 괄호째 곱해 부호를 모두 바꾼다. {SIGNW}",
        sol2=[
            "양변에 {L}{eul(L)} 곱하면 {co(fm)}(x {sgn(a)}) − {co(fn)}(x {sgn(b)}) {OP} {cL}",
            "괄호를 풀면 {co(fm)}x {sgn(fma)} − {co(fn)}x {sgn(nfnb)} {OP} {cL}, 정리하면 {co(K)}x {OP} {rhs}",
            "{DIVT} x {FOP} {x0}",
        ],
        sol2_fig=steps([
            {"text": "{co(fm)}(x {sgn(a)}) − {co(fn)}(x {sgn(b)}) {OP} {cL}", "hint": "양변 × {L} — 우변에도 곱한다"},
            {"text": "{co(fm)}x {sgn(fma)} − {co(fn)}x {sgn(nfnb)} {OP} {cL}", "hint": "괄호 풀기 — 빼는 괄호는 부호 반전"},
            {"text": "{co(K)}x {OP} {rhs}", "hint": "동류항 정리"},
            {"text": "x {FOP} {x0}", "hint": "{DIVT}", "marks": [{"on": "x {FOP} {x0}", "note": "방향 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3", "mark:3-0")]],
        sol3="경계값 x = {x0}{eul(x0)} 원래 부등식의 좌변에 넣으면 [[frac({x0} {sgn(a)}, {m})]] − [[frac({x0} {sgn(b)}, {n})]] = {c}{ro(c)} 우변과 같아진다. 부등호 방향은 x의 계수 {K}의 부호에 따라 {FLIPW}. 따라서 해는 x {FOP} {x0}이다.",
        sol3_fig=steps(["x = {x0}: 좌변 = {c} (경계 확인)", "x {FOP} {x0}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="양변에 {L}{eul(L)} 곱하면 {co(fm)}(x {sgn(a)}) − {co(fn)}(x {sgn(b)}) {OP} {cL}, 괄호를 풀어 정리하면 {co(K)}x {OP} {rhs}이다. {DIVT} x {FOP} {x0}이다.",
        rubric=[
            {"element": "분모 없애기", "points": 3, "criterion": "양변에 {L}{eul(L)} 곱해 {co(fm)}(x {sgn(a)}) − {co(fn)}(x {sgn(b)}) {OP} {cL}{eul(cL)} 얻었다.", "partial": "우변에 곱하지 않았으면 인정하지 않고, 괄호 부호 실수면 1점."},
            {"element": "정리·풀이", "points": 2, "criterion": "{co(K)}x {OP} {rhs}{ro(rhs)} 정리하고 x {FOP} {x0}{eul(x0)} 얻었다(음수로 나누면 방향을 바꾸었다).", "partial": "방향을 바꾸지 않았으면 인정하지 않는다."},
            {"element": "해 나타내기", "points": 2, "criterion": "해를 x {FOP} {x0}{ro(x0)} 썼다.", "partial": "등호 유무가 틀렸으면 1점."},
        ],
        rubric_total=7,
    )


# t2 — 소수 계수: d1·x + e1 OP d2·x + e2 (×10)
DEC_PAIRS = [(3, 5), (5, 3), (2, 5), (5, 2), (4, 7), (7, 4), (3, 7), (7, 3), (6, 4), (4, 6), (2, 6), (6, 2), (1, 3), (3, 1), (8, 5), (5, 8)]
DC_ROWS = {}
for _d1, _d2 in DEC_PAIRS:
    _K = _d1 - _d2
    for _ok, (_op, _opf) in OPS4.items():
        DC_ROWS[f"{_d1}-{_d2}-{_ok}"] = {"D1S": f"0.{_d1}", "D2S": f"0.{_d2}", "D1": _d1, "D2": _d2, "K": _K, "OP": _op, "FOP": _opf if _K < 0 else _op,
                                         "DIVT": _div_text(_K), "FLIPW": "바뀐다" if _K < 0 else "그대로다", "SIGNW": _sign_text(_K)}
E_VALS = [-15, -12, -8, -6, -4, -2, 2, 4, 6, 8, 12, 15]
E1_ROWS = {"key": "e1", "rows": {str(v): {"E1S": ("+ " if v > 0 else "− ") + (f"{abs(v) // 10}.{abs(v) % 10}" if abs(v) % 10 else str(abs(v) // 10)), "E1": v} for v in E_VALS}}
E2_ROWS = {"key": "e2", "rows": {str(v): {"E2S": ("+ " if v > 0 else "− ") + (f"{abs(v) // 10}.{abs(v) % 10}" if abs(v) % 10 else str(abs(v) // 10)), "E2": v} for v in E_VALS}}


def is_t2():
    return tpl(IS, 2, IS_BASE,
        title="소수 계수 일차부등식 0.ax + b ▷ 0.cx + d 풀기",
        skill="양변에 10을 곱해 정수 계수로 고친 뒤 이항해 풀고, x의 계수가 음수이면 방향을 바꾸기",
        variant_axis={"계수": "0.1~0.8", "부등호": "<, >, ≤, ≥"},
        discriminates="10을 모든 항에 곱하는가(정수 항 포함), 음수 계수로 나눌 때 방향을 바꾸는가",
        difficulty=3,
        params=[{"name": "f", "values": {"in": list(DC_ROWS)}}, {"name": "e1", "values": {"in": [str(v) for v in E_VALS]}}, {"name": "e2", "values": {"in": [str(v) for v in E_VALS]}}],
        table=[{"key": "f", "rows": DC_ROWS}, E1_ROWS, E2_ROWS],
        derive={"R": "E2 - E1", "x0": "(E2 - E1)/K"},
        constraints=["x0 == floor(x0)", "x0 != 0", "E1 != E2", "abs(x0) <= 12"],
        cost_values=["D1", "D2", "E1", "E2", "K", "R", "x0"],
        verify=["K*x0 == R", "R == E2 - E1"],
        question="일차부등식 {D1S}x {E1S} {OP} {D2S}x {E2S}{eul(E2)} 푸시오.",
        answer="x {FOP} {x0}", answer_alt=[],
        sol1="계수가 소수이면 양변에 10을 곱해 정수 계수로 고친다. 이때 소수가 아닌 항에도 10을 곱해야 한다. 그다음 x항은 좌변으로, 상수항은 우변으로 이항해 정리한다. {SIGNW}",
        sol2=[
            "양변에 10을 곱하면 {co(D1)}x {sgn(E1)} {OP} {co(D2)}x {sgn(E2)}",
            "이항해 정리하면 {co(D1)}x − {co(D2)}x {OP} {E2} − {pn(E1)}, 즉 {co(K)}x {OP} {R}",
            "{DIVT} x {FOP} {x0}",
        ],
        sol2_fig=steps([
            {"text": "{co(D1)}x {sgn(E1)} {OP} {co(D2)}x {sgn(E2)}", "hint": "양변 × 10 — 모든 항에"},
            {"text": "{co(K)}x {OP} {R}", "hint": "이항 — 부호가 바뀐다"},
            {"text": "x {FOP} {x0}", "hint": "{DIVT}", "marks": [{"on": "x {FOP} {x0}", "note": "방향 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="경계값 x = {x0}{eul(x0)} 넣으면 좌변 {D1S} × {pn(x0)} {E1S}{wa(E1)} 우변 {D2S} × {pn(x0)} {E2S}{ika(E2)} 같아진다(양변 모두 {dec(D1*x0/10 + E1/10)}). 부등호 방향은 x의 계수 {K}의 부호에 따라 {FLIPW}. 따라서 해는 x {FOP} {x0}이다.",
        sol3_fig=steps(["x = {x0}: 좌변 = 우변 = {dec(D1*x0/10 + E1/10)} (경계 확인)", "x {FOP} {x0}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="양변에 10을 곱하면 {co(D1)}x {sgn(E1)} {OP} {co(D2)}x {sgn(E2)}이고, 이항해 정리하면 {co(K)}x {OP} {R}이다. {DIVT} x {FOP} {x0}이다.",
        rubric=[
            {"element": "정수 계수로 고치기", "points": 3, "criterion": "양변에 10을 곱해 {co(D1)}x {sgn(E1)} {OP} {co(D2)}x {sgn(E2)}{eul(E2)} 얻었다.", "partial": "일부 항에만 10을 곱했으면 인정하지 않는다."},
            {"element": "이항·풀이", "points": 2, "criterion": "{co(K)}x {OP} {R}{ro(R)} 정리하고 x {FOP} {x0}{eul(x0)} 얻었다(음수로 나누면 방향을 바꾸었다).", "partial": "방향을 바꾸지 않았으면 인정하지 않는다."},
            {"element": "해 나타내기", "points": 2, "criterion": "해를 x {FOP} {x0}{ro(x0)} 썼다.", "partial": "등호 유무가 틀렸으면 1점."},
        ],
        rubric_total=7,
    )


# t3 — 자연수 해가 n개 → a의 범위
CNT_ROWS = {"key": "op", "rows": {
    "le": {"OP": "≤", "OPA": "≤", "OPB": "<", "AL": "≤", "AR": "<", "dlt": 0, "WHY": "x ≤ a + r의 자연수 해가 1, …, n이려면 n은 포함되고 n + 1은 포함되지 않아야 한다",
           "DL": "(조건에 맞으므로 경계 포함)", "DH": "(조건에 맞지 않으므로 경계 제외)"},
    "lt": {"OP": "<", "OPA": "<", "OPB": "≤", "AL": "<", "AR": "≤", "dlt": 1, "WHY": "x < a + r의 자연수 해가 1, …, n이려면 n은 포함되고 n + 1은 포함되지 않아야 한다",
           "DL": "(조건에 맞지 않으므로 경계 제외)", "DH": "(조건에 맞으므로 경계 포함)"},
}}


def is_t3():
    return tpl(IS, 3, IS_BASE,
        title="자연수인 해가 n개가 되도록 하는 상수 a의 값의 범위",
        skill="해를 x ▷ (a를 포함한 식)으로 정리하고, 자연수 해가 n개이려면 경계가 n과 n + 1 사이여야 함을 부등식으로 쓰기",
        variant_axis={"부등호": "≤ / <", "해의 개수": "2~6"},
        discriminates="경계값이 n일 때 포함되는지(≤이면 포함), n + 1일 때 제외되는지를 등호로 구별해 범위를 쓰는가",
        difficulty=3, process="문제해결",
        params=[{"name": "op", "values": {"in": ["le", "lt"]}}, {"name": "q", "values": {"int": [1, 4]}}, {"name": "r", "values": {"in": [-3, -2, -1, 1, 2, 3, 4, 5]}}, {"name": "n", "values": {"int": [2, 6]}}],
        table=CNT_ROWS,
        derive={"p": "q + 1", "lo": "n - r", "hi": "n + 1 - r", "n1": "n + 1", "nlo": "n - dlt", "nhi": "n + 1 - dlt"},
        constraints=["lo != hi"],
        cost_values=["p", "q", "r", "n", "lo", "hi"],
        verify=["hi == lo + 1", "p - q == 1"],
        question="x에 대한 일차부등식 {p}x − a {OP} {co(q)}x {sgn(r)}{eul(r)} 만족하는 자연수 x가 {n}개일 때, 상수 a의 값의 범위를 구하시오.",
        answer="{lo} {AL} a {AR} {hi}", answer_alt=[],
        sol1="먼저 부등식을 x에 대해 풀면 x {OP} a {sgn(r)}이다. 자연수인 해가 {n}개, 곧 1, 2, …, {n}이려면 경계 a {sgn(r)}{ika(r)} {n}{eun(n)} 포함하고 {n1}{eun(n1)} 포함하지 않아야 하므로 {n} {OPA} a {sgn(r)} {OPB} {n1}이다. 부등호 {OP}에서 등호의 유무가 경계의 포함 여부를 정한다.",
        sol2=[
            "x항을 좌변으로 모으면 {p}x − {co(q)}x {OP} a {sgn(r)}, 즉 x {OP} a {sgn(r)}",
            "자연수 해가 1, …, {n}의 {n}개이려면 {n} {OPA} a {sgn(r)} {OPB} {n1}",
            "각 변에서 {r}{eul(r)} 빼면 {lo} {AL} a {AR} {hi}",
        ],
        sol2_fig=steps([
            {"text": "x {OP} a {sgn(r)}", "hint": "x에 대해 푼다"},
            {"text": "{n} {OPA} a {sgn(r)} {OPB} {n1}", "hint": "{WHY}", "marks": [{"on": "{OPB} {n1}", "note": "{n1}은 해가 아니어야"}]},
            {"text": "{lo} {AL} a {AR} {hi}", "hint": "각 변 − {pn(r)}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")]],
        sol3="a = {lo}이면 x {OP} {n}{ika(n)} 되어 자연수 해가 {nlo}개{DL}, a = {hi}이면 x {OP} {n1}{ika(n1)} 되어 {nhi}개{DH}. 따라서 a의 범위는 {lo} {AL} a {AR} {hi}이다.",
        sol3_fig=steps(["a = {lo}: x {OP} {n} → 자연수 해 {nlo}개 {DL}", "a = {hi}: x {OP} {n1} → 자연수 해 {nhi}개 {DH}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{p}x − a {OP} {co(q)}x {sgn(r)}에서 x {OP} a {sgn(r)}이다. 자연수인 해가 {n}개이려면 {n} {OPA} a {sgn(r)} {OPB} {n1}이어야 하므로 {lo} {AL} a {AR} {hi}이다.",
        rubric=[
            {"element": "x에 대해 풀기", "points": 2, "criterion": "부등식을 x {OP} a {sgn(r)}{ro(r)} 정리했다.", "partial": "이항 부호 실수면 1점."},
            {"element": "경계 조건", "points": 3, "criterion": "자연수 해가 {n}개일 조건 {n} {OPA} a {sgn(r)} {OPB} {n1}{eul(n1)} 세웠다.", "partial": "등호의 위치가 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{lo} {AL} a {AR} {hi}{eul(hi)} 구했다.", "partial": "한쪽 경계만 맞으면 1점."},
        ],
        rubric_total=7,
    )


def is_t4():
    return tpl(IS, 4, IS_BASE,
        title="분수 꼴 부등식 (x − a)/m ▷ c의 해가 주어질 때 상수 a",
        skill="분모를 없애 x에 대해 풀고, 주어진 해의 경계값과 비교해 a를 구하기",
        variant_axis={"분모": "2~5", "부등호": "<, >, ≤, ≥"},
        discriminates="해의 경계값을 비교해 a를 구하는가 — 분모를 우변에도 곱하고 부호를 맞게 옮기는가",
        difficulty=2,
        params=[{"name": "op", "values": {"in": list(OPS4)}}, {"name": "m", "values": {"int": [2, 5]}}, {"name": "c", "values": {"in": [-3, -2, -1, 1, 2, 3]}}, {"name": "k", "values": {"int": [-8, 8]}}],
        table={"key": "op", "rows": {k: {"OP": v[0]} for k, v in OPS4.items()}},
        derive={"cm": "c*m", "a": "k - c*m", "ans": "k - c*m"},
        constraints=["a != 0", "ans not in (m, c, k)", "k != 0"],
        cost_values=["m", "c", "k", "cm", "a"],
        answer_var="ans",
        verify=["ans == k - cm", "cm + ans == k"],
        question="x에 대한 일차부등식 [[frac(x − a, {m})]] {OP} {c}의 해가 x {OP} {k}일 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="양변에 분모 {m}{eul(m)} 곱하면 x − a {OP} {cm}이고, a를 이항하면 x {OP} {cm} + a이다(양수를 곱했으므로 방향은 그대로). 이것이 주어진 해 x {OP} {k}{wa(k)} 같으려면 경계값이 같아야 하므로 {cm} + a = {k}이다.",
        sol2=[
            "양변에 {m}{eul(m)} 곱하면 x − a {OP} {cm}",
            "a를 이항하면 x {OP} {cm} + a",
            "해가 x {OP} {k}이므로 {cm} + a = {k}, 따라서 a = {a}",
        ],
        sol2_fig=steps([
            {"text": "x − a {OP} {cm}", "hint": "양변 × {m} — 우변에도"},
            {"text": "x {OP} {cm} + a", "hint": "a를 이항"},
            {"text": "{cm} + a = {k} → a = {a}", "hint": "주어진 해와 경계값 비교", "marks": [{"on": "{a}", "note": "경계값이 같아야"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="a = {a}{eul(a)} 넣으면 [[frac(x − {pn(a)}, {m})]] {OP} {c}에서 x − {pn(a)} {OP} {cm}, x {OP} {k}{ika(k)} 되어 주어진 해와 같다. 따라서 a = {a}이다.",
        sol3_fig=steps(["a = {a}: x − {pn(a)} {OP} {cm} → x {OP} {k} ✓", "a = {a}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[frac(x − a, {m})]] {OP} {c}의 양변에 {m}{eul(m)} 곱하면 x − a {OP} {cm}, 곧 x {OP} {cm} + a이다. 해가 x {OP} {k}이므로 {cm} + a = {k}에서 a = {a}이다.",
        rubric=[
            {"element": "x에 대해 풀기", "points": 3, "criterion": "양변에 {m}{eul(m)} 곱하고 이항해 x {OP} {cm} + a{eul(a)} 얻었다.", "partial": "우변에 {m}{eul(m)} 곱하지 않았으면 인정하지 않는다."},
            {"element": "경계값 비교·답", "points": 2, "criterion": "{cm} + a = {k}에서 a = {a}{eul(a)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def is_t5():
    return tpl(IS, 5, IS_BASE,
        title="두 일차부등식의 해가 서로 같을 때 상수 a",
        skill="상수가 없는 부등식을 먼저 풀어 해를 구하고, 다른 부등식의 해가 그것과 같도록 a를 정하기",
        variant_axis={"부등호": "<, >, ≤, ≥", "둘째 부등식의 x 계수": "−1~−4 (방향이 바뀜)"},
        discriminates="음수 계수 부등식을 풀 때 방향을 바꾸어 첫째 해와 같은 꼴로 맞추는가, 경계값이 같다는 식을 세우는가",
        difficulty=3, process="문제해결",
        params=[{"name": "op", "values": {"in": list(OPS4)}}, {"name": "p", "values": {"int": [2, 5]}}, {"name": "q", "values": {"in": NZ6}}, {"name": "x0", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}},
                {"name": "s", "values": {"int": [1, 4]}}, {"name": "t", "values": {"int": [-6, 6]}}],
        table={"key": "op", "rows": {k: {"OP": v[0], "OPF": v[1]} for k, v in OPS4.items()}},
        derive={"r": "p*x0 + q", "rq": "p*x0", "u": "-s", "ux0": "-s*x0", "a": "t + s*x0", "ans": "t + s*x0"},
        constraints=["a != 0", "ans not in (p, abs(q), r, u, t)", "r != 0", "t != 0"],
        cost_values=["p", "q", "r", "x0", "u", "t", "ux0", "a"],
        answer_var="ans",
        verify=["ans == t - u*x0", "p*x0 + q == r", "(t - ans) == u*x0"],
        question="두 일차부등식 {p}x {sgn(q)} {OP} {r}{wa(r)} {co(u)}x + a {OPF} {t}의 해가 서로 같을 때, 상수 a의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="상수 a가 없는 첫째 부등식을 먼저 풀면 해가 x {OP} {x0}이다. 둘째 부등식 {co(u)}x + a {OPF} {t}{eun(t)} x의 계수가 음수이므로 나눌 때 부등호의 방향이 바뀌어 x {OP} (경계값) 꼴이 된다. 두 해가 같으려면 이 경계값이 {x0}{wa(x0)} 같아야 한다.",
        sol2=[
            "첫째: {p}x {OP} {r} − {pn(q)} = {rq}이므로 x {OP} {x0}",
            "둘째: {co(u)}x {OPF} {t} − a, 양변을 음수 {u}{ro(u)} 나누면 방향이 바뀌어 x {OP} ({t} − a) ÷ ({u})",
            "두 해가 같으므로 ({t} − a) ÷ ({u}) = {x0}, 즉 {t} − a = {ux0}에서 a = {a}",
        ],
        sol2_fig=steps([
            {"text": "{p}x {OP} {rq} → x {OP} {x0}", "hint": "첫째 부등식의 해"},
            {"text": "{co(u)}x {OPF} {t} − a → x {OP} ({t} − a) ÷ ({u})", "hint": "음수로 나누면 방향이 바뀐다"},
            {"text": "{t} − a = {ux0} → a = {a}", "hint": "경계값이 같다", "marks": [{"on": "{a}", "note": "({t} − a) ÷ ({u}) = {x0}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="a = {a}{eul(a)} 둘째 부등식에 넣으면 {co(u)}x + {pn(a)} {OPF} {t}, {co(u)}x {OPF} {ux0}, x {OP} {x0}{ika(x0)} 되어 첫째 부등식의 해와 같다. 따라서 a = {a}이다.",
        sol3_fig=steps(["a = {a}: {co(u)}x {OPF} {ux0} → x {OP} {x0} ✓", "a = {a}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{p}x {sgn(q)} {OP} {r}에서 x {OP} {x0}이고, {co(u)}x + a {OPF} {t}에서 x {OP} ({t} − a) ÷ ({u})이다. 두 해가 같으므로 {t} − a = {ux0}, a = {a}이다.",
        rubric=[
            {"element": "첫째 부등식 풀기", "points": 2, "criterion": "{p}x {sgn(q)} {OP} {r}{eul(r)} 풀어 x {OP} {x0}{eul(x0)} 얻었다.", "partial": "이항 부호 실수면 1점."},
            {"element": "둘째 부등식 풀기", "points": 3, "criterion": "{co(u)}x + a {OPF} {t}{eul(t)} 풀며 음수로 나누어 방향을 바꾸어 x {OP} ({t} − a) ÷ ({u})로 썼다.", "partial": "방향을 바꾸지 않았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "경계값이 같다는 식에서 a = {a}{eul(a)} 구했다.", "partial": "식은 맞고 계산 실수면 1점."},
        ],
        rubric_total=7,
    )


IS_SEED = {
    "seed_id": IS, "category": "연산",
    "title": "일차부등식의 풀이 2 — 분수 계수·소수 계수·자연수 해 개수→a 범위·분수 꼴 해→상수·해가 같은 두 부등식",
    "unit_id": "m2-1", "concept_ids": ["m2-1-08"],
    "schema_id": None, "schema_name": "분수·소수 계수 일차부등식과 상수 결정",
    "source_item_ids": [],
    "note": "부등호 방향은 표 행(분모 순서·계수 쌍)이 정하고 나누는 문구(DIVT)도 행마다 고정 문자열. 해가 문자열인 t1·t2·t3 은 recheck.py 가 되읽어 대조.",
    "geometry": False,
    "templates": [is_t1(), is_t2(), is_t3(), is_t4(), is_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 일차부등식의 활용
IA = "m2-1-ineq-apply"
IA_BASE = {**COMMON_APPLY, "ops": ["부등식", "사칙"], "prereq": ["일차부등식의 풀이"], "traps": ["부등호 방향(이상·이하)", "자연수 조건"], "tags": ["일차부등식의 활용"], "qtype": "short", "pool_target": 300}
NAME_ROWS = {"key": "nm", "rows": {"1": {"S": "지수"}, "2": {"S": "민준"}, "3": {"S": "서연"}, "4": {"S": "도윤"}, "5": {"S": "하은"}, "6": {"S": "시우"}}}
SUBJ_ROWS = {"key": "sub", "rows": {"m": {"SUB": "수학"}, "e": {"SUB": "영어"}, "s": {"SUB": "과학"}}}


def ia_t1():
    return tpl(IA, 1, IA_BASE,
        title="세 번의 점수가 주어질 때 평균이 M점 이상이 되기 위한 네 번째 최소 점수",
        skill="평균 조건을 (점수의 합) ÷ 4 ≥ M의 부등식으로 세우고 풀어 최소 점수를 구하기",
        variant_axis={"점수": "70~96", "목표 평균": "80~92"},
        discriminates="평균을 합 ÷ 4로 세우는가, '이상'을 ≥로 옮기고 최소 점수를 경계값으로 답하는가",
        difficulty=2,
        params=[{"name": "nm", "values": {"in": list(NAME_ROWS["rows"])}}, {"name": "sub", "values": {"in": ["m", "e", "s"]}},
                {"name": "s1", "values": {"step": [70, 96, 2]}}, {"name": "s2", "values": {"step": [71, 97, 2]}}, {"name": "s3", "values": {"step": [74, 98, 3]}}, {"name": "M", "values": {"int": [80, 92]}}],
        table=[NAME_ROWS, SUBJ_ROWS],
        derive={"sum3": "s1 + s2 + s3", "M4": "4*M", "ans": "4*M - s1 - s2 - s3"},
        constraints=["ans >= 1", "ans <= 100", "ans not in (s1, s2, s3, M, 4)", "s1 != s2", "s2 != s3", "s1 != s3"],
        cost_values=["s1", "s2", "s3", "M", "sum3", "M4", "ans"],
        answer_var="ans",
        verify=["ans == 4*M - sum3", "(sum3 + ans)/4 == M"],
        question="{S}{eun(S)} 세 번의 {SUB} 시험에서 {s1}점, {s2}점, {s3}점을 받았다. 네 번째 시험까지의 평균이 {M}점 이상이 되려면 네 번째 시험에서 최소 몇 점을 받아야 하는지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="네 번째 시험 점수를 x점이라 하면 네 번의 평균은 (네 점수의 합) ÷ 4이다. '평균이 {M}점 이상'은 (합) ÷ 4 ≥ {M}이라는 부등식이고, 양변에 4를 곱해 풀면 x의 범위가 나온다. 최소 점수는 그 범위의 경계값이다.",
        sol2=[
            "네 번째 점수를 x점이라 하면 [[frac({s1} + {s2} + {s3} + x, 4)]] ≥ {M}",
            "양변에 4를 곱하면 {sum3} + x ≥ {M4}",
            "x ≥ {ans}이므로 최소 {ans}점",
        ],
        sol2_fig=steps([
            {"text": "[[frac({s1} + {s2} + {s3} + x, 4)]] ≥ {M}", "hint": "평균 = 합 ÷ 4, '이상' = ≥"},
            {"text": "{sum3} + x ≥ {M4}", "hint": "양변 × 4"},
            {"text": "x ≥ {ans} → 최소 {ans}점", "marks": [{"on": "{ans}", "note": "경계값이 최소"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="네 번째에 {ans}점을 받으면 합은 {sum3} + {ans} = {M4}이고 평균은 {M4} ÷ 4 = {M}점으로 꼭 {M}점이 된다. {ans}점보다 낮으면 평균이 {M}점에 못 미친다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{sum3} + {ans} = {M4},  {M4} ÷ 4 = {M} ✓", "최소 {ans}점"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="네 번째 시험 점수를 x점이라 하면 [[frac({s1} + {s2} + {s3} + x, 4)]] ≥ {M}에서 {sum3} + x ≥ {M4}, x ≥ {ans}이다. 따라서 최소 {ans}점을 받아야 한다.",
        rubric=[
            {"element": "부등식 세우기", "points": 3, "criterion": "네 번째 점수를 x로 놓고 [[frac({s1} + {s2} + {s3} + x, 4)]] ≥ {M}{eul(M)} 세웠다.", "partial": "4로 나누지 않았거나 부등호 방향이 틀렸으면 1점."},
            {"element": "부등식 풀기", "points": 3, "criterion": "x ≥ {ans}{eul(ans)} 얻었다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "최소 점수 {ans}점을 답했다.", "partial": "범위만 쓰고 최소 점수를 답하지 않았으면 1점."},
        ],
        rubric_total=8,
    )


ITEM_ROWS = {"key": "it", "rows": {
    "1": {"I1": "사과", "I2": "배", "U": "개"}, "2": {"I1": "연필", "I2": "볼펜", "U": "자루"}, "3": {"I1": "빵", "I2": "케이크", "U": "개"},
    "4": {"I1": "장미", "I2": "백합", "U": "송이"}, "5": {"I1": "귤", "I2": "망고", "U": "개"}, "6": {"I1": "공책", "I2": "파일", "U": "권"},
}}


def ia_t2():
    return tpl(IA, 2, IA_BASE,
        title="두 품목을 합해 n개 살 때 예산 안에서 비싼 품목의 최대 개수",
        skill="비싼 품목을 x개, 싼 품목을 (n − x)개로 놓고 금액 부등식을 세워 최대 개수를 자연수로 답하기",
        variant_axis={"단가": "500~1500원 / 1500~3000원", "총 개수": "10~20", "예산": "정확·나머지 있음"},
        discriminates="다른 품목의 개수를 (n − x)로 놓는가, 해의 범위에서 자연수 최댓값을 고르는가(올림하지 않는가)",
        difficulty=3,
        params=[{"name": "it", "values": {"in": list(ITEM_ROWS["rows"])}}, {"name": "a", "values": {"in": [500, 600, 800, 1000, 1200, 1500]}}, {"name": "b", "values": {"in": [1500, 2000, 2500, 3000]}},
                {"name": "n", "values": {"in": [10, 12, 15, 20]}}, {"name": "k", "values": {"int": [3, 9]}}, {"name": "dl", "values": {"in": [0, 100, 200, 300, 400]}}],
        table=ITEM_ROWS,
        derive={"bma": "b - a", "an": "a*n", "B": "a*n + (b - a)*k + dl", "Bmn": "(b - a)*k + dl", "q": "((b - a)*k + dl)/max(b - a, 1)", "ans": "k"},
        constraints=["b > a", "dl < bma", "k < n", "ans not in (a, b, n, B)", "q*100 == floor(q*100)"],
        cost_values=["a", "b", "n", "B", "an", "Bmn", "q", "ans"],
        answer_var="ans",
        verify=["ans == floor(q)", "b*ans + a*(n - ans) <= B", "b*(ans + 1) + a*(n - ans - 1) > B"],
        question="한 {U}에 {a}원인 {I1}{wa(I1)} 한 {U}에 {b}원인 {I2}{eul(I2)} 합하여 {n}{U} 사려고 한다. 전체 금액이 {B}원 이하가 되게 하려면 {I2}{eun(I2)} 최대 몇 {U}까지 살 수 있는지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{I2}{eul(I2)} x{U} 사면 {I1}{eun(I1)} 나머지 ({n} − x){U}이다. 전체 금액 {b}x + {a}({n} − x)가 {B}원 이하라는 부등식을 세워 풀면 x의 범위가 나오고, x는 자연수이므로 그 범위 안의 가장 큰 자연수가 답이다.",
        sol2=[
            "{I2}{eul(I2)} x{U} 사면 {I1}{eun(I1)} ({n} − x){U}이므로 {b}x + {a}({n} − x) ≤ {B}",
            "{b}x + {an} − {a}x ≤ {B}, {bma}x ≤ {Bmn}",
            "x ≤ {dec(q)}이고 x는 자연수이므로 최대 {ans}{U}",
        ],
        sol2_fig=steps([
            {"text": "{b}x + {a}({n} − x) ≤ {B}", "hint": "{I2} x{U}, {I1} ({n} − x){U}"},
            {"text": "{bma}x ≤ {Bmn}", "hint": "괄호 풀고 정리"},
            {"text": "x ≤ {dec(q)} → 최대 {ans}{U}", "marks": [{"on": "{ans}{U}", "note": "자연수 최댓값 — 올리지 않는다"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{I2} {ans}{U}, {I1} {n - ans}{U}이면 금액은 {b} × {ans} + {a} × {n - ans} = {b*ans + a*(n - ans)}원으로 {B}원 이하이고, {I2}{eul(I2)} {ans + 1}{U} 사면 {b*(ans + 1) + a*(n - ans - 1)}원으로 예산을 넘는다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{ans}{U}: {b*ans + a*(n - ans)}원 ≤ {B}원 ✓", "{ans + 1}{U}: {b*(ans + 1) + a*(n - ans - 1)}원 > {B}원 ✗"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{I2}{eul(I2)} x{U} 사면 {I1}{eun(I1)} ({n} − x){U}이므로 {b}x + {a}({n} − x) ≤ {B}, {bma}x ≤ {Bmn}, x ≤ {dec(q)}이다. x는 자연수이므로 {I2}{eun(I2)} 최대 {ans}{U}까지 살 수 있다.",
        rubric=[
            {"element": "부등식 세우기", "points": 3, "criterion": "{I2}{eul(I2)} x{U}로 놓고 {b}x + {a}({n} − x) ≤ {B}{eul(B)} 세웠다.", "partial": "{I1}의 개수를 ({n} − x)로 놓지 않았으면 인정하지 않는다."},
            {"element": "부등식 풀기", "points": 3, "criterion": "x ≤ {dec(q)}{eul(dec(q))} 얻었다.", "partial": "괄호를 풀 때 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "자연수 조건으로 최대 {ans}{U}{eul(U)} 답했다.", "partial": "올림해 {ans + 1}{U}{ro(U)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def ia_t3():
    return tpl(IA, 3, IA_BASE,
        title="기차 출발까지 남은 시간 안에 다녀올 수 있는 상점까지의 최대 거리",
        skill="왕복 거리 ÷ 속력을 시간으로 바꾸고(시간 단위를 분으로 맞추어) 머무는 시간까지 더해 부등식을 세우기",
        variant_axis={"속력": "시속 3·4·6 km", "남은 시간·머무는 시간": "40~60분 / 10~20분"},
        discriminates="왕복이므로 거리에 2를 곱하는가, 시간 단위(시·분)를 맞추는가",
        difficulty=3,
        params=[{"name": "nm", "values": {"in": list(NAME_ROWS["rows"])}}, {"name": "v", "values": {"in": [3, 4, 5, 6, 8]}}, {"name": "T", "values": {"in": [40, 45, 50, 55, 60, 70, 80, 90]}}, {"name": "s", "values": {"in": [10, 12, 15, 20, 25, 30]}}],
        table=NAME_ROWS,
        derive={"k": "120/v", "m": "T - s", "ans": "v*(T - s)/120"},
        constraints=["m >= 20", "ans*100 == floor(ans*100)", "ans not in (v, T, s)"],
        cost_values=["v", "T", "s", "k", "m", "ans"],
        answer_var="ans",
        verify=["ans == m/k", "k*v == 120", "2*ans/v*60 + s == T"],
        question="{S}{ika(S)} 역에서 기차를 기다리는데 출발까지 {T}분이 남아 있다. 시속 {v} km로 걸어서 상점에 가서 물건을 사는 데 {s}분이 걸린다고 할 때, 역에서 최대 몇 km 떨어진 상점까지 다녀올 수 있는지 구하시오.",
        answer="{dec(ans)}", answer_alt=[],
        sol1="상점까지의 거리를 x km라 하면 갔다 오는 거리는 2x km이고, 시속 {v} km로 걸으면 왕복 시간은 [[frac(2x, {v})]]시간이다. 남은 시간이 분 단위이므로 60을 곱해 분으로 바꾸면 {k}x분이다. (왕복 시간) + (물건 사는 시간) ≤ (남은 시간)의 부등식을 세운다.",
        sol2=[
            "상점까지의 거리를 x km라 하면 왕복 시간은 [[frac(2x, {v})]]시간 = [[frac(2x, {v})]] × 60분 = {k}x분",
            "{k}x + {s} ≤ {T}",
            "{k}x ≤ {m}, x ≤ {dec(ans)}이므로 최대 {dec(ans)} km",
        ],
        sol2_fig=steps([
            {"text": "왕복 [[frac(2x, {v})]]시간 = {k}x분", "hint": "거리 × 2, 시간 × 60"},
            {"text": "{k}x + {s} ≤ {T}", "hint": "왕복 + 머무는 시간 ≤ 남은 시간"},
            {"text": "x ≤ {dec(ans)} → 최대 {dec(ans)} km", "marks": [{"on": "{dec(ans)} km", "note": "{m} ÷ {k}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{dec(ans)} km 떨어진 상점이면 왕복 {dec(2*ans)} km를 시속 {v} km로 걷는 데 {m}분이 걸리고, 물건 사는 {s}분을 더하면 꼭 {T}분이다. 더 멀면 시간이 모자란다. 따라서 답은 {dec(ans)}이다.",
        sol3_fig=steps(["왕복 {dec(2*ans)} km ÷ 시속 {v} km = {m}분", "{m} + {s} = {T}분 ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="상점까지의 거리를 x km라 하면 왕복 시간은 [[frac(2x, {v})]] × 60 = {k}x(분)이므로 {k}x + {s} ≤ {T}, x ≤ {dec(ans)}이다. 따라서 최대 {dec(ans)} km 떨어진 상점까지 다녀올 수 있다.",
        rubric=[
            {"element": "부등식 세우기", "points": 3, "criterion": "왕복 시간을 {k}x분으로 나타내어 {k}x + {s} ≤ {T}{eul(T)} 세웠다.", "partial": "왕복(×2)이나 단위 변환(×60) 중 하나를 빠뜨렸으면 1점."},
            {"element": "부등식 풀기", "points": 3, "criterion": "x ≤ {dec(ans)}{eul(dec(ans))} 얻었다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "최대 거리 {dec(ans)} km를 답했다."},
        ],
        rubric_total=8,
    )


FIGA_ROWS = {"key": "sh", "rows": {
    "tri": {"D1": "밑변의 길이가", "D2": "높이가 x cm인 삼각형", "kk": 2, "PRE1": "[[frac(1,2)]] × ", "FIG": "삼각형", "FORMW": "(밑변) × (높이) ÷ 2"},
    "rect": {"D1": "가로의 길이가", "D2": "세로의 길이가 x cm인 직사각형", "kk": 1, "PRE1": "", "FIG": "직사각형", "FORMW": "(가로) × (세로)"},
}}
DIR_ROWS = {"key": "d", "rows": {"ge": {"W": " 이상일 때", "OP": "≥", "WW": "이상"}, "gt": {"W": "보다 클 때", "OP": ">", "WW": "초과"}}}


def ia_t4():
    return tpl(IA, 4, IA_BASE,
        title="넓이 조건을 만족하는 삼각형(직사각형)의 높이 x의 범위",
        skill="넓이 공식으로 부등식을 세우고 x의 계수로 나누어 x의 범위를 부등식으로 나타내기",
        variant_axis={"도형": "삼각형 / 직사각형", "조건": "이상 / 초과"},
        discriminates="삼각형의 넓이에 1/2을 곱하는가, '이상'과 '보다 크다'를 ≥와 >로 구별하는가",
        difficulty=2, context="기하맥락",
        params=[{"name": "sh", "values": {"in": ["tri", "rect"]}}, {"name": "d", "values": {"in": ["ge", "gt"]}}, {"name": "b", "values": {"int": [3, 12]}}, {"name": "k", "values": {"int": [2, 12]}}],
        table=[FIGA_ROWS, DIR_ROWS],
        derive={"c": "b/kk", "A": "b*k/kk"},
        constraints=["c == floor(c)", "A == floor(A)", "k != b", "A != b", "A != k"],
        cost_values=["b", "k", "c", "A"],
        verify=["c*k == A", "kk*A == b*k"],
        question="{D1} {b} cm이고 {D2}의 넓이가 {A} cm²{W}, x의 값의 범위를 구하시오.",
        answer="x {OP} {k}", answer_alt=[],
        sol1="{FIG}의 넓이는 {FORMW}이므로 {PRE1}{b} × x이다. 넓이가 {A} cm² {WW}라는 조건을 부등식으로 쓰면 {c}x {OP} {A}이고, 양변을 {c}{ro(c)} 나누면 x의 범위가 나온다. '이상'은 등호를 포함하고 '보다 크다'는 포함하지 않는다.",
        sol2=[
            "넓이는 {PRE1}{b} × x = {c}x (cm²)이므로 {c}x {OP} {A}",
            "양변을 {c}{ro(c)} 나누면 x {OP} {k}",
        ],
        sol2_fig=steps([
            {"text": "{PRE1}{b} × x {OP} {A}", "hint": "넓이 = {FORMW}"},
            {"text": "{c}x {OP} {A} → x {OP} {k}", "hint": "양변 ÷ {c}", "marks": [{"on": "x {OP} {k}", "note": "등호 유무 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="x = {k}이면 넓이는 {c} × {k} = {A} cm²로 경계값과 같고, x가 {k}보다 크면 넓이도 {A} cm²보다 커진다. 따라서 x의 범위는 x {OP} {k}이다.",
        sol3_fig=steps(["x = {k}: 넓이 = {A} cm² (경계)", "x {OP} {k}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{FIG}의 넓이는 {PRE1}{b} × x = {c}x이므로 {c}x {OP} {A}, 양변을 {c}{ro(c)} 나누면 x {OP} {k}이다.",
        rubric=[
            {"element": "부등식 세우기", "points": 3, "criterion": "넓이 {c}x를 써서 {c}x {OP} {A}{eul(A)} 세웠다.", "partial": "삼각형에서 2로 나누는 것을 빠뜨렸거나 부등호 종류가 틀렸으면 1점."},
            {"element": "범위 구하기", "points": 2, "criterion": "x {OP} {k}{eul(k)} 얻었다.", "partial": "등호 유무가 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


def ia_t5():
    return tpl(IA, 5, IA_BASE,
        title="엘리베이터 적재 한도 안에서 실을 수 있는 상자의 최대 개수",
        skill="(사람 몸무게) + (상자 무게) × (개수) ≤ (한도)의 부등식을 세우고 자연수 최댓값을 구하기",
        variant_axis={"한도": "450~1000 kg", "상자": "10~30 kg"},
        discriminates="사람의 몸무게를 더하는가, 해의 범위에서 자연수 최댓값을 고르는가",
        difficulty=2,
        params=[{"name": "W", "values": {"in": [450, 500, 550, 600, 650, 700, 750, 800, 900, 1000]}}, {"name": "p", "values": {"in": [50, 55, 60, 65, 70, 75, 80, 85]}}, {"name": "w", "values": {"in": [8, 10, 12, 15, 16, 20, 24, 25, 30]}}],
        derive={"Wp": "W - p", "q": "(W - p)/w", "ans": "floor((W - p)/w)"},
        constraints=["ans >= 3", "ans not in (W, p, w)", "q*100 == floor(q*100)"],
        cost_values=["W", "p", "w", "Wp", "q", "ans"],
        answer_var="ans",
        verify=["w*ans + p <= W", "w*(ans + 1) + p > W"],
        question="한 번에 {W} kg까지 실을 수 있는 엘리베이터에 몸무게가 {p} kg인 사람이 한 개에 {w} kg인 상자를 여러 개 싣고 타려고 한다. 한 번에 최대 몇 개까지 실을 수 있는지 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="상자를 x개 실으면 엘리베이터에 실리는 무게는 사람 {p} kg과 상자 {w}x kg을 합한 것이다. 이것이 한도 {W} kg 이하여야 하므로 {w}x + {p} ≤ {W}의 부등식을 세우고, x는 자연수이므로 범위 안의 가장 큰 자연수를 답한다.",
        sol2=[
            "상자를 x개 실으면 {w}x + {p} ≤ {W}",
            "{w}x ≤ {Wp}, x ≤ {dec(q)}",
            "x는 자연수이므로 최대 {ans}개",
        ],
        sol2_fig=steps([
            {"text": "{w}x + {p} ≤ {W}", "hint": "사람 무게도 더한다"},
            {"text": "{w}x ≤ {Wp} → x ≤ {dec(q)}", "hint": "양변 ÷ {w}"},
            {"text": "최대 {ans}개", "marks": [{"on": "{ans}개", "note": "자연수 최댓값"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="상자 {ans}개이면 {w} × {ans} + {p} = {w*ans + p} kg으로 한도 이하이고, {ans + 1}개이면 {w*(ans + 1) + p} kg으로 한도를 넘는다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{ans}개: {w*ans + p} kg ≤ {W} kg ✓", "{ans + 1}개: {w*(ans + 1) + p} kg > {W} kg ✗"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="상자를 x개 실으면 {w}x + {p} ≤ {W}에서 {w}x ≤ {Wp}, x ≤ {dec(q)}이다. x는 자연수이므로 최대 {ans}개까지 실을 수 있다.",
        rubric=[
            {"element": "부등식 세우기", "points": 3, "criterion": "상자 x개로 놓고 {w}x + {p} ≤ {W}{eul(W)} 세웠다.", "partial": "사람의 몸무게를 빠뜨렸으면 인정하지 않는다."},
            {"element": "부등식 풀기", "points": 3, "criterion": "x ≤ {dec(q)}{eul(dec(q))} 얻었다.", "partial": "계산 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "자연수 조건으로 최대 {ans}개를 답했다.", "partial": "올림해 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


IA_SEED = {
    "seed_id": IA, "category": "활용",
    "title": "일차부등식의 활용 — 평균 점수·두 품목 최대 개수·상점 다녀오기·넓이 조건 범위·엘리베이터",
    "unit_id": "m2-1", "concept_ids": ["m2-1-09", "m2-1-10"],
    "schema_id": None, "schema_name": "일차부등식 세우기(문장제)",
    "source_item_ids": [],
    "note": "최대 개수 틀은 답(k)을 파라미터로 두고 예산을 역산(나머지 dl)한다. 거리 틀의 답은 소수(dec) 표기, 넓이 틀의 답은 부등식 문자열.",
    "geometry": False,
    "templates": [ia_t1(), ia_t2(), ia_t3(), ia_t4(), ia_t5()],
}


if __name__ == "__main__":
    for seed in (IP_SEED, IS_SEED, IA_SEED):
        with_pitfalls(seed)
        dump(seed)
