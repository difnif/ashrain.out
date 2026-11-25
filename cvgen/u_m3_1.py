# 중3-1 — 제곱근과 실수 · 다항식의 곱셈과 인수분해 · 이차방정식 · 이차함수
import math
import sympy as sp
from cv import *
from figs import slide, slides, Strip, tw, CX, hop, travel, parabola, arcp


def rad(f, x0, x1, y, z, at, c="ink", dl=0, un=None, w=3):
    """근호 — 안쪽 글자가 x0 ~ x1, 글자 바탕선 y, 글자 크기 z"""
    pts = [(x0 - 0.62 * z, y - 0.34 * z), (x0 - 0.46 * z, y - 0.42 * z), (x0 - 0.26 * z, y + 0.12 * z), (x0 - 0.06 * z, y - 0.98 * z), (x1 + 0.08 * z, y - 0.98 * z)]
    return f.poly(pts, at=at, c=c, w=w, z=False, dr=True, dl=dl, un=un)


def qbez(P0, P1, P2, n=18):
    return [((1 - t) ** 2 * P0[0] + 2 * (1 - t) * t * P1[0] + t * t * P2[0], (1 - t) ** 2 * P0[1] + 2 * (1 - t) * t * P1[1] + t * t * P2[1]) for t in (k / n for k in range(n + 1))]


def tile(f, x, y, w, h, s, c, at, dl=0, un=None, z=26, fo=0.3):
    """칸(가운데 x, y) + 글자 — 두 요소"""
    r = f.rect(x - w / 2, y - h / 2, w, h, at=at, c=c, sw=3, rx=8, f=c, fo=fo, dl=dl, un=un)
    t = f.text(x, y + z * 0.36, s, z=z, c=c, at=at, dl=dl + 40, un=un, b=800)
    return [r, t]


def cell(f, x, y, w, h, c, at, s=None, z=30, dl=0, fo=0.35, tc=None, un=None):
    r = f.rect(x, y, w, h, at=at, c="ink", sw=2.5, f=c, fo=fo, dl=dl, un=un)
    if s:
        f.text(x + w / 2, y + h / 2 + z * 0.36, s, z=z, c=tc or c, at=at, dl=dl + 200, b=800, un=un)
    return r


def mvr(el, at, dx, dy, r, dl=0):
    """제자리 가운데를 중심으로 r 도 돌리면서 (dx, dy) 옮기기"""
    if el["k"] == "R":
        cx, cy = el["x"] + el["w"] / 2, el["y"] + el["h"] / 2
    else:
        xs = [p[0] for p in el["pts"]]
        ys = [p[1] for p in el["pts"]]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    el["mv"] = {"at": at, "dx": R1(dx), "dy": R1(dy), "r": R1(r), "cx": R1(cx), "cy": R1(cy)}
    if dl:
        el["mv"]["dl"] = int(dl)
    return el


