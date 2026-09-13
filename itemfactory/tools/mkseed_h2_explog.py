# itemfactory/tools/mkseed_h2_explog.py — 고2 수학I 지수·로그 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h2_explog.py
#     → seeds/h2-1-exp.json   (지수: 지수법칙 k·거듭제곱근/유리수 지수 값·지수함수 통과점·구간 최대최소·지수방정식·지수부등식, 6틀)
#     → seeds/h2-1-log.json   (로그: 로그 값·로그의 성질·상용로그(값/자릿수)·로그함수 통과점·로그방정식·로그부등식, 6틀)
#   문면의 수식은 pow/root/log/frac 마커. 값이 정해진 항은 파이썬 행에서 미리 계산(VN/VD)하고 노출(R-05)은 행 생성 시 걸렀다.
from __future__ import annotations

import math
import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
from genkit.expr import eul as _eul, eun as _eun, ika as _ika, ro as _ro  # noqa: E402

rng = random.Random(20260915)


def _nums(text):
    return {Fraction(x) for x in re.findall(r"(?<![\d.])-?\d+(?![\d.])", text)}


def _fr(v):
    """행에 넣을 분수 → (VN, VD)"""
    f = Fraction(v)
    return f.numerator, f.denominator


def _fm(v):
    """분수 → 마커 문자열(해설용)"""
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"[[{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})]]"


def _fmp(v):
    """연산자 뒤에 오는 값 — 음수면 괄호"""
    return f"({_fm(v)})" if Fraction(v) < 0 else _fm(v)


def _lt(c):
    """일차항 표기 — '+ x', '− 3x'"""
    s = "+" if c > 0 else "−"
    return f"{s} x" if abs(c) == 1 else f"{s} {abs(c)}x"


def _pick(d, n):
    keys = sorted(d)
    rng.shuffle(keys)
    return {k: d[k] for k in keys[:n]}


# ═══════════════════════════════════════════════════════════════════ 1. 지수
EX = "h2-1-exp"
EX_B = {**HS, "prereq": ["거듭제곱", "인수분해"], "ops": ["지수"], "traps": ["밑 통일", "지수의 부호"], "tags": ["지수법칙", "지수함수"]}


def _ex1_rows():
    out = {}
    for base, sq, cu in ((2, 4, 8), (3, 9, 27), (5, 25, 125)):
        for a in range(1, 7):
            for b in range(1, 5):
                for c in range(1, 4):
                    k = a + 2 * b - 3 * c
                    q = f"[[pow({base},{a})]] × [[pow({sq},{b})]] ÷ [[pow({cu},{c})]] = [[pow({base}, k)]]"
                    if k == 0 or Fraction(k) in _nums(q):
                        continue
                    out[f"i{base}_{a}_{b}_{c}"] = {"EXPR": q, "BASE": base, "STEP": f"[[pow({base},{a})]] × [[pow({base},{2 * b})]] ÷ [[pow({base},{3 * c})]]", "EXP": f"{a} + {2 * b} − {3 * c}", "VN": k, "VD": 1, "KIND": f"밑을 {base}{_ro(base)} 통일"}
    for base in (2, 3):
        for m in (2, 3, 4):
            for p in range(1, 6):
                for n in (2, 3, 4):
                    for q_ in range(1, 6):
                        if m == n and p == q_:
                            continue
                        k = Fraction(p, m) + Fraction(q_, n)
                        t1 = f"[[sqrt({base ** p})]]" if m == 2 else f"[[root({m}, {base ** p})]]"
                        t2 = f"[[sqrt({base ** q_})]]" if n == 2 else f"[[root({n}, {base ** q_})]]"
                        q = f"{t1} × {t2} = [[pow({base}, k)]]"
                        if k in _nums(q):
                            continue
                        out[f"r{base}_{m}_{p}_{n}_{q_}"] = {"EXPR": q, "BASE": base, "STEP": f"[[pow({base}, frac({p},{m}))]] × [[pow({base}, frac({q_},{n}))]]", "EXP": f"[[frac({p},{m})]] + [[frac({q_},{n})]]", "VN": k.numerator, "VD": k.denominator, "KIND": f"거듭제곱근을 유리수 지수로: [[root(n, pow(a, m))]] = [[pow(a, frac(m,n))]]"}
    return _pick(out, 320)


EX1_ROWS = _ex1_rows()


def ex_t1():
    return T(EX, 1, EX_B, title="지수법칙 — 밑을 통일해 지수 k 구하기",
        skill="밑을 하나로 통일하고 거듭제곱근을 유리수 지수로 바꾼 뒤 지수끼리 더하고 빼기", axis={"밑": "2, 3, 5", "형태": "정수 지수 / 거듭제곱근"}, disc="4 = 2², 8 = 2³처럼 밑을 통일하고 ⁿ√aᵐ = a^(m/n)임을 쓰는가", diff=2,
        params=[{"name": "f", "values": {"in": list(EX1_ROWS)}}], table={"key": "f", "rows": EX1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}일 때, 유리수 k의 값을 구하시오.", answer="{ans}",
        sol1="지수법칙 aᵐ × aⁿ = aᵐ⁺ⁿ, aᵐ ÷ aⁿ = aᵐ⁻ⁿ은 밑이 같을 때만 쓸 수 있다. {KIND}한 뒤 지수를 계산한다.",
        sol2=[("{STEP}", "밑 통일"), ("지수: {EXP}", "지수법칙"), ("k = {ans}", None, ("{ans}", "k"))],
        sol3=["밑을 통일한 각 항의 지수가 원래 식과 같은 값인지(예: 4ᵇ = 2²ᵇ) 확인한다. 따라서 k = {ans}이다.", "{STEP}", "k = {ans}"],
        model="{STEP}이므로 지수는 {EXP} = {ans}이다. 따라서 k = {ans}이다.",
        rubric=[("밑 통일", 3, "{STEP} 꼴로 바꿨다.", "한 항의 밑을 잘못 바꿨으면 1점."), ("지수 계산", 2, "k = {ans}{eul(ans)} 구했다.", "지수 계산 실수면 1점.")],
        pitfalls=[("밑이 다른데 지수끼리 더함", "밑 통일", "불인정"), ("나눗셈에서 지수를 더함", "지수 계산", "불인정"), ("ⁿ√aᵐ을 a^(n/m)으로 뒤집음", "밑 통일", "불인정")])


