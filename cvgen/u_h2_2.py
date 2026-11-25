# 고2 미적분Ⅰ — 함수의 극한과 연속 · 미분 · 적분
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, nl_range, hop


def scr_ang(P, x0, y0, x1, y1):
    """화면에서 (x0, y0) → (x1, y1) 방향의 각(도, 시계 반대 +)"""
    X0, Y0 = P.P(x0, y0)
    X1, Y1 = P.P(x1, y1)
    return math.degrees(math.atan2(-(Y1 - Y0), X1 - X0))


def long_line(P, x0, y0, ang, L=440, at="q", c="ink", w=4, d=False, dl=0, dr=False, back=None):
    """(x0, y0) 를 지나는 길이 L 의 선 — back: 뒤쪽(각의 반대쪽)으로 뻗는 길이(없으면 반반)"""
    X0, Y0 = P.P(x0, y0)
    dx, dy = math.cos(math.radians(ang)), -math.sin(math.radians(ang))
    b = L / 2 if back is None else back
    return P.f.line(X0 - dx * b, Y0 - dy * b, X0 + dx * (L - b), Y0 + dy * (L - b), at=at, c=c, w=w, d=d, dl=dl, dr=dr)


def build(U):
    # ── 01 좌극한과 우극한 ─────────────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 3), (-1, 5), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    f.line(*P.P(-1, 0), *P.P(1, 2), at="q", c="teal", w=4.5)
    f.line(*P.P(1, 3), *P.P(3, 5), at="q", c="coral", w=4.5)
    f.dot(*P.P(1, 2), r=10, f="paper", c="teal", sw=4, at="q")
    f.dot(*P.P(1, 3), r=10, f="coral", at="q")
    d = f.dot(*P.P(-0.6, 0.4), r=12, f="teal", at=0)
    slide(d, 0, dx=P.X(0.93) - P.X(-0.6), dy=P.Y(1.93) - P.Y(0.4), dl=300)
    f.line(*P.P(0, 2), *P.P(1, 2), at=0, c="teal", w=2.5, d=True, dl=1200)
    f.text(P.X(-0.1), P.Y(2) + 8, "2", z=28, c="teal", at=0, dl=1300, b=800, a="e")
    d = f.dot(*P.P(2.6, 4.6), r=12, f="coral", at=1)
    slide(d, 1, dx=P.X(1.07) - P.X(2.6), dy=P.Y(3.07) - P.Y(4.6), dl=300)
    f.line(*P.P(0, 3), *P.P(1, 3), at=1, c="coral", w=2.5, d=True, dl=1200)
    f.text(P.X(-0.1), P.Y(3) + 8, "3", z=28, c="coral", at=1, dl=1300, b=800, a="e")
    f.text(P.X(2), P.Y(1.2), "2 ≠ 3", z=34, c="red", at=2, b=800)
    U.ex("h2-2-01", "x < 1에서 f(x) = x + 1, x ≥ 1에서 f(x) = x + 2일 때, x → 1에서의 극한을 알아보자.", "왼쪽 · 오른쪽에서 다가갈 때의 목적지가 같아야 극한값이 있다",
         [L("lim_{x→1−} f(x) = 2", memo="왼쪽에서 다가가면 2"),
          L("lim_{x→1+} f(x) = 3", memo="오른쪽에서 다가가면 3"),
          L("2 ≠ 3 → 극한값이 없다", memo="좌극한 ≠ 우극한")],
         "극한값이 존재하지 않는다", f.out(), at=("b3", 1))

    # ── 02 0/0 꼴 — 약분 ────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 3), (-1, 4), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    f.line(*P.P(-1, 0), *P.P(3, 4), at="q", c="sky", w=4.5)
    f.dot(*P.P(1, 2), r=11, f="paper", c="sky", sw=4, at="q")
    f.text(P.X(1) + 18, P.Y(2) + 34, "구멍 (x = 1)", z=22, c="sky", at="q", b=800, a="s")
    for k, (x0, col) in enumerate(((-0.6, "teal"), (2.6, "coral"))):
        d = f.dot(*P.P(x0, x0 + 1), r=11, f=col, at=2, dl=200 * k)
        x1 = 0.94 if x0 < 1 else 1.06
        slide(d, 2, dx=P.X(x1) - P.X(x0), dy=P.Y(x1 + 1) - P.Y(x0 + 1), dl=300 + 200 * k)
    f.line(*P.P(0, 2), *P.P(1, 2), at=2, c="gold", w=2.5, d=True, dl=1400)
    f.text(P.X(-0.12), P.Y(2) + 8, "2", z=30, c="gold", at=2, dl=1500, b=800, a="e")
    f.text(P.X(2.2), P.Y(0.6), "y = x + 1 (x ≠ 1)", z=22, c="sky", at=1, b=800)
    U.ex("h2-2-02", "lim_{x→1}{x^{2} − 1/x − 1}의 값을 구해 보자.", "{0/0} 꼴은 인수분해해서 약분 — 구멍 난 직선의 높이",
         [L("x에 1을 넣으면 분모 · 분자가 모두 0", memo="그대로는 넣을 수 없다"),
          L("{x^{2} − 1/x − 1} = {(x − 1)(x + 1)/x − 1} = x + 1", memo="x ≠ 1에서 약분"),
          L("lim_{x→1}(x + 1) = 2", memo="양쪽에서 구멍의 높이 2로")],
         "2", f.out(), at=("b3", 2), ident=True)

    # ── 03 연속 — 구멍 메우기 ──────────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 4), (-1, 7), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    f.line(*P.P(-1, 1), *P.P(4, 6), at="q", c="sky", w=4.5)
    f.dot(*P.P(2, 4), r=11, f="paper", c="sky", sw=4, at="q")
    d = f.dot(*P.P(2, 1), r=12, f="coral", at="q")
    f.text(P.X(2) + 18, P.Y(1) + 10, "f(2) = k", z=22, c="coral", at="q", b=800, a="s", un=2)
    f.text(P.X(2) + 18, P.Y(4) + 40, "극한값 4", z=22, c="sky", at=0, dl=400, b=800, a="s")
    slide(d, 2, dy=P.Y(4) - P.Y(1), dl=300)
    f.text(P.X(2) + 20, P.Y(4) - 16, "k = 4", z=28, c="gold", at=2, dl=1200, b=800, a="s")
    U.ex("h2-2-03", "x ≠ 2에서 f(x) = {x^{2} − 4/x − 2}, f(2) = k인 함수가 x = 2에서 연속이 되도록 k를 정해 보자.", "연속 ⇔ (극한값) = (함숫값) — 구멍을 정확히 메운다",
         [L("lim_{x→2}{x^{2} − 4/x − 2} = lim_{x→2}(x + 2) = 4", memo="구멍의 높이"),
          L("(극한값) = (함숫값)이어야 연속"),
          L("k = 4", memo="점이 구멍으로 올라가 메운다")],
         "4", f.out(), at=("b4", 1))

    # ── 04 사잇값 정리 ─────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-0.5, 1.5), (-1.6, 2.2), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=None, lab_step=1, ystep=1)
    P.curve(lambda x: x ** 3 + x - 1, x0=-0.3, x1=1.3, at="q", c="sky", w=4.5)
    P.pt(0, -1, at=0, f="coral", r=12, label="f(0) = −1", pos="e", z=24, c="coral")
    P.pt(1, 1, at=1, f="teal", r=12, label="f(1) = 1", pos="w", z=24, c="teal")
    c0 = 0.6823
    f.line(*P.P(0, 0), *P.P(1, 0), at=2, c="gold", w=6, dr=True)
    P.pt(c0, 0, at=2, f="gold", r=13, label="c", pos="n", z=28, c="gold", dl=700)
    f.text(P.X(0.5), P.Y(-1.35), "부호가 바뀌면 x축을 꼭 지난다", z=22, c="gold", at=2, dl=1000, b=800)
    U.ex("h2-2-04", "f(x) = x^{3} + x − 1은 0과 1 사이에서 f(c) = 0인 c를 가질까?", "닫힌구간에서 연속이고 양 끝 부호가 다르면 그 사이에 근",
         [L("f(0) = −1 < 0", memo="출발은 x축 아래"),
          L("f(1) = 1 + 1 − 1 = 1 > 0", memo="도착은 x축 위"),
          L("연속이고 부호가 반대 → (0, 1)에 근이 있다", memo="사잇값 정리")],
         "0과 1 사이에 실근이 있다", f.out(), at=("b4", 1))

    # ── 05 미분계수 — 할선이 접선으로 ───────────────────────────
    f = Fig()
    P = Plane(f, (-1, 3.5), (-1, 9.5), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x * x, x0=-1, x1=3.08, at="q", c="sky", w=4.5)
    P.pt(1, 1, at="q", f="ink", r=11, label="(1, 1)", pos="se", z=22)
    a4 = scr_ang(P, 1, 1, 3, 9)
    long_line(P, 1, 1, a4, L=620, back=80, at=0, c="coral", w=3.5)          # (3, 9) 까지 닿는 할선
    P.pt(3, 9, at=0, f="coral", r=10, label="h = 2", pos="w", z=20, c="coral", dl=300)
    for k, hh in enumerate((1, 0.5)):
        a_ = scr_ang(P, 1, 1, 1 + hh, (1 + hh) ** 2)
        long_line(P, 1, 1, a_, L=380, back=80, at=1, c="soft", w=2.5, d=True, dl=600 * k)
        P.pt(1 + hh, (1 + hh) ** 2, at=1, f="soft", r=8, dl=600 * k)
    a2 = scr_ang(P, 1, 1, 2, 3)
    tl = long_line(P, 1, 1, a4, L=520, back=120, at=1, c="gold", w=4.5, dl=1)
    tl["mv"] = {"at": 1, "r": R1(a4 - a2), "cx": R1(P.X(1)), "cy": R1(P.Y(1)), "dl": 1300}
    f.text(P.X(-0.2), P.Y(-0.4), "기울기 2", z=26, c="gold", at=2, b=800)
    U.ex("h2-2-05", "f(x) = x^{2}에서 x = 1에서의 미분계수를 할선의 기울기로 구해 보자.", "h를 0으로 보내면 할선이 접선이 된다 — f'(a) = lim_{h→0}{f(a + h) − f(a)/h}",
         [L("h = 2: 기울기 {9 − 1/2} = 4", memo="(1, 1)과 (3, 9)를 잇는 할선"),
          L("{(1 + h)^{2} − 1/h} = 2 + h", memo="h를 줄이면 할선이 돌아간다"),
          L("f'(1) = 2", memo="h → 0 — 접선의 기울기")],
         "2", f.out(), at=("b3", 2))

    # ── 06 곱의 미분 — 넓이가 늘어나는 두 띠 ─────────────────────
    f = Fig()
    X0, Y0, W, H, dW, dH = 120, 180, 300, 230, 60, 50
    f.rect(X0, Y0 + dH, W, H, at="q", c="ink", sw=3, f="teal", fo=0.3)
    f.text(X0 + W / 2, Y0 + dH + H / 2 + 12, "fg", z=40, c="teal", at="q", b=800)
    f.text(X0 + W / 2, Y0 + dH + H + 40, "f = x^{2} + 1", z=24, at="q", b=800)
    f.text(X0 - 16, Y0 + dH + H / 2 + 8, "g = x − 3", z=24, at="q", b=800, a="e")
    f.rect(X0 + W, Y0 + dH, dW, H, at=0, c="ink", sw=2.5, f="coral", fo=0.45)
    f.text(X0 + W + dW / 2, Y0 + dH + H / 2 + 10, "f'g", z=26, c="coral", at=0, dl=300, b=800)
    f.rect(X0, Y0, W, dH, at=0, c="ink", sw=2.5, f="gold", fo=0.45, dl=600)
    f.text(X0 + W / 2, Y0 + dH / 2 + 10, "fg'", z=26, c="gold", at=0, dl=900, b=800)
    f.rect(X0 + W, Y0, dW, dH, at=0, c="ink", sw=2, f="red", fo=0.3, dl=1200)
    f.text(X0 + W + dW + 14, Y0 + dH / 2 + 8, "→ 0", z=22, c="red", at=0, dl=1400, b=800, a="s")
    f.text(CX, 560, "2x(x − 3) + (x^{2} + 1)", z=30, at=1, b=800)
    f.text(CX, 630, "= 3x^{2} − 6x + 1", z=32, c="gold", at=2, b=800)
    U.ex("h2-2-06", "y = (x^{2} + 1)(x − 3)을 미분해 보자.", "곱의 미분 — 앞 미분 × 뒤 + 앞 × 뒤 미분",
         [L("(fg)' = f'g + fg'", memo="넓이 fg가 늘어날 때 두 띠가 생긴다"),
          L("f' = 2x, g' = 1 → 2x(x − 3) + (x^{2} + 1) × 1"),
          L("2x(x − 3) + (x^{2} + 1) = 3x^{2} − 6x + 1")],
         "3x^{2} − 6x + 1", f.out(), at=("b3", 1), ident=True)

    # ── 07 접선의 방정식 ───────────────────────────────────────
    f = Fig()
    P = Plane(f, (-2, 3), (-2, 6), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x * x, x0=-2, x1=2.4, at="q", c="sky", w=4.5)
    P.pt(1, 1, at="q", f="ink", r=11, label="(1, 1)", pos="w", z=22)
    f.line(*P.P(1, 1), *P.P(2, 1), at=0, c="gold", w=5, ar=1, dr=True)
    f.line(*P.P(2, 1), *P.P(2, 3), at=0, c="coral", w=5, ar=1, dr=True, dl=600)
    f.text(P.X(1.5), P.Y(1) + 30, "1", z=24, c="gold", at=0, dl=300, b=800)
    f.text(P.X(2) + 14, P.Y(2) + 8, "2", z=24, c="coral", at=0, dl=900, b=800, a="s")
    P.lineq(2, -1, at=1, c="coral", w=4.5)
    P.pt(0, -1, at=2, f="gold", r=11, label="(0, −1)", pos="e", z=22, c="gold")
    f.text(P.X(2.6), P.Y(5.6), "y = 2x − 1", z=24, c="coral", at=2, dl=300, b=800)
    U.ex("h2-2-07", "곡선 y = x^{2} 위의 점 (1, 1)에서의 접선의 방정식을 구해 보자.", "접점과 그 점의 미분계수 — y − f(a) = f'(a)(x − a)",
         [L("f'(x) = 2x → f'(1) = 2", memo="접선의 기울기"),
          L("y − 1 = 2(x − 1)", memo="점 (1, 1)을 지나고 기울기 2"),
          L("y = 2x − 1")],
         "y = 2x − 1", f.out(), at=("b3", 1))

    # ── 08 평균값 정리 — 할선과 평행한 접선 ─────────────────────
    f = Fig()
    P = Plane(f, (-1, 3), (-2, 5), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x * x, x0=-1, x1=2.2, at="q", c="sky", w=4.5)
    P.pt(0, 0, at="q", f="ink", r=10)
    P.pt(2, 4, at="q", f="ink", r=10, label="(2, 4)", pos="w", z=22)
    f.line(*P.P(0, 0), *P.P(2, 4), at=0, c="coral", w=4, dr=True)
    f.text(P.X(1.5), P.Y(3.9), "기울기 2", z=22, c="coral", at=0, dl=700, b=800, a="e")
    sl = P.lineq(2, 0, at=1, c="gold", w=4, d=True, dr=False)
    slide(sl, 1, dy=P.Y(-1) - P.Y(0), dl=300)
    P.pt(1, 1, at=2, f="gold", r=12, label="c = 1", pos="e", z=26, c="gold")
    U.ex("h2-2-08", "f(x) = x^{2}에 대해 구간 [0, 2]에서 평균값 정리를 만족하는 c를 구해 보자.", "양 끝을 잇는 할선과 평행한 접선이 구간 안 어딘가에 있다",
         [L("평균변화율 = {4 − 0/2 − 0} = 2", memo="할선의 기울기"),
          L("f'(c) = 2c = 2", memo="할선을 평행하게 내려 접하는 곳"),
          L("c = 1", memo="0 < 1 < 2 — 구간 안")],
         "c = 1", f.out(), at=("b4", 1))

    # ── 09 증감과 극값 ─────────────────────────────────────────
    f = Fig()
    f.line(80, 110, 600, 110, at=0, c="ink", w=3, ar=1)
    xs = {-1: 250, 1: 430}
    for v, x in xs.items():
        f.line(x, 98, x, 122, at=0, c="ink", w=3)
        f.text(x, 152, str(v) if v > 0 else "−1", z=24, at=0, b=800)
    for (x, s, col) in ((160, "+", "teal"), (340, "−", "coral"), (520, "+", "teal")):
        f.text(x, 96, s, z=36, c=col, at=0, dl=500, b=800)
    f.text(70, 96, "f'", z=26, at=0, b=800, a="e")
    P = Plane(f, (-2.3, 2.3), (-3, 3), box=(80, 190, 600, 660), square=False)
    P.axes(at="q", grid=None, lab_step=1, ystep=1)
    P.curve(lambda x: x ** 3 - 3 * x, x0=-2.2, x1=2.2, at="q", c="sky", w=4.5)
    for (a, b, col) in ((-2.2, -1, "teal"), (-1, 1, "coral"), (1, 2.2, "teal")):
        P.curve(lambda x: x ** 3 - 3 * x, x0=a, x1=b, at=1 if col == "teal" and a < 0 else (1 if col == "coral" else 2), c=col, w=6)
    f.line(*P.P(-1.6, 2), *P.P(-0.4, 2), at=1, c="gold", w=3, dl=800)
    P.pt(-1, 2, at=1, f="gold", r=11, label="극대 2", pos="n", z=24, c="gold", dl=1000)
    f.line(*P.P(0.4, -2), *P.P(1.6, -2), at=2, c="gold", w=3, dl=300)
    P.pt(1, -2, at=2, f="gold", r=11, label="극소 −2", pos="s", z=24, c="gold", dl=500)
    U.ex("h2-2-09", "f(x) = x^{3} − 3x의 증가와 감소를 조사하고 극값을 구해 보자.", "f'(x)의 부호 — +이면 증가, −이면 감소, 바뀌는 곳이 극",
         [L("f'(x) = 3x^{2} − 3 = 3(x + 1)(x − 1)", memo="−1, 1에서 0"),
          L("x = −1에서 + → −: 극대", memo="f(−1) = 2"),
          L("x = 1에서 − → +: 극소", memo="f(1) = −2")],
         "극댓값 2, 극솟값 −2", f.out(), at=("b4", 1), ident=True)

    # ── 10 삼차함수가 극값을 가질 조건 ───────────────────────────
    f = Fig()
    P = Plane(f, (-2.5, 2.5), (-4, 4), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x ** 3 + x, x0=-1.5, x1=1.5, at=0, c="teal", w=4)
    f.text(P.X(1.6), P.Y(3.6), "a = 1: 극값 없음", z=22, c="teal", at=0, dl=900, b=800, a="s")
    P.curve(lambda x: x ** 3 - 3 * x, x0=-2.2, x1=2.2, at=1, c="coral", w=4.5)
    P.pt(-1, 2, at=1, f="coral", r=10, dl=1000)
    P.pt(1, -2, at=1, f="coral", r=10, dl=1100)
    f.text(P.X(-2.4), P.Y(3.2), "a = −3: 극대 · 극소", z=22, c="coral", at=1, dl=1200, b=800, a="s")
    f.text(P.X(1.2), P.Y(-3.4), "a < 0", z=36, c="gold", at=2, b=800)
    U.ex("h2-2-10", "f(x) = x^{3} + ax가 극값을 갖도록 하는 a의 값의 범위를 구해 보자.", "극값이 있다 ⇔ f'(x) = 0이 서로 다른 두 실근",
         [L("f'(x) = 3x^{2} + a"),
          L("3x^{2} + a = 0이 서로 다른 두 실근", memo="판별식 −12a > 0"),
          L("a < 0", memo="a = 1이면 계속 증가, a = −3이면 굴곡")],
         "a < 0", f.out(), at=("b4", 1))

    # ── 11 실근의 개수 — 수평선 내리기 ──────────────────────────
    f = Fig()
    P = Plane(f, (-2.5, 2.5), (-3.5, 3.5), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x ** 3 - 3 * x, x0=-2.3, x1=2.3, at="q", c="sky", w=4.5)
    P.lineq(0, 3, at="q", c="lilac", w=3.5)
    P.pt(2.1038, 3, at="q", f="lilac", r=9)
    f.text(P.X(-2.3), P.Y(3) - 14, "k = 3: 한 점", z=22, c="lilac", at="q", b=800, a="s")
    h1 = P.lineq(0, 3, at=1, c="coral", w=4, dr=False)
    slide(h1, 1, dy=P.Y(0) - P.Y(3), dl=200)
    for k, xv in enumerate((-math.sqrt(3), 0, math.sqrt(3))):
        P.pt(xv, 0, at=1, f="coral", r=10, dl=1200 + 150 * k)
    f.text(P.X(-2.3), P.Y(0) - 14, "k = 0: 세 점", z=22, c="coral", at=1, dl=1300, b=800, a="s")
    h2 = P.lineq(0, 0, at=2, c="gold", w=4, dr=False)
    slide(h2, 2, dy=P.Y(-2) - P.Y(0), dl=200)
    P.pt(1, -2, at=2, f="gold", r=10, dl=1200)
    P.pt(-2, -2, at=2, f="gold", r=10, dl=1300)
    f.text(P.X(-2.3), P.Y(-2) + 30, "k = −2: 두 점", z=22, c="gold", at=2, dl=1400, b=800, a="s")
    U.ex("h2-2-11", "방정식 x^{3} − 3x = k의 실근의 개수를 k의 값에 따라 알아보자.", "y = x^{3} − 3x와 수평선 y = k의 교점 — k를 위아래로 움직이며 센다",
         [L("극댓값 2, 극솟값 −2", memo="x = −1, x = 1"),
          L("−2 < k < 2 → 세 점", memo="서로 다른 세 실근"),
          L("k = ±2 → 두 점, |k| > 2 → 한 점")],
         "−2 < k < 2일 때 서로 다른 세 실근", f.out(), at=("b2", 2))

    # ── 12 속도 — 방향 바꾸기 ───────────────────────────────────
    f = Fig()
    nl = NL(f, -5, 1, y=220, x0=60, x1=600, step=1, lab_step=1, z=22)
    d = f.dot(nl.X(0), 220, r=13, f="coral", at=1)
    slide(d, 1, dx=nl.X(-4) - nl.X(0), dl=200)
    f.line(nl.X(-0.2), 170, nl.X(-3.8), 170, at=1, c="coral", w=3.5, ar=1, dr=True, dl=200)
    f.text(nl.X(-2), 150, "t: 0 → 2", z=22, c="coral", at=1, dl=600, b=800)
    d2 = f.dot(nl.X(-4), 220, r=13, f="teal", at=2)
    slide(d2, 2, dx=nl.X(0) - nl.X(-4), dl=600)
    f.line(nl.X(-3.8), 120, nl.X(-0.2), 120, at=2, c="teal", w=3.5, ar=1, dr=True, dl=600)
    f.text(nl.X(-2), 100, "t: 2 → 3", z=22, c="teal", at=2, dl=900, b=800)
    f.circ(nl.X(-4), 220, 24, at=2, c="gold", sw=4)
    P = Plane(f, (-0.3, 3.3), (-4, 9), box=(80, 330, 600, 660), square=False)
    P.axes(at=0, grid=None, lab_step=1, xn="t", yn="v")
    P.curve(lambda t: 3 * t * t - 6 * t, x0=0, x1=3.2, at=0, c="sky", w=4)
    f.poly([P.P(0, 0)] + [P.P(t / 10, 3 * (t / 10) ** 2 - 6 * t / 10) for t in range(0, 21)] + [P.P(2, 0)], at=1, c="none", f="coral", fo=0.3)
    P.pt(2, 0, at=2, f="gold", r=11, label="v = 0", pos="n", z=22, c="gold")
    U.ex("h2-2-12", "수직선 위를 움직이는 점의 위치가 x = t^{3} − 3t^{2}일 때, 운동 방향이 바뀌는 시각을 구해 보자.", "속도 v = x' — v의 부호가 바뀌는 순간 방향이 바뀐다",
         [L("v(t) = 3t^{2} − 6t = 3t(t − 2)", memo="위치를 미분"),
          L("0 < t < 2: v < 0 → 음의 방향", memo="t = 2에서 x = −4까지"),
          L("t = 2: v = 0, 부호가 − → +", memo="멈췄다가 돌아선다")],
         "t = 2", f.out(), at=("b4", 1))

    # ── 13 부정적분 — 적분상수 고르기 ───────────────────────────
    f = Fig()
    P = Plane(f, (-2, 2.5), (-2, 9), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=1, lab_step=1)
    for k, C in enumerate((-1, 0, 1, 2, 3)):
        P.curve(lambda x, C=C: 3 * x * x + C, x0=-1.9, x1=1.9, at=0, c="soft", w=2.5, d=C != 2)
    P.pt(1, 5, at=1, f="gold", r=12, label="(1, 5)", pos="e", z=24, c="gold")
    P.curve(lambda x: 3 * x * x + 2, x0=-1.7, x1=1.7, at=2, c="coral", w=5)
    f.text(P.X(-1.9), P.Y(7.4), "C = 2", z=26, c="coral", at=2, dl=600, b=800, a="s")
    U.ex("h2-2-13", "f'(x) = 6x이고 f(1) = 5인 함수 f(x)를 구해 보자.", "부정적분은 위아래로 평행한 곡선 묶음 — 지나는 점 하나로 C가 정해진다",
         [L("f(x) = ∫6x dx = 3x^{2} + C", memo="적분상수 C만큼 위아래로"),
          L("f(1) = 3 + C = 5", memo="점 (1, 5)를 지나는 것"),
          L("C = 2 → f(x) = 3x^{2} + 2")],
         "f(x) = 3x^{2} + 2", f.out(), at=("b4", 1))

    # ── 14 정적분 ──────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-0.5, 4), (-1, 7), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.lineq(2, -1, at="q", c="sky", w=4.5)
    f.poly([P.P(1, 0), P.P(1, 1), P.P(3, 5), P.P(3, 0)], at=1, c="ink", w=2.5, f="gold", fo=0.4, dr=True)
    f.text(P.X(1) - 14, P.Y(0.5) + 8, "1", z=24, c="gold", at=1, dl=600, b=800, a="e")
    f.text(P.X(3) + 14, P.Y(2.5) + 8, "5", z=24, c="gold", at=1, dl=700, b=800, a="s")
    f.text(P.X(2), P.Y(1.4), "6", z=40, c="ink", at=2, b=800)
    f.text(P.X(1.6), P.Y(6.4), "[x^{2} − x]_{1}^{3}", z=26, c="coral", at=0, b=800)
    U.ex("h2-2-14", "∫_{1}^{3}(2x − 1)dx의 값을 구해 보자.", "부정적분 F를 구해 위끝 − 아래끝 — 그래프가 x축 위면 넓이",
         [L("F(x) = x^{2} − x", memo="(x^{2} − x)' = 2x − 1"),
          L("F(3) − F(1) = (9 − 3) − (1 − 1) = 6"),
          L("넓이 = {1 + 5/2} × 2 = 6", memo="사다리꼴로 확인")],
         "6", f.out(), at=("b4", 1))

    # ── 15 두 곡선 사이의 넓이 ─────────────────────────────────
    f = Fig()
    P = Plane(f, (-0.2, 1.4), (-0.2, 1.4), box=(60, 50, 620, 610))
    f.line(P.X(-0.2), P.Y(0), P.X(1.4), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(-0.2), P.X(0), P.Y(1.4), at="q", c="ink", w=3, ar=1)
    f.text(P.X(1), P.Y(0) + 30, "1", z=22, c="soft", at="q")
    f.text(P.X(0) - 12, P.Y(1) + 8, "1", z=22, c="soft", at="q", a="e")
    P.curve(lambda x: x * x, x0=-0.2, x1=1.18, at="q", c="sky", w=4.5)
    P.lineq(1, 0, at="q", c="coral", w=4.5)
    f.text(P.X(1.2), P.Y(1.38), "y = x^{2}", z=22, c="sky", at="q", b=800, a="e")
    f.text(P.X(1.3), P.Y(1.15), "y = x", z=22, c="coral", at="q", b=800, a="s")
    P.pt(0, 0, at=0, f="gold", r=10)
    P.pt(1, 1, at=0, f="gold", r=10, label="(1, 1)", pos="e", z=22, c="gold", dl=300)
    n = 10
    for k in range(n):
        x = (k + 0.5) / n
        f.rect(P.X(k / n) + 2, P.Y(x), (P.X(1 / n) - P.X(0)) - 4, P.Y(x * x) - P.Y(x), at=1, c="none", f="gold", fo=0.55, dl=1 + 120 * k)
    f.text(P.X(0.75), P.Y(0.25), "{1/6}", z=40, c="gold", at=2, b=800)
    U.ex("h2-2-15", "곡선 y = x^{2}과 직선 y = x로 둘러싸인 부분의 넓이를 구해 보자.", "교점 사이에서 (위) − (아래)를 적분",
         [L("x^{2} = x → x = 0, 1", memo="교점"),
          L("0 < x < 1에서 x ≥ x^{2}", memo="직선이 위 — 세로 띠 높이 x − x^{2}"),
          L("∫_{0}^{1}(x − x^{2})dx = {1/2} − {1/3} = {1/6}")],
         "{1/6}", f.out(), at=("b4", 1))
