# 중1-1 — 소인수분해 · 정수와 유리수 · 문자와 식 · 일차방정식 · 좌표평면과 그래프
import math
from cv import *
from figs import (Strip, tw, nl_range, hop, travel, slope_tri, table, CX, dot_grid, chip, gear_pts, vnl, balance,
                  order_arcs, bar_grow)


def ladder1(f, n, at=0, step=700, x=380, y0=110, rh=None, z=44, dl0=0):
    """한 수를 소수로 차례로 나누는 사다리 — 판서 at 줄이 써지는 동안 한 칸씩(나눌 소수 → 몫)"""
    ps, m, p = [], n, 2
    while m > 1:
        while m % p == 0:
            ps.append(p)
            m //= p
        p += 1
    rh = rh or min(84, 470 / (len(ps) + 1))
    f.text(x, y0, str(n), z=z, at="q")
    m = n
    for i, p in enumerate(ps):
        y = y0 + rh * i
        d = dl0 + i * step
        f.text(x - 92, y, str(p), z=z, a="e", c="coral", b=700, at=at, dl=d + 1)
        f.poly([(x - 76, y - 40), (x - 68, y - 17), (x - 68, y + 4), (x - 74, y + 15)], z=False, c="ink", w=3, at=at, dl=d + 120, dr=True)
        f.line(x - 76, y + 15, x + 92, y + 15, c="ink", w=3, at=at, dl=d + 200, dr=True)
        m //= p
        f.text(x, y + rh, str(m), z=z, at=at, dl=d + 380)
    return ps, x - 92, y0, rh


def factor_cols(f, A, B, fa, fb, y0=120, gap=86, z=40):
    """두 수의 소인수를 같은 소수끼리 세로로 맞춰 늘어놓기 — 열 x 목록 · 열마다 (소수, 위 있음, 아래 있음)"""
    primes = sorted(set(fa) | set(fb))
    cols = []
    for p in primes:
        for k in range(max(fa.get(p, 0), fb.get(p, 0))):
            cols.append((p, k < fa.get(p, 0), k < fb.get(p, 0)))
    n = len(cols)
    xs = [CX + 40 + (i - (n - 1) / 2) * gap for i in range(n)]
    f.text(xs[0] - 90, y0, f"{A} =", z=z, at="q", a="e", b=700)
    f.text(xs[0] - 90, y0 + 110, f"{B} =", z=z, at="q", a="e", b=700)
    for i, (p, ia, ib) in enumerate(cols):
        if ia:
            chip(f, xs[i], y0, str(p), at="q", c="teal", z=z, dl=60 * i)
        if ib:
            chip(f, xs[i], y0 + 110, str(p), at="q", c="sky", z=z, dl=60 * i + 30)
    return xs, cols


