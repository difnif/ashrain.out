# 중등 ② — 원과 부채꼴 · 입체도형 · 대푯값과 산포도 · 순환소수 · 다항식의 계산 · 일차부등식
import math
from math import gcd
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, ang_pt, NL
from kit import *

def bat(x):
    from core import _has_batchim
    return _has_batchim(str(x))

def F_(n, d):
    return "{%d/%d}" % (n, d)

def PI(v):
    """π 의 계수 → '12π' · '{25/2}π' · 'π'"""
    v = Fr(v)
    if v == 1:
        return "π"
    return N(v) + "π"

def ell(cx, cy, rx, ry, a0=0, a1=360, n=48):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cy - ry * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


# ══════════ 원과 부채꼴 ══════════
def sector_fig(f, th, r_lab=None, at="q", fill_at="q", cx=330, cy=360, R0=230, a0=None):
    a0 = 90 - th / 2 if a0 is None else a0
    A, B = ang_pt(cx, cy, R0, a0), ang_pt(cx, cy, R0, a0 + th)
    f.arc(cx, cy, R0, a0, a0 + th, c="ink", sw=3.5, f="gold", fo=0.25, at=at)
    f.line(cx, cy, *A, c="ink", w=3, at=at)
    f.line(cx, cy, *B, c="ink", w=3, at=at)
    f.arc(cx, cy, 44, a0, a0 + th, c="teal", sw=3, at=at)
    m = ang_pt(cx, cy, 80, a0 + th / 2)
    f.text(m[0], m[1] + 10, f"{th}°", z=26, c="teal", b=700, at=at)
    if r_lab:
        mid = ((cx + A[0]) / 2, (cy + A[1]) / 2)
        f.text(mid[0] + 20, mid[1] + 30, r_lab, z=26, b=700, at=at)
    return A, B

