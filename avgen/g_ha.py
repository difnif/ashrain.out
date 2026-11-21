# 고등 ① (공통수학1) — 다항식의 연산 · 항등식 · 복소수 · 이차함수의 최대최소 · 고차 · 연립방정식 · 여러 가지 부등식
import math
from math import gcd
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, Plane, NL
from kit import *

x, y = SYMS["x"], SYMS["y"]

def bat(v):
    from core import _has_batchim
    return _has_batchim(str(v))

def F_(n, d):
    return "{%d/%d}" % (n, d)

def FR(v):
    v = Fr(v)
    if v.denominator == 1:
        return N(v)
    return (MI if v < 0 else "") + F_(abs(v.numerator), v.denominator)

def PS(e, var="x"):
    return sym_poly_str(sp.expand(e), var)

def ss(e):
    """sympy 식 → 무대 글자(간단한 것만)"""
    s = sp.sstr(e)
    return s

def cx(a, b):
    """a + bi 글자"""
    a, b = Fr(a), Fr(b)
    if b == 0:
        return FR(a)
    bs = "" if abs(b) == 1 else FR(abs(b))
    if a == 0:
        return (MI if b < 0 else "") + f"{bs}i"
    return f"{FR(a)} {'+' if b > 0 else MI} {bs}i"


