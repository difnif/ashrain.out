# 고1 공통수학2 — 도형의 방정식 · 집합과 명제 · 함수
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, nl_range, hop, travel, venn2, tree


def chipm(f, x, y, s, at, c="teal", z=32, dl=0, un=None, fo=0.16):
    w = max(z * 1.25, tw(s, z) + z * 0.6)
    r = f.rect(x - w / 2, y - z * 0.98, w, z * 1.4, c=c, sw=3, rx=z * 0.42, f=c, fo=fo, at=at, dl=dl, un=un)
    t = f.text(x, y, s, z=z, c=c, at=at, dl=dl + 60, un=un, b=800)
    return [r, t]


def build(U):
    # ── 01 내분점 ──────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (0, 8), (0, 5), box=(60, 80, 620, 600))
    P.axes(at="q", grid=1, lab_step=1)
    A, B = (1, 1), (7, 4)
    f.line(*P.P(*A), *P.P(*B), at="q", c="ink", w=4)
    P.pt(*A, at="q", f="ink", r=10, label="A(1, 1)", pos="se", z=22)
    P.pt(*B, at="q", f="ink", r=10, label="B(7, 4)", pos="nw", z=22)
    for t in (1 / 3, 2 / 3):
        x, y = A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t
        P.pt(x, y, at=0, f="soft", r=7, dl=300)
    d = f.dot(*P.P(*A), r=13, f="coral", at=0, dl=500)
    slide(d, 0, dx=P.X(5) - P.X(1), dy=P.Y(3) - P.Y(1), dl=800)
    f.text(P.X(5) - 10, P.Y(3) - 22, "P", z=28, c="coral", at=0, dl=1700, b=800, a="e")
    f.text(P.X(3), P.Y(2) - 30, "2", z=24, c="teal", at=0, dl=1900, b=800)
    f.text(P.X(6), P.Y(3.5) - 30, "1", z=24, c="gold", at=0, dl=2000, b=800)
    f.line(P.X(1), P.Y(0) - 14, P.X(5), P.Y(0) - 14, at=1, c="teal", w=6, dr=True)
    f.line(P.X(5), P.Y(0) - 14, P.X(7), P.Y(0) - 14, at=1, c="gold", w=6, dr=True, dl=400)
    f.line(*P.P(5, 0), *P.P(5, 3), at=1, c="coral", w=2.5, d=True, dl=600)
    f.text(P.X(5), P.Y(0) + 60, "x = 5", z=24, c="coral", at=1, dl=800, b=800)
    f.line(P.X(0) + 14, P.Y(1), P.X(0) + 14, P.Y(3), at=2, c="teal", w=6, dr=True)
    f.line(P.X(0) + 14, P.Y(3), P.X(0) + 14, P.Y(4), at=2, c="gold", w=6, dr=True, dl=400)
    f.line(*P.P(0, 3), *P.P(5, 3), at=2, c="coral", w=2.5, d=True, dl=600)
    f.text(P.X(0) + 56, P.Y(3) - 10, "y = 3", z=24, c="coral", at=2, dl=800, b=800, a="s")
    U.ex("h1-2-01", "두 점 A(1, 1), B(7, 4)를 잇는 선분 AB를 2 : 1로 내분하는 점 P의 좌표를 구해 보자.", "AB를 3칸으로 나눠 A에서 2칸 — x좌표, y좌표도 각각 2 : 1로",
         [L("AB를 3칸으로 — A에서 2칸, B에서 1칸"),
          L("x = {2 × 7 + 1 × 1/3} = 5", memo="1과 7 사이를 2 : 1로"),
          L("y = {2 × 4 + 1 × 1/3} = 3", memo="1과 4 사이를 2 : 1로")],
         "P(5, 3)", f.out(), at=("b3", 2))

    # ── 02 수직인 두 직선 — 90° 돌리기 ──────────────────────────
    f = Fig()
    P = Plane(f, (-4, 4), (-4, 4), box=(60, 50, 620, 610))
    P.axes(at="q", grid=1, lab_step=1)
    O = P.P(0, 0)
    els = [P.lineq(2, 0, at="q", c="teal", w=4.5, dr=False)]
    f.text(P.X(1.9), P.Y(3.9), "기울기 2", z=22, c="teal", at="q", b=800, a="e")
    els.append(f.line(*O, *P.P(1, 0), at=0, c="gold", w=5, ar=1, dr=True))
    els.append(f.line(*P.P(1, 0), *P.P(1, 2), at=0, c="coral", w=5, ar=1, dr=True, dl=600))
    f.text(P.X(0.5), P.Y(0) + 32, "1", z=24, c="gold", at=0, dl=400, b=800)
    f.text(P.X(1) + 16, P.Y(1) + 8, "2", z=24, c="coral", at=0, dl=1000, b=800, a="s")
    for el in els:
        cp = f.line(el["x"], el["y"], el["x2"], el["y2"], at=1, c=el.get("c", "ink"), w=el.get("sw", 3), ar=el.get("ar", 0))
        cp["mv"] = {"at": 1, "r": -90, "cx": R1(O[0]), "cy": R1(O[1]), "dl": 300}
    f.text(P.X(-1), P.Y(1) - 34, "2", z=24, c="gold", at=1, dl=1300, b=800)
    f.text(P.X(-2) - 16, P.Y(0.5) + 8, "1", z=24, c="coral", at=1, dl=1400, b=800, a="e")
    f.text(P.X(-3.9), P.Y(2.4), "기울기 −{1/2}", z=22, c="teal", at=1, dl=1500, b=800, a="s")
    angle_mark(f, O, P.P(1, 2), P.P(-2, 1), r=26, at=2, c="ink")
    U.ex("h1-2-02", "기울기가 2인 직선에 수직인 직선의 기울기를 구해 보자.", "직선을 90° 돌리면 가로 · 세로가 맞바뀌고 부호 하나가 바뀐다",
         [L("기울기 2: 오른쪽 1, 위로 2"),
          L("90° 돌리면 왼쪽 2, 위로 1 → 기울기 −{1/2}", memo="가로와 세로가 바뀐다"),
          L("2 × (−{1/2}) = −1", memo="수직 ⇔ 기울기의 곱이 −1")],
         "−{1/2}", f.out(), at=("b3", 2))

    # ── 03 평행한 두 직선 사이의 거리 ───────────────────────────
    f = Fig()
    P = Plane(f, (-2, 4), (-5, 3), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.lineq(-2, -1, at="q", c="teal", w=4)
    P.lineq(-2, 4, at="q", c="coral", w=4)
    f.text(P.X(-1.9), P.Y(2.6), "2x + y + 1 = 0", z=20, c="teal", at="q", b=800, a="s")
    f.text(P.X(1.0), P.Y(2.6), "2x + y − 4 = 0", z=20, c="coral", at="q", b=800, a="s")
    P.pt(0, -1, at=0, f="teal", r=11, label="(0, −1)", pos="w", z=22, c="teal")
    f.line(*P.P(0, -1), *P.P(2, 0), at=1, c="gold", w=4, d=True, dr=True)
    d = f.dot(*P.P(0, -1), r=10, f="gold", at=1, dl=200)
    slide(d, 1, dx=P.X(2) - P.X(0), dy=P.Y(0) - P.Y(-1), dl=300)
    angle_mark(f, P.P(2, 0), P.P(0, -1), P.P(3, -2), r=20, at=1, c="ink", dl=1200)
    f.text(P.X(1) + 16, P.Y(-0.5) + 30, "d", z=28, c="gold", at=1, dl=1300, b=800, a="s")
    f.text(P.X(2.2), P.Y(-3.6), "d = √{5}", z=34, c="gold", at=2, b=800)
    U.ex("h1-2-03", "평행한 두 직선 2x + y + 1 = 0, 2x + y − 4 = 0 사이의 거리를 구해 보자.", "한 직선 위의 점 하나에서 다른 직선까지의 거리",
         [L("2x + y + 1 = 0 위의 점 (0, −1)", memo="x = 0을 넣어 점 하나"),
          L("d = {|0 − 1 − 4|/√{2^{2} + 1^{2}}}", memo="점과 직선 사이의 거리 공식"),
          L("{5/√{5}} = √{5}")],
         "√{5}", f.out(), at=("b4", 1))

    # ── 04 원의 방정식 — 완전제곱식 ─────────────────────────────
    f = Fig()
    S = Strip(f, y=100, z=34)
    S.row("q", ["x^{2} + y^{2} − 4x + 6y + 4 = 0"], keep=True)
    S.row(0, [{"s": "(x^{2} − 4x + 4)", "c": "teal"}, "+", {"s": "(y^{2} + 6y + 9)", "c": "coral"}, "=", {"s": "−4 + 4 + 9", "g": 0.3}], y=180, keep=True, z=30)
    S.row(1, [{"s": "(x − 2)^{2}", "frm": 0, "c": "teal"}, {"s": "+", "frm": 1}, {"s": "(y + 3)^{2}", "frm": 2, "c": "coral"}, {"s": "=", "frm": 3}, {"s": "9", "frm": 4, "c": "gold"}], y=260, keep=True, z=36)
    P = Plane(f, (-2, 6), (-7, 1), box=(120, 300, 560, 670))
    P.axes(at=2, grid=1, lab_step=1)
    C = P.P(2, -3)
    f.dot(*C, r=11, f="gold", at=2, dl=300)
    f.text(C[0] - 14, C[1] - 16, "(2, −3)", z=20, c="gold", at=2, dl=400, b=800, a="e")
    f.circ(*C, 3 * P.sx, at=2, c="sky", sw=4, dl=700)
    f.line(*C, C[0] + 3 * P.sx, C[1], at=2, c="coral", w=4, dr=True, dl=1400)
    f.text(C[0] + 1.5 * P.sx, C[1] - 12, "3", z=24, c="coral", at=2, dl=1700, b=800)
    U.ex("h1-2-04", "x^{2} + y^{2} − 4x + 6y + 4 = 0이 나타내는 원의 중심과 반지름을 구해 보자.", "x끼리, y끼리 완전제곱식으로 묶는다",
         [L("(x^{2} − 4x + 4) + (y^{2} + 6y + 9) = −4 + 4 + 9", memo="양변에 4와 9를 더한다"),
          L("(x − 2)^{2} + (y + 3)^{2} = 9", memo="(x − a)^{2} + (y − b)^{2} = r^{2}"),
          L("중심 (2, −3), 반지름 3")],
         "중심 (2, −3), 반지름 3", f.out(), at=("b3", 1))

    # ── 05 원과 직선 — 중심까지의 거리 ──────────────────────────
    f = Fig()
    P = Plane(f, (-4, 6), (-3, 6), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    O = P.P(0, 0)
    r5 = math.sqrt(5)
    f.circ(*O, r5 * P.sx, at="q", c="sky", sw=4)

    def kline(k, at, c, dl=0, d=False):
        return P.lineq(-0.5, k / 2, at=at, c=c, w=4, d=d, dr=False)

    kline(9, "q", "lilac")
    f.line(*O, *P.P(9 / 5, 18 / 5), at=0, c="lilac", w=3, ar=1, dr=True)
    f.text(P.X(2.6), P.Y(4.4), "d > r", z=26, c="lilac", at=0, dl=800, b=800, a="s")
    g1 = kline(9, 1, "gold")
    slide(g1, 1, dx=P.X(-0.8) - P.X(0), dy=P.Y(-1.6) - P.Y(0), dl=200)
    f.line(*O, *P.P(1, 2), at=1, c="gold", w=3, ar=1, dr=True, dl=1100)
    P.pt(1, 2, at=1, f="gold", r=10, label="접점 (1, 2)", pos="e", z=20, c="gold", dl=1300)
    g2 = kline(5, 2, "coral")
    slide(g2, 2, dx=P.X(-0.6) - P.X(0), dy=P.Y(-1.2) - P.Y(0), dl=200)
    f.line(*O, *P.P(0.4, 0.8), at=2, c="coral", w=3, ar=1, dr=True, dl=1100)
    f.text(P.X(-3.8), P.Y(-2.4), "d < r: 두 점", z=24, c="coral", at=2, dl=1300, b=800, a="s")
    U.ex("h1-2-05", "원 x^{2} + y^{2} = 5와 직선 x + 2y = k가 어떻게 만나는지 중심에서 직선까지의 거리 d로 알아보자.", "d와 반지름 r = √{5}를 비교 — d > r 만나지 않음 · d = r 접함 · d < r 두 점",
         [L("k = 9: d = {9/√{5}} > √{5}", memo="만나지 않는다"),
          L("k = 5: d = {5/√{5}} = √{5}", memo="접한다 — 접점 (1, 2)"),
          L("k = 2: d = {2/√{5}} < √{5}", memo="두 점에서 만난다")],
         "d와 r의 크기로 판정", f.out(), at=("b2", 2))

    # ── 06 평행이동 ────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-2, 5), (-1, 7), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x * x, x0=-2.5, x1=2.5, at="q", c="soft", w=3.5)
    f.text(P.X(-1.9), P.Y(5.4), "y = x^{2}", z=22, c="soft", at="q", b=800, a="e")
    cv = P.curve(lambda x: x * x, x0=-2.3, x1=2.3, at=0, c="sky", w=4.5, dr=False)
    slides(cv, 0, dx=P.X(2) - P.X(0), dy=P.Y(1) - P.Y(0), dl=200)
    f.line(*P.P(0, 0), *P.P(2, 1), at=0, c="gold", w=3.5, ar=1, dr=True, dl=200)
    f.text(P.X(4.3), P.Y(6.4), "y − 1 = (x − 2)^{2}", z=22, c="sky", at=1, b=800)
    P.pt(3, 2, at=2, f="coral", r=11, label="(3, 2)", pos="e", z=22, c="coral")
    f.line(*P.P(3, 2), *P.P(1, 1), at=2, c="coral", w=3, d=True, ar=1, dr=True, dl=500)
    P.pt(1, 1, at=2, f="coral", r=9, label="(1, 1)", pos="w", z=22, c="coral", dl=1200)
    U.ex("h1-2-06", "y = x^{2}의 그래프를 x축 방향으로 2, y축 방향으로 1만큼 평행이동한 그래프의 식을 구해 보자.", "점은 (x + 2, y + 1)로, 식에서는 x → x − 2, y → y − 1",
         [L("점 (x, y) → (x + 2, y + 1)", memo="점은 그대로 더한다"),
          L("y − 1 = (x − 2)^{2}", memo="식에서는 반대로 뺀다"),
          L("새 점 (3, 2) → 되돌리면 (1, 1)", memo="원래 그래프 y = x^{2} 위의 점")],
         "y = (x − 2)^{2} + 1", f.out(), at=("b3", 1))

    # ── 07 대칭이동 ────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-5, 5), (-3, 5), box=(60, 50, 620, 610))
    P.axes(at="q", grid=1, lab_step=1)
    P.pt(4, 1, at="q", f="ink", r=11, label="(4, 1)", pos="ne", z=22)
    for k, ((x, y), col, lab, pos) in enumerate((((4, -1), "teal", "(4, −1)", "se"), ((-4, 1), "coral", "(−4, 1)", "nw"), ((1, 4), "gold", "(1, 4)", "ne"))):
        if k == 2:
            P.lineq(1, 0, at=2, c="soft", w=3, d=True)
            f.text(P.X(4.6), P.Y(4.9), "y = x", z=22, c="soft", at=2, b=800)
        d = f.dot(*P.P(4, 1), r=11, f=col, at=k, dl=300 if k == 2 else 0)
        slide(d, k, dx=P.X(x) - P.X(4), dy=P.Y(y) - P.Y(1), dl=600 if k == 2 else 200)
        f.line(*P.P(4, 1), *P.P(x, y), at=k, c=col, w=2.5, d=True, dr=True, dl=600 if k == 2 else 200)
        P.pt(x, y, at=k, f=col, r=1, label=lab, pos=pos, z=22, c=col, dl=1300 if k == 2 else 1000)
    angle_mark(f, P.P(2.5, 2.5), P.P(4, 1), P.P(5, 5), r=18, at=2, c="ink", dl=1500)
    U.ex("h1-2-07", "점 (4, 1)을 x축, y축, 직선 y = x에 대하여 대칭이동한 점을 구해 보자.", "축 대칭은 다른 쪽 좌표의 부호가, y = x 대칭은 두 좌표의 자리가 바뀐다",
         [L("x축 대칭: (4, 1) → (4, −1)", memo="y만 부호가 바뀐다"),
          L("y축 대칭: (4, 1) → (−4, 1)", memo="x만 부호가 바뀐다"),
          L("직선 y = x 대칭: (4, 1) → (1, 4)", memo="두 좌표를 맞바꾼다")],
         "(4, −1), (−4, 1), (1, 4)", f.out(), at=("b2", 2))

    # ── 08 집합의 표현 ─────────────────────────────────────────
    f = Fig()
    primes = (2, 3, 5, 7)
    xs = [60 + 60 * k for k in range(10)]
    for k in range(10):
        n = k + 1
        f.rect(xs[k] - 26, 100, 52, 60, at="q", c="ink", sw=2.5, rx=8)
        f.text(xs[k], 142, str(n), z=28, at="q", b=700)
        if n not in primes:
            f.cross(xs[k], 130, s=22, at=0, c="soft", dl=120 * k)
        else:
            f.rect(xs[k] - 26, 100, 52, 60, at=0, c="coral", sw=4, rx=8, f="coral", fo=0.2, dl=120 * k)
    f.poly([(330 + 220 * math.cos(math.radians(a)), 420 - 130 * math.sin(math.radians(a))) for a in range(0, 361, 10)], at=1, c="teal", w=4)
    f.text(130, 320, "A", z=34, c="teal", at=1, b=800)
    for j, n in enumerate(primes):
        e = f.text(220 + 75 * j, 435, str(n), z=40, c="coral", at=1, dl=300 + 250 * j, b=800)
        fly(e, xs[n - 1] - (220 + 75 * j), 142 - 435, dl=40, ms=700)
    f.text(CX, 620, "n(A) = 4", z=36, c="gold", at=2, b=800)
    U.ex("h1-2-08", "10 이하의 소수의 집합 A를 원소나열법으로 나타내고 n(A)를 구해 보자.", "조건에 맞는 원소를 골라 { } 안에 나열 — 개수는 n(A)",
         [L("1부터 10까지에서 소수 고르기", memo="1은 소수가 아니다"),
          L("A = {2, 3, 5, 7}", memo="원소나열법"),
          L("n(A) = 4", memo="원소의 개수")],
         "A = {2, 3, 5, 7}, n(A) = 4", f.out(), at=("b3", 1))

    # ── 09 부분집합의 개수 ──────────────────────────────────────
    f = Fig()
    pos = tree(f, [["a ○", "a ×"], ["b ○", "b ×"], ["c ○", "c ×"]], x0=40, x1=620, y0=110, dy=140, at_levels=["q", 0, 0], z=22)
    leaves = ["{a, b, c}", "{a, b}", "{a, c}", "{a}", "{b, c}", "{b}", "{c}", "∅"]
    for k, (x, y) in enumerate(pos[-1]):
        f.text(x, y + 80, leaves[k], z=20, c="teal", at=1, dl=150 * k, b=800)
    f.text(CX, 620, "2 × 2 × 2 = 8", z=34, c="gold", at=1, dl=1400, b=800)
    f.cross(pos[-1][0][0], pos[-1][0][1] + 70, s=40, at=2, c="red")
    f.text(CX, 670, "자기 자신 빼면 7", z=24, c="red", at=2, dl=300, b=800)
    U.ex("h1-2-09", "집합 {a, b, c}의 부분집합의 개수와 진부분집합의 개수를 구해 보자.", "원소마다 넣는다 · 뺀다 두 가지 — 곱의 법칙",
         [L("원소마다 ○ · × 2가지", memo="a, b, c 각각"),
          L("2 × 2 × 2 = 8", memo="부분집합 2^{3}개"),
          L("8 − 1 = 7", memo="진부분집합 — 자기 자신만 뺀다")],
         "8개, 진부분집합 7개", f.out(), at=("b4", 1))

    # ── 10 합집합의 원소의 개수 ─────────────────────────────────
    f = Fig()
    ca, cb = venn2(f, "A", "B", cx=330, cy=330, r=160, d=100)
    f.circ(*ca, 160, at=0, c="none", f="teal", fo=0.25)
    f.text(ca[0] - 70, 340, "15", z=34, c="teal", at=0, dl=300, b=800)
    f.circ(*cb, 160, at=1, c="none", f="coral", fo=0.25)
    f.text(cb[0] + 70, 340, "12", z=34, c="coral", at=1, dl=300, b=800)
    f.text(330, 330, "5", z=34, c="gold", at=1, dl=900, b=800)
    f.text(330, 380, "두 번", z=22, c="gold", at=1, dl=1100, b=800)
    f.text(CX, 600, "15 + 12 − 5 = 22", z=34, c="gold", at=2, b=800)
    U.ex("h1-2-10", "n(A) = 15, n(B) = 12, n(A ∩ B) = 5일 때 n(A ∪ B)를 구해 보자.", "두 집합을 더하면 겹친 부분을 두 번 센다 — 한 번 빼기",
         [L("n(A) + n(B) = 15 + 12 = 27"),
          L("겹친 n(A ∩ B) = 5를 두 번 셌다"),
          L("n(A ∪ B) = 27 − 5 = 22")],
         "22", f.out(), at=("b4", 1))

    # ── 11 조건의 부정 ─────────────────────────────────────────
    f = Fig()
    nl = NL(f, -2, 6, y=450, x0=60, x1=600, step=1, lab_step=1, z=24)
    nl_range(nl, 2, None, at=0, closed_a=False, right=True, c="teal", up=50)
    f.text(nl.X(4.2), 360, "P: x > 2", z=28, c="teal", at=0, dl=600, b=800)
    nl_range(nl, 2, None, at=1, closed_a=True, right=False, c="coral", up=130)
    f.text(nl.X(0), 280, "~p: x ≤ 2", z=28, c="coral", at=1, dl=600, b=800)
    f.circ(nl.X(2), 450 - 130, 22, at=2, c="gold", sw=4)
    f.text(nl.X(2), 220, "2는 ~p 쪽", z=24, c="gold", at=2, dl=300, b=800)
    U.ex("h1-2-11", "조건 p: x > 2의 부정과 그 진리집합을 수직선에 나타내 보자.", "부정의 진리집합은 여집합 — 경계의 등호가 넘어간다",
         [L("p: x > 2", memo="진리집합 P"),
          L("~p: x ≤ 2", memo="진리집합 P^{c}"),
          L("x = 2는 ~p를 만족", memo="부등호의 등호가 넘어간다")],
         "~p: x ≤ 2", f.out(), at=("b3", 1))

    # ── 12 역과 대우 ───────────────────────────────────────────
    f = Fig()
    f.rect(60, 100, 540, 440, at="q", c="soft", sw=2.5, rx=14)
    f.text(84, 136, "U", z=26, c="soft", at="q", a="s")
    f.poly([(330 + 210 * math.cos(math.radians(a)), 320 - 130 * math.sin(math.radians(a))) for a in range(0, 361, 10)], at="q", c="coral", w=4)
    f.text(160, 220, "Q", z=30, c="coral", at="q", b=800)
    f.circ(430, 320, 56, at="q", c="teal", sw=4)
    f.text(430, 250, "P", z=28, c="teal", at="q", b=800)
    f.dot(430, 330, r=9, f="teal", at="q")
    f.text(430, 364, "2", z=24, at="q", b=800)
    f.dot(230, 330, r=9, f="coral", at="q")
    f.text(230, 364, "−2", z=24, at="q", b=800)
    f.text(CX, 600, "P ⊂ Q → 참", z=28, c="teal", at=0, b=800)
    f.circ(230, 330, 26, at=1, c="red", sw=4)
    f.text(230, 420, "반례", z=24, c="red", at=1, dl=300, b=800)
    hole = [(64, 320), (64, 536), (596, 536), (596, 104), (64, 104), (64, 320), (120, 320)]
    hole += [(330 + 210 * math.cos(math.radians(a)), 320 - 130 * math.sin(math.radians(a))) for a in range(180, -181, -10)]
    f.poly(hole + [(64, 320)], at=2, c="none", f="sky", fo=0.22)   # 바깥 사각형과 안쪽 타원을 반대 방향으로 — 타원 안은 비운다(Q^c)
    f.text(560, 160, "Q^{c}", z=28, c="sky", at=2, dl=400, b=800)
    f.text(CX, 650, "Q^{c} ⊂ P^{c} → 대우도 참", z=26, c="sky", at=2, dl=800, b=800)
    U.ex("h1-2-12", "명제 'x = 2이면 x^{2} = 4이다'의 역과 대우의 참, 거짓을 알아보자.", "명제와 대우는 참 · 거짓이 같고, 역은 따로 따진다",
         [L("명제 p → q: 참", memo="P = {2} ⊂ Q = {−2, 2}"),
          L("역 q → p: 거짓", memo="반례 x = −2"),
          L("대우 ~q → ~p: 참", memo="Q^{c} ⊂ P^{c}")],
         "역은 거짓, 대우는 참", f.out(), at=("b3", 1))

    # ── 13 충분조건과 필요조건 ──────────────────────────────────
    f = Fig()
    nl = NL(f, -1, 3, y=470, x0=70, x1=590, step=0.5, lab_step=1, z=24)
    nl_range(nl, 2, None, at=0, closed_a=False, right=False, c="coral", up=150)
    f.text(nl.X(0.4), 290, "Q: x < 2", z=28, c="coral", at=0, dl=500, b=800)
    nl_range(nl, 0, 1, at=0, closed_a=False, closed_b=False, c="teal", up=60, dl=800)
    f.text(nl.X(0.5), 380, "P: 0 < x < 1", z=26, c="teal", at=0, dl=1300, b=800)
    f.text(CX, 160, "P ⊂ Q", z=40, c="gold", at=1, b=800)
    f.text(CX, 600, "p ⇒ q", z=36, c="gold", at=1, dl=400, b=800)
    f.text(CX, 660, "작은 쪽 p가 충분조건", z=24, c="teal", at=2, b=800)
    U.ex("h1-2-13", "p: 0 < x < 1, q: x < 2일 때, p는 q이기 위한 어떤 조건인지 알아보자.", "진리집합의 포함관계 — 작은 쪽이 충분조건, 큰 쪽이 필요조건",
         [L("P = {x | 0 < x < 1}, Q = {x | x < 2}"),
          L("P ⊂ Q → p ⇒ q", memo="P의 원소는 모두 Q에"),
          L("p는 충분조건, q는 필요조건", memo="Q ⊄ P이므로 필요충분은 아니다")],
         "p는 q이기 위한 충분조건", f.out(), at=("b4", 1))

    # ── 14 귀류법 — √2 는 무리수 ────────────────────────────────
    f = Fig()
    a = chipm(f, 190, 200, "a", "q", c="teal", z=48)
    b = chipm(f, 470, 200, "b", "q", c="coral", z=48)
    f.line(240, 184, 420, 184, at=0, c="gold", w=4, dr=True)
    f.text(CX, 160, "서로소", z=26, c="gold", at=0, dl=400, b=800)
    f.text(CX, 300, "√{2} = {b/a}", z=36, at=0, dl=600, b=800)
    chipm(f, 470, 290, "짝수", 1, c="coral", z=26, fo=0.35)
    f.text(CX, 400, "b^{2} = 2a^{2}", z=32, c="coral", at=1, dl=300, b=800)
    chipm(f, 190, 290, "짝수", 2, c="teal", z=26, fo=0.35)
    f.text(CX, 480, "a^{2} = 2k^{2}", z=32, c="teal", at=2, dl=300, b=800)
    f.cross(CX, 175, s=60, at=3, c="red")
    f.text(CX, 600, "모순! → √{2}는 무리수", z=34, c="red", at=3, dl=400, b=800)
    U.ex("h1-2-14", "귀류법으로 √{2}가 무리수임을 보여 보자.", "결론을 부정해 '유리수'라 두고 밀고 나가 모순을 찾는다",
         [L("√{2} = {b/a} (a, b는 서로소)", memo="유리수라고 가정"),
          L("b^{2} = 2a^{2} → b는 짝수", memo="제곱이 짝수면 그 수도 짝수"),
          L("b = 2k → a^{2} = 2k^{2} → a도 짝수"),
          L("a, b 모두 짝수 — 서로소에 모순", memo="가정이 틀렸다")],
         "√{2}는 무리수", f.out(), at=("b4", 1))

    # ── 15 산술평균과 기하평균 ──────────────────────────────────
    f = Fig()
    u = 36
    for k, (w, h, xx) in enumerate(((1, 4, 70), (2, 2, 250), (4, 1, 420))):
        f.rect(xx, 250 - h * u, w * u, h * u, at=0, c="ink", sw=3, f="gold" if w == 2 else "teal", fo=0.35, dl=500 * k)
        f.text(xx + w * u / 2, 290, f"{w} + {h} = {w + h}", z=22, c="gold" if w == 2 else "teal", at=0, dl=200 + 500 * k, b=800)
    f.text(560, 120, "넓이 4", z=24, c="soft", at=0, dl=1500, b=800)
    P = Plane(f, (0, 6.5), (0, 9), box=(70, 340, 620, 660), square=False)
    f.line(P.X(0), P.Y(0), P.X(6.5), P.Y(0), at=1, c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(0), P.X(0), P.Y(9), at=1, c="ink", w=3, ar=1)
    for v in (1, 2, 3, 4, 5, 6):
        f.text(P.X(v), P.Y(0) + 26, str(v), z=18, c="soft", at=1)
    f.text(P.X(0) - 8, P.Y(4) + 6, "4", z=18, c="soft", at=1, a="e")
    P.curve(lambda x: x + 4 / x, x0=0.5, x1=6.4, at=1, c="sky", w=4)
    f.line(*P.P(0, 4), *P.P(6.4, 4), at=1, c="coral", w=2.5, d=True, dl=600)
    P.pt(2, 4, at=2, f="gold", r=11, label="x = 2일 때 4", pos="n", z=22, c="gold")
    U.ex("h1-2-15", "x > 0일 때 x + {4/x}의 최솟값을 구해 보자.", "곱이 일정하면 합은 두 수가 같을 때 가장 작다 — a + b ≥ 2√{ab}",
         [L("x × {4/x} = 4", memo="넓이 4인 직사각형의 가로 · 세로"),
          L("x + {4/x} ≥ 2√{4} = 4", memo="산술평균 ≥ 기하평균"),
          L("등호: x = {4/x} → x = 2", memo="정사각형일 때")],
         "최솟값 4 (x = 2)", f.out(), at=("b4", 1))

    # ── 16 함수 판별 — 세로선 ───────────────────────────────────
    f = Fig()
    Pl = Plane(f, (-2.2, 2.2), (-0.5, 3.5), box=(40, 140, 300, 560), square=False)
    f.line(Pl.X(-2.2), Pl.Y(0), Pl.X(2.2), Pl.Y(0), at="q", c="ink", w=2.5)
    f.line(Pl.X(0), Pl.Y(-0.5), Pl.X(0), Pl.Y(3.5), at="q", c="ink", w=2.5)
    Pl.curve(lambda x: x * x * 0.7, at="q", c="teal", w=4)
    Pr = Plane(f, (-2.2, 2.2), (-2, 2), box=(360, 140, 620, 560), square=False)
    f.line(Pr.X(-2.2), Pr.Y(0), Pr.X(2.2), Pr.Y(0), at="q", c="ink", w=2.5)
    f.line(Pr.X(0), Pr.Y(-2), Pr.X(0), Pr.Y(2), at="q", c="ink", w=2.5)
    f.poly([Pr.P(1.6 * math.cos(math.radians(a)), 1.6 * math.sin(math.radians(a))) for a in range(0, 361, 10)], at="q", c="coral", w=4)
    for k, xv in enumerate((-1.4, 0.4, 1.6)):
        f.line(Pl.X(xv), Pl.Y(-0.4), Pl.X(xv), Pl.Y(3.4), at=1, c="gold", w=2.5, d=True, dl=500 * k)
        Pl.pt(xv, 0.7 * xv * xv, at=1, f="gold", r=9, dl=500 * k + 300)
    for k, xv in enumerate((-1.0, 0.5, 1.3)):
        f.line(Pr.X(xv), Pr.Y(-1.9), Pr.X(xv), Pr.Y(1.9), at=2, c="gold", w=2.5, d=True, dl=500 * k)
        yv = math.sqrt(1.6 ** 2 - xv * xv)
        Pr.pt(xv, yv, at=2, f="red", r=9, dl=500 * k + 300)
        Pr.pt(xv, -yv, at=2, f="red", r=9, dl=500 * k + 400)
    f.text(170, 620, "함수 ○", z=30, c="teal", at=1, dl=1500, b=800)
    f.text(490, 620, "함수 ×", z=30, c="red", at=2, dl=1500, b=800)
    U.ex("h1-2-16", "포물선과 원 중 함수의 그래프인 것을 세로선으로 판별해 보자.", "세로선이 두 점 이상에서 만나면 x 하나에 y가 둘 — 함수가 아니다",
         [L("세로선을 그어 본다", memo="x 하나를 고정"),
          L("포물선: 어디서나 한 점 → 함수"),
          L("원: 두 점에서 만나는 곳이 있다 → 함수가 아니다", memo="x 하나에 y가 둘")],
         "포물선은 함수, 원은 함수가 아니다", f.out(), at=("b3", 1))

    # ── 17 합성함수 ─────────────────────────────────────────────
    f = Fig()
    for (x0, lab, rule, col) in ((150, "f", "2x − 1", "teal"), (390, "g", "x^{2}", "coral")):
        f.rect(x0, 230, 140, 140, at="q", c=col, sw=4, rx=18, f=col, fo=0.15)
        f.text(x0 + 70, 290, lab, z=40, c=col, at="q", b=800)
        f.text(x0 + 70, 345, rule, z=26, at="q", b=700)
    f.line(90, 300, 146, 300, at="q", c="soft", w=3, ar=1)
    f.line(294, 300, 386, 300, at="q", c="soft", w=3, ar=1)
    f.line(534, 300, 600, 300, at="q", c="soft", w=3, ar=1)
    c2 = chipm(f, 60, 200, "2", 0, c="ink", z=34)
    c3 = chipm(f, 340, 200, "3", 0, c="teal", z=34, dl=900)
    for el in c3:
        fly(el, 220 - 340, 100, dl=40, ms=700)
    f.text(220, 460, "2 × 2 − 1 = 3", z=24, c="teal", at=0, dl=500, b=800)
    c9 = chipm(f, 610, 200, "9", 1, c="coral", z=34, dl=600)
    for el in c9:
        fly(el, 460 - 610, 100, dl=40, ms=700)
    f.text(460, 460, "3^{2} = 9", z=24, c="coral", at=1, dl=200, b=800)
    f.text(CX, 600, "(g∘f)(2) = g(f(2)) = 9", z=32, c="gold", at=2, b=800)
    U.ex("h1-2-17", "f(x) = 2x − 1, g(x) = x^{2}일 때 (g∘f)(2)를 구해 보자.", "f에 먼저 넣고, 그 결과를 g에 넣는다",
         [L("f(2) = 2 × 2 − 1 = 3", memo="f를 먼저"),
          L("g(3) = 3^{2} = 9", memo="f의 결과를 g에"),
          L("(g∘f)(2) = 9", memo="(f∘g)(2) = 7과는 다르다")],
         "9", f.out(), at=("b3", 1))

    # ── 18 역함수 ──────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-5, 4), (-5, 4), box=(60, 50, 620, 610))
    P.axes(at="q", grid=1, lab_step=1)
    P.lineq(2, -3, at="q", c="teal", w=4.5)
    f.text(P.X(3.2), P.Y(3.9), "y = 2x − 3", z=20, c="teal", at="q", b=800, a="e")
    P.lineq(1, 0, at=0, c="soft", w=3, d=True)
    f.text(P.X(-4.6), P.Y(-3.8), "y = x", z=20, c="soft", at=0, dl=600, b=800, a="s")
    for k, (x, y) in enumerate(((0, -3), (2, 1), (1, -1))):
        P.pt(x, y, at=1, f="teal", r=9, dl=300 * k)
        d = f.dot(*P.P(x, y), r=10, f="coral", at=1, dl=300 * k + 100)
        slide(d, 1, dx=P.X(y) - P.X(x), dy=P.Y(x) - P.Y(y), dl=300 * k + 400)
        f.line(*P.P(x, y), *P.P(y, x), at=1, c="coral", w=2, d=True, dr=True, dl=300 * k + 400)
    P.lineq(0.5, 1.5, at=2, c="coral", w=4.5)
    f.text(P.X(-4.5), P.Y(-0.2) - 20, "y = {x + 3/2}", z=20, c="coral", at=2, dl=600, b=800, a="s")
    U.ex("h1-2-18", "y = 2x − 3의 역함수를 구하고 두 그래프의 관계를 알아보자.", "x에 대해 정리한 뒤 x와 y를 맞바꾼다 — 그래프는 y = x에 대칭",
         [L("y = 2x − 3 → x = {y + 3/2}", memo="x에 대해 정리"),
          L("x와 y를 바꾸면 y = {x + 3/2}", memo="점 (a, b)가 (b, a)로"),
          L("그래프는 직선 y = x에 대칭")],
         "y = {x + 3/2}", f.out(), at=("b3", 1))

    # ── 19 유리함수 — 점근선째 옮기기 ───────────────────────────
    f = Fig()
    P = Plane(f, (-3, 5), (-2, 7), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: 2 / x, at="q", c="soft", w=3)
    cv = P.curve(lambda x: 2 / x, x0=-2, x1=4, at=0, c="sky", w=4.5, dr=False)
    slides(cv, 0, dx=P.X(1) - P.X(0), dy=P.Y(3) - P.Y(0), dl=300)
    h = f.line(*P.P(-3, 0), *P.P(5, 0), at=0, c="coral", w=3, d=True)
    slide(h, 0, dy=P.Y(3) - P.Y(0), dl=300)
    v = f.line(*P.P(0, -2), *P.P(0, 7), at=0, c="coral", w=3, d=True)
    slide(v, 0, dx=P.X(1) - P.X(0), dl=300)
    f.text(P.X(4.6), P.Y(3) - 12, "y = 3", z=22, c="coral", at=1, b=800)
    f.text(P.X(1) + 12, P.Y(6.6), "x = 1", z=22, c="coral", at=1, dl=200, b=800, a="s")
    P.pt(2, 5, at=2, f="gold", r=11, label="(2, 5)", pos="e", z=22, c="gold")
    U.ex("h1-2-19", "y = {2/x − 1} + 3의 그래프를 그려 보자.", "y = {2/x}를 x축으로 1, y축으로 3만큼 — 점근선도 함께 옮겨진다",
         [L("y = {2/x}를 x축으로 1, y축으로 3만큼", memo="x − 1, + 3"),
          L("점근선 x = 1, y = 3", memo="좌표축이 옮겨 간 자리"),
          L("x = 2 → y = 2 + 3 = 5", memo="지나는 점으로 확인")],
         "점근선 x = 1, y = 3", f.out(), at=("b4", 1))

    # ── 20 무리함수 ─────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 8), (-1, 5), box=(60, 80, 620, 560))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: math.sqrt(x) if x >= 0 else None, x0=0, x1=6, n=60, at="q", c="soft", w=3)
    cv = P.curve(lambda x: math.sqrt(x) if x >= 0 else None, x0=0, x1=6, n=60, at=0, c="sky", w=4.5, dr=False)
    slides(cv, 0, dx=P.X(2) - P.X(0), dy=P.Y(1) - P.Y(0), dl=300)
    f.line(*P.P(0, 0), *P.P(2, 1), at=0, c="gold", w=3, ar=1, dr=True, dl=300)
    P.pt(2, 1, at=1, f="gold", r=12, label="시작점 (2, 1)", pos="se", z=22, c="gold")
    P.pt(3, 2, at=2, f="coral", r=10, label="(3, 2)", pos="nw", z=22, c="coral")
    P.pt(6, 3, at=2, f="coral", r=10, label="(6, 3)", pos="nw", z=22, c="coral", dl=400)
    U.ex("h1-2-20", "y = √{x − 2} + 1의 그래프를 그려 보자.", "y = √{x}를 평행이동 — 시작점이 (2, 1)로",
         [L("y = √{x}를 x축으로 2, y축으로 1만큼"),
          L("시작점 (2, 1)", memo="정의역 x ≥ 2, 치역 y ≥ 1"),
          L("(3, 2), (6, 3)을 지난다", memo="x − 2가 1, 4일 때")],
         "시작점 (2, 1)에서 오른쪽 위로", f.out(), at=("b4", 1))
