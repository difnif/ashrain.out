# itemfactory/tools/mkseed_m2_number.py — m2-1 수와 식 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m2_number.py
#     → seeds/m2-1-repeating-decimal.json (유리수와 순환소수: n번째 자리 2·순환소수→분수 2·유한소수 조건 4, 8틀)
#     → seeds/m2-1-monomial.json          (단항식 곱셈·나눗셈: 계수·지수 결정 2·□ 안의 식·잘못 계산, 4틀)
#     → seeds/m2-1-polynomial.json        (다항식 계산: 괄호 전개 계수·분수 계수·단항식×다항식·잘못 계산·도형·식의 값, 6틀)
#
# 표기 원칙
#   · 순환소수는 [[recdec(정수부, 순환마디)]] / [[recdec(정수부, 비순환, 순환마디)]] 마커 (자릿수 라벨은 원문 그대로 — '09'·'037' 유지)
#   · 파라미터로 정해지는 단항식·다항식은 평문 위첨자(x²y³, 표 조각), 파생값으로 정해지는 것은 [[k*pow(x,e)*pow(y,f)]] 마커
#     — 마커 안 계수는 ±1 을 피하고(‘1x’), 지수 1 은 pow 를 쓰지 않는다(표 조각 'x' / 'pow(x,2)'). 파생 지수는 제약으로 2 이상.
#   · 식이 답인 틀(monomial-t3·t4, polynomial-t4·t5)은 verify 에 ans 를 쓰지 않고 recheck.py 가 mathir·sympy 로 대조한다.
from __future__ import annotations

import os
import sys
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


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
    """84 → '2² × 3 × 7'"""
    return " × ".join(f"{p}{sup(e)}" for p, e in sorted(fac(n).items())) if n > 1 else "1"


def strip25(n: int) -> int:
    while n % 2 == 0:
        n //= 2
    while n % 5 == 0:
        n //= 5
    return n