TERMS = [("[[pow(8, frac(2,3))]]", 4, "8 = 2³이므로 2² = 4"), ("[[pow(8, frac(1,3))]]", 2, "8 = 2³이므로 2"), ("[[pow(16, frac(3,4))]]", 8, "16 = 2⁴이므로 2³ = 8"), ("[[pow(16, frac(1,4))]]", 2, "16 = 2⁴이므로 2"),
         ("[[pow(27, frac(2,3))]]", 9, "27 = 3³이므로 3² = 9"), ("[[pow(27, frac(1,3))]]", 3, "27 = 3³이므로 3"), ("[[pow(32, frac(2,5))]]", 4, "32 = 2⁵이므로 2² = 4"), ("[[pow(32, frac(3,5))]]", 8, "32 = 2⁵이므로 2³ = 8"),
         ("[[pow(4, frac(3,2))]]", 8, "4 = 2²이므로 2³ = 8"), ("[[pow(9, frac(3,2))]]", 27, "9 = 3²이므로 3³ = 27"), ("[[pow(25, frac(3,2))]]", 125, "25 = 5²이므로 5³ = 125"), ("[[pow(81, frac(3,4))]]", 27, "81 = 3⁴이므로 3³ = 27"),
         ("[[pow(81, frac(1,4))]]", 3, "81 = 3⁴이므로 3"), ("[[pow(64, frac(2,3))]]", 16, "64 = 2⁶이므로 2⁴ = 16"), ("[[pow(64, frac(1,2))]]", 8, "64 = 8²이므로 8"), ("[[pow(64, frac(5,6))]]", 32, "64 = 2⁶이므로 2⁵ = 32"),
         ("[[pow(125, frac(2,3))]]", 25, "125 = 5³이므로 5² = 25"), ("[[pow(8, -frac(1,3))]]", Fraction(1, 2), "8 = 2³이므로 2⁻¹ = 1/2"), ("[[pow(16, -frac(3,4))]]", Fraction(1, 8), "16 = 2⁴이므로 2⁻³ = 1/8"), ("[[pow(27, -frac(2,3))]]", Fraction(1, 9), "27 = 3³이므로 3⁻² = 1/9"),
         ("[[pow(4, -frac(1,2))]]", Fraction(1, 2), "4 = 2²이므로 2⁻¹ = 1/2"), ("[[pow(9, -frac(1,2))]]", Fraction(1, 3), "9 = 3²이므로 3⁻¹ = 1/3"), ("[[pow(32, -frac(1,5))]]", Fraction(1, 2), "32 = 2⁵이므로 2⁻¹ = 1/2"), ("[[pow(frac(1,8), frac(1,3))]]", Fraction(1, 2), "1/8 = 2⁻³이므로 2⁻¹ = 1/2"),
         ("[[root(3, 64)]]", 4, "4³ = 64이므로 4"), ("[[root(4, 81)]]", 3, "3⁴ = 81이므로 3"), ("[[root(3, -8)]]", -2, "(−2)³ = −8이므로 −2"), ("[[root(5, 32)]]", 2, "2⁵ = 32이므로 2"), ("[[root(3, 125)]]", 5, "5³ = 125이므로 5"),
         ("[[root(4, 16)]]", 2, "2⁴ = 16이므로 2"), ("[[root(3, 27)]]", 3, "3³ = 27이므로 3"), ("[[root(3, -27)]]", -3, "(−3)³ = −27이므로 −3"), ("[[sqrt(pow(-5, 2))]]", 5, "√(a²) = |a|이므로 5"), ("[[root(3, pow(-2, 3))]]", -2, "홀수 제곱근이므로 −2 그대로"),
         ("[[root(4, pow(-3, 4))]]", 3, "짝수 제곱근은 |a|이므로 3"), ("[[pow(root(3, 5), 6)]]", 25, "(5^(1/3))⁶ = 5² = 25"), ("[[pow(root(4, 3), 8)]]", 9, "(3^(1/4))⁸ = 3² = 9"), ("[[root(3, root(2, 64))]]", 2, "⁶√64 = 2")]


def _ex2_rows():
    out = {}
    ops = [("×", lambda x, y: x * y, "곱"), ("÷", lambda x, y: x / y, "나눗셈"), ("+", lambda x, y: x + y, "합"), ("−", lambda x, y: x - y, "차")]
    for i, (t1, v1, e1) in enumerate(TERMS):
        for j, (t2, v2, e2) in enumerate(TERMS):
            if i == j:
                continue
            for op, fn, nm in ops:
                v = fn(Fraction(v1), Fraction(v2))
                if v == 0 or abs(v) > 200 or (v.denominator > 1 and v.denominator > 40):
                    continue
                q = f"{t1} {op} {t2}"
                if v in _nums(q) or abs(v) in _nums(q):
                    continue
                out[f"{i}_{j}_{nm}"] = {"EXPR": q, "T1": t1, "T2": t2, "E1": e1, "E2": e2, "V1": _fm(v1), "V2": _fm(v2), "V2P": _fmp(v2), "OP": op, "VN": v.numerator, "VD": v.denominator}
    return _pick(out, 320)


EX2_ROWS = _ex2_rows()


