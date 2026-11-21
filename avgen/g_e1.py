# 초1 — ① 10을 만들어 더하고 빼기 · ② 십 모형과 낱개(100까지의 수)
from core import *
from fig import Fig, mv, ten_frame, rod, cube

# ══════════ ① 10을 만들어 더하고 빼기 ══════════
def frames(f, at="q", two=True):
    a = ten_frame(f, 60, 90, 100, at=at)
    b = ten_frame(f, 60, 350, 100, at=at) if two else None
    return a, b

def set_a():
    S = Set("a", "10을 만들어 더하고 빼기", "10 만들기",
            {1: "가르기와 모으기", 2: "10의 짝꿍", 3: "10을 넘는 덧셈", 4: "10을 이용한 뺄셈", 5: "□가 있는 식 · 세 수"},
            mixed=True, pp=20,
            tips={1: "모으기는 앞의 수 다음부터 이어 세요. 가르기는 덜어 내고 남은 것을 세요.",
                  2: "10칸 상자에서 빈칸이 10의 짝꿍이에요. 1과 9 · 2와 8 · 3과 7 · 4와 6 · 5와 5",
                  3: "8 + 5 → 5를 2와 3으로 갈라 8을 먼저 10으로 채워요 → 10 + 3 = 13",
                  4: "13 − 5 → 13에서 낱개 3을 먼저 빼서 10, 남은 2를 더 빼요 → 8 (또는 10에서 5를 빼고 3을 더해요)",
                  5: "□가 있어도 10을 먼저 만들어요. 세 수는 더해서 10이 되는 둘을 먼저!"},
            note="1학년 덧셈·뺄셈의 핵심은 ‘10을 만들기’예요. 손가락보다 10칸 상자를 떠올리게 하고, 답만 맞히기보다 ‘어떻게 갈랐는지’를 말하게 해 주세요.")
    R = rng(101)

    # 1단계 — 가르기와 모으기
    def g1():
        if R.random() < 0.5:
            n = R.randint(4, 9); a = R.randint(1, n - 1); b = n - a
            f = Fig(); A, _ = frames(f, two=False)
            for i in range(n):
                f.dot(*A[i], r=30, f="gold" if i < a else "teal", at="q" if i < a else 0, dl=0 if i < a else (i - a) * 160)
            for i in range(a, n):
                f.text(A[i][0], A[i][1] + 10, str(i + 1), z=30, c="ink", at=1, dl=(i - a) * 220, ho=False)
            f.text(310, 380, f"{a} + {b} = {n}", z=44, at=2)
            S.add(1, f"{J(a, '과', '와')} {J(b, '을', '를')} 모으면 얼마인가요?", str(n), f"{a} 다음부터 {b}개를 이어 세요",
                  [L(f"{a}개 옆에 {b}개를 더 놓아요"), L(", ".join(str(i) for i in range(a + 1, n + 1)), memo=f"{a} 다음부터 세기"), L(f"{a} + {b} = {n}")], f.out())
        else:
            n = R.randint(5, 10); a = R.randint(1, n - 1); b = n - a
            f = Fig(); A, _ = frames(f, two=False)
            for i in range(n):
                f.dot(*A[i], r=30, f="gold", at="q")
            f.rect(A[0][0] - 46, A[0][1] - 46, 100 * min(a, 5) - 8, 92 if a <= 5 else 192, at=0, c="red", sw=4, rx=14) if a <= 5 else None
            if a > 5:
                f.rect(A[0][0] - 46, A[0][1] - 46, 492, 92, at=0, c="red", sw=4, rx=14)
                f.rect(A[5][0] - 46, A[5][1] - 46, 100 * (a - 5) - 8, 92, at=0, c="red", sw=4, rx=14)
            for i in range(a, n):
                f.dot(*A[i], r=30, f="teal", at=1, dl=(i - a) * 160)
            f.text(310, 380, f"{n} = {a} + {b}", z=44, at=2)
            S.add(1, f"{J(n, '은', '는')} {J(a, '과', '와')} □로 가를 수 있어요. □는 얼마인가요?", str(b), f"{n}개에서 {a}개를 덜어 내고 남은 것을 세요",
                  [L(f"{n}개 중 {a}개를 묶어요"), L(f"남은 것: {b}개", memo="하나씩 세기"), L(f"{n} = {a} + {b}")], f.out(), key=f"split{n}-{a}")
    fill(S, 1, 20, g1)

    # 2단계 — 10의 짝꿍
    forms2 = ["a+□", "□+a", "10은", "10−□"]
    def g2():
        a = R.randint(1, 9); b = 10 - a
        k = forms2[S.count(2) % 4]
        f = Fig(); A, _ = frames(f, two=False)
        for i in range(10):
            if i < a:
                f.dot(*A[i], r=30, f="gold", at="q")
            else:
                f.dot(*A[i], r=30, f="teal", at=0, dl=(i - a) * 150)
        f.text(310, 380, f"빈칸 {b}개", z=40, c="teal", at=0, dl=(b - 1) * 150 + 300)
        if k == "a+□":
            q, ln = f"{a} + □ = 10에서 □는 얼마인가요?", [L(f"10칸 중 {a}칸이 찼어요"), L(f"빈칸을 세면 {b}", memo=f"{a}의 짝꿍"), L(f"{a} + {b} = 10")]
        elif k == "□+a":
            q, ln = f"□ + {a} = 10에서 □는 얼마인가요?", [L(f"10칸 중 {a}칸이 찼어요"), L(f"빈칸을 세면 {b}", memo=f"{a}의 짝꿍"), L(f"{b} + {a} = 10")]
        elif k == "10은":
            q, ln = f"10은 {J(a, '과', '와')} □로 가를 수 있어요. □는 얼마인가요?", [L(f"{a}칸을 묶으면"), L(f"남은 칸 {b}개", memo=f"{a}의 짝꿍"), L(f"10 = {a} + {b}")]
        else:
            q, ln = f"10 − □ = {a}에서 □는 얼마인가요?", [L(f"10개 중 {a}개가 남았어요"), L(f"뺀 것 = 빈칸 {b}개", memo=f"{a}의 짝꿍"), L(f"10 − {b} = {a}")]
        S.add(2, q, str(b), "10칸 상자에서 빈칸을 세요", ln, f.out(), key=k + str(a))
    fill(S, 2, 20, g2)

    # 3단계 — 10을 넘는 덧셈 (10 만들기)
    def g3():
        a = R.randint(2, 9); b = R.randint(2, 9)
        if a + b <= 10 or a + b > 18:
            return
        big_first = a >= b
        x, y = (a, b) if big_first else (b, a)    # x 를 10으로 채운다
        need = 10 - x; rest = y - need
        f = Fig(); A, B = frames(f)
        # 위 상자: x, 아래 상자: y (앞의 수 위)
        for i in range(x):
            f.dot(*A[i], r=30, f="gold", at="q")
        for i in range(y):
            el = f.dot(*B[i], r=30, f="teal", at="q")
            if i < need:
                j = x + i
                mv(el, 1, A[j][0] - B[i][0], A[j][1] - B[i][1])
        f.text(618, 206, "10", z=46, c="gold", at=1, a="m")
        f.text(618, 466, str(rest), z=46, c="teal", at=2, a="m")
        first = f"{x}에 {need}을 더해 10" if need in (1, 3, 6, 7, 8) else f"{x}에 {need}를 더해 10"
        lines = [L(f"{y} = {need} + {rest}", memo=f"{x}의 짝꿍 {need}"), L(f"{x} + {need} = 10"), L(f"10 + {rest} = {a + b}")]
        S.add(3, f"{a} + {J(b, '은', '는')} 얼마인가요?", str(a + b), f"{J(x, '을', '를')} 먼저 10으로 채워요" + ("" if big_first else " (큰 수를 채우면 쉬워요)"), lines, f.out(), key=f"{a}+{b}")
    fill(S, 3, 20, g3)

    # 4단계 — 10을 이용한 뺄셈
    def g4():
        n = R.randint(11, 18); b = R.randint(2, 9)
        u = n - 10
        if b <= u or n - b < 1:
            return
        f = Fig(); A, B = frames(f)
        for i in range(10):
            f.dot(*A[i], r=30, f="gold", at="q")
        for i in range(u):
            f.dot(*B[i], r=30, f="gold", at="q")
        method = "빼고 빼기" if S.count(4) % 2 == 0 else "10에서 빼기"
        if method == "빼고 빼기":
            r2 = b - u
            for i in range(u):
                f.cross(*B[i], s=26, at=1, dl=i * 150)
            for i in range(r2):
                f.cross(*A[9 - i], s=26, at=2, dl=i * 150)
            lines = [L(f"{b} = {u} + {r2}", memo=f"{n}의 낱개 {u} 먼저"), L(f"{n} − {u} = 10"), L(f"10 − {r2} = {n - b}")]
            plan = f"{n}에서 {u}을 먼저 빼서 10을 만들어요" if u in (1, 3, 6, 7, 8) else f"{n}에서 {u}를 먼저 빼서 10을 만들어요"
        else:
            for i in range(b):
                f.cross(*A[9 - i], s=26, at=1, dl=i * 150)
            lines = [L(f"{n} = 10 + {u}"), L(f"10 − {b} = {10 - b}", memo="10에서 빼요"), L(f"{10 - b} + {u} = {n - b}")]
            plan = f"10에서 {J(b, '을', '를')} 빼고 낱개 {J(u, '을', '를')} 더해요"
        f.text(310, 630, f"남은 것 {n - b}개", z=40, c="ink", at=2)
        S.add(4, f"{n} − {J(b, '은', '는')} 얼마인가요?", str(n - b), plan, lines, f.out(), key=f"{n}-{b}")
    fill(S, 4, 20, g4)

    # 5단계 — □가 있는 식 · 세 수
    def g5():
        k = S.count(5) % 4
        if k == 0:                       # a + □ = s
            a = R.randint(3, 9); s = R.randint(11, 17)
            x = s - a
            if not (2 <= x <= 9):
                return
            need, rest = 10 - a, s - 10
            f = Fig(); A, B = frames(f)
            for i in range(a):
                f.dot(*A[i], r=30, f="gold", at="q")
            for i in range(need):
                f.dot(*A[a + i], r=30, f="teal", at=0, dl=i * 150)
            for i in range(rest):
                f.dot(*B[i], r=30, f="teal", at=1, dl=i * 150)
            S.add(5, f"{a} + □ = {s}에서 □는 얼마인가요?", str(x), "10까지 채우고, 10에서 몇 더 가는지 세요",
                  [L(f"{a} + {need} = 10", memo="10까지"), L(f"10 + {rest} = {s}"), L(f"□ = {need} + {rest} = {x}")], f.out(), key=f"a{a}{s}")
        elif k == 1:                     # □ − b = c
            b = R.randint(3, 9); c = R.randint(2, 9)
            s = b + c
            if s <= 10 or s > 18:
                return
            x, y = (c, b) if c >= b else (b, c)
            need, rest = 10 - x, y - (10 - x)
            S.add(5, f"□ − {b} = {c}에서 □는 얼마인가요?", str(s), "빼기를 거꾸로 — 남은 것과 뺀 것을 더해요",
                  [L(f"□ = {c} + {b}", memo="거꾸로 더하기"), L(f"{x} + {need} = 10"), L(f"10 + {rest} = {s}"), L(f"□ = {s}")], None, key=f"m{b}{c}")
        else:                            # 세 수
            while True:
                p = R.randint(1, 9); q_ = 10 - p; r = R.randint(2, 9)
                if p != q_:
                    break
            if k == 2:
                order = (p, q_, r)
                lines = [L(f"{p} + {q_} = 10", memo="10 먼저"), L(f"10 + {r} = {10 + r}")]
                plan = "앞의 두 수가 10이 돼요"
            else:
                order = (p, r, q_)
                lines = [L(f"{p} + {q_} = 10", memo="순서를 바꿔 10"), L(f"10 + {r} = {10 + r}")]
                plan = f"{J(p, '과', '와')} {q_}을 먼저 더하면 10" if q_ in (1, 3, 6, 7, 8) else f"{J(p, '과', '와')} {q_}를 먼저 더하면 10"
            expr = " + ".join(map(str, order))
            S.add(5, f"{J(expr, '은', '는')} 얼마인가요?", str(10 + r), plan, lines, None, key="t" + expr)
    fill(S, 5, 20, g5)
    return S


