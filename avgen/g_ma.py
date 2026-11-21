# 중등 ① — 소인수분해 · 문자와 식 · 좌표평면 · 정비례와 반비례 · 각과 평행선 · 다각형
import math
from math import gcd
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, Plane, ang_pt, angle_mark, dir_deg, NL
from kit import *

def bat(x):
    from core import _has_batchim
    return _has_batchim(str(x))

def F_(n, d):
    return "{%d/%d}" % (n, d)

def pf(n):
    out, p = {}, 2
    while n > 1:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p += 1
    return out

def pfs(fac):
    """{2: 2, 3: 1} → '2^{2} × 3'"""
    return " × ".join(f"{p}" + (sup(e) if e > 1 else "") for p, e in sorted(fac.items()))

def lad1(f, n, at0="q"):
    """한 수를 소수로 나누는 사다리 — 줄 i 가 판서 i 번째에"""
    ps = []
    m = n
    p = 2
    while m > 1:
        while m % p == 0:
            ps.append(p)
            m //= p
        p += 1
    x, y0, rh = 360, 120, min(70, 470 / (len(ps) + 1))
    f.text(x, y0, str(n), z=40, at=at0)
    m = n
    for i, p in enumerate(ps):
        y = y0 + rh * i
        f.text(x - 90, y, str(p), z=40, a="e", c="coral", b=700, at=0, dl=i * 250)
        f.poly([(x - 74, y - 38), (x - 66, y - 16), (x - 66, y + 4), (x - 72, y + 14)], z=False, c="ink", w=3, at=0, dl=i * 250)
        f.line(x - 74, y + 14, x + 90, y + 14, c="ink", w=3, at=0, dl=i * 250)
        m //= p
        f.text(x, y + rh, str(m), z=40, at=0, dl=i * 250 + 150)
    return ps


