# 초4 채우기 — 평면도형의 이동 · 막대그래프 · 꺾은선그래프 · 다각형
import math
from fractions import Fraction as Fr
from core import *
from core import _has_batchim
from fig import Fig
from kit import *

CIRN = "①②③④⑤⑥"

def bat(v):
    return _has_batchim(str(v))

UJ = {"kg": True, "g": True, "cm": False, "m": False, "km": False, "mm": False, "L": False, "mL": False}
def ul(u, a="을", b="를"):
    """단위 뒤 조사 — kg(킬로그램을) · cm(센티미터를)"""
    return u + (a if UJ.get(u, bat(u)) else b)

def DEC(v):
    v = Fr(v).limit_denominator(1000)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{float(v):g}"


# ══════════ 평면도형의 이동 ══════════
def mod12(h):
    h %= 12
    return 12 if h == 0 else h

def dial(f, h, at="q", new=None, new_at=0):
    cx, cy, R = 330, 350, 235
    f.circ(cx, cy, R, c="ink", sw=4, at=at)
    for k in range(1, 13):
        a = math.radians(90 - 30 * k)
        f.text(cx + 192 * math.cos(a), cy - 192 * math.sin(a) + 11, str(k), z=32, b=700, at=at)
        f.line(cx + 222 * math.cos(a), cy - 222 * math.sin(a), cx + 235 * math.cos(a), cy - 235 * math.sin(a), c="ink", w=3, at=at)
    f.circ(cx, cy, 150, c="soft", sw=2, d=True, f="sky", fo=0.08, at=at)
    a = math.radians(90 - 30 * h)
    f.line(cx, cy, cx + 145 * math.cos(a), cy - 145 * math.sin(a), c="ink", w=7, ar=1, at=at)
    f.dot(cx, cy, r=10, at=at)
    if new is not None:
        b = math.radians(90 - 30 * new)
        f.line(cx, cy, cx + 145 * math.cos(b), cy - 145 * math.sin(b), c="gold", w=6, d=True, ar=1, at=new_at)

DIRS = ["오른쪽", "왼쪽", "위쪽", "아래쪽"]
def flip(h, d):
    return mod12(12 - h) if d in ("오른쪽", "왼쪽") else mod12(6 - h)

