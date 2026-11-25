# 중2-2 — 삼각형 · 사각형의 성질 · 도형의 닮음 · 피타고라스 정리 (경우의 수와 확률 m2-2-12 ~ 14 는 다른 방에서 — 여기서는 다루지 않는다)
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, lab_pts, seg_ticks, rot, poly_pts, oblique


def P_(A, B, t):
    return (A[0] + (B[0] - A[0]) * t, A[1] + (B[1] - A[1]) * t)


def mid(A, B):
    return P_(A, B, 0.5)


def off(A, B, d):
    """선분 AB 의 가운데에서 왼쪽 법선 쪽으로 d 만큼(글자 자리)"""
    mx, my = mid(A, B)
    L_ = math.hypot(B[0] - A[0], B[1] - A[1])
    nx, ny = (B[1] - A[1]) / L_, -(B[0] - A[0]) / L_
    return (mx + nx * d, my + ny * d)


def build(U):
    # ── 01 이등변삼각형 ─────────────────────────────────────
    f = Fig()
    B, C = (150, 520), (510, 520)
    A = (330, 520 - 180 * math.tan(math.radians(64)))
    f.poly([A, B, C], at="q", c="ink", w=4)
    lab_pts(f, {"A": A, "B": B, "C": C}, at="q", z=30, off={"A": (0, -18), "B": (-18, 32), "C": (18, 32)})
    seg_ticks(f, A, B, 1, at="q", c="ink")
    seg_ticks(f, A, C, 1, at="q", c="ink")
    aAB, aAC = dir_deg(A, B), dir_deg(A, C)
    f.arc(*A, 52, aAB, aAC, at="q", c="gold", sw=3, f="gold", fo=0.45)
    f.text(A[0], A[1] + 92, "52°", z=26, c="gold", at="q", b=800)
    f.arc(*B, 62, 0, 64, at=0, c="teal", sw=3, f="teal", fo=0.4)
    f.arc(*C, 62, 116, 180, at=0, c="teal", sw=3, f="teal", fo=0.4, dl=300)
    f.text(B[0] + 92, B[1] - 24, "?", z=28, c="teal", at=0, dl=500, b=800, un=2)
    f.text(C[0] - 92, C[1] - 24, "?", z=28, c="teal", at=0, dl=600, b=800, un=2)
    f.line(A[0] - 250, A[1], A[0] + 250, A[1], at=1, c="soft", w=3, d=True)
    for V, a0, a1, W in ((B, 0, 64, A), (C, 116, 180, A)):
        el = f.arc(*V, 62, a0, a1, at=1, c="teal", sw=3, f="teal", fo=0.4, dl=200 if V is B else 1000)
        m = mid(V, W)
        el["mv"] = {"at": 1, "r": 180, "cx": R1(m[0]), "cy": R1(m[1]), "dl": 300 if V is B else 1100}
    f.text(A[0] - 120, A[1] - 22, "64°", z=26, c="teal", at=2, dl=200, b=800)
    f.text(A[0] + 120, A[1] - 22, "64°", z=26, c="teal", at=2, dl=300, b=800)
    f.text(B[0] + 92, B[1] - 24, "64°", z=26, c="teal", at=2, dl=500, b=800)
    f.text(C[0] - 92, C[1] - 24, "64°", z=26, c="teal", at=2, dl=600, b=800)
    f.text(CX, 630, "(180° − 52°) ÷ 2 = 64°", z=30, c="gold", at=2, dl=900, b=800)
    U.ex("m2-2-01", "꼭지각의 크기가 52°인 이등변삼각형의 한 밑각의 크기를 구해 보자.", "두 밑각의 크기는 같다 — 밑각 = (180° − 꼭지각) ÷ 2",
         [L("∠B = ∠C", memo="이등변삼각형의 두 밑각"),
          L("52° + ∠B + ∠C = 180°", memo="세 각을 꼭짓점 A에 모으면 평각"),
          L("∠B = (180° − 52°) ÷ 2 = 64°")],
         "64°", f.out(), at=("b3", 1))

    # ── 02 직각삼각형의 외심 ─────────────────────────────────
    f = Fig()
    A, B, C = (120, 140), (120, 540), (420, 540)
    O = mid(A, C)
    f.poly([A, B, C], at="q", c="ink", w=4)
    angle_mark(f, B, A, C, r=34, at="q", c="ink")
    lab_pts(f, {"A": A, "B": B, "C": C}, at="q", z=30, off={"A": (-20, -6), "B": (-22, 30), "C": (20, 30)})
    f.text(92, 350, "8", z=30, at="q", b=800)
    f.text(270, 586, "6", z=30, at="q", b=800)
    f.text(*off(A, O, 34), "10", z=30, at="q", b=800)
    f.line(40, O[1], 470, O[1], at=0, c="teal", w=3, d=True, dr=True)
    f.line(O[0], 600, O[0], 180, at=0, c="coral", w=3, d=True, dr=True, dl=700)
    f.dot(*O, r=11, f="gold", at=0, dl=1500)
    f.text(O[0] + 22, O[1] - 16, "O", z=30, c="gold", at=0, dl=1600, b=800, a="s")
    for k, V in enumerate((A, B, C)):
        f.line(*O, *V, at=1, c="gold", w=4, dr=True, dl=300 * k)
    f.text(*off(O, B, 22), "5", z=26, c="gold", at=1, dl=900, b=800)
    f.circ(*O, 250, at=2, c="sky", sw=4)
    f.text(560, 120, "R = 5", z=34, c="sky", at=2, dl=900, b=800)
    U.ex("m2-2-02", "직각을 낀 두 변이 6, 8이고 빗변이 10인 직각삼각형의 외접원의 반지름을 구해 보자.", "직각삼각형의 외심은 빗변의 중점",
         [L("두 변의 수직이등분선이 빗변의 중점에서 만난다", memo="외심 O = 빗변 AC의 중점"),
          L("OA = OB = OC", memo="세 꼭짓점까지의 거리가 같다"),
          L("R = 10 ÷ 2 = 5", memo="외접원의 반지름 = 빗변의 절반")],
         "5", f.out(), at=("b4", 1))

    # ── 03 평행사변형 ─────────────────────────────────────────
    f = Fig()
    B, C = (100, 500), (480, 500)
    A = (100 + 260 * math.cos(math.radians(70)), 500 - 260 * math.sin(math.radians(70)))
    D = (A[0] + C[0] - B[0], A[1])
    f.poly([A, B, C, D], at="q", c="ink", w=4)
    lab_pts(f, {"A": A, "B": B, "C": C, "D": D}, at="q", z=30, off={"A": (-14, -16), "B": (-20, 30), "C": (18, 30), "D": (18, -12)})
    O = mid(A, C)
    f.arc(*A, 52, 250, 360, at="q", c="coral", sw=3, f="coral", fo=0.4)
    f.text(A[0] + 26, A[1] + 76, "110°", z=24, c="coral", at="q", b=800)
    f.line(*A, *C, at=0, c="soft", w=2, d=True)
    f.dot(*O, r=7, f="soft", at=0)
    cp = f.arc(*A, 52, 250, 360, at=0, c="coral", sw=3, f="coral", fo=0.4, dl=200)
    cp["mv"] = {"at": 0, "r": 180, "cx": R1(O[0]), "cy": R1(O[1]), "dl": 400}
    f.text(C[0] - 30, C[1] - 70, "110°", z=24, c="coral", at=0, dl=1400, b=800)
    f.arc(*B, 56, 0, 70, at=1, c="teal", sw=3, f="teal", fo=0.4)
    cb = f.arc(*B, 56, 0, 70, at=1, c="teal", sw=3, f="teal", fo=0.4, dl=400)
    slide(cb, 1, dx=A[0] - B[0], dy=A[1] - B[1], dl=600)
    E = (A[0] + 0.55 * (A[0] - B[0]), A[1] + 0.55 * (A[1] - B[1]))
    f.line(*A, *E, at=1, c="soft", w=3, d=True, dl=200)
    f.text(A[0] - 160, A[1] - 12, "110° + 70° = 180°", z=22, c="soft", at=1, dl=1600, b=800)
    f.text(B[0] + 84, B[1] - 24, "70°", z=24, c="teal", at=2, b=800)
    U.ex("m2-2-03", "평행사변형 ABCD에서 ∠A = 110°일 때, ∠C와 ∠B의 크기를 구해 보자.", "대각의 크기는 같고, 이웃한 두 내각의 합은 180°",
         [L("∠C = ∠A = 110°", memo="대각 — 대각선의 교점에 대해 반 바퀴 돌리면 겹친다"),
          L("∠A + ∠B = 180°", memo="AD ∥ BC — 같은 쪽 내각"),
          L("∠B = 180° − 110° = 70°")],
         "∠C = 110°, ∠B = 70°", f.out(), at=("b3", 1))

    # ── 04 여러 가지 사각형 ─────────────────────────────────
    f = Fig()

    def hinge(B, base, side, ang, at, cs, lab0, lab1, y_lab, dl=200, side_c=None):
        C = (B[0] + base, B[1])
        A = (B[0] + side * math.cos(math.radians(ang)), B[1] - side * math.sin(math.radians(ang)))
        D = (A[0] + base, A[1])
        A2 = (B[0], B[1] - side)
        f.line(*B, *C, at=at, c=cs[0], w=5)
        e1 = f.line(*B, *A, at=at, c=cs[1], w=5)
        e2 = f.line(*C, *D, at=at, c=cs[1], w=5)
        e3 = f.line(*A, *D, at=at, c=cs[0], w=5)
        return (A, B, C, D, A2), (e1, e2, e3)

    (A1, B1, C1, D1, A1b), es = hinge((70, 300), 250, 160, 65, "q", ("ink", "teal"), None, None, 0)
    f.text(520, 230, "평행사변형", z=28, at="q", b=800, un=0)
    for e in es[:2]:
        e["mv"] = {"at": 0, "r": -25, "cx": R1(e["x"]), "cy": R1(e["y"]), "dl": 300}
    slide(es[2], 0, dx=A1b[0] - A1[0], dy=A1b[1] - A1[1], dl=300)
    for V in ((70, 300), (320, 300), (70, 140), (320, 140)):
        pass
    f.poly([(70, 278), (92, 278), (92, 300)], at=0, c="gold", w=3, z=False, dl=1300)
    f.poly([(298, 300), (298, 278), (320, 278)], at=0, c="gold", w=3, z=False, dl=1400)
    f.text(520, 230, "직사각형", z=30, c="teal", at=0, dl=1300, b=800)
    f.text(520, 270, "한 내각 90°", z=22, c="soft", at=0, dl=1500, b=700)
    (A2, B2, C2, D2, A2b), es2 = hinge((70, 620), 200, 200, 60, 1, ("coral", "coral"), None, None, 0)
    f.text(520, 540, "마름모", z=30, c="coral", at=1, dl=500, b=800, un=2)
    f.text(520, 580, "네 변이 같다", z=22, c="soft", at=1, dl=700, b=700, un=2)
    for e in es2[:2]:
        e["mv"] = {"at": 2, "r": -30, "cx": R1(e["x"]), "cy": R1(e["y"]), "dl": 300}
    slide(es2[2], 2, dx=A2b[0] - A2[0], dy=A2b[1] - A2[1], dl=300)
    f.poly([(70, 598), (92, 598), (92, 620)], at=2, c="gold", w=3, z=False, dl=1300)
    f.poly([(248, 620), (248, 598), (270, 598)], at=2, c="gold", w=3, z=False, dl=1400)
    f.text(520, 540, "정사각형", z=32, c="gold", at=2, dl=1300, b=800)
    f.text(520, 580, "마름모 + 90°", z=22, c="soft", at=2, dl=1500, b=700)
    U.ex("m2-2-04", "평행사변형의 각을 90°로 세우면 무엇이 될까? 마름모의 각을 90°로 세우면?", "평행사변형에 조건을 더할 때마다 특별한 사각형이 된다",
         [L("평행사변형 + 한 내각 90° → 직사각형", memo="변은 그대로 · 각만 직각"),
          L("평행사변형 + 이웃한 두 변이 같다 → 마름모", memo="네 변이 같다"),
          L("마름모 + 한 내각 90° → 정사각형", memo="직사각형이면서 마름모")],
         "정사각형은 직사각형이면서 마름모", f.out(), at=("b2", 2))

    # ── 05 닮은 도형 ─────────────────────────────────────────
    f = Fig()
    u = 32
    B = (60, 330)
    A = (B[0] + 6 * u * math.cos(math.radians(70)), B[1] - 6 * u * math.sin(math.radians(70)))
    C = (B[0] + 8 * u, B[1])
    E = (110, 650)
    D = (E[0] + 1.5 * (A[0] - B[0]), E[1] + 1.5 * (A[1] - B[1]))
    F = (E[0] + 1.5 * (C[0] - B[0]), E[1])
    f.poly([A, B, C], at="q", c="ink", w=3.5, f="teal", fo=0.12)
    f.poly([D, E, F], at="q", c="ink", w=3.5, f="coral", fo=0.12)
    lab_pts(f, {"A": A, "B": B, "C": C}, at="q", z=28, off={"A": (0, -16), "B": (-16, 28), "C": (16, 28)})
    lab_pts(f, {"D": D, "E": E, "F": F}, at="q", z=28, off={"D": (0, -16), "E": (-18, 26), "F": (16, 26)})
    f.text(*off(B, A, 26), "6", z=28, at="q", b=800)
    f.text(*off(E, D, 26), "?", z=30, c="coral", at="q", b=800, un=2)
    f.text(470, 200, "닮음비 2 : 3", z=30, c="gold", at="q", b=800)
    M = mid(B, A)
    f.line(*B, *M, at=0, c="teal", w=8, dr=True)
    f.line(*M, *A, at=0, c="gold", w=8, dr=True, dl=500)
    f.text(*off(B, M, -24), "3", z=24, c="teal", at=0, dl=400, b=800)
    f.text(*off(M, A, -24), "3", z=24, c="gold", at=0, dl=900, b=800)
    f.text(470, 260, "AB = 3 × 2", z=24, c="soft", at=0, dl=1200, b=800)
    Q1, Q2 = P_(E, D, 1 / 3), P_(E, D, 2 / 3)
    for k, (S0, S1, src, col) in enumerate(((E, Q1, B, "teal"), (Q1, Q2, M, "gold"), (Q2, D, M, "gold"))):
        el = f.line(*S0, *S1, at=1, c=col, w=8, dl=1 + 450 * k)
        fly(el, src[0] - S0[0], src[1] - S0[1], dl=40, ms=800)
        f.text(*off(S0, S1, -24), "3", z=24, c=col, at=1, dl=900 + 450 * k, b=800)
    f.text(470, 470, "DE = 3 × 3", z=24, c="soft", at=1, dl=2300, b=800)
    f.text(470, 560, "DE = 9", z=40, c="gold", at=2, b=800)
    U.ex("m2-2-05", "△ABC ∽ △DEF이고 닮음비가 2 : 3이다. AB = 6일 때 DE의 길이를 구해 보자.", "대응변의 길이의 비 = 닮음비 — 비례식으로",
         [L("6 : DE = 2 : 3", memo="AB는 2칸 → 한 칸이 3"),
          L("2 × DE = 6 × 3", memo="(내항의 곱) = (외항의 곱) — DE는 3칸"),
          L("DE = 9")],
         "9", f.out(), at=("b3", 1))

    # ── 06 삼각형의 닮음 조건(공통각) ───────────────────────
    f = Fig()
    u = 38
    A = (300, 100)
    B = (A[0] + 12 * u * math.cos(math.radians(240)), A[1] - 12 * u * math.sin(math.radians(240)))
    C = (A[0] + 8 * u * math.cos(math.radians(300)), A[1] - 8 * u * math.sin(math.radians(300)))
    Dp = P_(A, C, 6 / 8)
    Ep = P_(A, B, 4 / 12)
    f.poly([A, B, C], at="q", c="ink", w=3.5)
    f.line(*Dp, *Ep, at="q", c="ink", w=3.5)
    lab_pts(f, {"A": A, "B": B, "C": C, "D": Dp, "E": Ep}, at="q", z=28,
            off={"A": (0, -16), "B": (-16, 28), "C": (18, 22), "D": (20, 8), "E": (-20, 2)})
    f.text(*off(A, Ep, -26), "4", z=26, at="q", b=800)
    f.text(*off(A, Dp, 26), "6", z=26, at="q", b=800)
    f.text(*off(A, B, -44), "12", z=26, at="q", b=800)
    angle_mark(f, A, B, C, r=40, at=0, c="gold")
    angle_mark(f, Dp, A, Ep, r=36, at=0, c="teal", dl=400)
    angle_mark(f, B, A, C, r=46, at=0, c="teal", dl=700)
    # 떼어 내어 같은 방향으로 놓은 △ADE (D ↔ B, E ↔ C)
    A3 = (560, 400)
    D3 = (A3[0] + 6 * u * math.cos(math.radians(240)), A3[1] - 6 * u * math.sin(math.radians(240)))
    E3 = (A3[0] + 4 * u * math.cos(math.radians(300)), A3[1] - 4 * u * math.sin(math.radians(300)))
    g0 = ((A[0] + Dp[0] + Ep[0]) / 3, (A[1] + Dp[1] + Ep[1]) / 3)
    g1 = ((A3[0] + D3[0] + E3[0]) / 3, (A3[1] + D3[1] + E3[1]) / 3)
    tri = f.poly([A3, D3, E3], at=1, c="coral", w=3.5, f="coral", fo=0.18)
    fly(tri, g0[0] - g1[0], g0[1] - g1[1], dl=60, ms=900)
    lab_pts(f, {"A": A3, "D": D3, "E": E3}, at=1, z=24, c="coral", off={"A": (0, -14), "D": (-14, 26), "E": (16, 22)}, dl=900)
    angle_mark(f, A3, D3, E3, r=30, at=1, c="gold", dl=1000)
    angle_mark(f, D3, A3, E3, r=30, at=1, c="teal", dl=1100)
    f.text(560, 650, "△ADE ∽ △ABC", z=26, c="coral", at=1, dl=1300, b=800)
    f.text(520, 250, "AC = 8", z=30, c="gold", at=3, b=800)
    U.ex("m2-2-06", "그림의 △ABC에서 ∠ADE = ∠ABC이고 AE = 4, AD = 6, AB = 12일 때, AC의 길이를 구해 보자.", "겹친 그림은 공통각부터 — 공통각 + 같은 각 하나 = AA 닮음",
         [L("∠A는 공통, ∠ADE = ∠ABC", memo="두 쌍의 각이 같다"),
          L("△ADE ∽ △ABC (AA 닮음)", memo="대응 순서: A ↔ A, D ↔ B, E ↔ C"),
          L("AD : AB = AE : AC → 6 : 12 = 4 : AC", memo="대응변의 비"),
          L("AC = 8", memo="6 × AC = 12 × 4")],
         "8", f.out(), at=("b4", 1))

    # ── 07 평행선과 선분의 길이의 비 ─────────────────────────
    f = Fig()
    A, B, C = (300, 100), (90, 560), (540, 560)
    D, E = P_(A, B, 4 / 6), P_(A, C, 4 / 6)
    f.poly([A, B, C], at="q", c="ink", w=3.5)
    f.line(*D, *E, at="q", c="ink", w=3.5)
    lab_pts(f, {"A": A, "B": B, "C": C, "D": D, "E": E}, at="q", z=28, off={"A": (0, -16), "B": (-16, 30), "C": (16, 30), "D": (-22, 6), "E": (22, 6)})
    f.text(*off(A, D, -28), "4", z=26, at="q", b=800)
    f.text(*off(D, B, -28), "2", z=26, at="q", b=800)
    f.text(CX - 10, D[1] - 14, "6", z=26, at="q", b=800)
    f.text(CX - 10, 640, "?", z=30, c="coral", at="q", b=800, un=2)
    f.line(*A, *D, at=0, c="teal", w=7, dr=True)
    f.line(*D, *B, at=0, c="sky", w=7, dr=True, dl=600)
    f.text(560, 250, "AD : AB", z=24, c="soft", at=0, dl=900, b=800)
    f.text(560, 290, "= 4 : 6 = 2 : 3", z=24, c="teal", at=0, dl=1200, b=800)
    H = mid(D, E)
    f.line(*D, *H, at=1, c="gold", w=8, dr=True)
    f.line(*H, *E, at=1, c="coral", w=8, dr=True, dl=500)
    f.text(*off(D, H, 24), "3", z=22, c="gold", at=1, dl=500, b=800)
    f.text(*off(H, E, 24), "3", z=22, c="coral", at=1, dl=900, b=800)
    Q1, Q2 = P_(B, C, 1 / 3), P_(B, C, 2 / 3)
    for k, (S0, S1, src, col) in enumerate(((B, Q1, D, "gold"), (Q1, Q2, H, "coral"), (Q2, C, H, "coral"))):
        el = f.line(*S0, *S1, at=2, c=col, w=8, dl=1 + 450 * k)
        fly(el, src[0] - S0[0], src[1] - S0[1], dl=40, ms=800)
        f.text((S0[0] + S1[0]) / 2, 600, "3", z=22, c=col, at=2, dl=900 + 450 * k, b=800)
    f.text(560, 470, "BC = 9", z=36, c="gold", at=2, dl=2300, b=800)
    U.ex("m2-2-07", "△ABC에서 DE ∥ BC이고 AD = 4, DB = 2, DE = 6일 때 BC의 길이를 구해 보자.", "DE ∥ BC이면 △ADE ∽ △ABC — AD : AB = DE : BC",
         [L("AD : AB = 4 : 6 = 2 : 3", memo="AB = 4 + 2 = 6"),
          L("DE : BC = 2 : 3", memo="DE는 2칸 — 한 칸이 3"),
          L("6 : BC = 2 : 3 → BC = 9", memo="BC는 3칸")],
         "9", f.out(), at=("b3", 1))

    # ── 08 삼각형의 무게중심 ─────────────────────────────────
    f = Fig()
    A, B, C = (250, 100), (80, 560), (580, 560)
    D, Ee, Ff = mid(B, C), mid(A, C), mid(A, B)
    G = P_(A, D, 2 / 3)
    f.poly([A, B, C], at="q", c="ink", w=3.5)
    f.line(*B, *Ee, at="q", c="soft", w=2.5, d=True)
    f.line(*C, *Ff, at="q", c="soft", w=2.5, d=True)
    f.line(*A, *D, at="q", c="ink", w=3.5)
    lab_pts(f, {"A": A, "B": B, "C": C, "D": D}, at="q", z=28, off={"A": (0, -16), "B": (-16, 30), "C": (16, 30), "D": (0, 34)})
    f.dot(*G, r=10, f="gold", at="q")
    f.text(G[0] - 26, G[1] + 6, "G", z=28, c="gold", at="q", b=800)
    f.text(*off(A, D, 70), "AD = 15", z=26, at="q", b=800)
    P1 = P_(A, D, 1 / 3)
    cols = ("teal", "teal", "coral")
    for k, (S0, S1) in enumerate(((A, P1), (P1, G), (G, D))):
        f.line(*S0, *S1, at=1, c=cols[k], w=8, dr=True, dl=500 * k)
        f.text(*off(S0, S1, -24), "5", z=24, c=cols[k], at=1, dl=300 + 500 * k, b=800)
        if k < 2:
            f.dot(*S1, r=7, f="ink", at=1, dl=400 + 500 * k)
    f.text(*off(A, G, 70), "AG = 10", z=28, c="teal", at=2, b=800)
    f.text(*off(G, D, 70), "GD = 5", z=28, c="coral", at=2, dl=400, b=800)
    U.ex("m2-2-08", "△ABC의 무게중심을 G라 하자. 중선 AD의 길이가 15일 때 AG와 GD의 길이를 구해 보자.", "무게중심은 중선을 꼭짓점으로부터 2 : 1로 나눈다",
         [L("AG : GD = 2 : 1", memo="중선을 3칸으로 — 꼭짓점 쪽 2칸"),
          L("15 ÷ 3 = 5", memo="한 칸의 길이"),
          L("AG = 5 × 2 = 10, GD = 5")],
         "AG = 10, GD = 5", f.out(), at=("b3", 1))

    # ── 09 닮음과 넓이 · 부피 ───────────────────────────────
    f = Fig()
    s = 34
    f.rect(70, 110, s, s, at="q", c="ink", sw=2.5, f="teal", fo=0.5)
    f.text(87, 180, "1", z=24, at="q", b=800)
    gx, gy = 230, 70
    for k in range(9):
        r_, c_ = divmod(k, 3)
        el = f.rect(gx + c_ * s, gy + r_ * s, s, s, at=0, c="ink", sw=2.5, f="teal", fo=0.5, dl=1 + 110 * k)
        fly(el, 70 - (gx + c_ * s), 110 - (gy + r_ * s), dl=40, ms=560)
    f.text(gx + 1.5 * s, gy + 3 * s + 34, "9배", z=26, c="teal", at=0, dl=1300, b=800)
    f.text(500, 140, "넓이 1 : 9", z=30, c="teal", at=0, dl=1400, b=800)
    # 부피 — 작은 쌓기나무 하나와 3 × 3 × 3
    dx_, dy_ = 0.5, 0.42

    def box(x0, y0, w, h, dpt, at, dl=0, cs=("teal", "sky", "lilac"), fo=1.0):
        """앞면 왼쪽 아래 (x0, y0) · 가로 w · 높이 h · 깊이 dpt — 앞 · 위 · 옆 세 면"""
        ox, oy = dpt * dx_, -dpt * dy_
        els = [f.poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 - h), (x0, y0 - h)], at=at, c="ink", w=2, f=cs[0], fo=fo, dl=dl),
               f.poly([(x0, y0 - h), (x0 + w, y0 - h), (x0 + w + ox, y0 - h + oy), (x0 + ox, y0 - h + oy)], at=at, c="ink", w=2, f=cs[1], fo=fo, dl=dl),
               f.poly([(x0 + w, y0), (x0 + w + ox, y0 + oy), (x0 + w + ox, y0 - h + oy), (x0 + w, y0 - h)], at=at, c="ink", w=2, f=cs[2], fo=fo, dl=dl)]
        return els

    box(70, 420, s, s, s, "q")
    f.text(87, 460, "1", z=24, at="q", b=800)
    X0, Y0 = 230, 600
    for layer in range(3):
        y0 = Y0 - layer * s
        els = []
        for zi in range(2, -1, -1):
            for xi in range(3):
                ox, oy = zi * s * dx_, -zi * s * dy_
                els += box(X0 + xi * s + ox, y0 + oy, s, s, s, 1, dl=1 + 650 * layer)
        for el in els:
            fly(el, 0, -140, dl=40, ms=520)
    f.text(500, 470, "부피 1 : 27", z=30, c="lilac", at=1, dl=2200, b=800)
    f.text(500, 560, "5 × 27 = 135", z=32, c="gold", at=2, b=800)
    U.ex("m2-2-09", "닮음비가 1 : 3인 두 입체도형에서 작은 쪽의 부피가 5일 때, 큰 쪽의 부피를 구해 보자.", "닮음비 m : n → 넓이의 비 m^{2} : n^{2}, 부피의 비 m^{3} : n^{3}",
         [L("넓이의 비 1^{2} : 3^{2} = 1 : 9", memo="한 변이 3배 → 3 × 3칸"),
          L("부피의 비 1^{3} : 3^{3} = 1 : 27", memo="3 × 3 × 3개"),
          L("5 × 27 = 135")],
         "135", f.out(), at=("b3", 2))

    # ── 10 피타고라스 정리 ───────────────────────────────────
    f = Fig()
    u = 20
    Cc, Bb, Aa = (300, 360), (460, 360), (300, 240)
    f.poly([Aa, Bb, Cc], at="q", c="ink", w=4, f="gold", fo=0.15)
    angle_mark(f, Cc, Aa, Bb, r=30, at="q", c="ink")
    f.text(286, 308, "6", z=26, at="q", b=800, a="e")
    f.text(380, 390, "8", z=26, at="q", b=800)
    lab_pts(f, {"A": Aa, "B": Bb, "C": Cc}, at="q", z=24, off={"A": (-14, -10), "B": (20, 22), "C": (-16, 26)})
    src = []
    for i in range(8):                     # 변 CB 아래의 8 × 8
        for j in range(8):
            src.append(("coral", 300 + i * u, 360 + j * u, 1))
    for i in range(6):                     # 변 CA 왼쪽의 6 × 6
        for j in range(6):
            src.append(("teal", 180 + i * u, 240 + j * u, 0))
    nAB = ((Bb[0] - Aa[0]) / 10, (Bb[1] - Aa[1]) / 10)
    nN = (12, -16)
    tilt = math.degrees(math.atan2(Bb[1] - Aa[1], Bb[0] - Aa[0]))
    order = [(i, j) for j in range(10) for i in range(10)]
    for k, (col, x, y, at) in enumerate(src):
        el = f.rect(x, y, u, u, at=at, c="ink", sw=1.5, f=col, fo=0.55, dl=1 + 8 * (k if at == 1 else k - 64))
        i, j = order[k]
        tx = Aa[0] + (i + 0.5) * nAB[0] + (j + 0.5) * nN[0]
        ty = Aa[1] + (i + 0.5) * nAB[1] + (j + 0.5) * nN[1]
        cx0, cy0 = x + u / 2, y + u / 2
        el["mv"] = {"at": 2, "dx": R1(tx - cx0), "dy": R1(ty - cy0), "r": R1(tilt), "cx": R1(cx0), "cy": R1(cy0), "dl": 12 * k}
    f.text(240, 230, "36", z=30, c="teal", at=0, dl=500, b=800, un=2)
    f.text(380, 548, "64", z=30, c="coral", at=1, dl=700, b=800, un=2)
    sq = [Aa, Bb, (Bb[0] + 120, Bb[1] - 160), (Aa[0] + 120, Aa[1] - 160)]
    f.poly(sq, at=2, c="ink", w=3, d=True)
    f.text(440, 234, "100", z=40, c="gold", at=3, b=800)
    f.text(560, 330, "c = 10", z=36, c="gold", at=3, dl=500, b=800)
    U.ex("m2-2-10", "직각을 낀 두 변의 길이가 6, 8인 직각삼각형의 빗변의 길이를 구해 보자.", "a^{2} + b^{2} = c^{2} — 두 변 위 정사각형의 넓이의 합 = 빗변 위 정사각형의 넓이",
         [L("6^{2} = 36", memo="짧은 변 위 정사각형"),
          L("8^{2} = 64", memo="긴 변 위 정사각형"),
          L("c^{2} = 36 + 64 = 100", memo="두 정사각형의 칸이 빗변 위 정사각형을 꼭 채운다"),
          L("c = 10", memo="제곱해서 100이 되는 양수")],
         "10", f.out(), at=("b2", 1))

    # ── 11 피타고라스 정리의 활용(대각선이 직교하는 사각형) ──
    f = Fig()
    O = (250, 200)
    s_ = 30
    A = (O[0] - math.sqrt(3) * s_, O[1])
    Cq = (O[0] + math.sqrt(48) * s_, O[1])
    Bq = (O[0], O[1] + math.sqrt(33) * s_)
    Dq = (O[0], O[1] - 1 * s_)
    f.poly([A, Bq, Cq, Dq], at="q", c="ink", w=3.5)
    lab_pts(f, {"A": A, "B": Bq, "C": Cq, "D": Dq, "O": O}, at="q", z=26, off={"A": (-18, 8), "B": (0, 30), "C": (18, 8), "D": (0, -14), "O": (16, 26)})
    for V, col in ((A, "teal"), (Bq, "coral"), (Cq, "gold"), (Dq, "sky")):
        f.line(*O, *V, at="q", c=col, w=4)
    angle_mark(f, O, Cq, Dq, r=16, at="q", c="ink")
    f.text(*off(A, Bq, -26), "6", z=24, at="q", b=800)
    f.text(*off(Cq, Dq, -24), "7", z=24, at="q", b=800)
    f.text(*off(Bq, Cq, -24), "9", z=24, at="q", b=800)
    f.text(*off(Dq, A, -24), "?", z=26, c="red", at="q", b=800)
    S = Strip(f, y=470, z=34)
    toks = ["(", {"s": "OA^{2}", "c": "teal", "g": 0.04}, "+", {"s": "OB^{2}", "c": "coral"}, {"s": ")", "g": 0.04}, "+",
            "(", {"s": "OC^{2}", "c": "gold", "g": 0.04}, "+", {"s": "OD^{2}", "c": "sky"}, {"s": ")", "g": 0.04}]
    xa, _ = S.row(0, toks, keep=True)
    f.text((xa[0] + xa[4]) / 2, 530, "AB^{2} = 36", z=24, c="soft", at=0, dl=900, b=800)
    f.text((xa[6] + xa[10]) / 2, 530, "CD^{2} = 49", z=24, c="soft", at=0, dl=1100, b=800)
    xb, _ = S.row(1, ["(", {"s": "OB^{2}", "frm": 3, "c": "coral", "g": 0.04}, "+", {"s": "OC^{2}", "frm": 7, "c": "gold"}, {"s": ")", "g": 0.04}, "+",
                      "(", {"s": "OD^{2}", "frm": 9, "c": "sky", "g": 0.04}, "+", {"s": "OA^{2}", "frm": 1, "c": "teal"}, {"s": ")", "g": 0.04}], y=600, keep=True)
    f.text((xb[0] + xb[4]) / 2, 655, "BC^{2} = 81", z=24, c="soft", at=1, dl=900, b=800)
    f.text((xb[6] + xb[10]) / 2, 655, "DA^{2} = ?", z=24, c="red", at=1, dl=1100, b=800)
    f.text(560, 130, "DA = 2", z=34, c="gold", at=3, b=800)
    U.ex("m2-2-11", "두 대각선이 직교하는 사각형 ABCD에서 AB = 6, CD = 7, BC = 9일 때 DA의 길이를 구해 보자.", "숨은 직각삼각형 네 개 — 마주 보는 변끼리 제곱의 합이 같다",
         [L("AB^{2} + CD^{2} = OA^{2} + OB^{2} + OC^{2} + OD^{2}", memo="직각삼각형 OAB, OCD"),
          L("BC^{2} + DA^{2} = OB^{2} + OC^{2} + OD^{2} + OA^{2}", memo="같은 네 조각을 짝만 바꿔서"),
          L("36 + 49 = 81 + DA^{2} → DA^{2} = 4", memo="AB^{2} + CD^{2} = BC^{2} + DA^{2}"),
          L("DA = 2", memo="제곱해서 4가 되는 양수")],
         "2", f.out(), at=("b3", 1))
