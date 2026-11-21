# 중3 — ① 인수분해 — 넓이 타일로 거꾸로 곱하기 · ② 이차함수 — 꼭짓점과 평행이동
from math import gcd
from core import *
from fig import Fig, mv, Plane

x = SYMS["x"]; y = SYMS["y"]

def P_(e):
    return sym_poly_str(e)

def fac2(a, b):
    """(ax + b) 글자"""
    return f"({lin(a, b)})"

def tiles(f, cols, rows, at_tiles="q", at_cells=None, X=None, U=30, x0=None, y0=None):
    """넓이 타일 직사각형 — cols/rows: ['x', 'x', 3] (x 길이 또는 단위 칸 수). 칸 종류별 색: x² 금빛 · x 청록 · 1 보라"""
    nxc = sum(1 for c in cols if c == "x"); nuc = sum(c for c in cols if c != "x")
    nxr = sum(1 for r in rows if r == "x"); nur = sum(r for r in rows if r != "x")
    if X is None:
        X = min(230, (520 - nuc * U) / max(nxc, 1), (500 - nur * U) / max(nxr, 1))
    W = nxc * X + nuc * U
    H = nxr * X + nur * U
    x0 = 330 - W / 2 + 20 if x0 is None else x0
    y0 = 340 - H / 2 + 10 if y0 is None else y0
    xs, ws = [], []
    cx = x0
    for c in cols:
        w = X if c == "x" else c * U
        xs.append(cx); ws.append(w); cx += w
    ys, hs = [], []
    cy = y0
    for r in rows:
        h = X if r == "x" else r * U
        ys.append(cy); hs.append(h); cy += h
    for i, r in enumerate(rows):
        for j, c in enumerate(cols):
            kind = "xx" if (r == "x" and c == "x") else ("x" if (r == "x" or c == "x") else "1")
            col = {"xx": "gold", "x": "teal", "1": "lilac"}[kind]
            at = (at_cells or {}).get(kind, at_tiles)
            if kind == "1":
                f.grid(xs[j], ys[i], U, U, c, r, at=at, c="ink", sw=2, f=col, fo=0.4)
            elif kind == "x" and c != "x":
                f.grid(xs[j], ys[i], U, X, c, 1, at=at, c="ink", sw=2, f=col, fo=0.4)
            elif kind == "x" and r != "x":
                f.grid(xs[j], ys[i], X, U, 1, r, at=at, c="ink", sw=2, f=col, fo=0.4)
            else:
                f.rect(xs[j], ys[i], ws[j], hs[i], at=at, c="ink", sw=2.5, f=col, fo=0.4)
                f.text(xs[j] + ws[j] / 2, ys[i] + hs[i] / 2 + 12, "x^{2}", z=34, at=at, b=700)
    for j, c in enumerate(cols):
        f.text(xs[j] + ws[j] / 2, y0 - 16, "x" if c == "x" else str(c), z=28, c="soft", at="p", b=700)
    for i, r in enumerate(rows):
        f.text(x0 - 14, ys[i] + hs[i] / 2 + 10, "x" if r == "x" else str(r), z=28, c="soft", at="p", b=700, a="e")
    return x0, y0, W, H

