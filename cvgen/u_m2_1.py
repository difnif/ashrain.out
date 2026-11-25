# 중2-1 — 유리수와 순환소수 · 식의 계산 · 부등식 · 연립방정식 · 일차함수
import math
from cv import *
from figs import slide, slides, Strip, tw, CX, nl_range, hop, travel, slope_tri, strike


def chipm(f, x, y, s, at, c="teal", z=36, dl=0, un=None):
    """둥근 칸 글자(칸 + 글자 두 요소 — 함께 옮기려고 둘 다 돌려준다)"""
    w = max(z * 1.25, tw(s, z) + z * 0.6)
    r = f.rect(x - w / 2, y - z * 0.98, w, z * 1.4, c=c, sw=3, rx=z * 0.42, f=c, fo=0.16, at=at, dl=dl, un=un)
    t = f.text(x, y, s, z=z, c=c, at=at, dl=dl + 60, un=un, b=700)
    return [r, t]


def tile(f, x, y, s, c, at, dl=0, un=None, w=54, z=32):
    r = f.rect(x - w / 2, y - w / 2, w, w, c=c, sw=3, rx=9, f=c, fo=0.22, at=at, dl=dl, un=un)
    t = f.text(x, y + z * 0.36, s, z=z, c=c, at=at, dl=dl + 40, un=un, b=700)
    return [r, t]


def mvs(els, at, dx=0, dy=0, dl=0):
    for el in els:
        m = {"at": at}
        if dx:
            m["dx"] = dx
        if dy:
            m["dy"] = dy
        if dl:
            m["dl"] = dl
        el["mv"] = m
    return els


def flys(els, dx, dy, dl=60, ms=680):
    for el in els:
        fly(el, dx, dy, dl=dl, ms=ms)
    return els


def arch(f, x0, x1, y, at, h=46, c="gold", dl=0, un=None, w=3.5):
    """식 위로 휜 화살(분배 · 넘기기)"""
    pts = [(x0 + (x1 - x0) * k / 16, y - h * 4 * (k / 16) * (1 - k / 16)) for k in range(17)]
    return f.poly(pts, at=at, c=c, w=w, z=False, dr=True, ar=1, dl=dl, un=un)


