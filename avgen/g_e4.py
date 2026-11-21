# 초4 — ① 분모가 같은 분수의 덧셈 · 뺄셈 · ② 각도 — 직선 180°, 삼각형 180°, 사각형 360°, 시계
import math
from core import *
from fig import Fig, mv, fbar, ffill, angle_mark, ang_pt, dir_deg

def F_(n, d):
    return "{%d/%d}" % (n, d)

# ══════════ ① 분수 ══════════
def set_a():
    S = Set("a", "분모가 같은 분수의 덧셈과 뺄셈", "분수 덧셈·뺄셈",
            {1: "(진분수)+(진분수)", 2: "합이 1보다 큰 덧셈", 3: "(대분수)+(대분수)", 4: "(진분수)−(진분수) · 1에서 빼기", 5: "(대분수)−(대분수)"},
            mixed=True, pp=10,
            tips={1: "분모는 그대로, 분자끼리 더해요. {2/7} + {3/7} = {5/7}",
                  2: "분자끼리 더해 가분수가 되면 대분수로 — {8/8} = 1",
                  3: "자연수끼리, 분수끼리 더해요. 분수끼리 1이 넘으면 자연수로 올려요",
                  4: "1 = {8/8}처럼 1을 분모가 같은 분수로 바꾸어 빼요",
                  5: "분수끼리 뺄 수 없으면 자연수 1을 분수로 바꿔요. 4{1/6} = 3{7/6}"},
            note="분모가 같은 분수는 ‘분모는 그대로, 분자끼리’가 전부예요. 4학년은 약분하지 않아도 되고, 대분수와 가분수 답을 모두 맞게 해 주세요.")
    R = rng(401)
    BX, BW, BH = 50, 560, 74

    def g1():
        d = R.randint(3, 12); a = R.randint(1, d - 2); b = R.randint(1, d - 1 - a)
        f = Fig()
        fbar(f, BX, 200, BW, BH, d)
        ffill(f, BX, 200, BW, BH, d, 0, a, "gold", "q")
        ffill(f, BX, 200, BW, BH, d, a, b, "teal", 0)
        f.text(330, 160, f"1을 {d}칸으로", z=26, c="soft")
        f.text(330, 400, F_(a + b, d), z=64, at=1, b=700)
        S.add(1, f"{F_(a, d)} + {J(F_(b, d), '은', '는')} 얼마인가요?", F_(a + b, d), "분모는 그대로, 분자끼리 더해요",
              [L(f"{F_(1, d)}이 {a}개 + {b}개", memo="분모는 그대로"), L(f"{F_(a, d)} + {F_(b, d)} = {{{a} + {b}/{d}}} = {F_(a + b, d)}")], f.out(), key=f"{a}+{b}/{d}")
    fill(S, 1, 20, g1)

    def g2():
        d = R.randint(3, 12); a = R.randint(2, d - 1); b = R.randint(2, d - 1)
        r = a + b - d
        if r <= 0:
            return
        f = Fig()
        fbar(f, BX, 150, BW, BH, d)
        fbar(f, BX, 290, BW, BH, d)
        ffill(f, BX, 150, BW, BH, d, 0, a, "gold", "q")
        ffill(f, BX, 150, BW, BH, d, a, d - a, "teal", 0)
        ffill(f, BX, 290, BW, BH, d, 0, r, "teal", 0, dl=(d - a) * 90)
        f.text(620, 196, "1", z=40, c="gold", at=1, b=700)
        f.text(330, 480, f"1{F_(r, d)}", z=64, at=2, b=700)
        S.add(2, f"{F_(a, d)} + {J(F_(b, d), '은', '는')} 얼마인가요?", f"1{F_(r, d)}", "분자끼리 더한 뒤 1을 꺼내요",
              [L(f"{F_(a, d)} + {F_(b, d)} = {F_(a + b, d)}", memo="분자끼리"), L(f"{F_(a + b, d)} = {F_(d, d)} + {F_(r, d)}", memo=f"{F_(d, d)} = 1"),
               L(f"{F_(d, d)} + {F_(r, d)} = 1{F_(r, d)}")], f.out(), ap=f"1 {r}/{d}", key=f"{a}+{b}/{d}")
    fill(S, 2, 20, g2)

    def g3():
        d = R.randint(3, 12); a = R.randint(1, d - 1); b = R.randint(1, d - 1)
        w1, w2 = R.randint(1, 6), R.randint(1, 5)
        carry = a + b >= d
        if S.count(3) < 8 and carry:
            return
        if S.count(3) >= 8 and (not carry or a + b == d):
            return
        W = w1 + w2
        lines = [L(f"자연수끼리 {w1} + {w2} = {W}")]
        if carry:
            r = a + b - d
            lines.append(L(f"분수끼리 {F_(a, d)} + {F_(b, d)} = {F_(a + b, d)} = 1{F_(r, d)}", memo="1을 자연수로"))
            lines.append(L(f"{W} + 1{F_(r, d)} = {W + 1}{F_(r, d)}"))
            ans, ap = f"{W + 1}{F_(r, d)}", f"{W + 1} {r}/{d}"
        else:
            lines.append(L(f"분수끼리 {F_(a, d)} + {F_(b, d)} = {F_(a + b, d)}"))
            lines.append(L(f"{W} + {F_(a + b, d)} = {W}{F_(a + b, d)}"))
            ans, ap = f"{W}{F_(a + b, d)}", f"{W} {a + b}/{d}"
        S.add(3, f"{w1}{F_(a, d)} + {J(str(w2) + F_(b, d), '은', '는')} 얼마인가요?", ans, "자연수끼리, 분수끼리 더해요", lines, None, ap=ap, key=f"{w1}{a}+{w2}{b}/{d}")
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        d = R.randint(3, 12)
        if k == 0:
            a = R.randint(2, d - 1); b = R.randint(1, a - 1)
            f = Fig()
            fbar(f, BX, 230, BW, BH, d)
            ffill(f, BX, 230, BW, BH, d, 0, a, "gold", "q")
            cw = BW / d
            for i in range(b):
                f.cross(BX + cw * (a - 1 - i) + cw / 2, 230 + BH / 2, s=min(18, cw * 0.3), at=1, dl=i * 120)
            f.text(330, 420, F_(a - b, d), z=64, at=1, b=700, dl=b * 120 + 200)
            S.add(4, f"{F_(a, d)} − {J(F_(b, d), '은', '는')} 얼마인가요?", F_(a - b, d), "분모는 그대로, 분자끼리 빼요",
                  [L("분모는 그대로", memo=f"{F_(1, d)}이 몇 개"), L(f"{F_(a, d)} − {F_(b, d)} = {{{a} − {b}/{d}}} = {F_(a - b, d)}")], f.out(), key=f"{a}-{b}/{d}")
        elif k == 1:
            b = R.randint(1, d - 1)
            f = Fig()
            fbar(f, BX, 230, BW, BH, d)
            ffill(f, BX, 230, BW, BH, d, 0, d, "gold", 0)
            cw = BW / d
            for i in range(b):
                f.cross(BX + cw * (d - 1 - i) + cw / 2, 230 + BH / 2, s=min(18, cw * 0.3), at=1, dl=i * 120)
            f.text(330, 420, F_(d - b, d), z=64, at=1, b=700, dl=b * 120 + 200)
            S.add(4, f"1 − {J(F_(b, d), '은', '는')} 얼마인가요?", F_(d - b, d), f"1을 분모가 {d}인 분수로 바꿔요",
                  [L(f"1 = {F_(d, d)}", memo=f"1을 {d}칸으로"), L(f"{F_(d, d)} − {F_(b, d)} = {F_(d - b, d)}")], f.out(), key=f"1-{b}/{d}")
        else:
            n = R.randint(2, 5); b = R.randint(1, d - 1)
            S.add(4, f"{n} − {J(F_(b, d), '은', '는')} 얼마인가요?", f"{n - 1}{F_(d - b, d)}", "자연수에서 1을 분수로 바꿔요",
                  [L(f"{n} = {n - 1}{F_(d, d)}", memo=f"1 = {F_(d, d)}"), L(f"{n - 1}{F_(d, d)} − {F_(b, d)} = {n - 1}{F_(d - b, d)}")], None, ap=f"{n - 1} {d - b}/{d}", key=f"{n}-{b}/{d}")
    fill(S, 4, 20, g4)

    def g5():
        d = R.randint(3, 12); a = R.randint(1, d - 1); b = R.randint(1, d - 1)
        w1 = R.randint(2, 8); w2 = R.randint(1, w1 - 1)
        borrow = a < b
        if a == b:
            return
        if S.count(5) < 8 and borrow:
            return
        if S.count(5) >= 8 and not borrow:
            return
        if not borrow:
            lines = [L(f"자연수끼리 {w1} − {w2} = {w1 - w2}"), L(f"분수끼리 {F_(a, d)} − {F_(b, d)} = {F_(a - b, d)}"), L(f"{w1 - w2} + {F_(a - b, d)} = {MXu(w1 - w2, a - b, d)}")]
            ans, ap = MXu(w1 - w2, a - b, d), f"{w1 - w2} {a - b}/{d}"
        else:
            W = w1 - 1 - w2
            lines = [L(f"{F_(a, d)}에서 {F_(b, d)}" + ("을" if _bat(b) else "를") + " 뺄 수 없어요", memo=f"1을 {F_(d, d)}로"),
                     L(f"{w1}{F_(a, d)} = {w1 - 1}{F_(a + d, d)}"),
                     L(f"{w1 - 1}{F_(a + d, d)} − {w2}{F_(b, d)} = {MXu(W, a + d - b, d)}")]
            ans, ap = MXu(W, a + d - b, d), (f"{W} {a + d - b}/{d}" if W else f"{a + d - b}/{d}")
        S.add(5, f"{w1}{F_(a, d)} − {J(str(w2) + F_(b, d), '은', '는')} 얼마인가요?", ans, "분수끼리 뺄 수 없으면 1을 빌려 와요" if borrow else "자연수끼리, 분수끼리 빼요", lines, None, ap=ap, key=f"{w1}{a}-{w2}{b}/{d}")
    fill(S, 5, 20, g5)
    return S