def ex_t2():
    return T(EX, 2, EX_B, title="거듭제곱근과 유리수 지수 — 값 계산",
        skill="a^(m/n) = ⁿ√aᵐ, 밑을 소인수의 거듭제곱으로 써서 값을 구하기", axis={"항": "8^(2/3), 16^(3/4), ⁿ√a 등 38가지", "연산": "× ÷ + −"}, disc="밑을 소수의 거듭제곱으로 바꿔 지수를 곱한 뒤 값을 계산하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(EX2_ROWS)}}], table={"key": "f", "rows": EX2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="유리수 지수는 a^(m/n) = ⁿ√aᵐ, 음의 지수는 a⁻ⁿ = 1/aⁿ이다. 밑을 소수의 거듭제곱으로 바꾸면 (aᵖ)^(m/n) = a^(pm/n)으로 지수가 정수가 되어 값을 바로 읽을 수 있다.",
        sol2=[("{T1} = {V1} ({E1})", "첫째 항"), ("{T2} = {V2} ({E2})", "둘째 항"), ("{V1} {OP} {V2P} = {ans}", None, ("{ans}", "값"))],
        sol3=["각 항의 값을 거듭제곱해 원래 밑이 나오는지(예: 4³ = 64) 확인한다. 따라서 값은 {ans}이다.", "{T1} = {V1}, {T2} = {V2}", "답 {ans}"],
        model="{T1} = {V1}, {T2} = {V2}이므로 {V1} {OP} {V2P} = {ans}이다.",
        rubric=[("각 항의 값", 3, "{T1} = {V1}, {T2} = {V2}{eul(V2)} 구했다.", "한 항만 맞으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "연산 실수면 1점.")],
        pitfalls=[("a^(m/n)을 a^(n/m)으로 뒤집음", "각 항의 값", "불인정"), ("음의 지수를 음수 값으로 봄", "각 항의 값", "불인정"), ("짝수 제곱근에서 절댓값을 빠뜨림", "각 항의 값", "부분")])


def ex_t3():
    return T(EX, 3, EX_B, title="지수함수의 그래프가 지나는 점 — 상수 m",
        skill="점의 좌표를 y = aˣ⁻ᵐ + n에 대입해 a^(p − m)이 a의 거듭제곱임을 이용해 m 구하기", axis={"밑": "2, 3, 5", "점": "y − n이 밑의 거듭제곱"}, disc="대입 후 양변을 같은 밑의 거듭제곱으로 맞춰 지수를 비교하는가", diff=2,
        params=[{"name": "a", "values": {"in": [2, 3, 5]}}, {"name": "e", "values": {"int": [0, 4]}}, {"name": "n", "values": {"in": NZ(-5, 5)}}, {"name": "p", "values": {"int": [-3, 5]}}],
        derive={"pw": "a**e", "q": "n + a**e", "ans": "p - e"},
        constraints=["pw < 130", "ans != 0", "ans not in (a, n, p, q)", "q != 0"], cost=["a", "e", "n", "p", "q", "ans"], verify=["q - n == pw", "a**(p - ans) == pw"],
        q="함수 y = [[pow({a}, x − m)]] {sgn(n)}의 그래프가 점 ({p}, {q})를 지날 때, 상수 m의 값을 구하시오.", answer="{ans}",
        sol1="그래프가 점 ({p}, {q})를 지나므로 x = {p}, y = {q}를 넣으면 {q} = [[pow({a}, {p} − m)]] {sgn(n)}, 즉 [[pow({a}, {p} − m)]] = {pw}이다. {pw} = [[pow({a},{e})]]이므로 지수를 비교하면 {p} − m = {e}이다.",
        sol2=[("{q} = [[pow({a}, {p} − m)]] {sgn(n)}", "점 대입"), ("[[pow({a}, {p} − m)]] = {pw} = [[pow({a},{e})]] → {p} − m = {e}", "밑 맞춰 지수 비교"), ("m = {ans}", None, ("{ans}", "m"))],
        sol3=["m = {ans}일 때 x = {p}에서 y = [[pow({a},{e})]] {sgn(n)} = {q}{ika(q)} 되어 점을 지난다. 따라서 m = {ans}이다.", "x = {p} → y = {q} ✓", "m = {ans}"],
        model="점 ({p}, {q})를 대입하면 [[pow({a}, {p} − m)]] = {pw} = [[pow({a},{e})]]이므로 {p} − m = {e}, m = {ans}이다.",
        rubric=[("대입·지수 비교", 3, "[[pow({a}, {p} − m)]] = [[pow({a},{e})]]{ro(e)} 만들었다.", "n을 옮기지 않았으면 1점."), ("m 구하기", 2, "m = {ans}{eul(ans)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("n을 이항하지 않고 지수 비교", "대입·지수 비교", "불인정"), ("p − m = e에서 부호 실수", "m 구하기", "부분"), ("a^0 = 1을 잊음", "대입·지수 비교", "부분")])


def ex_t4():
    return T(EX, 4, EX_B, title="지수함수의 구간 최대·최소",
        skill="밑이 1보다 크면 증가, 0과 1 사이면 감소함수임을 써서 구간의 양 끝에서 최대·최소 읽기", axis={"밑": "2, 3, 1/2, 1/3", "구간": "−2~3", "묻는 것": "M + m / M − m"}, disc="밑의 크기에 따라 최댓값·최솟값이 나오는 끝점이 바뀜을 아는가", diff=2,
        params=[{"name": "b", "values": {"in": ["2", "3", "h", "t"]}}, {"name": "lo", "values": {"int": [-2, 1]}}, {"name": "hi", "values": {"int": [0, 3]}}, {"name": "k", "values": {"in": NZ(-5, 5)}}, {"name": "s", "values": {"in": ["sum", "diff"]}}],
        table=[{"key": "b", "rows": {"2": {"BASE": "2", "AN": 2, "AD": 1, "MONO": "증가", "w": 1}, "3": {"BASE": "3", "AN": 3, "AD": 1, "MONO": "증가", "w": 1}, "h": {"BASE": "frac(1,2)", "AN": 1, "AD": 2, "MONO": "감소", "w": 0}, "t": {"BASE": "frac(1,3)", "AN": 1, "AD": 3, "MONO": "감소", "w": 0}}},
               {"key": "s", "rows": {"sum": {"ASK": "M + m", "ws": 1}, "diff": {"ASK": "M − m", "ws": 0}}}],
        derive={"M": "w*((AN/AD)**hi + k) + (1 - w)*((AN/AD)**lo + k)", "mm": "w*((AN/AD)**lo + k) + (1 - w)*((AN/AD)**hi + k)", "xM": "w*hi + (1 - w)*lo", "xm": "w*lo + (1 - w)*hi", "ans": "ws*(M + mm) + (1 - ws)*(M - mm)"},
        constraints=["lo < hi", "ans != 0", "ans not in (lo, hi, k, M, mm)"], cost=["lo", "hi", "k", "M", "mm", "ans"], verify=["M > mm"],
        q="{lo} ≤ x ≤ {hi}에서 함수 y = [[pow({BASE}, x)]] {sgn(k)}의 최댓값을 M, 최솟값을 m이라 할 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="y = [[pow({BASE}, x)]] {sgn(k)}{eun(k)} 밑이 {BASE}이므로 x가 커질수록 y가 {MONO}하는 함수이다. 따라서 구간의 두 끝 x = {lo}, x = {hi}에서 최댓값과 최솟값이 나온다: 최댓값은 x = {xM}, 최솟값은 x = {xm}에서.",
        sol2=[("밑 {BASE} → {MONO}함수", "증가·감소"), ("M = [[pow({BASE}, {xM})]] {sgn(k)} = {M}, m = [[pow({BASE}, {xm})]] {sgn(k)} = {mm}", "끝점 대입"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["구간 안의 다른 x(예: 중간값)를 넣어 보면 M과 m 사이의 값이 나와 끝점이 최대·최소임을 확인할 수 있다. 따라서 {ASK} = {ans}이다.", "M = {M}, m = {mm}", "{ASK} = {ans}"],
        model="밑이 {BASE}인 {MONO}함수이므로 M = [[pow({BASE}, {xM})]] {sgn(k)} = {M}, m = [[pow({BASE}, {xm})]] {sgn(k)} = {mm}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("최대·최소", 3, "M = {M}, m = {mm}{eul(mm)} 구했다.", "증가·감소를 반대로 보았으면 인정하지 않는다."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("0 < 밑 < 1인데 증가함수로 봄", "최대·최소", "불인정"), ("k를 더하지 않음", "최대·최소", "부분"), ("음의 지수 계산 실수(2⁻² = −4 등)", "최대·최소", "부분")])


def _ex5_rows():
    out = {}
    for base in (2, 3):
        sq = base * base
        for i in range(0, 4):
            for j in range(i + 1, 5):
                s, p = base ** i + base ** j, base ** (i + j)
                q = f"[[pow({sq}, x)]] − {s} × [[pow({base}, x)]] + {p} = 0"
                for kk, ask, v in (("sum", "모든 해의 합", i + j), ("prod", "모든 해의 곱", i * j)):
                    if v == 0 or Fraction(v) in _nums(q):
                        continue
                    out[f"q{base}_{i}_{j}_{kk}"] = {"EXPR": q, "ASK": ask, "V": v, "SUB": f"[[pow({base}, x)]] = t (t > 0)로 놓으면 t² − {s}t + {p} = 0", "ROOTS": f"(t − {base ** i})(t − {base ** j}) = 0에서 t = {base ** i} 또는 t = {base ** j}", "SOL": f"[[pow({base}, x)]] = [[pow({base},{i})]] 또는 [[pow({base},{j})]]이므로 x = {i} 또는 x = {j}", "KIND": "치환"}
    for base in (2, 3):
        for (pp, qq) in ((1, 2), (1, 3), (2, 3), (2, 1), (3, 1), (3, 2)):
            for u in range(-3, 4):
                for v_ in range(-3, 4):
                    if pp == qq:
                        continue
                    x = Fraction(qq * v_ - pp * u, pp - qq)
                    if x.denominator != 1 or x == 0:
                        continue
                    lhs = f"[[pow({base ** pp}, x{'' if u == 0 else (' + ' if u > 0 else ' − ') + str(abs(u))})]]"
                    rhs = f"[[pow({base ** qq}, x{'' if v_ == 0 else (' + ' if v_ > 0 else ' − ') + str(abs(v_))})]]"
                    q = f"{lhs} = {rhs}"
                    if x in _nums(q):
                        continue
                    lin_l = f"{pp}(x{'' if u == 0 else (' + ' if u > 0 else ' − ') + str(abs(u))})"
                    lin_r = f"{qq}(x{'' if v_ == 0 else (' + ' if v_ > 0 else ' − ') + str(abs(v_))})"
                    out[f"e{base}_{pp}_{qq}_{u}_{v_}"] = {"EXPR": q, "ASK": "해", "V": int(x), "SUB": f"밑을 {base}{_ro(base)} 통일: [[pow({base}, {lin_l})]] = [[pow({base}, {lin_r})]]", "ROOTS": f"지수끼리 비교: {lin_l} = {lin_r}", "SOL": f"일차방정식을 풀면 x = {int(x)}", "KIND": "밑 통일"}
    return _pick(out, 320)


EX5_ROWS = _ex5_rows()


def ex_t5():
    return T(EX, 5, EX_B, title="지수방정식 — 밑 통일·치환",
        skill="밑을 통일해 지수를 비교하거나, aˣ = t(t > 0)로 치환해 이차방정식으로 풀기", axis={"형태": "밑 통일(a^(px+u) = a^(qx+v)) / 치환(a²ˣ − s·aˣ + p = 0)", "묻는 것": "해 / 해의 합·곱"}, disc="치환 후 t > 0 조건을 쓰고, t의 값을 다시 x로 되돌리는가", diff=3,
        params=[{"name": "f", "values": {"in": list(EX5_ROWS)}}], table={"key": "f", "rows": EX5_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="방정식 {EXPR}의 {ASK}{eul(ASK)} 구하시오.", answer="{ans}",
        sol1="지수방정식은 밑을 같게 만들어 지수를 비교하거나(a^f(x) = a^g(x) ⇔ f(x) = g(x)), aˣ이 반복되면 aˣ = t(t > 0)로 치환해 t의 방정식을 푼다. 이 문제는 {KIND} 유형이다.",
        sol2=[("{SUB}", "{KIND}"), ("{ROOTS}", "방정식 풀기"), ("{SOL} → {ASK} {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["구한 x를 원래 방정식에 넣어 양변이 같은지 확인한다(치환형은 t > 0인 근만 채택했는지도 확인). 따라서 {ASK}은 {ans}이다.", "{SOL}", "{ASK} {ans}"],
        model="{SUB}. {ROOTS}. {SOL}이므로 {ASK}은 {ans}이다.",
        rubric=[("변형", 3, "{SUB} 꼴로 세웠다.", "밑을 잘못 통일했거나 치환 조건 t > 0을 빠뜨렸으면 1점."), ("답", 2, "{ASK} {ans}{eul(ans)} 구했다.", "t를 x로 되돌리지 않고 답했으면 인정하지 않는다.")],
        pitfalls=[("치환한 t의 값을 그대로 답함", "답", "불인정"), ("밑 통일에서 지수에 계수를 곱하지 않음", "변형", "불인정"), ("t < 0인 근을 채택", "변형", "부분")])


def _ex6_rows():
    out = {}
    for a in (2, 3, 5, 7):
        for e in range(1, 6):
            for c in range(0, 5):
                if a ** e > 350:
                    continue
                rhs = a ** e
                lhs = f"[[pow({a}, x{'' if c == 0 else ' − ' + str(c)})]]"
                for op, cnt, rng_ in (("≤", c + e, f"x − {c} ≤ {e}, 즉 x ≤ {c + e}" if c else f"x ≤ {e}"), ("<", c + e - 1, f"x − {c} < {e}, 즉 x < {c + e}" if c else f"x < {e}")):
                    q = f"{lhs} {op} {rhs}"
                    if cnt < 1 or Fraction(cnt) in _nums(q):
                        continue
                    out[f"a{a}_{e}_{c}_{op}"] = {"EXPR": q, "ASK": "자연수 x의 개수", "V": cnt, "STEP": f"{rhs} = [[pow({a},{e})]]이므로 {lhs} {op} [[pow({a},{e})]]", "RANGE": rng_, "MONO": f"밑 {a} > 1이므로 부등호 방향 그대로", "KIND": "밑 통일"}
                lhs2 = f"[[pow(frac(1,{a}), x{'' if c == 0 else ' − ' + str(c)})]]"
                q = f"{lhs2} ≥ [[frac(1, {rhs})]]"
                cnt = c + e
                if Fraction(cnt) not in _nums(q):
                    out[f"h{a}_{e}_{c}"] = {"EXPR": q, "ASK": "자연수 x의 개수", "V": cnt, "STEP": f"[[frac(1, {rhs})]] = [[pow(frac(1,{a}), {e})]]이므로 {lhs2} ≥ [[pow(frac(1,{a}), {e})]]", "RANGE": (f"x − {c} ≤ {e}, 즉 x ≤ {c + e}" if c else f"x ≤ {e}"), "MONO": f"밑 [[frac(1,{a})]]{_ika(1)} 0과 1 사이이므로 부등호 방향이 바뀐다", "KIND": "밑 통일(0 < 밑 < 1)"}
    for base in (2, 3, 5):
        sq = base * base
        for i in range(0, 4):
            for j in range(i + 1, 5):
                s, p = base ** i + base ** j, base ** (i + j)
                if p > 4000:
                    continue
                for op, cnt, rng_ in (("≤", j - i + 1, f"{base ** i} ≤ t ≤ {base ** j}, 즉 {i} ≤ x ≤ {j}"), ("<", j - i - 1, f"{base ** i} < t < {base ** j}, 즉 {i} < x < {j}")):
                    q = f"[[pow({sq}, x)]] − {s} × [[pow({base}, x)]] + {p} {op} 0"
                    if cnt < 1 or Fraction(cnt) in _nums(q):
                        continue
                    out[f"q{base}_{i}_{j}_{op}"] = {"EXPR": q, "ASK": "정수 x의 개수", "V": cnt, "STEP": f"[[pow({base}, x)]] = t (t > 0)로 놓으면 t² − {s}t + {p} {op} 0, (t − {base ** i})(t − {base ** j}) {op} 0", "RANGE": rng_, "MONO": f"밑 {base} > 1이므로 t의 범위를 x의 범위로 그대로 옮긴다", "KIND": "치환"}
    return _pick(out, 320)


EX6_ROWS = _ex6_rows()


def ex_t6():
    return T(EX, 6, EX_B, title="지수부등식 — 밑의 크기에 따른 부등호 방향·치환",
        skill="밑을 통일해 지수를 비교하되 0 < 밑 < 1이면 부등호 방향을 바꾸고, 치환형은 t의 범위를 x로 되돌리기", axis={"형태": "밑 통일(밑 > 1 / 0 < 밑 < 1) / 치환", "묻는 것": "자연수·정수 x의 개수"}, disc="밑이 1보다 작을 때 부등호가 뒤집힘을 알고 정수 개수를 정확히 세는가", diff=3,
        params=[{"name": "f", "values": {"in": list(EX6_ROWS)}}], table={"key": "f", "rows": EX6_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="부등식 {EXPR}{eul(EXPR)} 만족시키는 {ASK}를 구하시오.", answer="{ans}",
        sol1="지수부등식은 밑을 통일한 뒤 지수를 비교한다. 밑이 1보다 크면 부등호 방향이 그대로이고, 0과 1 사이이면 방향이 바뀐다. aˣ이 반복되면 t = aˣ(t > 0)로 치환한다. 이 문제는 {KIND} 유형이다.",
        sol2=[("{STEP}", "{KIND}"), ("{MONO}: {RANGE}", "지수 비교"), ("{ASK}: {ans}", None, ("{ans}", "개수"))],
        sol3=["범위의 경계값을 원래 부등식에 넣어 등호·부등호가 맞는지 확인하면 개수를 잘못 세지 않는다. 따라서 {ASK}는 {ans}이다.", "{RANGE}", "개수 {ans}"],
        model="{STEP}. {MONO}: {RANGE}. 따라서 {ASK}는 {ans}이다.",
        rubric=[("부등식 변형", 3, "{RANGE}{eul(RANGE)} 얻었다.", "부등호 방향을 잘못 잡았으면 인정하지 않는다."), ("개수 세기", 2, "{ans}개를 구했다.", "경계 포함 여부 실수면 1점.")],
        pitfalls=[("0 < 밑 < 1에서 부등호 방향을 바꾸지 않음", "부등식 변형", "불인정"), ("치환한 t의 범위를 그대로 답함", "개수 세기", "불인정"), ("경계(등호) 포함 여부 실수", "개수 세기", "부분")])


EX_SEED = SEED(EX, category="대수", title="지수 — 지수법칙·거듭제곱근 값·지수함수 통과점·구간 최대최소·지수방정식·지수부등식", unit_id="h2-1", concept_ids=["h2-1-01", "h2-1-04", "h2-1-06"],
               schema_name="지수와 지수함수", note="식·값이 정해진 행은 파이썬에서 계산(VN/VD)하고 노출은 행 생성에서 걸렀다. 지수함수 최대최소는 밑 4종 × 구간.",
               templates=[ex_t1(), ex_t2(), ex_t3(), ex_t4(), ex_t5(), ex_t6()])


# ═══════════════════════════════════════════════════════════════════ 2. 로그
LG = "h2-1-log"
LG_B = {**HS, "prereq": ["지수법칙", "지수함수"], "ops": ["로그"], "traps": ["진수 조건", "밑 변환"], "tags": ["로그", "로그함수", "상용로그"]}

LTERMS = [("[[log(2, 32)]]", 5, "32 = 2⁵"), ("[[log(2, 8)]]", 3, "8 = 2³"), ("[[log(3, 81)]]", 4, "81 = 3⁴"), ("[[log(3, 27)]]", 3, "27 = 3³"), ("[[log(5, 125)]]", 3, "125 = 5³"), ("[[log(2, frac(1,8))]]", -3, "1/8 = 2⁻³"),
          ("[[log(3, frac(1,9))]]", -2, "1/9 = 3⁻²"), ("[[log(5, frac(1,25))]]", -2, "1/25 = 5⁻²"), ("[[log(frac(1,2), 8)]]", -3, "8 = (1/2)⁻³"), ("[[log(frac(1,3), 27)]]", -3, "27 = (1/3)⁻³"), ("[[log(4, 32)]]", Fraction(5, 2), "32 = 2⁵ = 4^(5/2)"),
          ("[[log(2, sqrt(2))]]", Fraction(1, 2), "√2 = 2^(1/2)"), ("[[log(9, 27)]]", Fraction(3, 2), "27 = 3³ = 9^(3/2)"), ("[[log(8, 4)]]", Fraction(2, 3), "4 = 2² = 8^(2/3)"), ("[[log(sqrt(3), 9)]]", 4, "9 = 3² = (√3)⁴"), ("[[log(7, 1)]]", 0, "1 = 7⁰"),
          ("[[log(2, 64)]]", 6, "64 = 2⁶"), ("[[log(3, sqrt(3))]]", Fraction(1, 2), "√3 = 3^(1/2)"), ("[[log(4, 8)]]", Fraction(3, 2), "8 = 2³ = 4^(3/2)"), ("[[log(27, 9)]]", Fraction(2, 3), "9 = 3² = 27^(2/3)"), ("[[log(frac(1,5), 25)]]", -2, "25 = (1/5)⁻²"),
          ("[[log(10, 1000)]]", 3, "1000 = 10³"), ("[[log(10, 0.01)]]", -2, "0.01 = 10⁻²"), ("[[log(2, root(3, 2))]]", Fraction(1, 3), "³√2 = 2^(1/3)"), ("[[log(5, sqrt(5))]]", Fraction(1, 2), "√5 = 5^(1/2)"), ("[[log(16, 2)]]", Fraction(1, 4), "2 = 16^(1/4)")]


def _lg1_rows():
    out = {}
    for i, (t1, v1, e1) in enumerate(LTERMS):
        for j, (t2, v2, e2) in enumerate(LTERMS):
            if i == j:
                continue
            for op, v in (("+", Fraction(v1) + Fraction(v2)), ("−", Fraction(v1) - Fraction(v2))):
                q = f"{t1} {op} {t2}"
                if v == 0 or v in _nums(q) or abs(v) in _nums(q):
                    continue
                out[f"{i}_{j}_{op}"] = {"EXPR": q, "T1": t1, "T2": t2, "E1": e1, "E2": e2, "V1": _fm(v1), "V2": _fm(v2), "V2P": _fmp(v2), "OP": op, "VN": v.numerator, "VD": v.denominator}
    return _pick(out, 320)


LG1_ROWS = _lg1_rows()


def lg_t1():
    return T(LG, 1, LG_B, title="로그의 값 — 진수를 밑의 거듭제곱으로",
        skill="log_a b에서 b = aᵏ이면 값이 k임을 써서 두 로그의 합·차 구하기", axis={"항": "log₂32, log₃(1/9), log₄32, log₈4 등 26가지", "연산": "+ −"}, disc="진수를 밑의 거듭제곱(분수·근호 지수 포함)으로 나타내 지수를 읽는가", diff=2,
        params=[{"name": "f", "values": {"in": list(LG1_ROWS)}}], table={"key": "f", "rows": LG1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="로그의 정의: aˣ = b ⇔ x = log_a b. 진수 b를 밑 a의 거듭제곱 aᵏ으로 쓰면 log_a b = k이다. 밑이 분수이거나 진수가 근호이면 지수가 음수·분수가 된다.",
        sol2=[("{T1} = {V1} ({E1})", "첫째 항"), ("{T2} = {V2} ({E2})", "둘째 항"), ("{V1} {OP} {V2P} = {ans}", None, ("{ans}", "값"))],
        sol3=["밑을 구한 값만큼 거듭제곱해 진수가 나오는지(예: 2⁵ = 32) 확인한다. 따라서 값은 {ans}이다.", "{T1} = {V1}, {T2} = {V2}", "답 {ans}"],
        model="{T1} = {V1}, {T2} = {V2}이므로 {V1} {OP} {V2P} = {ans}이다.",
        rubric=[("각 로그의 값", 3, "{T1} = {V1}, {T2} = {V2}{eul(V2)} 구했다.", "한 항만 맞으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("log_a(1/aᵏ)의 부호를 양수로 씀", "각 로그의 값", "불인정"), ("밑이 aᵖ일 때 지수를 p로 나누지 않음", "각 로그의 값", "불인정"), ("합·차 부호 실수", "계산", "부분")])


def _lg2_rows():
    out = {}
    for a in (2, 3, 5, 7):
        for b in (2, 3, 5, 7, 10):
            if a == b:
                continue
            for c in (4, 8, 9, 16, 25, 27, 32, 49, 64, 81, 125, 128, 243, 343, 625):
                # log_a b × log_b c = log_a c 가 정수인 경우: c = a^k
                k = None
                for kk in range(1, 8):
                    if a ** kk == c:
                        k = kk
                if k is None:
                    continue
                q = f"[[log({a}, {b})]] × [[log({b}, {c})]]"
                if Fraction(k) in _nums(q):
                    continue
                out[f"c{a}_{b}_{c}"] = {"EXPR": q, "V": k, "LAW": "log_a b × log_b c = log_a c", "STEP": f"[[log({a}, {b})]] × [[log({b}, {c})]] = [[log({a}, {c})]] = [[log({a}, pow({a},{k}))]]", "KIND": "밑 변환(곱)"}
    for a in (2, 3, 5, 6, 7, 10):
        for n in (2, 3, 4, 5, 6, 7, 9, 12, 15):
            for k in range(1, 5):
                m = n * a ** k
                if m > 1000:
                    continue
                q = f"[[log({a}, {m})]] − [[log({a}, {n})]]"
                if Fraction(k) in _nums(q):
                    continue
                out[f"d{a}_{n}_{k}"] = {"EXPR": q, "V": k, "LAW": "log_a m − log_a n = log_a (m/n)", "STEP": f"[[log({a}, {m})]] − [[log({a}, {n})]] = [[log({a}, frac({m},{n}))]] = [[log({a}, {a ** k})]]", "KIND": "차 → 나눗셈"}
                if True:
                    # 합: log_a p + log_a q, pq = a^k
                    for p in (2, 3, 4, 5, 6, 8, 9, 12, 18, 25):
                        if (a ** k) % p or p == 1 or (a ** k) // p == 1:
                            continue
                        qv = a ** k // p
                        if p > qv:
                            continue
                        q = f"[[log({a}, {p})]] + [[log({a}, {qv})]]"
                        if Fraction(k) in _nums(q):
                            continue
                        out[f"s{a}_{p}_{qv}"] = {"EXPR": q, "V": k, "LAW": "log_a p + log_a q = log_a (pq)", "STEP": f"[[log({a}, {p})]] + [[log({a}, {qv})]] = [[log({a}, {p * qv})]] = [[log({a}, pow({a},{k}))]]", "KIND": "합 → 곱"}
    return _pick(out, 300)


LG2_ROWS = _lg2_rows()


def lg_t2():
    return T(LG, 2, LG_B, title="로그의 성질 — 합·차·밑 변환으로 값 구하기",
        skill="log_a p + log_a q = log_a pq, log_a m − log_a n = log_a(m/n), log_a b·log_b c = log_a c를 써서 정수 값 만들기", axis={"성질": "합 / 차 / 밑 변환 곱", "밑": "2, 3, 5, 6, 7, 10"}, disc="로그의 합·차를 진수의 곱·몫으로 묶고, 밑 변환으로 곱을 하나의 로그로 만드는가", diff=2,
        params=[{"name": "f", "values": {"in": list(LG2_ROWS)}}], table={"key": "f", "rows": LG2_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="밑이 같은 로그의 합은 진수의 곱, 차는 진수의 몫이다. 밑이 다르면 밑 변환 공식 log_a b = log_c b / log_c a를 써서 log_a b × log_b c = log_a c로 이어 붙인다. 이 문제는 '{LAW}'를 쓴다.",
        sol2=[("{LAW}", "로그의 성질"), ("{STEP}", "하나의 로그로"), ("= {ans}", None, ("{ans}", "값"))],
        sol3=["마지막 로그의 진수가 밑의 {ans}제곱인지 확인한다. 따라서 값은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP} = {ans}이다.",
        rubric=[("성질 적용", 3, "{STEP} 꼴로 묶었다.", "합을 진수의 합으로 두었으면 인정하지 않는다."), ("값", 2, "{ans}{eul(ans)} 구했다.", "지수 읽기 실수면 1점.")],
        pitfalls=[("log_a p + log_a q = log_a(p + q)로 계산", "성질 적용", "불인정"), ("밑 변환에서 분자·분모를 바꿈", "성질 적용", "불인정"), ("진수를 밑의 거듭제곱으로 바꿀 때 지수 실수", "값", "부분")])


L2, L3 = Fraction("0.3010"), Fraction("0.4771")


def _lg3_rows():
    out = {}
    cands = {4: (2, 0, 0, 0), 6: (1, 1, 0, 0), 8: (3, 0, 0, 0), 9: (0, 2, 0, 0), 12: (2, 1, 0, 0), 15: (0, 1, 1, 0), 16: (4, 0, 0, 0), 18: (1, 2, 0, 0), 24: (3, 1, 0, 0), 25: (0, 0, 2, 0), 27: (0, 3, 0, 0), 32: (5, 0, 0, 0), 36: (2, 2, 0, 0), 45: (0, 2, 1, 0), 48: (4, 1, 0, 0), 50: (1, 0, 2, 0), 54: (1, 3, 0, 0), 72: (3, 2, 0, 0), 75: (0, 1, 2, 0), 80: (4, 0, 1, 0), 96: (5, 1, 0, 0), 120: (3, 1, 1, 0), 150: (1, 1, 2, 0), 200: (3, 0, 2, 0), 240: (4, 1, 1, 0), 300: (2, 1, 2, 0), 360: (3, 2, 1, 0), 600: (3, 1, 2, 0), 1200: (4, 1, 2, 0), 1500: (2, 1, 3, 0)}
    for N, (p, q, r, _) in cands.items():
        v = p * L2 + q * L3 + r * (1 - L2)
        parts = []
        if p: parts.append(f"{p} log 2" if p > 1 else "log 2")
        if q: parts.append(f"{q} log 3" if q > 1 else "log 3")
        if r: parts.append(f"{r} log 5" if r > 1 else "log 5")
        fact = " × ".join(([f"[[pow(2,{p})]]" if p > 1 else "2"] if p else []) + ([f"[[pow(3,{q})]]" if q > 1 else "3"] if q else []) + ([f"[[pow(5,{r})]]" if r > 1 else "5"] if r else []))
        expl = f"{N} = {fact}이므로 log {N} = " + " + ".join(parts) + (", log 5 = log 10 − log 2 = 1 − 0.3010 = 0.6990" if r else "")
        out[f"v{N}"] = {"ASK": f"log {N}의 값을 구하시오.", "KIND": "값", "EXPL": expl, "STEP": f"= {p} × 0.3010 + {q} × 0.4771 + {r} × 0.6990".replace(" + 0 × 0.4771", "").replace(" + 0 × 0.6990", "").replace("= 0 × 0.3010 + ", "= "), "VN": v.numerator, "VD": v.denominator, "DEC": 1}
    for base, L, lab in ((2, L2, "log 2 = 0.3010"), (3, L3, "log 3 = 0.4771"), (6, L2 + L3, "log 6 = log 2 + log 3 = 0.7781"), (12, 2 * L2 + L3, "log 12 = 2 log 2 + log 3 = 1.0791"), (15, L3 + 1 - L2, "log 15 = log 3 + log 5 = 1.1761")):
        for n in range(8, 61):
            x = n * L
            fl = math.floor(x)
            frac_ = x - fl
            if frac_ < Fraction("0.06") or frac_ > Fraction("0.94"):
                continue
            digits = fl + 1
            q = f"log 2 = 0.3010, log 3 = 0.4771, [[pow({base}, {n})]]은 몇 자리의 자연수"
            if Fraction(digits) in _nums(q):
                continue
            out[f"n{base}_{n}"] = {"ASK": f"[[pow({base}, {n})]]은 몇 자리의 자연수인지 구하시오.", "KIND": "자릿수", "EXPL": f"log [[pow({base}, {n})]] = {n} log {base}, {lab}", "STEP": f"= {n} × {float(L):.4f} = {float(x):.4f}, 정수 부분이 {fl}이므로 {fl} + 1 = {digits}자리", "VN": digits, "VD": 1, "DEC": 0}
    for base, L, lab in (("frac(1,2)", -L2, "log (1/2) = −log 2 = −0.3010"), ("0.3", L3 - 1, "log 0.3 = log 3 − 1 = −0.5229"), ("frac(1,3)", -L3, "log (1/3) = −log 3 = −0.4771")):
        for n in range(5, 41):
            x = n * L
            fl = math.floor(x)          # 음수: −m + f
            frac_ = x - fl
            if frac_ < Fraction("0.06") or frac_ > Fraction("0.94"):
                continue
            pos = -fl
            q = f"log 2 = 0.3010, log 3 = 0.4771, [[pow({base}, {n})]] 소수점 아래"
            if Fraction(pos) in _nums(q):
                continue
            out[f"d{base}_{n}"] = {"ASK": f"[[pow({base}, {n})]]을 소수로 나타낼 때 소수점 아래 몇째 자리에서 처음으로 0이 아닌 숫자가 나타나는지 구하시오.", "KIND": "소수점 아래 자리", "EXPL": f"log [[pow({base}, {n})]] = {n} log {base}, {lab}", "STEP": f"= {n} × ({float(L):.4f}) = {float(x):.4f} = −{pos} + {float(frac_):.4f}, 정수 부분이 −{pos}이므로 소수점 아래 {pos}째 자리", "VN": pos, "VD": 1, "DEC": 0}
    return _pick(out, 300)


LG3_ROWS = _lg3_rows()


def lg_t3():
    return T(LG, 3, LG_B, title="상용로그 — log 2, log 3으로 값·자릿수 구하기",
        skill="log 2 = 0.3010, log 3 = 0.4771을 써서 상용로그의 값을 구하고, 정수 부분으로 자릿수·소수점 아래 자리 읽기", axis={"묻는 것": "log N의 값 / 자릿수 / 소수점 아래 자리", "밑": "2, 3, 6, 12, 15, 1/2, 0.3, 1/3"}, disc="log 5 = 1 − log 2를 알고, 정수 부분 n ⇒ (n + 1)자리, 정수 부분 −n ⇒ 소수점 아래 n째 자리임을 아는가", diff=3,
        params=[{"name": "f", "values": {"in": list(LG3_ROWS)}}], table={"key": "f", "rows": LG3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="log 2 = 0.3010, log 3 = 0.4771로 계산할 때, {ASK}", answer="{dec(ans)}",
        sol1="상용로그는 밑이 10인 로그이다. 소인수분해해 log 2, log 3의 합으로 나타내고 log 5 = log(10/2) = 1 − log 2, log 10 = 1을 쓴다. 상용로그의 정수 부분이 n이면 그 수는 (n + 1)자리, 정수 부분이 −n이면 소수점 아래 n째 자리에서 처음으로 0이 아닌 숫자가 나타난다.",
        sol2=[("{EXPL}", "로그로 옮기기"), ("{STEP}", "값 계산"), ("답: {dec(ans)}", None, ("{dec(ans)}", "답"))],
        sol3=["10^(정수 부분) 과 비교해 크기가 맞는지(예: 10³ < N < 10⁴이면 4자리) 확인한다. 따라서 답은 {dec(ans)}이다.", "{STEP}", "답 {dec(ans)}"],
        model="{EXPL}이므로 {STEP}. 따라서 답은 {dec(ans)}이다.",
        rubric=[("로그 변형", 3, "{EXPL} 꼴로 나타냈다.", "log 5를 0.5 등으로 잘못 두었으면 인정하지 않는다."), ("계산·해석", 2, "{dec(ans)}{eul(dec(ans))} 구했다.", "정수 부분과 자릿수의 관계(n + 1)를 틀렸으면 1점.")],
        pitfalls=[("log 5를 log 2로 만들지 않음", "로그 변형", "불인정"), ("정수 부분 n을 그대로 자릿수로 답함", "계산·해석", "불인정"), ("음수 로그의 정수 부분을 잘못 읽음", "계산·해석", "부분")])


def lg_t4():
    return T(LG, 4, LG_B, title="로그함수의 그래프가 지나는 점 — 상수 n",
        skill="점의 좌표를 y = log_a(x − m) + n에 대입해 로그의 값을 읽고 n 구하기", axis={"밑": "2, 3, 5", "점": "x − m이 밑의 거듭제곱"}, disc="진수를 밑의 거듭제곱으로 바꿔 로그의 값을 읽고 n을 분리하는가", diff=2,
        params=[{"name": "a", "values": {"in": [2, 3, 5]}}, {"name": "e", "values": {"int": [0, 4]}}, {"name": "m", "values": {"in": NZ(-5, 5)}}, {"name": "q", "values": {"int": [-4, 6]}}],
        derive={"pw": "a**e", "p": "m + a**e", "ans": "q - e", "nm": "-m"},
        constraints=["pw < 130", "ans != 0", "ans not in (a, m, p, q)", "p != 0"], cost=["a", "e", "m", "p", "q", "ans"], verify=["p - m == pw", "ans + e == q"],
        q="함수 y = [[log({a}, x {sgn(nm)})]] + n의 그래프가 점 ({p}, {q})를 지날 때, 상수 n의 값을 구하시오.", answer="{ans}",
        sol1="그래프가 점 ({p}, {q})를 지나므로 x = {p}, y = {q}를 넣으면 {q} = [[log({a}, {pw})]] + n이다. {pw} = [[pow({a},{e})]]이므로 [[log({a}, {pw})]] = {e}, 따라서 n = {q} − {e}.",
        sol2=[("{q} = [[log({a}, {p} {sgn(nm)})]] + n = [[log({a}, {pw})]] + n", "점 대입"), ("[[log({a}, {pw})]] = {e} ({pw} = [[pow({a},{e})]])", "로그의 값"), ("n = {q} − {e} = {ans}", None, ("{ans}", "n"))],
        sol3=["n = {ans}일 때 x = {p}에서 y = {e} {sgn(ans)} = {q}{ika(q)} 되어 점을 지난다. 따라서 n = {ans}이다.", "x = {p} → y = {q} ✓", "n = {ans}"],
        model="점 ({p}, {q})를 대입하면 {q} = [[log({a}, {pw})]] + n = {e} + n이므로 n = {ans}이다.",
        rubric=[("대입·로그 값", 3, "[[log({a}, {pw})]] = {e}{eul(e)} 읽었다.", "진수를 잘못 계산했으면 1점."), ("n 구하기", 2, "n = {ans}{eul(ans)} 구했다.", "이항 실수면 1점.")],
        pitfalls=[("x − m의 부호를 반대로 계산", "대입·로그 값", "불인정"), ("log_a 1 = 0을 잊음", "대입·로그 값", "부분"), ("이항 부호 실수", "n 구하기", "부분")])


def _lg5_rows():
    out = {}
    for a in (2, 3, 5):
        for e in range(1, 6):
            for p in range(0, 7):
                for qv in range(1, 9):
                    tgt = a ** e
                    if tgt > 260:
                        continue
                    x0 = next((x for x in range(p + 1, 60) if (x - p) * (x + qv) == tgt), None)
                    if x0 is None:
                        continue
                    lhs1 = f"[[log({a}, x)]]" if p == 0 else f"[[log({a}, x − {p})]]"
                    q = f"{lhs1} + [[log({a}, x + {qv})]] = {e}"
                    if Fraction(x0) in _nums(q):
                        continue
                    other = -(qv - p) - x0   # 두 근의 합 = p − q
                    out[f"a{a}_{e}_{p}_{qv}"] = {"EXPR": q, "ASK": "해", "V": x0, "DOM": f"진수 조건: x > {p}" if p else "진수 조건: x > 0", "STEP": f"[[log({a}, (x − {p})(x + {qv}))]] = {e}이므로 (x − {p})(x + {qv}) = {tgt}" if p else f"[[log({a}, x(x + {qv}))]] = {e}이므로 x(x + {qv}) = {tgt}", "SOLVE": f"x² {_lt(qv - p)} − {tgt + p * qv} = 0, (x − {x0})(x + {-other}) = 0" if qv != p else f"x² − {tgt + p * qv} = 0, (x − {x0})(x + {x0}) = 0", "PICK": f"진수 조건에 맞는 x = {x0} (x = {other}{_eun(other)} 버림)", "KIND": "합 → 곱"}
    for a in (2, 3, 5, 10):
        for t1 in range(0, 4):
            for t2 in range(t1 + 1, 5):
                s, pr = t1 + t2, t1 * t2
                if a ** t2 > 1100:
                    continue
                q = f"[[pow(log({a}, x), 2)]] − {s}[[log({a}, x)]] + {pr} = 0" if pr else f"[[pow(log({a}, x), 2)]] − {s}[[log({a}, x)]] = 0"
                for kk, ask, v in (("prod", "모든 해의 곱", a ** s), ("sum", "모든 해의 합", a ** t1 + a ** t2)):
                    if Fraction(v) in _nums(q):
                        continue
                    out[f"t{a}_{t1}_{t2}_{kk}"] = {"EXPR": q, "ASK": ask, "V": v, "DOM": "진수 조건: x > 0", "STEP": f"[[log({a}, x)]] = t로 놓으면 t² − {s}t + {pr} = 0" if pr else f"[[log({a}, x)]] = t로 놓으면 t² − {s}t = 0", "SOLVE": f"(t − {t1})(t − {t2}) = 0에서 t = {t1} 또는 t = {t2}", "PICK": f"x = [[pow({a},{t1})]] = {a ** t1} 또는 x = [[pow({a},{t2})]] = {a ** t2}", "KIND": "치환"}
    for a, sq in ((2, 4), (3, 9), (5, 25)):
        for x0 in range(2, 13):
            c = x0 * x0 - x0
            q = f"[[log({a}, x)]] = [[log({sq}, x + {c})]]"
            if Fraction(x0) in _nums(q):
                continue
            out[f"b{a}_{x0}"] = {"EXPR": q, "ASK": "해", "V": x0, "DOM": "진수 조건: x > 0", "STEP": f"[[log({sq}, x + {c})]] = [[frac(1,2)]][[log({a}, x + {c})]]이므로 2[[log({a}, x)]] = [[log({a}, x + {c})]], 즉 x² = x + {c}", "SOLVE": f"x² − x − {c} = 0, (x − {x0})(x + {x0 - 1}) = 0", "PICK": f"진수 조건에 맞는 x = {x0} (x = {-(x0 - 1)}{_eun(-(x0 - 1))} 버림)", "KIND": "밑 통일"}
    return _pick(out, 300)


LG5_ROWS = _lg5_rows()


def lg_t5():
    return T(LG, 5, LG_B, title="로그방정식 — 진수 조건과 함께 풀기",
        skill="로그의 합을 곱으로 묶거나 치환·밑 통일로 방정식을 풀고 진수 조건으로 근을 가려내기", axis={"형태": "합→곱 / 치환 / 밑 통일", "묻는 것": "해 / 해의 합·곱"}, disc="진수 조건(진수 > 0)을 먼저 세우고 조건에 맞지 않는 근을 버리는가", diff=3,
        params=[{"name": "f", "values": {"in": list(LG5_ROWS)}}], table={"key": "f", "rows": LG5_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="방정식 {EXPR}의 {ASK}{eul(ASK)} 구하시오.", answer="{ans}",
        sol1="로그방정식은 먼저 진수 조건을 확인한다({DOM}). 그다음 밑이 같은 로그의 합은 진수의 곱으로 묶고, 로그가 반복되면 치환하며, 밑이 다르면 밑을 통일한다. 이 문제는 {KIND} 유형이다.",
        sol2=[("{DOM}; {STEP}", "{KIND}"), ("{SOLVE}", "방정식 풀기"), ("{PICK} → {ASK} {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["구한 해를 원래 방정식의 진수에 넣어 모두 양수인지 확인한다. 따라서 {ASK}은 {ans}이다.", "{PICK}", "{ASK} {ans}"],
        model="{DOM}. {STEP}. {SOLVE}. {PICK}이므로 {ASK}은 {ans}이다.",
        rubric=[("방정식 변형", 3, "{STEP} 꼴로 세웠다.", "합을 진수의 합으로 두었으면 인정하지 않는다."), ("진수 조건·답", 2, "진수 조건으로 근을 가려 {ASK} {ans}{eul(ans)} 답했다.", "진수 조건에 맞지 않는 근을 함께 답했으면 1점.")],
        pitfalls=[("진수 조건을 확인하지 않고 두 근을 모두 답함", "진수 조건·답", "부분"), ("log의 합을 진수의 합으로 계산", "방정식 변형", "불인정"), ("치환한 t를 x로 되돌리지 않음", "진수 조건·답", "불인정")])


def _lg6_rows():
    out = {}
    for a in (2, 3):
        for e in range(1, 5):
            for p in range(0, 5):
                tgt = a ** e
                lhs = f"[[log({a}, x)]]" if p == 0 else f"[[log({a}, x − {p})]]"
                for kk, ask, v in (("cnt", "자연수 x의 개수", tgt), ("max", "정수 x의 최댓값", p + tgt)):
                    q = f"{lhs} ≤ {e}"
                    if Fraction(v) in _nums(q):
                        continue
                    out[f"a{a}_{e}_{p}_{kk}"] = {"EXPR": q, "ASK": ask, "V": v, "DOM": f"진수 조건: x > {p}", "STEP": f"{lhs} ≤ [[log({a}, {tgt})]], 밑 {a} > 1이므로 x − {p} ≤ {tgt}" if p else f"{lhs} ≤ [[log({a}, {tgt})]], 밑 {a} > 1이므로 x ≤ {tgt}", "RANGE": f"{p} < x ≤ {p + tgt}", "KIND": "밑 > 1"}
                lhs2 = f"[[log(frac(1,{a}), x)]]" if p == 0 else f"[[log(frac(1,{a}), x − {p})]]"
                for kk, ask, v in (("cnt", "자연수 x의 개수", tgt), ("max", "정수 x의 최댓값", p + tgt)):
                    q = f"{lhs2} ≥ −{e}"
                    if Fraction(v) in _nums(q):
                        continue
                    out[f"h{a}_{e}_{p}_{kk}"] = {"EXPR": q, "ASK": ask, "V": v, "DOM": f"진수 조건: x > {p}", "STEP": f"−{e} = [[log(frac(1,{a}), {tgt})]]이므로 {lhs2} ≥ [[log(frac(1,{a}), {tgt})]], 밑이 0과 1 사이이므로 x − {p} ≤ {tgt}" if p else f"−{e} = [[log(frac(1,{a}), {tgt})]]이므로 {lhs2} ≥ [[log(frac(1,{a}), {tgt})]], 밑이 0과 1 사이이므로 x ≤ {tgt}", "RANGE": f"{p} < x ≤ {p + tgt}", "KIND": "0 < 밑 < 1 (부등호 방향 바뀜)"}
    for a in (2, 3):
        for t1 in range(0, 3):
            for t2 in range(t1 + 1, 4):
                s, pr = t1 + t2, t1 * t2
                q = f"[[pow(log({a}, x), 2)]] − {s}[[log({a}, x)]] + {pr} ≤ 0" if pr else f"[[pow(log({a}, x), 2)]] − {s}[[log({a}, x)]] ≤ 0"
                v = a ** t2 - a ** t1 + 1
                if Fraction(v) in _nums(q):
                    continue
                out[f"t{a}_{t1}_{t2}"] = {"EXPR": q, "ASK": "정수 x의 개수", "V": v, "DOM": "진수 조건: x > 0", "STEP": f"[[log({a}, x)]] = t로 놓으면 (t − {t1})(t − {t2}) ≤ 0, {t1} ≤ t ≤ {t2}", "RANGE": f"[[pow({a},{t1})]] ≤ x ≤ [[pow({a},{t2})]], 즉 {a ** t1} ≤ x ≤ {a ** t2}", "KIND": "치환"}
    for a in (2, 3, 5):
        for p in range(0, 5):
            for r in range(1, 12):
                # log_a(x − p) ≤ log_a(2x − r): x − p ≤ 2x − r, x > p, 2x > r
                lo = max(r - p, p + 1, r // 2 + 1)
                lhs = f"[[log({a}, x)]]" if p == 0 else f"[[log({a}, x − {p})]]"
                q = f"{lhs} ≤ [[log({a}, 2x − {r})]]"
                if Fraction(lo) in _nums(q) or lo < 2:
                    continue
                out[f"c{a}_{p}_{r}"] = {"EXPR": q, "ASK": "정수 x의 최솟값", "V": lo, "DOM": f"진수 조건: x > {p}, 2x − {r} > 0", "STEP": f"밑 {a} > 1이므로 x − {p} ≤ 2x − {r}, 즉 x ≥ {r - p}" if p else f"밑 {a} > 1이므로 x ≤ 2x − {r}, 즉 x ≥ {r}", "RANGE": f"진수 조건과 함께 x ≥ {lo}", "KIND": "진수 비교"}
    return _pick(out, 300)


LG6_ROWS = _lg6_rows()


def lg_t6():
    return T(LG, 6, LG_B, title="로그부등식 — 밑의 크기·진수 조건·치환",
        skill="진수 조건을 세우고 밑의 크기에 따라 부등호 방향을 정해 정수해 세기", axis={"형태": "밑 > 1 / 0 < 밑 < 1 / 치환 / 진수 비교", "묻는 것": "개수 / 최댓값 / 최솟값"}, disc="진수 조건과 부등호 방향(밑 < 1이면 반대)을 모두 반영해 정수해를 세는가", diff=3,
        params=[{"name": "f", "values": {"in": list(LG6_ROWS)}}], table={"key": "f", "rows": LG6_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="부등식 {EXPR}{eul(EXPR)} 만족시키는 {ASK}{eul(ASK)} 구하시오.", answer="{ans}",
        sol1="로그부등식은 진수 조건({DOM})을 먼저 세운다. 우변을 같은 밑의 로그로 바꾼 뒤 진수를 비교하는데, 밑이 1보다 크면 부등호 방향 그대로, 0과 1 사이면 방향을 바꾼다. 이 문제는 {KIND} 유형이다.",
        sol2=[("{DOM}", "진수 조건"), ("{STEP}", "{KIND}"), ("{RANGE} → {ASK} {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["범위의 경계값을 부등식과 진수 조건에 넣어 확인한다. 따라서 {ASK}은 {ans}이다.", "{RANGE}", "{ASK} {ans}"],
        model="{DOM}. {STEP}. 따라서 {RANGE}이고 {ASK}은 {ans}이다.",
        rubric=[("부등식 풀이", 3, "{RANGE}{eul(RANGE)} 얻었다.", "부등호 방향을 잘못 잡았으면 인정하지 않는다."), ("정수해", 2, "{ASK} {ans}{eul(ans)} 구했다.", "진수 조건을 빠뜨려 개수가 틀리면 1점.")],
        pitfalls=[("진수 조건을 빠뜨림", "정수해", "부분"), ("0 < 밑 < 1에서 부등호 방향을 바꾸지 않음", "부등식 풀이", "불인정"), ("치환한 t의 범위를 그대로 답함", "정수해", "불인정")])


LG_SEED = SEED(LG, category="대수", title="로그 — 로그 값·성질·상용로그·로그함수 통과점·로그방정식·로그부등식", unit_id="h2-1", concept_ids=["h2-1-02", "h2-1-03", "h2-1-05", "h2-1-07"],
               schema_name="로그와 로그함수", note="상용로그 값은 0.3010·0.4771을 분수로 정확히 계산해 dec()으로 표시. 자릿수 행은 소수 부분이 0.06~0.94인 것만(근사 오차 회피).",
               templates=[lg_t1(), lg_t2(), lg_t3(), lg_t4(), lg_t5(), lg_t6()])


if __name__ == "__main__":
    run(EX_SEED, LG_SEED)
