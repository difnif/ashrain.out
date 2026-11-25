# 고3 기하 — 이차곡선 · 공간도형과 공간좌표 · 벡터
import math
from cv import *
from figs import slide, CX, oblique, solid, lab_pts, ell_pts


def arrow(f, A, B, at, c="teal", w=5, dl=0, un=None, dr=True):
    return f.line(A[0], A[1], B[0], B[1], at=at, c=c, w=w, ar=1, dr=dr, dl=dl, un=un)


def ellipse(P, a, b, at, c="sky", w=4.5, n=72):
    pts = [P.P(a * math.cos(2 * math.pi * k / n), b * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
    return P.f.poly(pts, at=at, c=c, w=w, z=False)


def seg(P, A, B, at, c="coral", w=4, dr=False, d=False, dl=0):
    """수학 좌표 두 점을 잇는 선"""
    return P.f.line(*P.P(*A), *P.P(*B), at=at, c=c, w=w, dr=dr, d=d, dl=dl)


def right_mark(f, V, u, v, s=16, at="q", c="ink", dl=0):
    """꼭짓점 V 에서 단위 방향 u · v 사이 직각 표시(겨냥도에서도 쓰게 방향을 직접 받는다)"""
    f.poly([(V[0] + u[0] * s, V[1] + u[1] * s), (V[0] + (u[0] + v[0]) * s, V[1] + (u[1] + v[1]) * s), (V[0] + v[0] * s, V[1] + v[1] * s)],
           at=at, c=c, w=2.5, z=False, dl=dl)


def unit(A, B):
    dx, dy = B[0] - A[0], B[1] - A[1]
    n = math.hypot(dx, dy)
    return (dx / n, dy / n)


def build(U):
    # ── 01 포물선 — 초점과 준선까지 같은 거리 ──────────────────────
    f = Fig()
    P = Plane(f, (-2, 6), (-5, 5), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    f.poly([P.P(t * t / 4, t) for t in [k / 10 for k in range(-46, 47)]], at="q", c="sky", w=4.5, z=False)
    f.line(*P.P(-1, -5), *P.P(-1, 5), at=0, c="coral", w=3, d=True, dr=True)
    f.text(P.X(-1) - 10, P.Y(4.6), "x = −1", z=20, c="coral", at=0, dl=500, b=800, a="e")
    P.pt(1, 0, at=0, f="teal", r=11, label="F(1, 0)", pos="se", z=20, c="teal", dl=300)
    P.pt(4, 4, at=1, f="ink", r=11, label="P(4, 4)", pos="e", z=22)
    f.line(*P.P(4, 4), *P.P(1, 0), at=1, c="teal", w=5, dr=True, dl=300)
    f.text(390, 254, "5", z=28, c="teal", at=1, dl=900, b=800)
    f.line(*P.P(4, 4), *P.P(-1, 4), at=2, c="coral", w=5, dr=True)
    f.text(P.X(1.5), P.Y(4) - 16, "5", z=28, c="coral", at=2, dl=600, b=800)
    for t in (2, -2):
        seg(P, (1, t), (1, 0), 2, c="teal", w=2.5, d=True, dl=900)
        seg(P, (1, t), (-1, t), 2, c="coral", w=2.5, d=True, dl=900)
        P.pt(1, t, at=2, f="ink", r=7, dl=900)
    U.ex("h3-3-01", "포물선 y^{2} = 4x 위의 점 P(4, 4)에서 초점까지의 거리와 준선까지의 거리를 비교해 보자.", "포물선 = 초점과 준선에서 같은 거리에 있는 점들",
         [L("초점 F(1, 0), 준선 x = −1", memo="y^{2} = 4px에서 p = 1"),
          L("PF = √{3^{2} + 4^{2}} = 5"),
          L("PH = 4 + 1 = 5", memo="준선까지 — 같다. (1, ±2)에서도 2와 2")],
         "둘 다 5", f.out(), at=("b3", 1))

    # ── 02 타원 — 두 초점까지 거리의 합 ──────────────────────────
    f = Fig()
    P = Plane(f, (-6, 6), (-4, 4), box=(50, 100, 620, 560))
    P.axes(at="q", grid=1, lab_step=1)
    ellipse(P, 5, 3, "q")
    for sgn in (1, -1):
        d = f.dot(*P.P(0, 0), r=11, f="gold", at=1)
        slide(d, 1, dx=P.X(4 * sgn) - P.X(0), dl=300)
    f.text(P.X(4), P.Y(0) - 18, "F", z=24, c="gold", at=1, dl=1200, b=800)
    f.text(P.X(-4), P.Y(0) - 18, "F'", z=24, c="gold", at=1, dl=1200, b=800)
    P.pt(0, 3, at=2, f="ink", r=10, label="P", pos="n", z=24)
    f.line(*P.P(0, 3), *P.P(4, 0), at=2, c="teal", w=4, dr=True)
    f.line(*P.P(0, 3), *P.P(-4, 0), at=2, c="coral", w=4, dr=True, dl=300)
    f.text(P.X(2.3), P.Y(1.9), "5", z=24, c="teal", at=2, dl=700, b=800)
    f.text(P.X(-2.3), P.Y(1.9), "5", z=24, c="coral", at=2, dl=800, b=800)
    f.text(CX, 630, "어디서든 합 = 2a = 10", z=26, c="gold", at=2, dl=1300, b=800)
    U.ex("h3-3-02", "타원 {x^{2}/25} + {y^{2}/9} = 1의 초점을 구하고, 타원 위의 점에서 두 초점까지 거리의 합을 확인해 보자.", "큰 분모가 a^{2} — c^{2} = a^{2} − b^{2}",
         [L("a^{2} = 25, b^{2} = 9", memo="가로로 긴 타원"),
          L("c^{2} = 25 − 9 = 16 → c = 4", memo="초점 (±4, 0)"),
          L("PF + PF' = 2a = 10", memo="(0, 3)에서 5 + 5")],
         "초점 (±4, 0), 거리의 합 10", f.out(), at=("b3", 1))

    # ── 03 쌍곡선 — 직사각형의 대각선이 점근선 ────────────────────
    f = Fig()
    P = Plane(f, (-8, 8), (-6, 6), box=(40, 60, 620, 640))
    P.axes(at="q", grid=None, lab_step=2, ystep=2)
    for sgn in (1, -1):
        f.poly([P.P(sgn * 4 * math.cosh(u / 10), 3 * math.sinh(u / 10)) for u in range(-13, 14)], at="q", c="sky", w=4.5, z=False)
    f.poly([P.P(-4, -3), P.P(4, -3), P.P(4, 3), P.P(-4, 3)], at=0, c="soft", w=2.5, d=True, dr=True)
    f.text(P.X(-2), P.Y(-3) - 10, "8", z=22, c="soft", at=0, dl=600, b=800)
    f.text(P.X(-4) + 14, P.Y(1.5) + 8, "6", z=22, c="soft", at=0, dl=700, b=800, a="s")
    for k, sgn in enumerate((1, -1)):
        f.line(*P.P(-8, -6 * sgn), *P.P(8, 6 * sgn), at=1, c="coral", w=3, d=True, dr=True, dl=300 * k)
    f.text(P.X(5.6), P.Y(5.6), "y = ±{3/4}x", z=24, c="coral", at=1, dl=900, b=800)
    for sgn in (1, -1):
        d = f.dot(*P.P(4 * sgn, 0), r=11, f="gold", at=2)
        slide(d, 2, dx=P.X(5 * sgn) - P.X(4 * sgn), dl=300)
        f.text(P.X(5 * sgn), P.Y(0) - 16, "F", z=22, c="gold", at=2, dl=1200, b=800)
    U.ex("h3-3-03", "쌍곡선 {x^{2}/16} − {y^{2}/9} = 1의 점근선과 초점을 구해 보자.", "가로 2a, 세로 2b 직사각형의 대각선이 점근선 — c^{2} = a^{2} + b^{2}",
         [L("a = 4, b = 3"),
          L("대각선 → 점근선 y = ±{3/4}x", memo="가로 8, 세로 6인 직사각형"),
          L("c^{2} = 16 + 9 = 25 → c = 5", memo="초점은 꼭짓점보다 바깥 (±5, 0)")],
         "점근선 y = ±{3/4}x, 초점 (±5, 0)", f.out(), at=("b4", 0))

    # ── 04 이차곡선 — 원뿔 자르기 ───────────────────────────────
    f = Fig()
    Ap, H = (250, 340), 230
    k60 = math.tan(math.radians(60))
    for sgn in (1, -1):
        f.line(Ap[0] - sgn * H / k60, Ap[1] - H, Ap[0] + sgn * H / k60, Ap[1] + H, at="q", c="ink", w=3.5)
    f.line(Ap[0], 90, Ap[0], 590, at="q", c="soft", w=2, d=True)
    Cp, half = (250, 420), 220
    cuts = [("원", 0, "gold"), ("타원", 18, "teal"), ("포물선", 60, "coral"), ("쌍곡선", 80, "lilac")]
    for k, (nm, ang, col) in enumerate(cuts):
        at = "q" if k == 0 else k - 1
        el = f.line(Cp[0] - half, Cp[1], Cp[0] + half, Cp[1], at=at, c=col, w=5, un=k if k < 3 else None)
        if ang:
            el["mv"] = {"at": at, "r": -ang, "cx": Cp[0], "cy": Cp[1], "dl": 300}
        f.text(560, 150 + 64 * k, nm, z=30, c=col, at=at, dl=1100 if k else 0, b=800)
    U.ex("h3-3-04", "원뿔을 평면으로 자르는 각도에 따라 어떤 곡선이 생기는지 알아보자.", "모선보다 완만하면 타원(수평이면 원), 평행하면 포물선, 가파르면 쌍곡선",
         [L("수평이면 원, 조금 기울이면 타원", memo="한 원뿔만 자른다"),
          L("모선과 평행하면 포물선", memo="한쪽이 끝없이 열린다"),
          L("더 가파르면 위아래 원뿔을 모두 → 쌍곡선", memo="두 갈래")],
         "원 · 타원 · 포물선 · 쌍곡선", f.out(), at=("b3", 1))

    # ── 05 포물선의 접선 ───────────────────────────────────────
    f = Fig()
    P = Plane(f, (-2, 5), (-4, 5), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    f.poly([P.P(t * t / 4, t) for t in [k / 10 for k in range(-40, 41)]], at="q", c="sky", w=4.5, z=False)
    P.pt(1, 2, at="q", f="ink", r=11, label="(1, 2)", pos="w", z=22)
    g = seg(P, (-2.5, 0.5), (2.5, 5.5), 1, c="coral", w=4)            # y = x + 3 에서 내려와 닿는다
    slide(g, 1, dx=P.sx, dy=P.sy, dl=300)
    f.text(P.X(3.6), P.Y(4.5), "y = x + 1", z=24, c="coral", at=2, b=800, a="s")
    f.text(P.X(0) - 34, P.Y(-3.4), "(y − 2)^{2} = 0 — 중근", z=22, c="gold", at=2, dl=400, b=800, a="e")
    U.ex("h3-3-05", "포물선 y^{2} = 4x 위의 점 (1, 2)에서의 접선의 방정식을 구해 보자.", "y_{1}y = 2p(x + x_{1}) — 제곱 문자는 한 짝 양보, 일차는 평균",
         [L("y_{1}y = 2p(x + x_{1})에 p = 1, (x_{1}, y_{1}) = (1, 2)"),
          L("2y = 2(x + 1)", memo="기울기 1인 직선을 내려 닿게"),
          L("y = x + 1", memo="연립하면 (y − 2)^{2} = 0 — 접한다")],
         "y = x + 1", f.out(), at=("b2", -1))

    # ── 06 타원의 접선 ─────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-3.5, 4.8), (-2.5, 3.2), box=(50, 80, 620, 600))
    P.axes(at="q", grid=1, lab_step=1)
    ellipse(P, math.sqrt(8), math.sqrt(2), "q")
    P.pt(2, 1, at="q", f="ink", r=11, label="(2, 1)", pos="ne", z=22)
    g = seg(P, (0.5, 2.5), (4.9, 0.3), 1, c="coral", w=4)
    slide(g, 1, dx=-0.3 * P.sx, dy=0.6 * P.sy, dl=300)
    f.text(P.X(3.0), P.Y(-1.0), "x + 2y = 4", z=24, c="coral", at=2, b=800, a="s")
    U.ex("h3-3-06", "타원 {x^{2}/8} + {y^{2}/2} = 1 위의 점 (2, 1)에서의 접선의 방정식을 구해 보자.", "{x_{1}x/a^{2}} + {y_{1}y/b^{2}} = 1 — 원의 접선 공식과 같은 문법",
         [L("{2x/8} + {1 × y/2} = 1", memo="x^{2} → 2x, y^{2} → 1 × y"),
          L("{x/4} + {y/2} = 1", memo="기울기 −{1/2}인 직선이 (2, 1)에 닿는다"),
          L("x + 2y = 4")],
         "x + 2y = 4", f.out(), at=("b2", -1))

    # ── 07 쌍곡선의 접선 — 점근선보다 가파르게 ─────────────────────
    f = Fig()
    P = Plane(f, (-4, 4), (-4, 4), box=(50, 50, 620, 620))
    P.axes(at="q", grid=1, lab_step=1)
    for sgn in (1, -1):
        f.poly([P.P(sgn * math.cosh(u / 10), math.sinh(u / 10)) for u in range(-20, 21)], at="q", c="sky", w=4.5, z=False)
    for sgn in (1, -1):
        P.lineq(sgn, 0, at=0, c="soft", w=2.5, d=True)
    f.text(P.X(1.6), P.Y(3.5), "y = ±x", z=22, c="soft", at=0, dl=600, b=800)
    s3 = math.sqrt(3)
    for k, (c0, sx, tx) in enumerate(((s3, -1, -1.155), (-s3, 1, 1.155))):
        x0, x1 = (-2.6, 0.9) if c0 > 0 else (-0.9, 2.6)
        g = seg(P, (x0 + 0.5 * sx, 2 * x0 + c0), (x1 + 0.5 * sx, 2 * x1 + c0), 1, c="coral", w=3.5, dl=500 * k)
        slide(g, 1, dx=-0.5 * sx * P.sx, dl=300 + 500 * k)
        P.pt(tx, 2 * tx + c0, at=1, f="coral", r=8, dl=1300 + 500 * k)
    f.text(P.X(0.1), P.Y(-2.9), "기울기 2: 접선 2개", z=22, c="coral", at=1, dl=1800, b=800, a="s")
    g = P.lineq(0.5, 2.2, at=2, c="lilac", w=3.5, dr=False)
    slide(g, 2, dy=2.5 * P.sy, dl=300)
    for x, y in ((1.022, 0.211), (-1.422, -1.011)):
        P.pt(x, y, at=2, f="lilac", r=8, dl=1300)
    f.text(P.X(0.1), P.Y(-3.55), "기울기 {1/2}: 접선 없음", z=22, c="lilac", at=2, dl=1500, b=800, a="s")
    U.ex("h3-3-07", "쌍곡선 x^{2} − y^{2} = 1에 기울기가 2인 접선과 기울기가 {1/2}인 접선이 있는지 알아보자.", "y = mx ± √{a^{2}m^{2} − b^{2}} — 근호 안이 양수, 즉 점근선보다 가파를 때만",
         [L("x^{2} − y^{2} = 1: 점근선 y = ±x", memo="a = b = 1"),
          L("m = 2: y = 2x ± √{4 − 1} = 2x ± √{3}", memo="점근선보다 가파르다 → 접선 2개"),
          L("m = {1/2}: 근호 안 {1/4} − 1 < 0", memo="접선 없음 — 어디로 옮겨도 두 갈래를 가로지른다")],
         "y = 2x ± √{3} · 기울기 {1/2}은 없음", f.out(), at=("b3", 1))

    # ── 08 꼬인 위치 ───────────────────────────────────────────
    f = Fig()
    s = 260
    base = {"A": (0, 0, 0), "B": (s, 0, 0), "C": (s, 0, s), "D": (0, 0, s), "E": (0, s, 0), "F": (s, s, 0), "G": (s, s, s), "H": (0, s, s)}
    V = {k: (110 + oblique(p)[0], 230 + oblique(p)[1]) for k, p in base.items()}
    Ed = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"), ("A", "E"), ("B", "F"), ("C", "G"), ("D", "H")]
    solid(f, V, Ed, hidden=[("D", "H"), ("H", "E"), ("G", "H")], at="q")
    lab_pts(f, V, at="q", z=26, off={"A": (-18, -10), "B": (16, 28), "C": (18, -10), "D": (-16, -12), "E": (-18, 26), "F": (16, 28), "G": (18, 26), "H": (-16, -10)})
    f.line(*V["A"], *V["B"], at=0, c="teal", w=7, dr=True)
    f.line(*V["C"], *V["G"], at=0, c="coral", w=7, dr=True, dl=500)
    cp = f.line(*V["A"], *V["B"], at=1, c="teal", w=5, d=True)
    slide(cp, 1, dx=V["D"][0] - V["A"][0], dy=V["D"][1] - V["A"][1], dl=300)
    f.text(CX + 30, 60, "AB를 옮겨 와도 CG와 방향이 다르다", z=22, c="teal", at=1, dl=1200, b=800)
    f.poly([V["A"], V["B"], V["C"], V["D"]], at=2, c="none", f="gold", fo=0.3)
    f.circ(*V["G"], 18, at=2, c="red", sw=4, dl=400)
    f.text(CX, 640, "AB와 C를 담는 평면 위에 G가 없다", z=22, c="red", at=2, dl=700, b=800)
    U.ex("h3-3-08", "정육면체에서 두 모서리 AB와 CG의 위치 관계를 알아보자.", "만나지도 평행하지도 않으면 한 평면에 담을 수 없다 — 꼬인 위치",
         [L("AB와 CG는 만나지 않는다"),
          L("AB와 CG는 평행하지 않다", memo="방향이 다르다"),
          L("한 평면에 담을 수 없다 → 꼬인 위치", memo="AB와 C를 품은 평면은 윗면 — G는 아래")],
         "꼬인 위치", f.out(), at=("b3", 1))

    # ── 09 삼수선 정리 ─────────────────────────────────────────
    f = Fig()
    f.poly([(60, 520), (420, 520), (600, 380), (240, 380)], at="q", c="ink", w=3, f="soft", fo=0.15)
    f.text(100, 506, "α", z=28, c="soft", at="q", b=800)
    Pp, Oo, Hh = (380, 150), (380, 490), (444.3, 440)
    f.line(170, 440, 515, 440, at="q", c="ink", w=3.5)
    f.text(527, 448, "l", z=26, at="q", b=800, a="s")
    f.dot(*Pp, r=9, f="ink", at="q")
    f.text(Pp[0] + 16, Pp[1] + 8, "P", z=28, at="q", b=800, a="s")
    up, ex = (0, -1), (1, 0)
    oh = unit(Oo, Hh)
    f.line(*Pp, *Oo, at=0, c="teal", w=5, dr=True)
    f.text(Oo[0] - 14, Oo[1] + 26, "O", z=26, at=0, dl=500, b=800, a="e")
    f.text(Pp[0] - 14, 330, "4", z=26, c="teal", at=0, dl=600, b=800, a="e")
    right_mark(f, Oo, up, oh, s=18, at=0, dl=700)
    f.line(*Oo, *Hh, at=0, c="coral", w=5, dr=True, dl=900)
    f.text(Hh[0] + 22, Hh[1] + 30, "H", z=26, at=0, dl=1200, b=800, a="s")
    f.text(428, 486, "3", z=26, c="coral", at=0, dl=1300, b=800)
    right_mark(f, Hh, ex, (-oh[0], -oh[1]), s=16, at=0, dl=1400)
    f.line(*Pp, *Hh, at=0, c="gold", w=5, dr=True, dl=1800)
    right_mark(f, Hh, ex, unit(Hh, Pp), s=16, at=0, c="gold", dl=2300)
    f.poly([Pp, Oo, Hh], at=1, c="none", f="gold", fo=0.2)
    f.text(432, 300, "5", z=30, c="gold", at=2, b=800, a="s")
    U.ex("h3-3-09", "평면 α 밖의 점 P에서 α에 내린 수선의 발이 O, O에서 α 위의 직선 l에 내린 수선의 발이 H이다. PO = 4, OH = 3일 때 PH의 길이를 구해 보자.", "삼수선 정리 — PO ⊥ α, OH ⊥ l이면 PH ⊥ l, 직각삼각형 POH",
         [L("PO ⊥ α, OH ⊥ l → PH ⊥ l", memo="세 수직 중 둘을 확인"),
          L("PH^{2} = 4^{2} + 3^{2} = 25", memo="∠POH = 90°"),
          L("PH = 5", memo="P에서 직선 l까지의 거리")],
         "5", f.out(), at=("b4", 1))

    # ── 10 정사영 ──────────────────────────────────────────────
    f = Fig()
    f.poly([(40, 540), (500, 540), (620, 420), (160, 420)], at="q", c="ink", w=3, f="soft", fo=0.15)
    A = (150, 480)
    L_ = 340
    seg10 = f.line(A[0], A[1], A[0] + L_, A[1], at=0, c="teal", w=6)
    seg10["mv"] = {"at": 0, "r": -60, "cx": A[0], "cy": A[1], "dl": 300}
    Bt = (A[0] + L_ * math.cos(math.radians(60)), A[1] - L_ * math.sin(math.radians(60)))
    f.text(A[0] + 70, A[1] - 150, "10", z=28, c="teal", at=0, dl=1200, b=800, a="e")
    f.arc(*A, 60, 0, 60, at=0, c="gold", sw=3, f="gold", fo=0.3, dl=1300)
    f.text(A[0] + 84, A[1] - 22, "60°", z=22, c="gold", at=0, dl=1400, b=800)
    f.line(*Bt, Bt[0], A[1], at=1, c="soft", w=3, d=True, dr=True)
    f.line(*A, Bt[0], A[1], at=1, c="coral", w=8, dr=True, dl=500)
    f.text((A[0] + Bt[0]) / 2, A[1] + 40, "그림자 5", z=26, c="coral", at=1, dl=900, b=800)
    f.text(480, 160, "10 × cos 60° = 5", z=28, c="coral", at=1, dl=1200, b=800)
    f.text(480, 230, "넓이도 × cos θ", z=24, c="gold", at=2, b=800)
    U.ex("h3-3-10", "길이 10인 선분이 평면과 60°를 이룰 때, 평면 위로의 정사영의 길이를 구해 보자.", "정사영 = 수직으로 내린 그림자 — 길이 × cos θ",
         [L("길이 10, 평면과 이루는 각 60°", memo="눕혀 있던 선분을 60° 세운다"),
          L("그림자 = 10 × cos 60° = 5", memo="cos 60° = {1/2}"),
          L("넓이의 정사영도 S' = S cos θ", memo="기울수록 그림자가 줄어든다")],
         "5", f.out(), at=("b3", 1))

    # ── 11 공간좌표 — 상자의 대각선 ─────────────────────────────
    f = Fig()
    u = 56
    O = (130, 600)

    def Q(x, y, z):
        return (O[0] + x * u + y * u * 0.55, O[1] - z * u * 0.92 - y * u * 0.6)

    box = [((0, 0, 0), (2, 0, 0)), ((0, 0, 0), (0, 3, 0)), ((2, 0, 0), (2, 3, 0)), ((0, 3, 0), (2, 3, 0)),
           ((0, 0, 6), (2, 0, 6)), ((0, 0, 6), (0, 3, 6)), ((2, 0, 6), (2, 3, 6)), ((0, 3, 6), (2, 3, 6)),
           ((0, 0, 0), (0, 0, 6)), ((2, 0, 0), (2, 0, 6)), ((2, 3, 0), (2, 3, 6)), ((0, 3, 0), (0, 3, 6))]
    for a, b in box:
        f.line(*Q(*a), *Q(*b), at="q", c="soft", w=2.5, d=(0, 3, 0) in (a, b))
    f.text(Q(1, 0, 0)[0], Q(1, 0, 0)[1] + 28, "2", z=22, at="q", b=800)
    f.text(306, 572, "3", z=22, at="q", b=800)
    f.text(Q(0, 0, 3)[0] - 16, Q(0, 0, 3)[1], "6", z=22, at="q", b=800, a="e")
    f.text(O[0] - 14, O[1] + 26, "O", z=24, at="q", b=800, a="e")
    f.line(*Q(0, 0, 0), *Q(2, 3, 0), at=0, c="teal", w=5, dr=True)
    f.text(236, 530, "√{13}", z=20, c="teal", at=0, dl=600, b=800)
    f.line(*Q(2, 3, 0), *Q(2, 3, 6), at=1, c="coral", w=5, dr=True)
    f.line(*Q(0, 0, 0), *Q(2, 3, 6), at=1, c="gold", w=5, dr=True, dl=600)
    f.dot(*Q(2, 3, 6), r=10, f="gold", at=1, dl=1200)
    f.text(Q(2, 3, 6)[0] + 14, Q(2, 3, 6)[1] - 10, "P(2, 3, 6)", z=22, c="gold", at=1, dl=1300, b=800, a="s")
    mid = Q(1, 1.5, 3)
    f.text(mid[0] - 22, mid[1] + 8, "7", z=32, c="gold", at=2, b=800, a="e")
    U.ex("h3-3-11", "원점 O와 점 P(2, 3, 6) 사이의 거리를 구해 보자.", "피타고라스 두 번 — 바닥의 대각선, 그다음 세운 높이",
         [L("바닥의 대각선 √{2^{2} + 3^{2}} = √{13}", memo="xy평면 위에서"),
          L("OP^{2} = 13 + 6^{2} = 49", memo="높이 6을 세워 한 번 더"),
          L("OP = 7", memo="√{a^{2} + b^{2} + c^{2}}")],
         "7", f.out(), at=("b4", 1))

    # ── 12 xy평면이 나누는 비 ──────────────────────────────────
    f = Fig()
    P = Plane(f, (0, 5), (-3, 5), box=(80, 60, 600, 640))
    f.line(P.X(0), P.Y(-3), P.X(0), P.Y(5), at="q", c="ink", w=3, ar=1)
    f.text(P.X(0) - 12, P.Y(4.8), "z", z=24, at="q", b=800, a="e")
    for v, s_ in ((-2, "−2"), (2, "2"), (4, "4")):
        f.text(P.X(0) - 10, P.Y(v) + 7, s_, z=20, c="soft", at="q", a="e")
    f.poly([P.P(0, -0.15), P.P(5, -0.15), P.P(5, 0.15), P.P(0, 0.15)], at="q", c="none", f="gold", fo=0.4)
    f.text(P.X(0) + 10, P.Y(0) - 14, "xy평면 (z = 0)", z=20, c="gold", at="q", b=800, a="s")
    P.pt(1, 4, at=0, f="teal", r=11, label="A (z = 4)", pos="e", z=22, c="teal")
    P.pt(4, -2, at=0, f="coral", r=11, label="B (z = −2)", pos="w", z=22, c="coral", dl=300)
    seg(P, (1, 4), (4, -2), 1, c="ink", w=4, dr=True)
    P.pt(3, 0, at=1, f="gold", r=12, dl=900)
    seg(P, (1, 4), (4.6, 4), 2, c="soft", w=2.5, d=True)
    seg(P, (4, -2), (4.6, -2), 2, c="soft", w=2.5, d=True)
    seg(P, (4.6, 4), (4.6, 0), 2, c="teal", w=6, dr=True, dl=300)
    seg(P, (4.6, 0), (4.6, -2), 2, c="coral", w=6, dr=True, dl=800)
    f.text(P.X(4.6) + 14, P.Y(2) + 9, "4", z=26, c="teal", at=2, dl=600, b=800, a="s")
    f.text(P.X(4.6) + 14, P.Y(-1) + 9, "2", z=26, c="coral", at=2, dl=1100, b=800, a="s")
    U.ex("h3-3-12", "두 점 A(1, 2, 4), B(4, −1, −2)를 잇는 선분 AB가 xy평면에 의해 나누어지는 비를 구해 보자.", "xy평면은 z = 0 — z좌표 한 줄만 보면 된다",
         [L("A의 z좌표 4, B의 z좌표 −2"),
          L("xy평면 = z가 0인 곳", memo="AB가 z = 0을 지나는 점"),
          L("4 : 2 = 2 : 1", memo="4에서 0까지 4, 0에서 −2까지 2")],
         "2 : 1로 내분", f.out(), at=("b4", 1))

    # ── 13 구의 단면 ───────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-6, 6), (-3, 9), box=(60, 50, 620, 650))
    f.line(P.X(0), P.Y(-3), P.X(0), P.Y(9), at="q", c="soft", w=2, d=True)
    f.circ(*P.P(0, 3), 5 * P.sx, at="q", c="sky", sw=4)
    f.line(P.X(-6), P.Y(0), P.X(6), P.Y(0), at="q", c="gold", w=4)
    f.text(P.X(5.9), P.Y(0) - 14, "z = 0", z=22, c="gold", at="q", b=800, a="e")
    P.pt(0, 3, at="q", f="ink", r=9, label="중심 (0, 0, 3)", pos="e", z=20)
    seg(P, (0, 3), (0, 0), 0, c="coral", w=5, dr=True)
    f.text(P.X(0) - 14, P.Y(1.5), "3", z=26, c="coral", at=0, dl=500, b=800, a="e")
    seg(P, (0, 3), (4, 0), 0, c="ink", w=4, dr=True, dl=500)
    f.text(P.X(2.4), P.Y(1.9), "5", z=26, at=0, dl=900, b=800, a="s")
    seg(P, (0, 0), (4, 0), 1, c="teal", w=7, dr=True)
    f.text(P.X(2), P.Y(0) + 34, "4", z=28, c="teal", at=1, dl=500, b=800)
    f.poly([P.P(4 * math.cos(2 * math.pi * k / 48), -0.9 * math.sin(2 * math.pi * k / 48)) for k in range(49)], at=2, c="teal", w=3.5, z=False, dr=True)
    f.text(P.X(-3.6), P.Y(-1.8), "단면: 반지름 4인 원", z=22, c="teal", at=2, dl=600, b=800)
    U.ex("h3-3-13", "중심이 (0, 0, 3)이고 반지름이 5인 구를 xy평면으로 자른 단면의 반지름을 구해 보자.", "중심에서 평면까지 거리 · 반지름 · 단면 반지름의 직각삼각형",
         [L("중심에서 xy평면까지 거리 3", memo="z좌표"),
          L("(단면 반지름)^{2} = 5^{2} − 3^{2} = 16", memo="피타고라스"),
          L("단면 반지름 = 4")],
         "4", f.out(), at=("b4", 0))

    # ── 14 같은 벡터 — 평행이동 ─────────────────────────────────
    f = Fig()
    A, B, C, D = (120, 480), (420, 480), (560, 220), (260, 220)
    f.poly([A, B, C, D], at="q", c="soft", w=3)
    lab_pts(f, {"A": A, "B": B, "C": C, "D": D}, at="q", z=28, off={"A": (-18, 28), "B": (16, 28), "C": (18, -8), "D": (-18, -8)})
    arrow(f, A, B, 0)
    f.text((A[0] + B[0]) / 2, A[1] + 42, "⃗{AB}", z=28, c="teal", at=0, dl=700, b=800)
    cp = arrow(f, A, B, 1, dr=False)
    slide(cp, 1, dx=D[0] - A[0], dy=D[1] - A[1], dl=300)
    f.text((D[0] + C[0]) / 2, D[1] - 22, "⃗{DC}", z=28, c="teal", at=2, b=800)
    f.text(CX, 620, "크기 · 방향이 같으면 같은 벡터", z=26, c="gold", at=2, dl=500, b=800)
    U.ex("h3-3-14", "평행사변형 ABCD에서 ⃗{AB}와 같은 벡터를 찾아보자.", "벡터는 크기와 방향만 — 평행이동해서 겹치면 같은 벡터",
         [L("⃗{AB}: A에서 B로", memo="시점 A, 종점 B"),
          L("평행이동하면 DC에 겹친다", memo="크기 같고 방향 같다"),
          L("⃗{AB} = ⃗{DC}", memo="시점이 달라도 같은 벡터")],
         "⃗{DC}", f.out(), at=("b3", 1))

    # ── 15 벡터의 덧셈 — 이어 붙이기 ────────────────────────────
    f = Fig()
    P = Plane(f, (-0.5, 5), (-0.5, 5), box=(60, 60, 620, 620))
    O, Aa, Bb, Cc = P.P(0, 0), P.P(3, 1), P.P(1, 3), P.P(4, 4)
    arrow(f, O, Aa, "q", c="teal")
    f.text(P.X(1.6), P.Y(0.3) + 30, "⃗{a}", z=30, c="teal", at="q", b=800)
    arrow(f, O, Bb, "q", c="coral")
    f.text(P.X(0.3), P.Y(1.7), "⃗{b}", z=30, c="coral", at="q", b=800, a="e")
    cp = arrow(f, O, Bb, 0, c="coral", dr=False)
    slide(cp, 0, dx=Aa[0] - O[0], dy=Aa[1] - O[1], dl=300)
    arrow(f, O, Cc, 1, c="gold", w=6)
    f.text(P.X(2.2) - 6, P.Y(2.4) - 10, "⃗{a} + ⃗{b}", z=30, c="gold", at=1, dl=700, b=800, a="e")
    lab_pts(f, {"A": O, "B": Aa, "C": Cc}, at=2, z=26, off={"A": (-14, 28), "B": (22, 18), "C": (16, -12)})
    f.text(CX, 640, "⃗{AB} + ⃗{BC} = ⃗{AC}", z=30, c="gold", at=2, dl=400, b=800)
    U.ex("h3-3-15", "두 벡터 ⃗{a}, ⃗{b}의 합 ⃗{a} + ⃗{b}를 화살표로 그려 보자.", "이어 붙이기 — 처음 시점에서 마지막 끝점으로 가는 화살표",
         [L("⃗{a}의 끝에 ⃗{b}의 시점을 잇는다", memo="⃗{b}를 평행이동"),
          L("처음 시점 → 마지막 끝점이 ⃗{a} + ⃗{b}"),
          L("⃗{AB} + ⃗{BC} = ⃗{AC}", memo="경유지 B가 지워진다")],
         "⃗{a}의 시점에서 옮긴 ⃗{b}의 끝점까지", f.out(), at=("b3", 1))

    # ── 16 실수배 ──────────────────────────────────────────────
    f = Fig()
    O = (190, 420)
    v = (130, -70)
    tip = (O[0] + v[0], O[1] + v[1])
    arrow(f, O, tip, "q", c="teal")
    f.text(O[0] + v[0] / 2 - 6, O[1] + v[1] / 2 - 22, "⃗{a}", z=30, c="teal", at="q", b=800)
    cp = arrow(f, O, tip, 0, c="teal", dr=False)
    slide(cp, 0, dx=v[0], dy=v[1], dl=300)
    f.text(O[0] + 2 * v[0] + 26, O[1] + 2 * v[1], "2⃗{a}", z=30, c="teal", at=0, dl=1200, b=800, a="s")
    ng = arrow(f, O, tip, 1, c="coral", dr=False)
    ng["mv"] = {"at": 1, "r": 180, "cx": O[0], "cy": O[1], "dl": 300}
    f.text(O[0] - v[0] - 20, O[1] - v[1] + 12, "−⃗{a}", z=30, c="coral", at=1, dl=1200, b=800, a="e")
    f.text(CX, 600, "⃗{b} = k⃗{a} ⇔ ⃗{a} ∥ ⃗{b}", z=30, c="gold", at=2, b=800)
    U.ex("h3-3-16", "벡터 ⃗{a}로 2⃗{a}와 −⃗{a}를 그려 보자.", "k⃗{a} — 크기는 |k|배, k < 0이면 방향이 반대",
         [L("2⃗{a} = ⃗{a} + ⃗{a}", memo="같은 방향으로 크기 2배"),
          L("−⃗{a}: 크기 같고 방향 반대", memo="반 바퀴 돌린 화살표"),
          L("⃗{b} = k⃗{a}이면 ⃗{a} ∥ ⃗{b}", memo="실수배가 곧 평행")],
         "2⃗{a}는 같은 방향 2배, −⃗{a}는 반대 방향", f.out(), at=("b2", -1))

    # ── 17 위치벡터 — 내분점 ───────────────────────────────────
    f = Fig()
    O, A, B = (90, 540), (520, 470), (300, 130)
    Pp = ((A[0] + 2 * B[0]) / 3, (A[1] + 2 * B[1]) / 3)
    f.dot(*O, r=9, f="ink", at="q")
    f.text(O[0] - 14, O[1] + 26, "O", z=26, at="q", b=800, a="e")
    arrow(f, O, A, "q", c="soft", w=3.5)
    arrow(f, O, B, "q", c="soft", w=3.5)
    f.text(A[0] + 16, A[1] + 8, "A", z=26, at="q", b=800, a="s")
    f.text(B[0], B[1] - 16, "B", z=26, at="q", b=800)
    f.text((O[0] + A[0]) / 2, (O[1] + A[1]) / 2 + 40, "⃗{a}", z=26, c="soft", at="q", b=800)
    f.text((O[0] + B[0]) / 2 - 22, (O[1] + B[1]) / 2, "⃗{b}", z=26, c="soft", at="q", b=800, a="e")
    f.line(*A, *B, at=0, c="ink", w=3)
    for t in (1 / 3, 2 / 3):
        f.dot(A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t, r=6, f="soft", at=0, dl=300)
    f.dot(*Pp, r=11, f="gold", at=0, dl=600)
    f.text(Pp[0] + 16, Pp[1], "P", z=26, c="gold", at=0, dl=700, b=800, a="s")
    arrow(f, O, Pp, 1, c="gold", w=6)
    mid = (O[0] + (A[0] - O[0]) / 3, O[1] + (A[1] - O[1]) / 3)
    arrow(f, O, mid, 2, c="teal", w=5)
    arrow(f, mid, Pp, 2, c="coral", w=5, dl=600)
    f.text((O[0] + mid[0]) / 2, (O[1] + mid[1]) / 2 + 40, "{1/3}⃗{a}", z=24, c="teal", at=2, dl=300, b=800)
    f.text((mid[0] + Pp[0]) / 2 + 22, (mid[1] + Pp[1]) / 2 + 10, "{2/3}⃗{b}", z=24, c="coral", at=2, dl=900, b=800, a="s")
    U.ex("h3-3-17", "점 P가 선분 AB를 2 : 1로 내분할 때, ⃗{OP}를 ⃗{a} = ⃗{OA}, ⃗{b} = ⃗{OB}로 나타내 보자.", "내분점 — ⃗{p} = {m⃗{b} + n⃗{a}/m + n}, 계수의 합은 1",
         [L("P는 AB를 2 : 1로 내분", memo="A에서 2칸, B에서 1칸"),
          L("⃗{OP} = {2⃗{b} + ⃗{a}/3}"),
          L("⃗{OP} = {1/3}⃗{a} + {2/3}⃗{b}", memo="계수의 합 {1/3} + {2/3} = 1")],
         "{1/3}⃗{a} + {2/3}⃗{b}", f.out(), at=("b4", 0))

    # ── 18 벡터의 성분 ─────────────────────────────────────────
    f = Fig()
    P = Plane(f, (0, 6), (0, 7), box=(70, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.pt(1, 2, at="q", f="ink", r=10, label="A(1, 2)", pos="w", z=22)
    P.pt(4, 6, at="q", f="ink", r=10, label="B(4, 6)", pos="e", z=22)
    arrow(f, P.P(1, 2), P.P(4, 6), "q", c="gold", w=5)
    seg(P, (1, 2), (4, 2), 0, c="teal", w=5, dr=True)
    f.text(P.X(2.5), P.Y(2) + 32, "4 − 1 = 3", z=22, c="teal", at=0, dl=500, b=800)
    seg(P, (4, 2), (4, 6), 0, c="coral", w=5, dr=True, dl=700)
    f.text(P.X(4) + 14, P.Y(4) + 8, "6 − 2 = 4", z=22, c="coral", at=0, dl=1100, b=800, a="s")
    f.text(P.X(2.3), P.Y(4.3), "5", z=34, c="gold", at=1, b=800, a="e")
    U.ex("h3-3-18", "두 점 A(1, 2), B(4, 6)에 대해 ⃗{AB}의 성분과 크기를 구해 보자.", "성분 = (끝 − 시작), 크기는 피타고라스",
         [L("⃗{AB} = (4 − 1, 6 − 2) = (3, 4)", memo="가로 3, 세로 4"),
          L("|⃗{AB}| = √{3^{2} + 4^{2}} = 5")],
         "(3, 4), 크기 5", f.out(), at=("b3", 1))

    # ── 19 내적 — 수직 판정 ─────────────────────────────────────
    f = Fig()
    P = Plane(f, (-2, 3), (-1, 3), box=(60, 80, 620, 620))
    P.axes(at="q", grid=1, lab_step=1)
    arrow(f, P.P(0, 0), P.P(2, 1), "q", c="teal")
    f.text(P.X(2.1), P.Y(1) + 6, "⃗{a} = (2, 1)", z=22, c="teal", at="q", b=800, a="s")
    arrow(f, P.P(0, 0), P.P(-1, 2), "q", c="coral")
    f.text(P.X(-1.1), P.Y(2) - 12, "⃗{b} = (−1, 2)", z=22, c="coral", at="q", b=800, a="e")
    f.text(P.X(1.5), P.Y(2.6), "2 × (−1) + 1 × 2 = 0", z=24, c="gold", at=0, b=800)
    angle_mark(f, P.P(0, 0), P.P(2, 1), P.P(-1, 2), r=34, at=1, c="ink")
    f.text(P.X(0.4), P.Y(-0.6), "θ = 90°", z=26, c="gold", at=1, dl=400, b=800)
    U.ex("h3-3-19", "두 벡터 ⃗{a} = (2, 1), ⃗{b} = (−1, 2)가 수직인지 내적으로 알아보자.", "⃗{a} · ⃗{b} = a_{1}b_{1} + a_{2}b_{2} = |⃗{a}||⃗{b}|cos θ — 0이면 수직",
         [L("⃗{a} · ⃗{b} = 2 × (−1) + 1 × 2 = 0", memo="성분끼리 곱해 더한다"),
          L("cos θ = 0 → θ = 90°", memo="수직")],
         "수직", f.out(), at=("b4", 0))

    # ── 20 직선의 벡터방정식 ───────────────────────────────────
    f = Fig()
    P = Plane(f, (-2, 6), (-1, 4), box=(50, 100, 620, 560))
    P.axes(at="q", grid=1, lab_step=1)
    arrow(f, P.P(0, 0), P.P(1, 1), "q", c="soft", w=3.5)
    P.pt(1, 1, at="q", f="ink", r=10, label="A(1, 1)", pos="nw", z=22)
    arrow(f, P.P(1, 1), P.P(3, 2), 0, c="teal")
    f.text(P.X(2), P.Y(1.5) + 32, "⃗{d} = (2, 1)", z=22, c="teal", at=0, dl=600, b=800)
    cp = arrow(f, P.P(1, 1), P.P(3, 2), 1, c="teal", dr=False)
    slide(cp, 1, dx=P.X(3) - P.X(1), dy=P.Y(2) - P.Y(1), dl=300)
    bk = arrow(f, P.P(1, 1), P.P(3, 2), 1, c="teal", dr=False, dl=600)
    bk["mv"] = {"at": 1, "r": 180, "cx": R1(P.X(1)), "cy": R1(P.Y(1)), "dl": 900}
    for k, (x, y, lab, pos) in enumerate(((3, 2, "t = 1", "se"), (5, 3, "t = 2", "se"), (-1, 0, "t = −1", "nw"))):
        P.pt(x, y, at=1, f="coral", r=10, label=lab, pos=pos, z=20, c="coral", dl=1500 + 200 * k)
    P.lineq(0.5, 0.5, at=2, c="gold", w=4)
    U.ex("h3-3-20", "점 A(1, 1)을 지나고 방향벡터가 ⃗{d} = (2, 1)인 직선을 그리고, 방정식을 구해 보자.", "⃗{p} = ⃗{a} + t⃗{d} — A에서 ⃗{d}를 t배씩 더한 점들",
         [L("점 A(1, 1), 방향벡터 ⃗{d} = (2, 1)"),
          L("t = 1: (3, 2), t = 2: (5, 3), t = −1: (−1, 0)", memo="⃗{d}를 t배"),
          L("x = 1 + 2t, y = 1 + t → {x − 1/2} = y − 1", memo="t를 지운다 — 기울기 {1/2}")],
         "{x − 1/2} = y − 1", f.out(), at=("b2", -1))

    # ── 21 평면의 방정식 — 법선벡터 ─────────────────────────────
    f = Fig()
    f.poly([(60, 520), (440, 520), (610, 360), (230, 360)], at="q", c="ink", w=3, f="sky", fo=0.15)
    Ap = (330, 450)
    f.dot(*Ap, r=10, f="ink", at="q")
    f.text(Ap[0] - 16, Ap[1] + 30, "A(1, 0, 0)", z=22, at="q", b=800, a="e")
    arrow(f, Ap, (330, 170), 0, c="coral", w=6)
    f.text(346, 190, "⃗{n} = (1, 2, 2)", z=24, c="coral", at=0, dl=600, b=800, a="s")
    pts = ((480, 470), (230, 410), (430, 390))
    for k, Qp in enumerate(pts):
        arrow(f, Ap, Qp, 1, c="teal", w=4, dl=400 * k)
        f.text(Qp[0] + 10, Qp[1] + 26, "P", z=20, c="teal", at=1, dl=400 * k + 300, b=800)
    right_mark(f, Ap, (0, -1), unit(Ap, pts[0]), s=18, at=1, dl=1300)
    f.text(CX, 620, "⃗{n} · ⃗{AP} = 0", z=30, c="gold", at=1, dl=1400, b=800)
    f.text(CX, 90, "x + 2y + 2z = 1", z=32, c="gold", at=2, b=800)
    U.ex("h3-3-21", "점 A(1, 0, 0)을 지나고 법선벡터가 ⃗{n} = (1, 2, 2)인 평면의 방정식을 구해 보자.", "평면 위 어느 점 P에 대해서도 ⃗{n} ⊥ ⃗{AP} — 내적 0",
         [L("평면 위의 점 P(x, y, z)에 대해 ⃗{AP} = (x − 1, y, z)", memo="끝 − 시작"),
          L("⃗{n} · ⃗{AP} = 0 → (x − 1) + 2y + 2z = 0", memo="평면 위 모든 화살표와 수직"),
          L("x + 2y + 2z = 1", memo="계수 (1, 2, 2)가 곧 법선벡터")],
         "x + 2y + 2z = 1", f.out(), at=("b3", 1))