def _bat(n):
    return str(n)[-1] in "013678"


# ══════════ ② 각도 ══════════
def tri_pts(a, b, box=(70, 90, 590, 600)):
    """밑변 위 두 각 a(왼쪽) · b(오른쪽) 인 삼각형을 그림 칸에 맞춰"""
    ta, tb = math.tan(math.radians(a)), math.tan(math.radians(b))
    # 밑변 0~1, 꼭짓점 x = tb/(ta+tb)
    if a == 90:
        px, py = 0, tb
    elif b == 90:
        px, py = 1, ta
    else:
        px = tb / (ta + tb); py = ta * px
    pts = [(0, 0), (1, 0), (px, py)]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, y0, x1, y1 = box
    s = min((x1 - x0) / (max(xs) - min(xs)), (y1 - y0) / (max(ys) - min(ys)))
    cx = (x0 + x1) / 2 - s * (max(xs) + min(xs)) / 2
    cy = (y0 + y1) / 2 + s * (max(ys) + min(ys)) / 2
    return [(cx + s * x, cy - s * y) for x, y in pts]

def quad_pts(angs, rnd):
    """내각 angs(4개, 합 360) 인 볼록 사각형 — 두 변 길이를 정하고 나머지를 닫히게 푼다"""
    for _ in range(200):
        L1, L2 = rnd.uniform(0.8, 1.3), rnd.uniform(0.7, 1.2)
        dirs, d = [], 0.0
        for k in range(4):
            dirs.append(d)
            d += 180 - angs[(k + 1) % 4]
        u = [(math.cos(math.radians(x)), math.sin(math.radians(x))) for x in dirs]
        # L1 u0 + L2 u1 + L3 u2 + L4 u3 = 0 → L3, L4
        bx = -(L1 * u[0][0] + L2 * u[1][0]); by = -(L1 * u[0][1] + L2 * u[1][1])
        det = u[2][0] * u[3][1] - u[3][0] * u[2][1]
        if abs(det) < 1e-6:
            continue
        L3 = (bx * u[3][1] - u[3][0] * by) / det
        L4 = (u[2][0] * by - bx * u[2][1]) / det
        if L3 < 0.45 or L4 < 0.45:
            continue
        P = [(0.0, 0.0)]
        for k, Lk in enumerate([L1, L2, L3]):
            P.append((P[-1][0] + Lk * u[k][0], P[-1][1] + Lk * u[k][1]))
        xs = [p[0] for p in P]; ys = [p[1] for p in P]
        x0, y0, x1, y1 = 80, 90, 580, 600
        s = min((x1 - x0) / (max(xs) - min(xs)), (y1 - y0) / (max(ys) - min(ys)))
        cx = (x0 + x1) / 2 - s * (max(xs) + min(xs)) / 2
        cy = (y0 + y1) / 2 + s * (max(ys) + min(ys)) / 2
        return [(cx + s * x, cy - s * y) for x, y in P]
    return None