# ══════════ 다항식의 연산 ══════════
def poly_():
    S = Set("poly", "다항식의 연산 — 곱셈 공식의 변형과 식의 값", "다항식의 연산",
            {1: "다항식의 덧셈 · 뺄셈", 2: "세제곱 곱셈 공식", 3: "곱셈 공식의 변형", 4: "다항식의 나눗셈", 5: "식의 값"},
            pp=10,
            tips={1: "주어진 식을 괄호째 대입하고, 동류항끼리 정리해요",
                  2: "(a ± b)^{3} = a^{3} ± 3a^{2}b + 3ab^{2} ± b^{3} · (a ± b)(a^{2} ∓ ab + b^{2}) = a^{3} ± b^{3}",
                  3: "a^{3} + b^{3} = (a + b)^{3} − 3ab(a + b) · a^{2} + b^{2} + c^{2} = (a + b + c)^{2} − 2(ab + bc + ca)",
                  4: "A = BQ + R — 나머지의 차수는 나누는 식보다 낮아요",
                  5: "x = 1 + √{2} → x − 1 = √{2}를 제곱해 x^{2} − 2x − 1 = 0을 만들어 차수를 낮춰요"},
            note="고등 다항식은 중학교 곱셈 공식을 세제곱까지 넓히고, ‘합과 곱으로 바꾸기(대칭식)’를 익히는 단원이에요. 공식을 쓰기 전에 무엇이 a, b인지 먼저 표시하게 해 주세요.")
    R = rng(2101)

    def rpoly(deg):
        cs = [R.randint(-5, 5) for _ in range(deg + 1)]
        cs[0] = R.choice([1, 2, 3, -1, -2])
        return sum(c * x ** (deg - i) for i, c in enumerate(cs))

    def g1():
        A, B = rpoly(2), rpoly(2)
        p, qq = R.randint(1, 3), R.randint(1, 3)
        plus = R.random() < 0.5
        e = sp.expand(p * A + qq * B) if plus else sp.expand(p * A - qq * B)
        sgn = "+" if plus else MI
        if e == 0 or sp.degree(e, x) < 1:
            return
        ex = f"{p if p > 1 else ''}A {sgn} {qq if qq > 1 else ''}B"
        q = f"A = {PS(A)}, B = {PS(B)}일 때, {J(ex, '을', '를')} 계산하세요."
        lines = [L(f"{ex} = {p if p > 1 else ''}({PS(A)}) {sgn} {qq if qq > 1 else ''}({PS(B)})".replace(" 1(", " ("), memo="괄호째 대입"), L(f"{p if p > 1 else ''}({PS(A)}) {sgn} {qq if qq > 1 else ''}({PS(B)}) = {PS(e)}", memo="동류항끼리")]
        S.add(1, q, PS(e), "괄호째 대입하고 동류항끼리", lines, None, omr="ex", ident=True, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        a, b = R.randint(1, 3), R.randint(1, 5)
        sg = R.choice([1, -1])
        if k == 0:
            e0 = f"({lin(a, sg * b)})^{{3}}"
            E = sp.expand((a * x + sg * b) ** 3)
            A_ = f"{a if a > 1 else ''}x"
            mid = f"({A_})^{{3}} {'+' if sg > 0 else MI} 3 × ({A_})^{{2}} × {b} + 3 × {A_} × {b}^{{2}} {'+' if sg > 0 else MI} {b}^{{3}}"
            memo = "(a ± b)^{3} = a^{3} ± 3a^{2}b + 3ab^{2} ± b^{3}"
        elif k == 1:
            e0 = f"({lin(a, sg * b)})({mono(a * a, 'x', 2, first=True)} {MI if sg > 0 else '+'} {a * b}x + {b * b})" if a > 1 else f"(x {'+' if sg > 0 else MI} {b})(x^{{2}} {MI if sg > 0 else '+'} {b}x + {b * b})"
            if a > 1:
                e0 = f"({lin(a, sg * b)})({PS(a * a * x ** 2 - sg * a * b * x + b * b)})"
            E = sp.expand((a * x + sg * b) * (a * a * x ** 2 - sg * a * b * x + b * b))
            A_ = f"{a if a > 1 else ''}x"
            mid = f"({A_})^{{3}} {'+' if sg > 0 else MI} {b}^{{3}}"
            memo = "(a ± b)(a^{2} ∓ ab + b^{2}) = a^{3} ± b^{3}"
        else:
            p, q_, r = R.sample([-4, -3, -2, -1, 1, 2, 3, 4, 5], 3)
            e0 = f"(x {'+' if p > 0 else MI} {abs(p)})(x {'+' if q_ > 0 else MI} {abs(q_)})(x {'+' if r > 0 else MI} {abs(r)})"
            E = sp.expand((x + p) * (x + q_) * (x + r))
            mid = f"x^{{3}} + ({N(p)} + {NP(q_)} + {NP(r)})x^{{2}} + ({N(p)} × {NP(q_)} + {NP(q_)} × {NP(r)} + {NP(r)} × {NP(p)})x + {NP(p)} × {NP(q_)} × {NP(r)}"
            memo = "x^{3} + (a + b + c)x^{2} + (ab + bc + ca)x + abc"
        q = f"{J(e0, '을', '를')} 전개하세요."
        lines = [L(f"{e0} = {mid}", memo=memo), L(f"{mid} = {PS(E)}")]
        S.add(2, q, PS(E), "곱셈 공식에 맞추어 a, b를 정해요", lines, None, omr="ex", ident=True, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        if k == 0:
            s, p = R.randint(1, 6), R.randint(-5, 6)
            if s * s < 4 * p:                  # a, b 가 실수이려면 (a + b)^2 ≥ 4ab
                return
            v = s ** 3 - 3 * p * s
            q = f"a + b = {s}, ab = {N(p)}일 때, a^{{3}} + b^{{3}}의 값을 구하세요."
            lines = [L("a^{3} + b^{3} = (a + b)^{3} − 3ab(a + b)", memo="합과 곱으로"), L(f"{s}^{{3}} − 3 × {NP(p)} × {s} = {v}")]
        elif k == 1:
            s, p = R.randint(1, 6), R.randint(-5, 6)
            if s * s + 4 * p < 0:              # (a + b)^2 = (a − b)^2 + 4ab ≥ 0
                return
            v = s * s * s + 3 * p * s
            q = f"a − b = {s}, ab = {N(p)}일 때, a^{{3}} − b^{{3}}의 값을 구하세요."
            lines = [L("a^{3} − b^{3} = (a − b)^{3} + 3ab(a − b)"), L(f"{s}^{{3}} + 3 × {NP(p)} × {s} = {v}")]
        else:
            s, t = R.randint(-4, 6), R.randint(-6, 6)
            v = s * s - 2 * t
            if v < 0 or s * s < 3 * t:          # 실수 a, b, c: a^2 + b^2 + c^2 ≥ ab + bc + ca
                return
            q = f"a + b + c = {N(s)}, ab + bc + ca = {N(t)}일 때, a^{{2}} + b^{{2}} + c^{{2}}의 값을 구하세요."
            lines = [L("a^{2} + b^{2} + c^{2} = (a + b + c)^{2} − 2(ab + bc + ca)"), L(f"{NP(s)}^{{2}} − 2 × {NP(t)} = {v}")]
        S.add(3, q, N(v), "구하는 식을 합 · 곱(대칭식)으로 바꿔요", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        if k == 0:
            Bq = x - R.choice([-3, -2, -1, 1, 2, 3])
            Q = rpoly(2)
            Rr = R.randint(-9, 9)
        else:
            Bq = x ** 2 + R.randint(-3, 3) * x + R.choice([-2, -1, 1, 2, 3])
            Q = rpoly(1)
            Rr = R.randint(-5, 5) * x + R.randint(-6, 6)
        A = sp.expand(Bq * Q + Rr)
        q_, r_ = sp.div(A, Bq, x)
        assert sp.expand(q_ - Q) == 0 and sp.expand(r_ - Rr) == 0
        q = f"다항식 {J(PS(A), '을', '를')} {RO(PS(Bq))} 나누었을 때의 몫과 나머지를 구하세요."
        lead = sp.LC(A, x) / sp.LC(Bq, x)
        lines = [L(f"{PS(A)} = ({PS(Bq)})({PS(Q)}) + {PS(Rr) if Rr != 0 else 0}".replace("+ −", "− ").replace("+ " + MI, MI + " "), memo="A = BQ + R"), L(f"몫 {PS(Q)}, 나머지 {PS(Rr) if Rr != 0 else 0}", memo="나머지의 차수 < 나누는 식의 차수")]
        S.add(4, q, f"몫 {PS(Q)}, 나머지 {PS(Rr) if Rr != 0 else 0}", "높은 차수부터 몫을 한 항씩 — A = BQ + R", lines, None, ap=f"{plain(PS(Q))}, {plain(PS(Rr)) if Rr != 0 else 0}", omr="ex", ident=True, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            a, b = R.randint(-3, 3), R.choice([2, 3, 5, 6, 7])
            if a == 0:
                return
            # x = a + √b → x^2 − 2ax + a^2 − b = 0
            c1, c0 = -2 * a, a * a - b
            t = R.randint(-5, 5)
            v = (a + sp.sqrt(b)) ** 2 + c1 * (a + sp.sqrt(b)) + t
            v = sp.nsimplify(sp.expand(v))
            q = f"x = {a} + √{{{b}}}일 때, {PS(x ** 2 + c1 * x + t)}의 값을 구하세요." if a > 0 else f"x = {MI}{-a} + √{{{b}}}일 때, {PS(x ** 2 + c1 * x + t)}의 값을 구하세요."
            lines = [L(f"x {MI} {N(a)} = √{{{b}}}" if a > 0 else f"x + {-a} = √{{{b}}}", memo="근호만 남기고 제곱"), L(f"{PS(x ** 2 + c1 * x)} = {N(-c0)}", memo=f"x^{{2}} {'−' if c1 < 0 else '+'} {abs(c1)}x + {a * a} = {b}"), L(f"{PS(x ** 2 + c1 * x + t)} = {N(-c0)} {'+' if t >= 0 else MI} {abs(t)} = {N(-c0 + t)}")]
            assert v == -c0 + t
            S.add(5, q, N(-c0 + t), "x = a + √{b} → (x − a)^{2} = b로 차수 낮추기", lines, None, sub={"x": a + sp.sqrt(b)}, key=q)
        elif k == 1:
            s = R.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6, 7, 8])
            v = s ** 3 - 3 * s
            q = f"x + {{1/x}} = {N(s)}일 때, x^{{3}} + {{1/x^{{3}}}}의 값을 구하세요."
            lines = [L("x^{3} + {1/x^{3}} = (x + {1/x})^{3} − 3(x + {1/x})", memo="x × {1/x} = 1"), L(f"{NP(s)}^{{3}} − 3 × {NP(s)} = {N(v)}")]
            S.add(5, q, N(v), "a^{3} + b^{3} = (a + b)^{3} − 3ab(a + b), ab = 1", lines, None, key=q)
        else:
            s = R.randint(2, 9)
            v = s * s - 2
            q = f"x + {{1/x}} = {s}일 때, x^{{2}} + {{1/x^{{2}}}}와 x^{{3}} + {{1/x^{{3}}}}의 합을 구하세요."
            lines = [L(f"x^{{2}} + {{1/x^{{2}}}} = {s}^{{2}} − 2 = {v}"), L(f"x^{{3}} + {{1/x^{{3}}}} = {s}^{{3}} − 3 × {s} = {s ** 3 - 3 * s}"), L(f"{v} + {s ** 3 - 3 * s} = {v + s ** 3 - 3 * s}")]
            S.add(5, q, N(v + s ** 3 - 3 * s), "합 x + {1/x}와 곱 1로 차례로", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 항등식 ══════════
def ident():
    S = Set("ident", "항등식과 미정계수 — 계수 비교 · 수치 대입", "항등식",
            {1: "계수비교법", 2: "수치대입법", 3: "x − a의 거듭제곱으로 나타내기", 4: "나머지정리와 미정계수", 5: "k에 대한 항등식"},
            pp=10,
            tips={1: "양변을 전개해 같은 차수의 계수끼리 같다고 놓아요",
                  2: "식이 간단해지는 x 값(인수가 0이 되는 값)을 대입해요",
                  3: "x − a = t로 바꾸거나 조립제법을 되풀이해요",
                  4: "f(x)를 x − a로 나눈 나머지는 f(a)",
                  5: "k에 대해 정리 → (k의 계수) = 0, (상수항) = 0"},
            note="항등식은 ‘모든 x에 대해 성립’하므로 계수 비교와 수치 대입 둘 다 쓸 수 있어요. 대입할 값은 인수를 0으로 만드는 값부터 고르게 해 주세요.")
    R = rng(2102)

    def g1():
        p, q_, r = R.randint(-5, 5), R.randint(-5, 5), R.randint(-5, 5)
        if 0 in (p, q_):
            return
        lhs = sp.expand((x + p) * (x + q_))
        a, b = p + q_, p * q_
        q = f"등식 (x {'+' if p > 0 else MI} {abs(p)})(x {'+' if q_ > 0 else MI} {abs(q_)}) = x^{{2}} + ax + b가 x에 대한 항등식일 때, 상수 a, b의 값을 구하세요."
        lines = [L(f"(x {'+' if p > 0 else MI} {abs(p)})(x {'+' if q_ > 0 else MI} {abs(q_)}) = {PS(lhs)}", memo="좌변 전개"), L(f"a = {N(a)}, b = {N(b)}", memo="계수끼리 비교")]
        S.add(1, q, f"a = {N(a)}, b = {N(b)}", "전개해서 같은 차수의 계수끼리", lines, None, ap=f"a={a}, b={b}", omr="ex", ident=True, sub={"a": a, "b": b}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        p, q_ = R.sample([-3, -2, -1, 1, 2, 3], 2)
        a, b = R.randint(-5, 5), R.randint(-5, 5)
        if a == 0 and b == 0:
            return
        rhs = sp.expand(a * (x - p) + b * (x - q_))
        q = f"등식 {PS(rhs)} = a(x {'+' if -p > 0 else MI} {abs(p)}) + b(x {'+' if -q_ > 0 else MI} {abs(q_)})가 x에 대한 항등식일 때, 상수 a, b의 값을 구하세요."
        lines = [L(f"x = {N(q_)} 대입: {N(rhs.subs(x, q_))} = a × ({N(q_ - p)})", memo="b가 붙은 항이 0"), L(f"a = {N(a)}"), L(f"x = {N(p)} 대입: {N(rhs.subs(x, p))} = b × ({N(p - q_)})", memo="a가 붙은 항이 0"), L(f"b = {N(b)}")]
        S.add(2, q, f"a = {N(a)}, b = {N(b)}", "인수를 0으로 만드는 값을 대입", lines, None, ap=f"a={a}, b={b}", omr="ex", sub={"a": a, "b": b}, key=q)
    fill(S, 2, 20, g2)

    def g3():
        c = R.choice([-2, -1, 1, 2, 3])
        a, b, d = R.randint(1, 3), R.randint(-5, 5), R.randint(-6, 6)
        # a(x − c)^2 + b(x − c) + d
        E = sp.expand(a * (x - c) ** 2 + b * (x - c) + d)
        xc = f"(x {'+' if -c > 0 else MI} {abs(c)})"
        q = f"{PS(E)} = a{xc}^{{2}} + b{xc} + d가 x에 대한 항등식일 때, a + b + d의 값을 구하세요."
        lines = [L(f"x = {c} 대입 → d = {N(E.subs(x, c))}", memo="x − c = 0"), L(f"x^{{2}}의 계수 비교 → a = {a}"), L(f"x의 계수 비교 → {N(sp.Poly(E, x).all_coeffs()[1])} = −{2 * c}a + b → b = {N(b)}".replace("−-", "+")), L(f"{a} + {NP(b)} + {NP(d)} = {a + b + d}")]
        lines[2] = L(f"x의 계수 비교 → b = {N(b)}", memo=f"{N(sp.Poly(E, x).all_coeffs()[1])} = {N(-2 * c * a)} + b")
        S.add(3, q, N(a + b + d), "x = c 대입과 계수 비교를 함께", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        a_, b_ = R.randint(-5, 5), R.randint(-6, 6)
        f_ = x ** 3 + a_ * x + b_
        p, q_ = R.sample([-2, -1, 1, 2], 2)
        r1, r2 = f_.subs(x, p), f_.subs(x, q_)
        q = f"다항식 x^{{3}} + ax + b를 x {'+' if -p > 0 else MI} {abs(p)}로 나눈 나머지가 {N(r1)}, x {'+' if -q_ > 0 else MI} {abs(q_)}로 나눈 나머지가 {N(r2)}일 때, 상수 a, b의 값을 구하세요."
        lines = [L(f"f({N(p)}) = {N(p ** 3)} + {N(p)}a + b = {N(r1)}", memo="나머지정리"), L(f"f({N(q_)}) = {N(q_ ** 3)} + {N(q_)}a + b = {N(r2)}"), L(f"a = {N(a_)}, b = {N(b_)}", memo="연립해서")]
        S.add(4, q, f"a = {N(a_)}, b = {N(b_)}", "x − p로 나눈 나머지 = f(p)", lines, None, ap=f"a={a_}, b={b_}", omr="ex", sub={"a": a_, "b": b_}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        p, q_ = R.randint(-5, 5), R.randint(-5, 5)
        if p == 0 and q_ == 0:
            return
        # (k+1)x + (k-1)y - 2k? general: k(x + y - s) + (x - y - t) = 0 for all k → x + y = s, x - y = t
        s, t = p + q_, p - q_
        q = f"등식 k(x + y {'+' if -s > 0 else MI} {abs(s)}) + (x − y {'+' if -t > 0 else MI} {abs(t)}) = 0이 k의 값에 관계없이 항상 성립할 때, x, y의 값을 구하세요."
        lines = [L(f"x + y = {N(s)}, x − y = {N(t)}", memo="k의 계수 = 0, 나머지 = 0"), L(f"2x = {N(s + t)} → x = {N(p)}"), L(f"y = {N(q_)}")]
        S.add(5, q, f"x = {N(p)}, y = {N(q_)}", "k에 대해 정리해 두 부분이 모두 0", lines, None, ap=f"x={p}, y={q_}", omr="ex", sub={"x": p, "y": q_}, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 복소수 ══════════
def cplx():
    S = Set("cplx", "복소수 — i의 계산 · 켤레 · 거듭제곱", "복소수",
            {1: "덧셈 · 뺄셈 · 곱셈", 2: "나눗셈 — 켤레복소수", 3: "복소수의 상등", 4: "i의 거듭제곱", 5: "켤레복소수와 식의 값"},
            pp=10,
            tips={1: "i를 문자처럼 계산하고 i^{2} = −1로 바꿔요",
                  2: "분모의 켤레복소수를 분자 · 분모에 곱해 분모를 실수로",
                  3: "a + bi = c + di ⇔ a = c, b = d (a, b, c, d는 실수)",
                  4: "i, −1, −i, 1이 4개씩 되풀이 — 지수를 4로 나눈 나머지",
                  5: "z = a + bi면 z + z̄ = 2a, zz̄ = a^{2} + b^{2} — 이것으로 z가 근인 이차식을 만들어요"},
            note="복소수 계산은 ‘i를 문자처럼, i^{2}만 −1로’가 전부예요. 나눗셈은 중학교 분모의 유리화와 같은 생각임을 연결해 주세요.")
    R = rng(2103)
    I = sp.I

    def cstr(z):
        z = sp.nsimplify(sp.expand(z))
        a, b = sp.re(z), sp.im(z)
        return cx(Fr(str(a)), Fr(str(b)))

    def g1():
        a, b, c, d = (R.randint(-6, 6) for _ in range(4))
        if b == 0 or d == 0:
            return
        k = S.count(1) % 3
        z1, z2 = a + b * I, c + d * I
        if k == 0:
            op, z = "+", z1 + z2
        elif k == 1:
            op, z = "−", z1 - z2
        else:
            op, z = "×", z1 * z2
        e = f"({cx(a, b)}) {op} ({cx(c, d)})" if op != "×" else f"({cx(a, b)})({cx(c, d)})"
        q = f"{J(e, '을', '를')} 계산하세요."
        if op == "×":
            lines = [L(f"{e} = {N(a * c)} + ({N(a * d)})i + ({N(b * c)})i + ({N(b * d)})i^{{2}}", memo="분배법칙"), L(f"i^{{2}} = −1 → {N(a * c)} − ({N(b * d)}) + ({N(a * d + b * c)})i"), L(cstr(z))]
        else:
            lines = [L(f"실수부: {N(a)} {op} {NP(c)} = {N(a + c if op == '+' else a - c)}"), L(f"허수부: {N(b)} {op} {NP(d)} = {N(b + d if op == '+' else b - d)}"), L(cstr(z))]
        S.add(1, q, cstr(z), "i를 문자처럼 — i^{2} = −1", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        c, d = R.randint(-4, 4), R.randint(-4, 4)
        if d == 0 or c == 0:
            return
        za = R.randint(-4, 4) + R.randint(-4, 4) * I
        num = sp.expand(za * (c + d * I))
        a, b = int(sp.re(num)), int(sp.im(num))
        if b == 0:
            return
        z = sp.expand(num / (c + d * I))
        zz = sp.nsimplify(sp.simplify(z))
        e = f"{{{cx(a, b)}/{cx(c, d)}}}"
        q = f"{J(e, '을', '를')} 계산하세요."
        conj = cx(c, -d)
        n2 = c * c + d * d
        top = sp.expand((a + b * I) * (c - d * I))
        lines = [L(f"분자 · 분모에 {conj} 곱하기", memo="분모의 켤레복소수"), L(f"분모: {NP(c)}^{{2}} + {NP(d)}^{{2}} = {n2}"), L(f"분자: {cstr(top)}"), L(f"{{{cstr(top)}/{n2}}} = {cstr(zz)}")]
        S.add(2, q, cstr(zz), "분모의 켤레복소수를 곱해요", lines, None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        xv, yv = R.randint(-5, 5), R.randint(-5, 5)
        p, q_ = R.randint(1, 3), R.randint(1, 3)
        re_, im_ = p * xv + yv, xv - q_ * yv
        q = f"실수 x, y에 대하여 ({p if p > 1 else ''}x + y) + (x {MI} {q_ if q_ > 1 else ''}y)i = {cx(re_, im_)}일 때, x, y의 값을 구하세요."
        lines = [L(f"{p if p > 1 else ''}x + y = {N(re_)}", memo="실수부끼리"), L(f"x {MI} {q_ if q_ > 1 else ''}y = {N(im_)}", memo="허수부끼리"), L(f"x = {N(xv)}, y = {N(yv)}", memo="연립")]
        S.add(3, q, f"x = {N(xv)}, y = {N(yv)}", "실수부끼리, 허수부끼리 같다고 놓아요", lines, None, ap=f"x={xv}, y={yv}", omr="ex", sub={"x": xv, "y": yv}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        if k == 0:
            n = R.randint(5, 120)
            r = n % 4
            v = ["1", "i", "−1", "−i"][r]
            q = f"i^{{{n}}}의 값을 구하세요."
            lines = [L(f"{n} ÷ 4 = {n // 4} … {r}", memo="i^{4} = 1"), L(f"i^{{{n}}} = i^{{{r}}} = {v}" if r else f"i^{{{n}}} = (i^{{4}})^{{{n // 4}}} = 1")]
            S.add(4, q, v, "지수를 4로 나눈 나머지", lines, None, omr="ex", key=q)
        else:
            n = R.randint(5, 60)
            tot = sum([sp.I ** j for j in range(1, n + 1)])
            tot = sp.nsimplify(sp.expand(tot))
            r = n % 4
            q = f"i + i^{{2}} + i^{{3}} + … + i^{{{n}}}의 값을 구하세요."
            lines = [L("i + i^{2} + i^{3} + i^{4} = i − 1 − i + 1 = 0", memo="4개씩 묶으면 0"), L(f"{n} = 4 × {n // 4} + {r}"), L(f"남는 {r}개: " + (" + ".join(["i", "i^{2}", "i^{3}"][:r]) if r else "없음") + f" = {cstr(tot)}")]
            S.add(4, q, cstr(tot), "4개씩 묶으면 합이 0", lines, None, omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        a, b = R.randint(-4, 4), R.randint(1, 4)
        if a == 0:
            return
        k = S.count(5) % 2
        s, p = 2 * a, a * a + b * b
        if k == 0:
            q = f"z = {cx(a, b)}일 때, z + z̄와 zz̄의 값을 각각 구하세요. (z̄는 z의 켤레복소수)"
            lines = [L(f"z̄ = {cx(a, -b)}"), L(f"z + z̄ = {N(s)}", memo="허수부가 지워져요"), L(f"zz̄ = {NP(a)}^{{2}} + {b}^{{2}} = {p}")]
            S.add(5, q, f"{N(s)}, {p}", "z + z̄ = 2a, zz̄ = a^{2} + b^{2}", lines, None, ap=f"{s}, {p}", omr="ex", key=q)
        else:
            t = R.randint(-5, 5)
            v = t
            q = f"z = {cx(a, b)}일 때, z^{{2}} {'+' if -s > 0 else MI} {abs(s)}z + {p + t}의 값을 구하세요."
            lines = [L(f"z − {NP(a)} = {b}i → (z − {NP(a)})^{{2}} = −{b * b}", memo="허수부만 남기고 제곱"), L(f"z^{{2}} {'+' if -s > 0 else MI} {abs(s)}z + {p} = 0", memo="z가 근인 이차식"), L(f"0 + {t} = {t}" if t >= 0 else f"0 {MI} {-t} = {t}")]
            lines[-1] = L(f"z^{{2}} {'+' if -s > 0 else MI} {abs(s)}z + {p + t} = 0 + {NP(t)} = {N(t)}")
            S.add(5, q, N(t), "z가 근인 이차식으로 차수 낮추기", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 이차함수의 최대 · 최소 ══════════
def qmax():
    S = Set("qmax", "이차함수의 최대 · 최소 — 꼭짓점과 구간의 끝", "최대·최소",
            {1: "최솟값(아래로 볼록)", 2: "최댓값(위로 볼록)", 3: "제한된 범위에서", 4: "최대 · 최소로 미정계수", 5: "최대 · 최소의 활용"},
            pp=8,
            tips={1: "y = a(x − p)^{2} + q (a > 0) → x = p에서 최솟값 q",
                  2: "a < 0이면 x = p에서 최댓값 q",
                  3: "꼭짓점이 범위 안이면 꼭짓점과 양 끝, 밖이면 양 끝만 비교해요",
                  4: "완전제곱식으로 꼭짓점의 y좌표를 문자로 나타내 조건과 같다고 놓아요",
                  5: "구하는 양을 한 문자에 대한 이차식으로 — 변수의 범위를 꼭 확인"},
            note="최대 · 최소는 그래프를 그리면 바로 보이는 문제예요. 범위가 있을 때는 꼭짓점이 범위 안에 있는지를 먼저 판단하게 해 주세요.")
    R = rng(2104)

    def pl_for(f, a, p, q_, lo=None, hi=None, at="q"):
        xr = (p - 5.5, p + 5.5)
        ys = [a * (t - p) ** 2 + q_ for t in (xr[0], xr[1], p)]
        ymin, ymax = min(ys + [0]), max(ys + [0])
        yr = (max(ymin - 1, q_ - 9) if a > 0 else q_ - 9, q_ + 9 if a > 0 else min(ymax + 1, q_ + 9))
        yr = (min(yr[0], -1), max(yr[1], 1))
        pl = Plane(f, (min(xr[0], -1), max(xr[1], 1)), yr, box=(40, 30, 620, 650), square=False)
        pl.axes(at=at, grid=1 if yr[1] - yr[0] < 24 else 2, lab_step=2)
        pl.curve(lambda t: a * (t - p) ** 2 + q_, at=at)
        pl.pt(p, q_, label=f"({N(p)}, {N(q_)})", pos="s" if a > 0 else "n", at=1, f="coral")
        if lo is not None:
            f.rect(pl.X(lo), pl.Y(yr[1]), pl.X(hi) - pl.X(lo), pl.Y(yr[0]) - pl.Y(yr[1]), c="none", f="gold", fo=0.12, at=at)
        return pl

    def vstr(a, p, q_):
        return f"{N(a) if a not in (1, -1) else ('' if a == 1 else MI)}(x {'+' if -p > 0 else MI} {abs(p)})^{{2}}" + (f" {'+' if q_ > 0 else MI} {abs(q_)}" if q_ else "") if p else f"{N(a) if a not in (1, -1) else ('' if a == 1 else MI)}x^{{2}}" + (f" {'+' if q_ > 0 else MI} {abs(q_)}" if q_ else "")

    def g12(st):
        a = R.choice([1, 2, 3]) * (1 if st == 1 else -1)
        p, q_ = R.randint(-4, 4), R.randint(-6, 6)
        E = sp.expand(a * (x - p) ** 2 + q_)
        f = Fig()
        pl_for(f, a, p, q_)
        q = f"이차함수 y = {PS(E)}의 {'최솟값' if st == 1 else '최댓값'}을 구하세요."
        lines = [L(f"{PS(E)} = {vstr(a, p, q_)}", memo="완전제곱식으로"), L(f"꼭짓점 ({N(p)}, {N(q_)}) → {'최솟값' if st == 1 else '최댓값'} {N(q_)}", memo="a > 0 아래로 볼록" if st == 1 else "a < 0 위로 볼록")]
        S.add(st, q, N(q_), "완전제곱식 → 꼭짓점의 y좌표", lines, f.out(), ident=True, key=q)

    fill(S, 1, 20, lambda: g12(1))
    fill(S, 2, 20, lambda: g12(2))

    def g3():
        a = R.choice([1, -1, 2])
        p, q_ = R.randint(-3, 3), R.randint(-5, 5)
        lo = R.randint(p - 4, p + 2)
        hi = lo + R.randint(2, 5)
        E = sp.expand(a * (x - p) ** 2 + q_)
        fn = lambda t: a * (t - p) ** 2 + q_
        cands = [(lo, fn(lo)), (hi, fn(hi))] + ([(p, q_)] if lo <= p <= hi else [])
        mx = max(cands, key=lambda c: c[1])
        mn = min(cands, key=lambda c: c[1])
        f = Fig()
        pl_for(f, a, p, q_, lo, hi)
        q = f"{N(lo)} ≤ x ≤ {N(hi)}에서 이차함수 y = {PS(E)}의 최댓값과 최솟값을 구하세요."
        inside = lo <= p <= hi
        lines = [L(f"y = {vstr(a, p, q_)}", memo="꼭짓점 x = " + N(p)), L(f"꼭짓점 x = {N(p)}{'은' if bat(N(p)) else '는'} 범위 {'안' if inside else '밖'}", memo="꼭짓점 · 양 끝 비교" if inside else "양 끝만 비교"),
                 L(f"x = {N(lo)}: {N(fn(lo))}, x = {N(hi)}: {N(fn(hi))}" + (f", x = {N(p)}: {N(q_)}" if inside else "")), L(f"최댓값 {N(mx[1])}, 최솟값 {N(mn[1])}")]
        S.add(3, q, f"최댓값 {N(mx[1])}, 최솟값 {N(mn[1])}", "꼭짓점이 범위 안인지 먼저", lines, f.out(), ap=f"{mx[1]}, {mn[1]}", omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        p = R.randint(-4, 4)
        m = R.randint(-6, 6)
        a = R.choice([1, 1, 2, -1])
        b = -2 * a * p
        k = m + a * p * p
        q = f"이차함수 y = {PS(a * x ** 2 + b * x)} + k의 {'최솟값' if a > 0 else '최댓값'}이 {N(m)}일 때, 상수 k의 값을 구하세요."
        lines = [L(f"y = {vstr(a, p, 0)} {'+' if -a * p * p >= 0 else MI} {abs(a * p * p)} + k" if p else f"y = {PS(a * x ** 2)} + k", memo="완전제곱식"), L(f"k {'+' if -a * p * p >= 0 else MI} {abs(a * p * p)} = {N(m)}" if p else f"k = {N(m)}", memo="꼭짓점의 y좌표"), L(f"k = {N(k)}")]
        S.add(4, q, N(k), "꼭짓점의 y좌표를 k로 나타내 조건과 같다고", lines, None, sub={"k": k}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        if k == 0:
            P = R.randint(4, 20) * 4
            h = P // 4
            q = f"둘레의 길이가 {P} m인 직사각형 모양의 꽃밭을 만들 때, 넓이의 최댓값을 구하세요."
            q = q.replace(" m", " `m`")
            lines = [L(f"가로 x → 세로 {P // 2} − x", memo=f"0 < x < {P // 2}"), L(f"x({P // 2} − x) = −(x − {h})^{{2}} + {h * h}", pre="넓이"), L(f"가로 {h}일 때 최댓값 {h * h}")]
            S.add(5, q, f"{h * h} `m`²", "넓이를 한 문자에 대한 이차식으로", lines, None, ap=str(h * h), key=q)
        else:
            v = R.randint(1, 6) * 10
            h0 = R.choice([0, 5, 10, 15, 20, 25, 30])
            t0 = Fr(v, 10)
            hmax = h0 + Fr(v * v, 20)
            if hmax.denominator != 1:
                return
            where = "지면에서" if h0 == 0 else f"높이가 {h0} `m`인 건물 옥상에서"
            hs = f"{v}t − 5t^{{2}}" if h0 == 0 else f"{h0} + {v}t − 5t^{{2}}"
            q = f"{where} 똑바로 위로 던진 공의 t초 후의 높이가 ({hs}) `m`일 때, 공이 가장 높이 올라갔을 때의 높이를 구하세요."
            lines = [L(f"{hs} = −5(t − {N(t0)})^{{2}} + {N(hmax)}", memo="완전제곱식"), L(f"{N(t0)}초 뒤 최댓값 {N(hmax)}", memo="꼭짓점")]
            S.add(5, q, f"{N(hmax)} `m`", "높이 식의 꼭짓점", lines, None, ap=N(hmax), ident=True, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 고차방정식 · 연립방정식 ══════════
def eqs():
    S = Set("eqs", "삼차 · 사차방정식과 연립이차방정식", "고차·연립방정식",
            {1: "인수정리로 삼차방정식", 2: "복이차방정식", 3: "삼차방정식의 근과 계수", 4: "연립이차방정식 ①(일차 + 이차)", 5: "연립이차방정식 ②(인수분해되는 식)"},
            pp=10,
            tips={1: "f(a) = 0이 되는 a를 상수항의 약수 중에서 찾고 조립제법으로 인수분해",
                  2: "x^{2} = t로 놓아 t에 대한 이차방정식으로",
                  3: "ax^{3} + bx^{2} + cx + d = 0: α + β + γ = −{b/a}, αβ + βγ + γα = {c/a}, αβγ = −{d/a}",
                  4: "일차식을 한 문자에 대해 풀어 이차식에 대입",
                  5: "인수분해되는 이차식을 일차식 두 개로 나누어 각각 연립"},
            note="고차방정식은 ‘차수를 낮추기(인수분해 · 치환)’가 핵심이에요. 연립이차방정식은 일차식으로 대입하거나 인수분해로 일차식을 만들어 내는 두 가지 길을 정리해 주세요.")
    R = rng(2105)

    def g1():
        rs = R.sample([-3, -2, -1, 1, 2, 3, 4], 3)
        E = sp.expand((x - rs[0]) * (x - rs[1]) * (x - rs[2]))
        r0 = rs[0]
        Q = sp.expand((x - rs[1]) * (x - rs[2]))
        q = f"삼차방정식 {PS(E)} = 0을 푸세요."
        rr = sorted(rs)
        lines = [L(f"f({N(r0)}) = 0", memo="상수항의 약수 중에서 찾기"), L(f"{PS(E)} = (x {'+' if -r0 > 0 else MI} {abs(r0)})({PS(Q)})", memo="조립제법"), L(f"x = {', '.join(map(N, rr))}")]
        S.add(1, q, f"x = {', '.join(map(N, rr))}", "인수정리로 한 근 → 조립제법으로 나머지", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        a, b = R.sample([1, 2, 3, 4, -1, -2, -3], 2)
        # t^2 - (a+b)t + ab = 0, t = x^2
        E = sp.expand((x ** 2 - a) * (x ** 2 - b))
        sols = []
        for t in sorted([a, b]):
            if t > 0:
                r = sp.sqrt(t)
                sols.append(f"±{'√{' + str(t) + '}' if not r.is_integer else str(r)}")
            else:
                r = sp.sqrt(-t)
                sols.append(f"±{'√{' + str(-t) + '}' if not r.is_integer else (str(r) if r != 1 else '')}i")
        q = f"사차방정식 {PS(E)} = 0을 푸세요."
        lines = [L(f"x^{{2}} = t → {PS(sp.expand((x - a) * (x - b))).replace('x', 't')} = 0", memo="치환"), L(f"(t {'+' if -a > 0 else MI} {abs(a)})(t {'+' if -b > 0 else MI} {abs(b)}) = 0 → t = {N(min(a, b))}, {N(max(a, b))}"), L(f"x = {', '.join(sols)}")]
        S.add(2, q, f"x = {', '.join(sols)}", "x^{2} = t로 치환", lines, None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        rs = [R.randint(-3, 4) for _ in range(3)]
        s1 = sum(rs)
        s2 = rs[0] * rs[1] + rs[1] * rs[2] + rs[2] * rs[0]
        s3 = rs[0] * rs[1] * rs[2]
        E = sp.expand((x - rs[0]) * (x - rs[1]) * (x - rs[2]))
        k = S.count(3) % 3
        if k == 0:
            v = s1 * s1 - 2 * s2
            want = "α^{2} + β^{2} + γ^{2}"
            lines = [L(f"α + β + γ = {N(s1)}, αβ + βγ + γα = {N(s2)}", memo="근과 계수의 관계"), L(f"{want} = {NP(s1)}^{{2}} − 2 × {NP(s2)} = {v}")]
        elif k == 1:
            if s3 == 0:
                return
            v = Fr(s2, s3)
            want = "{1/α} + {1/β} + {1/γ}"
            lines = [L(f"αβ + βγ + γα = {N(s2)}, αβγ = {N(s3)}"), L(f"{want} = {{αβ + βγ + γα/αβγ}} = {FR(v)}")]
            v = FR(v)
        else:
            v = (1 - rs[0]) * (1 - rs[1]) * (1 - rs[2])
            want = "(1 − α)(1 − β)(1 − γ)"
            lines = [L(f"f(x) = (x − α)(x − β)(x − γ)", memo="삼차항의 계수 1"), L(f"{want} = f(1) = {N(E.subs(x, 1))}")]
        q = f"삼차방정식 {PS(E)} = 0의 세 근을 α, β, γ라 할 때, {want}의 값을 구하세요."
        S.add(3, q, v if isinstance(v, str) else N(v), "근과 계수의 관계로 합 · 곱을 써요", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        xv, yv = R.randint(-4, 5), R.randint(-4, 5)
        d = xv - yv
        s2 = xv * xv + yv * yv
        # x - y = d, x^2 + y^2 = s2 → other solution
        sol = sp.solve([x - y - d, x ** 2 + y ** 2 - s2], [x, y], dict=True)
        if len(sol) != 2:
            return
        pts = sorted([(int(s[x]), int(s[y])) for s in sol if s[x].is_integer and s[y].is_integer])
        if len(pts) != 2:
            return
        q = f"연립방정식 x − y = {N(d)}, x^{{2}} + y^{{2}} = {s2}를 푸세요." if not bat(s2) else f"연립방정식 x − y = {N(d)}, x^{{2}} + y^{{2}} = {s2}을 푸세요."
        lines = [L(f"x = y {'+' if d >= 0 else MI} {abs(d)}", memo="일차식을 x에 대해"), L(f"(y {'+' if d >= 0 else MI} {abs(d)})^{{2}} + y^{{2}} = {s2}", memo="대입"), L(f"{PS(sp.expand((y + d) ** 2 + y ** 2 - s2), 'y')} = 0"), L("(x, y) = " + ", ".join(f"({N(a)}, {N(b)})" for a, b in pts))]
        S.add(4, q, "(x, y) = " + ", ".join(f"({N(a)}, {N(b)})" for a, b in pts), "일차식을 이차식에 대입", lines, None, ap="; ".join(f"({a}, {b})" for a, b in pts), omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        a, b = R.choice([(1, 4), (1, 9), (2, 8), (3, 12), (1, 16), (4, 16), (2, 18), (1, 25)])
        k = R.randint(1, 3)
        c = b * k * k
        E1 = sp.expand((x - a * y) * (x - b * y))
        r = math.isqrt(b // a) if (b % a == 0) else None
        if r is None or r * r * a != b:
            r = math.isqrt(c // a)
        ya = math.isqrt(c // a)
        if ya * ya * a != c:
            return
        pts = [(a * ya, ya), (-a * ya, -ya), (b * k, k), (-b * k, -k)]
        q = f"연립방정식 {sym_poly2(E1)} = 0, xy = {c}{'을' if bat(c) else '를'} 푸세요."
        fa = "x − y" if a == 1 else f"x − {a}y"
        lines = [L(f"({fa})(x − {b}y) = 0", memo="첫 식을 인수분해"), L(f"x = {a if a > 1 else ''}y → {a if a > 1 else ''}y^{{2}} = {c} → y = ±{ya}", memo="둘째 식에 대입"), L(f"x = {b}y → {b}y^{{2}} = {c} → y = ±{k}"), L("(x, y) = " + ", ".join(f"({N(p)}, {N(q_)})" for p, q_ in pts))]
        S.add(5, q, "(x, y) = " + ", ".join(f"({N(p)}, {N(q_)})" for p, q_ in pts), "인수분해되는 식으로 일차식을 만들어 대입", lines, None, ap="; ".join(f"({p}, {q_})" for p, q_ in pts), omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S

def sym_poly2(e):
    """x, y 두 문자 이차식 글자 — x^{2}, xy, y^{2} 순"""
    P = sp.Poly(sp.expand(e), x, y)
    out = ""
    for (i, j), c in sorted(P.terms(), key=lambda t: (-t[0][0], -t[0][1])):
        c = int(c)
        var = ("x" + (sup(i) if i > 1 else "") if i else "") + ("y" + (sup(j) if j > 1 else "") if j else "")
        body = (str(abs(c)) if (abs(c) != 1 or not var) else "") + var
        if not out:
            out = (MI if c < 0 else "") + body
        else:
            out += f" {MI if c < 0 else '+'} {body}"
    return out


# ══════════ 여러 가지 부등식 ══════════
def ivl(lo, hi, lo_in, hi_in):
    s = ""
    if lo is not None:
        s += f"{FR(lo)} {'≤' if lo_in else '<'} "
    s += "x"
    if hi is not None:
        s += f" {'≤' if hi_in else '<'} {FR(hi)}"
    return s

def ineqs():
    S = Set("ineqs", "여러 가지 부등식 — 연립 · 절댓값 · 이차", "여러 가지 부등식",
            {1: "연립일차부등식", 2: "A < B < C 꼴", 3: "절댓값이 있는 부등식", 4: "이차부등식", 5: "연립이차부등식"},
            mixed=True, pp=8,
            tips={1: "각 부등식의 해를 수직선에 그려 공통부분",
                  2: "A < B < C → A < B와 B < C를 연립",
                  3: "|x − a| < b ⇔ −b < x − a < b · |x − a| > b ⇔ x − a < −b 또는 x − a > b",
                  4: "이차식을 인수분해해 두 근 α < β → (x − α)(x − β) < 0이면 α < x < β, > 0이면 x < α 또는 x > β",
                  5: "각각 풀어 수직선 위에서 공통부분"},
            note="부등식의 해는 반드시 수직선에 그려 공통부분을 확인하게 해 주세요. 이차부등식은 이차함수 그래프가 x축 아래(위)에 있는 x의 범위라는 그림과 연결하면 좋아요.")
    R = rng(2106)

    def nl_sol(f, segs, lo, hi, at=0):
        """segs: [(a, b, a_in, b_in)] (None = 무한)"""
        nl = NL(f, lo, hi, y=420, lab_step=1 if hi - lo <= 14 else 2)
        for i, (a, b, ain, bin_) in enumerate(segs):
            xa = nl.X(a) if a is not None else nl.X(lo) - 10
            xb = nl.X(b) if b is not None else nl.X(hi) + 10
            f.line(xa, 370 - i * 8, xb, 370 - i * 8, c="coral", w=6, at=at, ar=0)
            for v, inc in ((a, ain), (b, bin_)):
                if v is not None:
                    f.circ(nl.X(v), 420, 11, c="coral", sw=4, f="coral" if inc else "paper", fo=1, at=at)
        return nl

    def g1():
        a1, b1 = R.randint(1, 4), R.randint(-8, 8)
        a2, b2 = R.randint(1, 4), R.randint(-8, 8)
        L1 = Fr(R.randint(-5, 3))
        U1 = L1 + R.randint(2, 6)
        # a1 x + b1 > a1*L1 + b1 → x > L1 ; a2 x + b2 ≤ a2*U1 + b2 → x ≤ U1
        c1, c2 = a1 * L1 + b1, a2 * U1 + b2
        q = f"연립부등식 {lin(a1, b1)} > {N(c1)}, {lin(a2, b2)} ≤ {N(c2)}를 푸세요." if not bat(N(c2)) else f"연립부등식 {lin(a1, b1)} > {N(c1)}, {lin(a2, b2)} ≤ {N(c2)}을 푸세요."
        ans = ivl(L1, U1, False, True)
        f = Fig()
        nl_sol(f, [(L1, U1, False, True)], int(L1) - 3, int(U1) + 3, at=2)
        lines = [L(f"x > {N(L1)}", pre="첫째"), L(f"x ≤ {N(U1)}", pre="둘째"), L(ans, memo="공통부분")]
        S.add(1, q, ans, "각각 풀어 수직선에서 공통부분", lines, f.out(), omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        a, b = R.randint(1, 3), R.randint(-6, 6)
        lo, hi = R.randint(-6, 0), R.randint(1, 7)
        A_, C_ = a * lo + b, a * hi + b
        q = f"부등식 {N(A_)} < {lin(a, b)} ≤ {N(C_)}를 푸세요." if not bat(N(C_)) else f"부등식 {N(A_)} < {lin(a, b)} ≤ {N(C_)}을 푸세요."
        lines = [L(f"{N(A_ - b)} < {a if a > 1 else ''}x ≤ {N(C_ - b)}", memo=f"세 변에서 {N(b)}{'을' if bat(N(b)) else '를'} 빼요"), L(ivl(lo, hi, False, True), memo=f"세 변을 {RO(a)} 나눠요" if a > 1 else None)]
        ans = ivl(lo, hi, False, True)
        f = Fig()
        nl_sol(f, [(lo, hi, False, True)], lo - 3, hi + 3, at=1)
        S.add(2, q, ans, "세 변에 같은 계산을 해요", lines, f.out(), omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        a, b = R.randint(-5, 5), R.randint(1, 6)
        f = Fig()
        if k == 0:
            q = f"부등식 |x {'+' if -a > 0 else MI} {abs(a)}| < {b}를 푸세요." if not bat(b) else f"부등식 |x {'+' if -a > 0 else MI} {abs(a)}| < {b}을 푸세요."
            if a == 0:
                q = f"부등식 |x| < {b}{'을' if bat(b) else '를'} 푸세요."
            lines = [L(f"{MI}{b} < x {'+' if -a > 0 else MI} {abs(a)} < {b}" if a else f"{MI}{b} < x < {b}", memo="|A| < b ⇔ −b < A < b"), L(ivl(a - b, a + b, False, False))]
            ans = ivl(a - b, a + b, False, False)
            nl_sol(f, [(a - b, a + b, False, False)], a - b - 3, a + b + 3, at=1)
        else:
            q = f"부등식 |x {'+' if -a > 0 else MI} {abs(a)}| ≥ {b}를 푸세요." if not bat(b) else f"부등식 |x {'+' if -a > 0 else MI} {abs(a)}| ≥ {b}을 푸세요."
            if a == 0:
                q = f"부등식 |x| ≥ {b}{'을' if bat(b) else '를'} 푸세요."
            ans = f"x ≤ {N(a - b)} 또는 x ≥ {N(a + b)}"
            lines = [L(f"x {'+' if -a > 0 else MI} {abs(a)} ≤ {MI}{b} 또는 x {'+' if -a > 0 else MI} {abs(a)} ≥ {b}" if a else f"x ≤ {MI}{b} 또는 x ≥ {b}", memo="|A| ≥ b ⇔ A ≤ −b 또는 A ≥ b"), L(ans)]
            nl_sol(f, [(None, a - b, False, True), (a + b, None, True, False)], a - b - 3, a + b + 3, at=1)
        S.add(3, q, ans, "절댓값 기호를 범위로 풀어요", lines, f.out(), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        r1, r2 = sorted(R.sample(range(-5, 6), 2))
        a = R.choice([1, 1, 2])
        E = sp.expand(a * (x - r1) * (x - r2))
        op = R.choice(["<", ">", "≤", "≥"])
        f = Fig()
        if op in ("<", "≤"):
            ans = ivl(r1, r2, op == "≤", op == "≤")
            nl_sol(f, [(r1, r2, op == "≤", op == "≤")], r1 - 3, r2 + 3, at=1)
        else:
            inc = op == "≥"
            ans = f"x {'≤' if inc else '<'} {N(r1)} 또는 x {'≥' if inc else '>'} {N(r2)}"
            nl_sol(f, [(None, r1, False, inc), (r2, None, inc, False)], r1 - 3, r2 + 3, at=1)
        q = f"이차부등식 {PS(E)} {op} 0을 푸세요."
        fac = (f"{a}" if a > 1 else "") + f"(x {'+' if -r1 > 0 else MI} {abs(r1)})(x {'+' if -r2 > 0 else MI} {abs(r2)})".replace("(x + 0)", "x").replace("(x − 0)", "x")
        lines = [L(f"{fac} {op} 0", memo="인수분해"), L(f"두 근 {N(r1)}, {N(r2)} → {'사이' if op in ('<', '≤') else '바깥'}", memo="그래프가 x축 " + ("아래" if op in ("<", "≤") else "위")), L(ans)]
        S.add(4, q, ans, "두 근 사이(< 0) · 바깥(> 0)", lines, f.out(), omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        r1, r2 = sorted(R.sample(range(-4, 6), 2))
        s1, s2 = sorted(R.sample(range(-4, 6), 2))
        E1 = sp.expand((x - r1) * (x - r2))
        E2 = sp.expand((x - s1) * (x - s2))
        # E1 ≤ 0 : [r1, r2] ; E2 > 0 : (-inf, s1) ∪ (s2, inf)
        segs = []
        lo_, hi_ = r1, r2
        parts = []
        if lo_ < s1:
            parts.append((lo_, min(hi_, s1), True, hi_ < s1))
        if hi_ > s2:
            parts.append((max(lo_, s2), hi_, lo_ > s2, True))
        parts = [(a, b, ai, bi) for a, b, ai, bi in parts if a < b or (a == b and ai and bi)]
        if not parts or len(parts) > 1:
            return
        a, b, ai, bi = parts[0]
        if a == b:
            return
        for t2 in range(4 * (min(r1, s1) - 2), 4 * (max(r2, s2) + 2) + 1):
            tv = Fr(t2, 4)
            truth = (tv - r1) * (tv - r2) <= 0 and (tv - s1) * (tv - s2) > 0
            inside = (a < tv or (ai and tv == a)) and (tv < b or (bi and tv == b))
            assert truth == inside, (r1, r2, s1, s2, a, b, tv)
        ans = ivl(a, b, ai, bi)
        q = f"연립부등식 {PS(E1)} ≤ 0, {PS(E2)} > 0을 푸세요."
        f = Fig()
        lo_v, hi_v = min(r1, s1) - 2, max(r2, s2) + 2
        nl = NL(f, lo_v, hi_v, y=420, lab_step=1)
        f.line(nl.X(r1), 330, nl.X(r2), 330, c="teal", w=5)
        f.line(nl.X(lo_v) - 10, 360, nl.X(s1), 360, c="gold", w=5)
        f.line(nl.X(s2), 360, nl.X(hi_v) + 10, 360, c="gold", w=5)
        f.line(nl.X(a), 300, nl.X(b), 300, c="coral", w=7, at=2)
        lines = [L(f"{r1 if r1 >= 0 else N(r1)} ≤ x ≤ {N(r2)}", pre="첫째", memo="두 근 사이"), L(f"x < {N(s1)} 또는 x > {N(s2)}", pre="둘째", memo="두 근 바깥"), L(ans, memo="공통부분")]
        S.add(5, q, ans, "각각 풀어 수직선 위 공통부분", lines, f.out(), omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S