def build(U):
    # ── 01 유리수의 소수 표현 ─────────────────────────────────
    f = Fig()
    f.text(78, 205, "{7/20}", z=50, at="q", b=700)
    f.text(78, 515, "{4/15}", z=50, at="q", b=700)
    f.line(30, 372, 630, 372, at="q", c="soft", w=2, o=0.5)
    c2a = chipm(f, 210, 200, "2", at=0)
    c2b = chipm(f, 300, 200, "2", at=0, dl=160)
    c5a = chipm(f, 390, 200, "5", at=0, dl=320)
    for ch, x in ((c2a, 210), (c2b, 300), (c5a, 390)):
        flys(ch, 78 - x, 34)
    slides(c5a, 1, dx=-110, dl=100)              # 2 와 5 가 짝을 짓는다(5 는 미끄러지고 2 는 뛰어넘는다)
    mvs(c2b, 1, dx=120, dl=100)
    c5b = chipm(f, 490, 200, "5", at=1, c="gold", dl=900)
    flys(c5b, 78 - 490, -40, ms=760)
    f.rect(175, 150, 140, 80, at=1, c="gold", sw=3, rx=16, d=True, dl=1700)
    f.rect(385, 150, 140, 80, at=1, c="gold", sw=3, rx=16, d=True, dl=1800)
    f.text(245, 268, "10", z=30, c="gold", at=1, dl=1900, b=800)
    f.text(455, 268, "10", z=30, c="gold", at=1, dl=2000, b=800)
    f.text(350, 335, "{35/100} = 0.35", z=32, c="teal", at=1, dl=2300, b=800)
    c3 = chipm(f, 220, 510, "3", at=2, c="red")
    c5 = chipm(f, 310, 510, "5", at=2, dl=160)
    flys(c3, 78 - 220, 30)
    flys(c5, 78 - 310, 30)
    c2n = chipm(f, 400, 510, "2", at=3, c="gold")
    flys(c2n, 200, 0)
    f.rect(275, 460, 160, 80, at=3, c="gold", sw=3, rx=16, d=True, dl=800)
    f.text(355, 578, "10", z=30, c="gold", at=3, dl=1000, b=800)
    f.cross(220, 497, s=30, at=3, c="red", dl=1300)
    f.text(205, 578, "짝이 없다", z=24, c="red", at=3, dl=1400, b=800)
    f.text(350, 650, "0.2666…", z=40, c="coral", at=3, dl=1900, b=800)
    U.ex("m2-1-01", "{7/20}과 {4/15}를 소수로 나타낼 때, 유한소수인지 순환소수인지 분모를 보고 판정해 보자.", "기약분수의 분모를 소인수분해 — 2와 5뿐이면 유한소수",
         [L("20 = 2^{2} × 5", memo="분모의 소인수가 2와 5뿐"),
          L("{7/20} = {35/100} = 0.35", memo="2와 5를 짝지으면 10 × 10 = 100"),
          L("15 = 3 × 5", memo="3은 짝지을 수 없다"),
          L("{4/15} = 0.2666…", memo="6이 끝없이 되풀이 → 순환소수")],
         "{7/20}은 유한소수, {4/15}는 순환소수", f.out(), at=("b4", 1))

    # ── 02 순환소수를 분수로 ─────────────────────────────────
    f = Fig()
    xs = {-1: 262, 0: 292}
    for k in range(1, 6):
        xs[k] = 322 + 42 * (k - 1)
    xs[6] = 534
    yA, yB = 220, 330
    f.text(228, yB, "x =", z=44, at=0, a="e", b=700)
    f.text(xs[-1], yB, "0", z=46, at=0, b=700)
    f.text(xs[0], yB, ".", z=46, at=0, b=700)
    for k in range(1, 6):
        f.text(xs[k], yB, "7", z=46, c="teal", at=0, dl=120 * k, b=700)
    f.text(xs[6], yB, "…", z=46, c="teal", at=0, dl=700, b=700)
    f.text(228, yA, "10x =", z=44, at=1, a="e", b=700)
    el = f.text(xs[-1], yA, "7", z=46, c="coral", at=1, dl=200, b=800)
    fly(el, xs[1] - xs[-1], yB - yA, dl=60, ms=760)
    f.text(xs[0], yA, ".", z=46, at=1, b=700)
    for k in range(1, 6):
        el = f.text(xs[k], yA, "7", z=46, c="teal", at=1, dl=200 + 60 * k, b=700)
        fly(el, xs[k + 1] - xs[k], yB - yA, dl=60, ms=760)
    f.text(xs[6], yA, "…", z=46, c="teal", at=1, dl=600, b=700)
    f.text(560, 150, "한 칸씩 왼쪽으로", z=24, c="coral", at=1, dl=1200, b=800)
    f.text(104, yB, "−", z=50, c="coral", at=2, b=800)
    f.line(90, 366, 575, 366, at=2, c="ink", w=3, dl=200)
    f.line(278, yA - 15, 572, yA - 15, at=2, c="red", w=5, dr=True, dl=500)
    f.line(278, yB - 15, 572, yB - 15, at=2, c="red", w=5, dr=True, dl=900)
    f.text(425, 410, "꼬리끼리 지워진다", z=24, c="red", at=2, dl=1300, b=800)
    f.text(CX, 480, "9x = 7", z=50, c="gold", at=2, dl=1700, b=800)
    f.text(CX, 600, "x = {7/9}", z=54, c="gold", at=3, b=800)
    U.ex("m2-1-02", "순환소수 0.777…을 분수로 나타내 보자.", "10배 한 수에서 처음 수를 빼면 끝없는 꼬리가 지워진다",
         [L("x = 0.777…", memo="x로 놓기"),
          L("10x = 7.777…", memo="순환마디가 한 자리 → 10배"),
          L("10x − x = 7.777… − 0.777… = 7", memo="꼬리 .777…이 서로 지워진다"),
          L("9x = 7 → x = {7/9}")],
         "{7/9}", f.out(), at=("b2", 1))

    # ── 03 지수법칙 ───────────────────────────────────────────
    f = Fig()
    for k in range(3):
        tile(f, 60 + 60 * k, 170, "x", "teal", at="q", dl=80 * k)
    f.text(240, 182, "×", z=40, at="q", un=0)
    five = []
    for k in range(5):
        five += tile(f, 300 + 60 * k, 170, "x", "sky", at="q", dl=300 + 80 * k)
    f.text(120, 248, "x^{3}", z=30, c="teal", at="q", un=0, b=800)
    f.text(420, 248, "x^{5}", z=30, c="sky", at="q", un=0, b=800)
    mvs(five, 0, dx=-60, dl=200)
    f.line(33, 212, 507, 212, at=0, c="gold", w=3, dl=1100)
    f.text(270, 262, "x가 8개 → x^{8}", z=32, c="gold", at=0, dl=1300, b=800)
    f.text(120, 340, "(y^{3})^{4}", z=36, at="q", b=700)
    for g in range(4):
        y = 400 + 68 * g
        grp = []
        for k in range(3):
            grp += tile(f, 70 + 60 * k, y, "y", "coral", at=1, dl=250 * g, w=50, z=30)
        grp.append(f.rect(37, y - 32, 186, 64, at=1, c="coral", sw=2.5, rx=12, d=True, dl=250 * g))
        flys(grp, -160, 0, dl=40, ms=560)
    f.text(450, 470, "3개씩 4묶음", z=30, c="coral", at=1, dl=1300, b=800)
    f.text(450, 545, "y^{3 × 4} = y^{12}", z=40, c="gold", at=1, dl=1700, b=800)
    U.ex("m2-1-03", "x^{3} × x^{5}과 (y^{3})^{4}을 간단히 해 보자.", "같은 밑의 곱은 지수를 더하고, 거듭제곱의 거듭제곱은 지수를 곱한다",
         [L("x^{3} × x^{5} = x^{3 + 5} = x^{8}", memo="x 3개와 5개를 이어 붙이면 8개"),
          L("(y^{3})^{4} = y^{3 × 4} = y^{12}", memo="y 3개짜리 묶음이 4개")],
         "x^{8}, y^{12}", f.out(), at=("b2", 1), ident=True)

    # ── 04 단항식의 곱셈 ─────────────────────────────────────
    f = Fig()
    S = Strip(f, y=170, z=48)
    S.row("q", ["(", {"s": "−3", "g": 0.02}, {"s": "x^{2}", "g": 0.02}, {"s": ")", "g": 0.02}, "×", "2", {"s": "x^{4}", "g": 0.02}], keep=True)
    S.row(0, ["(", {"s": "−3", "frm": 1, "c": "coral", "g": 0.02}, "×", {"s": "2", "frm": 5, "c": "coral"}, {"s": ")", "g": 0.02}, "×",
              "(", {"s": "x^{2}", "frm": 2, "c": "teal", "g": 0.02}, "×", {"s": "x^{4}", "frm": 6, "c": "teal"}, {"s": ")", "g": 0.02}], y=320, keep=True)
    xs1, _ = S.row(1, [{"s": "−6", "frm": [1, 3], "c": "coral"}, {"s": "x^{6}", "frm": [7, 9], "c": "teal", "g": 0.02}], y=490, keep=True, z=66)
    f.text(xs1[0] - 30, 570, "(−3) × 2", z=24, c="coral", at=1, dl=1000, b=800)
    f.text(xs1[1] + 40, 570, "2 + 4", z=24, c="teal", at=1, dl=1100, b=800)
    U.ex("m2-1-04", "(−3x^{2}) × 2x^{4}을 계산해 보자.", "계수는 계수끼리 곱하고, 문자는 지수법칙으로",
         [L("(−3x^{2}) × 2x^{4} = (−3 × 2) × (x^{2} × x^{4})", memo="계수끼리 · 문자끼리 모으기"),
          L("(−3 × 2) × (x^{2} × x^{4}) = −6x^{6}", memo="부호 → 계수 곱 → 지수 덧셈")],
         "−6x^{6}", f.out(), at=("b2", 2), ident=True)

    # ── 05 다항식의 뺄셈 ─────────────────────────────────────
    f = Fig()
    S = Strip(f, y=190, z=40)
    xq, _ = S.row("q", ["(", {"s": "x^{2}", "g": 0.02}, "+", "3x", {"s": ")", "g": 0.02}, "−", "(", {"s": "2x^{2}", "g": 0.02}, "−", "x", {"s": ")", "g": 0.02}], keep=True)
    arch(f, xq[5], xq[7], 140, at=0, h=40, un=1)
    arch(f, xq[5], xq[9], 140, at=0, h=70, dl=250, un=1)
    x0, _ = S.row(0, [{"s": "x^{2}", "frm": 1, "c": "teal"}, {"s": "+", "frm": 2}, {"s": "3x", "frm": 3, "c": "sky"},
                      {"s": "−", "frm": 5, "c": "coral"}, {"s": "2x^{2}", "frm": 7, "c": "teal"}, {"s": "+", "frm": 8, "c": "coral"}, {"s": "x", "frm": 9, "c": "sky"}],
                  y=340, keep=True, z=44, dl0=500)
    f.text((x0[3] + x0[6]) / 2, 400, "부호가 모두 바뀐다", z=24, c="coral", at=0, dl=1500, b=800)
    S.row(1, [{"s": "−x^{2}", "frm": [0, 4], "c": "teal"}, {"s": "+", "frm": [1, 5]}, {"s": "4x", "frm": [2, 6], "c": "sky"}], y=520, keep=True, z=58)
    U.ex("m2-1-05", "(x^{2} + 3x) − (2x^{2} − x)를 계산해 보자.", "− 앞의 괄호를 풀 때는 안의 모든 항의 부호를 바꾼다",
         [L("(x^{2} + 3x) − (2x^{2} − x) = x^{2} + 3x − 2x^{2} + x", memo="−2x^{2}, +x — 부호가 바뀐다"),
          L("x^{2} + 3x − 2x^{2} + x = −x^{2} + 4x", memo="동류항끼리 모으기")],
         "−x^{2} + 4x", f.out(), at=("b3", 1), ident=True)

    # ── 06 다항식의 곱셈 ─────────────────────────────────────
    f = Fig()
    ux, u2, H = 200, 90, 190
    x0_, y0_ = 120, 110
    f.rect(x0_, y0_, ux + u2, H, at="q", c="ink", sw=3)
    f.line(x0_ + ux, y0_, x0_ + ux, y0_ + H, at="q", c="ink", w=2.5, d=True)
    f.text(x0_ + ux / 2, y0_ - 16, "x", z=32, at="q", b=700)
    f.text(x0_ + ux + u2 / 2, y0_ - 16, "2", z=32, at="q", b=700)
    f.text(x0_ - 26, y0_ + H / 2 + 10, "x", z=32, at="q", b=700)
    f.rect(x0_, y0_, ux, H, at=0, c="none", f="teal", fo=0.35, dl=100)
    f.text(x0_ + ux / 2, y0_ + H / 2 + 12, "x^{2}", z=40, c="teal", at=0, dl=300, b=800)
    f.rect(x0_ + ux, y0_, u2, H, at=0, c="none", f="gold", fo=0.4, dl=700)
    f.text(x0_ + ux + u2 / 2, y0_ + H / 2 + 12, "2x", z=36, c="gold", at=0, dl=900, b=800)
    f.text(560, y0_ + H / 2 + 12, "x^{2} + 2x", z=30, c="ink", at=0, dl=1300, b=800)
    S = Strip(f, y=440, z=46)
    xr, _ = S.row(1, ["−2x", {"s": "(", "g": 0.06}, {"s": "x", "g": 0.02}, "−", "1", {"s": ")", "g": 0.02}], keep=True)
    arch(f, xr[0], xr[2], 392, at=1, h=44, dl=600)
    arch(f, xr[0], xr[4], 392, at=1, h=74, dl=850)
    S.row(1, [{"s": "−2x^{2}", "frm": [0, 2], "c": "teal"}, {"s": "+", "frm": 3, "c": "coral"}, {"s": "2x", "frm": [0, 4], "c": "coral"}], y=590, keep=True, z=52, dl0=1400)
    f.text(CX, 650, "(−2x) × (−1) = +2x", z=24, c="coral", at=1, dl=2300, b=800)
    U.ex("m2-1-06", "x(x + 2)와 −2x(x − 1)을 전개해 보자.", "분배법칙 — 앞의 단항식을 괄호 안 모든 항에 곱한다",
         [L("x(x + 2) = x × x + x × 2 = x^{2} + 2x", memo="넓이로 보면 두 칸의 합"),
          L("−2x(x − 1) = −2x^{2} + 2x", memo="음수 계수는 부호까지 배달")],
         "x^{2} + 2x, −2x^{2} + 2x", f.out(), at=("b2", 2), ident=True)

    # ── 07 부등식의 성질 ─────────────────────────────────────
    f = Fig()
    nl = NL(f, -10, 4, y=420, x0=40, x1=620, step=1, lab_step=2, z=22)
    pa = f.dot(nl.X(2), nl.y, r=12, f="teal", at="q")
    pb = f.dot(nl.X(3), nl.y, r=12, f="coral", at="q", dl=150)
    f.text(nl.X(2), nl.y - 30, "2", z=28, c="teal", at="q", b=800)
    f.text(nl.X(3), nl.y - 30, "3", z=28, c="coral", at="q", b=800)
    f.text(nl.X(2.5), 250, "2 < 3", z=36, at=0, b=800)
    qa = f.dot(nl.X(2), nl.y, r=12, f="teal", at=1)
    slide(qa, 1, dx=nl.X(-6) - nl.X(2), dl=200)
    qb = f.dot(nl.X(3), nl.y, r=12, f="coral", at=1)
    slide(qb, 1, dx=nl.X(-9) - nl.X(3), dl=500)
    hop(nl, 2, -6, at=1, c="teal", up=False, dl=200, h=70)
    hop(nl, 3, -9, at=1, c="coral", up=False, dl=500, h=120)
    f.text(nl.X(-6), nl.y - 30, "−6", z=28, c="teal", at=1, dl=1200, b=800)
    f.text(nl.X(-9), nl.y - 30, "−9", z=28, c="coral", at=1, dl=1400, b=800)
    f.text(nl.X(-4.6), 600, "× (−3)", z=30, c="gold", at=1, dl=900, b=800)
    f.text(nl.X(-7.5), 250, "−6 > −9", z=36, c="gold", at=2, b=800)
    f.text(nl.X(-2.5), 160, "왼쪽 · 오른쪽이 뒤바뀐다", z=26, c="red", at=2, dl=600, b=800)
    U.ex("m2-1-07", "2 < 3의 양변에 −3을 곱하면 부등호는 어떻게 될까?", "음수를 곱하거나 나누면 부등호 방향이 반대로",
         [L("2 < 3", memo="양변에 −3을 곱하면?"),
          L("2 × (−3) = −6, 3 × (−3) = −9", memo="수직선에서 0을 사이에 두고 뒤집힌다"),
          L("−6 > −9", memo="부등호 방향이 반대")],
         "a < b이면 −3a > −3b", f.out(), at=("b4", 2))

    # ── 08 일차부등식의 풀이 ─────────────────────────────────
    f = Fig()
    S = Strip(f, y=120, z=46)
    S.row("q", ["−x", "+", "2", "<", "5"], keep=True)
    S.row(0, [{"s": "−x", "frm": 0}, {"s": "<", "frm": 3}, {"s": "5", "frm": 4}, {"s": "−", "frm": 1, "c": "coral"}, {"s": "2", "frm": 2, "c": "coral", "hop": True}], y=235, keep=True)
    S.row(1, [{"s": "−x", "frm": 0}, {"s": "<", "frm": 1}, {"s": "3", "frm": [2, 3, 4], "c": "teal"}], y=350, keep=True)
    S.row(2, [{"s": "x", "frm": 0}, {"s": ">", "frm": 1, "c": "red"}, {"s": "−3", "frm": 2, "c": "teal"}], y=465, keep=True, z=54)
    f.text(130, 440, "÷ (−1)", z=26, c="red", at=2, dl=200, b=800)
    f.text(520, 465, "방향 반대!", z=26, c="red", at=2, dl=700, b=800)
    nl = NL(f, -6, 3, y=630, x0=60, x1=600, step=1, lab_step=1, z=20, at=2)
    nl_range(nl, -3, None, at=2, closed_a=False, right=True, c="coral", dl=1200)
    U.ex("m2-1-08", "일차부등식 −x + 2 < 5를 풀어 보자.", "이항해서 x를 홀로 — 음수로 나누면 부등호 방향이 바뀐다",
         [L("−x < 5 − 2", memo="2를 우변으로 이항"),
          L("−x < 3"),
          L("x > −3", memo="−1로 나누면 방향이 반대 · −3은 ○")],
         "x > −3", f.out(), at=("b2", 2))

    # ── 09 일차부등식의 활용 (1) ─────────────────────────────
    f = Fig()
    sc = 560 / 5000
    f.rect(50, 150, 560, 60, at="q", c="ink", sw=3, rx=8, f="gold", fo=0.18)
    f.text(330, 190, "5000원", z=32, at="q", b=800)
    for k in range(6):
        x = 50 + 800 * sc * k
        tile_ = f.rect(x, 250, 800 * sc - 4, 70, at=0, c="ink", sw=2.5, rx=8, f="teal", fo=0.4, dl=1 + 260 * k)
        fly(tile_, 0, -150, dl=40, ms=480)
        t = f.text(x + 800 * sc / 2 - 2, 296, str(k + 1), z=30, at=0, dl=80 + 260 * k, b=800)
        fly(t, 0, -150, dl=40, ms=480)
    f.text(330, 380, "800원씩 6개 = 4800원", z=28, c="teal", at=1, b=800)
    x7 = 50 + 800 * sc * 6
    t7 = f.rect(x7, 250, 800 * sc - 4, 70, at=2, c="red", sw=3, rx=8, f="coral", fo=0.4, d=True)
    fly(t7, 0, -150, dl=40, ms=480)
    f.text(x7 + 44, 296, "7", z=30, c="red", at=2, dl=80, b=800)
    f.line(610, 230, 610, 340, at=2, c="red", w=3, d=True, dl=500)
    f.text(330, 470, "7개면 5600원 > 5000원", z=28, c="red", at=2, dl=700, b=800)
    f.text(330, 570, "최대 6개", z=44, c="gold", at=2, dl=1300, b=800)
    U.ex("m2-1-09", "한 개에 800원인 음료수를 5000원 이하로 산다면 최대 몇 개까지 살 수 있을까?", "미지수 → 부등식 → 풀기 → 조건(자연수) 확인",
         [L("800x ≤ 5000", memo="x개의 값이 5000원 이하"),
          L("x ≤ 6.25", memo="5000 ÷ 800 = 6.25"),
          L("x는 자연수 → 최대 6", memo="7개는 5600원 — 넘친다")],
         "6개", f.out(), at=("b2", 2))

    # ── 10 일차부등식의 활용 (2) ─────────────────────────────
    f = Fig()
    P = Plane(f, (0, 9.5), (0, 12), box=(90, 80, 630, 600), square=False)
    f.line(P.X(0), P.Y(0), P.X(9.5), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(0), P.X(0), P.Y(12), at="q", c="ink", w=3, ar=1)
    for v in range(1, 10):
        f.text(P.X(v), P.Y(0) + 28, str(v), z=20, c="soft", at="q")
    for v in (3, 6, 9):
        f.text(P.X(0) - 10, P.Y(v) + 7, f"{v}000", z=20, c="soft", at="q", a="e")
        f.line(P.X(0), P.Y(v), P.X(9.3), P.Y(v), at="q", c="soft", w=1, o=0.35)
    f.text(P.X(9.5) - 4, P.Y(0) + 62, "(개)", z=22, c="soft", at="q")
    f.text(P.X(0) + 40, P.Y(12) + 10, "(원)", z=22, c="soft", at="q")
    f.line(*P.P(0, 0), *P.P(9.5, 11.4), at=0, c="teal", w=4.5, dr=True)
    f.text(*P.P(2.6, 1.7), "문구점", z=26, c="teal", at=0, dl=600, b=800)
    f.line(*P.P(0, 1.8), *P.P(9.5, 10.35), at=0, c="coral", w=4.5, dr=True, dl=500)
    f.text(*P.P(1.3, 4.0), "할인 매장", z=26, c="coral", at=0, dl=1100, b=800)
    f.poly([P.P(6, 7.2), P.P(9.5, 11.4), P.P(9.5, 10.35)], at=1, c="none", f="gold", fo=0.4)
    f.text(*P.P(8.2, 11.6), "할인 매장이 더 싸다", z=22, c="gold", at=1, dl=300, b=800)
    f.line(*P.P(6, 0), *P.P(6, 7.2), at=2, c="gold", w=3, d=True, dr=True)
    P.pt(6, 7.2, at=2, f="gold", r=10, dl=400)
    f.text(*P.P(4.5, 8.3), "6개: 7200원으로 같다", z=22, c="ink", at=2, dl=700, b=700)
    for k in (7, 8, 9):
        P.pt(k, 0.9 * k + 1.8, at="a", f="coral", r=9, dl=150 * (k - 7))
    U.ex("m2-1-10", "문구점은 한 개 1200원, 할인 매장은 한 개 900원에 왕복 교통비 1800원이 든다. 몇 개 이상 살 때 할인 매장이 유리할까?", "두 곳의 비용을 식으로 세워 부등호로 비교한다",
         [L("문구점 1200x원, 할인 매장 (900x + 1800)원", memo="x개 살 때"),
          L("900x + 1800 < 1200x", memo="할인 매장이 더 싸려면"),
          L("1800 < 300x → x > 6", memo="6개면 두 곳이 같다")],
         "7개 이상", f.out(), at=("b2", 2))

    # ── 11 미지수가 2개인 일차방정식 ─────────────────────────
    f = Fig()
    P = Plane(f, (0, 5.5), (0, 9), box=(80, 70, 600, 620))
    P.axes(at="q", grid=1, lab_step=1)
    f.line(*P.P(0, 8), *P.P(4, 0), at="q", c="soft", w=2.5, d=True)
    for i, (x, y) in enumerate(((1, 6), (2, 4), (3, 2))):
        f.line(*P.P(x, 0), *P.P(x, y), at=i, c="teal", w=3, d=True, dr=True, ar=1)
        P.pt(x, y, at=i, f="teal", r=11, label=f"({x}, {y})", pos="e", z=26, c="teal", dl=700)
    P.pt(4, 0, at=3, f="red", r=11, dl=100)
    f.cross(P.X(4), P.Y(0), s=26, at=3, c="red", dl=500)
    f.text(P.X(4) + 20, P.Y(0) - 40, "y = 0 → 탈락", z=24, c="red", at=3, dl=700, b=800, a="s")
    U.ex("m2-1-11", "x, y가 자연수일 때 일차방정식 2x + y = 8의 해를 모두 구해 보자.", "x에 1, 2, 3, …을 차례로 넣고 y도 자연수인지 확인",
         [L("x = 1 → y = 8 − 2 = 6"),
          L("x = 2 → y = 8 − 4 = 4"),
          L("x = 3 → y = 8 − 6 = 2"),
          L("x = 4 → y = 0", memo="0은 자연수가 아니므로 탈락")],
         "(1, 6), (2, 4), (3, 2) — 3개", f.out(), at=("b3", 1))

    # ── 12 연립방정식의 풀이(가감법) ─────────────────────────
    f = Fig()
    cx_ = {"x": 230, "op": 300, "y": 360, "eq": 430, "r": 500}
    for row, (op, rhs) in ((180, ("+", "7")), (280, ("−", "3"))):
        f.text(cx_["x"], row, "x", z=48, c="teal", at="q", b=700)
        f.text(cx_["op"], row, op, z=48, c="coral", at="q", b=700)
        f.text(cx_["y"], row, "y", z=48, c="coral", at="q", b=700)
        f.text(cx_["eq"], row, "=", z=48, at="q", b=700)
        f.text(cx_["r"], row, rhs, z=48, at="q", b=700)
    f.text(140, 280, "+", z=52, c="gold", at=0, b=800)
    f.line(120, 318, 560, 318, at=0, c="ink", w=3, dl=200)
    f.rect(cx_["op"] - 34, 132, 104, 170, at=0, c="red", sw=3, rx=14, d=True, dl=500)
    f.text(cx_["y"] - 30, 380, "+y − y = 0", z=24, c="red", at=0, dl=800, b=800)
    e = f.text(cx_["x"], 440, "2x", z=52, c="teal", at=0, dl=1300, b=800)
    fly(e, 0, -210, dl=40, ms=700)
    f.text(cx_["eq"], 440, "=", z=52, at=0, dl=1400, b=700)
    e = f.text(cx_["r"], 440, "10", z=52, at=0, dl=1500, b=800)
    fly(e, 0, -210, dl=40, ms=700)
    f.text(CX, 530, "x = 5", z=48, c="gold", at=1, b=800)
    f.text(CX, 620, "y = 2", z=48, c="gold", at=2, b=800)
    U.ex("m2-1-12", "연립방정식 x + y = 7, x − y = 3을 풀어 보자.", "두 식을 더하면 +y와 −y가 지워진다(가감법)",
         [L("(x + y) + (x − y) = 7 + 3", memo="두 식을 더하면 y가 사라진다"),
          L("2x = 10 → x = 5"),
          L("5 + y = 7 → y = 2", memo="x = 5를 첫 식에 대입")],
         "x = 5, y = 2", f.out(), at=("b2", 1), sub={"x": 5, "y": 2})

    # ── 13 여러 가지 연립방정식 ─────────────────────────────
    f = Fig()
    S = Strip(f, y=140, z=44)
    S.row("q", ["0.3x", "−", "0.1y", "=", "0.5"], keep=True)
    S.row(0, [{"s": "3x", "frm": 0, "c": "coral"}, {"s": "−", "frm": 1}, {"s": "y", "frm": 2, "c": "coral"}, {"s": "=", "frm": 3}, {"s": "5", "frm": 4, "c": "coral"}], y=255, keep=True, z=48)
    f.text(70, 200, "× 10", z=30, c="gold", at=0, b=800)
    S2 = Strip(f, y=345, z=48)
    S2.row(1, ["x", "+", "y", "=", "3"], keep=True)
    f.text(140, 345, "+", z=50, c="gold", at=1, dl=300, b=800)
    f.line(140, 380, 520, 380, at=1, c="ink", w=3, dl=400)
    e = f.text(CX, 460, "4x = 8", z=50, c="teal", at=1, dl=1000, b=800)
    fly(e, 0, -150, dl=40, ms=700)
    f.text(CX, 580, "(2, 1)", z=52, c="gold", at=2, b=800)
    U.ex("m2-1-13", "연립방정식 0.3x − 0.1y = 0.5, x + y = 3을 풀어 보자.", "소수 계수는 10을 곱해 정수 계수로 바꾼다",
         [L("0.3x − 0.1y = 0.5 → 3x − y = 5", memo="양변에 10을 곱한다"),
          L("(3x − y) + (x + y) = 5 + 3 → 4x = 8", memo="짝꿍 식과 더하면 y가 지워진다"),
          L("x = 2, y = 1", memo="y = 3 − 2")],
         "x = 2, y = 1", f.out(), at=("b3", 1), sub={"x": 2, "y": 1})

    # ── 14 연립방정식의 활용 (1) ─────────────────────────────
    f = Fig()
    bx = [72 + 76 * k for k in range(7)]
    for k, x in enumerate(bx):
        f.rect(x - 32, 150, 64, 64, at=0, c="soft", sw=2.5, rx=10, dl=70 * k)
    f.text(CX, 120, "모두 7개", z=26, at=0, dl=600, b=800)
    for k, x in enumerate(bx):
        f.rect(x - 32, 150, 64, 64, at=1, c="teal", sw=3, rx=10, f="teal", fo=0.35, dl=80 * k)
        f.text(x, 192, "500", z=20, c="teal", at=1, dl=40 + 80 * k, b=800, un=2 if k >= 4 else None)
    f.text(CX, 270, "모두 사탕이면 500 × 7 = 3500원", z=24, c="teal", at=1, dl=800, b=800)
    for j, k in enumerate((4, 5, 6)):
        x = bx[k]
        f.rect(x - 32, 150, 64, 64, at=2, c="coral", sw=3, rx=10, f="coral", fo=0.55, dl=600 * j)
        f.text(x, 192, "800", z=20, c="coral", at=2, dl=60 + 600 * j, b=800)
        e = f.text(x, 140, "+300", z=22, c="coral", at=2, dl=120 + 600 * j, b=800)
        fly(e, 0, 30, dl=40, ms=500)
        f.text(CX, 340 + 52 * j, f"{3500 + 300 * (j + 1)}원", z=30 if j < 2 else 36, c="coral" if j < 2 else "gold", at=2, dl=300 + 600 * j, b=800)
    f.text(CX, 560, "사탕 4개 · 초콜릿 3개", z=32, c="gold", at=3, b=800)
    U.ex("m2-1-14", "500원짜리 사탕과 800원짜리 초콜릿을 합해서 7개 사고 4400원을 냈다. 각각 몇 개씩 샀을까?", "미지수 2개 → 조건 2개로 식 2개 → 풀고 검산",
         [L("x + y = 7", memo="사탕 x개, 초콜릿 y개"),
          L("500x + 800y = 4400", memo="금액 — 100으로 나누면 5x + 8y = 44"),
          L("5x + 8y − 5(x + y) = 44 − 35 → 3y = 9", memo="모두 사탕일 때보다 900원 더 — 하나 바꿀 때마다 300원"),
          L("y = 3, x = 4")],
         "사탕 4개, 초콜릿 3개", f.out(), at=("b3", 1), sub={"x": 4, "y": 3})

    # ── 15 연립방정식의 활용 (2) — 소금물 ───────────────────
    f = Fig()

    def beaker(x, y, w, h, at, lab):
        f.poly([(x, y), (x, y + h), (x + w, y + h), (x + w, y)], at=at, c="ink", w=3.5, z=False)
        f.text(x + w / 2, y + h + 36, lab, z=24, at=at, b=800)

    beaker(60, 120, 140, 200, "q", "5%  x g")
    beaker(250, 120, 140, 200, "q", "9%  y g")
    beaker(460, 120, 150, 420, "q", "7%  400 g")
    a = f.rect(64, 220, 132, 96, at="q", c="none", f="teal", fo=0.4)
    b_ = f.rect(254, 220, 132, 96, at="q", c="none", f="sky", fo=0.55)
    a2 = f.rect(64, 220, 132, 96, at=0, c="none", f="teal", fo=0.4)
    a2["mv"] = {"at": 0, "dx": 400, "dy": 224, "dl": 200}
    b2 = f.rect(254, 220, 132, 96, at=0, c="none", f="sky", fo=0.55, dl=500)
    b2["mv"] = {"at": 0, "dx": 210, "dy": 128, "dl": 700}
    f.text(535, 168, "x + y = 400", z=24, c="ink", at=0, dl=1700, b=800)
    for (cx0, n, col) in ((130, 5, "teal"), (320, 9, "sky")):
        for k in range(n):
            f.dot(cx0 - 50 + (k % 5) * 25, 255 + (k // 5) * 26, r=6, f="ink", at=1, dl=60 * k)
    f.text(130, 420, "소금 10 g", z=24, c="teal", at=1, dl=700, b=800)
    f.text(320, 420, "소금 18 g", z=24, c="sky", at=1, dl=900, b=800)
    f.text(535, 300, "소금 28 g", z=26, c="gold", at=1, dl=1400, b=800)
    f.text(225, 500, "10 + 18 = 28", z=28, c="gold", at=1, dl=1700, b=800)
    f.text(225, 600, "x = 200, y = 200", z=30, c="coral", at=3, b=800)
    U.ex("m2-1-15", "5% 소금물 x g과 9% 소금물 y g을 섞어 7% 소금물 400 g을 만들었다. x, y를 구해 보자.", "섞어도 변하지 않는 두 양 — 소금물의 양과 소금의 양",
         [L("x + y = 400", memo="소금물의 양"),
          L("{5/100}x + {9/100}y = {7/100} × 400", memo="소금의 양은 섞어도 그대로"),
          L("5x + 9y = 2800", memo="양변에 100을 곱한다"),
          L("4y = 800 → y = 200, x = 200", memo="5(x + y) = 2000을 빼면")],
         "5% 200 g, 9% 200 g", f.out(), at=("b3", 1), sub={"x": 200, "y": 200})

    # ── 16 함수와 함숫값 ─────────────────────────────────────
    f = Fig()
    f.poly([(260, 110), (300, 170), (360, 170), (400, 110)], at="q", c="ink", w=3, z=False)
    f.rect(210, 170, 240, 170, at="q", c="ink", sw=3.5, rx=18, f="lilac", fo=0.18)
    f.text(CX, 235, "f", z=40, c="lilac", at="q", b=800)
    f.text(CX, 300, "2x − 1", z=34, at="q", b=700)
    f.rect(300, 340, 60, 40, at="q", c="ink", sw=3, rx=6)
    i3 = chipm(f, CX, 90, "3", at=0, c="teal", z=36, un=1)
    flys(i3, 0, -60, dl=40, ms=500)
    slides(i3, 0, dy=50, dl=600)
    o5 = chipm(f, CX, 450, "5", at=0, c="coral", z=40, dl=1500)
    flys(o5, 0, -150, dl=40, ms=600)
    f.text(CX, 525, "2 × 3 − 1 = 5", z=26, c="coral", at=0, dl=1900, b=800, un=1)
    mvs(o5, 1, dx=-230, dl=100)
    f.text(100, 525, "f(3) = 5", z=26, c="coral", at=1, dl=900, b=800)
    i0 = chipm(f, CX, 90, "0", at=1, c="teal", z=36, dl=300)
    flys(i0, 0, -60, dl=40, ms=500)
    slides(i0, 1, dy=50, dl=900)
    o1 = chipm(f, CX, 450, "−1", at=1, c="coral", z=40, dl=1800)
    flys(o1, 0, -150, dl=40, ms=600)
    f.text(CX, 525, "f(0) = −1", z=26, c="coral", at=1, dl=2200, b=800)
    U.ex("m2-1-16", "f(x) = 2x − 1일 때, f(3)과 f(0)을 구해 보자.", "f(a)는 x = a를 넣었을 때 나오는 값",
         [L("f(3) = 2 × 3 − 1 = 5", memo="3을 넣으면 5가 나온다"),
          L("f(0) = 2 × 0 − 1 = −1", memo="0을 넣는 것도 똑같은 대입")],
         "f(3) = 5, f(0) = −1", f.out(), at=("b3", 1))

    # ── 17 일차함수의 그래프와 절편 ─────────────────────────
    f = Fig()
    P = Plane(f, (-2, 5), (-2, 8), box=(50, 50, 620, 640))
    P.axes(at="q", grid=1, lab_step=1)
    m = f.dot(*P.P(0, 0), r=12, f="coral", at=0)
    slide(m, 0, dy=P.Y(6) - P.Y(0), dl=200)
    f.text(P.X(0) - 18, P.Y(6) + 8, "y절편 6", z=26, c="coral", at=0, dl=1100, b=800, a="e")
    m = f.dot(*P.P(0, 0), r=12, f="teal", at=1)
    slide(m, 1, dx=P.X(2) - P.X(0), dl=200)
    f.text(P.X(2) + 6, P.Y(0) - 22, "x절편 2", z=26, c="teal", at=1, dl=1100, b=800, a="s")
    P.lineq(-3, 6, at=2, c="sky", w=5)
    f.text(P.X(3.2), P.Y(-1.2), "y = −3x + 6", z=26, c="sky", at=2, dl=800, b=800)
    U.ex("m2-1-17", "y = −3x + 6의 x절편과 y절편을 구하고 그래프를 그려 보자.", "x = 0을 넣으면 y절편, y = 0을 넣으면 x절편",
         [L("x = 0 → y = −3 × 0 + 6 = 6", memo="y축과 만나는 점 (0, 6)"),
          L("y = 0 → 3x = 6 → x = 2", memo="x축과 만나는 점 (2, 0)"),
          L("(0, 6)과 (2, 0)을 잇는다", memo="두 점이면 직선 하나")],
         "x절편 2, y절편 6", f.out(), at=("b3", 2))

    # ── 18 기울기 ─────────────────────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 5), (-1, 10), box=(60, 50, 620, 640))
    P.axes(at="q", grid=1, lab_step=1)
    P.pt(1, 2, at="q", f="teal", r=10, label="(1, 2)", pos="se", z=24, c="teal")
    P.pt(3, 8, at="q", f="coral", r=10, label="(3, 8)", pos="nw", z=24, c="coral")
    f.line(*P.P(1, 2), *P.P(3, 2), at=0, c="gold", w=5, dr=True, ar=1)
    f.text(P.X(2), P.Y(2) + 36, "+2", z=30, c="gold", at=0, dl=500, b=800)
    f.line(*P.P(3, 2), *P.P(3, 8), at=1, c="coral", w=5, dr=True, ar=1)
    f.text(P.X(3) + 18, P.Y(5) + 10, "+6", z=30, c="coral", at=1, dl=600, b=800, a="s")
    P.lineq(3, -1, at=2, c="sky", w=4.5)
    slope_tri(P, 0, -1, 1, 3, at=2, dl=700, z=22)
    f.text(P.X(4.0), P.Y(6.6), "{6/2} = 3", z=32, c="sky", at=2, dl=1300, b=800)
    U.ex("m2-1-18", "두 점 (1, 2), (3, 8)을 지나는 직선의 기울기를 구해 보자.", "기울기 = (y의 증가량) ÷ (x의 증가량)",
         [L("x의 증가량 = 3 − 1 = 2", memo="오른쪽으로 2"),
          L("y의 증가량 = 8 − 2 = 6", memo="위로 6"),
          L("기울기 = {6/2} = 3", memo="x가 1 늘 때 y는 3씩")],
         "3", f.out(), at=("b2", -1))

    # ── 19 일차함수의 식 구하기 ─────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 5), (-1, 9), box=(60, 50, 620, 640))
    P.axes(at="q", grid=1, lab_step=1)
    P.pt(1, 3, at="q", f="teal", r=10, label="(1, 3)", pos="se", z=24, c="teal")
    P.pt(3, 7, at="q", f="coral", r=10, label="(3, 7)", pos="nw", z=24, c="coral")
    slope_tri(P, 1, 3, 2, 4, at=0, z=26)
    f.text(P.X(4.1), P.Y(4.2), "{4/2} = 2", z=30, c="gold", at=0, dl=1300, b=800)
    g = P.lineq(2, 0, at=1, c="soft", w=3.5, d=True)
    g2 = P.lineq(2, 0, at=1, c="sky", w=4.5)
    slide(g2, 1, dy=P.Y(1) - P.Y(0), dl=700)
    f.text(P.X(-0.4), P.Y(-0.6), "y = 2x", z=22, c="soft", at=1, dl=300, b=800)
    P.pt(0, 1, at=2, f="gold", r=12, label="y절편 1", pos="w", z=26, c="gold")
    f.text(P.X(1.2), P.Y(7.8), "y = 2x + 1", z=28, c="sky", at=2, dl=400, b=800)
    U.ex("m2-1-19", "두 점 (1, 3), (3, 7)을 지나는 직선의 식을 구해 보자.", "기울기부터 → y = ax + b에 한 점을 대입해 b 찾기",
         [L("기울기 = {7 − 3/3 − 1} = 2", memo="두 점 사이의 증가량"),
          L("3 = 2 × 1 + b → b = 1", memo="y = 2x + b에 (1, 3) 대입 — 기울기 2인 직선을 올려 맞춘다"),
          L("y = 2x + 1")],
         "y = 2x + 1", f.out(), at=("b4", 2))

    # ── 20 일차함수의 활용 — 양초 ───────────────────────────
    f = Fig()
    seg_h = 56
    for k in range(6):                        # 위에서부터 5 cm 씩
        top = 196 + seg_h * k
        un = 1 if k < 2 else 2                # 20분 뒤 위의 두 마디(10 cm), 60분 뒤 나머지
        f.rect(70, top, 60, seg_h, at="q", c="ink", sw=2.5, f="yellow", fo=0.35, un=un)
    f.text(100, 570, "30 cm", z=22, c="soft", at="q", b=700)
    fl = f.poly([(100, 150), (88, 178), (100, 192), (112, 178)], at="q", c="coral", w=2.5, f="coral", fo=0.7)
    fl["un"] = 2
    slide(fl, 1, dy=2 * seg_h, dl=200)
    f.line(60, 532, 140, 532, at=2, c="soft", w=4, dl=300)
    f.text(100, 520, "다 탔다", z=22, c="soft", at=2, dl=600, b=800)
    P = Plane(f, (0, 70), (0, 34), box=(200, 100, 630, 560), square=False)
    f.line(P.X(0), P.Y(0), P.X(70), P.Y(0), at="q", c="ink", w=3, ar=1)
    f.line(P.X(0), P.Y(0), P.X(0), P.Y(34), at="q", c="ink", w=3, ar=1)
    for v in (20, 40, 60):
        f.text(P.X(v), P.Y(0) + 28, str(v), z=20, c="soft", at="q")
    for v in (10, 20, 30):
        f.text(P.X(0) - 8, P.Y(v) + 7, str(v), z=20, c="soft", at="q", a="e")
    f.text(P.X(70) - 6, P.Y(0) + 60, "(분)", z=20, c="soft", at="q")
    f.text(P.X(0) + 34, P.Y(34) + 10, "(cm)", z=20, c="soft", at="q")
    f.line(*P.P(0, 30), *P.P(60, 0), at=0, c="sky", w=4.5, dr=True)
    f.text(*P.P(45, 16), "y = 30 − 0.5x", z=24, c="sky", at=0, dl=800, b=800)
    d = f.dot(*P.P(0, 30), r=11, f="coral", at=0, dl=300)
    slide(d, 1, dx=P.X(20) - P.X(0), dy=P.Y(20) - P.Y(30), dl=200)
    f.line(*P.P(20, 0), *P.P(20, 20), at=1, c="coral", w=2.5, d=True, dl=1100)
    f.line(*P.P(0, 20), *P.P(20, 20), at=1, c="coral", w=2.5, d=True, dl=1100)
    f.text(P.X(20) + 14, P.Y(20) - 18, "(20, 20)", z=22, c="coral", at=1, dl=1300, b=800, a="s")
    d2 = f.dot(*P.P(20, 20), r=11, f="gold", at=2)
    slide(d2, 2, dx=P.X(60) - P.X(20), dy=P.Y(0) - P.Y(20), dl=200)
    f.text(P.X(60), P.Y(0) - 26, "60분", z=24, c="gold", at=2, dl=1200, b=800)
    U.ex("m2-1-20", "길이 30 cm인 양초가 1분에 0.5 cm씩 탄다. x분 후 남은 길이를 y cm라 할 때, 20분 후의 길이와 다 타는 시각을 구해 보자.", "y = (처음 양) + (변화율) × x — 줄어드니까 변화율은 음수",
         [L("y = 30 − 0.5x", memo="처음 30 cm, 1분에 0.5 cm씩 줄어든다"),
          L("x = 20 → y = 30 − 0.5 × 20 = 20", memo="20분 후 20 cm"),
          L("y = 0 → 0.5x = 30 → x = 60", memo="다 타는 순간 = x절편")],
         "20 cm, 60분", f.out(), at=("b3", 1))

    # ── 21 일차함수와 일차방정식 ─────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 4), (-1, 8), box=(60, 50, 620, 640))
    P.axes(at="q", grid=1, lab_step=1)
    P.lineq(-3, 6, at=0, c="sky", w=5)
    f.text(P.X(2.7), P.Y(1.2), "3x + y − 6 = 0", z=26, c="sky", at=0, dl=800, b=800)
    P.pt(1, 3, at=1, f="teal", r=12, dl=100)
    f.text(P.X(1) + 22, P.Y(3) - 14, "(1, 3) 참", z=28, c="teal", at=1, dl=600, b=800, a="s")
    P.pt(2, 1, at=2, f="coral", r=12, dl=100)
    f.text(P.X(2) + 22, P.Y(1) + 8, "(2, 1) 거짓", z=28, c="coral", at=2, dl=600, b=800, a="s")
    f.line(*P.P(2, 1), *P.P(2, 0), at=2, c="coral", w=2.5, d=True, dl=900)
    U.ex("m2-1-21", "점 (1, 3)과 (2, 1)이 직선 3x + y − 6 = 0 위에 있는지 알아보자.", "직선 위에 있다 ⇔ 좌표를 대입하면 참",
         [L("3x + y − 6 = 0 → y = −3x + 6", memo="기울기 −3, y절편 6인 직선"),
          L("(1, 3): 3 × 1 + 3 − 6 = 0", memo="참 → 직선 위의 점"),
          L("(2, 1): 3 × 2 + 1 − 6 = 1 ≠ 0", memo="거짓 → 직선 위에 없다")],
         "(1, 3)만 직선 위에 있다", f.out(), at=("b3", 1))

    # ── 22 직선 x = p, y = q ─────────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 5), (-1, 6), box=(60, 60, 620, 640))
    P.axes(at="q", grid=1, lab_step=1)
    v = f.line(*P.P(0, -1), *P.P(0, 6), at=0, c="teal", w=5)
    slide(v, 0, dx=P.X(2) - P.X(0), dl=300)
    f.text(P.X(2) + 14, P.Y(5.6), "x = 2", z=30, c="teal", at=0, dl=1200, b=800, a="s")
    h = f.line(*P.P(-1, 0), *P.P(5, 0), at=1, c="coral", w=5)
    slide(h, 1, dy=P.Y(4) - P.Y(0), dl=300)
    f.text(P.X(4.2), P.Y(4) - 16, "y = 4", z=30, c="coral", at=1, dl=1200, b=800)
    P.pt(2, 4, at=2, f="gold", r=13, label="(2, 4)", pos="ne", z=30, c="gold")
    U.ex("m2-1-22", "두 직선 x = 2와 y = 4를 그리고 만나는 점을 구해 보자.", "x = p는 세로 직선, y = q는 가로 직선",
         [L("x = 2", memo="x좌표가 2인 점 전부 — y축에 평행"),
          L("y = 4", memo="y좌표가 4인 점 전부 — x축에 평행"),
          L("만나는 점 (2, 4)", memo="세로줄과 가로줄이 만나는 칸")],
         "(2, 4)", f.out(), at=("b4", 1))

    # ── 23 그래프와 연립방정식 ───────────────────────────────
    f = Fig()
    P = Plane(f, (-1, 6), (-1, 7), box=(60, 60, 620, 640))
    P.axes(at="q", grid=1, lab_step=1)
    P.lineq(1, 1, at=0, c="teal", w=4.5)
    P.lineq(-1, 5, at=0, c="coral", w=4.5)
    f.text(P.X(4.6), P.Y(6.3), "y = x + 1", z=24, c="teal", at=0, dl=800, b=800)
    f.text(P.X(4.9), P.Y(0.9) - 20, "y = −x + 5", z=24, c="coral", at=0, dl=1000, b=800)
    a_ = f.dot(*P.P(0, 1), r=11, f="teal", at=1)
    slide(a_, 1, dx=P.X(2) - P.X(0), dy=P.Y(3) - P.Y(1), dl=200)
    b_ = f.dot(*P.P(0, 5), r=11, f="coral", at=1)
    slide(b_, 1, dx=P.X(2) - P.X(0), dy=P.Y(3) - P.Y(5), dl=200)
    f.line(*P.P(2, 0), *P.P(2, 3), at=1, c="gold", w=2.5, d=True, dl=1100)
    P.pt(2, 3, at=2, f="gold", r=13, label="(2, 3)", pos="e", z=30, c="gold")
    U.ex("m2-1-23", "두 일차함수 y = x + 1, y = −x + 5의 그래프의 교점을 구해 보자.", "연립방정식의 해 = 두 직선이 함께 지나는 점(교점)",
         [L("y = x + 1, y = −x + 5", memo="두 직선을 그린다"),
          L("x + 1 = −x + 5 → 2x = 4 → x = 2", memo="y가 같아지는 x"),
          L("y = 2 + 1 = 3", memo="x = 2를 대입")],
         "교점 (2, 3)", f.out(), at=("b2", 2), sub={"x": 2, "y": 3})
