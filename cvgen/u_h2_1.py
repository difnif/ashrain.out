# 고2 대수 — 지수와 로그 · 지수함수와 로그함수 · 삼각함수 · 수열
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, nl_range, hop, arcp


def chipm(f, x, y, s, at, c="teal", z=32, dl=0, un=None, fo=0.16):
    w = max(z * 1.25, tw(s, z) + z * 0.6)
    r = f.rect(x - w / 2, y - z * 0.98, w, z * 1.4, c=c, sw=3, rx=z * 0.42, f=c, fo=fo, at=at, dl=dl, un=un)
    t = f.text(x, y, s, z=z, c=c, at=at, dl=dl + 60, un=un, b=800)
    return [r, t]


def arch(f, x0, x1, y, at, h=40, c="gold", dl=0, w=3, up=True):
    s = -1 if up else 1
    pts = [(x0 + (x1 - x0) * k / 16, y + s * h * 4 * (k / 16) * (1 - k / 16)) for k in range(17)]
    return f.poly(pts, at=at, c=c, w=w, z=False, dr=True, ar=1, dl=dl)


def build(U):
    # ── 01 지수의 확장 — ÷2 계단 ───────────────────────────────
    f = Fig()
    ns = [3, 2, 1, 0, -1, -2, -3]
    base, u = 520, 40
    for k, n in enumerate(ns):
        x = 70 + 80 * k
        h = u * 2 ** n
        at = "q" if n >= 1 else (1 if n == 0 else 2)
        dl = 0 if n >= 1 else (0 if n == 0 else 500 * (-n - 1))
        f.rect(x - 26, base - h, 52, h, at=at, c="ink", sw=2.5, f="teal" if n > 0 else ("gold" if n == 0 else "coral"), fo=0.4, dl=dl)
        lab = str(2 ** n) if n >= 0 else "{1/" + str(2 ** -n) + "}"
        f.text(x, base - h - 16 if n >= -1 else base - 40, lab, z=24, at=at, dl=dl + 200, b=800)
        f.text(x, base + 40, f"2^{{{n}}}" if n >= 0 else f"2^{{−{-n}}}", z=24, c="soft", at=at, dl=dl, b=800)
        if k:
            arch(f, x - 80 + 18, x - 18, base - u * 2 ** (n + 1) - 50 if n >= 0 else base - 90, at, h=22, c="sky", dl=dl)
            f.text(x - 40, (base - u * 2 ** (n + 1) - 86) if n >= 0 else base - 126, "÷ 2", z=18, c="sky", at=at, dl=dl + 300, b=800)
    U.ex("h2-1-01", "2^{3}, 2^{2}, 2^{1}, …의 규칙을 이어 2^{0}과 2^{−3}의 값을 구해 보자.", "지수가 1 줄 때마다 2로 나눈다 — 지수법칙이 깨지지 않도록",
         [L("2^{3} = 8, 2^{2} = 4, 2^{1} = 2", memo="한 칸 내려갈 때마다 ÷ 2"),
          L("2^{0} = 2 ÷ 2 = 1"),
          L("2^{−1} = 1 ÷ 2 = {1/2}, 2^{−3} = {1/8}", memo="a^{−n} = {1/a^{n}}")],
         "2^{0} = 1, 2^{−3} = {1/8}", f.out(), at=("b2", 2))

    # ── 02 로그 — 곱하기 횟수 ───────────────────────────────────
    f = Fig()
    xs = [80 + 100 * k for k in range(6)]
    for k in range(6):
        f.text(xs[k], 220, str(2 ** k), z=36 if k < 5 else 34, at="q" if k <= 3 else 2, b=800)
        f.text(xs[k], 270, f"2^{{{k}}}", z=20, c="soft", at="q" if k <= 3 else 2, b=700)
    for k in range(3):
        arch(f, xs[k] + 16, xs[k + 1] - 16, 180, 0, h=36, c="teal", dl=500 * k)
        f.text((xs[k] + xs[k + 1]) / 2, 120, "× 2", z=20, c="teal", at=0, dl=500 * k + 300, b=800)
    f.text(xs[1] + 50, 330, "3번 → log_{2} 8 = 3", z=28, c="teal", at=1, b=800)
    nl_y = 520
    f.line(60, nl_y, 600, nl_y, at=2, c="ink", w=3, ar=1)
    for k in range(6):
        f.line(xs[k], nl_y - 10, xs[k], nl_y + 10, at=2, c="ink", w=2.5)
        f.text(xs[k], nl_y + 40, str(2 ** k), z=22, at=2, b=700)
    for (a_, b_, col, dl) in ((0, 2, "coral", 300), (2, 5, "gold", 900)):
        arch(f, xs[a_], xs[b_], nl_y - 8, 2, h=60 + 10 * (b_ - a_), c=col, dl=dl)
        f.text((xs[a_] + xs[b_]) / 2, nl_y - 90 - 10 * (b_ - a_), f"+{b_ - a_}", z=24, c=col, at=2, dl=dl + 400, b=800)
    f.text(CX, 640, "4 × 8 = 32 ↔ 2 + 3 = 5", z=26, c="gold", at=2, dl=1600, b=800)
    U.ex("h2-1-02", "log_{2} 8과 log_{2} 32를 구하고, log_{2} 32 = log_{2} 4 + log_{2} 8임을 확인해 보자.", "log_{2} N = 2를 몇 번 곱해야 N이 되는가",
         [L("2^{x} = 8 ⇔ x = log_{2} 8", memo="밑 2, 진수 8"),
          L("2를 3번 곱하면 8 → log_{2} 8 = 3"),
          L("log_{2} 32 = log_{2} 4 + log_{2} 8 = 2 + 3 = 5", memo="곱은 횟수의 합")],
         "3, 5", f.out(), at=("b3", 1))

    # ── 03 상용로그 — 자릿수 ───────────────────────────────────
    f = Fig()
    X = lambda v: 80 + 120 * v
    f.line(60, 400, 620, 400, at="q", c="ink", w=3, ar=1)
    for v in range(5):
        f.line(X(v), 388, X(v), 412, at="q", c="ink", w=2.5)
        f.text(X(v), 370, str(v), z=24, c="teal", at="q", b=800)
        f.text(X(v), 450, str(10 ** v), z=22, at="q", b=700)
    f.text(40, 370, "log", z=22, c="teal", at="q", b=800, a="e")
    f.text(40, 450, "N", z=22, at="q", b=800, a="e")
    d = f.dot(X(0), 400, r=12, f="coral", at=1)
    slide(d, 1, dx=X(3.01) - X(0), dl=200)
    f.text(X(3.01) + 10, 330, "3.010", z=26, c="coral", at=1, dl=1200, b=800)
    f.text(X(3.01) + 10, 520, "2^{10} = 1024", z=24, c="coral", at=2, b=800)
    f.rect(X(3) - 4, 470, X(4) - X(3) + 8, 80, at=2, c="gold", sw=3, rx=10, d=True, dl=400)
    f.text(CX, 620, "1000 ≤ 2^{10} < 10000 → 4자리", z=28, c="gold", at=2, dl=800, b=800)
    U.ex("h2-1-03", "log 2 = 0.3010일 때 2^{10}은 몇 자리 수인지 구해 보자.", "log N의 정수 부분이 n이면 N은 (n + 1)자리 수",
         [L("log 2^{10} = 10 × log 2", memo="지수가 앞으로"),
          L("10 × 0.3010 = 3.010"),
          L("3 ≤ 3.010 < 4 → 1000 ≤ 2^{10} < 10000", memo="정수 부분 3 → 4자리")],
         "4자리 수", f.out(), at=("b4", 1))

    # ── 04 지수함수의 평행이동 ──────────────────────────────────
    f = Fig()
    P = Plane(f, (-3, 4), (-1, 7), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: 2 ** x, x0=-3, x1=2.7, at="q", c="soft", w=3.5)
    P.pt(0, 1, at="q", f="soft", r=9)
    cv = P.curve(lambda x: 2 ** x, x0=-3, x1=2.3, at=1, c="sky", w=4.5, dr=False)
    slides(cv, 1, dx=P.X(1) - P.X(0), dy=P.Y(2) - P.Y(0), dl=300)
    h = f.line(*P.P(-3, 0), *P.P(4, 0), at=1, c="coral", w=3, d=True)
    slide(h, 1, dy=P.Y(2) - P.Y(0), dl=300)
    f.line(*P.P(0, 1), *P.P(1, 3), at=1, c="gold", w=3, ar=1, dr=True, dl=300)
    P.pt(1, 3, at=2, f="gold", r=11, label="(1, 3)", pos="w", z=22, c="gold")
    f.text(P.X(3.4), P.Y(2) - 12, "y = 2", z=22, c="coral", at=2, dl=300, b=800)
    U.ex("h2-1-04", "y = 2^{x}의 그래프를 이용해 y = 2^{x − 1} + 2의 그래프를 그려 보자.", "x축으로 1, y축으로 2만큼 — 점근선도 함께 y = 2로",
         [L("y = 2^{x}: 점 (0, 1), 점근선 y = 0"),
          L("x축으로 1, y축으로 2만큼 → y = 2^{x − 1} + 2"),
          L("점 (1, 3), 점근선 y = 2", memo="치역 y > 2")],
         "점근선 y = 2, 점 (1, 3)", f.out(), at=("b3", 1))

    # ── 05 로그함수의 평행이동 ──────────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 7), (-3, 4), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    lg = lambda x: math.log2(x) if x > 0 else None
    P.curve(lg, x0=0.13, x1=7, n=120, at="q", c="soft", w=3.5)
    P.pt(1, 0, at="q", f="soft", r=9)
    cv = P.curve(lg, x0=0.13, x1=4.9, n=120, at=1, c="sky", w=4.5, dr=False)
    slides(cv, 1, dx=P.X(2) - P.X(0), dy=P.Y(1) - P.Y(0), dl=300)
    v = f.line(*P.P(0, -3), *P.P(0, 4), at=1, c="coral", w=3, d=True)
    slide(v, 1, dx=P.X(2) - P.X(0), dl=300)
    f.line(*P.P(1, 0), *P.P(3, 1), at=1, c="gold", w=3, ar=1, dr=True, dl=300)
    P.pt(3, 1, at=2, f="gold", r=11, label="(3, 1)", pos="se", z=22, c="gold")
    f.text(P.X(2) + 12, P.Y(-2.6), "x = 2", z=22, c="coral", at=2, dl=300, b=800, a="s")
    U.ex("h2-1-05", "y = log_{2} x의 그래프를 이용해 y = log_{2}(x − 2) + 1의 그래프를 그려 보자.", "x축으로 2, y축으로 1만큼 — 점근선 x = 0이 x = 2로",
         [L("y = log_{2} x: 점 (1, 0), 점근선 x = 0"),
          L("x축으로 2, y축으로 1만큼 이동"),
          L("점근선 x = 2, 점 (3, 1)", memo="정의역 x > 2")],
         "점근선 x = 2, 점 (3, 1)", f.out(), at=("b3", 1))

    # ── 06 지수방정식 — 치환 ───────────────────────────────────
    f = Fig()
    S = Strip(f, y=100, z=34)
    S.row("q", ["4^{x} − 3 × 2^{x} + 2 = 0"], keep=True)
    S.row(0, [{"s": "t^{2} − 3t + 2 = 0", "c": "teal"}], y=175, keep=True)
    f.text(560, 140, "2^{x} = t > 0", z=22, c="teal", at=0, dl=200, b=800)
    S.row(1, [{"s": "t = 1", "c": "coral"}, {"s": "또는", "c": "soft"}, {"s": "t = 2", "c": "gold"}], y=250, keep=True)
    P = Plane(f, (-2, 3), (-0.5, 4), box=(80, 300, 600, 660), square=False)
    P.axes(at=1, grid=None, lab_step=1)
    P.curve(lambda x: 2 ** x, x0=-2, x1=2, at=1, c="sky", w=4)
    for k, (t, col) in enumerate(((1, "coral"), (2, "gold"))):
        h = f.line(*P.P(-2, 0), *P.P(3, 0), at=2, c=col, w=3, d=True, dl=600 * k)
        slide(h, 2, dy=P.Y(t) - P.Y(0), dl=200 + 600 * k)
        x = math.log2(t)
        f.line(*P.P(x, t), *P.P(x, 0), at=2, c=col, w=3, ar=1, dr=True, dl=1200 + 600 * k)
        P.pt(x, 0, at=2, f=col, r=11, label=f"x = {int(x)}", pos="se", z=22, c=col, dl=1600 + 600 * k)
    U.ex("h2-1-06", "지수방정식 4^{x} − 3 × 2^{x} + 2 = 0을 풀어 보자.", "2^{x} = t(t > 0)로 치환하면 이차방정식",
         [L("2^{x} = t → t^{2} − 3t + 2 = 0", memo="4^{x} = (2^{x})^{2}"),
          L("(t − 1)(t − 2) = 0 → t = 1 또는 t = 2", memo="둘 다 t > 0"),
          L("2^{x} = 1 → x = 0, 2^{x} = 2 → x = 1", memo="t를 x로 되돌리기")],
         "x = 0 또는 x = 1", f.out(), at=("b2", 2))

    # ── 07 로그방정식 — 진수 조건 ───────────────────────────────
    f = Fig()
    nl = NL(f, -4, 6, y=470, x0=60, x1=600, step=1, lab_step=1, z=22)
    nl_range(nl, 2, None, at=0, closed_a=False, right=True, c="teal", up=60)
    f.text(nl.X(4.2), 380, "x > 2", z=26, c="teal", at=0, dl=500, b=800)
    f.text(CX, 160, "x(x − 2) = 8", z=34, at=1, b=800)
    f.text(CX, 240, "x = 4 또는 x = −2", z=32, c="ink", at=2, b=800)
    for k, (v, col) in enumerate(((4, "gold"), (-2, "coral"))):
        d = f.dot(nl.X(v), 470, r=13, f=col, at=2, dl=500 + 300 * k)
        fly(d, CX - nl.X(v), 240 - 470, dl=40, ms=800)
    f.cross(nl.X(-2), 470, s=40, at=3, c="red")
    f.text(nl.X(-2), 560, "진수 조건 ×", z=22, c="red", at=3, dl=300, b=800)
    f.circ(nl.X(4), 470, 24, at=3, c="gold", sw=4, dl=500)
    U.ex("h2-1-07", "log_{2} x + log_{2}(x − 2) = 3을 풀어 보자.", "진수 조건부터 적어 두고 — 풀고 나서 걸러 낸다",
         [L("진수 조건: x > 0, x − 2 > 0 → x > 2"),
          L("log_{2} x(x − 2) = 3 → x(x − 2) = 8", memo="로그의 합 = 곱의 로그"),
          L("x^{2} − 2x − 8 = 0 → x = 4 또는 x = −2"),
          L("x > 2이므로 x = 4", memo="−2는 진수 조건에 걸린다")],
         "x = 4", f.out(), at=("b4", 1))

    # ── 08 호도법 ──────────────────────────────────────────────
    f = Fig()
    O, Rr = (330, 470), 220
    f.line(O[0] - Rr - 40, O[1], O[0] + Rr + 40, O[1], at="q", c="ink", w=3)
    f.poly([(O[0] + Rr * math.cos(math.radians(a)), O[1] - Rr * math.sin(math.radians(a))) for a in range(0, 181, 4)], at="q", c="soft", w=3, z=False)
    f.line(*O, O[0] + Rr, O[1], at="q", c="coral", w=5)
    f.text(O[0] + Rr / 2, O[1] + 34, "r", z=30, c="coral", at="q", b=800)
    one = math.degrees(1)
    cols = ["teal", "sky", "lilac"]
    for k in range(3):
        a0, a1 = one * k, one * (k + 1)
        arcp(f, *O, Rr, a0, a1, at=0 if k == 0 else 1, c=cols[k], sw=8, fill=cols[k], fo=0.15, dl=0 if k == 0 else 700 * (k - 1))
        mid = math.radians((a0 + a1) / 2)
        f.text(O[0] + (Rr + 34) * math.cos(mid), O[1] - (Rr + 34) * math.sin(mid) + 10, "r", z=28, c=cols[k], at=0 if k == 0 else 1, dl=400 if k == 0 else 700 * (k - 1) + 400, b=800)
    arcp(f, *O, Rr, 3 * one, 180, at=1, c="red", sw=8, dl=1500)
    f.text(O[0] - Rr - 20, O[1] - 60, "0.14r", z=22, c="red", at=1, dl=1800, b=800, a="e")
    f.text(O[0] + 80, O[1] - 30, "1 rad", z=24, c="teal", at=0, dl=700, b=800)
    f.text(CX, 160, "반원의 호 = πr", z=32, c="gold", at=1, dl=2100, b=800)
    f.text(CX, 600, "π rad = 180°", z=36, c="gold", at=2, b=800)
    U.ex("h2-1-08", "호의 길이가 반지름과 같을 때의 중심각을 1라디안이라 할 때, 180°는 몇 라디안일까?", "반원의 호 πr 안에 반지름 길이가 π번 — π 라디안 = 180°",
         [L("호의 길이 = 반지름일 때의 중심각 = 1 라디안", memo="약 57.3°"),
          L("반원의 호 = πr → 반지름 π개", memo="3개와 조금"),
          L("π 라디안 = 180°", memo="60° → {π/3}, 90° → {π/2}")],
         "π 라디안 = 180°", f.out(), at=("b3", 2))

    # ── 09 단위원과 삼각함수 ───────────────────────────────────
    f = Fig()
    O, Rr = (360, 380), 220
    f.line(O[0] - Rr - 50, O[1], O[0] + Rr + 50, O[1], at="q", c="ink", w=3, ar=1)
    f.line(O[0], O[1] + Rr + 40, O[0], O[1] - Rr - 50, at="q", c="ink", w=3, ar=1)
    f.circ(*O, Rr, at="q", c="soft", sw=3)
    f.text(O[0] + Rr + 14, O[1] + 34, "1", z=24, at="q", b=800)
    th = 150
    Pp = (O[0] + Rr * math.cos(math.radians(th)), O[1] - Rr * math.sin(math.radians(th)))
    rr = f.line(*O, O[0] + Rr, O[1], at=0, c="ink", w=4.5)
    rr["mv"] = {"at": 0, "r": -th, "cx": O[0], "cy": O[1], "dl": 200}
    f.arc(*O, 46, 0, th, at=0, c="gold", sw=3, f="gold", fo=0.3, dl=300)
    f.text(O[0] + 30, O[1] - 66, "150°", z=24, c="gold", at=0, dl=900, b=800)
    f.dot(*Pp, r=11, f="ink", at=0, dl=1200)
    f.text(Pp[0] - 16, Pp[1] - 20, "(−{√{3}/2}, {1/2})", z=22, at=0, dl=1300, b=800, a="e")
    f.line(Pp[0], O[1], *Pp, at=1, c="teal", w=7, dr=True)
    f.text(Pp[0] - 14, (O[1] + Pp[1]) / 2 + 10, "sin θ = {1/2}", z=22, c="teal", at=1, dl=500, b=800, a="e")
    f.line(*O, Pp[0], O[1], at=1, c="coral", w=7, dr=True, dl=700)
    f.text((O[0] + Pp[0]) / 2, O[1] + 48, "cos θ = −{√{3}/2}", z=22, c="coral", at=1, dl=1200, b=800)
    f.text(O[0] - Rr * 0.5, O[1] - Rr - 20, "제2사분면: sin만 +", z=22, c="gold", at=2, b=800)
    U.ex("h2-1-09", "θ = 150°일 때 sin θ, cos θ, tan θ의 값을 단위원으로 구해 보자.", "단위원 위의 점 (x, y) — sin θ = y, cos θ = x, tan θ = {y/x}",
         [L("θ = 150° → 점 (−{√{3}/2}, {1/2})", memo="제2사분면"),
          L("sin θ = {1/2}, cos θ = −{√{3}/2}", memo="y좌표, x좌표"),
          L("tan θ = {y/x} = −{√{3}/3}", memo="sin만 +")],
         "sin θ = {1/2}, cos θ = −{√{3}/2}, tan θ = −{√{3}/3}", f.out(), at=("b3", 1))

    # ── 10 삼각함수의 그래프 — 진폭과 주기 ──────────────────────
    f = Fig()
    P = Plane(f, (0, 2 * math.pi + 0.3), (-2.6, 2.6), box=(60, 120, 620, 600), square=False)
    f.line(P.X(0), P.Y(0), P.X(2 * math.pi + 0.3), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(-2.6), P.X(0), P.Y(2.6), at="q", c="ink", w=3, ar=1)
    for k, s in ((1, "{π/2}"), (2, "π"), (3, "{3π/2}"), (4, "2π")):
        f.line(P.X(k * math.pi / 2), P.Y(0) - 8, P.X(k * math.pi / 2), P.Y(0) + 8, at="q", c="ink", w=2)
        f.text(P.X(k * math.pi / 2), P.Y(0) + 40, s, z=22, c="soft", at="q", b=700)
    for v in (1, 2, -1, -2):
        f.text(P.X(0) - 10, P.Y(v) + 7, str(v) if v > 0 else "−" + str(-v), z=20, c="soft", at="q", a="e")
        f.line(P.X(0), P.Y(v), P.X(2 * math.pi), P.Y(v), at="q", c="soft", w=1, o=0.3)
    P.curve(lambda x: math.sin(x), x0=0, x1=2 * math.pi, at=0, c="soft", w=3.5)
    P.curve(lambda x: 2 * math.sin(x), x0=0, x1=2 * math.pi, at=1, c="teal", w=4)
    P.curve(lambda x: 2 * math.sin(2 * x), x0=0, x1=2 * math.pi, at=2, c="coral", w=4.5)
    f.line(P.X(0), P.Y(-2.4), P.X(math.pi), P.Y(-2.4), at=2, c="gold", w=4, ar=2, dl=1200)
    f.text(P.X(math.pi / 2), P.Y(-2.4) + 40, "주기 π", z=24, c="gold", at=2, dl=1400, b=800)
    U.ex("h2-1-10", "y = sin x, y = 2 sin x, y = 2 sin 2x의 그래프를 비교해 보자.", "a sin bx — |a|는 위아래 폭(진폭), 주기는 {2π/|b|}",
         [L("y = sin x: 최댓값 1, 주기 2π"),
          L("y = 2 sin x: 최댓값 2, 최솟값 −2", memo="위아래로 2배"),
          L("y = 2 sin 2x: 주기 {2π/2} = π", memo="옆으로 절반으로 줄어든다")],
         "최댓값 2, 최솟값 −2, 주기 π", f.out(), at=("b3", 1))

    # ── 11 코사인법칙 ───────────────────────────────────────────
    f = Fig()
    u = 50
    A = (100, 520)
    B = (A[0] + 8 * u, A[1])
    C = (A[0] + 5 * u * math.cos(math.radians(60)), A[1] - 5 * u * math.sin(math.radians(60)))
    f.poly([A, B, C], at="q", c="ink", w=3.5)
    for (Pt, s, dx, dy) in ((A, "A", -18, 30), (B, "B", 18, 30), (C, "C", 0, -16)):
        f.text(Pt[0] + dx, Pt[1] + dy, s, z=28, at="q", b=800)
    f.text((A[0] + C[0]) / 2 - 24, (A[1] + C[1]) / 2, "5", z=28, at="q", b=800, a="e")
    f.text((A[0] + B[0]) / 2, A[1] + 40, "8", z=28, at="q", b=800)
    f.arc(*A, 56, 0, 60, at="q", c="gold", sw=3, f="gold", fo=0.35)
    f.text(A[0] + 82, A[1] - 26, "60°", z=24, c="gold", at="q", b=800)
    H = (C[0], A[1])
    f.line(*C, *H, at=1, c="coral", w=3, d=True, dr=True)
    f.line(*A, *H, at=1, c="teal", w=7, dr=True, dl=400)
    f.text((A[0] + H[0]) / 2, A[1] - 16, "5 cos 60°", z=20, c="teal", at=1, dl=800, b=800)
    f.line(*B, *C, at=2, c="gold", w=7, dr=True)
    f.text((B[0] + C[0]) / 2 + 30, (B[1] + C[1]) / 2 - 10, "a = 7", z=32, c="gold", at=2, dl=600, b=800, a="s")
    U.ex("h2-1-11", "b = 5, c = 8, A = 60°인 삼각형 ABC에서 a의 길이를 구해 보자.", "두 변과 끼인각 — 코사인법칙 a^{2} = b^{2} + c^{2} − 2bc cos A",
         [L("a^{2} = 5^{2} + 8^{2} − 2 × 5 × 8 × cos 60°", memo="두 변과 그 끼인각"),
          L("25 + 64 − 2 × 5 × 8 × {1/2} = 49", memo="cos 60° = {1/2}"),
          L("a = 7")],
         "7", f.out(), at=("b3", 1))

    # ── 12 등차수열의 합 — 계단 두 개 ───────────────────────────
    f = Fig()
    u, x0, yb = 38, 130, 560
    for k in range(1, 11):
        f.rect(x0 + (k - 1) * u, yb - k * u, u, k * u, at="q", c="ink", sw=1.5, f="teal", fo=0.45, dl=60 * k)
        f.text(x0 + (k - 0.5) * u, yb + 26, str(k), z=18, c="soft", at="q")
    cx, cy = x0 + 5 * u, yb - 5.5 * u
    for k in range(1, 11):
        el = f.rect(x0 + (k - 1) * u, yb - k * u, u, k * u, at=1, c="ink", sw=1.5, f="coral", fo=0.45, dl=1)
        el["mv"] = {"at": 1, "r": 180, "cx": R1(cx), "cy": R1(cy), "dl": 300}
    f.rect(x0, yb - 11 * u, 10 * u, 11 * u, at=1, c="gold", sw=4, d=True, dl=1300)
    f.text(x0 + 5 * u, yb - 11 * u - 16, "10", z=26, c="gold", at=1, dl=1400, b=800)
    f.text(x0 + 10 * u + 16, yb - 5.5 * u, "11", z=26, c="gold", at=1, dl=1500, b=800, a="s")
    f.text(CX, 100, "110 ÷ 2 = 55", z=34, c="gold", at=2, b=800)
    U.ex("h2-1-12", "1 + 2 + 3 + ⋯ + 10을 등차수열의 합으로 구해 보자.", "같은 합을 거꾸로 하나 더 — 짝마다 (첫째항 + 끝항)",
         [L("S = 1 + 2 + ⋯ + 10", memo="계단 모양"),
          L("2S = 11 × 10 = 110", memo="똑같은 계단을 뒤집어 붙이면 직사각형"),
          L("S = {10 × (1 + 10)/2} = 55", memo="S_{n} = {n(a + l)/2}")],
         "55", f.out(), at=("b4", 1))

    # ── 13 등비수열의 합 ───────────────────────────────────────
    f = Fig()
    u, x0 = 8, 60
    x = x0
    cols = ["teal", "sky", "lilac", "gold", "coral", "leaf"]
    for k in range(6):
        w = u * 2 ** k
        f.rect(x, 230, w, 60, at="q", c="ink", sw=2, f=cols[k], fo=0.5, dl=200 * k)
        if k >= 3:
            f.text(x + w / 2, 270, str(2 ** k), z=22, at="q", dl=200 * k + 100, b=800)
        x += w
    f.text(x0 + 4, 200, "1  2  4", z=18, c="soft", at="q", b=800, a="s")
    f.line(x0, 320, x, 320, at=1, c="ink", w=2.5, ar=2)
    f.text((x0 + x) / 2, 360, "63", z=34, c="ink", at=1, dl=300, b=800)
    f.rect(x, 230, u, 60, at=2, c="ink", sw=2, f="red", fo=0.7)
    f.text(x + 4, 205, "+1", z=22, c="red", at=2, dl=200, b=800)
    f.rect(x0, 430, u * 64, 60, at=2, c="ink", sw=2.5, f="gold", fo=0.4, dl=600)
    f.text(x0 + u * 32, 470, "64 = 2^{6}", z=28, at=2, dl=800, b=800)
    U.ex("h2-1-13", "1 + 2 + 4 + 8 + 16 + 32를 등비수열의 합으로 구해 보자.", "첫째항 1, 공비 2, 항 6개 — S_{n} = {a(r^{n} − 1)/r − 1}",
         [L("첫째항 1, 공비 2, 항의 개수 6"),
          L("S = {1 × (2^{6} − 1)/2 − 1} = 63"),
          L("63 + 1 = 64 = 2^{6}", memo="1만 더하면 다음 항 — 그래서 2^{6} − 1")],
         "63", f.out(), at=("b4", 1))

    # ── 14 ∑ 의 성질 ───────────────────────────────────────────
    f = Fig()
    u, x0, yb = 12, 90, 560
    for k in range(1, 11):
        x = x0 + (k - 1) * 48
        f.rect(x, yb - 2 * k * u, 40, 2 * k * u, at=0, c="ink", sw=1.5, f="teal", fo=0.45, dl=60 * k)
        f.rect(x, yb - (2 * k + 1) * u, 40, u, at=0, c="ink", sw=1.5, f="coral", fo=0.6, dl=600 + 60 * k)
        f.text(x + 20, yb + 24, str(k), z=16, c="soft", at="q")
    f.text(260, 200, "2k: 2 × 55 = 110", z=26, c="teal", at=1, b=800)
    f.text(260, 250, "1: 1 × 10 = 10", z=26, c="coral", at=1, dl=400, b=800)
    f.text(560, 120, "120", z=40, c="gold", at=1, dl=900, b=800)
    U.ex("h2-1-14", "∑_{k=1}^{10}(2k + 1)의 값을 구해 보자.", "∑는 나누어 더할 수 있다 — ∑k = {n(n + 1)/2}, 상수의 합은 (상수) × n",
         [L("∑_{k=1}^{10}(2k + 1) = 2∑_{k=1}^{10}k + ∑_{k=1}^{10}1", memo="2k 부분과 1 부분으로"),
          L("2 × 55 + 1 × 10 = 120", memo="∑k = 55, 1을 10번")],
         "120", f.out(), at=("b4", 1))

    # ── 15 소거되는 합 ─────────────────────────────────────────
    f = Fig()
    toks = ["1", "− {1/2}", "+ {1/2}", "− {1/3}", "+ {1/3}", "− {1/4}", "+ {1/4}", "− {1/5}", "+ {1/5}", "− {1/6}"]
    xs = [70 + 58 * k for k in range(10)]
    for k, s in enumerate(toks):
        f.text(xs[k], 260, s, z=26, at=0, dl=80 * k, b=700)
    for j in range(4):
        a, b = 1 + 2 * j, 2 + 2 * j
        arch(f, xs[a], xs[b], 210, 1, h=34, c="gold", dl=450 * j)
        f.line(xs[a] - 24, 270, xs[a] + 24, 238, at=1, c="red", w=3, dl=450 * j + 300)
        f.line(xs[b] - 24, 270, xs[b] + 24, 238, at=1, c="red", w=3, dl=450 * j + 300)
    f.circ(xs[0], 250, 30, at=2, c="teal", sw=4)
    f.circ(xs[9], 250, 36, at=2, c="teal", sw=4, dl=200)
    f.text(CX, 420, "1 − {1/6} = {5/6}", z=42, c="gold", at=2, dl=600, b=800)
    U.ex("h2-1-15", "{1/1 × 2} + {1/2 × 3} + ⋯ + {1/5 × 6}의 값을 구해 보자.", "{1/k(k + 1)} = {1/k} − {1/k + 1}로 쪼개면 가운데가 줄줄이 지워진다",
         [L("{1/k(k + 1)} = {1/k} − {1/k + 1}", memo="통분을 거꾸로"),
          L("(1 − {1/2}) + ({1/2} − {1/3}) + ⋯ + ({1/5} − {1/6})", memo="이웃끼리 지워진다"),
          L("1 − {1/6} = {5/6}", memo="맨 앞과 맨 뒤만 남는다")],
         "{5/6}", f.out(), at=("b3", 2), ident=True)

    # ── 16 귀납적 정의 — 사다리 ─────────────────────────────────
    f = Fig()
    vals = [1, 4, 7, 10]
    for k, v in enumerate(vals):
        x, y = 110 + 140 * k, 540 - 120 * k
        at = "q" if k == 0 else k - 1
        ch = chipm(f, x, y, str(v), at, c="teal" if k == 0 else "coral", z=40)
        f.text(x, y + 50, f"a_{{{k + 1}}}", z=24, c="soft", at=at, b=800)
        if k:
            for el in ch:
                fly(el, -140, 120, dl=300, ms=700)
            px, py = 110 + 140 * (k - 1), 540 - 120 * (k - 1)
            arch(f, px + 30, x - 30, py - 40, at, h=40, c="gold")
            f.text((px + x) / 2, py - 100, "+3", z=24, c="gold", at=at, dl=300, b=800)
    U.ex("h2-1-16", "a_{1} = 1, a_{n + 1} = a_{n} + 3으로 정의된 수열의 a_{2}, a_{3}, a_{4}를 구해 보자.", "n에 1, 2, 3을 차례로 — 앞의 항에서 다음 항으로",
         [L("a_{2} = a_{1} + 3 = 4", memo="n = 1"),
          L("a_{3} = a_{2} + 3 = 7", memo="n = 2"),
          L("a_{4} = a_{3} + 3 = 10", memo="n = 3 — 공차 3인 등차수열")],
         "4, 7, 10", f.out(), at=("b3", 2))

    # ── 17 수학적 귀납법 — 도미노 ───────────────────────────────
    f = Fig()
    n, w, h, gap, yb = 8, 22, 150, 64, 520
    f.line(40, yb, 620, yb, at="q", c="ink", w=3)
    for k in range(n):
        x = 70 + gap * k
        el = f.rect(x, yb - h, w, h, at="q", c="ink", sw=2.5, f="coral" if k == 0 else "teal", fo=0.45)
        el["mv"] = {"at": 0 if k == 0 else 1, "r": 62, "cx": R1(x + w), "cy": yb, "dl": 300 if k == 0 else 250 * (k - 1)}
        lab = "1" if k == 0 else ("k" if k == 4 else ("k + 1" if k == 5 else ("2" if k == 1 else "")))
        if lab:
            f.text(x + w / 2, yb + 40, lab, z=22, c="coral" if k == 0 else "teal", at="q", b=800)
    f.text(160, 220, "(i) 첫 도미노", z=24, c="coral", at=0, dl=600, b=800)
    f.text(420, 220, "(ii) k → k + 1", z=24, c="teal", at=1, b=800)
    f.text(CX, 620, "모든 n에서 성립", z=34, c="gold", at=2, b=800)
    U.ex("h2-1-17", "수학적 귀납법의 두 단계가 왜 모든 자연수 n에 대한 증명이 되는지 도미노로 알아보자.", "(i) 첫 번째가 넘어지고 (ii) k번째가 넘어지면 k + 1번째도 넘어진다",
         [L("(i) n = 1일 때 성립", memo="첫 도미노가 넘어진다"),
          L("(ii) n = k일 때 성립 → n = k + 1일 때 성립", memo="앞이 넘어지면 다음도"),
          L("모든 자연수 n에서 성립", memo="도미노가 끝까지")],
         "(i), (ii)를 보이면 모든 n에서 성립", f.out(), at=("b2", 2))
