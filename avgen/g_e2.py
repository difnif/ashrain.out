# 초2 — ① 받아올림 · 받아내림 세로셈 · ② 곱셈구구 — 묶어 세기에서 곱셈으로
from core import *
from fig import Fig, mv, Col

def digits(n):
    return [int(c) for c in reversed(str(n))]

# ══════════ ① 세로셈 ══════════
NAME = ["일", "십", "백"]

def add_lines(a, b, C=None, base=0):
    """덧셈 세로셈 판서 줄 + 그림 (base: 판서 줄 번호 시작)"""
    da, db = digits(a), digits(b)
    n = max(len(da), len(db))
    lines, carry = [], 0
    for p in range(n):
        x, y = (da[p] if p < len(da) else 0), (db[p] if p < len(db) else 0)
        s = x + y + carry
        parts = ([str(carry)] if carry else []) + [str(x)] + ([str(y)] if p < len(db) else [])
        expr = " + ".join(parts) if len(parts) > 1 else parts[0]
        memo = "1 받아올림" if s >= 10 else None
        lines.append(L(f"{NAME[p]}의 자리 {expr} = {s}" if len(parts) > 1 else f"{NAME[p]}의 자리 그대로 {s}", memo=memo))
        if C:
            k = base + len(lines) - 1
            C.digit("r", p, s % 10, at=k)
            if s >= 10:
                C.digit("carry", p + 1, 1, at=k, c="red", z=36, dl=300)
        carry = 1 if s >= 10 else 0
    if carry:
        lines.append(L("백의 자리 1", memo="받아올린 1을 그대로"))
        if C:
            C.digit("r", n, 1, at=base + len(lines) - 1)
    return lines

def sub_lines(a, b, C=None, base=0):
    da, db = digits(a), digits(b)
    lines, borrow = [], 0
    for p in range(len(da)):
        x = da[p] - borrow
        y = db[p] if p < len(db) else 0
        if x < y:
            lines.append(L(f"{NAME[p]}의 자리 {x} − {J(y, '은', '는')} 안 돼요", memo=f"{NAME[p + 1]}에서 10 빌리기"))
            if C:
                k = base + len(lines) - 1
                C.f.cross(C.x(p + 1), C.rows["a"] - 22, s=22, at=k)
                C.digit("carry", p + 1, da[p + 1] - 1, at=k, c="red", z=36, dl=250)
                C.digit("carry", p, x + 10, at=k, c="red", z=36, dl=450, dx=8)
            lines.append(L(f"{x + 10} − {y} = {x + 10 - y}"))
            if C:
                C.digit("r", p, x + 10 - y, at=base + len(lines) - 1)
            borrow = 1
        else:
            if p < len(db):
                pre = f"{NAME[p]}의 자리 {x} − {y} = {x - y}"
            else:
                pre = f"{NAME[p]}의 자리 그대로 {x}"
            lines.append(L(pre, memo=("빌려준 뒤 " + str(x)) if borrow and p < len(db) else None))
            if C and not (p == len(da) - 1 and x - y == 0):
                C.digit("r", p, x - y, at=base + len(lines) - 1)
            borrow = 0
    return lines

