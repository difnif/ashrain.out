# 초5 — ① 약분과 통분 → 분모가 다른 분수의 덧셈 · 뺄셈 · ② 다각형의 넓이 — 잘라 붙이고 두 배 하기
import math
from math import gcd
from core import *
from fig import Fig, mv, fbar, ffill

def F_(n, d):
    return "{%d/%d}" % (n, d)

def lcm(a, b):
    return a * b // gcd(a, b)

def red(n, d):
    g = gcd(n, d)
    return n // g, d // g

# ══════════ ① 약분과 통분 ══════════
def tongbun_fig(f, a, b, c, d, L_, at_split=0):
    """두 분수 막대 — at_split 줄에 최소공배수 칸으로 잘게 나뉜다"""
    BX, BW, BH = 50, 560, 70
    for k, (n, m, col, y) in enumerate(((a, b, "gold", 150), (c, d, "teal", 400))):
        fbar(f, BX, y, BW, BH, m)
        ffill(f, BX, y, BW, BH, m, 0, n, col, "q", step=60)
        f.text(BX, y - 22, F_(n, m), z=36, c=col, b=700, a="s")
        # 잘게 나누는 선
        sub = L_ // m
        if sub > 1:
            for i in range(1, L_):
                if i % sub:
                    x = BX + BW * i / L_
                    f.line(x, y + 4, x, y + BH - 4, at=at_split, c="red", w=1.6, d=True, dl=(i % 8) * 40)
        f.text(BX + BW, y + BH + 56, F_(n * (L_ // m), L_), z=40, c=col, at=at_split, b=700, dl=500, a="e")

def set_a():
    S = Set("a", "약분과 통분 — 분모가 다른 분수의 덧셈 · 뺄셈", "약분·통분",
            {1: "약분 — 기약분수로", 2: "통분 — 최소공배수로", 3: "분모가 다른 덧셈", 4: "분모가 다른 뺄셈", 5: "대분수의 덧셈 · 뺄셈"},
            mixed=True, pp=10,
            tips={1: "분모와 분자를 최대공약수로 한 번에 나누면 기약분수 — {18/24} = {18 ÷ 6/24 ÷ 6} = {3/4}",
                  2: "두 분모의 최소공배수를 공통분모로 — {3/4}, {5/6} → {9/12}, {10/12}",
                  3: "통분해서 분모를 같게 한 뒤 분자끼리 더하고, 마지막에 약분해요",
                  4: "통분해서 분모를 같게 한 뒤 분자끼리 빼요",
                  5: "자연수끼리 · 분수끼리 — 분수끼리 뺄 수 없으면 자연수 1을 분수로 바꿔요"},
            note="분모가 다르면 ‘같은 크기의 조각으로 다시 자르기(통분)’부터예요. 그림의 빨간 점선이 바로 통분이에요. 답은 기약분수로 쓰게 해 주세요.")
    R = rng(501)

    def g1():
        d0 = R.randint(3, 12); n0 = R.randint(1, d0 - 1)
        if gcd(n0, d0) != 1:
            return
        k = R.randint(2, 9)
        n, d = n0 * k, d0 * k
        if d > 100:
            return
        g = gcd(n, d)
        S.add(1, f"{J(F_(n, d), '을', '를')} 기약분수로 나타내세요.", F_(n0, d0), "분모와 분자의 최대공약수로 나눠요",
              [L(f"{n}과 {d}의 최대공약수 = {g}" if _bat(n) else f"{n}와 {d}의 최대공약수 = {g}"), L(f"{F_(n, d)} = {{{n} ÷ {g}/{d} ÷ {g}}} = {F_(n0, d0)}")], None, key=f"{n}/{d}")
    fill(S, 1, 20, g1)

    def g2():
        b = R.randint(2, 12); d = R.randint(2, 12)
        if b == d or b % d == 0 or d % b == 0 and R.random() < 0.6:
            return
        a = R.randint(1, b - 1); c = R.randint(1, d - 1)
        if gcd(a, b) != 1 or gcd(c, d) != 1:
            return
        L_ = lcm(b, d)
        if L_ > 60:
            return
        f = Fig()
        tongbun_fig(f, a, b, c, d, L_, at_split=1)
        x1, x2 = L_ // b, L_ // d
        S.add(2, f"{F_(a, b)}, {J(F_(c, d), '을', '를')} 가장 작은 공통분모로 통분하세요.", f"{F_(a * x1, L_)}, {F_(c * x2, L_)}", "두 분모의 최소공배수가 공통분모",
              [L(f"{b}와 {d}의 최소공배수 = {L_}" if not _bat(b) else f"{b}과 {d}의 최소공배수 = {L_}"),
               L(f"{F_(a, b)} = {{{a} × {x1}/{b} × {x1}}} = {F_(a * x1, L_)}"), L(f"{F_(c, d)} = {{{c} × {x2}/{d} × {x2}}} = {F_(c * x2, L_)}")],
              f.out(), ap=f"{a * x1}/{L_}, {c * x2}/{L_}", omr="ex", key=f"{a}/{b},{c}/{d}")
    fill(S, 2, 20, g2)

    def addsub(st, op):
        def g():
            b = R.randint(2, 12); d = R.randint(2, 12)
            if b == d:
                return
            a = R.randint(1, b - 1); c = R.randint(1, d - 1)
            if gcd(a, b) != 1 or gcd(c, d) != 1:
                return
            L_ = lcm(b, d)
            if L_ > 60:
                return
            A, C = a * (L_ // b), c * (L_ // d)
            if op == "−" and A <= C:
                return
            T = A + C if op == "+" else A - C
            v = Fr(T, L_)
            lines = [L(f"통분: {b}, {d}의 최소공배수 {L_}"), L(f"{F_(a, b)} {op} {F_(c, d)} = {F_(A, L_)} {op} {F_(C, L_)}"), L(f"= {F_(T, L_)}" if False else f"{F_(A, L_)} {op} {F_(C, L_)} = {F_(T, L_)}")]
            if v.denominator != L_ or v > 1:
                tail = []
                if v.denominator != L_:
                    tail.append(N(v))
                if v > 1:
                    tail.append(MX(v))
                lines.append(L(f"{F_(T, L_)} = " + " = ".join(dict.fromkeys(tail)), memo="약분" if v.denominator != L_ else "대분수로"))
            ans = MX(v)
            f = Fig() if L_ <= 36 else None
            if f:
                tongbun_fig(f, a, b, c, d, L_, at_split=1)
            S.add(st, f"{F_(a, b)} {op} {J(F_(c, d), '은', '는')} 얼마인가요?", ans, "통분한 뒤 분자끼리 계산해요", lines, f.out() if f else None, ap=plain(ans), key=f"{a}/{b}{op}{c}/{d}")
        return g
    fill(S, 3, 20, addsub(3, "+"))
    fill(S, 4, 20, addsub(4, "−"))

    def g5():
        b = R.randint(2, 9); d = R.randint(2, 9)
        if b == d:
            return
        a = R.randint(1, b - 1); c = R.randint(1, d - 1)
        if gcd(a, b) != 1 or gcd(c, d) != 1:
            return
        L_ = lcm(b, d)
        if L_ > 36:
            return
        w1, w2 = R.randint(1, 6), R.randint(1, 5)
        A, C = a * (L_ // b), c * (L_ // d)
        op = "+" if S.count(5) % 2 == 0 else "−"
        if op == "−" and w1 <= w2:
            return
        x, y = w1 + Fr(a, b), w2 + Fr(c, d)
        v = x + y if op == "+" else x - y
        lines = [L(f"{w1}{F_(a, b)} {op} {w2}{F_(c, d)} = {w1}{F_(A, L_)} {op} {w2}{F_(C, L_)}", memo=f"통분 {L_}")]
        if op == "+":
            T = A + C
            lines.append(L(f"자연수끼리 {w1 + w2}, 분수끼리 {F_(T, L_)}"))
            lines.append(L(f"{w1 + w2} + {F_(T, L_)} = {MX(v)}", memo="1이 넘으면 올려요" if T >= L_ else None))
        else:
            if A >= C:
                lines.append(L(f"자연수끼리 {w1 - w2}, 분수끼리 {F_(A - C, L_)}"))
                lines.append(L(f"{w1 - w2} + {F_(A - C, L_)} = {MX(v)}"))
            else:
                lines.append(L(f"{w1}{F_(A, L_)} = {w1 - 1}{F_(A + L_, L_)}", memo="1을 빌려 와요"))
                lines.append(L(f"{w1 - 1}{F_(A + L_, L_)} − {w2}{F_(C, L_)} = {MXu(w1 - 1 - w2, A + L_ - C, L_)}"))
                if Fr(A + L_ - C, L_).denominator != L_:
                    lines.append(L(f"{MXu(w1 - 1 - w2, A + L_ - C, L_)} = {MX(v)}", memo="약분"))
        ans = MX(v)
        S.add(5, f"{w1}{F_(a, b)} {op} {J(str(w2) + F_(c, d), '은', '는')} 얼마인가요?", ans, "통분한 뒤 자연수끼리, 분수끼리", lines, None, ap=plain(ans), key=f"{w1}{a}/{b}{op}{w2}{c}/{d}")
    fill(S, 5, 20, g5)
    return S

def _bat(n):
    return str(n)[-1] in "013678"


# ══════════ ② 다각형의 넓이 ══════════
U = 34   # 1 cm = 34 칸(그림)

def place(pts, box=(60, 70, 600, 600), stretch=2.0):
    """도형을 그림 칸에 — 너무 납작하면 세로를 stretch 배까지 늘려 보인다(모양 이해용 그림)"""
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, y0, x1, y1 = box
    sx = (x1 - x0) / (max(xs) - min(xs) + 1e-9)
    sy = (y1 - y0) / (max(ys) - min(ys) + 1e-9)
    s = min(sx, sy, U)
    sx2 = s
    sy2 = min(sy, s * stretch, U * stretch)
    if sy2 < s:
        sy2 = s
    cx = (x0 + x1) / 2 - sx2 * (max(xs) + min(xs)) / 2
    cy = (y0 + y1) / 2 + sy2 * (max(ys) + min(ys)) / 2
    return [(cx + sx2 * x, cy - sy2 * y) for x, y in pts], s, (cx, cy)

def dim(f, A, B, s, off=26, at="q", c="ink", z=30, side=1):
    """두 점 사이 길이 글자(선분 옆)"""
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    dx, dy = B[0] - A[0], B[1] - A[1]
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln * side, dx / ln * side
    f.text(mx + nx * off, my + ny * off + z * 0.34, s, z=z, c=c, at=at, b=700)

def set_b():
    S = Set("b", "다각형의 넓이 — 잘라 붙이고 두 배 하기", "다각형의 넓이",
            {1: "직사각형 · 정사각형", 2: "평행사변형", 3: "삼각형", 4: "사다리꼴", 5: "마름모 · 복합 도형"},
            pp=6, unit="cm²",
            tips={1: "(직사각형의 넓이) = (가로) × (세로) · (정사각형) = (한 변) × (한 변)",
                  2: "한쪽 삼각형을 잘라 반대쪽에 붙이면 직사각형 → (밑변) × (높이)",
                  3: "똑같은 삼각형 2개를 붙이면 평행사변형 → (밑변) × (높이) ÷ 2",
                  4: "똑같은 사다리꼴 2개를 붙이면 평행사변형 → ((윗변) + (아랫변)) × (높이) ÷ 2",
                  5: "마름모 = (한 대각선) × (다른 대각선) ÷ 2 · 복합 도형은 큰 직사각형에서 빼요"},
            note="공식을 외우기보다 ‘잘라 붙이면 직사각형, 두 개 붙이면 평행사변형’을 그림으로 확인하게 해 주세요. 높이는 밑변과 수직인 길이예요.")
    R = rng(502)

    def g1():
        k = S.count(1) % 3
        f = Fig()
        if k < 2:
            w = R.randint(3, 15); h = R.randint(2, 12)
            if k == 1:
                h = w
            P, s, _ = place([(0, 0), (w, 0), (w, h), (0, h)])
            f.poly(P, c="ink", w=4, f="sky", fo=0.12)
            dim(f, P[0], P[1], f"{w} cm")
            dim(f, P[1], P[2], f"{h} cm", off=40)
            if k == 0:
                q, lines = f"가로 {w} cm, 세로 {h} cm인 직사각형의 넓이는 몇 cm²인가요?", [L("(넓이) = (가로) × (세로)"), L(f"{w} × {h} = {w * h}")]
            else:
                q, lines = f"한 변이 {w} cm인 정사각형의 넓이는 몇 cm²인가요?", [L("(넓이) = (한 변) × (한 변)"), L(f"{w} × {w} = {w * w}")]
            S.add(1, q, f"{w * h} cm²", "넓이 1 cm²인 칸이 몇 개인지 = 가로 × 세로", lines, f.out(), ap=str(w * h), key=q)
        else:
            w = R.randint(4, 15); h = R.randint(2, 12)
            P, s, _ = place([(0, 0), (w, 0), (w, h), (0, h)])
            f.poly(P, c="ink", w=4, f="sky", fo=0.12)
            dim(f, P[0], P[1], f"{w} cm")
            dim(f, P[1], P[2], "□ cm", c="teal", off=40)
            q = f"넓이가 {w * h} cm²이고 가로가 {w} cm인 직사각형의 세로는 몇 cm인가요?"
            S.add(1, q, f"{h} cm", "가로 × 세로 = 넓이를 거꾸로", [L(f"{w} × □ = {w * h}"), L(f"□ = {w * h} ÷ {w} = {h}")], f.out(), ap=str(h), key=q)
    fill(S, 1, 20, g1)

    def g2():
        b = R.randint(5, 14); h = R.randint(3, 10); sh = R.randint(1, max(1, b // 2))
        P, s, (cx, cy) = place([(0, 0), (b, 0), (b + sh, h), (sh, h)], box=(60, 80, 600, 560))
        f = Fig()
        f.poly(P, c="ink", w=4)
        Hf = (P[3][0], P[0][1])
        f.line(*P[3], *Hf, c="red", w=3, d=True)
        f.text(P[3][0] + 12, (P[3][1] + Hf[1]) / 2 + 10, f"{h} cm", z=30, c="red", a="s", b=700)
        dim(f, P[0], P[1], f"{b} cm")
        tri = f.poly([P[0], Hf, P[3]], at=0, c="none", f="teal", fo=0.45)
        mv(tri, 0, P[1][0] - P[0][0], 0)
        f.poly([P[0], Hf, P[3]], at=0, c="teal", w=2, d=True)
        f.text(330, max(p[1] for p in P) + 90, f"직사각형 {b} × {h}", z=34, c="gold", at=0, dl=900)
        q = f"밑변이 {b} cm, 높이가 {h} cm인 평행사변형의 넓이는 몇 cm²인가요?"
        S.add(2, q, f"{b * h} cm²", "왼쪽 삼각형을 잘라 오른쪽에 붙이면 직사각형",
              [L("잘라 붙이면 직사각형", memo="넓이는 그대로"), L("(넓이) = (밑변) × (높이)"), L(f"{b} × {h} = {b * h}")], f.out(), ap=str(b * h), key=q)
    fill(S, 2, 20, g2)

    def g3():
        b = R.randint(4, 16); h = R.randint(3, 12)
        if (b * h) % 2:
            return
        t = R.randint(1, b - 1)
        pts = [(0, 0), (b, 0), (t, h)]
        P, s, _ = place([(0, 0), (b, 0), (b + t, h), (t, h)], box=(60, 80, 600, 560))
        A, B, C, D = P
        f = Fig()
        f.poly([A, B, D], c="ink", w=4, f="sky", fo=0.15)
        Hf = (D[0], A[1])
        f.line(*D, *Hf, c="red", w=3, d=True)
        f.text(D[0] + 12, (D[1] + Hf[1]) / 2 + 10, f"{h} cm", z=30, c="red", a="s", b=700)
        dim(f, A, B, f"{b} cm")
        cp = f.poly([A, B, D], at=0, c="teal", w=3, f="teal", fo=0.25)
        mid = ((B[0] + D[0]) / 2, (B[1] + D[1]) / 2)
        mv(cp, 0, 0, 0, r=180, cx=mid[0], cy=mid[1])
        f.text(330, max(p[1] for p in P) + 90, "평행사변형의 반", z=34, c="gold", at=1)
        q = f"밑변이 {b} cm, 높이가 {h} cm인 삼각형의 넓이는 몇 cm²인가요?"
        S.add(3, q, f"{b * h // 2} cm²", "똑같은 삼각형 2개를 붙이면 평행사변형",
              [L("2개 붙이면 평행사변형", memo="180° 돌려 붙여요"), L("(넓이) = (밑변) × (높이) ÷ 2"), L(f"{b} × {h} ÷ 2 = {b * h // 2}")], f.out(), ap=str(b * h // 2), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.randint(3, 10); b = R.randint(a + 2, 15); h = R.randint(3, 10)
        if ((a + b) * h) % 2:
            return
        off = R.randint(0, b - a)
        P, s, _ = place([(0, 0), (b, 0), (off + a, h), (off, h), (b + a, h), (b + a, 0)], box=(40, 90, 620, 560))
        A, B, C, D = P[0], P[1], P[2], P[3]
        f = Fig()
        f.poly([A, B, C, D], c="ink", w=4, f="sky", fo=0.15)
        Hf = (D[0], A[1])
        f.line(*D, *Hf, c="red", w=3, d=True)
        f.text(D[0] - 12, (D[1] + Hf[1]) / 2 + 10, f"{h}", z=30, c="red", a="e", b=700)
        dim(f, A, B, f"{b} cm")
        dim(f, D, C, f"{a} cm", side=-1)
        cp = f.poly([A, B, C, D], at=0, c="teal", w=3, f="teal", fo=0.25)
        mid = ((B[0] + C[0]) / 2, (B[1] + C[1]) / 2)
        mv(cp, 0, 0, 0, r=180, cx=mid[0], cy=mid[1])
        f.text(330, max(p[1] for p in P) + 90, f"밑변 {a} + {b} = {a + b}인 평행사변형", z=32, c="gold", at=1)
        q = f"윗변이 {a} cm, 아랫변이 {b} cm, 높이가 {h} cm인 사다리꼴의 넓이는 몇 cm²인가요?"
        S.add(4, q, f"{(a + b) * h // 2} cm²", "똑같은 사다리꼴 2개 → 밑변이 (윗변 + 아랫변)인 평행사변형",
              [L("2개 붙이면 평행사변형", memo=f"밑변 {a} + {b}"), L("(넓이) = ((윗변) + (아랫변)) × (높이) ÷ 2"), L(f"({a} + {b}) × {h} ÷ 2 = {(a + b) * h // 2}")], f.out(), ap=str((a + b) * h // 2), key=q)
    fill(S, 4, 20, g4)

    def g5():
        f = Fig()
        if S.count(5) < 12:
            p = R.randint(4, 16); q_ = R.randint(4, 16)
            if (p * q_) % 2:
                return
            P, s, _ = place([(0, q_ / 2), (p / 2, 0), (p, q_ / 2), (p / 2, q_)], box=(80, 80, 580, 580))
            f.poly([(P[0][0], P[3][1]), (P[2][0], P[3][1]), (P[2][0], P[1][1]), (P[0][0], P[1][1])], at=0, c="soft", w=2, d=True)
            f.poly(P, c="ink", w=4, f="sky", fo=0.18)
            f.line(*P[0], *P[2], c="gold", w=3)
            f.line(*P[1], *P[3], c="teal", w=3)
            f.text((P[0][0] + P[2][0]) / 2 + 60, P[0][1] - 12, f"{p} cm", z=30, c="gold", b=700)
            f.text(P[1][0] + 14, (P[1][1] + P[3][1]) / 2 + 70, f"{q_} cm", z=30, c="teal", a="s", b=700)
            qq = f"두 대각선의 길이가 {p} cm, {q_} cm인 마름모의 넓이는 몇 cm²인가요?"
            S.add(5, qq, f"{p * q_ // 2} cm²", "마름모를 둘러싼 직사각형의 반",
                  [L(f"둘러싼 직사각형 {p} × {q_}", memo="점선"), L("(넓이) = (한 대각선) × (다른 대각선) ÷ 2"), L(f"{p} × {q_} ÷ 2 = {p * q_ // 2}")], f.out(), ap=str(p * q_ // 2), key=qq)
        else:
            W = R.randint(8, 15); H = R.randint(6, 12); w = R.randint(2, W - 3); h = R.randint(2, H - 3)
            P, s, _ = place([(0, 0), (W, 0), (W, H - h), (W - w, H - h), (W - w, H), (0, H)], box=(70, 80, 590, 580))
            Bp, _, _ = place([(0, 0), (W, 0), (W, H), (0, H)], box=(70, 80, 590, 580))
            f.poly(P, c="ink", w=4, f="sky", fo=0.18)
            f.poly([Bp[2], (P[3][0], Bp[2][1]), P[3], P[2]], at=0, c="red", w=3, d=True, f="red", fo=0.12)
            dim(f, P[0], P[1], f"{W} cm")
            dim(f, P[5], P[0], f"{H} cm", off=44)
            dim(f, P[3], P[4], f"{h} cm", c="red", off=40)
            dim(f, P[3], P[2], f"{w} cm", side=-1, c="red")
            qq = f"가로 {W} cm, 세로 {H} cm인 직사각형의 한 귀퉁이에서 가로 {w} cm, 세로 {h} cm인 직사각형을 잘라 냈어요. 남은 도형의 넓이는 몇 cm²인가요?"
            S.add(5, qq, f"{W * H - w * h} cm²", "큰 직사각형에서 잘라 낸 직사각형을 빼요",
                  [L(f"큰 직사각형 {W} × {H} = {W * H}"), L(f"잘라 낸 것 {w} × {h} = {w * h}"), L(f"{W * H} − {w * h} = {W * H - w * h}")], f.out(), ap=str(W * H - w * h), key=qq)
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "e5", "grade": "초5", "level": "초등", "icon": "🧩", "title": "초5 · 약분과 통분 · 다각형의 넓이",
         "desc": "약분과 통분 — 분모가 다른 분수의 덧셈 · 뺄셈 100제 · 다각형의 넓이 100제(잘라 붙이기 · 두 개 붙이기가 움직여요).",
         "thumb": ("b", 70), "sets": [set_a, set_b]}
