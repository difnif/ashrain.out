# 초3 — ① 곱셈: 자리마다 나누어 곱하기(넓이 모델) · ② 나눗셈: 곱셈을 거꾸로
from core import *
from fig import Fig, mv

# ══════════ ① 곱셈 ══════════
def area(f, cols, rows, at_cell, x0=60, y0=120, W=540, H=430, at_frame="q"):
    """넓이 모델: cols=[(이름, 값)], rows=[(이름, 값)] — 칸(i,j)의 곱이 at_cell[(i,j)] 줄에 나타난다"""
    cv = [max(v, 1) ** 0.5 for _, v in cols]
    rv = [max(v, 1) ** 0.5 for _, v in rows]
    # 너무 좁은 칸은 넓힌다 (넓이 비율은 제곱근으로 줄여 보인다)
    tw = [max(W * v / sum(cv), 140) for v in cv]
    k = W / sum(tw)
    ws = [w * k for w in tw]
    th = [max(H * v / sum(rv), 120) for v in rv]
    k2 = H / sum(th)
    hs = [h * k2 for h in th]
    xs = [x0 + sum(ws[:i]) for i in range(len(ws))]
    ys = [y0 + sum(hs[:i]) for i in range(len(hs))]
    for j, (nm, _) in enumerate(cols):
        f.text(xs[j] + ws[j] / 2, y0 - 22, nm, z=34, c="gold", at=at_frame, b=700)
    for i, (nm, _) in enumerate(rows):
        f.text(x0 - 16, ys[i] + hs[i] / 2 + 12, nm, z=34, c="teal", at=at_frame, b=700, a="e")
    cols_f = ["sky", "lilac", "leaf"]
    for i in range(len(rows)):
        for j in range(len(cols)):
            at = at_cell.get((i, j))
            f.rect(xs[j], ys[i], ws[j], hs[i], at=at_frame, c="ink", sw=3)
            if at is not None:
                f.rect(xs[j] + 3, ys[i] + 3, ws[j] - 6, hs[i] - 6, at=at, c="none", f=cols_f[(i + j) % 3], fo=0.28, hl=True)
                f.text(xs[j] + ws[j] / 2, ys[i] + hs[i] / 2 + 14, com(cols[j][1] * rows[i][1]), z=36 if ws[j] > 130 else 30, at=at, b=700)
    return xs, ys, ws, hs

def place_split(n):
    """214 → [200, 10, 4] (0 인 자리는 뺀다)"""
    s = str(n)
    out = []
    for i, ch in enumerate(s):
        v = int(ch) * 10 ** (len(s) - 1 - i)
        if v:
            out.append(v)
    return out