def expand(p: int, q: int):
    """p/q 의 소수 전개 → (비순환 자릿수 문자열, 순환마디, K, L)"""
    q2 = q
    k2 = k5 = 0
    while q2 % 2 == 0:
        q2 //= 2
        k2 += 1
    while q2 % 5 == 0:
        q2 //= 5
        k5 += 1
    K = max(k2, k5)
    if q2 == 1:
        L = 0
    else:
        L, x = 1, 10 % q2
        while x != 1:
            x = x * 10 % q2
            L += 1
    digits, r = [], p % q
    for _ in range(K + L):
        r *= 10
        digits.append(r // q)
        r %= q
    d = "".join(map(str, digits))
    return d[:K], d[K:], K, L


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


BASE = {"process": "절차수행", "context": "무맥락", "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}

# ═══════════════════════════════════════════════════════════════════ 1. 유리수와 순환소수
RD = "m2-1-repeating-decimal"
RD_BASE = {**BASE, "prereq": ["분수와 소수", "소인수분해"], "ops": ["순환소수"], "traps": ["순환마디 위치", "약분"], "tags": ["순환소수"]}

# t1 — 순수 순환소수 (분모가 2·5 와 서로소): 소수점 아래 첫째 자리부터 순환
PURE_ROWS = {}
for _q in (7, 11, 13, 27, 37, 41):
    for _p in range(1, min(_q, 14)):
        if gcd(_p, _q) == 1:
            _pre, _cyc, _K, _L = expand(_p, _q)
            if _K == 0 and 2 <= _L <= 6:
                PURE_ROWS[f"{_p}-{_q}"] = {"P": _p, "Q": _q, "CYC": _cyc, "L": _L}

# t2 — 혼합 순환소수: 순환하지 않는 자릿수 K(1~2) 뒤에 순환마디
MIX_ROWS = {}
for _q in (14, 22, 26, 28, 35, 44, 52, 55, 65, 66, 70, 74, 78):
    for _p in range(1, min(_q, 14)):
        if gcd(_p, _q) == 1:
            _pre, _cyc, _K, _L = expand(_p, _q)
            if 1 <= _K <= 2 and 2 <= _L <= 6:
                MIX_ROWS[f"{_p}-{_q}"] = {"P": _p, "Q": _q, "PRE": _pre, "CYC": _cyc, "K": _K, "L": _L, "Kp": _K + 1}

N_VALUES = [20, 25, 30, 33, 40, 45, 50, 55, 60, 70, 75, 80, 90, 99, 100]


def rd_t1():
    return tpl(RD, 1, RD_BASE,
        title="분수를 순환소수로 나타내어 소수점 아래 n번째 자리의 숫자 구하기",
        skill="분수를 소수로 고쳐 순환마디를 찾고, n을 순환마디의 길이로 나눈 나머지로 위치를 정하기",
        variant_axis={"분모": "7·11·13·27·37·41 (순환마디 길이 2~6)", "n": "20~100"},
        discriminates="순환마디를 정확히 끊고, 나머지가 0일 때 순환마디의 마지막 숫자를 고르는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(PURE_ROWS)}}, {"name": "n", "values": {"in": N_VALUES}}],
        table={"key": "f", "rows": PURE_ROWS},
        derive={"r": "((n - 1) % L) + 1", "qd": "(n - r) / L", "Lqd": "L*qd", "ans": "floor(10**n * P / Q) % 10"},
        constraints=["ans != P", "ans != Q"],
        cost_values=["P", "Q", "L", "r", "ans"],
        answer_var="ans",
        verify=["ans == floor(10**n * P / Q) % 10", "((10**L - 1) * P) % Q == 0", "L*qd + r == n", "r >= 1", "r <= L"],
        question="분수 [[frac({P},{Q})]]{eul(P)} 소수로 나타낼 때, 소수점 아래 {n}번째 자리의 숫자를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="분수를 소수로 나타내면 [[frac({P},{Q})]] = [[recdec(0, {CYC})]]이므로 순환마디는 {CYC}이고 길이는 {L}이다. 소수점 아래 첫째 자리부터 순환마디의 {L}개 숫자가 계속 반복되므로, {n}번째 자리의 숫자는 {n}을 {L}로 나눈 나머지가 정해 준다. 나머지가 0이면 순환마디의 마지막 숫자다.",
        sol2=[
            "[[frac({P},{Q})]] = [[recdec(0, {CYC})]]이므로 순환마디는 {CYC}, 길이는 {L}",
            "{n} = {L} × {qd} + {r}이므로 소수점 아래 {n}번째 자리는 순환마디가 {qd}번 반복된 뒤 {r}번째 숫자",
            "순환마디 {CYC}의 {r}번째 숫자는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "[[frac({P},{Q})]] = [[recdec(0, {CYC})]]", "hint": "순환마디 {CYC} (길이 {L})"},
            {"text": "{n} = {L} × {qd} + {r}", "hint": "{L}로 나눈 나머지 = 순환마디에서의 위치"},
            {"text": "{r}번째 숫자 → {ans}", "marks": [{"on": "{r}번째 숫자", "note": "나머지 0이면 마지막 숫자"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="순환마디 {CYC}는 {L}개의 숫자가 반복되므로 소수점 아래 {Lqd}번째 자리까지 {qd}번 반복되고, 그다음 {r}번째 숫자가 {n}번째 자리에 온다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{L} × {qd} = {Lqd}번째 자리까지 {qd}번 반복", "{Lqd} + {r} = {n}번째 자리 → {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[frac({P},{Q})]] = [[recdec(0, {CYC})]]이므로 순환마디는 {CYC}이고 길이는 {L}이다. {n} = {L} × {qd} + {r}이므로 소수점 아래 {n}번째 자리의 숫자는 순환마디의 {r}번째 숫자인 {ans}이다.",
        rubric=[
            {"element": "순환마디", "points": 3, "criterion": "[[frac({P},{Q})]]{eul(P)} 소수로 나타내어 순환마디 {CYC}와 길이 {L}{eul(L)} 구했다.", "partial": "순환마디의 길이만 맞고 숫자가 틀렸으면 1점."},
            {"element": "나머지로 위치 찾기", "points": 2, "criterion": "{n} = {L} × {qd} + {r}에서 {r}번째 숫자임을 밝혔다.", "partial": "나머지 0을 순환마디의 마지막 숫자로 읽지 못했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "소수점 아래 {n}번째 자리의 숫자 {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


def rd_t2():
    return tpl(RD, 2, RD_BASE,
        title="순환하지 않는 부분이 있는 순환소수의 소수점 아래 n번째 자리의 숫자",
        skill="순환하지 않는 자릿수를 빼고 남은 자릿수를 순환마디의 길이로 나누어 위치를 정하기",
        variant_axis={"분모": "14·22·26·28·35·44·52·55·65·66·70·74·78", "n": "20~100"},
        discriminates="순환마디가 소수점 아래 첫째 자리가 아니라 둘째·셋째 자리부터 시작함을 반영해 n에서 순환하지 않는 자릿수를 빼는가",
        difficulty=3,
        params=[{"name": "f", "values": {"in": list(MIX_ROWS)}}, {"name": "n", "values": {"in": N_VALUES}}],
        table={"key": "f", "rows": MIX_ROWS},
        derive={"m": "n - K", "r": "((n - K - 1) % L) + 1", "qd": "(n - K - r) / L", "ans": "floor(10**n * P / Q) % 10"},
        constraints=["ans != P", "ans != Q"],
        cost_values=["P", "Q", "K", "L", "m", "r", "ans"],
        answer_var="ans",
        verify=["ans == floor(10**n * P / Q) % 10", "L*qd + r == m", "m == n - K", "r >= 1", "r <= L"],
        question="분수 [[frac({P},{Q})]]{eul(P)} 소수로 나타낼 때, 소수점 아래 {n}번째 자리의 숫자를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="[[frac({P},{Q})]] = [[recdec(0, {PRE}, {CYC})]]이므로 소수점 아래 {K}번째 자리까지는 순환하지 않는 부분이고, {Kp}번째 자리부터 순환마디 {CYC}(길이 {L})가 반복된다. 그래서 {n}번째 자리는 순환하지 않는 {K}자리를 뺀 {m}번째 순환 숫자이고, {m}을 {L}로 나눈 나머지가 순환마디에서의 위치다.",
        sol2=[
            "[[frac({P},{Q})]] = [[recdec(0, {PRE}, {CYC})]] — 순환하지 않는 부분 {K}자리, 순환마디 {CYC} (길이 {L})",
            "{n} − {K} = {m}이고 {m} = {L} × {qd} + {r}이므로 순환마디가 {qd}번 반복된 뒤 {r}번째 숫자",
            "순환마디 {CYC}의 {r}번째 숫자는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "[[frac({P},{Q})]] = [[recdec(0, {PRE}, {CYC})]]", "hint": "순환마디는 {Kp}번째 자리부터"},
            {"text": "{n} − {K} = {m}, {m} = {L} × {qd} + {r}", "hint": "순환하지 않는 {K}자리를 먼저 뺀다"},
            {"text": "{r}번째 숫자 → {ans}", "marks": [{"on": "{r}번째 숫자", "note": "나머지 0이면 마지막 숫자"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="순환마디는 소수점 아래 {Kp}번째 자리부터 시작하므로 {n}번째 자리는 순환마디에서 {m}번째 숫자이고, {m} = {L} × {qd} + {r}이므로 순환마디 {CYC}의 {r}번째 숫자 {ans}이다. {n}을 바로 {L}로 나누면 위치가 어긋난다.",
        sol3_fig=steps(["순환 시작: {Kp}번째 자리 → {n}번째 자리는 순환 {m}번째", "{m} = {L} × {qd} + {r} → {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[frac({P},{Q})]] = [[recdec(0, {PRE}, {CYC})]]이므로 순환마디는 소수점 아래 {Kp}번째 자리부터 시작하는 {CYC}이다. {n} − {K} = {m} = {L} × {qd} + {r}이므로 소수점 아래 {n}번째 자리의 숫자는 순환마디의 {r}번째 숫자인 {ans}이다.",
        rubric=[
            {"element": "순환마디와 시작 위치", "points": 3, "criterion": "[[frac({P},{Q})]] = [[recdec(0, {PRE}, {CYC})]]에서 순환마디 {CYC}와 순환이 {Kp}번째 자리부터 시작함을 밝혔다.", "partial": "순환마디는 맞고 시작 위치를 첫째 자리로 보았으면 1점."},
            {"element": "위치 계산", "points": 2, "criterion": "{n} − {K} = {m}, {m} = {L} × {qd} + {r}로 순환마디의 {r}번째 숫자임을 밝혔다.", "partial": "순환하지 않는 자릿수를 빼지 않았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "소수점 아래 {n}번째 자리의 숫자 {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


# t3 — 순수 순환소수 → 기약분수 (약분이 꼭 필요한 순환마디만)
REP_ROWS = {}
for _v in (3, 6):
    REP_ROWS[str(_v)] = {"REP": str(_v), "V": _v, "L": 1, "TEN": 10, "NINES": 9}
for _v in range(10, 99):
    if gcd(_v, 99) > 1 and _v % 11 != 0:
        REP_ROWS[str(_v)] = {"REP": str(_v), "V": _v, "L": 2, "TEN": 100, "NINES": 99}
for _v in range(100, 999):
    _s = str(_v)
    if gcd(_v, 999) > 1 and len(set(_s)) > 1 and _v % 111 != 0:
        REP_ROWS[_s] = {"REP": _s, "V": _v, "L": 3, "TEN": 1000, "NINES": 999}
ASK2_ROWS = {"sum": {"ASK": "a + b", "s": 1}, "diff": {"ASK": "b − a", "s": -1}}


def rd_t3():
    return tpl(RD, 3, RD_BASE,
        title="순환소수를 기약분수로 나타내어 a + b (b − a) 구하기 — 순환마디만 있는 꼴",
        skill="x로 놓고 순환마디 길이만큼 10ⁿ을 곱해 빼서 분수로 만들고, 반드시 약분해 기약분수로 만들기",
        variant_axis={"순환마디 길이": "1~3", "구하는 것": "a + b / b − a"},
        discriminates="순환마디 길이에 맞는 10ⁿ을 곱하는가, 분수를 약분하지 않은 채 a, b를 읽지 않는가",
        difficulty=2,
        params=[{"name": "rep", "values": {"in": list(REP_ROWS)}}, {"name": "ask", "values": {"in": list(ASK2_ROWS)}}],
        table=[{"key": "rep", "rows": REP_ROWS}, {"key": "ask", "rows": ASK2_ROWS}],
        derive={"g": "gcd(V, NINES)", "a": "V / g", "b": "NINES / g", "ans": "b + s*a"},
        constraints=["g > 1", "ans != V", "ans != 0", "a != b"],
        cost_values=["V", "NINES", "g", "a", "b", "ans"],
        answer_var="ans",
        verify=["ans == b + s*a", "a * NINES == b * V", "gcd(a, b) == 1"],
        question="순환소수 [[recdec(0, {REP})]]{eul(V)} 기약분수 [[frac(a, b)]]로 나타낼 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="순환소수를 x로 놓고, 순환마디의 길이 {L}만큼 소수점이 옮겨지도록 양변에 {TEN}을 곱한 뒤 원래 식 x를 빼면 순환하는 부분이 사라진다. 그러면 {NINES}x = {V}가 되어 x = [[frac({V}, {NINES})]]이고, 이것을 약분해야 기약분수의 a, b가 정해진다.",
        sol2=[
            "x = [[recdec(0, {REP})]]로 놓으면 순환마디의 길이가 {L}이므로 {TEN}x = [[recdec({V}, {REP})]]",
            "{TEN}x − x = {V}, 즉 {NINES}x = {V}이므로 x = [[frac({V}, {NINES})]]",
            "분자와 분모를 {g}로 나누어 약분하면 [[frac({a}, {b})]]이므로 a = {a}, b = {b}, {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{TEN}x = [[recdec({V}, {REP})]]", "hint": "순환마디 길이 {L} → {TEN}배"},
            {"text": "{TEN}x − x = {V} → x = [[frac({V}, {NINES})]]", "hint": "소수 부분이 같아서 사라진다"},
            {"text": "= [[frac({a}, {b})]] → {ASK} = {ans}", "marks": [{"on": "[[frac({a}, {b})]]", "note": "{g}로 약분"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="[[frac({a}, {b})]]{eul(a)} 소수로 고치면 [[recdec(0, {REP})]]{ika(V)} 되어 처음 순환소수와 같다. 약분 전의 [[frac({V}, {NINES})]]{ro(V)} a, b를 읽으면 틀린다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["[[frac({a}, {b})]] = [[recdec(0, {REP})]]  (확인)", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = [[recdec(0, {REP})]]라 하면 {TEN}x − x = {V}에서 x = [[frac({V}, {NINES})]] = [[frac({a}, {b})]]이므로 a = {a}, b = {b}이고 {ASK} = {ans}이다.",
        rubric=[
            {"element": "10ⁿ 곱해 빼기", "points": 3, "criterion": "x = [[recdec(0, {REP})]]로 놓고 {TEN}x − x = {V}{eul(V)} 얻었다.", "partial": "순환마디 길이와 다른 10ⁿ을 곱해 소수 부분이 남았으면 인정하지 않는다."},
            {"element": "기약분수", "points": 2, "criterion": "x = [[frac({V}, {NINES})]]{eul(V)} 약분해 [[frac({a}, {b})]]{eul(a)} 구했다.", "partial": "약분하지 않은 분수를 답으로 썼으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "a = {a}, b = {b}에서 {ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


# t4 — 혼합 순환소수 → 기약분수
MREP_ROWS = {}
for _i in (0, 1, 2):
    for _pre in [str(x) for x in range(1, 10)] + ["12", "15", "23", "25", "31", "36", "42", "45", "51", "63", "72", "81"]:
        for _cyc in [str(x) for x in range(1, 10)] + ["12", "13", "18", "21", "24", "27", "32", "36", "45", "54", "63", "72", "81", "90"]:
            if len(_pre) == 2 and len(_cyc) == 2:
                continue
            if _pre[-1] == _cyc[-1]:                       # 0.1 1̇ = 0.1̇ 처럼 순환하지 않는 부분이 줄어드는 꼴 제외
                continue
            _K, _L = len(_pre), len(_cyc)
            _all = int(str(_i) + _pre + _cyc)
            _pv = int(str(_i) + _pre)
            _num, _den = _all - _pv, (10 ** _L - 1) * 10 ** _K
            if gcd(_num, _den) == 1:
                continue
            MREP_ROWS[f"{_i}-{_pre}-{_cyc}"] = {"I": _i, "PRE": _pre, "CYC": _cyc, "PN": int(_pre), "CN": int(_cyc), "K": _K, "L": _L,
                                                  "ALL": _all, "PV": _pv, "NUM": _num, "DEN": _den, "TENA": 10 ** (_K + _L), "TENK": 10 ** _K}


def rd_t4():
    return tpl(RD, 4, RD_BASE,
        title="순환하지 않는 부분이 있는 순환소수를 기약분수로 — a + b (b − a)",
        skill="10ᵏ⁺ˡx와 10ᵏx의 차로 순환 부분을 없애 분수로 만든 뒤 약분하기",
        variant_axis={"정수부": "0~2", "비순환·순환 자릿수": "(1,1)·(1,2)·(2,1)", "구하는 것": "a + b / b − a"},
        discriminates="순환하지 않는 부분이 있을 때 두 식(10ᵏ⁺ˡx, 10ᵏx)의 소수 부분을 맞추어 빼는가, 분모를 99·900처럼 자릿수에 맞게 두는가",
        difficulty=3,
        params=[{"name": "rep", "values": {"in": list(MREP_ROWS)}}, {"name": "ask", "values": {"in": list(ASK2_ROWS)}}],
        table=[{"key": "rep", "rows": MREP_ROWS}, {"key": "ask", "rows": ASK2_ROWS}],
        derive={"g": "gcd(NUM, DEN)", "a": "NUM / g", "b": "DEN / g", "ans": "b + s*a"},
        constraints=["g > 1", "ans != I", "ans != PN", "ans != CN", "ans != 0", "a != b"],
        cost_values=["ALL", "PV", "NUM", "DEN", "g", "a", "b", "ans"],
        answer_var="ans",
        verify=["ans == b + s*a", "a * DEN == b * NUM", "gcd(a, b) == 1", "TENA - TENK == DEN", "ALL - PV == NUM"],
        question="순환소수 [[recdec({I}, {PRE}, {CYC})]]{eul(CN)} 기약분수 [[frac(a, b)]]로 나타낼 때, {ASK}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="순환소수를 x로 놓고, 소수 부분이 순환마디부터 시작하도록 {TENK}x를, 순환마디가 한 번 지나가도록 {TENA}x를 만든다. 두 식의 소수 부분이 같으므로 빼면 순환 부분이 사라지고 {DEN}x = {ALL} − {PV}가 된다. 분모는 (순환마디 길이만큼 9)(순환하지 않는 자릿수만큼 0)인 {DEN}이 되고, 마지막에 반드시 약분한다.",
        sol2=[
            "x = [[recdec({I}, {PRE}, {CYC})]]로 놓으면 {TENA}x = [[recdec({ALL}, {CYC})]], {TENK}x = [[recdec({PV}, {CYC})]]",
            "{TENA}x − {TENK}x = {ALL} − {PV}이므로 {DEN}x = {NUM}",
            "x = [[frac({NUM}, {DEN})]] = [[frac({a}, {b})]] ({g}로 약분)이므로 a = {a}, b = {b}, {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "{TENA}x = [[recdec({ALL}, {CYC})]]", "hint": "순환마디가 한 번 지나가게"},
            {"text": "{TENK}x = [[recdec({PV}, {CYC})]]", "hint": "소수 부분이 순환마디부터 시작하게"},
            {"text": "{DEN}x = {ALL} − {PV} = {NUM} → x = [[frac({a}, {b})]]", "marks": [{"on": "[[frac({a}, {b})]]", "note": "{g}로 약분"}]},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")], [reveal(3)]],
        sol3="[[frac({a}, {b})]]{eul(a)} 소수로 고치면 [[recdec({I}, {PRE}, {CYC})]]{ika(CN)} 되어 처음 순환소수와 같다. 분모를 {DEN}이 아니라 순환마디 길이만큼의 9로만 두면 값이 달라진다. 따라서 {ASK} = {ans}이다.",
        sol3_fig=steps(["[[frac({a}, {b})]] = [[recdec({I}, {PRE}, {CYC})]]  (확인)", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = [[recdec({I}, {PRE}, {CYC})]]라 하면 {TENA}x − {TENK}x = {ALL} − {PV}에서 {DEN}x = {NUM}, x = [[frac({NUM}, {DEN})]] = [[frac({a}, {b})]]이므로 a = {a}, b = {b}이고 {ASK} = {ans}이다.",
        rubric=[
            {"element": "두 식의 차", "points": 3, "criterion": "{TENA}x와 {TENK}x를 만들어 {TENA}x − {TENK}x = {ALL} − {PV}{eul(PV)} 얻었다.", "partial": "10ⁿx와 x를 빼서 소수 부분이 남았으면 인정하지 않는다."},
            {"element": "기약분수", "points": 2, "criterion": "x = [[frac({NUM}, {DEN})]]{eul(NUM)} 약분해 [[frac({a}, {b})]]{eul(a)} 구했다.", "partial": "약분하지 않은 분수로 a, b를 읽었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "a = {a}, b = {b}에서 {ASK} = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


# t5 / t6 — 유한소수가 되도록 곱하는 가장 작은 자연수 (t5: 이미 기약분수, t6: 먼저 약분)
N_LIST = [6, 12, 14, 15, 18, 21, 22, 24, 26, 28, 30, 33, 35, 36, 39, 42, 44, 45, 48, 52, 54, 55, 56, 60, 63, 65, 66, 70, 72, 75, 77, 78, 84, 88, 90, 91, 96, 98, 99,
          105, 110, 120, 126, 130, 132, 140, 150, 154, 165, 168, 175, 180, 195, 198, 210, 220, 225, 231, 264, 275, 300, 330, 350, 360, 396, 420, 450, 495, 550]


def _fro(n: int) -> str:
    """소인수분해 문자열 뒤의 '로/으로' — 마지막 소인수가 거듭제곱이면 '…제곱' → 으로, 3·13 → 으로, 2·5·7·11 → 로"""
    pr, e = sorted(fac(n).items())[-1]
    return "으로" if e > 1 or pr in (3, 13) else "로"


def _mrow(m: int) -> dict:
    """2·5 이외의 부분 m 의 표 조각: 소인수 문자열과 조사용 마지막 소인수"""
    fs = sorted(fac(m))
    return {"MF": fstr(m), "MLAST": fs[-1] if fs else m}


FIN_ROWS = {}
for _n in N_LIST:
    _m = strip25(_n)
    if _m < 3 or _m == _n:
        continue
    _d2 = _n // _m
    if 10000 % _d2 != 0:
        continue
    for _a in range(1, 21):
        if _a < _n and gcd(_a, _n) == 1:
            FIN_ROWS[f"{_a}-{_n}"] = {"A": _a, "N": _n, "F": fstr(_n), "FRO": _fro(_n), "M": _m, "D2": _d2, **_mrow(_m)}

RED_ROWS = {}
for _n in N_LIST:
    _m = strip25(_n)
    if _m < 3:
        continue
    for _a in range(2, 41):
        _g = gcd(_a, _n)
        if _a >= _n or _g == 1:
            continue
        _n2 = _n // _g
        _m2 = strip25(_n2)
        _d2 = _n2 // _m2
        if _m2 < 3 or _m2 == _m or _m2 == _n2 or 10000 % _d2 != 0:
            continue
        _r = _mrow(_m2)
        RED_ROWS[f"{_a}-{_n}"] = {"A": _a, "N": _n, "G": _g, "A2": _a // _g, "N2": _n2, "F": fstr(_n), "M": _m, "F2": fstr(_n2), "M2": _m2, "D2": _d2,
                                  "MF2": _r["MF"], "MLAST2": _r["MLAST"]}


def rd_t5():
    return tpl(RD, 5, RD_BASE,
        title="분수에 곱하여 유한소수가 되게 하는 가장 작은 자연수 — 분모의 2·5 이외의 소인수",
        skill="분모를 소인수분해해 2, 5 이외의 소인수를 찾고, 그것이 약분되도록 곱할 가장 작은 자연수를 정하기",
        variant_axis={"분모": "6~550 (2·5 이외 소인수 3·7·9·11·13·21…)", "분자": "1~20 (분모와 서로소)"},
        discriminates="유한소수의 조건을 '기약분수의 분모의 소인수가 2, 5뿐'으로 알고, 2·5 이외의 소인수 전부(예: 3 × 7 = 21)를 곱하는가",
        difficulty=2,
        params=[{"name": "f", "values": {"in": list(FIN_ROWS)}}],
        table={"key": "f", "rows": FIN_ROWS},
        derive={"ans": "M", "MD": "M * D2"},
        constraints=["ans != A", "ans != N"],
        cost_values=["A", "N", "M", "ans"],
        answer_var="ans",
        verify=["ans == M", "N == M * D2", "gcd(A, N) == 1", "M % 2 != 0", "M % 5 != 0"],
        question="분수 [[frac({A},{N})]]에 자연수 x를 곱하면 유한소수가 된다고 할 때, x의 값이 될 수 있는 가장 작은 자연수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="분수를 소수로 나타냈을 때 유한소수가 되려면 기약분수의 분모의 소인수가 2와 5뿐이어야 한다. [[frac({A},{N})]]{eun(A)} 이미 기약분수이고 {N} = {F}이므로 분모에 2, 5 이외의 소인수 {MF}{ika(MLAST)} 있다. 이것이 약분되어 없어지도록 x는 {M}의 배수여야 하고, 그중 가장 작은 것이 {M}이다.",
        sol2=[
            "{N} = {F}이므로 분모에 2, 5 이외의 소인수 {MF}{ika(MLAST)} 있다",
            "[[frac({A},{N})]] × x가 유한소수가 되려면 x가 {MF}{eul(MLAST)} 약분해 없애야 하므로 x는 {M}의 배수",
            "따라서 가장 작은 자연수 x = {M}",
        ],
        sol2_fig=steps([
            {"text": "{N} = {F}", "hint": "분모의 소인수분해"},
            {"text": "2, 5 이외의 소인수: {MF}", "hint": "이것이 남으면 무한소수"},
            {"text": "x = {M}의 배수 → 가장 작은 x = {M}", "marks": [{"on": "{M}", "note": "2·5 이외의 소인수를 모두 곱한 수"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="실제로 [[frac({A},{N})]] × {M} = [[frac({A}, {D2})]] = {dec(A/D2)}{ro(dec(A/D2))} 유한소수가 된다. {M}보다 작은 자연수는 {M}의 배수가 아니므로 분모에 2, 5 이외의 소인수가 남는다. 따라서 답은 {M}이다.",
        sol3_fig=steps(["[[frac({A},{N})]] × {M} = [[frac({A}, {D2})]] = {dec(A/D2)}", "가장 작은 x = {M}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{N} = {F}이므로 [[frac({A},{N})]] × x가 유한소수가 되려면 x는 2, 5 이외의 소인수 {MF}{eul(MLAST)} 없애는 {M}의 배수여야 한다. 따라서 가장 작은 자연수 x는 {M}이다.",
        rubric=[
            {"element": "분모의 소인수분해", "points": 3, "criterion": "{N} = {F}{FRO} 소인수분해해 2, 5 이외의 소인수 {MF}{eul(MLAST)} 찾았다.", "partial": "소인수분해는 맞고 2, 5 이외의 소인수를 일부만 찾았으면 1점."},
            {"element": "곱할 수의 조건", "points": 2, "criterion": "x가 {M}의 배수여야 함을 밝혔다.", "partial": "분모 전체 {N}의 배수로 두었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "가장 작은 자연수 x = {M}{eul(M)} 구했다."},
        ],
        rubric_total=7,
    )


def rd_t6():
    return tpl(RD, 6, RD_BASE,
        title="약분이 필요한 분수에 곱하여 유한소수가 되게 하는 가장 작은 자연수",
        skill="먼저 기약분수로 약분한 다음 분모의 2·5 이외의 소인수를 찾아 곱할 가장 작은 자연수를 정하기",
        variant_axis={"분모": "6~550", "분자": "2~40 (분모와 공약수 있음)"},
        discriminates="유한소수 판정은 기약분수에서 해야 함을 알고 약분을 먼저 하는가 — 약분 없이 분모의 소인수만 보면 답이 커진다",
        difficulty=3,
        params=[{"name": "f", "values": {"in": list(RED_ROWS)}}],
        table={"key": "f", "rows": RED_ROWS},
        derive={"ans": "M2"},
        constraints=["ans != A", "ans != N", "ans != M"],
        cost_values=["A", "N", "G", "A2", "N2", "M2", "ans"],
        answer_var="ans",
        verify=["ans == M2", "A2 * G == A", "N2 * G == N", "gcd(A2, N2) == 1", "N2 == M2 * D2", "M2 % 2 != 0", "M2 % 5 != 0", "M2 != M"],
        question="분수 [[frac({A},{N})]]{wa(A)} 자연수 x의 곱이 유한소수가 되도록 하는 가장 작은 자연수 x를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="유한소수가 되는지는 기약분수의 분모로 판단해야 한다. [[frac({A},{N})]]{eun(A)} 분자와 분모에 공약수 {G}{ika(G)} 있으므로 먼저 약분하면 [[frac({A2},{N2})]]이고, {N2} = {F2}이므로 2, 5 이외의 소인수는 {MF2}{ida(MLAST2)}. 약분하지 않고 {N} = {F}에서 소인수를 읽으면 필요 없는 소인수까지 곱하게 된다.",
        sol2=[
            "[[frac({A},{N})]]{eul(A)} {G}{ro(G)} 약분하면 [[frac({A2},{N2})]]",
            "{N2} = {F2}이므로 2, 5 이외의 소인수는 {MF2}",
            "x가 {MF2}{eul(MLAST2)} 없애야 하므로 x는 {M2}의 배수이고, 가장 작은 x = {M2}",
        ],
        sol2_fig=steps([
            {"text": "[[frac({A},{N})]] = [[frac({A2},{N2})]]", "hint": "먼저 {G}{ro(G)} 약분"},
            {"text": "{N2} = {F2}", "hint": "기약분수의 분모를 소인수분해"},
            {"text": "2, 5 이외의 소인수 {MF2} → x = {M2}", "marks": [{"on": "{M2}", "note": "약분 전 {N} = {F}로 읽으면 {M}{ro(M)} 틀림"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="[[frac({A},{N})]] × {M2} = [[frac({A2},{N2})]] × {M2} = [[frac({A2}, {D2})]] = {dec(A2/D2)}{ro(dec(A2/D2))} 유한소수가 된다. 약분하지 않고 얻는 {M}{eun(M)} 조건을 만족하지만 가장 작은 수가 아니다. 따라서 답은 {M2}이다.",
        sol3_fig=steps(["[[frac({A2},{N2})]] × {M2} = [[frac({A2}, {D2})]] = {dec(A2/D2)}", "가장 작은 x = {M2} ({M}{eun(M)} 더 큰 배수)"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="[[frac({A},{N})]] = [[frac({A2},{N2})]]이고 {N2} = {F2}이므로 곱이 유한소수가 되려면 x는 {M2}의 배수여야 한다. 따라서 가장 작은 자연수 x는 {M2}이다.",
        rubric=[
            {"element": "약분", "points": 3, "criterion": "[[frac({A},{N})]]{eul(A)} 기약분수 [[frac({A2},{N2})]]{ro(N2)} 약분했다.", "partial": "약분하지 않고 {N} = {F}의 소인수로 풀었으면 인정하지 않는다."},
            {"element": "2·5 이외의 소인수", "points": 2, "criterion": "{N2} = {F2}에서 2, 5 이외의 소인수 {MF2}{eul(MLAST2)} 찾았다.", "partial": "소인수를 일부만 찾았으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "가장 작은 자연수 x = {M2}{eul(M2)} 구했다.", "partial": "{M}{eul(M)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


# t7 — x/N 이 유한소수가 되는 x (B 이하) 의 개수
CNT_ROWS = {}
for _n in N_LIST:
    _m = strip25(_n)
    if 3 <= _m < _n and _n <= 300:
        CNT_ROWS[str(_n)] = {"N": _n, "F": fstr(_n), "M": _m, **_mrow(_m)}
B_VALUES = [30, 40, 50, 60, 80, 100, 120, 150, 200]


def rd_t7():
    return tpl(RD, 7, RD_BASE,
        title="x/N이 유한소수가 되도록 하는 B 이하의 자연수 x의 개수",
        skill="분모의 2·5 이외의 소인수가 약분되려면 x가 그 배수여야 함을 알고, 범위 안의 배수의 개수를 세기",
        variant_axis={"분모": "6~300", "x의 범위": "30~200 이하"},
        discriminates="x가 분모의 2·5 이외의 소인수(예: 21)의 배수여야 함을 알고, 분모 전체의 배수로 세지 않는가",
        difficulty=3,
        params=[{"name": "N", "values": {"in": list(CNT_ROWS)}}, {"name": "B", "values": {"in": B_VALUES}}],
        table={"key": "N", "rows": CNT_ROWS},
        derive={"ans": "floor(B / M)", "ans1": "floor(B / M) + 1", "M2x": "2*M", "LAST": "M*ans", "NEXT": "M*ans1"},
        constraints=["ans >= 3", "ans != N", "ans != B", "ans != M", "N != B"],
        cost_values=["N", "B", "M", "ans"],
        answer_var="ans",
        verify=["ans == floor(B / M)", "M * ans <= B", "M * (ans + 1) > B", "M % 2 != 0", "M % 5 != 0", "N % M == 0"],
        question="x가 {B} 이하의 자연수일 때, 분수 [[frac(x, {N})]]{ika(N)} 유한소수가 되도록 하는 x의 개수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{N} = {F}이므로 [[frac(x, {N})]]{ika(N)} 유한소수가 되려면 분모의 2, 5 이외의 소인수 {MF}{ika(MLAST)} 약분되어 없어져야 한다. 그러려면 x가 {M}의 배수여야 하므로, {B} 이하의 자연수 중 {M}의 배수의 개수를 세면 된다.",
        sol2=[
            "{N} = {F}이므로 2, 5 이외의 소인수는 {MF}",
            "[[frac(x, {N})]]{ika(N)} 유한소수 ⟺ x가 {M}의 배수",
            "{B} 이하의 {M}의 배수는 {M}, {M2x}, …, {LAST}의 {ans}개",
        ],
        sol2_fig=steps([
            {"text": "{N} = {F}", "hint": "2, 5 이외의 소인수 {MF}"},
            {"text": "x = {M}의 배수", "hint": "{MF}{ika(MLAST)} 약분되어야 한다"},
            {"text": "{M}, {M2x}, …, {LAST} → {ans}개", "marks": [{"on": "{LAST}", "note": "{M} × {ans} ≤ {B}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{M} × {ans} = {LAST}{eun(LAST)} {B} 이하이고 {M} × {ans1} = {NEXT}{eun(NEXT)} {B}보다 크므로 {B} 이하의 {M}의 배수는 {ans}개다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{M} × {ans} = {LAST} ≤ {B} < {NEXT} = {M} × {ans1}", "x의 개수 = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{N} = {F}이므로 [[frac(x, {N})]]{ika(N)} 유한소수가 되려면 x는 {M}의 배수여야 한다. {B} 이하의 {M}의 배수는 {M}, {M2x}, …, {LAST}의 {ans}개이므로 답은 {ans}이다.",
        rubric=[
            {"element": "x의 조건", "points": 3, "criterion": "{N} = {F}에서 x가 {M}의 배수여야 함을 밝혔다.", "partial": "x를 {N}의 배수로 두었으면 인정하지 않는다."},
            {"element": "개수 세기", "points": 2, "criterion": "{B} 이하의 {M}의 배수가 {ans}개임을 구했다.", "partial": "범위의 끝을 잘못 세어 1개 차이면 1점."},
        ],
        rubric_total=5,
    )


# t8 — A/(2ᵃ5ᵇ x) 가 유한소수가 되는 한 자리 자연수 x 의 개수
def _cnt_rows():
    out = {}
    for A in (1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14, 15, 17, 18, 21, 22, 24, 27, 28, 33, 35, 36, 42, 49, 54, 63):
        xs = [x for x in range(1, 10) if A % strip25(x) == 0]
        by3 = A % 3 == 0
        by9 = A % 9 == 0
        by7 = A % 7 == 0
        note3 = ("x = 3, 6은 분모에 3이 생기지만 " + f"{A}{'이' if str(A)[-1] in '013678' else '가'} 3의 배수이므로 약분되어 유한소수가 된다") if by3 else \
                (f"x = 3, 6, 9는 분모에 3이 남는다({A}{'은' if str(A)[-1] in '013678' else '는'} 3의 배수가 아님)")
        note9 = ("x = 9도 3² = 9가 약분되어 된다" if by9 else "x = 9는 9 = 3²이 약분되지 않아 안 된다") if by3 else ""
        note7 = (f"x = 7은 {A}{'이' if str(A)[-1] in '013678' else '가'} 7의 배수이므로 된다") if by7 else "x = 7은 분모에 7이 남아 안 된다"
        out[str(A)] = {"A": A, "CNT": len(xs), "XS": ", ".join(map(str, xs)), "NOTE3": note3 + (", " + note9 if note9 else ""), "NOTE7": note7}
    return out


CNT9_ROWS = _cnt_rows()
BASE_ROWS = {
    "b1": {"BASE": "2 × 5 × x", "BT": "2 × 5", "HAS5": 1},
    "b2": {"BASE": "pow(2,2) × 5 × x", "BT": "2² × 5", "HAS5": 1},
    "b3": {"BASE": "2 × pow(5,2) × x", "BT": "2 × 5²", "HAS5": 1},
    "b4": {"BASE": "pow(2,3) × x", "BT": "2³", "HAS5": 0},
    "b5": {"BASE": "pow(2,2) × pow(5,2) × x", "BT": "2² × 5²", "HAS5": 1},
    "b6": {"BASE": "pow(5,2) × x", "BT": "5²", "HAS5": 1},
}


def rd_t8():
    return tpl(RD, 8, RD_BASE,
        title="분모에 x가 있는 분수가 유한소수가 되도록 하는 한 자리 자연수 x의 개수",
        skill="x의 소인수 중 2, 5 이외의 것이 분자와 약분되는지를 1부터 9까지 하나씩 따져 개수를 세기",
        variant_axis={"분자": "1~63", "분모의 2·5 부분": "2×5 / 2²×5 / 2×5² / 2³ / 2²×5² / 5²"},
        discriminates="x = 1, 2, 4, 5, 8은 항상 되고 x = 3, 6, 7, 9는 분자가 그 소인수의 배수일 때만 됨을 가려내는가",
        difficulty=3, process="문제해결",
        params=[{"name": "A", "values": {"in": list(CNT9_ROWS)}}, {"name": "b", "values": {"in": list(BASE_ROWS)}}],
        table=[{"key": "A", "rows": CNT9_ROWS}, {"key": "b", "rows": BASE_ROWS}],
        derive={"ans": "CNT"},
        constraints=["ans != A", "HAS5 == 0 or ans != 5"],
        cost_values=["A", "ans"],
        answer_var="ans",
        verify=["ans == CNT", "ans >= 5", "ans <= 9"],
        question="분수 [[frac({A}, {BASE})]]{ika(A)} 유한소수가 되도록 하는 한 자리 자연수 x의 개수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="분모의 {BT} 부분은 소인수가 2, 5뿐이므로 상관없고, x의 소인수 중 2, 5 이외의 것이 분자 {A}{wa(A)} 약분되어 없어지는지만 보면 된다. x = 1, 2, 4, 5, 8은 소인수가 2, 5뿐이라 항상 유한소수가 되고, x = 3, 6, 9는 3(또는 9)이, x = 7은 7이 {A}의 약수일 때만 된다.",
        sol2=[
            "x = 1, 2, 4, 5, 8: x의 소인수가 2, 5뿐이므로 항상 유한소수 (5개)",
            "{NOTE3}",
            "{NOTE7}. 따라서 x = {XS}의 {ans}개",
        ],
        sol2_fig=steps([
            {"text": "x = 1, 2, 4, 5, 8 → 항상 됨", "hint": "소인수가 2, 5뿐"},
            {"text": "x = 3, 6, 9 → 3(9)이 {A}{wa(A)} 약분되는가", "hint": "{A}{ika(A)} 3의 배수인지"},
            {"text": "x = 7 → 7이 {A}{wa(A)} 약분되는가", "hint": "{A}{ika(A)} 7의 배수인지"},
            {"text": "x = {XS} → {ans}개", "marks": [{"on": "{ans}개", "note": "하나씩 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="x = {XS}일 때 분모의 2, 5 이외의 소인수가 모두 {A}{wa(A)} 약분되어 분모에 2, 5만 남는다. 나머지 x는 분모에 3 또는 7이 남아 무한소수가 된다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["되는 x: {XS}", "x의 개수 = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x = 1, 2, 4, 5, 8은 소인수가 2, 5뿐이므로 항상 유한소수가 된다. {NOTE3}. {NOTE7}. 따라서 x = {XS}의 {ans}개이다.",
        rubric=[
            {"element": "항상 되는 x", "points": 2, "criterion": "x = 1, 2, 4, 5, 8은 소인수가 2, 5뿐이라 유한소수가 됨을 밝혔다.", "partial": "일부만 찾았으면 1점."},
            {"element": "3·7의 약분 판단", "points": 3, "criterion": "x = 3, 6, 9와 x = 7에 대해 분자 {A}{wa(A)} 약분되는지 판단했다.", "partial": "9 = 3²의 약분을 잘못 판단했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "x = {XS}의 {ans}개임을 구했다."},
        ],
        rubric_total=7,
    )


RD_SEED = {
    "seed_id": RD, "category": "연산",
    "title": "유리수와 순환소수 — 소수점 아래 n번째 자리·순환소수를 분수로·유한소수가 되는 조건",
    "unit_id": "m2-1", "concept_ids": ["m2-1-01", "m2-1-02"],
    "schema_id": None, "schema_name": "유리수의 소수 표현과 순환소수",
    "source_item_ids": [],
    "note": "순환소수는 recdec 마커(자릿수 라벨은 원문 유지). n번째 자리 답은 floor(10ⁿ·P/Q) mod 10 으로 파생해 순환마디 표와 독립으로 검산된다. 유한소수 조건 틀은 (A, N) 쌍을 표로 미리 걸러(2·5 이외의 부분 ≥ 3, 소수 확인용 분모 | 10⁴) 넣는다.",
    "geometry": False,
    "templates": [rd_t1(), rd_t2(), rd_t3(), rd_t4(), rd_t5(), rd_t6(), rd_t7(), rd_t8()],
}


# ═══════════════════════════════════════════════════════════════════ 공용: 계수 조각 표 (마커용 / 평문용)
def _lead(v: int, var: str, marker: bool) -> str:
    """앞항 조각: 2 → '2*x'/'2x', -1 → '-x', 1 → 'x'"""
    if v == 1:
        return var
    if v == -1:
        return "-" + var
    return f"{v}*{var}" if marker else f"{v}{var}"


def _sgnt(v: int, var: str, marker: bool) -> str:
    """부호 붙은 항 조각: 2 → '+ 2*x'/'+ 2x', -1 → '- x'/'− x', 1 → '+ x'"""
    s = ("+ " if v > 0 else ("- " if marker else "− "))
    a = abs(v)
    if var == "":
        body = str(a)
    else:
        body = var if a == 1 else (f"{a}*{var}" if marker else f"{a}{var}")
    return s + body


def lead_rows(vals, key, var, marker=False):
    return {"key": key, "rows": {str(v): {f"{key.upper()}L": _lead(v, var, marker)} for v in vals}}


def sgn_rows(vals, key, var, marker=False):
    return {"key": key, "rows": {str(v): {f"{key.upper()}S": _sgnt(v, var, marker)} for v in vals}}


NZ3 = [-3, -2, -1, 1, 2, 3]
NZ4 = [-4, -3, -2, -1, 1, 2, 3, 4]
NZ6 = [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]
SUP_ROWS = lambda key, hi, name: {"key": key, "rows": {str(i): {name: sup(i)} for i in range(1, hi + 1)}}   # noqa: E731

# ═══════════════════════════════════════════════════════════════════ 2. 단항식의 곱셈과 나눗셈
MO = "m2-1-monomial"
MO_BASE = {**BASE, "prereq": ["지수법칙"], "ops": ["단항식의 계산"], "traps": ["지수의 곱·합 혼동", "부호"], "tags": ["단항식의 곱셈과 나눗셈"]}


def mo_t1():
    return tpl(MO, 1, MO_BASE,
        title="(pxᵐy)ᵏ × qxyⁿ = axᵇyᶜ — 계수와 지수 결정 후 a + b + c",
        skill="괄호의 거듭제곱은 계수·지수에 모두 지수를 곱하고, 단항식의 곱은 계수끼리 곱하고 지수를 더하기",
        variant_axis={"계수": "p ±2·±3, q ±2~±5", "지수": "m 1~3, n 1~3, k 2~3"},
        discriminates="괄호의 거듭제곱에서 계수에도 지수를 적용하고 음수의 홀수·짝수 거듭제곱 부호를 맞히는가, 곱셈에서 지수를 더하는가",
        difficulty=2,
        params=[{"name": "p", "values": {"in": [-3, -2, 2, 3]}}, {"name": "k", "values": {"in": [2, 3]}}, {"name": "q", "values": {"in": [-5, -4, -3, -2, 2, 3, 4, 5]}},
                {"name": "m", "values": {"int": [1, 3]}}, {"name": "n", "values": {"int": [1, 3]}}],
        table=[SUP_ROWS("m", 3, "SM"), SUP_ROWS("n", 3, "SN"), SUP_ROWS("k", 3, "SK")],
        derive={"pk": "p**k", "mk": "m*k", "a": "p**k * q", "b": "m*k + 1", "c": "k + n", "ans": "p**k * q + m*k + 1 + k + n"},
        constraints=["ans != p", "ans != q", "abs(a) <= 200", "ans != 0"],
        cost_values=["p", "q", "pk", "a", "b", "c", "ans"],
        answer_var="ans",
        verify=["ans == a + b + c", "a == pk * q", "b == mk + 1", "c == k + n"],
        question="({co(p)}x{SM}y){SK} × ({co(q)}xy{SN}) = axᵇyᶜ일 때, 상수 a, b, c에 대하여 a + b + c의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="괄호의 거듭제곱은 계수와 각 문자의 지수에 모두 지수를 곱한다((ab)ⁿ = aⁿbⁿ, (xᵐ)ⁿ = xᵐⁿ). 단항식끼리의 곱은 계수는 계수끼리 곱하고 같은 문자는 지수를 더한다. 음수 계수의 거듭제곱은 지수가 짝수면 +, 홀수면 −가 된다.",
        sol2=[
            "({co(p)}x{SM}y){SK} = [[{pk}*pow(x,{mk})*pow(y,{k})]] — 계수는 {pn(p)}{SK} = {pk}, x의 지수는 {m} × {k} = {mk}, y의 지수는 {k}",
            "[[{pk}*pow(x,{mk})*pow(y,{k})]] × ({co(q)}xy{SN}) = [[{a}*pow(x,{b})*pow(y,{c})]] — 계수 {pk} × {pn(q)} = {a}, x의 지수 {mk} + 1 = {b}, y의 지수 {k} + {n} = {c}",
            "따라서 a = {a}, b = {b}, c = {c}이므로 a + b + c = {ans}",
        ],
        sol2_fig=steps([
            {"text": "({co(p)}x{SM}y){SK} = [[{pk}*pow(x,{mk})*pow(y,{k})]]", "hint": "계수 {pn(p)}{SK} = {pk}, 지수는 × {k}"},
            {"text": "× ({co(q)}xy{SN}) = [[{a}*pow(x,{b})*pow(y,{c})]]", "hint": "계수는 곱하고 지수는 더한다"},
            {"text": "a + b + c = {a} + {b} + {c} = {ans}", "marks": [{"on": "{ans}", "note": "a의 부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="괄호에서는 지수를 곱하고 곱셈에서는 지수를 더했는지 확인한다: x의 지수 {m} × {k} + 1 = {b}, y의 지수 {k} + {n} = {c}. 계수는 {pn(p)}{SK} = {pk}이고 {pk} × {pn(q)} = {a}이다. 따라서 a + b + c = {ans}이다.",
        sol3_fig=steps(["x: {m} × {k} + 1 = {b},  y: {k} + {n} = {c}", "계수: {pk} × {pn(q)} = {a}", "a + b + c = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        model_answer="({co(p)}x{SM}y){SK} × ({co(q)}xy{SN}) = [[{pk}*pow(x,{mk})*pow(y,{k})]] × ({co(q)}xy{SN}) = [[{a}*pow(x,{b})*pow(y,{c})]]이므로 a = {a}, b = {b}, c = {c}이고 a + b + c = {ans}이다.",
        rubric=[
            {"element": "괄호의 거듭제곱", "points": 3, "criterion": "({co(p)}x{SM}y){SK} = [[{pk}*pow(x,{mk})*pow(y,{k})]]으로 계수와 지수에 모두 {k}제곱을 적용했다.", "partial": "계수에 거듭제곱을 하지 않았거나 부호가 틀렸으면 1점."},
            {"element": "단항식의 곱셈", "points": 2, "criterion": "계수 {pk} × {pn(q)} = {a}, 지수 {mk} + 1 = {b}, {k} + {n} = {c}{ro(c)} 곱했다.", "partial": "지수를 곱해 구했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "a + b + c = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


def mo_t2():
    return tpl(MO, 2, MO_BASE,
        title="(pxᵐyⁿ)ᵏ ÷ qxˢyᵗ = axᵇyᶜ — 나눗셈에서 계수·지수 결정 후 a + b + c",
        skill="괄호의 거듭제곱을 먼저 계산하고, 나눗셈은 계수끼리 나누고 같은 문자의 지수를 빼기",
        variant_axis={"계수": "p ±2·±3, q ±2~±9 (나누어떨어짐)", "지수": "m 1~3, n 1~2, k 2~3, s 1~3, t 1~2"},
        discriminates="나눗셈에서 지수를 빼는가(나누지 않는가), 계수의 부호를 바르게 나누는가",
        difficulty=3,
        params=[{"name": "p", "values": {"in": [-3, -2, 2, 3]}}, {"name": "k", "values": {"in": [2, 3]}}, {"name": "q", "values": {"in": [-9, -8, -6, -4, -3, -2, 2, 3, 4, 6, 8, 9]}},
                {"name": "m", "values": {"int": [1, 3]}}, {"name": "n", "values": {"int": [1, 2]}}, {"name": "s", "values": {"int": [1, 3]}}, {"name": "t", "values": {"int": [1, 2]}}],
        table=[SUP_ROWS("m", 3, "SM"), SUP_ROWS("n", 2, "SN"), SUP_ROWS("k", 3, "SK"), SUP_ROWS("s", 3, "SS"), SUP_ROWS("t", 2, "ST")],
        derive={"pk": "p**k", "mk": "m*k", "nk": "n*k", "a": "p**k / q", "b": "m*k - s", "c": "n*k - t", "ans": "p**k / q + m*k - s + n*k - t"},
        constraints=["a == floor(a)", "abs(a) >= 2", "b >= 2", "c >= 2", "ans != p", "ans != q", "ans != 0"],
        cost_values=["p", "q", "pk", "a", "b", "c", "ans"],
        answer_var="ans",
        verify=["ans == a + b + c", "a * q == pk", "b == mk - s", "c == nk - t"],
        question="({co(p)}x{SM}y{SN}){SK} ÷ ({co(q)}x{SS}y{ST}) = axᵇyᶜ일 때, 상수 a, b, c에 대하여 a + b + c의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="먼저 괄호의 거듭제곱을 계산해 계수와 지수를 정리한다. 단항식의 나눗셈은 계수는 계수끼리 나누고, 같은 문자는 지수를 뺀다(xᵐ ÷ xⁿ = xᵐ⁻ⁿ). 지수를 나누거나 부호를 빠뜨리지 않도록 한다.",
        sol2=[
            "({co(p)}x{SM}y{SN}){SK} = [[{pk}*pow(x,{mk})*pow(y,{nk})]] — 계수 {pn(p)}{SK} = {pk}, 지수 {m} × {k} = {mk}, {n} × {k} = {nk}",
            "[[{pk}*pow(x,{mk})*pow(y,{nk})]] ÷ ({co(q)}x{SS}y{ST}) = [[{a}*pow(x,{b})*pow(y,{c})]] — 계수 {pk} ÷ {pn(q)} = {a}, x의 지수 {mk} − {s} = {b}, y의 지수 {nk} − {t} = {c}",
            "따라서 a = {a}, b = {b}, c = {c}이므로 a + b + c = {ans}",
        ],
        sol2_fig=steps([
            {"text": "({co(p)}x{SM}y{SN}){SK} = [[{pk}*pow(x,{mk})*pow(y,{nk})]]", "hint": "괄호의 거듭제곱 먼저"},
            {"text": "÷ ({co(q)}x{SS}y{ST}) = [[{a}*pow(x,{b})*pow(y,{c})]]", "hint": "계수는 나누고 지수는 뺀다"},
            {"text": "a + b + c = {a} + {b} + {c} = {ans}", "marks": [{"on": "{ans}", "note": "지수를 나누지 않았는지"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="나눗셈은 역수의 곱이므로 [[{a}*pow(x,{b})*pow(y,{c})]] × ({co(q)}x{SS}y{ST}) = [[{pk}*pow(x,{mk})*pow(y,{nk})]]이 되는지 확인한다: 계수 {a} × {pn(q)} = {pk}, 지수 {b} + {s} = {mk}, {c} + {t} = {nk}. 따라서 a + b + c = {ans}이다.",
        sol3_fig=steps(["{a} × {pn(q)} = {pk}", "{b} + {s} = {mk},  {c} + {t} = {nk}", "a + b + c = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        model_answer="({co(p)}x{SM}y{SN}){SK} ÷ ({co(q)}x{SS}y{ST}) = [[{pk}*pow(x,{mk})*pow(y,{nk})]] ÷ ({co(q)}x{SS}y{ST}) = [[{a}*pow(x,{b})*pow(y,{c})]]이므로 a = {a}, b = {b}, c = {c}이고 a + b + c = {ans}이다.",
        rubric=[
            {"element": "괄호의 거듭제곱", "points": 3, "criterion": "({co(p)}x{SM}y{SN}){SK} = [[{pk}*pow(x,{mk})*pow(y,{nk})]]으로 계산했다.", "partial": "계수의 부호 또는 지수 하나가 틀렸으면 1점."},
            {"element": "단항식의 나눗셈", "points": 2, "criterion": "계수 {pk} ÷ {pn(q)} = {a}, 지수 {mk} − {s} = {b}, {nk} − {t} = {c}{ro(c)} 나누었다.", "partial": "지수를 나누어 구했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "a + b + c = {ans}{eul(ans)} 구했다."},
        ],
        rubric_total=7,
    )


KX_ROWS = {"key": "kx", "rows": {"1": {"KX": "x", "SKX": ""}, "2": {"KX": "pow(x,2)", "SKX": "²"}, "3": {"KX": "pow(x,3)", "SKX": "³"}}}
KY_ROWS = {"key": "ky", "rows": {"1": {"KY": "y", "SKY": "", "KEUL": "를", "KIKA": "가", "KEUN": "는"}, "2": {"KY": "pow(y,2)", "SKY": "²", "KEUL": "을", "KIKA": "이", "KEUN": "은"}}}
DX_ROWS = {"key": "dx", "rows": {"1": {"SDX": ""}, "2": {"SDX": "²"}}}
DY_ROWS = {"key": "dy", "rows": {"1": {"SDY": "", "DRO": "로", "DEUL": "를", "DIKA": "가"}, "2": {"SDY": "²", "DRO": "으로", "DEUL": "을", "DIKA": "이"}}}
K_VALS = [-5, -4, -3, -2, 2, 3, 4, 5]
D_VALS = [-3, -2, 2, 3]


def _box_common(no, title, skill, disc, question, sol1, step1, hint1, note, sol3, model, r1elem, r1crit, r1part, pitfall_note):
    return tpl(MO, no, MO_BASE,
        title=title, skill=skill,
        variant_axis={"□의 계수": "±2~±5", "나누는 식": "±2·±3 x^1~2 y^1~2"},
        discriminates=disc,
        difficulty=2, process="문제해결",
        params=[{"name": "k", "values": {"in": K_VALS}}, {"name": "kx", "values": {"int": [1, 3]}}, {"name": "ky", "values": {"int": [1, 2]}},
                {"name": "d", "values": {"in": D_VALS}}, {"name": "dx", "values": {"int": [1, 2]}}, {"name": "dy", "values": {"int": [1, 2]}}],
        table=[KX_ROWS, KY_ROWS, DX_ROWS, DY_ROWS],
        derive={"pc": "k*d", "px": "kx + dx", "py": "ky + dy"},
        constraints=["abs(pc) <= 15"],
        cost_values=["k", "d", "pc", "px", "py"],
        verify=["pc == k*d", "px == kx + dx", "py == ky + dy", "px >= 2", "py >= 2"],
        question=question,
        answer="[[{k}*{KX}*{KY}]]", answer_alt=[],
        sol1=sol1,
        sol2=[
            step1,
            "계수: {pc} ÷ {pn(d)} = {k}, x의 지수: {px} − {dx} = {kx}, y의 지수: {py} − {dy} = {ky}",
            "따라서 □ = [[{k}*{KX}*{KY}]]",
        ],
        sol2_fig=steps([
            {"text": step1, "hint": hint1},
            {"text": "계수 {pc} ÷ {pn(d)} = {k},  지수 {px} − {dx} = {kx}, {py} − {dy} = {ky}", "hint": "계수는 나누고 지수는 뺀다"},
            {"text": "□ = [[{k}*{KX}*{KY}]]", "marks": [{"on": "[[{k}*{KX}*{KY}]]", "note": note}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3=sol3,
        sol3_fig=steps(["[[{k}*{KX}*{KY}]] × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]  (확인)", "□ = [[{k}*{KX}*{KY}]]"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer=model,
        rubric=[
            {"element": r1elem, "points": 3, "criterion": r1crit, "partial": r1part},
            {"element": "계수·지수 계산", "points": 2, "criterion": "계수 {pc} ÷ {pn(d)} = {k}, 지수 {px} − {dx} = {kx}, {py} − {dy} = {ky}{ro(ky)} 구했다.", "partial": "지수를 더하거나 계수의 부호가 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "□ = [[{k}*{KX}*{KY}]]{KEUL} 구했다.", "partial": pitfall_note},
        ],
        rubric_total=7,
    )


def mo_t3():
    return _box_common(3,
        title="□ × (단항식) = (단항식)에서 □ 안에 알맞은 식",
        skill="□ × A = B이면 □ = B ÷ A임을 이용해 계수는 나누고 지수는 빼서 □를 구하기",
        disc="곱해서 B가 되는 식을 구할 때 B ÷ A로 역연산하는가, 지수를 빼고 계수의 부호를 바르게 나누는가",
        question="□ × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]일 때, □ 안에 알맞은 식을 구하시오.",
        sol1="□ × A = B이면 □ = B ÷ A이다(곱셈의 역연산은 나눗셈). 단항식의 나눗셈은 계수는 계수끼리 나누고, 같은 문자는 지수를 뺀다. 구한 □에 A를 다시 곱해 B가 되는지 확인하면 실수를 잡을 수 있다.",
        step1="□ = [[{pc}*pow(x,{px})*pow(y,{py})]] ÷ ({co(d)}x{SDX}y{SDY})",
        hint1="□ × A = B → □ = B ÷ A",
        note="다시 곱해 확인",
        sol3="구한 식을 다시 곱하면 [[{k}*{KX}*{KY}]] × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]으로 우변과 같다. 따라서 □ = [[{k}*{KX}*{KY}]]이다.",
        model="□ = [[{pc}*pow(x,{px})*pow(y,{py})]] ÷ ({co(d)}x{SDX}y{SDY}) = [[{k}*{KX}*{KY}]]이다.",
        r1elem="역연산 식", r1crit="□ = [[{pc}*pow(x,{px})*pow(y,{py})]] ÷ ({co(d)}x{SDX}y{SDY}){DRO} 놓았다.", r1part="□ = B × A로 놓았으면 인정하지 않는다.",
        pitfall_note="B × A를 답했으면 인정하지 않는다.",
    )


def mo_t4():
    return _box_common(4,
        title="(단항식) ÷ □ = (단항식)에서 □ 안에 알맞은 식",
        skill="A ÷ □ = B이면 □ = A ÷ B임을 이용해(□ × B = A) □를 구하기",
        disc="나누는 식을 구할 때 □ = A ÷ B로 놓는가(B ÷ A로 거꾸로 나누지 않는가), 지수를 빼고 계수를 바르게 나누는가",
        question="[[{pc}*pow(x,{px})*pow(y,{py})]] ÷ □ = {co(d)}x{SDX}y{SDY}일 때, □ 안에 알맞은 식을 구하시오.",
        sol1="A ÷ □ = B이면 □ × B = A이므로 □ = A ÷ B이다. 나누는 식을 구하는 것이므로 B ÷ A로 거꾸로 나누지 않도록 한다. 단항식의 나눗셈은 계수는 나누고 같은 문자의 지수는 뺀다.",
        step1="□ × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]이므로 □ = [[{pc}*pow(x,{px})*pow(y,{py})]] ÷ ({co(d)}x{SDX}y{SDY})",
        hint1="A ÷ □ = B → □ = A ÷ B",
        note="B ÷ A가 아님",
        sol3="구한 식으로 나누면 [[{pc}*pow(x,{px})*pow(y,{py})]] ÷ [[{k}*{KX}*{KY}]] = {co(d)}x{SDX}y{SDY}{DIKA} 되어 조건과 같다(계수 {pc} ÷ {pn(k)} = {d}). 따라서 □ = [[{k}*{KX}*{KY}]]이다.",
        model="A ÷ □ = B에서 □ = A ÷ B이므로 □ = [[{pc}*pow(x,{px})*pow(y,{py})]] ÷ ({co(d)}x{SDX}y{SDY}) = [[{k}*{KX}*{KY}]]이다.",
        r1elem="역연산 식", r1crit="□ = [[{pc}*pow(x,{px})*pow(y,{py})]] ÷ ({co(d)}x{SDX}y{SDY}){DRO} 놓았다.", r1part="□ = B ÷ A로 거꾸로 놓았으면 인정하지 않는다.",
        pitfall_note="B ÷ A의 결과를 답했으면 인정하지 않는다.",
    )


def mo_t5():
    return tpl(MO, 5, MO_BASE,
        title="어떤 단항식을 나누어야 할 것을 잘못 곱한 결과로 바르게 계산한 식 구하기",
        skill="어떤 식을 A로 놓아 잘못된 계산을 식으로 세우고, 역연산으로 A를 구한 뒤 바르게 나누기",
        variant_axis={"바른 결과의 계수": "±2~±5", "나누는 식": "±2·±3 x^1~2 y^1~2"},
        discriminates="잘못 곱한 결과를 한 번만 나누고 멈추지 않는가 — 어떤 식을 먼저 구하고(÷1회) 다시 나누어야(÷2회) 바른 결과가 된다",
        difficulty=3, process="문제해결",
        params=[{"name": "k", "values": {"in": K_VALS}}, {"name": "kx", "values": {"int": [1, 3]}}, {"name": "ky", "values": {"int": [1, 2]}},
                {"name": "d", "values": {"in": D_VALS}}, {"name": "dx", "values": {"int": [1, 2]}}, {"name": "dy", "values": {"int": [1, 2]}}],
        table=[KX_ROWS, KY_ROWS, DX_ROWS, DY_ROWS],
        derive={"ac": "k*d", "ax": "kx + dx", "ay": "ky + dy", "pc": "k*d*d", "px": "kx + 2*dx", "py": "ky + 2*dy"},
        constraints=["abs(pc) <= 45"],
        cost_values=["k", "d", "ac", "pc", "px", "py"],
        verify=["pc == ac*d", "px == ax + dx", "py == ay + dy", "ax >= 2", "ay >= 2"],
        question="어떤 단항식을 {co(d)}x{SDX}y{SDY}{DRO} 나누어야 할 것을 잘못하여 곱했더니 [[{pc}*pow(x,{px})*pow(y,{py})]]이 되었다. 바르게 계산한 식을 구하시오.",
        answer="[[{k}*{KX}*{KY}]]", answer_alt=[],
        sol1="어떤 단항식을 A라 하고 잘못 계산한 과정을 식으로 쓰면 A × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]이다. 여기서 A를 구하려면 한 번 나누고, 바르게 계산한 결과 A ÷ ({co(d)}x{SDX}y{SDY})를 얻으려면 한 번 더 나누어야 한다. 잘못된 결과를 한 번만 나눈 A를 답으로 쓰지 않도록 한다.",
        sol2=[
            "어떤 식을 A라 하면 A × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]이므로 A = [[{pc}*pow(x,{px})*pow(y,{py})]] ÷ ({co(d)}x{SDX}y{SDY}) = [[{ac}*pow(x,{ax})*pow(y,{ay})]]",
            "바르게 계산하면 A ÷ ({co(d)}x{SDX}y{SDY}) = [[{ac}*pow(x,{ax})*pow(y,{ay})]] ÷ ({co(d)}x{SDX}y{SDY})",
            "계수 {ac} ÷ {pn(d)} = {k}, 지수 {ax} − {dx} = {kx}, {ay} − {dy} = {ky}이므로 바른 결과는 [[{k}*{KX}*{KY}]]",
        ],
        sol2_fig=steps([
            {"text": "A × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]", "hint": "잘못 곱한 식"},
            {"text": "A = [[{ac}*pow(x,{ax})*pow(y,{ay})]]", "hint": "한 번 나누어 어떤 식을 구한다"},
            {"text": "A ÷ ({co(d)}x{SDX}y{SDY}) = [[{k}*{KX}*{KY}]]", "hint": "바른 계산 — 한 번 더 나눈다", "marks": [{"on": "[[{k}*{KX}*{KY}]]", "note": "A가 답이 아님"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="구한 A = [[{ac}*pow(x,{ax})*pow(y,{ay})]]에 {co(d)}x{SDX}y{SDY}{DEUL} 곱하면 [[{pc}*pow(x,{px})*pow(y,{py})]]이 되어 조건과 같고, A를 {co(d)}x{SDX}y{SDY}{DRO} 나누면 [[{k}*{KX}*{KY}]]이다. 잘못된 결과를 한 번만 나눈 [[{ac}*pow(x,{ax})*pow(y,{ay})]]은 어떤 식이지 답이 아니다.",
        sol3_fig=steps(["[[{ac}*pow(x,{ax})*pow(y,{ay})]] × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]  (조건 확인)", "바른 계산: [[{k}*{KX}*{KY}]]"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="어떤 식을 A라 하면 A × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]이므로 A = [[{ac}*pow(x,{ax})*pow(y,{ay})]]이다. 따라서 바르게 계산한 식은 [[{ac}*pow(x,{ax})*pow(y,{ay})]] ÷ ({co(d)}x{SDX}y{SDY}) = [[{k}*{KX}*{KY}]]이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "어떤 식을 A로 놓고 A × ({co(d)}x{SDX}y{SDY}) = [[{pc}*pow(x,{px})*pow(y,{py})]]을 세웠다.", "partial": "나눗셈으로 식을 세웠으면 인정하지 않는다."},
            {"element": "어떤 식 구하기", "points": 2, "criterion": "역연산으로 A = [[{ac}*pow(x,{ax})*pow(y,{ay})]]을 구했다.", "partial": "계수의 부호 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "바르게 계산한 식 [[{k}*{KX}*{KY}]]{KEUL} 답했다.", "partial": "어떤 식 A를 답으로 썼으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


MO_SEED = {
    "seed_id": MO, "category": "연산",
    "title": "단항식의 곱셈과 나눗셈 — 계수·지수 결정(곱·나눗셈)·□ 안의 식(× / ÷)·잘못 계산",
    "unit_id": "m2-1", "concept_ids": ["m2-1-04"],
    "schema_id": None, "schema_name": "단항식의 곱셈과 나눗셈",
    "source_item_ids": [],
    "note": "주어진 단항식은 평문 위첨자(표 조각), 파생 단항식은 [[k*pow(x,e)*pow(y,f)]] 마커(지수 ≥ 2, |계수| ≥ 2 제약). 식이 답인 t3·t4·t5 는 recheck.py 가 mathir 로 x, y 대입 대조.",
    "geometry": False,
    "templates": [mo_t1(), mo_t2(), mo_t3(), mo_t4(), mo_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 다항식의 계산
PO = "m2-1-polynomial"
PO_BASE = {**BASE, "prereq": ["일차식의 계산", "단항식의 계산"], "ops": ["다항식의 계산"], "traps": ["괄호 앞 음수", "동류항"], "tags": ["다항식의 계산"]}
OP_ROWS = {"key": "op", "rows": {"p": {"OPS": "+", "s": 1}, "m": {"OPS": "−", "s": -1}}}
ASK3_ROWS = {"key": "ask", "rows": {
    "x2": {"ASKE": "x²의 계수를", "ASKN": "x²의 계수는", "w2": 1, "w1": 0, "w0": 0},
    "x1": {"ASKE": "x의 계수를", "ASKN": "x의 계수는", "w2": 0, "w1": 1, "w0": 0},
    "c": {"ASKE": "상수항을", "ASKN": "상수항은", "w2": 0, "w1": 0, "w0": 1},
    "s12": {"ASKE": "x²의 계수와 x의 계수의 합을", "ASKN": "x²의 계수와 x의 계수의 합은", "w2": 1, "w1": 1, "w0": 0},
}}


def po_t1():
    return tpl(PO, 1, PO_BASE,
        title="p(이차식) ± q(이차식)을 간단히 하여 계수·상수항 읽기",
        skill="분배법칙으로 괄호를 풀고(빼는 괄호는 부호 반전) 동류항끼리 모아 정리하기",
        variant_axis={"괄호 앞 수": "p ±2·±3, q 2~4", "구하는 것": "x²의 계수 / x의 계수 / 상수항 / 둘의 합"},
        discriminates="괄호 앞의 수를 모든 항에 곱하는가, 빼는 괄호 안 모든 항의 부호를 바꾸는가",
        difficulty=2,
        params=[{"name": "p", "values": {"in": [-3, -2, 2, 3]}}, {"name": "a2", "values": {"in": NZ3}}, {"name": "a1", "values": {"in": NZ4}}, {"name": "a0", "values": {"in": NZ6}},
                {"name": "op", "values": {"in": ["p", "m"]}}, {"name": "q", "values": {"int": [2, 4]}}, {"name": "b2", "values": {"in": NZ3}}, {"name": "b1", "values": {"in": NZ4}}, {"name": "b0", "values": {"in": NZ6}},
                {"name": "ask", "values": {"in": list(ASK3_ROWS["rows"])}}],
        table=[sgn_rows(NZ4, "a1", "x"), sgn_rows(NZ4, "b1", "x"), OP_ROWS, ASK3_ROWS],
        derive={"pa2": "p*a2", "pa1": "p*a1", "pa0": "p*a0", "sq": "s*q", "qb2": "s*q*b2", "qb1": "s*q*b1", "qb0": "s*q*b0",
                "c2": "p*a2 + s*q*b2", "c1": "p*a1 + s*q*b1", "c0": "p*a0 + s*q*b0", "ans": "w2*c2 + w1*c1 + w0*c0"},
        constraints=["c2 != 0", "c1 != 0", "abs(c1) != 1", "c0 != 0", "ans != 0", "ans not in (p, q, a2, b2, abs(a1), abs(a0), abs(b1), abs(b0))", "not (a2 == b2 and a1 == b1 and a0 == b0)"],
        cost_values=["p", "q", "pa2", "pa1", "pa0", "qb2", "qb1", "qb0", "c2", "c1", "c0", "ans"],
        answer_var="ans",
        verify=["ans == w2*c2 + w1*c1 + w0*c0", "c2 == pa2 + qb2", "c1 == pa1 + qb1", "c0 == pa0 + qb0"],
        question="{p}({co(a2)}x² {A1S} {sgn(a0)}) {OPS} {q}({co(b2)}x² {B1S} {sgn(b0)}){eul(b0)} 간단히 하였을 때, {ASKE} 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="괄호 앞의 수를 괄호 안의 모든 항에 곱해 괄호를 푼다(분배법칙). 특히 빼는 괄호는 안의 모든 항의 부호가 바뀐다. 그다음 x²항끼리, x항끼리, 상수항끼리 동류항을 모아 정리하고 묻는 계수를 읽는다.",
        sol2=[
            "{p}({co(a2)}x² {A1S} {sgn(a0)}) = {co(pa2)}x² {sgn(pa1)}x {sgn(pa0)}",
            "{OPS} {q}({co(b2)}x² {B1S} {sgn(b0)}) = {sgn(qb2)}x² {sgn(qb1)}x {sgn(qb0)}",
            "동류항끼리 모으면 x²: {pa2} {sgn(qb2)} = {c2}, x: {pa1} {sgn(qb1)} = {c1}, 상수항: {pa0} {sgn(qb0)} = {c0}",
            "정리한 식은 {co(c2)}x² {sgn(c1)}x {sgn(c0)}이므로 {ASKN} {ans}",
        ],
        sol2_fig=steps([
            {"text": "{p}({co(a2)}x² {A1S} {sgn(a0)}) = {co(pa2)}x² {sgn(pa1)}x {sgn(pa0)}", "hint": "{p}{eul(p)} 세 항에 모두 곱한다"},
            {"text": "{OPS} {q}({co(b2)}x² {B1S} {sgn(b0)}) = {sgn(qb2)}x² {sgn(qb1)}x {sgn(qb0)}", "hint": "괄호 앞 {OPS}{q}{eul(q)} 세 항에 곱한다"},
            {"text": "x²: {pa2} {sgn(qb2)} = {c2},  x: {pa1} {sgn(qb1)} = {c1},  상수: {pa0} {sgn(qb0)} = {c0}", "hint": "동류항끼리"},
            {"text": "{co(c2)}x² {sgn(c1)}x {sgn(c0)} → {ASKN} {ans}", "marks": [{"on": "{ans}", "note": "묻는 항만 읽는다"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="항별로 따로 계산해 보면 x²의 계수는 {p} × {pn(a2)} {OPS} {q} × {pn(b2)} = {c2}, x의 계수는 {p} × {pn(a1)} {OPS} {q} × {pn(b1)} = {c1}, 상수항은 {p} × {pn(a0)} {OPS} {q} × {pn(b0)} = {c0}으로 같다. 따라서 {ASKN} {ans}이다.",
        sol3_fig=steps(["x²: {p} × {pn(a2)} {OPS} {q} × {pn(b2)} = {c2}", "x: {p} × {pn(a1)} {OPS} {q} × {pn(b1)} = {c1}", "상수항: {p} × {pn(a0)} {OPS} {q} × {pn(b0)} = {c0}"]),
        sol3_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        model_answer="{p}({co(a2)}x² {A1S} {sgn(a0)}) {OPS} {q}({co(b2)}x² {B1S} {sgn(b0)}) = {co(pa2)}x² {sgn(pa1)}x {sgn(pa0)} {sgn(qb2)}x² {sgn(qb1)}x {sgn(qb0)} = {co(c2)}x² {sgn(c1)}x {sgn(c0)}이므로 {ASKN} {ans}이다.",
        rubric=[
            {"element": "괄호 풀기", "points": 3, "criterion": "두 괄호를 {co(pa2)}x² {sgn(pa1)}x {sgn(pa0)}, {sgn(qb2)}x² {sgn(qb1)}x {sgn(qb0)}{ro(qb0)} 바르게 풀었다.", "partial": "빼는 괄호의 부호를 일부만 바꾸었으면 1점."},
            {"element": "동류항 정리", "points": 2, "criterion": "{co(c2)}x² {sgn(c1)}x {sgn(c0)}{ro(c0)} 정리했다.", "partial": "차수가 다른 항을 합쳤으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKN} {ans}임을 구했다.", "partial": "다른 항의 계수를 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


MN_ROWS = {"key": "mn", "rows": {f"{m}-{n}": {"m": m, "n": n, "L": m * n // gcd(m, n)} for m, n in
           [(2, 3), (3, 2), (3, 4), (4, 3), (2, 5), (5, 2), (3, 5), (5, 3), (4, 5), (5, 4), (4, 6), (6, 4), (2, 6), (3, 6), (6, 3), (2, 4), (4, 2)]}}
ASKXY_ROWS = {"key": "ask", "rows": {
    "x": {"ASKE": "x의 계수를", "ASKN": "x의 계수는", "wx": 1, "wy": 0},
    "y": {"ASKE": "y의 계수를", "ASKN": "y의 계수는", "wx": 0, "wy": 1},
    "sum": {"ASKE": "x의 계수와 y의 계수의 합을", "ASKN": "x의 계수와 y의 계수의 합은", "wx": 1, "wy": 1},
}}


def po_t2():
    return tpl(PO, 2, PO_BASE,
        title="분모가 다른 분수 꼴 다항식의 덧셈·뺄셈 — 통분 후 계수 읽기",
        skill="분모의 최소공배수로 통분하고 빼는 분자는 괄호로 묶어 부호를 바꾼 뒤 x, y의 계수를 분수로 읽기",
        variant_axis={"분모": "2~6의 쌍", "구하는 것": "x의 계수 / y의 계수 / 합"},
        discriminates="통분할 때 분자 전체에 같은 수를 곱하는가, 빼는 분수의 분자 부호를 모두 바꾸는가, 계수를 약분해 읽는가",
        difficulty=3,
        params=[{"name": "mn", "values": {"in": list(MN_ROWS["rows"])}}, {"name": "a1", "values": {"in": NZ3}}, {"name": "a0", "values": {"in": NZ4}},
                {"name": "op", "values": {"in": ["p", "m"]}}, {"name": "b1", "values": {"in": NZ3}}, {"name": "b0", "values": {"in": NZ4}}, {"name": "ask", "values": {"in": ["x", "y", "sum"]}}],
        table=[MN_ROWS, lead_rows(NZ3, "a1", "x", True), sgn_rows(NZ4, "a0", "y", True), lead_rows(NZ3, "b1", "x", True), sgn_rows(NZ4, "b0", "y", True), OP_ROWS, ASKXY_ROWS],
        derive={"fm": "L / m", "fn": "L / n", "na1": "L / m * a1", "na0": "L / m * a0", "nb1u": "L / n * b1", "nb0u": "L / n * b0",
                "c1": "L / m * a1 + s * L / n * b1", "c0": "L / m * a0 + s * L / n * b0", "cx": "c1 / L", "cy": "c0 / L", "ax": "a1 / m", "bx": "b1 / n", "ay": "a0 / m", "by": "b0 / n",
                "ans": "wx * c1 / L + wy * c0 / L"},
        constraints=["abs(na1) >= 2", "abs(na0) >= 2", "abs(nb1u) >= 2", "abs(nb0u) >= 2", "abs(c1) >= 2", "abs(c0) >= 2", "ans != 0", "not (a1 == b1 and a0 == b0)",
                     "ans not in (m, n, abs(a1), abs(a0), abs(b1), abs(b0))"],
        cost_values=["m", "n", "L", "na1", "na0", "nb1u", "nb0u", "c1", "c0", "cx", "cy", "ans"],
        answer_var="ans",
        verify=["ans == wx*cx + wy*cy", "cx == ax + s*bx", "cy == ay + s*by", "L % m == 0", "L % n == 0"],
        question="[[frac({A1L} {A0S}, {m})]] {OPS} [[frac({B1L} {B0S}, {n})]]를 간단히 하였을 때, {ASKE} 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="분모가 다른 분수 꼴의 다항식은 분모의 최소공배수로 통분한 뒤 분자끼리 계산한다. 통분할 때는 분자의 모든 항에 같은 수를 곱하고, 빼는 분수의 분자는 괄호로 묶어 모든 항의 부호를 바꾼다. 마지막에 x의 계수와 y의 계수를 각각 분수로 읽고 약분한다.",
        sol2=[
            "분모 {m}, {n}의 최소공배수 {L}로 통분: [[frac({na1}*x {sgn(na0)}*y {OPS} ({nb1u}*x {sgn(nb0u)}*y), {L})]]",
            "분자를 정리: {na1}x {sgn(na0)}y {OPS} ({nb1u}x {sgn(nb0u)}y) = {co(c1)}x {sgn(c0)}y",
            "= [[frac({c1}*x {sgn(c0)}*y, {L})]]이므로 x의 계수는 {cx}, y의 계수는 {cy} → {ASKN} {ans}",
        ],
        sol2_fig=steps([
            {"text": "[[frac({na1}*x {sgn(na0)}*y {OPS} ({nb1u}*x {sgn(nb0u)}*y), {L})]]", "hint": "최소공배수 {L}로 통분 — 분자 전체에 {fm}, {fn}을 곱한다"},
            {"text": "분자 = {co(c1)}x {sgn(c0)}y", "hint": "빼는 괄호는 부호 반전", "marks": [{"on": "{co(c1)}x {sgn(c0)}y", "note": "동류항 정리"}]},
            {"text": "[[frac({c1}*x {sgn(c0)}*y, {L})]] → x: {cx}, y: {cy}", "hint": "계수는 분수로 읽고 약분"},
            {"text": "{ASKN} {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3)]],
        sol3="x의 계수만 따로 더하면 {ax} {OPS} ({bx}) = {cx}, y의 계수는 {ay} {OPS} ({by}) = {cy}{ro(cy)} 통분 결과와 같다. 따라서 {ASKN} {ans}이다.",
        sol3_fig=steps(["x: {ax} {OPS} ({bx}) = {cx}", "y: {ay} {OPS} ({by}) = {cy}", "{ASKN} {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        model_answer="[[frac({A1L} {A0S}, {m})]] {OPS} [[frac({B1L} {B0S}, {n})]] = [[frac({na1}*x {sgn(na0)}*y {OPS} ({nb1u}*x {sgn(nb0u)}*y), {L})]] = [[frac({c1}*x {sgn(c0)}*y, {L})]]이므로 x의 계수는 {cx}, y의 계수는 {cy}이다. 따라서 {ASKN} {ans}이다.",
        rubric=[
            {"element": "통분", "points": 3, "criterion": "최소공배수 {L}로 통분해 분자를 {na1}x {sgn(na0)}y {OPS} ({nb1u}x {sgn(nb0u)}y){ro(nb0u)} 썼다.", "partial": "분자의 한 항에만 곱했으면 인정하지 않는다."},
            {"element": "분자 정리", "points": 2, "criterion": "분자를 {co(c1)}x {sgn(c0)}y{ro(c0)} 정리했다.", "partial": "빼는 괄호의 부호를 일부만 바꾸었으면 1점."},
            {"element": "계수 읽기", "points": 2, "criterion": "x의 계수 {cx}, y의 계수 {cy}{eul(cy)} 읽어 {ASKN} {ans}임을 구했다.", "partial": "약분하지 않은 분수를 답했으면 1점."},
        ],
        rubric_total=7,
    )


ASK2X_ROWS = {"key": "ask", "rows": {
    "x2": {"ASKE": "x²의 계수를", "ASKN": "x²의 계수는", "w2": 1, "w1": 0},
    "x1": {"ASKE": "x의 계수를", "ASKN": "x의 계수는", "w2": 0, "w1": 1},
    "s12": {"ASKE": "x²의 계수와 x의 계수의 합을", "ASKN": "x²의 계수와 x의 계수의 합은", "w2": 1, "w1": 1},
}}


def po_t3():
    return tpl(PO, 3, PO_BASE,
        title="단항식 × 다항식의 전개 — ax(bx + c) ± dx(ex + f)의 계수",
        skill="분배법칙으로 단항식을 괄호 안의 각 항에 곱해 전개하고(x × x = x²) 동류항을 정리하기",
        variant_axis={"단항식 계수": "a ±1~±4, d 2~5", "구하는 것": "x²의 계수 / x의 계수 / 합"},
        discriminates="x × x를 x²으로 쓰는가(2x로 쓰지 않는가), 빼는 쪽 단항식의 부호까지 곱하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ4}}, {"name": "b", "values": {"in": NZ3}}, {"name": "c", "values": {"in": NZ6}},
                {"name": "op", "values": {"in": ["p", "m"]}}, {"name": "d", "values": {"int": [2, 5]}}, {"name": "e", "values": {"in": NZ3}}, {"name": "f", "values": {"in": NZ6}},
                {"name": "ask", "values": {"in": ["x2", "x1", "s12"]}}],
        table=[OP_ROWS, ASK2X_ROWS],
        derive={"ab": "a*b", "ac": "a*c", "sd": "s*d", "de": "s*d*e", "df": "s*d*f", "c2": "a*b + s*d*e", "c1": "a*c + s*d*f", "ans": "w2*c2 + w1*c1"},
        constraints=["abs(ac) != 1", "c2 != 0", "c1 != 0", "abs(c1) != 1", "ans != 0", "ans not in (a, b, d, e, abs(c), abs(f))"],
        cost_values=["a", "b", "c", "d", "e", "f", "ab", "ac", "de", "df", "c2", "c1", "ans"],
        answer_var="ans",
        verify=["ans == w2*c2 + w1*c1", "c2 == ab + de", "c1 == ac + df"],
        question="{co(a)}x({co(b)}x {sgn(c)}) {OPS} {d}x({co(e)}x {sgn(f)}){eul(f)} 전개하여 간단히 하였을 때, {ASKE} 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="단항식과 다항식의 곱은 분배법칙으로 단항식을 괄호 안의 각 항에 곱한다. 이때 x × x = x²이고, 빼는 쪽은 단항식의 부호까지 바꾸어 곱한다. 전개한 뒤 x²항끼리, x항끼리 동류항을 정리한다.",
        sol2=[
            "{co(a)}x({co(b)}x {sgn(c)}) = {co(ab)}x² {sgn(ac)}x",
            "{OPS} {d}x({co(e)}x {sgn(f)}) = {sgn(de)}x² {sgn(df)}x",
            "동류항끼리 모으면 x²: {ab} {sgn(de)} = {c2}, x: {ac} {sgn(df)} = {c1}이므로 {co(c2)}x² {sgn(c1)}x → {ASKN} {ans}",
        ],
        sol2_fig=steps([
            {"text": "{co(a)}x({co(b)}x {sgn(c)}) = {co(ab)}x² {sgn(ac)}x", "hint": "x × x = x²"},
            {"text": "{OPS} {d}x({co(e)}x {sgn(f)}) = {sgn(de)}x² {sgn(df)}x", "hint": "{OPS}{d}x를 두 항에 곱한다"},
            {"text": "{co(c2)}x² {sgn(c1)}x → {ASKN} {ans}", "marks": [{"on": "{ans}", "note": "동류항 정리"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="x²항은 {a} × {pn(b)} {OPS} {d} × {pn(e)} = {c2}, x항은 {a} × {pn(c)} {OPS} {d} × {pn(f)} = {c1}로 전개 결과와 같다. 따라서 {ASKN} {ans}이다.",
        sol3_fig=steps(["x²: {a} × {pn(b)} {OPS} {d} × {pn(e)} = {c2}", "x: {a} × {pn(c)} {OPS} {d} × {pn(f)} = {c1}", "{ASKN} {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        model_answer="{co(a)}x({co(b)}x {sgn(c)}) {OPS} {d}x({co(e)}x {sgn(f)}) = {co(ab)}x² {sgn(ac)}x {sgn(de)}x² {sgn(df)}x = {co(c2)}x² {sgn(c1)}x이므로 {ASKN} {ans}이다.",
        rubric=[
            {"element": "전개", "points": 3, "criterion": "두 곱을 {co(ab)}x² {sgn(ac)}x, {sgn(de)}x² {sgn(df)}x{ro(df)} 바르게 전개했다.", "partial": "x × x를 x²으로 쓰지 못했거나 부호 실수 하나면 1점."},
            {"element": "동류항 정리", "points": 2, "criterion": "{co(c2)}x² {sgn(c1)}x{ro(c1)} 정리했다.", "partial": "차수가 다른 항을 합쳤으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKN} {ans}임을 구했다."},
        ],
        rubric_total=7,
    )


R2_ROWS = {"key": "r2", "rows": {str(v): {"R2M": _lead(v, "pow(x,2)", True)} for v in NZ3}}
WR2_ROWS = {"key": "w", "rows": {
    "addsub": {"PRE": "에", "OPC": "더해야", "OPW": "뺐더니", "S1": "−", "S2": "+", "S3": "+", "i": 1, "WR": "뺀", "CR": "더한"},
    "subadd": {"PRE": "에서", "OPC": "빼야", "OPW": "더했더니", "S1": "+", "S2": "−", "S3": "−", "i": -1, "WR": "더한", "CR": "뺀"},
}}


def po_t4():
    return tpl(PO, 4, PO_BASE,
        title="어떤 다항식에 이차식을 잘못 더하거나 뺀 결과로 바르게 계산한 식 구하기",
        skill="어떤 식을 A로 놓아 잘못된 계산을 식으로 세우고, 역연산으로 A를 구한 뒤 바르게 계산하기",
        variant_axis={"잘못한 연산": "더함→뺌 / 뺌→더함", "계수": "±1~±6"},
        discriminates="어떤 식을 미지의 식으로 두고 역연산하는가, 괄호를 붙여 빼면서 세 항의 부호를 모두 바꾸는가",
        difficulty=3, process="문제해결",
        params=[{"name": "w", "values": {"in": ["addsub", "subadd"]}}, {"name": "r2", "values": {"in": NZ3}}, {"name": "r1", "values": {"in": NZ4}}, {"name": "r0", "values": {"in": NZ6}},
                {"name": "a2", "values": {"in": NZ3}}, {"name": "a1", "values": {"in": NZ4}}, {"name": "a0", "values": {"in": NZ6}}],
        table=[WR2_ROWS, R2_ROWS, sgn_rows(NZ4, "r1", "x", True), sgn_rows(NZ6, "r0", "", True), sgn_rows(NZ4, "a1", "x")],
        derive={"b2": "r2 - 2*i*a2", "b1": "r1 - 2*i*a1", "b0": "r0 - 2*i*a0", "p2": "r2 - i*a2", "p1": "r1 - i*a1", "p0": "r0 - i*a0"},
        constraints=["b2 != 0", "abs(b1) >= 2", "b0 != 0", "p2 != 0", "abs(p1) >= 2", "p0 != 0", "abs(b2) <= 9", "abs(b1) <= 12", "abs(b0) <= 18"],
        cost_values=["a2", "a1", "a0", "b2", "b1", "b0", "p2", "p1", "p0", "r2", "r1", "r0"],
        verify=["p2 == b2 + i*a2", "p1 == b1 + i*a1", "p0 == b0 + i*a0", "r2 == p2 + i*a2", "r1 == p1 + i*a1", "r0 == p0 + i*a0"],
        question="어떤 다항식{PRE} {co(a2)}x² {A1S} {sgn(a0)}{eul(a0)} {OPC} 할 것을 잘못하여 {co(a2)}x² {A1S} {sgn(a0)}{eul(a0)} {OPW} {co(b2)}x² {sgn(b1)}x {sgn(b0)}{ika(b0)} 되었다. 바르게 계산한 식을 구하시오.",
        answer="[[{R2M} {R1S} {R0S}]]", answer_alt=[],
        sol1="어떤 다항식을 A라 하고 잘못 계산한 과정을 그대로 식으로 쓰면 A {S1} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(b2)}x² {sgn(b1)}x {sgn(b0)}이다. 이 식에서 A를 구한 다음(역연산 — 괄호를 붙여 {S2} 한다), 원래 하려던 바른 계산 A {S3} ({co(a2)}x² {A1S} {sgn(a0)}){eul(a0)} 한다. 잘못 계산한 결과나 A 자체를 답으로 쓰지 않도록 한다.",
        sol2=[
            "어떤 다항식을 A라 하면 잘못 계산한 식은 A {S1} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(b2)}x² {sgn(b1)}x {sgn(b0)}",
            "따라서 A = ({co(b2)}x² {sgn(b1)}x {sgn(b0)}) {S2} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(p2)}x² {sgn(p1)}x {sgn(p0)}",
            "바르게 계산하면 ({co(p2)}x² {sgn(p1)}x {sgn(p0)}) {S3} ({co(a2)}x² {A1S} {sgn(a0)}) = [[{R2M} {R1S} {R0S}]]",
        ],
        sol2_fig=steps([
            {"text": "A {S1} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(b2)}x² {sgn(b1)}x {sgn(b0)}", "hint": "잘못 {WR} 계산"},
            {"text": "A = ({co(b2)}x² {sgn(b1)}x {sgn(b0)}) {S2} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(p2)}x² {sgn(p1)}x {sgn(p0)}", "hint": "역연산 — 괄호 붙여서", "marks": [{"on": "({co(a2)}x² {A1S} {sgn(a0)})", "note": "부호 주의"}]},
            {"text": "({co(p2)}x² {sgn(p1)}x {sgn(p0)}) {S3} ({co(a2)}x² {A1S} {sgn(a0)}) = [[{R2M} {R1S} {R0S}]]", "hint": "바르게 {CR} 계산"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")]],
        sol3="구한 어떤 식 {co(p2)}x² {sgn(p1)}x {sgn(p0)}{ro(p0)} 잘못 계산한 대로 하면 ({co(p2)}x² {sgn(p1)}x {sgn(p0)}) {S1} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(b2)}x² {sgn(b1)}x {sgn(b0)}{ika(b0)} 되어 조건과 같다. 따라서 바르게 계산한 식은 [[{R2M} {R1S} {R0S}]]이다.",
        sol3_fig=steps(["({co(p2)}x² {sgn(p1)}x {sgn(p0)}) {S1} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(b2)}x² {sgn(b1)}x {sgn(b0)}  (조건 확인)", "바른 계산: [[{R2M} {R1S} {R0S}]]"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="어떤 다항식을 A라 하면 A {S1} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(b2)}x² {sgn(b1)}x {sgn(b0)}이므로 A = {co(p2)}x² {sgn(p1)}x {sgn(p0)}이다. 따라서 바르게 계산한 식은 ({co(p2)}x² {sgn(p1)}x {sgn(p0)}) {S3} ({co(a2)}x² {A1S} {sgn(a0)}) = [[{R2M} {R1S} {R0S}]]이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "어떤 식을 A로 놓고 잘못 계산한 식 A {S1} ({co(a2)}x² {A1S} {sgn(a0)}) = {co(b2)}x² {sgn(b1)}x {sgn(b0)}{eul(b0)} 세웠다.", "partial": "바른 연산으로 식을 세웠으면 인정하지 않는다."},
            {"element": "어떤 식 구하기", "points": 2, "criterion": "역연산으로 A = {co(p2)}x² {sgn(p1)}x {sgn(p0)}{eul(p0)} 구했다.", "partial": "괄호 없이 계산해 부호가 일부 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "바르게 계산한 식 [[{R2M} {R1S} {R0S}]]{eul(r0)} 답했다.", "partial": "어떤 식 A를 답으로 썼으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


SHAPE_ROWS = {"key": "sh", "rows": {
    "xy": {"WV": "xy", "WRO": "로", "S1": "pow(x,2)*y", "S2": "x*pow(y,2)", "T1": "x²y", "T2": "xy²"},
    "x2": {"WV": "x²", "WRO": "으로", "S1": "pow(x,3)", "S2": "pow(x,2)*y", "T1": "x³", "T2": "x²y"},
    "y2": {"WV": "y²", "WRO": "으로", "S1": "x*pow(y,2)", "S2": "pow(y,3)", "T1": "xy²", "T2": "y³"},
    "x2y": {"WV": "x²y", "WRO": "로", "S1": "pow(x,3)*y", "S2": "pow(x,2)*pow(y,2)", "T1": "x³y", "T2": "x²y²"},
}}
FIG_ROWS = {"key": "fig", "rows": {
    "rect": {"FIG": "직사각형", "SIDE": "가로의 길이", "ASKW": "세로의 길이를", "ASKN": "세로의 길이는", "kk": 1, "FORM": "(넓이) ÷ (가로)", "MUL": "", "CHK": "가로 × 세로 =", "DIV": ""},
    "tri": {"FIG": "삼각형", "SIDE": "밑변의 길이", "ASKW": "높이를", "ASKN": "높이는", "kk": 2, "FORM": "2 × (넓이) ÷ (밑변)", "MUL": "2 × ", "CHK": "밑변 × 높이 ÷ 2 =", "DIV": " ÷ 2"},
    "para": {"FIG": "평행사변형", "SIDE": "밑변의 길이", "ASKW": "높이를", "ASKN": "높이는", "kk": 1, "FORM": "(넓이) ÷ (밑변)", "MUL": "", "CHK": "밑변 × 높이 =", "DIV": ""},
}}


def po_t5():
    return tpl(PO, 5, PO_BASE,
        title="넓이가 다항식으로 주어진 도형의 다른 변(높이) — 다항식 ÷ 단항식",
        skill="넓이 공식을 거꾸로 써서 (넓이) ÷ (한 변)으로 놓고, 다항식의 각 항을 단항식으로 나누기",
        variant_axis={"도형": "직사각형 / 삼각형 / 평행사변형", "한 변": "2~6 · xy, x², y², x²y", "다른 변": "px + qy (p 1~3, q 1~4)"},
        discriminates="삼각형은 넓이에 2를 곱한 뒤 나누는가, 다항식의 두 항을 각각 단항식으로 나누는가",
        difficulty=3, process="문제해결", context="기하맥락",
        params=[{"name": "fig", "values": {"in": ["rect", "tri", "para"]}}, {"name": "c", "values": {"int": [2, 6]}}, {"name": "sh", "values": {"in": ["xy", "x2", "y2", "x2y"]}},
                {"name": "p", "values": {"int": [1, 3]}}, {"name": "q", "values": {"int": [1, 4]}}],
        table=[FIG_ROWS, SHAPE_ROWS, lead_rows([1, 2, 3], "p", "x", True), sgn_rows([1, 2, 3, 4], "q", "y", True)],
        derive={"cp": "c*p/kk", "cq": "c*q/kk", "cp2": "c*p", "cq2": "c*q"},
        constraints=["cp == floor(cp)", "cq == floor(cq)", "abs(cp) >= 2", "abs(cq) >= 2"],
        cost_values=["c", "p", "q", "cp", "cq"],
        verify=["cp*kk == c*p", "cq*kk == c*q", "cp2 == c*p", "cq2 == c*q"],
        question="넓이가 [[{cp}*{S1} {sgn(cq)}*{S2}]]인 {FIG}의 {SIDE}가 {c}{WV}일 때, {ASKW} 구하시오.",
        answer="[[{PL} {QS}]]", answer_alt=[],
        sol1="{FIG}의 넓이 공식을 거꾸로 쓰면 {ASKN} {FORM}이다. 다항식을 단항식으로 나눌 때는 다항식의 각 항을 단항식으로 각각 나눈다(계수는 계수끼리, 문자는 지수를 뺀다).",
        sol2=[
            "{ASKN} {FORM} = {MUL}([[{cp}*{S1} {sgn(cq)}*{S2}]]) ÷ {c}{WV}",
            "= ([[{cp2}*{S1} {sgn(cq2)}*{S2}]]) ÷ {c}{WV} = [[{cp2}*{S1}]] ÷ {c}{WV} {sgn(cq2)}{T2} ÷ {c}{WV}",
            "각 항을 나누면 [[{PL} {QS}]]",
        ],
        sol2_fig=steps([
            {"text": "{ASKN} {FORM}", "hint": "넓이 공식을 거꾸로"},
            {"text": "= ([[{cp2}*{S1} {sgn(cq2)}*{S2}]]) ÷ {c}{WV}", "hint": "각 항을 {c}{WV}{WRO} 나눈다"},
            {"text": "= [[{PL} {QS}]]", "marks": [{"on": "[[{PL} {QS}]]", "note": "계수는 나누고 지수는 뺀다"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="확인: {CHK} {c}{WV} × ([[{PL} {QS}]]){DIV} = [[{cp}*{S1} {sgn(cq)}*{S2}]]. 주어진 넓이와 같으므로 맞다. 따라서 {ASKN} [[{PL} {QS}]]이다.",
        sol3_fig=steps(["{c}{WV} × ([[{PL} {QS}]]){DIV} = [[{cp}*{S1} {sgn(cq)}*{S2}]]  (넓이 확인)", "{ASKN} [[{PL} {QS}]]"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{ASKN} {FORM}이므로 ([[{cp2}*{S1} {sgn(cq2)}*{S2}]]) ÷ {c}{WV} = [[{PL} {QS}]]이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "{ASKN} {FORM}임을 써서 ([[{cp2}*{S1} {sgn(cq2)}*{S2}]]) ÷ {c}{WV}{WRO} 놓았다.", "partial": "삼각형에서 2를 곱하지 않았으면 인정하지 않는다."},
            {"element": "다항식의 나눗셈", "points": 2, "criterion": "각 항을 {c}{WV}{WRO} 나누어 [[{PL} {QS}]]를 구했다.", "partial": "한 항만 나누었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ASKN} [[{PL} {QS}]]임을 답했다."},
        ],
        rubric_total=7,
    )


def po_t6():
    return tpl(PO, 6, PO_BASE,
        title="(다항식) ÷ (단항식)을 간단히 한 뒤 x, y를 대입한 식의 값",
        skill="먼저 다항식을 단항식으로 나누어 간단히 한 다음 x, y의 값을 괄호를 써서 대입하기",
        variant_axis={"대입값": "x ±1~±3, y ±1~±3", "단항식": "2~4 · xy, x², y², x²y"},
        discriminates="식을 먼저 간단히 하고 대입하는가, 음수를 대입할 때 괄호를 써서 부호를 처리하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"in": NZ3}}, {"name": "b", "values": {"in": NZ3}}, {"name": "c", "values": {"int": [2, 4]}}, {"name": "sh", "values": {"in": ["xy", "x2", "y2", "x2y"]}},
                {"name": "p", "values": {"in": NZ3}}, {"name": "q", "values": {"in": NZ4}}],
        table=[SHAPE_ROWS, sgn_rows(NZ4, "q", "y")],
        derive={"cp": "c*p", "cq": "c*q", "t1": "p*a", "t2": "q*b", "ans": "p*a + q*b"},
        constraints=["ans != 0", "ans not in (a, b, c, cp, abs(cq), 2, 3)", "abs(ans) <= 30", "a != b"],
        cost_values=["a", "b", "c", "cp", "cq", "t1", "t2", "ans"],
        answer_var="ans",
        verify=["ans == t1 + t2", "cp == c*p", "cq == c*q"],
        question="x = {a}, y = {b}일 때, ([[{cp}*{S1} {sgn(cq)}*{S2}]]) ÷ {c}{WV}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="식의 값을 구할 때는 먼저 식을 간단히 한 다음 대입하면 계산이 쉽다. 다항식을 단항식으로 나눌 때는 각 항을 단항식으로 각각 나누고, 음수를 대입할 때는 반드시 괄호를 쓴다.",
        sol2=[
            "먼저 나눗셈: ([[{cp}*{S1} {sgn(cq)}*{S2}]]) ÷ {c}{WV} = [[{cp}*{S1}]] ÷ {c}{WV} {sgn(cq)}{T2} ÷ {c}{WV} = {co(p)}x {QS}",
            "x = {a}, y = {b}{eul(b)} 대입: {p} × {pn(a)} + {pn(q)} × {pn(b)} = {t1} {sgn(t2)}",
            "따라서 식의 값은 {ans}",
        ],
        sol2_fig=steps([
            {"text": "([[{cp}*{S1} {sgn(cq)}*{S2}]]) ÷ {c}{WV} = {co(p)}x {QS}", "hint": "각 항을 {c}{WV}{WRO} 나눈다"},
            {"text": "{p} × {pn(a)} + {pn(q)} × {pn(b)} = {t1} {sgn(t2)}", "hint": "음수는 괄호로 대입"},
            {"text": "= {ans}", "marks": [{"on": "{ans}", "note": "부호 확인"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="나눗셈 확인: {c}{WV} × ({co(p)}x {QS}) = [[{cp}*{S1} {sgn(cq)}*{S2}]]. 간단히 한 식 {co(p)}x {QS}에 x = {a}, y = {b}{eul(b)} 대입한 값은 {t1} {sgn(t2)} = {ans}이고, 나누기 전 식에 바로 대입해도 같은 값이 나온다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{c}{WV} × ({co(p)}x {QS}) = [[{cp}*{S1} {sgn(cq)}*{S2}]]  (나눗셈 확인)", "{t1} {sgn(t2)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="([[{cp}*{S1} {sgn(cq)}*{S2}]]) ÷ {c}{WV} = {co(p)}x {QS}이므로 x = {a}, y = {b}{eul(b)} 대입하면 {p} × {pn(a)} + {pn(q)} × {pn(b)} = {ans}이다.",
        rubric=[
            {"element": "다항식의 나눗셈", "points": 3, "criterion": "각 항을 {c}{WV}{WRO} 나누어 {co(p)}x {QS}로 간단히 했다.", "partial": "한 항만 나누었으면 인정하지 않는다."},
            {"element": "대입·계산", "points": 2, "criterion": "x = {a}, y = {b}{eul(b)} 괄호를 써서 대입해 {t1} {sgn(t2)} = {ans}{eul(ans)} 구했다.", "partial": "괄호 없이 대입해 부호가 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


PO_SEED = {
    "seed_id": PO, "category": "연산",
    "title": "다항식의 계산 — 괄호 전개 계수·분수 계수 통분·단항식×다항식·잘못 계산·도형의 변·식의 값",
    "unit_id": "m2-1", "concept_ids": ["m2-1-05", "m2-1-06"],
    "schema_id": None, "schema_name": "다항식의 덧셈·뺄셈과 곱셈·나눗셈",
    "source_item_ids": [],
    "note": "주어진 다항식은 평문(계수 ±1 은 표 조각), 파생 다항식은 제약(|일차 계수| ≥ 2, 0 제외)으로 '1x'·'0x' 를 막는다. 식이 답인 t4·t5 는 [[…pow(x,2)…]] 마커, recheck.py 가 sympy 로 대조.",
    "geometry": False,
    "templates": [po_t1(), po_t2(), po_t3(), po_t4(), po_t5(), po_t6()],
}


if __name__ == "__main__":
    for seed in (RD_SEED, MO_SEED, PO_SEED):
        with_pitfalls(seed)
        dump(seed)