def set_b():
    S = Set("b", "각도 — 직선 180°, 삼각형 180°, 사각형 360°", "각도",
            {1: "각도의 합과 차", 2: "직선이 이루는 각", 3: "삼각형의 세 각", 4: "사각형의 네 각", 5: "시계 바늘이 이루는 각"},
            pp=6,
            tips={1: "각도의 합과 차는 자연수처럼 계산하고 °를 붙여요",
                  2: "직선이 이루는 각은 180° — 모르는 각 = 180° − (아는 각)",
                  3: "삼각형 세 각의 합은 180°",
                  4: "사각형은 삼각형 2개 — 네 각의 합은 360°",
                  5: "시계 한 칸(숫자와 숫자 사이)은 360° ÷ 12 = 30° · 30분이면 짧은바늘은 반 칸(15°) 더 가요"},
            note="각도는 ‘직선 180° · 삼각형 180° · 사각형 360°’ 세 가지로 거의 다 풀려요. 모르는 각을 □로 두고 식으로 쓰게 해 주세요.")
    R = rng(402)

    def g1():
        if S.count(1) < 12:
            a = R.randint(15, 120); b = R.randint(15, 175 - a)
            V, Lr = ((330, 540), 300) if a + b > 90 else ((110, 560), 470)          # 둔각이면 꼭짓점을 가운데로 — 반직선이 그림 칸 밖(글자 쪽)으로 나가지 않게
            f = Fig()
            A, B, C = ang_pt(*V, Lr, 0), ang_pt(*V, Lr, a), ang_pt(*V, Lr, a + b)
            for P in (A, B, C):
                f.line(*V, *P, c="ink", w=4)
            angle_mark(f, V, A, B, r=110, label=f"{a}°", c="gold")
            angle_mark(f, V, B, C, r=150, label=f"{b}°", c="teal", f_="teal")
            angle_mark(f, V, A, C, r=210, label=f"{a + b}°", c="coral", f_=None, at=1, z=32)
            S.add(1, f"{a}° + {b}°는 몇 도인가요?", f"{a + b}°", "자연수처럼 더하고 °를 붙여요",
                  [L(f"{a} + {b} = {a + b}", memo="자연수의 덧셈"), L(f"{a}° + {b}° = {a + b}°")], f.out(), ap=str(a + b), key=f"{a}+{b}")
        else:
            a = R.randint(70, 175); b = R.randint(15, a - 20)
            V, Lr = ((330, 540), 300) if a > 90 else ((110, 560), 470)
            f = Fig()
            A, B, C = ang_pt(*V, Lr, 0), ang_pt(*V, Lr, a - b), ang_pt(*V, Lr, a)
            for P in (A, C):
                f.line(*V, *P, c="ink", w=4)
            f.line(*V, *B, c="teal", w=4, d=True)
            angle_mark(f, V, A, C, r=210, label=f"{a}°", c="gold", f_=None)
            angle_mark(f, V, B, C, r=140, label=f"{b}°", c="teal", f_="teal")
            angle_mark(f, V, A, B, r=95, label=f"{a - b}°", c="coral", f_="coral", at=1)
            S.add(1, f"{a}° − {b}°는 몇 도인가요?", f"{a - b}°", "자연수처럼 빼고 °를 붙여요",
                  [L(f"{a} − {b} = {a - b}", memo="자연수의 뺄셈"), L(f"{a}° − {b}° = {a - b}°")], f.out(), ap=str(a - b), key=f"{a}-{b}")
    fill(S, 1, 20, g1)

    def g2():
        V = (330, 470)
        f = Fig()
        Lp, Rp = (40, 470), (620, 470)
        f.line(*Lp, *Rp, c="ink", w=4)
        if S.count(2) < 12:
            a = R.randint(25, 155)
            P = ang_pt(*V, 300, a)
            f.line(*V, *P, c="ink", w=4)
            angle_mark(f, V, Rp, P, r=80, label=f"{a}°", c="gold")
            angle_mark(f, V, P, Lp, r=110, label="□", c="teal", f_="teal", z=40)
            angle_mark(f, V, Rp, Lp, r=200, label="180°", c="coral", f_=None, at=0, z=30)
            S.add(2, f"직선 위의 한 점에서 반직선을 그었어요. 한 각이 {a}°일 때 □는 몇 도인가요?", f"{180 - a}°", "직선이 이루는 각은 180°",
                  [L("직선이 이루는 각 = 180°"), L(f"□ = 180° − {a}° = {180 - a}°")], f.out(), ap=str(180 - a), key=f"1-{a}")
        else:
            a = R.randint(25, 90); b = R.randint(25, 130 - a)
            c = 180 - a - b
            P, Q = ang_pt(*V, 300, a), ang_pt(*V, 300, a + c)
            f.line(*V, *P, c="ink", w=4)
            f.line(*V, *Q, c="ink", w=4)
            angle_mark(f, V, Rp, P, r=80, label=f"{a}°", c="gold")
            angle_mark(f, V, P, Q, r=110, label="□", c="teal", f_="teal", z=40)
            angle_mark(f, V, Q, Lp, r=80, label=f"{b}°", c="gold")
            angle_mark(f, V, Rp, Lp, r=210, label="180°", c="coral", f_=None, at=0, z=30)
            S.add(2, f"직선 위의 한 점에서 반직선 두 개를 그었어요. 양쪽 각이 {a}°, {b}°일 때 가운데 □는 몇 도인가요?", f"{c}°", "세 각을 합하면 180°",
                  [L("직선이 이루는 각 = 180°"), L(f"□ = 180° − {a}° − {b}° = {c}°")], f.out(), ap=str(c), key=f"2-{a}-{b}")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3)
        f = Fig()
        if k < 12:
            a = R.randint(30, 100); b = R.randint(30, 150 - a)
            c = 180 - a - b
            q = f"삼각형의 두 각이 {a}°, {b}°일 때 나머지 한 각 □는 몇 도인가요?"
            lines = [L("삼각형 세 각의 합 = 180°"), L(f"□ = 180° − {a}° − {b}° = {c}°")]
            plan, labels = "세 각의 합 180°에서 아는 두 각을 빼요", (f"{a}°", f"{b}°", "□")
        elif k < 16:
            a = 90; b = R.randint(20, 70); c = 90 - b
            q = f"직각삼각형의 한 각이 {b}°일 때 직각이 아닌 다른 한 각 □는 몇 도인가요?"
            lines = [L("삼각형 세 각의 합 = 180°", memo="직각 = 90°"), L(f"□ = 180° − 90° − {b}° = {c}°")]
            plan, labels = "직각은 90°", (None, f"{b}°", "□")
        else:
            top = R.randrange(20, 141, 2)
            a = b = (180 - top) // 2
            c = top
            q = f"두 각의 크기가 같은 삼각형에서 나머지 한 각이 {top}°일 때, 크기가 같은 한 각 □는 몇 도인가요?"
            lines = [L("크기가 같은 두 각의 합", memo="180°에서 빼요"), L(f"180° − {top}° = {180 - top}°"), L(f"□ = {180 - top}° ÷ 2 = {a}°")]
            plan, labels = "남는 각을 둘로 똑같이 나눠요", ("□", "□", f"{top}°")
        A, B, C = tri_pts(a, b)
        f.poly([A, B, C], c="ink", w=4)
        cols = ["gold", "gold", "teal"]
        for (V, P, Q), lab, col in zip(((A, B, C), (B, C, A), (C, A, B)), labels, cols):
            if lab is None:
                angle_mark(f, V, P, Q, r=40, c="gold")
            else:
                angle_mark(f, V, P, Q, r=58, label=lab, c="teal" if lab == "□" else "gold", f_="teal" if lab == "□" else "gold", z=40 if lab == "□" else 28)
        S.add(3, q, f"{c if k < 16 else a}°", plan, lines, f.out(), ap=str(c if k < 16 else a), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.randint(60, 130); b = R.randint(60, 130); c = R.randint(60, 130)
        d = 360 - a - b - c
        if not (55 <= d <= 150):
            return
        P = quad_pts([a, b, c, d], R)
        if not P:
            return
        f = Fig()
        f.poly(P, c="ink", w=4)
        f.line(*P[0], *P[2], at=0, c="soft", w=3, d=True)
        labs = [f"{a}°", f"{b}°", f"{c}°", "□"]
        for i in range(4):
            V, A_, B_ = P[i], P[(i + 1) % 4], P[(i - 1) % 4]
            angle_mark(f, V, A_, B_, r=52, label=labs[i], c="teal" if labs[i] == "□" else "gold", f_="teal" if labs[i] == "□" else "gold", z=40 if labs[i] == "□" else 28)
        S.add(4, f"사각형의 세 각이 {a}°, {b}°, {c}°일 때 나머지 한 각 □는 몇 도인가요?", f"{d}°", "네 각의 합 360°에서 아는 세 각을 빼요",
              [L("사각형 네 각의 합 = 360°", memo="삼각형 2개 = 180° × 2"), L(f"□ = 360° − {a}° − {b}° − {c}° = {d}°")], f.out(), ap=str(d), key=f"{a},{b},{c}")
    fill(S, 4, 20, g4)

    def g5():
        half = S.count(5) >= 11
        h = R.randint(1, 11)
        f = Fig()
        cx, cy, rr = 330, 330, 250
        f.circ(cx, cy, rr, c="ink", sw=4)
        for i in range(12):
            ang = 90 - 30 * i
            p1, p2 = ang_pt(cx, cy, rr - 6, ang), ang_pt(cx, cy, rr - 26, ang)
            f.line(*p1, *p2, c="ink", w=4)
            tx, ty = ang_pt(cx, cy, rr - 58, ang)
            f.text(tx, ty + 12, str(12 if i == 0 else i), z=34, c="soft", ho=False)
        hpos = h + (0.5 if half else 0)
        mpos = 6 if half else 0
        ha, ma = 90 - 30 * hpos, 90 - 30 * mpos
        f.line(cx, cy, *ang_pt(cx, cy, rr * 0.55, ha), c="ink", w=9)
        f.line(cx, cy, *ang_pt(cx, cy, rr * 0.8, ma), c="ink", w=5)
        f.dot(cx, cy, r=10, f="ink")
        diff = abs(hpos - mpos)
        sm = min(diff, 12 - diff)
        deg = int(round(30 * sm))
        # 작은 쪽 호
        a0, a1 = (ha, ma) if ((ma - ha) % 360) <= 180 else (ma, ha)
        f.arc(cx, cy, 90, a0, a0 + ((a1 - a0) % 360), at=len([0, 0]) if not half else 1, c="gold", sw=4, f="gold", fo=0.25, hl=True)
        if half:
            whole = int(sm)
            q = f"{h}시 30분일 때 시계의 긴바늘과 짧은바늘이 이루는 작은 쪽의 각은 몇 도인가요?"
            lines = [L(f"짧은바늘은 {h}와 {h + 1 if h < 12 else 1}의 한가운데", memo="30분 → 반 칸"), L(f"작은 쪽은 {whole}칸 반" if whole else "작은 쪽은 반 칸"),
                     L(f"30° × {whole} + 15° = {deg}°" if whole else f"30° ÷ 2 = {deg}°")]
            plan = "한 칸 30° · 반 칸 15°"
        else:
            q = f"{h}시일 때 시계의 긴바늘과 짧은바늘이 이루는 작은 쪽의 각은 몇 도인가요?"
            k = int(sm)
            lines = [L("한 칸 = 360° ÷ 12 = 30°", memo="숫자 12칸"), L(f"작은 쪽은 {k}칸"), L(f"30° × {k} = {deg}°")]
            plan = "숫자 사이 한 칸이 몇 도인지 먼저"
        S.add(5, q, f"{deg}°", plan, lines, f.out(), ap=str(deg), key=q)
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "e4", "grade": "초4", "level": "초등", "icon": "📐", "title": "초4 · 분수의 덧셈과 뺄셈 · 각도",
         "desc": "분모가 같은 분수의 덧셈과 뺄셈 100제(분수 막대) · 각도 100제(직선 180° · 삼각형 180° · 사각형 360° · 시계).",
         "thumb": ("b", 50), "sets": [set_a, set_b]}
