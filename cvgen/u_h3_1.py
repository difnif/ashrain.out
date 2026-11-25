# 고3 미적분Ⅱ — 수열의 극한 · 여러 가지 미분법 · 도함수의 활용 · 여러 가지 적분법
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, nl_range, hop, arcp


def chipm(f, x, y, s, at, c="teal", z=32, dl=0, un=None, fo=0.16):
    w = max(z * 1.25, tw(s, z) + z * 0.6)
    r = f.rect(x - w / 2, y - z * 0.98, w, z * 1.4, c=c, sw=3, rx=z * 0.42, f=c, fo=fo, at=at, dl=dl, un=un)
    t = f.text(x, y, s, z=z, c=c, at=at, dl=dl + 60, un=un, b=800)
    return [r, t]


def area(P, fn, a, b, at, c="gold", fo=0.4, n=40, dl=0, base=0.0):
    pts = [P.P(a, base)] + [P.P(a + (b - a) * k / n, fn(a + (b - a) * k / n)) for k in range(n + 1)] + [P.P(b, base)]
    return P.f.poly(pts, at=at, c="none", f=c, fo=fo, dl=dl)


def build(U):
    # ── 01 수열의 극한 ─────────────────────────────────────────
    f = Fig()
    P = Plane(f, (0, 13), (0, 2.5), box=(70, 80, 620, 600), square=False)
    f.line(P.X(0), P.Y(0), P.X(13), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(0), P.X(0), P.Y(2.5), at="q", c="ink", w=3, ar=1)
    for v in (1, 2):
        f.text(P.X(0) - 10, P.Y(v) + 7, str(v), z=20, c="soft", at="q", a="e")
    for n in (1, 5, 10):
        f.text(P.X(n), P.Y(0) + 26, str(n), z=18, c="soft", at="q")
    f.text(P.X(12.6), P.Y(0) + 50, "n", z=22, c="soft", at="q")
    for n in range(1, 13):
        at = 0 if n <= 6 else 1
        P.pt(n, (2 * n + 1) / (n + 3), at=at, f="teal", r=9, dl=120 * ((n - 1) % 6))
    f.line(*P.P(0, 2), *P.P(13, 2), at=2, c="gold", w=3, d=True, dr=True)
    f.text(P.X(11), P.Y(2) - 18, "2로 다가간다", z=24, c="gold", at=2, dl=500, b=800)
    U.ex("h3-1-01", "lim_{n→∞}{2n + 1/n + 3}의 값을 구해 보자.", "∞/∞ 꼴 — 분자 · 분모를 분모의 최고차항 n으로 나눈다",
         [L("분자 · 분모를 n으로 나누면 2 + {1/n}, 1 + {3/n}", memo="항들이 2에 가까워진다"),
          L("n → ∞이면 {1/n} → 0, {3/n} → 0"),
          L("lim_{n→∞}{2n + 1/n + 3} = {2/1} = 2")],
         "2", f.out(), at=("b3", 1))

    # ── 02 등비수열의 극한 ─────────────────────────────────────
    f = Fig()
    P = Plane(f, (0, 8.5), (-1.2, 3.2), box=(70, 60, 620, 640), square=False)
    P.axes(at="q", grid=None, lab_step=1, ystep=1, xn="n", yn="")
    for k, (r, col, lab) in enumerate(((0.5, "teal", "r = {1/2}"), (-0.5, "coral", "r = −{1/2}"), (1.5, "lilac", "r = {3/2}"))):
        for n in range(0, 9):
            v = r ** n
            if v <= 3.2:
                P.pt(n, v, at=k, f=col, r=9, dl=110 * n)
        if k < 2:
            f.poly([P.P(n, r ** n) for n in range(0, 9)], at=k, c=col, w=2, z=False, d=True, dl=200)
        f.text(P.X(6.6), P.Y((2.6, 1.9, 3.0)[k]) + 0, lab, z=22, c=col, at=k, dl=1100, b=800, a="s")
    U.ex("h3-1-02", "공비 r가 {1/2}, −{1/2}, {3/2}인 등비수열 {r^{n}}의 극한을 비교해 보자.", "−1 < r < 1이면 0으로 수렴, r > 1이면 발산",
         [L("r = {1/2}: 1, {1/2}, {1/4}, … → 0"),
          L("r = −{1/2}: 부호를 바꾸며 0으로", memo="진동하지만 폭이 줄어든다"),
          L("r = {3/2}: 한없이 커진다 → 발산")],
         "|r| < 1이면 0으로 수렴", f.out(), at=("b2", 2))

    # ── 03 급수 — 망원경 ───────────────────────────────────────
    f = Fig()
    X0, Wd = 80, 480
    f.rect(X0, 260, Wd, 70, at="q", c="ink", sw=3, rx=6)
    f.text(X0, 360, "0", z=24, c="soft", at="q")
    f.text(X0 + Wd, 360, "1", z=24, c="soft", at="q")
    cols = ["teal", "sky", "lilac", "gold", "coral", "leaf", "teal", "sky"]
    prev = 0
    for n in range(1, 9):
        cur = 1 - 1 / (n + 1)
        f.rect(X0 + Wd * prev, 260, Wd * (cur - prev), 70, at=1, c="ink", sw=1.5, f=cols[n - 1], fo=0.5, dl=1 + 260 * (n - 1))
        if n <= 4:
            f.text(X0 + Wd * (prev + cur) / 2, 240, "{1/" + str(n * (n + 1)) + "}", z=20, c=cols[n - 1], at=1, dl=100 + 260 * (n - 1), b=800)
        prev = cur
    f.text(CX, 450, "S_{n} = 1 − {1/n + 1}", z=32, at=1, dl=2200, b=800)
    f.line(X0 + Wd, 220, X0 + Wd, 380, at=2, c="red", w=3, d=True)
    f.text(CX, 560, "→ 1", z=40, c="gold", at=2, dl=400, b=800)
    U.ex("h3-1-03", "급수 {1/1 × 2} + {1/2 × 3} + {1/3 × 4} + ⋯의 합을 구해 보자.", "부분합 S_{n}을 구해 극한으로 — 쪼개서 지워지는 망원경",
         [L("{1/n(n + 1)} = {1/n} − {1/n + 1}", memo="부분분수로 쪼개기"),
          L("S_{n} = 1 − {1/n + 1}", memo="가운데가 모두 지워진다"),
          L("lim_{n→∞} S_{n} = 1", memo="조각을 더할수록 1에 다가간다")],
         "1", f.out(), at=("b4", 1), ident=True)

    # ── 04 등비급수 — 정사각형의 1/3 ──────────────────────────
    f = Fig()
    X0, Y0, S = 110, 130, 440
    f.rect(X0, Y0, S, S, at="q", c="ink", sw=3)
    x, y, s = X0, Y0, S
    for k in range(5):
        h = s / 2
        at = 0 if k == 0 else 1
        dl = 0 if k == 0 else 500 * (k - 1)
        f.rect(x + h, y + h, h, h, at=at, c="ink", sw=1.5, f="gold", fo=0.6, dl=dl)
        f.rect(x, y + h, h, h, at=at, c="ink", sw=1.5, f="teal", fo=0.25, dl=dl + 100)
        f.rect(x + h, y, h, h, at=at, c="ink", sw=1.5, f="sky", fo=0.25, dl=dl + 200)
        if k == 0:
            f.text(x + 1.5 * h, y + 1.5 * h + 12, "{1/4}", z=34, c="ink", at=0, dl=400, b=800)
        if k == 1:
            f.text(x + 1.5 * h, y + 1.5 * h + 10, "{1/16}", z=22, c="ink", at=1, dl=300, b=800)
        x, y, s = x, y, h
    f.text(CX, 620, "금빛 = 셋 중 하나 = {1/3}", z=30, c="gold", at=2, b=800)
    U.ex("h3-1-04", "등비급수 {1/4} + {1/16} + {1/64} + ⋯의 합을 구해 보자.", "|r| < 1이면 합 = {a/1 − r}",
         [L("첫째항 {1/4}, 공비 {1/4}", memo="정사각형을 4등분하고 또 4등분"),
          L("합 = {1/4} ÷ (1 − {1/4}) = {1/3}", memo="{a/1 − r}"),
          L("세 조각 중 하나씩 — 전체의 {1/3}", memo="금빛 · 청록 · 하늘이 같은 몫")],
         "{1/3}", f.out(), at=("b3", 1))

    # ── 05 (e^x)' = e^x ────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-2, 2.2), (-0.5, 4.2), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: math.e ** x, x0=-2, x1=1.43, at="q", c="sky", w=4.5)
    for k, x0 in enumerate((0, 1)):
        y0 = math.e ** x0
        col = ("gold", "coral")[k]
        P.pt(x0, y0, at=k + 1, f=col, r=11)
        f.line(*P.P(x0 - 0.8, y0 - 0.8 * y0), *P.P(x0 + 0.5, y0 + 0.5 * y0), at=k + 1, c=col, w=3.5, dr=True, dl=300)
        f.line(*P.P(x0, 0), *P.P(x0, y0), at=k + 1, c=col, w=2.5, d=True, dl=700)
        f.text(P.X(x0) + 14, P.Y(y0 / 2) + 8, "높이 " + ("1" if k == 0 else "e"), z=22, c=col, at=k + 1, dl=900, b=800, a="s")
        f.text(P.X(x0) - 16, P.Y(y0) - 20, "기울기 " + ("1" if k == 0 else "e"), z=22, c=col, at=k + 1, dl=1200, b=800, a="e")
    f.text(P.X(-1.9), P.Y(3.8), "y = e^{x}", z=26, c="sky", at=0, b=800, a="s")
    U.ex("h3-1-05", "y = e^{x}의 그래프에서 각 점의 접선의 기울기와 높이를 비교해 보자.", "(e^{x})' = e^{x} — 기울기가 그 점의 높이와 같다",
         [L("(e^{x})' = e^{x}", memo="미분해도 자기 자신"),
          L("x = 0: 기울기 e^{0} = 1", memo="높이 1"),
          L("x = 1: 기울기 e^{1} = e", memo="높이 e")],
         "기울기 = 높이", f.out(), at=("b3", 1))

    # ── 06 lim sin x / x ──────────────────────────────────────
    f = Fig()
    O, Rr = (110, 560), 460
    f.poly([(O[0] + Rr * math.cos(math.radians(a)), O[1] - Rr * math.sin(math.radians(a))) for a in range(0, 91, 3)], at="q", c="soft", w=3, z=False)
    f.line(O[0], O[1], O[0] + Rr + 40, O[1], at="q", c="ink", w=3, ar=1)
    f.line(O[0], O[1], O[0], O[1] - Rr - 30, at="q", c="ink", w=3, ar=1)
    f.text(O[0] + Rr, O[1] + 34, "1", z=24, at="q", b=800)
    for k, deg in enumerate((60, 15)):
        Pp = (O[0] + Rr * math.cos(math.radians(deg)), O[1] - Rr * math.sin(math.radians(deg)))
        un = 1 if k == 0 else None
        f.line(*O, *Pp, at=k, c="ink", w=3.5, un=un)
        arcp(f, *O, Rr, 0, deg, at=k, c="gold", sw=7, dl=300, un=un)
        f.line(Pp[0], O[1], *Pp, at=k, c="coral", w=7, dr=True, dl=800, un=un)
        f.text(Pp[0] + 18, Pp[1] - 14, "호 x", z=24, c="gold", at=k, dl=600, b=800, a="s", un=un)
        f.text(Pp[0] - 14, (O[1] + Pp[1]) / 2 + 8, "sin x", z=24, c="coral", at=k, dl=1100, b=800, a="e", un=un)
        f.text(500, 120 + 0, ("{sin x/x} ≈ 0.83" if k == 0 else "{sin x/x} ≈ 0.99"), z=28, c="ink", at=k, dl=1400, b=800, un=un)
    f.text(500, 200, "→ 1", z=36, c="gold", at=2, b=800)
    U.ex("h3-1-06", "단위원에서 x가 0에 가까워질 때 {sin x/x}가 어떻게 되는지 알아보자.", "반지름 1인 원에서 호의 길이는 x, 세로 높이는 sin x — 각이 작아지면 둘이 같아진다",
         [L("x = {π/3}: {sin x/x} ≈ 0.83", memo="호가 높이보다 꽤 길다"),
          L("x = {π/12}: {sin x/x} ≈ 0.99", memo="거의 같다"),
          L("lim_{x→0}{sin x/x} = 1", memo="x는 라디안")],
         "1", f.out(), at=("b2", 2))

    # ── 07 몫의 미분 ───────────────────────────────────────────
    f = Fig()
    S = Strip(f, y=110, z=34)
    S.row("q", ["y =", {"s": "{x/x^{2} + 1}"}], keep=True)
    for k, (s, x, col) in enumerate((("f = x", 130, "teal"), ("f' = 1", 130, "teal"), ("g = x^{2} + 1", 500, "coral"), ("g' = 2x", 500, "coral"))):
        f.text(x, 200 + 50 * (k % 2), s, z=24, c=col, at=0, dl=300 * k, b=800)
    f.text(CX, 330, "{f'g − fg'/g^{2}}", z=34, c="soft", at=1, b=800)
    f.text(CX, 440, "{1 − x^{2}/(x^{2} + 1)^{2}}", z=36, c="gold", at=2, b=800)
    P = Plane(f, (-3, 3), (-0.7, 0.7), box=(80, 500, 600, 660), square=False)
    f.line(P.X(-3), P.Y(0), P.X(3), P.Y(0), at=2, c="ink", w=2.5)
    P.curve(lambda x: x / (x * x + 1), at=2, c="sky", w=3.5)
    for xv in (-1, 1):
        f.line(*P.P(xv - 0.5, xv / 2), *P.P(xv + 0.5, xv / 2), at=2, c="gold", w=3, dl=800)
    U.ex("h3-1-07", "y = {x/x^{2} + 1}을 미분해 보자.", "몫의 미분 — {f/g}' = {f'g − fg'/g^{2}}",
         [L("f = x, g = x^{2} + 1 → f' = 1, g' = 2x"),
          L("{1 × (x^{2} + 1) − x × 2x/(x^{2} + 1)^{2}}", memo="앞 미분 × 뒤 − 앞 × 뒤 미분"),
          L("{1 × (x^{2} + 1) − x × 2x/(x^{2} + 1)^{2}} = {1 − x^{2}/(x^{2} + 1)^{2}}", memo="x = ±1에서 기울기 0")],
         "y' = {1 − x^{2}/(x^{2} + 1)^{2}}", f.out(), at=("b3", 1), ident=True)

    # ── 08 합성함수의 미분 — 겉과 속 ───────────────────────────
    f = Fig()
    f.text(CX, 140, "(2x + 1)^{3}", z=56, at="q", b=800)
    f.rect(CX - 130, 82, 200, 78, at="q", c="teal", sw=3, rx=14, d=True)
    f.text(CX - 30, 210, "속 u", z=24, c="teal", at="q", b=800)
    f.text(CX + 140, 90, "겉 ( )^{3}", z=24, c="coral", at="q", b=800, a="s")
    e = f.text(250, 340, "3(2x + 1)^{2}", z=46, c="coral", at=0, b=800)
    fly(e, CX - 250, 140 - 340, dl=60, ms=800)
    f.text(250, 410, "겉을 미분 · 속은 그대로", z=22, c="coral", at=0, dl=900, b=800)
    e2 = f.text(470, 340, "× 2", z=46, c="teal", at=1, b=800)
    fly(e2, (CX - 30) - 470, 140 - 340, dl=60, ms=800)
    f.text(470, 410, "속의 미분", z=22, c="teal", at=1, dl=900, b=800)
    f.text(CX, 560, "6(2x + 1)^{2}", z=50, c="gold", at=2, b=800)
    U.ex("h3-1-08", "y = (2x + 1)^{3}을 미분해 보자.", "겉을 미분하고 속은 그대로 둔 뒤, 속의 미분을 곱한다",
         [L("겉: u^{3} → 3u^{2}, 속: u = 2x + 1", memo="u' = 2"),
          L("3(2x + 1)^{2} × 2", memo="겉 미분 × 속 미분"),
          L("3(2x + 1)^{2} × 2 = 6(2x + 1)^{2}")],
         "6(2x + 1)^{2}", f.out(), at=("b2", 2), ident=True)

    # ── 09 매개변수 미분 ───────────────────────────────────────
    f = Fig()
    P = Plane(f, (-0.3, 2.6), (-0.4, 3.5), box=(70, 60, 620, 650))
    P.axes(at="q", grid=None, lab_step=1, ystep=1)
    P.curve(lambda x: x ** 1.5 if x >= 0 else None, x0=0, x1=2.3, at="q", c="sky", w=4)
    for k, t in enumerate((0, 0.5, 1, 1.5)):
        P.pt(t * t, t ** 3, at=0, f="teal", r=9, label=f"t = {t:g}", pos="w" if t > 0 else "se", z=20, c="teal", dl=300 * k)
    P.lineq(1.5, -0.5, at=2, c="gold", w=4)
    P.pt(1, 1, at=2, f="gold", r=12, label="기울기 {3/2}", pos="e", z=22, c="gold", dl=400)
    U.ex("h3-1-09", "x = t^{2}, y = t^{3}으로 나타낸 곡선에서 t = 1인 점의 접선의 기울기를 구해 보자.", "{dy/dx} = (y를 t로 미분) ÷ (x를 t로 미분)",
         [L("x를 t로 미분: 2t, y를 t로 미분: 3t^{2}", memo="점이 t에 따라 움직인다"),
          L("{3t^{2}/2t} = {3t/2}", memo="(y쪽) ÷ (x쪽)"),
          L("t에 1을 넣으면 기울기 {3/2}, 점 (1, 1)")],
         "{3/2}", f.out(), at=("b3", 1), ident=True)

    # ── 10 음함수의 미분 ───────────────────────────────────────
    f = Fig()
    P = Plane(f, (-1.4, 1.6), (-1.3, 1.5), box=(60, 50, 620, 650))
    P.axes(at="q", grid=None, lab_step=1, ystep=1)
    f.circ(*P.P(0, 0), P.sx, at="q", c="sky", sw=4)
    Q = (0.6, 0.8)
    P.pt(*Q, at=1, f="ink", r=11, label="({3/5}, {4/5})", pos="ne", z=22)
    f.line(*P.P(0, 0), *P.P(*Q), at=1, c="teal", w=3.5, dr=True, dl=300)
    f.text(P.X(0.2), P.Y(0.45), "기울기 {4/3}", z=20, c="teal", at=1, dl=700, b=800, a="e")
    f.line(*P.P(Q[0] - 0.8, Q[1] + 0.6), *P.P(Q[0] + 0.8, Q[1] - 0.6), at=2, c="coral", w=4, dr=True)
    angle_mark(f, P.P(*Q), P.P(0, 0), P.P(Q[0] + 0.8, Q[1] - 0.6), r=20, at=2, c="ink", dl=800)
    f.text(P.X(1.25), P.Y(0.1), "−{3/4}", z=28, c="coral", at=2, dl=900, b=800)
    U.ex("h3-1-10", "원 x^{2} + y^{2} = 1 위의 점 ({3/5}, {4/5})에서의 접선의 기울기를 구해 보자.", "양변을 x로 미분 — y는 x의 함수라 y^{2}의 미분은 2y × y'",
         [L("2x + 2y × y' = 0", memo="y^{2} → 2yy'"),
          L("y' = −{x/y}"),
          L("점 ({3/5}, {4/5}): y' = −{3/4}", memo="반지름의 기울기 {4/3}과 수직")],
         "−{3/4}", f.out(), at=("b2", 2))

    # ── 11 접선 — y = e^x 의 (0, 1) ────────────────────────────
    f = Fig()
    P = Plane(f, (-3, 2), (-1, 5), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: math.e ** x, x0=-3, x1=1.6, at="q", c="sky", w=4.5)
    P.pt(0, 1, at="q", f="ink", r=10, label="(0, 1)", pos="w", z=22)
    tl = P.lineq(1, 3, at=1, c="coral", w=4, dr=False)
    slide(tl, 1, dy=P.Y(1) - P.Y(3), dl=300)
    f.text(P.X(1.4), P.Y(2.0), "y = x + 1", z=24, c="coral", at=2, b=800, a="s")
    f.text(P.X(-2.9), P.Y(4.4), "곡선이 늘 접선 위", z=22, c="sky", at=2, dl=400, b=800, a="s")
    U.ex("h3-1-11", "곡선 y = e^{x} 위의 점 (0, 1)에서의 접선의 방정식을 구해 보자.", "접점과 그 점의 미분계수 — 기울기는 (e^{x})' = e^{x}",
         [L("y' = e^{x} → 기울기 e^{0} = 1"),
          L("y − 1 = 1 × (x − 0)", memo="기울기 1인 직선을 내려 (0, 1)에 닿게"),
          L("y = x + 1")],
         "y = x + 1", f.out(), at=("b3", 1))

    # ── 12 변곡점 ──────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-2.3, 2.3), (-3, 3), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x ** 3 - 3 * x, x0=-2.2, x1=2.2, at="q", c="soft", w=3.5)
    P.curve(lambda x: x ** 3 - 3 * x, x0=-2.2, x1=0, at=1, c="coral", w=6)
    P.curve(lambda x: x ** 3 - 3 * x, x0=0, x1=2.2, at=1, c="teal", w=6, )
    f.text(P.X(-1.6), P.Y(2.6), "∩ 위로 볼록", z=22, c="coral", at=1, dl=500, b=800)
    f.text(P.X(1.6), P.Y(-2.6), "∪ 아래로 볼록", z=22, c="teal", at=1, dl=700, b=800)
    P.pt(0, 0, at=2, f="gold", r=13, label="변곡점 (0, 0)", pos="e", z=22, c="gold")
    P.lineq(-3, 0, at=2, c="gold", w=2.5, d=True)
    U.ex("h3-1-12", "y = x^{3} − 3x의 오목 · 볼록과 변곡점을 구해 보자.", "y''의 부호 — 음수면 위로 볼록, 양수면 아래로 볼록, 바뀌는 곳이 변곡점",
         [L("y'' = 6x", memo="두 번 미분"),
          L("x < 0: y'' < 0 (∩), x > 0: y'' > 0 (∪)"),
          L("변곡점 (0, 0)", memo="접선이 곡선을 가로지른다")],
         "변곡점 (0, 0)", f.out(), at=("b4", 1))

    # ── 13 sin 의 정적분 ───────────────────────────────────────
    f = Fig()
    P = Plane(f, (-0.2, math.pi + 0.4), (-0.3, 1.4), box=(70, 120, 620, 600), square=False)
    f.line(P.X(-0.2), P.Y(0), P.X(math.pi + 0.4), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(-0.3), P.X(0), P.Y(1.4), at="q", c="ink", w=3, ar=1)
    for k, s in ((1, "{π/2}"), (2, "π")):
        f.text(P.X(k * math.pi / 2), P.Y(0) + 40, s, z=22, c="soft", at="q")
    f.text(P.X(0) - 10, P.Y(1) + 7, "1", z=20, c="soft", at="q", a="e")
    P.curve(math.sin, x0=0, x1=math.pi, at="q", c="sky", w=4.5)
    area(P, math.sin, 0, math.pi, 1, c="gold", fo=0.4)
    f.text(P.X(math.pi / 2), P.Y(0.4), "2", z=50, c="ink", at=2, b=800)
    U.ex("h3-1-13", "∫_{0}^{π}sin x dx의 값을 구해 보자.", "∫sin x dx = −cos x + C — 위끝 − 아래끝",
         [L("∫sin x dx = −cos x + C", memo="(−cos x)' = sin x"),
          L("[−cos x]_{0}^{π} = (−cos π) − (−cos 0)", memo="사인 곡선 한 봉우리 아래"),
          L("(−cos π) − (−cos 0) = 1 + 1 = 2")],
         "2", f.out(), at=("b4", 1))

    # ── 14 치환적분 — 넓이가 같은 두 그림 ───────────────────────
    f = Fig()
    Pa = Plane(f, (-0.1, 1.3), (-0.3, 5.8), box=(60, 60, 310, 600), square=False)
    Pb = Plane(f, (-0.1, 1.3), (-0.3, 5.8), box=(370, 60, 620, 600), square=False)
    for Pp, lab, xn in ((Pa, "y = 2xe^{x^{2}}", "x"), (Pb, "y = e^{t}", "t")):
        f.line(Pp.X(-0.1), Pp.Y(0), Pp.X(1.3), Pp.Y(0), at="q", c="ink", w=2.5, ar=1)
        f.line(Pp.X(0), Pp.Y(-0.3), Pp.X(0), Pp.Y(5.8), at="q", c="ink", w=2.5, ar=1)
        f.text(Pp.X(1), Pp.Y(0) + 28, "1", z=20, c="soft", at="q")
        f.text(Pp.X(1.25), Pp.Y(0) + 28, xn, z=20, c="soft", at="q")
        f.text(Pp.X(0.55), Pp.Y(5.7), lab, z=20, at="q", b=800)
    Pa.curve(lambda x: 2 * x * math.e ** (x * x), x0=0, x1=1.05, at="q", c="coral", w=4)
    Pb.curve(lambda t: math.e ** t, x0=0, x1=1.2, at=0, c="teal", w=4)
    f.text(340, 330, "t = x^{2}", z=22, c="gold", at=0, dl=300, b=800)
    area(Pa, lambda x: 2 * x * math.e ** (x * x), 0, 1, 1, c="coral", fo=0.35)
    area(Pb, lambda t: math.e ** t, 0, 1, 1, c="teal", fo=0.35, dl=400)
    f.text(CX, 650, "두 넓이가 같다: e − 1", z=28, c="gold", at=2, b=800)
    U.ex("h3-1-14", "∫_{0}^{1}2xe^{x^{2}}dx의 값을 구해 보자.", "속 x^{2}을 t로 — 속의 미분 2x가 곱해져 있으면 치환",
         [L("t = x^{2} → dt = 2x dx", memo="2x dx가 dt로"),
          L("x: 0 → 1이면 t: 0 → 1", memo="구간도 t로 갈아탄다"),
          L("∫_{0}^{1}e^{t}dt = [e^{t}]_{0}^{1} = e − 1")],
         "e − 1", f.out(), at=("b4", 1))

    # ── 15 부분적분 — 미분 · 적분 표 ───────────────────────────
    f = Fig()
    f.text(200, 110, "미분", z=28, c="teal", at="q", b=800)
    f.text(460, 110, "적분", z=28, c="coral", at="q", b=800)
    rows = [("x", "e^{x}"), ("1", "e^{x}"), ("0", "e^{x}")]
    for k, (a, b) in enumerate(rows):
        at = 0 if k < 2 else 1
        f.text(200, 190 + 90 * k, a, z=36, c="teal", at=at, dl=300 * k, b=800)
        f.text(460, 190 + 90 * k, b, z=36, c="coral", at=at, dl=300 * k + 150, b=800)
    f.line(225, 182, 425, 262, at=1, c="gold", w=3.5, ar=1, dr=True, dl=200)
    f.text(325, 205, "+", z=30, c="gold", at=1, dl=500, b=800)
    f.line(225, 272, 425, 352, at=1, c="red", w=3.5, ar=1, dr=True, dl=900)
    f.text(325, 295, "−", z=30, c="red", at=1, dl=1200, b=800)
    f.text(CX, 520, "x e^{x} − e^{x} + C", z=40, c="gold", at=2, b=800)
    U.ex("h3-1-15", "∫x e^{x}dx를 구해 보자.", "∫fg' = fg − ∫f'g — 미분하면 간단해지는 쪽을 f로",
         [L("f = x, g' = e^{x}", memo="x는 미분하면 1 — 간단해진다"),
          L("x e^{x} − ∫1 × e^{x}dx", memo="대각선으로 곱하고 부호 + , −"),
          L("x e^{x} − e^{x} + C")],
         "x e^{x} − e^{x} + C", f.out(), at=("b4", 1))

    # ── 16 정적분과 급수 — 직사각형을 잘게 ──────────────────────
    f = Fig()
    P = Plane(f, (-0.05, 1.15), (-0.05, 1.15), box=(70, 60, 620, 610))
    f.line(P.X(-0.05), P.Y(0), P.X(1.15), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(-0.05), P.X(0), P.Y(1.15), at="q", c="ink", w=3, ar=1)
    f.text(P.X(1), P.Y(0) + 28, "1", z=20, c="soft", at="q")
    f.text(P.X(0) - 10, P.Y(1) + 7, "1", z=20, c="soft", at="q", a="e")
    for k, (n, col) in enumerate(((4, "teal"), (8, "coral"), (32, "gold"))):
        for i in range(1, n + 1):
            x0 = (i - 1) / n
            h = (i / n) ** 2
            f.rect(P.X(x0), P.Y(h), P.X(1 / n) - P.X(0), P.Y(0) - P.Y(h), at=k, c="ink" if n < 32 else "none", sw=1.2, f=col, fo=0.4, dl=1 + (600 // n) * i, un=k + 1 if k < 2 else None)
    P.curve(lambda x: x * x, x0=0, x1=1.07, at="q", c="sky", w=4.5)
    for k, s in enumerate(("n = 4: 0.47", "n = 8: 0.40", "n → ∞: {1/3}")):
        f.text(P.X(0.05), P.Y(1.05) + 0, s, z=24, c=("teal", "coral", "gold")[k], at=k, dl=700, b=800, a="s", un=k + 1 if k < 2 else None)
    U.ex("h3-1-16", "lim_{n→∞}∑_{k=1}^{n}{1/n}({k/n})^{2}을 정적분으로 나타내어 계산해 보자.", "{1/n} → dx, {k/n} → x — 폭 {1/n}인 직사각형의 합이 넓이로",
         [L("n = 4: 합 = {30/64}", memo="직사각형 4개"),
          L("n = 8: 합 = {204/512}", memo="잘게 나눌수록 곡선 아래 넓이에"),
          L("∫_{0}^{1}x^{2}dx = {1/3}", memo="n → ∞")],
         "{1/3}", f.out(), at=("b3", 1))

    # ── 17 1/x 아래 넓이 = ln ──────────────────────────────────
    f = Fig()
    P = Plane(f, (-0.2, 3.6), (-0.2, 3), box=(60, 80, 620, 600), square=False)
    f.line(P.X(-0.2), P.Y(0), P.X(3.6), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(-0.2), P.X(0), P.Y(3), at="q", c="ink", w=3, ar=1)
    for v, s in ((1, "1"), (math.e, "e")):
        f.text(P.X(v), P.Y(0) + 30, s, z=22, c="soft", at="q")
    P.curve(lambda x: 1 / x, x0=0.34, x1=3.5, at="q", c="sky", w=4.5)
    f.text(P.X(0.5), P.Y(2.6), "y = {1/x}", z=24, c="sky", at="q", b=800, a="s")
    area(P, lambda x: 1 / x, 1, math.e, 0, c="gold", fo=0.45)
    f.text(P.X(1.8), P.Y(0.3), "1", z=44, c="ink", at=1, b=800)
    f.text(P.X(2.4), P.Y(2.0), "ln e − ln 1", z=26, c="gold", at=1, dl=400, b=800)
    U.ex("h3-1-17", "곡선 y = {1/x}와 x축, 두 직선 x = 1, x = e로 둘러싸인 부분의 넓이를 구해 보자.", "∫{1/x}dx = ln|x| + C — 1/x 아래 넓이가 곧 자연로그",
         [L("∫_{1}^{e}{1/x}dx = [ln x]_{1}^{e}"),
          L("ln e − ln 1 = 1 − 0 = 1"),
          L("1에서 e까지 넓이가 정확히 1", memo="자연로그의 기하적 뜻")],
         "1", f.out(), at=("b4", 1))

    # ── 18 속도와 거리 ─────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-0.3, 4.6), (-3, 7), box=(70, 50, 620, 420), square=False)
    P.axes(at="q", grid=None, lab_step=1, ystep=2, xn="t", yn="v")
    P.lineq(-2, 6, at="q", c="sky", w=4)
    f.poly([P.P(0, 0), P.P(0, 6), P.P(3, 0)], at=0, c="none", f="teal", fo=0.4)
    f.text(P.X(1), P.Y(2), "9", z=34, c="teal", at=0, dl=400, b=800)
    f.poly([P.P(3, 0), P.P(4, -2), P.P(4, 0)], at=1, c="none", f="coral", fo=0.45)
    f.text(P.X(3.75), P.Y(-0.9) + 8, "1", z=28, c="coral", at=1, dl=400, b=800, a="s")
    nl = NL(f, 0, 10, y=560, x0=70, x1=600, step=1, lab_step=1, z=20)
    d = f.dot(nl.X(0), 560, r=13, f="teal", at=0)
    slide(d, 0, dx=nl.X(9) - nl.X(0), dl=600)
    d2 = f.dot(nl.X(9), 560, r=13, f="coral", at=1)
    slide(d2, 1, dx=nl.X(8) - nl.X(9), dl=600)
    f.text(nl.X(8), 640, "변화량 8 · 거리 10", z=26, c="gold", at=2, b=800)
    U.ex("h3-1-18", "속도가 v(t) = 6 − 2t인 점이 t = 0부터 t = 4까지 움직였다. 위치의 변화량과 움직인 거리를 구해 보자.", "변화량은 ∫v dt (부호 그대로), 거리는 ∫|v|dt (방향을 바꾼 t = 3에서 나눠서)",
         [L("∫_{0}^{3}(6 − 2t)dt = 9", memo="앞으로 9"),
          L("∫_{3}^{4}(6 − 2t)dt = −1", memo="뒤로 1"),
          L("변화량 9 − 1 = 8, 거리 9 + 1 = 10")],
         "변화량 8, 거리 10", f.out(), at=("b4", 1))