def set_a():
    S = Set("a", "곱셈 — 자리마다 나누어 곱하기", "곱셈",
            {1: "(몇십)×(몇) · (몇백)×(몇)", 2: "(두 자리)×(한 자리)", 3: "(세 자리)×(한 자리)", 4: "(두 자리)×(몇십)", 5: "(두 자리)×(두 자리)"},
            pp=10,
            tips={1: "40 × 3 → 4 × 3 = 12 → 10이 12개 → 120",
                  2: "23 × 4 = 20 × 4 + 3 × 4 = 80 + 12 = 92 — 자리마다 곱해서 더해요",
                  3: "214 × 3 = 200 × 3 + 10 × 3 + 4 × 3",
                  4: "34 × 20 = 34 × 2 × 10 → 68에 0을 하나 붙여요",
                  5: "26 × 34 → 직사각형을 네 조각으로: 20 × 30 + 20 × 4 + 6 × 30 + 6 × 4"},
            note="곱셈의 원리는 ‘자리마다 나누어 곱하고 더하기’예요(넓이 그림). 세로셈 방법을 외우기 전에 그림의 네 조각이 세로셈의 어느 줄인지 짚어 주세요.")
    R = rng(301)

    def g1():
        k = S.count(1)
        if k < 13:
            a = R.randint(2, 9) * 10; b = R.randint(2, 9)
            t = a // 10
            f = Fig()
            # 묶음 그림: b 줄 × (10이 t개)
            gap = min(66, 520 / b)
            bw, bh = min(56, 520 / t - 8), gap * 0.72
            x0 = 330 - (t * (bw + 8) - 8) / 2
            for i in range(b):
                y = 60 + i * gap
                for j in range(t):
                    f.rect(x0 + j * (bw + 8), y, bw, bh, at="q", c="ink", sw=2, f="gold", fo=0.35, rx=4, dl=i * 120)
                    f.text(x0 + j * (bw + 8) + bw / 2, y + bh / 2 + 8, "10", z=min(22, bh * 0.55), at="q", dl=i * 120, ho=False)
            f.text(330, 60 + b * gap + 50, f"10이 {t * b}개 → {com(a * b)}", z=36, c="gold", at=0)
            S.add(1, f"{a} × {J(b, '은', '는')} 얼마인가요?", com(a * b), "몇십은 10이 몇 개인지 보고 곱해요",
                  [L(f"{t} × {b} = {t * b}", memo=f"10이 {t * b}개"), L(f"{a} × {b} = {com(a * b)}")], f.out(), ap=str(a * b), key=f"{a}x{b}")
        else:
            a = R.randint(2, 9) * 100; b = R.randint(2, 9)
            t = a // 100
            S.add(1, f"{a} × {J(b, '은', '는')} 얼마인가요?", com(a * b), "몇백은 100이 몇 개인지 보고 곱해요",
                  [L(f"{t} × {b} = {t * b}", memo=f"100이 {t * b}개"), L(f"{a} × {b} = {com(a * b)}")], None, ap=str(a * b), key=f"{a}x{b}")
    fill(S, 1, 20, g1)

    def g23(st, lo, hi):
        def g():
            a = R.randint(lo, hi); b = R.randint(2, 9)
            parts = place_split(a)
            if len(parts) < (2 if st == 2 else 3) or a % 10 == 0:
                return
            if st == 2 and S.count(2) >= 6 and (a % 10) * b < 10:
                return
            f = Fig()
            area(f, [(com(p), p) for p in parts], [(str(b), b)], {(0, j): j for j in range(len(parts))}, y0=170, H=300)
            lines = [L(f"{com(p)} × {b} = {com(p * b)}") for p in parts]
            lines.append(L(" + ".join(com(p * b) for p in parts) + f" = {com(a * b)}"))
            S.add(st, f"{a} × {J(b, '은', '는')} 얼마인가요?", com(a * b), f"{J(a, '을', '를')} " + " + ".join(com(p) for p in parts) + "로 나누어 곱해요",
                  lines, f.out(), ap=str(a * b), key=f"{a}x{b}")
        return g
    fill(S, 2, 20, g23(2, 12, 98))
    fill(S, 3, 20, g23(3, 111, 989))

    def g4():
        a = R.randint(12, 98); m = R.randint(2, 9); b = m * 10
        if a % 10 == 0:
            return
        S.add(4, f"{a} × {J(b, '은', '는')} 얼마인가요?", com(a * b), f"{a} × {m}을 먼저, 그다음 × 10" if m in (1, 3, 6, 7, 8) else f"{a} × {m}를 먼저, 그다음 × 10",
              [L(f"{a} × {b} = {a} × {m} × 10", memo=f"{b} = {m} × 10"), L(f"{a} × {m} = {com(a * m)}"), L(f"{com(a * m)} × 10 = {com(a * b)}", memo="0을 하나 붙여요")], None, ap=str(a * b), key=f"{a}x{b}")
    fill(S, 4, 20, g4)

    def g5():
        a = R.randint(12, 98); b = R.randint(12, 98)
        if a % 10 == 0 or b % 10 == 0:
            return
        pa, pb = place_split(a), place_split(b)
        f = Fig()
        cells, k = {}, 0
        for i in range(2):
            for j in range(2):
                cells[(i, j)] = k
                k += 1
        area(f, [(str(p), p) for p in pb], [(str(p), p) for p in pa], cells, x0=90, y0=110, W=510, H=470)
        lines = [L(f"{pa[i]} × {pb[j]} = {com(pa[i] * pb[j])}") for i in range(2) for j in range(2)]
        lines.append(L(" + ".join(com(pa[i] * pb[j]) for i in range(2) for j in range(2)) + f" = {com(a * b)}"))
        S.add(5, f"{a} × {J(b, '은', '는')} 얼마인가요?", com(a * b), "직사각형을 네 조각으로 나누어 곱하고 더해요", lines, f.out(), ap=str(a * b), key=f"{a}x{b}")
    fill(S, 5, 20, g5)
    return S


