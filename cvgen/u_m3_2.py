# 중3-2 — 삼각비 · 원의 성질 · 통계(대푯값 · 산포도 · 산점도)
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, lab_pts, seg_ticks, rot


def mid(A, B):
    return ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)


def off(A, B, d):
    mx, my = mid(A, B)
    L_ = math.hypot(B[0] - A[0], B[1] - A[1])
    return (mx + (B[1] - A[1]) / L_ * d, my - (B[0] - A[0]) / L_ * d)


def on_c(O, R, deg):
    return (O[0] + R * math.cos(math.radians(deg)), O[1] - R * math.sin(math.radians(deg)))


def build(U):
    # ── 01 삼각비 ─────────────────────────────────────────────
    f = Fig()
    B, C, A = (90, 520), (490, 520), (490, 220)
    f.poly([A, B, C], at="q", c="ink", w=3.5)
    angle_mark(f, C, A, B, r=30, at="q", c="ink")
    angle_mark(f, B, C, A, r=60, at="q", c="gold", fo=0.3)
    lab_pts(f, {"A": A, "B": B, "C": C}, at="q", z=28, off={"A": (18, -8), "B": (-18, 30), "C": (18, 30)})
    f.line(*A, *C, at=0, c="coral", w=7, dr=True)
    f.text(A[0] + 30, 380, "3", z=32, c="coral", at=0, dl=500, b=800)
    f.line(*B, *A, at=0, c="teal", w=7, dr=True, dl=700)
    f.text(*off(B, A, 30), "5", z=32, c="teal", at=0, dl=1200, b=800)
    f.line(*B, *C, at=1, c="gold", w=7, dr=True)
    f.text(290, 566, "4", z=32, c="gold", at=1, dl=500, b=800)
    f.text(220, 140, "cos B = {4/5}", z=32, c="gold", at=2, b=800)
    f.text(220, 220, "tan B = {3/4}", z=32, c="coral", at=2, dl=400, b=800)
    U.ex("m3-2-01", "∠C = 90°인 직각삼각형 ABC에서 sin B = {3/5}일 때, cos B와 tan B의 값을 구해 보자.", "삼각비 하나로 직각삼각형을 그린 뒤 피타고라스로 나머지 변",
         [L("sin B = {3/5}", memo="높이 3, 빗변 5인 직각삼각형"),
          L("(밑변)^{2} = 5^{2} − 3^{2} = 16 → 밑변 4", memo="피타고라스 정리"),
          L("cos B = {4/5}, tan B = {3/4}", memo="밑변 ÷ 빗변, 높이 ÷ 밑변")],
         "cos B = {4/5}, tan B = {3/4}", f.out(), at=("b4", 1))

    # ── 02 특수한 각의 삼각비 — 정삼각형의 반쪽 ─────────────────
    f = Fig()
    L0_, R0_ = (100, 560), (500, 560)
    T = (300, 560 - 400 * math.sqrt(3) / 2)
    M = (300, 560)
    f.poly([L0_, R0_, T], at="q", c="ink", w=3.5)
    for P1, P2 in ((L0_, R0_), (R0_, T), (T, L0_)):
        seg_ticks(f, P1, P2, 1, at="q", c="ink")
    f.text(*off(T, L0_, 30), "2", z=30, at="q", b=800)
    f.text(*off(R0_, T, 30), "2", z=30, at="q", b=800, un=0)
    f.line(*T, *M, at=0, c="ink", w=3, d=True, dr=True)
    half = f.poly([M, R0_, T], at=0, c="soft", w=3, f="soft", fo=0.15, dl=600)
    slide(half, 0, dx=90, dl=900)
    f.text(200, 600, "1", z=30, c="coral", at=0, dl=1500, b=800)
    f.text(328, 420, "√{3}", z=30, c="teal", at=0, dl=1700, b=800, a="s")
    angle_mark(f, M, T, L0_, r=26, at=0, c="ink", dl=1600)
    f.arc(*T, 64, 240, 270, at=1, c="coral", sw=3, f="coral", fo=0.4)
    f.text(T[0] - 22, T[1] + 96, "30°", z=24, c="coral", at=1, dl=300, b=800)
    f.line(*L0_, *M, at=1, c="coral", w=7, dr=True, dl=300)
    f.text(540, 150, "sin 30° = {1/2}", z=28, c="coral", at=1, dl=800, b=800)
    f.text(540, 225, "cos 30° = {√{3}/2}", z=28, c="coral", at=1, dl=1100, b=800)
    f.arc(*L0_, 64, 0, 60, at=2, c="teal", sw=3, f="teal", fo=0.4)
    f.text(L0_[0] + 90, L0_[1] - 30, "60°", z=24, c="teal", at=2, dl=300, b=800)
    f.line(*M, *T, at=2, c="teal", w=7, dr=True, dl=300)
    f.text(540, 330, "sin 60° = {√{3}/2}", z=28, c="teal", at=2, dl=800, b=800)
    f.text(540, 405, "cos 60° = {1/2}", z=28, c="teal", at=2, dl=1100, b=800)
    U.ex("m3-2-02", "한 변이 2인 정삼각형을 반으로 잘라 30°, 60°의 삼각비를 구해 보자.", "정삼각형의 반쪽 — 변 1, 높이 √{3}, 빗변 2",
         [L("정삼각형을 반으로 → 1, √{3}, 2", memo="높이는 √{2^{2} − 1^{2}} = √{3}"),
          L("sin 30° = {1/2}, cos 30° = {√{3}/2}", memo="30°의 마주 보는 변은 1"),
          L("sin 60° = {√{3}/2}, cos 60° = {1/2}", memo="60°의 마주 보는 변은 √{3}")],
         "sin 30° = {1/2}, sin 60° = {√{3}/2}", f.out(), at=("b4", 2))

    # ── 03 사분원에서 읽는 삼각비 ───────────────────────────────
    f = Fig()
    O, Rr, x = (110, 570), 400, 40
    f.poly([(O[0] + Rr * math.cos(math.radians(a)), O[1] - Rr * math.sin(math.radians(a))) for a in range(0, 91, 3)], at="q", c="ink", w=3, z=False)
    f.line(O[0], O[1], O[0] + Rr + 60, O[1], at="q", c="ink", w=3, ar=1)
    f.line(O[0], O[1], O[0], O[1] - Rr - 40, at="q", c="ink", w=3, ar=1)
    f.text(O[0] + Rr, O[1] + 34, "1", z=26, at="q", b=800)
    f.text(O[0] - 18, O[1] - Rr + 8, "1", z=26, at="q", b=800, a="e")
    f.text(O[0] - 14, O[1] + 30, "O", z=24, c="soft", at="q", a="e")
    P = on_c(O, Rr, x)
    rr = f.line(*O, O[0] + Rr, O[1], at=0, c="ink", w=4.5)
    rr["mv"] = {"at": 0, "r": -x, "cx": O[0], "cy": O[1], "dl": 200}
    f.arc(*O, 70, 0, x, at=0, c="gold", sw=3, f="gold", fo=0.35, dl=300)
    f.text(O[0] + 100, O[1] - 28, "x", z=28, c="gold", at=0, dl=900, b=800)
    f.text(*off(O, P, 26), "1", z=26, at=0, dl=1100, b=800)
    f.line(P[0], O[1], *P, at=1, c="coral", w=7, dr=True)
    f.text(P[0] + 16, (O[1] + P[1]) / 2 + 10, "sin x", z=28, c="coral", at=1, dl=500, b=800, a="s")
    f.line(*O, P[0], O[1], at=2, c="teal", w=7, dr=True)
    f.text((O[0] + P[0]) / 2, O[1] + 40, "cos x", z=28, c="teal", at=2, dl=500, b=800)
    Tq = (O[0] + Rr, O[1] - Rr * math.tan(math.radians(x)))
    f.line(O[0] + Rr, O[1] + 10, O[0] + Rr, O[1] - Rr - 20, at=3, c="soft", w=2.5, d=True)
    f.line(*P, *Tq, at=3, c="ink", w=2.5, d=True, dl=200)
    f.line(O[0] + Rr, O[1], *Tq, at=3, c="gold", w=7, dr=True, dl=500)
    f.text(O[0] + Rr + 16, (O[1] + Tq[1]) / 2 + 10, "tan x", z=28, c="gold", at=3, dl=900, b=800, a="s")
    U.ex("m3-2-03", "반지름이 1인 사분원에서 각 x의 sin, cos, tan을 길이로 읽어 보자.", "빗변이 1이면 분모가 1 — 삼각비가 곧 선분의 길이",
         [L("빗변 = 반지름 = 1", memo="분모가 1"),
          L("sin x = (세로의 길이)", memo="높이 ÷ 1"),
          L("cos x = (가로의 길이)", memo="밑변 ÷ 1"),
          L("tan x = (접선 위의 길이)", memo="가로가 1인 곳에 세운 접선")],
         "sin x, cos x, tan x를 길이로 읽는다", f.out(), at=("b2", 2))

    # ── 04 삼각비의 활용 — 사다리 ───────────────────────────────
    f = Fig()
    u = 60
    foot, wallx = (340, 560), 520
    f.line(60, 560, 620, 560, at="q", c="ink", w=4)
    f.rect(wallx, 120, 30, 440, at="q", c="ink", sw=3, f="soft", fo=0.2)
    top = (wallx, 560 - 6 * u * math.sin(math.radians(60)))
    lad = f.line(foot[0], foot[1], foot[0], foot[1] - 6 * u, at="q", c="gold", w=8)
    lad["mv"] = {"at": "q", "r": 30, "cx": foot[0], "cy": foot[1], "dl": 900}
    f.text(380, 330, "6 m", z=28, c="gold", at="q", dl=1800, b=800, a="e")
    f.arc(*foot, 60, 0, 60, at=0, c="teal", sw=3, f="teal", fo=0.35)
    f.text(foot[0] + 84, foot[1] - 26, "60°", z=26, c="teal", at=0, dl=300, b=800)
    f.line(wallx - 4, 560, wallx - 4, top[1], at=0, c="coral", w=7, dr=True, dl=600)
    f.text(wallx + 42, (560 + top[1]) / 2, "높이", z=24, c="coral", at=0, dl=1200, b=800, a="s")
    f.text(wallx + 42, (560 + top[1]) / 2 + 46, "3√{3} m", z=28, c="coral", at=1, b=800, a="s")
    U.ex("m3-2-04", "길이 6 m인 사다리를 지면과 60°를 이루도록 벽에 기대었다. 사다리 끝이 닿는 높이를 구해 보자.", "빗변과 각을 알 때 높이는 (빗변) × sin",
         [L("높이 = 6 × sin 60°", memo="사다리가 빗변"),
          L("6 × {√{3}/2} = 3√{3}", memo="sin 60° = {√{3}/2}")],
         "3√{3} m", f.out(), at=("b3", 1))

    # ── 05 삼각비의 활용 — 넓이 ─────────────────────────────────
    f = Fig()
    B, C = (90, 540), (570, 540)
    A = (90 + 360 * math.cos(math.radians(30)), 540 - 360 * math.sin(math.radians(30)))
    H = (A[0], 540)
    f.poly([A, B, C], at="q", c="ink", w=3.5)
    lab_pts(f, {"A": A, "B": B, "C": C}, at="q", z=28, off={"A": (0, -16), "B": (-18, 30), "C": (18, 30)})
    f.text(*off(B, A, 26), "6", z=28, at="q", b=800)
    f.text(330, 586, "8", z=28, at="q", b=800)
    f.arc(*B, 80, 0, 30, at="q", c="gold", sw=3, f="gold", fo=0.35)
    f.text(B[0] + 112, B[1] - 18, "30°", z=24, c="gold", at="q", b=800)
    f.line(*A, *H, at=0, c="coral", w=5, d=True, dr=True)
    angle_mark(f, H, A, C, r=22, at=0, c="coral", dl=600)
    f.text(A[0] + 16, (A[1] + 540) / 2 + 10, "3", z=30, c="coral", at=0, dl=800, b=800, a="s")
    f.text(500, 260, "높이 = 6 × sin 30°", z=24, c="coral", at=0, dl=1000, b=800)
    f.poly([A, B, C], at=1, c="none", f="gold", fo=0.3)
    f.text(300, 490, "S = 12", z=34, c="gold", at=1, dl=500, b=800)
    U.ex("m3-2-05", "두 변의 길이가 6, 8이고 그 끼인각이 30°인 삼각형의 넓이를 구해 보자.", "높이 대신 sin — S = {1/2}ab sin x",
         [L("높이 = 6 × {1/2} = 3", memo="sin 30° = {1/2}"),
          L("S = {1/2} × 8 × 3 = 12")],
         "12", f.out(), at=("b3", 1))

    # ── 06 원의 현 ─────────────────────────────────────────────
    f = Fig()
    O, u = (330, 300), 44
    Rr = 5 * u
    f.circ(*O, Rr, at="q", c="ink", sw=3)
    f.dot(*O, r=8, f="ink", at="q")
    f.text(O[0] - 18, O[1] - 12, "O", z=26, at="q", b=800, a="e")
    yc = O[1] + 3 * u
    Ap, Bp, Mp = (O[0] - 4 * u, yc), (O[0] + 4 * u, yc), (O[0], yc)
    f.line(*Ap, *Bp, at="q", c="ink", w=4)
    f.line(*O, *Mp, at="q", c="soft", w=3, d=True)
    f.text(O[0] - 14, (O[1] + yc) / 2 + 10, "3", z=28, at="q", b=800, a="e")
    f.poly([O, Mp, Bp], at=0, c="none", f="gold", fo=0.25)
    f.line(*O, *Bp, at=0, c="teal", w=5, dr=True)
    f.text(*off(O, Bp, 26), "5", z=28, c="teal", at=0, dl=500, b=800)
    angle_mark(f, Mp, O, Bp, r=22, at=0, c="ink", dl=300)
    f.line(*Mp, *Bp, at=1, c="coral", w=7, dr=True)
    f.text((Mp[0] + Bp[0]) / 2, yc + 40, "4", z=30, c="coral", at=1, dl=500, b=800)
    cp = f.line(*Mp, *Bp, at=2, c="coral", w=7)
    cp["mv"] = {"at": 2, "r": 180, "cx": Mp[0], "cy": Mp[1], "dl": 200}
    f.text((Mp[0] + Ap[0]) / 2, yc + 40, "4", z=30, c="coral", at=2, dl=1100, b=800)
    f.text(O[0], yc + 120, "현의 길이 8", z=32, c="gold", at=2, dl=1300, b=800)
    U.ex("m3-2-06", "반지름이 5인 원에서 중심으로부터 거리가 3인 현의 길이를 구해 보자.", "중심에서 내린 수선은 현을 이등분 — 반지름 · 거리 · 현의 절반으로 직각삼각형",
         [L("(현의 절반)^{2} = 5^{2} − 3^{2} = 16", memo="피타고라스 정리"),
          L("현의 절반 = 4"),
          L("현의 길이 = 4 × 2 = 8", memo="수선이 현을 이등분")],
         "8", f.out(), at=("b4", 1))

    # ── 07 원의 접선 ───────────────────────────────────────────
    f = Fig()
    O, u = (200, 340), 50
    P = (O[0] + 5 * u, O[1])
    th = math.degrees(math.acos(3 / 5))
    T1, T2 = on_c(O, 3 * u, th), on_c(O, 3 * u, -th)
    f.circ(*O, 3 * u, at="q", c="ink", sw=3)
    f.dot(*O, r=8, f="ink", at="q")
    f.dot(*P, r=9, f="ink", at="q")
    lab_pts(f, {"O": O, "P": P}, at="q", z=28, off={"O": (-14, 30), "P": (20, 10)})
    f.line(*O, *P, at="q", c="soft", w=3, d=True)
    f.text((O[0] + P[0]) / 2 + 40, O[1] + 34, "5", z=28, at="q", b=800)
    f.line(*P, *T1, at=0, c="teal", w=5, dr=True)
    f.line(*O, *T1, at=0, c="coral", w=4, dr=True, dl=500)
    angle_mark(f, T1, O, P, r=22, at=0, c="ink", dl=900)
    f.text(T1[0], T1[1] - 20, "A", z=28, at=0, b=800)
    f.poly([O, T1, P], at=1, c="none", f="gold", fo=0.25)
    f.text(*off(O, T1, 22), "3", z=28, c="coral", at=1, dl=200, b=800)
    f.text(*off(T1, P, 24), "4", z=30, c="teal", at=1, dl=500, b=800)
    f.line(*P, *T2, at=2, c="teal", w=5, dr=True)
    f.line(*O, *T2, at=2, c="coral", w=3, d=True, dr=True, dl=300)
    f.text(T2[0], T2[1] + 40, "B", z=28, at=2, b=800)
    f.text(*off(P, T2, 24), "4", z=30, c="teal", at=2, dl=600, b=800)
    f.text(540, 560, "PA = PB = 4", z=30, c="gold", at=2, dl=900, b=800)
    U.ex("m3-2-07", "반지름이 3인 원의 중심 O에서 5만큼 떨어진 점 P에서 그은 접선의 길이를 구해 보자.", "접선은 접점의 반지름과 수직 — 직각삼각형이 생긴다",
         [L("OA ⊥ PA", memo="접선과 반지름은 수직"),
          L("PA^{2} = 5^{2} − 3^{2} = 16 → PA = 4", memo="빗변 OP = 5"),
          L("PA = PB = 4", memo="한 점에서 그은 두 접선의 길이는 같다")],
         "4", f.out(), at=("b2", 2))

    # ── 08 직각삼각형의 내접원 ─────────────────────────────────
    f = Fig()
    u = 100
    C, B, A = (120, 540), (520, 540), (120, 240)
    I = (C[0] + u, C[1] - u)
    D, E = (I[0], C[1]), (C[0], I[1])
    F = (A[0] + 0.8 * 2 * u, A[1] + 0.6 * 2 * u)
    f.poly([A, B, C], at="q", c="ink", w=3.5)
    f.circ(*I, u, at="q", c="sky", sw=3)
    lab_pts(f, {"A": A, "B": B, "C": C}, at="q", z=28, off={"A": (-18, -6), "B": (18, 30), "C": (-18, 30)})
    f.text(C[0] - 20, (A[1] + C[1]) / 2 + 10, "3", z=28, at="q", b=800, a="e")
    f.text((C[0] + B[0]) / 2 + 60, C[1] + 40, "4", z=28, at="q", b=800)
    f.text(*off(A, B, -30), "5", z=28, at="q", b=800)
    f.rect(C[0], I[1], u, u, at=0, c="gold", sw=3, f="gold", fo=0.3)
    f.text(C[0] + u / 2, C[1] + 34, "r", z=28, c="gold", at=0, dl=400, b=800)
    f.text(C[0] - 20, I[1] + u / 2 + 10, "r", z=28, c="gold", at=0, dl=500, b=800, a="e")
    f.line(*D, *B, at=1, c="teal", w=7, dr=True)
    f.line(*F, *B, at=1, c="teal", w=7, dr=True, dl=300)
    f.line(*A, *E, at=1, c="coral", w=7, dr=True, dl=700)
    f.line(*A, *F, at=1, c="coral", w=7, dr=True, dl=1000)
    f.text((D[0] + B[0]) / 2, C[1] - 18, "4 − r", z=24, c="teal", at=1, dl=600, b=800)
    f.text(*off(F, B, 28), "4 − r", z=24, c="teal", at=1, dl=700, b=800)
    f.text(A[0] + 18, (A[1] + E[1]) / 2 + 8, "3 − r", z=24, c="coral", at=1, dl=1100, b=800, a="s")
    f.text(*off(A, F, 30), "3 − r", z=24, c="coral", at=1, dl=1300, b=800)
    f.text(450, 250, "r = 1", z=36, c="gold", at=2, b=800)
    U.ex("m3-2-08", "세 변의 길이가 3, 4, 5인 직각삼각형의 내접원의 반지름을 구해 보자.", "같은 꼭짓점에서 그은 두 접선은 같다 — 직각 옆은 한 변이 r인 정사각형",
         [L("직각 꼭짓점 옆의 접선 = r", memo="한 변이 r인 정사각형"),
          L("5 = (3 − r) + (4 − r)", memo="빗변을 두 꼭짓점의 접선으로 나누면"),
          L("r = {3 + 4 − 5/2} = 1", memo="r = {a + b − c/2}")],
         "1", f.out(), at=("b3", 1), sub={"r": 1})

    # ── 09 원주각 ──────────────────────────────────────────────
    f = Fig()
    O, Rr = (330, 330), 230
    A, B = on_c(O, Rr, 220), on_c(O, Rr, 320)
    f.circ(*O, Rr, at="q", c="ink", sw=3)
    f.dot(*O, r=8, f="ink", at="q")
    f.dot(*A, r=9, f="ink", at="q")
    f.dot(*B, r=9, f="ink", at="q")
    lab_pts(f, {"A": A, "B": B}, at="q", z=28, off={"A": (-20, 26), "B": (20, 26)})
    f.text(O[0] + 18, O[1] - 14, "O", z=26, at="q", b=800, a="s")
    f.line(*O, *A, at=0, c="gold", w=4, dr=True)
    f.line(*O, *B, at=0, c="gold", w=4, dr=True, dl=300)
    f.arc(*O, 50, 220, 320, at=0, c="gold", sw=3, f="gold", fo=0.35, dl=600)
    f.text(O[0], O[1] + 92, "100°", z=26, c="gold", at=0, dl=900, b=800)
    for k, (deg, col) in enumerate(((100, "teal"), (145, "coral"), (45, "sky"))):
        at = 1 if k == 0 else 2
        Pp = on_c(O, Rr, deg)
        dl = 0 if k == 0 else 800 * (k - 1)
        f.dot(*Pp, r=10, f=col, at=at, dl=dl)
        f.line(*Pp, *A, at=at, c=col, w=3.5, dr=True, dl=dl + 100)
        f.line(*Pp, *B, at=at, c=col, w=3.5, dr=True, dl=dl + 300)
        angle_mark(f, Pp, A, B, r=42, at=at, c=col, label="50°", z=24, dl=dl + 600)
    U.ex("m3-2-09", "호 AB에 대한 중심각이 100°일 때, 호 AB에 대한 원주각의 크기를 구해 보자.", "원주각은 같은 호에 대한 중심각의 절반",
         [L("∠AOB = 100°", memo="중심각"),
          L("원주각 = {1/2} × 100° = 50°"),
          L("P가 호 위를 움직여도 50°", memo="같은 호에 대한 원주각은 모두 같다")],
         "50°", f.out(), at=("b2", -1))

    # ── 10 원에 내접하는 사각형 ────────────────────────────────
    f = Fig()
    O, Rr = (330, 330), 230
    A, B, C, D = on_c(O, Rr, 180), on_c(O, Rr, 285), on_c(O, Rr, 0), on_c(O, Rr, 75)
    f.circ(*O, Rr, at="q", c="ink", sw=3)
    f.poly([A, B, C, D], at="q", c="ink", w=3.5)
    lab_pts(f, {"A": A, "B": B, "C": C, "D": D}, at="q", z=28, off={"A": (-20, 10), "B": (8, 30), "C": (20, 10), "D": (6, -14)})
    angle_mark(f, A, B, D, r=50, at="q", c="teal", label="75°", z=24)
    f.dot(*O, r=7, f="ink", at=0)
    f.line(*O, *B, at=0, c="teal", w=3, d=True, dr=True)
    f.line(*O, *D, at=0, c="teal", w=3, d=True, dr=True, dl=200)
    f.arc(*O, 60, -75, 75, at=0, c="teal", sw=3, f="teal", fo=0.3, dl=500)
    f.text(O[0] + 92, O[1] + 10, "150°", z=24, c="teal", at=0, dl=800, b=800)
    f.arc(*O, 46, 75, 285, at=1, c="coral", sw=3, f="coral", fo=0.3)
    f.text(O[0] - 84, O[1] + 10, "210°", z=24, c="coral", at=1, dl=500, b=800)
    angle_mark(f, C, D, B, r=50, at=2, c="coral", label="105°", z=24)
    U.ex("m3-2-10", "원에 내접하는 사각형 ABCD에서 ∠A = 75°일 때, ∠C의 크기를 구해 보자.", "마주 보는 두 원주각이 바라보는 호를 합치면 원 전체 — 두 각의 합은 180°",
         [L("∠A = 75° → 호 BCD의 중심각 150°", memo="중심각은 원주각의 2배"),
          L("호 BAD의 중심각 = 360° − 150° = 210°"),
          L("∠C = {1/2} × 210° = 105°", memo="∠A + ∠C = 180°")],
         "105°", f.out(), at=("b2", 2))

    # ── 11 접선과 현이 이루는 각 ───────────────────────────────
    f = Fig()
    O, Rr = (330, 300), 200
    P = on_c(O, Rr, 270)
    A = on_c(O, Rr, 50)
    f.circ(*O, Rr, at="q", c="ink", sw=3)
    f.line(90, P[1], 600, P[1], at="q", c="ink", w=3.5)
    f.line(*P, *A, at="q", c="ink", w=3.5)
    lab_pts(f, {"P": P, "A": A}, at="q", z=28, off={"P": (0, 36), "A": (18, -6)})
    f.arc(*P, 56, 0, 70, at="q", c="gold", sw=3, f="gold", fo=0.4)
    f.text(P[0] + 92, P[1] - 18, "70°", z=24, c="gold", at="q", b=800)
    for k, (deg, col) in enumerate(((150, "teal"), (205, "coral"), (240, "sky"))):
        at = 1 if k == 0 else 2
        Bp = on_c(O, Rr, deg)
        dl = 0 if k == 0 else 900 * (k - 1)
        f.dot(*Bp, r=10, f=col, at=at, dl=dl)
        f.line(*Bp, *P, at=at, c=col, w=3.5, dr=True, dl=dl + 100)
        f.line(*Bp, *A, at=at, c=col, w=3.5, dr=True, dl=dl + 300)
        angle_mark(f, Bp, P, A, r=44, at=at, c=col, label="70°" if k == 0 else None, z=24, dl=dl + 600)
        if k == 0:
            f.text(Bp[0] - 18, Bp[1] - 14, "B", z=28, c=col, at=at, dl=dl, b=800, a="e")
    f.text(200, 640, "B가 P에 가까워지면 BP → 접선", z=24, c="sky", at=2, dl=2000, b=800)
    U.ex("m3-2-11", "점 P에서 원에 접하는 접선과 현 PA가 이루는 각이 70°일 때, 호 PA에 대한 원주각 ∠PBA의 크기를 구해 보자.", "접선과 현이 이루는 각 = 그 각 안의 호에 대한 원주각",
         [L("접선과 현 PA가 이루는 각 = 70°"),
          L("∠PBA = 70°", memo="호 PA에 대한 원주각"),
          L("B가 어디 있든 70°", memo="B가 P에 다가가면 현 BP가 접선이 된다")],
         "70°", f.out(), at=("b2", 2))

    # ── 12 대푯값 — 중앙값 ─────────────────────────────────────
    f = Fig()
    vals = [7, 2, 9, 5]
    xs = [150, 270, 390, 510]
    srt = sorted(vals)
    for k, v in enumerate(vals):
        r_ = f.rect(xs[k] - 46, 150, 92, 110, at="q", c="ink", sw=3, rx=12, f="teal" if v not in (5, 7) else "gold", fo=0.25, dl=120 * k)
        t = f.text(xs[k], 222, str(v), z=48, at="q", dl=120 * k + 60, b=800)
        tx = xs[srt.index(v)]
        if tx != xs[k]:
            for el in (r_, t):
                el["mv"] = {"at": 0, "dx": tx - xs[k], "dl": 200 + 150 * k}
    f.text(CX, 110, "작은 값부터", z=24, c="soft", at=0, dl=300, b=800)
    f.rect(214, 132, 232, 146, at=1, c="gold", sw=4, rx=16, d=True)
    f.text(CX, 320, "가운데 두 값", z=26, c="gold", at=1, dl=300, b=800)
    nl = NL(f, 0, 10, y=500, x0=60, x1=600, step=1, lab_step=1, z=22, at=2)
    f.dot(nl.X(5), 500, r=10, f="gold", at=2, dl=300)
    f.dot(nl.X(7), 500, r=10, f="gold", at=2, dl=400)
    f.line(nl.X(5), 470, nl.X(7), 470, at=2, c="gold", w=3, ar=2, dl=600)
    f.dot(nl.X(6), 500, r=13, f="coral", at=2, dl=1100)
    f.text(nl.X(6), 440, "6", z=36, c="coral", at=2, dl=1200, b=800)
    U.ex("m3-2-12", "자료 7, 2, 9, 5의 중앙값을 구해 보자.", "작은 값부터 정렬 — 짝수 개면 가운데 두 값의 평균",
         [L("2, 5, 7, 9", memo="크기순으로 다시 세우기"),
          L("가운데 두 값 5와 7", memo="4개 — 짝수 개"),
          L("중앙값 = {5 + 7/2} = 6")],
         "6", f.out(), at=("b3", 1))

    # ── 13 산포도 — 편차의 제곱 ─────────────────────────────────
    f = Fig()
    nl = NL(f, 0, 10, y=430, x0=60, x1=580, step=1, lab_step=1, z=22)
    u = nl.X(1) - nl.X(0)
    for k, v in enumerate((2, 4, 6, 8)):
        f.dot(nl.X(v), 430, r=11, f="teal", at="q", dl=100 * k)
    tri = f.poly([(nl.X(5), 440), (nl.X(5) - 16, 470), (nl.X(5) + 16, 470)], at=0, c="gold", w=3, f="gold", fo=0.7)
    f.line(nl.X(5), 90, nl.X(5), 430, at=0, c="gold", w=2.5, d=True, dl=300)
    f.text(nl.X(5), 510, "평균 5", z=26, c="gold", at=0, dl=500, b=800)
    for k, v in enumerate((2, 4, 6, 8)):
        d = v - 5
        col = "coral" if d < 0 else "teal"
        yy = 404 - 16 * k
        f.line(nl.X(5), yy, nl.X(v), yy, at=1, c=col, w=3.5, ar=1, dr=True, dl=250 * k, un=2)
        f.text(nl.X(v) + (-22 if d < 0 else 22), yy + 8, ("−" if d < 0 else "+") + str(abs(d)), z=22, c=col, at=1, dl=250 * k + 400, b=800, un=2, a="e" if d < 0 else "s")
    for k, (v, d) in enumerate(((2, -3), (4, -1), (6, 1), (8, 3))):
        side = abs(d) * u
        x0 = nl.X(v) if d < 0 else nl.X(5)
        big = abs(d) == 3
        y0 = 430 - side if big else 540
        f.rect(x0, y0, side, side, at=2, c="ink", sw=2.5, f="coral" if d < 0 else "teal", fo=0.3, dl=300 * k)
        f.text(x0 + side / 2, y0 + side / 2 + 10, str(d * d), z=30 if big else 22, c="coral" if d < 0 else "teal", at=2, dl=300 * k + 200, b=800)
    f.text(CX, 650, "(9 + 1 + 1 + 9) ÷ 4 = 5", z=28, c="gold", at=2, dl=1500, b=800)
    f.text(560, 120, "√{5}", z=40, c="gold", at=3, b=800)
    U.ex("m3-2-13", "자료 2, 4, 6, 8의 분산과 표준편차를 구해 보자.", "평균 → 편차 → 편차의 제곱의 평균(분산) → √(표준편차)",
         [L("평균 = {2 + 4 + 6 + 8/4} = 5"),
          L("편차: −3, −1, 1, 3", memo="(변량) − (평균)"),
          L("분산 = {9 + 1 + 1 + 9/4} = 5", memo="편차를 한 변으로 하는 정사각형 넓이의 평균"),
          L("표준편차 = √{5}")],
         "분산 5, 표준편차 √{5}", f.out(), at=("b3", 1))

    # ── 14 산점도 ──────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (45, 105), (45, 105), box=(80, 50, 620, 590))
    f.line(P.X(45), P.Y(45), P.X(105), P.Y(45), at="q", c="ink", w=3, ar=1)
    f.line(P.X(45), P.Y(45), P.X(45), P.Y(105), at="q", c="ink", w=3, ar=1)
    for v in (50, 60, 70, 80, 90, 100):
        f.text(P.X(v), P.Y(45) + 28, str(v), z=20, c="soft", at="q")
        f.text(P.X(45) - 8, P.Y(v) + 7, str(v), z=20, c="soft", at="q", a="e")
        f.line(P.X(v), P.Y(45), P.X(v), P.Y(105), at="q", c="soft", w=1, o=0.3)
        f.line(P.X(45), P.Y(v), P.X(105), P.Y(v), at="q", c="soft", w=1, o=0.3)
    f.text(P.X(103), P.Y(45) + 60, "수학", z=22, c="soft", at="q", b=700)
    f.text(P.X(45) + 36, P.Y(104) + 6, "과학", z=22, c="soft", at="q", b=700)
    pts = [(60, 70), (65, 60), (70, 80), (75, 75), (80, 70), (85, 90), (90, 85), (70, 65), (95, 100), (55, 50)]
    for k, (x, y) in enumerate(pts):
        P.pt(x, y, at="q", f="ink", r=9, dl=60 * k)
    f.line(*P.P(45, 45), *P.P(105, 105), at=0, c="gold", w=3.5, dr=True)
    f.text(P.X(100), P.Y(104), "y = x", z=24, c="gold", at=0, dl=800, b=800, a="e")
    f.poly([P.P(45, 45), P.P(45, 105), P.P(105, 105)], at=1, c="none", f="coral", fo=0.12)
    f.text(P.X(55), P.Y(97), "과학 > 수학", z=24, c="coral", at=1, dl=300, b=800)
    k2 = 0
    for (x, y) in pts:
        if y > x:
            k2 += 1
            P.pt(x, y, at=2, f="coral", r=13, dl=300 * k2)
            f.text(P.X(x) - 14, P.Y(y) - 16, str(k2), z=22, c="coral", at=2, dl=300 * k2 + 100, b=800, a="e")
    U.ex("m3-2-14", "산점도에서 과학 점수가 수학 점수보다 높은 학생은 몇 명일까?", "보조선 y = x를 긋고 그 위쪽의 점을 센다",
         [L("y = x인 직선을 긋는다", memo="두 점수가 같은 점들"),
          L("직선 위쪽 = 과학 점수가 더 높은 학생", memo="선 위의 점은 빼고"),
          L("4명")],
         "4명", f.out(), at=("b4", 1))