def build(U):
    # ── 01 소수와 합성수 ──────────────────────────────────────
    f = Fig()
    f.text(70, 110, "12", z=40, c="teal", at="q", a="s", b=800)
    p1 = dot_grid(f, 12, 12, "q", cy=170, gap=44, r=12, un=0)
    p2 = dot_grid(f, 12, 6, 0, cy=190, gap=60, r=13, src=p1, un=1)
    f.rect(CX - 186, 132, 372, 116, c="teal", sw=3, rx=14, d=True, at=0, dl=900, un=1)
    dot_grid(f, 12, 4, 1, cy=210, gap=64, r=13, src=p2)
    f.rect(CX - 134, 126, 268, 172, c="teal", sw=3, rx=14, d=True, at=1, dl=900)
    f.text(70, 440, "7", z=40, c="coral", at=2, a="s", b=800)
    q7 = dot_grid(f, 7, 7, 2, cy=500, gap=60, r=13, c="coral")
    f.rect(q7[0][0] - 30, 470, 60 * 6 + 60, 60, c="coral", sw=3, rx=14, d=True, at=2, dl=700)
    f.text(CX, 580, "한 줄로만 놓여요", z=28, c="coral", at=2, dl=1100, b=700)
    U.ex("m1-1-01", "12와 7은 소수일까, 합성수일까? 점을 직사각형으로 늘어놓아 보자.",
         "직사각형으로 늘어놓는 방법 = 곱셈 짝꿍 — 한 줄(1 × 그 수)뿐이면 소수",
         [L("12 = 2 × 6", memo="두 줄로 놓인다"),
          L("12 = 3 × 4", memo="세 줄로도 — 약수가 1, 12 말고도 있다"),
          L("7 = 1 × 7", memo="한 줄뿐 — 약수는 1, 7 두 개")],
         "12는 합성수, 7은 소수", f.out(), at=("b1", 1))

    # ── 02 거듭제곱 ──────────────────────────────────────────
    f = Fig()
    S = Strip(f, y=120, z=46)
    xs, _ = S.row("q", ["2", "×", "2", "×", "2", "×", "2", "×", "2"], keep=True)
    for i, k in enumerate((0, 2, 4, 6, 8)):
        f.text(xs[k], 178, str(i + 1), z=28, c="teal", at=0, dl=1 + 260 * i, b=800)
    f.text(CX - 20, 290, "2", z=78, c="coral", at=0, dl=1500, b=800)
    fly(f.text(CX + 26, 246, "5", z=46, c="teal", at=0, dl=1700, b=800), xs[8] - (CX + 26), 178 - 246, dl=60, ms=700)
    base = 640
    for i in range(5):
        v = 2 ** (i + 1)
        bar_grow(f, 150 + i * 86, base, 58, v * 9.4, at=1, c="gold" if i == 4 else "teal", dl=1 + 330 * i, lab=str(v), z=28)
    f.line(120, base, 600, base, at=1, c="ink", w=3)
    U.ex("m1-1-02", "2를 다섯 번 곱한 수를 거듭제곱으로 나타내고, 그 값을 구해 보자.", "곱한 횟수를 지수로 — 하나씩 곱할 때마다 2배",
         [L("2 × 2 × 2 × 2 × 2 = 2^{5}", memo="2를 5번 → 지수 5"),
          L("2, 4, 8, 16, 32", memo="하나 더 곱할 때마다 2배씩"),
          L("2^{5} = 32")],
         "2^{5} = 32", f.out(), at=("b1", 1))

    # ── 03 소인수분해 ─────────────────────────────────────────
    f = Fig()
    ps, xp, y0, rh = ladder1(f, 72, at=0)
    yb = y0 + rh * (len(ps) + 1) + 40
    fly(f.text(CX - 70, yb, "2^{3}", z=50, c="coral", at=1, b=700, dl=1), xp - 20 - (CX - 70), y0 + rh * 1 - yb, dl=160, ms=760)
    f.text(CX, yb, "×", z=46, at=1, dl=500)
    fly(f.text(CX + 70, yb, "3^{2}", z=50, c="coral", at=1, b=700, dl=2), xp - 20 - (CX + 70), y0 + rh * 3.5 - yb, dl=400, ms=760)
    U.ex("m1-1-03", "72를 소인수분해해 보자.", "나누어떨어지는 가장 작은 소수로 1이 될 때까지 나누기",
         [L("72 = 2 × 2 × 2 × 3 × 3", memo="2로 세 번, 3으로 두 번"),
          L("72 = 2^{3} × 3^{2}", memo="같은 소인수는 거듭제곱으로")],
         "2^{3} × 3^{2}", f.out(), at=("b4", 1))

    # ── 04 약수 구하기(표) ────────────────────────────────────
    f = Fig()
    cw, rh, x0, y0 = 108, 86, 150, 120
    f.rect(x0 - cw, y0, cw, rh, c="ink", sw=2.5, f="gold", fo=0.2, at="q")
    f.text(x0 - cw / 2, y0 + 56, "×", z=36, at="q", b=700)
    for j, v in enumerate((1, 2, 4, 8)):
        f.rect(x0 + j * cw, y0, cw, rh, c="ink", sw=2.5, f="teal", fo=0.18, at=0, dl=1 + 200 * j)
        f.text(x0 + j * cw + cw / 2, y0 + 56, str(v), z=36, c="teal", at=0, dl=80 + 200 * j, b=700)
    for i, v in enumerate((1, 3)):
        f.rect(x0 - cw, y0 + (i + 1) * rh, cw, rh, c="ink", sw=2.5, f="sky", fo=0.18, at=1, dl=1 + 200 * i)
        f.text(x0 - cw / 2, y0 + (i + 1) * rh + 56, str(v), z=36, c="sky", at=1, dl=80 + 200 * i, b=700)
    k = 0
    for i, a in enumerate((1, 3)):
        for j, b in enumerate((1, 2, 4, 8)):
            f.rect(x0 + j * cw, y0 + (i + 1) * rh, cw, rh, c="ink", sw=2, at=2, dl=1 + 170 * k)
            el = f.text(x0 + j * cw + cw / 2, y0 + (i + 1) * rh + 56, str(a * b), z=36, at=2, dl=60 + 170 * k, b=700)
            fly(el, 0, -(i + 1) * rh * 0.5, dl=40, ms=420)
            k += 1
    f.text(x0 + 2 * cw, y0 + 3 * rh + 80, "4 × 2 = 8개", z=36, c="coral", at=3, b=800)
    U.ex("m1-1-04", "24 = 2^{3} × 3의 약수를 표로 빠짐없이 구해 보자.", "(2^{3}의 약수) × (3의 약수)를 가로 · 세로로 곱한다",
         [L("2^{3}의 약수: 1, 2, 4, 8", memo="4개"),
          L("3의 약수: 1, 3", memo="2개"),
          L("곱하면 1, 2, 4, 8, 3, 6, 12, 24", memo="한 칸에 하나씩 — 빠짐없이"),
          L("(3 + 1) × (1 + 1) = 8", memo="지수에 1씩 더해 곱하기")],
         "8개", f.out(), at=("b2", 1))

    # ── 05 최대공약수 ─────────────────────────────────────────
    f = Fig()
    xs, cols = factor_cols(f, 24, 36, {2: 3, 3: 1}, {2: 2, 3: 2})
    common = [i for i, (p, a, b) in enumerate(cols) if a and b]
    for k, i in enumerate(common):
        f.rect(xs[i] - 40, 62, 80, 196, c="gold", sw=4, rx=16, at=1, dl=1 + 300 * k)
    gx = [CX - 120, CX, CX + 120]
    for k, i in enumerate(common):
        fly(f.text(gx[k], 400, str(cols[i][0]), z=50, c="gold", at=2, b=800, dl=1 + 150 * k), xs[i] - gx[k], 230 - 400, dl=80, ms=720)
    f.text(CX - 60, 400, "×", z=44, at=2, dl=700)
    f.text(CX + 60, 400, "×", z=44, at=2, dl=700)
    f.text(CX, 490, "= 12", z=50, c="coral", at=2, dl=1100, b=800)
    U.ex("m1-1-05", "24와 36의 최대공약수를 소인수분해로 구해 보자.", "공통인 소인수만 골라, 지수는 작은 쪽으로 곱한다",
         [L("24 = 2^{3} × 3, 36 = 2^{2} × 3^{2}", memo="소인수분해"),
          L("공통인 소인수: 2^{2}, 3", memo="2는 두 개, 3은 한 개가 함께 있다"),
          L("2^{2} × 3 = 12", memo="지수는 작은 쪽")],
         "12", f.out(), at=("b4", 0))

    # ── 06 최소공배수 ─────────────────────────────────────────
    f = Fig()
    xs, cols = factor_cols(f, 24, 36, {2: 3, 3: 1}, {2: 2, 3: 2})
    for i in range(len(cols)):
        f.rect(xs[i] - 40, 62, 80, 196, c="coral", sw=4, rx=16, at=1, dl=1 + 220 * i)
    gx = [CX - 220 + 110 * k for k in range(len(cols))]
    for i, (p, a, b) in enumerate(cols):
        fly(f.text(gx[i], 400, str(p), z=48, c="coral", at=2, b=800, dl=1 + 120 * i), xs[i] - gx[i], (110 if a else 220) - 400, dl=80, ms=720)
        if i:
            f.text((gx[i] + gx[i - 1]) / 2, 400, "×", z=40, at=2, dl=800)
    f.text(CX, 490, "= 72", z=50, c="coral", at=2, dl=1200, b=800)
    U.ex("m1-1-06", "24와 36의 최소공배수를 소인수분해로 구해 보자.", "모든 소인수를 빠짐없이, 공통인 것은 지수가 큰 쪽으로 곱한다",
         [L("24 = 2^{3} × 3, 36 = 2^{2} × 3^{2}", memo="소인수분해"),
          L("소인수를 모두, 큰 지수로: 2^{3}, 3^{2}", memo="한 열에서 하나씩"),
          L("2^{3} × 3^{2} = 72", memo="지수는 큰 쪽")],
         "72", f.out(), at=("b4", 0))

    # ── 07 최대공약수 · 최소공배수의 응용 ─────────────────────
    f = Fig()
    u = 18
    ox, oy = CX - 12 * u + 60, 120
    f.rect(40, 210, 6 * u, 8 * u, c="ink", sw=3, f="sky", fo=0.35, at="q")
    f.text(40 + 3 * u, 200, "6", z=28, at="q", b=700)
    f.text(32, 210 + 4 * u + 9, "8", z=28, at="q", a="e", b=700)
    k = 0
    for r in range(3):
        for c in range(4):
            el = f.rect(ox + c * 6 * u, oy + r * 8 * u, 6 * u, 8 * u, c="ink", sw=2.5, f="sky", fo=0.3, at=1 + (1 if k >= 6 else 0), dl=1 + 170 * (k % 6))
            fly(el, 40 - (ox + c * 6 * u), 210 - (oy + r * 8 * u), dl=40, ms=560)
            k += 1
    f.rect(ox, oy, 24 * u, 24 * u, c="gold", sw=5, at=3, dl=100)
    f.text(ox + 12 * u, oy - 16, "24", z=34, c="gold", at=3, dl=400, b=800)
    f.text(ox + 24 * u + 16, oy + 12 * u + 12, "24", z=34, c="gold", at=3, dl=400, a="s", b=800)
    U.ex("m1-1-07", "가로 6 cm, 세로 8 cm인 카드를 같은 방향으로 빈틈없이 붙여 가장 작은 정사각형을 만들면, 한 변은 몇 cm일까?",
         "한 변은 6의 배수이면서 8의 배수 — 가장 작은 것은 최소공배수",
         [L("가로로 붙이면 6, 12, 18, 24, …", memo="6의 배수"),
          L("세로로 붙이면 8, 16, 24, …", memo="8의 배수"),
          L("처음 같아지는 길이 24", memo="최소공배수"),
          L("가로 24 ÷ 6 = 4장, 세로 24 ÷ 8 = 3장", memo="모두 12장")],
         "24 cm", f.out(), at=("b3", 0))

    # ── 08 최대공약수와 최소공배수의 관계 ─────────────────────
    f = Fig()
    f.circ(CX - 85, 300, 165, c="teal", sw=4, at="q")
    f.circ(CX + 85, 300, 165, c="sky", sw=4, at="q")
    f.text(CX - 190, 120, "12", z=40, c="teal", at="q", b=800)
    f.text(CX + 190, 120, "18", z=40, c="sky", at="q", b=800)
    fly(f.text(CX, 316, "6", z=56, c="gold", at=0, b=800, dl=1), 0, -200, dl=60, ms=700)
    fly(f.text(CX - 160, 316, "2", z=50, c="teal", at=0, b=800, dl=500), -30, -190, dl=60, ms=700)
    fly(f.text(CX + 160, 316, "3", z=50, c="sky", at=0, b=800, dl=900), 30, -190, dl=60, ms=700)
    f.text(CX, 545, "L = 2 × 6 × 3 = 36", z=40, c="coral", at=1, b=800)
    f.text(CX, 620, "12 × 18 = 6 × 36", z=38, at=2, b=700)
    U.ex("m1-1-08", "12와 18로 최대공약수 G와 최소공배수 L의 관계를 확인해 보자.", "공통 부분 G에, 서로 다른 부분 a, b를 모두 얹으면 L",
         [L("12 = 6 × 2, 18 = 6 × 3", memo="G = 6, 2와 3은 서로소"),
          L("L = 6 × 2 × 3 = 36", memo="모두 한 번씩"),
          L("12 × 18 = 216 = 6 × 36", memo="두 수의 곱 = G × L")],
         "G = 6, L = 36", f.out(), at=("b2", 1))

    # ── 09 양수와 음수 ─────────────────────────────────────────
    f = Fig()
    Y = vnl(f, -6, 6, x=250, y0=620, y1=90)
    f.rect(232, Y(6) - 10, 36, Y(-6) - Y(6) + 20, c="soft", sw=2.5, rx=18, at="q", o=0.6)
    f.line(250, Y(0), 250, Y(3), at=0, c="coral", w=16, dr=True, dl=200, un=1)
    f.text(320, Y(3) + 10, "영상 3도 → +3도", z=30, c="coral", at=0, a="s", dl=900, b=700)
    f.line(250, Y(0), 250, Y(-5), at=1, c="sky", w=16, dr=True, dl=200)
    f.text(320, Y(-5) + 10, "영하 5도 → −5도", z=30, c="sky", at=1, a="s", dl=900, b=700)
    f.text(320, Y(0) + 10, "0도(기준)", z=26, c="soft", at="q", a="s")
    U.ex("m1-1-09", "영상 3도와 영하 5도를 부호를 붙인 수로 나타내 보자.", "기준 0보다 높으면 +, 낮으면 −",
         [L("영상 3도 → +3도", memo="0보다 3만큼 위"),
          L("영하 5도 → −5도", memo="0보다 5만큼 아래")],
         "+3도, −5도", f.out(), at=("b4", 0))

    # ── 10 정수와 유리수 ─────────────────────────────────────
    f = Fig()
    f.rect(40, 200, 580, 440, c="teal", sw=4, rx=24, at="q")
    f.text(70, 240, "유리수", z=30, c="teal", at="q", a="s", b=800)
    f.rect(70, 270, 330, 340, c="sky", sw=4, rx=20, at="q")
    f.text(96, 310, "정수", z=30, c="sky", at="q", a="s", b=800)
    f.rect(110, 340, 170, 120, c="coral", sw=3.5, rx=16, at="q")
    f.text(130, 376, "자연수", z=26, c="coral", at="q", a="s", b=800)
    tops = {"−2": 100, "0": 190, "3": 280, "−{1/2}": 400, "0.7": 520}
    for s, x in tops.items():
        f.text(x, 110, s, z=40, at="q", b=700, un=0 if s == "3" else (1 if s in ("−2", "0") else 2))
    fly(f.text(195, 430, "3", z=44, c="coral", at=0, b=800, dl=1), tops["3"] - 195, 110 - 430, dl=80, ms=720)
    fly(f.text(150, 540, "−2", z=44, c="sky", at=1, b=800, dl=1), tops["−2"] - 150, 110 - 540, dl=80, ms=720)
    fly(f.text(300, 540, "0", z=44, c="sky", at=1, b=800, dl=300), tops["0"] - 300, 110 - 540, dl=80, ms=720)
    fly(f.text(500, 380, "−{1/2}", z=44, c="teal", at=2, b=800, dl=1), tops["−{1/2}"] - 500, 110 - 380, dl=80, ms=720)
    fly(f.text(500, 520, "0.7", z=44, c="teal", at=2, b=800, dl=300), tops["0.7"] - 500, 110 - 520, dl=80, ms=720)
    U.ex("m1-1-10", "−2, 0, 3, −{1/2}, 0.7을 자연수 · 정수 · 유리수로 분류해 보자.", "정수는 자연수 · 0 · 음의 정수, 유리수는 분수로 나타낼 수 있는 수",
         [L("자연수: 3", memo="양의 정수"),
          L("정수: −2, 0, 3", memo="0과 음의 정수까지"),
          L("정수가 아닌 유리수: −{1/2}, 0.7", memo="0.7 = {7/10}")],
         "모두 유리수", f.out(), at=("b4", 1))

    # ── 11 수직선 ─────────────────────────────────────────────
    f = Fig()
    nl = NL(f, -3, 3, y=360, x0=50, x1=610)
    for k in (1, 2):
        x = nl.X(-1 - k / 3)
        f.line(x, nl.y - 9, x, nl.y + 9, at=0, c="coral", w=3, dl=1 + 250 * k)
    nl.pt(-4 / 3, "−{4/3}", at=0, f_="coral", dl=900, z=34)
    f.line(nl.X(2.5), nl.y - 9, nl.X(2.5), nl.y + 9, at=1, c="teal", w=3, dl=1)
    nl.pt(2.5, "+{5/2}", at=1, f_="teal", dl=600, z=34)
    hop(nl, -1, -4 / 3, at=0, c="coral", up=False, dl=500, h=50)
    hop(nl, 2, 2.5, at=1, c="teal", up=False, dl=300, h=50)
    U.ex("m1-1-11", "−{4/3}과 +{5/2}를 수직선 위에 나타내 보자.", "분모만큼 등분한 다음, 0에서 왼쪽(−) · 오른쪽(+)으로",
         [L("−{4/3} = −1 − {1/3}", memo="−1과 −2 사이를 3등분한 첫 칸"),
          L("+{5/2} = 2 + {1/2}", memo="2와 3의 한가운데")],
         "−{4/3}, +{5/2}의 자리", f.out(), at=("b2", 0))

    # ── 12 절댓값 ─────────────────────────────────────────────
    f = Fig()
    nl = NL(f, -6, 6, y=330, x0=40, x1=620)
    nl.pt(0, "0", at="q", f_="ink", r=8, z=26)
    nl.pt(-5, "−5", at="q", f_="coral", z=32)
    nl.pt(3, "+3", at="q", f_="teal", z=32)
    for k in range(5):
        hop(nl, -k, -k - 1, at=0, c="coral", up=False, dl=1 + 260 * k, h=36)
    f.text(nl.X(-2.5), 450, "5칸 → |−5| = 5", z=32, c="coral", at=0, dl=1400, b=800)
    for k in range(3):
        hop(nl, k, k + 1, at=1, c="teal", up=False, dl=1 + 260 * k, h=36)
    f.text(nl.X(1.8), 520, "3칸 → |+3| = 3", z=32, c="teal", at=1, dl=900, b=800)
    U.ex("m1-1-12", "|−5|와 |+3|을 수직선 위의 거리로 구해 보자.", "절댓값 = 원점에서 그 수까지의 거리(칸 수)",
         [L("|−5| = 5", memo="원점에서 왼쪽으로 5칸"),
          L("|+3| = 3", memo="거리는 언제나 0 이상")],
         "5, 3", f.out(), at=("b3", 1))

    # ── 13 수의 대소 관계 ─────────────────────────────────────
    f = Fig()
    nl = NL(f, -6, 2, y=300, x0=50, x1=610)
    nl.pt(-5, "−5", at="q", f_="coral", z=32)
    nl.pt(-2, "−2", at="q", f_="teal", z=32)
    f.line(nl.X(-5.5), 200, nl.X(1.5), 200, at=0, c="gold", w=5, ar=1, dr=True)
    f.text(CX, 170, "오른쪽으로 갈수록 크다", z=28, c="gold", at=0, dl=700, b=800)
    f.line(nl.X(0), 420, nl.X(-5), 420, at=1, c="coral", w=6, ar=1, dr=True)
    f.text(nl.X(-2.5), 465, "거리 5", z=28, c="coral", at=1, dl=500, b=700)
    f.line(nl.X(0), 520, nl.X(-2), 520, at=1, c="teal", w=6, ar=1, dr=True, dl=600)
    f.text(nl.X(-1), 565, "거리 2", z=28, c="teal", at=1, dl=1100, b=700)
    U.ex("m1-1-13", "−5와 −2의 크기를 비교해 보자.", "수직선에서 오른쪽에 있는 수가 더 크다",
         [L("−5는 −2보다 왼쪽 → −5 < −2", memo="왼쪽이 작다"),
          L("|−5| > |−2|인데 −5 < −2", memo="음수끼리는 절댓값이 큰 쪽이 작다")],
         "−5 < −2", f.out(), at=("b3", 0))

    # ── 14 부등호의 사용 ─────────────────────────────────────
    f = Fig()
    nl = NL(f, -4, 5, y=430, x0=40, x1=620)
    nl_range(nl, -2, None, at=0, closed_a=True, right=True, c="sky", up=60)
    nl_range(nl, 3, None, at=1, closed_a=False, right=False, c="coral", up=110)
    f.rect(nl.X(-2), 200, nl.X(3) - nl.X(-2), 130, c="none", f="gold", fo=0.22, at=2, dl=100)
    f.text((nl.X(-2) + nl.X(3)) / 2, 250, "−2 ≤ a < 3", z=40, c="gold", at=2, dl=500, b=800)
    U.ex("m1-1-14", "‘a는 −2 이상이고 3 미만’을 부등호로 나타내 보자.", "이상 · 이하는 등호 포함(●), 초과 · 미만은 빼고(○)",
         [L("−2 이상 → −2 ≤ a", memo="−2를 포함 ●"),
          L("3 미만 → a < 3", memo="3은 빼고 ○"),
          L("−2 ≤ a < 3", memo="작은 수를 왼쪽에, 방향을 맞춰 이어 쓰기")],
         "−2 ≤ a < 3", f.out(), at=("b3", 0))

    # ── 15 유리수의 덧셈 ──────────────────────────────────────
    f = Fig()
    nl = NL(f, -8, 2, y=380, x0=40, x1=620)
    nl.pt(0, "0", at="q", f_="ink", r=8, z=26)
    hop(nl, 0, -7, at=0, c="coral", label="−7", up=True, h=120)
    nl.pt(-7, None, at=0, f_="coral", dl=900)
    hop(nl, -7, -4, at=1, c="teal", label="+3", up=False, h=90)
    nl.pt(-4, "−4", at=1, f_="gold", up=True, dl=900, z=34)
    U.ex("m1-1-15", "(−7) + (+3)을 수직선 위에서 계산해 보자.", "0에서 출발해 −7만큼, 다시 +3만큼 움직인 자리",
         [L("0에서 왼쪽으로 7칸 → −7", memo="음수는 왼쪽"),
          L("오른쪽으로 3칸 → −4", memo="양수는 오른쪽"),
          L("(−7) + (+3) = −4", memo="절댓값의 차 7 − 3, 큰 쪽 부호 −")],
         "−4", f.out(), at=("b2", 1))

    # ── 16 유리수의 곱셈 ──────────────────────────────────────
    f = Fig()
    S = Strip(f, y=120, z=44)
    xs, _ = S.row("q", ["(−2)", "×", "(−3)", "×", "(−5)"], keep=True)
    for i, k in enumerate((0, 2, 4)):
        chip(f, xs[k], 250, "−", at=0, c="coral", z=40, dl=1 + 300 * i, un=1 if i < 2 else 2)
    mid = (xs[0] + xs[2]) / 2
    fly(chip(f, mid, 360, "+", at=1, c="teal", z=40, dl=200, un=2), 0, -110, dl=80, ms=620)
    fly(chip(f, (mid + xs[4]) / 2, 470, "−", at=2, c="coral", z=46, dl=200), 0, -110, dl=80, ms=620)
    f.text(CX, 600, "2 × 3 × 5 = 30", z=40, at=3, b=800)
    U.ex("m1-1-16", "(−2) × (−3) × (−5)를 계산해 보자.", "부호 먼저(음수의 개수) → 절댓값끼리 곱하기",
         [L("음수의 개수: 3개", memo="부호부터 정한다"),
          L("(−) × (−) → (+)", memo="음수 둘이 만나면 +"),
          L("(+) × (−) → (−)", memo="홀수 개면 −"),
          L("2 × 3 × 5 = 30", pre="절댓값"),
          L("(−2) × (−3) × (−5) = −30")],
         "−30", f.out(), at=("b2", 1))

    # ── 17 혼합 계산 ──────────────────────────────────────────
    f = Fig()
    S = Strip(f, y=110, z=46)
    S.row("q", ["12", "÷", "(−2)^{2}", "+", "(5 − 8)"], keep=True)
    S.row(0, [{"s": "12", "frm": 0}, {"s": "÷", "frm": 1}, {"s": "4", "frm": 2, "c": "coral"}, {"s": "+", "frm": 3}, {"s": "(5 − 8)", "frm": 4}], y=230, keep=True)
    S.row(1, [{"s": "12", "frm": 0}, {"s": "÷", "frm": 1}, {"s": "4", "frm": 2}, {"s": "+", "frm": 3}, {"s": "(−3)", "frm": 4, "c": "coral"}], y=350, keep=True)
    S.row(2, [{"s": "3", "frm": [0, 1, 2], "c": "coral"}, {"s": "+", "frm": 3}, {"s": "(−3)", "frm": 4}], y=470, keep=True)
    S.row(3, [{"s": "0", "frm": [0, 1, 2], "c": "gold"}], y=590, keep=True, z=56)
    for k, y in enumerate((230, 350, 470, 590)):
        f.text(60, y, "①②③④"[k], z=36, c="teal", at=k, b=700)
    U.ex("m1-1-17", "12 ÷ (−2)^{2} + (5 − 8)을 계산해 보자.", "거듭제곱 → 괄호 → 곱셈 · 나눗셈 → 덧셈 · 뺄셈",
         [L("(−2)^{2} = 4", memo="① 거듭제곱"),
          L("5 − 8 = −3", memo="② 괄호"),
          L("12 ÷ 4 = 3", memo="③ 나눗셈"),
          L("3 + (−3) = 0", memo="④ 마지막 덧셈")],
         "0", f.out(), at=("b3", 1))

    # ── 18 유리수의 계산의 활용 ───────────────────────────────
    f = Fig()
    nl = NL(f, -4, 6, y=360, x0=40, x1=620)
    nl.pt(-3, "A(−3)", at="q", f_="coral", z=30)
    nl.pt(5, "B(5)", at="q", f_="sky", z=30)
    for k in range(8):
        hop(nl, -3 + k, -2 + k, at=0, c="teal", up=False, dl=1 + 150 * k, h=30)
    f.text(nl.X(1), 470, "8칸", z=32, c="teal", at=0, dl=1300, b=800)
    hop(nl, -3, 1, at=1, c="gold", up=True, label="+4", h=110)
    nl.pt(1, "1", at=1, f_="gold", dl=900, z=34, up=False)
    U.ex("m1-1-18", "두 점 A(−3), B(5) 사이의 거리와 한가운데 점을 구해 보자.", "거리 = (큰 수) − (작은 수), 한가운데는 거리의 절반만큼 이동",
         [L("5 − (−3) = 8", memo="거리 8"),
          L("−3 + 4 = 1", memo="A에서 8의 절반 4만큼"),
          L("(−3 + 5) ÷ 2 = 1", memo="두 수의 합 ÷ 2 로도 같다")],
         "거리 8, 한가운데 점 1", f.out(), at=("b2", 1))

    # ── 19 곱셈 · 나눗셈 기호의 생략 ─────────────────────────
    f = Fig()
    S = Strip(f, y=160, z=46)
    S.row("q", ["(−1)", "×", "a", "×", "b", "×", "a", "×", "3"], keep=True)
    S.row(0, [{"s": "(−1)", "frm": 0}, {"s": "×", "frm": 1}, {"s": "3", "frm": 8, "hop": True, "c": "coral"}, {"s": "×", "frm": 3},
              {"s": "a", "frm": 2}, {"s": "×", "frm": 5}, {"s": "a", "frm": 6, "c": "teal"}, {"s": "×", "frm": 7}, {"s": "b", "frm": 4, "c": "teal"}], y=300, keep=True)
    S.row(1, [{"s": "−3", "frm": [0, 2], "c": "coral"}, {"s": "a", "frm": 4, "g": 0.06}, {"s": "a", "frm": 6, "g": 0.06}, {"s": "b", "frm": 8, "g": 0.06}], y=430, keep=True)
    S.row(2, [{"s": "−3", "frm": 0, "c": "coral"}, {"s": "a^{2}", "frm": [1, 2], "c": "teal", "g": 0.06}, {"s": "b", "frm": 3, "g": 0.06}], y=560, keep=True, z=56)
    U.ex("m1-1-19", "(−1) × a × b × a × 3을 곱셈 기호를 생략해 나타내 보자.", "수는 앞으로, 문자는 알파벳 순서로, 같은 문자는 거듭제곱",
         [L("(−1) × 3 × a × a × b", memo="수를 앞으로, 문자는 알파벳 순서"),
          L("(−3) × a × a × b", memo="수끼리 곱하고 × 생략"),
          L("−3a^{2}b", memo="a × a = a^{2}")],
         "−3a^{2}b", f.out(), at=("b2", 1))

    # ── 20 문자를 사용한 식 ───────────────────────────────────
    f = Fig()
    x0, w, y = 60, 540, 260
    for i in range(10):
        el = f.rect(x0 + w * i / 10, y, w / 10, 90, c="ink", sw=2.5, f="coral" if i >= 7 else "teal", fo=0.3, at="q", dl=40 * i)
        if i >= 7:
            el["mv"] = {"at": 1, "dx": 40, "dy": 170}
    f.line(x0, y - 26, x0 + w, y - 26, at="q", c="ink", w=2.5)
    f.text(x0 + w / 2, y - 40, "정가 x원(10칸 = 100%)", z=30, at="q", b=700)
    f.text(x0 + w * 0.85, y + 300, "30% = 0.3x", z=30, c="coral", at=0, b=800)
    f.text(x0 + w * 0.35, y + 160, "남은 70% = 0.7x", z=32, c="teal", at=2, b=800)
    U.ex("m1-1-20", "정가 x원인 물건을 30% 할인한 가격을 문자를 사용한 식으로 나타내 보자.", "a% = {a/100} — 할인한 만큼 빼기",
         [L("할인 금액 = x × {30/100} = 0.3x", memo="30% = {30/100}"),
          L("x − 0.3x", memo="정가에서 뺀다"),
          L("x − 0.3x = 0.7x", memo="100% − 30% = 70%")],
         "0.7x원", f.out(), at=("b3", 0), ident=True)

    # ── 21 식의 값 ────────────────────────────────────────────
    f = Fig()
    f.text(CX, 110, "a = −2", z=44, c="coral", at="q", b=800)
    S = Strip(f, y=230, z=56)
    S.row("q", ["3", {"s": "a^{2}", "g": 0.05}], keep=True)
    S.y = 345
    xs, els = S.row(0, [{"s": "3", "frm": 0}, {"s": "×", "dl": 300}, {"s": "(−2)^{2}", "c": "coral", "dl": 400}], keep=True)
    fly(els[2], CX - xs[2], 110 - 345, dl=60, ms=760)
    S.row(1, [{"s": "3", "frm": 0}, {"s": "×", "frm": 1}, {"s": "4", "frm": 2, "c": "coral"}], y=460, keep=True)
    S.row(2, [{"s": "12", "frm": [0, 2], "c": "gold"}], y=590, keep=True, z=64)
    U.ex("m1-1-21", "a = −2일 때, 3a^{2}의 값을 구해 보자.", "생략된 ×를 되살리고, 음수는 괄호에 넣어 대입",
         [L("3a^{2} = 3 × (−2)^{2}", memo="음수는 반드시 괄호"),
          L("3 × (−2)^{2} = 3 × 4", memo="(−2)^{2} = 4"),
          L("3 × 4 = 12")],
         "12", f.out(), at=("b4", 0), sub={"a": -2})

    # ── 22 다항식과 일차식 ────────────────────────────────────
    f = Fig()
    S = Strip(f, y=200, z=56)
    xs, _ = S.row("q", ["−3x", "+ 8y", "− 5"], keep=True)
    ws = [tw(s, 56) for s in ("−3x", "+ 8y", "− 5")]
    for i in range(3):
        f.rect(xs[i] - ws[i] / 2 - 10, 140, ws[i] + 20, 84, c="gold", sw=3.5, rx=14, at=0, dl=1 + 350 * i)
        f.text(xs[i], 270, "항", z=28, c="gold", at=0, dl=200 + 350 * i, b=700)
    fly(f.text(xs[0], 400, "x의 계수 −3", z=32, c="teal", at=1, dl=1, b=800), 0, -200, dl=60, ms=600)
    fly(f.text(xs[1], 470, "y의 계수 8", z=32, c="sky", at=1, dl=400, b=800), 0, -270, dl=60, ms=600)
    fly(f.text(xs[2], 540, "상수항 −5", z=32, c="coral", at=2, dl=1, b=800), 0, -340, dl=60, ms=600)
    U.ex("m1-1-22", "다항식 −3x + 8y − 5의 항, 계수, 상수항을 말해 보자.", "항은 부호까지 한 덩어리, 계수는 문자 앞의 수",
         [L("항: −3x, 8y, −5", memo="부호까지 포함"),
          L("x의 계수 −3, y의 계수 8", memo="계수도 부호째"),
          L("상수항 −5", memo="문자가 없는 항")],
         "항 3개, 상수항 −5", f.out(), at=("b2", 1))

    # ── 23 일차식의 덧셈과 뺄셈 ───────────────────────────────
    f = Fig()
    S = Strip(f, y=150, z=46)
    S.row("q", ["(2x − 4)", "−", "(3x − 1)"], keep=True)
    S.row(0, [{"s": "2x", "frm": 0}, {"s": "− 4", "frm": 0}, {"s": "− 3x", "frm": 2, "c": "coral"}, {"s": "+ 1", "frm": 2, "c": "coral"}], y=280, keep=True)
    S.row(1, [{"s": "2x", "frm": 0}, {"s": "− 3x", "frm": 2, "c": "coral"}, {"s": "− 4", "frm": 1}, {"s": "+ 1", "frm": 3, "c": "coral"}], y=410, keep=True)
    S.row(2, [{"s": "−x", "frm": [0, 1], "c": "gold"}, {"s": "− 3", "frm": [2, 3], "c": "gold"}], y=540, keep=True, z=54)
    U.ex("m1-1-23", "(2x − 4) − (3x − 1)을 계산해 보자.", "괄호 앞 −는 안의 부호를 모두 바꾸고, 동류항끼리 모은다",
         [L("2x − 4 − 3x + 1", memo="괄호 앞 −: 3x → −3x, −1 → +1"),
          L("2x − 3x − 4 + 1", memo="동류항끼리 모으기"),
          L("2x − 4 − 3x + 1 = −x − 3", memo="계수끼리 계산")],
         "−x − 3", f.out(), at=("b3", 1), ident=True)

    # ── 24 방정식과 항등식 ────────────────────────────────────
    f = Fig()
    xsx = [110, 300, 500]
    for j, h in enumerate(["x", "2x + 1", "= 7 ?"]):
        f.text(xsx[j], 110, h, z=34, c="soft", at="q", b=800)
    f.line(50, 135, 610, 135, at="q", c="ink", w=2.5)
    for i, x in enumerate((1, 2, 3, 4)):
        y = 200 + 72 * i
        f.text(xsx[0], y, str(x), z=34, at=0, dl=1 + 260 * i, b=700)
        f.text(xsx[1], y, str(2 * x + 1), z=34, at=0, dl=120 + 260 * i, b=700)
        ok = 2 * x + 1 == 7
        f.text(xsx[2], y, "참" if ok else "거짓", z=32, c="teal" if ok else "soft", at=0, dl=220 + 260 * i, b=800)
    f.rect(50, 200 + 72 * 2 - 48, 560, 66, c="teal", sw=4, rx=12, at=0, dl=1400)
    f.text(CX, 540, "2(x + 1)과 2x + 2는", z=32, at=1, b=700)
    f.text(CX, 600, "어느 x에서나 같다 → 항등식", z=32, c="coral", at=1, dl=400, b=800)
    U.ex("m1-1-24", "x = 1, 2, 3, 4를 대입해 2x + 1 = 7의 해를 찾고, 2(x + 1) = 2x + 2와 비교해 보자.", "대입해서 참이 되는 x가 해 — 언제나 참이면 항등식",
         [L("2 × 3 + 1 = 7", pre="x = 3", memo="참 → x = 3은 해"),
          L("2(x + 1) = 2x + 2", memo="x에 무엇을 넣어도 참 → 항등식")],
         "해 x = 3 · 2(x + 1) = 2x + 2는 항등식", f.out(), at=("b4", 1), ident=True)

    # ── 25 등식의 성질 ────────────────────────────────────────
    f = Fig()
    py = balance(f, at="q", y=220, half=200)
    lx, rx = CX - 200, CX + 200
    for k in range(2):
        el = f.rect(lx - 100 + k * 62, py - 62, 54, 54, c="ink", sw=3, f="gold", fo=0.4, at="q")
        t = f.text(lx - 73 + k * 62, py - 22, "x", z=32, at="q", b=700)
        if k == 1:
            el["un"] = 2
            t["un"] = 2
    for k in range(3):
        el = f.rect(lx + 30 + k * 30, py - 30, 26, 26, c="ink", sw=2, f="teal", fo=0.5, at="q")
        el["mv"] = {"at": 0, "dx": -60, "dy": -260, "dl": 1 + 120 * k}
        el["un"] = 1
    for k in range(13):
        r, c = divmod(k, 5)
        el = f.rect(rx - 85 + c * 34, py - 30 - r * 32, 28, 28, c="ink", sw=2, f="teal", fo=0.5, at="q")
        if k >= 10:
            el["mv"] = {"at": 0, "dx": 60, "dy": -220, "dl": 1 + 120 * (k - 10)}
            el["un"] = 1
        elif k >= 5:
            el["un"] = 2
    f.text(CX, 90, "양쪽에서 똑같이 3개씩 빼기", z=28, c="teal", at=0, dl=900, b=700, un=2)
    f.text(CX, 90, "양쪽을 똑같이 반으로", z=28, c="coral", at=2, dl=200, b=700)
    U.ex("m1-1-25", "2x + 3 = 13을 저울처럼 등식의 성질로 풀어 보자.", "양변에 같은 수를 더하고 · 빼고 · 곱하고 · 나눠도 등식은 그대로",
         [L("2x + 3 − 3 = 13 − 3", memo="양변에서 3을 빼기"),
          L("2x = 10"),
          L("{2x/2} = {10/2}", memo="양변을 2로 나누기"),
          L("x = 5")],
         "x = 5", f.out(), at=("b4", 1), sub={"x": 5})

    # ── 26 일차방정식의 풀이 ──────────────────────────────────
    f = Fig()
    S = Strip(f, y=360, z=50)
    xs, _ = S.row("q", ["3", {"s": "(x − 2)", "g": 0.06}, "=", "x", "+ 4"])
    for k, tx in enumerate((xs[1] - 40, xs[1] + 44)):
        a, b = xs[0], tx
        f.poly([(a + (b - a) * i / 12, 300 - 70 * 4 * (i / 12) * (1 - i / 12)) for i in range(13)], at=0, c="teal", w=3.5, z=False, dr=True, ar=1, dl=1 + 350 * k, un=1)
    S.row(0, [{"s": "3x", "frm": [0, 1]}, {"s": "− 6", "frm": 1}, {"s": "=", "frm": 2}, {"s": "x", "frm": 3}, {"s": "+ 4", "frm": 4}])
    S.row(1, [{"s": "3x", "frm": 0}, {"s": "− x", "frm": 3, "hop": True, "c": "coral", "un_hop": 2},
              {"s": "=", "frm": 2}, {"s": "4", "frm": 4}, {"s": "+ 6", "frm": 1, "hop": True, "c": "coral", "un_hop": 2}])
    x2, _ = S.row(2, [{"s": "2x", "frm": [0, 1]}, {"s": "=", "frm": 2}, {"s": "10", "frm": [3, 4]}])
    S.note(3, x2[0], "÷ 2", dy=66, c="teal", z=34, dl=1)
    S.note(3, x2[2], "÷ 2", dy=66, c="teal", z=34, dl=2)
    S.row(3, [{"s": "x", "frm": 0, "dl": 500}, {"s": "=", "frm": 1, "dl": 500}, {"s": "5", "frm": 2, "dl": 500, "c": "gold"}], keep=True)
    U.ex("m1-1-26", "3(x − 2) = x + 4를 풀어 보자.", "괄호 풀기 → 이항해 모으기 → ax = b → 나누기",
         [L("3x − 6 = x + 4", memo="괄호를 풀어요"),
          L("3x − x = 4 + 6", memo="이항하면 부호가 바뀐다"),
          L("2x = 10", memo="양변을 정리"),
          L("x = 5", memo="양변을 2로 나누기")],
         "x = 5", f.out(), at=("b3", 1), sub={"x": 5})

    # ── 27 일차방정식의 활용 ──────────────────────────────────
    f = Fig()
    u = 9.5
    lab = ["x − 1", "x", "x + 1"]
    for i in range(3):
        y = 130 + 120 * i
        f.rect(130, y, 15 * u * 2, 70, c="ink", sw=3, f="teal", fo=0.3, at="q", dl=120 * i)
        f.text(110, y + 47, lab[i], z=28, at="q", a="e", b=700)
    f.rect(130 + 15 * u * 2, 130 + 120, u * 2, 70, c="ink", sw=3, f="teal", fo=0.3, at="q")
    f.rect(130 + 15 * u * 2, 130 + 240, u * 2, 70, c="ink", sw=3, f="teal", fo=0.3, at="q")
    piece = f.rect(130 + 16 * u * 2, 130 + 240, u * 2, 70, c="ink", sw=3, f="coral", fo=0.5, at="q")
    piece["mv"] = {"at": 0, "dx": -u * 2, "dy": -240, "dl": 300}
    f.rect(130 + 15 * u * 2, 130, u * 2, 70, c="coral", sw=3, d=True, at="q")
    for i in range(3):
        f.text(130 + 16 * u, 130 + 120 * i + 47, "x", z=34, c="gold", at=1, dl=1 + 200 * i, b=800)
    f.text(CX, 520, "x × 3 = 48 → x = 16", z=36, c="coral", at=2, b=800)
    f.text(CX, 600, "15, 16, 17", z=42, c="gold", at=3, b=800)
    U.ex("m1-1-27", "연속한 세 자연수의 합이 48일 때, 세 수를 구해 보자.", "가운데 수를 x로 — 세 수는 x − 1, x, x + 1",
         [L("(x − 1) + x + (x + 1) = 48", memo="가운데를 x로"),
          L("3x = 48", memo="−1과 +1이 서로 지워진다"),
          L("x = 16"),
          L("x − 1 = 15, x + 1 = 17", memo="묻는 것은 세 수")],
         "15, 16, 17", f.out(), at=("b3", 0), sub={"x": 16})

    # ── 28 거리 · 속력 · 시간 ────────────────────────────────
    f = Fig()
    table(f, ["", "거리", "속력", "시간"], [["갈 때", "x km", "시속 2 km", "{x/2}시간"], ["올 때", "x km", "시속 3 km", "{x/3}시간"]],
          x0=40, y0=110, cw=[120, 140, 160, 160], rh=84, at_rows=[0, 0], z=30)
    f.rect(40 + 120 + 140 + 160, 110 + 84, 160, 168, c="coral", sw=4, rx=10, at=1, dl=100)
    f.text(40 + 120 + 140 + 160 + 80, 110 + 84 * 3 + 50, "합 = 5시간", z=32, c="coral", at=1, dl=500, b=800)
    f.text(CX, 520, "3x + 2x = 30", z=38, at=2, b=800)
    f.text(CX, 600, "x = 6 (km)", z=42, c="gold", at=3, b=800)
    U.ex("m1-1-28", "등산로를 갈 때는 시속 2 km, 올 때는 시속 3 km로 걸었더니 모두 5시간이 걸렸다. 편도 거리는 몇 km일까?",
         "거리 · 속력 · 시간 3칸 표 — 시간끼리 더해 식을 세운다",
         [L("갈 때 {x/2}시간, 올 때 {x/3}시간", memo="시간 = 거리 ÷ 속력"),
          L("{x/2} + {x/3} = 5", memo="두 시간의 합"),
          L("3x + 2x = 30", memo="양변에 6을 곱하기"),
          L("x = 6")],
         "6 km", f.out(), at=("b3", 1), sub={"x": 6})

    # ── 29 순서쌍과 좌표평면 ──────────────────────────────────
    f = Fig()
    P = Plane(f, (-5, 5), (-5, 5), box=(50, 50, 610, 630))
    P.axes(at="q", grid=1, lab_step=1)
    travel(P, 3, -2, at=0, label="A(3, −2)", pos="se")
    travel(P, -4, 1, at=1, c="sky", label="B(−4, 1)", pos="nw")
    U.ex("m1-1-29", "두 점 A(3, −2), B(−4, 1)을 좌표평면 위에 나타내 보자.", "원점에서 x좌표만큼 가로로, y좌표만큼 세로로",
         [L("A: 오른쪽으로 3, 아래로 2", memo="x좌표 3 → 가로, y좌표 −2 → 세로"),
          L("B: 왼쪽으로 4, 위로 1", memo="음수는 왼쪽 · 아래")],
         "A(3, −2), B(−4, 1)", f.out(), at=("b4", 1))

    # ── 30 사분면 ─────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-6, 6), (-8, 8), box=(50, 40, 610, 640))
    P.axes(at="q", grid=1, lab_step=2)
    f.poly([P.P(-6, 8), P.P(0, 8), P.P(0, 0), P.P(-6, 0)], at=0, c="none", f="sky", fo=0.18, dl=1300)
    f.text(P.X(-3), P.Y(7), "제2사분면 (−, +)", z=28, c="sky", at=0, dl=1500, b=700)
    travel(P, -3, 5, at=0, c="sky", label="(−3, 5)", pos="ne")
    f.poly([P.P(0, 0), P.P(6, 0), P.P(6, -8), P.P(0, -8)], at=1, c="none", f="coral", fo=0.18, dl=1300)
    f.text(P.X(3), P.Y(-2.6), "제4사분면 (+, −)", z=28, c="coral", at=1, dl=1500, b=700)
    travel(P, 2, -7, at=1, c="coral", label="(2, −7)", pos="e")
    U.ex("m1-1-30", "점 (−3, 5)와 점 (2, −7)은 각각 제몇 사분면 위의 점일까?", "x좌표 · y좌표의 부호만 보면 방이 정해진다",
         [L("(−3, 5) → (−, +)", memo="왼쪽 위"),
          L("(2, −7) → (+, −)", memo="오른쪽 아래")],
         "제2사분면, 제4사분면", f.out(), at=("b3", 0))

    # ── 31 그래프 ─────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (0, 32), (0, 1000), box=(70, 60, 620, 560), square=False)
    P.axes(at="q", grid=None, xn="분", yn="m")
    for v in (10, 20, 30):
        f.text(P.X(v), P.Y(0) + 32, str(v), z=24, c="soft", at="q")
    f.text(P.X(0) - 12, P.Y(800) + 8, "800", z=24, c="soft", at="q", a="e")
    f.line(P.X(0), P.Y(800), P.X(10), P.Y(800), at="q", c="soft", w=1.5, d=True)
    pts = [(0, 0), (10, 800), (20, 800), (30, 0)]
    cols = ["teal", "gold", "coral"]
    labs = ["멀어진다", "그대로(쉼)", "돌아온다"]
    for i in range(3):
        A, B = P.P(*pts[i]), P.P(*pts[i + 1])
        f.line(A[0], A[1], B[0], B[1], at=i, c=cols[i], w=6, dr=True)
        f.dot(B[0], B[1], r=10, f=cols[i], at=i, dl=1000)
        f.text((A[0] + B[0]) / 2, min(A[1], B[1]) - 22, labs[i], z=28, c=cols[i], at=i, dl=700, b=800)
    U.ex("m1-1-31", "집에서 공원까지 다녀온 시간과 거리의 그래프를 읽어 보자.", "오르면 멀어지고, 수평이면 그대로, 내리면 가까워진다",
         [L("0 ~ 10분: 800 m까지 멀어진다", memo="그래프가 오른쪽 위로"),
          L("10 ~ 20분: 수평 → 거리가 그대로", memo="공원에서 쉬었다"),
          L("20 ~ 30분: 0으로 내려온다", memo="집으로 돌아왔다")],
         "10분 동안 쉬었다", f.out(), at=("b3", 1))

    # ── 32 정비례 ─────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 5), (-1, 9), box=(80, 50, 600, 640))
    P.axes(at="q", grid=1, lab_step=1, ystep=2)
    for i, x in enumerate((1, 2, 3, 4)):
        P.pt(x, 2 * x, at=0, f="sky", r=10, dl=1 + 300 * i)
    P.lineq(2, 0, at=1, c="sky", w=4.5)
    P.pt(3, 6, at=1, f="coral", r=12, label="(3, 6)", pos="nw", z=28, c="coral", dl=600)
    slope_tri(P, 0, 0, 3, 6, at=2, c="gold")
    U.ex("m1-1-32", "y가 x에 정비례하고 x = 3일 때 y = 6이다. 식을 구하고 그래프를 그려 보자.", "y = ax에 점 하나를 대입하면 a가 결정",
         [L("x가 1, 2, 3, 4일 때 y = 2, 4, 6, 8", memo="x가 2배, 3배 → y도 2배, 3배"),
          L("6 = 3a → a = 2", memo="(3, 6)을 y = ax에 대입"),
          L("y = 2x", memo="원점을 지나는 직선")],
         "y = 2x", f.out(), at=("b3", 1), sub={"a": 2})

    # ── 33 반비례 ─────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-0.5, 7), (-0.5, 7), box=(70, 50, 610, 620))
    P.axes(at="q", grid=1, lab_step=1)
    rects = ((2, 6), (3, 4), (4, 3), (6, 2))
    for i, (x, y) in enumerate(rects):
        at = 0 if i == 0 else 2
        c = "coral" if i == 0 else "gold"
        f.poly([P.P(0, 0), P.P(x, 0), P.P(x, y), P.P(0, y)], at=at, c=c, w=3, f=c, fo=0.14, dl=1 + 450 * max(0, i - 1))
        P.pt(x, y, at=at, f=c, r=10, dl=250 + 450 * max(0, i - 1))
    P.curve(lambda x: 12 / x, 12 / 7, 7, at=3, c="sky", w=4.5)
    f.text(P.X(1), P.Y(6.6), "넓이 = 2 × 6 = 12", z=28, c="coral", at=0, dl=700, b=800, a="s")
    U.ex("m1-1-33", "y가 x에 반비례하고 x = 2일 때 y = 6이다. 식을 구해 보자.", "곱 xy가 일정 — 곱부터 구하면 a",
         [L("a = 2 × 6 = 12", memo="xy = a"),
          L("y = {12/x}"),
          L("3 × 4 = 4 × 3 = 6 × 2 = 12", memo="모서리가 그래프 위인 직사각형의 넓이는 늘 12"),
          L("곡선은 축에 한없이 가까워진다", memo="x = 0인 점은 없다")],
         "y = {12/x}", f.out(), at=("b3", 1))

    # ── 34 정비례와 반비례의 활용 ─────────────────────────────
    f = Fig()
    ca, cb = (200, 290), (200 + 112 + 132, 290)
    ga = f.poly(gear_pts(*ca, 24, 124, 108), at="q", c="ink", w=2.5, f="teal", fo=0.3)
    gb = f.poly(gear_pts(*cb, 30, 152, 136, phase=math.pi / 30), at="q", c="ink", w=2.5, f="sky", fo=0.3)
    ma = f.dot(ca[0], ca[1] - 80, r=11, f="coral", at="q")
    mb = f.dot(cb[0], cb[1] - 104, r=11, f="coral", at="q")
    for el in (ga, ma):
        el["mv"] = {"at": 0, "r": -1800, "cx": ca[0], "cy": ca[1], "dl": 200}
    for el in (gb, mb):
        el["mv"] = {"at": 0, "r": 1440, "cx": cb[0], "cy": cb[1], "dl": 200}
    f.text(ca[0], ca[1] + 14, "24", z=40, at="q", b=800)
    f.text(cb[0], cb[1] + 14, "30", z=40, at="q", b=800)
    f.text(ca[0], 520, "5바퀴", z=32, c="teal", at=0, dl=900, b=800)
    f.text(cb[0], 520, "y바퀴", z=32, c="sky", at=1, dl=1, b=800)
    f.text(CX, 600, "24 × 5 = 30 × y", z=36, c="coral", at=1, dl=500, b=800)
    U.ex("m1-1-34", "톱니 24개짜리 톱니바퀴가 5바퀴 돌 때, 맞물린 톱니 30개짜리는 몇 바퀴 돌까?", "맞물린 두 톱니바퀴는 (톱니 수) × (회전수)가 같다",
         [L("24 × 5 = 120", memo="맞물려 지나간 톱니 수"),
          L("30 × y = 120", memo="곱이 일정 → 반비례"),
          L("y = 4")],
         "4바퀴", f.out(), at=("b3", 1), sub={"y": 4})