# ══════════ ② 나눗셈 ══════════
def groups(f, n, size, at_groups=0, extra_at=None):
    """n 개를 size 개씩 묶기 — 묶음마다 상자, 남는 것은 빨강"""
    q, r = divmod(n, size)
    cols = min(size, 9)
    sp_ = 34
    per_row = max(1, min(4, 580 // (cols * sp_ + 24)))
    bw = cols * sp_ + 14
    bh = ((size + cols - 1) // cols) * sp_ + 14
    out_pos = []
    for g in range(q + (1 if r else 0)):
        gx = 30 + (g % per_row) * (bw + 18)
        gy = 60 + (g // per_row) * (bh + 18)
        cnt = size if g < q else r
        if g < q:
            f.rect(gx, gy, bw, bh, at=at_groups, c="gold", sw=3, rx=10, dl=g * 140)
        for i in range(cnt):
            x = gx + 24 + (i % cols) * sp_
            y = gy + 24 + (i // cols) * sp_
            f.dot(x, y, r=12, f="teal" if g < q else "red", at="q")
    return q, r

def set_b():
    S = Set("b", "나눗셈 — 곱셈을 거꾸로", "나눗셈",
            {1: "곱셈구구로 몫 구하기", 2: "나머지가 있는 나눗셈", 3: "(몇십)÷(몇)", 4: "(두 자리)÷(한 자리)", 5: "나머지를 생각하는 문장제"},
            pp=10,
            tips={1: "42 ÷ 6 → 6 × □ = 42 → 6 × 7 = 42 → 몫 7",
                  2: "29 ÷ 4 → 29를 넘지 않는 4단의 곱 28 = 4 × 7 → 몫 7, 나머지 1 (나머지는 4보다 작아요)",
                  3: "80 ÷ 4 → 10이 8개를 4로 나누면 10이 2개씩 → 20",
                  4: "72 ÷ 3 → 72 = 60 + 12로 나누어 60 ÷ 3 = 20, 12 ÷ 3 = 4 → 24",
                  5: "남은 것도 모두 태워야 하면 몫 + 1, 꽉 채운 것만 세면 몫 그대로"},
            note="나눗셈은 곱셈구구를 거꾸로 쓰는 것이에요. 나머지는 항상 나누는 수보다 작아야 하고, (나누는 수) × (몫) + (나머지) = (나누어지는 수)로 꼭 확인하게 해 주세요.")
    R = rng(302)

    def g1():
        d = R.randint(2, 9); q = R.randint(2, 9)
        n = d * q
        f = Fig()
        groups(f, n, q, at_groups=1)
        S.add(1, f"{n} ÷ {J(d, '은', '는')} 얼마인가요?", str(q), f"{d}단에서 {J(n, '이', '가')} 되는 곱을 찾아요",
              [L(f"{d} × □ = {n}"), L(f"{d} × {q} = {n}", memo=f"{d}묶음에 {q}개씩"), L(f"{n} ÷ {d} = {q}")], f.out(), key=f"{n}/{d}")
    fill(S, 1, 20, g1)

    def g2():
        d = R.randint(3, 9); q = R.randint(2, 9); r = R.randint(1, d - 1)
        n = d * q + r
        f = Fig()
        groups(f, n, d, at_groups=0)
        S.add(2, f"{n} ÷ {d}의 몫과 나머지를 구하세요.", f"몫 {q}, 나머지 {r}", f"{J(n, '을', '를')} 넘지 않는 {d}단의 곱을 찾아요",
              [L(f"{d} × {q} = {d * q}", memo=f"{n}보다 크지 않은 가장 큰 곱"), L(f"{n} − {d * q} = {r}", memo=f"{r} < {d}"), L(f"몫 {q}, 나머지 {r}"),
               L(f"확인 {d} × {q} + {r} = {n}")], f.out(), ap=f"{q}, {r}", omr="ex", key=f"{n}/{d}")
    fill(S, 2, 20, g2)

    def g3():
        d = R.randint(2, 9); n = R.randint(2, 9) * 10
        if n % d:
            return
        q = n // d
        t = n // 10
        if t % d == 0:
            lines = [L(f"{t} ÷ {d} = {t // d}", memo=f"10이 {t}개 → 10이 {t // d}개씩"), L(f"{n} ÷ {d} = {q}")]
            plan = f"10이 {t}개를 {d}묶음으로"
        else:
            big = (t // d) * d * 10
            rest = n - big
            if big == 0 or rest % d:
                return
            lines = [L(f"{n} = {big} + {rest}", memo=f"{d}로 나누기 쉬운 수로"), L(f"{big} ÷ {d} = {big // d}"), L(f"{rest} ÷ {d} = {rest // d}"), L(f"{big // d} + {rest // d} = {q}")]
            plan = f"{J(n, '을', '를')} 나누기 쉬운 두 수로 갈라요"
        S.add(3, f"{n} ÷ {J(d, '은', '는')} 얼마인가요?", str(q), plan, lines, None, key=f"{n}/{d}")
    fill(S, 3, 20, g3)

    def g4():
        d = R.randint(2, 9); n = R.randint(21, 99)
        q, r = divmod(n, d)
        if q < 11:
            return
        big = (n // (d * 10)) * d * 10
        rest = n - big
        if big == 0 or rest < d:
            return
        if S.count(4) < 10 and r:
            return
        if S.count(4) >= 10 and not r:
            return
        q2, r2 = divmod(rest, d)
        lines = [L(f"{n} = {big} + {rest}", memo=f"{d} × 10 = {d * 10}의 배수로"), L(f"{big} ÷ {d} = {big // d}")]
        if r:
            lines.append(L(f"{rest} ÷ {d} = {q2} … {r2}"))
            lines.append(L(f"몫 {big // d} + {q2} = {q}, 나머지 {r}"))
            lines.append(L(f"확인 {d} × {q} + {r} = {n}"))
            ans, ap, omr, q_ = f"몫 {q}, 나머지 {r}", f"{q}, {r}", "ex", f"{n} ÷ {d}의 몫과 나머지를 구하세요."
        else:
            lines.append(L(f"{rest} ÷ {d} = {q2}"))
            lines.append(L(f"{big // d} + {q2} = {q}"))
            ans, ap, omr, q_ = str(q), str(q), "num", f"{n} ÷ {J(d, '은', '는')} 얼마인가요?"
        S.add(4, q_, ans, f"{J(n, '을', '를')} 나누기 쉬운 두 수로 갈라 나눠요", lines, None, ap=ap, omr=omr, key=f"{n}/{d}")
    fill(S, 4, 20, g4)

    CTX = [
        ("학생 {n}명이 한 대에 {d}명씩 탈 수 있는 보트에 모두 타려고 해요. 보트는 적어도 몇 대 있어야 하나요?", "대", "up", "남은 {r}명도 타야 해요"),
        ("구슬 {n}개를 상자 하나에 {d}개씩 담으려고 해요. 구슬을 모두 담으려면 상자는 적어도 몇 개 있어야 하나요?", "개", "up", "남은 {r}개도 담아야 해요"),
        ("사탕 {n}개를 한 봉지에 {d}개씩 담으면 몇 봉지를 가득 채울 수 있나요?", "봉지", "down", "남은 {r}개로는 한 봉지가 안 돼요"),
        ("리본 {n} cm를 {d} cm씩 자르면 {d} cm짜리 리본은 몇 개 생기나요?", "개", "down", "남은 {r} cm는 {d} cm가 안 돼요"),
        ("연필 {n}자루를 {d}명에게 똑같이 나누어 주고 남는 연필은 몇 자루인가요?", "자루", "rem", "나머지가 남는 것"),
        ("의자 {n}개를 한 줄에 {d}개씩 놓으면 마지막 줄에는 의자가 몇 개 놓이나요?", "개", "rem", "꽉 찬 줄 다음 마지막 줄"),
    ]
    def g5():
        d = R.randint(3, 9); q = R.randint(3, 9); r = R.randint(1, d - 1)
        n = d * q + r
        t, unit, how, memo = CTX[S.count(5) % len(CTX)]
        if how == "up":
            ans = q + 1
            lines = [L(f"{n} ÷ {d} = {q} … {r}", memo=memo.format(r=r, d=d)), L(f"{q} + 1 = {q + 1}")]
            plan = "나머지도 들어가야 하면 몫에 1을 더해요"
        elif how == "down":
            ans = q
            lines = [L(f"{n} ÷ {d} = {q} … {r}", memo=memo.format(r=r, d=d)), L(f"답은 몫 그대로 {q}")]
            plan = "꽉 채운 것만 세면 몫 그대로"
        else:
            ans = r
            lines = [L(f"{n} ÷ {d} = {q} … {r}", memo=memo), L(f"확인 {d} × {q} + {r} = {n}"), L(f"남는 것은 나머지 {r}")]
            plan = "묻는 것이 나머지예요"
        S.add(5, t.format(n=n, d=d), f"{ans}{unit}", plan, lines, None, ap=str(ans), key=f"{t[:6]}{n}/{d}")
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "e3", "grade": "초3", "level": "초등", "icon": "✖️", "title": "초3 · 곱셈의 원리 · 나눗셈",
         "desc": "곱셈 — 자리마다 나누어 곱하기 100제(넓이 그림) · 나눗셈 — 곱셈을 거꾸로 100제(묶음 · 나머지 · 문장제).",
         "thumb": ("a", 85), "sets": [set_a, set_b]}
