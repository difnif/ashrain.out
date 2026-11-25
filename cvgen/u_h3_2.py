# 고3 확률과 통계 — 순열과 조합 · 확률 · 통계
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, nl_range, hop


def chipm(f, x, y, s, at, c="teal", z=30, dl=0, un=None, fo=0.18):
    w = max(z * 1.25, tw(s, z) + z * 0.6)
    r = f.rect(x - w / 2, y - z * 0.98, w, z * 1.4, c=c, sw=3, rx=z * 0.42, f=c, fo=fo, at=at, dl=dl, un=un)
    t = f.text(x, y, s, z=z, c=c, at=at, dl=dl + 60, un=un, b=800)
    return [r, t]


def coin(f, x, y, head, at, r=16, dl=0):
    c = "teal" if head else "coral"
    f.circ(x, y, r, at=at, c=c, sw=2.5, f=c, fo=0.35, dl=dl)
    f.text(x, y + r * 0.42, "앞" if head else "뒤", z=r * 1.05, c=c, at=at, dl=dl, b=800)


def build(U):
    # ── 01 원순열 ──────────────────────────────────────────────
    f = Fig()
    O, Rr = (330, 290), 150
    f.circ(*O, 110, at="q", c="soft", sw=3, f="soft", fo=0.12)
    spots = [(O[0] + Rr * math.cos(math.radians(90 - 90 * k)), O[1] - Rr * math.sin(math.radians(90 - 90 * k)) + 10) for k in range(4)]
    for k, s_ in enumerate("ABCD"):
        els = chipm(f, *spots[k], s_, "q", c=("coral", "teal", "sky", "gold")[k], z=32)
        nx, ny = spots[(k + 1) % 4]
        for el in els:
            el["mv"] = {"at": 1, "dx": R1(nx - spots[k][0]), "dy": R1(ny - spots[k][1]), "dl": 300}
    f.text(O[0], O[1] + 14, "회전", z=22, c="soft", at=1, dl=200, b=800)
    rots = ["ABCD", "DABC", "CDAB", "BCDA"]
    for j, rs in enumerate(rots):
        cx0 = 105 + 150 * j
        f.circ(cx0, 560, 46, at=1, c="soft", sw=2, dl=600 + 200 * j)
        for k, s in enumerate(rs):
            a = math.radians(90 - 90 * k)
            f.text(cx0 + 46 * math.cos(a), 560 - 46 * math.sin(a) + 7, s, z=18, at=1, dl=700 + 200 * j, b=800)
        if j:
            f.text(cx0 - 75, 568, "=", z=26, c="gold", at=1, dl=700 + 200 * j, b=800)
    f.text(CX, 650, "24 ÷ 4 = 6", z=30, c="gold", at=2, b=800)
    U.ex("h3-2-01", "A, B, C, D 4명이 원탁에 둘러앉는 경우의 수를 구해 보자.", "돌려서 같아지는 배치는 하나로 — (n − 1)!",
         [L("4명을 일렬로: 4 × 3 × 2 × 1 = 24"),
          L("돌려서 같은 배치가 4개씩", memo="원탁은 회전해도 이웃이 그대로"),
          L("24 ÷ 4 = 6", memo="(4 − 1)! = 3!")],
         "6", f.out(), at=("b2", 2))

    # ── 02 중복조합 — ○와 칸막이 ───────────────────────────────
    f = Fig()
    xs = [100 + 92 * k for k in range(6)]
    for x in xs:
        f.rect(x - 38, 170, 76, 90, at="q", c="soft", sw=2, rx=10)
    arr1 = {"c1": 0, "c2": 1, "b1": 2, "c3": 3, "b2": 4, "c4": 5}
    arr2 = {"c1": 0, "b1": 1, "c2": 2, "c3": 3, "c4": 4, "b2": 5}
    for key, slot in arr1.items():
        x = xs[slot]
        if key[0] == "c":
            el = f.circ(x, 215, 26, at=0, c="teal", sw=3, f="teal", fo=0.4, dl=100 * slot)
        else:
            el = f.rect(x - 6, 180, 12, 72, at=0, c="coral", sw=2, f="coral", fo=0.8, dl=100 * slot)
        if arr2[key] != slot:
            slide(el, 1, dx=xs[arr2[key]] - x, dl=300)
    f.text(CX, 320, "x, y, z = 2, 1, 1", z=28, c="ink", at=0, dl=800, b=800, un=1)
    f.text(CX, 320, "x, y, z = 1, 3, 0", z=28, c="ink", at=1, dl=1300, b=800)
    f.text(CX, 120, "○ 4개 · 칸막이 2개", z=24, c="soft", at=0, b=800)
    f.text(CX, 470, "6자리 중 칸막이 2자리", z=28, c="coral", at=2, b=800)
    f.text(CX, 560, "{6 × 5/2 × 1} = 15", z=36, c="gold", at=2, dl=400, b=800)
    U.ex("h3-2-02", "x + y + z = 4를 만족하는 음이 아닌 정수 x, y, z의 순서쌍의 개수를 구해 보자.", "○ 4개와 칸막이 2개의 배열 — 칸막이 자리만 고르면 된다(3H4 = 6C4)",
         [L("○ 4개와 칸막이 | 2개를 한 줄로", memo="칸막이가 x, y, z 세 칸으로 나눈다"),
          L("○○|○|○ → (2, 1, 1), ○|○○○| → (1, 3, 0)", memo="칸막이를 옮기면 다른 해"),
          L("{6 × 5/2 × 1} = 15", memo="6자리 중 칸막이 2자리 — 6C2")],
         "15", f.out(), at=("b4", 1))

    # ── 03 이항정리 — 파스칼의 삼각형 ───────────────────────────
    f = Fig()
    rows = [[math.comb(n, k) for k in range(n + 1)] for n in range(5)]
    pos = {}
    for n, row in enumerate(rows):
        for k, v in enumerate(row):
            x, y = CX + (k - n / 2) * 96, 110 + 92 * n
            pos[(n, k)] = (x, y)
            dl = 150 * k + 300 * n
            col = "gold" if (n == 4 and k == 1) else ("teal" if n == 4 else "ink")
            e = f.text(x, y, str(v), z=34, c=col, at=0, dl=dl, b=800)
            if 0 < k < n:
                for (pn, pk) in ((n - 1, k - 1), (n - 1, k)):
                    px, py = pos[(pn, pk)]
                    f.line(px, py + 10, x, y - 30, at=0, c="soft", w=2, dr=True, dl=dl - 100)
    f.text(560, 110 + 92 * 4 + 50, "4C_{r}", z=22, c="teal", at=0, dl=2800, b=800)
    f.text(CX, 590, "x^{3}: r = 1", z=30, c="coral", at=1, b=800)
    f.circ(*pos[(4, 1)], 30, at=2, c="gold", sw=4, dl=0)
    f.text(CX, 660, "4 × 2^{1} = 8", z=34, c="gold", at=2, dl=400, b=800)
    U.ex("h3-2-03", "(x + 2)^{4}의 전개식에서 x^{3}의 계수를 구해 보자.", "일반항 4Cr × x^{4 − r} × 2^{r} — 원하는 차수가 되는 r를 찾는다",
         [L("일반항 4Cr × x^{4 − r} × 2^{r}", memo="계수는 파스칼 삼각형의 넷째 줄"),
          L("4 − r = 3 → r = 1", memo="x^{3}이 되려면"),
          L("4 × 2^{1} = 8", memo="4C1 = 4")],
         "8", f.out(), at=("b3", 1))

    # ── 04 확률의 뜻 — 주사위 두 개 ────────────────────────────
    f = Fig()
    x0, y0, cs = 150, 120, 72
    for i in range(6):
        f.text(x0 + cs * i + cs / 2, y0 - 16, str(i + 1), z=24, c="coral", at="q", b=800)
        f.text(x0 - 22, y0 + cs * i + cs / 2 + 8, str(i + 1), z=24, c="teal", at="q", b=800)
    k = 0
    for i in range(6):
        for j in range(6):
            s = i + j + 2
            f.rect(x0 + cs * j, y0 + cs * i, cs, cs, at=0, c="ink", sw=1.2, dl=1 + 25 * k)
            f.text(x0 + cs * j + cs / 2, y0 + cs * i + cs / 2 + 8, str(s), z=20, c="soft", at=0, dl=20 + 25 * k)
            if s == 7:
                f.rect(x0 + cs * j + 4, y0 + cs * i + 4, cs - 8, cs - 8, at=1, c="gold", sw=3, f="gold", fo=0.45, rx=6, dl=250 * i)
            k += 1
    f.text(CX + 30, 600, "{6/36} = {1/6}", z=36, c="gold", at=2, b=800)
    U.ex("h3-2-04", "주사위 두 개를 던질 때 나온 눈의 합이 7일 확률을 구해 보자.", "P(A) = {n(A)/n(S)} — 같은 가능성의 경우를 센다",
         [L("n(S) = 6 × 6 = 36", memo="36칸"),
          L("합이 7: (1, 6), (2, 5), …, (6, 1) — 6가지", memo="대각선 한 줄"),
          L("P = {6/36} = {1/6}")],
         "{1/6}", f.out(), at=("b4", 1))

    # ── 05 여사건 — 적어도 하나 ─────────────────────────────────
    f = Fig()
    outs = [(a, b, c) for a in (1, 0) for b in (1, 0) for c in (1, 0)]
    for k, o in enumerate(outs):
        cx0 = 110 + 150 * (k % 4)
        cy0 = 180 + 160 * (k // 4)
        for j, h in enumerate(o):
            coin(f, cx0 - 40 + 40 * j, cy0, h, 0, dl=80 * k)
        if o == (0, 0, 0):
            f.rect(cx0 - 70, cy0 - 36, 140, 72, at=1, c="red", sw=4, rx=12)
            f.cross(cx0, cy0, s=60, at=2, c="red", dl=200)
        else:
            f.rect(cx0 - 70, cy0 - 36, 140, 72, at=2, c="gold", sw=3, rx=12, d=True, dl=400 + 60 * k)
    f.text(CX, 480, "모두 뒷면 {1/8}", z=28, c="red", at=1, dl=300, b=800)
    f.text(CX, 580, "1 − {1/8} = {7/8}", z=38, c="gold", at=2, dl=900, b=800)
    U.ex("h3-2-05", "동전 3개를 던질 때 적어도 하나는 앞면이 나올 확률을 구해 보자.", "'적어도 하나'는 반대(하나도 없음)를 1에서 뺀다",
         [L("전체 2 × 2 × 2 = 8가지"),
          L("모두 뒷면: 1가지 → {1/8}", memo="여사건"),
          L("1 − {1/8} = {7/8}", memo="P(A^{c}) = 1 − P(A)")],
         "{7/8}", f.out(), at=("b4", 1))

    # ── 06 조건부확률 — 표 ─────────────────────────────────────
    f = Fig()
    cx_ = [120, 270, 410, 550]
    ry = [180, 280, 380]
    for x, h in zip(cx_, ["", "안경 O", "안경 X", "합"]):
        f.text(x, ry[0], h, z=26, c="soft", at="q", b=800)
    for r_, row in enumerate((["남", "12", "18", "30"], ["여", "8", "12", "20"])):
        for x, v in zip(cx_, row):
            f.text(x, ry[r_ + 1], v, z=32, at="q", b=800 if x == 120 else 700)
    f.line(60, 215, 610, 215, at="q", c="ink", w=2.5)
    f.line(480, 140, 480, 410, at="q", c="ink", w=2, d=True)
    f.rect(60, 330, 550, 76, at=0, c="none", f="soft", fo=0.6)
    f.rect(60, 232, 550, 76, at=0, c="gold", sw=4, rx=12, dl=300)
    f.text(CX, 460, "남학생 30명만 남긴다", z=24, c="gold", at=0, dl=700, b=800)
    f.circ(270, 270, 36, at=1, c="coral", sw=4)
    f.text(CX, 580, "{12/30} = {2/5}", z=40, c="gold", at=2, b=800)
    U.ex("h3-2-06", "남학생 30명, 여학생 20명 중 안경을 쓴 학생이 남 12명, 여 8명이다. 남학생을 한 명 뽑았을 때 안경을 썼을 확률을 구해 보자.", "조건(남학생)의 줄만 남기고 그 안에서 비율 — 분모가 전체에서 조건으로 줄어든다",
         [L("조건: 남학생 30명만 본다", memo="분모가 50에서 30으로"),
          L("그중 안경 12명"),
          L("P(안경 | 남) = {12/30} = {2/5}")],
         "{2/5}", f.out(), at=("b4", 1))

    # ── 07 독립시행 — 앞면 3번의 자리 ───────────────────────────
    f = Fig()
    from itertools import combinations
    combs = list(combinations(range(5), 3))
    for r_, cmb in enumerate(combs):
        cx0 = 80 + 300 * (r_ // 5)
        cy0 = 110 + 72 * (r_ % 5)
        for j in range(5):
            coin(f, cx0 + 50 * j, cy0, j in cmb, 0, r=17, dl=180 * r_)
    f.text(CX, 500, "앞면 자리 고르기 10가지", z=26, c="teal", at=0, dl=1900, b=800)
    f.rect(55, 110 - 30, 250, 60, at=1, c="gold", sw=4, rx=12)
    f.text(CX, 560, "한 줄의 확률 ({1/2})^{5} = {1/32}", z=26, c="gold", at=1, dl=300, b=800)
    f.text(CX, 640, "10 × {1/32} = {5/16}", z=34, c="gold", at=2, b=800)
    U.ex("h3-2-07", "동전을 5번 던질 때 앞면이 정확히 3번 나올 확률을 구해 보자.", "독립시행 — (몇 번째에 성공할지 고르기) × (성공)^{r} × (실패)^{n − r}",
         [L("앞면이 나올 회차 3개 고르기: {5 × 4 × 3/3 × 2 × 1} = 10", memo="5C3"),
          L("한 경우의 확률 ({1/2})^{5} = {1/32}", memo="매번 독립"),
          L("10 × {1/32} = {5/16}")],
         "{5/16}", f.out(), at=("b4", 1))

    # ── 08 확률분포 — 앞면의 개수 ───────────────────────────────
    f = Fig()
    outs = [(1, 1), (1, 0), (0, 1), (0, 0)]
    bins = {0: 190, 1: 330, 2: 470}
    stack = {0: 0, 1: 0, 2: 0}
    for k, o in enumerate(outs):
        cx0 = 120 + 140 * k
        X = sum(o)
        tx, ty = bins[X], 560 - 70 * stack[X]
        stack[X] += 1
        for j, h in enumerate(o):
            c = "teal" if h else "coral"
            e1 = f.circ(cx0 - 22 + 44 * j, 120, 18, at="q", c=c, sw=2.5, f=c, fo=0.35, dl=100 * k)
            e2 = f.text(cx0 - 22 + 44 * j, 128, "앞" if h else "뒤", z=18, c=c, at="q", dl=100 * k, b=800)
            for el in (e1, e2):
                el["mv"] = {"at": 1, "dx": R1(tx - 22 + 44 * j - (cx0 - 22 + 44 * j)), "dy": R1(ty - 120), "dl": 250 * k}
    f.line(110, 600, 560, 600, at=1, c="ink", w=3)
    for X, x in bins.items():
        f.text(x, 640, f"X = {X}", z=24, c="ink", at=1, b=800)
    for X, (x, p) in {0: (190, "{1/4}"), 1: (330, "{2/4}"), 2: (470, "{1/4}")}.items():
        f.text(x, 560 - 70 * stack[X] - 10, p, z=28, c="gold", at=2, dl=200 * X, b=800)
    f.text(CX, 250, "{1/4} + {2/4} + {1/4} = 1", z=26, c="gold", at=2, dl=900, b=800)
    U.ex("h3-2-08", "동전 2개를 던져 나온 앞면의 개수를 X라 할 때, X의 확률분포를 구해 보자.", "X의 값마다 경우를 모아 확률을 적는다 — 확률의 합은 1",
         [L("앞앞, 앞뒤, 뒤앞, 뒤뒤 — 4가지"),
          L("X = 0: 1가지, X = 1: 2가지, X = 2: 1가지", memo="앞면 개수대로 모으기"),
          L("{1/4} + {2/4} + {1/4} = 1", memo="확률의 합")],
         "X = 0, 1, 2일 때 확률 {1/4}, {1/2}, {1/4}", f.out(), at=("b4", 1))

    # ── 09 기댓값 — 무게중심 ───────────────────────────────────
    f = Fig()
    X = lambda v: 130 + 200 * v
    f.line(70, 420, 590, 420, at="q", c="ink", w=4)
    for v, p in ((0, 1), (1, 2), (2, 1)):
        f.rect(X(v) - 34, 420 - 70 * p, 68, 70 * p, at="q", c="ink", sw=2.5, f="teal", fo=0.4)
        f.text(X(v), 460, str(v), z=28, at="q", b=800)
        f.text(X(v), 420 - 70 * p - 14, "{" + str(p) + "/4}", z=24, c="teal", at="q", b=800)
    tri = f.poly([(X(1), 430), (X(1) - 26, 480), (X(1) + 26, 480)], at=1, c="gold", w=3, f="gold", fo=0.7)
    tri["fr"] = {"dx": R1(X(1.8) - X(1)), "dy": 0, "dl": 200, "ms": 1100}
    f.text(X(1), 540, "E(X) = 1", z=32, c="gold", at=1, dl=1400, b=800)
    f.text(CX, 620, "확률을 무게로 한 균형점", z=24, c="gold", at=2, b=800)
    U.ex("h3-2-09", "X가 0, 1, 2일 확률이 각각 {1/4}, {1/2}, {1/4}일 때 기댓값 E(X)를 구해 보자.", "E(X) = Σ(값 × 확률) — 확률을 무게로 한 평균",
         [L("E(X) = 0 × {1/4} + 1 × {1/2} + 2 × {1/4}"),
          L("0 × {1/4} + 1 × {1/2} + 2 × {1/4} = 1"),
          L("균형을 이루는 자리 1", memo="좌우대칭이라 가운데")],
         "1", f.out(), at=("b2", 2))

    # ── 10 이항분포 ────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (28, 72), (0, 0.085), box=(60, 120, 620, 560), square=False)
    f.line(P.X(28), P.Y(0), P.X(72), P.Y(0), at="q", c="ink", w=3, ar=1)
    for kk in range(30, 71):
        p = math.comb(100, kk) / 2 ** 100
        f.rect(P.X(kk - 0.45), P.Y(p), P.X(0.9) - P.X(0), P.Y(0) - P.Y(p), at="q", c="none", f="sky", fo=0.6, dl=15 * (kk - 30))
    for v in (30, 40, 50, 60, 70):
        f.text(P.X(v), P.Y(0) + 30, str(v), z=20, c="soft", at="q")
    f.line(*P.P(50, 0), *P.P(50, 0.085), at=0, c="gold", w=3.5, dr=True)
    f.text(P.X(50), P.Y(0.085) - 12, "평균 50", z=24, c="gold", at=0, dl=500, b=800)
    f.line(P.X(45), P.Y(0.02), P.X(55), P.Y(0.02), at=2, c="coral", w=4, ar=2, dr=True)
    f.text(P.X(50), P.Y(0.02) + 40, "± 5", z=26, c="coral", at=2, dl=500, b=800)
    f.text(CX, 640, "분산 25", z=28, c="teal", at=1, b=800)
    U.ex("h3-2-10", "동전을 100번 던질 때 앞면이 나오는 횟수 X의 평균, 분산, 표준편차를 구해 보자.", "X ~ B(n, p) — E(X) = np, V(X) = npq",
         [L("E(X) = 100 × {1/2} = 50"),
          L("V(X) = 100 × {1/2} × {1/2} = 25"),
          L("σ(X) = √{25} = 5", memo="평균 주위 ±5")],
         "평균 50, 분산 25, 표준편차 5", f.out(), at=("b3", 1))

    # ── 11 정규분포 — 표준화 ───────────────────────────────────
    f = Fig()
    P = Plane(f, (-3.3, 3.3), (0, 0.45), box=(60, 120, 620, 520), square=False)
    phi = lambda z: math.exp(-z * z / 2) / math.sqrt(2 * math.pi)
    f.line(P.X(-3.3), P.Y(0), P.X(3.3), P.Y(0), at="q", c="ink", w=3)
    P.curve(phi, at="q", c="sky", w=4.5)
    for zv in range(-3, 4):
        f.text(P.X(zv), P.Y(0) + 30, str(70 + 10 * zv), z=20, c="soft", at="q", un=0)
        f.text(P.X(zv), P.Y(0) + 30, ("−" if zv < 0 else "") + str(abs(zv)), z=22, c="teal", at=0, dl=300 + 80 * (zv + 3), b=800)
    f.text(P.X(3.2), P.Y(0) + 66, "Z", z=22, c="teal", at=0, dl=900, b=800)
    f.text(P.X(-3.1), P.Y(0) + 66, "X → Z", z=20, c="soft", at=0, dl=900, b=800, a="s")
    pts = [P.P(1, 0)] + [P.P(1 + k * 0.1, phi(1 + k * 0.1)) for k in range(24)] + [P.P(3.3, 0)]
    f.poly(pts, at=1, c="none", f="coral", fo=0.5)
    f.text(P.X(1.9), P.Y(0.17), "P(Z ≥ 1)", z=22, c="coral", at=1, dl=300, b=800)
    pts = [P.P(0, 0)] + [P.P(k * 0.05, phi(k * 0.05)) for k in range(21)] + [P.P(1, 0)]
    f.poly(pts, at=2, c="none", f="gold", fo=0.45)
    f.text(P.X(0.5), P.Y(0.12), "0.3413", z=22, at=2, dl=300, b=800)
    f.text(CX, 620, "0.5 − 0.3413 = 0.1587", z=30, c="gold", at=2, dl=700, b=800)
    U.ex("h3-2-11", "X가 정규분포 N(70, 10^{2})을 따를 때 P(X ≥ 80)을 구해 보자. (P(0 ≤ Z ≤ 1) = 0.3413)", "Z = {X − m/σ}로 표준화 — 평균에서 표준편차 몇 개인가",
         [L("Z = {X − 70/10}", memo="눈금을 X에서 Z로"),
          L("P(X ≥ 80) = P(Z ≥ 1)", memo="80은 평균에서 표준편차 1개"),
          L("0.5 − 0.3413 = 0.1587", memo="오른쪽 절반에서 0 ~ 1을 뺀다")],
         "0.1587", f.out(), at=("b4", 1))

    # ── 12 표본평균의 분포 ─────────────────────────────────────
    f = Fig()
    P = Plane(f, (-3.3, 3.3), (0, 1.7), box=(60, 80, 620, 560), square=False)
    f.line(P.X(-3.3), P.Y(0), P.X(3.3), P.Y(0), at="q", c="ink", w=3)
    f.text(P.X(0), P.Y(0) + 32, "m", z=26, at="q", b=800)
    for k, (s, col) in enumerate(((1, "soft"), (0.5, "teal"), (0.25, "coral"))):
        fn = lambda z, s=s: math.exp(-z * z / (2 * s * s)) / (s * math.sqrt(2 * math.pi))
        P.curve(fn, at=k if k else "q", c=col, w=3.5 if k == 0 else 4.5, n=120)
    f.text(P.X(1.9), P.Y(0.3), "모집단 σ", z=22, c="soft", at="q", b=800)
    f.text(P.X(1.2), P.Y(0.8), "n = 4: {σ/2}", z=22, c="teal", at=1, dl=600, b=800, a="s")
    f.text(P.X(0.6), P.Y(1.55), "n = 16: {σ/4}", z=22, c="coral", at=2, dl=600, b=800, a="s")
    U.ex("h3-2-12", "모표준편차가 σ인 모집단에서 크기 4, 16인 표본을 뽑을 때 표본평균의 표준편차를 비교해 보자.", "σ(X̄) = {σ/√{n}} — 많이 뽑을수록 표본평균이 m 근처에 모인다",
         [L("모집단: 평균 m, 표준편차 σ"),
          L("n = 4: σ(X̄) = {σ/√{4}} = {σ/2}"),
          L("n = 16: σ(X̄) = {σ/√{16}} = {σ/4}", memo="n이 4배면 퍼짐은 절반")],
         "{σ/2}, {σ/4}", f.out(), at=("b4", 1))

    # ── 13 신뢰구간의 길이 ─────────────────────────────────────
    f = Fig()
    nl = NL(f, 44, 56, y=470, x0=60, x1=600, step=1, lab_step=2, z=22)
    f.dot(nl.X(50), 470, r=12, f="ink", at="q")
    f.text(nl.X(50), 430, "X̄ = 50", z=24, at="q", b=800)
    for k, (h, col, y) in enumerate(((3.92, "teal", 330), (1.96, "coral", 250))):
        f.line(nl.X(50 - h), y, nl.X(50 + h), y, at=k, c=col, w=8, dr=True)
        for sgn in (-1, 1):
            f.line(nl.X(50 + sgn * h), y - 18, nl.X(50 + sgn * h), y + 18, at=k, c=col, w=3, dl=400)
            f.line(nl.X(50 + sgn * h), y + 18, nl.X(50 + sgn * h), 460, at=k, c=col, w=2, d=True, dl=500)
        f.text(nl.X(50), y - 30, ("n = 25" if k == 0 else "n = 100"), z=24, c=col, at=k, dl=600, b=800)
    f.text(CX, 600, "n을 4배 → 길이 절반", z=30, c="gold", at=2, b=800)
    U.ex("h3-2-13", "모표준편차 10, 표본평균 50일 때 표본의 크기가 25, 100인 경우의 모평균 m의 신뢰도 95% 신뢰구간을 비교해 보자.", "X̄ ± 1.96 × {σ/√{n}} — n이 커질수록 좁아진다",
         [L("n = 25: 50 ± 1.96 × {10/√{25}} = 50 ± 3.92", memo="{10/5} = 2"),
          L("n = 100: 50 ± 1.96 × {10/√{100}} = 50 ± 1.96", memo="{10/10} = 1"),
          L("n을 4배 → 길이는 절반", memo="√{n}이 2배")],
         "n이 4배면 신뢰구간의 길이는 {1/2}배", f.out(), at=("b3", 1))

    # ── 14 모비율의 추정 ───────────────────────────────────────
    f = Fig()
    for k in range(100):
        r_, c_ = divmod(k, 20)
        col = "coral" if k < 20 else "soft"
        f.dot(80 + 26 * c_, 110 + 26 * r_, r=9, f=col, at="q" if k >= 20 else 0, dl=0 if k >= 20 else 50 * k)
    f.text(CX, 270, "100명 중 20명", z=26, c="coral", at=0, dl=1100, b=800)
    class _NL:
        y = 470

        @staticmethod
        def X(v):
            return 70 + 520 * v / 0.4
    nl = _NL()
    f.line(60, 470, 604, 470, at=1, c="ink", w=3, ar=1)
    for k in range(9):
        v = 0.05 * k
        f.line(nl.X(v), 470 - (12 if k % 2 == 0 else 7), nl.X(v), 470 + (12 if k % 2 == 0 else 7), at=1, c="ink", w=2.5 if k % 2 == 0 else 1.5)
        if k % 2 == 0:
            f.text(nl.X(v), 514, ("0" if k == 0 else f"0.{k // 2}"), z=20, c="soft", at=1)
    f.dot(nl.X(0.2), 470, r=12, f="coral", at=1, dl=300)
    f.text(nl.X(0.2), 420, "p̂ = 0.2", z=24, c="coral", at=1, dl=400, b=800)
    lo, hi = 0.2 - 0.0784, 0.2 + 0.0784
    f.line(nl.X(lo), 380, nl.X(hi), 380, at=2, c="gold", w=8, dr=True)
    for v in (lo, hi):
        f.line(nl.X(v), 362, nl.X(v), 398, at=2, c="gold", w=3, dl=400)
    f.text(nl.X(lo), 600, "0.12", z=24, c="gold", at=2, dl=600, b=800)
    f.text(nl.X(hi), 600, "0.28", z=24, c="gold", at=2, dl=700, b=800)
    U.ex("h3-2-14", "100명을 조사해 20명이 찬성했을 때, 모비율 p의 신뢰도 95% 신뢰구간을 구해 보자.", "표본비율 p̂에서 양쪽으로 1.96 × (표준편차)",
         [L("p̂ = {20/100} = 0.2"),
          L("√{0.0016} = 0.04", memo="표준편차 — 0.2 × 0.8 ÷ 100 = 0.0016"),
          L("0.2 ± 1.96 × 0.04 = 0.2 ± 0.0784", memo="약 0.12에서 0.28")],
         "약 0.12 ≤ p ≤ 0.28", f.out(), at=("b4", 1))
