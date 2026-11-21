# 고등 ③ — 합성함수와 역함수 · 유리함수와 무리함수 · 지수함수와 로그함수 · 삼각함수 · 사인법칙과 코사인법칙
import math
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, Plane, NL, ang_pt, angle_mark
from kit import *

x = SYMS["x"]

def bat(v):
    from core import _has_batchim
    return _has_batchim(str(v))

def FR(v):
    v = Fr(v)
    if v.denominator == 1:
        return N(v)
    return (MI if v < 0 else "") + "{%d/%d}" % (abs(v.numerator), v.denominator)

def LIN(m, b, var="x"):
    m, b = Fr(m), Fr(b)
    if m == 0:
        return FR(b)
    s = ("" if m == 1 else (MI if m == -1 else FR(m))) + var
    if b > 0:
        s += f" + {FR(b)}"
    elif b < 0:
        s += f" {MI} {FR(-b)}"
    return s

def PS(e):
    return sym_poly_str(sp.expand(e))

def TAIL(q_):
    """ + 3 · − 2 · (0 이면 빈 글자)"""
    q_ = Fr(q_)
    return "" if q_ == 0 else f" {'+' if q_ > 0 else MI} {FR(abs(q_))}"

def XM(p, var="x"):
    """x − p (p = 0 이면 x)"""
    return var if p == 0 else f"{var} {'+' if p < 0 else MI} {abs(p)}"

def AT(cs, v):
    """다항식(높은 차수부터 계수) 에 v 를 넣은 계산 글자 — '(−2)^{2} − 3 × (−2) + 1'"""
    deg = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        e = deg - i
        if c == 0:
            continue
        a = abs(c)
        if e == 0:
            body = N(a)
        else:
            pw = NP(v) + ("" if e == 1 else f"^{{{e}}}")
            body = pw if a == 1 else f"{N(a)} × {pw}"
        if not out:
            out = (MI if c < 0 else "") + body
        else:
            out += f" {MI if c < 0 else '+'} {body}"
    return out or "0"


def gx(p, lo, hi, n=34):
    """p 에서 멀어질수록 성기게 — p + lo … p + hi (기하 간격, hi 쪽 부호 그대로)"""
    sg = 1 if hi > 0 else -1
    a, b = abs(lo), abs(hi)
    return [p + sg * a * (b / a) ** (i / n) for i in range(n + 1)]

def pcurve(pl, fn, xs, at="q", c="sky", w=4.5):
    """Plane.curve 와 같지만 x 자리를 직접 준다(점근선 · 시작점 가까이 촘촘히)"""
    pts, segs = [], []
    for t in xs:
        try:
            v = fn(t)
        except (ZeroDivisionError, ValueError):
            v = None
        if v is None or not (pl.yr[0] - 0.05 <= v <= pl.yr[1] + 0.05):
            if len(pts) > 1:
                segs.append(pts)
            pts = []
            continue
        pts.append(pl.P(t, v))
    if len(pts) > 1:
        segs.append(pts)
    return [pl.f.poly(sg, at=at, c=c, w=w, z=False, dr=True) for sg in segs]

def ptj(yv):
    return "을" if bat(yv) else "를"


