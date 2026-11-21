# 고2 — ① 지수와 로그 — 정의에서 성질까지 · ② 미분 — 접선의 기울기에서 극값까지
from core import *
from fig import Fig, Plane

x = SYMS["x"]

def P_(e):
    return sym_poly_str(e)

def ex_str(fr):
    """지수 글자 — 2 · −1 · 2/3 · −1/3 (지수 안의 분수는 한 줄로)"""
    fr = Fr(fr)
    if fr.denominator == 1:
        return N(fr.numerator)
    return (MI if fr < 0 else "") + f"{abs(fr.numerator)}/{fr.denominator}"

def exq(fr):
    """곱셈 안에 들어갈 지수 — 음수면 괄호"""
    s = ex_str(fr)
    return f"({s})" if Fr(fr) < 0 else s

def num_eq(expr_s, v):
    """판서 글자 계산이 v 와 같은지 (검산)"""
    got = val(expr_s)
    assert got is not None and sp.simplify(got - sp.nsimplify(v)) == 0, (expr_s, got, v)

def logv(arg, base):
    v = sp.nsimplify(sp.simplify(sp.expand_log(sp.log(arg) / sp.log(base), force=True)))
    assert abs(float(v) - math.log(float(arg)) / math.log(float(base))) < 1e-9, (arg, base, v)
    assert v.is_rational, (arg, base, v)
    return Fr(int(sp.fraction(v)[0]), int(sp.fraction(v)[1]))

# ══════════ ① 지수와 로그 ══════════
POW = {2: [2, 4, 8, 16, 32], 3: [3, 9, 27, 81], 5: [5, 25, 125], 10: [10, 100, 1000]}

