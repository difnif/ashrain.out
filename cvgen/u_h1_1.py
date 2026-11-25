# 고1 공통수학1 — 다항식 · 방정식과 부등식 · 경우의 수 · 행렬
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, nl_range, hop, travel, parabola


def chipm(f, x, y, s, at, c="teal", z=34, dl=0, un=None, fo=0.16):
    w = max(z * 1.25, tw(s, z) + z * 0.6)
    r = f.rect(x - w / 2, y - z * 0.98, w, z * 1.4, c=c, sw=3, rx=z * 0.42, f=c, fo=fo, at=at, dl=dl, un=un)
    t = f.text(x, y, s, z=z, c=c, at=at, dl=dl + 60, un=un, b=800)
    return [r, t]


def brackets(f, x0, y0, x1, y1, at="q", c="ink", dl=0, w=3):
    """행렬 괄호 ( )"""
    h = y1 - y0
    f.poly([(x0 + 14, y0), (x0, y0 + h * 0.2), (x0, y1 - h * 0.2), (x0 + 14, y1)], at=at, c=c, w=w, z=False, dl=dl)
    f.poly([(x1 - 14, y0), (x1, y0 + h * 0.2), (x1, y1 - h * 0.2), (x1 - 14, y1)], at=at, c=c, w=w, z=False, dl=dl)


