# 고1 — ① 나머지정리와 조립제법 · ② 이차방정식과 이차함수 — 판별식으로 읽기
from math import gcd
from core import *
from fig import Fig, mv, Plane

x = SYMS["x"]; k_ = SYMS["k"]; a_ = SYMS["a"]

def P_(e):
    return sym_poly_str(e)

def synth_fig(f, coeffs, r, at0=0, at_rows=None):
    """조립제법 표 — at_rows[i]: i 번째 열이 채워지는 판서 줄"""
    n = len(coeffs)
    dx = 110 if n <= 4 else 96
    X0 = 200
    xs = [X0 + i * dx for i in range(n)]
    yc, yp, yq = 210, 300, 400
    f.text(110, yc + 12, N(r), z=40, c="coral", at=at0, b=800)
    f.line(160, yc - 50, 160, yp + 30, c="ink", w=3)
    f.line(160, yp + 34, xs[-1] + 60, yp + 34, c="ink", w=3)
    for i, c in enumerate(coeffs):
        f.text(xs[i], yc + 12, N(c), z=38, b=700)
    q = [coeffs[0]]
    for i in range(1, n):
        q.append(coeffs[i] + q[-1] * r)
    f.text(xs[0], yq + 12, N(q[0]), z=38, c="teal", at=at_rows[0], b=700)
    f.line(xs[0], yc + 30, xs[0], yq - 30, c="teal", w=3, ar=1, at=at_rows[0], dr=True)
    for i in range(1, n):
        p = q[i - 1] * r
        at = at_rows[i]
        f.line(xs[i - 1] + 18, yq - 26, xs[i] - 18, yp + 22, c="red", w=2.5, ar=1, at=at, dr=True)
        f.text(xs[i], yp + 12, N(p), z=34, c="red", at=at, b=700, dl=250)
        f.text(xs[i], yq + 12, N(q[i]), z=38, c="teal" if i < n - 1 else "coral", at=at, b=700, dl=550)
    f.rect(xs[-1] - 46, yq - 34, 92, 64, c="coral", sw=3, rx=8, at=at_rows[-1], dl=700)
    f.text((xs[0] + xs[-2]) / 2 if n > 2 else xs[0], yq + 80, "몫의 계수", z=26, c="teal", at=at_rows[-1], dl=800)
    f.text(xs[-1], yq + 80, "나머지", z=26, c="coral", at=at_rows[-1], dl=800)
    return q

def synth_lines(coeffs, r, base=0):
    q = [coeffs[0]]
    lines = [L(f"{N(q[0])} 내려쓰기", memo="첫 계수 그대로")]
    for i in range(1, len(coeffs)):
        p = q[-1] * r
        q.append(coeffs[i] + p)
        lines.append(L(f"{NP(q[-2])} × {NP(r)} = {N(p)} → {N(coeffs[i])} + {NP(p)} = {N(q[-1])}"))
    return lines, q