def set_a():
    S = Set("a", "인수분해 — 넓이 타일로 거꾸로 곱하기", "인수분해",
            {1: "공통인수 묶기", 2: "완전제곱식", 3: "합과 차의 곱", 4: "x² + (a + b)x + ab", 5: "acx² + (ad + bc)x + bd"},
            pp=10,
            tips={1: "모든 항에 공통으로 곱해진 수 · 문자를 앞으로 묶어 내요 — 수는 최대공약수, 문자는 가장 낮은 차수",
                  2: "a^{2} ± 2ab + b^{2} = (a ± b)^{2} — 끝항이 제곱수이고 가운데 항이 2 × (곱)인지 확인",
                  3: "a^{2} − b^{2} = (a + b)(a − b)",
                  4: "곱이 상수항, 합이 x의 계수인 두 수를 찾아요",
                  5: "x^{2}의 계수와 상수항을 각각 두 수의 곱으로 쪼개고, 엇갈려 곱한 합(크로스)이 가운데 항"},
            note="인수분해는 곱셈공식을 거꾸로 쓰는 것이에요. 넓이 타일(x^{2} · x · 1 조각)을 직사각형으로 모으는 그림을 보면 ‘두 수 찾기’가 왜 곱과 합인지 보여요.")
    R = rng(1301)

    def g1():
        g = R.randint(2, 6); k = R.choice([1, 1, 2])
        a, b = R.randint(1, 5), R.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        if gcd(a, abs(b)) != 1:
            return
        e = g * x ** k * (a * x + b)
        gs = f"{g}x" + (f"^{{{k}}}" if k > 1 else "")
        q = P_(e)
        ans = f"{gs}({lin(a, b)})"
        f = Fig()
        bx, by, bw, bh = 120, 180, 440, 260
        wa = bw * 0.6
        f.rect(bx, by, wa, bh, c="ink", sw=3, f="gold", fo=0.35)
        f.rect(bx + wa, by, bw - wa, bh, c="ink", sw=3, f="teal", fo=0.35)
        f.text(bx + wa / 2, by + bh / 2 + 12, monom(g * a, {"x": k + 1}), z=36, b=700)
        f.text(bx + wa + (bw - wa) / 2, by + bh / 2 + 12, monom(g * b, {"x": k}), z=36, b=700)
        f.text(bx - 16, by + bh / 2 + 12, gs, z=36, c="coral", a="e", b=800, at=0)
        f.text(bx + wa / 2, by - 20, f"{monom(a, {'x': 1})}", z=32, c="soft", at=1, b=700)
        f.text(bx + wa + (bw - wa) / 2, by - 20, N(b), z=32, c="soft", at=1, b=700)
        S.add(1, f"{J(q, '을', '를')} 인수분해하세요.", ans, "공통인수를 앞으로 묶어 내요",
              [L(f"공통인수 {gs}", memo="수 최대공약수 · 문자 낮은 차수"), L(f"{q} = {ans}")], f.out(), ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2)
        if k < 12:
            p = R.choice([-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9])
            e = (x + p) ** 2
            q = P_(e)
            ans = f"({lin(1, p)})^{{2}}"
            f = None
            if p > 0:
                f = Fig()
                tiles(f, ["x", p], ["x", p])
            lines = [L(f"{p * p} = {abs(p)}^{{2}}, {2 * p}x = 2 × x × {NP(p)}", memo="끝항 제곱 · 가운데 2배"), L(f"{q} = {ans}")]
        else:
            a = R.randint(2, 4); b = R.choice([-5, -3, -1, 1, 3, 5])
            if gcd(a, abs(b)) != 1:
                return
            e = (a * x + b) ** 2
            q = P_(e)
            ans = f"({lin(a, b)})^{{2}}"
            f = None
            lines = [L(f"{a * a}x^{{2}} = ({a}x)^{{2}}, {b * b} = {abs(b)}^{{2}}"), L(f"{N(2 * a * b)}x = 2 × {a}x × {NP(b)}", memo="가운데 항 확인"), L(f"{q} = {ans}")]
        S.add(2, f"{J(q, '을', '를')} 인수분해하세요.", ans, "a^{2} ± 2ab + b^{2} = (a ± b)^{2}", lines, f.out() if f else None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3)
        if k < 8:
            a = R.randint(2, 9)
            q = f"x^{{2}} − {a * a}"
            ans = f"(x + {a})(x − {a})"
            f = Fig()
            Xp, Ap = 330, 33 * a if a <= 6 else 22 * a
            x0, y0 = 120, 110
            f.rect(x0, y0, Xp, Xp, c="ink", sw=3, f="gold", fo=0.3)
            f.text(x0 + Xp / 2, y0 - 16, "x", z=30, c="soft", b=700)
            f.text(x0 - 14, y0 + Xp / 2, "x", z=30, c="soft", b=700, a="e")
            cut = f.rect(x0 + Xp - Ap, y0 + Xp - Ap, Ap, Ap, at="q", c="red", sw=3, d=True, f="red", fo=0.25, un=0)
            f.text(x0 + Xp - Ap / 2, y0 + Xp - Ap / 2 + 10, f"{a}^{{2}}", z=28, c="red", b=700, un=0)
            strip = f.rect(x0, y0 + Xp - Ap, Xp - Ap, Ap, at=0, c="teal", sw=3, f="teal", fo=0.45)
            cx0, cy0 = x0 + (Xp - Ap) / 2, y0 + Xp - Ap / 2
            tx, ty = x0 + Xp + Ap / 2, y0 + (Xp - Ap) / 2
            mv(strip, 1, tx - cx0, ty - cy0, r=-90, cx=cx0, cy=cy0)
            f.text(x0 + (Xp + Ap) / 2, y0 + Xp - Ap + 50, f"(x + {a})(x − {a})", z=34, c="coral", b=800, at=2)
            lines = [L(f"{a * a} = {a}^{{2}}", memo="제곱수"), L("a^{2} − b^{2} = (a + b)(a − b)"), L(f"{q} = {ans}")]
        else:
            a, b = R.randint(2, 7), R.randint(1, 9)
            if gcd(a, b) != 1:
                return
            v = R.choice(["y", "1"])
            if v == "1":
                q = f"{a * a}x^{{2}} − {b * b}"
                ans = f"({a}x + {b})({a}x − {b})"
                lines = [L(f"{a * a}x^{{2}} = ({a}x)^{{2}}, {b * b} = {b}^{{2}}"), L(f"{q} = {ans}")]
            else:
                bs = "y" if b == 1 else f"{b}y"
                q = f"{a * a}x^{{2}} − {b * b if b > 1 else ''}y^{{2}}"
                ans = f"({a}x + {bs})({a}x − {bs})"
                lines = [L(f"{a * a}x^{{2}} = ({a}x)^{{2}}, {(str(b * b) if b > 1 else '')}y^{{2}} = ({bs})^{{2}}"), L(f"{q} = {ans}")]
            f = None
        S.add(3, f"{J(q, '을', '를')} 인수분해하세요.", ans, "제곱 − 제곱 = (합)(차)", lines, f.out() if f else None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 3, 20, g3)

    def g4():
        p, q_ = R.choice([-9, -8, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8, 9]), R.choice([-9, -7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7, 8])
        if p == q_ or p + q_ == 0:
            return
        if S.count(4) < 8 and (p < 0 or q_ < 0):
            return
        if S.count(4) >= 8 and p > 0 and q_ > 0:
            return
        p, q_ = sorted((p, q_))
        e = (x + p) * (x + q_)
        q = P_(e)
        ans = f"({lin(1, p)})({lin(1, q_)})"
        f = None
        if p > 0 and q_ > 0:
            f = Fig()
            tiles(f, ["x", q_], ["x", p])
        lines = [L(f"곱이 {N(p * q_)}, 합이 {N(p + q_)}인 두 수", memo="두 수 찾기"), L(f"{NP(p)} × {NP(q_)} = {N(p * q_)}, {NP(p)} + {NP(q_)} = {N(p + q_)}"), L(f"{q} = {ans}")]
        S.add(4, f"{J(q, '을', '를')} 인수분해하세요.", ans, "곱 → 상수항, 합 → x의 계수", lines, f.out() if f else None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 4, 20, g4)

    def g5():
        a, c = R.choice([(2, 1), (3, 1), (2, 3), (3, 2), (4, 1), (5, 1), (2, 5), (6, 1), (3, 4)])
        b, d = R.choice([-5, -3, -2, -1, 1, 2, 3, 4, 5]), R.choice([-5, -4, -3, -2, -1, 1, 2, 3, 5])
        if gcd(a, abs(b)) != 1 or gcd(c, abs(d)) != 1:
            return
        if S.count(5) < 6 and (b < 0 or d < 0):
            return
        e = (a * x + b) * (c * x + d)
        q = P_(e)
        A, B, C = a * c, a * d + b * c, b * d
        if B == 0:
            return
        ans = f"({lin(a, b)})({lin(c, d)})"
        f = None
        if b > 0 and d > 0 and a + c <= 5 and a * c <= 6:
            f = Fig()
            tiles(f, ["x"] * c + [d], ["x"] * a + [b])
        lines = [L(f"{A}x^{{2}} = {a}x × {'x' if c == 1 else str(c) + 'x'}, {N(C)} = {NP(b)} × {NP(d)}", memo="곱해서 나오는 짝"),
                 L(f"크로스: {a}x × {NP(d)} + {NP(b)} × {'x' if c == 1 else str(c) + 'x'} = {mono(B, 'x', 1, True)}", memo="합이 가운데 항"), L(f"{q} = {ans}")]
        S.add(5, f"{J(q, '을', '를')} 인수분해하세요.", ans, "x^{2}의 계수와 상수항을 쪼개 크로스로 확인", lines, f.out() if f else None, ap=plain(ans), omr="ex", ident=True, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ ② 이차함수 ══════════
def parab(f, a, p, q, at="q", c="sky", rng_=None, pts=None, axis=True, vertex=True, vat=None, lab=True):
    a, p, q = Fr(a), Fr(p), Fr(q)
    xr = rng_ or (float(p) - 6, float(p) + 6)
    yv = [float(a * (t - p) ** 2 + q) for t in (xr[0], xr[1])] + [float(q)]
    ex = [float(y) for _, y in (pts or [])]          # 꼭 보여야 하는 점(지나는 점)
    lo, hi = min(yv + [0]), max(yv + [0])
    span = max(xr[1] - xr[0], 8)
    yr = (max(lo - 1.5, float(q) - span * 0.9), min(hi + 1.5, float(q) + span * 0.9))
    if ex:
        yr = (min(yr[0], min(ex) - abs(min(ex)) * 0.08 - 1.5), max(yr[1], max(ex) + abs(max(ex)) * 0.08 + 1.5))
    if yr[1] - yr[0] < 6:
        yr = (yr[0] - 3, yr[1] + 3)
    if not (yr[0] < 0 < yr[1]):
        yr = (min(yr[0], -1.5), max(yr[1], 1.5))
    if not (xr[0] < 0 < xr[1]):
        xr = (min(xr[0], -1.5), max(xr[1], 1.5))
    P = Plane(f, xr, yr, box=(40, 40, 620, 640), square=False)
    P.axes(grid=0, lab_step=None)
    P.curve(lambda t: float(a * (t - p) ** 2 + q), at=at, c=c, w=4.5)
    if axis:
        f.line(P.X(float(p)), P.Y(yr[0]), P.X(float(p)), P.Y(yr[1]), at=vat if vat is not None else at, c="red", w=2.5, d=True)
    if vertex:
        P.pt(float(p), float(q), at=vat if vat is not None else at, f="coral", r=10, label=f"({N(p)}, {N(q)})" if lab else None, pos="se" if a > 0 else "ne", z=28, c="coral")
    return P

def set_b():
    S = Set("b", "이차함수 — 꼭짓점과 평행이동", "이차함수",
            {1: "y = ax² 위의 점", 2: "꼭짓점과 축", 3: "평행이동", 4: "표준형으로 바꾸기", 5: "이차함수의 식 구하기"},
            pp=6,
            tips={1: "그래프가 점 (p, q)를 지나면 x = p, y = q를 식에 대입해 맞아요",
                  2: "y = a(x − p)^{2} + q → 꼭짓점 (p, q), 축 x = p",
                  3: "x축 방향 m → x 대신 x − m · y축 방향 n → 식 끝에 + n",
                  4: "x의 계수의 반의 제곱을 더하고 빼서 완전제곱식을 만들어요",
                  5: "꼭짓점 (p, q)를 알면 y = a(x − p)^{2} + q 로 두고 지나는 점을 대입해 a"},
            note="이차함수는 y = ax^{2}를 옮긴 그래프예요. 꼭짓점이 어디로 갔는지(평행이동)만 보면 식과 그래프가 한 번에 이어져요.")
    R = rng(1302)

    def g1():
        k = S.count(1) % 2
        a = R.choice([Fr(1, 2), 1, 2, 3, -1, -2, Fr(-1, 2), Fr(1, 3), -3])
        t = R.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        v = a * t * t
        if v.denominator != 1:
            return
        f = Fig()
        P = parab(f, a, 0, 0, axis=False, vertex=False, rng_=(-5, 5), pts=[(t, v)])
        P.pt(t, float(v), at="a", f="coral", r=11, label=f"({N(t)}, {N(v)})", pos="ne" if t < 0 else "nw", z=28, c="coral")
        if k == 0:
            q = f"y = {monom(a, {'x': 2})}의 그래프가 점 ({N(t)}, k)를 지날 때, k의 값을 구하세요."
            lines = [L(f"x = {J(N(t), '을', '를')} 대입"), L(f"k = {N(a)} × {NP(t)}^{{2}} = {N(v)}")]
            S.add(1, q, N(v), "지나는 점의 좌표를 식에 대입해요", lines, f.out(), ap=plain(N(v)), key=q)
        else:
            q = f"y = ax^{{2}}의 그래프가 점 {J(f'({N(t)}, {N(v)})', '을', '를')} 지날 때, a의 값을 구하세요."
            lines = [L(f"{N(v)} = a × {NP(t)}^{{2}}", memo="점을 대입"), L(f"{mono(t * t, 'a', 1, True)} = {N(v)} → a = {N(a)}" if t * t != 1 else f"a = {N(a)}")]
            S.add(1, q, N(a), "지나는 점의 좌표를 식에 대입해요", lines, f.out(), ap=plain(N(a)), sub={"a": a}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        a = R.choice([1, 2, 3, -1, -2, Fr(1, 2), Fr(-1, 2), -3])
        p, q = R.randint(-5, 5), R.randint(-6, 6)
        if p == 0 and q == 0:
            return
        f = Fig()
        parab(f, a, p, q, vat=1)
        sq = f"(x {'−' if p > 0 else '+'} {abs(p)})^{{2}}" if p else "x^{2}"
        expr = f"y = {'' if a == 1 else ('−' if a == -1 else N(a))}{sq}" + (f" {'+' if q > 0 else '−'} {abs(q)}" if q else "")
        q_ = f"이차함수 {expr}의 그래프의 꼭짓점의 좌표와 축의 방정식을 구하세요."
        lines = [L("y = a(x − p)^{2} + q → 꼭짓점 (p, q)"), L(f"p = {N(p)}, q = {N(q)}", memo="괄호 안 부호 반대"), L(f"꼭짓점 ({N(p)}, {N(q)}), 축 x = {N(p)}")]
        S.add(2, q_, f"({N(p)}, {N(q)}), x = {N(p)}", "괄호 안의 수는 부호를 바꿔 읽어요", lines, f.out(), ap=f"({p}, {q}), x={p}", omr="ex", key=q_)
    fill(S, 2, 20, g2)

    def g3():
        a = R.choice([1, 2, 3, -1, -2, Fr(1, 2), -3])
        m, n = R.randint(-5, 5), R.randint(-6, 6)
        if m == 0 or n == 0:
            return
        f = Fig()
        P = parab(f, a, m, n, at=2, c="coral", vertex=True, axis=False, rng_=(min(0, m) - 4, max(0, m) + 4))
        P.curve(lambda t: float(Fr(a) * t * t), at="q", c="sky", w=4)
        P.pt(0, 0, at="q", f="sky", r=8)
        f.line(P.X(0), P.Y(0), P.X(m), P.Y(n), at=1, c="red", w=3, ar=1, dr=True)
        sq = f"(x {'−' if m > 0 else '+'} {abs(m)})^{{2}}"
        ac = '' if a == 1 else ('−' if a == -1 else N(a))
        ans = f"y = {ac}{sq} {'+' if n > 0 else '−'} {abs(n)}"
        q = f"y = {monom(a, {'x': 2})}의 그래프를 x축의 방향으로 {N(m)}만큼, y축의 방향으로 {N(n)}만큼 평행이동한 그래프의 식을 구하세요."
        lines = [L(f"x 대신 x − {NP(m)}", memo=f"x축 방향 {N(m)}"), L(f"식 끝에 {'+' if n > 0 else '−'} {abs(n)}", memo=f"y축 방향 {N(n)}"), L(ans)]
        S.add(3, q, ans, "꼭짓점 (0, 0)이 (m, n)으로 옮겨 가요", lines, f.out(), ap=plain(ans), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.choice([1, 1, 1, 2, -1, 2, 3, -2])
        p, q = R.randint(-5, 5), R.randint(-9, 9)
        if p == 0:
            return
        e = a * (x - p) ** 2 + q
        poly_ = P_(e)
        b_ = -2 * a * p
        c_ = a * p * p + q
        f = Fig()
        parab(f, a, p, q, vat=len([0, 0, 0]) if a == 1 else 3)
        if a == 1:
            lines = [L(f"x^{{2}} {'−' if b_ < 0 else '+'} {abs(b_)}x = (x {'−' if p > 0 else '+'} {abs(p)})^{{2}} − {p * p}", memo=f"{NP(Fr(b_, 2))}^{{2}} = {J(p * p, '을', '를')} 더하고 빼요"),
                     L(f"{poly_} = (x {'−' if p > 0 else '+'} {abs(p)})^{{2}} − {p * p} {'+' if c_ >= 0 else '−'} {abs(c_)}"),
                     L(f"{poly_} = (x {'−' if p > 0 else '+'} {abs(p)})^{{2}}" + (f" {'+' if q > 0 else '−'} {abs(q)}" if q else "")), L(f"꼭짓점 ({N(p)}, {N(q)})")]
        else:
            inner = f"x^{{2}} {'−' if p > 0 else '+'} {2 * abs(p)}x"
            ac = "−" if a == -1 else N(a)
            lines = [L(f"{poly_} = {ac}({inner}){' + ' + str(c_) if c_ > 0 else (' − ' + str(-c_) if c_ < 0 else '')}", memo="x^{2}의 계수로 묶어요"),
                     L(f"{inner} = (x {'−' if p > 0 else '+'} {abs(p)})^{{2}} − {p * p}"),
                     L(f"{poly_} = {ac}(x {'−' if p > 0 else '+'} {abs(p)})^{{2}}" + (f" {'+' if q > 0 else '−'} {abs(q)}" if q else ""), memo=f"{N(a)} × (−{p * p}) {'+' if c_ >= 0 else '−'} {abs(c_)} = {N(q)}"),
                     L(f"꼭짓점 ({N(p)}, {N(q)})")]
        q_ = f"이차함수 y = {poly_}의 그래프의 꼭짓점의 좌표를 구하세요."
        S.add(4, q_, f"({N(p)}, {N(q)})", "완전제곱식을 만들어 y = a(x − p)^{2} + q 꼴로", lines, f.out(), ap=f"({p}, {q})", omr="pt", ident=True, key=q_)
    fill(S, 4, 20, g4)

    def g5():
        a = R.choice([1, 2, -1, -2, 3, Fr(1, 2)])
        p, q = R.randint(-4, 4), R.randint(-6, 6)
        t = p + R.choice([-3, -2, -1, 1, 2, 3])
        v = Fr(a) * (t - p) ** 2 + q
        if v.denominator != 1 or abs(v) > 14:
            return
        sq = f"(x {'−' if p > 0 else '+'} {abs(p)})^{{2}}" if p else "x^{2}"
        ans = f"y = {'' if a == 1 else ('−' if a == -1 else N(a))}{sq}" + (f" {'+' if q > 0 else '−'} {abs(q)}" if q else "")
        f = Fig()
        P = parab(f, a, p, q, at="a", rng_=(p - 5, p + 5), vat="q", pts=[(t, v)])
        P.pt(t, float(v), at="q", f="teal", r=10, label=f"({N(t)}, {N(v)})", pos="ne" if t < p else "nw", z=26, c="teal")
        q_ = f"꼭짓점의 좌표가 ({N(p)}, {N(q)})이고 점 {J(f'({N(t)}, {N(v)})', '을', '를')} 지나는 포물선을 그래프로 하는 이차함수의 식을 구하세요."
        lines = [L(f"y = a{sq}" + (f" {'+' if q > 0 else '−'} {abs(q)}" if q else ""), memo="꼭짓점으로 두기"), L(f"{N(v)} = a × {NP(t - p)}^{{2}}" + (f" {'+' if q > 0 else '−'} {abs(q)}" if q else ""), memo="지나는 점 대입"),
                 L(f"{mono((t - p) ** 2, 'a', 1, True)} = {N(v - q)} → a = {N(a)}" if (t - p) ** 2 != 1 else f"a = {N(a)}"), L(ans)]
        S.add(5, q_, ans, "꼭짓점을 알면 a 하나만 구하면 돼요", lines, f.out(), ap=plain(ans), omr="ex", sub={"a": a}, key=q_)
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "m3", "grade": "중3", "level": "중등", "icon": "🧱", "title": "중3 · 인수분해 · 이차함수",
         "desc": "인수분해 — 넓이 타일로 거꾸로 곱하기 100제 · 이차함수 — 꼭짓점과 평행이동 100제(포물선이 옮겨 가요).",
         "thumb": ("a", 70), "sets": [set_a, set_b]}