# ══════════ 소인수분해 ══════════
def prime():
    S = Set("prime", "소인수분해 — 거듭제곱으로 정리하기", "소인수분해",
            {1: "소인수분해하기", 2: "제곱인 수 만들기", 3: "약수의 개수", 4: "최대공약수", 5: "최소공배수와 활용"},
            pp=10,
            tips={1: "작은 소수부터 차례로 나누고, 같은 소수는 거듭제곱으로 — 180 = 2^{2} × 3^{2} × 5",
                  2: "제곱인 수는 소인수의 지수가 모두 짝수. 지수가 홀수인 소인수를 하나 더 곱해요",
                  3: "a^{m} × b^{n}의 약수의 개수 = (m + 1) × (n + 1)",
                  4: "공통인 소인수를 모두 곱하되, 지수는 작은 쪽",
                  5: "모든 소인수를 곱하되, 지수는 큰 쪽. 두 수의 곱 = 최대공약수 × 최소공배수"},
            note="소인수분해는 사다리 나눗셈으로 시작해 거듭제곱 표기로 정리하게 해 주세요. 최대공약수 · 최소공배수는 소인수의 지수를 ‘작은 쪽 · 큰 쪽’으로 고르는 것으로 정리하면 초등의 공약수 사다리와 이어져요.")
    R = rng(1201)

    def rnd_num(lo, hi, maxp=3):
        for _ in range(200):
            fac = {}
            for p in R.sample([2, 3, 5, 7, 11], R.randint(2, maxp)):
                fac[p] = R.randint(1, 4 if p == 2 else (3 if p == 3 else 2))
            n = 1
            for p, e in fac.items():
                n *= p ** e
            if lo <= n <= hi:
                return n, fac
        return None, None

    def g1():
        n, fac = rnd_num(24, 600)
        if not n or max(fac.values()) < 2:
            return
        f = Fig()
        ps = lad1(f, n)
        lines = [L(f"{n} = {' × '.join(map(str, ps))}", memo="작은 소수부터 나누기"), L(f"{n} = {pfs(fac)}", memo="같은 소수는 거듭제곱으로")]
        S.add(1, f"{n}을 소인수분해하세요." if bat(n) else f"{n}를 소인수분해하세요.", pfs(fac), "작은 소수부터 차례로 나누어 — 거듭제곱으로 정리", lines, f.out(), omr="ex", key=f"f{n}")
    fill(S, 1, 20, g1)

    def g2():
        n, fac = rnd_num(20, 800)
        if not n:
            return
        odd = [p for p, e in fac.items() if e % 2]
        if not odd or len(odd) > 2:
            return
        m = 1
        for p in odd:
            m *= p
        k = S.count(2) % 2
        if k == 0:
            q = f"{n}에 가장 작은 자연수를 곱하여 어떤 자연수의 제곱이 되게 하려고 해요. 곱해야 하는 자연수는 무엇인가요?"
            lines = [L(f"{n} = {pfs(fac)}", memo="소인수분해"), L(f"지수가 홀수인 소인수: {', '.join(map(str, odd))}", memo="제곱수는 지수가 모두 짝수"), L(f"{' × '.join(map(str, odd))} = {m}" if len(odd) > 1 else f"{m}")]
            plan = "지수가 홀수인 소인수를 하나씩 더 곱해요"
        else:
            q = f"{n}을 가장 작은 자연수로 나누어 어떤 자연수의 제곱이 되게 하려고 해요. 나누어야 하는 자연수는 무엇인가요?" if bat(n) else f"{n}를 가장 작은 자연수로 나누어 어떤 자연수의 제곱이 되게 하려고 해요. 나누어야 하는 자연수는 무엇인가요?"
            lines = [L(f"{n} = {pfs(fac)}", memo="소인수분해"), L(f"지수가 홀수인 소인수: {', '.join(map(str, odd))}", memo="하나씩 덜어 내면 지수가 짝수"), L(f"{' × '.join(map(str, odd))} = {m}" if len(odd) > 1 else f"{m}")]
            plan = "지수가 홀수인 소인수로 나누어 지수를 짝수로"
        if m == n:
            return
        S.add(2, q, str(m), plan, lines, None, key=f"{k}{n}")
    fill(S, 2, 20, g2)

    def g3():
        n, fac = rnd_num(30, 2000, 3)
        if not n:
            return
        es = [e for _, e in sorted(fac.items())]
        cnt = 1
        for e in es:
            cnt *= e + 1
        k = S.count(3) % 2
        if k == 0:
            q = f"{n}의 약수는 모두 몇 개인가요?"
            lines = [L(f"{n} = {pfs(fac)}", memo="소인수분해"), L(" × ".join(f"({e} + 1)" for e in es) + f" = {cnt}", memo="지수에 1씩 더해 곱해요"), L(f"{cnt}개")]
        else:
            q = f"{pfs(fac)}의 약수는 모두 몇 개인가요?"
            lines = [L(" × ".join(f"({e} + 1)" for e in es) + f" = {cnt}", memo="각 소인수를 0번부터 지수 번까지 고르는 방법"), L(f"{cnt}개")]
        S.add(3, q, f"{cnt}개", "약수의 개수 = (지수 + 1)끼리의 곱", lines, None, ap=str(cnt), key=q)
    fill(S, 3, 20, g3)

    def two():
        for _ in range(100):
            base = {p: R.randint(1, 3) for p in R.sample([2, 3, 5, 7], R.randint(1, 2))}
            fa, fb = dict(base), dict(base)
            for p in base:
                if R.random() < 0.6:
                    fb[p] = R.randint(1, 4)
            pa, pb = R.choice([3, 5, 7, 11]), R.choice([3, 5, 7, 11, 13])
            if pa not in fa and R.random() < 0.6:
                fa[pa] = R.randint(1, 2)
            if pb not in fb and pb != pa and R.random() < 0.6:
                fb[pb] = R.randint(1, 2)
            a = math.prod(p ** e for p, e in fa.items())
            b = math.prod(p ** e for p, e in fb.items())
            if a != b and a < 3000 and b < 3000:
                return fa, fb, a, b
        return None

    def g4():
        t = two()
        if not t:
            return
        fa, fb, a, b = t
        common = {p: min(fa[p], fb[p]) for p in fa if p in fb}
        g = math.prod(p ** e for p, e in common.items())
        if g == 1:
            return
        if S.count(4) % 2:
            q = f"두 수 {pfs(fa)}, {pfs(fb)}의 최대공약수를 소인수의 곱으로 나타내세요."
            lines = [L(f"공통인 소인수: {', '.join(map(str, sorted(common)))}", memo="둘 다 있는 소인수만"), L(f"{pfs(common)}", memo="지수는 작은 쪽")]
            S.add(4, q, pfs(common), "공통인 소인수 — 지수는 작은 쪽", lines, None, omr="ex", key=q)
        else:
            q = f"{wa(a)} {b}의 최대공약수를 구하세요."
            lines = [L(f"{a} = {pfs(fa)}"), L(f"{b} = {pfs(fb)}"), L(f"{pfs(common)} = {g}", pre="최대공약수", memo="공통 소인수, 작은 지수")]
            S.add(4, q, str(g), "소인수분해하고 — 공통인 소인수, 지수는 작은 쪽", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        t = two()
        if not t:
            return
        fa, fb, a, b = t
        allp = {p: max(fa.get(p, 0), fb.get(p, 0)) for p in set(fa) | set(fb)}
        l = math.prod(p ** e for p, e in allp.items())
        common = {p: min(fa[p], fb[p]) for p in fa if p in fb}
        g = math.prod(p ** e for p, e in common.items())
        if k == 0:
            q = f"두 수 {pfs(fa)}, {pfs(fb)}의 최소공배수를 소인수의 곱으로 나타내세요."
            lines = [L(f"모든 소인수: {', '.join(map(str, sorted(allp)))}", memo="한쪽에만 있어도"), L(f"{pfs(allp)}", memo="지수는 큰 쪽")]
            S.add(5, q, pfs(allp), "모든 소인수 — 지수는 큰 쪽", lines, None, omr="ex", key=q)
        elif k == 1:
            if l > 20000:
                return
            q = f"{wa(a)} {b}의 최소공배수를 구하세요."
            lines = [L(f"{a} = {pfs(fa)}"), L(f"{b} = {pfs(fb)}"), L(f"{pfs(allp)} = {l}", pre="최소공배수", memo="모든 소인수, 큰 지수")]
            S.add(5, q, str(l), "소인수분해하고 — 모든 소인수, 지수는 큰 쪽", lines, None, key=q)
        else:
            if l > 5000:
                return
            q = f"두 자연수의 곱이 {a * b}이고 최대공약수가 {g}일 때, 최소공배수는 얼마인가요?"
            lines = [L("두 수의 곱 = 최대공약수 × 최소공배수", memo="A = Ga, B = Gb → AB = G × Gab"), L(f"{a * b} ÷ {g} = {l}"), L(f"{l}")]
            S.add(5, q, str(l), "두 수의 곱 = 최대공약수 × 최소공배수", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 문자와 식 ══════════
def expr():
    S = Set("expr", "문자와 식 — 식의 값과 일차식의 계산", "문자와 식",
            {1: "곱셈 · 나눗셈 기호 생략", 2: "식의 값", 3: "일차식과 수의 곱셈 · 나눗셈", 4: "동류항 정리", 5: "괄호가 있는 일차식의 덧셈 · 뺄셈"},
            mixed=True, pp=10,
            tips={1: "수는 문자 앞에, 문자는 알파벳 순으로. 1은 생략하고 나눗셈은 분수로 — x ÷ 5 = {x/5}",
                  2: "음수를 대입할 때는 반드시 괄호를 씌워요 — x = −2이면 x^{2} = (−2)^{2} = 4",
                  3: "분배법칙 — 3(2x − 5) = 6x − 15. 나눗셈은 역수의 곱셈으로",
                  4: "문자와 차수가 같은 항(동류항)끼리 계수를 더해요",
                  5: "괄호 앞이 −이면 괄호 안의 부호가 모두 바뀌어요"},
            note="식의 값에서 음수 대입 실수가 가장 많아요. 대입하기 전에 문자 자리에 빈 괄호를 먼저 쓰게 하고, 일차식 계산은 ‘분배 → 동류항 모으기’ 두 단계로 나누어 쓰게 해 주세요.")
    R = rng(1202)

    def g1():
        k = S.count(1) % 4
        a, b = R.randint(2, 9), R.randint(2, 9)
        v1, v2 = R.sample(list("abxy"), 2)
        v1, v2 = sorted([v1, v2])
        if k == 0:
            q = f"{v2} × {a} × {v1}에서 곱셈 기호를 생략하여 나타내세요."
            ans = f"{a}{v1}{v2}"
            lines = [L("수를 앞에, 문자는 알파벳 순으로"), L(f"{v2} × {a} × {v1} = {ans}")]
        elif k == 1:
            q = f"{v1} ÷ {a}에서 나눗셈 기호를 생략하여 나타내세요."
            ans = f"{{{v1}/{a}}}"
            lines = [L("나눗셈은 분수로", memo="÷ a = × {1/a}"), L(f"{v1} ÷ {a} = {ans}")]
        elif k == 2:
            q = f"({v1} + {v2}) × ({MI}{a})에서 곱셈 기호를 생략하여 나타내세요."
            ans = f"{MI}{a}({v1} + {v2})"
            lines = [L("괄호 묶음도 하나의 문자처럼 — 수를 앞에"), L(f"({v1} + {v2}) × ({MI}{a}) = {ans}")]
        else:
            q = f"{v1} × {v1} × {a} ÷ {v2}에서 곱셈 · 나눗셈 기호를 생략하여 나타내세요."
            ans = f"{{{a}{v1}^{{2}}/{v2}}}"
            lines = [L(f"{v1} × {v1} = {v1}^{{2}}", memo="같은 문자의 곱은 거듭제곱"), L(f"÷ {v2} → 분모로"), L(f"{v1} × {v1} × {a} ÷ {v2} = {ans}")]
        S.add(1, q, ans, "수는 앞, 문자는 알파벳 순, 나눗셈은 분수로", lines, None, omr="ex", ident=True, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        x = R.choice([-5, -4, -3, -2, -1, 2, 3, 4])
        if k == 0:
            a, b, c = R.randint(1, 5), R.randint(-6, 6), R.randint(-9, 9)
            if b == 0:
                return
            e = poly([a, b, c])
            v = a * x * x + b * x + c
            sub_ = f"{a if a != 1 else ''}{' × ' if a != 1 else ''}{NP(x)}^{{2}}" + (f" + {b} × {NP(x)}" if b > 0 else f" {MI} {-b} × {NP(x)}") + (f" + {c}" if c > 0 else (f" {MI} {-c}" if c < 0 else ""))
            sub_ = sub_.replace(f" + 1 × {NP(x)}", f" + {NP(x)}").replace(f" {MI} 1 × {NP(x)}", f" {MI} {NP(x)}")
            q = f"x = {N(x)}일 때, {e}의 값을 구하세요."
            lines = [L(f"{sub_}", memo="음수는 괄호를 씌워 대입"), L(f"{sub_} = {v}")]
            S.add(2, q, N(v), "x 자리에 괄호를 쓰고 대입", lines, None, sub={"x": x}, key=q)
        elif k == 1:
            y = R.choice([-3, -2, -1, 2, 3, 5])
            a, b = R.randint(2, 6), R.randint(2, 6)
            v = a * x - b * y
            q = f"x = {N(x)}, y = {N(y)}일 때, {a}x {MI} {b}y의 값을 구하세요."
            lines = [L(f"{a} × {NP(x)} {MI} {b} × {NP(y)}", memo="두 문자 모두 괄호로"), L(f"{a} × {NP(x)} {MI} {b} × {NP(y)} = {v}")]
            S.add(2, q, N(v), "문자마다 괄호를 씌워 대입", lines, None, key=q)
        else:
            a = R.choice([2, 3, 4, 6, 12])
            x = Fr(1, R.choice([2, 3, 4]))
            if R.random() < 0.5:
                x = -x
            v = Fr(a) / x
            if v.denominator != 1:
                return
            q = f"x = {N(x)}일 때, {{{a}/x}}의 값을 구하세요."
            lines = [L(f"{{{a}/x}} = {a} ÷ x", memo="분모의 분수는 나눗셈으로"), L(f"{a} ÷ ({N(x)}) = {a} × ({N(1 / x)})", memo="역수의 곱"), L(f"{a} × ({N(1 / x)}) = {N(v)}")]
            S.add(2, q, N(v), "분모에 분수를 대입할 땐 나눗셈으로 바꿔요", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        a, b = R.randint(2, 9) * R.choice([1, -1]), R.randint(1, 9) * R.choice([1, -1])
        c = R.randint(2, 6) * R.choice([1, -1])
        if k == 0:
            ex_ = f"{c}({lin(a, b)})" if c > 0 else f"({N(c)})({lin(a, b)})"
            q = f"{J(ex_, '을', '를')} 계산하세요."
            ans = lin(a * c, b * c)
            lines = [L(f"{c if c > 0 else NP(c)}({lin(a, b)}) = {c if c > 0 else NP(c)} × {NP(a)}x + {c if c > 0 else NP(c)} × {NP(b)}", memo="분배법칙 — 괄호 안 항마다"), L(f"{c if c > 0 else NP(c)} × {NP(a)}x + {c if c > 0 else NP(c)} × {NP(b)} = {ans}")]
        elif k == 1:
            d = R.randint(2, 6)
            A, B = a * d, b * d
            q = f"({lin(A, B)}) ÷ {eul(d)} 계산하세요."
            ans = lin(a, b)
            lines = [L(f"({lin(A, B)}) ÷ {d} = ({lin(A, B)}) × {{1/{d}}}", memo="역수의 곱셈으로"), L(f"({lin(A, B)}) × {{1/{d}}} = {ans}")]
        else:
            p, qd = R.randint(1, 4), R.randint(2, 5)
            if gcd(p, qd) != 1:
                return
            A, B = a * p, b * p
            fr = Fr(-p, qd) if R.random() < 0.5 else Fr(p, qd)
            res_a, res_b = Fr(A) / fr, Fr(B) / fr
            if res_a.denominator != 1 or res_b.denominator != 1:
                A, B = a * p * qd, b * p * qd
                res_a, res_b = Fr(A) / fr, Fr(B) / fr
            q = f"({lin(A, B)}) ÷ ({N(fr)})를 계산하세요." if not bat(N(fr)) else f"({lin(A, B)}) ÷ ({N(fr)})을 계산하세요."
            inv = 1 / fr
            ans = lin(res_a, res_b)
            lines = [L(f"({lin(A, B)}) ÷ ({N(fr)}) = ({lin(A, B)}) × ({N(inv)})", memo="나누는 수의 역수를 곱해요"), L(f"({lin(A, B)}) × ({N(inv)}) = {ans}")]
        S.add(3, q, ans, "분배법칙 — 나눗셈은 역수의 곱셈으로", lines, None, omr="ex", ident=True, key=q)
    fill(S, 3, 20, g3)

    def g4():
        terms = []
        for _ in range(R.randint(3, 4)):
            if R.random() < 0.55:
                terms.append((R.randint(1, 9) * R.choice([1, -1]), "x"))
            else:
                terms.append((R.randint(1, 12) * R.choice([1, -1]), ""))
        xs = [c for c, v in terms if v]
        cs = [c for c, v in terms if not v]
        if len(xs) < 2 or len(cs) < 1:
            return
        A, B = sum(xs), sum(cs)
        if A == 0:
            return
        e = ""
        for c, v in terms:
            e += mono(c, "x" if v else "", 1, first=(e == ""))
        ans = lin(A, B)
        q = f"{J(e, '을', '를')} 간단히 하세요."
        xpart = "".join(mono(c, "x", 1, first=(i == 0)) for i, c in enumerate(xs))
        cpart = "".join(mono(c, "", 1, first=(i == 0)) for i, c in enumerate(cs))
        lines = [L(f"{e} = ({xpart}) + ({cpart})", memo="동류항끼리 모으기"), L(f"({xpart}) + ({cpart}) = {ans}", memo="계수끼리 더해요")]
        S.add(4, q, ans, "x항끼리, 상수항끼리 모아요", lines, None, omr="ex", ident=True, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        if k == 0:
            p, q_ = R.randint(2, 5), R.randint(2, 5) * R.choice([1, -1])
            a, b, c, d = R.randint(1, 5), R.randint(-6, 6), R.randint(1, 5) * R.choice([1, -1]), R.randint(-6, 6)
            if b == 0 or d == 0:
                return
            A, B = p * a + q_ * c, p * b + q_ * d
            if A == 0:
                return
            op = "+" if q_ > 0 else MI
            e = f"{p}({lin(a, b)}) {op} {abs(q_)}({lin(c, d)})"
            mid = lin(p * a, p * b) + (" + " if q_ > 0 else f" {MI} ") + f"{abs(q_)}({lin(c, d)})"
            exp2 = lin(p * a, p * b) + "".join([mono(q_ * c, "x", 1), mono(q_ * d, "", 1)])
            ans = lin(A, B)
            q = f"{J(e, '을', '를')} 간단히 하세요."
            lines = [L(f"{e} = {exp2}", memo="괄호를 풀어요 — 앞이 −면 부호가 모두 바뀌어요" if q_ < 0 else "분배법칙으로 괄호를 풀어요"), L(f"{exp2} = {ans}", memo="동류항끼리")]
            S.add(5, q, ans, "분배법칙으로 괄호를 풀고 동류항끼리", lines, None, omr="ex", ident=True, key=q)
        else:
            d1, d2 = R.sample([2, 3, 4, 5, 6], 2)
            a, b, c, d = R.randint(1, 5), R.randint(-5, 5), R.randint(1, 5), R.randint(-5, 5)
            if b == 0 or d == 0:
                return
            l = d1 * d2 // gcd(d1, d2)
            m1, m2 = l // d1, l // d2
            op = R.choice(["+", MI])
            sg = 1 if op == "+" else -1
            A, B = a * m1 + sg * c * m2, b * m1 + sg * d * m2
            if A == 0:
                return
            e = f"{{{lin(a, b)}/{d1}}} {op} {{{lin(c, d)}/{d2}}}"
            mid = f"{{{m1}({lin(a, b)}) {op} {m2}({lin(c, d)})/{l}}}"
            ans_num = lin(A, B)
            g_ = gcd(gcd(abs(A), abs(B)), l)
            ans = f"{{{ans_num}/{l}}}" if g_ == 1 else f"{{{lin(A // g_, B // g_)}/{l // g_}}}"
            if l // g_ == 1:
                ans = lin(A // g_, B // g_)
            q = f"{J(e, '을', '를')} 간단히 하세요."
            lines = [L(f"{e} = {mid}", memo=f"분모를 {RO(l)} 통분"), L(f"{mid} = {{{ans_num}/{l}}}", memo="분자의 괄호를 풀어 동류항끼리")] + ([L(f"{{{ans_num}/{l}}} = {ans}", memo="약분")] if g_ > 1 else [])
            S.add(5, q, ans, "통분한 뒤 분자의 괄호를 풀어요", lines, None, omr="ex", ident=True, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 좌표평면 ══════════
QN = {1: "제1사분면", 2: "제2사분면", 3: "제3사분면", 4: "제4사분면"}

def quad(x, y):
    if x > 0 and y > 0:
        return 1
    if x < 0 and y > 0:
        return 2
    if x < 0 and y < 0:
        return 3
    if x > 0 and y < 0:
        return 4
    return 0

def P_(x, y):
    return f"({N(x)}, {N(y)})"

def coord():
    S = Set("coord", "좌표평면 — 사분면 · 대칭인 점 · 넓이", "좌표평면",
            {1: "점의 좌표와 사분면", 2: "부호로 사분면 찾기", 3: "대칭인 점", 4: "세 점으로 만든 삼각형의 넓이", 5: "네 점으로 만든 사각형의 넓이"},
            pp=8,
            tips={1: "(x좌표, y좌표) — 제1사분면 (+, +) · 제2 (−, +) · 제3 (−, −) · 제4 (+, −). 축 위의 점은 어느 사분면에도 속하지 않아요",
                  2: "부호만 따지면 돼요 — a < 0이면 −a > 0",
                  3: "x축 대칭: y 부호만 · y축 대칭: x 부호만 · 원점 대칭: 둘 다 바꿔요",
                  4: "축과 평행한 변을 밑변으로 — 밑변과 높이를 좌표의 차로",
                  5: "둘러싼 직사각형에서 바깥 삼각형들을 빼거나, 두 삼각형으로 나누어요"},
            note="좌표는 ‘가로 먼저, 세로 나중’. 사분면은 부호 표(+ +, − +, − −, + −)를 손으로 그려 보게 하고, 넓이는 축에 평행한 변을 먼저 찾게 해 주세요.")
    R = rng(1203)

    def plane(f, lim=6):
        pl = Plane(f, (-lim - 0.5, lim + 0.5), (-lim - 0.5, lim + 0.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=lim // 3 if lim > 6 else 2)
        return pl

    def g1():
        x, y = R.randint(-6, 6), R.randint(-6, 6)
        if x == 0 or y == 0:
            if R.random() < 0.8:
                return
        f = Fig()
        pl = plane(f)
        pl.pt(x, y, label=P_(x, y), pos="ne" if x >= 0 else "nw", at="q", f="gold")
        Q = quad(x, y)
        q = f"점 {P_(x, y)}{'은' if bat(N(y) + ')') else '는'} 어느 사분면 위의 점인가요?"
        if Q:
            lines = [L(f"x좌표 {N(x)} → {'+' if x > 0 else MI}", memo="부호만 봐요"), L(f"y좌표 {N(y)} → {'+' if y > 0 else MI}"), L(QN[Q])]
            ans = QN[Q]
        else:
            lines = [L(f"{'x' if x == 0 else 'y'}좌표가 0 → {'y' if x == 0 else 'x'}축 위의 점", memo="축 위의 점"), L("어느 사분면에도 속하지 않아요")]
            ans = "어느 사분면에도 속하지 않음"
        S.add(1, q, ans, "x좌표 · y좌표의 부호로", lines, f.out(), omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        sa, sb = R.choice([1, -1]), R.choice([1, -1])
        forms = [("a", "b", lambda a, b: (a, b)), ("−a", "b", lambda a, b: (-a, b)), ("a", "−b", lambda a, b: (a, -b)), ("b", "a", lambda a, b: (b, a)),
                 ("ab", "b", lambda a, b: (a * b, b)), ("a − b", "ab", lambda a, b: (a - b, a * b)), ("−b", "a", lambda a, b: (-b, a)), ("{b/a}", "−a", lambda a, b: (b / a, -a))]
        fx, fy, fn = R.choice(forms)
        if fx == "a − b" and sa == sb:
            return
        a, b = sa * 2, sb * 3
        x, y = fn(a, b)
        Q = quad(x, y)
        conds = f"a {'>' if sa > 0 else '<'} 0, b {'>' if sb > 0 else '<'} 0"
        q = f"{conds}일 때, 점 ({fx}, {fy})는 어느 사분면 위의 점인가요?"
        sx, sy = ("+" if x > 0 else MI), ("+" if y > 0 else MI)
        lines = [L(f"x좌표 {fx} → {sx}", memo="부호만 따져요"), L(f"y좌표 {fy} → {sy}"), L(QN[Q])]
        S.add(2, q, QN[Q], "좌표의 부호를 차례로 정해요", lines, None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        x, y = R.randint(-6, 6), R.randint(-6, 6)
        if x == 0 or y == 0:
            return
        kind = ["x축", "y축", "원점"][S.count(3) % 3]
        X, Y = {"x축": (x, -y), "y축": (-x, y), "원점": (-x, -y)}[kind]
        f = Fig()
        pl = plane(f)
        pl.pt(x, y, label=f"P{P_(x, y)}", pos="ne" if x > 0 else "nw", f="gold")
        pl.pt(X, Y, label=f"Q", pos="ne" if X > 0 else "nw", f="coral", at=1)
        f.line(*pl.P(x, y), *pl.P(X, Y), c="coral", w=2.5, d=True, at=0)
        q = f"점 P{P_(x, y)}와 {kind}에 대하여 대칭인 점 Q의 좌표를 구하세요." if not bat(N(y)) else f"점 P{P_(x, y)}과 {kind}에 대하여 대칭인 점 Q의 좌표를 구하세요."
        rule_ = {"x축": "y좌표의 부호만 바꿔요", "y축": "x좌표의 부호만 바꿔요", "원점": "x좌표 · y좌표의 부호를 모두 바꿔요"}[kind]
        lines = [L(f"{kind} 대칭 → {rule_}"), L(f"Q{P_(X, Y)}")]
        S.add(3, q, P_(X, Y), rule_, lines, f.out(), omr="pt", key=q)
    fill(S, 3, 20, g3)

    def g4():
        for _ in range(50):
            x1, x2 = sorted(R.sample(range(-6, 7), 2))
            yb = R.randint(-5, 5)
            xc, yc = R.randint(-6, 6), R.randint(-6, 6)
            if yc != yb and abs(yc - yb) >= 2 and x2 - x1 >= 2:
                break
        else:
            return
        horiz = S.count(4) % 2 == 0
        if horiz:
            A, B, C = (x1, yb), (x2, yb), (xc, yc)
            base, h = x2 - x1, abs(yc - yb)
            bl = f"{x2} − ({N(x1)}) = {base}" if x1 < 0 else f"{x2} − {x1} = {base}"
            hl = f"|{N(yc)} − ({N(yb)})| = {h}" if yb < 0 else f"|{N(yc)} − {yb}| = {h}"
        else:
            A, B, C = (yb, x1), (yb, x2), (yc, xc)
            base, h = x2 - x1, abs(yc - yb)
            bl = f"{x2} − ({N(x1)}) = {base}" if x1 < 0 else f"{x2} − {x1} = {base}"
            hl = f"|{N(yc)} − ({N(yb)})| = {h}" if yb < 0 else f"|{N(yc)} − {yb}| = {h}"
        area = Fr(base * h, 2)
        f = Fig()
        pl = plane(f)
        f.poly([pl.P(*A), pl.P(*B), pl.P(*C)], c="gold", w=3.5, f="gold", fo=0.2)
        for nm_, p, pos in (("A", A, "sw"), ("B", B, "se"), ("C", C, "n")):
            pl.pt(*p, label=nm_, pos=pos)
        foot = (C[0], yb) if horiz else (yb, C[1])
        f.line(*pl.P(*C), *pl.P(*foot), c="coral", w=3, d=True, at=1)
        q = f"세 점 A{P_(*A)}, B{P_(*B)}, C{P_(*C)}을 꼭짓점으로 하는 삼각형 ABC의 넓이를 구하세요."
        lines = [L(bl, pre="밑변 AB", memo=f"{'x' if horiz else 'y'}좌표의 차"), L(hl, pre="높이", memo=f"C에서 AB까지 — {'y' if horiz else 'x'}좌표의 차"), L(f"{{1/2}} × {base} × {h} = {N(area)}")]
        S.add(4, q, N(area), "축에 평행한 변을 밑변으로 — 좌표의 차로 밑변 · 높이", lines, f.out(), key=q)
    fill(S, 4, 20, g4)

    def g5():
        for _ in range(80):
            pts = [(R.randint(-6, -1), R.randint(-6, -1)), (R.randint(1, 6), R.randint(-6, -1)), (R.randint(1, 6), R.randint(1, 6)), (R.randint(-6, -1), R.randint(1, 6))]
            xs, ys = [p[0] for p in pts], [p[1] for p in pts]
            W, H = max(xs) - min(xs), max(ys) - min(ys)
            # 넓이(신발끈)
            A2 = abs(sum(pts[i][0] * pts[(i + 1) % 4][1] - pts[(i + 1) % 4][0] * pts[i][1] for i in range(4)))
            if A2 % 2 == 0 and W * H * 2 > A2:
                break
        else:
            return
        area = A2 // 2
        corner_tris = []
        rect = [(min(xs), min(ys)), (max(xs), min(ys)), (max(xs), max(ys)), (min(xs), max(ys))]
        cut = 0
        parts = []
        for i in range(4):
            p, q_ = pts[i], pts[(i + 1) % 4]
            a2 = abs((q_[0] - p[0]) * (q_[1] - p[1]))
            if a2:
                parts.append(f"{{1/2}} × {abs(q_[0] - p[0])} × {abs(q_[1] - p[1])}")
                cut += Fr(a2, 2)
        rest = W * H - cut
        if rest != area or len(parts) < 2:
            return
        f = Fig()
        pl = plane(f)
        f.rect(*pl.P(min(xs), max(ys)), pl.sx * W, pl.sy * H, c="teal", sw=2.5, d=True, at=0)
        f.poly([pl.P(*p) for p in pts], c="gold", w=3.5, f="gold", fo=0.2)
        for nm_, p, pos in zip("ABCD", pts, ("sw", "se", "ne", "nw")):
            pl.pt(*p, label=nm_, pos=pos)
        q = "네 점 " + ", ".join(f"{n_}{P_(*p)}" for n_, p in zip("ABCD", pts)) + "을 꼭짓점으로 하는 사각형 ABCD의 넓이를 구하세요."
        lines = [L(f"{W} × {H} = {W * H}", pre="둘러싼 직사각형", memo="가로 · 세로는 좌표의 차"), L(" + ".join(parts) + f" = {N(cut)}", pre="바깥 삼각형들"), L(f"{W * H} − {N(cut)} = {area}")]
        S.add(5, q, str(area), "둘러싼 직사각형에서 바깥 삼각형을 빼요", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 정비례와 반비례 ══════════
def prop():
    S = Set("prop", "정비례와 반비례 — 표 · 식 · 그래프", "정비례·반비례",
            {1: "정비례 관계식", 2: "반비례 관계식", 3: "y = ax의 그래프", 4: "y = {a/x}의 그래프", 5: "정비례 · 반비례의 활용"},
            mixed=True, pp=8,
            tips={1: "y가 x에 정비례 → y = ax. 한 쌍의 (x, y)로 a = {y/x}",
                  2: "y가 x에 반비례 → y = {a/x}. 한 쌍의 (x, y)로 a = xy",
                  3: "y = ax의 그래프는 원점을 지나는 직선 — 지나는 점을 대입해 a를 구해요",
                  4: "y = {a/x}의 그래프 위의 점은 xy = a를 만족해요",
                  5: "한쪽이 2배, 3배일 때 다른 쪽도 2배, 3배면 정비례, {1/2}배, {1/3}배면 반비례"},
            note="정비례 · 반비례는 표에서 ‘몫이 일정(정비례) · 곱이 일정(반비례)’을 먼저 확인하게 해 주세요. 식을 세우면 그래프 위의 점 문제는 대입 한 번이에요.")
    R = rng(1204)

    def g1():
        a = R.choice([-5, -4, -3, -2, 2, 3, 4, 5, Fr(1, 2), Fr(-1, 2), Fr(3, 2), Fr(2, 3)])
        x0 = R.choice([2, 3, 4, 6, -2, -3, -4])
        y0 = a * x0
        if Fr(y0).denominator != 1:
            return
        x1 = R.choice([v for v in (-6, -4, -2, 5, 8, 10, 12) if v != x0])
        y1 = a * x1
        q = f"y가 x에 정비례하고 x = {N(x0)}일 때 y = {N(y0)}예요. x = {N(x1)}일 때 y의 값을 구하세요." if not bat(N(y0)) else f"y가 x에 정비례하고 x = {N(x0)}일 때 y = {N(y0)}이에요. x = {N(x1)}일 때 y의 값을 구하세요."
        lines = [L("y = ax로 놓아요", memo="정비례"), L(f"{N(y0)} = a × {NP(x0)}", memo="한 쌍 대입"), L(f"a = {N(a)} → y = {N(a) if a not in (1, -1) else ('' if a == 1 else MI)}x"), L(f"{N(a)} × {NP(x1)} = {N(y1)}", pre=f"x = {N(x1)}")]
        S.add(1, q, N(y1), "y = ax — 한 쌍을 대입해 a를 구해요", lines, None, sub={"a": a}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        a = R.choice([6, 12, 18, 24, 36, -6, -12, -24, 8, 16, 20])
        divs = [d for d in range(-12, 13) if d and a % d == 0]
        x0, x1 = R.sample(divs, 2)
        y0, y1 = a // x0, a // x1
        q = f"y가 x에 반비례하고 x = {N(x0)}일 때 y = {N(y0)}예요. x = {N(x1)}일 때 y의 값을 구하세요." if not bat(N(y0)) else f"y가 x에 반비례하고 x = {N(x0)}일 때 y = {N(y0)}이에요. x = {N(x1)}일 때 y의 값을 구하세요."
        lines = [L("y = {a/x}로 놓아요", memo="반비례 — xy = a"), L(f"{NP(x0)} × {NP(y0)} = {N(a)}", pre="a = xy"), L(f"y = {{{N(a)}/x}}" if a > 0 else f"y = {MI}{{{-a}/x}}"), L(f"{N(a)} ÷ {NP(x1)} = {N(y1)}", pre=f"x = {N(x1)}")]
        S.add(2, q, N(y1), "반비례는 xy가 일정 — a = xy", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        a = R.choice([-3, -2, -1, 1, 2, 3, Fr(1, 2), Fr(-1, 2), Fr(1, 3), Fr(-2, 3), Fr(3, 2)])
        x0 = R.choice([2, 3, 4, 6, -2, -3, -4, -6])
        y0 = a * x0
        if Fr(y0).denominator != 1 or abs(y0) > 6:
            return
        f = Fig()
        pl = Plane(f, (-6.5, 6.5), (-6.5, 6.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=2)
        pl.lineq(float(a), 0, at="q")
        pl.pt(x0, int(y0), label=P_(x0, int(y0)), pos="ne" if x0 > 0 else "nw", f="gold")
        k = S.count(3) % 2
        if k == 0:
            q = f"y = ax의 그래프가 점 {P_(x0, int(y0))}{'을' if bat(N(int(y0))) else '를'} 지날 때, 상수 a의 값을 구하세요."
            lines = [L(f"{N(int(y0))} = a × {NP(x0)}", memo="지나는 점을 대입"), L(f"a = {N(int(y0))} ÷ {NP(x0)} = {N(a)}")]
            S.add(3, q, N(a), "지나는 점의 좌표를 대입해요", lines, f.out(), key=q)
        else:
            m = R.choice([v for v in (-6, -4, -2, 2, 4, 6) if v != x0])
            ym = a * m
            if Fr(ym).denominator != 1:
                return
            q = f"y = ax의 그래프가 점 {P_(x0, int(y0))}{'을' if bat(N(int(y0))) else '를'} 지날 때, 이 그래프 위의 점 ({N(m)}, k)에서 k의 값을 구하세요."
            lines = [L(f"{N(int(y0))} = a × {NP(x0)} → a = {N(a)}", memo="먼저 a"), L(f"k = {N(a)} × {NP(m)} = {N(ym)}", memo="같은 그래프 위의 점")]
            S.add(3, q, N(ym), "a를 먼저 구하고 다시 대입", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.choice([4, 6, 8, 12, -4, -6, -8, -12])
        divs = [d for d in range(-6, 7) if d and a % d == 0 and abs(a // d) <= 6]
        x0 = R.choice(divs)
        y0 = a // x0
        f = Fig()
        pl = Plane(f, (-6.5, 6.5), (-6.5, 6.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=2)
        pl.curve(lambda x: a / x if abs(x) > 0.05 else None, -6.5, -0.3, n=60)
        pl.curve(lambda x: a / x if abs(x) > 0.05 else None, 0.3, 6.5, n=60)
        pl.pt(x0, y0, label=P_(x0, y0), pos="ne" if x0 > 0 else "nw", f="gold")
        k = S.count(4) % 2
        if k == 0:
            q = f"y = {{a/x}}의 그래프가 점 {P_(x0, y0)}{'을' if bat(N(y0)) else '를'} 지날 때, 상수 a의 값을 구하세요."
            lines = [L(f"a = xy", memo="반비례 그래프 위의 점"), L(f"{NP(x0)} × {NP(y0)} = {N(a)}")]
            S.add(4, q, N(a), "a = x좌표 × y좌표", lines, f.out(), key=q)
        else:
            m = R.choice([d for d in divs if d != x0])
            ym = a // m
            q = f"y = {{a/x}}의 그래프가 점 {P_(x0, y0)}{'을' if bat(N(y0)) else '를'} 지날 때, 이 그래프 위의 점 ({N(m)}, k)에서 k의 값을 구하세요."
            lines = [L(f"{NP(x0)} × {NP(y0)} = {N(a)}", pre="a = xy"), L(f"k = {N(a)} ÷ {NP(m)} = {N(ym)}", memo="xy = a")]
            S.add(4, q, N(ym), "a = xy를 먼저 — 같은 그래프 위의 점도 xy = a", lines, f.out(), key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        if k == 0:
            r = R.randint(2, 9); t = R.randint(5, 30)
            q = f"빈 물통에 1분에 {r} L씩 물을 넣어요. x분 동안 넣은 물의 양을 y L라 할 때, {t}분 동안 넣은 물은 몇 L인가요?"
            lines = [L(f"y = {r}x", memo="1분에 일정하게 → 정비례"), L(f"{r} × {t} = {r * t}", pre=f"x = {t}"), L(f"{r * t} L")]
            ans, ap = f"{r * t} L", str(r * t)
        elif k == 1:
            a, b = R.randint(10, 40), R.randint(2, 8)
            ta = a * b
            cands = [d for d in range(5, 61) if ta % d == 0 and d != a]
            if not cands:
                return
            nb = R.choice(cands)
            q = f"톱니가 {a}개인 톱니바퀴 A와 맞물려 도는 톱니바퀴 B가 있어요. A가 {b}바퀴 돌 때, 톱니가 {nb}개인 B는 몇 바퀴 도나요?"
            lines = [L(f"{a} × {b} = {ta}", pre="맞물린 톱니 수", memo="두 바퀴가 지나간 톱니 수는 같아요"), L(f"(B의 톱니 수) × (회전 수) = {ta}", memo="반비례"), L(f"{ta} ÷ {nb} = {ta // nb}"), L(f"{ta // nb}바퀴")]
            ans, ap = f"{ta // nb}바퀴", str(ta // nb)
        elif k == 2:
            n, d = R.randint(3, 12), R.randint(2, 6)
            work = n * d
            cands = [v for v in range(2, 25) if work % v == 0 and v != n]
            if not cands:
                return
            m = R.choice(cands)
            q = f"어떤 일을 {n}명이 하면 {d}일이 걸려요. 같은 빠르기로 {m}명이 하면 며칠이 걸리나요?"
            lines = [L(f"{n} × {d} = {work}", pre="전체 일의 양", memo="사람 수 × 날수 일정 → 반비례"), L(f"{work} ÷ {m} = {work // m}"), L(f"{work // m}일")]
            ans, ap = f"{work // m}일", str(work // m)
        else:
            w = R.randint(2, 9); L0 = R.randint(10, 40); x = R.randint(2, 12)
            q = f"용수철에 무게 x g인 추를 매달면 용수철이 y cm 늘어나요. 추 1 `g`에 {D2(Fr(w, 10))} cm씩 늘어날 때, 무게 {x * 10} `g`인 추를 매달면 몇 cm 늘어나나요?"
            v = Fr(w, 10) * x * 10
            lines = [L(f"y = {D2(Fr(w, 10))}x", memo="무게에 정비례"), L(f"{D2(Fr(w, 10))} × {x * 10} = {D2(v)}", pre=f"x = {x * 10}"), L(f"{D2(v)} cm")]
            ans, ap = f"{D2(v)} cm", D2(v)
        S.add(5, q, ans, "2배 · 3배 하면 2배 · 3배(정비례), {1/2}배 · {1/3}배(반비례)", lines, None, ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S

def D2(v):
    return DEC(Fr(v))


# ══════════ 각과 평행선 ══════════
def X_lines(f, ang, at="q"):
    """두 직선이 만나는 그림 — 가로선과 ang° 기울어진 선, 교점 (330, 330)"""
    O = (330, 330)
    f.line(60, 330, 600, 330, c="ink", w=3, at=at)
    A = ang_pt(*O, 280, ang)
    B = ang_pt(*O, 280, ang + 180)
    f.line(*B, *A, c="ink", w=3, at=at)
    return O, A, B

def angle():
    S = Set("angle", "맞꼭지각과 평행선 — 동위각 · 엇각", "각과 평행선",
            {1: "맞꼭지각", 2: "평각 위의 각", 3: "평행선의 동위각 · 엇각", 4: "평행선 사이의 꺾인 선", 5: "종이 테이프 접기"},
            pp=8,
            tips={1: "두 직선이 만나서 생기는 맞꼭지각의 크기는 같아요",
                  2: "한 직선(평각) 위에 모인 각들의 합은 180°",
                  3: "두 직선이 평행하면 동위각 · 엇각의 크기가 같아요",
                  4: "꺾인 점을 지나고 두 직선에 평행한 보조선을 그으면 엇각 두 개의 합",
                  5: "접은 각은 접기 전 각과 같고, 평행선의 엇각도 같아요 — 접힌 부분은 이등변삼각형"},
            note="각 문제는 ‘같은 각 찾기(맞꼭지각 · 동위각 · 엇각 · 접은 각)’와 ‘합이 180°인 각’ 두 가지로 정리하게 해 주세요. 보조선 긋기는 꺾인 점에서 평행선을 그리는 것부터 연습해요.")
    R = rng(1205)

    def g1():
        x = R.randint(10, 50)
        a, b = R.randint(2, 4), R.randint(1, 3)
        if a <= b:
            return
        c = R.randint(5, 40)
        d = (a - b) * x + c
        if d <= 0:
            return
        ang = a * x + c
        if not 20 <= ang <= 160:
            return
        f = Fig()
        O, A, B = X_lines(f, ang)
        angle_mark(f, O, (600, 330), A, r=50, label=f"({a}x + {c})°")
        angle_mark(f, O, (60, 330), B, r=50, label=f"({b}x + {d})°" if b > 1 else f"(x + {d})°", c="teal", f_="teal")
        lb = f"{b}x + {d}" if b > 1 else f"x + {d}"
        q = f"두 직선이 만나서 생긴 맞꼭지각의 크기가 각각 ({a}x + {c})°, ({lb})°일 때, x의 값을 구하세요."
        lines = [L(f"{a}x + {c} = {lb}", memo="맞꼭지각의 크기는 같아요"), L(f"{mono(a - b, 'x', 1, first=True)} = {N(d - c)}", memo="이항"), L(f"x = {x}")]
        S.add(1, q, str(x), "맞꼭지각끼리 같다고 놓아요", lines, f.out(), sub={"x": x}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        x = R.randint(10, 40)
        if k == 0:
            a, c = R.randint(2, 4), R.randint(10, 50)
            rest = 180 - (a + 1) * x - c
            if not 20 <= rest <= 120:
                return
            f = Fig()
            O = (330, 420)
            f.line(60, 420, 600, 420, c="ink", w=3)
            t1 = rest
            t2 = rest + x
            f.line(*O, *ang_pt(*O, 250, t1), c="ink", w=3)
            f.line(*O, *ang_pt(*O, 250, t2), c="ink", w=3)
            angle_mark(f, O, (600, 420), ang_pt(*O, 250, t1), r=56, label=f"{rest}°")
            angle_mark(f, O, ang_pt(*O, 250, t1), ang_pt(*O, 250, t2), r=80, label="x°", c="teal", f_="teal")
            angle_mark(f, O, ang_pt(*O, 250, t2), (60, 420), r=56, label=f"({a}x + {c})°", c="coral", f_="coral")
            q = f"한 직선 위에서 세 각의 크기가 {rest}°, x°, ({a}x + {c})°일 때, x의 값을 구하세요."
            lines = [L(f"{rest} + x + {a}x + {c} = 180", memo="평각 180°"), L(f"{a + 1}x = {180 - rest - c}"), L(f"x = {x}")]
        else:
            a, b = R.randint(2, 5), R.randint(1, 4)
            c = 180 - (a + b) * x
            if not 10 <= c <= 120:
                return
            f = Fig()
            O = (330, 420)
            f.line(60, 420, 600, 420, c="ink", w=3)
            t1, t2 = a * x, a * x + c
            f.line(*O, *ang_pt(*O, 250, t1), c="ink", w=3)
            f.line(*O, *ang_pt(*O, 250, t2), c="ink", w=3)
            angle_mark(f, O, (600, 420), ang_pt(*O, 250, t1), r=56, label=f"{a}x°")
            angle_mark(f, O, ang_pt(*O, 250, t1), ang_pt(*O, 250, t2), r=80, label=f"{c}°", c="teal", f_="teal")
            angle_mark(f, O, ang_pt(*O, 250, t2), (60, 420), r=56, label=f"{b}x°" if b > 1 else "x°", c="coral", f_="coral")
            q = f"한 직선 위에서 세 각의 크기가 {a}x°, {c}°, {f'{b}x' if b > 1 else 'x'}°일 때, x의 값을 구하세요."
            lines = [L(f"{a}x + {c} + {b}x = 180" if b > 1 else f"{a}x + {c} + x = 180", memo="평각 180°"), L(f"{a + b}x = {180 - c}"), L(f"x = {x}")]
        S.add(2, q, str(x), "한 직선 위의 각을 모두 더하면 180°", lines, f.out(), sub={"x": x}, key=q)
    fill(S, 2, 20, g2)

    def par(f, t, at="q"):
        """평행선 두 개(y=230, 430) + 기울기 t° 인 직선(가로선과 만나는 각)"""
        f.line(40, 230, 620, 230, c="ink", w=3, ar=1, at=at)
        f.line(40, 430, 620, 430, c="ink", w=3, ar=1, at=at)
        f.text(612, 216, "l", z=28, c="soft", at=at)
        f.text(612, 416, "m", z=28, c="soft", at=at)
        dx = 200 / math.tan(math.radians(t))
        P1 = (330 + dx / 2, 230)
        P2 = (330 - dx / 2, 430)
        E1 = (P1[0] + (P1[0] - P2[0]) * 0.6, 230 - 120)
        E2 = (P2[0] - (P1[0] - P2[0]) * 0.6, 430 + 120)
        f.line(*E2, *E1, c="ink", w=3, at=at)
        return P1, P2, E1, E2

    def g3():
        k = S.count(3) % 4
        t = R.choice([40, 50, 55, 60, 65, 70, 75, 110, 115, 120, 125, 130, 135])
        f = Fig()
        P1, P2, E1, E2 = par(f, t)
        right = (620, 0)
        if k == 0:
            angle_mark(f, P1, (620, 230), E1, r=46, label=f"{t}°")
            angle_mark(f, P2, (620, 430), P1, r=46, label="x", c="coral", f_="coral", at=0)
            q = f"두 직선 l, m이 평행할 때, 위쪽 교점에서 오른쪽 위 각이 {t}°예요. 아래쪽 교점에서 같은 위치(오른쪽 위)의 각 x의 크기를 구하세요."
            lines = [L("l // m → 동위각의 크기는 같아요", memo="같은 위치의 각"), L(f"x = {t}°")]
            ans = t
            plan = "평행선의 동위각은 같아요"
        elif k == 1:
            angle_mark(f, P1, (40, 230), P2, r=46, label=f"{180 - t}°")
            angle_mark(f, P2, (620, 430), P1, r=46, label="x", c="coral", f_="coral", at=0)
            q = f"두 직선 l, m이 평행할 때, 위쪽 교점에서 왼쪽 아래 각이 {180 - t}°예요. 아래쪽 교점에서 오른쪽 위 각 x의 크기를 구하세요."
            lines = [L("l // m → 엇각의 크기는 같아요", memo="Z 모양"), L(f"x = {180 - t}°")]
            ans = 180 - t
            plan = "평행선의 엇각은 같아요"
        elif k == 2:
            angle_mark(f, P1, (620, 230), E1, r=46, label=f"{t}°")
            angle_mark(f, P2, (40, 430), P1, r=46, label="x", c="coral", f_="coral", at=0)
            q = f"두 직선 l, m이 평행할 때, 위쪽 교점에서 오른쪽 위 각이 {t}°예요. 아래쪽 교점에서 왼쪽 위 각 x의 크기를 구하세요."
            lines = [L(f"오른쪽 위 각 = {t}°", pre="동위각", memo="아래 교점에서도 같은 위치"), L(f"180 − {t} = {180 - t}", memo="평각에서 빼요"), L(f"x = {180 - t}°")]
            ans = 180 - t
            plan = "동위각으로 옮긴 뒤 평각 180°"
        else:
            a, b = R.randint(2, 4), R.randint(5, 40)
            xv = (t - b) / a
            if xv != int(xv) or xv <= 0:
                return
            xv = int(xv)
            angle_mark(f, P1, (620, 230), E1, r=46, label=f"({a}x + {b})°")
            angle_mark(f, P2, (620, 430), P1, r=46, label=f"{t}°", c="teal", f_="teal")
            q = f"두 직선 l, m이 평행할 때, 동위각의 크기가 각각 ({a}x + {b})°, {t}°예요. x의 값을 구하세요."
            lines = [L(f"{a}x + {b} = {t}", memo="동위각의 크기는 같아요"), L(f"{a}x = {t - b}"), L(f"x = {xv}")]
            S.add(3, q, str(xv), "동위각끼리 같다고 놓아요", lines, f.out(), sub={"x": xv}, key=q)
            return
        S.add(3, q, f"{ans}°", plan, lines, f.out(), ap=str(ans), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.randint(20, 70), R.randint(20, 70)
        k = S.count(4) % 2
        f = Fig()
        f.line(40, 200, 620, 200, c="ink", w=3, ar=1)
        f.line(40, 480, 620, 480, c="ink", w=3, ar=1)
        f.text(612, 186, "l", z=28, c="soft"); f.text(612, 466, "m", z=28, c="soft")
        Pm = (420, 340)
        A = (Pm[0] - 140 / math.tan(math.radians(a)), 200)
        B = (Pm[0] - 140 / math.tan(math.radians(b)), 480)
        f.line(*A, *Pm, c="ink", w=3)
        f.line(*B, *Pm, c="ink", w=3)
        f.line(80, 340, 620, 340, c="teal", w=2.5, d=True, at=0)
        angle_mark(f, A, (620, 200), Pm, r=44, label=f"{a}°")
        angle_mark(f, B, (620, 480), Pm, r=44, label=f"{b}°")
        if k == 0:
            angle_mark(f, Pm, A, B, r=40, label="x", c="coral", f_="coral", at=2)
            q = f"두 직선 l, m이 평행하고, 꺾인 선이 l과 {a}°, m과 {b}°를 이루며 두 직선 사이의 한 점에서 꺾였어요. 꺾인 점에서의 각 x의 크기를 구하세요."
            lines = [L("꺾인 점을 지나고 l, m에 평행한 보조선", memo="엇각 두 개로 나뉘어요"), L(f"위 엇각 {a}°, 아래 엇각 {b}°"), L(f"x = {a} + {b} = {a + b}")]
            ans, ap = f"{a + b}°", str(a + b)
        else:
            angle_mark(f, Pm, A, B, r=40, label=f"{a + b}°", c="coral", f_="coral")
            q = f"두 직선 l, m이 평행하고, 꺾인 선이 l과 {a}°를 이루고 꺾인 점에서의 각이 {a + b}°예요. 꺾인 선이 m과 이루는 각의 크기를 구하세요."
            lines = [L("꺾인 점에서 l, m에 평행한 보조선", memo="꺾인 각 = 두 엇각의 합"), L(f"{a + b} − {a} = {b}"), L(f"{b}°")]
            ans, ap = f"{b}°", str(b)
        S.add(4, q, ans, "꺾인 점에서 평행한 보조선 — 엇각 두 개의 합", lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        a = R.choice([40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70])
        k = S.count(5) % 2
        f = Fig()
        f.line(40, 220, 620, 220, c="ink", w=3)
        f.line(40, 460, 620, 460, c="ink", w=3)
        px = 330
        P = (px, 460)
        Q = (px + 240 / math.tan(math.radians(a)), 220)
        T = (px + 240 / math.tan(math.radians(2 * a)), 220) if a != 45 else (px, 220)
        f.poly([P, Q, T], c="gold", w=3, f="gold", fo=0.18, at=0)
        f.line(*P, *Q, c="coral", w=3.5)
        f.text((P[0] + Q[0]) / 2 + 30, (P[1] + Q[1]) / 2 + 10, "접은 선", z=22, c="coral", b=700, a="s")
        if k == 0:
            angle_mark(f, Q, (40, 220), P, r=46, label=f"{a}°")
            angle_mark(f, T, P, Q, r=40, label="?", c="coral", f_="coral", at=2)
            q = f"폭이 일정한 종이 테이프를 접었더니 접은 선과 테이프의 윗변이 이루는 각이 {a}°가 되었어요. 겹쳐진 삼각형에서 나머지 한 꼭짓점(윗변 위)의 각의 크기를 구하세요."
            lines = [L(f"접은 선과 아랫변의 각 {a}°", memo="평행선의 엇각"), L(f"겹친 삼각형의 접은 선 양 끝 각: {a}°, {a}°", memo="접은 각은 접기 전과 같아요"), L(f"180 − {a} × 2 = {180 - 2 * a}"), L(f"{180 - 2 * a}°")]
            ans, ap = f"{180 - 2 * a}°", str(180 - 2 * a)
        else:
            top = 180 - 2 * a
            angle_mark(f, T, P, Q, r=40, label=f"{top}°", c="teal", f_="teal")
            angle_mark(f, Q, (40, 220), P, r=46, label="?", c="coral", f_="coral", at=1)
            q = f"폭이 일정한 종이 테이프를 접었더니 겹쳐진 삼각형에서 윗변 위의 꼭짓점의 각이 {top}°가 되었어요. 접은 선과 테이프의 윗변이 이루는 각의 크기를 구하세요."
            lines = [L("겹쳐진 삼각형은 접은 선 양 끝 각이 같은 이등변삼각형", memo="엇각 = 접은 각"), L(f"(180 − {top}) ÷ 2 = {a}"), L(f"{a}°")]
            ans, ap = f"{a}°", str(a)
        S.add(5, q, ans, "접은 각과 엇각이 같아 — 이등변삼각형", lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 다각형 ══════════
KN = {3: "삼", 4: "사", 5: "오", 6: "육", 7: "칠", 8: "팔", 9: "구", 10: "십", 11: "십일", 12: "십이", 13: "십삼", 14: "십사", 15: "십오", 16: "십육", 18: "십팔", 20: "이십", 24: "이십사", 30: "삼십", 36: "삼십육"}

def ngon(f, n, at="q", r=230, cx=330, cy=340, diag=False, diag_at=0):
    pts = [ang_pt(cx, cy, r, 90 + 360 * i / n) for i in range(n)]
    f.poly(pts, c="ink", w=3, at=at)
    if diag:
        k = 0
        for j in range(2, n - 1):
            f.line(*pts[0], *pts[j], c="teal", w=2.5, d=True, at=diag_at, dl=k * 120)
            k += 1
    return pts

def pgon():
    S = Set("pgon", "다각형 — 대각선 · 내각 · 외각", "다각형",
            {1: "대각선의 개수", 2: "내각의 크기의 합", 3: "정다각형의 한 내각 · 외각", 4: "삼각형의 외각", 5: "외각의 합 360°"},
            pp=8,
            tips={1: "한 꼭짓점에서 n − 3개 → 모두 {n(n − 3)/2}개(두 번 센 것 나누기)",
                  2: "한 꼭짓점에서 대각선을 그으면 삼각형 n − 2개 → 180° × (n − 2)",
                  3: "정n각형의 한 외각 = 360° ÷ n, 한 내각 = 180° − 한 외각",
                  4: "삼각형의 한 외각 = 이웃하지 않는 두 내각의 합",
                  5: "다각형의 외각의 크기의 합은 늘 360°"},
            note="공식을 외우기 전에 ‘한 꼭짓점에서 대각선을 그어 삼각형으로 나누기’를 직접 그려 보게 해 주세요. 정다각형은 외각(360° ÷ n)부터 구하는 것이 가장 빨라요.")
    R = rng(1206)

    def g1():
        k = S.count(1) % 2
        n = R.randint(4, 20)
        d = n * (n - 3) // 2
        f = Fig()
        if n <= 12:
            ngon(f, n, diag=True)
        if k == 0:
            q = f"{KN.get(n, n)}각형의 대각선은 모두 몇 개인가요?" if n in KN else f"{n}각형의 대각선은 모두 몇 개인가요?"
            lines = [L(f"{n} − 3 = {n - 3}", pre="한 꼭짓점에서", memo="자신과 이웃한 두 점 빼기"), L(f"{n} × {n - 3} ÷ 2 = {d}", memo="두 번씩 센 것"), L(f"{d}개")]
            S.add(1, q, f"{d}개", "{n(n − 3)/2}", lines, f.out() if f.els else None, ap=str(d), key=q)
        else:
            q = f"대각선이 모두 {d}개인 다각형은 몇 각형인가요?"
            lines = [L(f"{{n(n − 3)/2}} = {d}", memo="n각형으로 놓아요"), L(f"n(n − 3) = {2 * d}"), L(f"{n} × {n - 3} = {2 * d} → n = {n}", memo="연속하지 않는 두 수(차 3)의 곱"), L(f"{KN.get(n, n)}각형" if n in KN else f"{n}각형")]
            S.add(1, q, f"{KN.get(n, str(n))}각형", "n(n − 3) = 대각선 수 × 2", lines, f.out() if f.els else None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        n = R.randint(4, 15)
        T = 180 * (n - 2)
        f = Fig()
        if n <= 10:
            pts = ngon(f, n, diag=True)
        if k == 0:
            q = f"{KN[n]}각형의 내각의 크기의 합을 구하세요."
            lines = [L(f"{n} − 2 = {n - 2}", pre="삼각형 수", memo="한 꼭짓점에서 대각선"), L(f"180 × {n - 2} = {T}"), L(f"{T}°")]
            S.add(2, q, f"{T}°", "180° × (n − 2)", lines, f.out() if f.els else None, ap=str(T), key=q)
        else:
            q = f"내각의 크기의 합이 {T}°인 다각형은 몇 각형인가요?"
            lines = [L(f"180 × (n − 2) = {T}"), L(f"n − 2 = {n - 2}"), L(f"n = {n} → {KN[n]}각형")]
            S.add(2, q, f"{KN[n]}각형", "180° × (n − 2) = 합", lines, f.out() if f.els else None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        n = R.choice([3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36])
        k = S.count(3) % 3
        ex = 360 // n
        inn = 180 - ex
        f = Fig()
        if n <= 12:
            pts = ngon(f, n)
            A, B = pts[0], pts[1]
            Ext = (B[0] + (B[0] - A[0]) * 0.6, B[1] + (B[1] - A[1]) * 0.6)
            f.line(*B, *Ext, c="soft", w=2.5, d=True)
            angle_mark(f, B, Ext, pts[2], r=36, c="coral", f_="coral", at=0)
        if k == 0:
            q = f"정{KN[n]}각형의 한 내각의 크기를 구하세요."
            lines = [L(f"360 ÷ {n} = {ex}", pre="한 외각", memo="외각의 합 360°"), L(f"180 − {ex} = {inn}", pre="한 내각"), L(f"{inn}°")]
            ans, ap = f"{inn}°", str(inn)
        elif k == 1:
            q = f"정{KN[n]}각형의 한 외각의 크기를 구하세요."
            lines = [L("외각의 합은 360°", memo="모든 외각이 같아요"), L(f"360 ÷ {n} = {ex}"), L(f"{ex}°")]
            ans, ap = f"{ex}°", str(ex)
        else:
            q = f"한 내각의 크기가 {inn}°인 정다각형은 정몇각형인가요?"
            lines = [L(f"180 − {inn} = {ex}", pre="한 외각"), L(f"360 ÷ {ex} = {n}", memo="외각의 합 360°"), L(f"정{KN[n]}각형")]
            ans, ap = f"정{KN[n]}각형", f"정{KN[n]}각형"
        S.add(3, q, ans, "한 외각 = 360° ÷ n부터", lines, f.out() if f.els else None, ap=ap, omr="ex" if k == 2 else "num", key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.randint(25, 80), R.randint(25, 80)
        if a + b >= 170:
            return
        k = S.count(4) % 3
        f = Fig()
        A, B, C = (330 - 40, 140), (90, 500), (520, 500)
        # 각 B = a, 각 A = b 근사 그림 — 위치는 고정, 글자로 표시
        f.poly([A, B, C], c="ink", w=3)
        f.line(*C, 620, 500, c="soft", w=2.5, d=True)
        angle_mark(f, B, C, A, r=44, label=f"{a}°" if k != 2 else "x")
        angle_mark(f, A, B, C, r=44, label=f"{b}°" if k != 1 else None)
        if k == 0:
            angle_mark(f, C, (620, 500), A, r=40, label="x", c="coral", f_="coral", at=0)
            q = f"삼각형 ABC에서 ∠A = {b}°, ∠B = {a}°일 때, 꼭짓점 C에서의 외각의 크기 x를 구하세요."
            lines = [L("한 외각 = 이웃하지 않는 두 내각의 합"), L(f"x = {b} + {a} = {a + b}"), L(f"{a + b}°")]
            ans, ap = f"{a + b}°", str(a + b)
        elif k == 1:
            angle_mark(f, C, (620, 500), A, r=40, label=f"{a + b}°", c="coral", f_="coral")
            q = f"삼각형 ABC에서 ∠B = {a}°이고 꼭짓점 C에서의 외각이 {a + b}°일 때, ∠A의 크기를 구하세요."
            lines = [L("외각 = 이웃하지 않는 두 내각의 합"), L(f"∠A = {a + b} − {a} = {b}"), L(f"{b}°")]
            ans, ap = f"{b}°", str(b)
        else:
            m = R.randint(2, 3)
            xv = a
            c0 = (a + b) - m * xv
            if c0 <= 0:
                return
            angle_mark(f, C, (620, 500), A, r=40, label=f"({m}x + {c0})°", c="coral", f_="coral")
            q = f"삼각형 ABC에서 ∠A = {b}°, ∠B = x°이고 꼭짓점 C에서의 외각이 ({m}x + {c0})°일 때, x의 값을 구하세요."
            lines = [L(f"{m}x + {c0} = {b} + x", memo="외각 = 두 내각의 합"), L(f"{m - 1}x = {b - c0}" if m > 2 else f"x = {b - c0}"), L(f"x = {xv}")]
            if b - c0 != (m - 1) * xv:
                return
            S.add(4, q, str(xv), "외각 = 이웃하지 않는 두 내각의 합으로 식", lines, f.out(), sub={"x": xv}, key=q)
            return
        S.add(4, q, ans, "삼각형의 외각 = 이웃하지 않는 두 내각의 합", lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        if k == 0:
            n = R.randint(4, 7)
            angs = [R.randint(40, 110) for _ in range(n - 1)]
            x = 360 - sum(angs)
            if not 30 <= x <= 130:
                return
            f = Fig()
            pts = ngon(f, n, r=190)
            for i in range(n):
                A, B = pts[i - 1], pts[i]
                E = (B[0] + (B[0] - A[0]) * 0.45, B[1] + (B[1] - A[1]) * 0.45)
                f.line(*B, *E, c="soft", w=2.5, d=True)
            q = f"{KN[n]}각형의 외각의 크기가 각각 {', '.join(f'{a}°' for a in angs)}, x°일 때, x의 값을 구하세요."
            lines = [L(f"{' + '.join(map(str, angs))} + x = 360", memo="외각의 합 360°"), L(f"{sum(angs)} + x = 360"), L(f"x = {x}")]
            S.add(5, q, str(x), "다각형의 외각의 합은 360°", lines, f.out(), sub={"x": x}, key=q)
        else:
            n = R.randint(5, 9)
            angs = [R.randint(95, 150) for _ in range(n - 1)]
            T = 180 * (n - 2)
            x = T - sum(angs)
            if not 80 <= x <= 170:
                return
            q = f"{KN[n]}각형의 내각의 크기가 각각 {', '.join(f'{a}°' for a in angs)}, x°일 때, x의 값을 구하세요."
            lines = [L(f"180 × ({n} − 2) = {T}", pre="내각의 합"), L(f"{T} − {sum(angs)} = {x}", memo="나머지 내각의 합 빼기"), L(f"x = {x}")]
            S.add(5, q, str(x), "내각의 합 180° × (n − 2)에서 빼요", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S
