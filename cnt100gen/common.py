from fractions import Fraction as F
from itertools import permutations as PERM, combinations as COMB, product as PROD


def josa(w, a, b):
    ch = w[-1]
    if '가' <= ch <= '힣':
        has = (ord(ch) - 0xAC00) % 28 != 0
    else:
        has = ch in '013678'  # 일 삼 육 칠 팔 공(영)
    return w + (a if has else b)


def c2(n):
    return n * (n - 1) // 2


def c3(n):
    return n * (n - 1) * (n - 2) // 6


def cnt(it, cond=lambda s: True):
    return sum(1 for s in it if cond(s))


def fr(x):
    """해설용 표기: 정수 → 문자열, Fraction → {a/b}"""
    if isinstance(x, F):
        if x.denominator == 1:
            return str(x.numerator)
        return "{%d/%d}" % (x.numerator, x.denominator)
    return str(x)


def feq(num, den):
    """{num/den}, 약분되면 = 기약분수까지"""
    v = F(num, den)
    s = "{%d/%d}" % (num, den)
    if v.denominator != den:
        s += " = " + fr(v)
    return s


# ───────── 해설 식 — 공식은 다 펼치고, 무엇을 센 식인지 이름표를 붙인다(2026-11-28) ─────────
# 한 줄 = 「이름표: 펼친 식 = 값」. 식(eq)은 이런 줄의 목록 — 해설지는 줄마다, 해설 액자 판서도 줄마다.
#   자격이 다른 r명(차례로)   n × (n − 1) × …        (r개)
#   n명을 한 줄로             n × (n − 1) × … × 1
#   자격이 같은 2명           n × (n − 1) ÷ 2
#   자격이 같은 3명           n × (n − 1) × (n − 2) ÷ (3 × 2 × 1)
def chain(n, k):
    """n부터 k개를 차례로 곱한 식 — chain(5, 2) = '5 × 4'"""
    return " × ".join(str(n - i) for i in range(k)) if k > 0 else "1"


def fall(n, k):
    v = 1
    for i in range(k):
        v *= n - i
    return v


def row(n):
    """n명(개)을 한 줄로 — '3 × 2 × 1'"""
    return chain(n, n) if n > 1 else "1"


def fac(n):
    return fall(n, n)


def c2s(n):
    return f"{n} × {n - 1} ÷ 2"


def c3s(n):
    return f"{n} × {n - 1} × {n - 2} ÷ (3 × 2 × 1)"


def L(label, expr, val=None):
    """「label: expr = val」 — expr 이 곧 val 이면 「label: val」"""
    e = str(expr)
    v = e if val is None else str(val)
    body = v if e == v else f"{e} = {v}"
    return f"{label}: {body}" if label else body


def plus(xs):
    return " + ".join(str(x) for x in xs)


def times(xs):
    return " × ".join(str(x) for x in xs)


def pfeq(num, den, lead="확률"):
    """확률 줄 — 「확률: {num/den} = 기약분수」"""
    return f"{lead}: " + feq(num, den)


def pnot(num, den, lead="확률"):
    """1 − (반대 확률) 줄 — 「확률: 1 − {num/den} = {den−num/den} = 기약분수」"""
    return f"{lead}: 1 − {{{num}/{den}}} = " + feq(den - num, den)
