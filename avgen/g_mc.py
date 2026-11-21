# 중등 ③ — 일차함수 · 이등변삼각형과 외심 · 내심 · 사각형의 성질 · 닮음 · 피타고라스 정리 · 경우의 수 · 확률
import math
from math import gcd, comb, factorial
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, Plane, ang_pt, angle_mark, dir_deg, NL
from kit import *

def bat(x):
    from core import _has_batchim
    return _has_batchim(str(x))

def F_(n, d):
    return "{%d/%d}" % (n, d)

def FR(v):
    """분수 값 → 기약분수 글자({3/4}, 정수는 그대로)"""
    v = Fr(v)
    if v.denominator == 1:
        return N(v)
    return (MI if v < 0 else "") + F_(abs(v.numerator), v.denominator)

def P_(x, y):
    return f"({N(x)}, {N(y)})"

def line_eq(m, b):
    m, b = Fr(m), Fr(b)
    if m == 0:
        return f"y = {FR(b)}"
    mm = "" if m == 1 else (MI if m == -1 else FR(m))
    s = f"y = {mm}x"
    if b > 0:
        s += f" + {FR(b)}"
    elif b < 0:
        s += f" {MI} {FR(-b)}"
    return s

def plane(f, lim=6, at="q"):
    pl = Plane(f, (-lim - 0.5, lim + 0.5), (-lim - 0.5, lim + 0.5), box=(40, 30, 620, 650))
    pl.axes(at=at, lab_step=2)
    return pl