def set_a():
    S = Set("a", "받아올림 · 받아내림 세로셈", "세로셈",
            {1: "(두 자리)+(한 자리)", 2: "(두 자리)+(두 자리)", 3: "백의 자리로 받아올림", 4: "받아내림 뺄셈", 5: "□ 구하기"},
            pp=10,
            tips={1: "일의 자리끼리 더해 10이 넘으면 10은 십의 자리로 받아올려 작은 1로 써요",
                  2: "일의 자리부터! 받아올린 1을 십의 자리 위에 써 두고 함께 더해요",
                  3: "십의 자리 합이 10을 넘으면 백의 자리로 1을 받아올려요",
                  4: "일의 자리에서 못 빼면 십의 자리에서 10을 빌려요 — 십의 자리 숫자는 1 작아져요",
                  5: "□ + 38 = 71 → □ = 71 − 38 · 65 − □ = 28 → □ = 65 − 28 · □ − 19 = 44 → □ = 44 + 19"},
            note="세로셈은 ‘일의 자리부터’와 ‘받아올린 1 · 빌려 온 10을 작게 써 두기’가 전부예요. 작은 숫자를 지우지 말고 남겨 두게 해 주세요.")
    R = rng(201)

    def mk(a, b, op):
        f = Fig()
        C = Col(f, ncol=3)
        C.num("a", a)
        C.num("b", b)
        C.op("+" if op == "+" else "−")
        lines = add_lines(a, b, C) if op == "+" else sub_lines(a, b, C)
        res = a + b if op == "+" else a - b
        lines.append(L(f"{a} {op} {b} = {res}"))
        return f, lines, res

    def g1():
        a = R.randint(12, 89); b = R.randint(2, 9)
        if a % 10 + b < 10 or a + b >= 100:
            return
        f, lines, res = mk(a, b, "+")
        S.add(1, f"{a} + {J(b, '은', '는')} 얼마인가요?", str(res), "일의 자리부터 — 10이 넘으면 받아올려요", lines, f.out(), key=f"{a}+{b}")
    fill(S, 1, 20, g1)

    def g2():
        a = R.randint(14, 79); b = R.randint(12, 79)
        if a % 10 + b % 10 < 10 or a + b >= 100:
            return
        f, lines, res = mk(a, b, "+")
        S.add(2, f"{a} + {J(b, '은', '는')} 얼마인가요?", str(res), "받아올린 1을 십의 자리에 함께 더해요", lines, f.out(), key=f"{a}+{b}")
    fill(S, 2, 20, g2)

    def g3():
        a = R.randint(35, 99); b = R.randint(25, 99)
        if a + b < 100 or a + b > 198:
            return
        if S.count(3) < 6 and a % 10 + b % 10 >= 10:
            return
        if S.count(3) >= 6 and a % 10 + b % 10 < 10:
            return
        f, lines, res = mk(a, b, "+")
        S.add(3, f"{a} + {J(b, '은', '는')} 얼마인가요?", str(res), "십의 자리 합이 10을 넘으면 백의 자리로", lines, f.out(), key=f"{a}+{b}")
    fill(S, 3, 20, g3)

    def g4():
        a = R.randint(21, 98); b = R.randint(3, a - 3)
        if a % 10 >= b % 10:
            return
        if S.count(4) < 6 and b >= 10:
            return
        if S.count(4) >= 6 and b < 10:
            return
        f, lines, res = mk(a, b, "−")
        S.add(4, f"{a} − {J(b, '은', '는')} 얼마인가요?", str(res), "일의 자리에서 못 빼면 십의 자리에서 10을 빌려요", lines, f.out(), key=f"{a}-{b}")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:            # □ + b = c
            b = R.randint(12, 59); c = R.randint(b + 11, 98)
            x = c - b
            if c % 10 >= b % 10:
                return
            q, inv, op, A, B = f"□ + {b} = {c}에서 □는 얼마인가요?", f"□ = {c} − {b}", "−", c, b
        elif k == 1:          # a − □ = c
            a = R.randint(31, 98); c = R.randint(11, a - 11)
            x = a - c
            if a % 10 >= c % 10:
                return
            q, inv, op, A, B = f"{a} − □ = {c}에서 □는 얼마인가요?", f"□ = {a} − {c}", "−", a, c
        else:                 # □ − b = c
            b = R.randint(12, 49); c = R.randint(12, 49)
            x = b + c
            if b % 10 + c % 10 < 10 or x >= 100:
                return
            q, inv, op, A, B = f"□ − {b} = {c}에서 □는 얼마인가요?", f"□ = {c} + {b}", "+", c, b
        f = Fig()
        C = Col(f, ncol=3, top=190)
        C.num("a", A, at=0)
        C.num("b", B, at=0)
        C.op("+" if op == "+" else "−", at=0)
        body = add_lines(A, B, C, base=1) if op == "+" else sub_lines(A, B, C, base=1)
        lines = [L(inv, memo="덧셈 ↔ 뺄셈")] + body + [L(f"□ = {x}")]
        S.add(5, q, str(x), "□가 있는 식을 거꾸로 바꿔 세로셈으로", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ ② 곱셈구구 ══════════
def array(f, rows, cols, at="q", split=None, cross_col=None, cross_at=None, dl_row=120, r=None, labels=None, lab_at=None, rsplit=None, cross_row=None):
    """rows × cols 점 배열(한 줄 = 한 묶음). split: 앞 열 수(금빛 | 청록) · rsplit: 위 줄 수 · cross_col/row: 그 열/줄을 × 로"""
    gap = min(560 / max(cols, 1), 520 / max(rows, 1), 62)
    rr = r or gap * 0.32
    x0 = 330 - gap * (cols - 1) / 2 - (30 if labels else 0)
    y0 = 340 - gap * (rows - 1) / 2
    for i in range(rows):
        for j in range(cols):
            col = "gold" if (split is None or j < split) and (rsplit is None or i < rsplit) else "teal"
            f.dot(x0 + j * gap, y0 + i * gap, r=rr, f=col, at=at, dl=i * dl_row)
        if labels:
            f.text(x0 + (cols - 1) * gap + gap * 0.9, y0 + i * gap + 9, str(labels[i]), z=26, c="soft", a="s", at=lab_at if lab_at is not None else at, dl=i * 260)
    if split is not None and 0 < split < cols:
        xs = x0 + (split - 0.5) * gap
        f.line(xs, y0 - gap * 0.6, xs, y0 + (rows - 0.4) * gap, at=0, c="red", w=3, d=True)
    if rsplit is not None and 0 < rsplit < rows:
        ys = y0 + (rsplit - 0.5) * gap
        f.line(x0 - gap * 0.6, ys, x0 + (cols - 0.4) * gap, ys, at=0, c="red", w=3, d=True)
    if cross_col is not None:
        for i in range(rows):
            f.cross(x0 + cross_col * gap, y0 + i * gap, s=rr * 0.9, at=cross_at, dl=i * 120)
    if cross_row is not None:
        for j in range(cols):
            f.cross(x0 + j * gap, y0 + cross_row * gap, s=rr * 0.9, at=cross_at, dl=j * 120)
    return x0, y0, gap

def set_b():
    S = Set("b", "곱셈구구 — 묶어 세기에서 곱셈으로", "곱셈구구",
            {1: "몇씩 몇 묶음", 2: "2단 · 5단 · 3단", 3: "4단 · 6단 · 8단", 4: "7단 · 9단 · 1과 0", 5: "□ 채우기 · 곱셈표"},
            pp=20,
            tips={1: "3씩 4묶음 = 3의 4배 = 3 + 3 + 3 + 3 = 3 × 4",
                  2: "5단은 5씩, 2단은 2씩, 3단은 3씩 뛰어 세요. 5 × 7 → 5, 10, 15, 20, 25, 30, 35",
                  3: "4단은 2단의 2배, 6단은 3단의 2배, 8단은 4단의 2배예요. 6 × 7 = 3 × 7 + 3 × 7",
                  4: "9 × 6 = 10 × 6 − 6 · 7 × 8 = 5 × 8 + 2 × 8 · 1 × 5 = 5 · 5 × 0 = 0",
                  5: "곱하는 두 수의 순서를 바꿔도 곱은 같아요. □ × 6 = 6 × □"},
            note="곱셈구구는 외우기 전에 ‘몇씩 몇 묶음’을 그림으로 보는 단계가 꼭 필요해요. 모르는 단은 아는 단에서 만들어 내게(2배 · 10에서 빼기) 해 주세요.")
    R = rng(202)

    def g1():
        a = R.randint(2, 9); b = R.randint(2, 6)
        f = Fig()
        array(f, b, a, at="q")
        f.text(330, 650, f"{a} × {b} = {a * b}", z=44, at=2)
        S.add(1, f"{a}씩 {b}묶음은 모두 몇 개인가요?", f"{a * b}개", f"{a}씩 {b}묶음 = {a}의 {b}배",
              [L(f"{a}씩 {b}묶음 = {a}의 {b}배"), L(" + ".join([str(a)] * b) + f" = {a * b}", memo=f"{b}번 더하기"), L(f"{a} × {b} = {a * b}")], f.out(), ap=str(a * b), key=f"{a}x{b}")
    fill(S, 1, 20, g1)

    def g2():
        a = (5, 2, 3)[S.count(2) % 3]
        b = R.randint(2, 9)
        f = Fig()
        run = [a * (i + 1) for i in range(b)]
        array(f, b, a, at="q", labels=run, lab_at=0)
        S.add(2, f"{a} × {J(b, '은', '는')} 얼마인가요?", str(a * b), f"{a}씩 {b}번 뛰어 세요",
              [L(f"{a}씩 {b}번 뛰어 세기"), L(", ".join(map(str, run)), memo=f"{b}번째"), L(f"{a} × {b} = {a * b}")], f.out(), key=f"{a}x{b}")
    fill(S, 2, 20, g2)

    def g3():
        a = (4, 6, 8)[S.count(3) % 3]; b = R.randint(2, 9)
        h = a // 2
        f = Fig()
        array(f, b, a, at="q", split=h)
        lines = [L(f"{h} × {b} = {h * b}", memo=f"{a}단 = {h}단의 2배"), L(f"{h * b} + {h * b} = {a * b}"), L(f"{a} × {b} = {a * b}")]
        S.add(3, f"{a} × {J(b, '은', '는')} 얼마인가요?", str(a * b), f"{a}씩을 {h}씩 둘로 나눠 {h}단을 두 번", lines, f.out(), key=f"{a}x{b}")
    fill(S, 3, 20, g3)

    def g4():
        n = S.count(4)
        k = ("9" if n % 2 == 0 else "7") if n < 16 else ("1" if n % 2 == 0 else "0")
        b = R.randint(2, 9)
        f = Fig()
        if k == "9":          # 9 × b = 10 × b − b
            array(f, b, 10, at="q", cross_col=9, cross_at=1)
            a, lines, plan = (9, b), [L(f"10 × {b} = {10 * b}", memo="9는 10보다 1 작아요"), L(f"{10 * b} − {b} = {9 * b}"), L(f"9 × {b} = {9 * b}")], f"10씩 {b}묶음에서 {b}개를 빼요"
        elif k == "7":        # 7 × b = 5 × b + 2 × b
            array(f, b, 7, at="q", split=5)
            a, lines, plan = (7, b), [L(f"5 × {b} = {5 * b}", memo="7 = 5 + 2"), L(f"2 × {b} = {2 * b}"), L(f"{5 * b} + {2 * b} = {7 * b}"), L(f"7 × {b} = {7 * b}")], "7을 5와 2로 나눠 아는 단으로"
        elif k == "1":        # 1 × b
            array(f, b, 1, at="q")
            a, lines, plan = (1, b), [L(f"1씩 {b}묶음", memo="한 묶음에 1개"), L(" + ".join(["1"] * b) + f" = {b}"), L(f"1 × {b} = {b}")], "1씩 몇 묶음은 묶음 수와 같아요"
        else:                 # b × 0
            f = None
            a, lines, plan = (b, 0), [L(f"{b}씩 0묶음", memo="묶음이 없어요"), L("아무것도 없으니 0"), L(f"{b} × 0 = 0")], "0묶음이면 아무것도 없어요"
        S.add(4, f"{a[0]} × {J(a[1], '은', '는')} 얼마인가요?", str(a[0] * a[1]), plan, lines, f.out() if f else None, key=f"{a[0]}x{a[1]}")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            a = R.randint(3, 9); x = R.randint(2, 9)
            run = ", ".join(str(a * i) for i in range(1, x + 1))
            S.add(5, f"□ × {a} = {a * x}에서 □는 얼마인가요?", str(x), "곱하는 순서를 바꿔 아는 단으로",
                  [L(f"□ × {a} = {a} × □", memo="순서를 바꿔도 같아요"), L(f"{a}단: {run}"), L(f"{J(a * x, '은', '는')} {x}번째 → □ = {x}")], None, key=f"L{a}{x}")
        elif k == 1:
            a = R.randint(3, 9); x = R.randint(2, 9)
            run = ", ".join(str(a * i) for i in range(1, x + 1))
            S.add(5, f"{a} × □ = {a * x}에서 □는 얼마인가요?", str(x), f"{a}단을 {a * x}까지 외워요",
                  [L(f"{a}단: {run}"), L(f"{J(a * x, '은', '는')} {x}번째"), L(f"□ = {x}")], None, key=f"R{a}{x}")
        else:
            n = R.choice([12, 16, 18, 24, 36, 8, 6, 20, 28, 30, 40, 42, 45, 48, 54, 56, 63, 72])
            pairs = [(i, n // i) for i in range(2, 10) if n % i == 0 and 2 <= n // i <= 9]
            if len(pairs) < 2:
                return
            uniq = sorted(set(tuple(sorted(p)) for p in pairs))
            first = " = ".join(f"{p} × {q}" for p, q in uniq)
            rev = [f"{q} × {p}" for p, q in uniq if p != q]
            S.add(5, f"곱이 {n}인 곱셈구구(2단 ~ 9단)는 모두 몇 개인가요? (순서가 다르면 다른 것)", f"{len(pairs)}개",
                  f"{J(n, '이', '가')} 되는 두 수를 찾고, 순서를 바꾼 것도 세요",
                  [L(f"{n} = {first}"), L("순서를 바꾼 것: " + ", ".join(rev), memo="같은 수끼리는 하나") if rev else L("순서를 바꿔도 같은 것뿐"), L(f"모두 {len(pairs)}개")], None, ap=str(len(pairs)), key=f"P{n}")
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "e2", "grade": "초2", "level": "초등", "icon": "🧮", "title": "초2 · 세로셈 · 곱셈구구",
         "desc": "받아올림 · 받아내림 세로셈 100제 · 곱셈구구 100제. 받아올린 1 · 빌려 온 10이 작게 써지고, 곱셈은 점 배열이 둘로 나뉘어요.",
         "thumb": ("a", 50), "sets": [set_a, set_b]}
