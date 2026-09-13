# itemfactory/tools/mkseed_m1_number2.py — m1-1 수와 연산 기본 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m1_number2.py
#     → seeds/m1-1-prime-factor.json   (소인수분해: 지수 합·약수의 개수·제곱수 만들기·지수 역산·소인수의 합, 6틀)
#     → seeds/m1-1-gcd-lcm-basic.json  (최대공약수·최소공배수 기본: 인수형 G·공약수 개수·L·지수 미지수·나머지 조건·분수, 7틀)
#     → seeds/m1-1-rational-ops.json   (유리수 계산: 거듭제곱 혼합·분수 혼합·잘못 계산·역수·크고 작은 수, 5틀)
#
# 소인수분해 문자열(2³ × 3 × 5)처럼 식으로 못 만드는 것은 파이썬에서 굽어 표(table)로 넣는다 (SEEDSPEC "표 파생").
from __future__ import annotations

import math
import os
import sys
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
PRIMES = [2, 3, 5, 7, 11, 13]


def sup(n: int) -> str:
    return "" if n == 1 else str(n).translate(SUP)


def fac(n: int) -> dict:
    d, m, p = {}, n, 2
    while p * p <= m:
        while m % p == 0:
            m //= p
            d[p] = d.get(p, 0) + 1
        p += 1
    if m > 1:
        d[m] = d.get(m, 0) + 1
    return d


def fstr(n: int) -> str:
    """12 → '2² × 3'"""
    return " × ".join(f"{p}{sup(e)}" for p, e in sorted(fac(n).items())) if n > 1 else "1"


def ndiv(n: int) -> int:
    out = 1
    for e in fac(n).values():
        out *= e + 1
    return out


def dstr(n: int) -> str:
    """약수의 개수 계산식 '(3 + 1) × (1 + 1)'"""
    return " × ".join(f"({e} + 1)" for _, e in sorted(fac(n).items()))


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