# ══════════ 합성함수와 역함수 ══════════
def func():
    S = Set("func", "함수 — 합성함수와 역함수", "합성·역함수",
            {1: "합성함수의 값", 2: "합성함수의 식", 3: "역함수 구하기", 4: "역함수의 값", 5: "합성함수로 함수 찾기"},
            mixed=True, pp=10,
            tips={1: "(f∘g)(a) = f(g(a)) — 안쪽 g(a)부터",
                  2: "(f∘g)(x) = f(g(x)) — f의 x 자리에 g(x)를 통째로",
                  3: "y = f(x)를 x에 대해 풀고 x와 y를 바꿔요",
                  4: "f^{−1}(a) = k ⇔ f(k) = a — 역함수를 구하지 않아도 돼요",
                  5: "모르는 함수를 g(x) = px + r로 놓고 계수 비교"},
            note="합성함수는 ‘안쪽부터’, 역함수는 ‘거꾸로 되돌리기’예요. f^{−1}(a)는 f(□) = a인 □를 찾는 것이라는 뜻을 먼저 잡게 해 주세요.")
    R = rng(2301)

    def rl():
        return R.choice([-3, -2, 2, 3, 4]), R.choice([-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6])

    def g1():
        a, b = rl()
        c, d, e = R.choice([1, 2, -1]), R.randint(-3, 3), R.randint(-4, 4)
        gcs = [c, d, e]
        f_ = lambda t: a * t + b
        g_ = lambda t: c * t * t + d * t + e
        v = R.randint(-3, 3)
        gs = PS(c * x ** 2 + d * x + e)
        if S.count(1) % 2 == 0:
            gv = g_(v)
            q = f"f(x) = {LIN(a, b)}, g(x) = {gs}일 때, (f∘g)({N(v)})의 값을 구하세요."
            lines = [L(f"g({N(v)}) = {AT(gcs, v)} = {N(gv)}", memo="안쪽 g부터"),
                     L(f"(f∘g)({N(v)}) = f({N(gv)}) = {AT([a, b], gv)} = {N(f_(gv))}")]
            ans = f_(gv)
        else:
            fv = f_(v)
            q = f"f(x) = {LIN(a, b)}, g(x) = {gs}일 때, (g∘f)({N(v)})의 값을 구하세요."
            lines = [L(f"f({N(v)}) = {AT([a, b], v)} = {N(fv)}", memo="안쪽 f부터"),
                     L(f"(g∘f)({N(v)}) = g({N(fv)}) = {AT(gcs, fv)} = {N(g_(fv))}")]
            ans = g_(fv)
        S.add(1, q, N(ans), "(f∘g)(a) = f(g(a)) — 안쪽부터", lines, None, key=q)
    fill(S, 1, 20, g1)

    def g2():
        a, b = rl()
        c, d = R.choice([1, 2, -1, 3]), R.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        F = a * x + b
        G = c * x ** 2 + d
        if S.count(2) % 2 == 0:
            res = sp.expand(F.subs(x, G))
            q = f"f(x) = {LIN(a, b)}, g(x) = {PS(G)}일 때, (f∘g)(x)를 구하세요."
            lines = [L(f"(f∘g)(x) = f(g(x)) = f({PS(G)})", memo="f의 x 자리에 g(x)"),
                     L(f"{N(a)}({PS(G)}){TAIL(b)} = {PS(res)}")]
        else:
            res = sp.expand(G.subs(x, F))
            q = f"f(x) = {LIN(a, b)}, g(x) = {PS(G)}일 때, (g∘f)(x)를 구하세요."
            lines = [L(f"(g∘f)(x) = g(f(x)) = g({LIN(a, b)})", memo="g의 x 자리에 f(x)"),
                     L(f"{'' if c == 1 else (MI if c == -1 else N(c))}({LIN(a, b)})^{{2}}{TAIL(d)} = {PS(res)}")]
        S.add(2, q, PS(res), "바깥 함수의 x 자리에 안쪽 함수를 통째로", lines, None, omr="ex", ident=True, key=q)
    fill(S, 2, 20, g2)

    def g3():
        a, b = rl()
        im, ib = Fr(1, a), Fr(-b, a)
        q = f"함수 f(x) = {LIN(a, b)}의 역함수 f^{{−1}}(x)를 구하세요."
        lines = [L(f"y = {LIN(a, b)} → {N(a)}x = y{TAIL(-b)} → x = {LIN(im, ib, 'y')}", memo="x에 대해 풀기"),
                 L(f"f^{{−1}}(x) = {LIN(im, ib)}", memo="x와 y를 바꿔요")]
        S.add(3, q, f"f^{{−1}}(x) = {LIN(im, ib)}", "x에 대해 풀고 x, y 바꾸기", lines, None, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = rl()
        if S.count(4) % 2 == 0:
            t = R.randint(-4, 5)
            v = a * t + b
            q = f"함수 f(x) = {LIN(a, b)}에 대하여 f^{{−1}}({N(v)})의 값을 구하세요."
            lines = [L(f"f^{{−1}}({N(v)}) = k라 하면 f(k) = {N(v)}", memo="역함수를 구하지 않고"),
                     L(f"{N(a)}k{TAIL(b)} = {N(v)}"), L(f"k = {N(t)}")]
            S.add(4, q, N(t), "f^{−1}(a) = k ⇔ f(k) = a", lines, None, sub={"k": t}, key=q)
        else:
            c, d = R.choice([2, 3, -1, -2]), R.randint(-4, 4)
            s = R.randint(-3, 3)
            gs = c * s + d
            kk = Fr(gs - b, a)
            if kk.denominator != 1:
                return
            q = f"f(x) = {LIN(a, b)}, g(x) = {LIN(c, d)}일 때, (f^{{−1}}∘g)({N(s)})의 값을 구하세요."
            lines = [L(f"g({N(s)}) = {AT([c, d], s)} = {N(gs)}", memo="안쪽 g부터"),
                     L(f"f^{{−1}}({N(gs)}) = k라 하면 {N(a)}k{TAIL(b)} = {N(gs)}"), L(f"k = {N(kk)}")]
            S.add(4, q, N(kk), "안쪽 g부터, 역함수 값은 f(k) = □로", lines, None, sub={"k": kk}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        a, b = rl()
        p, r = R.choice([-3, -2, 2, 3]), R.randint(-5, 5)
        H = sp.expand(a * (p * x + r) + b)
        hm_, hb_ = int(H.coeff(x, 1)), int(H.coeff(x, 0))
        q = f"f(x) = {LIN(a, b)}이고 (f∘g)(x) = {LIN(hm_, hb_)}일 때, 일차함수 g(x)를 구하세요."
        lines = [L("g(x) = px + r로 놓아요"),
                 L(f"f(g(x)) = {N(a)}(px + r){TAIL(b)} = {LIN(hm_, hb_)}"),
                 L(f"{N(a)}p = {N(hm_)} → p = {N(p)}, {N(a)}r{TAIL(b)} = {N(hb_)} → r = {N(r)}", memo="계수 비교"),
                 L(f"g(x) = {LIN(p, r)}")]
        S.add(5, q, f"g(x) = {LIN(p, r)}", "모르는 함수를 일차식으로 놓고 계수 비교", lines, None, omr="ex", sub={"p": p, "r": r}, ident=True, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 유리함수와 무리함수 ══════════
def hyp_rhs(k, p):
    return (f"{{{k}/{XM(p)}}}" if k > 0 else f"{MI}{{{-k}/{XM(p)}}}")

def hyp_fig(f, k, p, q_, at="q"):
    pl = Plane(f, (p - 6.5, p + 6.5), (q_ - 6.5, q_ + 6.5), box=(40, 30, 620, 650))
    pl.axes(at=at, lab_step=2)
    fn = lambda t: k / (t - p) + q_
    pcurve(pl, fn, gx(p, -0.12, -6.5)[::-1], at=at)
    pcurve(pl, fn, gx(p, 0.12, 6.5), at=at)
    f.line(*pl.P(p, q_ - 6.5), *pl.P(p, q_ + 6.5), c="coral", w=2.5, d=True, at=at)
    f.line(*pl.P(p - 6.5, q_), *pl.P(p + 6.5, q_), c="coral", w=2.5, d=True, at=at)
    return pl

def shift_words(p, q_):
    ws = []
    if p:
        ws.append(f"x축 방향으로 {N(p)}만큼")
    if q_:
        ws.append(f"y축 방향으로 {N(q_)}만큼")
    return ", ".join(ws) + " 평행이동"

def ratf():
    S = Set("ratf", "유리함수와 무리함수 — 점근선과 평행이동", "유리·무리함수",
            {1: "유리함수의 점근선", 2: "분수식 꼴의 점근선", 3: "유리함수 위의 점과 미정계수", 4: "무리함수의 정의역과 치역", 5: "무리함수의 그래프와 미정계수"},
            mixed=True, pp=8,
            tips={1: "y = {k/x − p} + q: 점근선 x = p, y = q — y = {k/x}를 평행이동한 그래프",
                  2: "분자를 분모로 나누어 {k/x − p} + q 꼴로",
                  3: "지나는 점의 좌표를 대입해 k를 구해요",
                  4: "근호 안 ≥ 0으로 정의역, 시작점 (p, q)에서 치역",
                  5: "지나는 점 대입 → 양변 제곱"},
            note="유리함수 · 무리함수 모두 ‘기본형을 평행이동’한 그래프예요. 점근선(유리함수)과 시작점(무리함수)을 먼저 찾게 하면 그래프와 식이 함께 보여요.")
    R = rng(2302)

    def g1():
        k, p, q_ = R.choice([-6, -4, -3, -2, -1, 1, 2, 3, 4, 6]), R.randint(-4, 4), R.randint(-4, 4)
        if p == 0 and q_ == 0:
            return
        f = Fig()
        hyp_fig(f, k, p, q_)
        e = f"y = {hyp_rhs(k, p)}{TAIL(q_)}"
        q = f"유리함수 {e}의 그래프의 점근선의 방정식을 구하세요."
        lines = [L(f"y = {{k/x − p}} + q 꼴 → p = {N(p)}, q = {N(q_)}", memo="표준형과 견주기"),
                 L(f"점근선 x = {N(p)}, y = {N(q_)}", memo=f"y = {hyp_rhs(k, 0)}의 점근선을 평행이동")]
        S.add(1, q, f"x = {N(p)}, y = {N(q_)}", "y = {k/x − p} + q → 점근선 x = p, y = q", lines, f.out(), ap=f"x={p}, y={q_}", omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        p, q_, k = R.randint(-4, 4), R.choice([-4, -3, -2, -1, 1, 2, 3, 4]), R.choice([-5, -3, -2, -1, 1, 2, 3, 5])
        if p == 0:
            return
        a, b = q_, k - q_ * p
        num = LIN(a, b)
        e = f"y = {{{num}/{XM(p)}}}"
        assert sp.simplify((a * x + b) / (x - p) - (k / (x - p) + q_)) == 0
        q = f"유리함수 {e}의 그래프의 점근선의 방정식을 구하세요."
        lines = [L(f"{{{num}/{XM(p)}}} = {{{N(q_)}({XM(p)}){TAIL(k)}/{XM(p)}}} = {hyp_rhs(k, p)}{TAIL(q_)}", memo="분자를 분모로 나누기"),
                 L(f"점근선 x = {N(p)}, y = {N(q_)}")]
        f = Fig()
        hyp_fig(f, k, p, q_, at=0)
        S.add(2, q, f"x = {N(p)}, y = {N(q_)}", "분자를 분모로 나누어 표준형으로", lines, f.out(), ap=f"x={p}, y={q_}", omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        p, q_ = R.randint(-3, 3), R.randint(-3, 3)
        k = R.choice([-6, -4, -3, -2, 2, 3, 4, 6])
        d = R.choice([d for d in (-3, -2, -1, 1, 2, 3) if k % d == 0])
        x0 = p + d
        y0 = k // d + q_
        q = f"유리함수 y = {{k/{XM(p)}}}{TAIL(q_)}의 그래프가 점 ({N(x0)}, {N(y0)}){ptj(N(y0))} 지날 때, 상수 k의 값을 구하세요."
        sub_den = f"{NP(x0)} {'+' if p < 0 else MI} {abs(p)}" if p else NP(x0)
        lines = [L(f"{N(y0)} = {{k/{sub_den}}}{TAIL(q_)}" + (f" = {{k/{N(d)}}}{TAIL(q_)}" if p else ""), memo="지나는 점 대입"),
                 L(f"{{k/{N(d)}}} = {N(y0 - q_)} → k = {N(k)}")]
        f = Fig()
        pl = hyp_fig(f, k, p, q_, at=1)
        pl.pt(x0, y0, label=f"({N(x0)}, {N(y0)})", pos="ne" if x0 >= p else "nw", f="coral")
        S.add(3, q, N(k), "지나는 점을 대입", lines, f.out(), sub={"k": k}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.choice([1, 2, 3, -1, -2])
        s = R.choice([1, 1, -1])
        p, q_ = R.randint(-4, 4), R.randint(-4, 4)
        ac = "" if a == 1 else (MI if a == -1 else N(a))
        inner = (f"{ac}({XM(p)})" if a != 1 else XM(p)) if p else f"{ac}x"
        e = f"y = {'' if s > 0 else MI}√{{{inner}}}{TAIL(q_)}"
        dom = f"x ≥ {N(p)}" if a > 0 else f"x ≤ {N(p)}"
        rng_ = f"y ≥ {N(q_)}" if s > 0 else f"y ≤ {N(q_)}"
        q = f"무리함수 {e}의 정의역과 치역을 구하세요."
        lines = [L(f"{inner} ≥ 0 → {dom}", memo="근호 안 ≥ 0"),
                 L(f"{'' if s > 0 else MI}√{{{inner}}} {'≥' if s > 0 else '≤'} 0 → {rng_}", memo=f"시작점 ({N(p)}, {N(q_)})"),
                 L(f"정의역 {dom}, 치역 {rng_}")]
        f = Fig()
        pl = Plane(f, (p - 6.5, p + 6.5), (q_ - 6.5, q_ + 6.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=2)
        fn = lambda t: s * math.sqrt(a * (t - p)) + q_ if a * (t - p) >= 0 else None
        xs = [p] + gx(p, 0.02, 6.5, 30) if a > 0 else [p] + gx(p, -0.02, -6.5, 30)
        pcurve(pl, fn, xs)
        pl.pt(p, q_, label=f"({N(p)}, {N(q_)})", pos="s" if s > 0 else "n", f="coral", at=1)
        S.add(4, q, f"정의역 {dom}, 치역 {rng_}", "근호 안 ≥ 0 · 시작점에서 치역", lines, f.out(), ap=f"{dom}; {rng_}", omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        a = R.choice([1, 2, 3, 4, -1, -2, -4])
        p, q_ = R.randint(-4, 3), R.randint(-3, 3)
        t = R.choice([1, 2, 3])
        dx = Fr(t * t, a)
        if dx.denominator != 1:
            return
        dx = int(dx)
        x0, y0 = p + dx, t + q_
        inner = f"a({XM(p)})" if p else "ax"
        q = f"무리함수 y = √{{{inner}}}{TAIL(q_)}의 그래프가 점 ({N(x0)}, {N(y0)}){ptj(N(y0))} 지날 때, 상수 a의 값을 구하세요."
        ca = "a" if dx == 1 else (MI + "a" if dx == -1 else f"{N(dx)}a")
        lines = [L(f"{N(y0)} = √{{a × {NP(dx)}}}{TAIL(q_)}", memo="지나는 점 대입"),
                 L(f"√{{{ca}}} = {t} → {ca} = {t * t}", memo="양변 제곱"),
                 L(f"a = {N(a)}")]
        S.add(5, q, N(a), "지나는 점 대입 → 양변 제곱", lines, None, sub={"a": a}, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 지수함수와 로그함수 ══════════
def expg():
    S = Set("expg", "지수함수와 로그함수 — 그래프 · 대소 · 방정식", "지수·로그함수",
            {1: "지수함수의 그래프", 2: "로그함수의 그래프", 3: "크기 비교", 4: "지수방정식 · 부등식", 5: "로그방정식 · 최대최소"},
            mixed=True, pp=8,
            tips={1: "y = a^{x − p} + q: 점근선 y = q, 점 (p, 1 + q)를 지나요",
                  2: "y = log_{a}(x − p) + q: 점근선 x = p, 점 (p + 1, q)를 지나요",
                  3: "밑을 같게 만든 뒤 — 밑 > 1이면 지수가 클수록 커요",
                  4: "양변의 밑을 같게 → 지수끼리. 밑이 1보다 작으면 부등호 방향 반대",
                  5: "log_{a}f(x) = b ⇔ f(x) = a^{b}(진수 > 0) · 구간의 양 끝에서 최대 · 최소"},
            note="지수함수와 로그함수는 서로 역함수예요. 그래프의 점근선과 지나는 점(지수: (0, 1), 로그: (1, 0))의 평행이동으로 정리하게 해 주세요.")
    R = rng(2303)

    def g1():
        a = R.choice([2, 3, 4, 5])
        p, q_ = R.randint(-3, 3), R.randint(-4, 4)
        if p == 0 and q_ == 0:
            return
        e = f"y = {a}^{{{XM(p)}}}{TAIL(q_)}"
        f = Fig()
        pl = Plane(f, (-6.5, 6.5), (-6.5, 6.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=2)
        pl.curve(lambda t: a ** (t - p) + q_ if a ** (t - p) + q_ < 7 else None, -6.5, 6.5, n=64)
        f.line(*pl.P(-6.5, q_), *pl.P(6.5, q_), c="coral", w=2.5, d=True, at=0)
        if S.count(1) % 2 == 0:
            q = f"함수 {e}의 그래프의 점근선의 방정식을 구하세요."
            lines = [L(f"y = {a}^{{x}}의 점근선은 x축(y = 0)", memo="기본형"),
                     L(f"y축 방향으로 {N(q_)}만큼 평행이동 → 점근선 y = {N(q_)}" if q_ else "y축 방향으로는 평행이동하지 않아요 → 점근선 y = 0")]
            S.add(1, q, f"y = {N(q_)}", "지수함수의 점근선은 y = q", lines, f.out(), omr="ex", key=q)
        else:
            q = f"함수 {e}의 그래프가 항상 지나는 점의 좌표를 구하세요."
            pl.pt(p, 1 + q_, label=f"({N(p)}, {N(1 + q_)})", pos="nw", f="coral", at=1)
            lines = [L(f"y = {a}^{{x}}의 그래프는 점 (0, 1)을 지나요", memo="a^{0} = 1"),
                     L(f"점 (0, 1) → ({N(p)}, {N(1 + q_)})", memo="같은 만큼 평행이동")]
            S.add(1, q, f"({N(p)}, {N(1 + q_)})", "기본형이 지나는 (0, 1)을 평행이동", lines, f.out(), omr="pt", key=q)
    fill(S, 1, 20, g1)

    def g2():
        a = R.choice([2, 3, 5, 10])
        p, q_ = R.randint(-3, 3), R.randint(-4, 4)
        if p == 0 and q_ == 0:
            return
        arg = f"({XM(p)})" if p else "x"
        e = f"y = log_{{{a}}}{arg}{TAIL(q_)}"
        f = Fig()
        pl = Plane(f, (-6.5, 6.5), (-6.5, 6.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=2)
        pcurve(pl, lambda t: math.log(t - p, a) + q_, gx(p, max(a ** (-7.0 - q_), 1e-12), 6.5 - p, 52))
        f.line(*pl.P(p, -6.5), *pl.P(p, 6.5), c="coral", w=2.5, d=True, at=0)
        if S.count(2) % 2 == 0:
            q = f"함수 {e}의 그래프의 점근선의 방정식을 구하세요."
            lines = [L(f"y = log_{{{a}}}x의 점근선은 y축(x = 0)", memo="기본형"),
                     L(f"x축 방향으로 {N(p)}만큼 평행이동 → 점근선 x = {N(p)}" if p else "x축 방향으로는 평행이동하지 않아요 → 점근선 x = 0")]
            S.add(2, q, f"x = {N(p)}", "로그함수의 점근선은 x = p", lines, f.out(), omr="ex", key=q)
        else:
            q = f"함수 {e}의 그래프가 항상 지나는 점의 좌표를 구하세요."
            pl.pt(p + 1, q_, label=f"({N(p + 1)}, {N(q_)})", pos="se", f="coral", at=1)
            lines = [L(f"y = log_{{{a}}}x의 그래프는 점 (1, 0)을 지나요", memo=f"log_{{{a}}}1 = 0"),
                     L(f"점 (1, 0) → ({N(p + 1)}, {N(q_)})", memo="같은 만큼 평행이동")]
            S.add(2, q, f"({N(p + 1)}, {N(q_)})", "기본형이 지나는 (1, 0)을 평행이동", lines, f.out(), omr="pt", key=q)
    fill(S, 2, 20, g2)

    def g3():
        base = R.choice([2, 3])
        pw = [1, 2, 3]
        es = [Fr(R.randint(1, 9), 10) for _ in range(3)]
        vals = [pw[i] * es[i] for i in range(3)]
        if len(set(vals)) < 3:
            return
        idx = [0, 1, 2]
        R.shuffle(idx)
        names = {i: f"{base ** pw[i]}^{{{DEC(es[i])}}}" for i in range(3)}
        shown = [names[i] for i in idx]
        best = max(range(3), key=lambda i: vals[i])
        q = f"세 수 {', '.join(shown)} 중에서 가장 큰 수를 구하세요."
        conv = ", ".join(names[i] if pw[i] == 1 else f"{names[i]} = {base}^{{{DEC(vals[i])}}}" for i in idx)
        lines = [L(conv, memo=f"밑을 {RO(base)} 맞추기"),
                 L(f"밑 {base} > 1 → 지수가 클수록 커요"),
                 L(f"{J(names[best], '이', '가')} 가장 커요")]
        S.add(3, q, names[best], "밑을 같게 만든 뒤 지수 비교", lines, None, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.choice([2, 3, 5])
        if S.count(4) % 2 == 0:
            m, c = R.randint(1, 3), R.randint(-3, 3)
            e = R.randint(2, {2: 6, 3: 4, 5: 3}[a])
            xv = Fr(e - c, m)
            if xv.denominator != 1:
                return
            ex_ = f"{a}^{{{LIN(m, c)}}}"
            q = f"방정식 {ex_} = {J(a ** e, '을', '를')} 푸세요."
            lines = [L(f"{a ** e} = {a}^{{{e}}}", memo="밑을 같게"), L(f"{LIN(m, c)} = {e}", memo="지수끼리"), L(f"x = {N(xv)}")]
            S.add(4, q, f"x = {N(xv)}", "밑을 같게 → 지수끼리", lines, None, omr="ex", sub={"x": xv}, key=q)
        else:
            e = R.randint(1, {2: 5, 3: 4, 5: 3}[a])
            op = R.choice([">", "<", "≥", "≤"])
            flip = {">": "<", "<": ">", "≥": "≤", "≤": "≥"}[op]
            q = f"부등식 ({{1/{a}}})^{{x}} {op} {J(a ** e, '을', '를')} 푸세요."
            lines = [L(f"({{1/{a}}})^{{x}} = {a}^{{{MI}x}}, {a ** e} = {a}^{{{e}}}", memo="밑을 같게"),
                     L(f"{a}^{{{MI}x}} {op} {a}^{{{e}}} → {MI}x {op} {e}", memo=f"밑 {a} > 1 → 지수끼리 그대로"),
                     L(f"x {flip} {MI}{e}", memo="양변에 −1 → 부등호 방향 반대")]
            S.add(4, q, f"x {flip} {MI}{e}", "밑을 같게 — 밑이 1보다 크면 부등호 그대로", lines, None, omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        a = R.choice([2, 3])
        if S.count(5) % 2 == 0:
            m, c = R.randint(1, 2), R.randint(-4, 4)
            e = R.randint(1, 4 if a == 2 else 3)
            xv = Fr(a ** e - c, m)
            if xv.denominator != 1:
                return
            q = f"방정식 log_{{{a}}}({LIN(m, c)}) = {J(e, '을', '를')} 푸세요."
            lines = [L(f"{LIN(m, c)} = {a}^{{{e}}} = {a ** e}", memo="로그의 정의"), L(f"x = {N(xv)}"),
                     L(f"진수 {LIN(m, c)} = {a ** e} > 0", memo="진수 조건 확인")]
            S.add(5, q, f"x = {N(xv)}", "log_{a}f(x) = b ⇔ f(x) = a^{b}, 진수 > 0", lines, None, omr="ex", sub={"x": xv}, key=q)
        else:
            lo, hi = sorted(R.sample(range(-2, 5), 2))
            c = R.randint(-5, 5)
            inc = R.random() < 0.6
            bs = str(a) if inc else f"({{1/{a}}})"
            b_ = Fr(a) if inc else Fr(1, a)
            vmax, vmin = (hi, lo) if inc else (lo, hi)
            mx, mn = b_ ** vmax + c, b_ ** vmin + c
            q = f"{N(lo)} ≤ x ≤ {N(hi)}에서 함수 y = {bs}^{{x}}{TAIL(c)}의 최댓값과 최솟값의 합을 구하세요."
            lines = [L(f"밑 {FR(b_)} > 1 → 증가함수" if inc else f"0 < 밑 {FR(b_)} < 1 → 감소함수", memo="구간의 양 끝"),
                     L(f"최댓값 {bs}^{{{N(vmax)}}}{TAIL(c)} = {FR(mx)}, 최솟값 {bs}^{{{N(vmin)}}}{TAIL(c)} = {FR(mn)}", memo=f"x = {N(vmax)}에서 최대"),
                     L(f"{FR(mx)} + {('(' + FR(mn) + ')') if mn < 0 else FR(mn)} = {FR(mx + mn)}")]
            S.add(5, q, FR(mx + mn), "증가함수는 오른쪽 끝, 감소함수는 왼쪽 끝에서 최대", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 삼각함수 ══════════
SPC = {0: ("0", "1", "0"), 30: ("{1/2}", "{√{3}/2}", "{√{3}/3}"), 45: ("{√{2}/2}", "{√{2}/2}", "1"), 60: ("{√{3}/2}", "{1/2}", "√{3}"), 90: ("1", "0", None)}

def rad(deg):
    v = Fr(deg, 180)
    if v == 0:
        return "0"
    sg = MI if v < 0 else ""
    n, d = abs(v.numerator), v.denominator
    if d == 1:
        return f"{sg}{'' if n == 1 else n}π"
    return f"{sg}{{{'' if n == 1 else n}π/{d}}}"

def trig_val(fn, deg):
    d = deg % 360
    ref = min(d % 180, 180 - d % 180)
    v = SPC[ref][{"sin": 0, "cos": 1, "tan": 2}[fn]]
    if v is None:
        return None
    r = math.radians(d)
    s = {"sin": math.sin, "cos": math.cos, "tan": math.tan}[fn](r)
    if abs(s) < 1e-9:
        return "0"
    return v if s > 0 else (MI + v)

def unit_circle(f, at="q"):
    f.circ(330, 340, 220, c="ink", sw=2.5, at=at)
    f.line(80, 340, 585, 340, c="soft", w=2, ar=1, at=at)
    f.line(330, 595, 330, 85, c="soft", w=2, ar=1, at=at)
    f.text(575, 378, "x", z=28, c="soft", at=at)
    f.text(352, 100, "y", z=28, c="soft", at=at)

def trig():
    S = Set("trig", "삼각함수 — 호도법 · 일반각 · 주기와 최대최소", "삼각함수",
            {1: "호도법", 2: "일반각의 삼각함수 값", 3: "삼각함수 사이의 관계", 4: "최댓값 · 최솟값 · 주기", 5: "간단한 삼각방정식"},
            pp=10,
            tips={1: "180° = π — 도 × {π/180} = 라디안",
                  2: "동경이 있는 사분면으로 부호, 기준각으로 크기",
                  3: "sin^{2}θ + cos^{2}θ = 1, tan θ = {sin θ/cos θ} — 사분면으로 부호",
                  4: "y = a sin bx + c (a > 0, b > 0): 최댓값 a + c, 최솟값 −a + c, 주기 {2π/b}",
                  5: "단위원에서 같은 값을 갖는 두 각을 찾아요"},
            note="삼각함수 값은 단위원 위의 점 (cos θ, sin θ)로 생각하게 해 주세요. 사분면의 부호와 특수각(30°, 45°, 60°)만 확실하면 어떤 일반각도 계산할 수 있어요.")
    R = rng(2304)

    def g1():
        deg = R.choice([30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 72, 36, 15, 18, 20, 540, 450, 75, 105])
        if S.count(1) % 2 == 0:
            q = f"{deg}°를 호도법으로 나타내세요."
            lines = [L(f"{deg} × {{π/180}} = {rad(deg)}", memo="180° = π")]
            S.add(1, q, rad(deg), "도 × {π/180}", lines, None, omr="ex", key=q)
        else:
            q = f"{J(rad(deg), '을', '를')} 육십분법으로 나타내세요."
            lines = [L(f"{rad(deg)} × {{180°/π}} = {deg}°", memo="π = 180°")]
            S.add(1, q, f"{deg}°", "라디안 × {180°/π}", lines, None, ap=str(deg), key=q)
    fill(S, 1, 20, g1)

    def g2():
        deg = R.choice([120, 135, 150, 210, 225, 240, 300, 315, 330, 390, 405, 420, -30, -45, -60, -120, -150, 180, 270, 480, 510])
        fn = R.choice(["sin", "cos", "tan"])
        v = trig_val(fn, deg)
        if v is None:
            return
        d = deg % 360
        quad_ = 1 if d < 90 else 2 if d < 180 else 3 if d < 270 else 4
        ref = min(d % 180, 180 - d % 180)
        th = rad(deg)
        arg = th if deg > 0 else f"({th})"
        f = Fig()
        unit_circle(f)
        P = ang_pt(330, 340, 220, d)
        f.line(330, 340, *P, c="coral", w=3.5)
        f.dot(*P, r=8, f="coral")
        if deg > 0:
            f.arc(330, 340, 46, 0, d, c="teal", sw=3)
        else:
            f.arc(330, 340, 46, d, 360, c="teal", sw=3)
        f.line(*P, P[0], 340, c="gold", w=2.5, d=True, at=1)
        q = f"{fn} {arg}의 값을 구하세요."
        lines = [L(f"{th} → {N(deg)}°" + (f" — 동경은 {d}°와 같아요" if d != deg else ""), memo="일반각"),
                 L(f"제{quad_}사분면 → {fn}의 부호 {'+' if not v.startswith(MI) else MI}" if d % 90 else "동경이 좌표축 위에 있어요", memo="부호"),
                 L(f"{fn} {arg} = {v}", memo=f"기준각 {ref}°" if d % 90 else "단위원 위의 점")]
        S.add(2, q, v, "사분면으로 부호, 기준각으로 크기", lines, f.out(), omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        a, b, c = R.choice([(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (8, 15, 17), (15, 8, 17)])
        quad_ = R.randint(2, 4)
        sx = {2: -1, 3: -1, 4: 1}[quad_]
        sy = {2: 1, 3: -1, 4: -1}[quad_]
        sinv, cosv = Fr(sy * b, c), Fr(sx * a, c)
        tanv = sinv / cosv
        given = R.choice(["sin", "cos"])
        other_fn = "cos" if given == "sin" else "sin"
        want = R.choice([other_fn, "tan"])
        gv = sinv if given == "sin" else cosv
        ov = cosv if given == "sin" else sinv
        wv = {"sin": sinv, "cos": cosv, "tan": tanv}[want]
        q = f"θ가 제{quad_}사분면의 각이고 {given} θ = {FR(gv)}일 때, {want} θ의 값을 구하세요."
        lines = [L(f"{other_fn}^{{2}}θ = 1 {MI} ({FR(gv)})^{{2}} = {FR(ov * ov)}", memo="sin^{2}θ + cos^{2}θ = 1"),
                 L(f"제{quad_}사분면에서 {other_fn} θ {'>' if ov > 0 else '<'} 0 → {other_fn} θ = {FR(ov)}", memo="사분면으로 부호")]
        if want == "tan":
            lines.append(L(f"tan θ = {{sin θ/cos θ}} = {FR(sinv)} ÷ {NP(cosv)} = {FR(tanv)}"))
        S.add(3, q, FR(wv), "제곱 관계로 크기, 사분면으로 부호", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.choice([1, 2, 3, 4, 5]) * R.choice([1, -1])
        b = R.choice([1, 2, 3, 4, Fr(1, 2)])
        c = R.randint(-3, 3)
        fn = R.choice(["sin", "cos"])
        bs = "" if b == 1 else FR(b)
        e = f"y = {'' if a == 1 else (MI if a == -1 else N(a))}{fn} {bs}x{TAIL(c)}"
        mx, mn = abs(a) + c, -abs(a) + c
        per = Fr(2) / Fr(b)
        per_s = rad(int(per * 180))
        q = f"함수 {e}의 최댓값, 최솟값, 주기를 구하세요."
        lines = [L(f"최댓값 {abs(a)}" + (f" + {NP(c)} = {N(mx)}" if c else ""), memo=f"−1 ≤ {fn} {bs}x ≤ 1"),
                 L(f"최솟값 {MI}{abs(a)}" + (f" + {NP(c)} = {N(mn)}" if c else "")),
                 L(f"주기 2π ÷ {FR(b)} = {per_s}" if b != 1 else "주기 2π", memo="{2π/b}")]
        S.add(4, q, f"최댓값 {N(mx)}, 최솟값 {N(mn)}, 주기 {per_s}", f"−1 ≤ {fn} bx ≤ 1로 최대 · 최소, 주기는 {{2π/b}}", lines, None, ap=f"{mx}, {mn}, {plain(per_s)}", omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        fn = R.choice(["sin", "cos", "tan"])
        targets = {"sin": [("{1/2}", [30, 150]), (MI + "{1/2}", [210, 330]), ("{√{2}/2}", [45, 135]), (MI + "{√{3}/2}", [240, 300]), ("{√{3}/2}", [60, 120]), (MI + "{√{2}/2}", [225, 315])],
                   "cos": [("{1/2}", [60, 300]), (MI + "{1/2}", [120, 240]), ("{√{2}/2}", [45, 315]), ("{√{3}/2}", [30, 330]), (MI + "{√{3}/2}", [150, 210]), (MI + "{√{2}/2}", [135, 225])],
                   "tan": [("1", [45, 225]), (MI + "1", [135, 315]), ("√{3}", [60, 240]), ("{√{3}/3}", [30, 210]), (MI + "√{3}", [120, 300]), (MI + "{√{3}/3}", [150, 330])]}[fn]
        val_, sols = R.choice(targets)
        dbl = {"{1/2}": "1", MI + "{1/2}": MI + "1", "{√{2}/2}": "√{2}", MI + "{√{2}/2}": MI + "√{2}", "{√{3}/2}": "√{3}", MI + "{√{3}/2}": MI + "√{3}",
               "1": "2", MI + "1": MI + "2", "√{3}": "2√{3}", "{√{3}/3}": "{2√{3}/3}", MI + "√{3}": MI + "2√{3}", MI + "{√{3}/3}": MI + "{2√{3}/3}"}
        two = R.random() < 0.5
        eq = f"2{fn} x = {dbl[val_]}" if two else f"{fn} x = {val_}"
        q = f"0 ≤ x < 2π일 때, 방정식 {J(eq, '을', '를')} 푸세요."
        ans = f"x = {rad(sols[0])}, {rad(sols[1])}"
        lines = ([L(f"{fn} x = {val_}", memo="양변을 2로 나눠요")] if two else []) + \
                [L(f"{fn}의 값이 {val_}인 동경 두 개", memo="단위원"), L(ans)]
        f = Fig()
        unit_circle(f)
        for dd in sols:
            P = ang_pt(330, 340, 220, dd)
            f.line(330, 340, *P, c="coral", w=3.5, at=len(lines) - 2)
            f.dot(*P, r=8, f="coral", at=len(lines) - 2)
            f.text(*ang_pt(330, 340, 262, dd), rad(dd), z=26, c="coral", at=len(lines) - 1)
        S.add(5, q, ans, "단위원에서 같은 값을 갖는 두 각", lines, f.out(), omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 사인법칙 · 코사인법칙 ══════════
SINV = {30: sp.Rational(1, 2), 45: sp.sqrt(2) / 2, 60: sp.sqrt(3) / 2, 90: sp.Integer(1), 120: sp.sqrt(3) / 2, 135: sp.sqrt(2) / 2, 150: sp.Rational(1, 2)}
SINS = {30: "{1/2}", 45: "{√{2}/2}", 60: "{√{3}/2}", 90: "1", 120: "{√{3}/2}", 135: "{√{2}/2}", 150: "{1/2}"}
COSV = {30: sp.sqrt(3) / 2, 45: sp.sqrt(2) / 2, 60: sp.Rational(1, 2), 90: sp.Integer(0), 120: -sp.Rational(1, 2), 135: -sp.sqrt(2) / 2, 150: -sp.sqrt(3) / 2}
COSS = {30: "{√{3}/2}", 45: "{√{2}/2}", 60: "{1/2}", 90: "0", 120: MI + "{1/2}", 135: MI + "{√{2}/2}", 150: MI + "{√{3}/2}"}

def SS(v):
    """sympy 수(유리수 · 유리수 × √n) → 무대 글자"""
    v = sp.nsimplify(sp.radsimp(v))
    if v.is_Rational:
        return FR(Fr(int(v.p), int(v.q)))
    c, r = v.as_coeff_Mul()
    assert r.is_Pow and r.exp == sp.Rational(1, 2), v
    n = int(r.base)
    c = Fr(int(sp.Rational(c).p), int(sp.Rational(c).q))
    sg = MI if c < 0 else ""
    c = abs(c)
    if c.denominator == 1:
        return f"{sg}{'' if c == 1 else N(c)}√{{{n}}}"
    return f"{sg}{{{'' if c.numerator == 1 else c.numerator}√{{{n}}}/{c.denominator}}}"

def fit(pts, box=(80, 90, 580, 540)):
    """수학 좌표(위가 +) → 그림 칸 안에 비율 그대로"""
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    bx0, by0, bx1, by1 = box
    s = min((bx1 - bx0) / w, (by1 - by0) / h)
    ox = (bx0 + bx1) / 2 - s * (min(xs) + max(xs)) / 2
    oy = (by0 + by1) / 2 + s * (min(ys) + max(ys)) / 2
    return [(ox + s * px, oy - s * py) for px, py in pts]

def tri_draw(f, Ap, Bp, Cp, at="q", fill_at=None):
    G = ((Ap[0] + Bp[0] + Cp[0]) / 3, (Ap[1] + Bp[1] + Cp[1]) / 3)
    f.poly([Ap, Bp, Cp], c="ink", w=3, at=at)
    if fill_at is not None:
        f.poly([Ap, Bp, Cp], c="none", f="teal", fo=0.18, at=fill_at)
    for nm_, P in (("A", Ap), ("B", Bp), ("C", Cp)):
        dx, dy = P[0] - G[0], P[1] - G[1]
        r = math.hypot(dx, dy) or 1
        f.text(P[0] + dx / r * 30, P[1] + dy / r * 30 + 10, nm_, z=28, b=700, at=at)
    return G

def side_lab(f, P, Q, G, s, at="q", c="ink", z=28):
    mx, my = (P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2
    dx, dy = mx - G[0], my - G[1]
    r = math.hypot(dx, dy) or 1
    f.text(mx + dx / r * 30, my + dy / r * 30 + 9, s, z=z, c=c, at=at, b=700)

def tri_AB(A, B):
    """각 A, B(도) · BC = 1 → A, B, C 수학 좌표"""
    Cg = 180 - A - B
    c = math.sin(math.radians(Cg)) / math.sin(math.radians(A))
    Ap = (c * math.cos(math.radians(B)), c * math.sin(math.radians(B)))
    return Ap, (0.0, 0.0), (1.0, 0.0)

def tri_SAS(a, b, Cdeg):
    """BC = a, CA = b, 끼인각 C → A, B, C 수학 좌표"""
    Cp = (0.0, 0.0)
    Bp = (-float(a), 0.0)
    Ap = (-b * math.cos(math.radians(Cdeg)), b * math.sin(math.radians(Cdeg)))
    return Ap, Bp, Cp

def tri_sides(a, b, c):
    """세 변 a(BC) · b(CA) · c(AB) → A, B, C 수학 좌표"""
    xa = (a * a + c * c - b * b) / (2 * a)
    ya = math.sqrt(max(c * c - xa * xa, 0))
    return (xa, ya), (0.0, 0.0), (float(a), 0.0)

def law():
    S = Set("law", "사인법칙과 코사인법칙 · 삼각형의 넓이", "사인·코사인법칙",
            {1: "사인법칙으로 변의 길이", 2: "사인법칙과 외접원", 3: "코사인법칙으로 변의 길이", 4: "코사인법칙으로 각", 5: "삼각형의 넓이"},
            pp=8,
            tips={1: "{a/sin A} = {b/sin B} = {c/sin C}",
                  2: "{a/sin A} = 2R (R은 외접원의 반지름)",
                  3: "c^{2} = a^{2} + b^{2} − 2ab cos C",
                  4: "cos C = {a^{2} + b^{2} − c^{2}/2ab}",
                  5: "S = {1/2}ab sin C"},
            note="사인법칙은 ‘마주 보는 변과 각의 쌍’, 코사인법칙은 ‘두 변과 끼인각’이나 ‘세 변’이 주어질 때 써요. 주어진 정보로 법칙을 고르게 해 주세요.")
    R = rng(2305)

    def g1():
        A, B = R.sample([30, 45, 60, 120, 135], 2)
        if A + B >= 180:
            return
        a = R.choice([2, 3, 4, 6, 8, 10, 12])
        bv = a * SINV[B] / SINV[A]
        q = f"삼각형 ABC에서 a = {a}, A = {A}°, B = {B}°일 때, b의 값을 구하세요."
        lines = [L("{a/sin A} = {b/sin B}", memo="마주 보는 변과 각의 쌍"),
                 L(f"b = {{a sin B/sin A}} = {a} × {SINS[B]} ÷ {SINS[A]} = {SS(bv)}")]
        f = Fig()
        Ap, Bp, Cp = fit(list(tri_AB(A, B)))
        G = tri_draw(f, Ap, Bp, Cp)
        angle_mark(f, Ap, Bp, Cp, r=40, label=f"{A}°", z=24)
        angle_mark(f, Bp, Cp, Ap, r=40, label=f"{B}°", z=24)
        side_lab(f, Bp, Cp, G, str(a))
        side_lab(f, Cp, Ap, G, "b", c="coral")
        S.add(1, q, SS(bv), "사인법칙 {a/sin A} = {b/sin B}", lines, f.out(), omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        A = R.choice([30, 45, 60, 90, 120, 135, 150])
        Rv = R.randint(2, 9)
        a = 2 * Rv * SINV[A]
        f = Fig()
        cx, cy, rr = 330, 330, 230
        Ap = ang_pt(cx, cy, rr, 90)
        Bp = ang_pt(cx, cy, rr, 270 - A)
        Cp = ang_pt(cx, cy, rr, 270 + A)
        f.circ(cx, cy, rr, c="soft", sw=2.5)
        G = tri_draw(f, Ap, Bp, Cp)
        f.dot(cx, cy, r=6, f="ink")
        f.text(cx + 18, cy - 12, "O", z=24, c="soft")
        f.line(cx, cy, *Bp, c="teal", w=3, d=True, at=1)
        f.text((cx + Bp[0]) / 2 - 16, (cy + Bp[1]) / 2 - 8, "R", z=26, c="teal", b=700, at=1)
        if A < 120:
            angle_mark(f, Ap, Bp, Cp, r=40, label=f"{A}°", z=24)
        else:
            angle_mark(f, Ap, Bp, Cp, r=28)
            f.text(Ap[0], Ap[1] - 44, f"{A}°", z=24, b=700)
        if S.count(2) % 2 == 0:
            q = f"삼각형 ABC에서 a = {SS(a)}, A = {A}°일 때, 삼각형 ABC의 외접원의 반지름의 길이를 구하세요."
            side_lab(f, Bp, Cp, (cx, cy) if A < 90 else G, SS(a))
            lines = [L("{a/sin A} = 2R", memo="사인법칙"), L(f"2R = {SS(a)} ÷ {SINS[A]} = {2 * Rv}"), L(f"R = {Rv}")]
            ans = str(Rv)
        else:
            q = f"외접원의 반지름의 길이가 {Rv}인 삼각형 ABC에서 A = {A}°일 때, a의 값을 구하세요."
            side_lab(f, Bp, Cp, (cx, cy) if A < 90 else G, "a", c="coral")
            lines = [L("a = 2R sin A", memo="사인법칙"), L(f"a = 2 × {Rv} × {SINS[A]} = {SS(a)}")]
            ans = SS(a)
        S.add(2, q, ans, "{a/sin A} = 2R", lines, f.out(), omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        C = R.choice([60, 120, 90, 60, 120])
        a, b = R.randint(2, 9), R.randint(2, 9)
        c2 = a * a + b * b - 2 * a * b * COSV[C]
        if not c2.is_Integer:
            return
        c2 = int(c2)
        cs_ = SS(sp.sqrt(c2))
        q = f"삼각형 ABC에서 a = {a}, b = {b}, C = {C}°일 때, c의 값을 구하세요."
        lines = [L("c^{2} = a^{2} + b^{2} − 2ab cos C", memo="두 변과 끼인각"),
                 L(f"c^{{2}} = {a}^{{2}} + {b}^{{2}} − 2 × {a} × {b} × {'0' if C == 90 else '(' + COSS[C] + ')'} = {c2}"),
                 L(f"c = {cs_}", memo="c > 0")]
        f = Fig()
        Ap, Bp, Cp = fit(list(tri_SAS(a, b, C)))
        G = tri_draw(f, Ap, Bp, Cp)
        angle_mark(f, Cp, Bp, Ap, r=40, label=None if C == 90 else f"{C}°", z=24)
        side_lab(f, Bp, Cp, G, str(a))
        side_lab(f, Cp, Ap, G, str(b))
        side_lab(f, Ap, Bp, G, "c", c="coral")
        S.add(3, q, cs_, "코사인법칙 c^{2} = a^{2} + b^{2} − 2ab cos C", lines, f.out(), omr="ex", key=q)
    fill(S, 3, 20, g3)

    TRIPLES = []
    for u in range(2, 16):
        for v in range(2, 16):
            for th, cv in ((60, Fr(1, 2)), (120, Fr(-1, 2)), (90, Fr(0))):
                w2 = u * u + v * v - 2 * u * v * cv
                w = math.isqrt(int(w2))
                if w * w == w2 and not (u == v == w):
                    TRIPLES.append((u, v, w, th))

    def g4():
        u, v, w, th = R.choice(TRIPLES)
        if th == 90 and R.random() < 0.6:
            return
        T = R.choice("ABC")
        o1, o2 = [n for n in "ABC" if n != T]
        sd = {T.lower(): w, o1.lower(): u, o2.lower(): v}
        a, b, c = sd["a"], sd["b"], sd["c"]
        x1, x2 = o1.lower(), o2.lower()
        cosv = Fr(u * u + v * v - w * w, 2 * u * v)
        q = f"세 변의 길이가 a = {a}, b = {b}, c = {c}인 삼각형 ABC에서 {T}의 크기를 구하세요."
        lines = [L(f"cos {T} = {{{x1}^{{2}} + {x2}^{{2}} − {T.lower()}^{{2}}/2{x1}{x2}}}", memo=f"마주 보는 변 {T.lower()}"),
                 L(f"cos {T} = {{{u}^{{2}} + {v}^{{2}} − {w}^{{2}}/2 × {u} × {v}}} = {FR(cosv)}"),
                 L(f"{T} = {th}°", memo="0° < 각 < 180°")]
        f = Fig()
        Ap, Bp, Cp = fit(list(tri_sides(a, b, c)))
        G = tri_draw(f, Ap, Bp, Cp)
        P = {"A": Ap, "B": Bp, "C": Cp}
        V = P[T]
        angle_mark(f, V, P[o1], P[o2], r=40, label="?", z=24)
        side_lab(f, Bp, Cp, G, str(a))
        side_lab(f, Cp, Ap, G, str(b))
        side_lab(f, Ap, Bp, G, str(c))
        S.add(4, q, f"{th}°", f"세 변 → 코사인법칙으로 cos {T}", lines, f.out(), ap=str(th), key=q)
    fill(S, 4, 20, g4)

    def g5():
        C = R.choice([30, 45, 60, 90, 120, 135, 150])
        a, b = R.randint(2, 10), R.randint(2, 10)
        Sv = sp.Rational(1, 2) * a * b * SINV[C]
        q = f"삼각형 ABC에서 a = {a}, b = {b}, C = {C}°일 때, 삼각형 ABC의 넓이를 구하세요."
        lines = [L("S = {1/2}ab sin C", memo="두 변과 끼인각"),
                 L(f"S = {{1/2}} × {a} × {b} × {SINS[C]} = {SS(Sv)}")]
        f = Fig()
        Ap, Bp, Cp = fit(list(tri_SAS(a, b, C)))
        G = tri_draw(f, Ap, Bp, Cp, fill_at=1)
        angle_mark(f, Cp, Bp, Ap, r=40, label=None if C == 90 else f"{C}°", z=24)
        side_lab(f, Bp, Cp, G, str(a))
        side_lab(f, Cp, Ap, G, str(b))
        S.add(5, q, SS(Sv), "{1/2}ab sin C", lines, f.out(), omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S