def build(U):
    # ── 01 제곱근의 뜻 — 넓이 5인 정사각형 ─────────────────────
    f = Fig()
    g, ox, oy = 120, 150, 520

    def G(i, j):
        return (ox + g * i, oy - g * j)

    for i in range(4):
        for j in range(4):
            f.dot(*G(i, j), r=6, f="soft", at="q")
    f.poly([G(1, 0), G(3, 1), G(2, 3), G(0, 2)], at="q", c="teal", w=4, f="teal", fo=0.25)
    f.poly([G(0, 0), G(3, 0), G(3, 3), G(0, 3)], at=0, c="ink", w=2.5, d=True)
    f.text(*G(1.5, 3.2), "3 × 3 = 9", z=26, at=0, dl=200, b=800)
    tris = [[G(0, 0), G(1, 0), G(0, 2)], [G(1, 0), G(3, 0), G(3, 1)], [G(3, 1), G(3, 3), G(2, 3)], [G(2, 3), G(0, 3), G(0, 2)]]
    outs = [(-46, 46), (46, 46), (46, -46), (-46, -46)]
    for k, (t, (dx, dy)) in enumerate(zip(tris, outs)):
        el = f.poly(t, at=0, c="coral", w=2.5, f="coral", fo=0.35, dl=500 + 200 * k)
        el["mv"] = {"at": 0, "dx": dx, "dy": dy, "dl": 1500 + 120 * k}
    f.text(560, 600, "귀퉁이 넷 = 4", z=24, c="coral", at=0, dl=2300, b=800)
    f.text(*G(1.5, 1.38), "5", z=56, c="teal", at=1, b=800)
    f.text(G(2.3, 0.3)[0] + 18, G(2.3, 0.3)[1] + 20, "√{5}", z=36, c="gold", at=2, b=800, a="s")
    U.ex("m3-1-01", "넓이가 5인 정사각형의 한 변의 길이를 구해 보자.", "제곱해서 5가 되는 양수 — 5의 양의 제곱근",
         [L("3 × 3 − 4 × 1 = 5", memo="3 × 3 정사각형에서 넓이 1인 귀퉁이 넷을 뺀다"),
          L("(한 변)^{2} = 5", memo="제곱해서 5"),
          L("한 변 = √{5}", memo="5의 제곱근은 ±√{5} — 길이는 양수")],
         "√{5}", f.out(), at=("b3", 1))

    # ── 02 무리수 √2 를 수직선 위에 ─────────────────────────────
    f = Fig()
    nl = NL(f, -1, 3, y=480, x0=60, x1=620, step=1, lab_step=1, z=24)
    u = nl.X(1) - nl.X(0)
    O = (nl.X(0), 480)
    f.rect(O[0], 480 - u, u, u, at="q", c="ink", sw=3, f="teal", fo=0.15)
    f.text(O[0] + u / 2, 480 - u - 14, "1", z=26, at="q", b=800)
    f.text(O[0] - 18, 480 - u / 2 + 8, "1", z=26, at="q", b=800, a="e")
    f.line(O[0], 480, O[0] + u, 480 - u, at=0, c="coral", w=5, dr=True)
    f.text(O[0] + u * 0.42, 480 - u * 0.62, "√{2}", z=30, c="coral", at=1, b=800, a="e")
    cp = f.line(O[0], 480, O[0] + u, 480 - u, at=2, c="coral", w=5)
    cp["mv"] = {"at": 2, "r": 45, "cx": R1(O[0]), "cy": 480, "dl": 200}
    arcp(f, O[0], 480, u * math.sqrt(2), 0, 45, at=2, c="gold", sw=3, rv=True, dl=200)
    xs2 = nl.X(math.sqrt(2))
    f.dot(xs2, 480, r=11, f="gold", at=2, dl=1200)
    f.text(xs2, 430, "√{2}", z=30, c="gold", at=2, dl=1300, b=800)
    f.text(xs2, 600, "1.414…", z=28, c="gold", at=2, dl=1500, b=800)
    U.ex("m3-1-02", "한 변이 1인 정사각형의 대각선을 이용해 √{2}를 수직선 위에 나타내 보자.", "대각선의 길이 √{2}를 컴퍼스로 수직선에 옮긴다",
         [L("(대각선)^{2} = 1^{2} + 1^{2} = 2", memo="피타고라스 정리"),
          L("대각선 = √{2}", memo="제곱해서 2가 되는 양수"),
          L("√{2} = 1.414…", memo="끝없이, 되풀이 없이 — 무리수도 수직선 위의 한 점")],
         "0에서 대각선만큼 간 점 √{2}", f.out(), at=("b4", 1))

    # ── 03 실수의 대소 — √13 은 3 과 4 사이 ─────────────────────
    f = Fig()
    X1 = lambda v: 50 + (620 - 50) * v / 17
    f.line(40, 200, 632, 200, at="q", c="ink", w=3, ar=1)
    for v in range(18):
        big = v in (0, 1, 4, 9, 16)
        f.line(X1(v), 200 - (10 if big else 6), X1(v), 200 + (10 if big else 6), at="q", c="ink", w=2.5 if big else 1.5)
        if big:
            f.text(X1(v), 244, str(v), z=24, c="gold", at="q", b=800)
    f.text(600, 160, "제곱", z=22, c="soft", at="q", b=700)
    nl = NL(f, 0, 4.5, y=500, x0=50, x1=620, step=0.5, lab_step=1, z=24)
    f.text(600, 460, "수", z=22, c="soft", at="q", b=700)
    for v, col, dl in ((9, "soft", 0), (13, "coral", 300), (16, "soft", 600)):
        f.dot(X1(v), 200, r=10, f=col if col != "soft" else "ink", at=0, dl=dl)
    f.text(X1(13), 160, "13", z=28, c="coral", at=0, dl=300, b=800)
    for k, (sq, v, col) in enumerate(((9, 3, "teal"), (16, 4, "teal"), (13, math.sqrt(13), "coral"))):
        f.line(X1(sq), 212, nl.X(v), 488, at=1, c=col, w=3, d=col != "coral", dr=True, ar=1, dl=450 * k)
    f.dot(nl.X(math.sqrt(13)), 500, r=11, f="coral", at=1, dl=1500)
    f.line(nl.X(3), 560, nl.X(4), 560, at=2, c="gold", w=7, dr=True)
    f.text(nl.X(3.5), 620, "3 < √{13} < 4", z=34, c="gold", at=2, dl=500, b=800)
    f.text(nl.X(math.sqrt(13)), 460, "√{13}", z=26, c="coral", at=2, dl=200, b=800)
    U.ex("m3-1-03", "√{13}은 어떤 두 정수 사이에 있을까?", "제곱수 사이에 끼워 넣기 — 양수끼리는 제곱이 크면 수도 크다",
         [L("9 < 13 < 16", memo="13 앞뒤의 제곱수"),
          L("√{9} < √{13} < √{16}", memo="제곱의 순서 그대로 내려온다"),
          L("3 < √{13} < 4")],
         "3과 4 사이", f.out(), at=("b3", 1))

    # ── 04 근호 안의 제곱인수를 밖으로 ─────────────────────────
    f = Fig()
    z = 58
    f.text(CX, 170, "12", z=z, at="q", b=700)
    rad(f, CX - 38, CX + 38, 170, z, "q")
    rad(f, 270, 410, 340, z, 0)
    for s, x, col in (("4", 298, "coral"), ("×", 340, "ink"), ("3", 382, "ink")):
        el = f.text(x, 340, s, z=z, c=col, at=0, dl=200, b=700)
        if s != "×":
            fly(el, CX - x, 170 - 340, dl=60, ms=700)
    f.text(560, 300, "4 = 2^{2}", z=26, c="coral", at=0, dl=1200, b=800)
    e2 = f.text(250, 520, "2", z=z + 6, c="coral", at=1, dl=200, b=800)
    fly(e2, 298 - 250, 340 - 520, dl=80, ms=900)
    f.poly(qbez((298, 270), (200, 200), (250, 455)), at=1, c="gold", w=3.5, z=False, dr=True, ar=1, dl=100)
    f.text(150, 330, "√{4} = 2", z=26, c="gold", at=1, dl=500, b=800)
    rad(f, 330, 370, 520, z, 1, dl=300)
    e3 = f.text(350, 520, "3", z=z, at=1, dl=300, b=700)
    fly(e3, 382 - 350, 340 - 520, dl=80, ms=800)
    U.ex("m3-1-04", "√{12}를 a√{b} 꼴로 나타내 보자.", "근호 안의 제곱인수를 밖으로 꺼낸다",
         [L("√{12} = √{4 × 3}", memo="12 안의 제곱수 4"),
          L("√{4 × 3} = √{4} × √{3} = 2√{3}", memo="√{4} = 2가 근호 밖으로")],
         "2√{3}", f.out(), at=("b3", 1))

    # ── 05 근호 안이 같은 것끼리 ───────────────────────────────
    f = Fig()
    f.text(220, 150, "√{18}", z=48, at="q", b=700)
    f.text(330, 150, "+", z=48, at="q", b=700)
    f.text(430, 150, "√{8}", z=48, at="q", b=700)
    tw_, th_ = 84, 60
    teal_t, coral_t = [], []
    for k in range(3):
        t = tile(f, 130 + 92 * k, 300, tw_, th_, "√{2}", "teal", 0, dl=250 * k)
        for e in t:
            fly(e, 220 - (130 + 92 * k), -150, dl=40, ms=600)
        teal_t.append(t)
    f.text(222, 380, "3√{2}", z=28, c="teal", at=0, dl=1100, b=800, un=2)
    for k in range(2):
        t = tile(f, 450 + 92 * k, 300, tw_, th_, "√{2}", "coral", 1, dl=250 * k)
        for e in t:
            fly(e, 430 - (450 + 92 * k), -150, dl=40, ms=600)
        coral_t.append(t)
    f.text(496, 380, "2√{2}", z=28, c="coral", at=1, dl=900, b=800, un=2)
    for k, t in enumerate(teal_t + coral_t):
        tx = 146 + 92 * k
        ox_ = 130 + 92 * k if k < 3 else 450 + 92 * (k - 3)
        slides(t, 2, dx=tx - ox_, dy=180, dl=100 * k)
    f.text(330, 590, "5√{2}", z=48, c="gold", at=2, dl=1300, b=800)
    U.ex("m3-1-05", "√{18} + √{8}을 계산해 보자.", "가장 간단한 근호로 고친 뒤 — 근호 안이 같으면 계수끼리",
         [L("√{18} = √{9 × 2} = 3√{2}", memo="√{2}가 3개"),
          L("√{8} = √{4 × 2} = 2√{2}", memo="√{2}가 2개"),
          L("3√{2} + 2√{2} = 5√{2}", memo="√{2}를 x처럼 — 동류항")],
         "5√{2}", f.out(), at=("b3", 1))

    # ── 06 정수 부분과 소수 부분 ───────────────────────────────
    f = Fig()
    nl = NL(f, 0, 4, y=330, x0=60, x1=600, step=0.5, lab_step=1, z=24)
    s7 = math.sqrt(7)
    f.dot(nl.X(s7), 330, r=11, f="coral", at=0, dl=300)
    f.text(nl.X(s7), 290, "√{7}", z=28, c="coral", at=0, dl=400, b=800)
    f.text(nl.X(2), 410, "√{4}", z=22, c="soft", at=0, dl=700, b=700)
    f.text(nl.X(3), 410, "√{9}", z=22, c="soft", at=0, dl=800, b=700)
    f.line(nl.X(0), 250, nl.X(2), 250, at=1, c="teal", w=8, dr=True)
    f.text(nl.X(1), 225, "정수 부분 2", z=26, c="teal", at=1, dl=500, b=800)
    f.line(nl.X(2), 250, nl.X(s7), 250, at=2, c="coral", w=8, dr=True)
    f.line(nl.X(2), 372, 100, 520, at=2, c="soft", w=2, d=True, dl=300)
    f.line(nl.X(3), 372, 580, 520, at=2, c="soft", w=2, d=True, dl=300)
    f.line(100, 540, 580, 540, at=2, c="ink", w=3, dl=500)
    f.text(100, 580, "2", z=26, at=2, dl=500, b=800)
    f.text(580, 580, "3", z=26, at=2, dl=500, b=800)
    zx = 100 + 480 * (s7 - 2)
    f.line(100, 520, zx, 520, at=2, c="coral", w=8, dr=True, dl=800)
    f.dot(zx, 540, r=10, f="coral", at=2, dl=1300)
    f.text((100 + zx) / 2, 495, "√{7} − 2", z=28, c="coral", at=2, dl=1300, b=800)
    f.text(zx, 625, "0.64…", z=24, c="coral", at=2, dl=1500, b=800)
    U.ex("m3-1-06", "√{7}의 정수 부분과 소수 부분을 구해 보자.", "√{7}을 두 정수 사이에 끼우면 — 정수 부분 n, 소수 부분 √{7} − n",
         [L("4 < 7 < 9 → 2 < √{7} < 3", memo="제곱수 사이에 끼우기"),
          L("정수 부분 = 2", memo="√{7} = 2.64…"),
          L("소수 부분 = √{7} − 2", memo="전체에서 정수 부분을 뺀다")],
         "정수 부분 2, 소수 부분 √{7} − 2", f.out(), at=("b3", 2))

    # ── 07 다항식의 곱셈 — 넓이 네 칸 ─────────────────────────
    f = Fig()
    f.text(CX, 100, "(x + 2)(x + 3)", z=44, at="q", b=700)
    X0, Y0, ux, u3, u2 = 120, 170, 220, 135, 90
    f.rect(X0, Y0, ux + u3, ux + u2, at="q", c="ink", sw=3)
    f.line(X0 + ux, Y0, X0 + ux, Y0 + ux + u2, at="q", c="ink", w=2, d=True)
    f.line(X0, Y0 + ux, X0 + ux + u3, Y0 + ux, at="q", c="ink", w=2, d=True)
    f.text(X0 + ux / 2, Y0 - 12, "x", z=30, at="q", b=700)
    f.text(X0 + ux + u3 / 2, Y0 - 12, "3", z=30, at="q", b=700)
    f.text(X0 - 22, Y0 + ux / 2 + 10, "x", z=30, at="q", b=700, a="e")
    f.text(X0 - 22, Y0 + ux + u2 / 2 + 10, "2", z=30, at="q", b=700, a="e")
    cell(f, X0, Y0, ux, ux, "teal", 0, "x^{2}", z=40)
    cell(f, X0 + ux, Y0, u3, ux, "gold", 0, "3x", z=34, dl=500)
    cell(f, X0, Y0 + ux, ux, u2, "sky", 0, "2x", z=34, dl=1000)
    cell(f, X0 + ux, Y0 + ux, u3, u2, "coral", 0, "6", z=34, dl=1500)
    f.text(580, 300, "3x + 2x", z=28, c="gold", at=1, b=800)
    f.text(580, 345, "= 5x", z=28, c="gold", at=1, dl=300, b=800)
    f.text(CX, 580, "x^{2} + 5x + 6", z=44, c="ink", at=1, dl=700, b=800)
    U.ex("m3-1-07", "(x + 2)(x + 3)을 전개해 보자.", "앞 괄호의 각 항 × 뒤 괄호의 각 항 — 네 번 곱하고 동류항 정리",
         [L("(x + 2)(x + 3) = x^{2} + 3x + 2x + 6", memo="네 칸의 넓이"),
          L("x^{2} + 3x + 2x + 6 = x^{2} + 5x + 6", memo="가운데 두 칸은 동류항")],
         "x^{2} + 5x + 6", f.out(), at=("b3", 1), ident=True)

    # ── 08 곱셈 공식 (a + b)^2 ────────────────────────────────
    f = Fig()
    X0, Y0, a, b = 90, 110, 240, 120
    f.text(X0 + a / 2, Y0 - 14, "a", z=32, at="q", b=700)
    f.text(X0 + a + b / 2, Y0 - 14, "b", z=32, at="q", b=700)
    f.text(X0 - 20, Y0 + a / 2 + 10, "a", z=32, at="q", b=700, a="e")
    f.text(X0 - 20, Y0 + a + b / 2 + 10, "b", z=32, at="q", b=700, a="e")
    f.rect(X0, Y0, a + b, a + b, at="q", c="ink", sw=3)
    cell(f, X0, Y0, a, a, "teal", 0, "a^{2}", z=40)
    cell(f, X0 + a, Y0, b, a, "gold", 0, "ab", z=34, dl=500)
    cell(f, X0, Y0 + a, a, b, "gold", 0, "ab", z=34, dl=1000)
    cell(f, X0 + a, Y0 + a, b, b, "coral", 0, "b^{2}", z=34, dl=1500)
    cp = f.rect(X0, Y0 + a, a, b, at=1, c="ink", sw=2.5, f="gold", fo=0.55)
    mvr(cp, 1, (X0 + a + b + 20 + b / 2) - (X0 + a / 2), (Y0 + a / 2) - (Y0 + a + b / 2), 90, dl=200)
    f.text(X0 + a + b + 20 + b / 2, Y0 + a / 2 + 12, "ab", z=34, c="gold", at=1, dl=1300, b=800)
    f.text(X0 + a + b + 10, Y0 - 50, "똑같은 직사각형 2개 → 2ab", z=24, c="gold", at=1, dl=1500, b=800)
    f.text(CX, 600, "a^{2} + 2ab + b^{2}", z=44, at=1, dl=1900, b=800)
    U.ex("m3-1-08", "넓이로 (a + b)^{2} = a^{2} + 2ab + b^{2}을 확인해 보자.", "한 변이 a + b인 정사각형을 네 조각으로 나눈다",
         [L("(a + b)^{2} = a^{2} + ab + ab + b^{2}", memo="네 조각의 넓이"),
          L("a^{2} + ab + ab + b^{2} = a^{2} + 2ab + b^{2}", memo="같은 직사각형이 두 개")],
         "(a + b)^{2} = a^{2} + 2ab + b^{2}", f.out(), at=("b2", 2), ident=True)

    # ── 09 곱셈 공식으로 수 계산 — 98 × 102 ────────────────────
    f = Fig()
    X0, Y0, A_, B_ = 80, 130, 300, 75
    W, H = A_ + B_, A_ - B_
    f.rect(X0, Y0, W, H, at="q", c="ink", sw=3, f="teal", fo=0.25)
    f.text(X0 + W / 2, Y0 - 16, "102 = 100 + 2", z=26, at="q", b=800)
    f.text(X0 - 14, Y0 + H / 2 + 8, "98", z=26, at="q", b=800, a="e")
    f.line(X0 + A_, Y0, X0 + A_, Y0 + H, at=0, c="coral", w=3, d=True, dr=True)
    st = f.rect(X0 + A_, Y0, B_, H, at=1, c="ink", sw=2.5, f="coral", fo=0.45)
    mvr(st, 1, (X0 + H / 2) - (X0 + A_ + B_ / 2), (Y0 + H + B_ / 2) - (Y0 + H / 2), -90, dl=200)
    f.rect(X0, Y0, A_, A_, at=1, c="gold", sw=3, d=True, dl=1300)
    f.rect(X0 + H, Y0 + H, B_, B_, at=1, c="red", sw=3, d=True, f="red", fo=0.12, dl=1500)
    f.text(X0 + H + B_ / 2, Y0 + H + B_ / 2 + 10, "2^{2}", z=26, c="red", at=1, dl=1700, b=800)
    f.text(X0 + A_ + 26, Y0 + A_ / 2 + 10, "100", z=26, c="gold", at=1, dl=1600, b=800, a="s")
    f.text(CX, 560, "100^{2} − 2^{2}", z=40, c="gold", at=1, dl=1900, b=800)
    f.text(CX, 640, "= 9996", z=40, c="gold", at=2, b=800)
    U.ex("m3-1-09", "98 × 102를 곱셈 공식으로 계산해 보자.", "100을 기준으로 — (합) × (차) = (제곱의 차)",
         [L("98 × 102 = (100 − 2)(100 + 2)"),
          L("(100 − 2)(100 + 2) = 100^{2} − 2^{2}", memo="튀어나온 띠를 옮기면 큰 정사각형에서 작은 정사각형이 빠진 꼴"),
          L("100^{2} − 2^{2} = 10000 − 4 = 9996")],
         "9996", f.out(), at=("b2", 3))

    # ── 10 곱셈 공식의 변형 ─────────────────────────────────────
    f = Fig()
    X0, Y0, a, b = 90, 120, 230, 130
    f.rect(X0, Y0, a + b, a + b, at="q", c="ink", sw=3)
    f.text(X0 + (a + b) / 2, Y0 - 16, "a + b = 5", z=26, at="q", b=800)
    cell(f, X0, Y0, a, a, "teal", "q", "a^{2}", z=36)
    cell(f, X0 + a, Y0 + a, b, b, "teal", "q", "b^{2}", z=30)
    r1 = cell(f, X0 + a, Y0, b, a, "coral", "q", None)
    r2 = cell(f, X0, Y0 + a, a, b, "coral", "q", None)
    t1 = f.text(X0 + a + b / 2, Y0 + a / 2 + 10, "ab", z=30, c="coral", at="q", b=800, un=1)
    t2 = f.text(X0 + a / 2, Y0 + a + b / 2 + 10, "ab", z=30, c="coral", at="q", b=800, un=1)
    f.text(X0 + (a + b) / 2, Y0 + a + b + 40, "(a + b)^{2} = 25", z=30, c="ink", at=0, b=800)
    slide(r1, 1, dx=575 - (X0 + a + b / 2), dl=200)
    mvr(r2, 1, 575 - (X0 + a / 2), 470 - (Y0 + a + b / 2), 90, dl=500)
    f.text(575, 245, "ab", z=28, c="coral", at=1, dl=1200, b=800)
    f.text(575, 480, "ab", z=28, c="coral", at=1, dl=1400, b=800)
    f.text(575, 640, "2ab = 6", z=30, c="coral", at=1, dl=1600, b=800)
    f.text(220, 640, "25 − 6 = 19", z=36, c="gold", at=2, b=800)
    a_, b_ = (5 + sp.sqrt(13)) / 2, (5 - sp.sqrt(13)) / 2
    U.ex("m3-1-10", "a + b = 5, ab = 3일 때 a^{2} + b^{2}의 값을 구해 보자.", "(a + b)^{2}에서 2ab를 덜어 낸다",
         [L("(a + b)^{2} = 5^{2} = 25", memo="큰 정사각형 전체"),
          L("a^{2} + b^{2} = (a + b)^{2} − 2ab", memo="직사각형 ab 두 개를 뺀다"),
          L("a^{2} + b^{2} = 25 − 2 × 3 = 19")],
         "19", f.out(), at=("b2", 2), sub={"a": a_, "b": b_})

    # ── 11 인수분해 — 타일을 직사각형으로 ─────────────────────
    f = Fig()
    X, Uu = 150, 40
    x2 = cell(f, 40, 80, X, X, "teal", "q", None)
    f.text(115, 165, "x^{2}", z=34, c="teal", at="q", b=800, un=1)
    xt = []
    for k in range(5):
        xt.append(cell(f, 220, 80 + 45 * k, X, Uu, "gold", "q", None))
    f.text(295, 64, "x × 5", z=22, c="gold", at="q", b=800, un=1)
    ut = []
    for k in range(6):
        i, j = k % 3, k // 3
        ut.append(cell(f, 400 + 45 * i, 80 + 45 * j, Uu, Uu, "coral", "q", None))
    f.text(468, 64, "1 × 6", z=22, c="coral", at="q", b=800, un=1)
    f.text(530, 240, "2 × 3 = 6", z=26, c="ink", at=0, b=800)
    f.text(530, 284, "2 + 3 = 5", z=26, c="ink", at=0, dl=400, b=800)
    TX, TY = 120, 360
    slide(x2, 1, dx=TX - 40, dy=TY - 80, dl=100)
    for k in range(3):
        mvr(xt[k], 1, (TX + X + Uu / 2 + Uu * k) - (220 + X / 2), (TY + X / 2) - (80 + 45 * k + Uu / 2), 90, dl=300 + 150 * k)
    for k in (3, 4):
        slide(xt[k], 1, dx=TX - 220, dy=(TY + X + Uu * (k - 3)) - (80 + 45 * k), dl=300 + 150 * k)
    for k in range(6):
        i, j = k % 3, k // 3
        slide(ut[k], 1, dx=(TX + X + Uu * i) - (400 + 45 * i), dy=(TY + X + Uu * j) - (80 + 45 * j), dl=900 + 80 * k)
    f.text(TX + X / 2, TY - 14, "x", z=28, at=1, dl=1500, b=800)
    f.text(TX + X + 1.5 * Uu, TY - 14, "3", z=28, at=1, dl=1500, b=800)
    f.text(TX - 16, TY + X / 2 + 10, "x", z=28, at=1, dl=1600, b=800, a="e")
    f.text(TX - 16, TY + X + Uu + 10, "2", z=28, at=1, dl=1600, b=800, a="e")
    f.text(520, 470, "(x + 2)(x + 3)", z=32, c="gold", at=1, dl=1900, b=800)
    U.ex("m3-1-11", "x^{2} + 5x + 6을 인수분해해 보자.", "곱이 6, 합이 5인 두 수 — 타일을 빈틈없는 직사각형으로 모은다",
         [L("곱이 6, 합이 5 → 2와 3", memo="상수항 6 = 2 × 3, x의 계수 5 = 2 + 3"),
          L("x^{2} + 5x + 6 = (x + 2)(x + 3)", memo="세로 x + 2, 가로 x + 3인 직사각형")],
         "(x + 2)(x + 3)", f.out(), at=("b1", 2), ident=True)

    # ── 12 복잡한 식의 인수분해 — 치환 ─────────────────────────
    f = Fig()
    S = Strip(f, y=130, z=40)
    xq, _ = S.row("q", [{"s": "(x + y)^{2}", "c": "teal"}, "+", "3", {"s": "(x + y)", "c": "teal", "g": 0.02}, "+", "2"], keep=True)
    f.rect(xq[0] - 82, 86, 150, 62, at=0, c="teal", sw=3, rx=10, d=True)
    f.rect(xq[3] - 66, 86, 132, 62, at=0, c="teal", sw=3, rx=10, d=True, dl=200)
    f.text(110, 215, "x + y = A", z=26, c="teal", at=0, dl=500, b=800)
    S.row(0, [{"s": "A^{2}", "frm": 0, "c": "teal"}, {"s": "+", "frm": 1}, {"s": "3", "frm": 2}, {"s": "A", "frm": 3, "c": "teal", "g": 0.02}, {"s": "+", "frm": 4}, {"s": "2", "frm": 5}], y=280, keep=True, z=48, dl0=700)
    S.row(1, [{"s": "(A + 1)", "frm": [0, 1, 2], "c": "gold"}, {"s": "(A + 2)", "frm": [3, 4, 5], "c": "gold", "g": 0.02}], y=420, keep=True, z=48)
    S.row(2, [{"s": "(x + y + 1)", "frm": 0, "c": "coral"}, {"s": "(x + y + 2)", "frm": 1, "c": "coral", "g": 0.02}], y=570, keep=True, z=42)
    f.text(110, 500, "A → x + y", z=24, c="coral", at=2, dl=200, b=800)
    U.ex("m3-1-12", "(x + y)^{2} + 3(x + y) + 2를 인수분해해 보자.", "공통부분 x + y를 한 문자 A로 바꾸면 아는 꼴",
         [L("x + y를 A로 → A^{2} + 3A + 2", memo="복잡한 식이 단순해진다"),
          L("A^{2} + 3A + 2 = (A + 1)(A + 2)", memo="곱이 2, 합이 3"),
          L("(x + y + 1)(x + y + 2)", memo="A를 원래대로 되돌리기까지가 답")],
         "(x + y + 1)(x + y + 2)", f.out(), at=("b2", 2))

    # ── 13 인수분해로 수 계산 — 52^2 − 48^2 ───────────────────
    f = Fig()
    X0, Y0, A_, B_ = 80, 100, 300, 220
    f.rect(X0, Y0, A_, A_, at="q", c="ink", sw=3)
    f.text(X0 + A_ / 2, Y0 - 14, "52", z=26, at="q", b=800)
    f.rect(X0, Y0, B_, B_, at=0, c="soft", sw=3, d=True)
    f.text(X0 + B_ / 2, Y0 + B_ / 2 + 10, "48^{2}", z=32, c="soft", at=0, b=800)
    rs = f.rect(X0 + B_, Y0, A_ - B_, A_, at=0, c="ink", sw=2.5, f="coral", fo=0.4, dl=500)
    rb = f.rect(X0, Y0 + B_, B_, A_ - B_, at=0, c="ink", sw=2.5, f="coral", fo=0.4, dl=700)
    mvr(rb, 1, (X0 + B_ + (A_ - B_) / 2) - (X0 + B_ / 2), (Y0 + A_ + B_ / 2) - (Y0 + B_ + (A_ - B_) / 2), 90, dl=200)
    f.line(X0 + A_ + 30, Y0, X0 + A_ + 30, Y0 + A_ + B_, at=1, c="gold", w=3, ar=2, dl=1300)
    f.text(X0 + A_ + 44, Y0 + (A_ + B_) / 2, "52 + 48 = 100", z=26, c="gold", at=1, dl=1500, b=800, a="s")
    f.text(X0 + B_ + (A_ - B_) / 2, Y0 + A_ + B_ + 40, "4", z=28, c="gold", at=1, dl=1500, b=800)
    f.text(200, 600, "100 × 4 = 400", z=34, c="gold", at=1, dl=1900, b=800)
    U.ex("m3-1-13", "52^{2} − 48^{2}을 계산해 보자.", "제곱의 차 = (합) × (차)",
         [L("52^{2} − 48^{2} = (52 + 48)(52 − 48)", memo="ㄱ자 조각을 잘라 붙이면 직사각형"),
          L("(52 + 48)(52 − 48) = 100 × 4 = 400")],
         "400", f.out(), at=("b2", 1))

    # ── 14 인수분해로 이차방정식 ───────────────────────────────
    f = Fig()
    S = Strip(f, y=120, z=44)
    S.row("q", ["x^{2} − 5x + 6", "=", "0"], keep=True)
    S.row(0, [{"s": "(x − 2)", "frm": 0, "c": "teal"}, {"s": "(x − 3)", "frm": 0, "c": "coral", "g": 0.02}, {"s": "=", "frm": 1}, {"s": "0", "frm": 2}], y=240, keep=True, z=48)
    f.text(560, 190, "곱이 0", z=24, c="gold", at=0, dl=900, b=800)
    S.row(1, [{"s": "x − 2", "frm": 0, "c": "teal"}, {"s": "= 0", "frm": [2, 3]}, {"s": "또는", "c": "soft"}, {"s": "x − 3", "frm": 1, "c": "coral"}, {"s": "= 0", "frm": [2, 3]}], y=370, keep=True, z=40)
    S.row(2, [{"s": "x = 2", "frm": [0, 1], "c": "teal"}, {"s": "또는", "frm": 2, "c": "soft"}, {"s": "x = 3", "frm": [3, 4], "c": "coral"}], y=490, keep=True, z=46)
    nl = NL(f, 0, 5, y=610, x0=80, x1=580, step=1, lab_step=1, z=22, at=2)
    f.dot(nl.X(2), 610, r=11, f="teal", at=2, dl=900)
    f.dot(nl.X(3), 610, r=11, f="coral", at=2, dl=1100)
    U.ex("m3-1-14", "이차방정식 x^{2} − 5x + 6 = 0을 풀어 보자.", "인수분해해서 AB = 0이면 A = 0 또는 B = 0",
         [L("(x − 2)(x − 3) = 0", memo="곱이 6, 합이 −5"),
          L("x − 2 = 0 또는 x − 3 = 0", memo="곱이 0이면 적어도 하나는 0"),
          L("x = 2 또는 x = 3")],
         "x = 2 또는 x = 3", f.out(), at=("b3", 2))

    # ── 15 제곱근으로 이차방정식 ───────────────────────────────
    f = Fig()
    nl = NL(f, -2, 4, y=430, x0=50, x1=620, step=1, lab_step=1, z=24)
    s5 = math.sqrt(5)
    f.dot(nl.X(1), 430, r=12, f="gold", at="q")
    f.text(nl.X(1), 380, "x − 1 = 0인 곳", z=22, c="gold", at="q", b=800)
    f.rect(240, 120, 180, 76, at=0, c="teal", sw=3, rx=14, d=True)
    f.text(CX, 172, "x − 1", z=40, c="teal", at=0, b=800)
    f.text(CX, 260, "제곱해서 5", z=24, c="soft", at=0, dl=300, b=800)
    hop(nl, 1, 1 + s5, at=1, c="teal", label="+√{5}", dl=100, h=90)
    hop(nl, 1, 1 - s5, at=1, c="coral", label="−√{5}", dl=600, h=90)
    f.dot(nl.X(1 + s5), 430, r=11, f="teal", at=1, dl=900)
    f.dot(nl.X(1 - s5), 430, r=11, f="coral", at=1, dl=1300)
    f.text(nl.X(1 + s5), 520, "1 + √{5}", z=28, c="teal", at=1, dl=1200, b=800)
    f.text(nl.X(1 - s5), 520, "1 − √{5}", z=28, c="coral", at=1, dl=1500, b=800)
    U.ex("m3-1-15", "이차방정식 (x − 1)^{2} = 5를 풀어 보자.", "x − 1을 한 덩어리로 — 제곱해서 5가 되는 수는 ±√{5}",
         [L("x − 1 = ±√{5}", memo="x − 1은 5의 제곱근"),
          L("x = 1 ± √{5}", memo="1에서 양쪽으로 √{5}만큼")],
         "x = 1 ± √{5}", f.out(), at=("b3", 1))

    # ── 16 완전제곱식으로 — 정사각형 완성 ─────────────────────
    f = Fig()
    X0, Y0, X, T = 90, 120, 210, 70
    cell(f, X0, Y0, X, X, "teal", "q", "x^{2}", z=40)
    h1 = f.rect(X0 + X + 30, Y0, T, X, at="q", c="ink", sw=2.5, f="gold", fo=0.4)
    h2 = f.rect(X0 + X + 30 + T, Y0, T, X, at="q", c="ink", sw=2.5, f="gold", fo=0.4)
    f.text(X0 + X + 30 + T, Y0 + X / 2 + 12, "4x", z=34, c="gold", at="q", b=800, un=0)
    slide(h1, 0, dx=-30, dl=200)
    mvr(h2, 0, (X0 + X / 2) - (X0 + X + 30 + 1.5 * T), (Y0 + X + T / 2) - (Y0 + X / 2), 90, dl=500)
    f.text(X0 + X + T / 2, Y0 + X / 2 + 10, "2x", z=28, c="gold", at=0, dl=1400, b=800)
    f.text(X0 + X / 2, Y0 + X + T / 2 + 10, "2x", z=28, c="gold", at=0, dl=1500, b=800)
    cn = f.rect(X0 + X, Y0 + X, T, T, at=1, c="ink", sw=2.5, f="coral", fo=0.5)
    fly(cn, 170, 60, dl=60, ms=800)
    f.text(X0 + X + T / 2, Y0 + X + T / 2 + 10, "4", z=30, c="coral", at=1, dl=900, b=800)
    f.text(560, 400, "+ 4", z=34, c="coral", at=1, dl=200, b=800)
    f.rect(X0 - 6, Y0 - 6, X + T + 12, X + T + 12, at=2, c="gold", sw=4, rx=6, d=True)
    f.text(X0 + (X + T) / 2, Y0 - 22, "x + 2", z=28, c="gold", at=2, dl=300, b=800)
    f.text(X0 - 20, Y0 + (X + T) / 2 + 10, "x + 2", z=28, c="gold", at=2, dl=400, b=800, a="e")
    f.text(CX, 520, "(x + 2)^{2} = 3", z=38, c="gold", at=2, dl=700, b=800)
    f.text(CX, 620, "x + 2 = ±√{3}", z=34, c="ink", at=3, b=800)
    s3 = sp.sqrt(3)
    U.ex("m3-1-16", "x^{2} + 4x + 1 = 0을 완전제곱식을 이용해 풀어 보자.", "x의 계수의 절반의 제곱(4)을 더해 정사각형을 완성한다",
         [L("x^{2} + 4x = −1", memo="상수항을 우변으로 — 4x를 2x 두 개로 나눠 붙인다"),
          L("x^{2} + 4x + 4 = −1 + 4", memo="빈 귀퉁이 2 × 2 = 4를 양변에"),
          L("(x + 2)^{2} = 3"),
          L("x = −2 ± √{3}", memo="x + 2 = ±√{3}")],
         "x = −2 ± √{3}", f.out(), at=("b3", 2), sub={"x": -2 + s3})

    # ── 17 근의 공식 ─────────────────────────────────────────
    f = Fig()
    S = Strip(f, y=120, z=42)
    xe, _ = S.row("q", ["x^{2}", "+", "3x", "+", "1", "=", "0"], keep=True)
    chips = {}
    for key, x, s, col in (("a", xe[0], "a = 1", "teal"), ("b", xe[2], "b = 3", "coral"), ("c", xe[4], "c = 1", "gold")):
        chips[key] = (x, 56)
        f.text(x, 56, s, z=24, c=col, at=0, dl={"a": 0, "b": 300, "c": 600}[key], b=800)
    f.text(110, 345, "x =", z=42, at="q", b=700)
    f.line(160, 330, 560, 330, at="q", c="ink", w=3, un=2)
    f.text(220, 300, "−b ±", z=40, at="q", b=700, un=1)
    rad(f, 300, 470, 300, 40, "q", un=1)
    f.text(385, 300, "b^{2} − 4ac", z=40, at="q", b=700, un=1)
    f.text(360, 395, "2a", z=40, at="q", b=700, un=1)
    e = f.text(220, 300, "−3 ±", z=40, c="coral", at=1, dl=200, b=800)
    fly(e, chips["b"][0] - 220, 56 - 300, dl=40, ms=800)
    rad(f, 300, 545, 300, 40, 1, dl=300, un=2)
    e = f.text(422, 300, "3^{2} − 4 × 1 × 1", z=34, c="coral", at=1, dl=500, b=800, un=2)
    fly(e, chips["c"][0] - 422, 56 - 300, dl=40, ms=800)
    e = f.text(360, 395, "2 × 1", z=38, c="teal", at=1, dl=700, b=800, un=2)
    fly(e, chips["a"][0] - 360, 56 - 395, dl=40, ms=800)
    f.line(160, 330, 360, 330, at=2, c="ink", w=3)
    rad(f, 300, 330, 300, 40, 2, dl=200)
    f.text(315, 300, "5", z=40, c="gold", at=2, dl=300, b=800)
    f.text(262, 395, "2", z=40, c="gold", at=2, dl=400, b=800)
    f.text(CX, 560, "x = {−3 ± √{5}/2}", z=44, c="gold", at=2, dl=900, b=800)
    U.ex("m3-1-17", "근의 공식으로 x^{2} + 3x + 1 = 0을 풀어 보자.", "a, b, c를 부호까지 읽어 근의 공식에 넣는다",
         [L("a = 1, b = 3, c = 1", memo="계수를 부호까지 읽기"),
          L("x = {−3 ± √{9 − 4}/2}", memo="b^{2} − 4ac = 9 − 4"),
          L("x = {−3 ± √{5}/2}")],
         "x = {−3 ± √{5}/2}", f.out(), at=("b3", 1))

    # ── 18 소수 계수 이차방정식 ────────────────────────────────
    f = Fig()
    S = Strip(f, y=120, z=40)
    S.row("q", ["0.2x^{2}", "−", "0.5x", "−", "0.3", "=", "0"], keep=True)
    S.row(0, [{"s": "2x^{2}", "frm": 0, "c": "coral"}, {"s": "−", "frm": 1}, {"s": "5x", "frm": 2, "c": "coral"}, {"s": "−", "frm": 3}, {"s": "3", "frm": 4, "c": "coral"}, {"s": "=", "frm": 5}, {"s": "0", "frm": 6}], y=230, keep=True, z=44)
    f.text(70, 180, "× 10", z=28, c="gold", at=0, dl=200, b=800)
    S.row(1, [{"s": "(2x + 1)", "frm": [0, 1, 2], "c": "teal"}, {"s": "(x − 3)", "frm": [2, 3, 4], "c": "sky", "g": 0.02}, {"s": "=", "frm": 5}, {"s": "0", "frm": 6}], y=345, keep=True, z=44)
    S.row(2, [{"s": "x = −{1/2}", "frm": 0, "c": "teal"}, {"s": "또는", "c": "soft"}, {"s": "x = 3", "frm": 1, "c": "sky"}], y=470, keep=True, z=44)
    cx0, cy0 = 200, 560
    for (s, x, y, col) in (("2x", cx0, cy0, "teal"), ("1", cx0 + 120, cy0, "teal"), ("x", cx0, cy0 + 70, "sky"), ("−3", cx0 + 120, cy0 + 70, "sky")):
        f.text(x, y, s, z=30, c=col, at=1, dl=700, b=800)
    f.line(cx0 + 22, cy0 - 8, cx0 + 98, cy0 + 50, at=1, c="gold", w=3, dr=True, dl=1000)
    f.line(cx0 + 22, cy0 + 50, cx0 + 98, cy0 - 8, at=1, c="gold", w=3, dr=True, dl=1200)
    f.text(470, cy0 + 40, "−6x + x = −5x", z=26, c="gold", at=1, dl=1500, b=800)
    U.ex("m3-1-18", "0.2x^{2} − 0.5x − 0.3 = 0을 풀어 보자.", "양변에 10을 곱해 정수 계수로 — 그다음 인수분해",
         [L("2x^{2} − 5x − 3 = 0", memo="양변에 10을 곱한다"),
          L("(2x + 1)(x − 3) = 0", memo="십자 곱: −6x + x = −5x"),
          L("x = −{1/2} 또는 x = 3")],
         "x = −{1/2} 또는 x = 3", f.out(), at=("b3", 1), sub={"x": 3})

    # ── 19 근의 판별 — 포물선을 올려 x축에 닿게 ─────────────────
    f = Fig()
    P = Plane(f, (-7, 1), (-5, 9), box=(60, 50, 620, 650), square=False)
    P.axes(at="q", grid=1, lab_step=2)
    P.curve(lambda x: x * x + 6 * x + 5, at="q", c="soft", w=3.5, d=True)
    P.pt(-5, 0, at="q", f="soft", r=8)
    P.pt(-1, 0, at="q", f="soft", r=8)
    f.text(P.X(-6.9), P.Y(-2.2), "k = 5: 두 점에서 만난다", z=22, c="soft", at="q", b=800, a="s")
    cv = P.curve(lambda x: x * x + 6 * x + 5, x0=-5.8, x1=-0.2, at=1, c="gold", w=5, dr=False)
    slides(cv, 1, dy=P.Y(4) - P.Y(0), dl=300)
    P.pt(-3, 0, at=2, f="gold", r=12)
    f.text(P.X(-6.9), P.Y(-3.2), "k = 9: 한 점 — 중근 x = −3", z=22, c="gold", at=2, b=800, a="s")
    P.curve(lambda x: x * x + 6 * x + 12, at=2, c="lilac", w=3, d=True, dr=True)
    f.text(P.X(-6.9), P.Y(-4.2), "k > 9: 만나지 않는다", z=22, c="lilac", at=2, dl=600, b=800, a="s")
    U.ex("m3-1-19", "이차방정식 x^{2} + 6x + k = 0이 중근을 갖도록 하는 k의 값을 구해 보자.", "중근 ⇔ b^{2} − 4ac = 0 — 그래프가 x축에 딱 한 점에서 닿는다",
         [L("b^{2} − 4ac = 6^{2} − 4 × 1 × k", memo="a = 1, b = 6, c = k"),
          L("36 − 4k = 0", memo="중근이 되려면"),
          L("k = 9", memo="x^{2} + 6x + 9 = (x + 3)^{2}")],
         "9", f.out(), at=("b4", 1), sub={"k": 9})

    # ── 20 두 근으로 이차방정식 만들기 ─────────────────────────
    f = Fig()
    nl = NL(f, -5, 4, y=540, x0=50, x1=620, step=1, lab_step=1, z=22)
    f.dot(nl.X(2), 540, r=12, f="teal", at="q")
    f.dot(nl.X(-3), 540, r=12, f="coral", at="q")
    f.text(nl.X(2), 495, "근 2", z=24, c="teal", at="q", b=800)
    f.text(nl.X(-3), 495, "근 −3", z=24, c="coral", at="q", b=800)
    for (s, x, src, col, dl) in (("(x − 2)", 250, 2, "teal", 0), ("(x + 3)", 400, -3, "coral", 400)):
        e = f.text(x, 250, s, z=46, c=col, at=0, dl=dl, b=800)
        fly(e, nl.X(src) - x, 540 - 250, dl=60, ms=900)
    f.text(510, 250, "= 0", z=46, at=0, dl=1100, b=700)
    f.text(400, 315, "x − (−3)", z=22, c="coral", at=0, dl=1400, b=800)
    e = f.text(CX, 400, "x^{2} + x − 6 = 0", z=46, c="gold", at=1, b=800)
    fly(e, 0, -150, dl=60, ms=700)
    U.ex("m3-1-20", "두 근이 2, −3이고 x^{2}의 계수가 1인 이차방정식을 구해 보자.", "근 α, β → (x − α)(x − β) = 0",
         [L("(x − 2)(x + 3) = 0", memo="근 2 → x − 2, 근 −3 → x + 3"),
          L("x^{2} + x − 6 = 0", memo="전개")],
         "x^{2} + x − 6 = 0", f.out(), at=("b3", 1), sub={"x": 2})

    # ── 21 이차방정식의 활용 — 연속한 두 자연수 ─────────────────
    f = Fig()
    gx, gy, gp = 160, 170, 50
    for r_ in range(7):
        for c_ in range(8):
            f.dot(gx + c_ * gp, gy + r_ * gp, r=12, f="teal", at=0, dl=1 + 160 * r_ + 15 * c_)
    f.text(gx + 3.5 * gp, gy - 40, "x + 1", z=28, at="q", b=800, un=2)
    f.text(gx - 30, gy + 3 * gp + 10, "x", z=28, at="q", b=800, a="e", un=2)
    f.text(560, 330, "56개", z=30, c="teal", at=0, dl=1300, b=800)
    f.text(gx + 3.5 * gp, gy - 40, "8", z=32, c="gold", at=2, dl=900, b=800)
    f.text(gx - 30, gy + 3 * gp + 10, "7", z=32, c="gold", at=2, dl=800, b=800, a="e")
    f.text(200, 580, "x = −8", z=32, c="coral", at=2, b=800)
    f.cross(200, 568, s=60, at=2, c="red", dl=400)
    f.text(440, 580, "x = 7", z=32, c="teal", at=2, dl=200, b=800)
    f.text(200, 640, "자연수가 아니다", z=22, c="red", at=2, dl=600, b=800)
    U.ex("m3-1-21", "연속한 두 자연수의 곱이 56일 때 두 수를 구해 보자.", "작은 수를 x로 — 큰 수는 x + 1, 마지막에 자연수 조건 확인",
         [L("x(x + 1) = 56", memo="세로 x, 가로 x + 1 — 점 56개"),
          L("x^{2} + x − 56 = 0 → (x + 8)(x − 7) = 0"),
          L("x = −8 또는 x = 7", memo="자연수이므로 x = 7")],
         "7과 8", f.out(), at=("b4", 1), sub={"x": 7})

    # ── 22 이차함수의 함숫값 ───────────────────────────────────
    f = Fig()
    P = Plane(f, (-2, 4), (-1, 8), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: x * x - 2 * x + 3, at="q", c="soft", w=3, d=True)
    travel(P, 2, 3, at=0, c="teal", label="(2, 3)", pos="e")
    travel(P, -1, 6, at=1, c="coral", label="(−1, 6)", pos="w")
    U.ex("m3-1-22", "f(x) = x^{2} − 2x + 3일 때 f(2)와 f(−1)을 구해 보자.", "x 자리에 통째로 대입 — 음수는 괄호부터",
         [L("f(2) = 2^{2} − 2 × 2 + 3 = 3", memo="그래프 위의 점 (2, 3)"),
          L("f(−1) = (−1)^{2} − 2 × (−1) + 3 = 6", memo="그래프 위의 점 (−1, 6)")],
         "f(2) = 3, f(−1) = 6", f.out(), at=("b4", 1))

    # ── 23 y = ax^2 — 지나는 점으로 a 찾기 ─────────────────────
    f = Fig()
    P = Plane(f, (-3, 3), (-1, 13), box=(80, 50, 600, 650), square=False)
    P.axes(at="q", grid=None, lab_step=1, ystep=2)
    P.pt(2, 12, at="q", f="gold", r=12, label="(2, 12)", pos="e", z=26, c="gold")
    for k, (a_, col) in enumerate(((1, "soft"), (2, "sky"), (3, "coral"))):
        cvs = P.curve(lambda x, a_=a_: a_ * x * x, at=0, c=col, w=4.5 if a_ == 3 else 3)
        for el in cvs:
            el["dl"] = 1 + 900 * k
        f.text(P.X(2) + 20, P.Y(4 * a_) + 8, f"a = {a_}", z=22, c=col, at=0, dl=700 + 900 * k, b=800, a="s")
    U.ex("m3-1-23", "y = ax^{2}의 그래프가 점 (2, 12)를 지날 때 a의 값을 구해 보자.", "점 (m, n)이 그래프 위에 있다 ⇔ n = am^{2}",
         [L("12 = a × 2^{2}", memo="x = 2, y = 12를 대입"),
          L("a = 3", memo="|a|가 클수록 폭이 좁다")],
         "3", f.out(), at=("b4", 1), sub={"a": 3})

    # ── 24 y = ax^2 + q — 위아래 평행이동 ──────────────────────
    f = Fig()
    P = Plane(f, (-3, 3), (-4, 6), box=(80, 50, 600, 650))
    P.axes(at="q", grid=1, lab_step=1)
    rr = math.sqrt(3)
    parabola(P, 2, 0, 0, at=0, c="teal", x0=-rr, x1=rr)
    f.text(P.X(1.9), P.Y(5.4), "y = 2x^{2}", z=24, c="teal", at=0, dl=900, b=800, a="s")
    cv = parabola(P, 2, 0, 0, at=1, c="coral", x0=-rr, x1=rr, dr=False)
    slides(cv, 1, dy=P.Y(-3) - P.Y(0), dl=300)
    f.line(*P.P(0.35, 0), *P.P(0.35, -3), at=1, c="gold", w=3.5, ar=1, dr=True, dl=300)
    f.text(P.X(0.5), P.Y(-1.5), "−3", z=26, c="gold", at=1, dl=900, b=800, a="s")
    P.pt(0, -3, at=2, f="coral", r=11, label="(0, −3)", pos="w", z=26, c="coral")
    f.text(P.X(1.9), P.Y(2.6), "y = 2x^{2} − 3", z=24, c="coral", at=2, dl=300, b=800, a="s")
    U.ex("m3-1-24", "y = 2x^{2}의 그래프를 이용해 y = 2x^{2} − 3의 그래프를 그려 보자.", "+q는 y축 방향으로 q만큼 평행이동 — 모양은 그대로",
         [L("y = 2x^{2}", memo="꼭짓점 (0, 0)"),
          L("y축 방향으로 −3만큼 → y = 2x^{2} − 3", memo="통째로 아래로 3"),
          L("꼭짓점 (0, −3), 축 x = 0")],
         "꼭짓점 (0, −3)", f.out(), at=("b3", 1))

    # ── 25 y = a(x − p)^2 — 좌우 평행이동 ──────────────────────
    f = Fig()
    P = Plane(f, (-6, 6), (-1, 7), box=(40, 60, 620, 640), square=False)
    P.axes(at="q", grid=1, lab_step=1)
    rr = 2.55
    parabola(P, 1, 0, 0, at="q", c="soft", x0=-rr, x1=rr, d=True)
    for k, (p, col) in enumerate(((3, "teal"), (-3, "coral"))):
        cv = parabola(P, 1, 0, 0, at=k, c=col, x0=-rr, x1=rr, dr=False)
        slides(cv, k, dx=P.X(p) - P.X(0), dl=300)
        f.line(*P.P(0, -0.5), *P.P(p, -0.5), at=k, c=col, w=3.5, ar=1, dr=True, dl=300)
        f.text(P.X(p), P.Y(6.6), f"y = (x {'−' if p > 0 else '+'} 3)^{{2}}", z=24, c=col, at=k, dl=1000, b=800)
    for p, col in ((3, "teal"), (-3, "coral")):
        f.line(*P.P(p, -1), *P.P(p, 7), at=2, c=col, w=2.5, d=True)
        P.pt(p, 0, at=2, f=col, r=10, dl=300)
    U.ex("m3-1-25", "y = x^{2}의 그래프를 평행이동해 y = (x − 3)^{2}과 y = (x + 3)^{2}의 그래프를 그려 보자.", "(x − p)^{2} → x축 방향으로 p만큼 — 괄호 안 부호와 반대 방향",
         [L("y = (x − 3)^{2} → p = 3", memo="오른쪽으로 3"),
          L("y = (x + 3)^{2} = (x − (−3))^{2} → p = −3", memo="왼쪽으로 3"),
          L("꼭짓점 (3, 0), (−3, 0)", memo="축은 직선 x = 3, x = −3")],
         "오른쪽으로 3, 왼쪽으로 3", f.out(), at=("b3", 1))

    # ── 26 y = a(x − p)^2 + q — 네 단계 ─────────────────────────
    f = Fig()
    P = Plane(f, (-1, 5), (-2, 6), box=(60, 60, 620, 640))
    P.axes(at="q", grid=1, lab_step=1)
    rr = 2.6
    parabola(P, 1, 0, 0, at="q", c="soft", x0=-1, x1=rr, d=True)
    cv = parabola(P, 1, 0, 0, at=0, c="sky", x0=-rr, x1=rr, dr=False)
    slides(cv, 0, dx=P.X(2) - P.X(0), dy=P.Y(-1) - P.Y(0), dl=300)
    P.pt(2, -1, at=0, f="gold", r=12, label="(2, −1)", pos="e", z=26, c="gold", dl=1200)
    f.line(*P.P(2, -2), *P.P(2, 6), at=1, c="gold", w=3, d=True, dr=True)
    f.text(P.X(2) + 12, P.Y(5.5), "x = 2", z=24, c="gold", at=1, dl=500, b=800, a="s")
    f.text(P.X(3.9), P.Y(1.2), "아래로 볼록", z=24, c="sky", at=2, b=800)
    P.pt(0, 3, at=3, f="teal", r=11, label="(0, 3)", pos="e", z=26, c="teal")
    P.pt(4, 3, at=3, f="teal", r=9, dl=400)
    f.line(*P.P(0, 3), *P.P(4, 3), at=3, c="teal", w=2, d=True, dl=300)
    U.ex("m3-1-26", "y = (x − 2)^{2} − 1의 그래프를 그려 보자.", "꼭짓점 → 축 → 볼록 방향 → y절편",
         [L("꼭짓점 (2, −1)", memo="p = 2, q = −1 — y = x^{2}을 옮긴다"),
          L("축 x = 2"),
          L("a = 1 > 0 → 아래로 볼록"),
          L("x = 0 → y = (0 − 2)^{2} − 1 = 3", memo="y절편 3 — 축에 대칭인 점 (4, 3)도")],
         "꼭짓점 (2, −1), y절편 3", f.out(), at=("b3", 1))

    # ── 27 y = ax^2 + bx + c → 표준형 ──────────────────────────
    f = Fig()
    S = Strip(f, y=105, z=38)
    S.row("q", ["x^{2}", "−", "4x", "+", "1"], keep=True)
    S.row(0, ["(", {"s": "x^{2}", "frm": 0, "g": 0.02}, {"s": "−", "frm": 1}, {"s": "4x", "frm": 2}, {"s": "+ 4", "c": "gold", "dl": 600}, {"s": ")", "g": 0.02},
              {"s": "− 4", "c": "gold", "dl": 800}, {"s": "+", "frm": 3}, {"s": "1", "frm": 4}], y=205, keep=True, z=40)
    f.text(560, 160, "(−4 ÷ 2)^{2} = 4", z=22, c="gold", at=0, dl=1200, b=800)
    S.row(1, [{"s": "(x − 2)^{2}", "frm": [0, 1, 2, 3, 4, 5], "c": "sky"}, {"s": "− 3", "frm": [6, 7, 8], "c": "coral"}], y=305, keep=True, z=46)
    P = Plane(f, (-1, 5), (-4, 3), box=(60, 360, 620, 660), square=False)
    P.axes(at=2, grid=1, lab_step=1)
    P.curve(lambda x: (x - 2) ** 2 - 3, at=2, c="sky", w=4.5)
    P.pt(2, -3, at=2, f="gold", r=12, label="(2, −3)", pos="e", z=24, c="gold", dl=900)
    U.ex("m3-1-27", "y = x^{2} − 4x + 1의 꼭짓점을 구해 보자.", "x의 계수의 절반의 제곱(4)을 더하고 그만큼 뺀다 — 값은 그대로",
         [L("x^{2} − 4x + 1 = (x^{2} − 4x + 4) − 4 + 1", memo="+4와 −4를 함께 넣는다"),
          L("(x^{2} − 4x + 4) − 4 + 1 = (x − 2)^{2} − 3", memo="표준형"),
          L("꼭짓점 (2, −3)")],
         "(2, −3)", f.out(), at=("b2", 2), ident=True)

    # ── 28 이차함수의 식 구하기 ────────────────────────────────
    f = Fig()
    P = Plane(f, (-2, 5), (-3, 8), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.pt(1, -2, at="q", f="gold", r=12, label="꼭짓점 (1, −2)", pos="e", z=22, c="gold")
    P.pt(3, 6, at="q", f="coral", r=12, label="(3, 6)", pos="e", z=24, c="coral")
    P.curve(lambda x: (x - 1) ** 2 - 2, at=0, c="soft", w=3, d=True)
    f.text(P.X(-1.4), P.Y(3.6), "a = 1?", z=22, c="soft", at=0, dl=900, b=800)
    P.pt(3, 2, at=1, f="soft", r=8)
    f.line(*P.P(3, 2), *P.P(3, 6), at=1, c="coral", w=3, ar=1, dr=True, dl=200)
    f.text(P.X(3) + 14, P.Y(4), "4a − 2 = 6", z=22, c="coral", at=1, dl=700, b=800, a="s")
    P.curve(lambda x: 2 * (x - 1) ** 2 - 2, at=2, c="sky", w=4.5)
    f.text(P.X(-0.6), P.Y(7.2), "y = 2(x − 1)^{2} − 2", z=24, c="sky", at=2, dl=800, b=800)
    U.ex("m3-1-28", "꼭짓점이 (1, −2)이고 점 (3, 6)을 지나는 포물선의 식을 구해 보자.", "꼭짓점을 알면 y = a(x − 1)^{2} − 2 — 남은 a는 지나는 점으로",
         [L("y = a(x − 1)^{2} − 2", memo="미지수는 a 하나"),
          L("6 = a(3 − 1)^{2} − 2 → 6 = 4a − 2", memo="(3, 6) 대입"),
          L("a = 2 → y = 2(x − 1)^{2} − 2")],
         "y = 2(x − 1)^{2} − 2", f.out(), at=("b3", 1), sub={"a": 2})

    # ── 29 최솟값 — 가로선이 내려와 꼭짓점에 닿는다 ─────────────
    f = Fig()
    P = Plane(f, (-1, 7), (-1, 9), box=(60, 50, 620, 650))
    P.axes(at="q", grid=1, lab_step=1)
    P.curve(lambda x: (x - 3) ** 2 + 1, at="q", c="sky", w=4.5)
    P.pt(3, 1, at=0, f="gold", r=12, label="(3, 1)", pos="e", z=26, c="gold", dl=600)
    hl = f.line(*P.P(-0.5, 6), *P.P(6.5, 6), at=1, c="coral", w=4)
    slide(hl, 1, dy=P.Y(1) - P.Y(6), dl=400)
    f.text(P.X(5.6), P.Y(7), "(x − 3)^{2} ≥ 0", z=24, c="coral", at=1, dl=200, b=800)
    f.line(*P.P(3, 0), *P.P(3, 1), at=2, c="gold", w=3, d=True)
    f.text(P.X(3), P.Y(-0.6) + 10, "최솟값 1", z=28, c="gold", at=2, dl=300, b=800)
    U.ex("m3-1-29", "y = x^{2} − 6x + 10의 최솟값을 구해 보자.", "표준형으로 바꾸면 꼭짓점의 y좌표가 최솟값",
         [L("x^{2} − 6x + 10 = (x − 3)^{2} + 1", memo="꼭짓점 (3, 1)"),
          L("(x − 3)^{2} ≥ 0", memo="제곱은 0 이상 — 1보다 작아질 수 없다"),
          L("x = 3일 때 최솟값 1")],
         "x = 3일 때 최솟값 1", f.out(), at=("b4", 1))

    # ── 30 이차함수의 활용 — 둘레 20인 직사각형 ─────────────────
    f = Fig()
    sc = 22
    for k, (w, xx) in enumerate(((2, 40), (5, 140), (8, 310))):
        h = 10 - w
        f.rect(xx, 280 - h * sc, w * sc, h * sc, at=0, c="ink", sw=3, f="teal" if w != 5 else "gold", fo=0.35, dl=600 * k)
        f.text(xx + w * sc / 2, 280 - h * sc - 14, f"{w} × {h} = {w * h}", z=22, c="ink", at=0, dl=200 + 600 * k, b=800)
    P = Plane(f, (0, 10.5), (0, 28), box=(70, 340, 620, 650), square=False)
    f.line(P.X(0), P.Y(0), P.X(10.5), P.Y(0), at=1, c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(0), P.X(0), P.Y(28), at=1, c="ink", w=3, ar=1)
    for v in (2, 5, 8, 10):
        f.text(P.X(v), P.Y(0) + 26, str(v), z=20, c="soft", at=1)
    for v in (16, 25):
        f.text(P.X(0) - 8, P.Y(v) + 7, str(v), z=20, c="soft", at=1, a="e")
    for k, (x, y) in enumerate(((2, 16), (5, 25), (8, 16))):
        P.pt(x, y, at=1, f="teal" if x != 5 else "gold", r=10, dl=300 + 250 * k)
    P.curve(lambda x: x * (10 - x), x0=0, x1=10, at=1, c="sky", w=4)
    f.line(*P.P(5, 0), *P.P(5, 25), at=2, c="gold", w=2.5, d=True)
    f.text(P.X(5) + 16, P.Y(25) + 6, "최대 25", z=26, c="gold", at=2, dl=300, b=800, a="s")
    U.ex("m3-1-30", "둘레가 20인 직사각형의 넓이가 가장 클 때, 가로의 길이와 넓이를 구해 보자.", "가로 x → 세로 10 − x → 넓이를 x의 이차함수로",
         [L("넓이 = x(10 − x)", memo="가로 + 세로 = 10"),
          L("x(10 − x) = −(x − 5)^{2} + 25", memo="표준형 — 위로 볼록"),
          L("가로가 5일 때 넓이가 최대 25", memo="정사각형일 때 가장 넓다")],
         "가로 5, 넓이 25", f.out(), at=("b3", 2), ident=True)
