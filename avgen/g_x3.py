# 초3 채우기 — 평면도형 · 원 · 분수(3-2) · 자료의 정리(그림그래프)
import math
from fractions import Fraction as Fr
from core import *
from core import _has_batchim
from fig import Fig
from kit import *

KN = "ㄱㄴㄷㄹㅁㅂㅅㅇ"

def bat(v):
    return _has_batchim(str(v))


# ══════════ 평면도형 ══════════
def plane3():
    S = Set("plane3", "평면도형 — 선분 · 각 · 직각 · 직사각형 · 정사각형", "평면도형",
            {1: "선분 · 반직선 · 직선", 2: "각과 직각", 3: "직사각형 · 정사각형의 둘레", 4: "잘라 만들기 · 이어 붙이기", 5: "크고 작은 사각형 세기"},
            pp=10,
            tips={1: "두 점을 곧게 이은 선이 선분 — 점마다 다른 점과 하나씩 이어 보고, 두 번 센 것은 반으로",
                  2: "직사각형 · 정사각형은 네 각이 모두 직각, 직각삼각형은 직각이 하나",
                  3: "직사각형의 둘레 = (가로 + 세로) × 2, 정사각형의 둘레 = 한 변 × 4",
                  4: "가로로 몇 개, 세로로 몇 개 들어가는지 따로 세어 곱해요",
                  5: "칸 1개짜리, 2개짜리, 3개짜리 … 크기별로 나누어 세어 더해요"},
            note="도형의 이름은 ‘약속’이에요. 직사각형은 네 각이 모두 직각, 정사각형은 거기에 네 변의 길이까지 같은 사각형 — 정사각형도 직사각형이라는 것을 같이 짚어 주세요.")
    R = rng(5301)

    def pts_circle(f, n, at="q"):
        P = []
        for i in range(n):
            a = 2 * math.pi * i / n - math.pi / 2
            P.append((330 + 200 * math.cos(a), 350 + 200 * math.sin(a)))
        for i, (x, y) in enumerate(P):
            f.dot(x, y, r=10, f="ink", at=at)
            f.text(x + (x - 330) * 0.18, y + (y - 350) * 0.18 + 10, f"점 {KN[i]}", z=24, at=at, b=700)
        return P

    def pts_line(f, n, at="q"):
        P = [(70 + 520 * i / (n - 1), 340) for i in range(n)]
        f.line(30, 340, 630, 340, c="soft", w=2, d=True, at=at)
        for i, (x, y) in enumerate(P):
            f.dot(x, y, r=10, f="ink", at=at)
            f.text(x, y + 46, KN[i], z=26, at=at, b=700)
        return P

    def g1():
        where = R.choice(["원 위", "한 직선 위"])
        what = R.choice(["선분", "직선", "반직선"])
        n = R.randint(3, 8) if where == "원 위" else R.randint(3, 7)
        if where == "한 직선 위" and what == "직선" and n > 5:
            return
        f = Fig()
        if where == "원 위":
            P = pts_circle(f, n)
            if what == "반직선":
                a = n * (n - 1)
                lines = [L(f"시작점 {n}개마다 지나는 점 {n - 1}개", memo="반직선은 시작점이 있어요"), L(f"{n} × {n - 1} = {a}")]
            else:
                a = n * (n - 1) // 2
                lines = [L(f"점 하나에서 다른 점으로 {n - 1}개씩", memo="점마다 이어 보기"), L(f"{n} × {n - 1} = {n * (n - 1)}"), L(f"{n * (n - 1)} ÷ 2 = {a}", memo=f"같은 {what}을 두 번 셌어요")]
                k = 0
                for i in range(n):
                    for j in range(i + 1, n):
                        f.line(*P[i], *P[j], c="sky", w=3, at=0, dl=k * 60)
                        k += 1
        else:
            pts_line(f, n)
            if what == "선분":
                seq = list(range(n - 1, 0, -1))
                a = sum(seq)
                lines = [L(f"왼쪽 점부터 오른쪽 점들과 {', '.join(map(str, seq))}개씩", memo="겹치지 않게 차례로"), L(f"{' + '.join(map(str, seq))} = {a}")]
            elif what == "직선":
                a = 1
                lines = [L("어느 두 점을 지나는 직선도 모두 같은 직선", memo="직선은 양쪽으로 끝없이"), L("1개")]
            else:
                a = 2 * (n - 1)
                lines = [L(f"오른쪽으로 가는 반직선: 맨 오른쪽 점을 뺀 {n - 1}개"), L(f"왼쪽으로 가는 반직선: 맨 왼쪽 점을 뺀 {n - 1}개"), L(f"{n - 1} + {n - 1} = {a}")]
        q = f"{where}에 점 {n}개가 있어요. 이 점들 가운데 두 점을 지나는 {what}은 모두 몇 개 그을 수 있나요?"
        S.add(1, q, f"{a}개", "선분은 두 끝, 반직선은 한 끝, 직선은 끝이 없어요", lines, f.out(), ap=str(a), key=q)
    fill(S, 1, 20, g1)

    RA = {"직사각형": 4, "정사각형": 4, "직각삼각형": 1, "직각이 없는 삼각형": 0}
    def g2():
        t = R.randrange(3)
        if t == 0:
            a, b = R.sample(["직사각형", "정사각형", "직각삼각형"], 2)
            x, y = R.randint(1, 6), R.randint(1, 6)
            q = f"{a} {x}개와 {b} {y}개에 있는 직각은 모두 몇 개인가요?"
            v = RA[a] * x + RA[b] * y
            lines = [L(f"{a} 하나에 {RA[a]}개, {b} 하나에 {RA[b]}개"), L(f"{RA[a]} × {x} + {RA[b]} × {y} = {v}")]
            S.add(2, q, f"{v}개", "도형마다 직각이 몇 개인지", lines, None, ap=str(v), key=q)
        elif t == 1:
            sides = R.choice([3, 4, 5, 6])
            nm = {3: "삼각형", 4: "사각형", 5: "오각형", 6: "육각형"}[sides]
            k = R.randint(2, 6)
            q = f"{nm} {k}개의 각은 모두 몇 개인가요?"
            lines = [L(f"{nm} 하나에 각 {sides}개", memo="꼭짓점마다 각 하나"), L(f"{sides} × {k} = {sides * k}")]
            S.add(2, q, f"{sides * k}개", "꼭짓점마다 각 하나", lines, None, ap=str(sides * k), key=q)
        else:
            x, y, z = R.randint(1, 5), R.randint(1, 5), R.randint(1, 4)
            a = R.choice(["직사각형", "정사각형"])
            q = f"{a} {x}개, 직각삼각형 {y}개, 직각이 없는 삼각형 {z}개에 있는 직각은 모두 몇 개인가요?"
            v = 4 * x + y
            lines = [L(f"{a} 4개씩, 직각삼각형 1개씩, 직각이 없는 삼각형 0개"), L(f"4 × {x} + 1 × {y} + 0 × {z} = {v}")]
            S.add(2, q, f"{v}개", "도형마다 직각이 몇 개인지", lines, None, ap=str(v), key=q)
    fill(S, 2, 20, g2)

    def rect_fig(f, w, h, lw, lh, at="q", sq=False):
        sc = min(420 / w, 300 / h)
        W, H = w * sc, h * sc
        x0, y0 = 330 - W / 2, 330 - H / 2
        f.rect(x0, y0, W, H, c="ink", sw=4, f="sky", fo=0.2, at=at)
        f.text(330, y0 - 18, lw, z=28, at=at, b=700)
        if lh:
            f.text(x0 + W + 18, 330 + 10, lh, z=28, at=at, b=700, a="s")
        for (cx, cy, dx, dy) in ((x0, y0, 1, 1), (x0 + W, y0, -1, 1), (x0, y0 + H, 1, -1), (x0 + W, y0 + H, -1, -1)):
            f.poly([(cx + dx * 22, cy), (cx + dx * 22, cy + dy * 22), (cx, cy + dy * 22)], c="ink", w=2.5, z=False, at=at)

    def g3():
        t = R.randrange(4)
        f = Fig()
        if t == 0:
            w, h = R.sample(range(3, 16), 2)
            q = f"가로가 {w} cm, 세로가 {h} cm인 직사각형의 네 변의 길이의 합은 몇 cm인가요?"
            rect_fig(f, w, h, f"{w} cm", f"{h} cm")
            lines = [L(f"마주 보는 변의 길이가 같아요", memo="직사각형"), L(f"({w} + {h}) × 2 = {(w + h) * 2}")]
            S.add(3, q, f"{(w + h) * 2} cm", "(가로 + 세로) × 2", lines, f.out(), ap=str((w + h) * 2), key=q)
        elif t == 1:
            a = R.randint(3, 25)
            q = f"한 변이 {a} cm인 정사각형의 네 변의 길이의 합은 몇 cm인가요?"
            rect_fig(f, a, a, f"{a} cm", "", sq=True)
            lines = [L("네 변의 길이가 모두 같아요", memo="정사각형"), L(f"{a} × 4 = {a * 4}")]
            S.add(3, q, f"{a * 4} cm", "한 변 × 4", lines, f.out(), ap=str(a * 4), key=q)
        elif t == 2:
            a = R.randint(3, 25)
            q = f"네 변의 길이의 합이 {4 * a} cm인 정사각형의 한 변은 몇 cm인가요?"
            lines = [L("네 변의 길이가 모두 같아요"), L(f"{4 * a} ÷ 4 = {a}")]
            S.add(3, q, f"{a} cm", "네 변의 합 ÷ 4", lines, None, ap=str(a), key=q)
        else:
            w, h = R.sample(range(3, 16), 2)
            q = f"네 변의 길이의 합이 {(w + h) * 2} cm이고 가로가 {w} cm인 직사각형의 세로는 몇 cm인가요?"
            lines = [L(f"(가로 + 세로) × 2 = {(w + h) * 2}"), L(f"가로 + 세로 = {(w + h) * 2} ÷ 2 = {w + h}"), L(f"세로 = {w + h} − {w} = {h}")]
            S.add(3, q, f"{h} cm", "둘레의 반 = 가로 + 세로", lines, None, ap=str(h), key=q)
    fill(S, 3, 20, g3)

    def g4():
        if R.random() < 0.5:
            c = R.randint(2, 6)
            m, n = R.randint(2, 6), R.randint(2, 5)
            w, h = c * m, c * n
            q = f"가로가 {w} cm, 세로가 {h} cm인 직사각형 종이를 잘라 한 변이 {c} cm인 정사각형을 만들려고 해요. 정사각형을 몇 개까지 만들 수 있나요?"
            f = Fig()
            sc = min(500 / w, 340 / h)
            x0, y0 = 330 - w * sc / 2, 340 - h * sc / 2
            f.grid(x0, y0, c * sc, c * sc, m, n, c="ink", sw=2.5, at=0)
            f.rect(x0, y0, w * sc, h * sc, c="ink", sw=4, f="sky", fo=0.15)
            lines = [L(f"가로로 {w} ÷ {c} = {m}개"), L(f"세로로 {h} ÷ {c} = {n}개"), L(f"{m} × {n} = {m * n}")]
            S.add(4, q, f"{m * n}개", "가로로 몇 개 × 세로로 몇 개", lines, f.out(), ap=str(m * n), key=q)
        else:
            s, n = R.randint(2, 9), R.randint(2, 6)
            q = f"한 변이 {s} cm인 정사각형 {n}개를 겹치지 않게 한 줄로 이어 붙여 직사각형을 만들었어요. 만든 직사각형의 네 변의 길이의 합은 몇 cm인가요?"
            f = Fig()
            cs = min(90, 520 / n)
            f.grid(330 - cs * n / 2, 300, cs, cs, n, 1, c="ink", sw=3, f="gold", fo=0.25)
            lines = [L(f"가로 {s} × {n} = {s * n}, 세로 {s}"), L(f"({s * n} + {s}) × 2 = {(s * n + s) * 2}")]
            S.add(4, q, f"{(s * n + s) * 2} cm", "이어 붙인 직사각형의 가로 · 세로부터", lines, f.out(), ap=str((s * n + s) * 2), key=q)
    fill(S, 4, 20, g4)

    def g5():
        t = R.randrange(3)
        if t == 0:
            k = R.randint(2, 7)
            seq = list(range(k, 0, -1))
            q = f"직사각형 {k}개를 한 줄로 이어 붙인 도형이 있어요. 크고 작은 직사각형은 모두 몇 개인가요?"
            f = Fig()
            cs = min(90, 540 / k)
            f.grid(330 - cs * k / 2, 300, cs, cs * 1.3, k, 1, c="ink", sw=3)
            ls = ", ".join(f"{i}칸짜리 {k - i + 1}개" for i in range(1, k + 1)) if k <= 3 else f"1칸짜리 {k}개, 2칸짜리 {k - 1}개, …, {k}칸짜리 1개"
            lines = [L(ls, memo="크기별로"), L(f"{' + '.join(map(str, seq))} = {sum(seq)}")]
            S.add(5, q, f"{sum(seq)}개", "크기별로 나누어 세기", lines, f.out(), ap=str(sum(seq)), key=q)
        elif t == 1:
            n = R.randint(2, 4)
            sq = [(n - i + 1) ** 2 for i in range(1, n + 1)]
            q = f"가로 {n}칸, 세로 {n}칸인 모눈 도형에서 크고 작은 정사각형은 모두 몇 개인가요?"
            f = Fig()
            cs = 300 / n
            f.grid(330 - 150, 200, cs, cs, n, n, c="ink", sw=3)
            lines = [L(", ".join(f"{i}칸짜리 {(n - i + 1) ** 2}개" for i in range(1, n + 1)), memo="한 변이 몇 칸인지 크기별로"), L(f"{' + '.join(map(str, sq))} = {sum(sq)}")]
            S.add(5, q, f"{sum(sq)}개", "크기별로 나누어 세기", lines, f.out(), ap=str(sum(sq)), key=q)
        else:
            a, b = R.randint(2, 9), R.randint(2, 9)
            k = R.randint(2, 6)
            q = f"가로 {a} cm, 세로 {b} cm인 직사각형 {k}개를 가로로 한 줄로 이어 붙였어요. 이어 붙인 도형에서 가장 큰 직사각형의 네 변의 길이의 합은 몇 cm인가요?"
            lines = [L(f"가장 큰 직사각형: 가로 {a} × {k} = {a * k}, 세로 {b}"), L(f"({a * k} + {b}) × 2 = {(a * k + b) * 2}")]
            S.add(5, q, f"{(a * k + b) * 2} cm", "가장 큰 직사각형의 가로 · 세로부터", lines, None, ap=str((a * k + b) * 2), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 원 ══════════
def circ3():
    S = Set("circ3", "원 — 중심 · 반지름 · 지름", "원",
            {1: "반지름과 지름", 2: "원을 이어 그리기", 3: "사각형 안의 원", 4: "맞닿은 원", 5: "원으로 만든 도형의 둘레"},
            pp=10,
            tips={1: "지름 = 반지름 × 2 — 지름은 원 안에서 가장 긴 선분",
                  2: "겹치지 않게 이으면 지름씩, 중심을 지나게 겹치면 반지름씩 늘어요",
                  3: "정사각형 안에 꼭 맞는 원의 지름 = 정사각형의 한 변",
                  4: "밖에서 맞닿으면 중심 사이 = 두 반지름의 합",
                  5: "중심끼리 이은 선분의 길이를 반지름으로 나타내 보기"},
            note="반지름은 중심에서 원 위의 한 점까지, 지름은 원 위의 두 점을 중심을 지나게 이은 선분이에요. 그림에 반지름을 직접 그어 보며 길이를 옮기게 해 주세요.")
    R = rng(5302)

    def g1():
        t = R.randrange(3)
        r = R.randint(2, 30)
        if t == 0:
            q = f"반지름이 {r} cm인 원의 지름은 몇 cm인가요?"
            lines = [L(f"{r} × 2 = {2 * r}", memo="지름 = 반지름 × 2")]
            S.add(1, q, f"{2 * r} cm", "지름 = 반지름 × 2", lines, None, ap=str(2 * r), key=q)
        elif t == 1:
            q = f"지름이 {2 * r} cm인 원의 반지름은 몇 cm인가요?"
            lines = [L(f"{2 * r} ÷ 2 = {r}", memo="반지름 = 지름 ÷ 2")]
            S.add(1, q, f"{r} cm", "반지름 = 지름 ÷ 2", lines, None, ap=str(r), key=q)
        else:
            q = f"컴퍼스를 {r} cm만큼 벌려서 그린 원의 지름은 몇 cm인가요?"
            f = Fig()
            f.circ(330, 340, 210, c="ink", sw=4, f="sky", fo=0.12)
            f.dot(330, 340, r=8)
            f.line(330, 340, 540, 340, c="ink", w=3, at=0)
            f.text(435, 325, f"{r} cm", z=26, at=0, b=700)
            f.line(120, 340, 330, 340, c="gold", w=3, d=True, at=1)
            lines = [L(f"벌린 길이 {r} cm가 반지름", memo="컴퍼스 침 = 원의 중심"), L(f"{r} × 2 = {2 * r}")]
            S.add(1, q, f"{2 * r} cm", "컴퍼스를 벌린 길이 = 반지름", lines, f.out(), ap=str(2 * r), key=q)
    fill(S, 1, 20, g1)

    def g2():
        r, n = R.randint(2, 9), R.randint(2, 6)
        f = Fig()
        if R.random() < 0.5:
            q = f"반지름이 {r} cm인 원 {n}개를 겹치지 않게 한 줄로 맞닿게 그렸어요. 양 끝 원의 바깥쪽 끝 사이의 길이는 몇 cm인가요?"
            cr = min(60, 270 / n)
            for i in range(n):
                f.circ(330 - cr * n + cr + 2 * cr * i, 340, cr, c="ink", sw=3)
            lines = [L(f"지름 {r} × 2 = {2 * r}", memo="원 하나에 지름 하나씩"), L(f"{2 * r} × {n} = {2 * r * n}")]
            S.add(2, q, f"{2 * r * n} cm", "겹치지 않게 이으면 지름씩", lines, f.out(), ap=str(2 * r * n), key=q)
        else:
            q = f"반지름이 {r} cm인 원 {n}개를 각 원이 바로 앞 원의 중심을 지나도록 한 줄로 겹쳐 그렸어요. 양 끝 원의 바깥쪽 끝 사이의 길이는 몇 cm인가요?"
            cr = min(80, 560 / (n + 1))
            for i in range(n):
                f.circ(330 - cr * (n + 1) / 2 + cr + cr * i, 340, cr, c="ink", sw=3)
                f.dot(330 - cr * (n + 1) / 2 + cr + cr * i, 340, r=6)
            lines = [L(f"반지름이 {n + 1}개 늘어선 길이", memo="겹치면 반지름씩"), L(f"{r} × {n + 1} = {r * (n + 1)}")]
            S.add(2, q, f"{r * (n + 1)} cm", "겹쳐 이으면 반지름이 (원의 수 + 1)개", lines, f.out(), ap=str(r * (n + 1)), key=q)
    fill(S, 2, 20, g2)

    def g3():
        t = R.randrange(3)
        f = Fig()
        if t == 0:
            a = R.randint(4, 30)
            q = f"한 변이 {a} cm인 정사각형 안에 꼭 맞게 그린 원의 반지름은 몇 cm인가요?" if a % 2 == 0 else f"한 변이 {a} cm인 정사각형 안에 꼭 맞게 그린 원의 지름은 몇 cm인가요?"
            f.rect(130, 140, 400, 400, c="ink", sw=4)
            f.circ(330, 340, 200, c="ink", sw=3, f="sky", fo=0.15)
            if a % 2 == 0:
                lines = [L(f"원의 지름 = 정사각형의 한 변 = {a}"), L(f"반지름 {a} ÷ 2 = {a // 2}")]
                S.add(3, q, f"{a // 2} cm", "꼭 맞는 원의 지름 = 한 변", lines, f.out(), ap=str(a // 2), key=q)
            else:
                lines = [L(f"원의 지름 = 정사각형의 한 변 = {a}")]
                S.add(3, q, f"{a} cm", "꼭 맞는 원의 지름 = 한 변", lines, f.out(), ap=str(a), key=q)
        else:
            r = R.randint(2, 9)
            m, n = (R.randint(2, 4), 1) if t == 1 else (R.randint(2, 4), R.randint(2, 3))
            q = f"반지름이 {r} cm인 원 {m * n}개가 가로 {m}줄, 세로 {n}줄로 꼭 맞게 들어간 직사각형이 있어요. 직사각형의 네 변의 길이의 합은 몇 cm인가요?" if n > 1 else \
                f"반지름이 {r} cm인 원 {m}개가 한 줄로 꼭 맞게 들어간 직사각형이 있어요. 직사각형의 네 변의 길이의 합은 몇 cm인가요?"
            cr = min(70, 250 / m, 160 / n)
            x0, y0 = 330 - cr * m, 340 - cr * n
            f.rect(x0, y0, 2 * cr * m, 2 * cr * n, c="ink", sw=4)
            for i in range(m):
                for j in range(n):
                    f.circ(x0 + cr + 2 * cr * i, y0 + cr + 2 * cr * j, cr, c="ink", sw=2.5, f="sky", fo=0.12)
            W, H = 2 * r * m, 2 * r * n
            lines = [L(f"가로 = 지름 {m}개 = {2 * r} × {m} = {W}"), L(f"세로 = 지름 {n}개 = {2 * r} × {n} = {H}" if n > 1 else f"세로 = 지름 = {H}"), L(f"({W} + {H}) × 2 = {2 * (W + H)}")]
            S.add(3, q, f"{2 * (W + H)} cm", "가로 · 세로를 지름으로 세기", lines, f.out(), ap=str(2 * (W + H)), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.sample(range(2, 16), 2)
        a, b = max(a, b), min(a, b)
        t = R.randrange(3)
        f = Fig()
        if t == 0:
            q = f"반지름이 {a} cm인 원과 반지름이 {b} cm인 원이 밖에서 한 점에서 맞닿아 있어요. 두 원의 중심 사이의 거리는 몇 cm인가요?"
            s = 280 / (a + b)
            cx1 = 50 + a * s
            f.circ(cx1, 340, a * s, c="ink", sw=3)
            f.circ(cx1 + (a + b) * s, 340, b * s, c="ink", sw=3)
            f.line(cx1, 340, cx1 + (a + b) * s, 340, c="gold", w=3, at=0)
            f.dot(cx1, 340, r=7); f.dot(cx1 + (a + b) * s, 340, r=7)
            lines = [L(f"중심 사이 = 큰 원의 반지름 + 작은 원의 반지름"), L(f"{a} + {b} = {a + b}")]
            S.add(4, q, f"{a + b} cm", "밖에서 맞닿으면 반지름의 합", lines, f.out(), ap=str(a + b), key=q)
        elif t == 1:
            q = f"반지름이 {a} cm인 원 안에 반지름이 {b} cm인 원이 안쪽에서 한 점에서 맞닿아 있어요. 두 원의 중심 사이의 거리는 몇 cm인가요?"
            s = 220 / a
            f.circ(330, 340, a * s, c="ink", sw=3)
            f.circ(330 + (a - b) * s, 340, b * s, c="ink", sw=3)
            f.dot(330, 340, r=7); f.dot(330 + (a - b) * s, 340, r=7)
            f.line(330, 340, 330 + (a - b) * s, 340, c="gold", w=3, at=0)
            lines = [L("큰 원의 반지름 = 중심 사이 + 작은 원의 반지름"), L(f"{a} − {b} = {a - b}")]
            S.add(4, q, f"{a - b} cm", "안에서 맞닿으면 반지름의 차", lines, f.out(), ap=str(a - b), key=q)
        else:
            q = f"큰 원 안에 반지름이 {b} cm인 똑같은 원 2개가 큰 원의 지름 위에 나란히 꼭 맞게 들어 있어요. 큰 원의 반지름은 몇 cm인가요?"
            f.circ(330, 340, 220, c="ink", sw=3)
            f.circ(220, 340, 110, c="ink", sw=3, f="sky", fo=0.12)
            f.circ(440, 340, 110, c="ink", sw=3, f="sky", fo=0.12)
            f.line(110, 340, 550, 340, c="gold", w=3, d=True, at=0)
            lines = [L(f"큰 원의 지름 = 작은 원의 지름 2개 = {2 * b} × 2 = {4 * b}"), L(f"큰 원의 반지름 = {4 * b} ÷ 2 = {2 * b}")]
            S.add(4, q, f"{2 * b} cm", "큰 원의 지름을 작은 원의 지름으로", lines, f.out(), ap=str(2 * b), key=q + "|" + str(b))
    fill(S, 4, 20, g4)

    def g5():
        t = R.randrange(3)
        f = Fig()
        if t == 0:
            r = R.randint(2, 12)
            q = f"반지름이 {r} cm인 원 3개가 서로 맞닿아 있어요. 세 원의 중심을 이은 삼각형의 세 변의 길이의 합은 몇 cm인가요?"
            cr = 110
            C = [(330 - cr, 430), (330 + cr, 430), (330, 430 - cr * math.sqrt(3))]
            for (x, y) in C:
                f.circ(x, y, cr, c="ink", sw=3)
                f.dot(x, y, r=7)
            f.poly(C, c="gold", w=3.5, at=0)
            lines = [L(f"변 하나 = 반지름 2개 = {r} × 2 = {2 * r}"), L(f"{2 * r} × 3 = {6 * r}")]
            S.add(5, q, f"{6 * r} cm", "중심 사이 = 반지름 2개", lines, f.out(), ap=str(6 * r), key=q)
        elif t == 1:
            r = R.randint(2, 12)
            q = f"반지름이 {r} cm인 원 4개가 서로 맞닿게 2줄로 놓여 있어요. 네 원의 중심을 차례로 이은 정사각형의 네 변의 길이의 합은 몇 cm인가요?"
            cr = 95
            C = [(330 - cr, 340 - cr), (330 + cr, 340 - cr), (330 + cr, 340 + cr), (330 - cr, 340 + cr)]
            for (x, y) in C:
                f.circ(x, y, cr, c="ink", sw=3)
                f.dot(x, y, r=7)
            f.poly(C, c="gold", w=3.5, at=0)
            lines = [L(f"한 변 = 반지름 2개 = {r} × 2 = {2 * r}"), L(f"{2 * r} × 4 = {8 * r}")]
            S.add(5, q, f"{8 * r} cm", "중심 사이 = 반지름 2개", lines, f.out(), ap=str(8 * r), key=q)
        else:
            a, b = R.sample(range(2, 12), 2)
            c = R.choice([x for x in range(2, 12) if x not in (a, b)])
            q = f"반지름이 {a} cm, {b} cm, {c} cm인 원 3개가 서로 맞닿아 있어요. 세 원의 중심을 이은 삼각형의 세 변의 길이의 합은 몇 cm인가요?"
            lines = [L(f"변마다 두 반지름의 합: {a} + {b}, {b} + {c}, {c} + {a}"), L(f"({a} + {b} + {c}) × 2 = {2 * (a + b + c)}", memo="반지름마다 두 번씩")]
            S.add(5, q, f"{2 * (a + b + c)} cm", "중심 사이 = 두 반지름의 합", lines, None, ap=str(2 * (a + b + c)), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 분수(3-2) ══════════
def F(a, b):
    return f"{{{a}/{b}}}"

def MX(w, a, b):
    return f"{w}{{{a}/{b}}}"

def frac3():
    S = Set("frac3", "분수 — 묶음의 분수 · 진분수 · 가분수 · 대분수", "분수",
            {1: "전체의 몇 분의 몇", 2: "묶음의 분수만큼", 3: "진분수 · 가분수 · 대분수", 4: "대분수 ↔ 가분수", 5: "분수의 크기 비교"},
            mixed=True, pp=10,
            tips={1: "전체를 똑같이 □로 나눈 것 중 ○ → {○/□}",
                  2: "12의 {1/3} = 12를 똑같이 3묶음으로 나눈 것 중 1묶음",
                  3: "분자 < 분모 → 진분수, 분자 ≥ 분모 → 가분수, 자연수와 진분수 → 대분수",
                  4: "2{1/3} = {6/3} + {1/3} = {7/3} — 자연수를 분모가 같은 분수로",
                  5: "분모가 같으면 분자가 큰 쪽이 커요 — 대분수와 가분수는 한 가지로 바꾸어 견주기"},
            note="‘똑같이 나누기’가 분수의 출발이에요. 묶음의 분수에서는 먼저 몇 묶음으로 나누는지(분모), 그중 몇 묶음인지(분자)를 차례로 말하게 해 주세요.")
    R = rng(5303)

    def bar(f, b, a, at="q"):
        w = 520 / b
        x0 = 330 - 260
        for i in range(b):
            f.rect(x0 + i * w, 280, w, 110, c="ink", sw=3, f="sky" if i < a else None, fo=0.55 if i < a else None, at=at)

    def g1():
        b = R.randint(2, 10)
        a = R.randint(1, b - 1)
        t = R.randrange(2)
        f = Fig()
        bar(f, b, a)
        if t == 0:
            q = f"막대를 똑같이 {b}칸으로 나누어 {a}칸을 색칠했어요. 색칠한 부분은 전체의 얼마인가요?"
            lines = [L(f"전체를 똑같이 {b}로 나눈 것 중 {a}", memo="분모 = 나눈 수, 분자 = 색칠한 수"), L(F(a, b))]
            S.add(1, q, F(a, b), "똑같이 나눈 수가 분모", lines, f.out(), ap=f"{a}/{b}", key=q)
        else:
            q = f"막대를 똑같이 {b}칸으로 나누어 {a}칸을 색칠했어요. 색칠하지 않은 부분은 전체의 얼마인가요?"
            lines = [L(f"색칠하지 않은 칸 {b} − {a} = {b - a}"), L(f"전체의 {F(b - a, b)}")]
            S.add(1, q, F(b - a, b), "남은 칸의 수가 분자", lines, f.out(), ap=f"{b - a}/{b}", key=q)
    fill(S, 1, 20, g1)

    THING = [("구슬", "개"), ("사탕", "개"), ("연필", "자루"), ("색종이", "장"), ("쿠키", "개"), ("귤", "개")]
    def g2():
        b = R.randint(2, 8)
        k = R.randint(2, 8)
        n = b * k
        a = R.randint(1, b - 1)
        th, u = R.choice(THING)
        if R.random() < 0.5:
            q = f"{n}의 {eun(F(a, b))} 얼마인가요?"
            lines = [L(f"{eul(n)} 똑같이 {b}묶음 → 한 묶음에 {n} ÷ {b} = {k}"), L(f"{a}묶음 → {k} × {a} = {k * a}")]
            S.add(2, q, str(k * a), "분모만큼 묶고, 분자만큼 모으기", lines, None, key=q)
        else:
            q = f"{th} {n}{u}의 {eun(F(a, b))} 몇 {u}인가요?"
            f = Fig()
            cw = 560 / b
            for i in range(b):
                f.rect(50 + i * cw + 4, 250, cw - 8, 180, c="soft", sw=2, rx=14, f="sky" if i < a else None, fo=0.15 if i < a else None, at=0)
                for j in range(k):
                    cols = 2 if k > 4 else 1
                    f.circ(50 + i * cw + cw / 2 + ((j % cols) - (cols - 1) / 2) * 30, 280 + (j // cols) * 30, 11, c="ink", sw=2, f="gold", fo=0.5)
            lines = [L(f"{n} ÷ {b} = {k}", memo=f"{b}묶음으로 똑같이"), L(f"{k} × {a} = {k * a}", memo=f"그중 {a}묶음")]
            S.add(2, q, f"{k * a}{u}", "분모만큼 묶고, 분자만큼 모으기", lines, f.out(), ap=str(k * a), key=q)
    fill(S, 2, 20, g2)

    def g3():
        t = R.randrange(3)
        if t == 0:
            b = R.randint(3, 12)
            q = f"분모가 {b}인 진분수는 모두 몇 개인가요?"
            lines = [L(f"분자가 1, 2, …, {b - 1}", memo="분자 < 분모"), L(f"{b - 1}개")]
            S.add(3, q, f"{b - 1}개", "진분수는 분자가 분모보다 작아요", lines, None, ap=str(b - 1), key=q)
        elif t == 1:
            b = R.randint(3, 9)
            hi = R.randint(b + 1, 2 * b + 3)
            q = f"분모가 {b}이고 분자가 {hi} 이하인 가분수는 모두 몇 개인가요?"
            cnt = hi - b + 1
            lines = [L(f"분자가 {b}, {b + 1}, …, {hi}", memo="분자 ≥ 분모"), L(f"{hi} − {b} + 1 = {cnt}")]
            S.add(3, q, f"{cnt}개", "가분수는 분자가 분모와 같거나 커요", lines, None, ap=str(cnt), key=q)
        else:
            fs = []
            while len(fs) < 6:
                kind = R.randrange(3)
                b = R.randint(2, 9)
                if kind == 0:
                    x = F(R.randint(1, b - 1), b)
                elif kind == 1:
                    x = F(R.randint(b, 2 * b + 2), b)
                else:
                    x = MX(R.randint(1, 4), R.randint(1, b - 1), b)
                if x not in [y for y, _ in fs]:
                    fs.append((x, kind))
            want = R.randrange(3)
            nm = ["진분수", "가분수", "대분수"][want]
            cnt = sum(1 for _, k in fs if k == want)
            if not cnt:
                return
            q = f"{', '.join(x for x, _ in fs)} 중에서 {eun(nm)} 몇 개인가요?"
            lines = [L(", ".join(x for x, k in fs if k == want), memo=nm), L(f"{cnt}개")]
            S.add(3, q, f"{cnt}개", "분자와 분모를 견주어 가르기", lines, None, ap=str(cnt), key=q)
    fill(S, 3, 20, g3)

    def g4():
        b = R.randint(2, 9)
        w = R.randint(1, 5)
        a = R.randint(1, b - 1)
        n = w * b + a
        if R.random() < 0.5:
            q = f"{eul(MX(w, a, b))} 가분수로 나타내세요."
            lines = [L(f"{w} = {F(w * b, b)}", memo=f"자연수 {eul(w)} 분모가 {b}인 분수로"), L(f"{MX(w, a, b)} = {F(w * b, b)} + {F(a, b)} = {F(n, b)}")]
            S.add(4, q, F(n, b), "자연수 부분을 분모가 같은 분수로", lines, None, ap=f"{n}/{b}", key=q)
        else:
            q = f"{eul(F(n, b))} 대분수로 나타내세요."
            lines = [L(f"{n} ÷ {b} = {w} … {a}", memo=f"{F(b, b)} = 1이 몇 번"), L(f"{F(n, b)} = {F(w * b, b)} + {F(a, b)} = {MX(w, a, b)}")]
            S.add(4, q, MX(w, a, b), "분자 안에 분모가 몇 번 들어가는지", lines, None, ap=f"{w} {a}/{b}", key=q)
    fill(S, 4, 20, g4)

    def g5():
        b = R.randint(3, 9)
        t = R.randrange(3)
        if t == 0:
            a1, a2 = R.sample(range(1, 3 * b), 2)
            big = R.random() < 0.5
            ans = F(max(a1, a2), b) if big else F(min(a1, a2), b)
            q = f"{wa(F(a1, b))} {F(a2, b)} 중에서 더 {'큰' if big else '작은'} 분수는 무엇인가요?"
            lines = [L("분모가 같아요 → 분자를 견주기"), L(f"{max(a1, a2)} > {min(a1, a2)}"), L(f"더 {'큰' if big else '작은'} 분수 {ans}")]
            S.add(5, q, ans, "분모가 같으면 분자 견주기", lines, None, ap=ans.strip("{}"), key=q)
        elif t == 1:
            w, a = R.randint(1, 4), R.randint(1, b - 1)
            n2 = w * b + a + R.choice([-2, -1, 1, 2])
            if n2 <= b or n2 == w * b + a:
                return
            m = MX(w, a, b)
            q = f"{wa(m)} {F(n2, b)} 중에서 더 큰 분수는 무엇인가요?"
            n1 = w * b + a
            ans = m if n1 > n2 else F(n2, b)
            lines = [L(f"{m} = {F(n1, b)}", memo="가분수로 바꾸기"), L(f"{F(n1, b)} {'>' if n1 > n2 else '<'} {F(n2, b)}"), L(f"더 큰 분수 {ans}")]
            S.add(5, q, ans, "한 가지 꼴로 바꾸어 견주기", lines, None, ap=(f"{w} {a}/{b}" if n1 > n2 else f"{n2}/{b}"), key=q)
        else:
            d1, d2 = R.sample(range(2, 13), 2)
            big = R.random() < 0.5
            ans = F(1, min(d1, d2)) if big else F(1, max(d1, d2))
            q = f"{wa(F(1, d1))} {F(1, d2)} 중에서 더 {'큰' if big else '작은'} 분수는 무엇인가요?"
            lines = [L("분자가 1인 분수(단위분수)는 분모가 작을수록 커요", memo="똑같이 적게 나눌수록 한 조각이 커요"), L(f"더 {'큰' if big else '작은'} 분수 {ans}")]
            S.add(5, q, ans, "단위분수는 분모가 작을수록 커요", lines, None, ap=ans.strip("{}"), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 자료의 정리 — 그림그래프 ══════════
VILL = ["가 마을", "나 마을", "다 마을", "라 마을", "마 마을"]
KIND = [("학생 수", "명", 10, 1), ("사과 생산량", "상자", 100, 10), ("자동차 수", "대", 10, 1), ("책 수", "권", 100, 10), ("우유 판매량", "개", 100, 10)]
def pict():
    S = Set("pict", "자료의 정리 — 표와 그림그래프", "자료의 정리",
            {1: "표 읽기", 2: "그림그래프 읽기", 3: "그림그래프로 견주기", 4: "그림그래프로 나타내기", 5: "그림그래프로 답하기"},
            pp=8,
            tips={1: "합계에서 아는 칸을 빼면 모르는 칸",
                  2: "큰 그림 수 × 큰 그림 값 + 작은 그림 수 × 작은 그림 값",
                  3: "두 칸의 수를 먼저 읽고 견주기",
                  4: "큰 그림은 큰 자리, 작은 그림은 그다음 자리의 숫자만큼",
                  5: "모두의 수는 칸마다 읽은 수를 더해요"},
            note="그림그래프는 그림 크기가 나타내는 수를 먼저 확인해야 해요. ‘큰 그림 하나 = 10’처럼 약속을 소리 내어 읽고 시작하게 해 주세요.")
    R = rng(5304)

    def pgraph(f, names, vals, big, small, unit, at="q", title=""):
        n = len(names)
        rh = min(92, 400 / n)
        y0 = 180
        f.rect(30, y0 - 50, 600, 50 + rh * n, c="ink", sw=2.5, at=at)
        f.line(170, y0 - 50, 170, y0 + rh * n, c="ink", w=2, at=at)
        f.text(100, y0 - 16, "마을", z=24, b=700, at=at)
        f.text(400, y0 - 16, title, z=24, b=700, at=at)
        for i, (nm, v) in enumerate(zip(names, vals)):
            y = y0 + rh * i
            f.line(30, y, 630, y, c="ink", w=1.5, at=at)
            f.text(100, y + rh / 2 + 9, nm, z=24, at=at, b=700)
            x = 200
            for _ in range(v // big):
                f.circ(x + 19, y + rh / 2, 19, c="ink", sw=3, f="ink", fo=0.75, at=at)
                x += 44
            for _ in range((v % big) // small):
                f.circ(x + 10, y + rh / 2, 10, c="ink", sw=2.5, at=at)
                x += 24
        yl = y0 + rh * n + 40
        f.circ(200, yl, 18, c="ink", sw=3, f="ink", fo=0.75, at=at)
        f.text(230, yl + 9, f"{big}{unit}", z=24, a="s", at=at, b=700)
        f.circ(380, yl, 10, c="ink", sw=2.5, at=at)
        f.text(400, yl + 9, f"{small}{unit}", z=24, a="s", at=at, b=700)

    def data(big, small, n):
        return [R.randint(1, 4) * big + R.randint(0, 9) * small for _ in range(n)]

    def g1():
        nm, u, big, small = R.choice(KIND)
        n = R.randint(3, 4)
        names = VILL[:n]
        vals = data(big, small, n)
        h = R.randrange(n)
        tot = sum(vals)
        q = f"마을별 {eul(nm)} 조사한 표에서 합계가 {tot}{u}이에요. " + ", ".join(f"{a} {v}{u}" for i, (a, v) in enumerate(zip(names, vals)) if i != h) + f"일 때, {names[h]}의 {eun(nm)} 몇 {u}인가요?"
        known = [v for i, v in enumerate(vals) if i != h]
        lines = [L(f"{tot} − {' − '.join(map(str, known))} = {vals[h]}", memo="합계에서 아는 칸 빼기")]
        S.add(1, q, f"{vals[h]}{u}", "합계 − 아는 칸", lines, None, ap=str(vals[h]), key=q)
    fill(S, 1, 20, g1)

    def g2():
        nm, u, big, small = R.choice(KIND)
        n = R.randint(3, 4)
        names = VILL[:n]
        vals = data(big, small, n)
        i = R.randrange(n)
        q = f"마을별 {eul(nm)} 그림그래프로 나타냈어요. {names[i]}의 {eun(nm)} 몇 {u}인가요?"
        f = Fig()
        pgraph(f, names, vals, big, small, u, title=nm)
        k1, k2 = vals[i] // big, (vals[i] % big) // small
        lines = [L(f"큰 그림 {k1}개, 작은 그림 {k2}개", memo=f"큰 그림 {big}{u} · 작은 그림 {small}{u}"), L(f"{big} × {k1} + {small} × {k2} = {vals[i]}")]
        S.add(2, q, f"{vals[i]}{u}", "그림 하나가 나타내는 수부터", lines, f.out(), ap=str(vals[i]), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 2, 20, g2)

    def g3():
        nm, u, big, small = R.choice(KIND)
        n = R.randint(3, 4)
        names = VILL[:n]
        vals = data(big, small, n)
        if len(set(vals)) < n:
            return
        a, b = R.sample(range(n), 2)
        hi, lo = (a, b) if vals[a] > vals[b] else (b, a)
        q = f"마을별 {eul(nm)} 그림그래프로 나타냈어요. {eun(names[hi])} {names[lo]}보다 {iga(nm)} 몇 {u} 더 많은가요?"
        f = Fig()
        pgraph(f, names, vals, big, small, u, title=nm)
        lines = [L(f"{names[hi]} {vals[hi]}{u}, {names[lo]} {vals[lo]}{u}", memo="그림 읽기"), L(f"{vals[hi]} − {vals[lo]} = {vals[hi] - vals[lo]}")]
        S.add(3, q, f"{vals[hi] - vals[lo]}{u}", "두 칸을 읽고 빼기", lines, f.out(), ap=str(vals[hi] - vals[lo]), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 3, 20, g3)

    def g4():
        nm, u, big, small = R.choice(KIND)
        v = R.randint(1, 5) * big + R.randint(1, 9) * small
        q = f"큰 그림은 {big}{u}, 작은 그림은 {eul(f'{small}{u}')} 나타내는 그림그래프에 {eul(f'{v}{u}')} 나타내려고 해요. 큰 그림과 작은 그림을 각각 몇 개 그려야 하나요?"
        k1, k2 = v // big, (v % big) // small
        lines = [L(f"{v} = {big} × {k1} + {small} × {k2}"), L(f"큰 그림 {k1}개, 작은 그림 {k2}개")]
        S.add(4, q, f"큰 그림 {k1}개, 작은 그림 {k2}개", "큰 그림부터 채우기", lines, None, ap=f"{k1}, {k2}", omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        nm, u, big, small = R.choice(KIND)
        n = R.randint(3, 4)
        names = VILL[:n]
        vals = data(big, small, n)
        t = R.randrange(2)
        f = Fig()
        pgraph(f, names, vals, big, small, u, title=nm)
        if t == 0:
            ks = sorted(R.sample(range(n), R.randint(2, n)))
            who = f"{['', '', '', '세', '네'][n]} 마을" if len(ks) == n else " · ".join(names[k] for k in ks)
            q = f"마을별 {eul(nm)} 그림그래프로 나타냈어요. {who}의 {eun(nm)} 모두 몇 {u}인가요?"
            sel = [vals[k] for k in ks]
            lines = [L(", ".join(f"{names[k]} {vals[k]}" for k in ks), memo="칸마다 읽기"), L(f"{' + '.join(map(str, sel))} = {sum(sel)}")]
            S.add(5, q, f"{sum(sel)}{u}", "칸마다 읽어 모두 더하기", lines, f.out(), ap=str(sum(sel)), qfig=True, key=q + str(vals), dupq=True)
        else:
            if len(set(vals)) < n:
                return
            i = max(range(n), key=lambda k: vals[k])
            j = min(range(n), key=lambda k: vals[k])
            q = f"마을별 {eul(nm)} 그림그래프로 나타냈어요. {iga(nm)} 가장 많은 마을과 가장 적은 마을의 차는 몇 {u}인가요?"
            lines = [L(f"가장 많은 {names[i]} {vals[i]}, 가장 적은 {names[j]} {vals[j]}", memo="큰 그림이 많은 쪽부터"), L(f"{vals[i]} − {vals[j]} = {vals[i] - vals[j]}")]
            S.add(5, q, f"{vals[i] - vals[j]}{u}", "가장 많은 칸과 가장 적은 칸", lines, f.out(), ap=str(vals[i] - vals[j]), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 5, 20, g5)
    return S