NUM_BASE = {"process": "절차수행", "context": "무맥락", "ops": ["인수분해", "사칙"], "traps": ["조건누락", "구하는대상혼동"],
            "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}

# ═══════════════════════════════════════════════════════════════════ 1. 소인수분해
PF = "m1-1-prime-factor"
PF_BASE = {**NUM_BASE, "prereq": ["소인수분해", "거듭제곱"], "tags": ["소인수분해"]}

PQ_ROWS = {"23": {"p": 2, "q": 3}, "25": {"p": 2, "q": 5}, "35": {"p": 3, "q": 5}, "27": {"p": 2, "q": 7}}
Q1_ROWS = {"sum": {"QT": "a + b + c", "s1": 1, "s2": 1, "s3": 1, "m1": 0},
           "prod": {"QT": "a × b × c", "s1": 0, "s2": 0, "s3": 0, "m1": 1},
           "diff": {"QT": "c − a − b", "s1": -1, "s2": -1, "s3": 1, "m1": 0}}
SUPA = {"key": "a", "rows": {str(i): {"SA": sup(i)} for i in range(1, 7)}}
SUPB = {"key": "b", "rows": {str(i): {"SB": sup(i)} for i in range(1, 7)}}


def pf_t1():
    return tpl(PF, 1, PF_BASE,
        title="N = pᵃ × qᵇ × c 꼴의 소인수분해 — 지수와 소인수로 만든 식의 값",
        skill="자연수를 소인수분해하여 각 소인수의 지수를 읽고, 묻는 식(a + b + c 등)의 값을 구하기",
        variant_axis={"구하는 것": "a + b + c / a × b × c / c − a − b", "밑": "(2, 3)·(2, 5)·(3, 5)·(2, 7)", "지수": "a 1~5 · b 1~3"},
        discriminates="같은 소인수끼리 모아 지수로 나타내고, 지수와 소인수(밑)를 구분해 읽는가",
        difficulty=2,
        params=[{"name": "q1", "values": {"in": list(Q1_ROWS)}}, {"name": "pq", "values": {"in": list(PQ_ROWS)}},
                {"name": "a", "values": {"int": [1, 5]}}, {"name": "b", "values": {"int": [1, 3]}}, {"name": "c", "values": {"in": [5, 7, 11, 13]}}],
        table=[{"key": "q1", "rows": Q1_ROWS}, {"key": "pq", "rows": PQ_ROWS}, SUPA, SUPB],
        derive={"N": "p**a * q**b * c", "pa": "p**a", "qb": "q**b", "ans": "(1 - m1)*(s1*a + s2*b + s3*c) + m1*a*b*c"},
        constraints=["c != p", "c != q", "N <= 5000", "ans > 0", "ans != N", "ans != p", "ans != q"],
        cost_values=["N", "a", "b", "c", "ans"],
        answer_var="ans",
        verify=["N == p**a * q**b * c", "ans == (1 - m1)*(s1*a + s2*b + s3*c) + m1*a*b*c", "isprime(c)"],
        question="{N}{eul(N)} 소인수분해하면 {p}ᵃ × {q}ᵇ × c (a, b는 자연수, c는 {p}, {q}{wa(q)} 다른 소수)일 때, {QT}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="소인수분해는 자연수를 소수들만의 곱으로 나타내는 것이다. {N}{eul(N)} 가장 작은 소수부터 차례로 나누어 소인수를 모두 찾은 뒤, 같은 소인수는 거듭제곱으로 묶는다. 그러면 {p}의 지수가 a, {q}의 지수가 b, 남은 소인수가 c이므로 그 값을 {QT}에 넣는다.",
        sol2=[
            "{N}{eul(N)} 소수로 차례로 나누면 {N} = {p}{SA} × {q}{SB} × {c}",
            "따라서 {p}의 지수는 a = {a}, {q}의 지수는 b = {b}, 남은 소인수는 c = {c}",
            "{QT} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{N} = {p}{SA} × {q}{SB} × {c}", "hint": "작은 소수부터 나눈다"},
            {"text": "a = {a},  b = {b},  c = {c}", "hint": "지수 · 지수 · 남은 소인수"},
            {"text": "{QT} = {ans}", "marks": [{"on": "{ans}", "note": "지수와 밑을 바꾸지 말 것"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="거꾸로 곱해 보면 {p}{SA} × {q}{SB} × {c} = {pa} × {qb} × {c} = {N}{ro(N)} 원래 수와 같다. 따라서 a = {a}, b = {b}, c = {c}이고 {QT} = {ans}이다.",
        sol3_fig=steps(["{pa} × {qb} × {c} = {N}", "{QT} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{N} = {p}{SA} × {q}{SB} × {c}이므로 a = {a}, b = {b}, c = {c}이다. 따라서 {QT} = {ans}이다.",
        rubric=[
            {"element": "소인수분해", "points": 3, "criterion": "{N}{eul(N)} {p}{SA} × {q}{SB} × {c}{ro(c)} 바르게 소인수분해했다.", "partial": "소인수는 모두 찾았으나 지수를 잘못 셌으면 1점."},
            {"element": "지수와 소인수 읽기", "points": 2, "criterion": "a = {a}, b = {b}, c = {c}{ro(c)} 대응시켰다.", "partial": "밑과 지수를 바꿔 읽었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 구했다.", "partial": "다른 식({QT}가 아닌 것)의 값을 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def _nd_rows():
    """약수의 개수용 N 목록 — 소인수 2~3개, N ≤ 3000."""
    rows = {}
    sets = [(2, 3), (2, 5), (2, 7), (3, 5), (3, 7), (5, 7), (2, 11), (3, 11), (2, 13), (5, 11), (7, 11), (3, 13), (5, 13), (2, 3, 5), (2, 3, 7), (2, 5, 7), (3, 5, 7), (2, 3, 11), (2, 5, 11), (2, 3, 13), (2, 7, 11)]
    for ps in sets:
        ranges = [range(1, 7), range(1, 5)] + ([range(1, 3)] if len(ps) == 3 else [])
        for es in product(*ranges):
            n = 1
            for p, e in zip(ps, es):
                n *= p ** e
            if n > 6000 or n in rows.values():
                continue
            d = ndiv(n)
            rows[str(n)] = {"N": n, "FN": fstr(n), "D": d, "DS": dstr(n), "K": len(ps)}
    return rows


ND_ROWS = _nd_rows()


def pf_t2(no, fmt):
    facd = fmt == "fac"
    return tpl(PF, no, PF_BASE,
        title="약수의 개수 — " + ("소인수분해된 꼴" if facd else "자연수") + "에서 (지수 + 1)의 곱",
        skill="소인수분해 pᵃ × qᵇ 의 약수의 개수가 (a + 1) × (b + 1)임을 알고 구하기" + ("" if facd else " (먼저 소인수분해)"),
        variant_axis={"주어진 꼴": "소인수분해된 꼴" if facd else "자연수", "소인수 개수": "2·3개"},
        discriminates="약수의 개수를 지수에 1을 더한 것들의 곱으로 구하는가 (지수만 곱하거나 1을 빼지 않는가)",
        difficulty=2 if facd else 3,
        params=[{"name": "k", "values": {"in": list(ND_ROWS)}}],
        table={"key": "k", "rows": ND_ROWS},
        derive={"ans": "D"},
        constraints=["D != N", "D >= 4"],
        cost_values=["N", "D", "K"],
        answer_var="ans",
        verify=["ans == D"],
        question=("{FN}의 약수의 개수를 구하시오." if facd else "{N}의 약수의 개수를 구하시오."),
        answer="{D}", answer_alt=["{D}개"],
        sol1=("소인수분해된 수의 약수는 각 소인수를 0번부터 지수만큼 쓴 것들의 곱으로 모두 만들어진다. 소인수마다 고를 수 있는 지수가 (지수 + 1)가지이므로 약수의 개수는 (지수 + 1)들을 곱한 것이다."
              if facd else "약수를 하나하나 나열하면 빠뜨리기 쉽다. 먼저 {N}{eul(N)} 소인수분해하면, 약수는 각 소인수를 0번부터 지수만큼 쓴 것들의 곱으로 모두 만들어지므로 개수는 (지수 + 1)들의 곱이다."),
        sol2=([] if facd else ["{N}{eul(N)} 소인수분해하면 {N} = {FN}"]) + [
            "각 소인수의 지수에 1을 더해 곱하면 약수의 개수는 {DS} = {D}",
            "따라서 {N}의 약수는 모두 {D}개이다.",
        ],
        sol2_fig=steps(([] if facd else [{"text": "{N} = {FN}", "hint": "소인수분해"}]) + [
            {"text": "{DS} = {D}", "hint": "(지수 + 1)의 곱", "marks": [{"on": "+ 1", "note": "지수 0(=1)인 경우도 센다"}]},
        ]),
        sol2_anim=([[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], []] if not facd else [[reveal(0), hl("hint:0", "mark:0-0")], []]),
        sol3="예를 들어 소인수 하나가 pᵉ이면 그 약수는 1, p, p², …, pᵉ의 (e + 1)개다. {FN}에서 소인수마다 이렇게 고르는 가짓수를 곱한 {DS} = {D}{ika(D)} 약수의 개수다. 답은 {D}개다.",
        sol3_fig=steps(["소인수마다 고를 수 있는 지수: 0, 1, …, e → (e + 1)가지", "{DS} = {D}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer=("" if facd else "{N} = {FN}이므로 ") + "약수의 개수는 각 소인수의 지수에 1을 더한 것들의 곱 {DS} = {D}이다. 따라서 {D}개다.",
        rubric=([{"element": "약수의 개수 공식", "points": 3, "criterion": "약수의 개수가 각 소인수의 (지수 + 1)의 곱임을 밝히고 {DS} 꼴로 나타냈다.", "partial": "지수만 곱하거나 1을 더하지 않았으면 인정하지 않는다."},
                 {"element": "답 구하기", "points": 2, "criterion": "{DS} = {D}{eul(D)} 계산해 {D}개로 답했다.", "partial": "곱셈 실수면 1점."}]
                if facd else
                [{"element": "소인수분해", "points": 3, "criterion": "{N} = {FN} 꼴로 바르게 소인수분해했다.", "partial": "소인수는 맞으나 지수가 틀렸으면 1점."},
                 {"element": "약수의 개수 공식", "points": 2, "criterion": "약수의 개수가 각 소인수의 (지수 + 1)의 곱임을 써서 {DS} 꼴로 나타냈다.", "partial": "지수만 곱하거나 1을 더하지 않았으면 인정하지 않는다."},
                 {"element": "답 구하기", "points": 2, "criterion": "{D}개를 답으로 썼다.", "partial": "곱셈 실수면 1점."}]),
        rubric_total=5 if facd else 7,
    )


def _sq_rows():
    """제곱수 만들기 — 지수가 홀수인 소인수가 있는 N (N ≤ 1500), x = 홀수 지수 소인수의 곱."""
    rows = {}
    for n in range(2, 1501):
        f = fac(n)
        if len(f) > 3 or max(f) > 13:
            continue
        odd = [p for p, e in f.items() if e % 2 == 1]
        if not odd:
            continue
        x = 1
        for p in odd:
            x *= p
        if x == n:
            continue                                            # x = N 이면 답이 문면에 노출(R-05)
        r = math.isqrt(n * x)
        rows[str(n)] = {"N": n, "FN": fstr(n), "x": x, "ODD": " × ".join(str(p) for p in odd), "RM": r, "RQ": math.isqrt(n // x),
                        "FM": fstr(n * x), "FQ": fstr(n // x), "M": n * x, "Q": n // x}
    return rows


SQ_ROWS = _sq_rows()
OP_ROWS = {"mul": {"OPW": "곱하여", "OPS": "×", "isD": 0, "RES": "곱", "NOTE": "지수가 홀수인 소인수를 하나씩 더 곱하면 모든 지수가 짝수가 된다"},
           "div": {"OPW": "나누어", "OPS": "÷", "isD": 1, "RES": "몫", "NOTE": "지수가 홀수인 소인수로 나누면 모든 지수가 짝수가 된다"}}


def pf_t4():
    return tpl(PF, 4, PF_BASE,
        title="어떤 자연수의 제곱이 되게 하는 가장 작은 자연수 — 곱하기·나누기",
        skill="제곱수는 소인수분해했을 때 모든 지수가 짝수임을 알고, 지수가 홀수인 소인수들의 곱을 구하기",
        variant_axis={"연산": "곱하기 / 나누기", "N": "소인수 2~3개, 1500 이하"},
        discriminates="'모든 지수가 짝수'라는 제곱수의 조건을 쓰는가, 홀수 지수의 소인수를 빠짐없이 모으는가",
        difficulty=3,
        params=[{"name": "op", "values": {"in": list(OP_ROWS)}}, {"name": "k", "values": {"in": list(SQ_ROWS)}}],
        table=[{"key": "op", "rows": OP_ROWS}, {"key": "k", "rows": SQ_ROWS}],
        derive={"ans": "x", "R": "(1 - isD)*M + isD*Q", "RR": "(1 - isD)*RM + isD*RQ", "SQN": "isD*RQ*RQ + (1 - isD)*RM*RM"},
        constraints=["x >= 2", "isD == 0 or x < N", "x != N"],
        cost_values=["N", "x", "R"],
        answer_var="ans",
        verify=["ans == x", "sqrt(N*x) == floor(sqrt(N*x))", "isD == 0 or sqrt(N/x) == floor(sqrt(N/x))", "SQN == R"],
        question="{N}에 자연수 x를 {OPW} 어떤 자연수의 제곱이 되게 하려고 한다. 가장 작은 자연수 x의 값을 구하시오.",
        answer="{x}", answer_alt=[],
        sol1="어떤 자연수의 제곱은 소인수분해했을 때 모든 소인수의 지수가 짝수다. {N}{eul(N)} 소인수분해해서 지수가 홀수인 소인수를 찾으면, {NOTE}. 그 소인수들을 곱한 것이 가장 작은 x다.",
        sol2=[
            "{N}{eul(N)} 소인수분해하면 {N} = {FN}",
            "지수가 홀수인 소인수는 {ODD}이다.",
            "따라서 x = {ODD} = {x}{ika(x)} 가장 작고, 그때 {N} {OPS} {x} = {R} = {RR}²이다.",
        ],
        sol2_fig=steps([
            {"text": "{N} = {FN}", "hint": "소인수분해"},
            {"text": "지수가 홀수인 소인수: {ODD}", "hint": "제곱수 = 모든 지수가 짝수"},
            {"text": "x = {x},  {N} {OPS} {x} = {R} = {RR}²", "marks": [{"on": "{RR}²", "note": "제곱수 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{N} {OPS} {x} = {R}{ika(R)} {RR}² = {R}{ro(R)} 실제로 제곱수이다. x보다 작은 자연수를 {OPW} 만든 수는 홀수 지수의 소인수가 남아 제곱수가 되지 않으므로 답은 {x}이다.",
        sol3_fig=steps(["{N} {OPS} {x} = {R}", "{R} = {RR} × {RR} = {RR}²"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{N} = {FN}에서 지수가 홀수인 소인수는 {ODD}이므로, 가장 작은 자연수 x는 {ODD} = {x}이다. 실제로 {N} {OPS} {x} = {R} = {RR}²이다.",
        rubric=[
            {"element": "소인수분해", "points": 2, "criterion": "{N} = {FN} 꼴로 소인수분해했다.", "partial": "지수가 틀렸으면 1점."},
            {"element": "제곱수의 조건", "points": 3, "criterion": "모든 지수가 짝수여야 함을 근거로 지수가 홀수인 소인수({ODD})를 모두 찾았다.", "partial": "홀수 지수의 소인수를 일부만 찾았으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "x = {x}{eul(x)} 답으로 썼다.", "partial": "{N} {OPS} {x}의 값 {R}{eul(R)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def _ex_rows():
    """지수 역산 — 미지수 지수 a 가 붙은 소인수와 지수 k 가 알려진 소인수(+ 선택 소인수 r), 오름차순 표시. 행에 k·자리까지 굽는다."""
    rows = {}
    pairs = [(2, 3), (2, 5), (2, 7), (3, 5), (3, 7), (5, 7)]
    for p, q in pairs:
        for r in (0, 5, 7, 11):
            if r and r <= q:
                continue
            for k in (1, 2, 3):
                for pos in ("first", "second"):
                    # pos=first: 미지수가 작은 소인수 p 에, second: 큰 소인수 q 에
                    if pos == "first":
                        FQ = f"{p}ᵃ × {q}{sup(k)}" + (f" × {r}" if r else "")
                        P, Q = p, q
                    else:
                        FQ = f"{p}{sup(k)} × {q}ᵃ" + (f" × {r}" if r else "")
                        P, Q = q, p
                    key = f"{p}-{q}-{r}-{k}-{pos}"
                    rows[key] = {"p": P, "q": Q, "r": r, "k": k, "hasR": 1 if r else 0, "FQ": FQ, "RC": " × (1 + 1)" if r else "", "M": (k + 1) * (2 if r else 1)}
    return rows


EX_ROWS = _ex_rows()
SUPK = {"key": "k", "rows": {str(i): {"SK": sup(i)} for i in range(1, 5)}}


def pf_t5():
    return tpl(PF, 5, PF_BASE,
        title="약수의 개수가 주어질 때 미지수 지수 a 구하기",
        skill="pᵃ × qᵏ 의 약수의 개수 (a + 1)(k + 1)을 주어진 개수와 같게 놓고 a를 구하기",
        variant_axis={"소인수": "2·3·5·7 조합", "세 번째 소인수": "없음 / 있음", "k": "1~3"},
        discriminates="약수의 개수 식을 세우고 (a + 1)을 구한 뒤 1을 빼서 a를 얻는가",
        difficulty=3,
        params=[{"name": "e", "values": {"in": list(EX_ROWS)}}, {"name": "a", "values": {"int": [1, 6]}}],
        table={"key": "e", "rows": EX_ROWS},
        derive={"D": "(a + 1)*M", "A1": "a + 1", "ans": "a"},
        constraints=["a != k", "a != p", "a != q", "a != r", "a != D", "D != p", "D != q", "D != r"],
        cost_values=["D", "a", "k", "hasR"],
        answer_var="ans",
        verify=["ans == a", "(ans + 1)*(k + 1)*(1 + hasR) == D", "M == (k + 1)*(1 + hasR)"],
        question="{FQ}의 약수의 개수가 {D}일 때, 자연수 a의 값을 구하시오.",
        answer="{a}", answer_alt=[],
        sol1="소인수분해된 수의 약수의 개수는 (각 소인수의 지수 + 1)을 모두 곱한 것이다. 지수 a를 모르므로 개수를 a의 식 (a + 1) × {M}{ro(M)} 세워 {D}{wa(D)} 같게 놓고 푼다. 마지막에 a + 1이 아니라 a를 답하는 것에 주의한다.",
        sol2=[
            "약수의 개수는 (a + 1) × ({k} + 1){RC} = (a + 1) × {M}",
            "이것이 {D}이므로 (a + 1) × {M} = {D}, a + 1 = {A1}",
            "따라서 a = {a}",
        ],
        sol2_fig=steps([
            {"text": "(a + 1) × ({k} + 1){RC} = {D}", "hint": "약수의 개수 = (지수 + 1)의 곱"},
            {"text": "a + 1 = {D} ÷ {M} = {A1}", "hint": "{M}{ro(M)} 나눈다"},
            {"text": "a = {a}", "marks": [{"on": "{a}", "note": "a + 1 이 아니라 a"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="a = {a}{eul(a)} 넣으면 약수의 개수는 ({a} + 1) × ({k} + 1){RC} = {A1} × {M} = {D}{ro(D)} 주어진 개수와 같다. 답은 {a}이다.",
        sol3_fig=steps(["({a} + 1) × ({k} + 1){RC} = {D}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="약수의 개수는 (a + 1) × ({k} + 1){RC} = (a + 1) × {M}이고 이것이 {D}이므로 a + 1 = {A1}, a = {a}이다.",
        rubric=[
            {"element": "약수의 개수 식", "points": 3, "criterion": "약수의 개수를 (a + 1) × ({k} + 1){RC} 꼴로 나타내고 {D}{wa(D)} 같게 놓았다.", "partial": "일부 소인수의 (지수 + 1)을 빠뜨렸으면 1점."},
            {"element": "a 구하기", "points": 2, "criterion": "a + 1 = {A1}에서 a = {a}{eul(a)} 구했다.", "partial": "a + 1 = {A1}{eul(A1)} 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def _ps_rows():
    rows = {}
    for n in range(6, 2001):
        f = fac(n)
        if len(f) < 2 or max(f) > 31:
            continue
        s = sum(f)
        rows[str(n)] = {"N": n, "FN": fstr(n), "S": s, "PL": ", ".join(str(p) for p in sorted(f)), "PS": " + ".join(str(p) for p in sorted(f)), "K": len(f),
                        "ES": sum(f.values())}
    return rows


PS_ROWS = _ps_rows()
PS_Q = {"sum": {"QT": "모든 소인수의 합", "isS": 1}, "cnt": {"QT": "서로 다른 소인수의 개수", "isS": 0}}


def pf_t6():
    return tpl(PF, 6, PF_BASE,
        title="자연수의 소인수 — 모든 소인수의 합·서로 다른 소인수의 개수",
        skill="소인수분해하여 소인수(밑)만 골라 합하거나 세기 (지수·약수와 혼동하지 않기)",
        variant_axis={"구하는 것": "소인수의 합 / 소인수의 개수", "N": "2000 이하, 소인수 2개 이상"},
        discriminates="소인수(밑)와 약수·지수를 구별하는가, 같은 소인수를 한 번만 세는가",
        difficulty=2,
        params=[{"name": "q", "values": {"in": list(PS_Q)}}, {"name": "k", "values": {"in": list(PS_ROWS)}}],
        table=[{"key": "q", "rows": PS_Q}, {"key": "k", "rows": PS_ROWS}],
        derive={"ans": "isS*S + (1 - isS)*K"},
        constraints=["ans != N", "isS == 1 or ES != K"],
        cost_values=["N", "S", "K"],
        answer_var="ans",
        verify=["ans == isS*S + (1 - isS)*K"],
        question="{N}의 {QT}{eul(QT)} 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="소인수는 어떤 수의 약수 중 소수인 것이다. {N}{eul(N)} 소인수분해하면 곱에 나타나는 밑들이 바로 소인수이고, 같은 소인수가 여러 번 곱해져 있어도 소인수로는 하나로 센다. 약수의 개수나 지수의 합과 헷갈리지 않도록 한다.",
        sol2=[
            "{N}{eul(N)} 소인수분해하면 {N} = {FN}",
            "따라서 {N}의 소인수는 {PL}이다.",
            "{QT}{eun(QT)} {ans}이다.",
        ],
        sol2_fig=steps([
            {"text": "{N} = {FN}", "hint": "소인수분해"},
            {"text": "소인수: {PL}", "hint": "밑만 고른다 (거듭제곱은 하나로)"},
            {"text": "{QT} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="{PL}{eun(PL)} 모두 소수이고 각각 {N}{eul(N)} 나누어떨어지게 하므로 소인수가 맞다. {N} = {FN}에 이 밖의 소수는 나타나지 않으므로 {QT}{eun(QT)} {ans}이다.",
        sol3_fig=steps(["{N} = {FN}", "소인수 {PL} → {QT} {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{N} = {FN}이므로 {N}의 소인수는 {PL}이다. 따라서 {QT}{eun(QT)} {ans}이다.",
        rubric=[
            {"element": "소인수분해", "points": 3, "criterion": "{N} = {FN} 꼴로 소인수분해했다.", "partial": "소인수는 맞으나 지수가 틀렸으면 2점."},
            {"element": "소인수 고르기와 답 구하기", "points": 2, "criterion": "소인수 {PL}{eul(PL)} 골라 {QT} {ans}{eul(ans)} 구했다.", "partial": "약수나 지수를 소인수로 잘못 셌으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


PF_SEED = {
    "seed_id": PF, "category": "연산",
    "title": "소인수분해 — 지수 읽기·약수의 개수·제곱수 만들기·지수 역산·소인수",
    "unit_id": "m1-1", "concept_ids": ["m1-1-03", "m1-1-04"],
    "schema_id": None, "schema_name": "소인수분해와 약수의 개수",
    "source_item_ids": [],
    "note": "구조만 차용. 소인수분해 문자열·약수 개수식·홀수 지수 소인수는 파이썬에서 굽어 표로 넣는다. x = N(제곱수 만들기)은 R-05라 뺀다.",
    "geometry": False,
    "templates": [pf_t1(), pf_t2(2, "int"), pf_t2(3, "fac"), pf_t4(), pf_t5(), pf_t6()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 최대공약수·최소공배수 기본
GL = "m1-1-gcd-lcm-basic"
GL_BASE = {**NUM_BASE, "prereq": ["소인수분해", "공약수와 최대공약수", "공배수와 최소공배수"], "tags": ["최대공약수", "최소공배수"]}


def _pair_rows():
    """소인수분해 꼴 두 수 (A, B) — 소인수 {2,3,5,7}, 각각 소인수 2개 이상, A·B ≤ 1000, G > 1, L ≤ 5000."""
    rows = {}
    ps = [2, 3, 5, 7]
    for ea in product(range(0, 4), range(0, 3), range(0, 2), range(0, 2)):
        A = 1
        for p, e in zip(ps, ea):
            A *= p ** e
        if A > 1000 or sum(1 for e in ea if e) < 2:
            continue
        for eb in product(range(0, 4), range(0, 3), range(0, 2), range(0, 2)):
            B = 1
            for p, e in zip(ps, eb):
                B *= p ** e
            if B > 1000 or sum(1 for e in eb if e) < 2 or B == A or B < A:
                continue
            g, L = math.gcd(A, B), A * B // math.gcd(A, B)
            if g < 4 or L > 5000 or g in (A, B):
                continue
            rows[f"{A}-{B}"] = {"A": A, "B": B, "FA": fstr(A), "FB": fstr(B), "G": g, "FG": fstr(g), "L": L, "FL": fstr(L), "DG": ndiv(g), "DS": dstr(g),
                                "GD": ", ".join(str(d) for d in range(1, g + 1) if g % d == 0)}
    return rows


PAIR_ROWS = _pair_rows()
PAIR_PARAM = {"name": "k", "values": {"in": list(PAIR_ROWS)}}


def gl_t1():
    return tpl(GL, 1, GL_BASE,
        title="소인수분해된 두 수의 최대공약수 — 공통 소인수의 작은 지수",
        skill="두 수의 소인수분해에서 공통인 소인수마다 지수가 작은(같은) 쪽을 택해 곱하기",
        variant_axis={"소인수": "2·3·5·7 조합", "지수": "1~3"},
        discriminates="공통 소인수만 고르고 지수는 작은 쪽을 택하는가 (최소공배수 규칙과 혼동하지 않는가)",
        difficulty=2,
        params=[PAIR_PARAM], table={"key": "k", "rows": PAIR_ROWS},
        derive={"ans": "G"},
        constraints=["G != 5", "G != 7"],
        cost_values=["A", "B", "G"],
        answer_var="ans",
        verify=["ans == G", "gcd(A, B) == G"],
        question="두 수 {FA}, {FB}의 최대공약수를 구하시오.",
        answer="{G}", answer_alt=["{FG}"],
        sol1="최대공약수는 두 수에 공통으로 들어 있는 소인수를 모두 곱한 것이다. 소인수분해된 꼴에서 두 수에 모두 있는 소인수를 고르고, 소인수마다 지수가 작은 쪽(같으면 그 지수)을 택해 곱한다. 한쪽에만 있는 소인수는 공약수가 될 수 없으므로 뺀다.",
        sol2=[
            "두 수 {FA}({A})와 {FB}({B})에 공통인 소인수를 찾는다.",
            "공통인 소인수마다 지수가 작은 쪽을 택하면 최대공약수는 {FG}",
            "따라서 최대공약수는 {FG} = {G}이다.",
        ],
        sol2_fig=steps([
            {"text": "{FA}", "hint": "A"},
            {"text": "{FB}", "hint": "B"},
            {"text": "최대공약수 = {FG} = {G}", "hint": "공통 소인수 · 작은 지수", "marks": [{"on": "{G}", "note": "한쪽에만 있는 소인수는 제외"}]},
        ]),
        sol2_anim=[[reveal(0), reveal(1)], [reveal(2), hl("hint:2")], [hl("mark:2-0")]],
        sol3="{G}{eun(G)} {A} ÷ {G} = {A/G}, {B} ÷ {G} = {B/G}{ro(B/G)} 두 수를 모두 나누어떨어지게 하고, {A/G}{wa(A/G)} {B/G}{eun(B/G)} 서로소이므로 이보다 큰 공약수는 없다. 답은 {G}이다.",
        sol3_fig=steps(["{A} ÷ {G} = {A/G},  {B} ÷ {G} = {B/G}", "{A/G}{wa(A/G)} {B/G}{eun(B/G)} 서로소"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="두 수에 공통인 소인수마다 지수가 작은 쪽을 택해 곱하면 최대공약수는 {FG} = {G}이다.",
        rubric=[
            {"element": "공통 소인수와 지수 선택", "points": 3, "criterion": "두 수에 공통인 소인수를 고르고 소인수마다 작은 지수를 택해 {FG} 꼴로 나타냈다.", "partial": "공통 소인수는 맞으나 큰 지수를 택했으면(최소공배수 규칙) 인정하지 않고, 지수 하나만 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{FG} = {G}{eul(G)} 답으로 썼다.", "partial": "곱셈 실수면 1점."},
        ],
        rubric_total=5,
    )


def gl_t2():
    return tpl(GL, 2, GL_BASE,
        title="두 수의 공약수의 개수 — 최대공약수의 약수의 개수",
        skill="공약수는 최대공약수의 약수임을 알고, 최대공약수를 소인수분해해 약수의 개수 공식으로 세기",
        variant_axis={"소인수": "2·3·5·7 조합"},
        discriminates="'공약수 = 최대공약수의 약수'를 근거로 쓰는가, 약수의 개수를 (지수 + 1)의 곱으로 구하는가",
        difficulty=3,
        params=[PAIR_PARAM], table={"key": "k", "rows": PAIR_ROWS},
        derive={"ans": "DG"},
        constraints=["DG >= 4", "DG != 5", "DG != 7", "DG != G"],
        cost_values=["A", "B", "G", "DG"],
        answer_var="ans",
        verify=["ans == DG", "gcd(A, B) == G"],
        question="두 수 {FA}, {FB}의 공약수는 모두 몇 개인지 구하시오.",
        answer="{DG}", answer_alt=["{DG}개"],
        sol1="두 수의 공약수는 두 수의 최대공약수의 약수와 같다. 그러므로 먼저 최대공약수를 소인수분해된 꼴로 구하고, 그 약수의 개수를 (지수 + 1)의 곱으로 세면 공약수의 개수가 된다. 공약수를 일일이 나열하지 않아도 된다.",
        sol2=[
            "공통인 소인수마다 작은 지수를 택하면 최대공약수는 {FG} = {G}",
            "두 수의 공약수는 최대공약수 {G}의 약수와 같으므로, 그 개수는 {DS} = {DG}",
            "따라서 공약수는 모두 {DG}개이다.",
        ],
        sol2_fig=steps([
            {"text": "최대공약수 = {FG} = {G}", "hint": "공통 소인수 · 작은 지수"},
            {"text": "공약수 = {G}의 약수", "hint": "근거"},
            {"text": "{DS} = {DG}", "hint": "약수의 개수 = (지수 + 1)의 곱"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")]],
        sol3="{G}의 약수를 나열하면 {GD}의 {DG}개이고, 이들은 모두 {A}{wa(A)} {B}{eul(B)} 나누어떨어지게 한다. 답은 {DG}개다.",
        sol3_fig=steps(["{G}의 약수: {GD}", "→ {DG}개"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="최대공약수는 {FG} = {G}이고 두 수의 공약수는 최대공약수의 약수와 같다. 따라서 공약수의 개수는 {G}의 약수의 개수 {DS} = {DG}개다.",
        rubric=[
            {"element": "최대공약수 구하기", "points": 2, "criterion": "최대공약수 {FG} = {G}{eul(G)} 구했다.", "partial": "지수 하나가 틀렸으면 1점."},
            {"element": "공약수와 최대공약수의 관계", "points": 3, "criterion": "공약수가 최대공약수의 약수임을 밝히고 약수의 개수를 {DS} 꼴로 나타냈다.", "partial": "관계를 밝히지 않고 나열만 했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{DG}개를 답으로 썼다.", "partial": "최대공약수 {G}{eul(G)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def gl_t3():
    return tpl(GL, 3, GL_BASE,
        title="소인수분해된 두 수의 최소공배수 — 모든 소인수의 큰 지수",
        skill="두 수의 소인수분해에 나오는 모든 소인수를 쓰되 소인수마다 지수가 큰 쪽을 택해 곱하기",
        variant_axis={"소인수": "2·3·5·7 조합", "지수": "1~3"},
        discriminates="한쪽에만 있는 소인수도 포함하고 지수는 큰 쪽을 택하는가 (최대공약수 규칙과 혼동하지 않는가)",
        difficulty=2,
        params=[PAIR_PARAM], table={"key": "k", "rows": PAIR_ROWS},
        derive={"ans": "L"},
        constraints=["L <= 3000"],
        cost_values=["A", "B", "L"],
        answer_var="ans",
        verify=["ans == L", "lcm(A, B) == L"],
        question="두 수 {FA}, {FB}의 최소공배수를 구하시오.",
        answer="{L}", answer_alt=["{FL}"],
        sol1="최소공배수는 두 수의 배수가 되는 가장 작은 수이므로 두 수의 소인수를 모두 갖되, 소인수마다 지수가 큰 쪽(같으면 그 지수)만큼 갖는다. 한쪽에만 있는 소인수도 빠뜨리지 말고 넣어야 한다.",
        sol2=[
            "두 수 {FA}({A})와 {FB}({B})에 나오는 소인수를 모두 쓴다.",
            "소인수마다 지수가 큰 쪽을 택하면 최소공배수는 {FL}",
            "따라서 최소공배수는 {FL} = {L}이다.",
        ],
        sol2_fig=steps([
            {"text": "{FA}", "hint": "A"},
            {"text": "{FB}", "hint": "B"},
            {"text": "최소공배수 = {FL} = {L}", "hint": "모든 소인수 · 큰 지수", "marks": [{"on": "{L}", "note": "한쪽에만 있는 소인수도 포함"}]},
        ]),
        sol2_anim=[[reveal(0), reveal(1)], [reveal(2), hl("hint:2")], [hl("mark:2-0")]],
        sol3="{L} = {A} × {L/A} = {B} × {L/B}{ro(L/B)} 두 수의 공배수이고, 두 수의 최대공약수가 {G}이므로 (두 수의 곱) ÷ (최대공약수) = {A} × {B} ÷ {G} = {L}{ro(L)} 맞는다. 답은 {L}이다.",
        sol3_fig=steps(["{A} × {L/A} = {L},  {B} × {L/B} = {L}", "{A} × {B} ÷ {G} = {L}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="두 수의 소인수를 모두 쓰고 소인수마다 지수가 큰 쪽을 택해 곱하면 최소공배수는 {FL} = {L}이다.",
        rubric=[
            {"element": "소인수와 지수 선택", "points": 3, "criterion": "두 수의 소인수를 모두 쓰고 소인수마다 큰 지수를 택해 {FL} 꼴로 나타냈다.", "partial": "한쪽에만 있는 소인수를 빠뜨렸거나 작은 지수를 택했으면 인정하지 않고, 지수 하나만 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{FL} = {L}{eul(L)} 답으로 썼다.", "partial": "곱셈 실수면 1점."},
        ],
        rubric_total=5,
    )


def _ex2_rows():
    """지수 미지수 — A = pᵃ × q^e1 (× r), B = p^e2 × qᵇ (× s). G·L 은 문자열로 굽는다."""
    rows = {}
    pq = [(2, 3), (2, 5), (3, 2), (3, 5), (5, 2), (5, 3)]
    for p, q in pq:
        for r in (0, 5, 7):
            for s in (0, 7, 11):
                if r in (p, q) or s in (p, q) or (r and r == s):
                    continue
                for e1, e2 in product(range(1, 4), range(1, 4)):
                    for a, b in product(range(1, 5), range(1, 5)):
                        gp, lp = min(a, e2), max(a, e2)
                        gq, lq = min(e1, b), max(e1, b)
                        A = p ** a * q ** e1 * (r or 1)
                        B = p ** e2 * q ** b * (s or 1)
                        G = p ** gp * q ** gq
                        L = p ** lp * q ** lq * (r or 1) * (s or 1)
                        FA = f"{p}ᵃ × {q}{sup(e1)}" + (f" × {r}" if r else "")
                        FB = f"{p}{sup(e2)} × {q}ᵇ" + (f" × {s}" if s else "")
                        key = f"{p}{q}{r}{s}-{e1}{e2}-{a}{b}"
                        rows[key] = {"p": p, "q": q, "r": r, "s": s, "e1": e1, "e2": e2, "a": a, "b": b, "FA": FA, "FB": FB, "FG": fstr(G), "FL": fstr(L),
                                     "gp": gp, "lp": lp, "gq": gq, "lq": lq, "A": A, "B": B, "G": G, "L": L}
    return rows


EX2_ROWS = _ex2_rows()


def gl_t4():
    return tpl(GL, 4, GL_BASE,
        title="최대공약수·최소공배수가 주어질 때 미지수 지수 a, b 구하기",
        skill="소인수마다 최대공약수의 지수 = 작은 쪽, 최소공배수의 지수 = 큰 쪽임을 이용해 a, b를 정하기",
        variant_axis={"소인수": "2·3·5 조합 + 다른 소인수", "지수": "1~4"},
        discriminates="같은 소인수의 지수를 최대공약수·최소공배수와 각각 비교해 a, b를 정하는가",
        difficulty=3,
        params=[{"name": "k", "values": {"in": list(EX2_ROWS)}}], table={"key": "k", "rows": EX2_ROWS},
        derive={"ans": "a + b"},
        constraints=["ans != p", "ans != q", "ans != r", "ans != s", "L <= 20000"],
        cost_values=["a", "b", "e1", "e2", "ans"],
        answer_var="ans",
        verify=["ans == a + b", "gcd(A, B) == G", "lcm(A, B) == L"],
        question="두 수 {FA}, {FB}의 최대공약수가 {FG}, 최소공배수가 {FL}일 때, 자연수 a, b에 대하여 a + b의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="소인수분해된 두 수에서 최대공약수는 공통 소인수마다 작은 지수, 최소공배수는 소인수마다 큰 지수를 택한 것이다. 그러므로 소인수 {p}에 대해 지수 a와 {e2}{eul(e2)} 최대공약수의 지수 {gp}·최소공배수의 지수 {lp}{wa(lp)} 비교하면 a가 정해지고, 소인수 {q}에 대해 같은 방법으로 b가 정해진다.",
        sol2=[
            "소인수 {p}의 지수: 두 수에서 a와 {e2}, 최대공약수에서 {gp}, 최소공배수에서 {lp} → a와 {e2} 중 작은 것이 {gp}, 큰 것이 {lp}이므로 a = {a}",
            "소인수 {q}의 지수: 두 수에서 {e1}{wa(e1)} b, 최대공약수에서 {gq}, 최소공배수에서 {lq} → b = {b}",
            "따라서 a + b = {a} + {b} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{p}: (a, {e2}) → 작은 쪽 {gp}, 큰 쪽 {lp}  ⇒  a = {a}", "hint": "최대공약수는 작은 지수, 최소공배수는 큰 지수"},
            {"text": "{q}: ({e1}, b) → 작은 쪽 {gq}, 큰 쪽 {lq}  ⇒  b = {b}"},
            {"text": "a + b = {ans}", "marks": [{"on": "{ans}", "note": "a, b가 아니라 a + b"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("mark:2-0")]],
        sol3="a = {a}, b = {b}{eul(b)} 넣으면 두 수는 {A}, {B}이고 실제로 최대공약수는 {G} = {FG}, 최소공배수는 {L} = {FL} 꼴로 주어진 것과 같다. 답은 {ans}이다.",
        sol3_fig=steps(["a = {a}, b = {b}  →  {A}, {B}", "최대공약수 {G} = {FG},  최소공배수 {L} = {FL}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="최대공약수는 공통 소인수의 작은 지수, 최소공배수는 큰 지수를 택한 것이므로 소인수 {p}에서 a = {a}, 소인수 {q}에서 b = {b}이다. 따라서 a + b = {ans}이다.",
        rubric=[
            {"element": "지수 비교 원리", "points": 3, "criterion": "최대공약수는 작은 지수, 최소공배수는 큰 지수라는 원리를 써서 소인수별로 지수를 비교했다.", "partial": "원리를 밝히지 않고 값만 맞췄으면 1점."},
            {"element": "a, b 구하기", "points": 2, "criterion": "a = {a}, b = {b}{eul(b)} 구했다.", "partial": "둘 중 하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "a + b = {ans}{eul(ans)} 답했다.", "partial": "a와 b를 따로 쓰고 합을 쓰지 않았으면 1점."},
        ],
        rubric_total=7,
    )


COP2 = [(u, v) for u in range(2, 10) for v in range(2, 10) if u != v and math.gcd(u, v) == 1]


def gl_t5():
    return tpl(GL, 5, GL_BASE,
        title="나누면 나머지가 남는 조건 — 가장 큰 자연수 (최대공약수)",
        skill="'A를 나누면 r이 남는다'를 '(A − r)이 나누어떨어진다'로 바꾸어 두 수의 최대공약수를 구하기",
        variant_axis={"나머지": "1~3", "최대공약수": "4~15"},
        discriminates="나머지를 빼서 나누어떨어지는 수로 바꾸는가, 답이 나머지보다 커야 함을 확인하는가",
        difficulty=3,
        params=[{"name": "g", "values": {"int": [4, 15]}}, {"name": "uv", "values": {"in": [u * 10 + v for u, v in COP2]}},
                {"name": "r1", "values": {"int": [1, 3]}}, {"name": "r2", "values": {"int": [1, 3]}}],
        derive={"u": "floor(uv/10)", "v": "uv % 10", "A": "g*floor(uv/10) + r1", "B": "g*(uv % 10) + r2", "A0": "g*floor(uv/10)", "B0": "g*(uv % 10)", "ans": "g"},
        constraints=["r1 < g", "r2 < g", "A <= 150", "B <= 150", "g != r1", "g != r2", "g != A", "g != B"],
        cost_values=["A", "B", "r1", "r2", "g"],
        answer_var="ans",
        verify=["ans == g", "gcd(A - r1, B - r2) == g", "g > r1", "g > r2", "A % g == r1", "B % g == r2"],
        question="어떤 자연수로 {A}{eul(A)} 나누면 {r1}{ika(r1)} 남고, {B}{eul(B)} 나누면 {r2}{ika(r2)} 남는다. 이러한 자연수 중 가장 큰 수를 구하시오.",
        answer="{g}", answer_alt=[],
        sol1="{A}{eul(A)} 어떤 수로 나누어 {r1}{ika(r1)} 남는다는 것은 {A} − {r1} = {A0}{ika(A0)} 그 수로 나누어떨어진다는 뜻이다. 마찬가지로 {B} − {r2} = {B0}{ika(B0)} 나누어떨어진다. 그러므로 구하는 수는 {A0}{wa(A0)} {B0}의 공약수이고, 가장 큰 것은 최대공약수다. 단, 나누는 수는 나머지보다 커야 한다.",
        sol2=[
            "{A}{eul(A)} 나누면 {r1}{ika(r1)} 남으므로 {A} − {r1} = {A0}{eun(A0)} 나누어떨어지고, {B}{eul(B)} 나누면 {r2}{ika(r2)} 남으므로 {B} − {r2} = {B0}{eun(B0)} 나누어떨어진다.",
            "구하는 수는 {A0}{wa(A0)} {B0}의 공약수 중 가장 큰 수, 곧 최대공약수이다.",
            "{A0} = {g} × {u}, {B0} = {g} × {v}이고 {u}{wa(u)} {v}{eun(v)} 서로소이므로 최대공약수는 {g}",
            "{g}{eun(g)} 나머지 {r1}, {r2}보다 크므로 조건에 맞는다. 따라서 구하는 수는 {g}이다.",
        ],
        sol2_fig=steps([
            {"text": "{A} − {r1} = {A0},  {B} − {r2} = {B0}", "hint": "나머지를 빼면 나누어떨어진다"},
            {"text": "{A0}{wa(A0)} {B0}의 최대공약수", "hint": "가장 큰 공약수"},
            {"text": "{A0} = {g} × {u},  {B0} = {g} × {v}  ⇒  {g}", "marks": [{"on": "{g}", "note": "나머지 {r1}, {r2}보다 커야 함"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)], [hl("mark:2-0")]],
        sol3="{A} ÷ {g} = {u} … {r1}, {B} ÷ {g} = {v} … {r2}{ro(r2)} 나머지가 조건과 같다. {g}보다 큰 수는 {A0}{wa(A0)} {B0}{eul(B0)} 동시에 나눌 수 없으므로 답은 {g}이다.",
        sol3_fig=steps(["{A} ÷ {g} = {u} … {r1}", "{B} ÷ {g} = {v} … {r2}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{A} − {r1} = {A0}, {B} − {r2} = {B0}{ika(B0)} 구하는 수로 나누어떨어지므로 구하는 수는 {A0}{wa(A0)} {B0}의 최대공약수이다. {A0} = {g} × {u}, {B0} = {g} × {v}이므로 최대공약수는 {g}이고, 이는 나머지 {r1}, {r2}보다 크다. 따라서 구하는 수는 {g}이다.",
        rubric=[
            {"element": "나누어떨어지는 수로 바꾸기", "points": 3, "criterion": "{A} − {r1} = {A0}, {B} − {r2} = {B0}{ika(B0)} 나누어떨어짐을 밝혔다.", "partial": "한쪽만 바꿨거나 나머지를 더했으면 1점."},
            {"element": "최대공약수 구하기", "points": 3, "criterion": "{A0}{wa(A0)} {B0}의 최대공약수 {g}{eul(g)} 구했다.", "partial": "공약수를 구했으나 가장 큰 것을 택하지 않았으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "나머지보다 큰지 확인하고 {g}{eul(g)} 답했다.", "partial": "{A}, {B}의 최대공약수를 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def _triples():
    out = []
    for a in range(3, 13):
        for b in range(a + 1, 16):
            for c in range(b + 1, 19):
                L = math.lcm(a, b, c)
                if L > 400 or L in (a, b, c) or (b % a == 0 and c % b == 0):
                    continue
                out.append((a, b, c))
    return out


TRI3 = _triples()
TRI_ROWS = {f"{a}-{b}-{c}": {"a": a, "b": b, "c": c, "L": math.lcm(a, b, c), "FA": fstr(a), "FB": fstr(b), "FC": fstr(c), "FL": fstr(math.lcm(a, b, c))} for a, b, c in TRI3}


def gl_t6():
    return tpl(GL, 6, GL_BASE,
        title="세 수 중 어느 것으로 나누어도 r이 남는 가장 작은 자연수 (최소공배수 + r)",
        skill="'어느 것으로 나누어도 r이 남는 수'는 (세 수의 공배수) + r 꼴임을 알고 최소공배수에 r을 더하기",
        variant_axis={"나머지": "1~2", "세 수": "3~18"},
        discriminates="구하는 수를 (공배수) + r 꼴로 놓는 근거를 쓰는가, 최소공배수에 r을 더하는 것을 잊지 않는가",
        difficulty=3,
        params=[{"name": "k", "values": {"in": list(TRI_ROWS)}}, {"name": "r", "values": {"int": [1, 2]}}],
        table={"key": "k", "rows": TRI_ROWS},
        derive={"ans": "L + r"},
        constraints=["r < a", "L + r != a", "L + r != b", "L + r != c"],
        cost_values=["a", "b", "c", "r", "L"],
        answer_var="ans",
        verify=["ans == L + r", "lcm(lcm(a, b), c) == L", "ans % a == r", "ans % b == r", "ans % c == r"],
        question="{a}, {b}, {c} 중 어느 수로 나누어도 나머지가 {r}인 자연수 중 가장 작은 수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{a}, {b}, {c}{ro(c)} 나누어 모두 {r}{ika(r)} 남는 수에서 {r}{eul(r)} 빼면 세 수 모두로 나누어떨어진다. 그러므로 구하는 수는 (세 수의 공배수) + {r} 꼴이고, 가장 작은 것은 최소공배수에 {r}{eul(r)} 더한 수다. 최소공배수를 답하고 끝내지 않도록 한다.",
        sol2=[
            "구하는 수를 x라 하면 x − {r}{eun(r)} {a}, {b}, {c}{ro(c)} 모두 나누어떨어지므로 세 수의 공배수이다.",
            "{a} = {FA}, {b} = {FB}, {c} = {FC}이므로 최소공배수는 {FL} = {L}",
            "x − {r}{ika(r)} 가장 작으려면 최소공배수 {L}이어야 하므로 x = {L} + {r} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "x − {r} = ({a}, {b}, {c}의 공배수)", "hint": "나머지를 빼면 나누어떨어진다"},
            {"text": "최소공배수 = {FL} = {L}", "hint": "소인수마다 큰 지수"},
            {"text": "x = {L} + {r} = {ans}", "marks": [{"on": "+ {r}", "note": "나머지를 다시 더한다"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{ans} ÷ {a} = {L/a} … {r}, {ans} ÷ {b} = {L/b} … {r}, {ans} ÷ {c} = {L/c} … {r}{ro(r)} 모두 나머지가 {r}이다. {ans}보다 작은 수는 {r}{eul(r)} 뺐을 때 공배수가 되지 않으므로 답은 {ans}이다.",
        sol3_fig=steps(["{ans} ÷ {a} = {L/a} … {r}", "{ans} ÷ {b} = {L/b} … {r}", "{ans} ÷ {c} = {L/c} … {r}"]),
        sol3_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        model_answer="구하는 수를 x라 하면 x − {r}{eun(r)} {a}, {b}, {c}의 공배수이다. 세 수의 최소공배수는 {FL} = {L}이므로 가장 작은 x는 {L} + {r} = {ans}이다.",
        rubric=[
            {"element": "구하는 수의 꼴", "points": 3, "criterion": "구하는 수에서 {r}{eul(r)} 뺀 수가 세 수의 공배수임을 밝혔다.", "partial": "공배수라는 말 없이 최소공배수 계산만 했으면 1점."},
            {"element": "최소공배수 구하기", "points": 3, "criterion": "세 수의 최소공배수 {L}{eul(L)} 바르게 구했다.", "partial": "소인수분해는 옳고 지수 선택이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{L} + {r} = {ans}{eul(ans)} 답했다.", "partial": "최소공배수 {L}{eul(L)} 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def _frac_rows():
    rows = {}
    for g in (2, 3, 4, 5, 6):
        for u1, u2 in [(u, v) for u in range(1, 6) for v in range(1, 6) if u != v and math.gcd(u, v) == 1]:
            n1, n2 = g * u1, g * u2
            for d1 in (2, 3, 4, 5, 6, 8, 9, 10, 12):
                for d2 in (2, 3, 4, 5, 6, 8, 9, 10, 12):
                    if d1 == d2 or math.gcd(n1, d1) != 1 or math.gcd(n2, d2) != 1 or (n1 > d1 * 3) or (n2 > d2 * 3):
                        continue
                    L = math.lcm(d1, d2)
                    rows[f"{n1}/{d1}-{n2}/{d2}"] = {"n1": n1, "d1": d1, "n2": n2, "d2": d2, "g": g, "L": L, "q1": L // d1, "q2": L // d2, "m1": n1 // g, "m2": n2 // g}
    return rows


FR_ROWS = _frac_rows()


def gl_t7():
    return tpl(GL, 7, GL_BASE,
        title="두 분수 어느 것에 곱해도 자연수가 되는 가장 작은 분수 — (분모의 최소공배수) / (분자의 최대공약수)",
        skill="곱해서 자연수가 되려면 분자는 두 분모의 공배수, 분모는 두 분자의 공약수여야 함을 알고 가장 작은 분수 만들기",
        variant_axis={"분자의 최대공약수": "2~6", "분모": "2~12"},
        discriminates="분자에 분모의 최소공배수, 분모에 분자의 최대공약수를 두는 근거를 쓰는가 (뒤바꾸지 않는가)",
        difficulty=3,
        params=[{"name": "k", "values": {"in": list(FR_ROWS)}}], table={"key": "k", "rows": FR_ROWS},
        derive={"ans": "L/g"},
        constraints=["L <= 60"],
        cost_values=["n1", "d1", "n2", "d2", "L", "g"],
        answer_var="ans",
        verify=["ans == lcm(d1, d2)/gcd(n1, n2)", "ans*n1/d1 == floor(ans*n1/d1)", "ans*n2/d2 == floor(ans*n2/d2)"],
        question="두 분수 [[frac({n1},{d1})]], [[frac({n2},{d2})]] 중 어느 것에 곱하여도 그 결과가 자연수가 되는 분수 중 가장 작은 분수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="구하는 분수를 [[frac(b,a)]]라 하자. [[frac({n1},{d1})]] × [[frac(b,a)]]가 자연수가 되려면 b는 {d1}의 배수이고 a는 {n1}의 약수여야 한다. [[frac({n2},{d2})]]에 대해서도 같으므로 b는 {d1}{wa(d1)} {d2}의 공배수, a는 {n1}{wa(n1)} {n2}의 공약수다. 분수가 가장 작으려면 분자 b는 가장 작게(최소공배수), 분모 a는 가장 크게(최대공약수) 잡는다.",
        sol2=[
            "구하는 분수를 [[frac(b,a)]]라 하면, 두 곱 [[frac({n1},{d1})]] × [[frac(b,a)]], [[frac({n2},{d2})]] × [[frac(b,a)]]가 모두 자연수여야 한다.",
            "따라서 b는 {d1}{wa(d1)} {d2}의 공배수, a는 {n1}{wa(n1)} {n2}의 공약수이다.",
            "가장 작은 분수가 되려면 b는 {d1}{wa(d1)} {d2}의 최소공배수 {L}, a는 {n1}{wa(n1)} {n2}의 최대공약수 {g}",
            "따라서 구하는 분수는 [[frac({L},{g})]]이다.",
        ],
        sol2_fig=steps([
            {"text": "b = ({d1}, {d2}의 최소공배수) = {L}", "hint": "분자는 분모들의 공배수 — 가장 작게"},
            {"text": "a = ({n1}, {n2}의 최대공약수) = {g}", "hint": "분모는 분자들의 공약수 — 가장 크게"},
            {"text": "[[frac(b,a)]] = [[frac({L},{g})]]", "marks": [{"on": "[[frac({L},{g})]]", "note": "분자·분모를 뒤바꾸지 말 것"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [], [reveal(2), hl("mark:2-0")]],
        sol3="확인하면 [[frac({n1},{d1})]] × [[frac({L},{g})]] = {m1*q1}, [[frac({n2},{d2})]] × [[frac({L},{g})]] = {m2*q2}{ro(m2*q2)} 둘 다 자연수이다. 분자를 더 작게 하거나 분모를 더 크게 하면 어느 한쪽이 자연수가 되지 않으므로 답은 [[frac({L},{g})]]이다.",
        sol3_fig=steps(["[[frac({n1},{d1})]] × [[frac({L},{g})]] = {m1*q1}", "[[frac({n2},{d2})]] × [[frac({L},{g})]] = {m2*q2}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="구하는 분수를 [[frac(b,a)]]라 하면 b는 {d1}{wa(d1)} {d2}의 공배수, a는 {n1}{wa(n1)} {n2}의 공약수여야 하고, 가장 작은 분수가 되려면 b는 최소공배수 {L}, a는 최대공약수 {g}이다. 따라서 구하는 분수는 [[frac({L},{g})]]이다.",
        rubric=[
            {"element": "조건 해석", "points": 3, "criterion": "분자가 두 분모의 공배수, 분모가 두 분자의 공약수여야 함을 밝혔다.", "partial": "한 조건만 밝혔으면 1점."},
            {"element": "최소공배수·최대공약수", "points": 3, "criterion": "분모의 최소공배수 {L}{wa(L)} 분자의 최대공약수 {g}{eul(g)} 구했다.", "partial": "둘 중 하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "[[frac({L},{g})]]{eul(L)} 답했다.", "partial": "분자와 분모를 뒤바꾸어 [[frac({g},{L})]]{ro(g)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


GL_SEED = {
    "seed_id": GL, "category": "연산",
    "title": "최대공약수·최소공배수 기본 — 인수형 G·공약수 개수·L·지수 미지수·나머지 조건·분수",
    "unit_id": "m1-1", "concept_ids": ["m1-1-05", "m1-1-06"],
    "schema_id": None, "schema_name": "최대공약수와 최소공배수의 기본 계산",
    "source_item_ids": [],
    "note": "구조만 차용. 인수형 두 수·G·L 문자열은 파이썬에서 굽어 표로. 나머지 조건은 g·서로소 쌍으로 생성(제약 내장).",
    "geometry": False,
    "templates": [gl_t1(), gl_t2(), gl_t3(), gl_t4(), gl_t5(), gl_t6(), gl_t7()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 유리수의 계산
RO = "m1-1-rational-ops"
RO_BASE = {**NUM_BASE, "prereq": ["유리수의 사칙연산", "거듭제곱"], "ops": ["사칙", "거듭제곱"], "traps": ["부호", "계산순서"], "tags": ["유리수의 계산", "혼합 계산"]}
SIGN_ROWS = {"plus": {"S2": "+", "s2": 1}, "minus": {"S2": "−", "s2": -1}}
SUPK2 = {"key": "k", "rows": {"2": {"SK": "²"}, "3": {"SK": "³"}}}


def ro_t1():
    return tpl(RO, 1, RO_BASE,
        title="거듭제곱이 있는 유리수의 혼합 계산 — (−a)ᵏ × b ± c ÷ (−d)",
        skill="거듭제곱 → 곱셈·나눗셈 → 덧셈·뺄셈의 순서로 계산하며 음수의 거듭제곱 부호를 바르게 정하기",
        variant_axis={"지수": "2 / 3", "가운데 부호": "+ / −", "밑": "2~5"},
        discriminates="(−a)²은 양수, (−a)³은 음수임을 알고 계산 순서(거듭제곱 → 곱·나눗셈 → 덧·뺄셈)를 지키는가",
        difficulty=2,
        params=[{"name": "sg", "values": {"in": list(SIGN_ROWS)}}, {"name": "k", "values": {"in": [2, 3]}}, {"name": "a", "values": {"int": [2, 5]}},
                {"name": "b", "values": {"int": [2, 6]}}, {"name": "d", "values": {"int": [2, 6]}}, {"name": "m", "values": {"int": [1, 6]}}],
        table=[{"key": "sg", "rows": SIGN_ROWS}, SUPK2],
        derive={"c": "d*m", "pk": "(-a)**k", "t1": "(-a)**k * b", "q": "-m", "ans": "(-a)**k * b + s2*(-m)", "na": "-a", "nd": "-d"},
        constraints=["abs(t1) <= 200", "ans != 0", "ans != -a", "ans != b", "ans != c", "ans != -d", "c != b"],
        cost_values=["a", "k", "b", "c", "d", "ans"],
        answer_var="ans",
        verify=["ans == (-a)**k * b + s2*(-m)", "c == d*m"],
        question="{pn(na)}{SK} × {b} {S2} {c} ÷ {pn(nd)}{eul(nd)} 계산하시오.",
        answer="{ans}", answer_alt=[],
        sol1="혼합 계산은 거듭제곱을 가장 먼저, 그다음 곱셈·나눗셈, 마지막에 덧셈·뺄셈 순서로 한다. {pn(na)}{SK}은 음수를 {k}번 곱한 것이므로 부호가 {pk}{ro(pk)} 정해지고, {c} ÷ {pn(nd)}{eun(nd)} 부호가 다른 두 수의 나눗셈이라 음수다. 두 결과를 {S2} 기호로 이으면 된다.",
        sol2=[
            "거듭제곱을 먼저 계산하면 {pn(na)}{SK} = {pk}",
            "곱셈과 나눗셈: {pk} × {b} = {t1}, {c} ÷ {pn(nd)} = {q}",
            "따라서 (주어진 식) = {t1} {S2} {pn(q)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{pn(na)}{SK} = {pk}", "hint": "거듭제곱 먼저 · 음수를 {k}번 곱한 부호"},
            {"text": "{pk} × {b} = {t1},   {c} ÷ {pn(nd)} = {q}", "hint": "곱셈·나눗셈"},
            {"text": "{t1} {S2} {pn(q)} = {ans}", "hint": "덧셈·뺄셈은 마지막", "marks": [{"on": "{pn(q)}", "note": "음수는 괄호"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="거듭제곱 {pn(na)}{SK} = {pk}{ika(pk)} 맞는지 부호부터 확인하고({k}번 곱하면 부호는 {pk}의 부호), 나눗셈 {c} ÷ {pn(nd)} = {q}도 부호가 음수임을 확인한다. {t1} {S2} {pn(q)} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["{pn(na)}{SK} = {pk}  (부호 확인)", "{t1} {S2} {pn(q)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{pn(na)}{SK} = {pk}이므로 {pk} × {b} = {t1}이고, {c} ÷ {pn(nd)} = {q}이다. 따라서 (주어진 식) = {t1} {S2} {pn(q)} = {ans}이다.",
        rubric=[
            {"element": "거듭제곱 계산", "points": 2, "criterion": "{pn(na)}{SK} = {pk}{ro(pk)} 부호까지 바르게 계산했다.", "partial": "부호가 틀렸으면 인정하지 않는다."},
            {"element": "곱셈·나눗셈 계산", "points": 3, "criterion": "{pk} × {b} = {t1}, {c} ÷ {pn(nd)} = {q}{eul(q)} 계산 순서에 맞게 구했다.", "partial": "둘 중 하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{t1} {S2} {pn(q)} = {ans}{eul(ans)} 구했다.", "partial": "앞의 계산은 옳고 마지막 덧셈·뺄셈의 부호가 틀렸으면 1점."},
        ],
        rubric_total=7,
    )


def ro_t2():
    return tpl(RO, 2, RO_BASE,
        title="분수의 거듭제곱과 나눗셈이 섞인 혼합 계산",
        skill="분수의 거듭제곱은 분자·분모를 각각 제곱하고, 분수의 나눗셈은 역수의 곱셈으로 바꾸어 순서대로 계산하기",
        variant_axis={"가운데 부호": "+ / −", "분모": "2~6"},
        discriminates="(−p/q)²의 부호와 값을 바르게 구하고, 나눗셈을 역수의 곱셈으로 바꾸는가",
        difficulty=3,
        params=[{"name": "sg", "values": {"in": list(SIGN_ROWS)}}, {"name": "a", "values": {"int": [1, 3]}}, {"name": "b", "values": {"in": [2, 3, 4, 5]}},
                {"name": "m", "values": {"int": [1, 3]}}, {"name": "c", "values": {"int": [1, 4]}}, {"name": "d", "values": {"in": [2, 3, 4, 5, 6]}}, {"name": "n", "values": {"int": [2, 4]}}],
        table={"key": "sg", "rows": SIGN_ROWS},
        derive={"e": "b*b*m", "h": "d*n", "sq": "a*a/(b*b)", "t1": "a*a*m", "q": "-n", "ans": "a*a*m + s2*(-n)"},
        constraints=["gcd(a, b) == 1", "a < b", "gcd(c, d) == 1", "c < d", "gcd(c, h) == 1", "ans != 0", "ans != a", "ans != b", "ans != e", "ans != c", "ans != d", "ans != h", "e <= 60"],
        cost_values=["a", "b", "e", "c", "d", "h", "ans"],
        answer_var="ans",
        verify=["ans == a*a*m + s2*(-n)", "e == b*b*m", "h == d*n"],
        question="(-[[frac({a},{b})]])² × {e} {S2} [[frac({c},{d})]] ÷ (-[[frac({c},{h})]]){eul(c)} 계산하시오.",
        answer="{ans}", answer_alt=[],
        sol1="거듭제곱을 먼저 계산한다. (−[[frac({a},{b})]])²은 음수를 두 번 곱한 것이므로 양수 [[frac({a*a},{b*b})]]이다. 나눗셈 [[frac({c},{d})]] ÷ (−[[frac({c},{h})]])는 나누는 수의 역수 −[[frac({h},{c})]]{eul(h)} 곱하는 것으로 바꾼다. 그런 다음 곱셈·나눗셈을 먼저, 덧셈·뺄셈을 마지막에 한다.",
        sol2=[
            "거듭제곱: (−[[frac({a},{b})]])² = [[frac({a*a},{b*b})]]",
            "곱셈: [[frac({a*a},{b*b})]] × {e} = {t1}",
            "나눗셈: [[frac({c},{d})]] ÷ (−[[frac({c},{h})]]) = [[frac({c},{d})]] × (−[[frac({h},{c})]]) = {q}",
            "따라서 (주어진 식) = {t1} {S2} {pn(q)} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "(−[[frac({a},{b})]])² = [[frac({a*a},{b*b})]]", "hint": "분자·분모 각각 제곱, 부호는 +"},
            {"text": "[[frac({a*a},{b*b})]] × {e} = {t1}", "hint": "약분"},
            {"text": "[[frac({c},{d})]] × (−[[frac({h},{c})]]) = {q}", "hint": "나눗셈 → 역수의 곱셈"},
            {"text": "{t1} {S2} {pn(q)} = {ans}", "hint": "덧셈·뺄셈은 마지막"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")]],
        sol3="(−[[frac({a},{b})]])²의 부호가 양수인 것, 나눗셈에서 역수를 취할 때 부호가 그대로 음수인 것을 다시 확인한다. {t1} {S2} {pn(q)} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["(−[[frac({a},{b})]])² > 0,   [[frac({c},{d})]] ÷ (−[[frac({c},{h})]]) < 0", "{t1} {S2} {pn(q)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="(−[[frac({a},{b})]])² = [[frac({a*a},{b*b})]]이므로 [[frac({a*a},{b*b})]] × {e} = {t1}이고, [[frac({c},{d})]] ÷ (−[[frac({c},{h})]]) = [[frac({c},{d})]] × (−[[frac({h},{c})]]) = {q}이다. 따라서 (주어진 식) = {t1} {S2} {pn(q)} = {ans}이다.",
        rubric=[
            {"element": "거듭제곱 계산", "points": 2, "criterion": "(−[[frac({a},{b})]])² = [[frac({a*a},{b*b})]]{ro(a*a)} 부호와 값을 바르게 구했다.", "partial": "분자만 제곱하거나 부호를 음수로 했으면 인정하지 않는다."},
            {"element": "나눗셈을 역수의 곱셈으로", "points": 3, "criterion": "나눗셈을 역수 −[[frac({h},{c})]]의 곱셈으로 바꾸어 {q}{eul(q)} 구했다.", "partial": "역수를 취하지 않고 그대로 곱했으면 인정하지 않고, 역수는 맞으나 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{t1} {S2} {pn(q)} = {ans}{eul(ans)} 구했다.", "partial": "마지막 덧셈·뺄셈의 부호가 틀렸으면 1점."},
        ],
        rubric_total=7,
    )


WRONG_ROWS = {
    "md": {"PRE": "에", "OP1": "를 곱해야", "OP2": "로 나누었더니", "S1": "÷", "S2": "×", "S3": "×", "WR": "나눈", "CR": "곱한", "iMD": 1, "iDM": 0, "iAS": 0, "iSA": 0},
    "dm": {"PRE": "를", "OP1": "로 나누어야", "OP2": "를 곱했더니", "S1": "×", "S2": "÷", "S3": "÷", "WR": "곱한", "CR": "나눈", "iMD": 0, "iDM": 1, "iAS": 0, "iSA": 0},
    "as": {"PRE": "에", "OP1": "를 더해야", "OP2": "를 뺐더니", "S1": "−", "S2": "+", "S3": "+", "WR": "뺀", "CR": "더한", "iMD": 0, "iDM": 0, "iAS": 1, "iSA": 0},
    "sa": {"PRE": "에서", "OP1": "를 빼야", "OP2": "를 더했더니", "S1": "+", "S2": "−", "S3": "−", "WR": "더한", "CR": "뺀", "iMD": 0, "iDM": 0, "iAS": 0, "iSA": 1},
}


def ro_t3():
    return tpl(RO, 3, RO_BASE,
        title="잘못 계산한 결과로 어떤 수를 찾아 바르게 계산하기",
        skill="잘못된 계산을 식으로 세워 어떤 수를 구한 뒤, 바른 연산을 다시 하기",
        variant_axis={"잘못한 연산": "곱→나눔 / 나눔→곱 / 더함→뺌 / 뺌→더함", "수": "2~15"},
        discriminates="어떤 수 x를 잘못된 연산의 식으로 세우고 역연산으로 x를 구한 뒤 바른 연산을 마지막에 하는가",
        difficulty=2, context="무맥락", process="문제해결",
        params=[{"name": "w", "values": {"in": list(WRONG_ROWS)}}, {"name": "a", "values": {"in": [2, 4, 5, 9, 12, 15]}}, {"name": "q", "values": {"int": [1, 20]}}],
        table={"key": "w", "rows": WRONG_ROWS},
        derive={"b": "iMD*q + iDM*a*a*q + iAS*q + iSA*(q + 2*a)", "x": "(iMD + iDM)*a*q + (iAS + iSA)*(q + a)", "ans": "iMD*a*a*q + iDM*q + iAS*(q + 2*a) + iSA*q"},
        constraints=["b <= 300", "ans <= 400", "ans != a", "ans != b", "x != a", "x != b", "b != a", "ans != x", "q != a"],
        cost_values=["a", "b", "x", "ans"],
        answer_var="ans",
        verify=["iMD == 0 or (x/a == b and ans == x*a)", "iDM == 0 or (x*a == b and ans == x/a)", "iAS == 0 or (x - a == b and ans == x + a)", "iSA == 0 or (x + a == b and ans == x - a)"],
        question="어떤 수{PRE} {a}{OP1} 할 것을 잘못하여 {a}{OP2} {b}{ika(b)} 되었다. 바르게 계산한 답을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="'어떤 수'를 x로 놓고 잘못 계산한 과정을 그대로 식으로 쓰면 x {S1} {a} = {b}이다. 이 식에서 x를 구한 다음(역연산), 원래 하려던 바른 계산 x {S3} {a}{eul(a)} 한다. 잘못 계산한 결과 {b}{eul(b)} 답으로 쓰지 않도록 한다.",
        sol2=[
            "어떤 수를 x라 하면 잘못 계산한 식은 x {S1} {a} = {b}",
            "따라서 x = {b} {S2} {a} = {x}",
            "바르게 계산하면 {x} {S3} {a} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "x {S1} {a} = {b}", "hint": "잘못 {WR} 계산을 식으로"},
            {"text": "x = {b} {S2} {a} = {x}", "hint": "역연산으로 어떤 수"},
            {"text": "{x} {S3} {a} = {ans}", "hint": "바르게 {CR} 계산", "marks": [{"on": "{ans}", "note": "x가 아니라 바른 계산 결과"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="어떤 수 {x}{ro(x)} 잘못 계산한 대로 하면 {x} {S1} {a} = {b}{ika(b)} 되어 문제의 조건과 같다. 따라서 바르게 계산한 답은 {x} {S3} {a} = {ans}이다.",
        sol3_fig=steps(["{x} {S1} {a} = {b}  (조건 확인)", "{x} {S3} {a} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="어떤 수를 x라 하면 x {S1} {a} = {b}이므로 x = {x}이다. 따라서 바르게 계산하면 {x} {S3} {a} = {ans}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "어떤 수를 x로 놓고 잘못 계산한 식 x {S1} {a} = {b}{eul(b)} 세웠다.", "partial": "바른 연산으로 식을 세웠으면 인정하지 않는다."},
            {"element": "어떤 수 구하기", "points": 2, "criterion": "x = {x}{eul(x)} 구했다.", "partial": "역연산을 잘못 골랐으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "바르게 계산한 값 {ans}{eul(ans)} 답했다.", "partial": "어떤 수 {x}{eul(x)} 답으로 썼으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


RQ_ROWS = {"sum": {"QT": "x + y", "c1": 1, "c2": 1, "cp": 0}, "diff": {"QT": "x − y", "c1": 1, "c2": -1, "cp": 0}, "prod": {"QT": "xy", "c1": 0, "c2": 0, "cp": 1}}
FSG_ROWS = {"pos": {"SG": "", "s": 1, "SGW": ""}, "neg": {"SG": "-", "s": -1, "SGW": "−"}}


def ro_t4():
    return tpl(RO, 4, RO_BASE,
        title="분수와 정수의 역수로 만든 식의 값 — x + y, x − y, xy",
        skill="역수는 곱하여 1이 되는 수임을 알고 분수의 역수(분자·분모 바꾸기)와 정수의 역수(1/n)를 구해 식의 값 계산하기",
        variant_axis={"구하는 것": "x + y / x − y / xy", "분수의 부호": "+ / −"},
        discriminates="역수를 취할 때 부호는 그대로 두고 분자·분모만 바꾸는가, 정수 n의 역수를 1/n으로 쓰는가",
        difficulty=2,
        params=[{"name": "q", "values": {"in": list(RQ_ROWS)}}, {"name": "sg", "values": {"in": list(FSG_ROWS)}}, {"name": "a", "values": {"int": [1, 5]}},
                {"name": "b", "values": {"int": [2, 9]}}, {"name": "c", "values": {"int": [2, 9]}}],
        table=[{"key": "q", "rows": RQ_ROWS}, {"key": "sg", "rows": FSG_ROWS}],
        derive={"x": "s*b/a", "y": "-1/c", "nc": "-c", "ans": "c1*x + c2*y + cp*x*y"},
        constraints=["gcd(a, b) == 1", "a != b", "ans != 0", "ans != a", "ans != b", "ans != -c", "b != c"],
        cost_values=["a", "b", "c", "x", "y", "ans"],
        answer_var="ans",
        verify=["x*(s*a/b) == 1", "y*(-c) == 1", "ans == c1*x + c2*y + cp*x*y"],
        question="{SG}[[frac({a},{b})]]의 역수를 x, {nc}의 역수를 y라 할 때, {QT}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="어떤 수의 역수는 그 수와 곱하여 1이 되는 수다. 분수의 역수는 부호는 그대로 두고 분자와 분모를 바꾼 것이고, 정수 {pn(nc)}의 역수는 1을 {pn(nc)}{ro(nc)} 나눈 {y}이다. x와 y를 구한 뒤 {QT}{eul(QT)} 계산한다.",
        sol2=[
            "{SG}[[frac({a},{b})]]의 역수는 분자와 분모를 바꾼 x = {x}",
            "{pn(nc)}의 역수는 y = {y}",
            "따라서 {QT} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "x = {x}", "hint": "분자·분모 바꾸기, 부호는 그대로"},
            {"text": "y = {y}", "hint": "정수 n의 역수는 1/n"},
            {"text": "{QT} = {ans}", "marks": [{"on": "{ans}", "note": "통분·부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{SG}[[frac({a},{b})]] × {pn(x)} = 1, {pn(nc)} × {pn(y)} = 1이므로 x, y는 역수가 맞다. {QT} = {ans}이므로 답은 {ans}이다.",
        sol3_fig=steps(["{SG}[[frac({a},{b})]] × {pn(x)} = 1", "{pn(nc)} × {pn(y)} = 1", "{QT} = {ans}"]),
        sol3_anim=[[reveal(0), reveal(1)], [reveal(2)]],
        model_answer="{SG}[[frac({a},{b})]]의 역수는 x = {x}, {pn(nc)}의 역수는 y = {y}이다. 따라서 {QT} = {ans}이다.",
        rubric=[
            {"element": "역수 구하기", "points": 3, "criterion": "x = {x}, y = {y}{eul(y)} 구했다.", "partial": "부호를 바꾸거나 정수의 역수를 그 수 자신으로 썼으면 인정하지 않고, 하나만 맞으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 구했다.", "partial": "통분 또는 부호 실수면 1점."},
        ],
        rubric_total=5,
    )


BS_ROWS = {"sum": {"QT": "x + y", "c1": 1, "c2": 1}, "diff": {"QT": "x − y", "c1": 1, "c2": -1}, "rdiff": {"QT": "y − x", "c1": -1, "c2": 1}}
NZ = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def ro_t5():
    return tpl(RO, 5, RO_BASE,
        title="'a보다 b만큼 큰 수'·'c보다 d만큼 작은 수'로 만든 식의 값",
        skill="'b만큼 큰 수'는 덧셈, 'd만큼 작은 수'는 뺄셈으로 옮겨 음수의 덧셈·뺄셈을 하기",
        variant_axis={"구하는 것": "x + y / x − y / y − x", "수": "−9~9"},
        discriminates="'−5만큼 큰 수'를 −5를 더하는 것으로 옮기고 뺄셈을 덧셈으로 고쳐 부호를 처리하는가",
        difficulty=2, ops=["사칙"],
        params=[{"name": "q", "values": {"in": list(BS_ROWS)}}, {"name": "a", "values": {"in": NZ}}, {"name": "b", "values": {"in": NZ}},
                {"name": "c", "values": {"in": NZ}}, {"name": "d", "values": {"in": NZ}}],
        table={"key": "q", "rows": BS_ROWS},
        derive={"x": "a + b", "y": "c - d", "ans": "c1*(a + b) + c2*(c - d)"},
        constraints=["ans != 0", "ans != a", "ans != b", "ans != c", "ans != d", "x != y", "a != b", "c != d", "x != 0", "y != 0"],
        cost_values=["a", "b", "c", "d", "x", "y", "ans"],
        answer_var="ans",
        verify=["ans == c1*(a + b) + c2*(c - d)"],
        question="{a}보다 {b}만큼 큰 수를 x, {c}보다 {d}만큼 작은 수를 y라 할 때, {QT}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="'{a}보다 {b}만큼 큰 수'는 {a}에 {b}{eul(b)} 더한 수이고, '{c}보다 {d}만큼 작은 수'는 {c}에서 {d}{eul(d)} 뺀 수다. 음수를 더하거나 빼는 것이므로 뺄셈은 부호를 바꾸어 더하는 것으로 고쳐 계산한 뒤 {QT}{eul(QT)} 구한다.",
        sol2=[
            "x = {a} + {pn(b)} = {x}",
            "y = {c} − {pn(d)} = {c} + {pn(-d)} = {y}",
            "따라서 {QT} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "x = {a} + {pn(b)} = {x}", "hint": "'큰 수' = 더한다"},
            {"text": "y = {c} − {pn(d)} = {c} + {pn(-d)} = {y}", "hint": "'작은 수' = 뺀다 → 부호 바꿔 더하기"},
            {"text": "{QT} = {ans}", "marks": [{"on": "{ans}", "note": "x, y의 부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="x = {x}{eun(x)} {a}보다 {b}만큼 크고({x} − {pn(a)} = {b}), y = {y}{eun(y)} {c}보다 {d}만큼 작다({c} − {pn(y)} = {d}). 따라서 {QT} = {ans}이다.",
        sol3_fig=steps(["{x} − {pn(a)} = {b}", "{c} − {pn(y)} = {d}", "{QT} = {ans}"]),
        sol3_anim=[[reveal(0), reveal(1)], [reveal(2)]],
        model_answer="x = {a} + {pn(b)} = {x}, y = {c} − {pn(d)} = {y}이므로 {QT} = {ans}이다.",
        rubric=[
            {"element": "x, y 구하기", "points": 3, "criterion": "x = {a} + {pn(b)} = {x}, y = {c} − {pn(d)} = {y}{eul(y)} 구했다.", "partial": "'작은 수'를 더해 구했으면 인정하지 않고, 부호 실수 하나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 구했다.", "partial": "x, y는 옳고 마지막 계산의 부호가 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


RO_SEED = {
    "seed_id": RO, "category": "연산",
    "title": "유리수의 계산 — 거듭제곱 혼합·분수 혼합·잘못 계산·역수·크고 작은 수",
    "unit_id": "m1-1", "concept_ids": ["m1-1-15", "m1-1-16", "m1-1-17"],
    "schema_id": None, "schema_name": "유리수의 사칙연산과 혼합 계산",
    "source_item_ids": [],
    "note": "구조만 차용. 잘못 계산 틀은 조사가 고정되도록 a를 받침 없는 수(2·4·5·9·12·15)로 제한하고 조사는 표 문자열에 둔다.",
    "geometry": False,
    "templates": [ro_t1(), ro_t2(), ro_t3(), ro_t4(), ro_t5()],
}


if __name__ == "__main__":
    for seed in (PF_SEED, GL_SEED, RO_SEED):
        with_pitfalls(seed)
        dump(seed)
