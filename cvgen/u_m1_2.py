# 중1-2 — 기본 도형 · 작도와 합동 · 평면도형 · 입체도형 · 자료의 정리와 해석
import math
from cv import *
from figs import (slide, arcp, Strip, tw, CX, chip, bar_grow, table, ell_pts, sector_pts, oblique, solid, lab_pts, seg_ticks,
                  tri_from, rot, poly_pts)


def ray_turn(f, O, r, a_from, a_to, at, c="gold", dl=0, un=None, w=5):
    """O 에서 뻗은 반직선이 a_from 도에서 a_to 도로 돌아간다(시계 반대 +)"""
    x2, y2 = O[0] + r * math.cos(math.radians(a_from)), O[1] - r * math.sin(math.radians(a_from))
    el = f.line(O[0], O[1], x2, y2, at=at, c=c, w=w, dl=dl, un=un)
    el["mv"] = {"at": at, "r": -(a_to - a_from), "cx": O[0], "cy": O[1], "dl": dl + 200}
    return el


def build(U):
    # ── 01 점, 선, 면 ────────────────────────────────────────
    f = Fig()
    A, B = (70, 330), (590, 330)
    f.line(*A, *B, at="q", c="ink", w=4, dr=True)
    for P_, n in ((A, "A"), (B, "B")):
        f.dot(*P_, r=10, f="ink", at="q")
        f.text(P_[0], P_[1] + 54, n, z=34, at="q", b=800)
    f.line(A[0], 230, B[0], 230, at="q", c="soft", w=2.5, ar=2)
    f.text(CX, 205, "10 cm", z=32, at="q", b=700)
    M = ((A[0] + B[0]) / 2, A[1])
    m = f.dot(A[0], A[1], r=13, f="coral", at=0)
    slide(m, 0, dx=M[0] - A[0], dl=200)
    f.text(M[0], M[1] + 54, "M", z=34, c="coral", at=0, dl=1100, b=800)
    seg_ticks(f, A, M, 1, at=1, c="coral")
    seg_ticks(f, M, B, 1, at=1, c="coral", dl=200)
    f.line(A[0], 450, M[0] - 6, 450, at=1, c="coral", w=2.5, ar=2, dl=300)
    f.line(M[0] + 6, 450, B[0], 450, at=1, c="coral", w=2.5, ar=2, dl=500)
    f.text((A[0] + M[0]) / 2, 500, "5 cm", z=32, c="coral", at=1, dl=400, b=800)
    f.text((M[0] + B[0]) / 2, 500, "5 cm", z=32, c="coral", at=1, dl=600, b=800)
    U.ex("m1-2-01", "길이가 10 cm인 선분 AB의 중점을 M이라 할 때, AM의 길이를 구해 보자.", "중점은 선분을 똑같이 둘로 나누는 점",
         [L("AM = MB", memo="중점 → 양쪽 길이가 같다"),
          L("AM = {1/2}AB = {1/2} × 10 = 5", memo="전체의 절반")],
         "5 cm", f.out(), at=("b4", 1))

    # ── 02 각 ─────────────────────────────────────────────────
    f = Fig()
    O = (CX, 470)
    f.line(O[0] - 270, O[1], O[0] + 270, O[1], at="q", c="ink", w=4)
    f.dot(*O, r=9, f="ink", at="q")
    angs = [50, 90, 130, 180]
    names = ["예각", "직각", "둔각", "평각"]
    cols = ["teal", "gold", "coral", "sky"]
    prev = 0
    for k, a in enumerate(angs):
        last = k == 3
        ray_turn(f, O, 240, prev, a, at=k, c=cols[k], un=None if last else k + 1)
        if not last:                             # 돌아간 자리에 흐린 반직선을 남긴다
            x2, y2 = ang_pt(O[0], O[1], 240, a)
            f.line(O[0], O[1], x2, y2, at=k + 1, c=cols[k], w=3, o=0.55)
        f.arc(O[0], O[1], 56 + 22 * k, 0, a, at=k, c=cols[k], sw=3.5, f=cols[k], fo=0.12, dl=300)
        lx, ly = ang_pt(O[0], O[1], 300, a) if a < 180 else (O[0] - 200, O[1] + 60)
        f.text(lx, ly + 10, f"{names[k]} {a}°", z=30, c=cols[k], at=k, dl=900, b=800)
        prev = a
    U.ex("m1-2-02", "반직선 하나를 돌려 예각, 직각, 둔각, 평각을 차례로 만들어 보자.", "직각 90°와 평각 180°를 기준으로 나눈다",
         [L("50° → 예각", memo="0°보다 크고 90°보다 작은 각"),
          L("90° → 직각", memo="평각의 절반"),
          L("130° → 둔각", memo="90°보다 크고 180°보다 작은 각"),
          L("180° → 평각", memo="두 반직선이 일직선")],
         "예각 < 직각 < 둔각 < 평각", f.out(), at=("b2", 1))

    # ── 03 점, 직선, 평면의 위치 관계 ─────────────────────────
    f = Fig()
    s = 260
    base = {"A": (0, 0, 0), "B": (s, 0, 0), "C": (s, 0, s), "D": (0, 0, s), "E": (0, s, 0), "F": (s, s, 0), "G": (s, s, s), "H": (0, s, s)}
    V = {k: (110 + oblique(p)[0], 230 + oblique(p)[1]) for k, p in base.items()}
    E = [("A", "B"), ("B", "C"), ("C", "D"), ("D", "A"), ("E", "F"), ("F", "G"), ("G", "H"), ("H", "E"),
         ("A", "E"), ("B", "F"), ("C", "G"), ("D", "H")]
    hidden = {("D", "H"), ("H", "E"), ("G", "H")}
    solid(f, V, E, hidden=list(hidden), at="q")
    lab_pts(f, V, at="q", z=28, off={"A": (-18, -10), "B": (-14, -16), "C": (18, -10), "D": (-16, -12), "E": (-18, 26), "F": (16, 28), "G": (18, 26), "H": (-16, -10)})
    f.line(*V["A"], *V["B"], at="q", c="gold", w=8)
    groups = [(("D", "C"), ("E", "F"), ("H", "G")), (("A", "D"), ("A", "E"), ("B", "C"), ("B", "F")), (("C", "G"), ("D", "H"), ("E", "H"), ("F", "G"))]
    gc = ["teal", "coral", "sky"]
    for k, g in enumerate(groups):
        for j, (a, b) in enumerate(g):
            hd = (a, b) in hidden or (b, a) in hidden
            f.line(*V[a], *V[b], at=k, c=gc[k], w=5 if hd else 7, d=hd, dr=True, dl=1 + 330 * j)
    U.ex("m1-2-03", "정육면체 ABCD−EFGH에서 모서리 AB와 평행한 · 만나는 · 꼬인 위치에 있는 모서리를 찾아보자.", "같은 평면 위에 있는지부터 — 만나지도 평행하지도 않으면 꼬인 위치",
         [L("평행: DC, EF, HG", memo="3개"),
          L("만난다: AD, AE, BC, BF", memo="4개"),
          L("꼬인 위치: CG, DH, EH, FG", memo="4개"),
          L("3 + 4 + 4 = 11", memo="AB를 뺀 나머지 모서리 전부")],
         "평행 3, 만남 4, 꼬인 위치 4", f.out(), at=("b4", 1))

    # ── 04 평행선의 성질 ─────────────────────────────────────
    f = Fig()
    yl, ym = 210, 470
    f.line(50, yl, 610, yl, at="q", c="ink", w=4)
    f.line(50, ym, 610, ym, at="q", c="ink", w=4)
    f.text(620, yl + 10, "l", z=34, at="q", a="s")
    f.text(620, ym + 10, "m", z=34, at="q", a="s")
    P_ = (250, yl)
    t = (ym - yl) / math.sin(math.radians(70))
    Q = (P_[0] + t * math.cos(math.radians(70)), ym)
    f.line(P_[0] - 90 * math.cos(math.radians(70)), yl - 90 * math.sin(math.radians(70)), Q[0] + 90 * math.cos(math.radians(70)), ym + 90 * math.sin(math.radians(70)), at="q", c="ink", w=3.5)
    f.arc(*P_, 58, 290, 360, at="q", c="gold", sw=4, f="gold", fo=0.3)
    f.text(P_[0] + 92, yl + 50, "70°", z=32, c="gold", at="q", b=800)
    w2 = f.arc(*P_, 58, 290, 360, at=0, c="teal", sw=4, f="teal", fo=0.35)
    slide(w2, 0, dx=Q[0] - P_[0], dy=ym - yl, dl=200)
    f.text(Q[0] + 92, ym + 50, "동위각 70°", z=30, c="teal", at=0, dl=1100, b=800)
    w3 = f.arc(*Q, 58, 290, 360, at=1, c="coral", sw=4, f="coral", fo=0.35)
    w3["mv"] = {"at": 1, "r": 180, "cx": Q[0], "cy": Q[1], "dl": 200}
    f.text(Q[0] - 110, ym - 30, "엇각 70°", z=30, c="coral", at=1, dl=1100, b=800)
    f.arc(*Q, 84, 0, 110, at=2, c="sky", sw=4, f="sky", fo=0.2)
    f.text(Q[0] + 104, ym - 70, "110°", z=30, c="sky", at=2, dl=600, b=800)
    U.ex("m1-2-04", "l ∥ m이고 한 직선이 l과 이루는 각이 70°일 때, 동위각과 엇각의 크기를 구해 보자.", "평행선에서 동위각끼리 · 엇각끼리는 크기가 같다",
         [L("각을 그대로 미끄러뜨리면 동위각 → 70°", memo="같은 자리"),
          L("맞꼭지각만큼 돌리면 엇각 → 70°", memo="엇갈린 자리"),
          L("같은 쪽 내각 = 180° − 70° = 110°", memo="두 내각의 합 180°")],
         "동위각 70°, 엇각 70°", f.out(), at=("b4", 1))

    # ── 05 삼각형의 작도 ─────────────────────────────────────
    f = Fig()
    u = 40
    B1, C1 = (CX - 4 * u, 220), (CX + 4 * u, 220)
    f.line(*B1, *C1, at=0, c="ink", w=5, dr=True)
    f.text(CX, 262, "8", z=30, at=0, b=700)
    a1 = f.line(B1[0], B1[1], B1[0] + 3 * u, B1[1], at=0, c="teal", w=5, dl=600)
    a1["mv"] = {"at": 0, "r": -70, "cx": B1[0], "cy": B1[1], "dl": 900}
    b1 = f.line(C1[0], C1[1], C1[0] - 4 * u, C1[1], at=0, c="coral", w=5, dl=600)
    b1["mv"] = {"at": 0, "r": 70, "cx": C1[0], "cy": C1[1], "dl": 900}
    f.line(B1[0] + 3 * u + 3, B1[1] - 22, C1[0] - 4 * u - 3, C1[1] - 22, at=0, c="red", w=3.5, ar=2, dl=1200)
    f.text(B1[0] + 3.5 * u, B1[1] - 40, "1", z=24, c="red", at=0, dl=1300, b=800)
    a1["mv"]["dl"] = 1700
    b1["mv"]["dl"] = 1700
    f.text(B1[0] + 30, B1[1] - 130, "3", z=30, c="teal", at=0, dl=2500, b=800)
    f.text(C1[0] - 30, C1[1] - 160, "4", z=30, c="coral", at=0, dl=2500, b=800)
    f.text(CX, 110, "만나지 못한다", z=30, c="red", at=0, dl=2700, b=800)
    u2 = 50
    B2, C2 = (CX - 3 * u2, 560), (CX + 3 * u2, 560)
    al = math.degrees(math.acos((16 + 36 - 25) / 48))
    be = math.degrees(math.acos((25 + 36 - 16) / 60))
    f.line(*B2, *C2, at=1, c="ink", w=5, dr=True)
    f.text(CX, 602, "6", z=30, at=1, b=700)
    a2 = f.line(B2[0], B2[1], B2[0] + 4 * u2, B2[1], at=1, c="teal", w=5, dl=600)
    a2["mv"] = {"at": 1, "r": -al, "cx": B2[0], "cy": B2[1], "dl": 900}
    b2_ = f.line(C2[0], C2[1], C2[0] - 5 * u2, C2[1], at=1, c="coral", w=5, dl=600)
    b2_["mv"] = {"at": 1, "r": be, "cx": C2[0], "cy": C2[1], "dl": 900}
    A2 = (B2[0] + 4 * u2 * math.cos(math.radians(al)), B2[1] - 4 * u2 * math.sin(math.radians(al)))
    f.dot(*A2, r=11, f="gold", at=1, dl=1900)
    f.text(A2[0], A2[1] - 24, "만난다!", z=30, c="gold", at=1, dl=2000, b=800)
    U.ex("m1-2-05", "길이가 3, 4, 8인 선분과 4, 5, 6인 선분으로 삼각형을 만들 수 있을까?", "가장 긴 변 < 나머지 두 변의 합 이어야 두 변이 만난다",
         [L("3 + 4 = 7 < 8", memo="두 변이 만나지 못한다"),
          L("4 + 5 = 9 > 6", memo="두 변이 만나 삼각형이 된다")],
         "4, 5, 6만 삼각형이 된다", f.out(), at=("b3", 1))

    # ── 06 삼각형의 합동 ─────────────────────────────────────
    f = Fig()
    A, B, C = (150, 200), (70, 420), (320, 420)
    th = -28
    E_ = (430, 560)
    dx, dy = E_[0] - B[0], E_[1] - B[1]
    D, F_ = [(rot(p, B, th)[0] + dx, rot(p, B, th)[1] + dy) for p in (A, C)]
    f.poly([A, B, C], at="q", c="teal", w=4, f="teal", fo=0.12)
    f.poly([D, E_, F_], at="q", c="coral", w=4, f="coral", fo=0.12)
    lab_pts(f, {"A": A, "B": B, "C": C}, at="q", z=30, off={"A": (0, -16), "B": (-20, 24), "C": (16, 26)})
    lab_pts(f, {"D": D, "E": E_, "F": F_}, at="q", z=30, off={"D": (-6, -18), "E": (-20, 24), "F": (20, 16)})
    for (P1, P2), (Q1, Q2), n in (((A, B), (D, E_), 1), ((B, C), (E_, F_), 2)):
        seg_ticks(f, P1, P2, n, at=0, c="gold")
        seg_ticks(f, Q1, Q2, n, at=0, c="gold", dl=300)
    from fig import angle_mark
    angle_mark(f, B, A, C, r=40, at=0, c="gold", dl=600)
    angle_mark(f, E_, D, F_, r=40, at=0, c="gold", dl=800)
    cp = f.poly([A, B, C], at=1, c="teal", w=4, f="teal", fo=0.3)
    cp["mv"] = {"at": 1, "dx": dx, "dy": dy, "r": th, "cx": B[0], "cy": B[1], "dl": 300}
    f.text(CX + 60, 140, "꼭 포개진다", z=30, c="gold", at=2, b=800)
    U.ex("m1-2-06", "△ABC와 △DEF에서 AB = DE, ∠B = ∠E, BC = EF일 때 두 삼각형이 합동인지 포개어 확인해 보자.", "합동 조건 — 두 변과 그 끼인각(SAS)",
         [L("AB = DE, ∠B = ∠E, BC = EF", memo="두 변과 그 끼인각"),
          L("△ABC를 옮기고 돌리면 △DEF에 포개진다", memo="SAS 합동"),
          L("△ABC ≡ △DEF", memo="대응하는 꼭짓점 차례로")],
         "△ABC ≡ △DEF (SAS 합동)", f.out(), at=("b2", 2))

    # ── 07 다각형 ─────────────────────────────────────────────
    f = Fig()
    pts = poly_pts(CX, 330, 230, 6, rot=90)
    f.poly(pts, at="q", c="ink", w=4)
    for i, p in enumerate(pts):
        f.dot(*p, r=8, f="ink", at="q")
    for k, j in enumerate((2, 3, 4)):
        f.line(*pts[0], *pts[j], at=0, c="coral", w=4.5, dr=True, dl=1 + 400 * k)
    f.text(pts[0][0], pts[0][1] - 26, "3", z=28, c="coral", at=0, dl=1300, b=800)
    for i in range(1, 6):                       # 꼭짓점마다 3개씩 — 이미 그은 대각선을 한 번 더 긋는다(두 번 세기)
        for k, d in enumerate((2, 3, 4)):
            j = (i + d) % 6
            f.line(*pts[i], *pts[j], at=1, c="teal", w=3, dr=True, dl=1 + 330 * (i - 1) + 80 * k)
        ox, oy = pts[i][0] - CX, pts[i][1] - 330
        f.text(pts[i][0] + ox * 0.13, pts[i][1] + oy * 0.13 + 10, "3", z=28, c="teal", at=1, dl=200 + 330 * (i - 1), b=800)
    f.text(CX, 640, "6 × 3 ÷ 2 = 9", z=36, c="gold", at=2, b=800)
    U.ex("m1-2-07", "육각형의 대각선의 개수를 구해 보자.", "한 꼭짓점에서 (n − 3)개, 한 대각선을 두 번 세니까 ÷ 2",
         [L("한 꼭짓점에서 6 − 3 = 3개", memo="자기 자신과 양옆은 빼기"),
          L("6 × 3 = 18", memo="꼭짓점마다 3개씩 — 같은 대각선을 두 번 셌다"),
          L("18 ÷ 2 = 9")],
         "9개", f.out(), at=("b4", 1))

    # ── 08 삼각형의 내각과 외각 ───────────────────────────────
    f = Fig()
    B, C = (60, 540), (450, 540)
    A = tri_from(B, C, 35, 70)
    f.poly([A, B, C], at="q", c="ink", w=4)
    f.line(C[0], C[1], 640, C[1], at="q", c="ink", w=3, d=True)
    lab_pts(f, {"A": A, "B": B, "C": C}, at="q", z=30, off={"A": (0, -18), "B": (-14, 34), "C": (0, 38)})
    aAB, aAC = dir_deg(A, B), dir_deg(A, C)
    f.arc(*B, 62, 0, 35, at="q", c="teal", sw=3, f="teal", fo=0.45)
    f.text(*ang_pt(B[0], B[1] + 10, 100, 17.5), "35°", z=28, c="teal", at="q", b=800)
    f.arc(*A, 52, aAB, aAC, at="q", c="coral", sw=3, f="coral", fo=0.45)
    f.text(*ang_pt(A[0], A[1] + 10, 92, (aAB + aAC) / 2), "75°", z=28, c="coral", at="q", b=800)
    mAC = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
    cB = f.arc(*B, 62, 0, 35, at=0, c="teal", sw=3, f="teal", fo=0.45)
    slide(cB, 0, dx=C[0] - B[0], dl=200)
    cA = f.arc(*A, 52, aAB, aAC, at=0, c="coral", sw=3, f="coral", fo=0.45, dl=900)
    cA["mv"] = {"at": 0, "r": 180, "cx": mAC[0], "cy": mAC[1], "dl": 1100}
    f.line(C[0], C[1], *ang_pt(C[0], C[1], 170, 35), at=0, c="soft", w=3, d=True, dl=2100)
    f.text(*ang_pt(C[0], C[1], 196, 35), "AB와 평행", z=22, c="soft", at=0, dl=2200, b=700)
    f.arc(*C, 56, 110, 180, at=1, c="gold", sw=4, f="gold", fo=0.5)
    f.text(*ang_pt(C[0], C[1] + 10, 92, 145), "70°", z=28, c="gold", at=1, dl=300, b=800)
    f.arc(*C, 104, 0, 110, at=2, c="sky", sw=4.5)
    f.text(*ang_pt(C[0], C[1] + 10, 140, 62), "110°", z=30, c="sky", at=2, dl=400, b=800)
    U.ex("m1-2-08", "∠A = 75°, ∠B = 35°인 △ABC에서 ∠C의 크기와, 꼭짓점 C에서의 외각의 크기를 구해 보자.", "세 내각을 모으면 일직선(180°) — 외각은 이웃하지 않은 두 내각의 합",
         [L("35° + 75° + ∠C = 180°", memo="∠A, ∠B를 C로 옮기면 평각"),
          L("∠C = 180° − 110° = 70°"),
          L("외각 = 35° + 75° = 110°", memo="180° − 70°와 같다")],
         "∠C = 70°, 외각 110°", f.out(), at=("b2", 0))

    # ── 09 다각형의 내각과 외각 ───────────────────────────────
    f = Fig()
    pts = poly_pts(CX, 330, 250, 8, rot=112.5)
    f.poly(pts, at="q", c="ink", w=4)
    tcol = ["teal", "gold", "coral", "sky", "lilac", "leaf"]
    for k in range(6):
        f.poly([pts[0], pts[k + 1], pts[k + 2]], at=0, c="ink", w=2.5, f=tcol[k], fo=0.3, dl=1 + 380 * k)
        cx_ = (pts[0][0] + pts[k + 1][0] + pts[k + 2][0]) / 3
        cy_ = (pts[0][1] + pts[k + 1][1] + pts[k + 2][1]) / 3
        f.text(cx_, cy_ + 12, str(k + 1), z=32, at=0, dl=200 + 380 * k, b=800)
    f.text(CX, 640, "180° × 6 = 1080°", z=38, c="gold", at=1, b=800)
    U.ex("m1-2-09", "팔각형의 내각의 크기의 합을 구해 보자.", "한 꼭짓점에서 대각선을 그으면 삼각형 (n − 2)개",
         [L("삼각형 8 − 2 = 6개", memo="한 꼭짓점에서 대각선 5개"),
          L("180° × 6 = 1080°", memo="삼각형마다 180°")],
         "1080°", f.out(), at=("b2", 1))

    # ── 10 원과 부채꼴 ─────────────────────────────────────
    f = Fig()
    O = (260, 400)
    R = 230
    f.circ(*O, R, at="q", c="ink", sw=3)
    f.dot(*O, r=7, f="ink", at="q")
    f.poly(sector_pts(*O, R, 0, 30), at="q", c="ink", w=3, f="teal", fo=0.35)
    f.arc(*O, R, 0, 30, at="q", c="teal", sw=8)
    f.text(O[0] + R + 46, O[1] - 50, "4 cm", z=30, c="teal", at="q", b=800)
    for k in (1, 2):
        el = f.poly(sector_pts(*O, R, 0, 30), at=0, c="ink", w=3, f="gold", fo=0.35, dl=1 + 600 * (k - 1))
        el["mv"] = {"at": 0, "r": -30 * k, "cx": O[0], "cy": O[1], "dl": 100 + 600 * (k - 1)}
        el2 = f.arc(*O, R, 0, 30, at=0, c="gold", sw=8, dl=1 + 600 * (k - 1))
        el2["mv"] = {"at": 0, "r": -30 * k, "cx": O[0], "cy": O[1], "dl": 100 + 600 * (k - 1)}
    f.text(O[0] + 60, O[1] - R - 30, "90° → 4 × 3 = 12 cm", z=32, c="gold", at=1, b=800, a="s")
    U.ex("m1-2-10", "중심각 30°인 부채꼴의 호가 4 cm일 때, 중심각 90°인 부채꼴의 호의 길이를 구해 보자.", "한 원에서 호의 길이는 중심각에 정비례",
         [L("90° = 30° × 3", memo="30°짜리 부채꼴 3개"),
          L("4 × 3 = 12", memo="호의 길이도 3배")],
         "12 cm", f.out(), at=("b4", 1))

    # ── 11 부채꼴의 호의 길이와 넓이 ─────────────────────────
    f = Fig()
    O = (CX, 350)
    R = 250
    f.circ(*O, R, at="q", c="ink", sw=3)
    f.dot(*O, r=7, f="ink", at="q")
    for k in range(9):
        f.line(O[0], O[1], O[0] + R * math.cos(math.radians(40 * k)), O[1] - R * math.sin(math.radians(40 * k)), at=0, c="soft", w=2.5, dr=True, dl=1 + 160 * k)
    f.poly(sector_pts(*O, R, 0, 40), at=1, c="coral", w=4, f="coral", fo=0.35)
    f.arc(*O, R, 0, 40, at=1, c="coral", sw=9, dl=300)
    f.text(O[0] + R * 0.62, O[1] - R * 0.18, "{1/9}", z=34, c="coral", at=1, dl=500, b=800)
    f.text(O[0] - 10, O[1] + R + 50, "r = 9, 중심각 40°", z=30, at="q", b=700)
    U.ex("m1-2-11", "반지름 9, 중심각 40°인 부채꼴의 호의 길이와 넓이를 구해 보자.", "부채꼴은 원의 {x/360} — 원 전체에 그 몫을 곱한다",
         [L("40° = 360° × {1/9}", memo="원을 9조각 낸 하나"),
          L("l = 2π × 9 × {1/9} = 2π", memo="원둘레의 {1/9}"),
          L("S = π × 9^{2} × {1/9} = 9π", memo="원 넓이의 {1/9}")],
         "l = 2π, S = 9π", f.out(), at=("b2", 1))

    # ── 12 다면체 ─────────────────────────────────────────────
    f = Fig()
    top = poly_pts(CX, 190, 190, 5, rot=90)
    top = [(x, 190 + (y - 190) * 0.42) for x, y in top]
    bot = [(x, y + 330) for x, y in top]
    for i in range(5):                          # 꼭짓점 0 이 가장 안쪽 — 아래 밑면의 (4, 0) · (0, 1)과 0 의 옆 모서리는 가려진다
        j = (i + 1) % 5
        f.line(*top[i], *top[j], at="q", c="ink", w=3)
        f.line(*bot[i], *bot[j], at="q", c="ink", w=3, d=(i, j) in ((4, 0), (0, 1)))
        f.line(*top[i], *bot[i], at="q", c="ink", w=3, d=i == 0)
    for i in range(5):
        j = (i + 1) % 5
        f.line(*top[i], *top[j], at=0, c="teal", w=7, dr=True, dl=1 + 250 * i)
        hb = (i, j) in ((4, 0), (0, 1))
        f.line(*bot[i], *bot[j], at=1, c="coral", w=5 if hb else 7, d=hb, dr=True, dl=1 + 250 * i)
        f.line(*top[i], *bot[i], at=2, c="gold", w=5 if i == 0 else 7, d=i == 0, dr=True, dl=1 + 250 * i)
    f.text(CX, 660, "5 + 5 + 5 = 15", z=36, c="gold", at=3, b=800)
    U.ex("m1-2-12", "오각기둥의 모서리의 개수를 구해 보자.", "위 · 아래 밑면의 모서리와 옆 모서리를 따로 센다",
         [L("위 오각형: 5", memo="밑면 하나에 5개"),
          L("아래 오각형: 5"),
          L("옆 모서리: 5", memo="꼭짓점끼리 잇는 세로선"),
          L("5 + 5 + 5 = 15 = 3 × 5", memo="n각기둥의 모서리는 3n개")],
         "15개", f.out(), at=("b2", 0))

    # ── 13 회전체 ─────────────────────────────────────────────
    f = Fig()
    xs = (110, 330, 550)
    cl = ("teal", "coral", "sky")
    for k, x0 in enumerate(xs):
        f.line(x0, 120, x0, 570, at="q", c="soft", w=2.5, d=True)
    f.poly([(110, 200), (190, 200), (190, 480), (110, 480)], at="q", c="teal", w=4, f="teal", fo=0.3)
    f.poly([(330, 200), (410, 480), (330, 480)], at="q", c="coral", w=4, f="coral", fo=0.3)
    f.poly(ell_pts(550, 340, 90, 90, -90, 90, 32), at="q", c="sky", w=4, f="sky", fo=0.3)
    for k, x0 in enumerate(xs):                  # 축 둘레를 도는 화살표
        f.poly(ell_pts(x0, 150, 46, 13, 210, 510, 30), at=k, c=cl[k], w=3.5, z=False, dr=True, ar=1)
    f.poly(ell_pts(110, 200, 80, 22, 0, 360), at=0, c="teal", w=3, z=False, dr=True, dl=500)
    f.poly(ell_pts(110, 480, 80, 22, 180, 360), at=0, c="teal", w=3, z=False, dr=True, dl=800)
    f.poly(ell_pts(110, 480, 80, 22, 0, 180), at=0, c="teal", w=2.5, z=False, d=True, dl=800)
    f.line(30, 200, 30, 480, at=0, c="teal", w=3, dr=True, dl=1100)
    f.poly(ell_pts(330, 480, 80, 22, 180, 360), at=1, c="coral", w=3, z=False, dr=True, dl=500)
    f.poly(ell_pts(330, 480, 80, 22, 0, 180), at=1, c="coral", w=2.5, z=False, d=True, dl=500)
    f.line(330, 200, 250, 480, at=1, c="coral", w=3, dr=True, dl=900)
    f.poly(ell_pts(550, 340, 90, 90, 90, 270, 32), at=2, c="sky", w=3, z=False, dr=True, dl=500)
    f.poly(ell_pts(550, 340, 90, 24, 180, 360), at=2, c="sky", w=2.5, z=False, dr=True, dl=900)
    for k, s_ in enumerate(("원기둥", "원뿔", "구")):
        f.text(xs[k], 630, s_, z=34, c=cl[k], at=k, dl=1300, b=800)
    U.ex("m1-2-13", "직사각형 · 직각삼각형 · 반원을 한 직선을 축으로 한 바퀴 돌리면 어떤 입체가 될까?", "축 둘레로 돌린 자국 — 축에 수직으로 자르면 원",
         [L("직사각형 → 원기둥", memo="한 변을 축으로"),
          L("직각삼각형 → 원뿔", memo="직각을 낀 변을 축으로"),
          L("반원 → 구", memo="지름을 축으로")],
         "원기둥, 원뿔, 구", f.out(), at=("b1", 1))

    # ── 14 기둥의 겉넓이와 부피 ───────────────────────────────
    f = Fig()
    u = 30
    r, h = 2 * u, 7 * u
    cx0 = 120
    f.poly(ell_pts(cx0, 160, r, r * 0.3), at="q", c="ink", w=3, f="teal", fo=0.25)
    f.line(cx0 - r, 160, cx0 - r, 160 + h, at="q", c="ink", w=3)
    f.line(cx0 + r, 160, cx0 + r, 160 + h, at="q", c="ink", w=3)
    f.poly(ell_pts(cx0, 160 + h, r, r * 0.3, 180, 360), at="q", c="ink", w=3, z=False)
    f.text(cx0, 160 + h + 60, "r = 2, h = 7", z=26, at="q", b=700)
    W = 2 * math.pi * 2 * u
    x1 = 230
    f.circ(x1 + W / 2, 130, r, at=0, c="ink", sw=3, f="teal", fo=0.3)
    f.rect(x1, 130 + r, W, h, at=1, c="ink", sw=3, f="gold", fo=0.3)
    f.circ(x1 + W / 2, 130 + 2 * r + h, r, at=0, c="ink", sw=3, f="teal", fo=0.3, dl=300)
    f.line(x1 + 8, 130 + r + 26, x1 + W - 8, 130 + r + 26, at=1, c="gold", w=2.5, ar=2, dl=500)
    f.text(x1 + W / 2, 130 + r + 62, "2π × 2 = 4π", z=26, c="gold", at=1, dl=700, b=800)
    f.text(x1 + W + 22, 130 + r + h / 2 + 10, "7", z=28, at=1, dl=700, b=800)
    f.text(x1 + W / 2, 130 + r + h / 2 + 50, "4π × 7 = 28π", z=30, at=1, dl=1000, b=800)
    f.text(CX + 20, 660, "4π × 2 + 28π = 36π", z=34, c="coral", at=2, b=800)
    U.ex("m1-2-14", "밑면의 반지름이 2, 높이가 7인 원기둥의 겉넓이를 전개도로 구해 보자.", "겉넓이 = (밑넓이) × 2 + (옆넓이) — 옆면을 펼치면 직사각형",
         [L("밑넓이 = π × 2^{2} = 4π", memo="원 두 장"),
          L("옆넓이 = (2π × 2) × 7 = 28π", memo="가로 = 밑면 둘레"),
          L("겉넓이 = 4π × 2 + 28π = 36π")],
         "36π", f.out(), at=("b3", 1))

    # ── 15 뿔의 겉넓이와 부피 ─────────────────────────────────
    f = Fig()
    ap, bc = (95, 130), (95, 360)
    f.poly([ap, (bc[0] - 70, bc[1]), (bc[0] + 70, bc[1])], at="q", c="ink", w=3, f="gold", fo=0.18, z=False)
    f.poly(ell_pts(*bc, 70, 20, 180, 360), at="q", c="ink", w=3, z=False)
    f.poly(ell_pts(*bc, 70, 20, 0, 180), at="q", c="ink", w=2.5, z=False, d=True)
    f.line(*bc, bc[0] + 70, bc[1], at="q", c="teal", w=3)
    f.text(bc[0] + 35, bc[1] - 12, "2", z=24, c="teal", at="q", b=800)
    f.text(bc[0] + 52, (ap[1] + bc[1]) / 2, "6", z=26, at="q", b=800)
    O = (410, 130)
    Rl = 6 * 40
    f.poly(sector_pts(*O, Rl, 210, 330, 30), at=0, c="ink", w=3, f="gold", fo=0.28)
    arcp(f, *O, Rl, 210, 330, at=0, c="coral", sw=7, dl=400)
    f.text(*ang_pt(O[0], O[1], 120, 236), "6", z=28, at=0, dl=600, b=800)
    f.text(O[0] + 160, O[1] + Rl + 6, "호 = 2π × 2 = 4π", z=24, c="coral", at=0, dl=800, b=800)
    f.circ(O[0], O[1] + Rl + 2 * 40 + 6, 2 * 40, at=2, c="ink", sw=3, f="teal", fo=0.3)
    f.text(O[0] + 150, O[1] + Rl + 96, "밑면 4π", z=26, c="teal", at=2, b=800)
    f.text(O[0], O[1] + 120, "12π", z=34, c="ink", at=1, dl=500, b=800)
    f.text(O[0], 62, "{1/2} × 6 × 4π = 12π", z=28, c="gold", at=1, dl=900, b=800)
    U.ex("m1-2-15", "밑면의 반지름이 2, 모선의 길이가 6인 원뿔의 겉넓이를 구해 보자.", "옆면을 펼치면 반지름이 모선, 호가 밑면 둘레인 부채꼴",
         [L("옆면 = 반지름 6, 호 4π인 부채꼴", memo="호 = 밑면 둘레"),
          L("옆넓이 = {1/2} × 6 × 4π = 12π", memo="S = {1/2}rl"),
          L("겉넓이 = 4π + 12π = 16π", memo="밑면은 한 장")],
         "16π", f.out(), at=("b3", 1))

    # ── 16 구의 겉넓이와 부피 ─────────────────────────────────
    f = Fig()
    f.circ(160, 330, 120, at="q", c="ink", sw=3.5, f="coral", fo=0.3)
    f.poly(ell_pts(160, 330, 120, 34, 180, 360), at="q", c="ink", w=2.5, z=False)
    f.text(160, 500, "r = 2", z=28, at="q", b=700)
    cs = [(390, 210), (540, 210), (390, 450), (540, 450)]
    for k, (x, y) in enumerate(cs):
        f.circ(x, y, 70, at=0, c="ink", sw=3, dl=1 + 200 * k)
        for j in range(10):
            a = 360 * j / 10
            el = f.dot(x + 40 * math.cos(math.radians(a)), y - 40 * math.sin(math.radians(a)), r=10, f="coral", at=0, dl=600 + 200 * k + 40 * j)
            fly(el, 160 - x, 330 - y, dl=40, ms=600)
        f.circ(x, y, 70, at=0, c="none", f="coral", fo=0.35, dl=1400 + 200 * k)
    f.text(465, 640, "원 4개 = 4πr^{2}", z=32, c="coral", at=0, dl=2000, b=800)
    U.ex("m1-2-16", "반지름이 2인 구의 겉넓이와 부피를 구해 보자.", "겉넓이는 같은 반지름 원 넓이의 4배, 부피는 {4/3}πr^{3}",
         [L("S = 4 × π × 2^{2} = 16π", memo="귤껍질이 원 4개를 채운다"),
          L("V = {4/3} × π × 2^{3} = {32/3}π", memo="반지름의 세제곱")],
         "16π, {32/3}π", f.out(), at=("b2", 1))

    # ── 17 대푯값 ─────────────────────────────────────────────
    f = Fig()
    nl = NL(f, 0, 20, y=430, x0=50, x1=610, step=1, lab_step=2, z=22)
    data = [2, 3, 3, 4, 18]
    stack = {}
    for i, v in enumerate(data):
        k = stack.get(v, 0)
        stack[v] = k + 1
        f.dot(nl.X(v), nl.y - 24 - 30 * k, r=12, f="teal" if v != 18 else "coral", at="q", dl=120 * i)
    tri = f.poly([(nl.X(6), nl.y + 4), (nl.X(6) - 18, nl.y + 40), (nl.X(6) + 18, nl.y + 40)], at=0, c="gold", w=3, f="gold", fo=0.6)
    tri["fr"] = {"dx": nl.X(3) - nl.X(6), "dy": 0, "dl": 300, "ms": 1200}
    f.text(nl.X(6), nl.y + 100, "평균 6", z=30, c="gold", at=0, dl=1500, b=800)
    f.circ(nl.X(3), nl.y - 54, 40, at=1, c="sky", sw=4)
    f.text(nl.X(3), nl.y - 120, "중앙값 · 최빈값 3", z=30, c="sky", at=1, dl=400, b=800)
    f.text(nl.X(14), nl.y - 90, "18이 평균을 끌고 간다", z=26, c="coral", at=2, b=800)
    U.ex("m1-2-17", "자료 2, 3, 3, 4, 18의 평균, 중앙값, 최빈값을 구해 보자.", "평균은 무게중심, 중앙값은 가운데, 최빈값은 가장 많은 값",
         [L("평균 = (2 + 3 + 3 + 4 + 18) ÷ 5 = 6", memo="받침이 균형 잡는 자리"),
          L("중앙값 3, 최빈값 3", memo="크기순 가운데 · 가장 많이"),
          L("극단값 18 → 중앙값이 더 믿음직", memo="평균이 한쪽으로 끌려간다")],
         "평균 6, 중앙값 3, 최빈값 3", f.out(), at=("b4", 1))

    # ── 18 줄기와 잎 그림 ─────────────────────────────────────
    f = Fig()
    data = [12, 15, 18, 20, 23, 23, 27, 31]
    for i, v in enumerate(data):
        f.text(70 + 72 * i, 110, str(v), z=32, at="q", b=700, un=0 if v < 20 else (1 if v < 30 else 2))
    f.line(200, 160, 200, 520, at="q", c="ink", w=3)
    f.text(140, 190, "줄기", z=26, c="soft", at="q", b=700)
    f.text(330, 190, "잎", z=26, c="soft", at="q", b=700)
    cnt = {}
    for i, v in enumerate(data):
        st, lf = divmod(v, 10)
        k = cnt.get(st, 0)
        cnt[st] = k + 1
        y = 270 + 100 * (st - 1)
        if k == 0:
            f.text(150, y, str(st), z=40, c="teal", at=st - 1, b=800)
        el = f.text(240 + 52 * k, y, str(lf), z=40, at=st - 1, dl=1 + 260 * k, b=700)
        fly(el, 70 + 72 * i - (240 + 52 * k), 110 - y, dl=60, ms=640)
    f.rect(230, 270 + 100 - 52, 52 * 4, 70, c="gold", sw=4, rx=12, at=3)
    f.text(CX + 140, 620, "20 이상 30 미만: 4개", z=30, c="gold", at=3, dl=300, b=800)
    U.ex("m1-2-18", "자료 12, 15, 18, 20, 23, 23, 27, 31로 줄기와 잎 그림을 그려 보자.", "십의 자리는 줄기, 일의 자리는 잎",
         [L("1 | 2 5 8", memo="줄기 1"),
          L("2 | 0 3 3 7", memo="줄기 2"),
          L("3 | 1", memo="줄기 3"),
          L("20 이상 30 미만: 4개", memo="줄기 2의 잎 수")],
         "4개", f.out(), at=("b3", 1))

    # ── 19 도수분포표 ─────────────────────────────────────────
    f = Fig()
    vals = [5, 8, None, 10, 7]
    cols = ["teal", "sky", "gold", "coral", "lilac"]
    x0, W_, y = 50, 560, 300
    x = x0
    for i, v in enumerate(vals):
        w = W_ * (v or 10) / 40
        el = f.rect(x, y, w, 90, at="q" if v else 1, c="ink", sw=2.5, f=cols[i], fo=0.45 if v else 0.6, dl=120 * i)
        f.text(x + w / 2, y + 56, str(v) if v else "x", z=32, at="q" if v else 1, dl=120 * i + 60, b=800)
        if v is None:
            gap_x = x
        x += w
    f.line(x0, y - 30, x0 + W_, y - 30, at="q", c="ink", w=2.5)
    f.text(x0 + W_ / 2, y - 46, "전체 40명", z=30, at="q", b=700)
    f.rect(gap_x, y, W_ * 10 / 40, 90, c="red", sw=3, d=True, at="q")
    f.text(gap_x + W_ * 5 / 40, y + 170, "40 − 30 = 10", z=32, c="gold", at=1, dl=500, b=800)
    U.ex("m1-2-19", "전체 40명의 도수가 5, 8, x, 10, 7일 때 x를 구해 보자.", "도수를 모두 더하면 전체 — 빈칸은 전체에서 빼기",
         [L("5 + 8 + x + 10 + 7 = 40", memo="도수의 합 = 전체"),
          L("x = 40 − 30 = 10")],
         "10", f.out(), at=("b4", 1), sub={"x": 10})

    # ── 20 히스토그램과 도수분포다각형 ─────────────────────────
    f = Fig()
    P = Plane(f, (40, 110), (0, 9), box=(80, 80, 620, 590), square=False)
    f.line(P.X(40), P.Y(0), P.X(110), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(40), P.Y(0), P.X(40), P.Y(9), at="q", c="ink", w=3, ar=1)
    f.text(P.X(110) - 6, P.Y(0) + 66, "(점)", z=24, c="soft", at="q")
    f.text(P.X(40) + 34, P.Y(9) + 10, "(명)", z=24, c="soft", at="q")
    for v in (2, 4, 6, 8):
        f.line(P.X(40), P.Y(v), P.X(108), P.Y(v), at="q", c="soft", w=1, o=0.35)
    freq = [(50, 2), (60, 5), (70, 8), (80, 4), (90, 1)]
    for v in (40, 50, 60, 70, 80, 90, 100):
        f.text(P.X(v), P.Y(0) + 30, str(v), z=22, c="soft", at="q")
    for v in (2, 4, 6, 8):
        f.text(P.X(40) - 12, P.Y(v) + 8, str(v), z=22, c="soft", at="q", a="e")
    for i, (a, n) in enumerate(freq):
        f.poly([P.P(a, 0), P.P(a, n), P.P(a + 10, n), P.P(a + 10, 0)], at=0, c="ink", w=3, f="teal", fo=0.35, z=False, dr=True, dl=1 + 300 * i)
    mids = [(45, 0)] + [(a + 5, n) for a, n in freq] + [(105, 0)]
    for i, (a, n) in enumerate(mids):
        P.pt(a, n, at=1, f="coral", r=9, dl=1 + 160 * i)
    f.poly([P.P(a, n) for a, n in mids], at=2, c="coral", w=4.5, z=False, dr=True)
    U.ex("m1-2-20", "도수분포표로 히스토그램과 도수분포다각형을 그려 보자.", "히스토그램 막대 윗변의 가운데를 잇고, 양 끝은 도수 0인 계급까지",
         [L("50 ~ 60: 2, 60 ~ 70: 5, 70 ~ 80: 8, 80 ~ 90: 4, 90 ~ 100: 1", memo="계급마다 도수만큼 막대"),
          L("막대 윗변의 가운데에 점", memo="계급값 자리"),
          L("점을 잇고 양 끝은 0까지 내려 닫기", memo="도수 0인 계급이 있다고 치고")],
         "도수분포다각형 완성", f.out(), at=("b3", 1))

    # ── 21 상대도수와 그 그래프 ───────────────────────────────
    f = Fig()
    for k in range(50):
        r_, c_ = divmod(k, 10)
        f.rect(70 + c_ * 52, 120 + r_ * 52, 46, 46, at="q", c="soft", sw=2, rx=6, dl=8 * k)
    for k in range(12):
        r_, c_ = divmod(k, 10)
        f.rect(70 + c_ * 52, 120 + r_ * 52, 46, 46, at=0, c="none", f="coral", fo=0.7, dl=1 + 110 * k)
    f.text(CX, 440, "{12/50} = 0.24", z=40, c="coral", at=0, dl=1500, b=800)
    for k in range(15):
        r_, c_ = divmod(k, 10)
        f.rect(70 + c_ * 52, 120 + r_ * 52, 46, 46, at=1, c="teal", sw=4, rx=6, dl=1 + 90 * k)
    f.text(CX, 540, "50 × 0.3 = 15명", z=40, c="teal", at=1, dl=1500, b=800)
    U.ex("m1-2-21", "50명 중 도수가 12인 계급의 상대도수를 구하고, 상대도수가 0.3인 계급의 도수를 구해 보자.", "상대도수 = (도수) ÷ (전체), 도수 = (전체) × (상대도수)",
         [L("{12/50} = 0.24", memo="50칸 중 12칸"),
          L("50 × 0.3 = 15", memo="거꾸로 — 전체 × 상대도수")],
         "0.24, 15명", f.out(), at=("b3", 1))