# ══════════ 일차함수 ══════════
def lin():
    S = Set("lin", "일차함수 — 기울기 · 절편 · 식 세우기", "일차함수",
            {1: "기울기", 2: "x절편과 y절편", 3: "기울기와 한 점으로 식", 4: "두 점으로 식", 5: "평행 · 절편으로 식"},
            mixed=True, pp=8,
            tips={1: "기울기 = {(y의 값의 증가량)/(x의 값의 증가량)} — 두 점이면 {y_{2} − y_{1}/x_{2} − x_{1}}",
                  2: "x절편: y = 0일 때의 x · y절편: x = 0일 때의 y(= 식의 상수항)",
                  3: "y = ax + b에 기울기 a를 넣고, 지나는 점을 대입해 b를 구해요",
                  4: "두 점으로 기울기를 먼저 구한 뒤, 한 점을 대입해 b",
                  5: "평행하면 기울기가 같아요. x절편 p, y절편 q → 기울기 {−q/p}"},
            note="일차함수는 ‘기울기 = 증가량의 비’ 하나만 정확히 잡으면 식 세우기는 모두 같은 과정(기울기 → 한 점 대입)이에요. 그래프 위에 증가량 화살표를 직접 그려 보게 해 주세요.")
    R = rng(1401)

    def pick_line(lim=6):
        for _ in range(200):
            m = Fr(R.choice([-3, -2, -1, 1, 2, 3]), R.choice([1, 1, 1, 2, 3]))
            b = R.randint(-5, 5)
            xs = [x for x in range(-lim, lim + 1) if (m * x + b).denominator == 1 and abs(m * x + b) <= lim]
            if len(xs) >= 2:
                return m, b, xs
        return None

    def g1():
        t = pick_line()
        if not t:
            return
        m, b, xs = t
        x1, x2 = sorted(R.sample(xs, 2))
        y1, y2 = m * x1 + b, m * x2 + b
        f = Fig()
        pl = plane(f)
        pl.lineq(float(m), b)
        pl.pt(x1, y1, label=P_(x1, y1), pos="nw" if m > 0 else "sw")
        pl.pt(x2, y2, label=P_(x2, y2), pos="se" if m > 0 else "ne")
        f.line(*pl.P(x1, y1), *pl.P(x2, y1), c="teal", w=3, ar=1, at=0)
        f.line(*pl.P(x2, y1), *pl.P(x2, y2), c="coral", w=3, ar=1, at=0, dl=300)
        q = f"두 점 {P_(x1, y1)}, {P_(x2, y2)}를 지나는 직선의 기울기를 구하세요." if not bat(N(y2)) else f"두 점 {P_(x1, y1)}, {P_(x2, y2)}을 지나는 직선의 기울기를 구하세요."
        dy = f"{N(y2)} − {NP(y1)}"
        dx = f"{N(x2)} − {NP(x1)}"
        lines = [L(f"{{{dy}/{dx}}} = {FR(m)}", memo="y의 증가량 ÷ x의 증가량")]
        lines.insert(0, L(f"x: {N(x1)} → {N(x2)}, y: {N(y1)} → {N(y2)}", memo="두 점 사이의 증가량"))
        S.add(1, q, FR(m), "기울기 = (y의 증가량) ÷ (x의 증가량)", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        m = Fr(R.choice([-3, -2, -1, 1, 2, 3, 4]), R.choice([1, 1, 2]))
        b = R.randint(-6, 6)
        if b == 0:
            return
        p = -Fr(b) / m
        if p.denominator != 1 or abs(p) > 6:
            return
        f = Fig()
        pl = plane(f)
        pl.lineq(float(m), b)
        pl.pt(float(p), 0, label=f"({N(p)}, 0)", pos="se", at=0, f="coral")
        pl.pt(0, b, label=f"(0, {N(b)})", pos="ne", at=1, f="teal")
        q = f"일차함수 {line_eq(m, b)}의 그래프의 x절편과 y절편을 구하세요."
        lines = [L(f"0 = {FR(m) if m not in (1, -1) else ('' if m == 1 else MI)}x {'+' if b > 0 else MI} {abs(b)}", pre="y = 0", memo="x절편: x축과 만나는 점"), L(f"x = {N(p)}", pre="x절편"), L(f"{N(b)}", pre="y절편", memo="x = 0 → 상수항")]
        S.add(2, q, f"x절편 {N(p)}, y절편 {N(b)}", "x절편은 y = 0, y절편은 x = 0을 대입", lines, f.out(), ap=f"{N(p)}, {N(b)}", omr="ex", sub={"x": p}, key=q)
    fill(S, 2, 20, g2)

    def g3():
        t = pick_line()
        if not t:
            return
        m, b, xs = t
        x0 = R.choice(xs)
        y0 = m * x0 + b
        q = f"기울기가 {FR(m)}이고 점 {P_(x0, y0)}을 지나는 직선을 그래프로 하는 일차함수의 식을 구하세요." if bat(N(y0)) else f"기울기가 {FR(m)}이고 점 {P_(x0, y0)}를 지나는 직선을 그래프로 하는 일차함수의 식을 구하세요."
        mm = FR(m) if m not in (1, -1) else ("" if m == 1 else MI)
        lines = [L(f"y = {mm}x + b로 놓아요", memo="기울기를 먼저"), L(f"{N(y0)} = {FR(m)} × {NP(x0)} + b", memo="지나는 점 대입"), L(f"b = {N(b)}"), L(line_eq(m, b))]
        f = Fig()
        pl = plane(f)
        pl.pt(x0, y0, label=P_(x0, y0), pos="ne")
        pl.lineq(float(m), b, at=3)
        S.add(3, q, line_eq(m, b), "y = ax + b에 기울기 → 한 점 대입으로 b", lines, f.out(), omr="ex", sub={"b": b}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        t = pick_line()
        if not t:
            return
        m, b, xs = t
        x1, x2 = sorted(R.sample(xs, 2))
        y1, y2 = m * x1 + b, m * x2 + b
        q = f"두 점 {P_(x1, y1)}, {P_(x2, y2)}를 지나는 직선을 그래프로 하는 일차함수의 식을 구하세요." if not bat(N(y2)) else f"두 점 {P_(x1, y1)}, {P_(x2, y2)}을 지나는 직선을 그래프로 하는 일차함수의 식을 구하세요."
        lines = [L(f"{{{N(y2)} − {NP(y1)}/{N(x2)} − {NP(x1)}}} = {FR(m)}", pre="기울기"), L(f"{N(y1)} = {FR(m)} × {NP(x1)} + b", memo="한 점 대입"), L(f"b = {N(b)}"), L(line_eq(m, b))]
        f = Fig()
        pl = plane(f)
        pl.pt(x1, y1, label=P_(x1, y1), pos="nw")
        pl.pt(x2, y2, label=P_(x2, y2), pos="se")
        pl.lineq(float(m), b, at=3)
        S.add(4, q, line_eq(m, b), "두 점으로 기울기 → 한 점 대입", lines, f.out(), omr="ex", sub={"b": b}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        f = Fig()
        pl = plane(f)
        if k == 0:
            t = pick_line()
            if not t:
                return
            m, b, xs = t
            b2 = R.randint(-5, 5)
            if b2 == b:
                return
            x0 = R.choice([x for x in range(-5, 6) if (m * x + b).denominator == 1 and abs(m * x + b) <= 6] or [0])
            y0 = m * x0 + b
            q = f"일차함수 {line_eq(m, b2)}의 그래프와 평행하고 점 {P_(x0, y0)}{'을' if bat(N(y0)) else '를'} 지나는 직선의 식을 구하세요."
            pl.lineq(float(m), b2, c="soft", d=True)
            pl.pt(x0, y0, label=P_(x0, y0), pos="ne")
            pl.lineq(float(m), b, at=2)
            lines = [L(f"평행 → 기울기 {FR(m)}", memo="기울기가 같고 y절편이 달라요"), L(f"{N(y0)} = {FR(m)} × {NP(x0)} + b → b = {N(b)}"), L(line_eq(m, b))]
            S.add(5, q, line_eq(m, b), "평행하면 기울기가 같아요", lines, f.out(), omr="ex", key=q)
        elif k == 1:
            p, qq = R.choice([-6, -4, -3, -2, 2, 3, 4, 6]), R.choice([-6, -4, -3, -2, 2, 3, 4, 6])
            m = Fr(-qq, p)
            q = f"x절편이 {N(p)}, y절편이 {N(qq)}인 직선을 그래프로 하는 일차함수의 식을 구하세요."
            pl.pt(p, 0, label=f"({N(p)}, 0)", pos="se")
            pl.pt(0, qq, label=f"(0, {N(qq)})", pos="ne")
            pl.lineq(float(m), qq, at=1)
            lines = [L(f"{{{N(qq)} − 0/0 − {NP(p)}}} = {FR(m)}", pre="기울기", memo=f"두 점 ({N(p)}, 0), (0, {N(qq)})"), L(line_eq(m, qq), memo="y절편이 상수항")]
            S.add(5, q, line_eq(m, qq), "두 절편 = 두 점 → 기울기, y절편은 상수항", lines, f.out(), omr="ex", key=q)
        else:
            t = pick_line()
            if not t:
                return
            m, b, xs = t
            x0 = R.choice(xs)
            y0 = m * x0 + b
            a = R.randint(-4, 4)
            if a == 0 or (y0 - a * x0) == b:
                return
            q = f"일차함수 y = ax {'+' if b >= 0 else MI} {abs(b)}의 그래프가 점 {P_(x0, y0)}{'을' if bat(N(y0)) else '를'} 지날 때, 상수 a의 값을 구하세요."
            if x0 == 0:
                return
            pl.pt(x0, y0, label=P_(x0, y0), pos="ne")
            pl.lineq(float(m), b, at=1)
            lines = [L(f"{N(y0)} = a × {NP(x0)} {'+' if b >= 0 else MI} {abs(b)}", memo="지나는 점 대입"), L(f"a = {FR(m)}")]
            S.add(5, q, FR(m), "지나는 점을 대입해 미지의 계수를 구해요", lines, f.out(), sub={"a": m}, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 이등변삼각형 · 외심 · 내심 ══════════
def tri_pts():
    return (330, 110), (110, 540), (550, 540)

def iso():
    S = Set("iso", "이등변삼각형 · 외심 · 내심 — 각의 크기", "외심·내심",
            {1: "이등변삼각형의 밑각", 2: "이등변삼각형이 이어진 그림", 3: "외심과 각", 4: "내심과 각", 5: "외접원 · 내접원의 반지름"},
            mixed=True, pp=8,
            tips={1: "AB = AC면 ∠B = ∠C · 꼭지각의 이등분선은 밑변을 수직이등분해요",
                  2: "이등변삼각형의 밑각과 외각(= 두 밑각의 합)을 이어 가며 같은 각을 찾아요",
                  3: "외심 O: ∠OAB + ∠OBC + ∠OCA = 90° · ∠BOC = 2∠A",
                  4: "내심 I: 반각의 합 90° · ∠BIC = 90° + {1/2}∠A",
                  5: "직각삼각형의 외심은 빗변의 중점 · 넓이 = {1/2} × r × (세 변의 합)"},
            note="외심은 세 변의 수직이등분선(꼭짓점까지 거리가 같음), 내심은 세 각의 이등분선(변까지 거리가 같음)이에요. 이등변삼각형 세 개로 쪼개진 그림을 그려 같은 각에 같은 표시를 하게 해 주세요.")
    R = rng(1402)

    def g1():
        k = S.count(1) % 3
        A, B, C = tri_pts()
        f = Fig()
        f.poly([A, B, C], c="ink", w=3)
        f.text(A[0], A[1] - 18, "A", z=28, b=700); f.text(B[0] - 20, B[1] + 30, "B", z=28, b=700); f.text(C[0] + 20, C[1] + 30, "C", z=28, b=700)
        if k == 0:
            top = R.choice([20, 28, 36, 40, 44, 52, 56, 64, 72, 80, 88, 96, 100, 108, 116, 124])
            base = (180 - top) // 2
            angle_mark(f, A, B, C, label=f"{top}°")
            angle_mark(f, B, C, A, label="x", c="coral", f_="coral", at=0)
            q = f"AB = AC인 이등변삼각형 ABC에서 ∠A = {top}°일 때, ∠B의 크기를 구하세요."
            lines = [L(f"∠B = ∠C", memo="이등변삼각형의 두 밑각"), L(f"(180 − {top}) ÷ 2 = {base}"), L(f"{base}°")]
            ans, ap = f"{base}°", str(base)
        elif k == 1:
            x = R.randint(10, 35)
            a, c = R.randint(2, 3), R.randint(0, 20)
            top = 180 - 2 * (a * x + c)
            if not 10 <= top <= 140:
                return
            angle_mark(f, B, C, A, label=f"({a}x + {c})°" if c else f"{a}x°")
            angle_mark(f, A, B, C, label=f"{top}°", c="teal", f_="teal")
            q = f"AB = AC인 이등변삼각형 ABC에서 ∠A = {top}°, ∠B = ({a}x + {c})°일 때, x의 값을 구하세요." if c else f"AB = AC인 이등변삼각형 ABC에서 ∠A = {top}°, ∠B = {a}x°일 때, x의 값을 구하세요."
            lines = [L(f"{top} + 2({a}x + {c}) = 180" if c else f"{top} + 2 × {a}x = 180", memo="∠B = ∠C"), L(f"{2 * a}x = {180 - top - 2 * c}"), L(f"x = {x}")]
            S.add(1, q, str(x), "두 밑각이 같으니 세 각의 합으로 식", lines, f.out(), sub={"x": x}, key=q)
            return
        else:
            bc = R.randint(3, 12) * 2
            D = ((B[0] + C[0]) / 2, B[1])
            f.line(*A, *D, c="teal", w=3, d=True, at=0)
            angle_mark(f, D, C, A, r=26, at=0)
            q = f"AB = AC인 이등변삼각형 ABC에서 꼭지각 A의 이등분선이 밑변 BC와 만나는 점을 D라 해요. BC = {bc} cm일 때, BD의 길이와 ∠ADB의 크기를 구하세요."
            lines = [L("꼭지각의 이등분선은 밑변을 수직이등분", memo="이등변삼각형"), L(f"BD = {bc} ÷ 2 = {bc // 2}"), L("∠ADB = 90°")]
            S.add(1, q, f"BD = {bc // 2} cm, ∠ADB = 90°", "꼭지각의 이등분선 = 밑변의 수직이등분선", lines, f.out(), ap=f"{bc // 2}, 90", omr="ex", key=q)
            return
        S.add(1, q, ans, "이등변삼각형의 두 밑각은 같아요", lines, f.out(), ap=ap, key=q)
    fill(S, 1, 20, g1)

    def g2():
        x = R.choice([20, 22, 24, 25, 26, 28, 30, 32, 34, 35, 36])
        f = Fig()
        B, C = (90, 520), (300, 520)
        D = (560, 520)
        A = (195, 520 - 105 * math.tan(math.radians(x)) * 1.0)
        f.line(*B, *D, c="ink", w=3)
        f.poly([B, A, C], c="ink", w=3, z=False)
        f.line(*A, *C, c="ink", w=3)
        angle_mark(f, B, C, A, r=50, label=f"{x}°")
        angle_mark(f, C, D, A, r=50, label="?", c="coral", f_="coral", at=1)
        k = S.count(2) % 2
        if k == 0:
            q = f"삼각형 ABC에서 AC = BC이고 ∠B = {x}°예요. 변 BC의 연장선 위의 점 D에 대하여 ∠ACD의 크기를 구하세요."
            lines = [L(f"∠BAC = ∠B = {x}°", memo="CA = CB → 이등변삼각형"), L(f"∠ACD = {x} + {x} = {2 * x}", memo="외각 = 이웃하지 않는 두 내각의 합"), L(f"{2 * x}°")]
            ans, ap = f"{2 * x}°", str(2 * x)
        else:
            q = f"삼각형 ABC에서 AC = BC이고, 변 BC의 연장선 위의 점 D에 대하여 ∠ACD = {2 * x}°예요. ∠B의 크기를 구하세요."
            lines = [L("∠B = ∠BAC", memo="CA = CB"), L(f"2∠B = {2 * x}", memo="외각 = 두 내각의 합"), L(f"∠B = {x}°")]
            ans, ap = f"{x}°", str(x)
        S.add(2, q, ans, "이등변삼각형의 밑각 → 외각으로 이어 가요", lines, f.out(), ap=ap, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        A, B, C = (300, 120), (100, 520), (560, 520)
        f = Fig()
        f.poly([A, B, C], c="ink", w=3)
        # 외심(실제 계산)
        ax, ay = A; bx, by = B; cx, cy = C
        d = 2 * (ax * (by - cy) + bx * (cy - ay) + cx * (ay - by))
        ux = ((ax ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay) + (cx ** 2 + cy ** 2) * (ay - by)) / d
        uy = ((ax ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax - cx) + (cx ** 2 + cy ** 2) * (bx - ax)) / d
        O = (ux, uy)
        for P in (A, B, C):
            f.line(*O, *P, c="teal", w=2.5, d=True, at="q")
        f.dot(*O, r=7, f="teal")
        f.text(O[0] + 18, O[1] + 8, "O", z=26, c="teal", b=700)
        for nm_, P, dx, dy in (("A", A, 0, -18), ("B", B, -20, 30), ("C", C, 20, 30)):
            f.text(P[0] + dx, P[1] + dy, nm_, z=28, b=700)
        if k == 0:
            x, y = R.randint(10, 40), R.randint(10, 40)
            z = 90 - x - y
            if z <= 5:
                return
            q = f"점 O가 삼각형 ABC의 외심이고 ∠OAB = {x}°, ∠OBC = {y}°일 때, ∠OCA의 크기를 구하세요."
            lines = [L(f"{x} + {y} + ∠OCA = 90", memo="외심 — 세 이등변삼각형의 밑각의 합"), L(f"∠OCA = 90 − {x} − {y} = {z}"), L(f"{z}°")]
            ans, ap = f"{z}°", str(z)
        elif k == 1:
            a = R.randint(30, 85)
            q = f"점 O가 삼각형 ABC의 외심이고 ∠A = {a}°일 때, ∠BOC의 크기를 구하세요."
            lines = [L("∠BOC = 2∠A", memo="중심각은 원주각의 2배"), L(f"2 × {a} = {2 * a}"), L(f"{2 * a}°")]
            ans, ap = f"{2 * a}°", str(2 * a)
            angle_mark(f, O, B, C, r=36, label="?", c="coral", f_="coral", at=1)
        else:
            boc = R.randint(30, 80) * 2
            q = f"점 O가 삼각형 ABC의 외심이고 ∠BOC = {boc}°일 때, ∠A의 크기를 구하세요."
            lines = [L(f"∠A = {{1/2}}∠BOC", memo="∠BOC = 2∠A"), L(f"{boc} ÷ 2 = {boc // 2}"), L(f"{boc // 2}°")]
            ans, ap = f"{boc // 2}°", str(boc // 2)
        S.add(3, q, ans, "외심 — 세 꼭짓점까지 거리가 같아 이등변삼각형 세 개", lines, f.out(), ap=ap, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        A, B, C = (300, 120), (100, 520), (560, 520)
        a_, b_, c_ = math.dist(B, C), math.dist(A, C), math.dist(A, B)
        I = ((a_ * A[0] + b_ * B[0] + c_ * C[0]) / (a_ + b_ + c_), (a_ * A[1] + b_ * B[1] + c_ * C[1]) / (a_ + b_ + c_))
        f = Fig()
        f.poly([A, B, C], c="ink", w=3)
        for P in (A, B, C):
            f.line(*I, *P, c="teal", w=2.5, d=True)
        f.dot(*I, r=7, f="teal")
        f.text(I[0] + 18, I[1] - 10, "I", z=26, c="teal", b=700)
        for nm_, P, dx, dy in (("A", A, 0, -18), ("B", B, -20, 30), ("C", C, 20, 30)):
            f.text(P[0] + dx, P[1] + dy, nm_, z=28, b=700)
        if k == 0:
            a = R.randint(20, 100)
            if a % 2:
                return
            v = 90 + a // 2
            angle_mark(f, I, B, C, r=34, label="?", c="coral", f_="coral", at=1)
            q = f"점 I가 삼각형 ABC의 내심이고 ∠A = {a}°일 때, ∠BIC의 크기를 구하세요."
            lines = [L("∠BIC = 90° + {1/2}∠A", memo="내심의 성질"), L(f"90 + {a} ÷ 2 = {v}"), L(f"{v}°")]
            ans, ap = f"{v}°", str(v)
        elif k == 1:
            x, y = R.randint(10, 40), R.randint(10, 40)
            z = 90 - x - y
            if z <= 5:
                return
            q = f"점 I가 삼각형 ABC의 내심이고 ∠IAB = {x}°, ∠IBC = {y}°일 때, ∠ICA의 크기를 구하세요."
            lines = [L(f"{x} + {y} + ∠ICA = 90", memo="세 반각의 합 = 180° ÷ 2"), L(f"∠ICA = 90 − {x} − {y} = {z}"), L(f"{z}°")]
            ans, ap = f"{z}°", str(z)
        else:
            bic = R.randint(100, 150)
            a = 2 * (bic - 90)
            q = f"점 I가 삼각형 ABC의 내심이고 ∠BIC = {bic}°일 때, ∠A의 크기를 구하세요."
            lines = [L(f"90 + {{1/2}}∠A = {bic}", memo="∠BIC = 90° + {1/2}∠A"), L(f"{{1/2}}∠A = {bic - 90}"), L(f"∠A = {a}°")]
            ans, ap = f"{a}°", str(a)
        S.add(4, q, ans, "내심 — 세 각의 이등분선", lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        trip = R.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29)])
        m = R.randint(1, 4 if trip[2] <= 13 else 2)
        a, b, c = (t * m for t in trip)
        f = Fig()
        P = [(120, 520), (120 + 420 * 1, 520), (120, 520 - 420 * a / b)]
        sc = min(420 / b, 400 / a)
        A, B, C = (120, 520 - sc * a), (120, 520), (120 + sc * b, 520)
        f.poly([A, B, C], c="ink", w=3)
        angle_mark(f, B, C, A, r=30)
        f.text(B[0] - 22, (A[1] + B[1]) / 2, f"{a}", z=28, b=700, a="e")
        f.text((B[0] + C[0]) / 2, B[1] + 38, f"{b}", z=28, b=700)
        f.text((A[0] + C[0]) / 2 + 20, (A[1] + C[1]) / 2 - 14, f"{c}", z=28, b=700, a="s")
        if k == 0:
            M = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
            f.circ(*M, sc * c / 2, c="teal", sw=2.5, d=True, at=0)
            f.dot(*M, r=7, f="teal", at=0)
            q = f"세 변의 길이가 {a} cm, {b} cm, {c} cm인 직각삼각형의 외접원의 반지름의 길이를 구하세요."
            R_ = Fr(c, 2)
            lines = [L("직각삼각형의 외심 = 빗변의 중점", memo="빗변이 외접원의 지름"), L(f"{c} ÷ 2 = {N(R_) if R_.denominator == 1 else DEC(R_)}"), L(f"{N(R_) if R_.denominator == 1 else DEC(R_)} cm")]
            ans = f"{N(R_) if R_.denominator == 1 else DEC(R_)} cm"
            ap = N(R_) if R_.denominator == 1 else DEC(R_)
        else:
            area = Fr(a * b, 2)
            r = area * 2 / (a + b + c)
            if r.denominator != 1:
                return
            r = int(r)
            Ic = (B[0] + sc * r, B[1] - sc * r)
            f.circ(*Ic, sc * r, c="teal", sw=2.5, d=True, at=1)
            q = f"세 변의 길이가 {a} cm, {b} cm, {c} cm인 직각삼각형의 내접원의 반지름의 길이를 구하세요."
            lines = [L(f"{{1/2}} × {a} × {b} = {N(area)}", pre="넓이"), L(f"{{1/2}} × r × ({a} + {b} + {c}) = {N(area)}", memo="넓이 = {1/2} × r × 둘레"), L(f"r = {r}")]
            ans, ap = f"{r} cm", str(r)
            S.add(5, q, ans, "넓이 = {1/2} × r × (세 변의 합)", lines, f.out(), ap=ap, sub={"r": r}, key=q)
            return
        S.add(5, q, ans, "직각삼각형의 외심은 빗변의 중점", lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 사각형의 성질 ══════════
def pg_pts(slant=110):
    A, B = (110 + slant, 160), (550 + slant * 0, 160)
    return (110 + slant, 160), (110, 500), (550, 500), (550 + slant, 160)

def quad():
    S = Set("quad", "평행사변형과 여러 사각형", "사각형의 성질",
            {1: "평행사변형의 변과 대각선", 2: "평행사변형의 각", 3: "평행사변형과 넓이", 4: "직사각형 · 마름모 · 정사각형", 5: "사다리꼴과 넓이가 같은 삼각형"},
            mixed=True, pp=8,
            tips={1: "두 쌍의 대변의 길이가 같고, 두 대각선은 서로를 이등분해요",
                  2: "두 쌍의 대각의 크기가 같고, 이웃한 두 각의 합은 180°",
                  3: "내부의 한 점 P: △PAB + △PCD = △PDA + △PBC = {1/2}□ABCD",
                  4: "직사각형: 대각선 길이가 같음 · 마름모: 대각선이 수직 · 정사각형: 둘 다",
                  5: "밑변이 같고 높이가 같은 두 삼각형은 넓이가 같아요(평행선 사이)"},
            note="여러 사각형의 성질은 ‘평행사변형 + 조건 하나’로 정리하게 해 주세요. 직사각형은 각, 마름모는 변, 정사각형은 둘 다가 더해진 평행사변형이에요.")
    R = rng(1403)

    def base_fig(f, labels=True):
        A, B, C, D = pg_pts()
        f.poly([A, B, C, D], c="ink", w=3)
        if labels:
            for nm_, P, dx, dy in (("A", A, -16, -16), ("B", B, -22, 30), ("C", C, 20, 30), ("D", D, 18, -16)):
                f.text(P[0] + dx, P[1] + dy, nm_, z=28, b=700)
        return A, B, C, D

    def g1():
        k = S.count(1) % 2
        f = Fig()
        A, B, C, D = base_fig(f)
        if k == 0:
            x = R.randint(2, 9); y = R.randint(2, 9)
            a, b = R.randint(2, 4), R.randint(1, 9)
            c, d = R.randint(1, 3), R.randint(10, 30)
            if a == c:
                return
            dd = (a - c) * x + b
            if dd <= 0:
                return
            q = f"평행사변형 ABCD에서 AD = ({a}x + {b}) cm, BC = ({c}x + {dd}) cm일 때, x의 값을 구하세요."
            lines = [L(f"{a}x + {b} = {c}x + {dd}", memo="평행사변형의 대변의 길이는 같아요"), L(f"{a - c}x = {dd - b}" if a - c != 1 else f"x = {dd - b}"), L(f"x = {x}")]
            if a - c == 1:
                lines = lines[:2]
            S.add(1, q, str(x), "대변의 길이가 같다고 놓아요", lines, f.out(), sub={"x": x}, key=q)
        else:
            O = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
            f.line(*A, *C, c="teal", w=2.5, d=True)
            f.line(*B, *D, c="teal", w=2.5, d=True)
            f.dot(*O, r=6, f="teal")
            ac, bd = R.randint(5, 15) * 2, R.randint(5, 15) * 2
            q = f"평행사변형 ABCD에서 두 대각선의 교점을 O라 할 때, AC = {ac} cm, BD = {bd} cm이면 OA + OB는 몇 cm인가요?"
            lines = [L("대각선은 서로를 이등분", memo="OA = {1/2}AC, OB = {1/2}BD"), L(f"{ac} ÷ 2 + {bd} ÷ 2 = {(ac + bd) // 2}"), L(f"{(ac + bd) // 2} cm")]
            S.add(1, q, f"{(ac + bd) // 2} cm", "대각선은 서로를 이등분해요", lines, f.out(), ap=str((ac + bd) // 2), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        f = Fig()
        A, B, C, D = base_fig(f)
        if k == 0:
            p, q_ = R.sample(range(1, 8), 2)
            if gcd(p, q_) != 1 or 180 * p % (p + q_):
                return
            a = 180 * p // (p + q_)
            q = f"평행사변형 ABCD에서 ∠A : ∠B = {p} : {q_}일 때, ∠A의 크기를 구하세요."
            lines = [L("∠A + ∠B = 180°", memo="이웃한 두 각"), L(f"180 × {{{p}/{p + q_}}} = {a}"), L(f"{a}°")]
            ans, ap = f"{a}°", str(a)
        elif k == 1:
            a = R.randint(50, 130)
            angle_mark(f, B, C, A, r=44, label=f"{a}°")
            angle_mark(f, D, A, C, r=44, label="?", c="coral", f_="coral", at=0)
            q = f"평행사변형 ABCD에서 ∠B = {a}°일 때, ∠D의 크기를 구하세요."
            lines = [L("∠D = ∠B", memo="대각의 크기는 같아요"), L(f"{a}°")]
            ans, ap = f"{a}°", str(a)
        else:
            x = R.randint(15, 40)
            a, b = R.randint(2, 3), R.randint(0, 30)
            B_ = a * x + b
            if not 40 <= B_ <= 140:
                return
            c = 180 - B_
            q = f"평행사변형 ABCD에서 ∠A = {c}°, ∠B = ({a}x + {b})°일 때, x의 값을 구하세요." if b else f"평행사변형 ABCD에서 ∠A = {c}°, ∠B = {a}x°일 때, x의 값을 구하세요."
            lines = [L(f"{c} + {a}x + {b} = 180" if b else f"{c} + {a}x = 180", memo="이웃한 두 각의 합 180°"), L(f"{a}x = {180 - c - b}"), L(f"x = {x}")]
            S.add(2, q, str(x), "이웃한 두 각의 합 180°", lines, f.out(), sub={"x": x}, key=q)
            return
        S.add(2, q, ans, "대각은 같고, 이웃한 두 각의 합은 180°", lines, f.out(), ap=ap, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        f = Fig()
        A, B, C, D = base_fig(f)
        P = (R.randint(300, 400), R.randint(280, 380))
        for V in (A, B, C, D):
            f.line(*P, *V, c="teal", w=2, d=True)
        f.dot(*P, r=7, f="coral")
        f.text(P[0] + 16, P[1] - 12, "P", z=26, c="coral", b=700)
        T = R.randint(10, 40) * 4
        a = R.randint(T // 10, T // 2 - 5)
        if k == 0:
            q = f"넓이가 {T} cm²인 평행사변형 ABCD의 내부에 점 P가 있어요. △PAB의 넓이가 {a} cm²일 때, △PCD의 넓이를 구하세요."
            lines = [L(f"△PAB + △PCD = {{1/2}} × {T} = {T // 2}", memo="마주 보는 두 삼각형의 합 = 절반"), L(f"{T // 2} − {a} = {T // 2 - a}"), L(f"{T // 2 - a} cm²")]
            ans, ap = f"{T // 2 - a} cm²", str(T // 2 - a)
        else:
            b = R.randint(T // 10, T // 2 - 5)
            q = f"평행사변형 ABCD의 내부의 한 점 P에 대하여 △PAB = {a} cm², △PCD = {T // 2 - a} cm²일 때, □ABCD의 넓이를 구하세요."
            lines = [L(f"{a} + {T // 2 - a} = {T // 2}", memo="마주 보는 두 삼각형의 합"), L(f"{T // 2} × 2 = {T}", memo="평행사변형 넓이의 절반이었으니"), L(f"{T} cm²")]
            ans, ap = f"{T} cm²", str(T)
        S.add(3, q, ans, "마주 보는 두 삼각형의 넓이의 합 = 평행사변형의 절반", lines, f.out(), ap=ap, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        f = Fig()
        if k == 0:
            A, B, C, D = (130, 160), (130, 500), (530, 500), (530, 160)
            f.poly([A, B, C, D], c="ink", w=3)
            f.line(*A, *C, c="teal", w=2.5, d=True); f.line(*B, *D, c="teal", w=2.5, d=True)
            x = R.randint(2, 9)
            a, b = R.randint(2, 4), R.randint(1, 9)
            AC = a * x + b
            c = R.randint(1, a - 1) if a > 1 else 1
            d = AC - c * x
            if d <= 0:
                return
            q = f"직사각형 ABCD에서 AC = ({a}x + {b}) cm, BD = ({c}x + {d}) cm일 때, x의 값을 구하세요." if c > 1 else f"직사각형 ABCD에서 AC = ({a}x + {b}) cm, BD = (x + {d}) cm일 때, x의 값을 구하세요."
            lines = [L(f"{a}x + {b} = {c}x + {d}" if c > 1 else f"{a}x + {b} = x + {d}", memo="직사각형의 두 대각선은 길이가 같아요"), L(f"{a - c}x = {d - b}"), L(f"x = {x}")]
            S.add(4, q, str(x), "직사각형 — 두 대각선의 길이가 같아요", lines, f.out(), sub={"x": x}, key=q)
            return
        elif k == 1:
            d1, d2 = R.randint(3, 12) * 2, R.randint(3, 12) * 2
            A, B, C, D = (330, 120), (130, 330), (330, 540), (530, 330)
            f.poly([A, B, C, D], c="ink", w=3)
            f.line(*A, *C, c="teal", w=2.5, d=True); f.line(*B, *D, c="teal", w=2.5, d=True)
            angle_mark(f, (330, 330), D, A, r=24)
            q = f"두 대각선의 길이가 {d1} cm, {d2} cm인 마름모의 넓이를 구하세요."
            lines = [L("마름모의 대각선은 수직이등분", memo="네 직각삼각형"), L(f"{d1} × {d2} ÷ 2 = {d1 * d2 // 2}"), L(f"{d1 * d2 // 2} cm²")]
            ans, ap = f"{d1 * d2 // 2} cm²", str(d1 * d2 // 2)
        else:
            d = R.randint(3, 15) * 2
            A, B, C, D = (330, 120), (120, 330), (330, 540), (540, 330)
            f.poly([A, B, C, D], c="ink", w=3)
            f.line(*A, *C, c="teal", w=2.5, d=True); f.line(*B, *D, c="teal", w=2.5, d=True)
            q = f"대각선의 길이가 {d} cm인 정사각형의 넓이를 구하세요."
            lines = [L("정사각형도 마름모 — 대각선은 길이가 같고 수직", memo="넓이 = 대각선 × 대각선 ÷ 2"), L(f"{d} × {d} ÷ 2 = {d * d // 2}"), L(f"{d * d // 2} cm²")]
            ans, ap = f"{d * d // 2} cm²", str(d * d // 2)
        S.add(4, q, ans, "대각선의 성질 — 길이가 같음(직사각형) · 수직(마름모)", lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        f = Fig()
        A, D = (220, 170), (440, 170)
        B, C = (100, 500), (560, 500)
        f.poly([A, B, C, D], c="ink", w=3)
        f.line(*A, *C, c="teal", w=2.5, d=True)
        f.line(*B, *D, c="coral", w=2.5, d=True)
        for nm_, P, dx, dy in (("A", A, -16, -16), ("B", B, -22, 30), ("C", C, 20, 30), ("D", D, 18, -16)):
            f.text(P[0] + dx, P[1] + dy, nm_, z=28, b=700)
        if k == 0:
            a = R.randint(10, 60)
            q = f"AD // BC인 사다리꼴 ABCD에서 △ABC의 넓이가 {a} cm²일 때, △DBC의 넓이를 구하세요."
            lines = [L("밑변 BC가 같아요"), L("AD // BC → 높이가 같아요", memo="평행선 사이의 거리"), L(f"△DBC = △ABC = {a} cm²")]
            ans, ap = f"{a} cm²", str(a)
        else:
            a, o = R.randint(20, 60), R.randint(4, 15)
            if o >= a:
                return
            q = f"AD // BC인 사다리꼴 ABCD에서 두 대각선의 교점을 O라 해요. △ABC = {a} cm², △OBC = {o} cm²일 때, △ABO의 넓이를 구하세요."
            lines = [L(f"△ABO = △ABC − △OBC", memo="△ABC를 둘로 나누기"), L(f"{a} − {o} = {a - o}"), L(f"{a - o} cm²")]
            ans, ap = f"{a - o} cm²", str(a - o)
        S.add(5, q, ans, "평행선 사이에서 밑변이 같으면 넓이가 같아요", lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 닮음 ══════════
def sim():
    S = Set("sim", "닮음 — 닮음비 · 평행선과 선분의 비 · 넓이의 비", "닮음",
            {1: "닮음비와 대응변", 2: "넓이의 비 · 부피의 비", 3: "삼각형과 평행선", 4: "평행선 사이의 선분의 비", 5: "중점연결정리와 무게중심"},
            mixed=True, pp=8,
            tips={1: "대응변의 길이의 비가 닮음비 — 모든 대응변이 같은 비",
                  2: "닮음비가 m : n이면 넓이의 비 m^{2} : n^{2}, 부피의 비 m^{3} : n^{3}",
                  3: "DE // BC면 AD : AB = AE : AC = DE : BC",
                  4: "세 평행선이 두 직선과 만나면 a : b = c : d",
                  5: "두 변의 중점을 이은 선분은 나머지 변과 평행하고 길이는 {1/2} · 무게중심은 중선을 2 : 1로 나눠요"},
            note="닮음은 ‘대응하는 것끼리 짝짓기’가 먼저예요. 비례식을 세우기 전에 대응변에 같은 색을 칠하게 하면 실수가 줄어요.")
    R = rng(1404)

    def g1():
        k = S.count(1) % 2
        m, n = R.sample(range(1, 7), 2)
        if gcd(m, n) != 1:
            return
        t = R.randint(1, 4)
        ab, bc = m * t * R.randint(1, 2), m * R.randint(2, 6)
        de = n * ab // m if (n * ab) % m == 0 else None
        if de is None or (n * bc) % m:
            return
        ef = n * bc // m
        f = Fig()
        s1, s2 = 1.0, n / m
        sc = 300 / max(m, n)
        T1 = [(60, 520), (60 + sc * m * 0.9, 520), (60 + sc * m * 0.3, 520 - sc * m * 0.8)]
        T2 = [(360, 520), (360 + sc * n * 0.9, 520), (360 + sc * n * 0.3, 520 - sc * n * 0.8)]
        f.poly(T1, c="gold", w=3, f="gold", fo=0.15)
        f.poly(T2, c="teal", w=3, f="teal", fo=0.15)
        q = f"△ABC ∽ △DEF이고 AB = {ab} cm, BC = {bc} cm, DE = {de} cm일 때, EF의 길이를 구하세요."
        lines = [L(f"{ab} : {de} = {m} : {n}", pre="닮음비", memo="대응변 AB와 DE"), L(f"{bc} : EF = {m} : {n}", memo="BC와 EF도 같은 비"), L(f"EF = {bc} × {{{n}/{m}}} = {ef}"), L(f"{ef} cm")]
        S.add(1, q, f"{ef} cm", "대응변 한 쌍으로 닮음비 → 나머지 대응변", lines, f.out(), ap=str(ef), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        m, n = R.sample(range(1, 6), 2)
        if gcd(m, n) != 1:
            return
        if k == 0:
            A1 = m * m * R.randint(1, 5)
            A2 = Fr(A1 * n * n, m * m)
            q = f"닮음비가 {m} : {n}인 두 평면도형 P, Q에서 P의 넓이가 {A1} cm²일 때, Q의 넓이를 구하세요."
            lines = [L(f"{m}^{{2}} : {n}^{{2}} = {m * m} : {n * n}", pre="넓이의 비"), L(f"{A1} × {{{n * n}/{m * m}}} = {N(A2)}"), L(f"{N(A2)} cm²")]
            ans, ap = f"{N(A2)} cm²", N(A2)
            if A2.denominator != 1:
                return
        elif k == 1:
            V1 = m ** 3 * R.randint(1, 3)
            V2 = Fr(V1 * n ** 3, m ** 3)
            q = f"닮음비가 {m} : {n}인 두 입체도형 P, Q에서 P의 부피가 {V1} cm³일 때, Q의 부피를 구하세요."
            lines = [L(f"{m}^{{3}} : {n}^{{3}} = {m ** 3} : {n ** 3}", pre="부피의 비"), L(f"{V1} × {{{n ** 3}/{m ** 3}}} = {N(V2)}"), L(f"{N(V2)} cm³")]
            ans, ap = f"{N(V2)} cm³", N(V2)
        else:
            A1, A2 = m * m * R.randint(1, 4), None
            A2 = A1 * n * n // (m * m) if (A1 * n * n) % (m * m) == 0 else None
            if A2 is None:
                return
            q = f"닮은 두 도형의 넓이가 각각 {A1} cm², {A2} cm²일 때, 두 도형의 닮음비를 가장 간단한 자연수의 비로 나타내세요."
            lines = [L(f"{A1} : {A2} = {m * m} : {n * n}", pre="넓이의 비"), L(f"{m}^{{2}} : {n}^{{2}}", memo="넓이의 비 = 닮음비의 제곱"), L(f"닮음비 {m} : {n}")]
            ans, ap = f"{m} : {n}", f"{m}:{n}"
            S.add(2, q, ans, "넓이의 비가 제곱 꼴이면 닮음비는 그 밑의 비", lines, None, ap=ap, omr="ex", key=q)
            return
        S.add(2, q, ans, "넓이는 닮음비의 제곱, 부피는 세제곱", lines, None, ap=ap, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        p, qq = R.randint(1, 5), R.randint(1, 5)
        t = R.randint(1, 4)
        AD, DB = p * t, qq * t
        AB = AD + DB
        bc = (p + qq) * R.randint(1, 4)
        de = Fr(bc * p, p + qq)
        f = Fig()
        A, B, C = (300, 110), (100, 540), (560, 540)
        r_ = p / (p + qq)
        D = (A[0] + (B[0] - A[0]) * r_, A[1] + (B[1] - A[1]) * r_)
        E = (A[0] + (C[0] - A[0]) * r_, A[1] + (C[1] - A[1]) * r_)
        f.poly([A, B, C], c="ink", w=3)
        f.line(*D, *E, c="teal", w=3.5)
        for nm_, P, dx, dy in (("A", A, 0, -18), ("B", B, -20, 30), ("C", C, 20, 30), ("D", D, -24, 6), ("E", E, 24, 6)):
            f.text(P[0] + dx, P[1] + dy, nm_, z=28, b=700)
        if k == 0:
            if de.denominator != 1:
                return
            q = f"△ABC에서 DE // BC이고 AD = {AD} cm, DB = {DB} cm, BC = {bc} cm일 때, DE의 길이를 구하세요."
            lines = [L(f"AD : AB = {AD} : {AB}", memo="AB = AD + DB"), L(f"{AD} : {AB} = DE : {bc}", memo="DE // BC → 닮음"), L(f"DE = {bc} × {{{AD}/{AB}}} = {N(de)}"), L(f"{N(de)} cm")]
            ans, ap = f"{N(de)} cm", N(de)
        else:
            ae = R.randint(2, 12)
            ec = Fr(ae * qq, p)
            if ec.denominator != 1:
                return
            q = f"△ABC에서 DE // BC이고 AD = {AD} cm, DB = {DB} cm, AE = {ae} cm일 때, EC의 길이를 구하세요."
            lines = [L(f"AD : DB = AE : EC", memo="평행선이 두 변을 같은 비로 나눠요"), L(f"{AD} : {DB} = {ae} : EC"), L(f"EC = {ae} × {{{DB}/{AD}}} = {N(ec)}"), L(f"{N(ec)} cm")]
            ans, ap = f"{N(ec)} cm", N(ec)
        S.add(3, q, ans, "DE // BC → AD : AB = AE : AC = DE : BC", lines, f.out(), ap=ap, key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.randint(2, 8), R.randint(2, 8)
        if a == b:
            return
        c = R.randint(2, 9) * (a // gcd(a, b))
        d = Fr(c * b, a)
        if d.denominator != 1:
            return
        f = Fig()
        for y, nm_ in ((160, "l"), (330, "m"), (500, "n")):
            f.line(40, y, 620, y, c="ink", w=3, ar=1)
            f.text(612, y - 14, nm_, z=26, c="soft")
        f.line(150, 120, 230, 540, c="teal", w=3)
        f.line(380, 120, 560, 540, c="coral", w=3)
        f.text(170, 250, f"{a}", z=28, c="teal", b=700, a="e")
        f.text(200, 420, f"{b}", z=28, c="teal", b=700, a="e")
        f.text(470, 250, f"{c}", z=28, c="coral", b=700, a="s")
        f.text(520, 420, "x", z=30, c="coral", b=700, a="s")
        q = f"세 직선 l, m, n이 평행하고 두 직선과 만나 생긴 선분의 길이가 한쪽은 {a}, {b}, 다른 쪽은 {c}, x일 때, x의 값을 구하세요."
        lines = [L(f"{a} : {b} = {c} : x", memo="평행선 사이의 선분의 비"), L(f"{a}x = {b * c}"), L(f"x = {N(d)}")]
        S.add(4, q, N(d), "a : b = c : d", lines, f.out(), sub={"x": d}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        f = Fig()
        A, B, C = (300, 110), (100, 540), (560, 540)
        f.poly([A, B, C], c="ink", w=3)
        if k == 0:
            bc = R.randint(3, 20) * 2
            M = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
            Nn = ((A[0] + C[0]) / 2, (A[1] + C[1]) / 2)
            f.line(*M, *Nn, c="teal", w=3.5, at=0)
            q = f"△ABC에서 두 변 AB, AC의 중점을 각각 M, N이라 할 때, BC = {bc} cm이면 MN의 길이는 몇 cm인가요?"
            lines = [L("MN // BC, MN = {1/2}BC", memo="삼각형의 두 변의 중점을 연결한 선분"), L(f"{bc} ÷ 2 = {bc // 2}"), L(f"{bc // 2} cm")]
            ans, ap = f"{bc // 2} cm", str(bc // 2)
        elif k == 1:
            ad = R.randint(2, 12) * 3
            Dm = ((B[0] + C[0]) / 2, B[1])
            G = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
            f.line(*A, *Dm, c="teal", w=3, at="q")
            f.dot(*G, r=8, f="coral", at=0)
            f.text(G[0] + 18, G[1], "G", z=26, c="coral", b=700, at=0)
            q = f"△ABC의 무게중심을 G, 변 BC의 중점을 D라 할 때, 중선 AD의 길이가 {ad} cm이면 AG의 길이는 몇 cm인가요?"
            lines = [L("AG : GD = 2 : 1", memo="무게중심은 중선을 2 : 1로"), L(f"{ad} × {{2/3}} = {ad * 2 // 3}"), L(f"{ad * 2 // 3} cm")]
            ans, ap = f"{ad * 2 // 3} cm", str(ad * 2 // 3)
        else:
            T = R.randint(2, 15) * 6
            G = ((A[0] + B[0] + C[0]) / 3, (A[1] + B[1] + C[1]) / 3)
            for P in (A, B, C):
                f.line(*G, *P, c="teal", w=2.5, d=True)
            f.dot(*G, r=8, f="coral")
            q = f"넓이가 {T} cm²인 △ABC의 무게중심을 G라 할 때, △GBC의 넓이를 구하세요."
            lines = [L("무게중심과 세 꼭짓점을 이으면 넓이가 3등분", memo="△GAB = △GBC = △GCA"), L(f"{T} ÷ 3 = {T // 3}"), L(f"{T // 3} cm²")]
            ans, ap = f"{T // 3} cm²", str(T // 3)
        S.add(5, q, ans, "중점연결정리 · 무게중심의 2 : 1", lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 피타고라스 정리 ══════════
TRIPS = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41)]

def rt_fig(f, a, b, labs, at="q"):
    sc = min(420 / b, 380 / a)
    A, B, C = (130, 530 - sc * a), (130, 530), (130 + sc * b, 530)
    f.poly([A, B, C], c="ink", w=3, f="gold", fo=0.1, at=at)
    angle_mark(f, B, C, A, r=30, at=at)
    la, lb, lc = labs
    f.text(B[0] - 20, (A[1] + B[1]) / 2 + 10, la, z=28, b=700, a="e", at=at)
    f.text((B[0] + C[0]) / 2, B[1] + 40, lb, z=28, b=700, at=at)
    f.text((A[0] + C[0]) / 2 + 22, (A[1] + C[1]) / 2 - 10, lc, z=28, b=700, a="s", at=at)

def pyth():
    S = Set("pyth", "피타고라스 정리 — 세 변의 관계에서 거리까지", "피타고라스",
            {1: "빗변의 길이", 2: "다른 한 변의 길이", 3: "직각삼각형 판별과 활용", 4: "두 점 사이의 거리", 5: "대각선 · 높이 — 제곱근으로"},
            pp=8,
            tips={1: "직각삼각형에서 (빗변)^{2} = (다른 두 변의 제곱의 합)",
                  2: "구하는 변을 x로 두고 x^{2} = 빗변^{2} − 아는 변^{2}",
                  3: "가장 긴 변의 제곱 = 나머지 두 변의 제곱의 합이면 직각삼각형",
                  4: "두 점 사이의 거리 = √{(x의 차)^{2} + (y의 차)^{2}} — 좌표평면 위의 직각삼각형",
                  5: "직사각형의 대각선 √{a^{2} + b^{2}} · 정삼각형의 높이 {√{3}/2}a"},
            note="1 ~ 3단계는 제곱해서 자연수가 되는 세 수(3, 4, 5 등)로만 다루고, 4 ~ 5단계에서 제곱근으로 넓혀요. 직각을 낀 두 변과 빗변을 그림에서 먼저 구별하게 해 주세요.")
    R = rng(1405)

    def g1():
        a, b, c = R.choice(TRIPS)
        k = R.randint(1, 4 if c < 20 else 1)
        a, b, c = a * k, b * k, c * k
        if R.random() < 0.5:
            a, b = b, a
        f = Fig()
        rt_fig(f, a, b, (f"{a}", f"{b}", "x"))
        q = f"직각을 낀 두 변의 길이가 {a} cm, {b} cm인 직각삼각형의 빗변의 길이를 구하세요."
        lines = [L(f"x^{{2}} = {a}^{{2}} + {b}^{{2}}", memo="피타고라스 정리"), L(f"{a}^{{2}} + {b}^{{2}} = {a * a + b * b} = {c}^{{2}}"), L(f"x = {c}", memo="x > 0")]
        S.add(1, q, f"{c} cm", "빗변의 제곱 = 두 변의 제곱의 합", lines, f.out(), ap=str(c), sub={"x": c}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        a, b, c = R.choice(TRIPS)
        k = R.randint(1, 4 if c < 20 else 1)
        a, b, c = a * k, b * k, c * k
        if R.random() < 0.5:
            a, b = b, a
        f = Fig()
        rt_fig(f, a, b, ("x", f"{b}", f"{c}"))
        q = f"빗변의 길이가 {c} cm이고 다른 한 변의 길이가 {b} cm인 직각삼각형의 나머지 한 변의 길이를 구하세요."
        lines = [L(f"x^{{2}} + {b}^{{2}} = {c}^{{2}}", memo="빗변은 가장 긴 변"), L(f"x^{{2}} = {c * c} − {b * b} = {a * a}"), L(f"x = {a}", memo="x > 0")]
        S.add(2, q, f"{a} cm", "x^{2} = 빗변^{2} − 아는 변^{2}", lines, f.out(), ap=str(a), sub={"x": a}, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        if k == 0:
            a, b, c = R.choice(TRIPS)
            m = R.randint(1, 3)
            a, b, c = a * m, b * m, c * m
            if R.random() < 0.5:
                c += R.choice([-1, 1])
            sides = sorted([a, b, c])
            ok = sides[0] ** 2 + sides[1] ** 2 == sides[2] ** 2
            q = f"세 변의 길이가 {a} cm, {b} cm, {c} cm인 삼각형은 직각삼각형인가요?"
            s2 = sides[0] ** 2 + sides[1] ** 2
            lines = [L(f"가장 긴 변 {sides[2]} → {sides[2]}^{{2}} = {sides[2] ** 2}"), L(f"{sides[0]}^{{2}} + {sides[1]}^{{2}} = {s2}"), L("같으므로 직각삼각형" if ok else "다르므로 직각삼각형이 아니에요")]
            S.add(3, q, "예" if ok else "아니요", "가장 긴 변의 제곱과 나머지 두 변의 제곱의 합 비교", lines, None, omr="ex", key=q)
        elif k == 1:
            a, b, c = R.choice(TRIPS[:3])
            m = R.randint(1, 3)
            a, b, c = a * m, b * m, c * m
            f = Fig()
            f.line(140, 540, 560, 540, c="ink", w=3)
            f.line(500, 540, 500, 120, c="ink", w=4)
            sc = 380 / max(a, b)
            top = (500, 540 - sc * b)
            foot = (500 - sc * a, 540)
            f.line(*foot, *top, c="gold", w=6)
            f.text((foot[0] + top[0]) / 2 - 20, (foot[1] + top[1]) / 2, f"사다리 {c} `m`", z=26, b=700, a="e")
            f.text((foot[0] + 500) / 2, 576, f"{a} `m`", z=26, b=700)
            q = f"길이가 {c} `m`인 사다리를 벽에 기대어 세웠더니 사다리의 아래 끝이 벽에서 {a} `m` 떨어졌어요. 사다리의 위 끝은 바닥에서 몇 `m` 높이에 있나요?"
            lines = [L(f"x^{{2}} + {a}^{{2}} = {c}^{{2}}", memo="벽 · 바닥 · 사다리가 직각삼각형"), L(f"x^{{2}} = {c * c} − {a * a} = {b * b}"), L(f"x = {b}")]
            S.add(3, q, f"{b} `m`", "벽과 바닥이 직각 — 사다리가 빗변", lines, f.out(), ap=str(b), sub={"x": b}, key=q)
        else:
            a, b, c = R.choice(TRIPS[:3])
            m = R.randint(1, 4)
            a, b, c = a * m, b * m, c * m
            f = Fig()
            sc = 400 / max(a, b)
            f.rect(130, 140, sc * b, sc * a, c="ink", sw=3)
            f.line(130, 140 + sc * a, 130 + sc * b, 140, c="teal", w=3, d=True)
            q = f"가로 {b} cm, 세로 {a} cm인 직사각형의 대각선의 길이를 구하세요."
            lines = [L(f"x^{{2}} = {b}^{{2}} + {a}^{{2}}", memo="대각선이 빗변"), L(f"{b * b} + {a * a} = {c * c}"), L(f"x = {c}")]
            S.add(3, q, f"{c} cm", "대각선으로 나뉜 직각삼각형", lines, f.out(), ap=str(c), sub={"x": c}, key=q)
    fill(S, 3, 20, g3)

    def sqrt_simplify(n):
        o, i = 1, n
        for p in range(2, int(math.isqrt(n)) + 1):
            while i % (p * p) == 0:
                i //= p * p
                o *= p
        return o, i

    def RT(n):
        o, i = sqrt_simplify(n)
        if i == 1:
            return str(o)
        return (str(o) if o > 1 else "") + f"√{{{i}}}"

    def g4():
        x1, y1, x2, y2 = R.randint(-5, 5), R.randint(-5, 5), R.randint(-5, 5), R.randint(-5, 5)
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 or dy == 0:
            return
        d2 = dx * dx + dy * dy
        f = Fig()
        pl = Plane(f, (-6.5, 6.5), (-6.5, 6.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=2)
        pl.pt(x1, y1, label=f"A({N(x1)}, {N(y1)})", pos="sw" if x1 < x2 else "se")
        pl.pt(x2, y2, label=f"B({N(x2)}, {N(y2)})", pos="ne" if x2 > x1 else "nw")
        f.line(*pl.P(x1, y1), *pl.P(x2, y2), c="gold", w=3.5, at=2)
        f.line(*pl.P(x1, y1), *pl.P(x2, y1), c="teal", w=3, d=True, at=0)
        f.line(*pl.P(x2, y1), *pl.P(x2, y2), c="coral", w=3, d=True, at=0)
        q = f"두 점 A({N(x1)}, {N(y1)}), B({N(x2)}, {N(y2)}) 사이의 거리를 구하세요."
        lines = [L(f"x의 차 {abs(dx)}, y의 차 {abs(dy)}", memo="직각삼각형의 두 변"), L(f"AB^{{2}} = {abs(dx)}^{{2}} + {abs(dy)}^{{2}} = {d2}"), L(f"AB = √{{{d2}}} = {RT(d2)}" if RT(d2) != f"√{{{d2}}}" else f"AB = √{{{d2}}}")]
        S.add(4, q, RT(d2), "좌표의 차로 직각삼각형을 만들어요", lines, f.out(), omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            a, b = R.randint(2, 9), R.randint(2, 9)
            d2 = a * a + b * b
            if math.isqrt(d2) ** 2 == d2:
                return
            q = f"가로 {a} cm, 세로 {b} cm인 직사각형의 대각선의 길이를 구하세요."
            lines = [L(f"{a}^{{2}} + {b}^{{2}} = {d2}"), L(f"√{{{d2}}} = {RT(d2)}" if RT(d2) != f"√{{{d2}}}" else f"√{{{d2}}}"), L(f"{RT(d2)} cm")]
            ans, ap = f"{RT(d2)} cm", plain(RT(d2))
        elif k == 1:
            a = R.randint(2, 12)
            q = f"한 변의 길이가 {a} cm인 정삼각형의 높이를 구하세요."
            h = f"{{{a}√{{3}}/2}}" if a % 2 else (f"{a // 2}√{{3}}" if a != 2 else "√{3}")
            lines = [L(f"h^{{2}} + ({{{a}/2}})^{{2}} = {a}^{{2}}", memo="높이는 밑변을 이등분"), L(f"h^{{2}} = {N(Fr(3 * a * a, 4))}"), L(f"h = {h}")]
            ans, ap = f"{h} cm", plain(h)
        else:
            a = R.randint(2, 12)
            q = f"한 변의 길이가 {a} cm인 정사각형의 대각선의 길이를 구하세요."
            dg = f"{a}√{{2}}"
            lines = [L(f"{a}^{{2}} + {a}^{{2}} = {2 * a * a}"), L(f"√{{{2 * a * a}}} = {dg}"), L(f"{dg} cm")]
            ans, ap = f"{dg} cm", plain(dg)
        S.add(5, q, ans, "직각삼각형을 찾아 제곱근으로", lines, None, ap=ap, omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 경우의 수 ══════════
def dice_grid(f, cells, at=0):
    """주사위 두 개 6 × 6 표 — cells: 칠할 (a, b) 목록"""
    x0, y0, s = 150, 130, 66
    for i in range(6):
        f.text(x0 + s * i + s / 2, y0 - 16, str(i + 1), z=24, c="soft")
        f.text(x0 - 18, y0 + s * i + s / 2 + 8, str(i + 1), z=24, c="soft", a="e")
    f.grid(x0, y0, s, s, 6, 6, c="ink", sw=2)
    for k, (a, b) in enumerate(cells):
        f.rect(x0 + s * (a - 1) + 4, y0 + s * (b - 1) + 4, s - 8, s - 8, c="none", f="gold", fo=0.55, at=at, dl=k * 60)
    f.text(x0 + 3 * s, y0 + 6 * s + 46, "첫째(가로) · 둘째(세로)", z=22, c="soft")

def count():
    S = Set("count", "경우의 수의 기초 — 합의 법칙 · 곱의 법칙", "경우의 수",
            {1: "합의 법칙", 2: "곱의 법칙", 3: "한 줄로 세우기", 4: "자연수 만들기", 5: "대표 뽑기"},
            pp=8,
            tips={1: "동시에 일어나지 않는 두 사건 — 경우의 수를 더해요",
                  2: "동시에(잇달아) 일어나는 두 사건 — 경우의 수를 곱해요",
                  3: "n명을 한 줄로: n × (n − 1) × … × 1 · 이웃하면 한 묶음으로",
                  4: "맨 앞자리부터 — 0은 맨 앞에 올 수 없어요",
                  5: "자격이 다르면(회장 · 부회장) 순서 있게 n(n − 1), 같으면 {n(n − 1)/2}"},
            note="경우의 수는 ‘또는 → 더하기, 그리고 → 곱하기’로 시작해요. 줄 세우기와 뽑기는 자리(칸)를 그려 놓고 칸마다 올 수 있는 수를 적게 하면 곱의 법칙으로 자연스럽게 이어져요.")
    R = rng(1406)

    def g1():
        k = S.count(1) % 2
        if k == 0:
            s1, s2 = R.sample(range(3, 12), 2)
            c1 = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == s1]
            c2 = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == s2]
            f = Fig()
            dice_grid(f, c1, at=0)
            for kk, (a, b) in enumerate(c2):
                f.rect(150 + 66 * (a - 1) + 4, 130 + 66 * (b - 1) + 4, 58, 58, c="none", f="teal", fo=0.55, at=1, dl=kk * 60)
            q = f"서로 다른 두 주사위를 던질 때, 나오는 눈의 수의 합이 {s1} 또는 {s2}인 경우의 수를 구하세요."
            lines = [L(f"합 {s1}: {len(c1)}가지", memo=", ".join(f"({a}, {b})" for a, b in c1[:4]) + (" …" if len(c1) > 4 else "")), L(f"합 {s2}: {len(c2)}가지"), L(f"{len(c1)} + {len(c2)} = {len(c1) + len(c2)}", memo="동시에 일어나지 않으니 더해요")]
            S.add(1, q, str(len(c1) + len(c2)), "‘또는’이고 겹치지 않으면 더해요", lines, f.out(), key=q)
        else:
            a, b = R.randint(2, 9), R.randint(2, 9)
            t1, t2 = R.choice([("버스", "지하철"), ("빵", "떡"), ("소설책", "만화책"), ("우유", "주스")])
            q = f"{t1}{'이' if bat(t1) else '가'} {a}종류, {t2}{'이' if bat(t2) else '가'} {b}종류 있어요. 이 중 한 가지를 고르는 경우의 수를 구하세요."
            lines = [L(f"{t1}에서 고르기 {a}가지, {t2}에서 고르기 {b}가지", memo="둘 중 하나만"), L(f"{a} + {b} = {a + b}")]
            S.add(1, q, str(a + b), "한 가지만 고르면 더해요", lines, None, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        if k == 0:
            a, b = R.randint(2, 7), R.randint(2, 7)
            q = f"윗옷이 {a}벌, 바지가 {b}벌 있어요. 윗옷과 바지를 하나씩 골라 입는 경우의 수를 구하세요."
            lines = [L(f"윗옷 {a}가지 각각에 바지 {b}가지", memo="잇달아 고르기"), L(f"{a} × {b} = {a * b}")]
            v = a * b
        elif k == 1:
            c, d = R.randint(1, 4), R.randint(1, 3)
            if c + d > 5:
                return
            v = 2 ** c * 6 ** d
            q = f"동전 {c}개와 주사위 {d}개를 동시에 던질 때, 일어나는 모든 경우의 수를 구하세요."
            lines = [L(f"동전 {c}개: 2^{{{c}}} = {2 ** c}", memo="동전 하나 2가지"), L(f"주사위 {d}개: 6^{{{d}}} = {6 ** d}"), L(f"{2 ** c} × {6 ** d} = {v}")]
        else:
            a, b, c = R.randint(2, 4), R.randint(2, 4), R.randint(2, 4)
            q = f"A 마을에서 B 마을로 가는 길이 {a}가지, B 마을에서 C 마을로 가는 길이 {b}가지, C 마을에서 D 마을로 가는 길이 {c}가지예요. A에서 D까지 B, C를 차례로 거쳐 가는 경우의 수를 구하세요."
            lines = [L(f"A→B {a}가지, B→C {b}가지, C→D {c}가지", memo="이어서 가니 곱해요"), L(f"{a} × {b} × {c} = {a * b * c}")]
            v = a * b * c
        S.add(2, q, str(v), "잇달아(동시에) 일어나면 곱해요", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        n = R.randint(3, 6)
        names = R.sample(PEOPLE, n)
        f = Fig()
        w = 520 / n
        for i in range(n):
            f.rect(70 + w * i + 6, 280, w - 12, 90, c="ink", sw=3, rx=10)
        if k == 0:
            v = factorial(n)
            for i in range(n):
                f.text(70 + w * i + w / 2, 340, str(n - i), z=36, c="coral", b=700, at=0, dl=i * 150)
            q = f"{n}명의 학생 {J(', '.join(names), '을', '를')} 한 줄로 세우는 경우의 수를 구하세요."
            lines = [L(" × ".join(str(n - i) for i in range(n)) + f" = {v}", memo="첫 자리부터 남은 사람 수")]
            lines.insert(0, L(f"자리 {n}개 — 차례로 {n}명, {n - 1}명, …, 1명"))
        elif k == 1:
            v = factorial(n - 1)
            f.text(70 + w / 2, 340, names[0], z=26 if n > 4 else 30, c="gold", b=700)
            for i in range(1, n):
                f.text(70 + w * i + w / 2, 340, str(n - i), z=36, c="coral", b=700, at=0, dl=i * 150)
            q = f"{n}명의 학생 {J(', '.join(names), '을', '를')} 한 줄로 세울 때, {iga(names[0])} 맨 앞에 서는 경우의 수를 구하세요."
            lines = [L(f"{eun(names[0])} 맨 앞에 고정", memo="나머지만 줄 세우기"), L(" × ".join(str(n - 1 - i) for i in range(n - 1)) + f" = {v}" if n > 2 else f"{v}")]
        else:
            v = factorial(n - 1) * 2
            f.rect(70 + 6, 280, 2 * w - 12, 90, c="gold", sw=4, rx=12, at=0)
            q = f"{n}명의 학생 {J(', '.join(names), '을', '를')} 한 줄로 세울 때, {wa(names[0])} {iga(names[1])} 이웃하여 서는 경우의 수를 구하세요."
            lines = [L(f"{names[0]} · {eul(names[1])} 한 묶음 → {n - 1}명 줄 세우기처럼", memo="묶음 안에서 자리 바꾸기 2가지"), L(f"{' × '.join(str(n - 1 - i) for i in range(n - 1))} × 2 = {v}")]
        S.add(3, q, str(v), "자리마다 올 수 있는 사람 수를 곱해요", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        n = R.randint(4, 7)
        zero = k == 2
        cards = sorted(([0] + R.sample(range(1, 10), n - 1)) if zero else R.sample(range(1, 10), n))
        if k == 0:
            v = n * (n - 1)
            q = f"{', '.join(map(str, cards))}의 숫자가 하나씩 적힌 카드 {n}장 중에서 2장을 뽑아 만들 수 있는 두 자리 자연수의 개수를 구하세요."
            lines = [L(f"십의 자리 {n}가지, 일의 자리 {n - 1}가지", memo="같은 카드는 다시 못 써요"), L(f"{n} × {n - 1} = {v}")]
        elif k == 1:
            v = n * (n - 1) * (n - 2)
            q = f"{', '.join(map(str, cards))}의 숫자가 하나씩 적힌 카드 {n}장 중에서 3장을 뽑아 만들 수 있는 세 자리 자연수의 개수를 구하세요."
            lines = [L(f"백 {n}가지, 십 {n - 1}가지, 일 {n - 2}가지"), L(f"{n} × {n - 1} × {n - 2} = {v}")]
        else:
            v = (n - 1) * (n - 1)
            q = f"{', '.join(map(str, cards))}의 숫자가 하나씩 적힌 카드 {n}장 중에서 2장을 뽑아 만들 수 있는 두 자리 자연수의 개수를 구하세요."
            lines = [L(f"십의 자리: 0 빼고 {n - 1}가지", memo="0은 맨 앞에 못 와요"), L(f"일의 자리: 남은 {n - 1}가지", memo="0이 다시 들어와요"), L(f"{n - 1} × {n - 1} = {v}")]
        S.add(4, q, str(v), "맨 앞자리부터 — 0은 맨 앞에 올 수 없어요", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        n = R.randint(4, 10)
        if k == 0:
            v = n * (n - 1)
            q = f"{n}명의 후보 중에서 회장 1명, 부회장 1명을 뽑는 경우의 수를 구하세요."
            lines = [L(f"회장 {n}가지, 부회장 {n - 1}가지", memo="자격이 달라 순서가 있어요"), L(f"{n} × {n - 1} = {v}")]
        elif k == 1:
            v = n * (n - 1) // 2
            q = f"{n}명의 후보 중에서 대표 2명을 뽑는 경우의 수를 구하세요."
            lines = [L(f"{n} × {n - 1} = {n * (n - 1)}", memo="순서 있게 뽑으면"), L(f"{n * (n - 1)} ÷ 2 = {v}", memo="(A, B)와 (B, A)는 같은 뽑기")]
        else:
            v = n * (n - 1) * (n - 2) // 6
            q = f"원 위에 있는 서로 다른 {n}개의 점 중에서 세 점을 골라 만들 수 있는 삼각형의 개수를 구하세요."
            lines = [L(f"{n} × {n - 1} × {n - 2} = {n * (n - 1) * (n - 2)}", memo="세 점을 순서 있게"), L(f"{n * (n - 1) * (n - 2)} ÷ 6 = {v}", memo="같은 세 점의 순서 3 × 2 × 1 = 6")]
            f = Fig()
            for i in range(n):
                p = ang_pt(330, 340, 220, 90 - 360 * i / n)
                f.dot(*p, r=10, f="ink")
            f.circ(330, 340, 220, c="soft", sw=2)
            pts = [ang_pt(330, 340, 220, 90 - 360 * i / n) for i in range(3)]
            f.poly(pts, c="gold", w=3, f="gold", fo=0.2, at=0)
            S.add(5, q, str(v), "세 점을 고르는 순서는 상관없어요", lines, f.out(), key=q)
            return
        S.add(5, q, str(v), "자격이 다르면 순서 있게, 같으면 ÷ 2", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 확률 ══════════
def prob():
    S = Set("prob", "확률의 기초 — 여사건 · 덧셈 · 곱셈", "확률",
            {1: "확률의 뜻", 2: "어떤 사건이 일어나지 않을 확률", 3: "확률의 덧셈", 4: "확률의 곱셈", 5: "연속하여 꺼내기"},
            mixed=True, pp=8,
            tips={1: "확률 = (사건이 일어나는 경우의 수) ÷ (모든 경우의 수)",
                  2: "(일어나지 않을 확률) = 1 − (일어날 확률) — ‘적어도 하나’에 써요",
                  3: "동시에 일어나지 않는 두 사건 — 확률을 더해요",
                  4: "서로 영향을 주지 않는 두 사건이 함께 — 확률을 곱해요",
                  5: "꺼낸 것을 다시 넣지 않으면 두 번째의 전체 개수가 1 줄어요"},
            note="확률은 모든 경우를 표나 수형도로 세는 것부터 시작해 주세요. ‘적어도’라는 말이 보이면 반대 사건(여사건)을 먼저 떠올리게 해요.")
    R = rng(1407)

    def g1():
        k = S.count(1) % 3
        if k == 0:
            s = R.randint(3, 11)
            cells = [(a, b) for a in range(1, 7) for b in range(1, 7) if a + b == s]
            f = Fig()
            dice_grid(f, cells)
            q = f"서로 다른 두 주사위를 던질 때, 나오는 눈의 수의 합이 {s}일 확률을 구하세요."
            p = Fr(len(cells), 36)
            lines = [L("모든 경우 6 × 6 = 36"), L(f"합 {s}: {len(cells)}가지"), L(f"{{{len(cells)}/36}} = {FR(p)}" if Fr(len(cells), 36).denominator != 36 else f"{{{len(cells)}/36}}")]
            S.add(1, q, FR(p), "(일어나는 경우) ÷ (모든 경우)", lines, f.out(), key=q)
        elif k == 1:
            r, b = R.randint(1, 8), R.randint(1, 8)
            g = R.randint(0, 5)
            T = r + b + g
            p = Fr(r, T)
            q = f"주머니에 빨간 공 {r}개, 파란 공 {b}개" + (f", 노란 공 {g}개" if g else "") + "가 들어 있어요. 공 한 개를 꺼낼 때 빨간 공일 확률을 구하세요."
            lines = [L(f"모든 경우 {r} + {b}" + (f" + {g}" if g else "") + f" = {T}"), L(f"빨간 공 {r}가지"), L(f"{F_(r, T)}" + (f" = {FR(p)}" if p.denominator != T else ""))]
            S.add(1, q, FR(p), "(빨간 공의 수) ÷ (전체 공의 수)", lines, None, key=q)
        else:
            n = R.choice([10, 12, 15, 20, 24, 30])
            d = R.randint(2, 6)
            c = n // d
            p = Fr(c, n)
            q = f"1부터 {n}까지의 자연수가 하나씩 적힌 카드 {n}장 중 한 장을 뽑을 때, {d}의 배수가 나올 확률을 구하세요."
            lines = [L(f"{d}의 배수: {n} ÷ {d} = {c} … {n % d}", memo=f"{c}가지"), L(f"{F_(c, n)}" + (f" = {FR(p)}" if p.denominator != n else ""))]
            S.add(1, q, FR(p), "배수의 개수 ÷ 전체 카드 수", lines, None, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        if k == 0:
            if R.random() < 0.5:
                n = R.randint(2, 4)
                face, other = R.choice([("앞면", "뒷면"), ("뒷면", "앞면")])
                p = 1 - Fr(1, 2 ** n)
                q = f"동전 {n}개를 동시에 던질 때, 적어도 한 개는 {face}이 나올 확률을 구하세요."
                lines = [L(f"모두 {other}: {{1/{2 ** n}}}", memo="반대 사건"), L(f"1 − {{1/{2 ** n}}} = {FR(p)}")]
            else:
                n = R.randint(2, 3)
                ev, pe = R.choice([("6의 눈", Fr(1, 6)), ("짝수의 눈", Fr(1, 2)), ("3의 배수의 눈", Fr(1, 3))])
                pn = (1 - pe) ** n
                p = 1 - pn
                q = f"주사위 {n}개를 동시에 던질 때, 적어도 한 개는 {ev}이 나올 확률을 구하세요."
                lines = [L(f"한 개에서 {ev}이 아닐 확률 {FR(1 - pe)}", memo="반대 사건"), L(f"모두 아닐 확률 ({FR(1 - pe)})^{{{n}}} = {FR(pn)}"), L(f"1 − {FR(pn)} = {FR(p)}")]
        elif k == 1:
            p0 = Fr(R.randint(1, 9), 10)
            p = 1 - p0
            q = f"내일 비가 올 확률이 {DEC(p0)}일 때, 내일 비가 오지 않을 확률을 구하세요."
            lines = [L("(오지 않을 확률) = 1 − (올 확률)"), L(f"1 − {DEC(p0)} = {DEC(p)}")]
            S.add(2, q, DEC(p), "1 − (일어날 확률)", lines, None, key=q)
            return
        else:
            r, b = R.randint(2, 6), R.randint(2, 6)
            T = r + b
            pb = Fr(b * (b - 1), T * (T - 1))
            p = 1 - pb
            q = f"주머니에 빨간 공 {r}개, 파란 공 {b}개가 있어요. 공 2개를 동시에 꺼낼 때, 적어도 한 개는 빨간 공일 확률을 구하세요."
            lines = [L(f"모두 파란 공: {{{b}/{T}}} × {{{b - 1}/{T - 1}}} = {FR(pb)}", memo="반대 사건"), L(f"1 − {FR(pb)} = {FR(p)}")]
        S.add(2, q, FR(p), "‘적어도’ → 1 − (모두 반대일 확률)", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        if k == 0:
            s1, s2 = R.sample(range(2, 13), 2)
            c1 = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s1)
            c2 = sum(1 for a in range(1, 7) for b in range(1, 7) if a + b == s2)
            p = Fr(c1 + c2, 36)
            q = f"서로 다른 두 주사위를 던질 때, 눈의 수의 합이 {s1} 또는 {s2}일 확률을 구하세요."
            lines = [L(f"{{{c1}/36}} + {{{c2}/36}} = {FR(p)}", memo="동시에 일어나지 않아요"), L(f"{FR(p)}")]
        else:
            n = R.choice([10, 12, 15, 20])
            a, b = R.sample([3, 4, 5, 7], 2)
            ca, cb = n // a, n // b
            both = n // (a * b // gcd(a, b))
            if both:
                return
            p = Fr(ca + cb, n)
            q = f"1부터 {n}까지의 자연수가 적힌 카드 중 한 장을 뽑을 때, {a}의 배수 또는 {b}의 배수가 나올 확률을 구하세요."
            lines = [L(f"{a}의 배수 {ca}장, {b}의 배수 {cb}장", memo="겹치는 수가 없어요"), L(f"{{{ca}/{n}}} + {{{cb}/{n}}} = {FR(p)}")]
        S.add(3, q, FR(p), "동시에 일어나지 않으면 확률을 더해요", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        if k == 0:
            e = R.choice([(Fr(1, 2), "앞면"), (Fr(1, 2), "뒷면")])
            d = R.choice([(Fr(1, 2), "짝수"), (Fr(1, 2), "홀수"), (Fr(1, 3), "3의 배수"), (Fr(1, 6), "6의 눈"), (Fr(2, 3), "5 미만의 눈")])
            p = e[0] * d[0]
            q = f"동전 한 개와 주사위 한 개를 동시에 던질 때, 동전은 {e[1]}이 나오고 주사위는 {d[1]}{'이' if bat(d[1]) else '가'} 나올 확률을 구하세요."
            lines = [L(f"{FR(e[0])} × {FR(d[0])} = {FR(p)}", memo="서로 영향을 주지 않아요")]
            lines.insert(0, L(f"동전 {e[1]}: {FR(e[0])}, 주사위 {d[1]}: {FR(d[0])}"))
        elif k == 1:
            pa, pb = Fr(R.randint(1, 9), 10), Fr(R.randint(1, 9), 10)
            p = pa * pb
            q = f"A, B 두 사람이 어떤 문제를 맞힐 확률이 각각 {DEC(pa)}, {DEC(pb)}일 때, 두 사람이 모두 맞힐 확률을 구하세요."
            lines = [L(f"{DEC(pa)} × {DEC(pb)} = {DEC(p)}", memo="함께 일어나니 곱해요")]
            S.add(4, q, DEC(p), "서로 영향을 주지 않으면 곱해요", lines, None, key=q)
            return
        else:
            r, b = R.randint(1, 6), R.randint(1, 6)
            T = r + b
            p = Fr(r, T) * Fr(b, T)
            q = f"주머니에 빨간 공 {r}개, 파란 공 {b}개가 있어요. 한 개를 꺼내 확인하고 다시 넣은 뒤 또 한 개를 꺼낼 때, 첫 번째는 빨간 공, 두 번째는 파란 공일 확률을 구하세요."
            lines = [L(f"{{{r}/{T}}} × {{{b}/{T}}} = {FR(p)}", memo="다시 넣으니 두 번 모두 전체가 같아요")]
        S.add(4, q, FR(p), "서로 영향을 주지 않으면 곱해요", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        r, b = R.randint(2, 7), R.randint(2, 7)
        T = r + b
        if k == 0:
            p = Fr(r, T) * Fr(r - 1, T - 1)
            q = f"주머니에 빨간 공 {r}개, 파란 공 {b}개가 있어요. 꺼낸 공은 다시 넣지 않고 두 번 꺼낼 때, 두 번 모두 빨간 공일 확률을 구하세요."
            lines = [L(f"첫 번째 빨간 공: {F_(r, T)}"), L(f"두 번째 빨간 공: {F_(r - 1, T - 1)}", memo="하나 줄었어요"), L(f"{F_(r, T)} × {F_(r - 1, T - 1)} = {FR(p)}")]
        else:
            p = Fr(r, T) * Fr(b, T - 1) + Fr(b, T) * Fr(r, T - 1)
            q = f"주머니에 빨간 공 {r}개, 파란 공 {b}개가 있어요. 꺼낸 공은 다시 넣지 않고 두 번 꺼낼 때, 두 공의 색이 서로 다를 확률을 구하세요."
            p1, p2 = Fr(r * b, T * (T - 1)), Fr(b * r, T * (T - 1))
            lines = [L(f"빨강 → 파랑: {F_(r, T)} × {F_(b, T - 1)} = {FR(p1)}"), L(f"파랑 → 빨강: {F_(b, T)} × {F_(r, T - 1)} = {FR(p2)}"), L(f"{FR(p1)} + {FR(p2)} = {FR(p)}", memo="두 경우를 더해요")]
        S.add(5, q, FR(p), "다시 넣지 않으면 두 번째 전체가 1 줄어요", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S
