# 중2 — ① 지수법칙과 단항식의 계산 · ② 연립일차방정식 — 가감법 · 대입법 (해 = 두 직선의 교점)
from math import gcd
from core import *
from fig import Fig, Plane

def F_(n, d):
    return "{%d/%d}" % (n, d)

V = {"a": SYMS["a"], "b": SYMS["b"], "x": SYMS["x"], "y": SYMS["y"]}

def mstr(c, pw):
    return monom(c, pw, order="abxy")

# ══════════ ① 지수법칙 ══════════
def set_a():
    S = Set("a", "지수법칙과 단항식의 계산", "지수법칙",
            {1: "aᵐ × aⁿ", 2: "(aᵐ)ⁿ · (ab)ⁿ", 3: "aᵐ ÷ aⁿ", 4: "단항식의 곱셈 · 나눗셈", 5: "단항식의 혼합 계산"},
            pp=10,
            tips={1: "밑이 같은 거듭제곱의 곱 → 지수끼리 더해요: a^{m} × a^{n} = a^{m + n}",
                  2: "거듭제곱의 거듭제곱 → 지수끼리 곱해요: (a^{m})^{n} = a^{mn}, (ab)^{n} = a^{n}b^{n}",
                  3: "a^{m} ÷ a^{n} → 지수끼리 빼요 (같으면 1, 나누는 쪽이 크면 {1/a^{n − m}})",
                  4: "계수끼리, 문자끼리 계산해요 — 나눗셈은 분수 꼴이나 역수의 곱으로",
                  5: "거듭제곱 먼저, 나눗셈은 역수의 곱으로 바꾸어 앞에서부터"},
            note="지수법칙은 ‘곱하는 개수 세기’로 설명하면 외우지 않아도 돼요. x^{3} × x^{4} = (x × x × x) × (x × x × x × x)처럼 한 번은 늘어놓아 보게 해 주세요.")
    R = rng(1201)
    VS = ["a", "x", "y", "b"]

    def g1():
        k = S.count(1) % 3
        if k < 2:
            v = R.choice(VS); m, n = R.randint(2, 6), R.randint(2, 6)
            if k == 0:
                q = f"{v}^{{{m}}} × {v}^{{{n}}}"
                lines = [L("밑이 같으면 지수끼리 더해요", memo=f"{v}를 {m}번, 또 {n}번 곱해요"), L(f"{q} = {v}^{{{m} + {n}}} = {v}^{{{m + n}}}")]
                ans = f"{v}^{{{m + n}}}"
            else:
                u = "b" if v != "b" else "y"
                p = R.randint(1, 4)
                q = f"{v}^{{{m}}} × {u}^{{{p}}} × {v}^{{{n}}}"
                lines = [L(f"{v}끼리 {v}^{{{m} + {n}}} = {v}^{{{m + n}}}", memo="밑이 같은 것끼리"), L(f"{q} = {v}^{{{m + n}}}{u}" + (f"^{{{p}}}" if p > 1 else ""))]
                ans = f"{v}^{{{m + n}}}{u}" + (f"^{{{p}}}" if p > 1 else "")
        else:
            b = R.choice([2, 3, 5]); m, n = R.randint(2, 6), R.randint(2, 6)
            q = f"{b}^{{{m}}} × {b}^{{{n}}}"
            lines = [L("밑이 같으면 지수끼리 더해요"), L(f"{q} = {b}^{{{m} + {n}}} = {b}^{{{m + n}}}")]
            ans = f"{b}^{{{m + n}}}"
        S.add(1, f"{J(q, '을', '를')} 간단히 하세요.", ans, "a^{m} × a^{n} = a^{m + n}", lines, None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        v = R.choice(VS)
        if k == 0:
            m, n = R.randint(2, 5), R.randint(2, 5)
            q = f"({v}^{{{m}}})^{{{n}}}"
            lines = [L("거듭제곱의 거듭제곱 → 지수끼리 곱해요"), L(f"{q} = {v}^{{{m} × {n}}} = {v}^{{{m * n}}}")]
            ans = f"{v}^{{{m * n}}}"
        elif k == 1:
            c = R.choice([2, 3, -2, -3, 5]); m, n = R.randint(1, 4), R.randint(2, 3)
            inside = mstr(c, {v: m})
            q = f"({inside})^{{{n}}}"
            ans = mstr(c ** n, {v: m * n})
            lines = [L("괄호 안 각각을 거듭제곱해요", memo="(ab)^{n} = a^{n}b^{n}"), L(f"{q} = {NP(c)}^{{{n}}} × ({v}" + (f"^{{{m}}}" if m > 1 else "") + f")^{{{n}}}"), L(f"= {ans}" if False else f"{NP(c)}^{{{n}}} × {v}^{{{m * n}}} = {ans}")]
        else:
            u = "y" if v != "y" else "b"
            m, p, n = R.randint(1, 3), R.randint(1, 3), R.randint(2, 4)
            q = f"({{{v}" + (f"^{{{m}}}" if m > 1 else "") + f"/{u}" + (f"^{{{p}}}" if p > 1 else "") + f"}})^{{{n}}}"
            ans = f"{{{v}^{{{m * n}}}/{u}^{{{p * n}}}}}"
            lines = [L("분자 · 분모를 각각 거듭제곱해요"), L(f"{q} = {ans}")]
        S.add(2, f"{J(q, '을', '를')} 간단히 하세요.", ans, "지수끼리 곱해요", lines, None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 2, 20, g2)

    def g3():
        v = R.choice(VS); m, n = R.randint(1, 9), R.randint(1, 9)
        k = S.count(3) % 3
        if k == 0 and m <= n:
            return
        if k == 1 and m != n:
            m = n
        if k == 2 and m >= n:
            return
        q = f"{v}^{{{m}}} ÷ {v}^{{{n}}}"
        if m > n:
            ans = f"{v}^{{{m - n}}}" if m - n > 1 else v
            lines = [L(f"{q} = {v}^{{{m} − {n}}} = {ans}", memo="지수끼리 빼요")]
        elif m == n:
            ans = "1"
            lines = [L("같은 것끼리 나누면 1", memo="지수가 같아요"), L(f"{q} = 1")]
        else:
            ans = f"{{1/{v}" + (f"^{{{n - m}}}" if n - m > 1 else "") + "}"
            lines = [L("나누는 쪽 지수가 더 커요", memo="분모에 남아요"), L(f"{q} = {{1/{v}^{{{n} − {m}}}}} = {ans}")]
        lines.insert(0, L(f"{q} = {{{v}^{{{m}}}/{v}^{{{n}}}}}", memo="분수 꼴로"))
        S.add(3, f"{J(q, '을', '를')} 간단히 하세요.", ans, "a^{m} ÷ a^{n} — 지수의 크기를 비교해요", lines, None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 3, 20, g3)

    def rand_mono(vs=("a", "b")):
        c = R.choice([1, 2, 3, 4, 5, 6, -1, -2, -3, -4])
        pw = {v: R.randint(0, 3) for v in vs}
        if not any(pw.values()):
            pw[vs[0]] = 1
        return c, pw

    def g4():
        vs = ("a", "b") if S.count(4) % 2 == 0 else ("x", "y")
        if S.count(4) < 10:
            c1, p1 = rand_mono(vs); c2, p2 = rand_mono(vs)
            c, pw = c1 * c2, {v: p1[v] + p2[v] for v in vs}
            A, B = mstr(c1, p1), mstr(c2, p2)
            q = f"{A} × " + (f"({B})" if B.startswith(MI) else B)
            ans = mstr(c, pw)
            def ex(v):
                a_, b_ = p1[v], p2[v]
                if a_ and b_:
                    return f"{v}^{{{a_} + {b_}}}"
                e = a_ or b_
                return "" if not e else (v if e == 1 else f"{v}^{{{e}}}")
            lines = [L(f"계수끼리 {N(c1)} × {NP(c2)} = {N(c)}"), L("문자끼리 " + "".join(ex(v) for v in vs), memo="지수끼리 더해요"),
                     L(f"{q} = {ans}")]
        else:
            c2, p2 = rand_mono(vs)
            cq = R.choice([1, 2, 3, -2, -3, 4])
            pq = {v: R.randint(0, 3) for v in vs}
            c1 = c2 * cq
            p1 = {v: p2[v] + pq[v] for v in vs}
            A, B = mstr(c1, p1), mstr(c2, p2)
            q = f"{A} ÷ " + (f"({B})" if B.startswith(MI) else B)
            ans = mstr(cq, pq)
            lines = [L(f"{q} = {{{A}/{B}}}", memo="분수 꼴로"), L(f"계수 {N(c1)} ÷ {NP(c2)} = {N(cq)}, 문자는 지수끼리 빼요"), L(f"= {ans}" if False else f"{{{A}/{B}}} = {ans}")]
        S.add(4, f"{J(q, '을', '를')} 간단히 하세요.", ans, "계수끼리, 문자끼리 계산해요", lines, None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 4, 20, g4)

    def g5():
        vs = ("a", "b") if S.count(5) % 2 == 0 else ("x", "y")
        c0 = R.choice([-2, 2, -3, 3]); p0 = {vs[0]: R.randint(1, 2), vs[1]: R.randint(0, 1)}
        n = 2 if abs(c0) == 3 else R.choice([2, 3])
        A = mstr(c0, p0)
        Ac, Ap = c0 ** n, {v: p0[v] * n for v in vs}
        c2 = R.choice([2, 3, 4, 6]); p2 = {v: R.randint(0, Ap[v]) for v in vs}
        c3 = R.choice([1, 2, 3, -1]); p3 = {v: R.randint(0, 2) for v in vs}
        cres = Fr(Ac, c2) * c3
        if cres.denominator != 1:
            return
        pres = {v: Ap[v] - p2[v] + p3[v] for v in vs}
        B, C = mstr(c2, p2), mstr(c3, p3)
        if not B or B == "1":
            return
        q = f"({A})^{{{n}}} ÷ {B} × " + (f"({C})" if C.startswith(MI) else C)
        ans = mstr(cres, pres)
        lines = [L(f"({A})^{{{n}}} = {mstr(Ac, Ap)}", memo="거듭제곱 먼저"), L(f"÷ {B} → × {{1/{B}}}", memo="역수의 곱으로"),
                 L(f"{mstr(Ac, Ap)} × {{1/{B}}} × " + (f"({C})" if C.startswith(MI) else C) + f" = {ans}")]
        S.add(5, f"{J(q, '을', '를')} 간단히 하세요.", ans, "거듭제곱 → 나눗셈은 역수의 곱 → 앞에서부터", lines, None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ ② 연립방정식 ══════════
def eq_str(a, b, c):
    return f"{mono(a, 'x', 1, True)}{mono(b, 'y')} = {N(c)}"

def graph(f, sysm, sol, ans_at):
    (a1, b1, c1), (a2, b2, c2) = sysm
    x0, y0 = sol
    r = max(abs(x0), abs(y0)) + 3
    r = max(r, 5)
    P = Plane(f, (-r, r), (-r, r), box=(40, 40, 620, 640))
    P.axes(grid=1 if r <= 8 else 2, lab_step=None)
    for (a, b, c), col, nm in (((a1, b1, c1), "sky", "①"), ((a2, b2, c2), "lilac", "②")):
        if b == 0:
            continue
        m, k = Fr(-a, b), Fr(c, b)
        el = P.lineq(float(m), float(k), at="q", c=col, w=4)
    P.pt(x0, y0, at=ans_at, f="coral", r=11, label=f"({N(x0)}, {N(y0)})", pos="ne" if x0 < r - 3 else "nw", z=30, c="coral")
    f.text(70, 80, "①", z=34, c="sky", a="s", b=800)
    f.text(120, 80, "②", z=34, c="lilac", a="s", b=800)

def elim(E1, E2, sol):
    """두 식에서 y 를 없애는 판서 — 곱해서 맞추고 더하거나 뺀다"""
    (a1, b1, c1), (a2, b2, c2) = E1, E2
    x0, y0 = sol
    g = gcd(abs(b1), abs(b2))
    m1, m2 = abs(b2) // g, abs(b1) // g
    out = []
    A1, B1, C1 = a1 * m1, b1 * m1, c1 * m1
    A2, B2, C2 = a2 * m2, b2 * m2, c2 * m2
    if m1 != 1:
        out.append(L(f"① × {m1}: {eq_str(A1, B1, C1)}"))
    if m2 != 1:
        out.append(L(f"② × {m2}: {eq_str(A2, B2, C2)}"))
    if B1 == B2:
        out.append(L(f"빼면 {mono(A1 - A2, 'x', 1, True)} = {N(C1 - C2)}", memo="y가 없어져요"))
    else:
        out.append(L(f"더하면 {mono(A1 + A2, 'x', 1, True)} = {N(C1 + C2)}", memo="y가 없어져요"))
    out.append(L(f"x = {N(x0)} → y = {N(y0)}"))
    return out

def set_b():
    S = Set("b", "연립일차방정식 — 가감법과 대입법", "연립방정식",
            {1: "가감법 — 바로 없애기", 2: "가감법 — 곱해서 맞추기", 3: "대입법", 4: "괄호 · 분수 · 소수가 있는 연립방정식", 5: "연립방정식의 활용"},
            pp=6,
            tips={1: "한 문자의 계수가 같으면 빼고, 부호만 다르면 더해서 없애요",
                  2: "계수의 최소공배수를 맞추도록 식에 같은 수를 곱한 뒤 더하거나 빼요",
                  3: "y = (x의 식) 꼴이면 다른 식의 y 자리에 그대로 넣어요",
                  4: "괄호는 풀고, 분수는 분모의 최소공배수를, 소수는 10을 곱해 계수를 정수로",
                  5: "구하는 두 수를 x, y로 놓고 조건 두 개로 식 두 개"},
            note="연립방정식의 해는 두 직선의 교점이에요. 그림에서 두 직선이 만나는 점이 답과 같은지 확인하게 하면 2학기 일차함수와 이어져요.")
    R = rng(1202)

    def pick_sol():
        return R.randint(-4, 6), R.randint(-4, 6)

    def solve_lines_elim(e1, e2, sol, which):
        (a1, b1, c1), (a2, b2, c2) = e1, e2
        x0, y0 = sol
        lines = []
        if which == "y":
            if b1 == b2:
                lines.append(L(f"① − ②: {mono(a1 - a2, 'x', 1, True)} = {N(c1 - c2)}", memo="y가 없어져요"))
                k = a1 - a2
            else:
                lines.append(L(f"① + ②: {mono(a1 + a2, 'x', 1, True)} = {N(c1 + c2)}", memo="y가 없어져요"))
                k = a1 + a2
            lines.append(L(f"x = {N(x0)}"))
            lines.append(L(f"①에 대입: {mono(b1, 'y', 1, True)} = {N(c1)} − {NP(a1 * x0)}" if a1 != 1 else f"①에 대입: {N(x0)}{mono(b1, 'y')} = {N(c1)}"))
            lines.append(L(f"y = {N(y0)}"))
        else:
            if a1 == a2:
                lines.append(L(f"① − ②: {mono(b1 - b2, 'y', 1, True)} = {N(c1 - c2)}", memo="x가 없어져요"))
            else:
                lines.append(L(f"① + ②: {mono(b1 + b2, 'y', 1, True)} = {N(c1 + c2)}", memo="x가 없어져요"))
            lines.append(L(f"y = {N(y0)}"))
            lines.append(L(f"①에 대입: {mono(a1, 'x', 1, True)} = {N(c1)} − {NP(b1 * y0)}"))
            lines.append(L(f"x = {N(x0)}"))
        return lines

    def g1():
        x0, y0 = pick_sol()
        which = "y" if S.count(1) % 2 == 0 else "x"
        if which == "y":
            b = R.choice([1, 2, 3]); a1, a2 = R.randint(1, 4), R.choice([-3, -2, -1, 1, 2, 3])
            b2 = b if R.random() < 0.5 else -b
            if a1 == (a2 if b2 == b else -a2):
                return
            e1, e2 = (a1, b, a1 * x0 + b * y0), (a2, b2, a2 * x0 + b2 * y0)
        else:
            a = R.choice([1, 2, 3]); b1, b2 = R.randint(1, 4), R.choice([-3, -2, -1, 1, 2, 3])
            a2 = a if R.random() < 0.5 else -a
            if b1 == (b2 if a2 == a else -b2):
                return
            e1, e2 = (a, b1, a * x0 + b1 * y0), (a2, b2, a2 * x0 + b2 * y0)
        if (a1 if which == "y" else e1[0]) == 0:
            return
        f = Fig()
        graph(f, (e1, e2), (x0, y0), "a")
        lines = solve_lines_elim(e1, e2, (x0, y0), which)
        q = f"연립방정식 ① {eq_str(*e1)}, ② {J(eq_str(*e2), '을', '를')} 푸세요."
        S.add(1, q, f"x = {N(x0)}, y = {N(y0)}", f"{'y' if which == 'y' else 'x'}의 계수가 {'같으면 빼고' if (e1[1] == e2[1] if which == 'y' else e1[0] == e2[0]) else '부호만 다르면 더해'} 없애요",
              lines, f.out(), ap=f"x={x0}, y={y0}", omr="ex", sub={"x": x0, "y": y0}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        x0, y0 = pick_sol()
        a1, b1 = R.choice([1, 2, 3, 4, 5]), R.choice([-3, -2, 2, 3, 4, 5])
        a2, b2 = R.choice([1, 2, 3, 4, 5]), R.choice([-3, -2, 1, 2, 3])
        if a1 * b2 - a2 * b1 == 0 or b1 == b2 or b1 == -b2 or a1 == a2:
            return
        e1, e2 = (a1, b1, a1 * x0 + b1 * y0), (a2, b2, a2 * x0 + b2 * y0)
        # y 를 없앤다: ① × |b2|, ② × |b1|
        m1, m2 = abs(b2) // gcd(abs(b1), abs(b2)), abs(b1) // gcd(abs(b1), abs(b2))
        E1 = (a1 * m1, b1 * m1, e1[2] * m1)
        E2 = (a2 * m2, b2 * m2, e2[2] * m2)
        same = E1[1] == E2[1]
        k = E1[0] - E2[0] if same else E1[0] + E2[0]
        kc = E1[2] - E2[2] if same else E1[2] + E2[2]
        if k == 0:
            return
        lines = []
        if m1 != 1:
            lines.append(L(f"① × {m1}: {eq_str(*E1)}"))
        if m2 != 1:
            lines.append(L(f"② × {m2}: {eq_str(*E2)}"))
        lines.append(L(f"{'빼면' if same else '더하면'} {mono(k, 'x', 1, True)} = {N(kc)}", memo="y의 계수를 맞췄어요"))
        lines.append(L(f"x = {N(x0)} → ①에서 y = {N(y0)}"))
        f = Fig()
        graph(f, (e1, e2), (x0, y0), "a")
        q = f"연립방정식 ① {eq_str(*e1)}, ② {J(eq_str(*e2), '을', '를')} 푸세요."
        S.add(2, q, f"x = {N(x0)}, y = {N(y0)}", "y의 계수의 절댓값을 같게 만들어요", lines, f.out(), ap=f"x={x0}, y={y0}", omr="ex", sub={"x": x0, "y": y0}, key=q)
    fill(S, 2, 20, g2)

    def g3():
        x0, y0 = pick_sol()
        m = R.choice([-3, -2, -1, 1, 2, 3]); k0 = y0 - m * x0
        a2, b2 = R.choice([1, 2, 3, 4]), R.choice([-3, -2, -1, 1, 2, 3])
        if a2 + b2 * m == 0 or abs(k0) > 12:
            return
        c2 = a2 * x0 + b2 * y0
        e1 = (-m, 1, k0)
        q = f"연립방정식 ① y = {lin(m, k0)}, ② {J(eq_str(a2, b2, c2), '을', '를')} 푸세요."
        lines = [L(f"①을 ②에 대입: {mono(a2, 'x', 1, True)}{' + ' if b2 > 0 else ' − '}{abs(b2) if abs(b2) != 1 else ''}({lin(m, k0)}) = {N(c2)}", memo="y 자리에 그대로"),
                 L(f"{lin(a2 + b2 * m, b2 * k0)} = {N(c2)}"), L(f"{mono(a2 + b2 * m, 'x', 1, True)} = {N(c2 - b2 * k0)} → x = {N(x0)}"),
                 L(f"y = {lin(m, k0).replace('x', '×' + NP(x0)) if False else ''}" if False else f"y = {N(m)} × {NP(x0)} {'+' if k0 >= 0 else '−'} {abs(k0)} = {N(y0)}")]
        f = Fig()
        graph(f, (e1, (a2, b2, c2)), (x0, y0), "a")
        S.add(3, q, f"x = {N(x0)}, y = {N(y0)}", "y = (x의 식)을 다른 식에 대입해요", lines, f.out(), ap=f"x={x0}, y={y0}", omr="ex", sub={"x": x0, "y": y0}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        x0, y0 = pick_sol()
        k = S.count(4) % 2
        if k == 0:
            # ① p(x + q) + y = r 꼴 · ② 보통 식
            p, qq = R.choice([2, 3]), R.choice([-2, -1, 1, 2])
            r = p * (x0 + qq) + y0
            a2, b2 = R.choice([1, 2]), R.choice([-1, 1, 2])
            if p * b2 == a2:
                return
            c2 = a2 * x0 + b2 * y0
            q = f"연립방정식 ① {p}({lin(1, qq)}) + y = {N(r)}, ② {J(eq_str(a2, b2, c2), '을', '를')} 푸세요."
            E1 = (p, 1, r - p * qq)
            lines = [L(f"① 괄호 풀기: {eq_str(*E1)}", memo="분배법칙")]
        else:
            d1 = R.choice([2, 3, 4]); d2 = R.choice([2, 3, 6])
            # ① x/d1 + y/d2 = s
            s = Fr(x0, d1) + Fr(y0, d2)
            if s.denominator != 1:
                return
            m = d1 * d2 // gcd(d1, d2)
            a2, b2 = R.choice([1, 2]), R.choice([-1, 1])
            c2 = a2 * x0 + b2 * y0
            q = f"연립방정식 ① {{x/{d1}}} + {{y/{d2}}} = {N(s)}, ② {J(eq_str(a2, b2, c2), '을', '를')} 푸세요."
            E1 = (m // d1, m // d2, s.numerator * m)
            if E1[0] * b2 - E1[1] * a2 == 0:
                return
            lines = [L(f"① × {m}: {eq_str(*E1)}", memo="분모의 최소공배수")]
        lines += elim(E1, (a2, b2, c2), (x0, y0))
        f = Fig()
        graph(f, (E1, (a2, b2, c2)), (x0, y0), "a")
        S.add(4, q, f"x = {N(x0)}, y = {N(y0)}", "먼저 계수를 정수로 정리해요", lines, f.out(), ap=f"x={x0}, y={y0}", omr="ex", sub={"x": x0, "y": y0}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        if k == 0:
            x0 = R.randint(3, 12); y0 = R.randint(3, 12)
            if x0 == y0:
                return
            n, legs = x0 + y0, 2 * x0 + 4 * y0
            q = f"닭과 토끼가 모두 {n}마리 있고, 다리는 모두 {legs}개예요. 닭은 몇 마리인가요?"
            lines = [L("닭 x마리, 토끼 y마리"), L(f"x + y = {n}, 2x + 4y = {legs}"), L(f"① × 2 − ②: −2y = {N(2 * n - legs)}"), L(f"y = {y0} → x = {x0}")]
            S.add(5, q, f"{x0}마리", "마리 수 · 다리 수로 식 두 개", lines, None, ap=str(x0), sub={"x": x0, "y": y0}, key=q)
        elif k == 1:
            p1, p2 = R.choice([(500, 800), (700, 1000), (1200, 1500), (300, 600)])
            x0, y0 = R.randint(2, 9), R.randint(2, 9)
            n, T = x0 + y0, p1 * x0 + p2 * y0
            q = f"한 개에 {com(p1)}원인 연필과 {com(p2)}원인 볼펜을 모두 {n}자루 사고 {com(T)}원을 냈어요. 볼펜은 몇 자루인가요?"
            lines = [L("연필 x자루, 볼펜 y자루"), L(f"x + y = {n}, {p1}x + {p2}y = {T}"), L(f"② − ① × {p1}: {mono(p2 - p1, 'y', 1, True)} = {N(T - p1 * n)}"), L(f"y = {y0} → x = {x0}")]
            S.add(5, q, f"{y0}자루", "개수 · 금액으로 식 두 개", lines, None, ap=str(y0), sub={"x": x0, "y": y0}, key=q)
        elif k == 2:
            x0, y0 = R.randint(10, 60), R.randint(5, 50)
            if x0 <= y0:
                return
            s, d = x0 + y0, x0 - y0
            q = f"두 수의 합은 {s}이고 차는 {d}예요. 큰 수를 구하세요." if not str(d)[-1] in "013678" else f"두 수의 합은 {s}이고 차는 {d}이에요. 큰 수를 구하세요."
            q = q.replace(f"합은 {s}이고", f"합은 {s}이고" if str(s)[-1] in "013678" else f"합은 {s}이고")
            lines = [L("큰 수 x, 작은 수 y"), L(f"x + y = {s}, x − y = {d}"), L(f"더하면 2x = {s + d} → x = {x0}")]
            S.add(5, q, str(x0), "합과 차를 더하면 큰 수의 2배", lines, None, sub={"x": x0, "y": y0}, key=q)
        else:
            a, b = R.choice([(3, 4), (4, 5), (2, 3), (3, 5), (4, 6)])
            x0, y0 = R.randint(1, 6), R.randint(1, 6)
            D, T = a * x0 + b * y0, x0 + y0
            q = f"집에서 공원까지 {D} km를 가는데, 처음에는 시속 {a} km로 걷다가 나중에는 시속 {b} km로 걸어서 모두 {T}시간이 걸렸어요. 시속 {b} km로 걸은 거리는 몇 km인가요?"
            lines = [L(f"시속 {a} km로 x시간, 시속 {b} km로 y시간"), L(f"x + y = {T}, {a}x + {b}y = {D}"), L(f"② − ① × {a}: {mono(b - a, 'y', 1, True)} = {N(D - a * T)}"), L(f"y = {y0} → 거리 {b} × {y0} = {b * y0}")]
            S.add(5, q, f"{b * y0} km", "시간 · 거리로 식 두 개 — 거리 = 속력 × 시간", lines, None, ap=str(b * y0), sub={"x": x0, "y": y0}, key=q)
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "m2", "grade": "중2", "level": "중등", "icon": "🔗", "title": "중2 · 지수법칙 · 연립방정식",
         "desc": "지수법칙과 단항식의 계산 100제 · 연립일차방정식 100제(가감법 · 대입법 — 해는 두 직선의 교점으로 확인).",
         "thumb": ("b", 30), "sets": [set_a, set_b]}