# ══════════ ② 십 모형과 낱개 ══════════
def blocks(f, n, x0, y0, at="q", tens_f="gold", ones_f="teal", dl=0, ones_cols=2, room=None):
    """n 을 십 모형 + 낱개로 — 낱개 상자 자리 목록을 돌려준다. room: 쓸 수 있는 너비(넘치면 막대 사이를 좁힌다)"""
    t, o = divmod(n, 10)
    step, rw = 34, 26
    if room and t:
        ext = t * step + 16 + (23 + 30 * (min(o, ones_cols) - 1) if o else -16 - step + rw)
        if ext > room:
            step = (room - 16 - (23 + 30 * (min(o, ones_cols) - 1) if o else rw - step - 16)) / t
            rw = min(26, step - 3)
    els = []
    for i in range(t):
        els.append(rod(f, x0 + i * step, y0, at=at, w=rw, f_=tens_f, dl=dl + i * 80))
    pos = []
    for j in range(o):
        x = x0 + t * step + 16 + (j % ones_cols) * 30
        y = y0 + 230 - 23 - (j // ones_cols) * 30
        els.append(cube(f, x, y, at=at, f_=ones_f, dl=dl + (t + j) * 80))
        pos.append((x, y))
    return els, pos

def set_b():
    S = Set("b", "십 모형과 낱개로 읽는 100까지의 수", "100까지의 수",
            {1: "몇십 몇", 2: "뛰어 세기", 3: "크기 비교", 4: "두 자리 덧셈", 5: "두 자리 뺄셈"},
            pp=20,
            tips={1: "10개씩 묶음이 몇 개, 낱개가 몇 개인지 세요. 묶음 4개와 낱개 7개 → 47",
                  2: "10씩 뛰어 세면 10개씩 묶음 수만 1씩, 1씩 뛰어 세면 낱개 수가 1씩 바뀌어요",
                  3: "10개씩 묶음 수가 큰 쪽이 커요. 묶음 수가 같으면 낱개를 비교해요",
                  4: "낱개는 낱개끼리, 10개씩 묶음은 묶음끼리 더해요",
                  5: "낱개는 낱개끼리, 10개씩 묶음은 묶음끼리 빼요"},
            note="수를 ‘10개씩 묶음과 낱개’로 보는 눈이 받아올림·받아내림의 바탕이에요. 그림의 막대(10개)와 낱개를 직접 세게 해 주세요.")
    R = rng(102)

    def g1():
        n = R.randint(21, 99)
        t, o = divmod(n, 10)
        if o == 0 or t > 9:
            return
        f = Fig()
        blocks(f, n, 70, 120)
        f.text(330, 450, f"묶음 {t} → {t * 10}", z=36, c="gold", at=0)
        f.text(330, 510, f"낱개 {o} → {o}", z=36, c="teal", at=1)
        f.text(330, 600, f"{t * 10} + {o} = {n}", z=44, at=2)
        if S.count(1) % 2 == 0:
            S.add(1, f"10개씩 묶음 {t}개와 낱개 {o}개는 얼마인가요?", str(n), "묶음은 몇십, 낱개는 몇",
                  [L(f"10개씩 묶음 {t}개 → {t * 10}"), L(f"낱개 {o}개 → {o}"), L(f"{t * 10} + {o} = {n}")], f.out(), key=f"r{n}")
        else:
            S.add(1, f"{J(n, '은', '는')} 10개씩 묶음 몇 개와 낱개 몇 개인가요?", f"묶음 {t}개, 낱개 {o}개", "십의 자리 숫자 = 묶음 수, 일의 자리 숫자 = 낱개 수",
                  [L(f"{n}의 십의 자리 {t} → 묶음 {t}개"), L(f"일의 자리 {o} → 낱개 {o}개"), L(f"{t * 10} + {o} = {n}")], f.out(), ap=f"{t}, {o}", omr="ex", key=f"w{n}")
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 4
        if k in (0, 1):                      # 10씩
            step = 10 if k == 0 else -10
            n = R.randint(12, 59) if step > 0 else R.randint(45, 99)
            m = R.randint(2, 4)
        else:                                # 1씩 — 몇십을 지나가게
            step = 1 if k == 2 else -1
            base = R.randint(2, 8) * 10
            m = R.randint(3, 5)
            n = base - R.randint(1, m - 1) if step > 0 else base + R.randint(1, m - 1)
        seq = [n + step * i for i in range(m + 1)]
        if not all(1 <= v <= 100 for v in seq):
            return
        f = Fig()
        lo, hi = min(seq), max(seq)
        x0, x1 = 50, 610
        span = max(hi - lo, 1)
        X = lambda v: x0 + (x1 - x0) * (v - lo) / span
        f.line(x0 - 20, 360, x1 + 20, 360, at="q", c="ink", w=3)
        for i, v in enumerate(seq):
            f.line(X(v), 348, X(v), 372, at="q" if i == 0 else 0, c="ink", w=3, dl=i * 300)
            f.text(X(v), 410, str(v), z=30 if m < 5 else 26, at="q" if i == 0 else 0, dl=i * 300, c="gold" if i == m else "ink")
            if i:
                a, b = X(seq[i - 1]), X(v)
                mid, h = (a + b) / 2, 70
                f.poly([(a, 340), (a + (b - a) * 0.2, 340 - h * 0.8), (mid, 340 - h), (b - (b - a) * 0.2, 340 - h * 0.8), (b, 340)], at=0, c="teal", w=4, z=False, dr=True, dl=i * 300, ar=1)
        word = {10: "10씩", -10: "10씩 거꾸로", 1: "1씩", -1: "1씩 거꾸로"}[step]
        memo = "묶음 수만 바뀌어요" if abs(step) == 10 else ("몇십을 지나요" if any(v % 10 == 0 for v in seq[1:]) else "낱개만 바뀌어요")
        S.add(2, f"{n}에서 {word} {m}번 뛰어 세면 얼마인가요?", str(seq[-1]), f"{'10개씩 묶음' if abs(step) == 10 else '낱개'}가 {'1개씩 늘어요' if step > 0 else '1개씩 줄어요'}",
              [L(" → ".join(map(str, seq)), memo=memo), L(f"{m}번 뛰면 {seq[-1]}")], f.out(), key=f"{n}{step}{m}")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        if k < 2:
            a = R.randint(21, 98); b = R.randint(21, 98)
            if a == b or (k == 1 and a // 10 != b // 10) or (k == 0 and a // 10 == b // 10):
                return
            big = max(a, b)
            ta, tb = a // 10, b // 10
            f = Fig()
            blocks(f, a, 40, 150, room=290)
            blocks(f, b, 350, 150, room=290)
            f.text(170, 120, str(a), z=40, at="q")
            f.text(480, 120, str(b), z=40, at="q")
            if ta != tb:
                lines = [L(f"10개씩 묶음: {ta}개, {tb}개", memo="묶음 수부터"), L(f"{ta} {'>' if ta > tb else '<'} {tb} → {J(big, '이', '가')} 더 커요")]
                plan = "10개씩 묶음 수를 먼저 비교해요"
            else:
                oa, ob = a % 10, b % 10
                lines = [L(f"10개씩 묶음: {ta}개로 같아요"), L(f"낱개: {oa}개, {ob}개", memo="낱개 비교"), L(f"{oa} {'>' if oa > ob else '<'} {ob} → {J(big, '이', '가')} 더 커요")]
                plan = "묶음 수가 같으면 낱개 수를 비교해요"
            f.text(330, 470, f"{J(big, '이', '가')} 더 커요", z=38, c="gold", at=len(lines) - 1)
            S.add(3, f"{J(a, '과', '와')} {b} 중에서 더 큰 수는 무엇인가요?", str(big), plan, lines, f.out(), key=f"c{a},{b}")
        else:
            v = sorted(R.sample(range(21, 99), 3))
            if len(set(x // 10 for x in v)) == 1:
                return
            R.shuffle(v)
            small = min(v)
            ts = sorted(set(x // 10 for x in v))
            low = [x for x in v if x // 10 == ts[0]]
            lines = [L(f"10개씩 묶음: " + ", ".join(f"{x // 10}개" for x in v), memo="묶음이 가장 적은 수")]
            if len(low) > 1:
                lines.append(L(f"묶음이 같은 {', '.join(map(str, low))} → 낱개 비교"))
            lines.append(L(f"가장 작은 수: {small}"))
            S.add(3, f"{', '.join(map(str, v))} 중에서 가장 작은 수는 무엇인가요?", str(small), "10개씩 묶음 수가 가장 적은 수를 찾아요", lines, None, key="s" + ",".join(map(str, v)))
    fill(S, 3, 20, g3)

    def g4():
        a = R.randint(11, 78); b = R.randint(2, 68)
        if (a % 10) + (b % 10) >= 10 or a + b > 99:
            return
        if S.count(4) < 4 and b >= 10:
            return
        if S.count(4) >= 4 and b < 10:
            return
        ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
        f = Fig()
        _, pa = blocks(f, a, 40, 60)
        f.text(40, 330, f"+ {b}", z=34, a="s", at="q")
        blocks(f, b, 340, 60, tens_f="lilac", ones_f="leaf")
        f.text(330, 420, f"낱개 {oa} + {ob} = {oa + ob}", z=34, c="teal", at=0)
        f.text(330, 480, f"묶음 {ta} + {tb} = {ta + tb}", z=34, c="gold", at=1)
        f.text(330, 580, f"{a} + {b} = {a + b}", z=44, at=2)
        lines = [L(f"낱개끼리 {oa} + {ob} = {oa + ob}")]
        if tb:
            lines.append(L(f"묶음끼리 {ta} + {tb} = {ta + tb}"))
        else:
            lines.append(L(f"묶음은 그대로 {ta}", memo="더할 묶음이 없어요"))
        lines.append(L(f"{a} + {b} = {a + b}"))
        S.add(4, f"{a} + {J(b, '은', '는')} 얼마인가요?", str(a + b), "낱개는 낱개끼리, 묶음은 묶음끼리", lines, f.out(), key=f"{a}+{b}")
    fill(S, 4, 20, g4)

    def g5():
        a = R.randint(25, 99); b = R.randint(2, a - 10)
        if (a % 10) < (b % 10):
            return
        if S.count(5) < 4 and b >= 10:
            return
        if S.count(5) >= 4 and b < 10:
            return
        ta, oa, tb, ob = a // 10, a % 10, b // 10, b % 10
        f = Fig()
        els, pos = blocks(f, a, 60, 80)
        # 빼는 만큼 × (낱개 먼저, 그다음 묶음)
        for j in range(ob):
            x, y = pos[len(pos) - 1 - j]
            f.cross(x + 11.5, y + 11.5, s=14, at=0, dl=j * 150)
        for i in range(tb):
            x = 60 + (ta - 1 - i) * 34 + 13
            f.line(x - 16, 90, x + 16, 300, at=1, c="red", w=5, dl=i * 200)
            f.line(x + 16, 90, x - 16, 300, at=1, c="red", w=5, dl=i * 200)
        f.text(330, 420, f"낱개 {oa} − {ob} = {oa - ob}", z=34, c="teal", at=0)
        f.text(330, 480, f"묶음 {ta} − {tb} = {ta - tb}", z=34, c="gold", at=1)
        f.text(330, 580, f"{a} − {b} = {a - b}", z=44, at=2)
        lines = [L(f"낱개끼리 {oa} − {ob} = {oa - ob}")]
        if tb:
            lines.append(L(f"묶음끼리 {ta} − {tb} = {ta - tb}"))
        else:
            lines.append(L(f"묶음은 그대로 {ta}", memo="뺄 묶음이 없어요"))
        lines.append(L(f"{a} − {b} = {a - b}"))
        S.add(5, f"{a} − {J(b, '은', '는')} 얼마인가요?", str(a - b), "낱개는 낱개끼리, 묶음은 묶음끼리", lines, f.out(), key=f"{a}-{b}")
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "e1", "grade": "초1", "level": "초등", "icon": "🔟", "title": "초1 · 10 만들기 · 100까지의 수",
         "desc": "10을 만들어 더하고 빼기 100제 · 십 모형과 낱개로 읽는 100까지의 수 100제. 10칸 상자와 십 모형이 판서 줄마다 움직여요.",
         "thumb": ("a", 45), "sets": [set_a, set_b]}