def sector():
    S = Set("sector", "원과 부채꼴 — π로 나타내는 길이와 넓이", "원과 부채꼴",
            {1: "원의 둘레와 넓이", 2: "부채꼴의 호의 길이", 3: "부채꼴의 넓이", 4: "중심각 · 반지름 구하기", 5: "색칠한 부분"},
            mixed=True, pp=8,
            tips={1: "반지름 r인 원: 둘레 2πr, 넓이 πr^{2} — 원주율은 기호 π로 써요",
                  2: "호의 길이 = 2πr × {x/360} — 중심각에 정비례",
                  3: "넓이 = πr^{2} × {x/360} = {1/2}rl(l은 호의 길이)",
                  4: "구하는 것을 x로 두고 호의 길이(넓이) 식을 세워요",
                  5: "둘레는 곡선(호)과 직선(반지름)을 모두 더하고, 넓이는 큰 도형에서 빼거나 옮겨 붙여요"},
            note="부채꼴은 ‘원 전체의 {x/360}’이라는 한 가지 생각으로 호의 길이와 넓이를 모두 구하게 해 주세요. 넓이 = {1/2}rl은 부채꼴을 잘게 잘라 삼각형으로 보는 그림으로 설명하면 좋아요.")
    R = rng(1301)

    def g1():
        r = R.randint(2, 15)
        k = S.count(1) % 3
        f = Fig()
        f.circ(330, 340, 230, c="ink", sw=3.5, f="gold", fo=0.15)
        f.line(330, 340, 560, 340, c="teal", w=3)
        f.text(445, 326, f"{r} cm", z=26, c="teal", b=700)
        f.dot(330, 340, r=6)
        if k == 0:
            q = f"반지름이 {r} cm인 원의 둘레의 길이를 구하세요."
            lines = [L("둘레 = 2πr"), L(f"2 × π × {r} = {PI(2 * r)}"), L(f"{PI(2 * r)} cm")]
            ans, ap = f"{PI(2 * r)} cm", f"{2 * r}π"
        elif k == 1:
            q = f"반지름이 {r} cm인 원의 넓이를 구하세요."
            lines = [L("넓이 = πr^{2}"), L(f"π × {r}^{{2}} = {PI(r * r)}"), L(f"{PI(r * r)} cm²")]
            ans, ap = f"{PI(r * r)} cm²", f"{r * r}π"
        else:
            q = f"둘레의 길이가 {PI(2 * r)} cm인 원의 넓이를 구하세요."
            lines = [L(f"2πr = {PI(2 * r)} → r = {r}", memo="반지름부터"), L(f"π × {r}^{{2}} = {PI(r * r)}"), L(f"{PI(r * r)} cm²")]
            ans, ap = f"{PI(r * r)} cm²", f"{r * r}π"
        S.add(1, q, ans, "둘레 2πr · 넓이 πr^{2}", lines, f.out(), ap=ap, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        r = R.randint(2, 18)
        th = R.choice([30, 36, 40, 45, 60, 72, 90, 120, 135, 144, 150, 180, 210, 240, 270])
        l = Fr(2 * r * th, 360)
        f = Fig()
        sector_fig(f, th, f"{r} cm")
        q = f"반지름이 {r} cm이고 중심각의 크기가 {th}°인 부채꼴의 호의 길이를 구하세요."
        lines = [L(f"2π × {r} × {{{th}/360}}", memo="원 둘레의 {x/360}"), L(f"2π × {r} × {{{th}/360}} = {PI(l)}"), L(f"{PI(l)} cm")]
        S.add(2, q, f"{PI(l)} cm", "호의 길이 = 2πr × {x/360}", lines, f.out(), ap=plain(PI(l)), omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        r = R.randint(2, 16)
        th = R.choice([30, 36, 40, 45, 60, 72, 90, 120, 135, 144, 150, 180, 240, 270])
        A_ = Fr(r * r * th, 360)
        f = Fig()
        sector_fig(f, th, f"{r} cm")
        if k == 0:
            q = f"반지름이 {r} cm이고 중심각의 크기가 {th}°인 부채꼴의 넓이를 구하세요."
            lines = [L(f"π × {r}^{{2}} × {{{th}/360}}", memo="원 넓이의 {x/360}"), L(f"π × {r}^{{2}} × {{{th}/360}} = {PI(A_)}"), L(f"{PI(A_)} cm²")]
            plan = "넓이 = πr^{2} × {x/360}"
        else:
            l = Fr(2 * r * th, 360)
            q = f"반지름이 {r} cm이고 호의 길이가 {PI(l)} cm인 부채꼴의 넓이를 구하세요."
            lines = [L("넓이 = {1/2}rl", memo="중심각을 몰라도 돼요"), L(f"{{1/2}} × {r} × {PI(l)} = {PI(A_)}"), L(f"{PI(A_)} cm²")]
            plan = "반지름과 호의 길이를 알면 {1/2}rl"
        S.add(3, q, f"{PI(A_)} cm²", plan, lines, f.out(), ap=plain(PI(A_)), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        r = R.randint(2, 15)
        th = R.choice([30, 40, 45, 60, 72, 90, 120, 135, 150, 216, 240])
        l = Fr(2 * r * th, 360)
        A_ = Fr(r * r * th, 360)
        f = Fig()
        sector_fig(f, th, f"{r} cm" if k != 2 else "r")
        if k == 0:
            q = f"반지름이 {r} cm이고 호의 길이가 {PI(l)} cm인 부채꼴의 중심각의 크기를 구하세요."
            lines = [L(f"2π × {r} × {{x/360}} = {PI(l)}", memo="중심각을 x°로"), L(f"x = {th}")]
            ans, ap = f"{th}°", str(th)
            S.add(4, q, ans, "호의 길이 식에 x를 두고 풀어요", lines, f.out(), ap=ap, sub={"x": th}, key=q)
        elif k == 1:
            q = f"반지름이 {r} cm이고 넓이가 {PI(A_)} cm²인 부채꼴의 중심각의 크기를 구하세요."
            lines = [L(f"π × {r}^{{2}} × {{x/360}} = {PI(A_)}", memo="중심각을 x°로"), L(f"x = {th}")]
            S.add(4, q, f"{th}°", "넓이 식에 x를 두고 풀어요", lines, f.out(), ap=str(th), sub={"x": th}, key=q)
        else:
            q = f"중심각의 크기가 {th}°이고 호의 길이가 {PI(l)} cm인 부채꼴의 반지름의 길이를 구하세요."
            lines = [L(f"2π × r × {{{th}/360}} = {PI(l)}", memo="반지름을 r로"), L(f"r = {r}")]
            S.add(4, q, f"{r} cm", "호의 길이 식에 r을 두고 풀어요", lines, f.out(), ap=str(r), sub={"r": r}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        a = R.randint(2, 12) * 2
        f = Fig()
        if k == 0:
            f.rect(130, 140, 400, 400, c="ink", sw=3)
            f.arc(130, 540, 400, 0, 90, c="coral", sw=3.5, f="gold", fo=0.25)
            q = f"한 변이 {a} cm인 정사각형 안에, 한 꼭짓점을 중심으로 반지름이 {a} cm인 사분원을 그렸어요. 사분원의 둘레의 길이를 구하세요."
            arc_ = Fr(2 * a, 4)
            lines = [L(f"2π × {a} × {{1/4}} = {PI(arc_)}", pre="호", memo="원의 {1/4}"), L(f"{a} × 2 = {2 * a}", pre="반지름 두 개"), L(f"({PI(arc_)} + {2 * a}) cm")]
            ans, ap = f"({PI(arc_)} + {2 * a}) cm", f"{plain(PI(arc_))} + {2 * a}"
            plan = "둘레 = 호 + 반지름 두 개"
        elif k == 1:
            f.rect(130, 140, 400, 400, c="ink", sw=3, f="gold", fo=0.3)
            f.arc(130, 540, 400, 0, 90, c="ink", sw=3, f="paper", fo=1)
            q = f"한 변이 {a} cm인 정사각형에서, 한 꼭짓점을 중심으로 반지름이 {a} cm인 사분원을 뺀 부분의 넓이를 구하세요."
            qa = Fr(a * a, 4)
            lines = [L(f"{a} × {a} = {a * a}", pre="정사각형"), L(f"π × {a}^{{2}} × {{1/4}} = {PI(qa)}", pre="사분원"), L(f"({a * a} − {PI(qa)}) cm²")]
            ans, ap = f"({a * a} − {PI(qa)}) cm²", f"{a * a} − {plain(PI(qa))}"
            plan = "정사각형 − 사분원"
        elif k == 2:
            r1, r2 = sorted(R.sample(range(2, 13), 2))
            th = R.choice([45, 60, 90, 120, 150])
            f.arc(330, 500, 360, 90 - th / 2, 90 + th / 2, c="ink", sw=3, f="gold", fo=0.3)
            f.arc(330, 500, 360 * r1 / r2, 90 - th / 2, 90 + th / 2, c="ink", sw=3, f="paper", fo=1)
            f.line(330, 500, *ang_pt(330, 500, 360, 90 - th / 2), c="ink", w=3)
            f.line(330, 500, *ang_pt(330, 500, 360, 90 + th / 2), c="ink", w=3)
            q = f"중심각이 {th}°로 같고 반지름이 {r2} cm, {r1} cm인 두 부채꼴에서, 큰 부채꼴에서 작은 부채꼴을 뺀 부분의 넓이를 구하세요."
            A2, A1 = Fr(r2 * r2 * th, 360), Fr(r1 * r1 * th, 360)
            lines = [L(f"π × {r2}^{{2}} × {{{th}/360}} = {PI(A2)}", pre="큰 부채꼴"), L(f"π × {r1}^{{2}} × {{{th}/360}} = {PI(A1)}", pre="작은 부채꼴"), L(f"{PI(A2)} − {PI(A1)} = {PI(A2 - A1)}"), L(f"{PI(A2 - A1)} cm²")]
            ans, ap = f"{PI(A2 - A1)} cm²", plain(PI(A2 - A1))
            plan = "큰 부채꼴 − 작은 부채꼴"
        else:
            r = R.randint(2, 10)
            f.arc(330, 360, 240, 0, 180, c="ink", sw=3, f="gold", fo=0.3)
            f.arc(210, 360, 120, 180, 360, c="ink", sw=3, f="gold", fo=0.3)
            f.arc(450, 360, 120, 0, 180, c="ink", sw=3, f="paper", fo=1)
            q = f"지름이 {4 * r} cm인 반원과 지름이 {2 * r} cm인 반원 두 개로 만든 물결 모양 도형(넓이는 큰 반원과 같음)의 둘레의 길이를 구하세요."
            big = Fr(2 * (2 * r), 2)
            small = Fr(2 * r, 2) * 2
            lines = [L(f"π × {4 * r} × {{1/2}} = {PI(big)}", pre="큰 반원의 호"), L(f"π × {2 * r} × {{1/2}} × 2 = {PI(small)}", pre="작은 반원의 호 두 개"), L(f"{PI(big)} + {PI(small)} = {PI(big + small)}"), L(f"{PI(big + small)} cm")]
            ans, ap = f"{PI(big + small)} cm", plain(PI(big + small))
            plan = "둘레는 곡선 부분(호)만 모두 더해요"
        S.add(5, q, ans, plan, lines, f.out(), ap=ap, omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 입체도형 ══════════
def cyl_fig(f, r_lab, h_lab, cone=False, at="q"):
    cx, top, bot, rx, ry = 330, 150, 540, 190, 50
    if not cone:
        f.poly(ell(cx, top, rx, ry), c="ink", w=3, z=False, at=at)
        f.line(cx - rx, top, cx - rx, bot, c="ink", w=3, at=at)
        f.line(cx + rx, top, cx + rx, bot, c="ink", w=3, at=at)
    else:
        f.line(cx, top - 20, cx - rx, bot, c="ink", w=3, at=at)
        f.line(cx, top - 20, cx + rx, bot, c="ink", w=3, at=at)
        f.line(cx, top - 20, cx, bot, c="soft", w=2.5, d=True, at=at)
    f.poly(ell(cx, bot, rx, ry, 180, 360, 24), c="ink", w=3, z=False, at=at)
    f.poly(ell(cx, bot, rx, ry, 0, 180, 24), c="soft", w=2, z=False, d=True, at=at)
    f.line(cx, bot, cx + rx, bot, c="teal", w=3, at=at)
    f.text(cx + rx / 2, bot + 36, r_lab, z=26, c="teal", b=700, at=at)
    f.text(cx + rx + 16 if not cone else cx + 14, (top + bot) / 2, h_lab, z=26, b=700, a="s", at=at)

def solid():
    S = Set("solid", "입체도형 — 기둥 · 뿔 · 구의 겉넓이와 부피", "입체도형",
            {1: "기둥의 부피", 2: "원기둥의 겉넓이", 3: "뿔의 부피", 4: "원뿔의 겉넓이", 5: "구의 겉넓이와 부피"},
            mixed=True, pp=8,
            tips={1: "기둥의 부피 = 밑넓이 × 높이 — 원기둥은 πr^{2}h",
                  2: "원기둥의 겉넓이 = 밑넓이 × 2 + 옆넓이(2πr × h) — 옆면을 펼치면 직사각형",
                  3: "뿔의 부피 = {1/3} × 밑넓이 × 높이",
                  4: "원뿔의 옆면을 펼치면 부채꼴 — 옆넓이 = πrl(l은 모선)",
                  5: "구의 겉넓이 4πr^{2} · 부피 {4/3}πr^{3}"},
            note="겉넓이는 전개도를 떠올려 ‘밑면 + 옆면’으로, 부피는 ‘밑넓이 × 높이’(뿔은 {1/3})로 통일해서 생각하게 해 주세요.")
    R = rng(1302)

    def g1():
        k = S.count(1) % 3
        f = Fig()
        if k == 0:
            r, h = R.randint(2, 10), R.randint(3, 15)
            cyl_fig(f, f"{r} cm", f"{h} cm")
            V = r * r * h
            q = f"밑면의 반지름이 {r} cm, 높이가 {h} cm인 원기둥의 부피를 구하세요."
            lines = [L(f"π × {r}^{{2}} = {PI(r * r)}", pre="밑넓이"), L(f"{PI(r * r)} × {h} = {PI(V)}", memo="밑넓이 × 높이"), L(f"{PI(V)} cm³")]
            ans, ap = f"{PI(V)} cm³", plain(PI(V))
        elif k == 1:
            a, b, h = R.randint(3, 12), R.randint(3, 12), R.randint(3, 15)
            V = Fr(a * b, 2) * h
            if V.denominator != 1:
                return
            q = f"밑면이 두 변의 길이가 {a} cm, {b} cm인 직각삼각형이고 높이가 {h} cm인 삼각기둥의 부피를 구하세요."
            lines = [L(f"{{1/2}} × {a} × {b} = {N(Fr(a * b, 2))}", pre="밑넓이"), L(f"{N(Fr(a * b, 2))} × {h} = {N(V)}", memo="밑넓이 × 높이"), L(f"{N(V)} cm³")]
            ans, ap = f"{N(V)} cm³", N(V)
            f = None
        else:
            r, h = R.randint(2, 10), R.randint(3, 15)
            V = r * r * h
            cyl_fig(f, "r", f"{h} cm")
            q = f"높이가 {h} cm이고 부피가 {PI(V)} cm³인 원기둥의 밑면의 반지름의 길이를 구하세요."
            lines = [L(f"π × r^{{2}} × {h} = {PI(V)}", memo="밑넓이 × 높이"), L(f"r^{{2}} = {r * r}"), L(f"r = {r}")]
            S.add(1, q, f"{r} cm", "부피 식에 r을 두고 풀어요", lines, f.out(), ap=str(r), sub={"r": r}, key=q)
            return
        S.add(1, q, ans, "기둥의 부피 = 밑넓이 × 높이", lines, f.out() if f else None, ap=ap, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        r, h = R.randint(2, 10), R.randint(3, 15)
        f = Fig()
        cyl_fig(f, f"{r} cm", f"{h} cm")
        base, side = r * r, 2 * r * h
        T = 2 * base + side
        q = f"밑면의 반지름이 {r} cm, 높이가 {h} cm인 원기둥의 겉넓이를 구하세요."
        lines = [L(f"π × {r}^{{2}} × 2 = {PI(2 * base)}", pre="두 밑면"), L(f"2π × {r} × {h} = {PI(side)}", pre="옆넓이", memo="펼치면 가로 2πr, 세로 h"), L(f"{PI(2 * base)} + {PI(side)} = {PI(T)}"), L(f"{PI(T)} cm²")]
        S.add(2, q, f"{PI(T)} cm²", "두 밑면 + 옆면(직사각형)", lines, f.out(), ap=plain(PI(T)), omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        f = Fig()
        if k == 0:
            r, h = R.randint(2, 12), R.randint(3, 18)
            V = Fr(r * r * h, 3)
            cyl_fig(f, f"{r} cm", f"{h} cm", cone=True)
            q = f"밑면의 반지름이 {r} cm, 높이가 {h} cm인 원뿔의 부피를 구하세요."
            lines = [L(f"{{1/3}} × π × {r}^{{2}} × {h} = {PI(V)}", memo="같은 기둥의 {1/3}"), L(f"{PI(V)} cm³")]
            ans, ap = f"{PI(V)} cm³", plain(PI(V))
        else:
            a, h = R.randint(2, 12), R.randint(3, 18)
            V = Fr(a * a * h, 3)
            f = None
            q = f"밑면이 한 변 {a} cm인 정사각형이고 높이가 {h} cm인 사각뿔의 부피를 구하세요."
            lines = [L(f"{a} × {a} = {a * a}", pre="밑넓이"), L(f"{{1/3}} × {a * a} × {h} = {N(V)}"), L(f"{N(V)} cm³")]
            ans, ap = f"{N(V)} cm³", N(V)
        S.add(3, q, ans, "뿔의 부피 = {1/3} × 밑넓이 × 높이", lines, f.out() if f else None, ap=ap, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        r, l = R.randint(2, 10), R.randint(3, 16)
        if l <= r:
            return
        f = Fig()
        cyl_fig(f, f"{r} cm", f"모선 {l} cm", cone=True)
        base, side = r * r, r * l
        T = base + side
        q = f"밑면의 반지름이 {r} cm, 모선의 길이가 {l} cm인 원뿔의 겉넓이를 구하세요."
        lines = [L(f"π × {r}^{{2}} = {PI(base)}", pre="밑넓이"), L(f"π × {r} × {l} = {PI(side)}", pre="옆넓이", memo="펼친 부채꼴 = πrl"), L(f"{PI(base)} + {PI(side)} = {PI(T)}"), L(f"{PI(T)} cm²")]
        S.add(4, q, f"{PI(T)} cm²", "밑넓이 + 옆넓이(πrl)", lines, f.out(), ap=plain(PI(T)), omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        r = R.randint(1, 12)
        f = Fig()
        f.circ(330, 340, 220, c="ink", sw=3.5, f="sky", fo=0.12)
        f.poly(ell(330, 340, 220, 55, 180, 360, 24), c="ink", w=2.5, z=False)
        f.poly(ell(330, 340, 220, 55, 0, 180, 24), c="soft", w=2, z=False, d=True)
        f.line(330, 340, 550, 340, c="teal", w=3)
        f.text(440, 326, f"{r} cm", z=26, c="teal", b=700)
        if k == 0:
            T = 4 * r * r
            q = f"반지름이 {r} cm인 구의 겉넓이를 구하세요."
            lines = [L("겉넓이 = 4πr^{2}"), L(f"4π × {r}^{{2}} = {PI(T)}"), L(f"{PI(T)} cm²")]
            ans, ap = f"{PI(T)} cm²", plain(PI(T))
        elif k == 1:
            V = Fr(4 * r ** 3, 3)
            q = f"반지름이 {r} cm인 구의 부피를 구하세요."
            lines = [L("부피 = {4/3}πr^{3}"), L(f"{{4/3}}π × {r}^{{3}} = {PI(V)}"), L(f"{PI(V)} cm³")]
            ans, ap = f"{PI(V)} cm³", plain(PI(V))
        elif k == 2:
            T = 3 * r * r
            q = f"반지름이 {r} cm인 반구의 겉넓이를 구하세요. (잘린 면 포함)"
            lines = [L(f"4π × {r}^{{2}} × {{1/2}} = {PI(2 * r * r)}", pre="곡면", memo="구의 반"), L(f"π × {r}^{{2}} = {PI(r * r)}", pre="잘린 면(원)"), L(f"{PI(2 * r * r)} + {PI(r * r)} = {PI(T)}"), L(f"{PI(T)} cm²")]
            ans, ap = f"{PI(T)} cm²", plain(PI(T))
        else:
            V = Fr(2 * r ** 3, 3)
            q = f"반지름이 {r} cm인 반구의 부피를 구하세요."
            lines = [L(f"{{4/3}}π × {r}^{{3}} × {{1/2}} = {PI(V)}", memo="구의 부피의 반"), L(f"{PI(V)} cm³")]
            ans, ap = f"{PI(V)} cm³", plain(PI(V))
        S.add(5, q, ans, "구의 겉넓이 4πr^{2} · 부피 {4/3}πr^{3}", lines, f.out(), ap=ap, omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 대푯값과 산포도 ══════════
def dotplot(f, data, at="q", mark=None, mark_at=0, mean=None, mean_at=0):
    lo, hi = min(data), max(data)
    if hi - lo < 6:
        hi = lo + 6
    nl = NL(f, lo - 1, hi + 1, y=500, lab_step=1 if hi - lo <= 12 else 2, z=22)
    cnt = {}
    for v in sorted(data):
        cnt[v] = cnt.get(v, 0) + 1
        f.dot(nl.X(v), 500 - 34 * cnt[v], r=12, f="teal", at=at)
    if mark is not None:
        f.line(nl.X(mark), 520, nl.X(mark), 220, c="gold", w=3, d=True, at=mark_at)
    if mean is not None:
        f.poly([(nl.X(float(mean)), 520), (nl.X(float(mean)) - 14, 548), (nl.X(float(mean)) + 14, 548)], c="coral", w=2, f="coral", fo=0.8, at=mean_at)
    return nl

def stat():
    S = Set("stat", "대푯값과 산포도 — 평균 · 중앙값 · 최빈값 · 분산", "대푯값·산포도",
            {1: "중앙값", 2: "최빈값과 대푯값", 3: "상대도수", 4: "편차와 분산", 5: "표준편차"},
            pp=8,
            tips={1: "크기순으로 늘어놓아 한가운데 — 개수가 짝수면 가운데 두 값의 평균",
                  2: "가장 많이 나온 값이 최빈값(여러 개일 수도). 극단적인 값이 있으면 평균보다 중앙값이 대표로 알맞아요",
                  3: "상대도수 = 그 계급의 도수 ÷ 도수의 총합 — 상대도수의 합은 1",
                  4: "편차 = 자료 − 평균(편차의 합은 0) · 분산 = 편차의 제곱의 평균",
                  5: "표준편차 = √{분산} — 클수록 자료가 넓게 흩어져 있어요"},
            note="대푯값은 ‘자료를 대표하는 한 값’, 산포도는 ‘흩어진 정도’예요. 점 그림(점도표)에서 중앙값 · 최빈값 · 평균의 자리를 먼저 눈으로 찾게 하면 계산의 뜻이 분명해져요.")
    R = rng(1303)

    def g1():
        n = R.choice([5, 7, 9, 6, 8, 10])
        data = [R.randint(1, 20) for _ in range(n)]
        s = sorted(data)
        if n % 2:
            med = Fr(s[n // 2])
            mid = f"{(n + 1) // 2}번째 값 {s[n // 2]}"
            lines = [L(f"크기순: {', '.join(map(str, s))}"), L(f"{n}개 → {mid}", memo="한가운데"), L(f"중앙값 {N(med)}")]
        else:
            a, b = s[n // 2 - 1], s[n // 2]
            med = Fr(a + b, 2)
            lines = [L(f"크기순: {', '.join(map(str, s))}"), L(f"{n}개 → {n // 2}번째 · {n // 2 + 1}번째 값의 평균", memo="짝수 개"), L(f"({a} + {b}) ÷ 2 = {N(med)}")]
        if med.denominator not in (1, 2):
            return
        f = Fig()
        dotplot(f, data, mark=float(med), mark_at=len(lines) - 1)
        q = f"자료 {', '.join(map(str, data))}의 중앙값을 구하세요."
        S.add(1, q, DEC(med) if med.denominator == 2 else N(med), "크기순으로 늘어놓고 한가운데", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            n = R.randint(7, 11)
            mode = R.randint(2, 12)
            data = [mode] * R.randint(3, 4) + [R.randint(1, 15) for _ in range(n - 4)]
            from collections import Counter
            c = Counter(data)
            top = max(c.values())
            modes = sorted(v for v, t in c.items() if t == top)
            if len(modes) > 1:
                return
            R.shuffle(data)
            f = Fig()
            dotplot(f, data, mark=modes[0], mark_at=1)
            q = f"자료 {', '.join(map(str, data))}의 최빈값을 구하세요."
            lines = [L(f"{modes[0]}이 {top}번" if bat(modes[0]) else f"{modes[0]}가 {top}번", memo="가장 많이 나온 값"), L(f"최빈값 {modes[0]}")]
            S.add(2, q, str(modes[0]), "가장 많이 나온 값", lines, f.out(), key=q)
        else:
            n = R.randint(5, 7)
            base = [R.randint(10, 20) for _ in range(n - 1)]
            out = R.randint(70, 120)
            data = base + [out]
            R.shuffle(data)
            s = sorted(data)
            tot = sum(data)
            if tot % n:
                return
            mean = tot // n
            med = Fr(s[n // 2]) if n % 2 else Fr(s[n // 2 - 1] + s[n // 2], 2)
            if med.denominator != 1:
                return
            q = f"자료 {', '.join(map(str, data))}에서 평균과 중앙값 중 자료 전체를 대표하기에 더 알맞은 값은 어느 것이고, 그 값은 얼마인가요?"
            lines = [L(f"{' + '.join(map(str, data))} = {tot}", pre="합"), L(f"{tot} ÷ {n} = {mean}", pre="평균", memo=f"{out} 하나 때문에 커졌어요"), L(f"크기순 가운데 → {N(med)}", pre="중앙값"), L(f"극단적인 값 {out} → 중앙값 {N(med)}")]
            f = Fig()
            dotplot(f, data, mark=float(med), mark_at=2, mean=mean, mean_at=1)
            S.add(2, q, f"중앙값, {N(med)}", "극단적인 값이 있으면 중앙값이 대표로 알맞아요", lines, f.out(), ap=f"중앙값 {N(med)}", omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        T = R.choice([20, 25, 40, 50, 80, 100, 200])
        c = R.randint(1, T // 3)
        rf = Fr(c, T)
        if dp_ok(rf) is None:
            return
        if k == 0:
            q = f"도수의 총합이 {T}인 도수분포표에서 어떤 계급의 도수가 {c}일 때, 이 계급의 상대도수를 구하세요."
            lines = [L("상대도수 = 계급의 도수 ÷ 총합"), L(f"{c} ÷ {T} = {DEC(rf)}")]
            ans = DEC(rf)
        elif k == 1:
            q = f"도수의 총합이 {T}이고 어떤 계급의 상대도수가 {DEC(rf)}일 때, 이 계급의 도수를 구하세요."
            lines = [L("도수 = 총합 × 상대도수"), L(f"{T} × {DEC(rf)} = {c}")]
            ans = str(c)
        else:
            q = f"어떤 계급의 도수가 {c}이고 상대도수가 {DEC(rf)}일 때, 도수의 총합을 구하세요."
            lines = [L("총합 = 도수 ÷ 상대도수"), L(f"{c} ÷ {DEC(rf)} = {T}")]
            ans = str(T)
        S.add(3, q, ans, "상대도수 = 도수 ÷ 총합 — 세 가지로 바꿔 써요", lines, None, key=q)
    fill(S, 3, 20, g3)

    def nice_data(n, var_sq=False):
        for _ in range(400):
            m = R.randint(4, 15)
            devs = [R.randint(-4, 4) for _ in range(n - 1)]
            last = -sum(devs)
            if abs(last) > 5:
                continue
            devs.append(last)
            v = Fr(sum(d * d for d in devs), n)
            if v.denominator != 1 or v == 0:
                continue
            if var_sq and int(math.isqrt(int(v))) ** 2 != v:
                continue
            data = [m + d for d in devs]
            if min(data) < 1:
                continue
            return data, m, devs, int(v)
        return None

    def g4():
        n = R.choice([4, 5, 6])
        t = nice_data(n)
        if not t:
            return
        data, m, devs, v = t
        q = f"자료 {', '.join(map(str, data))}의 분산을 구하세요."
        lines = [L(f"({' + '.join(map(str, data))}) ÷ {n} = {m}", pre="평균"), L(f"편차: {', '.join(N(d) for d in devs)}", memo="자료 − 평균 (합은 0)"),
                 L(f"({' + '.join(f'{NP(d)}^{{2}}' for d in devs)}) ÷ {n} = {v}", pre="분산", memo="편차의 제곱의 평균")]
        f = Fig()
        dotplot(f, data, mean=m, mean_at=0)
        S.add(4, q, str(v), "평균 → 편차 → 편차의 제곱의 평균", lines, f.out(), key=q)
    fill(S, 4, 20, g4)

    def g5():
        n = R.choice([4, 5, 6, 8])
        t = nice_data(n, var_sq=True)
        if not t:
            return
        data, m, devs, v = t
        sd = math.isqrt(v)
        q = f"자료 {', '.join(map(str, data))}의 표준편차를 구하세요."
        lines = [L(f"({' + '.join(map(str, data))}) ÷ {n} = {m}", pre="평균"), L(f"({' + '.join(f'{NP(d)}^{{2}}' for d in devs)}) ÷ {n} = {v}", pre="분산"), L(f"√{{{v}}} = {sd}", pre="표준편차")]
        f = Fig()
        dotplot(f, data, mean=m, mean_at=0)
        S.add(5, q, str(sd), "분산을 구한 뒤 √", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S

def dp_ok(v):
    v = Fr(v)
    d = v.denominator
    while d % 2 == 0:
        d //= 2
    while d % 5 == 0:
        d //= 5
    return True if d == 1 else None


# ══════════ 순환소수 ══════════
def rep_dec(n, d):
    """n/d → (정수부, 비순환부, 순환마디) 문자열"""
    ip, r = divmod(n, d)
    seen, digs = {}, []
    while r and r not in seen:
        seen[r] = len(digs)
        r *= 10
        digs.append(str(r // d))
        r %= d
    if not r:
        return str(ip), "".join(digs), ""
    k = seen[r]
    return str(ip), "".join(digs[:k]), "".join(digs[k:])

def rep_str(ip, pre, cyc, times=3):
    return f"{ip}.{pre}{cyc * times}…"

def rec():
    S = Set("rec", "유리수와 순환소수 — 순환마디와 분수", "순환소수",
            {1: "순환마디", 2: "유한소수로 나타낼 수 있는 분수", 3: "순환소수를 분수로 ①", 4: "순환소수를 분수로 ②", 5: "소수점 아래 n번째 숫자"},
            mixed=True, pp=10,
            tips={1: "소수점 아래에서 같은 숫자의 배열이 한없이 되풀이되는 한 부분이 순환마디",
                  2: "기약분수로 고친 뒤 분모의 소인수가 2나 5뿐이면 유한소수",
                  3: "순환마디가 소수점 바로 뒤에서 시작하면 — 분모는 순환마디 자리 수만큼 9",
                  4: "순환하지 않는 자리가 있으면 — 분모는 9 뒤에 그 자리 수만큼 0, 분자는 (전체 − 순환하지 않는 부분)",
                  5: "순환마디가 k자리면 n을 k로 나눈 나머지 자리의 숫자"},
            note="순환소수를 분수로 바꾸는 방법은 x로 놓고 10의 거듭제곱을 곱해 빼는 과정을 한두 번 직접 보여 준 뒤 공식으로 정리하게 해 주세요.")
    R = rng(1304)

    def g1():
        d = R.choice([3, 6, 7, 9, 11, 12, 13, 15, 22, 27, 33, 37, 41, 44, 45, 55, 74, 90, 99, 101, 111])
        n = R.randint(1, 3 * d)
        if gcd(n, d) != 1 or n % d == 0:
            return
        ip, pre, cyc = rep_dec(n, d)
        if not cyc or len(cyc) > 6:
            return
        q = f"순환소수 {rep_str(ip, pre, cyc)}의 순환마디를 구하세요."
        lines = [L(f"소수점 아래: {pre + cyc * 3}…", memo="되풀이되는 부분 찾기"), L(f"되풀이되는 숫자의 배열 {cyc}" + (f" (앞의 {pre}는 순환하지 않음)" if pre else "")), L(f"순환마디 {cyc}")]
        S.add(1, q, cyc, "처음으로 되풀이가 시작되는 곳부터 한 묶음", lines, None, ap=cyc, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            d = R.choice([12, 14, 15, 18, 20, 24, 28, 30, 35, 36, 40, 42, 45, 48, 50, 56, 60, 70, 75, 80, 84, 90, 96, 120, 125, 140, 150, 160])
            n = R.randint(1, d - 1)
            g = gcd(n, d)
            rn, rd = n // g, d // g
            fin = dp_ok(Fr(n, d)) is not None
            pf_ = []
            x = rd
            for p in (2, 3, 5, 7, 11, 13):
                e = 0
                while x % p == 0:
                    x //= p
                    e += 1
                if e:
                    pf_.append(f"{p}" + (sup(e) if e > 1 else ""))
            q = f"분수 {F_(n, d)}를 소수로 나타내면 유한소수인가요, 순환소수인가요?" if not bat(n) else f"분수 {F_(n, d)}을 소수로 나타내면 유한소수인가요, 순환소수인가요?"
            lines = ([L(f"{F_(n, d)} = {F_(rn, rd)}", memo="기약분수로")] if g > 1 else []) + [L(f"분모 {rd} = {' × '.join(pf_) if pf_ else '1'}", memo="분모의 소인수"), L("2나 5뿐 → 유한소수" if fin else "2, 5 말고 다른 소인수 → 순환소수")]
            S.add(2, q, "유한소수" if fin else "순환소수", "기약분수의 분모가 2와 5만으로 되어 있는지", lines, None, omr="ex", key=q)
        else:
            d = R.choice([12, 18, 21, 24, 28, 33, 35, 36, 42, 44, 45, 48, 56, 60, 63, 66, 70, 72, 84, 90, 105, 110, 120, 126, 132, 140, 150])
            x = d
            bad = 1
            for p in (3, 7, 11, 13):
                while x % p == 0:
                    x //= p
                    bad *= p
            if bad == 1:
                return
            q = f"분수 {{x/{d}}}를 소수로 나타내면 유한소수가 될 때, x가 될 수 있는 가장 작은 자연수를 구하세요."
            lines = [L(f"{d} = {pfs_(d)}", memo="분모의 소인수분해"), L(f"2, 5가 아닌 소인수 {pfs_(bad)}", memo="x가 이것을 약분해 없애야 해요"), L(f"x는 {bad}의 배수 → 가장 작은 수 {bad}")]
            S.add(2, q, str(bad), "분모에서 2, 5 말고 남은 소인수를 분자가 없애야 해요", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = R.randint(1, 3)
        ip = R.randint(0, 3)
        cyc = "".join(str(R.randint(0, 9)) for _ in range(k))
        if len(set(cyc)) == 1 and k > 1 or cyc == "0" * k or cyc == "9" * k:
            return
        num = int(str(ip) + cyc) - ip
        den = int("9" * k)
        v = Fr(num, den)
        q = f"순환소수 {rep_str(ip, '', cyc)}를 기약분수로 나타내세요." if not bat(cyc[-1]) else f"순환소수 {rep_str(ip, '', cyc)}을 기약분수로 나타내세요."
        lines = [L(f"x = {rep_str(ip, '', cyc)}", memo="x로 놓아요"), L(f"{10 ** k}x − x = {int(str(ip) + cyc)} − {ip}", memo=f"{10 ** k}배 하면 소수 부분이 같아져요"), L(f"{den}x = {num}"), L(f"x = {F_(num, den)} = {MX(v) if v.denominator > 1 else v}" if Fr(num, den) != Fr(num, den).limit_denominator(den) or gcd(num, den) > 1 else f"x = {F_(num, den)}")]
        ans = F_(v.numerator, v.denominator) if v.denominator > 1 else str(v.numerator)
        lines[-1] = L(f"x = {F_(num, den)}" + (f" = {ans}" if gcd(num, den) > 1 else ""), memo="약분" if gcd(num, den) > 1 else None)
        S.add(3, q, ans, "x로 놓고 10의 거듭제곱을 곱해 빼요", lines, None, sub={"x": v}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = R.randint(1, 2)
        a = 1 if k == 2 else R.randint(1, 2)
        ip = R.randint(0, 1)
        pre = "".join(str(R.randint(0, 9)) for _ in range(a))
        cyc = "".join(str(R.randint(0, 9)) for _ in range(k))
        if cyc == "0" * k or cyc == "9" * k or (pre and pre[-1] == cyc[-1] and k == 1):
            return
        whole = int(str(ip) + pre + cyc)
        nonrep = int(str(ip) + pre)
        num = whole - nonrep
        den = int("9" * k + "0" * a)
        v = Fr(num, den)
        q = f"순환소수 {rep_str(ip, pre, cyc)}를 기약분수로 나타내세요." if not bat(cyc[-1]) else f"순환소수 {rep_str(ip, pre, cyc)}을 기약분수로 나타내세요."
        ans = F_(v.numerator, v.denominator) if v.denominator > 1 else str(v.numerator)
        lines = [L(f"분모: 9 {k}개, 0 {a}개 → {den}", memo="순환마디 자리 수 · 순환하지 않는 자리 수"), L(f"분자: {whole} − {nonrep} = {num}", memo="전체 − 순환하지 않는 부분"), L(f"{F_(num, den)} = {ans}" if gcd(num, den) > 1 else f"{F_(num, den)}", memo="약분" if gcd(num, den) > 1 else None)]
        S.add(4, q, ans, "분모는 9…90…, 분자는 (전체 − 순환하지 않는 부분)", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        d = R.choice([7, 13, 27, 37, 41, 11, 33])
        n = R.randint(1, d - 1)
        if gcd(n, d) != 1:
            return
        ip, pre, cyc = rep_dec(n, d)
        if pre or not cyc:
            return
        k = len(cyc)
        m = R.randint(20, 120)
        r = m % k
        dig = cyc[r - 1] if r else cyc[-1]
        f = Fig()
        for i, ch in enumerate(cyc):
            p = ang_pt(330, 340, 200, 90 - 360 * i / k)
            hl = (i == (r - 1) % k)
            f.circ(*p, 44, c="coral" if hl else "ink", sw=4 if hl else 2.5, f="gold" if hl else None, fo=0.25, at=2 if hl else "q")
            f.text(p[0], p[1] + 16, ch, z=44, b=700)
            f.text(p[0], p[1] - 52, f"{i + 1}", z=20, c="soft")
        f.text(330, 350, f"{k}자리마다", z=28, c="teal", b=700)
        q = f"분수 {F_(n, d)}를 소수로 나타낼 때, 소수점 아래 {m}번째 자리의 숫자를 구하세요." if not bat(n) else f"분수 {F_(n, d)}을 소수로 나타낼 때, 소수점 아래 {m}번째 자리의 숫자를 구하세요."
        lines = [L(f"{F_(n, d)} = {rep_str(ip, '', cyc, 2)}", memo=f"순환마디 {cyc} — {k}자리"), L(f"{m} ÷ {k} = {m // k} … {r}"), L(f"순환마디의 {r if r else k}번째 숫자 {dig}", memo="나머지가 0이면 마지막 숫자")]
        S.add(5, q, dig, "순환마디의 자리 수로 나눈 나머지", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S

def pfs_(n):
    out, p = [], 2
    m = n
    while m > 1:
        e = 0
        while m % p == 0:
            m //= p
            e += 1
        if e:
            out.append(f"{p}" + (sup(e) if e > 1 else ""))
        p += 1
    return " × ".join(out)


# ══════════ 다항식의 계산 ══════════
def P2(cx2=0, cx=0, c0=0, cy=0, cxy=0):
    """ax^{2} + bx + c + dy + exy 같은 식 글자 — (x², x, xy, y, 상수) 순"""
    out = ""
    for coef, var in ((cx2, "x^{2}"), (cxy, "xy"), (cx, "x"), (cy, "y"), (c0, "")):
        if coef == 0:
            continue
        a = abs(coef)
        body = (str(a) if (a != 1 or not var) else "") + var
        if out == "":
            out = (MI if coef < 0 else "") + body
        else:
            out += f" {MI if coef < 0 else '+'} {body}"
    return out or "0"

def calc():
    S = Set("calc", "다항식의 계산 — 덧셈 · 뺄셈 · 분배법칙", "다항식의 계산",
            {1: "다항식의 덧셈", 2: "다항식의 뺄셈", 3: "이차식의 덧셈 · 뺄셈", 4: "단항식 × 다항식", 5: "다항식 ÷ 단항식"},
            mixed=True, pp=10,
            tips={1: "괄호를 풀고 동류항(문자와 차수가 같은 항)끼리 모아요",
                  2: "빼는 식의 괄호를 풀 때 모든 항의 부호를 바꿔요",
                  3: "x^{2}항, x항, 상수항을 따로따로 — x^{2}과 x는 동류항이 아니에요",
                  4: "분배법칙 — 단항식을 괄호 안 각 항에 곱해요. 지수법칙 x × x = x^{2}",
                  5: "각 항을 단항식으로 나누거나, 역수를 곱해요"},
            note="다항식의 계산에서 가장 흔한 실수는 ‘빼는 식의 둘째 항 이후 부호를 안 바꾸기’와 ‘x^{2}과 x를 더하기’예요. 동류항에 같은 표시(밑줄 · 동그라미)를 하게 해 주세요.")
    R = rng(1305)

    def rc(lo=1, hi=9, z=False):
        v = R.randint(lo, hi) * R.choice([1, -1])
        return 0 if (z and R.random() < 0.2) else v

    def g12(st):
        a, b, c = rc(), rc(), rc(z=True)
        d, e, g = rc(), rc(), rc(z=True)
        A = P2(cx=a, cy=b, c0=c)
        B = P2(cx=d, cy=e, c0=g)
        if st == 1:
            res = P2(cx=a + d, cy=b + e, c0=c + g)
            open_ = P2(cx=a, cy=b, c0=c) + " " + ("+ " + P2(cx=d, cy=e, c0=g) if d > 0 else f"{MI} " + P2(cx=-d, cy=e, c0=g).lstrip())
            q = f"({A}) + ({B})를 계산하세요."
            mid = f"{A} " + " ".join(f"{'+' if v > 0 else MI} {abs(v) if (abs(v) != 1 or not t) else ''}{t}" for v, t in ((d, "x"), (e, "y"), (g, "")) if v)
            lines = [L(f"({A}) + ({B}) = {mid}", memo="괄호를 그대로 풀어요"), L(f"{mid} = {res}", memo="동류항끼리")]
            plan = "괄호를 풀고 동류항끼리"
        else:
            res = P2(cx=a - d, cy=b - e, c0=c - g)
            q = f"({A}) − ({B})를 계산하세요."
            mid = f"{A} " + " ".join(f"{'+' if -v > 0 else MI} {abs(v) if (abs(v) != 1 or not t) else ''}{t}" for v, t in ((d, "x"), (e, "y"), (g, "")) if v)
            lines = [L(f"({A}) − ({B}) = {mid}", memo="빼는 식의 부호를 모두 바꿔요"), L(f"{mid} = {res}", memo="동류항끼리")]
            plan = "빼는 식의 모든 항의 부호를 바꿔 더해요"
        if res == "0":
            return
        S.add(st, q, res, plan, lines, None, omr="ex", ident=True, key=q)

    fill(S, 1, 20, lambda: g12(1))
    fill(S, 2, 20, lambda: g12(2))

    def g3():
        a, b, c = rc(1, 6), rc(), rc(z=True)
        d, e, g = rc(1, 6), rc(), rc(z=True)
        op = R.choice(["+", "−"])
        sg = 1 if op == "+" else -1
        A, B = P2(cx2=a, cx=b, c0=c), P2(cx2=d, cx=e, c0=g)
        res = P2(cx2=a + sg * d, cx=b + sg * e, c0=c + sg * g)
        if res == "0" or a + sg * d == 0 and R.random() < 0.7:
            return
        q = f"({A}) {op} ({B})를 계산하세요."
        mid = f"{A} " + " ".join(f"{'+' if sg * v > 0 else MI} {abs(v) if (abs(v) != 1 or not t) else ''}{t}" for v, t in ((d, "x^{2}"), (e, "x"), (g, "")) if v)
        lines = [L(f"({A}) {op} ({B}) = {mid}", memo="괄호 풀기" + (" — 부호를 모두 바꿔요" if op == "−" else "")), L(f"{mid} = {res}", memo="x^{2}항 · x항 · 상수항끼리")]
        S.add(3, q, res, "차수가 같은 항끼리 — x^{2}과 x는 따로", lines, None, omr="ex", ident=True, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = rc(1, 6)
        a, b = rc(1, 6), rc(1, 9)
        kind = S.count(4) % 2
        if kind == 0:
            M = monom(k, {"x": 1})
            inner = P2(cx=a, cy=b)
            t1, t2 = monom(a, {"x": 1}), monom(b, {"y": 1})
            r1, r2 = monom(k * a, {"x": 2}), monom(k * b, {"x": 1, "y": 1})
            res = P2(cx2=k * a, cxy=k * b)
        else:
            M = monom(k, {"a": 1})
            inner = P2(cx=a, c0=b).replace("x", "a")
            t1, t2 = monom(a, {"a": 1}), N(b)
            r1, r2 = monom(k * a, {"a": 2}), monom(k * b, {"a": 1})
            res = P2(cx2=k * a, cx=k * b).replace("x^{2}", "a^{2}").replace("x", "a")
        Mp = f"({M})" if k < 0 else M
        T1 = f"({t1})" if t1.startswith(MI) else t1
        T2 = f"({t2})" if t2.startswith(MI) else t2
        q = f"{J(M + '(' + inner + ')', '을', '를')} 계산하세요."
        lines = [L(f"{Mp} × {T1} = {r1}, {Mp} × {T2} = {r2}", memo="분배법칙 — 괄호 안 각 항에 곱하기"), L(f"{M}({inner}) = {res}")]
        S.add(4, q, res, "단항식을 괄호 안 각 항에 곱해요", lines, None, omr="ex", ident=True, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = rc(2, 6)
        a, b = rc(1, 5), rc(1, 5)
        kind = S.count(5) % 2
        if kind == 0:
            num = P2(cx2=k * a, cxy=k * b)
            den = monom(k, {"x": 1})
            res = P2(cx=a, cy=b)
        else:
            num = monom(k * a, {"x": 2, "y": 1}) + monom(k * b, {"x": 1, "y": 2}, first=False)
            den = monom(k, {"x": 1, "y": 1})
            res = P2(cx=a, cy=b)
        den_s = f"({den})" if k < 0 else den
        q = f"({num}) ÷ {J(den_s, '을', '를')} 계산하세요."
        lines = [L(f"({num}) ÷ {den_s} = {{{num}/{den}}}", memo="분수 꼴로 — 각 항을 나눠요"), L(f"{{{num}/{den}}} = {res}", memo="계수끼리 · 문자끼리 나누기")]
        S.add(5, q, res, "각 항을 단항식으로 나눠요", lines, None, omr="ex", ident=True, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 일차부등식 ══════════
def sol_fig(f, b, gt, incl, at=0, lo=None, hi=None):
    lo = int(math.floor(b)) - 5 if lo is None else lo
    hi = int(math.ceil(b)) + 5 if hi is None else hi
    nl = NL(f, lo, hi, y=360, lab_step=1 if hi - lo <= 12 else 2)
    X = nl.X(b)
    if gt:
        f.line(X, 300, X, 330, c="coral", w=4, at=at)
        f.line(X, 300, nl.X(hi) + 10, 300, c="coral", w=5, ar=1, at=at)
    else:
        f.line(X, 300, X, 330, c="coral", w=4, at=at)
        f.line(X, 300, nl.X(lo) - 10, 300, c="coral", w=5, ar=1, at=at)
    f.circ(X, 360, 12, c="coral", sw=4, f="coral" if incl else "paper", fo=1, at=at)

OPS_ = {"<": lambda a, b: a < b, ">": lambda a, b: a > b, "≤": lambda a, b: a <= b, "≥": lambda a, b: a >= b}

def ineq_ok(lhs, op, rhs, bnd, newop):
    """원래 부등식과 구한 해가 같은 x 들에서 같은지(경계 근처 · 멀리)"""
    bnd = Fr(bnd)
    for dx in (Fr(-7), Fr(-1), Fr(-1, 3), Fr(0), Fr(1, 3), Fr(1), Fr(7)):
        x = bnd + dx
        assert OPS_[op](lhs(x), rhs(x)) == OPS_[newop](x, bnd), (op, newop, bnd, x)
    return True

def ineq():
    S = Set("ineq", "일차부등식 — 부등호 방향과 해의 범위", "일차부등식",
            {1: "부등식의 성질", 2: "일차부등식 풀기", 3: "괄호 · 분수 · 소수가 있는 부등식", 4: "해의 조건", 5: "일차부등식의 활용"},
            mixed=True, pp=8,
            tips={1: "양변에 같은 수를 더하거나 빼도, 양수를 곱하거나 나누어도 그대로 — 음수를 곱하거나 나누면 방향이 바뀌어요",
                  2: "x항은 왼쪽, 수는 오른쪽으로 이항 → ax > b → x의 계수로 나누기(음수면 방향 반대)",
                  3: "괄호를 풀고, 분수는 분모의 최소공배수를, 소수는 10의 거듭제곱을 양변에 곱해요",
                  4: "해를 수직선에 그려 놓고 조건에 맞는 정수 · 자연수를 세요",
                  5: "구하는 것을 x로 놓고 ‘이하 · 이상 · 초과 · 미만’을 부등호로"},
            note="부등식은 방정식과 같은 방법으로 풀되 ‘음수로 곱하거나 나눌 때 부등호 방향이 바뀐다’는 한 가지만 다르다는 점을 강조해 주세요. 해는 수직선에 꼭 그려 보게 해요.")
    R = rng(1306)

    def g1():
        p = R.randint(2, 6) * R.choice([1, -1])
        c = R.randint(-9, 9)
        base = R.choice(["<", ">"])
        flip = p < 0
        res = {"<": ">", ">": "<"}[base] if flip else base
        L_ = f"{N(p)}a" + (f" + {c}" if c > 0 else (f" {MI} {-c}" if c < 0 else ""))
        R_ = f"{N(p)}b" + (f" + {c}" if c > 0 else (f" {MI} {-c}" if c < 0 else ""))
        q = f"a {base} b일 때, {L_} □ {R_}의 □ 안에 알맞은 부등호를 써넣으세요."
        lines = [L(f"a {base} b"), L(f"{N(p)}a {res} {N(p)}b", memo=("음수를 곱해 방향이 바뀌어요" if flip else "양수를 곱해 방향 그대로")), L(f"{L_} {res} {R_}", memo="같은 수를 더해도(빼도) 그대로")]
        S.add(1, q, res, "음수를 곱할 때만 방향이 바뀌어요", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def solve_lines(a, b, c, d, op):
        """ax + b op cx + d → 줄들, 경계, 방향"""
        A, B = a - c, d - b
        lines = [L(f"{mono(a, 'x', 1, first=True)}{mono(-c, 'x', 1) if c else ''} {op} {N(d)}{mono(-b, '', 1) if b else ''}", memo="이항: x항은 왼쪽, 수는 오른쪽")]
        lines.append(L(f"{mono(A, 'x', 1, first=True)} {op} {N(B)}", memo="정리"))
        flip = A < 0
        newop = {"<": ">", ">": "<", "≤": "≥", "≥": "≤"}[op] if flip else op
        bnd = Fr(B, A)
        lines.append(L(f"x {newop} {N(bnd)}", memo=(f"{RO(NP(A))} 나누면 방향이 바뀌어요" if flip else f"{RO(A)} 나눠요")))
        return lines, bnd, newop

    def g2():
        a, b = R.randint(-6, 8), R.randint(-12, 12)
        c, d = R.randint(-4, 4), R.randint(-12, 12)
        if a == c or a == 0:
            return
        op = R.choice(["<", ">", "≤", "≥"])
        lines, bnd, newop = solve_lines(a, b, c, d, op)
        if bnd.denominator != 1:
            return
        ineq_ok(lambda x: a * x + b, op, lambda x: c * x + d, bnd, newop)
        lhs = lin(a, b)
        rhs = lin(c, d) if c else N(d)
        q = f"일차부등식 {lhs} {op} {J(rhs, '을', '를')} 푸세요."
        f = Fig()
        sol_fig(f, int(bnd), newop in (">", "≥"), newop in ("≤", "≥"), at=len(lines) - 1)
        S.add(2, q, f"x {newop} {N(bnd)}", "이항해서 ax > b 꼴 → x의 계수로 나누기", lines, f.out(), omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        op = R.choice(["<", ">", "≤", "≥"])
        if k == 0:
            p, a, b = R.randint(2, 5), R.randint(-3, 4), R.randint(-6, 6)
            c, d = R.randint(-5, 5), R.randint(-9, 9)
            if a == 0 or b == 0:
                return
            A_, B_ = p * a, p * b
            orig = (lambda x, p=p, a=a, b=b: p * (a * x + b), lambda x, c=c, d=d: c * x + d)
            q_s = f"{p}({lin(a, b)}) {op} {lin(c, d) if c else N(d)}"
            first = L(f"{lin(A_, B_)} {op} {lin(c, d) if c else N(d)}", memo="괄호를 풀어요")
            a2, b2 = A_, B_
            if a2 == c:
                return
        elif k == 1:
            m1, m2 = R.sample([2, 3, 4, 6], 2)
            l = m1 * m2 // gcd(m1, m2)
            a, b = R.randint(1, 4), R.randint(-3, 3)
            c = R.randint(-3, 3)
            q_s = f"{{{lin(a, b)}/{m1}}} {op} {{{lin(1, c)}/{m2}}}" if c else f"{{{lin(a, b)}/{m1}}} {op} {{x/{m2}}}"
            orig = (lambda x, a=a, b=b, m1=m1: Fr(a * x + b) / m1, lambda x, c=c, m2=m2: Fr(x + c) / m2)
            a2, b2 = a * (l // m1), b * (l // m1)
            c, d = (l // m2), c * (l // m2)
            first = L(f"{l // m1}({lin(a, b)}) {op} {l // m2}({lin(1, c // (l // m2)) if d else 'x'})" if d else f"{l // m1}({lin(a, b)}) {op} {l // m2}x", memo=f"양변에 {l}{'을' if bat(l) else '를'} 곱해요")
            if a2 == c:
                return
        else:
            a, b, c, d = R.randint(1, 9), R.randint(-20, 20), R.randint(1, 9), R.randint(-20, 20)
            if a == c:
                return
            q_s = f"{DEC(Fr(a, 10))}x {'+' if b >= 0 else MI} {DEC(Fr(abs(b), 10))} {op} {DEC(Fr(c, 10))}x {'+' if d >= 0 else MI} {DEC(Fr(abs(d), 10))}"
            orig = (lambda x, a=a, b=b: Fr(a, 10) * x + Fr(b, 10), lambda x, c=c, d=d: Fr(c, 10) * x + Fr(d, 10))
            first = L(f"{lin(a, b)} {op} {lin(c, d)}", memo="양변에 10을 곱해요")
            a2, b2 = a, b
        lines_rest, bnd, newop = solve_lines(a2, b2, c, d, op)
        if bnd.denominator != 1 or abs(bnd) > 12:
            return
        ineq_ok(orig[0], op, orig[1], bnd, newop)
        lines = [first] + lines_rest
        f = Fig()
        sol_fig(f, int(bnd), newop in (">", "≥"), newop in ("≤", "≥"), at=len(lines) - 1)
        q = f"일차부등식 {q_s}를 푸세요."
        S.add(3, q, f"x {newop} {N(bnd)}", "괄호 · 분모 · 소수를 먼저 없애고 풀어요", lines, f.out(), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        a, b = R.randint(2, 6), R.randint(-10, 20)
        c = R.randint(1, 30)
        op = R.choice(["<", "≤"])
        bnd = Fr(c - b, a)
        if bnd <= 0 or bnd > 12:
            return
        if k == 0:
            nat = [x for x in range(1, 40) if (a * x + b < c if op == "<" else a * x + b <= c)]
            if not nat:
                return
            q = f"일차부등식 {lin(a, b)} {op} {c}를 만족하는 자연수 x는 모두 몇 개인가요?" if not bat(c) else f"일차부등식 {lin(a, b)} {op} {c}을 만족하는 자연수 x는 모두 몇 개인가요?"
            lines = [L(f"{a}x {op} {c - b}", memo="이항"), L(f"x {op} {N(bnd)}"), L(f"자연수: {', '.join(map(str, nat))}", memo="수직선에서 세기"), L(f"{len(nat)}개")]
            ans, ap = f"{len(nat)}개", str(len(nat))
            f = Fig()
            sol_fig(f, float(bnd), False, op == "≤", at=1, lo=-1, hi=max(8, int(bnd) + 2))
            for i, x in enumerate(nat):
                pass
        elif k == 1:
            op2 = R.choice([">", "≥"])
            bnd2 = Fr(R.randint(-12, 12) * 2 + 1, 2) if R.random() < 0.5 else Fr(R.randint(-8, 8))
            m = math.floor(bnd2) + 1 if (op2 == ">" or bnd2.denominator != 1) else int(bnd2)
            A_ = R.randint(2, 5)
            B_ = A_ * bnd2
            if B_.denominator != 1:
                return
            q = f"일차부등식 {A_}x {op2} {N(B_)}를 만족하는 가장 작은 정수 x를 구하세요." if not bat(N(B_)) else f"일차부등식 {A_}x {op2} {N(B_)}을 만족하는 가장 작은 정수 x를 구하세요."
            lines = [L(f"x {op2} {N(bnd2)}", memo=f"{RO(A_)} 나눠요"), L(f"가장 작은 정수 → {N(m)}", memo="경계가 포함되는지 확인")]
            ans, ap = N(m), N(m)
            f = Fig()
            sol_fig(f, float(bnd2), True, op2 == "≥", at=0)
        else:
            a2 = R.randint(2, 5)
            sol = R.randint(-5, 8)
            kx = R.randint(1, 9)
            # ax + k > 2x + ... 해가 x > sol 일 때 상수 m
            q = f"일차부등식 {a2}x {MI} m > x + {kx}의 해가 x > {N(sol)}일 때, 상수 m의 값을 구하세요."
            m = (a2 - 1) * sol - kx
            lines = [L(f"{a2 - 1}x > {kx} + m" if a2 > 2 else f"x > {kx} + m", memo="이항"), L(f"x > {{{kx} + m/{a2 - 1}}}" if a2 > 2 else f"x > {kx} + m"), L(f"{{{kx} + m/{a2 - 1}}} = {N(sol)}" if a2 > 2 else f"{kx} + m = {N(sol)}", memo="해의 경계가 같아요"), L(f"m = {N(m)}")]
            ans, ap = N(m), N(m)
            f = None
            S.add(4, q, ans, "부등식을 풀어 경계를 문자로 → 주어진 해와 비교", lines, None, sub={"m": m}, key=q)
            return
        S.add(4, q, ans, "해를 수직선에 그리고 조건에 맞는 수를 찾아요", lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            p, box_, tot = R.randint(5, 15) * 100, R.randint(1, 5) * 500, R.randint(10, 40) * 1000
            n = (tot - box_) // p
            if n < 2:
                return
            q = f"한 개에 {p}원인 사과를 {box_}원짜리 바구니에 담아 사려고 해요. 전체 값이 {com(tot)}원 이하가 되게 하려면 사과를 최대 몇 개까지 살 수 있나요?"
            lines = [L(f"{p}x + {box_} ≤ {tot}", memo="사과 x개"), L(f"{p}x ≤ {tot - box_}"), L(f"x ≤ {N(Fr(tot - box_, p))}"), L(f"최대 {n}개", memo="x는 자연수")]
            ans, ap = f"{n}개", str(n)
        elif k == 1:
            a, b = R.randint(500, 1500) // 100 * 100, R.randint(2, 6) * 1000
            c = R.randint(1, 3) * 1000 + a + R.randint(1, 9) * 100
            if c <= a:
                return
            # 가게 A: 개당 c원 · B: 개당 a원 + 배송비 b원 → B가 유리한 최소 개수
            x0 = b // (c - a) + 1
            q = f"한 권에 {c}원인 공책을 동네 문구점에서 사거나, 한 권에 {a}원인 인터넷 가게에서 배송비 {b}원을 내고 살 수 있어요. 인터넷 가게에서 사는 것이 더 싸려면 공책을 적어도 몇 권 사야 하나요?"
            lines = [L(f"{a}x + {b} < {c}x", memo="공책 x권 — 인터넷이 더 싸려면"), L(f"{b} < {c - a}x"), L(f"x > {N(Fr(b, c - a))}"), L(f"적어도 {x0}권")]
            ans, ap = f"{x0}권", str(x0)
        else:
            s, t = R.randint(60, 95), R.randint(3, 6)
            target = R.randint(s + 1, min(100, s + 15))
            need = target * (t + 1) - s * t
            if need > 100:
                return
            q = f"수학 시험을 {t}번 보았는데 평균이 {s}점이에요. 다음 시험까지 {t + 1}번의 평균이 {target}점 이상이 되려면 다음 시험에서 몇 점 이상을 받아야 하나요?"
            lines = [L(f"{{{s} × {t} + x/{t + 1}}} ≥ {target}", memo="다음 시험 x점"), L(f"{s * t} + x ≥ {target * (t + 1)}"), L(f"x ≥ {need}"), L(f"{need}점 이상")]
            ans, ap = f"{need}점", str(need)
        S.add(5, q, ans, "구하는 것을 x로 — ‘이하 · 이상 · 미만 · 초과’를 부등호로", lines, None, ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S
