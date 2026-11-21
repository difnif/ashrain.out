# 중3 · 고3 채우기 — 통계(대푯값 · 산포도 · 산점도와 상관관계) · 공간도형과 공간좌표
import math
from fractions import Fraction as Fr
from core import *
from fig import Fig, Plane
from kit import *

def DEC(v):
    v = Fr(v).limit_denominator(100000)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{float(v):g}"

def SURD(n):
    """√n 을 a√{b} 꼴로 — n 은 0 이상의 정수"""
    if n == 0:
        return "0"
    a, b = 1, n
    k = 2
    while k * k <= b:
        while b % (k * k) == 0:
            a *= k
            b //= k * k
        k += 1
    if b == 1:
        return str(a)
    return f"{'' if a == 1 else a}√{{{b}}}"

def SURDP(n):
    s = SURD(n)
    return s.replace("√{", "√").replace("}", "")


# ══════════ 통계(중3) ══════════
SUBJ = [("수학", "영어"), ("국어", "사회"), ("키", "몸무게"), ("공부 시간", "게임 시간"), ("운동 시간", "휴대폰 사용 시간")]
def stat3():
    S = Set("stat3", "통계 — 평균 · 편차 · 분산 · 산점도와 상관관계", "통계",
            {1: "평균과 자료", 2: "편차로 자료 구하기", 3: "편차로 분산 · 표준편차", 4: "자료를 바꾸면", 5: "산점도와 상관관계"},
            pp=8,
            tips={1: "(평균) × (개수) = (자료의 합)",
                  2: "편차의 합은 0 — 자료 = 평균 + 편차",
                  3: "분산 = (편차)²의 평균, 표준편차 = √{분산}",
                  4: "모든 자료에 a를 더하면 평균만 a 늘고 분산은 그대로, k배 하면 표준편차도 |k|배",
                  5: "오른쪽 위로 향하면 양의 상관관계, 오른쪽 아래로 향하면 음의 상관관계"},
            note="편차의 합이 0이라는 사실 하나로 모르는 편차를 찾을 수 있어요. 분산을 구할 때는 편차를 먼저 표로 정리하고 제곱해 더하게 해 주세요.")
    R = rng(5701)

    def g1():
        t = R.randrange(3)
        n = R.randint(4, 8)
        m = R.randint(50, 90)
        if t == 0:
            x = R.randint(40, 100)
            tot = m * n + x
            if tot % (n + 1):
                return
            q = f"학생 {n}명의 점수의 평균이 {m}점이에요. 점수가 {x}점인 학생 한 명이 더 들어오면 {n + 1}명의 평균은 몇 점인가요?"
            lines = [L(f"{n}명의 합 = {m} × {n} = {m * n}"), L(f"{n + 1}명의 합 = {m * n} + {x} = {tot}"), L(f"평균 = {tot} ÷ {n + 1} = {tot // (n + 1)}")]
            S.add(1, q, f"{tot // (n + 1)}점", "평균 × 개수 = 합", lines, None, ap=str(tot // (n + 1)), key=q)
        elif t == 1:
            m2 = m + R.randint(1, 4)
            x = m2 * (n + 1) - m * n
            if not (0 < x <= 100):
                return
            q = f"학생 {n}명의 점수의 평균이 {m}점이에요. 한 명이 더 시험을 보아 {n + 1}명의 평균이 {m2}점이 되려면, 이 학생은 몇 점을 받아야 하나요?"
            lines = [L(f"{n + 1}명의 합 = {m2} × {n + 1} = {m2 * (n + 1)}"), L(f"{n}명의 합 = {m} × {n} = {m * n}"), L(f"{m2 * (n + 1)} − {m * n} = {x}")]
            S.add(1, q, f"{x}점", "목표 합 − 지금 합", lines, None, ap=str(x), key=q)
        else:
            data = [R.randint(40, 100) for _ in range(n - 1)]
            tot = m * n
            x = tot - sum(data)
            if not (0 <= x <= 100):
                return
            q = f"자료 {', '.join(map(str, data))}, x의 평균이 {m}일 때, x의 값은?"
            lines = [L(f"자료의 합 = {m} × {n} = {tot}"), L(f"x = {tot} − ({' + '.join(map(str, data))}) = {x}")]
            S.add(1, q, str(x), "평균 × 개수 = 합", lines, None, key=q)
    fill(S, 1, 20, g1)

    def g2():
        n = R.randint(4, 6)
        m = R.randint(10, 80)
        while True:
            dev = [R.randint(-6, 6) for _ in range(n - 1)]
            last = -sum(dev)
            if -8 <= last <= 8:
                break
        dev.append(last)
        names = "ABCDEF"[:n]
        k = R.randrange(n)
        known = ", ".join(f"{names[i]} {N(dev[i])}" for i in range(n) if i != k)
        val = m + dev[k]
        q = f"{n}명의 몸무게의 평균이 {m} kg이고, 편차가 {known}일 때, {names[k]}의 몸무게는 몇 kg인가요?"
        kn = [dev[i] for i in range(n) if i != k]
        expr = " + ".join(f"({N(x)})" if x < 0 else str(x) for x in kn)
        lines = [L(f"편차의 합은 0 → {names[k]}의 편차 = −({expr}) = {N(dev[k])}"), L((f"{m} + {dev[k]}" if dev[k] >= 0 else f"{m} − {-dev[k]}") + f" = {val}", memo="자료 = 평균 + 편차")]
        S.add(2, q, f"{val} kg", "편차의 합은 0", lines, None, ap=str(val), key=q)
    fill(S, 2, 20, g2)

    def g3():
        n = R.randint(4, 6)
        while True:
            dev = [R.randint(-5, 5) for _ in range(n - 1)]
            last = -sum(dev)
            if -6 <= last <= 6:
                dev.append(last)
                break
        ss = sum(x * x for x in dev)
        var = Fr(ss, n)
        want = R.choice(["분산", "표준편차"])
        if want == "표준편차" and var.denominator != 1:
            return
        q = f"편차가 {', '.join(N(x) for x in dev)}인 자료의 {eun(want)} 얼마인가요?"
        sq = " + ".join(f"({N(x)})^{{2}}" if x < 0 else f"{x}^{{2}}" for x in dev)
        lines = [L(f"(편차)²의 합 = {sq} = {ss}"), L(f"분산 = {ss} ÷ {n} = {N(var) if var.denominator == 1 else f'{{{var.numerator}/{var.denominator}}}'}")]
        if want == "분산":
            ans = N(var) if var.denominator == 1 else f"{{{var.numerator}/{var.denominator}}}"
            S.add(3, q, ans, "(편차)²의 평균", lines, None, ap=ans.strip("{}"), key=q)
        else:
            v = var.numerator
            sd = SURD(v)
            lines.append(L(f"표준편차 = √{{{v}}}" + (f" = {sd}" if sd != f"√{{{v}}}" else "")))
            S.add(3, q, sd, "표준편차 = √{분산}", lines, None, ap=SURDP(v), omr="ex" if "√" in sd else "num", key=q)
    fill(S, 3, 20, g3)

    def g4():
        m, v = R.randint(10, 90), R.choice([4, 9, 16, 25, 36, 2, 3, 5, 8])
        t = R.randrange(3)
        a = R.randint(2, 10) * R.choice([1, -1])
        k = R.randint(2, 5)
        sd = SURD(v)
        if t == 0:
            q = f"평균이 {m}, 분산이 {v}인 자료의 모든 값에 {N(a)}을(를) 더했어요. 새 자료의 평균과 분산을 차례로 구하세요."
            q = q.replace(f"{N(a)}을(를)", J(N(a), "을", "를"))
            lines = [L(f"평균 {m} + ({N(a)}) = {m + a}", memo="모두 같은 만큼 움직여요"), L(f"분산 {v} 그대로", memo="흩어진 정도는 그대로")]
            S.add(4, q, f"{m + a}, {v}", "더하면 평균만 바뀌어요", lines, None, ap=f"{m + a}, {v}", omr="ex", key=q)
        elif t == 1:
            q = f"평균이 {m}, 표준편차가 {sd}인 자료의 모든 값을 {k}배 했어요. 새 자료의 평균과 표준편차를 차례로 구하세요."
            nsd = SURD(v * k * k)
            lines = [L(f"평균 {m} × {k} = {m * k}"), L(f"표준편차 {sd} × {k} = {nsd}", memo="표준편차도 k배")]
            S.add(4, q, f"{m * k}, {nsd}", "k배 하면 평균 · 표준편차 모두 k배", lines, None, ap=f"{m * k}, {SURDP(v * k * k)}", omr="ex", key=q)
        else:
            q = f"분산이 {v}인 자료의 모든 값을 {k}배 한 다음 {N(a)}을(를) 더했어요. 새 자료의 분산은 얼마인가요?"
            q = q.replace(f"{N(a)}을(를)", J(N(a), "을", "를"))
            lines = [L(f"{k}배 → 분산은 {k}^{{2}}배", memo="표준편차가 k배라서"), L(f"{v} × {k * k} = {v * k * k}"), L(f"{N(a)}을(를) 더해도 분산은 그대로".replace(f"{N(a)}을(를)", J(N(a), "을", "를")))]
            S.add(4, q, str(v * k * k), "분산은 k^{2}배, 더한 값은 영향 없음", lines, None, key=q)
    fill(S, 4, 20, g4)

    class Box:
        def __init__(s_, lo=40, hi=100, box=(130, 110, 590, 540)):
            s_.lo, s_.hi, s_.b = lo, hi, box
        def X(s_, v):
            x0, y0, x1, y1 = s_.b
            return x0 + (v - s_.lo) / (s_.hi - s_.lo) * (x1 - x0)
        def Y(s_, v):
            x0, y0, x1, y1 = s_.b
            return y1 - (v - s_.lo) / (s_.hi - s_.lo) * (y1 - y0)

    def scatter(f, pts, xn, yn, at="q", line=None):
        pl = Box()
        x0, y0, x1, y1 = pl.b
        for v in range(40, 101, 10):
            f.line(pl.X(v), y0, pl.X(v), y1, c="soft", w=1, o=0.35, at=at)
            f.line(x0, pl.Y(v), x1, pl.Y(v), c="soft", w=1, o=0.35, at=at)
            f.text(pl.X(v), y1 + 30, str(v), z=20, c="soft", at=at)
            f.text(x0 - 10, pl.Y(v) + 7, str(v), z=20, c="soft", a="e", at=at)
        f.line(x0, y1, x1 + 30, y1, c="ink", w=3, ar=1, at=at)
        f.line(x0, y1, x0, y0 - 30, c="ink", w=3, ar=1, at=at)
        f.text(x1 + 10, y1 + 62, f"{xn}", z=22, b=700, at=at, a="e")
        f.text(x0 + 10, y0 - 40, f"{yn}", z=22, b=700, at=at, a="s")
        for (x, y) in pts:
            f.dot(pl.X(x), pl.Y(y), r=8, at=at)
        if line:
            x0, y0, x1, y1 = line
            f.line(pl.X(x0), pl.Y(y0), pl.X(x1), pl.Y(y1), c="gold", w=3, d=True, at=0)
        return pl

    def g5():
        xn, yn = R.choice(SUBJ)
        n = R.randint(10, 14)
        t = R.randrange(3)
        f = Fig()
        if t == 0:
            kind = R.choice(["양", "음", "없음"])
            pts = set()
            while len(pts) < n:
                x = R.randrange(45, 100, 5)
                if kind == "양":
                    y = x + R.randrange(-10, 11, 5)
                elif kind == "음":
                    y = 145 - x + R.randrange(-10, 11, 5)
                else:
                    y = R.randrange(45, 100, 5)
                if 40 < y < 100:
                    pts.add((x, y))
            pts = sorted(pts)
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            if kind == "없음":
                mx, my = sum(xs) / n, sum(ys) / n
                r = sum((a - mx) * (b - my) for a, b in pts) / math.sqrt(sum((a - mx) ** 2 for a in xs) * sum((b - my) ** 2 for b in ys))
                if abs(r) > 0.25:
                    return
            ans = {"양": "양의 상관관계", "음": "음의 상관관계", "없음": "상관관계가 없다"}[kind]
            q = f"학생 {n}명의 {wa(xn)} {yn}을(를) 조사해 산점도로 나타냈어요. 두 변량 사이에는 어떤 상관관계가 있나요?".replace(f"{yn}을(를)", J(yn, "을", "를"))
            scatter(f, pts, xn, yn, line=((45, 45, 95, 95) if kind == "양" else (45, 95, 95, 45) if kind == "음" else None))
            how = {"양": "점들이 오른쪽 위로 향하는 직선 가까이", "음": "점들이 오른쪽 아래로 향하는 직선 가까이", "없음": "점들이 어느 쪽으로도 기울지 않고 흩어져 있음"}[kind]
            lines = [L(how), L(ans)]
            S.add(5, q, ans, "점들이 늘어선 방향 보기", lines, f.out(), omr="ex", qfig=True, key=q + str(pts), dupq=True)
            return
        pts = set()
        while len(pts) < n:
            x = R.randrange(45, 100, 5)
            y = min(95, max(45, x + R.randrange(-20, 21, 5)))
            pts.add((x, y))
        pts = sorted(pts)
        if t == 1:
            c = R.choice([60, 65, 70, 75, 80])
            cnt = sum(1 for x, y in pts if x >= c and y >= c)
            q = f"학생 {n}명의 {wa(xn)} {yn}을(를) 조사한 산점도예요. 두 변량이 모두 {c} 이상인 학생은 몇 명인가요?".replace(f"{yn}을(를)", J(yn, "을", "를"))
            pl = scatter(f, pts, xn, yn)
            f.rect(pl.X(c) - 6, pl.Y(100), pl.X(100) - pl.X(c) + 6, pl.Y(c) - pl.Y(100) + 6, c="gold", sw=3, d=True, at=0)
            lines = [L(f"x ≥ {c}, y ≥ {c}인 영역의 점 세기", memo="경계 위의 점도 포함"), L(f"{cnt}명")]
            S.add(5, q, f"{cnt}명", "조건에 맞는 영역을 표시하고 세기", lines, f.out(), ap=str(cnt), qfig=True, key=q + str(pts), dupq=True)
        else:
            cnt = sum(1 for x, y in pts if x > y)
            q = f"학생 {n}명의 {wa(xn)} {yn}을(를) 조사한 산점도예요. {xn} 값이 {yn} 값보다 큰 학생은 몇 명인가요?".replace(f"{yn}을(를)", J(yn, "을", "를"))
            pl = scatter(f, pts, xn, yn, line=(40, 40, 100, 100))
            lines = [L("y = x인 직선을 긋고 그 아래쪽(x > y)의 점 세기", memo="직선 위의 점은 빼요"), L(f"{cnt}명")]
            S.add(5, q, f"{cnt}명", "대각선을 그어 아래쪽 세기", lines, f.out(), ap=str(cnt), qfig=True, key=q + str(pts), dupq=True)
    fill(S, 5, 20, g5)
    return S


# ══════════ 공간도형과 공간좌표(기하) ══════════
QUAD = [(1, 2, 2, 3), (2, 3, 6, 7), (1, 4, 8, 9), (4, 4, 7, 9), (2, 6, 9, 11), (6, 6, 7, 11), (3, 4, 12, 13), (2, 10, 11, 15), (1, 12, 12, 17), (8, 9, 12, 17), (2, 2, 1, 3), (4, 8, 1, 9)]
def P3(x, y, z):
    return f"({N(x)}, {N(y)}, {N(z)})"

def space3():
    S = Set("space3", "공간좌표 — 대칭점 · 거리 · 내분점 · 구 · 정사영", "공간좌표",
            {1: "대칭인 점", 2: "두 점 사이의 거리", 3: "선분의 내분점", 4: "구의 방정식", 5: "정사영"},
            pp=8,
            tips={1: "xy평면 대칭은 z의 부호만, x축 대칭은 y · z의 부호를, 원점 대칭은 모두 바꿔요",
                  2: "√{(x₂ − x₁)² + (y₂ − y₁)² + (z₂ − z₁)²}",
                  3: "m : n 내분점 = (mx₂ + nx₁) ÷ (m + n) — 성분마다",
                  4: "(x − a)² + (y − b)² + (z − c)² = r² — 완전제곱식으로 묶어 중심과 반지름",
                  5: "정사영의 길이 = l cos θ, 넓이 = S cos θ"},
            note="공간좌표는 평면좌표에 z 성분 하나가 더해졌을 뿐이에요. 공식마다 평면에서의 꼴을 먼저 떠올리고 성분을 하나 늘리게 해 주세요.")
    R = rng(5801)

    SYM = {"xy평면": (1, 1, -1), "yz평면": (-1, 1, 1), "zx평면": (1, -1, 1), "x축": (1, -1, -1), "y축": (-1, 1, -1), "z축": (-1, -1, 1), "원점": (-1, -1, -1)}
    def g1():
        p = [R.randint(-6, 6) for _ in range(3)]
        if 0 in p:
            return
        k = R.choice(list(SYM))
        s = SYM[k]
        r = [a * b for a, b in zip(p, s)]
        q = f"점 P{P3(*p)}을 {k}에 대하여 대칭이동한 점의 좌표를 구하세요." if k != "원점" else f"점 P{P3(*p)}을 원점에 대하여 대칭이동한 점의 좌표를 구하세요."
        keep = {"xy평면": "x, y는 그대로, z의 부호만", "yz평면": "y, z는 그대로, x의 부호만", "zx평면": "z, x는 그대로, y의 부호만",
                "x축": "x는 그대로, y와 z의 부호를", "y축": "y는 그대로, z와 x의 부호를", "z축": "z는 그대로, x와 y의 부호를", "원점": "x, y, z의 부호를 모두"}[k]
        lines = [L(f"{k} 대칭 → {keep} 바꿔요"), L(f"{P3(*p)} → {P3(*r)}")]
        S.add(1, q, P3(*r), "대칭인 대상에 들어 있는 성분은 그대로", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        if R.random() < 0.6:
            a, b, c, d = R.choice(QUAD)
            sg = [R.choice([1, -1]) for _ in range(3)]
            dv = [a * sg[0], b * sg[1], c * sg[2]]
            R.shuffle(dv)
            p = [R.randint(-5, 5) for _ in range(3)]
            q2 = [x + y for x, y in zip(p, dv)]
            ans = str(d)
            dd = d * d
        else:
            p = [R.randint(-5, 5) for _ in range(3)]
            q2 = [R.randint(-5, 5) for _ in range(3)]
            dv = [y - x for x, y in zip(p, q2)]
            dd = sum(x * x for x in dv)
            if dd == 0:
                return
            ans = SURD(dd)
        q = f"두 점 A{P3(*p)}, B{P3(*q2)} 사이의 거리를 구하세요."
        terms = " + ".join(f"({N(x)})^{{2}}" if x < 0 else f"{x}^{{2}}" for x in dv)
        lines = [L("성분마다 차: " + ", ".join(f"{N(y)} − ({N(x)}) = {N(y - x)}" if x < 0 else f"{N(y)} − {x} = {N(y - x)}" for x, y in zip(p, q2))),
                 L(f"AB = √{{{terms}}} = √{{{dd}}}" + (f" = {ans}" if ans != f"√{{{dd}}}" else ""))]
        S.add(2, q, ans, "성분마다 차를 제곱해 더하고 √", lines, None, ap=SURDP(dd), omr="ex" if "√" in ans else "num", key=q)
    fill(S, 2, 20, g2)

    def g3():
        m, n = R.choice([(1, 1), (1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2)])
        a = [R.randint(-6, 6) for _ in range(3)]
        b = [R.randint(-6, 6) for _ in range(3)]
        if a == b:
            return
        pts = [Fr(m * y + n * x, m + n) for x, y in zip(a, b)]
        if any(v.denominator != 1 for v in pts):
            return
        pts = [int(v) for v in pts]
        what = "중점" if m == n else f"{m} : {n}으로 내분하는 점"
        q = f"두 점 A{P3(*a)}, B{P3(*b)}에 대하여 선분 AB를 {what}의 좌표를 구하세요." if m != n else f"두 점 A{P3(*a)}, B{P3(*b)}에 대하여 선분 AB의 중점의 좌표를 구하세요."
        lines = []
        for x, y, v, nm in zip(a, b, pts, "xyz"):
            py = N(y) if y >= 0 else f"({N(y)})"
            px = N(x) if x >= 0 else f"({N(x)})"
            lines.append(L(f"{{{m} × {py} + {n} × {px}/{m + n}}} = {N(v)}" if m != n else f"{{{N(x)} + {py}/2}} = {N(v)}", pre=f"{nm} 성분"))
        lines.append(L(P3(*pts)))
        S.add(3, q, P3(*pts), "성분마다 가중 평균", lines, None, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        c = [R.randint(-5, 5) for _ in range(3)]
        r = R.randint(1, 7)
        t = R.randrange(3)
        if t == 0:
            D = c[0] ** 2 + c[1] ** 2 + c[2] ** 2 - r * r
            coef = [-2 * v for v in c]
            eq = "x^{2} + y^{2} + z^{2}"
            for v, nm in zip(coef, "xyz"):
                if v:
                    eq += f" {'+' if v > 0 else '−'} {abs(v) if abs(v) != 1 else ''}{nm}"
            if D:
                eq += f" {'+' if D > 0 else '−'} {abs(D)}"
            eq += " = 0"
            q = f"구 {eq}의 중심의 좌표와 반지름의 길이를 차례로 구하세요."
            parts = []
            for v, nm in zip(c, "xyz"):
                parts.append(f"({nm} {'−' if v > 0 else '+'} {abs(v)})^{{2}}" if v else f"{nm}^{{2}}")
            lines = [L(f"{' + '.join(parts)} = {r * r}", memo="완전제곱식으로 묶기"), L(f"중심 {P3(*c)}, 반지름 {r}")]
            S.add(4, q, f"{P3(*c)}, {r}", "완전제곱식으로 묶기", lines, None, omr="ex", key=q)
        elif t == 1:
            pl = R.choice(["xy평면", "yz평면", "zx평면"])
            idx = {"xy평면": 2, "yz평면": 0, "zx평면": 1}[pl]
            dist = abs(c[idx])
            if dist >= r:
                return
            rr = r * r - dist * dist
            ans = SURD(rr)
            q = f"중심이 {P3(*c)}이고 반지름의 길이가 {r}인 구가 {pl}과 만나서 생기는 원의 반지름의 길이를 구하세요."
            lines = [L(f"중심에서 {pl}까지의 거리 = |{N(c[idx])}| = {dist}"), L(f"√{{{r}^{{2}} − {dist}^{{2}}}} = √{{{rr}}}" + (f" = {ans}" if ans != f"√{{{rr}}}" else ""), memo="피타고라스 정리")]
            S.add(4, q, ans, "중심과 평면 사이 거리 → 피타고라스", lines, None, ap=SURDP(rr), omr="ex" if "√" in ans else "num", key=q)
        else:
            pl = R.choice(["xy평면", "yz평면", "zx평면"])
            idx = {"xy평면": 2, "yz평면": 0, "zx평면": 1}[pl]
            if c[idx] == 0:
                return
            rr = abs(c[idx])
            q = f"중심이 {P3(*c)}이고 {pl}에 접하는 구의 반지름의 길이를 구하세요."
            lines = [L(f"{pl}에 접한다 → 반지름 = 중심에서 {pl}까지의 거리"), L(f"|{N(c[idx])}| = {rr}")]
            S.add(4, q, str(rr), "접하면 반지름 = 중심과 평면 사이 거리", lines, None, key=q)
    fill(S, 4, 20, g4)

    COS = {30: (Fr(1, 2), 3, "{√{3}/2}"), 45: (Fr(1, 2), 2, "{√{2}/2}"), 60: (Fr(1, 2), 1, "{1/2}")}
    def g5():
        th = R.choice([30, 45, 60])
        what = R.choice(["길이", "넓이"])
        l = 2 * R.randint(1, 10)
        if th == 60:
            v = N(Fr(l, 2))
            ap = v
        else:
            k = 3 if th == 30 else 2
            v = f"{'' if l // 2 == 1 else l // 2}√{{{k}}}"
            ap = v.replace("√{", "√").replace("}", "")
        if what == "길이":
            q = f"길이가 {l}인 선분 AB가 평면 α와 이루는 각의 크기가 {th}°일 때, 선분 AB의 평면 α 위로의 정사영의 길이를 구하세요."
            lines = [L(f"정사영의 길이 = {l} cos {th}°", memo="l cos θ"), L(f"{l} × {COS[th][2]} = {v}")]
        else:
            q = f"넓이가 {l}인 삼각형이 평면 α와 이루는 각의 크기가 {th}°일 때, 이 삼각형의 평면 α 위로의 정사영의 넓이를 구하세요."
            lines = [L(f"정사영의 넓이 = {l} cos {th}°", memo="S cos θ"), L(f"{l} × {COS[th][2]} = {v}")]
        S.add(5, q, v, f"정사영의 {what} = (처음 {what}) × cos θ", lines, None, ap=ap, omr="ex" if "√" in v else "num", key=q)
    fill(S, 5, 20, g5)
    return S