def set_a():
    S = Set("a", "나머지정리와 조립제법", "나머지정리",
            {1: "A = BQ + R", 2: "나머지정리", 3: "인수정리 · 미정계수", 4: "조립제법", 5: "삼차식의 인수분해"},
            pp=6,
            tips={1: "(나뉠 식) = (나누는 식) × (몫) + (나머지), 나머지의 차수 < 나누는 식의 차수",
                  2: "f(x)를 x − a로 나눈 나머지 = f(a) — 나누지 않고 대입만",
                  3: "x − a로 나누어떨어지면 f(a) = 0",
                  4: "x − a로 나눌 때 a를 왼쪽에: 내려쓰기 → a를 곱해 다음 칸에 더하기를 반복",
                  5: "상수항의 약수 중 f(a) = 0인 a를 찾고, 조립제법으로 나머지 이차식을 구해요"},
            note="나머지정리는 ‘A = BQ + R에 x = a를 넣으면 B가 0이 된다’는 한 줄이 전부예요. 조립제법은 그 나눗셈을 계수만으로 빠르게 하는 방법이에요.")
    R = rng(2101)

    def g1():
        b1 = R.choice([-3, -2, -1, 1, 2, 3])
        Bq = x ** 2 + b1 * x + R.choice([-2, -1, 1, 2, 3])
        Q = x + R.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        Rr = R.choice([-3, -2, 2, 3, 1]) * x + R.choice([-5, -4, -2, -1, 1, 2, 3, 5])
        A = sp.expand(Bq * Q + Rr)
        prod = sp.expand(Bq * Q)
        q = f"다항식 A를 {P_(Bq)}로 나누었을 때의 몫이 {P_(Q)}, 나머지가 {P_(Rr)}일 때, A를 구하세요."
        ans = P_(A)
        rs = P_(Rr)
        lines = [L(f"A = ({P_(Bq)})({P_(Q)}) " + (f"+ ({rs})" if rs.startswith(MI) else f"+ {rs}"), memo="A = BQ + R"), L(f"({P_(Bq)})({P_(Q)}) = {P_(prod)}"), L(f"{P_(prod)} + ({P_(Rr)}) = {ans}")]
        S.add(1, q, ans, "A = BQ + R 에 그대로 넣어 전개해요", lines, None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 1, 20, g1)

    def rand_cubic():
        cs = [R.choice([1, 1, 2, -1, 3]), R.randint(-5, 5), R.randint(-6, 6), R.randint(-8, 8)]
        return cs

    def ev_line(cs, a):
        n = len(cs) - 1
        terms = []
        for i, c in enumerate(cs):
            e = n - i
            if c == 0:
                continue
            if e == 0:
                terms.append(N(c))
            elif e == 1:
                terms.append(f"{N(c)} × {NP(a)}" if c != 1 else NP(a))
            else:
                terms.append((f"{N(c)} × " if c != 1 else "") + f"{NP(a)}^{{{e}}}")
        s = " + ".join(terms).replace("+ −", "− ")
        val = sum(c * a ** (n - i) for i, c in enumerate(cs))
        return s, val

    def g2():
        cs = rand_cubic()
        a = R.choice([-3, -2, -1, 1, 2, 3])
        e = sum(c * x ** (3 - i) for i, c in enumerate(cs))
        s, val = ev_line(cs, a)
        dv = f"x {'−' if a > 0 else '+'} {abs(a)}"
        q = f"f(x) = {J(P_(e), '을', '를')} {dv}로 나누었을 때의 나머지를 구하세요."
        lines = [L(f"나머지 = f({N(a)})", memo=f"{dv} = 0 인 x = {N(a)}"), L(f"f({N(a)}) = {s} = {N(val)}")]
        S.add(2, q, N(val), "나누지 않고 x = a를 대입해요", lines, None, ap=plain(N(val)), key=q)
    fill(S, 2, 20, g2)

    def g3():
        cs = rand_cubic()
        a = R.choice([-3, -2, -1, 1, 2, 3])
        pos = R.choice([1, 2])
        if a ** (3 - pos) == 0:
            return
        val_rest = sum(c * a ** (3 - i) for i, c in enumerate(cs) if i != pos)
        coef = a ** (3 - pos)
        if val_rest % coef:
            return
        m = Fr(-val_rest, coef)
        cs2 = list(cs)
        cs2[pos] = m
        ee = sum((a_ if i == pos else c) * x ** (3 - i) for i, c in enumerate(cs))
        es = str(sp.expand(ee))
        poly_s = poly([c if i != pos else 0 for i, c in enumerate(cs)])
        # 식 글자: 미정계수 a 를 넣어 적는다
        terms = []
        for i, c in enumerate(cs):
            e = 3 - i
            if i == pos:
                terms.append(("a" if True else "") + ("x" + (f"^{{{e}}}" if e > 1 else "") if e else ""))
            elif c:
                terms.append(mono(c, "x", e, first=not terms).strip() if terms else mono(c, "x", e, first=True))
        fs = ""
        for i, c in enumerate(cs):
            e = 3 - i
            if i == pos:
                fs += ("" if not fs else " + ") + "a" + ("x" + (f"^{{{e}}}" if e > 1 else "") if e else "")
            elif c:
                fs += mono(c, "x", e, first=(fs == ""))
        dv = f"x {'−' if a > 0 else '+'} {abs(a)}"
        q = f"다항식 {fs}가 {dv}로 나누어떨어질 때, 상수 a의 값을 구하세요." if not _bat_s(fs) else f"다항식 {fs}이 {dv}로 나누어떨어질 때, 상수 a의 값을 구하세요."
        sub = []
        for i, c in enumerate(cs):
            e = 3 - i
            if i == pos:
                sub.append(f"{coef}a" if coef != 1 else "a")
            elif c:
                sub.append(N(c * a ** e))
        line2 = " + ".join(sub).replace("+ −", "− ")
        lines = [L(f"f({N(a)}) = 0", memo="인수정리"), L(f"{line2} = 0"), L(f"{mono(coef, 'a', 1, True)} = {N(-val_rest)} → a = {N(m)}" if coef != 1 else f"a = {N(m)}")]
        S.add(3, q, f"a = {N(m)}", "나누어떨어지면 f(a) = 0", lines, None, ap=plain(N(m)), sub={"a": m}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        deg = 3 if S.count(4) < 14 else 4
        cs = [R.choice([1, 2, 3, -1])] + [R.randint(-5, 5) for _ in range(deg)]
        r = R.choice([-3, -2, -1, 1, 2, 3])
        e = sum(c * x ** (deg - i) for i, c in enumerate(cs))
        f = Fig()
        lines, q = synth_lines(cs, r)
        lines.insert(0, L(f"x {'−' if r > 0 else '+'} {abs(r)} = 0 → x = {N(r)}", memo="왼쪽에 쓰는 수"))
        quo = poly(q[:-1])
        lines.append(L(f"몫 {quo}, 나머지 {N(q[-1])}"))
        synth_fig(f, cs, r, at0=0, at_rows=list(range(1, len(cs) + 1)))
        dv = f"x {'−' if r > 0 else '+'} {abs(r)}"
        qq = f"조립제법을 이용하여 {J(P_(e), '을', '를')} {dv}로 나누었을 때의 몫과 나머지를 구하세요."
        S.add(4, qq, f"몫 {quo}, 나머지 {N(q[-1])}", "계수만 늘어놓고 내려쓰기 → 곱하기 → 더하기", lines, f.out(), ap=f"{plain(quo)}, {q[-1]}", omr="ex", key=qq)
    fill(S, 4, 20, g4)

    def g5():
        r1, r2, r3 = R.choice([-3, -2, -1, 1, 2, 3]), R.choice([-4, -3, -2, -1, 1, 2, 3, 4]), R.choice([-5, -4, -3, -2, 2, 3, 4, 5])
        if len({r1, r2, r3}) < 3:
            return
        lead = 1
        e = sp.expand((x - r1) * (x - r2) * (x - r3))
        cs = [int(c) for c in sp.Poly(e, x).all_coeffs()]
        # 상수항 약수 중 가장 작은 |a| 근부터
        cands = sorted({r1, r2, r3}, key=lambda t: (abs(t), t < 0))
        r = cands[0]
        s, val = ev_line(cs, r)
        assert val == 0
        lines_s, q = synth_lines(cs, r)
        quad = sp.cancel(e / (x - r))
        o = [t for t in (r1, r2, r3) if t != r]
        o.sort()
        fac = f"(x {'−' if r > 0 else '+'} {abs(r)})" + "".join(f"(x {'−' if t > 0 else '+'} {abs(t)})" for t in o)
        f = Fig()
        synth_fig(f, cs, r, at0=1, at_rows=[2] * len(cs))
        lines = [L(f"f({N(r)}) = {s} = 0", memo="상수항의 약수를 대입"), L(f"x {'−' if r > 0 else '+'} {abs(r)}로 조립제법"),
                 L(f"몫 {P_(quad)}, 나머지 0"), L(f"{P_(quad)} = " + "".join(f"(x {'−' if t > 0 else '+'} {abs(t)})" for t in o)), L(f"{P_(e)} = {fac}")]
        q_ = f"{J(P_(e), '을', '를')} 인수분해하세요."
        S.add(5, q_, fac, "f(a) = 0 인 a를 찾아 일차식 하나를 꺼내요", lines, f.out(), ap=plain(fac), omr="ex", ident=True, key=q_)
    fill(S, 5, 20, g5)
    return S

def _bat_s(s):
    import re
    s2 = re.sub(r"\^\{[^{}]*\}$", "", s)
    if s2 != s:
        return True
    return s[-1] in "013678LMNR"


# ══════════ ② 판별식 ══════════
def qplot(f, a, b, c, at="q", extra=None, xr=None):
    """y = ax^2 + bx + c 그래프와 x축"""
    a, b, c = Fr(a), Fr(b), Fr(c)
    p = -b / (2 * a)
    qv = c - b * b / (4 * a)
    xr = xr or (float(p) - 5, float(p) + 5)
    if not (xr[0] < 0 < xr[1]):
        xr = (min(xr[0], -1), max(xr[1], 1))
    ys = [float(a * t * t + b * t + c) for t in (xr[0], xr[1])] + [float(qv), 0]
    yr = (min(ys) - 1.5, max(ys) + 1.5)
    yr = (max(yr[0], float(qv) - 14), min(yr[1], float(qv) + 14)) if a > 0 else (max(yr[0], float(qv) - 14), min(yr[1], float(qv) + 14))
    yr = (min(yr[0], -1.5), max(yr[1], 1.5))
    P = Plane(f, xr, yr, box=(40, 40, 620, 620), square=False)
    P.axes(grid=0)
    P.curve(lambda t: float(a * t * t + b * t + c), at=at, c="sky", w=4.5)
    return P

def set_b():
    S = Set("b", "이차방정식과 이차함수 — 판별식으로 읽기", "판별식",
            {1: "판별식", 2: "근과 계수의 관계", 3: "이차함수와 x축", 4: "이차함수와 직선", 5: "이차부등식"},
            pp=6,
            tips={1: "D = b^{2} − 4ac — D > 0 서로 다른 두 실근 · D = 0 중근 · D < 0 서로 다른 두 허근",
                  2: "ax^{2} + bx + c = 0의 두 근 α, β → α + β = −{b/a}, αβ = {c/a}",
                  3: "그래프와 x축의 교점 개수 = 이차방정식의 실근 개수 → 판별식",
                  4: "두 식을 같다고 놓은 이차방정식의 판별식 — 접하면 D = 0",
                  5: "y = (이차식)의 그래프가 x축보다 아래(< 0)인지 위(> 0)인지 읽어요"},
            note="판별식은 ‘그래프가 x축과 몇 번 만나는가’를 계산으로 보는 것이에요. 그림에서 포물선과 x축(또는 직선)이 만나는 점의 개수와 D의 부호를 함께 보게 해 주세요.")
    R = rng(2102)

    def g1():
        if S.count(1) < 12:
            b, c = R.randint(-8, 8), R.randint(-9, 12)
            D = b * b - 4 * c
            kind = "서로 다른 두 실근" if D > 0 else "중근" if D == 0 else "서로 다른 두 허근"
            want = ["서로 다른 두 실근", "중근", "서로 다른 두 허근"][S.count(1) % 3]
            if kind != want:
                return
            e = x ** 2 + b * x + c
            f = Fig()
            P = qplot(f, 1, b, c)
            if D >= 0:
                rts = sorted(set(sp.solve(e, x)), key=lambda t: float(t))
                for i, rt in enumerate(rts):
                    P.pt(float(rt), 0, at=2, f="coral", r=10, dl=i * 200)
            q = f"이차방정식 {P_(e)} = 0의 근을 판별하세요."
            lines = [L("D = b^{2} − 4ac"), L(f"D = {NP(b)}^{{2}} − 4 × 1 × {NP(c)} = {N(D)}"), L(f"D {'>' if D > 0 else '=' if D == 0 else '<'} 0 → {kind}", memo="x축과 만나는 점의 개수")]
            S.add(1, q, kind, "판별식 D의 부호를 봐요", lines, f.out(), omr="ex", key=q)
        else:
            b = R.choice([-8, -6, -4, -2, 2, 4, 6, 8])
            h = b // 2
            want = R.choice(["두 실근", "허근"])
            q = f"이차방정식 x^{{2}} {'+' if b > 0 else '−'} {abs(b)}x + k = 0이 {'서로 다른 두 실근' if want == '두 실근' else '서로 다른 두 허근'}을 가질 때, 실수 k의 값의 범위를 구하세요."
            sign = ">" if want == "두 실근" else "<"
            ans = f"k {'<' if want == '두 실근' else '>'} {h * h}"
            lines = [L(f"{'D/4 > 0' if want == '두 실근' else 'D/4 < 0'}", memo="x의 계수가 짝수면 D/4"), L(f"{NP(h)}^{{2}} − k {sign} 0"), L(ans)]
            S.add(1, q, ans, "근의 조건을 판별식의 부호로", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        a = R.choice([1, 1, 1, 2, 3])
        b, c = R.randint(-7, 7), R.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])
        s, p = Fr(-b, a), Fr(c, a)
        k = S.count(2) % 4
        e = a * x ** 2 + b * x + c
        if k == 0:
            val, ask, lines2 = s * s - 2 * p, "α^{2} + β^{2}", [L("α^{2} + β^{2} = (α + β)^{2} − 2αβ"), L(f"{NP(s)}^{{2}} − 2 × {NP(p)} = {N(s * s - 2 * p)}")]
        elif k == 1:
            if p == 0:
                return
            val, ask, lines2 = s / p, "{1/α} + {1/β}", [L("{1/α} + {1/β} = {α + β/αβ}"), L(f"{{{N(s)}/{N(p)}}} = {N(s / p)}" if False else f"{N(s)} ÷ {NP(p)} = {N(s / p)}")]
        elif k == 2:
            val, ask, lines2 = s * s - 4 * p, "(α − β)^{2}", [L("(α − β)^{2} = (α + β)^{2} − 4αβ"), L(f"{NP(s)}^{{2}} − 4 × {NP(p)} = {N(s * s - 4 * p)}")]
        else:
            val, ask, lines2 = s * s * s - 3 * p * s, "α^{3} + β^{3}", [L("α^{3} + β^{3} = (α + β)^{3} − 3αβ(α + β)"), L(f"{NP(s)}^{{3}} − 3 × {NP(p)} × {NP(s)} = {N(s ** 3 - 3 * p * s)}")]
        # 검산: 실제 두 근으로
        rts = sp.solve(e, x)
        if len(rts) != 2:
            return
        al, be = rts
        chk = {0: al ** 2 + be ** 2, 1: 1 / al + 1 / be, 2: (al - be) ** 2, 3: al ** 3 + be ** 3}[k]
        assert sp.simplify(chk - sp.Rational(val.numerator, val.denominator)) == 0
        q = f"이차방정식 {P_(e)} = 0의 두 근을 α, β라 할 때, {ask}의 값을 구하세요."
        lines = [L(f"α + β = {N(s)}, αβ = {N(p)}", memo="−{b/a}, {c/a}")] + lines2
        S.add(2, q, N(val), "두 근을 구하지 말고 합과 곱으로", lines, None, ap=plain(N(val)), key=q)
    fill(S, 2, 20, g2)

    def g3():
        b = R.choice([-8, -6, -4, -2, 2, 4, 6, 8]); h = b // 2
        want = ["만나지 않을", "서로 다른 두 점에서 만날", "접할"][S.count(3) % 3]
        q = f"이차함수 y = x^{{2}} {'+' if b > 0 else '−'} {abs(b)}x + k의 그래프가 x축과 {want} 때, 실수 k의 {'값을' if want == '접할' else '값의 범위를'} 구하세요."
        crit = h * h
        Dk = (b * b - 4 * k_)
        assert sp.solve(sp.Eq(Dk, 0), k_) == [crit]
        if want == "만나지 않을":
            ans, cond = f"k > {crit}", "D/4 < 0"
        elif want == "접할":
            ans, cond = f"k = {crit}", "D/4 = 0"
        else:
            ans, cond = f"k < {crit}", "D/4 > 0"
        f = Fig()
        P = qplot(f, 1, b, crit, at="p")
        f.text(320, 60, f"k = {crit}일 때 접해요", z=26, c="soft", at="p")
        sample = crit + (3 if want == "만나지 않을" else -3 if want != "접할" else 0)
        if want != "접할":
            P.curve(lambda t: t * t + b * t + sample, at=2, c="coral", w=4)
        lines = [L(f"x^{{2}} {'+' if b > 0 else '−'} {abs(b)}x + k = 0의 판별식", memo="x축과 만나는 점 = 실근"), L(f"{cond}: {NP(h)}^{{2}} − k {cond.split()[1]} 0"), L(ans)]
        S.add(3, q, ans, "그래프와 x축의 교점 개수 = 실근의 개수", lines, f.out(), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        b, c = R.randint(-4, 4), R.randint(-3, 6)
        m = R.randint(-3, 4)
        # x^2 + bx + c = mx + k  →  x^2 + (b − m)x + (c − k) = 0
        B = b - m
        if B % 2 or B == 0:
            return
        h = B // 2
        kc = c - h * h          # 접할 때 k
        want = ["접할", "서로 다른 두 점에서 만날", "만나지 않을"][S.count(4) % 3]
        if want == "접할":
            ans = f"k = {N(kc)}"
            cond = "D/4 = 0"
        elif want == "만나지 않을":
            ans = f"k < {N(kc)}"
            cond = "D/4 < 0"
        else:
            ans = f"k > {N(kc)}"
            cond = "D/4 > 0"
        par = poly([1, b, c])
        q = f"이차함수 y = {par}의 그래프와 직선 y = {lin(m, 0).replace('0', '') if m else ''}{'' if m == 0 else ' + '}k가 {want} 때, 실수 k의 {'값을' if want == '접할' else '값의 범위를'} 구하세요."
        Dk = sp.discriminant(x ** 2 + B * x + (c - k_), x)
        assert sp.solve(sp.Eq(Dk, 0), k_) == [kc]
        assert (sp.Poly(x ** 2 + b * x + c - (m * x + kc), x).discriminant()) == 0
        q = q.replace("y =  + k", "y = k").replace("y = x + k", "y = x + k")
        f = Fig()
        P = qplot(f, 1, b, c)
        P.lineq(m, float(kc), at="p", c="coral", w=4, d=want != "접할")
        tx = float(-h)
        P.pt(tx, tx * tx + b * tx + c, at="a" if want == "접할" else "p", f="coral", r=9)
        const = " − k" if c == 0 else f" {'+' if c > 0 else '−'} {abs(c)} − k"
        op = cond.split()[1]
        d4 = f"{NP(h)}^{{2}} − ({N(c)} − k)" if c else f"{NP(h)}^{{2}} + k"
        lines = [L(f"{par} = {lin(m, 0) if m else ''}{' + ' if m else ''}k", memo="두 식을 같다고 놓기"), L(f"{poly([1, B, 0])}{const} = 0"),
                 L(f"{cond}: {d4} {op} 0"), L(ans)]
        S.add(4, q, ans, "만나는 점의 x좌표 = 두 식을 같게 놓은 방정식의 실근", lines, f.out(), omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5)
        f = Fig()
        if k < 16:
            r1, r2 = sorted(R.sample(range(-6, 7), 2))
            if r1 == r2:
                return
            op = ["<", ">", "≤", "≥"][k % 4]
            e = sp.expand((x - r1) * (x - r2))
            P = qplot(f, 1, -(r1 + r2), r1 * r2, xr=(min(r1, -1) - 3, max(r2, 1) + 3))
            for rt in (r1, r2):
                P.pt(rt, 0, at=1, f="coral", r=9, label=N(rt), pos="s", z=26, c="coral")
            if op in ("<", "≤"):
                f.line(P.X(r1), P.Y(0), P.X(r2), P.Y(0), at=2, c="gold", w=10, o=0.8)
                ans = f"{N(r1)} {'<' if op == '<' else '≤'} x {'<' if op == '<' else '≤'} {N(r2)}"
                where = "x축보다 아래" if op == "<" else "x축보다 아래 또는 x축 위"
            else:
                f.line(P.X(P.xr[0]), P.Y(0), P.X(r1), P.Y(0), at=2, c="gold", w=10, o=0.8)
                f.line(P.X(r2), P.Y(0), P.X(P.xr[1]), P.Y(0), at=2, c="gold", w=10, o=0.8)
                ans = f"x {'<' if op == '>' else '≤'} {N(r1)} 또는 x {'>' if op == '>' else '≥'} {N(r2)}"
                where = "x축보다 위" if op == ">" else "x축보다 위 또는 x축 위"
            q = f"이차부등식 {P_(e)} {op} 0을 푸세요."
            fx = lambda t: "x" if t == 0 else f"(x {'−' if t > 0 else '+'} {abs(t)})"
            fs = "".join(fx(t) for t in sorted((r1, r2), key=lambda t: t != 0))
            lines = [L(f"{P_(e)} = {fs}"), L(f"y = {P_(e)}의 그래프가 {where}", memo=f"{op} 0"), L(ans)]
            S.add(5, q, ans, "그래프가 x축과 만나는 두 점을 찾고, 위 · 아래를 읽어요", lines, f.out(), omr="ex", ident=True, key=q)
        else:
            b, c = R.choice([-4, -2, 2, 4]), R.randint(3, 9)
            if b * b - 4 * c >= 0:
                return
            op = [">", "<"][k % 2]
            e = x ** 2 + b * x + c
            P = qplot(f, 1, b, c)
            ans = "모든 실수" if op == ">" else "해가 없다"
            q = f"이차부등식 {P_(e)} {op} 0을 푸세요."
            lines = [L(f"D/4 = {NP(b // 2)}^{{2}} − {c} = {N((b // 2) ** 2 - c)} < 0", memo="x축과 만나지 않아요"), L("그래프가 항상 x축보다 위"), L(ans)]
            S.add(5, q, ans, "D < 0이면 그래프가 x축과 만나지 않아요", lines, f.out(), omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "h1", "grade": "고1", "level": "고등", "icon": "🧾", "title": "고1 · 나머지정리 · 판별식",
         "desc": "나머지정리와 조립제법 100제(조립제법 표가 한 칸씩 채워져요) · 이차방정식과 이차함수 — 판별식으로 읽기 100제.",
         "thumb": ("a", 70), "sets": [set_a, set_b]}