def build(U):
    # ── 01 다항식의 나눗셈(세로셈) ─────────────────────────────
    f = Fig()
    c2, c1, c0 = 290, 420, 540
    f.text(130, 200, "x + 1", z=36, at="q", b=700)
    f.poly([(203, 224), (213, 196), (216, 168), (214, 150), (600, 150)], at="q", c="ink", w=3, z=False)
    for s, x in (("2x^{2}", c2), ("+ 3x", c1), ("+ 4", c0)):
        f.text(x, 200, s, z=36, at="q", b=700)
    f.text(c1, 118, "2x", z=36, c="teal", at=0, b=800)
    for s, x in (("2x^{2}", c2), ("+ 2x", c1)):
        e = f.text(x, 270, s, z=36, c="teal", at=0, dl=500, b=800)
        fly(e, c1 - x, 118 - 270, dl=40, ms=700)
    f.text(232, 270, "−", z=36, c="teal", at=0, dl=900, b=800)
    f.line(240, 292, 470, 292, at=0, c="ink", w=2.5, dl=1000)
    f.text(c1, 345, "x", z=36, at=1, b=700)
    e = f.text(c0, 345, "+ 4", z=36, at=1, dl=300, b=700)
    fly(e, 0, 200 - 345, dl=40, ms=700)
    f.text(c0, 118, "+ 1", z=36, c="sky", at=2, b=800)
    for s, x in (("x", c1), ("+ 1", c0)):
        e = f.text(x, 415, s, z=36, c="sky", at=2, dl=500, b=800)
        fly(e, c0 - x, 118 - 415, dl=40, ms=700)
    f.text(362, 415, "−", z=36, c="sky", at=2, dl=900, b=800)
    f.line(370, 437, 590, 437, at=2, c="ink", w=2.5, dl=1000)
    f.text(c0, 490, "3", z=40, c="coral", at=2, dl=1300, b=800)
    f.rect(c0 - 30, 452, 60, 54, at=2, c="coral", sw=3, rx=10, dl=1500)
    f.text(CX, 600, "(x + 1)(2x + 1) + 3", z=34, c="gold", at=3, b=800)
    U.ex("h1-1-01", "2x^{2} + 3x + 4를 x + 1로 나눈 몫과 나머지를 구해 보자.", "내림차순으로 세로셈 — 나머지의 차수가 나누는 식보다 낮아질 때까지",
         [L("2x × (x + 1) = 2x^{2} + 2x", memo="몫의 첫 항 2x"),
          L("(2x^{2} + 3x + 4) − (2x^{2} + 2x) = x + 4", memo="빼고 다음 항 내리기"),
          L("(x + 4) − (x + 1) = 3", memo="몫의 다음 항 +1"),
          L("2x^{2} + 3x + 4 = (x + 1)(2x + 1) + 3", memo="A = BQ + R")],
         "몫 2x + 1, 나머지 3", f.out(), at=("b4", 2), ident=True)

    # ── 02 조립제법 ────────────────────────────────────────────
    f = Fig()
    xc = [220, 320, 420, 520]
    c1v, prod, res = ["1", "−2", "−5", "6"], [None, "1", "−1", "−6"], ["1", "−1", "−6", "0"]
    f.line(155, 160, 155, 330, at="q", c="ink", w=3)
    f.line(155, 310, 580, 310, at="q", c="ink", w=3)
    for k, s in enumerate(c1v):
        f.text(xc[k], 200, s, z=36, at="q", b=700)
    f.text(110, 200, "1", z=38, c="gold", at="q", b=800)
    f.rect(85, 160, 50, 56, at=0, c="gold", sw=3, rx=10)
    f.text(110, 262, "f(1) = 0", z=20, c="gold", at=0, dl=500, b=800)
    t = 0
    e = f.text(xc[0], 370, res[0], z=36, c="teal", at=1, dl=t, b=800)
    fly(e, 0, -170, dl=40, ms=600)
    for k in range(1, 4):
        t += 600
        f.line(xc[k - 1] + 18, 350, xc[k] - 18, 292, at=1, c="soft", w=2.5, ar=1, dr=True, dl=t)
        e = f.text(xc[k], 280, prod[k], z=30, c="sky", at=1, dl=t + 200, b=800)
        fly(e, xc[k - 1] - xc[k], 90, dl=40, ms=500)
        t += 600
        f.text(xc[k], 370, res[k], z=36, c="coral" if k == 3 else "teal", at=1, dl=t, b=800)
    f.rect(xc[3] - 32, 332, 64, 56, at=1, c="coral", sw=3, rx=10, dl=t + 200)
    f.text(320, 430, "몫의 계수", z=22, c="teal", at=2, b=800)
    f.text(520, 430, "나머지", z=22, c="coral", at=2, dl=200, b=800)
    f.text(CX, 540, "(x − 1)(x^{2} − x − 6)", z=36, c="gold", at=2, dl=600, b=800)
    U.ex("h1-1-02", "x^{3} − 2x^{2} − 5x + 6을 x − 1로 나눈 몫과 나머지를 조립제법으로 구해 보자.", "나머지 정리 f(1)로 먼저 확인 — 계수만 내려 적고 1을 곱해 더한다",
         [L("f(1) = 1 − 2 − 5 + 6 = 0", memo="나머지 0 — 나누어떨어진다"),
          L("1, −2, −5, 6 → 1, −1, −6, 0", memo="내리고 · 곱하고 · 더하고"),
          L("x^{3} − 2x^{2} − 5x + 6 = (x − 1)(x^{2} − x − 6)", memo="앞의 수들이 몫의 계수")],
         "몫 x^{2} − x − 6, 나머지 0", f.out(), at=("b4", 2), ident=True)

    # ── 03 인수정리로 인수분해 ─────────────────────────────────
    f = Fig()
    for k, s in enumerate(("1", "−1", "3", "−3")):
        chipm(f, 150 + 110 * k, 90, s, "q", c="soft", z=30, dl=100 * k)
    f.text(560, 92, "후보", z=22, c="soft", at="q", b=800)
    chipm(f, 150, 90, "1", 0, c="gold", z=30, fo=0.4)
    f.text(150, 160, "f(1) = 0", z=24, c="gold", at=0, dl=400, b=800)
    S = Strip(f, y=230, z=36)
    S.row(1, [{"s": "(x − 1)", "c": "gold"}, {"s": "(x^{2} − 2x − 3)", "g": 0.02}], keep=True)
    S.row(2, [{"s": "(x − 1)", "frm": 0, "c": "gold"}, {"s": "(x − 3)", "frm": 1, "c": "teal", "g": 0.02}, {"s": "(x + 1)", "frm": 1, "c": "coral", "g": 0.02}], y=310, keep=True)
    P = Plane(f, (-2, 4), (-5, 5), box=(60, 360, 620, 660), square=False)
    P.axes(at=2, grid=None, lab_step=1, ystep=10)
    P.curve(lambda x: x ** 3 - 3 * x ** 2 - x + 3, at=2, c="sky", w=4)
    for k, (r_, col) in enumerate(((-1, "coral"), (1, "gold"), (3, "teal"))):
        P.pt(r_, 0, at=2, f=col, r=11, dl=900 + 250 * k)
    U.ex("h1-1-03", "x^{3} − 3x^{2} − x + 3을 인수분해해 보자.", "f(a) = 0인 a를 찾으면 x − a가 인수 — 후보는 ±(상수항의 약수)",
         [L("f(1) = 1 − 3 − 1 + 3 = 0", memo="후보 ±1, ±3 중 1이 근"),
          L("x^{3} − 3x^{2} − x + 3 = (x − 1)(x^{2} − 2x − 3)", memo="조립제법으로 몫 구하기"),
          L("(x − 1)(x^{2} − 2x − 3) = (x − 1)(x − 3)(x + 1)")],
         "(x − 1)(x − 3)(x + 1)", f.out(), at=("b4", 3), ident=True)

    # ── 04 i 의 거듭제곱 — 한 바퀴에 4번 ──────────────────────
    f = Fig()
    O, Rr = (330, 340), 200
    f.circ(*O, Rr, at="q", c="soft", sw=2.5, d=True)
    pos = {0: "1", 90: "i", 180: "−1", 270: "−i"}
    for a, s in pos.items():
        x, y = O[0] + (Rr + 46) * math.cos(math.radians(a)), O[1] - (Rr + 46) * math.sin(math.radians(a))
        f.text(x, y + 12, s, z=34, at="q", b=800)
    f.dot(*O, r=8, f="ink", at="q")
    steps = [(0, 0, 0), (0, 1, 1100), (1, 2, 0), (2, 3, 0)]
    cols = ["teal", "coral", "sky", "gold"]
    for k, (at, n, dl) in enumerate(steps):
        a0 = 90 * n
        el = f.line(O[0], O[1], O[0] + Rr * math.cos(math.radians(a0)), O[1] - Rr * math.sin(math.radians(a0)), at=at, c=cols[k], w=5, ar=1, dl=dl)
        el["mv"] = {"at": at, "r": -90, "cx": O[0], "cy": O[1], "dl": dl + 200}
        a1 = a0 + 90
        x, y = O[0] + (Rr - 50) * math.cos(math.radians(a1 - 22)), O[1] - (Rr - 50) * math.sin(math.radians(a1 - 22))
        f.text(x, y + 10, f"i^{{{k + 1}}}", z=26, c=cols[k], at=at, dl=dl + 1100, b=800)
    f.text(560, 600, "× i = 90° 회전", z=22, c="soft", at=0, dl=1800, b=800)
    f.circ(O[0] - Rr - 46, O[1] - 2, 40, at=3, c="red", sw=4)
    f.text(160, 620, "i^{10}: 4번씩 두 바퀴 + 2", z=24, c="red", at=3, dl=300, b=800)
    U.ex("h1-1-04", "i, i^{2}, i^{3}, i^{4}, …의 규칙을 찾고 i^{10}을 구해 보자.", "i를 곱할 때마다 한 칸씩 — 네 번이면 제자리(주기 4)",
         [L("i^{1} = i, i^{2} = −1", memo="i^{2} = −1은 약속"),
          L("i^{3} = i^{2} × i = −i"),
          L("i^{4} = (i^{2})^{2} = 1", memo="다시 1 — 주기 4"),
          L("i^{10} = i^{4 × 2 + 2} = i^{2} = −1", memo="지수를 4로 나눈 나머지 2")],
         "−1", f.out(), at=("b4", 1))

    # ── 05 허근 ───────────────────────────────────────────────
    f = Fig()
    S = Strip(f, y=110, z=40)
    S.row("q", ["x^{2} + 2x + 3", "=", "0"], keep=True)
    S.row(0, ["x", "=", {"s": "{−2 ± √{4 − 12}/2}"}], y=235, keep=True, z=40)
    S2 = Strip(f, y=370, z=40)
    S2.row(1, [{"s": "√{−8}", "c": "coral"}, "=", {"s": "√{8}", "c": "coral"}, {"s": "i", "c": "red", "g": 0.06}, "=", {"s": "2√{2}i", "c": "coral"}], keep=True)
    f.text(560, 310, "−1 → i^{2}", z=22, c="red", at=1, dl=900, b=800)
    S3 = Strip(f, y=500, z=40)
    S3.row(2, ["x", "=", {"s": "{−2 ± 2√{2}i/2}"}], keep=True)
    S4 = Strip(f, y=620, z=46)
    S4.row(2, ["x", "=", {"s": "−1 ± √{2}i", "c": "gold"}], keep=True, dl0=1200)
    U.ex("h1-1-05", "이차방정식 x^{2} + 2x + 3 = 0을 풀어 보자.", "근의 공식 그대로 — 근호 안이 음수면 i로 바꾼다",
         [L("x = {−2 ± √{4 − 12}/2}", memo="근의 공식"),
          L("√{−8} = √{8}i = 2√{2}i", memo="음수의 제곱근은 i를 붙여서"),
          L("x = {−2 ± 2√{2}i/2} = −1 ± √{2}i", memo="약분")],
         "x = −1 ± √{2}i", f.out(), at=("b3", 1))

    # ── 06 근과 계수의 관계 ─────────────────────────────────────
    f = Fig()
    S = Strip(f, y=100, z=40)
    xs, _ = S.row("q", ["x^{2}", "−", "3x", "+", "1", "=", "0"], keep=True)
    e = chipm(f, 180, 200, "α + β = 3", 0, c="teal", z=30)
    for el in e:
        fly(el, (xs[1] + xs[2]) / 2 - 180, -100, dl=40, ms=700)
    e = chipm(f, 480, 200, "αβ = 1", 0, c="coral", z=30, dl=700)
    for el in e:
        fly(el, xs[4] - 480, -100, dl=40, ms=700)
    X0, Y0, a, b = 140, 270, 220, 120
    f.rect(X0, Y0, a + b, a + b, at=1, c="ink", sw=3)
    f.text(X0 + (a + b) / 2, Y0 - 12, "α + β", z=26, c="teal", at=1, b=800)
    f.rect(X0, Y0, a, a, at=1, c="ink", sw=2, f="teal", fo=0.3)
    f.text(X0 + a / 2, Y0 + a / 2 + 10, "α^{2}", z=30, c="teal", at=1, b=800)
    f.rect(X0 + a, Y0 + a, b, b, at=1, c="ink", sw=2, f="teal", fo=0.3)
    f.text(X0 + a + b / 2, Y0 + a + b / 2 + 10, "β^{2}", z=26, c="teal", at=1, b=800)
    for (x, y, w, h) in ((X0 + a, Y0, b, a), (X0, Y0 + a, a, b)):
        f.rect(x, y, w, h, at=1, c="ink", sw=2, f="coral", fo=0.35, dl=300)
        f.text(x + w / 2, y + h / 2 + 10, "αβ", z=26, c="coral", at=1, dl=400, b=800)
    f.cross(X0 + a + b / 2, Y0 + a / 2, s=40, at=2, c="red")
    f.cross(X0 + a / 2, Y0 + a + b / 2, s=40, at=2, c="red", dl=200)
    f.text(560, 400, "3^{2}", z=32, c="teal", at=2, dl=300, b=800)
    f.text(560, 460, "− 2 × 1", z=30, c="coral", at=2, dl=500, b=800)
    f.text(560, 540, "= 7", z=40, c="gold", at=2, dl=800, b=800)
    U.ex("h1-1-06", "x^{2} − 3x + 1 = 0의 두 근을 α, β라 할 때, α^{2} + β^{2}의 값을 구해 보자.", "풀지 않고 합과 곱으로 — α + β = −{b/a}, αβ = {c/a}",
         [L("α + β = 3, αβ = 1", memo="계수에서 바로"),
          L("α^{2} + β^{2} = (α + β)^{2} − 2αβ", memo="한 변이 α + β인 정사각형에서 αβ 두 조각을 뺀다"),
          L("α^{2} + β^{2} = 3^{2} − 2 × 1 = 7")],
         "7", f.out(), at=("b3", 1))

    # ── 07 포물선과 직선의 위치 관계 ─────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 5), (-2, 8), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x * x - 3 * x + 4, at="q", c="sky", w=4.5)
    ln = P.lineq(1, 1, at=0, c="coral", w=4)
    f.text(P.X(4.4), P.Y(6.6), "y = x + 1", z=22, c="coral", at=0, dl=800, b=800)
    for k, (dk, col, lab) in enumerate(((1, "gold", "D = 0 접한다"), (2, "lilac", "D < 0 만나지 않는다"))):
        g = P.lineq(1, 1, at=1, c=col, w=3, d=True, dr=False)
        slide(g, 1, dy=P.Y(-dk) - P.Y(0), dl=600 + 700 * k)
        f.text(P.X(4.4), P.Y(4.4 - 1.6 * k) + 0, lab, z=20, c=col, at=1, dl=1500 + 700 * k, b=800, a="s")
    f.text(P.X(4.4), P.Y(7.4), "D > 0 두 점", z=20, c="coral", at=1, dl=200, b=800, a="s")
    P.pt(1, 2, at=2, f="coral", r=11, label="(1, 2)", pos="w", z=24, c="coral")
    P.pt(3, 4, at=2, f="coral", r=11, label="(3, 4)", pos="w", z=24, c="coral", dl=300)
    P.pt(2, 2, at=1, f="gold", r=9, dl=1300)
    U.ex("h1-1-07", "포물선 y = x^{2} − 3x + 4와 직선 y = x + 1의 위치 관계를 판별하고 교점을 구해 보자.", "연립한 이차방정식의 판별식 D의 부호로 — 두 점 · 접함 · 만나지 않음",
         [L("x^{2} − 3x + 4 = x + 1 → x^{2} − 4x + 3 = 0", memo="두 식의 y가 같은 x"),
          L("D = 16 − 12 = 4 > 0", memo="직선을 내리면 D = 0(접함), 더 내리면 D < 0"),
          L("(x − 1)(x − 3) = 0 → (1, 2), (3, 4)", memo="교점")],
         "두 점 (1, 2), (3, 4)에서 만난다", f.out(), at=("b3", 1), sub={"x": 1})

    # ── 08 제한된 범위의 최대 · 최소 ───────────────────────────
    f = Fig()
    P = Plane(f, (-1, 5), (-1, 10), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=1, lab_step=1)
    f.poly([P.P(0, -1), P.P(3, -1), P.P(3, 10), P.P(0, 10)], at="q", c="none", f="gold", fo=0.1)
    P.curve(lambda x: (x - 2) ** 2 + 1, at="q", c="soft", w=3, d=True)
    P.curve(lambda x: (x - 2) ** 2 + 1, x0=0, x1=3, at=0, c="sky", w=6)
    f.text(P.X(1.5), P.Y(9.4), "0 ≤ x ≤ 3", z=24, c="gold", at="q", b=800)
    P.pt(0, 5, at=1, f="coral", r=11, label="f(0) = 5", pos="e", z=22, c="coral")
    P.pt(3, 2, at=1, f="teal", r=11, label="f(3) = 2", pos="e", z=22, c="teal", dl=300)
    P.pt(2, 1, at=1, f="gold", r=11, label="f(2) = 1", pos="s", z=22, c="gold", dl=600)
    f.text(P.X(0) + 20, P.Y(5) - 40, "최댓값", z=24, c="coral", at=2, b=800, a="s")
    f.text(P.X(2), P.Y(1) + 70, "최솟값", z=24, c="gold", at=2, dl=300, b=800)
    U.ex("h1-1-08", "0 ≤ x ≤ 3에서 f(x) = x^{2} − 4x + 5의 최댓값과 최솟값을 구해 보자.", "꼭짓점이 범위 안에 있는지 확인 — 양 끝값과 꼭짓점을 비교",
         [L("f(x) = (x − 2)^{2} + 1", memo="꼭짓점 x = 2는 범위 안"),
          L("f(0) = 5, f(3) = 2, f(2) = 1", memo="후보 셋"),
          L("최댓값 5, 최솟값 1")],
         "최댓값 5, 최솟값 1", f.out(), at=("b3", 1))

    # ── 09 사차방정식 — x^2 = t ────────────────────────────────
    f = Fig()
    S = Strip(f, y=110, z=40)
    S.row("q", ["x^{4} − 5x^{2} + 4", "=", "0"], keep=True)
    S.row(0, [{"s": "t^{2} − 5t + 4", "frm": 0, "c": "teal"}, {"s": "=", "frm": 1}, {"s": "0", "frm": 2}], y=210, keep=True)
    f.text(90, 165, "x^{2} = t", z=24, c="teal", at=0, dl=200, b=800)
    S.row(1, [{"s": "(t − 1)(t − 4)", "frm": 0, "c": "teal"}, {"s": "=", "frm": 1}, {"s": "0", "frm": 2}], y=310, keep=True)
    nl = NL(f, -3, 3, y=560, x0=70, x1=590, step=1, lab_step=1, z=22)
    for k, (tv, col, xs_) in enumerate(((1, "coral", (-1, 1)), (4, "gold", (-2, 2)))):
        ch = chipm(f, CX, 430, f"t = {tv}", 2, c=col, z=28, dl=900 * k, un=None)
        for xv in xs_:
            d = f.dot(nl.X(xv), 560, r=12, f=col, at=2, dl=900 * k + 500)
            fly(d, CX - nl.X(xv), 430 - 560, dl=40, ms=700)
            f.text(nl.X(xv), 520, ("" if xv > 0 else "−") + str(abs(xv)), z=24, c=col, at=2, dl=900 * k + 1100, b=800)
        for el in ch:
            el["un"] = "a"
    U.ex("h1-1-09", "사차방정식 x^{4} − 5x^{2} + 4 = 0을 풀어 보자.", "x^{2} = t로 치환하면 이차방정식",
         [L("x^{2} = t → t^{2} − 5t + 4 = 0"),
          L("(t − 1)(t − 4) = 0 → t = 1 또는 t = 4"),
          L("x^{2} = 1 → x = ±1, x^{2} = 4 → x = ±2", memo="t 하나에서 x 두 개")],
         "x = ±1, ±2", f.out(), at=("b3", 1))

    # ── 10 연립이차방정식 — 원과 직선 ───────────────────────────
    f = Fig()
    P = Plane(f, (-5, 5), (-5, 5), box=(60, 50, 620, 610))
    P.axes(at="q", grid=1, lab_step=1)
    f.circ(*P.P(0, 0), P.sx * math.sqrt(13), at="q", c="sky", sw=4)
    f.text(P.X(3.2), P.Y(3.6), "x^{2} + y^{2} = 13", z=22, c="sky", at="q", b=800)
    P.lineq(1, 1, at=0, c="coral", w=4)
    f.text(P.X(-3.6), P.Y(-1.4), "y = x + 1", z=22, c="coral", at=0, dl=800, b=800)
    P.pt(2, 3, at=3, f="gold", r=12, label="(2, 3)", pos="e", z=24, c="gold")
    P.pt(-3, -2, at=3, f="gold", r=12, label="(−3, −2)", pos="w", z=24, c="gold", dl=300)
    f.line(*P.P(2, 0), *P.P(2, 3), at=2, c="gold", w=2.5, d=True)
    f.line(*P.P(-3, 0), *P.P(-3, -2), at=2, c="gold", w=2.5, d=True, dl=200)
    U.ex("h1-1-10", "연립방정식 y = x + 1, x^{2} + y^{2} = 13을 풀어 보자.", "일차식을 이차식에 대입해 문자 하나를 없앤다",
         [L("x^{2} + (x + 1)^{2} = 13", memo="y = x + 1을 대입"),
          L("2x^{2} + 2x − 12 = 0 → x^{2} + x − 6 = 0"),
          L("(x − 2)(x + 3) = 0 → x는 2 또는 −3"),
          L("(2, 3), (−3, −2)", memo="원과 직선의 두 교점")],
         "(2, 3), (−3, −2)", f.out(), at=("b2", 2), sub={"x": 2, "y": 3})

    # ── 11 연립일차부등식 ───────────────────────────────────────
    f = Fig()
    nl = NL(f, 0, 6, y=470, x0=70, x1=590, step=1, lab_step=1, z=24)
    nl_range(nl, 2, None, at=0, closed_a=False, right=True, c="teal", up=60)
    f.text(nl.X(4.5), 360, "x > 2", z=28, c="teal", at=0, dl=600, b=800)
    nl_range(nl, 4, None, at=1, closed_a=True, right=False, c="coral", up=150)
    f.text(nl.X(1.5), 270, "x ≤ 4", z=28, c="coral", at=1, dl=600, b=800)
    f.rect(nl.X(2), 290, nl.X(4) - nl.X(2), 180, at=2, c="none", f="gold", fo=0.3)
    f.text(nl.X(3), 590, "2 < x ≤ 4", z=36, c="gold", at=2, dl=300, b=800)
    U.ex("h1-1-11", "부등식 1 < 2x − 3 ≤ 5를 풀어 보자.", "A < B ≤ C는 두 부등식 A < B, B ≤ C를 함께 — 수직선의 공통부분",
         [L("1 < 2x − 3 → x > 2", memo="4 < 2x"),
          L("2x − 3 ≤ 5 → x ≤ 4", memo="2x ≤ 8"),
          L("2 < x ≤ 4", memo="겹치는 부분")],
         "2 < x ≤ 4", f.out(), at=("b3", 1))

    # ── 12 절댓값 부등식 — 거리 ─────────────────────────────────
    f = Fig()
    nl = NL(f, -4, 5, y=430, x0=50, x1=620, step=0.5, lab_step=1, z=22)
    cx_ = nl.X(0.5)
    f.dot(cx_, 430, r=11, f="gold", at="q")
    f.text(cx_, 380, "{1/2}", z=26, c="gold", at="q", b=800)
    for k, (v, col) in enumerate(((-2, "teal"), (3, "teal"))):
        d = f.dot(cx_, 430, r=11, f="paper", c=col, sw=4, at=0, dl=100)
        slide(d, 0, dx=nl.X(v) - cx_, dl=400)
        f.line(cx_, 470 + 20 * k, nl.X(v), 470 + 20 * k, at=0, c=col, w=3, ar=1, dr=True, dl=400)
    f.text(cx_, 540, "거리 {5/2}씩", z=24, c="teal", at=0, dl=1300, b=800)
    f.line(nl.X(-2), 396, nl.X(3), 396, at=2, c="gold", w=7, dr=True)
    f.text(CX, 300, "−2 < x < 3", z=38, c="gold", at=2, dl=400, b=800)
    U.ex("h1-1-12", "부등식 |2x − 1| < 5를 풀어 보자.", "|A| < a ⇔ −a < A < a — 가운데에서 거리가 a 미만",
         [L("−5 < 2x − 1 < 5", memo="절댓값을 벗기면 사이"),
          L("−4 < 2x < 6"),
          L("−2 < x < 3", memo="{1/2}에서 거리 {5/2} 미만")],
         "−2 < x < 3", f.out(), at=("b2", 1))

    # ── 13 이차부등식 — x축 아래 ───────────────────────────────
    f = Fig()
    P = Plane(f, (-4, 5), (-7, 6), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x * x - x - 6, at="q", c="sky", w=4)
    P.pt(-2, 0, at=0, f="ink", r=9)
    P.pt(3, 0, at=0, f="ink", r=9, dl=200)
    P.curve(lambda x: x * x - x - 6, x0=-2, x1=3, at=1, c="coral", w=7)
    f.line(*P.P(-2, 0), *P.P(3, 0), at=1, c="gold", w=8, dr=True, dl=600)
    f.text(P.X(0.5), P.Y(-6.8) + 4, "x축 아래", z=24, c="coral", at=1, dl=300, b=800)
    f.text(P.X(0.5), P.Y(1.2), "−2 < x < 3", z=30, c="gold", at=1, dl=1100, b=800)
    U.ex("h1-1-13", "이차부등식 x^{2} − x − 6 < 0을 풀어 보자.", "y = x^{2} − x − 6이 x축 아래에 있는 x의 범위",
         [L("(x + 2)(x − 3) < 0", memo="x축과 −2, 3에서 만난다"),
          L("−2 < x < 3", memo="그래프가 x축 아래인 구간 — 두 근 사이")],
         "−2 < x < 3", f.out(), at=("b2", 1))

    # ── 14 약수의 개수 — 곱의 법칙 ──────────────────────────────
    f = Fig()
    rows_, cols_ = [1, 2, 4, 8], [1, 3, 9]
    x0, y0, cw, rh = 170, 150, 140, 90
    f.text(x0 - 60, y0 - 30, "×", z=30, c="soft", at="q", b=800)
    for j, c_ in enumerate(cols_):
        f.text(x0 + cw * j + cw / 2, y0 - 24, str(c_), z=30, c="coral", at=0, dl=200 * j, b=800)
    for i, r_ in enumerate(rows_):
        f.text(x0 - 40, y0 + rh * i + rh / 2 + 10, str(r_), z=30, c="teal", at=0, dl=700 + 150 * i, b=800)
    f.text(x0 + 1.5 * cw, 86, "3^{0}, 3^{1}, 3^{2}", z=22, c="coral", at=1, b=800)
    f.text(70, y0 + 2 * rh + 10, "2^{0} ~ 2^{3}", z=20, c="teal", at=1, dl=200, b=800, a="m")
    k = 0
    for i, r_ in enumerate(rows_):
        for j, c_ in enumerate(cols_):
            f.rect(x0 + cw * j, y0 + rh * i, cw, rh, at=2, c="ink", sw=2, f="gold", fo=0.2, dl=1 + 120 * k)
            f.text(x0 + cw * j + cw / 2, y0 + rh * i + rh / 2 + 10, str(r_ * c_), z=30, at=2, dl=60 + 120 * k, b=700)
            k += 1
    f.text(CX + 40, 560, "4 × 3 = 12개", z=36, c="gold", at=2, dl=1700, b=800)
    U.ex("h1-1-14", "72의 약수의 개수를 구해 보자.", "72 = 2^{3} × 3^{2} — 2의 지수와 3의 지수를 각각 고르는 곱의 법칙",
         [L("72 = 2^{3} × 3^{2}"),
          L("2의 지수 0 ~ 3: 4가지, 3의 지수 0 ~ 2: 3가지", memo="각각 독립으로 고른다"),
          L("4 × 3 = 12", memo="곱의 법칙 — (3 + 1)(2 + 1)")],
         "12개", f.out(), at=("b3", 1))

    # ── 15 순열 — 이웃하게 세우기 ───────────────────────────────
    f = Fig()
    xs = [150, 260, 370, 480]
    cards = {}
    for k, s in enumerate("ABCD"):
        col = "coral" if s in "AB" else "teal"
        r_ = f.rect(xs[k] - 42, 110, 84, 90, at="q", c=col, sw=3, rx=12, f=col, fo=0.2)
        t = f.text(xs[k], 170, s, z=40, c=col, at="q", b=800)
        cards[s] = (r_, t)
    f.rect(xs[0] - 54, 98, 218, 114, at=0, c="gold", sw=4, rx=16, d=True)
    f.text(xs[0] + 55, 245, "한 묶음", z=24, c="gold", at=0, dl=300, b=800, un=2)
    arr = ["[AB] C D", "[AB] D C", "C [AB] D", "D [AB] C", "C D [AB]", "D C [AB]"]
    for k, s in enumerate(arr):
        f.text(170 + 300 * (k % 2), 320 + 60 * (k // 2), s, z=28, c="ink", at=1, dl=200 * k, b=700)
    f.text(CX, 520, "3 × 2 × 1 = 6", z=28, c="teal", at=1, dl=1400, b=800)
    for el in cards["A"]:
        el["mv"] = {"at": 2, "dx": 110, "dl": 200}
    for el in cards["B"]:
        el["mv"] = {"at": 2, "dx": -110, "dl": 200}
    f.text(xs[0] + 55, 245, "AB, BA", z=24, c="coral", at=2, dl=1100, b=800)
    f.text(CX, 610, "6 × 2 = 12", z=38, c="gold", at=3, b=800)
    U.ex("h1-1-15", "A, B, C, D 4명이 한 줄로 설 때, A와 B가 이웃하는 경우의 수를 구해 보자.", "이웃하는 것은 한 묶음으로 세우고, 묶음 안의 순서를 곱한다",
         [L("A, B를 한 묶음으로 → 3개를 한 줄로", memo="[AB], C, D"),
          L("3 × 2 × 1 = 6"),
          L("묶음 안에서 AB, BA → 2가지"),
          L("6 × 2 = 12")],
         "12", f.out(), at=("b3", 1))

    # ── 16 순열과 조합 ─────────────────────────────────────────
    f = Fig()
    names = "ABCDE"
    x0, y0, cs = 170, 130, 84
    for i, s in enumerate(names):
        f.text(x0 + cs * i + cs / 2, y0 - 18, s, z=28, c="coral", at="q", b=800)
        f.text(x0 - 26, y0 + cs * i + cs / 2 + 10, s, z=28, c="teal", at="q", b=800)
    f.text(x0 + 2.5 * cs, y0 - 60, "부회장", z=22, c="coral", at="q", b=800)
    f.text(x0 - 26, y0 - 40, "회장", z=22, c="teal", at="q", b=800)
    k = 0
    for i in range(5):
        for j in range(5):
            x, y = x0 + cs * j, y0 + cs * i
            if i == j:
                f.rect(x, y, cs, cs, at="q", c="soft", sw=1.5, f="soft", fo=0.15)
                continue
            f.rect(x, y, cs, cs, at=0, c="ink", sw=1.5, f="teal", fo=0.25, dl=1 + 50 * k)
            f.text(x + cs / 2, y + cs / 2 + 9, names[i] + names[j], z=24, at=0, dl=40 + 50 * k, b=700)
            if i > j:
                f.cross(x + cs / 2, y + cs / 2, s=30, at=1, c="red", dl=40 * k)
            else:
                f.rect(x + 4, y + 4, cs - 8, cs - 8, at=1, c="gold", sw=3, rx=6, dl=40 * k)
            k += 1
    f.text(CX, 600, "20 ÷ 2 = 10", z=36, c="gold", at=1, dl=1300, b=800)
    U.ex("h1-1-16", "5명 중에서 회장 · 부회장을 뽑는 경우와 대표 2명을 뽑는 경우의 수를 비교해 보자.", "역할이 있으면 순열, 그냥 뽑기만 하면 조합 — 순서의 중복을 나눈다",
         [L("회장 · 부회장: 5 × 4 = 20", memo="순서가 있다 — 순열 5P2"),
          L("대표 2명: 20 ÷ 2 = 10", memo="AB와 BA가 같은 뽑기 — 조합 5C2")],
         "20가지, 10가지", f.out(), at=("b3", 2))

    # ── 17 행렬의 성분 ─────────────────────────────────────────
    f = Fig()
    x0, y0, cw, rh = 230, 200, 160, 130
    brackets(f, x0 - 20, y0 - 10, x0 + 2 * cw + 20, y0 + 2 * rh + 10, at="q")
    for j in range(2):
        f.text(x0 + cw * j + cw / 2, y0 - 40, f"j = {j + 1}", z=24, c="coral", at="q", b=800)
    for i in range(2):
        f.text(x0 - 50, y0 + rh * i + rh / 2 + 8, f"i = {i + 1}", z=24, c="teal", at="q", b=800, a="e")
    vals = [[1, 0], [3, 2]]
    for i in range(2):
        for j in range(2):
            cx0, cy0 = x0 + cw * j + cw / 2, y0 + rh * i + rh / 2
            f.text(cx0, cy0 - 10, f"2 × {i + 1} − {j + 1}", z=22, c="soft", at=i, dl=500 * j, b=700)
            f.text(cx0, cy0 + 40, str(vals[i][j]), z=44, c="gold", at=i, dl=500 * j + 400, b=800)
    f.text(CX, 560, "a_{ij} = 2i − j", z=32, at="q", b=800)
    U.ex("h1-1-17", "(i, j) 성분이 a_{ij} = 2i − j인 2 × 2 행렬을 구해 보자.", "i는 행 번호, j는 열 번호 — 칸마다 대입",
         [L("a_{11} = 2 × 1 − 1 = 1, a_{12} = 2 × 1 − 2 = 0", memo="1행"),
          L("a_{21} = 2 × 2 − 1 = 3, a_{22} = 2 × 2 − 2 = 2", memo="2행")],
         "1행 (1, 0), 2행 (3, 2)", f.out(), at=("b3", 1))

    # ── 18 행렬의 곱셈 — 행 × 열 ───────────────────────────────
    f = Fig()
    A = [[1, 2], [3, 4]]
    Bm = [[5, 6], [7, 8]]
    AB = [[19, 22], [43, 50]]

    def mat(x0, y0, M, lab, col="ink", at="q"):
        brackets(f, x0 - 16, y0 - 46, x0 + 116, y0 + 86, at=at)
        for i in range(2):
            for j in range(2):
                f.text(x0 + 25 + 50 * j, y0 + 70 * i, str(M[i][j]), z=34, c=col, at=at, b=700)
        f.text(x0 + 50, y0 - 66, lab, z=28, at=at, b=800)

    mat(60, 160, A, "A")
    mat(260, 160, Bm, "B")
    f.text(410, 195, "=", z=40, at="q", b=700)
    brackets(f, 444, 114, 624, 246, at="q")
    f.text(535, 94, "AB", z=28, at="q", b=800)
    k = 0
    for i in range(2):
        for j in range(2):
            at = k
            f.rect(60 - 6, 160 + 70 * i - 40, 112, 54, at=at, c="teal", sw=3, rx=10, un=at + 1 if k < 3 else None)
            f.rect(260 + 50 * j - 4, 160 - 44, 58, 124, at=at, c="coral", sw=3, rx=10, dl=200, un=at + 1 if k < 3 else None)
            f.text(CX, 380 + 0, f"{A[i][0]} × {Bm[0][j]} + {A[i][1]} × {Bm[1][j]}", z=32, c="ink", at=at, dl=500, b=700, un=at + 1 if k < 3 else None)
            e = f.text(485 + 90 * j, 160 + 70 * i, str(AB[i][j]), z=32, c="gold", at=at, dl=1200, b=800)
            fly(e, CX - (485 + 90 * j), 380 - (160 + 70 * i), dl=40, ms=700)
            k += 1
    f.text(CX, 520, "i행 · j열을 짝지어 곱해 더한다", z=24, c="soft", at=0, dl=1600, b=800)
    U.ex("h1-1-18", "A = (1 2 / 3 4), B = (5 6 / 7 8)일 때 AB를 구해 보자.", "AB의 (i, j) 성분 = A의 i행과 B의 j열을 차례로 곱해 더한 값",
         [L("1 × 5 + 2 × 7 = 19", memo="1행 · 1열"),
          L("1 × 6 + 2 × 8 = 22", memo="1행 · 2열"),
          L("3 × 5 + 4 × 7 = 43", memo="2행 · 1열"),
          L("3 × 6 + 4 × 8 = 50", memo="2행 · 2열")],
         "AB = (19 22 / 43 50)", f.out(), at=("b3", 1))