def move4():
    S = Set("move4", "평면도형의 이동 — 밀기 · 뒤집기 · 돌리기", "평면도형의 이동",
            {1: "점의 이동", 2: "도형 밀기", 3: "뒤집기", 4: "돌리기", 5: "뒤집고 돌리기"},
            pp=8,
            tips={1: "옆으로 몇 칸, 위아래로 몇 칸을 따로 세어 옮겨요",
                  2: "밀어도 모양과 크기는 그대로 — 자리만 바뀌어요",
                  3: "오른쪽(왼쪽)으로 뒤집으면 왼쪽과 오른쪽이, 위쪽(아래쪽)으로 뒤집으면 위와 아래가 바뀌어요",
                  4: "시계 방향으로 90°는 시계의 숫자 3칸 — 180°는 6칸, 360°는 제자리",
                  5: "한 번 움직일 때마다 바늘이 가리키는 수를 메모하며 차례로"},
            note="뒤집기 · 돌리기 문제의 ‘투명한 원판’은 수가 적힌 밑판 위에 바늘만 그려진 투명한 판이에요. 수는 밑판에 그대로 있고 바늘만 움직인다는 것을 먼저 손으로 짚어 보게 해 주세요.")
    R = rng(5401)

    def gridfig(f, at="q"):
        x0, y0, cs = 40, 140, 58
        f.grid(x0, y0, cs, cs, 10, 7, c="soft", sw=1.8, at=at)
        return lambda c, r: (x0 + c * cs, y0 + r * cs)

    def g1():
        a = (R.randint(1, 9), R.randint(1, 6))
        dx, dy = R.randint(-5, 5), R.randint(-4, 4)
        if dx == 0 and dy == 0:
            return
        t = (a[0] + dx, a[1] - dy)
        if not (0 <= t[0] <= 10 and 0 <= t[1] <= 7):
            return
        cand = {t}
        for d in [(dy, dx), (-dx, dy), (dx, -dy), (dx + 1, dy), (dx - 1, dy), (dx, dy + 1), (dx, dy - 1), (dy, -dx)]:
            p = (a[0] + d[0], a[1] - d[1])
            if 0 <= p[0] <= 10 and 0 <= p[1] <= 7 and p != a:
                cand.add(p)
            if len(cand) >= 5:
                break
        if len(cand) < 4:
            return
        cand = list(cand)
        R.shuffle(cand)
        k = cand.index(t)
        f = Fig()
        P = gridfig(f)
        f.dot(*P(*a), r=13, f="ink")
        f.text(P(*a)[0] - 20, P(*a)[1] - 16, "ㄱ", z=34, b=800)
        for i, p in enumerate(cand):
            f.circ(*P(*p), 12, c="ink", sw=3.5)
            f.text(P(*p)[0] + 15, P(*p)[1] - 15, CIRN[i], z=32, b=800, a="s")
        mid = (a[0] + dx, a[1])
        if dx:
            f.line(*P(*a), *P(*mid), c="gold", w=5, ar=1, at=0)
        if dy:
            f.line(*P(*mid), *P(*t), c="gold", w=5, ar=1, at=1 if dx else 0)
        parts = []
        if dx:
            parts.append(f"{'오른쪽' if dx > 0 else '왼쪽'}으로 {abs(dx)}칸")
        if dy:
            parts.append(f"{'위쪽' if dy > 0 else '아래쪽'}으로 {abs(dy)}칸")
        q = f"모눈 위의 점 ㄱ을 {', '.join(parts)} 옮긴 자리에 있는 점은 {CIRN[0]} ~ {CIRN[len(cand) - 1]} 중 어느 것인가요?"
        lines = [L(f"{p} 옮기기") for p in parts] + [L(f"닿은 점 → {CIRN[k]}")]
        S.add(1, q, CIRN[k], "옆으로, 위아래로 따로 세기", lines, f.out(), ap=str(k + 1), qfig=True, key=q + str(cand), dupq=True)
    fill(S, 1, 20, g1)

    def g2():
        if R.random() < 0.2:
            a, b = R.randint(2, 15), R.randint(2, 20)
            d = R.choice(DIRS)
            q = f"한 변이 {a} cm인 정사각형을 {d}으로 {b} cm 밀었어요. 민 정사각형의 네 변의 길이의 합은 몇 cm인가요?"
            lines = [L("밀어도 모양과 크기는 그대로", memo="한 변은 그대로"), L(f"{a} × 4 = {4 * a}")]
            S.add(2, q, f"{4 * a} cm", "밀기는 자리만 바뀌어요", lines, None, ap=str(4 * a), key=q)
            return
        ax = R.choice(["h", "v"])
        n = R.randint(2, 3)
        mv_ = [R.randint(1, 12) * R.choice([1, -1]) for _ in range(n)]
        net = sum(mv_)
        if net == 0:
            return
        pos, neg = ("오른쪽", "왼쪽") if ax == "h" else ("위쪽", "아래쪽")
        say = ", ".join(f"{pos if m > 0 else neg}으로 {abs(m)} cm" for m in mv_)
        q = f"어떤 도형을 {say} 차례로 밀었어요. 처음 자리에서 어느 쪽으로 몇 cm 민 것과 같은가요?"
        expr = " ".join((("+ " if m > 0 else "− ") if i else ("" if m > 0 else "−")) + str(abs(m)) for i, m in enumerate(mv_))
        ans = f"{pos if net > 0 else neg}으로 {abs(net)} cm"
        lines = [L(f"{pos}을 +, {neg}을 −로 메모", memo="방향을 부호로"), L(f"{expr} = {net}"), L(ans)]
        S.add(2, q, ans, "같은 방향은 더하고, 반대 방향은 빼기", lines, None, ap=f"{pos if net > 0 else neg} {abs(net)}", omr="ex", key=q)
    fill(S, 2, 20, g2)

    PRE = ""
    def g3():
        h = R.randint(1, 12)
        f = Fig()
        if R.random() < 0.6:
            d = R.choice(DIRS)
            v = flip(h, d)
            q = f"투명한 원판의 바늘이 {eul(h)} 가리켜요. 원판을 {d}으로 뒤집으면 바늘은 어떤 수를 가리키나요?"
            lr = d in ("오른쪽", "왼쪽")
            lines = [L(f"{d}으로 뒤집기 → {'좌우' if lr else '위아래'}가 바뀌어요", memo="12와 6은 그대로" if lr else "3과 9는 그대로"), L(f"{h} → {v}")]
            dial(f, h, new=v)
            S.add(3, q, str(v), "뒤집으면 바뀌는 쪽과 그대로인 쪽", lines, f.out(), key=q)
        else:
            d1, d2 = R.choice(DIRS), R.choice(DIRS)
            v1 = flip(h, d1)
            v = flip(v1, d2)
            q = f"투명한 원판의 바늘이 {eul(h)} 가리켜요. 원판을 {d1}으로 뒤집고 다시 {d2}으로 뒤집으면 바늘은 어떤 수를 가리키나요?"
            lines = [L(f"{d1}으로 뒤집기: {h} → {v1}", memo="한 번씩 메모"), L(f"{d2}으로 뒤집기: {v1} → {v}")]
            if {d1, d2} <= {"오른쪽", "왼쪽"}:
                lines.append(L("좌우로 두 번 뒤집으면 처음과 같아요"))
            elif {d1, d2} <= {"위쪽", "아래쪽"}:
                lines.append(L("위아래로 두 번 뒤집으면 처음과 같아요"))
            dial(f, h, new=v)
            S.add(3, q, str(v), "한 번 뒤집을 때마다 메모", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        h = R.randint(1, 12)
        cw = R.random() < 0.6
        deg = R.choice([90, 180, 270, 360])
        k = R.randint(1, 3) if deg == 90 else 1
        step = deg // 30 * k
        v = mod12(h + step if cw else h - step)
        way = "시계 방향" if cw else "시계 반대 방향"
        times = f" {k}번" if k > 1 else ""
        q = f"투명한 원판의 바늘이 {eul(h)} 가리켜요. 원판을 {way}으로 {deg}°만큼{times} 돌리면 바늘은 어떤 수를 가리키나요?"
        lines = [L(f"{deg}°는 시계의 숫자 {deg // 30}칸" + (f", {k}번이면 {step}칸" if k > 1 else ""), memo="90° = 숫자 3칸"),
                 L(f"{h}에서 {way}으로 {step}칸 → {v}")]
        f = Fig()
        dial(f, h, new=v)
        S.add(4, q, str(v), "90°만큼 = 숫자 3칸", lines, f.out(), key=q)
    fill(S, 4, 20, g4)

    def g5():
        if R.random() < 0.3:
            k = R.choice([1, 2, 3, 5, 6, 7])
            r = (4 - k % 4) % 4
            q = f"원판을 시계 방향으로 90°만큼 {k}번 돌린 것은 시계 반대 방향으로 90°만큼 몇 번 돌린 것과 같나요? (4번보다 적게)"
            lines = [L(f"90°만큼 4번 = 360° = 제자리", memo="4번마다 처음으로")] + ([L(f"{k} = 4 + {k - 4}")] if k > 4 else []) + \
                    [L(f"시계 방향 {k % 4}번 = 시계 반대 방향 {r}번", memo=f"{k % 4} + {r} = 4")]
            S.add(5, q, f"{r}번", "4번 돌리면 제자리", lines, None, ap=str(r), key=q)
            return
        h = R.randint(1, 12)
        d = R.choice(DIRS)
        cw = R.random() < 0.5
        deg = R.choice([90, 180, 270])
        way = "시계 방향" if cw else "시계 반대 방향"
        v1 = flip(h, d)
        step = deg // 30
        v = mod12(v1 + step if cw else v1 - step)
        q = f"투명한 원판의 바늘이 {eul(h)} 가리켜요. 원판을 {d}으로 뒤집은 다음 {way}으로 {deg}°만큼 돌리면 바늘은 어떤 수를 가리키나요?"
        lines = [L(f"{d}으로 뒤집기: {h} → {v1}", memo="먼저 뒤집기"), L(f"{way}으로 {step}칸: {v1} → {v}", memo=f"{deg}° = 숫자 {step}칸")]
        f = Fig()
        dial(f, h, new=v)
        S.add(5, q, str(v), "움직일 때마다 가리키는 수를 메모", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 막대그래프 ══════════
BTOP = {"좋아하는 과일": ["사과", "배", "귤", "포도", "딸기"], "좋아하는 운동": ["축구", "야구", "수영", "피구", "농구"],
        "좋아하는 계절": ["봄", "여름", "가을", "겨울"], "반별 안경 쓴 학생 수": ["1반", "2반", "3반", "4반", "5반"],
        "좋아하는 악기": ["피아노", "기타", "드럼", "바이올린", "리코더"], "가고 싶은 나라": ["미국", "영국", "일본", "호주", "스페인"]}
def bar4():
    S = Set("bar4", "막대그래프 — 눈금 읽기 · 견주기 · 표와 그래프", "막대그래프",
            {1: "눈금 한 칸의 크기", 2: "막대 읽기", 3: "막대 견주기", 4: "표와 막대그래프", 5: "그래프로 답하기"},
            pp=8,
            tips={1: "눈금 □칸이 ○명이면 한 칸은 ○ ÷ □명",
                  2: "막대 끝의 눈금 칸 수 × 한 칸의 크기",
                  3: "막대가 길수록 많아요 — 차는 칸 수의 차 × 한 칸의 크기",
                  4: "합계에서 아는 칸을 빼고, 한 칸의 크기로 나누면 막대의 칸 수",
                  5: "읽은 수로 셈하기 — 몇 배는 큰 수 ÷ 작은 수"},
            note="막대그래프는 ‘눈금 한 칸이 얼마인가’를 먼저 확인해야 해요. 세로 눈금의 수를 손가락으로 짚어 한 칸의 크기부터 말하게 해 주세요.")
    R = rng(5402)

    def chart(f, names, vals, s, at="q", hl=None):
        n = len(names)
        top = max(vals) // s + 1
        top = max(top, 5)
        x0, x1, yb, yt = 110, 620, 560, 170
        ch = (yb - yt) / top
        for k in range(top + 1):
            y = yb - k * ch
            f.line(x0, y, x1, y, c="soft", w=1.2 if k else 3, at=at)
            if k % (1 if top <= 8 else 2) == 0:
                f.text(x0 - 14, y + 9, str(k * s), z=22, a="e", at=at)
        f.line(x0, yt - 20, x0, yb, c="ink", w=3, at=at)
        f.text(x0 - 14, yt - 34, "(명)", z=22, a="e", at=at)
        bw = (x1 - x0) / n
        for i, (nm, v) in enumerate(zip(names, vals)):
            f.rect(x0 + bw * i + bw * 0.22, yb - v / s * ch, bw * 0.56, v / s * ch, c="ink", sw=2.5, f="sky", fo=0.45, at=at)
            f.text(x0 + bw * i + bw / 2, yb + 34, nm, z=22 if len(nm) >= 4 else 24, b=700, at=at)
            if hl is not None and i in hl:
                f.text(x0 + bw * i + bw / 2, yb - v / s * ch - 14, str(v), z=24, b=700, c="coral", at=0)

    def data(n, s):
        return R.sample(range(1, 12), n) if s == 1 else [s * x for x in R.sample(range(1, 11), n)]

    def g1():
        s = R.choice([2, 5, 10, 20, 50])
        k = R.choice([2, 4, 5, 10])
        u = R.choice(["명", "개", "그루", "대"])
        if R.random() < 0.5:
            q = f"세로 눈금 {k}칸이 {s * k}{ul(u)} 나타내는 막대그래프에서 눈금 한 칸은 몇 {ul(u)} 나타내나요?"
            lines = [L(f"{s * k} ÷ {k} = {s}", memo=f"{k}칸이 {s * k}{u}")]
            S.add(1, q, f"{s}{u}", "전체 ÷ 칸 수", lines, None, ap=str(s), key=q)
        else:
            m = R.randint(3, 12)
            q = f"눈금 한 칸이 {s}{u}인 막대그래프에서 막대가 {m}칸이면 몇 {u}인가요?"
            lines = [L(f"{s} × {m} = {s * m}", memo="한 칸의 크기 × 칸 수")]
            S.add(1, q, f"{s * m}{u}", "한 칸의 크기 × 칸 수", lines, None, ap=str(s * m), key=q)
    fill(S, 1, 20, g1)

    def g2():
        tp = R.choice(list(BTOP))
        n = R.randint(4, min(5, len(BTOP[tp])))
        names = R.sample(BTOP[tp], n)
        s = R.choice([1, 2, 5])
        vals = data(n, s)
        i = R.randrange(n)
        q = f"{eul(tp)} 조사해 막대그래프로 나타냈어요. {eul(names[i])} 고른 학생은 몇 명인가요?" if not tp.startswith("반별") else \
            f"{eul(tp)} 조사해 막대그래프로 나타냈어요. {names[i]}의 안경 쓴 학생은 몇 명인가요?"
        f = Fig()
        chart(f, names, vals, s, hl=[i])
        lines = [L(f"세로 눈금 한 칸 = {s}명", memo="한 칸의 크기부터"), L(f"{names[i]} 막대 {vals[i] // s}칸 → {s} × {vals[i] // s} = {vals[i]}")]
        S.add(2, q, f"{vals[i]}명", "한 칸의 크기 × 칸 수", lines, f.out(), ap=str(vals[i]), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 2, 20, g2)

    def g3():
        tp = R.choice([t for t in BTOP if not t.startswith("반별")])
        n = R.randint(4, min(5, len(BTOP[tp])))
        names = R.sample(BTOP[tp], n)
        s = R.choice([1, 2, 5])
        vals = data(n, s)
        if R.random() < 0.5:
            i = max(range(n), key=lambda k: vals[k])
            j = min(range(n), key=lambda k: vals[k])
            q = f"{eul(tp)} 조사해 막대그래프로 나타냈어요. 가장 많은 학생이 고른 것과 가장 적은 학생이 고른 것의 학생 수의 차는 몇 명인가요?"
        else:
            i, j = R.sample(range(n), 2)
            if vals[i] < vals[j]:
                i, j = j, i
            q = f"{eul(tp)} 조사해 막대그래프로 나타냈어요. {eul(names[i])} 고른 학생은 {eul(names[j])} 고른 학생보다 몇 명 더 많은가요?"
        f = Fig()
        chart(f, names, vals, s, hl=[i, j])
        lines = [L(f"{names[i]} {vals[i]}명, {names[j]} {vals[j]}명", memo=f"한 칸 = {s}명"), L(f"{vals[i]} − {vals[j]} = {vals[i] - vals[j]}")]
        S.add(3, q, f"{vals[i] - vals[j]}명", "두 막대를 읽고 빼기", lines, f.out(), ap=str(vals[i] - vals[j]), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 3, 20, g3)

    def g4():
        tp = R.choice(list(BTOP))
        n = R.randint(4, min(5, len(BTOP[tp])))
        names = R.sample(BTOP[tp], n)
        s = R.choice([1, 2, 5])
        vals = data(n, s)
        h = R.randrange(n)
        tot = sum(vals)
        known = ", ".join(f"{a} {v}명" for k, (a, v) in enumerate(zip(names, vals)) if k != h)
        q = f"{eul(tp)} 조사한 표에서 합계가 {tot}명이고 {known}이에요. 세로 눈금 한 칸을 {s}명으로 하는 막대그래프로 나타내면 {names[h]}의 막대는 몇 칸인가요?"
        kn = [v for k, v in enumerate(vals) if k != h]
        lines = [L(f"{names[h]}: {tot} − {' − '.join(map(str, kn))} = {vals[h]}", memo="합계에서 아는 칸 빼기"), L(f"{vals[h]} ÷ {s} = {vals[h] // s}", memo=f"한 칸 = {s}명")]
        S.add(4, q, f"{vals[h] // s}칸", "모르는 칸부터, 그다음 한 칸의 크기로 나누기", lines, None, ap=str(vals[h] // s), key=q)
    fill(S, 4, 20, g4)

    def g5():
        tp = R.choice([t for t in BTOP if not t.startswith("반별")])
        n = R.randint(4, min(5, len(BTOP[tp])))
        names = R.sample(BTOP[tp], n)
        s = R.choice([1, 2, 5])
        vals = data(n, s)
        t = R.randrange(2)
        f = Fig()
        if t == 0:
            pairs = [(i, j) for i in range(n) for j in range(n) if i != j and vals[i] % vals[j] == 0 and vals[i] // vals[j] >= 2]
            if not pairs:
                return
            i, j = R.choice(pairs)
            q = f"{eul(tp)} 조사해 막대그래프로 나타냈어요. {eul(names[i])} 고른 학생 수는 {eul(names[j])} 고른 학생 수의 몇 배인가요?"
            chart(f, names, vals, s, hl=[i, j])
            lines = [L(f"{names[i]} {vals[i]}명, {names[j]} {vals[j]}명"), L(f"{vals[i]} ÷ {vals[j]} = {vals[i] // vals[j]}")]
            S.add(5, q, f"{vals[i] // vals[j]}배", "큰 수 ÷ 작은 수", lines, f.out(), ap=str(vals[i] // vals[j]), qfig=True, key=q + str(vals), dupq=True)
        else:
            q = f"{eul(tp)} 조사해 막대그래프로 나타냈어요. 조사한 학생은 모두 몇 명인가요?"
            chart(f, names, vals, s, hl=list(range(n)))
            lines = [L(", ".join(f"{a} {v}" for a, v in zip(names, vals)), memo=f"한 칸 = {s}명"), L(f"{' + '.join(map(str, vals))} = {sum(vals)}")]
            S.add(5, q, f"{sum(vals)}명", "막대마다 읽어 모두 더하기", lines, f.out(), ap=str(sum(vals)), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 5, 20, g5)
    return S


# ══════════ 꺾은선그래프 ══════════
LCTX = [("교실의 기온", "도", ["9시", "10시", "11시", "12시", "1시", "2시"], "시각", 1),
        ("운동장의 기온", "도", ["오전 8시", "오전 10시", "낮 12시", "오후 2시", "오후 4시"], "시각", 1),
        ("강낭콩 줄기의 키", "cm", ["1일", "3일", "5일", "7일", "9일", "11일"], "날짜", 1),
        ("민지의 몸무게", "kg", ["1월", "2월", "3월", "4월", "5월", "6월"], "월", 1),
        ("가게의 하루 우유 판매량", "개", ["월", "화", "수", "목", "금"], "요일", 2)]
def line4():
    S = Set("line4", "꺾은선그래프 — 읽기 · 변화 · 중간값 예상", "꺾은선그래프",
            {1: "점 읽기", 2: "변화의 크기", 3: "가장 많이 변한 때", 4: "사이의 값 예상", 5: "눈금과 물결선"},
            pp=8,
            tips={1: "가로에서 때를 찾고 위로 올라가 점의 눈금 읽기",
                  2: "두 점의 값을 읽어 빼기 — 선이 올라가면 늘고 내려가면 줄어요",
                  3: "선이 가장 많이 기울어진 곳이 가장 많이 변한 때",
                  4: "두 점 사이의 한가운데는 두 값의 가운데쯤",
                  5: "필요 없는 부분은 물결선으로 줄여 변화를 크게 보여 줘요"},
            note="꺾은선그래프는 ‘변화’를 보는 그래프예요. 선이 올라가는지 내려가는지, 얼마나 가파른지를 말로 먼저 설명하게 한 뒤 값을 읽게 해 주세요.")
    R = rng(5403)

    def make(ctx):
        nm, u, xs, kind, st = ctx
        base = R.randint(10, 20) if u == "도" else (R.randint(5, 15) if u == "cm" else (R.randint(30, 40) if u == "kg" else R.randint(20, 40)))
        vals = [base]
        for _ in range(len(xs) - 1):
            vals.append(max(1, vals[-1] + R.choice([-3, -2, -1, 1, 2, 3, 4, 5]) * st))
        return vals

    def chart(f, xs, vals, u, st, at="q", hl=None, wave=False):
        lo = min(vals)
        b0 = (lo // (5 * st)) * 5 * st if wave else 0
        b0 = max(0, b0 - (5 * st if wave and b0 == lo else 0))
        top = (max(vals) - b0) // st + 2
        x0, x1, yb, yt = 110, 620, 560, 170
        ch = (yb - yt) / top
        for k in range(top + 1):
            y = yb - k * ch
            f.line(x0, y, x1, y, c="soft", w=1.2 if k else 3, at=at)
            if k % max(1, top // 8 + (1 if top > 10 else 0)) == 0:
                f.text(x0 - 14, y + 8, str(b0 + k * st), z=20, a="e", at=at)
        f.line(x0, yt - 20, x0, yb, c="ink", w=3, at=at)
        if b0 > 0:
            f.poly([(x0 - 10, yb - 4), (x0 - 3, yb - 14), (x0 + 3, yb - 4), (x0 + 10, yb - 14)], c="ink", w=3, z=False, at=at)
        f.text(x0 - 14, yt - 34, f"({u})", z=20, a="e", at=at)
        n = len(xs)
        bw = (x1 - x0) / n
        P = [(x0 + bw * i + bw / 2, yb - (v - b0) / st * ch) for i, v in enumerate(vals)]
        for i, xl in enumerate(xs):
            f.text(P[i][0], yb + 32, xl, z=19 if len(xl) >= 4 else 22, b=700, at=at)
        f.poly(P, c="ink", w=4, z=False, at=at)
        for i, (x, y) in enumerate(P):
            f.dot(x, y, r=8, at=at)
            if hl is not None and i in hl:
                f.text(x, y - 18, DEC(vals[i]), z=22, b=700, c="coral", at=0)
        return P

    def g1():
        ctx = R.choice(LCTX)
        nm, u, xs, kind, st = ctx
        vals = make(ctx)
        i = R.randrange(len(xs))
        q = f"{eul(nm)} 꺾은선그래프로 나타냈어요. {xs[i]}의 {eun(nm.split('의 ')[-1])} 몇 {u}인가요?" if u != "개" else \
            f"{eul(nm)} 꺾은선그래프로 나타냈어요. {xs[i]}요일의 판매량은 몇 개인가요?"
        f = Fig()
        chart(f, xs, vals, u, st, hl=[i], wave=R.random() < 0.5 or max(vals) > 25)
        lines = [L(f"가로에서 {xs[i]}" + ("요일" if u == "개" else "") + " → 위로 올라가 점의 눈금", memo=f"한 칸 = {st}{u}"), L(f"{vals[i]}{u}")]
        S.add(1, q, f"{vals[i]}{u}", "때를 찾고 점의 눈금 읽기", lines, f.out(), ap=str(vals[i]), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 1, 20, g1)

    def g2():
        ctx = R.choice(LCTX)
        nm, u, xs, kind, st = ctx
        vals = make(ctx)
        i, j = sorted(R.sample(range(len(xs)), 2))
        if vals[i] == vals[j]:
            return
        up = vals[j] > vals[i]
        xi, xj = (xs[i] + "요일", xs[j] + "요일") if u == "개" else (xs[i], xs[j])
        q = f"{eul(nm)} 꺾은선그래프로 나타냈어요. {xi}부터 {xj}까지 몇 {u} {'늘었나요' if up else '줄었나요'}?"
        f = Fig()
        chart(f, xs, vals, u, st, hl=[i, j], wave=True)
        d = abs(vals[j] - vals[i])
        lines = [L(f"{xi} {vals[i]}{u}, {xj} {vals[j]}{u}", memo="두 점 읽기"), L(f"{max(vals[i], vals[j])} − {min(vals[i], vals[j])} = {d}")]
        S.add(2, q, f"{d}{u}", "두 점의 값을 읽어 빼기", lines, f.out(), ap=str(d), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 2, 20, g2)

    def g3():
        ctx = R.choice(LCTX)
        nm, u, xs, kind, st = ctx
        vals = make(ctx)
        ds = [abs(vals[k + 1] - vals[k]) for k in range(len(vals) - 1)]
        m = max(ds)
        if ds.count(m) > 1:
            return
        k = ds.index(m)
        xa, xb = (xs[k] + "요일", xs[k + 1] + "요일") if u == "개" else (xs[k], xs[k + 1])
        q = f"{eul(nm)} 꺾은선그래프로 나타냈어요. 바로 이웃한 두 때 사이에서 가장 많이 변한 때는 언제와 언제 사이인가요?"
        f = Fig()
        chart(f, xs, vals, u, st, hl=[k, k + 1], wave=True)
        lines = [L("선이 가장 많이 기울어진 곳 찾기", memo="기울기가 클수록 많이 변해요"), L(f"{wa(xa)} {xb} 사이"), L(f"{max(vals[k], vals[k + 1])} − {min(vals[k], vals[k + 1])} = {m}")]
        S.add(3, q, f"{wa(xa)} {xb} 사이", "가장 많이 기울어진 선분", lines, f.out(), ap=f"{xs[k]}, {xs[k + 1]}", omr="ex", qfig=True, key=q + str(vals), dupq=True)
    fill(S, 3, 20, g3)

    def g4():
        ctx = R.choice([c for c in LCTX if c[3] in ("시각", "날짜")])
        nm, u, xs, kind, st = ctx
        vals = make(ctx)
        k = R.randrange(len(xs) - 1)
        a, b = vals[k], vals[k + 1]
        mid = Fr(a + b, 2)
        if kind == "시각":
            if "오전" in xs[k] or "낮" in xs[k] or "오후" in xs[k]:
                hh = {"오전 8시": "오전 9시", "오전 10시": "오전 11시", "낮 12시": "오후 1시", "오후 2시": "오후 3시"}[xs[k]]
            else:
                hh = xs[k].replace("시", "시 30분")
        else:
            hh = f"{int(xs[k][:-1]) + 1}일"
        q = f"{eul(nm)} 꺾은선그래프로 나타냈어요. {hh}의 {eun(nm.split('의 ')[-1])} 몇 {u}였을까요?"
        f = Fig()
        chart(f, xs, vals, u, st, hl=[k, k + 1], wave=max(vals) > 25)
        lines = [L(f"{xs[k]} {a}{u}, {xs[k + 1]} {b}{u}", memo="양쪽 두 점"), L(f"({a} + {b}) ÷ 2 = {DEC(mid)}", memo="두 값의 가운데쯤")]
        S.add(4, q, f"{DEC(mid)}{u}", "두 점 사이 한가운데 값", lines, f.out(), ap=DEC(mid), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 4, 20, g4)

    def g5():
        if R.random() < 0.5:
            k = R.choice([2, 4, 5, 10])
            v = R.choice([1, 2])
            u = R.choice(["도", "kg", "cm"])
            q = f"세로 눈금 {k}칸이 {v}{ul(u)} 나타내는 꺾은선그래프에서 눈금 한 칸은 몇 {ul(u)} 나타내나요?"
            r = Fr(v, k)
            lines = [L(f"{v} ÷ {k} = {DEC(r)}", memo=f"{k}칸이 {v}{u}")]
            S.add(5, q, f"{DEC(r)}{u}", "나타내는 크기 ÷ 칸 수", lines, None, ap=DEC(r), key=q)
        else:
            ctx = R.choice(LCTX)
            nm, u, xs, kind, st = ctx
            vals = make(ctx)
            q = f"{eul(nm)} 물결선을 넣은 꺾은선그래프로 나타냈어요. 가장 클 때와 가장 작을 때의 차는 몇 {u}인가요?"
            i = max(range(len(vals)), key=lambda k: vals[k])
            j = min(range(len(vals)), key=lambda k: vals[k])
            f = Fig()
            chart(f, xs, vals, u, st, hl=[i, j], wave=True)
            lines = [L(f"가장 높은 점 {vals[i]}{u}, 가장 낮은 점 {vals[j]}{u}", memo="물결선 아래는 0부터 줄인 부분"), L(f"{vals[i]} − {vals[j]} = {vals[i] - vals[j]}")]
            S.add(5, q, f"{vals[i] - vals[j]}{u}", "가장 높은 점과 가장 낮은 점", lines, f.out(), ap=str(vals[i] - vals[j]), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 5, 20, g5)
    return S


# ══════════ 다각형 ══════════
PN = {3: "삼각형", 4: "사각형", 5: "오각형", 6: "육각형", 7: "칠각형", 8: "팔각형", 9: "구각형", 10: "십각형", 12: "십이각형"}
def pgon4():
    S = Set("pgon4", "다각형 — 정다각형 · 대각선 · 각의 크기", "다각형",
            {1: "다각형의 이름", 2: "정다각형의 둘레", 3: "대각선의 수", 4: "정다각형의 한 각", 5: "사각형의 대각선"},
            pp=10,
            tips={1: "변이 □개인 다각형은 □각형 — 꼭짓점도 □개",
                  2: "정다각형은 변의 길이가 모두 같아요 — 한 변 × 변의 수",
                  3: "한 꼭짓점에서 (꼭짓점 수 − 3)개, 꼭짓점마다 그으면 두 번씩 세어져요",
                  4: "한 꼭짓점에서 대각선을 그어 삼각형으로 나누면 각의 합 = 180° × 삼각형 수",
                  5: "직사각형은 두 대각선의 길이가 같고, 평행사변형은 두 대각선이 서로를 반으로 나눠요"},
            note="다각형의 이름은 변의 수로 붙여요. 대각선은 ‘이웃하지 않는 두 꼭짓점을 이은 선분’이라는 뜻을 소리 내어 말하게 한 뒤 세게 해 주세요.")
    R = rng(5404)

    def ngon(f, n, at="q", diag_from=None, regular=True):
        cx, cy, r = 330, 350, 215
        P = [(cx + r * math.cos(2 * math.pi * i / n - math.pi / 2), cy + r * math.sin(2 * math.pi * i / n - math.pi / 2)) for i in range(n)]
        f.poly(P, c="ink", w=4, f="sky", fo=0.15, at=at)
        if diag_from is not None:
            for j in range(2, n - 1):
                f.line(*P[0], *P[j], c="gold", w=3, at=0, dl=(j - 2) * 150)
        return P

    def g1():
        n = R.choice(list(PN))
        t = R.randrange(3)
        if t == 0:
            what = R.choice(["변", "꼭짓점"])
            q = f"{what}이 {n}개인 다각형의 이름은 무엇인가요?"
            lines = [L(f"{what} {n}개 → {PN[n]}")]
            S.add(1, q, PN[n], "변(꼭짓점)의 수로 이름", lines, None, omr="ex", key=q)
        elif t == 1:
            m = R.choice([k for k in PN if k != n])
            q = f"{PN[n]}의 변의 수와 {PN[m]}의 꼭짓점의 수의 합은 몇 개인가요?"
            lines = [L(f"{PN[n]} 변 {n}개, {PN[m]} 꼭짓점 {m}개"), L(f"{n} + {m} = {n + m}")]
            S.add(1, q, f"{n + m}개", "□각형은 변도 꼭짓점도 □개", lines, None, ap=str(n + m), key=q)
        else:
            k = R.randint(2, 5)
            q = f"똑같은 {PN[n]} {k}개를 만드는 데 쓴 변은 모두 몇 개인가요?"
            lines = [L(f"{PN[n]} 하나에 변 {n}개"), L(f"{n} × {k} = {n * k}")]
            S.add(1, q, f"{n * k}개", "도형 하나의 변 수 × 개수", lines, None, ap=str(n * k), key=q)
    fill(S, 1, 20, g1)

    def g2():
        n = R.choice(list(PN))
        a = R.randint(2, 15)
        f = Fig()
        ngon(f, n)
        if R.random() < 0.5:
            q = f"한 변이 {a} cm인 정{PN[n]}의 둘레는 몇 cm인가요?"
            lines = [L("정다각형은 변의 길이가 모두 같아요"), L(f"{a} × {n} = {a * n}")]
            S.add(2, q, f"{a * n} cm", "한 변 × 변의 수", lines, f.out(), ap=str(a * n), key=q)
        else:
            q = f"둘레가 {a * n} cm인 정{PN[n]}의 한 변은 몇 cm인가요?"
            lines = [L(f"변이 {n}개, 길이가 모두 같아요"), L(f"{a * n} ÷ {n} = {a}")]
            S.add(2, q, f"{a} cm", "둘레 ÷ 변의 수", lines, f.out(), ap=str(a), key=q)
    fill(S, 2, 20, g2)

    def g3():
        n = R.choice([4, 5, 6, 7, 8, 9, 10, 12])
        t = R.randrange(4)
        f = Fig()
        ngon(f, n, diag_from=0)
        if t == 2:
            d = n * (n - 3) // 2
            q = f"대각선이 모두 {d}개인 다각형은 무엇인가요?"
            lines = [L("꼭짓점 수 × (꼭짓점 수 − 3) ÷ 2 = 대각선 수", memo="대각선 세는 법을 거꾸로"), L(f"{n} × {n - 3} ÷ 2 = {d}"), L(f"→ {PN[n]}")]
            S.add(3, q, PN[n], "꼭짓점 수를 하나씩 넣어 보기", lines, f.out(), omr="ex", key=q)
            return
        if t == 3:
            q = f"{PN[n]}의 한 꼭짓점에서 대각선을 모두 그으면 삼각형 몇 개로 나뉘나요?"
            lines = [L(f"한 꼭짓점에서 대각선 {n} − 3 = {n - 3}개"), L(f"삼각형 {n - 3} + 1 = {n - 2}개", memo="대각선 수보다 하나 많아요")]
            S.add(3, q, f"{n - 2}개", "대각선 수 + 1", lines, f.out(), ap=str(n - 2), key=q)
            return
        if t == 0:
            d = n * (n - 3) // 2
            q = f"{PN[n]}의 대각선은 모두 몇 개인가요?"
            lines = [L(f"한 꼭짓점에서 {n} − 3 = {n - 3}개", memo="자기와 이웃한 두 꼭짓점 빼기"), L(f"{n} × {n - 3} = {n * (n - 3)}", memo="꼭짓점마다"), L(f"{n * (n - 3)} ÷ 2 = {d}", memo="같은 대각선을 두 번 셌어요")]
            S.add(3, q, f"{d}개", "한 꼭짓점에서 (꼭짓점 수 − 3)개, 두 번 센 것은 반으로", lines, f.out(), ap=str(d), key=q)
        else:
            q = f"{PN[n]}의 한 꼭짓점에서 그을 수 있는 대각선은 몇 개인가요?"
            lines = [L(f"{n} − 3 = {n - 3}", memo="자기 자신과 이웃한 두 꼭짓점 빼기")]
            S.add(3, q, f"{n - 3}개", "자기와 이웃한 꼭짓점에는 못 그어요", lines, f.out(), ap=str(n - 3), key=q)
    fill(S, 3, 20, g3)

    def g4():
        n = R.choice([3, 4, 5, 6, 8, 9, 10, 12])
        t = R.randrange(4)
        tot = 180 * (n - 2)
        f = Fig()
        ngon(f, n, diag_from=0)
        if t == 2 and n > 3:
            q = f"한 각의 크기가 {tot // n}°인 정다각형의 이름은 무엇인가요?"
            lines = [L(f"정{PN[n]}: 180° × {n - 2} ÷ {n} = {tot // n}°", memo="정다각형의 한 각을 차례로 구해 보기"), L(f"→ 정{PN[n]}")]
            S.add(4, q, f"정{PN[n]}", "한 각 = 각의 합 ÷ 각의 수", lines, f.out(), omr="ex", key=q)
            return
        if t == 3 and n > 3:
            q = f"모든 각의 크기의 합이 {tot}°인 다각형의 이름은 무엇인가요?"
            lines = [L(f"{tot}° ÷ 180° = {n - 2}", memo="삼각형 몇 개로 나뉘는지"), L(f"삼각형 {n - 2}개 → 꼭짓점 {n}개 → {PN[n]}", memo="삼각형 수 + 2 = 꼭짓점 수")]
            S.add(4, q, PN[n], "각의 합 ÷ 180° = 삼각형 수", lines, f.out(), omr="ex", key=q)
            return
        if t != 1 or n == 3:
            q = f"{PN[n]}의 모든 각의 크기의 합은 몇 도인가요?" if n > 3 else "삼각형의 세 각의 크기의 합은 몇 도인가요?"
            lines = [L(f"한 꼭짓점에서 대각선을 그으면 삼각형 {n - 2}개"), L(f"180° × {n - 2} = {tot}°")]
            S.add(4, q, f"{tot}°", "삼각형으로 나누어 180°씩", lines, f.out(), ap=str(tot), key=q)
        else:
            q = f"정{PN[n]}의 한 각의 크기는 몇 도인가요?"
            lines = [L(f"모든 각의 합: 180° × {n - 2} = {tot}°", memo="삼각형으로 나누기"), L(f"{tot}° ÷ {n} = {tot // n}°", memo="정다각형은 각의 크기가 모두 같아요")]
            S.add(4, q, f"{tot // n}°", "각의 합 ÷ 각의 수", lines, f.out(), ap=str(tot // n), key=q)
    fill(S, 4, 20, g4)

    def g5():
        t = R.randrange(3)
        a = R.randint(4, 30)
        if t == 0:
            q = f"직사각형의 한 대각선의 길이가 {a} cm일 때, 다른 대각선의 길이는 몇 cm인가요?"
            lines = [L("직사각형은 두 대각선의 길이가 같아요"), L(f"{a} cm")]
            S.add(5, q, f"{a} cm", "직사각형 — 두 대각선의 길이가 같다", lines, None, ap=str(a), key=q)
        elif t == 1:
            a = 2 * R.randint(3, 15)
            nm = R.choice(["평행사변형", "마름모", "직사각형"])
            q = f"{nm}의 한 대각선의 길이가 {a} cm일 때, 두 대각선이 만나는 점에서 이 대각선의 한쪽 끝까지의 길이는 몇 cm인가요?"
            lines = [L(f"{nm}의 두 대각선은 서로를 반으로 나눠요"), L(f"{a} ÷ 2 = {a // 2}")]
            S.add(5, q, f"{a // 2} cm", "두 대각선이 서로를 반으로", lines, None, ap=str(a // 2), key=q)
        else:
            nm = R.choice(["정사각형", "직사각형"])
            q = f"{nm}의 한 대각선의 길이가 {a} cm일 때, 두 대각선의 길이의 합은 몇 cm인가요?"
            lines = [L(f"{nm}은 두 대각선의 길이가 같아요"), L(f"{a} × 2 = {2 * a}")]
            S.add(5, q, f"{2 * a} cm", "두 대각선의 길이가 같다", lines, None, ap=str(2 * a), key=q)
    fill(S, 5, 20, g5)
    return S