def set_a():
    S = Set("a", "지수와 로그 — 정의에서 성질까지", "지수와 로그",
            {1: "유리수 지수", 2: "지수법칙", 3: "로그의 정의", 4: "로그의 성질", 5: "지수 · 로그 방정식"},
            pp=10,
            tips={1: "a^{m/n} — 밑을 소수의 거듭제곱으로 바꾸면 지수끼리 곱하기만 남아요",
                  2: "밑을 같게 → 곱하면 지수끼리 더하기, 나누면 빼기",
                  3: "log_{a} N = x ⇔ a^{x} = N — ‘a를 몇 제곱하면 N?’",
                  4: "곱 → 합, 몫 → 차, 거듭제곱 → 앞으로, 밑변환 log_{a} b = {log b/log a}",
                  5: "밑을 같게 해서 지수끼리, 로그는 정의로 풀고 진수 조건(진수 > 0)을 확인"},
            note="로그는 ‘지수를 묻는 말’이에요. log_{2} 8을 ‘2를 몇 제곱하면 8?’이라고 소리 내어 읽게 하면 로그의 성질이 지수법칙에서 그대로 나와요.")
    R = rng(2201)

    def pick(bases=(2, 3, 5, 10), kmin=2):
        b = R.choice(bases)
        n = R.choice([n for n in POW[b] if round(math.log(n, b)) >= kmin])
        k = round(math.log(n, b))
        assert b ** k == n
        return b, n, k

    # 1단계 — 유리수 지수
    def g1():
        b, n, k = pick()
        e = Fr(R.choice([1, 2, 3, 5, -1, -2]), R.choice([2, 3, 4, 5]))
        if e.denominator == 1:
            return
        tot = k * e
        if tot.denominator != 1 or tot == 0 or b ** abs(tot.numerator) > 1000:
            return
        v = Fr(b) ** tot.numerator
        q = f"{n}^{{{ex_str(e)}}}의 값을 구하세요."
        lines = [L(f"{n} = {b}^{{{k}}}", memo="밑을 소수의 거듭제곱으로"),
                 L(f"{n}^{{{ex_str(e)}}} = ({b}^{{{k}}})^{{{ex_str(e)}}} = {b}^{{{k} × {exq(e)}}}", memo="지수끼리 곱하기"),
                 L(f"{b}^{{{N(tot)}}} = {N(v)}")]
        S.add(1, q, N(v), "밑을 바꾸고 지수끼리 곱해요", lines, ap=plain(N(v)))
    fill(S, 1, 20, g1)

    # 2단계 — 지수법칙
    def g2():
        b = R.choice([2, 3, 5])
        n1, n2 = R.choice(POW[b][1:]), R.choice(POW[b][1:])
        k1, k2 = round(math.log(n1, b)), round(math.log(n2, b))
        e1 = Fr(R.choice([1, 2, 3, -1]), R.choice([2, 3, 4]))
        e2 = Fr(R.choice([1, 2, 3, -1, -2]), R.choice([2, 3, 4]))
        if e1.denominator == 1 or e2.denominator == 1 or (n1, e1) == (n2, e2):
            return
        op = R.choice(["×", "÷"])
        t1, t2 = k1 * e1, k2 * e2
        tot = t1 + t2 if op == "×" else t1 - t2
        if tot.denominator != 1 or tot == 0 or b ** abs(tot.numerator) > 1000:
            return
        v = Fr(b) ** tot.numerator
        q = f"{n1}^{{{ex_str(e1)}}} {op} {n2}^{{{ex_str(e2)}}}의 값을 구하세요."
        same = f"{n1} = {b}^{{{k1}}}" + (f", {n2} = {b}^{{{k2}}}" if n2 != n1 else "")
        sgn = "+" if op == "×" else "−"
        lines = [L(same, memo="밑을 같게"),
                 L(f"({b}^{{{k1}}})^{{{ex_str(e1)}}} {op} ({b}^{{{k2}}})^{{{ex_str(e2)}}} = {b}^{{{ex_str(t1)}}} {op} {b}^{{{ex_str(t2)}}}"),
                 L(f"{b}^{{{ex_str(t1)} {sgn} {exq(t2)}}} = {b}^{{{N(tot)}}} = {N(v)}", memo="지수끼리 " + ("더하기" if op == "×" else "빼기"))]
        S.add(2, q, N(v), "밑을 같게 만든 뒤 지수끼리 계산해요", lines, ap=plain(N(v)))
    fill(S, 2, 20, g2)

    # 3단계 — 로그의 정의
    def g3():
        form = S.count(3) % 4
        if form == 0:
            b, n, k = pick()
            arg, argv, v = str(n), n, Fr(k)
            lines = [L(f"{n} = {b}^{{{k}}}", memo=f"{J(str(b), '을', '를')} 몇 제곱하면 {n}?"), L(f"log_{{{b}}} {n} = {k}")]
            sub = None
        elif form == 1:
            b, n, k = pick()
            arg, argv, v = f"{{1/{n}}}", sp.Rational(1, n), Fr(-k)
            lines = [L(f"{{1/{n}}} = {b}^{{{N(-k)}}}", memo="역수는 지수가 음수"), L(f"log_{{{b}}} {{1/{n}}} = {N(-k)}")]
            sub = None
        elif form == 2:
            b0 = R.choice([2, 3]); p = R.choice([2, 3]); qq = R.randint(1, 5)
            if qq % p == 0 or b0 ** p > 27 or b0 ** qq > 81:
                return
            b, n = b0 ** p, b0 ** qq
            arg, argv, v = str(n), n, Fr(qq, p)
            lines = [L(f"{b}^{{x}} = {n} 에서 {b0}^{{{p}x}} = {b0}^{{{qq}}}", memo="값을 x로 두고 정의대로"),
                     L(f"{p}x = {qq} → x = {N(v)}"), L(f"log_{{{b}}} {n} = {N(v)}")]
            sub = {"x": v}
        else:
            b, n, k = pick((2, 3, 5, 10), kmin=1)
            if k % 2 == 0 or b ** k > 125:
                return
            v = Fr(k, 2)
            arg, argv = f"√{{{n}}}", sp.sqrt(n)
            lines = [L(f"√{{{n}}} = {n}^{{1/2}}" if k == 1 else f"√{{{n}}} = ({b}^{{{k}}})^{{1/2}} = {b}^{{{ex_str(v)}}}", memo="거듭제곱근을 지수로"),
                     L(f"log_{{{b}}} {b}^{{{ex_str(v)}}} = {N(v)}")]
            sub = None
        assert logv(argv, b) == v, (b, arg, v)
        q = f"log_{{{b}}} {arg}의 값을 구하세요."
        S.add(3, q, N(v), "log_{a} N = x ⇔ a^{x} = N", lines, ap=plain(N(v)), sub=sub)
    fill(S, 3, 20, g3)

    # 4단계 — 로그의 성질
    def g4():
        form = S.count(4) % 4
        if form == 0:
            b = R.choice([6, 10, 12, 15]); k = R.choice([2, 2, 3])
            tot = b ** k
            pows = {b ** i for i in range(k + 1)}
            ds = [d for d in range(2, tot) if tot % d == 0 and d not in pows and tot // d not in pows and d <= 250 and tot // d <= 250]
            if not ds:
                return
            p = R.choice(ds)
            qq = tot // p
            ukey = f"{b}|{min(p, qq)}|{max(p, qq)}"
            q = f"log_{{{b}}} {p} + log_{{{b}}} {qq}의 값을 구하세요."
            lines = [L(f"log_{{{b}}} {p} + log_{{{b}}} {qq} = log_{{{b}}} ({p} × {qq})", memo="합 → 곱"),
                     L(f"log_{{{b}}} {tot} = log_{{{b}}} {b}^{{{k}}} = {k}")]
            v = Fr(k)
            assert abs(math.log(p, b) + math.log(qq, b) - k) < 1e-9
            if ukey in S.seen:
                return
            S.seen.add(ukey)
        elif form == 1:
            b = R.choice([2, 3, 5]); k = R.choice([2, 3, 4]); d = R.choice([3, 5, 6, 7, 10, 11])
            if b ** k > 81 or d % b == 0:
                return
            p = b ** k * d
            q = f"log_{{{b}}} {p} − log_{{{b}}} {d}의 값을 구하세요."
            lines = [L(f"log_{{{b}}} {p} − log_{{{b}}} {d} = log_{{{b}}} {{{p}/{d}}}", memo="차 → 몫"),
                     L(f"log_{{{b}}} {b ** k} = {k}")]
            v = Fr(k)
            assert abs(math.log(p, b) - math.log(d, b) - k) < 1e-9
        elif form == 2:
            a, bb = R.choice([(2, 3), (3, 2), (2, 5), (5, 2), (3, 5), (5, 3), (2, 7), (7, 2), (3, 7), (7, 3)])
            k = R.choice([2, 3, 4])
            if a ** k > 243:
                return
            q = f"log_{{{a}}} {bb} × log_{{{bb}}} {a ** k}의 값을 구하세요."
            lines = [L(f"log_{{{a}}} {bb} × log_{{{bb}}} {a ** k} = {{log {bb}/log {a}}} × {{log {a ** k}/log {bb}}}", memo="밑변환 — 밑을 10으로"),
                     L(f"= {{log {a ** k}/log {a}}} = {{{k} log {a}/log {a}}} = {k}", memo="log " + str(bb) + "끼리 약분")]
            v = Fr(k)
            assert abs(math.log(bb, a) * math.log(a ** k, bb) - k) < 1e-9
        else:
            b = R.choice([2, 3, 5]); m = R.choice([2, 2, 3]); u = R.choice([1, 1, 2]); t = R.choice([2, 3, 5, 6, 7])
            if t % b == 0:
                return
            p = b ** u * t
            if p > 60 or t ** m > 400 or p ** m > 1000:
                return
            qq = t ** m
            v = Fr(m * u)
            q = f"{m} log_{{{b}}} {p} − log_{{{b}}} {qq}의 값을 구하세요."
            lines = [L(f"{m} log_{{{b}}} {p} = log_{{{b}}} {p}^{{{m}}}", memo="앞의 수는 지수로"),
                     L(f"log_{{{b}}} {p}^{{{m}}} − log_{{{b}}} {qq} = log_{{{b}}} {{{p ** m}/{qq}}}"),
                     L(f"log_{{{b}}} {b ** (m * u)} = {N(v)}")]
            assert abs(m * math.log(p, b) - math.log(qq, b) - float(v)) < 1e-9
            assert Fr(p ** m, qq) == b ** (m * u)
        S.add(4, q, N(v), "곱 → 합 · 몫 → 차 · 거듭제곱 → 앞으로 · 밑변환", lines, ap=plain(N(v)))
    fill(S, 4, 20, g4)

    # 5단계 — 지수 · 로그 방정식
    def g5():
        form = S.count(5) % 4
        if form == 0:
            b, n, k = pick((2, 3, 5))
            if R.random() < 0.35:
                # (1/b)^x = n → b^{−x} = b^{k} → x = −k
                sol = Fr(-k)
                q = f"방정식 ({{1/{b}}})^{{x}} = {J(str(n), '을', '를')} 푸세요."
                lines = [L(f"({{1/{b}}})^{{x}} = {b}^{{−x}}, {n} = {b}^{{{k}}}", memo="밑을 같게"), L(f"−x = {k}"), L(f"x = {N(sol)}")]
            else:
                c = R.choice([-3, -2, -1, 1, 2, 3])
                sol = Fr(k - c)
                ex = f"x + {c}" if c > 0 else f"x − {-c}"
                q = f"방정식 {b}^{{{ex}}} = {J(str(n), '을', '를')} 푸세요."
                lines = [L(f"{n} = {b}^{{{k}}}", memo="밑을 같게"), L(f"{ex} = {k}", memo="지수끼리 같다"), L(f"x = {N(sol)}")]
        elif form == 1:
            b0 = R.choice([2, 3, 5]); p = R.choice([2, 3]); qq = R.randint(1, 5) * R.choice([1, 1, -1])
            if qq % p == 0 or b0 ** p > 27 or b0 ** abs(qq) > 243:
                return
            B = b0 ** p
            rhs = str(b0 ** qq) if qq > 0 else f"{{1/{b0 ** -qq}}}"
            sol = Fr(qq, p)
            q = f"방정식 {B}^{{x}} = {J(rhs, '을', '를')} 푸세요."
            lines = [L(f"({b0}^{{{p}}})^{{x}} = {b0}^{{{p}x}}, {rhs} = {b0}^{{{N(qq)}}}", memo="밑을 같게"),
                     L(f"{p}x = {N(qq)}"), L(f"x = {N(sol)}")]
        elif form == 2:
            b = R.choice([2, 3, 5]); m = R.randint(1, 3 if b < 5 else 2); c = R.choice([-4, -3, -2, -1, 1, 2, 3, 4, 5])
            sol = Fr(b ** m + c)
            inner = f"x − {c}" if c > 0 else f"x + {-c}"
            q = f"방정식 log_{{{b}}} ({inner}) = {J(str(m), '을', '를')} 푸세요."
            lines = [L(f"{inner} = {b}^{{{m}}} = {b ** m}", memo="로그의 정의"), L(f"x = {N(sol)}"),
                     L(f"진수 {inner} = {b ** m} > 0", memo="진수 조건 확인")]
        else:
            b = R.choice([2, 2, 3]); r = R.randint(1, 8); s_ = R.randint(1, 4)
            rhs = b ** s_
            if rhs > 64:
                return
            roots = sp.solve(x * (x - r) - rhs, x)
            if not all(t.is_integer for t in roots):
                return
            good = [int(t) for t in roots if t > r]
            bad = [int(t) for t in roots if t <= r]
            if len(good) != 1:
                return
            sol = Fr(good[0])
            r2 = bad[0]
            fac = f"(x − {good[0]})(x {'+' if r2 < 0 else '−'} {abs(r2)})" if r2 else f"x(x − {good[0]})"
            q = f"방정식 log_{{{b}}} x + log_{{{b}}} (x − {r}) = {J(str(s_), '을', '를')} 푸세요."
            lines = [L(f"log_{{{b}}} x(x − {r}) = {s_}", memo="합 → 곱"),
                     L(f"x(x − {r}) = {b}^{{{s_}}} = {rhs}", memo="로그의 정의"),
                     L(f"{P_(x * (x - r) - rhs)} = {fac} = 0"),
                     L(f"x = {N(sol)}", memo=f"x = {N(r2)}는 진수 조건(x > {r})에 맞지 않아요")]
        S.add(5, q, f"x = {N(sol)}", "밑을 같게 하거나 로그의 정의로 — 진수 조건 확인", lines, ap=plain(N(sol)), sub={"x": sol})
    fill(S, 5, 20, g5)
    return S


# ══════════ ② 미분 ══════════
def plane_for(f, fn, xr, box=(40, 40, 620, 640), extra_y=()):
    xr = (min(xr[0], -0.6), max(xr[1], 0.6))
    ys = [fn(xr[0] + (xr[1] - xr[0]) * i / 80) for i in range(81)] + list(extra_y) + [0]
    lo, hi = min(ys), max(ys)
    pad = (hi - lo) * 0.1 + 0.6
    P = Plane(f, xr, (lo - pad, hi + pad), box=box, square=False)
    P.axes(grid=0)
    return P

def subst(e, a):
    """다항식에 a 를 넣는 글자 — 3 × 2^{2} − 4 × 2 + 1"""
    Pl = sp.Poly(e, x)
    out = []
    for (k,), c in sorted(Pl.terms(), key=lambda t: -t[0][0]):
        c = int(c)
        if k == 0:
            body = str(abs(c))
        else:
            body = (f"{abs(c)} × " if abs(c) != 1 else "") + NP(a) + (f"^{{{k}}}" if k > 1 else "")
        if not out:
            out.append((MI if c < 0 else "") + body)
        else:
            out.append((" − " if c < 0 else " + ") + body)
    return "".join(out)

def pt_slope(m, t, ft):
    lhs = "y" if ft == 0 else (f"y − {ft}" if ft > 0 else f"y + {-ft}")
    if t == 0:
        rhs = lin(m, 0)
    else:
        inner = f"x − {t}" if t > 0 else f"x + {-t}"
        cm = "" if m == 1 else (MI if m == -1 else N(m))
        rhs = f"{cm}({inner})"
    return f"{lhs} = {rhs}"

def tline(m, b):
    return f"y = {lin(m, b)}" if m else f"y = {N(b)}"

def cubic(s, r1, r2, c):
    """f'(x) = 3s(x − r1)(x − r2) 인 삼차함수"""
    return s * (x ** 3 - sp.Rational(3, 2) * (r1 + r2) * x ** 2 + 3 * r1 * r2 * x) + c

def fac_str(s, r1, r2):
    def one(r):
        return "x" if r == 0 else (f"(x − {r})" if r > 0 else f"(x + {-r})")
    lead = "3" if s == 1 else "−3"
    parts = [one(r1), one(r2)]
    if r1 == 0 or r2 == 0:
        parts = ["x"] + [p for p in parts if p != "x"]
    return lead + "".join(parts)

def set_b():
    S = Set("b", "미분 — 접선의 기울기에서 극값까지", "미분",
            {1: "평균변화율", 2: "미분계수", 3: "접선의 방정식", 4: "극대 · 극소", 5: "닫힌구간의 최대 · 최소"},
            pp=6,
            tips={1: "평균변화율 = {f(b) − f(a)/b − a} — 두 점을 이은 직선의 기울기",
                  2: "(x^{n})' = nx^{n − 1}, 상수는 0 — f'(a)는 x = a에서 접선의 기울기",
                  3: "기울기 f'(a), 지나는 점 (a, f(a)) → y − f(a) = f'(a)(x − a)",
                  4: "f'(x) = 0인 x에서 부호가 + → − 이면 극대, − → + 이면 극소",
                  5: "극값과 구간 양 끝의 함숫값을 모두 비교해요"},
            note="미분계수는 ‘그 점에서 접선의 기울기’예요. 평균변화율(두 점을 이은 직선)의 두 점을 붙이면 접선이 된다는 그림을 먼저 보여 주고, 증감표는 f'(x)의 부호를 한 줄씩 채우게 해 주세요.")
    R = rng(2202)

    def rnd_poly(deg, lead=(1, 1, -1, 2)):
        cs = [R.choice(lead)] + [R.randint(-4, 4) for _ in range(deg)]
        return sum(c * x ** (deg - i) for i, c in enumerate(cs))

    # 1단계 — 평균변화율
    def g1():
        e = rnd_poly(R.choice([2, 2, 3]))
        a = R.randint(-2, 2); b = a + R.randint(1, 3)
        fa, fb = int(e.subs(x, a)), int(e.subs(x, b))
        v = Fr(fb - fa, b - a)
        fn = sp.lambdify(x, e)
        f = Fig()
        P = plane_for(f, fn, (a - 1.4, b + 1.4))
        P.curve(fn, at="q", c="sky", w=4.5)
        P.pt(a, fa, at=0, f="coral", r=9, label=f"({N(a)}, {N(fa)})", pos="nw", z=24, c="coral")
        P.pt(b, fb, at=0, f="coral", r=9, label=f"({N(b)}, {N(fb)})", pos="ne", z=24, c="coral", dl=200)
        P.lineq(float(v), float(fa - v * a), at=1, c="coral", w=3.5, d=True)
        q = f"함수 f(x) = {P_(e)}에서 x의 값이 {N(a)}에서 {N(b)}까지 변할 때의 평균변화율을 구하세요."
        lines = [L(f"f({N(b)}) = {N(fb)}, f({N(a)}) = {N(fa)}"),
                 L(f"{{{N(fb)} − {NP(fa)}/{N(b)} − {NP(a)}}} = {N(v)}", memo="두 점을 이은 직선의 기울기")]
        S.add(1, q, N(v), "(y의 증가량) ÷ (x의 증가량)", lines, f.out(), ap=plain(N(v)))
    fill(S, 1, 20, g1)

    # 2단계 — 미분계수
    def g2():
        e = rnd_poly(R.choice([2, 3, 3, 4]))
        a = R.choice([-2, -1, 1, 2, 3])
        d = sp.expand(sp.diff(e, x))
        v = int(d.subs(x, a))
        s_ = subst(d, a)
        num_eq(s_, v)
        fn = sp.lambdify(x, e)
        fa = float(e.subs(x, a))
        f = Fig()
        P = plane_for(f, fn, (a - 1.6, a + 1.6))
        P.curve(fn, at="q", c="sky", w=4.5)
        P.pt(a, fa, at="q", f="coral", r=9)
        P.lineq(float(v), fa - v * a, at=1, c="coral", w=3.5)
        q = f"함수 f(x) = {P_(e)}에 대하여 f'({N(a)})의 값을 구하세요."
        lines = [L(f"f'(x) = {P_(d)}", memo="(x^{n})' = nx^{n − 1}"), L(f"f'({N(a)}) = {s_} = {N(v)}", memo="x = " + N(a) + "에서 접선의 기울기")]
        S.add(2, q, N(v), "도함수를 구한 뒤 x = a를 넣어요", lines, f.out(), ap=plain(N(v)))
    fill(S, 2, 20, g2)

    # 3단계 — 접선의 방정식
    def g3():
        form = S.count(3) % 2
        if form == 0:
            e = rnd_poly(R.choice([2, 3]))
            t = R.randint(-2, 2)
            d = sp.expand(sp.diff(e, x))
            ft, m = int(e.subs(x, t)), int(d.subs(x, t))
            bb = ft - m * t
            q = f"곡선 y = {P_(e)} 위의 점 ({N(t)}, {N(ft)})에서의 접선의 방정식을 구하세요."
            s_ = subst(d, t)
            lines = [L(f"y' = {P_(d)}"), L(f"기울기 {s_} = {N(m)}", memo=f"x = {N(t)} 대입")]
            lines += [L(pt_slope(m, t, ft), memo="한 점과 기울기"), L(tline(m, bb))] if m else [L(tline(m, bb), memo="기울기 0 — x축에 평행")]
            sub = None
            pat = 1
        else:
            e = rnd_poly(2, lead=(1, 1, -1))
            d = sp.expand(sp.diff(e, x))
            t = R.randint(-2, 3)
            m = int(d.subs(x, t)); ft = int(e.subs(x, t)); bb = ft - m * t
            if m == 0:
                return
            q = f"곡선 y = {P_(e)}에 접하고 기울기가 {N(m)}인 직선의 방정식을 구하세요."
            lines = [L(f"y' = {P_(d)} = {N(m)}"), L(f"x = {N(t)}", memo="접점의 x좌표"), L(f"접점 ({N(t)}, {N(ft)})"),
                     L(pt_slope(m, t, ft)), L(tline(m, bb))]
            sub = {"x": t}
            pat = 2
        # 접선 검산
        assert sp.expand(e.subs(x, t) - (m * t + bb)) == 0 and sp.diff(e, x).subs(x, t) == m
        fn = sp.lambdify(x, e)
        f = Fig()
        P = plane_for(f, fn, (t - 2.2, t + 2.2))
        P.curve(fn, at="q", c="sky", w=4.5)
        P.pt(t, ft, at="q" if form == 0 else pat, f="coral", r=10, label=f"({N(t)}, {N(ft)})", pos="nw" if m > 0 else "ne", z=24, c="coral")
        P.lineq(float(m), float(bb), at=len(lines) - 1, c="coral", w=4)
        S.add(3, q, tline(m, bb), "기울기 = f'(a), 지나는 점 (a, f(a))", lines, f.out(), ap=plain(tline(m, bb)), omr="ex", sub=sub)
    fill(S, 3, 20, g3)

    def table(f, s, r1, r2, at_row=(1, 2, 2)):
        """증감표 — 아래 칸 (x0 40, y0 452)"""
        x0, y0, lw, cw, rh = 40, 452, 130, 90, 58
        W = lw + 5 * cw
        f.rect(x0, y0, W, rh * 3, at="p", c="ink", sw=2.5)
        for i in (1, 2):
            f.line(x0, y0 + rh * i, x0 + W, y0 + rh * i, at="p", c="ink", w=2)
        f.line(x0 + lw, y0, x0 + lw, y0 + rh * 3, at="p", c="ink", w=2)
        for i, lab in enumerate(["x", "f'(x)", "f(x)"]):
            f.text(x0 + lw / 2, y0 + rh * i + rh / 2 + 10, lab, z=26, at="p", c="ink")
        top = ["…", N(r1), "…", N(r2), "…"]
        sg = ["+", "0", MI, "0", "+"] if s == 1 else [MI, "0", "+", "0", MI]
        up, dn = "↗", "↘"
        fx = [up, "극대", dn, "극소", up] if s == 1 else [dn, "극소", up, "극대", dn]
        for row, vals in enumerate([top, sg, fx]):
            for j, t_ in enumerate(vals):
                f.text(x0 + lw + cw * j + cw / 2, y0 + rh * row + rh / 2 + 10, t_, z=26 if row != 2 or j % 2 == 0 else 22,
                       at=at_row[row], c="coral" if (row == 2 and j % 2 == 1) else "ink", dl=j * 120)

    # 4단계 — 극대 · 극소
    def g4():
        s = 1 if S.count(4) % 4 != 3 else -1
        r1 = R.randint(-3, 2); r2 = r1 + 2 * R.randint(1, 2)
        c = R.randint(-4, 4)
        e = sp.expand(cubic(s, r1, r2, c))
        if any(cc.q != 1 for cc in sp.Poly(e, x).coeffs()):
            return
        d = sp.expand(sp.diff(e, x))
        assert sp.expand(d - 3 * s * (x - r1) * (x - r2)) == 0
        v1, v2 = int(e.subs(x, r1)), int(e.subs(x, r2))
        mx_x, mn_x = (r1, r2) if s == 1 else (r2, r1)
        mx, mn = int(e.subs(x, mx_x)), int(e.subs(x, mn_x))
        want = "극댓값" if S.count(4) % 2 == 0 else "극솟값"
        at_x, v = (mx_x, mx) if want == "극댓값" else (mn_x, mn)
        fn = sp.lambdify(x, e)
        f = Fig()
        P = plane_for(f, fn, (r1 - 1.6, r2 + 1.6), box=(40, 30, 620, 410))
        P.curve(fn, at="q", c="sky", w=4.5)
        P.pt(mx_x, mx, at=3, f="coral", r=9, label=f"극대 {N(mx)}", pos="n", z=22, c="coral")
        P.pt(mn_x, mn, at=3, f="teal", r=9, label=f"극소 {N(mn)}", pos="s", z=22, c="teal", dl=200)
        table(f, s, r1, r2)
        q = f"함수 f(x) = {P_(e)}의 {J(want, '을', '를')} 구하세요."
        lines = [L(f"f'(x) = {P_(d)} = {fac_str(s, r1, r2)}"),
                 L(f"f'(x) = 0 → x = {N(r1)} 또는 x = {N(r2)}"),
                 L((f"x = {N(r1)}: + → −, x = {N(r2)}: − → +") if s == 1 else (f"x = {N(r1)}: − → +, x = {N(r2)}: + → −"), memo="f'(x)의 부호 — 증감표"),
                 L(f"{want} f({N(at_x)}) = {N(v)}")]
        S.add(4, q, N(v), "f'(x) = 0인 x에서 부호가 바뀌는 쪽을 봐요", lines, f.out(), ap=plain(N(v)))
    fill(S, 4, 20, g4)

    # 5단계 — 닫힌구간의 최대 · 최소
    def g5():
        s = 1 if S.count(5) % 3 != 2 else -1
        r1 = R.randint(-2, 1); r2 = r1 + 2
        c = R.randint(-4, 4)
        e = sp.expand(cubic(s, r1, r2, c))
        if any(cc.q != 1 for cc in sp.Poly(e, x).coeffs()):
            return
        lo = r1 - R.randint(0, 2); hi = r2 + R.randint(0, 2)
        if lo == r1 and hi == r2:
            return
        cand = sorted({lo, hi, r1, r2})
        vals = [(t, int(e.subs(x, t))) for t in cand]
        want = "최댓값" if S.count(5) % 2 == 0 else "최솟값"
        v = max(w for _, w in vals) if want == "최댓값" else min(w for _, w in vals)
        if sum(1 for _, w in vals if w == v) > 1:
            return
        # 답이 극값만으로 정해지지 않는 것(끝값과 비교해야 하는 것)을 섞는다
        d = sp.expand(sp.diff(e, x))
        fn = sp.lambdify(x, e)
        f = Fig()
        ys = [w for _, w in vals]
        P = plane_for(f, fn, (lo - 0.5, hi + 0.5), extra_y=ys)
        P.curve(fn, at="q", c="soft", w=2.5, d=True)
        P.curve(fn, x0=lo, x1=hi, at="q", c="sky", w=5)
        for t in (lo, hi):
            f.line(P.X(t), P.Y(P.yr[0]), P.X(t), P.Y(P.yr[1]), at="q", c="soft", w=2, d=True)
        mean = sum(ys) / len(ys)
        for i, (t, w) in enumerate(vals):
            P.pt(t, w, at=2, f="ink", r=7, label=N(w), pos="n" if w >= mean else "s", z=22, c="ink", dl=i * 150)
        bt = [t for t, w in vals if w == v][0]
        P.pt(bt, v, at=3, f="gold", r=13)
        q = f"닫힌구간 [{N(lo)}, {N(hi)}]에서 함수 f(x) = {P_(e)}의 {J(want, '을', '를')} 구하세요."
        lines = [L(f"f'(x) = {P_(d)} = {fac_str(s, r1, r2)}"),
                 L(f"f'(x) = 0 → x = {N(r1)} 또는 x = {N(r2)}"),
                 L(", ".join(f"f({N(t)}) = {N(w)}" for t, w in vals), memo="극값과 양 끝값"),
                 L(f"{want} {N(v)} (x = {N(bt)})")]
        S.add(5, q, N(v), "극값과 구간 양 끝의 함숫값을 모두 비교해요", lines, f.out(), ap=plain(N(v)))
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "h2", "grade": "고2", "level": "고등", "icon": "📉", "title": "고2 · 지수와 로그 · 미분",
         "desc": "지수와 로그 — 정의에서 성질까지 100제 · 미분 — 접선의 기울기에서 극값까지 100제(할선 · 접선 · 증감표가 그래프 위에).",
         "thumb": ("b", 70), "sets": [set_a, set_b]}
