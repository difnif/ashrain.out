# 중등 ④ (중3) — 제곱근과 실수 · 곱셈 공식 · 이차방정식 · 삼각비 · 원의 성질
import math
from math import gcd
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, Plane, ang_pt, angle_mark, dir_deg
from kit import *

def bat(x):
    from core import _has_batchim
    return _has_batchim(str(x))

def F_(n, d):
    return "{%d/%d}" % (n, d)

def FR(v):
    v = Fr(v)
    if v.denominator == 1:
        return N(v)
    return (MI if v < 0 else "") + F_(abs(v.numerator), v.denominator)

def sq(n):
    """√n 간단히: (밖, 안)"""
    o, i = 1, n
    p = 2
    while p * p <= i:
        while i % (p * p) == 0:
            i //= p * p
            o *= p
        p += 1
    return o, i

def RT(o, i):
    """o√i 글자 — i = 1 이면 o"""
    if i == 1:
        return N(o)
    if o == 1:
        return f"√{{{i}}}"
    if o == -1:
        return f"{MI}√{{{i}}}"
    return f"{N(o)}√{{{i}}}"

def RTn(n):
    return RT(*sq(n))


# ══════════ 제곱근과 실수 ══════════
def root():
    S = Set("root", "제곱근과 실수 — 근호의 계산과 분모의 유리화", "제곱근",
            {1: "근호 안을 간단히", 2: "제곱근의 곱셈 · 나눗셈", 3: "분모의 유리화", 4: "제곱근의 덧셈 · 뺄셈", 5: "분배법칙과 정수 부분"},
            pp=10,
            tips={1: "근호 안의 제곱인 인수를 밖으로 — √{72} = √{36 × 2} = 6√{2}",
                  2: "√{a} × √{b} = √{ab} · √{a} ÷ √{b} = √{{a/b}}",
                  3: "분모의 √{a}를 분자 · 분모에 똑같이 곱해요 — {6/√{3}} = {6√{3}/3} = 2√{3}",
                  4: "근호 안이 같은 것끼리 — 먼저 a√{b} 꼴로 바꾸면 같은 꼴이 보여요",
                  5: "분배법칙은 다항식과 같아요 · √{n}의 정수 부분은 n을 사이에 끼는 두 제곱수로"},
            note="제곱근의 계산은 ‘a√{b} 꼴로 정리’가 출발점이에요. 근호 안을 소인수분해해서 짝을 이루는 소인수를 밖으로 꺼내는 과정을 손으로 쓰게 해 주세요.")
    R = rng(1501)

    def g1():
        o, i = R.randint(2, 9), R.choice([2, 3, 5, 6, 7, 10, 11, 13])
        n = o * o * i
        if n > 500:
            return
        k = S.count(1) % 2
        if k == 0:
            q = f"√{{{n}}}을 a√{{b}} 꼴로 나타내세요. (b는 가장 작은 자연수)" if bat(n) else f"√{{{n}}}를 a√{{b}} 꼴로 나타내세요. (b는 가장 작은 자연수)"
            lines = [L(f"√{{{n}}} = √{{{o * o} × {i}}}", memo="제곱인 인수 찾기"), L(f"√{{{o * o} × {i}}} = {RT(o, i)}", memo=f"{o * o} = {o}^{{2}}")]
            ans = RT(o, i)
        else:
            q = f"{RT(o, i)}를 √{{a}} 꼴로 나타내세요." if not bat(i) else f"{RT(o, i)}을 √{{a}} 꼴로 나타내세요."
            lines = [L(f"{RT(o, i)} = √{{{o}^{{2}} × {i}}}", memo="밖의 수는 제곱해서 안으로"), L(f"√{{{o}^{{2}} × {i}}} = √{{{n}}}")]
            ans = f"√{{{n}}}"
        S.add(1, q, ans, "근호 안의 제곱인 인수를 밖으로(밖의 수는 제곱해서 안으로)", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            a, b = R.choice([2, 3, 5, 6, 7, 10, 14, 15]), R.choice([2, 3, 5, 6, 10, 12, 15, 21])
            if a == b:
                return
            p = a * b
            o, i = sq(p)
            if o == 1:
                return
            c, d = R.randint(1, 4), R.randint(1, 4)
            A = f"{c if c > 1 else ''}√{{{a}}}"
            B = f"{d if d > 1 else ''}√{{{b}}}"
            res = RT(c * d * o, i)
            q = f"{A} × {J(B, '을', '를')} 간단히 하세요."
            lines = [L(f"{A} × {B} = {c * d if c * d > 1 else ''}√{{{p}}}", memo="수끼리 · 근호끼리 곱해요"), L(f"{c * d if c * d > 1 else ''}√{{{p}}} = {res}", memo="근호 안을 간단히")]
        else:
            b = R.choice([2, 3, 5, 6, 7])
            m = R.choice([2, 3, 4, 5, 6, 8, 10, 12])
            a = b * m
            o, i = sq(m)
            res = RT(o, i)
            q = f"√{{{a}}} ÷ √{{{b}}}를 간단히 하세요." if not bat(b) else f"√{{{a}}} ÷ √{{{b}}}을 간단히 하세요."
            lines = [L(f"√{{{a}}} ÷ √{{{b}}} = √{{{F_(a, b)}}}", memo="근호끼리 나누기"), L(f"√{{{F_(a, b)}}} = √{{{m}}}"), L(f"√{{{m}}} = {res}")]
            if res == f"√{{{m}}}":
                lines = lines[:2]
        S.add(2, q, res, "근호끼리 곱하고(나누고) 간단히", lines, None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        if k == 0:
            b = R.choice([2, 3, 5, 6, 7, 10])
            a = b * R.randint(1, 6) if R.random() < 0.6 else R.randint(1, 12)
            g = gcd(a, b)
            res = f"{{{a // g if a // g > 1 else ''}√{{{b}}}/{b // g}}}" if b // g > 1 else RT(a // g, b)
            q = f"{{{a}/√{{{b}}}}}의 분모를 유리화하세요."
            lines = [L(f"{{{a}/√{{{b}}}}} = {{{a} × √{{{b}}}/√{{{b}}} × √{{{b}}}}}", memo=f"분자 · 분모에 √{{{b}}}를 곱해요"), L(f"{{{a} × √{{{b}}}/√{{{b}}} × √{{{b}}}}} = {{{a}√{{{b}}}/{b}}}"), L(f"{{{a}√{{{b}}}/{b}}} = {res}", memo="약분")]
            if g == 1:
                lines = lines[:2]
                res = f"{{{a if a > 1 else ''}√{{{b}}}/{b}}}"
        else:
            a, b = R.sample([2, 3, 5, 6, 7, 10, 11], 2)
            p = a * b
            o, i = sq(p)
            res = f"{{{RT(o, i)}/{b}}}"
            q = f"{{√{{{a}}}/√{{{b}}}}}의 분모를 유리화하세요."
            lines = [L(f"{{√{{{a}}}/√{{{b}}}}} = {{√{{{a}}} × √{{{b}}}/√{{{b}}} × √{{{b}}}}}", memo=f"√{{{b}}}를 곱해요"), L(f"{{√{{{a}}} × √{{{b}}}/√{{{b}}} × √{{{b}}}}} = {res}")]
        S.add(3, q, res, "분모의 근호를 분자 · 분모에 똑같이 곱해요", lines, None, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        base = R.choice([2, 3, 5, 6, 7])
        ks = [R.randint(1, 5) for _ in range(3)]
        sg = [1, R.choice([1, -1]), R.choice([1, -1])]
        terms = []
        tot = 0
        for j, (kk, s_) in enumerate(zip(ks, sg)):
            if j == 0:
                terms.append((RT(kk, base), kk * s_, f"{RT(kk, base)}"))
            else:
                n = kk * kk * base
                terms.append((f"√{{{n}}}", kk * s_, f"{RT(kk, base)}"))
            tot += kk * s_
        if tot == 0 or (ks[1] == ks[2] and sg[1] != sg[2]):
            return
        ex = terms[0][0] + "".join(f" {'+' if t[1] > 0 else MI} {t[0]}" for t in terms[1:])
        ex2 = terms[0][2] + "".join(f" {'+' if t[1] > 0 else MI} {t[2]}" for t in terms[1:])
        res = RT(tot, base)
        q = f"{J(ex, '을', '를')} 간단히 하세요."
        lines = [L(f"{ex} = {ex2}", memo="모두 a√{b} 꼴로"), L(f"{ex2} = {res}", memo="근호 안이 같은 것끼리")]
        S.add(4, q, res, "a√{b} 꼴로 바꾼 뒤 근호 안이 같은 것끼리", lines, None, omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        if k == 0:
            a = R.choice([2, 3, 5, 6])
            b, c = R.sample([2, 3, 5, 6, 10, 15], 2)
            o1, i1 = sq(a * b)
            o2, i2 = sq(a * c)
            t1, t2 = RT(o1, i1), RT(o2, i2)
            if i1 == i2:
                return
            q = f"√{{{a}}}(√{{{b}}} + √{{{c}}})를 계산하세요." if not bat(c) else f"√{{{a}}}(√{{{b}}} + √{{{c}}})을 계산하세요."
            res = f"{t1} + {t2}" if i1 > i2 or i2 == 1 else f"{t2} + {t1}"
            res = f"{t1} + {t2}"
            lines = [L(f"√{{{a}}}(√{{{b}}} + √{{{c}}}) = √{{{a * b}}} + √{{{a * c}}}", memo="분배법칙"), L(f"√{{{a * b}}} + √{{{a * c}}} = {res}")]
            S.add(5, q, res, "분배법칙으로 괄호를 풀고 간단히", lines, None, omr="ex", key=q)
        else:
            n = R.randint(5, 90)
            r = math.isqrt(n)
            if r * r == n:
                return
            c = R.randint(1, 6)
            q = f"{c} + √{{{n}}}의 정수 부분을 구하세요."
            lines = [L(f"{r}^{{2}} = {r * r}, {r + 1}^{{2}} = {(r + 1) ** 2}", memo="사이에 끼는 제곱수"), L(f"{r * r} < {n} < {(r + 1) ** 2} → {r} < √{{{n}}} < {r + 1}"), L(f"{c + r} < {c} + √{{{n}}} < {c + r + 1} → 정수 부분 {c + r}")]
            S.add(5, q, str(c + r), "√{n}을 사이에 끼는 두 정수로", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 곱셈 공식 ══════════
def term(c, v="x"):
    return mono(c, v, 1, first=True)

def expand():
    S = Set("expand", "곱셈 공식 — 전개하고 변형하기", "곱셈 공식",
            {1: "(a ± b)^{2}", 2: "(a + b)(a − b)", 3: "(x + a)(x + b) · (ax + b)(cx + d)", 4: "곱셈 공식으로 수 계산", 5: "곱셈 공식의 변형"},
            pp=10,
            tips={1: "(a + b)^{2} = a^{2} + 2ab + b^{2} · (a − b)^{2} = a^{2} − 2ab + b^{2} — 가운데 항 2ab를 잊지 마세요",
                  2: "(a + b)(a − b) = a^{2} − b^{2}",
                  3: "(x + a)(x + b) = x^{2} + (a + b)x + ab · (ax + b)(cx + d) = acx^{2} + (ad + bc)x + bd",
                  4: "103^{2} = (100 + 3)^{2} · 98 × 102 = (100 − 2)(100 + 2)",
                  5: "a^{2} + b^{2} = (a + b)^{2} − 2ab · (a − b)^{2} = (a + b)^{2} − 4ab"},
            note="곱셈 공식은 넓이 그림(정사각형을 네 조각으로)으로 한 번 확인한 뒤 외우게 해 주세요. 변형 공식은 공식 하나에서 이항해서 만들어 내는 연습이 좋아요.")
    R = rng(1502)

    def g1():
        a, b = R.randint(1, 5), R.randint(1, 9)
        s = R.choice([1, -1])
        A = term(a)
        B = N(b)
        e = f"({A} {'+' if s > 0 else MI} {B})^{{2}}"
        res = poly([a * a, 2 * a * b * s, b * b])
        q = f"{J(e, '을', '를')} 전개하세요."
        lines = [L(f"{e} = ({A})^{{2}} {'+' if s > 0 else MI} 2 × {A} × {B} + {B}^{{2}}" if a > 1 else f"{e} = x^{{2}} {'+' if s > 0 else MI} 2 × x × {B} + {B}^{{2}}", memo="(a ± b)^{2} = a^{2} ± 2ab + b^{2}"), None]
        lines[1] = L(f"({A})^{{2}} {'+' if s > 0 else MI} 2 × {A} × {B} + {B}^{{2}} = {res}" if a > 1 else f"x^{{2}} {'+' if s > 0 else MI} 2 × x × {B} + {B}^{{2}} = {res}")
        if a > 1:
            f = Fig()
            W = 420
            p = W * a / (a + b)
            f.rect(120, 120, W, W, c="ink", sw=3)
            f.line(120 + p, 120, 120 + p, 540, c="ink", w=2.5)
            f.line(120, 120 + p, 540, 120 + p, c="ink", w=2.5)
            f.rect(122, 122, p - 4, p - 4, c="none", f="gold", fo=0.35, at=0)
            f.rect(124 + p, 124 + p, W - p - 6, W - p - 6, c="none", f="teal", fo=0.35, at=0)
            f.rect(124 + p, 122, W - p - 6, p - 4, c="none", f="coral", fo=0.3, at=0, dl=300)
            f.rect(122, 124 + p, p - 4, W - p - 6, c="none", f="coral", fo=0.3, at=0, dl=300)
            f.text(120 + p / 2, 108, A, z=28, b=700)
            f.text(120 + p + (W - p) / 2, 108, B, z=28, b=700)
            fig = f.out() if s > 0 else None
        else:
            fig = None
        S.add(1, q, res, "(a ± b)^{2} = a^{2} ± 2ab + b^{2}", lines, fig, omr="ex", ident=True, key=q)
    fill(S, 1, 20, g1)

    def g2():
        a, b = R.randint(1, 6), R.randint(1, 9)
        A = term(a)
        v2 = R.choice(["", "y"])
        Bs = f"{b}{v2}" if v2 else str(b)
        e = f"({A} + {Bs})({A} {MI} {Bs})" if R.random() < 0.5 else f"({A} {MI} {Bs})({A} + {Bs})"
        res = f"{mono(a * a, 'x', 2, first=True)} {MI} {b * b}{v2 + '^{2}' if v2 else ''}"
        q = f"{J(e, '을', '를')} 전개하세요."
        lines = [L(f"{e} = ({A})^{{2}} {MI} ({Bs})^{{2}}" if a > 1 else f"{e} = x^{{2}} {MI} ({Bs})^{{2}}", memo="(a + b)(a − b) = a^{2} − b^{2}"), None]
        lines[1] = L(f"({A})^{{2}} {MI} ({Bs})^{{2}} = {res}" if a > 1 else f"x^{{2}} {MI} ({Bs})^{{2}} = {res}")
        S.add(2, q, res, "합과 차의 곱 = 제곱의 차", lines, None, omr="ex", ident=True, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        if k == 0:
            a, b = R.randint(-9, 9), R.randint(-9, 9)
            if a == 0 or b == 0 or a == -b:
                return
            e = f"(x {'+' if a > 0 else MI} {abs(a)})(x {'+' if b > 0 else MI} {abs(b)})"
            res = poly([1, a + b, a * b])
            q = f"{J(e, '을', '를')} 전개하세요."
            lines = [L(f"{e} = x^{{2}} + ({N(a)} + {NP(b)})x + ({N(a)}) × {NP(b)}", memo="(x + a)(x + b) = x^{2} + (a + b)x + ab"), L(f"x^{{2}} + ({N(a)} + {NP(b)})x + ({N(a)}) × {NP(b)} = {res}")]
        else:
            a, b, c, d = R.randint(1, 5), R.randint(-7, 7), R.randint(1, 5), R.randint(-7, 7)
            if b == 0 or d == 0 or (a == 1 and c == 1):
                return
            e = f"({lin(a, b)})({lin(c, d)})"
            res = poly([a * c, a * d + b * c, b * d])
            q = f"{J(e, '을', '를')} 전개하세요."
            lines = [L(f"{e} = {a * c}x^{{2}} + ({a} × {NP(d)} + {NP(b)} × {c})x + ({N(b)}) × {NP(d)}", memo="acx^{2} + (ad + bc)x + bd"), L(f"{a * c}x^{{2}} + ({a} × {NP(d)} + {NP(b)} × {c})x + ({N(b)}) × {NP(d)} = {res}")]
        S.add(3, q, res, "곱셈 공식에 맞추어 계수를 정리해요", lines, None, omr="ex", ident=True, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        base = R.choice([10, 20, 30, 50, 100, 200])
        d = R.randint(1, 4)
        if k == 0:
            n = base + d
            e = f"{n}^{{2}}"
            lines = [L(f"{n}^{{2}} = ({base} + {d})^{{2}}", memo="계산하기 쉬운 수로 나누기"), L(f"({base} + {d})^{{2}} = {base * base} + {2 * base * d} + {d * d}", memo="a^{2} + 2ab + b^{2}"), L(f"{base * base} + {2 * base * d} + {d * d} = {n * n}")]
            v = n * n
        elif k == 1:
            n = base - d
            e = f"{n}^{{2}}"
            lines = [L(f"{n}^{{2}} = ({base} − {d})^{{2}}"), L(f"({base} − {d})^{{2}} = {base * base} − {2 * base * d} + {d * d}", memo="a^{2} − 2ab + b^{2}"), L(f"{base * base} − {2 * base * d} + {d * d} = {n * n}")]
            v = n * n
        else:
            e = f"{base - d} × {base + d}"
            lines = [L(f"{e} = ({base} − {d})({base} + {d})", memo="합과 차의 곱"), L(f"({base} − {d})({base} + {d}) = {base}^{{2}} − {d}^{{2}}"), L(f"{base}^{{2}} − {d}^{{2}} = {base * base - d * d}")]
            v = base * base - d * d
        q = f"곱셈 공식을 이용하여 {J(e, '을', '를')} 계산하세요."
        S.add(4, q, N(v), "계산하기 쉬운 수(몇십 · 몇백)와 차로 나누어 곱셈 공식", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            s, p = R.randint(2, 9), R.randint(1, 12)
            if s * s < 4 * p:                  # a, b 가 실수이려면 (a + b)^2 ≥ 4ab
                return
            v = s * s - 2 * p
            q = f"a + b = {s}, ab = {p}일 때, a^{{2}} + b^{{2}}의 값을 구하세요."
            lines = [L("a^{2} + b^{2} = (a + b)^{2} − 2ab", memo="(a + b)^{2} = a^{2} + 2ab + b^{2}에서"), L(f"{s}^{{2}} − 2 × {p} = {v}")]
        elif k == 1:
            s, p = R.randint(2, 9), R.randint(1, 12)
            v = s * s - 4 * p
            if v < 0:
                return
            q = f"a + b = {s}, ab = {p}일 때, (a − b)^{{2}}의 값을 구하세요."
            lines = [L("(a − b)^{2} = (a + b)^{2} − 4ab", memo="두 공식의 차"), L(f"{s}^{{2}} − 4 × {p} = {v}")]
        else:
            s = R.randint(2, 7)
            v = s * s - 2
            q = f"x + {{1/x}} = {s}일 때, x^{{2}} + {{1/x^{{2}}}}의 값을 구하세요."
            lines = [L("x^{2} + {1/x^{2}} = (x + {1/x})^{2} − 2", memo="x × {1/x} = 1"), L(f"{s}^{{2}} − 2 = {v}")]
        S.add(5, q, N(v), "구하는 식을 합과 곱으로 바꾸어 나타내요", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 이차방정식 ══════════
def roots_str(r1, r2):
    if r1 == r2:
        return f"x = {FR(r1)} (중근)"
    a, b = sorted([r1, r2])
    return f"x = {FR(a)} 또는 x = {FR(b)}"

def qeq():
    S = Set("qeq", "이차방정식 — 인수분해 · 완전제곱식 · 근의 공식", "이차방정식",
            {1: "인수분해로 풀기", 2: "제곱근으로 풀기", 3: "완전제곱식으로 풀기", 4: "근의 공식", 5: "이차방정식의 활용"},
            mixed=True, pp=10,
            tips={1: "AB = 0이면 A = 0 또는 B = 0 — 인수분해한 뒤 각 인수를 0으로",
                  2: "x^{2} = k(k > 0)면 x = ±√{k} · (x − p)^{2} = k면 x = p ± √{k}",
                  3: "x^{2}의 계수를 1로, 상수항을 이항, 양변에 ({x의 계수/2})^{2}을 더해요",
                  4: "ax^{2} + bx + c = 0의 근 x = {−b ± √{b^{2} − 4ac}/2a}",
                  5: "구하는 것을 x로, 식을 세워 풀고, 문제의 조건(자연수 · 양수)에 맞는 근만"},
            note="풀이 방법은 ‘인수분해가 보이면 인수분해, 아니면 근의 공식’으로 정리하게 해 주세요. 완전제곱식 만들기는 근의 공식이 어디서 나왔는지 보여 주는 과정이에요.")
    R = rng(1503)

    def g1():
        k = S.count(1) % 3
        if k < 2:
            r1, r2 = R.randint(-9, 9), R.randint(-9, 9)
            if r1 == r2 and k == 0 or r1 == 0 and r2 == 0:
                return
            a = 1 if k == 0 else R.randint(2, 3)
            b, c = -a * (r1 + r2), a * r1 * r2
            eq = f"{poly([a, b, c])} = 0"
            f1 = f"(x {'+' if -r1 > 0 else MI} {abs(r1)})" if r1 else "x"
            f2 = f"(x {'+' if -r2 > 0 else MI} {abs(r2)})" if r2 else "x"
            fac = (f"{a}" if a > 1 else "") + f"{f1}{f2}"
            lines = [L(f"{fac} = 0", memo="인수분해"), L(f"x = {N(r1)} 또는 x = {N(r2)}" if r1 != r2 else f"x = {N(r1)}", memo="각 인수 = 0")]
            ans = roots_str(Fr(r1), Fr(r2))
        else:
            p, q_ = R.randint(1, 4), R.randint(-6, 6)
            r = R.randint(1, 3)
            if q_ == 0:
                return
            # (px + q)(rx − s) = 0
            s_ = R.randint(-6, 6)
            if s_ == 0:
                return
            A, B, C = p * r, p * (-s_) + q_ * r, -q_ * s_
            eq = f"{poly([A, B, C])} = 0"
            fac = f"({lin(p, q_)})({lin(r, -s_)})"
            r1, r2 = Fr(-q_, p), Fr(s_, r)
            lines = [L(f"{fac} = 0", memo="인수분해"), L(f"x = {FR(r1)} 또는 x = {FR(r2)}" if r1 != r2 else f"x = {FR(r1)}", memo="각 인수 = 0")]
            ans = roots_str(r1, r2)
        q = f"이차방정식 {J(eq, '을', '를')} 푸세요."
        X = sp.Symbol("x")
        assert all(sp.simplify(val(eq.split(" = ")[0]).subs({SYMS["x"]: rr})) == 0 for rr in (sp.Rational(r1.numerator, r1.denominator) if isinstance(r1, Fr) else r1, sp.Rational(Fr(r2).numerator, Fr(r2).denominator)))
        S.add(1, q, ans, "인수분해해서 각 인수를 0으로", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            a = R.randint(1, 4)
            n = R.choice([2, 3, 5, 6, 7, 8, 12, 18, 20, 27, 45, 48])
            o, i = sq(n)
            q = f"이차방정식 {a if a > 1 else ''}x^{{2}} = {a * n}을 푸세요." if bat(a * n) else f"이차방정식 {a if a > 1 else ''}x^{{2}} = {a * n}를 푸세요."
            lines = ([L(f"x^{{2}} = {n}", memo=f"양변을 {RO(a)} 나눠요")] if a > 1 else []) + [L(f"x = ±√{{{n}}}", memo="제곱해서 n이 되는 수"), L(f"x = ±{RT(o, i)}" if o > 1 else f"x = ±√{{{n}}}")]
            ans = f"x = ±{RT(o, i)}"
            S.add(2, q, ans, "x^{2} = k → x = ±√{k}", lines if o > 1 else lines[:-1], None, omr="ex", sub={"x": o * sp.sqrt(i)}, key=q)
        else:
            p = R.randint(-6, 6)
            n = R.choice([2, 3, 5, 6, 7, 10, 12, 18])
            o, i = sq(n)
            if p == 0:
                return
            eq = f"(x {'+' if -p > 0 else MI} {abs(p)})^{{2}} = {n}"
            r = f"{N(p)} ± {RT(o, i)}"
            q = f"이차방정식 {J(eq, '을', '를')} 푸세요."
            lines = [L(f"x {'+' if -p > 0 else MI} {abs(p)} = ±{RT(o, i)}", memo="제곱근을 생각해요"), L(f"x = {r}", memo="이항")]
            S.add(2, q, f"x = {r}", "(x − p)^{2} = k → x = p ± √{k}", lines, None, omr="ex", sub={"x": p + o * sp.sqrt(i)}, key=q)
    fill(S, 2, 20, g2)

    def g3():
        h = R.randint(-5, 5)
        if h == 0:
            return
        k_ = R.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13])
        b = 2 * h
        c = h * h - k_
        o, i = sq(k_)
        eq = f"{poly([1, b, c])} = 0"
        q = f"완전제곱식을 이용하여 이차방정식 {J(eq, '을', '를')} 푸세요."
        lines = [L(f"{poly([1, b, 0])} = {N(-c)}", memo="상수항을 이항"), L(f"{poly([1, b, 0])} + {h * h} = {N(-c)} + {h * h}", memo=f"양변에 ({{{N(b)}/2}})^{{2}} = {h * h}을 더해요" if bat(h * h) else f"양변에 ({{{N(b)}/2}})^{{2}} = {h * h}를 더해요"),
                 L(f"(x {'+' if h > 0 else MI} {abs(h)})^{{2}} = {k_}"), L(f"x = {N(-h)} ± {RT(o, i)}")]
        S.add(3, q, f"x = {N(-h)} ± {RT(o, i)}", "x^{2} + bx 꼴로 만들고 ({b/2})^{2}을 더해요", lines, None, omr="ex", sub={"x": -h + o * sp.sqrt(i)}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b, c = R.randint(1, 4), R.randint(-9, 9), R.randint(-9, 9)
        D = b * b - 4 * a * c
        if D <= 0 or math.isqrt(D) ** 2 == D or a == 0 or c == 0:
            return
        o, i = sq(D)
        g = gcd(gcd(abs(b), o), 2 * a)
        eq = f"{poly([a, b, c])} = 0"
        num = f"{N(-b)} ± {RT(o, i)}" if b != 0 else f"±{RT(o, i)}"
        ans_n = f"{N(-b // g)} ± {RT(o // g, i)}" if b != 0 else f"±{RT(o // g, i)}"
        den = 2 * a // g
        ans = f"x = {{{ans_n}/{den}}}" if den > 1 else f"x = {ans_n}"
        q = f"근의 공식을 이용하여 이차방정식 {J(eq, '을', '를')} 푸세요."
        lines = [L(f"a = {a}, b = {N(b)}, c = {N(c)}"), L(f"b^{{2}} − 4ac = {NP(b)}^{{2}} − 4 × {a} × {NP(c)} = {D}"), L(f"x = {{{num}/{2 * a}}}" + (f" = {{{ans_n}/{den}}}" if g > 1 and den > 1 else (f" = {ans_n}" if g > 1 else "")))]
        S.add(4, q, ans, "x = {−b ± √{b^{2} − 4ac}/2a}", lines, None, omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            n = R.randint(3, 20)
            P = n * (n + 1)
            q = f"연속하는 두 자연수의 곱이 {P}일 때, 두 자연수 중 작은 수를 구하세요."
            lines = [L(f"x(x + 1) = {P}", memo="작은 수 x"), L(f"x^{{2}} + x − {P} = 0"), L(f"(x − {n})(x + {n + 1}) = 0"), L(f"x는 자연수 → x = {n}")]
            S.add(5, q, str(n), "작은 수를 x로 — 자연수 조건", lines, None, sub={"x": n}, key=q)
        elif k == 1:
            w = R.randint(3, 15); d = R.randint(1, 6)
            A = w * (w + d)
            q = f"가로가 세로보다 {d} cm 긴 직사각형의 넓이가 {A} cm²일 때, 세로의 길이를 구하세요."
            lines = [L(f"x(x + {d}) = {A}", memo="세로 x cm"), L(f"x^{{2}} + {d}x − {A} = 0"), L(f"(x − {w})(x + {w + d}) = 0"), L(f"x > 0 → x = {w}")]
            S.add(5, q, f"{w} cm", "길이는 양수 — 맞는 근만 골라요", lines, None, ap=str(w), sub={"x": w}, key=q)
        else:
            r1, r2 = R.randint(-6, 6), R.randint(-6, 6)
            if r1 == r2 or r1 == 0 or r2 == 0:
                return
            b, c = -(r1 + r2), r1 * r2
            q = f"이차방정식 x^{{2}} + ax + b = 0의 두 근이 {N(r1)}, {N(r2)}일 때, 상수 a, b의 값을 구하세요."
            lines = [L(f"(x − {NP(r1)})(x − {NP(r2)}) = 0", memo="두 근으로 식 만들기"), L(f"x^{{2}} − ({N(r1)} + {NP(r2)})x + ({N(r1)}) × {NP(r2)} = 0"), L(f"a = {N(b)}, b = {N(c)}")]
            S.add(5, q, f"a = {N(b)}, b = {N(c)}", "두 근이 p, q → (x − p)(x − q) = 0", lines, None, ap=f"a={b}, b={c}", omr="ex", sub={"x": r1}, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 삼각비 ══════════
TR = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)]
SP = {30: ("{1/2}", "{√{3}/2}", "{√{3}/3}"), 45: ("{√{2}/2}", "{√{2}/2}", "1"), 60: ("{√{3}/2}", "{1/2}", "√{3}")}

def rtri(f, a, b, labs, at="q"):
    """∠C = 90°, BC = a(밑변), AC = b(높이) — A 위, B 오른쪽 아래, C 왼쪽 아래"""
    sc = min(440 / a, 380 / b)
    C, B, A = (120, 530), (120 + sc * a, 530), (120, 530 - sc * b)
    f.poly([A, B, C], c="ink", w=3, f="gold", fo=0.08, at=at)
    angle_mark(f, C, B, A, r=28, at=at)
    angle_mark(f, B, A, C, r=50, at=at, label=None)
    for nm_, P, dx, dy in (("A", A, -18, -10), ("B", B, 22, 30), ("C", C, -22, 30)):
        f.text(P[0] + dx, P[1] + dy, nm_, z=28, b=700, at=at)
    la, lb, lc = labs
    if la:
        f.text((B[0] + C[0]) / 2, 572, la, z=28, b=700, at=at)
    if lb:
        f.text(98, (A[1] + C[1]) / 2, lb, z=28, b=700, a="e", at=at)
    if lc:
        f.text((A[0] + B[0]) / 2 + 24, (A[1] + B[1]) / 2 - 10, lc, z=28, b=700, a="s", at=at)
    return A, B, C

def trig():
    S = Set("trig", "삼각비 — 직각삼각형의 변의 비와 특수각", "삼각비",
            {1: "삼각비의 값", 2: "한 삼각비로 나머지 구하기", 3: "30° · 45° · 60°의 삼각비", 4: "삼각비로 변의 길이", 5: "삼각비의 활용"},
            mixed=True, pp=8,
            tips={1: "∠B 기준: sin B = {(높이)/(빗변)}, cos B = {(밑변)/(빗변)}, tan B = {(높이)/(밑변)}",
                  2: "주어진 비로 직각삼각형을 그리고, 피타고라스 정리로 나머지 변",
                  3: "30° · 60°는 1 : √{3} : 2, 45°는 1 : 1 : √{2} 직각삼각형",
                  4: "빗변을 알면 sin · cos, 밑변을 알면 tan로",
                  5: "높이 = 거리 × tan(올려본각) · 넓이 = {1/2}ab sin C"},
            note="삼각비는 ‘기준각에서 본 높이 · 밑변 · 빗변’을 정하는 것이 먼저예요. 기준각에 표시를 하고 변 세 개에 이름을 붙인 뒤 비를 쓰게 해 주세요.")
    R = rng(1504)

    def g1():
        a, b, c = R.choice(TR)
        if R.random() < 0.5:
            a, b = b, a
        fn = R.choice(["sin", "cos", "tan"])
        f = Fig()
        rtri(f, a, b, (str(a), str(b), str(c)))
        v = {"sin": Fr(b, c), "cos": Fr(a, c), "tan": Fr(b, a)}[fn]
        part = {"sin": ("높이 AC", "빗변 AB", b, c), "cos": ("밑변 BC", "빗변 AB", a, c), "tan": ("높이 AC", "밑변 BC", b, a)}[fn]
        q = f"∠C = 90°인 직각삼각형 ABC에서 BC = {a}, AC = {b}, AB = {c}일 때, {fn} B의 값을 구하세요."
        lines = [L(f"{fn} B = {{{part[0]}/{part[1]}}}", memo="∠B에서 본 변"), L(f"{F_(part[2], part[3])}")]
        S.add(1, q, F_(part[2], part[3]), "기준각 B에서 높이 · 밑변 · 빗변을 정해요", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        a, b, c = R.choice(TR)
        if R.random() < 0.5:
            a, b = b, a
        given = R.choice(["sin", "cos", "tan"])
        want = R.choice([x for x in ("sin", "cos", "tan") if x != given])
        gv = {"sin": (b, c), "cos": (a, c), "tan": (b, a)}[given]
        wv = {"sin": (b, c), "cos": (a, c), "tan": (b, a)}[want]
        f = Fig()
        known = {"sin": (None, str(b), str(c)), "cos": (str(a), None, str(c)), "tan": (str(a), str(b), None)}[given]
        rtri(f, a, b, known)
        missing = {"sin": ("밑변", a, f"√{{{c}^{{2}} − {b}^{{2}}}} = {a}"), "cos": ("높이", b, f"√{{{c}^{{2}} − {a}^{{2}}}} = {b}"), "tan": ("빗변", c, f"√{{{a}^{{2}} + {b}^{{2}}}} = {c}")}[given]
        q = f"∠C = 90°인 직각삼각형 ABC에서 {given} B = {F_(*gv)}일 때, {want} B의 값을 구하세요."
        lines = [L(f"{given} B = {F_(*gv)} → 변의 비로 삼각형 그리기"), L(f"{missing[0]} = {missing[2]}", memo="피타고라스 정리"), L(f"{want} B = {F_(*wv)}")]
        S.add(2, q, F_(*wv), "주어진 비로 직각삼각형 → 피타고라스로 나머지 변", lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 4
        exprs = [
            ("sin 30° + cos 60°", "{1/2} + {1/2} = 1", "1"),
            ("sin 60° × cos 30°", "{√{3}/2} × {√{3}/2} = {3/4}", "{3/4}"),
            ("tan 45° + sin 30°", "1 + {1/2} = {3/2}", "{3/2}"),
            ("cos 45° × sin 45°", "{√{2}/2} × {√{2}/2} = {1/2}", "{1/2}"),
            ("tan 60° × tan 30°", "√{3} × {√{3}/3} = 1", "1"),
            ("sin 30° × tan 60°", "{1/2} × √{3} = {√{3}/2}", "{√{3}/2}"),
            ("cos 60° + tan 45°", "{1/2} + 1 = {3/2}", "{3/2}"),
            ("sin 45° ÷ cos 45°", "{√{2}/2} ÷ {√{2}/2} = 1", "1"),
            ("2sin 30° + tan 45°", "2 × {1/2} + 1 = 2", "2"),
            ("sin 60° ÷ cos 60°", "{√{3}/2} ÷ {1/2} = √{3}", "√{3}"),
            ("cos 30° − sin 60°", "{√{3}/2} − {√{3}/2} = 0", "0"),
            ("sin 30° + cos 30° × tan 30°", "{1/2} + {√{3}/2} × {√{3}/3} = 1", "1"),
            ("tan 30° × cos 30°", "{√{3}/3} × {√{3}/2} = {1/2}", "{1/2}"),
            ("(sin 45°)^{2} + (cos 45°)^{2}", "({√{2}/2})^{2} + ({√{2}/2})^{2} = 1", "1"),
            ("(sin 60°)^{2} + (cos 60°)^{2}", "({√{3}/2})^{2} + ({1/2})^{2} = 1", "1"),
            ("4cos 60° − tan 45°", "4 × {1/2} − 1 = 1", "1"),
            ("2cos 30° × tan 60°", "2 × {√{3}/2} × √{3} = 3", "3"),
            ("sin 30° × cos 60° × tan 45°", "{1/2} × {1/2} × 1 = {1/4}", "{1/4}"),
            ("6sin 30° − 2tan 45°", "6 × {1/2} − 2 × 1 = 1", "1"),
            ("cos 45° × 2√{2}", "{√{2}/2} × 2√{2} = 2", "2"),
            ("tan 60° ÷ tan 30°", "√{3} ÷ {√{3}/3} = 3", "3"),
            ("3tan 30° × sin 60°", "3 × {√{3}/3} × {√{3}/2} = {3/2}", "{3/2}"),
        ]
        e, calc_, ans = R.choice(exprs)
        q = f"{J(e, '을', '를')} 계산하세요."
        lines = [L(calc_.split(" = ")[0], memo="특수각의 삼각비 값을 넣어요"), L(calc_)]
        if k == 0:
            f = Fig()
            sc = 220
            A0, B0, C0 = (120, 520), (120 + sc * math.sqrt(3), 520), (120, 520 - sc)
            f.poly([A0, B0, C0], c="ink", w=3)
            f.text((A0[0] + B0[0]) / 2, 560, "√{3}", z=28, b=700)
            f.text(100, 410, "1", z=28, b=700, a="e")
            f.text(330, 380, "2", z=28, b=700)
            f.text(B0[0] - 60, 506, "30°", z=24, c="teal", b=700)
            f.text(140, 330, "60°", z=24, c="teal", b=700, a="s")
        else:
            f = None
        S.add(3, q, ans, "30° · 45° · 60°의 삼각비를 넣어 계산", lines, f.out() if f else None, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        ang = R.choice([30, 45, 60])
        L_ = R.randint(2, 12) * 2
        f = Fig()
        if k == 0:
            if ang == 30:
                v, s = f"{L_ // 2}", f"{L_} × {{1/2}} = {L_ // 2}"
            elif ang == 45:
                v, s = f"{L_ // 2}√{{2}}", f"{L_} × {{√{{2}}/2}} = {L_ // 2}√{{2}}"
            else:
                v, s = f"{L_ // 2}√{{3}}", f"{L_} × {{√{{3}}/2}} = {L_ // 2}√{{3}}"
            v = v.replace("1√", "√") if v.startswith("1√") else v
            s = s.replace(" 1√", " √")
            rtri(f, 6, 4, (None, "x", f"{L_}"))
            q = f"∠C = 90°인 직각삼각형 ABC에서 AB = {L_}, ∠B = {ang}°일 때, AC의 길이를 구하세요."
            lines = [L(f"AC = AB × sin {ang}°", memo="빗변과 높이 → sin"), L(s)]
        elif k == 1:
            if ang == 30:
                v, s = f"{L_ // 2}√{{3}}", f"{L_} × {{√{{3}}/2}} = {L_ // 2}√{{3}}"
            elif ang == 45:
                v, s = f"{L_ // 2}√{{2}}", f"{L_} × {{√{{2}}/2}} = {L_ // 2}√{{2}}"
            else:
                v, s = f"{L_ // 2}", f"{L_} × {{1/2}} = {L_ // 2}"
            v = v.replace("1√", "√") if v.startswith("1√") else v
            s = s.replace(" 1√", " √")
            rtri(f, 6, 4, ("x", None, f"{L_}"))
            q = f"∠C = 90°인 직각삼각형 ABC에서 AB = {L_}, ∠B = {ang}°일 때, BC의 길이를 구하세요."
            lines = [L(f"BC = AB × cos {ang}°", memo="빗변과 밑변 → cos"), L(s)]
        else:
            a = R.randint(2, 12) * 3
            if ang == 30:
                v, s = f"{a // 3}√{{3}}", f"{a} × {{√{{3}}/3}} = {a // 3}√{{3}}"
            elif ang == 45:
                v, s = f"{a}", f"{a} × 1 = {a}"
            else:
                v, s = f"{a}√{{3}}", f"{a} × √{{3}} = {a}√{{3}}"
            v = v.replace("1√", "√") if v.startswith("1√") else v
            s = s.replace(" 1√", " √")
            rtri(f, 6, 4, (f"{a}", "x", None))
            q = f"∠C = 90°인 직각삼각형 ABC에서 BC = {a}, ∠B = {ang}°일 때, AC의 길이를 구하세요."
            lines = [L(f"AC = BC × tan {ang}°", memo="밑변과 높이 → tan"), L(s)]
        S.add(4, q, v, "알고 있는 변과 구하는 변으로 삼각비를 골라요", lines, f.out(), omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        if k == 0:
            d = R.randint(2, 20) * 3
            ang = R.choice([30, 45, 60])
            if ang == 30:
                hv, s = f"{d // 3}√{{3}}", f"{d} × tan 30° = {d} × {{√{{3}}/3}} = {d // 3}√{{3}}"
            elif ang == 45:
                hv, s = f"{d}", f"{d} × tan 45° = {d}"
            else:
                hv, s = f"{d}√{{3}}", f"{d} × tan 60° = {d}√{{3}}"
            hv = hv.replace("1√", "√") if hv.startswith("1√") else hv
            f = Fig()
            f.line(60, 520, 600, 520, c="ink", w=3)
            f.line(520, 520, 520, 140, c="ink", w=5)
            f.line(120, 520, 520, 140, c="teal", w=2.5, d=True)
            f.text(320, 560, f"{d} `m`", z=26, b=700)
            f.text(160, 500, f"{ang}°", z=24, c="teal", b=700, a="s")
            q = f"나무로부터 {d} `m` 떨어진 곳에서 나무 꼭대기를 올려본각의 크기가 {ang}°였어요. 나무의 높이는 몇 `m`인가요? (눈높이는 생각하지 않아요)"
            lines = [L("높이 = 거리 × tan(올려본각)", memo="밑변과 높이 → tan"), L(s), L(f"{hv} `m`")]
            S.add(5, q, f"{hv} `m`", "올려본각 → tan", lines, f.out(), ap=plain(hv), omr="ex", key=q)
        else:
            a, b = R.randint(2, 12), R.randint(2, 12)
            ang = R.choice([30, 45, 60, 120, 135, 150])
            if ang in (30, 150):
                A_ = Fr(a * b, 4)
                v = FR(A_)
                calc_ = f"{{1/2}} × {a} × {b} × {{1/2}} = {v}"
            elif ang in (45, 135):
                A_ = Fr(a * b, 4)
                v = f"{{{a * b}√{{2}}/4}}" if (a * b) % 4 else (f"{a * b // 4}√{{2}}" if a * b // 4 > 1 else "√{2}")
                calc_ = f"{{1/2}} × {a} × {b} × {{√{{2}}/2}} = {v}"
            else:
                v = f"{{{a * b}√{{3}}/4}}" if (a * b) % 4 else (f"{a * b // 4}√{{3}}" if a * b // 4 > 1 else "√{3}")
                calc_ = f"{{1/2}} × {a} × {b} × {{√{{3}}/2}} = {v}"
            q = f"두 변의 길이가 {a} cm, {b} cm이고 그 끼인각의 크기가 {ang}°인 삼각형의 넓이를 구하세요."
            lines = [L(f"넓이 = {{1/2}}ab sin C", memo=("둔각이면 sin(180° − C)" if ang > 90 else "끼인각의 sin")), L(calc_), L(f"{v} cm²")]
            S.add(5, q, f"{v} cm²", "두 변과 끼인각 → {1/2}ab sin C", lines, None, ap=plain(v), omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 원의 성질 ══════════
def circ():
    S = Set("circ", "원의 성질 — 원주각 · 중심각 · 접선", "원의 성질",
            {1: "원주각과 중심각", 2: "같은 호 · 반원의 원주각", 3: "원에 내접하는 사각형", 4: "원의 접선의 길이", 5: "접선과 현이 이루는 각"},
            pp=8,
            tips={1: "한 호에 대한 원주각은 중심각의 {1/2}",
                  2: "같은 호에 대한 원주각은 모두 같고, 반원(지름)에 대한 원주각은 90°",
                  3: "마주 보는 두 각의 합은 180° · 한 외각은 마주 보는 내각과 같아요",
                  4: "원 밖의 한 점에서 그은 두 접선의 길이는 같아요 · 접선 ⊥ 반지름",
                  5: "접선과 현이 이루는 각 = 그 각 안에 있는 호에 대한 원주각"},
            note="원주각 문제는 ‘어느 호에 대한 각인가’를 먼저 표시하게 해 주세요. 같은 호를 같은 색으로 칠하면 같은 각이 한눈에 보여요.")
    R = rng(1505)
    O, Rr = (330, 340), 220

    def P(deg):
        return ang_pt(*O, Rr, deg)

    def base(f):
        f.circ(*O, Rr, c="ink", sw=3)
        f.dot(*O, r=6)
        f.text(O[0] + 16, O[1] + 26, "O", z=24, c="soft")

    def g1():
        k = S.count(1) % 2
        c = R.choice([40, 50, 60, 70, 80, 100, 110, 120, 130, 140, 150, 160])
        f = Fig()
        base(f)
        A, B = P(-90 - c / 2), P(-90 + c / 2)
        Pp = P(90 + R.randint(-30, 30))
        f.line(*O, *A, c="teal", w=3); f.line(*O, *B, c="teal", w=3)
        f.line(*Pp, *A, c="ink", w=3); f.line(*Pp, *B, c="ink", w=3)
        for nm_, Q, dx, dy in (("A", A, -18, 26), ("B", B, 18, 26), ("P", Pp, 0, -18)):
            f.text(Q[0] + dx, Q[1] + dy, nm_, z=26, b=700)
        if k == 0:
            angle_mark(f, O, A, B, r=40, label=f"{c}°", c="teal", f_="teal")
            angle_mark(f, Pp, A, B, r=40, label="x", c="coral", f_="coral", at=0)
            q = f"원 O에서 호 AB에 대한 중심각 ∠AOB = {c}°일 때, 원주각 ∠APB의 크기를 구하세요."
            lines = [L("원주각 = {1/2} × 중심각", memo="같은 호 AB"), L(f"{c} ÷ 2 = {c // 2}"), L(f"{c // 2}°")]
            ans, ap = f"{c // 2}°", str(c // 2)
        else:
            angle_mark(f, Pp, A, B, r=40, label=f"{c // 2}°")
            angle_mark(f, O, A, B, r=40, label="x", c="coral", f_="coral", at=0)
            q = f"원 O에서 호 AB에 대한 원주각 ∠APB = {c // 2}°일 때, 중심각 ∠AOB의 크기를 구하세요."
            lines = [L("중심각 = 2 × 원주각"), L(f"{c // 2} × 2 = {c}"), L(f"{c}°")]
            ans, ap = f"{c}°", str(c)
        S.add(1, q, ans, "같은 호에 대한 원주각은 중심각의 {1/2}", lines, f.out(), ap=ap, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        f = Fig()
        base(f)
        if k == 0:
            x = R.randint(20, 75)
            A, B = P(-120), P(-60)
            P1, P2 = P(100), P(150)
            for Q in (P1, P2):
                f.line(*Q, *A, c="ink", w=3); f.line(*Q, *B, c="ink", w=3)
            angle_mark(f, P1, A, B, r=40, label=f"{x}°")
            angle_mark(f, P2, A, B, r=40, label="y", c="coral", f_="coral", at=0)
            q = f"원에서 같은 호 AB에 대한 두 원주각 ∠APB, ∠AQB가 있어요. ∠APB = {x}°일 때 ∠AQB의 크기를 구하세요."
            lines = [L("같은 호에 대한 원주각은 모두 같아요"), L(f"∠AQB = {x}°")]
            ans, ap = f"{x}°", str(x)
        else:
            a = R.randint(20, 70)
            A, B = P(180), P(0)
            C = P(R.randint(40, 140))
            f.line(*A, *B, c="teal", w=3)
            f.line(*C, *A, c="ink", w=3); f.line(*C, *B, c="ink", w=3)
            angle_mark(f, C, A, B, r=30, at=0)
            angle_mark(f, A, B, C, r=44, label=f"{a}°")
            angle_mark(f, B, C, A, r=44, label="x", c="coral", f_="coral", at=1)
            q = f"선분 AB가 원 O의 지름이고 점 C는 원 위의 점이에요. ∠CAB = {a}°일 때, ∠CBA의 크기를 구하세요."
            lines = [L("∠ACB = 90°", memo="지름(반원)에 대한 원주각"), L(f"180 − 90 − {a} = {90 - a}"), L(f"{90 - a}°")]
            ans, ap = f"{90 - a}°", str(90 - a)
        S.add(2, q, ans, "같은 호의 원주각은 같고, 지름의 원주각은 90°", lines, f.out(), ap=ap, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        f = Fig()
        base(f)
        degs = [R.randint(100, 140), R.randint(190, 230), R.randint(280, 320), R.randint(20, 60)]
        A, B, C, D = (P(d) for d in degs)
        f.poly([A, B, C, D], c="ink", w=3)
        for nm_, Q, d in zip("ABCD", (A, B, C, D), degs):
            q_ = ang_pt(*O, Rr + 28, d)
            f.text(q_[0], q_[1] + 9, nm_, z=26, b=700)
        a = R.randint(60, 120)
        if k == 0:
            angle_mark(f, A, B, D, r=40, label=f"{a}°")
            angle_mark(f, C, D, B, r=40, label="x", c="coral", f_="coral", at=0)
            q = f"사각형 ABCD가 원에 내접하고 ∠A = {a}°일 때, ∠C의 크기를 구하세요."
            lines = [L("∠A + ∠C = 180°", memo="마주 보는 두 각"), L(f"180 − {a} = {180 - a}"), L(f"{180 - a}°")]
            ans, ap = f"{180 - a}°", str(180 - a)
        elif k == 1:
            x = R.randint(20, 50)
            m = R.randint(2, 3)
            c0 = 180 - x - m * x
            if c0 <= 0:
                return
            q = f"원에 내접하는 사각형 ABCD에서 ∠A = (x + {c0})°, ∠C = {m}x°일 때, x의 값을 구하세요."
            lines = [L(f"x + {c0} + {m}x = 180", memo="대각의 합 180°"), L(f"{m + 1}x = {180 - c0}"), L(f"x = {x}")]
            S.add(3, q, str(x), "마주 보는 두 각의 합 180°", lines, f.out(), sub={"x": x}, key=q)
            return
        else:
            f.line(*C, *(C[0] + (C[0] - B[0]) * 0.5, C[1] + (C[1] - B[1]) * 0.5), c="soft", w=2.5, d=True)
            q = f"원에 내접하는 사각형 ABCD에서 ∠A = {a}°일 때, 꼭짓점 C에서의 외각(변 BC의 연장선과 CD가 이루는 각)의 크기를 구하세요."
            lines = [L("한 외각 = 마주 보는 내각", memo="∠C의 외각 = 180° − ∠C = ∠A"), L(f"{a}°")]
            ans, ap = f"{a}°", str(a)
        S.add(3, q, ans, "내접사각형 — 대각의 합 180°, 외각 = 마주 보는 내각", lines, f.out(), ap=ap, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        f = Fig()
        f.circ(330, 300, 160, c="ink", sw=3)
        T1, T2 = (330 - 160 * 0.8, 300 + 160 * 0.6), (330 + 160 * 0.8, 300 + 160 * 0.6)
        Pp = (330, 300 + 160 / 0.6)
        f.line(*Pp, *T1, c="ink", w=3); f.line(*Pp, *T2, c="ink", w=3)
        f.line(330, 300, *T1, c="teal", w=2.5, d=True)
        f.dot(330, 300, r=6)
        angle_mark(f, T1, (330, 300), Pp, r=22)
        if k == 0:
            L_ = R.randint(4, 20)
            q = f"원 밖의 점 P에서 원 O에 그은 두 접선의 접점을 A, B라 할 때, PA = {L_} cm이면 PB의 길이는 몇 cm인가요?"
            lines = [L("원 밖의 한 점에서 그은 두 접선의 길이는 같아요"), L(f"PB = PA = {L_}"), L(f"{L_} cm")]
            ans, ap = f"{L_} cm", str(L_)
        else:
            a, b, c = R.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (4, 3, 5), (12, 5, 13), (15, 8, 17), (7, 24, 25)])
            m = R.randint(1, 3) if c < 20 else 1
            a, b, c = a * m, b * m, c * m
            q = f"반지름이 {a} cm인 원 O 밖의 점 P에서 그은 접선의 접점을 A라 할 때, PO = {c} cm이면 PA의 길이는 몇 cm인가요?"
            lines = [L("OA ⊥ PA", memo="접선은 반지름에 수직"), L(f"PA^{{2}} = {c}^{{2}} − {a}^{{2}} = {b * b}"), L(f"PA = {b} cm")]
            ans, ap = f"{b} cm", str(b)
        S.add(4, q, ans, "두 접선의 길이는 같고, 접선은 반지름에 수직", lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        x = R.randint(25, 80)
        k = S.count(5) % 2
        f = Fig()
        base(f)
        T = P(-90)
        f.line(T[0] - 280, T[1], T[0] + 280, T[1], c="ink", w=3)
        B = P(-90 + 2 * x)
        C = P(90 + R.randint(-20, 30))
        f.line(*T, *B, c="ink", w=3)
        f.line(*C, *T, c="ink", w=3); f.line(*C, *B, c="ink", w=3)
        if k == 0:
            angle_mark(f, T, (T[0] + 280, T[1]), B, r=46, label=f"{x}°")
            angle_mark(f, C, T, B, r=40, label="?", c="coral", f_="coral", at=0)
            q = f"직선 l이 원에 점 A에서 접하고, 현 AB와 직선 l이 이루는 각이 {x}°예요. 호 AB에 대한 원주각 ∠ACB의 크기를 구하세요."
            lines = [L("접선과 현이 이루는 각 = 그 안의 호에 대한 원주각", memo="접선과 현이 이루는 각"), L(f"∠ACB = {x}°")]
            ans, ap = f"{x}°", str(x)
        else:
            angle_mark(f, C, T, B, r=40, label=f"{x}°")
            angle_mark(f, T, (T[0] + 280, T[1]), B, r=46, label="?", c="coral", f_="coral", at=0)
            q = f"직선 l이 원에 점 A에서 접하고, 호 AB에 대한 원주각 ∠ACB = {x}°예요. 현 AB와 접선 l이 이루는 각(호 AB 쪽)의 크기를 구하세요."
            lines = [L("접선과 현이 이루는 각 = 원주각"), L(f"{x}°")]
            ans, ap = f"{x}°", str(x)
        S.add(5, q, ans, "접선과 현이 이루는 각 = 같은 호의 원주각", lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S
