# 고3 — ① 경우의 수 — 세는 원리(확률과 통계) · ② 여러 가지 미분법(미적분)
from math import gcd, factorial as F, comb as C, perm as Pm, cos as _cos, sin as _sin, pi as PI
from core import *
from fig import Fig, Plane
from g_h2 import pt_slope, tline

x = SYMS["x"]
LET = "ABCDEFGH"

# ══════════ 그림 ══════════
def slots_fig(counts, heads=None, cap=None, res=None):
    f = Fig()
    n = len(counts)
    w, gap = (96, 46) if n <= 4 else (80, 30)
    tot = n * w + (n - 1) * gap
    x0, y0 = 330 - tot / 2, 230
    for i, c in enumerate(counts):
        X = x0 + i * (w + gap)
        f.rect(X, y0, w, w, at="q", c="ink", sw=3, rx=12)
        if heads:
            f.text(X + w / 2, y0 - 24, heads[i], z=26, at="q", c="soft")
        f.text(X + w / 2, y0 + w / 2 + 15, str(c), z=42, at=0, c="coral", b=700, dl=i * 160)
        if i < n - 1:
            f.text(X + w + gap / 2, y0 + w / 2 + 12, "×", z=34, at=1, c="ink", dl=i * 120)
    if cap:
        f.text(330, y0 + w + 80, cap, z=28, at=0, c="soft")
    if res is not None:
        f.text(330, y0 + w + 170, f"= {res}", z=48, at=1, c="ink", b=700, dl=n * 120)
    return f.out()

def word_fig(word):
    f = Fig()
    n = len(word)
    w = min(84, 560 // n)
    x0, y0 = 330 - n * w / 2, 240
    reps = [ch for ch in dict.fromkeys(word) if word.count(ch) > 1]
    cols = ["gold", "teal", "coral"]
    for i, ch in enumerate(word):
        X = x0 + i * w
        f.rect(X + 4, y0, w - 8, w - 8, at="q", c="ink", sw=3, rx=10)
        if ch in reps:
            f.rect(X + 4, y0, w - 8, w - 8, at=0, c=cols[reps.index(ch) % 3], sw=3, rx=10, f=cols[reps.index(ch) % 3], fo=0.3, dl=i * 60)
        f.text(X + w / 2, y0 + w / 2 + 8, ch, z=40, at="q", c="ink", b=700)
    cap = " · ".join(f"{ch} {word.count(ch)}개" for ch in reps)
    f.text(330, y0 + w + 70, cap, z=30, at=0, c="ink")
    f.text(330, y0 - 40, f"{n}개를 한 줄로", z=28, at="q", c="soft")
    return f.out()

def path_seq(m, n, seed):
    R = rng(seed)
    seq = ["R"] * m + ["U"] * n
    R.shuffle(seq)
    return seq

def grid_fig(m, n, via=None, seed=1):
    f = Fig()
    cell = min(500 / m, 440 / n, 110)
    x0, y0 = 330 - m * cell / 2, 320 - n * cell / 2
    f.grid(x0, y0, cell, cell, m, n, at="q", c="ink", sw=3)
    P = lambda i, j: (x0 + i * cell, y0 + (n - j) * cell)
    A, B = P(0, 0), P(m, n)
    f.dot(*A, r=10, f="ink", at="q"); f.text(A[0] - 18, A[1] + 34, "A", z=30, at="q", a="e")
    f.dot(*B, r=10, f="ink", at="q"); f.text(B[0] + 18, B[1] - 10, "B", z=30, at="q", a="s")
    if via:
        pi, pj = via
        Q = P(pi, pj)
        f.dot(*Q, r=11, f="coral", at="q"); f.text(Q[0] + 16, Q[1] - 12, "P", z=30, at="q", c="coral", a="s")
        seq = path_seq(pi, pj, seed) + path_seq(m - pi, n - pj, seed + 7)
    else:
        seq = path_seq(m, n, seed)
    pts, i, j = [A], 0, 0
    for s in seq:
        i, j = (i + 1, j) if s == "R" else (i, j + 1)
        pts.append(P(i, j))
    f.poly(pts, at=1, c="gold", w=8, z=False, dr=True)
    f.text(330, y0 + n * cell + 70, f"→ {m}번 · ↑ {n}번", z=30, at=0, c="coral")
    return f.out()

def seats_fig(n, mode="plain", r=None):
    """원탁 — mode: plain · pair(A, B 묶음) · opp(마주 보기) · alt(번갈아)"""
    f = Fig()
    cx, cy, R0, rs = 330, 320, 205, 40 if n <= 6 else 34
    k = r or n
    f.circ(cx, cy, R0 - 70, at="q", c="soft", sw=3, f="soft", fo=0.12)
    pos = [(cx + R0 * _cos(-PI / 2 + 2 * PI * i / k), cy + R0 * _sin(-PI / 2 + 2 * PI * i / k)) for i in range(k)]
    if mode == "pair":
        f.line(*pos[0], *pos[1], at=1, c="gold", w=rs * 2 + 14, o=0.35)
    for i, (X, Y) in enumerate(pos):
        col = "ink"
        if mode == "alt":
            col = "teal" if i % 2 == 0 else "coral"
        f.circ(X, Y, rs, at="q", c=col, sw=3, f=col if mode == "alt" else None, fo=0.18 if mode == "alt" else None)
        if mode != "alt" or i == 0:
            lab = LET[i] if mode != "alt" else "남"
            f.text(X, Y + 11, lab, z=30, at="q" if i else "q", c="ink", b=700)
    f.circ(*pos[0], rs + 9, at=0, c="gold", sw=5)
    f.text(cx, cy + 10, "기준 고정", z=28, at=0, c="soft")
    if mode == "opp":
        X, Y = pos[k // 2]
        f.line(pos[0][0], pos[0][1] + rs, X, Y - rs, at=1, c="coral", w=3, d=True)
    return f.out()

def stars_fig(r, n, dist, names):
    f = Fig()
    T = r + n - 1
    w = min(70, 600 / T)
    x0, y0 = 330 - T * w / 2, 300
    k = 0
    gi = 0
    xs_group = []
    start = x0
    for g, cnt in enumerate(dist):
        gx0 = x0 + k * w
        for _ in range(cnt):
            X = x0 + k * w + w / 2
            f.circ(X, y0, w * 0.32, at="q", c="ink", sw=3, f="gold", fo=0.6)
            k += 1
        gx1 = x0 + k * w
        xs_group.append((gx0, gx1))
        if g < n - 1:
            X = x0 + k * w + w / 2
            f.line(X, y0 - w * 0.75, X, y0 + w * 0.75, at=0, c="coral", w=7, dl=g * 200)
            k += 1
    for g, (a, b) in enumerate(xs_group):
        nm = names[g]
        lab = f"{nm} = {dist[g]}" if re.fullmatch(r"[a-z]( − 1)?", nm) else f"{nm} {dist[g]}개"
        f.text((a + b) / 2 if b > a else a, y0 + w + 34, lab, z=24, at=1, c="ink", dl=g * 150)
    f.text(330, y0 - 120, f"○ {r}개 · 칸막이 {n - 1}개", z=30, at=0, c="soft")
    return f.out()

def pascal_fig(n, r):
    f = Fig()
    rows = n + 1
    dy = min(78, 560 / rows)
    sp_ = min(78, 600 / (n + 1))
    z = int(min(30, sp_ * 0.42))
    y0 = 330 - (rows - 1) * dy / 2
    for i in range(rows):
        Y = y0 + i * dy
        for j in range(i + 1):
            X = 330 + (j - i / 2) * sp_
            hi = i == n
            f.text(X, Y + z * 0.35, str(C(i, j)), z=z, at="q" if not hi else 0, c="ink" if not hi else "coral", b=700 if hi else 500)
    X = 330 + (r - n / 2) * sp_
    f.circ(X, y0 + n * dy, z * 0.95, at=2, c="gold", sw=5)
    return f.out()

# ══════════ ① 경우의 수 ══════════
WORDS = ["banana", "apple", "level", "letter", "coffee", "school", "tomato", "pepper", "papaya", "bubble",
         "attack", "eleven", "seesaw", "sheep", "carrot", "puppy", "jelly", "happy", "access", "cookie", "google", "kitten"]

def set_a():
    S = Set("a", "경우의 수 — 세는 원리", "경우의 수",
            {1: "중복순열", 2: "같은 것이 있는 순열", 3: "원순열", 4: "중복조합", 5: "이항정리"},
            pp=8,
            tips={1: "자리(또는 대상)마다 고를 수 있는 가짓수를 곱해요 — _{n}Π_{r} = n^{r}",
                  2: "n개 중 같은 것이 p개, q개 → {n!/p! × q!} — 최단 경로는 →와 ↑의 나열",
                  3: "돌려서 같은 것 n가지를 하나로 — {n!/n} = (n − 1)!",
                  4: "같은 것 r개를 n칸에 — ○ r개와 칸막이 (n − 1)개의 나열 _{n}H_{r} = _{n + r − 1}C_{r}",
                  5: "일반항 _{n}C_{r} a^{n − r} b^{r}에서 원하는 차수가 되는 r을 찾아요"},
            note="공식보다 ‘무엇이 무엇을 고르는가’를 먼저 말하게 해 주세요. 공이 상자를 고르면 (상자 수)^{공 수}, 같은 사탕을 나누면 ○와 칸막이를 늘어놓는 문제가 돼요.")
    R = rng(2301)

    # 1단계 — 중복순열
    def g1():
        form = S.count(1) % 5
        if form == 0:
            m = R.randint(3, 6); r = R.randint(2, 4)
            if m ** r > 1300:
                return
            v = m ** r
            ds = ", ".join(str(i) for i in range(1, m + 1))
            nm = {2: "두", 3: "세", 4: "네"}[r]
            q = f"숫자 {ds} 중에서 중복을 허용하여 만들 수 있는 {nm} 자리 자연수의 개수를 구하세요."
            heads = ["천", "백", "십", "일"][-r:]
            lines = [L(f"자리마다 {m}가지씩", memo="중복 허용"), L(f"_{{{m}}}Π_{{{r}}} = {m}^{{{r}}} = {v}")]
            fig = slots_fig([m] * r, heads, res=v)
            key = f"0|{m}|{r}"
        elif form == 1:
            m = R.randint(3, 6); r = R.randint(2, 4)
            v = (m - 1) * m ** (r - 1)
            if v > 1300:
                return
            ds = ", ".join(str(i) for i in range(0, m))
            nm = {2: "두", 3: "세", 4: "네"}[r]
            q = f"숫자 {ds} 중에서 중복을 허용하여 만들 수 있는 {nm} 자리 자연수의 개수를 구하세요."
            heads = ["천", "백", "십", "일"][-r:]
            lines = [L(f"맨 앞자리는 0을 빼고 {m - 1}가지", memo="0은 맨 앞에 못 와요"), L(f"{m - 1} × {m}^{{{r - 1}}} = {v}" if r > 2 else f"{m - 1} × {m} = {v}")]
            fig = slots_fig([m - 1] + [m] * (r - 1), heads, res=v)
            key = f"1|{m}|{r}"
        elif form == 2:
            nb = R.randint(3, 5); k = R.randint(2, 4)
            v = k ** nb
            if v > 1100:
                return
            q = f"서로 다른 공 {nb}개를 서로 다른 상자 {k}개에 넣는 방법의 수를 구하세요. (빈 상자가 있어도 돼요.)"
            lines = [L(f"공 하나마다 상자 {k}가지", memo="공이 상자를 고른다"), L(f"_{{{k}}}Π_{{{nb}}} = {k}^{{{nb}}} = {v}")]
            fig = slots_fig([k] * nb, [f"공{i + 1}" for i in range(nb)], cap="공마다 들어갈 상자를 고른다", res=v)
            key = f"2|{nb}|{k}"
        elif form == 3:
            np_ = R.randint(3, 6); k = R.randint(2, 3)
            v = k ** np_
            if v > 800:
                return
            what = {2: "찬성, 반대", 3: "찬성, 반대, 기권"}[k]
            q = f"{np_}명이 각자 {what} 중 하나에 투표하는 방법의 수를 구하세요. (누가 무엇에 투표했는지 구별해요.)"
            lines = [L(f"한 사람마다 {k}가지", memo="사람이 고른다"), L(f"_{{{k}}}Π_{{{np_}}} = {k}^{{{np_}}} = {v}")]
            fig = slots_fig([k] * np_, [LET[i] for i in range(np_)], res=v) if np_ <= 5 else None
            key = f"3|{np_}|{k}"
        else:
            m = R.randint(4, 7); r = R.randint(2, 3)
            ev = m // 2
            v = m ** (r - 1) * ev
            ds = ", ".join(str(i) for i in range(1, m + 1))
            nm = {2: "두", 3: "세"}[r]
            q = f"숫자 {ds} 중에서 중복을 허용하여 만들 수 있는 {nm} 자리 짝수의 개수를 구하세요."
            heads = ["백", "십", "일"][-r:]
            evs = ", ".join(str(i) for i in range(2, m + 1, 2))
            lines = [L(f"일의 자리는 짝수 {evs} → {ev}가지", memo="짝수는 일의 자리가 결정"), L(f"{m}^{{{r - 1}}} × {ev} = {v}" if r > 2 else f"{m} × {ev} = {v}")]
            fig = slots_fig([m] * (r - 1) + [ev], heads, res=v)
            key = f"4|{m}|{r}"
        S.add(1, q, str(v), "고를 수 있는 가짓수를 자리마다 곱해요", lines, fig, key=key)
    fill(S, 1, 20, g1)

    # 2단계 — 같은 것이 있는 순열
    def g2():
        form = S.count(2) % 4
        if form in (0, 1):
            w = R.choice(WORDS)
            reps = [ch for ch in dict.fromkeys(w) if w.count(ch) > 1]
            if not reps:
                return
            n = len(w)
            den = " × ".join(f"{w.count(ch)}!" for ch in reps)
            dv = 1
            for ch in reps:
                dv *= F(w.count(ch))
            v = F(n) // dv
            q = f"{w}의 {n}개 문자를 모두 한 줄로 나열하는 방법의 수를 구하세요."
            grp = ", ".join(f"{ch} {w.count(ch)}개" for ch in reps)
            lines = [L(f"{n}개 중 같은 것 {grp}", memo="같은 것끼리는 바꿔도 같아요"), L(f"{{{n}!/{den}}} = {{{F(n)}/{dv}}} = {v}")]
            S.add(2, q, str(v), "{n!/p! × q!} — 같은 것끼리 바꾼 만큼 나눠요", lines, word_fig(w), key=w)
        elif form == 2:
            m, n = R.randint(2, 6), R.randint(2, 5)
            v = C(m + n, m)
            q = f"그림과 같은 모양의 길에서 A 지점에서 B 지점까지 최단 거리로 가는 방법의 수를 구하세요. (가로 {m}칸, 세로 {n}칸)"
            lines = [L(f"→ {m}번, ↑ {n}번을 한 줄로 나열", memo="최단 경로 = 같은 것이 있는 순열"), L(f"{{{m + n}!/{m}! × {n}!}} = {v}")]
            S.add(2, q, str(v), "→ m번과 ↑ n번의 나열", lines, grid_fig(m, n, seed=m * 10 + n), key=f"g|{m}|{n}", qfig=True)
        else:
            m, n = R.randint(3, 6), R.randint(2, 5)
            pi, pj = R.randint(1, m - 1), R.randint(1, n - 1)
            v1, v2 = C(pi + pj, pi), C(m - pi + n - pj, m - pi)
            v = v1 * v2
            q = f"그림과 같은 모양의 길에서 A 지점에서 P 지점을 거쳐 B 지점까지 최단 거리로 가는 방법의 수를 구하세요. (가로 {m}칸, 세로 {n}칸, P는 A에서 → {pi}칸, ↑ {pj}칸)"
            lines = [L(f"{{{pi + pj}!/{pi}! × {pj}!}} = {v1}", pre="A → P"), L(f"{{{m - pi + n - pj}!/{m - pi}! × {n - pj}!}} = {v2}", pre="P → B"),
                     L(f"{v1} × {v2} = {v}", memo="거쳐 가면 곱하기")]
            S.add(2, q, str(v), "A → P, P → B로 나누어 곱해요", lines, grid_fig(m, n, via=(pi, pj), seed=pi * 7 + pj), key=f"p|{m}|{n}|{pi}|{pj}", qfig=True)
    fill(S, 2, 20, g2)

    # 3단계 — 원순열
    def g3():
        form = S.count(3) % 4
        if form == 0:
            n = R.randint(4, 8)
            v = F(n - 1)
            q = f"{n}명이 원탁에 둘러앉는 방법의 수를 구하세요."
            lines = [L(f"한 명을 기준으로 고정", memo="돌려서 같은 것은 하나"), L(f"{{{n}!/{n}}} = ({n} − 1)! = {v}")]
            fig = seats_fig(n)
            key = f"0|{n}"
        elif form == 1:
            n = R.randint(4, 8)
            v = F(n - 2) * 2
            q = f"A, B를 포함한 {n}명이 원탁에 둘러앉을 때, A와 B가 이웃하여 앉는 방법의 수를 구하세요."
            lines = [L(f"A, B를 한 묶음 → {n - 1}개의 원순열", memo="묶어서 하나로"), L(f"({n - 1} − 1)! × 2! = {F(n - 2)} × 2 = {v}", memo="묶음 안에서 자리 바꾸기 2!")]
            fig = seats_fig(n, "pair")
            key = f"1|{n}"
        elif form == 2:
            n = R.randint(5, 8); r = R.randint(3, min(5, n - 1))
            v = Pm(n, r) // r
            if v > 2000:
                return
            q = f"{n}명 중에서 {r}명을 뽑아 원탁에 둘러앉히는 방법의 수를 구하세요."
            lines = [L(f"_{{{n}}}P_{{{r}}} = {Pm(n, r)}", memo="뽑아서 한 줄로"), L(f"_{{{n}}}P_{{{r}}} ÷ {r} = {Pm(n, r)} ÷ {r} = {v}", memo="돌려서 같은 것 " + str(r) + "가지")]
            fig = seats_fig(n, r=r)
            key = f"2|{n}|{r}"
        else:
            if R.random() < 0.5:
                n = R.choice([4, 6, 8])
                v = F(n - 2)
                q = f"A, B를 포함한 {n}명이 일정한 간격으로 원탁에 둘러앉을 때, A와 B가 마주 보고 앉는 방법의 수를 구하세요."
                lines = [L("A를 고정하면 B의 자리는 정해져요"), L(f"나머지 {n - 2}명 → ({n} − 2)! = {v}")]
                fig = seats_fig(n, "opp")
                key = f"3|{n}"
            else:
                k = R.randint(2, 4)
                v = F(k - 1) * F(k)
                q = f"남학생 {k}명과 여학생 {k}명이 원탁에 번갈아 둘러앉는 방법의 수를 구하세요."
                lines = [L(f"남학생의 원순열 ({k} − 1)! = {F(k - 1)}"), L(f"여학생은 사이사이 {k}자리에 {k}! = {F(k)}"), L(f"{F(k - 1)} × {F(k)} = {v}")]
                fig = seats_fig(2 * k, "alt")
                key = f"4|{k}"
        S.add(3, q, str(v), "한 자리를 고정해 돌려서 같은 것을 하나로", lines, fig, key=key)
    fill(S, 3, 20, g3)

    # 4단계 — 중복조합
    def g4():
        form = S.count(4) % 4
        if form == 0:
            n = R.randint(2, 4); r = R.randint(3, 7)
            v = C(n + r - 1, r)
            who = ["A", "B", "C", "D"][:n]
            q = f"같은 사탕 {r}개를 {n}명에게 남김없이 나누어 주는 방법의 수를 구하세요. (한 개도 못 받는 사람이 있어도 돼요.)"
            dist = [r // n + (1 if i < r % n else 0) for i in range(n)]
            names = who
        elif form == 1:
            n = R.choice([3, 3, 4]); r = R.randint(3, 7)
            v = C(n + r - 1, r)
            vs = ["x", "y", "z", "w"][:n]
            q = f"방정식 {' + '.join(vs)} = {r}을 만족시키는 음이 아닌 정수 {', '.join(vs)}의 순서쌍의 개수를 구하세요."
            q = q.replace(f"= {r}을", f"= {J(str(r), '을', '를')}")
            dist = [r // n + (1 if i < r % n else 0) for i in range(n)]
            dist = dist[::-1]
            names = vs
        elif form == 2:
            n = 3; r = R.randint(5, 10)
            v = C(n + r - 3 - 1, r - 3)
            q = f"방정식 x + y + z = {J(str(r), '을', '를')} 만족시키는 자연수 x, y, z의 순서쌍의 개수를 구하세요."
            lines = [L(f"x, y, z에 1씩 먼저 주면 나머지 {r - 3}", memo="자연수 → 1씩 미리 나누기"),
                     L(f"_{{3}}H_{{{r - 3}}} = _{{{r - 1}}}C_{{{r - 3}}} = {v}")]
            rr = r - 3
            dist = [rr // 3 + (1 if i < rr % 3 else 0) for i in range(3)]
            S.add(4, q, str(v), "○ r개와 칸막이 (n − 1)개의 나열", lines, stars_fig(rr, 3, dist, ["x − 1", "y − 1", "z − 1"]) if rr > 0 else None, key=f"2|{r}")
            return
        else:
            n = R.randint(3, 5); r = R.randint(2, 6)
            v = C(n + r - 1, r)
            kinds = {3: "사과, 배, 감", 4: "사과, 배, 감, 귤", 5: "사과, 배, 감, 귤, 키위"}[n]
            q = f"{kinds} {n}종류의 과일 중에서 중복을 허용하여 {r}개를 고르는 방법의 수를 구하세요. (같은 종류의 과일은 구별하지 않아요.)"
            dist = [r // n + (1 if i < r % n else 0) for i in range(n)]
            names = kinds.split(", ")
        if v > 400:
            return
        lines = [L(f"○ {r}개와 칸막이 {n - 1}개의 나열", memo="같은 것을 칸에 나누기"),
                 L(f"_{{{n}}}H_{{{r}}} = _{{{n + r - 1}}}C_{{{r}}} = {v}")]
        S.add(4, q, str(v), "○ r개와 칸막이 (n − 1)개의 나열", lines, stars_fig(r, n, dist, names), key=f"{form}|{n}|{r}")
    fill(S, 4, 20, g4)

    # 5단계 — 이항정리
    def g5():
        form = S.count(5) % 4
        if form == 0:
            a = R.choice([1, 2, 3, -1, -2, -3]); n = R.randint(4, 7); k = R.randint(1, n - 1)
            r = n - k
            v = C(n, r) * a ** r
            q = f"(x {'+' if a > 0 else '−'} {abs(a)})^{{{n}}}의 전개식에서 x^{{{k}}}의 계수를 구하세요." if k > 1 else f"(x {'+' if a > 0 else '−'} {abs(a)})^{{{n}}}의 전개식에서 x의 계수를 구하세요."
            lines = [L(f"일반항 _{{{n}}}C_{{r}} x^{{{n} − r}}" + (f" × {NP(a)}^{{r}}" if a != 1 else "")), L(f"{n} − r = {k} → r = {r}", memo=J(f"x^{{{k}}}" if k > 1 else "x", "이", "가") + " 되는 r"),
                     L(f"_{{{n}}}C_{{{r}}} × {NP(a)}^{{{r}}} = {C(n, r)} × {NP(a ** r)} = {N(v)}" if a != 1 else f"_{{{n}}}C_{{{r}}} = {N(v)}")]
            fn, fr = n, r
        elif form == 1:
            a = R.choice([2, 3]); b = R.choice([1, -1, 2, -2]); n = R.randint(3, 6); k = R.randint(1, n - 1)
            r = n - k
            v = C(n, r) * a ** k * b ** r
            bs = f"{'+' if b > 0 else '−'} {abs(b)}"
            xs = f"x^{{{k}}}" if k > 1 else "x"
            q = f"({a}x {bs})^{{{n}}}의 전개식에서 {xs}의 계수를 구하세요."
            lines = [L(f"일반항 _{{{n}}}C_{{r}} ({a}x)^{{{n} − r}} × {NP(b)}^{{r}}"), L(f"{n} − r = {k} → r = {r}"),
                     L(f"_{{{n}}}C_{{{r}}} × {a}^{{{k}}} × {NP(b)}^{{{r}}} = {C(n, r)} × {a ** k} × {NP(b ** r)} = {N(v)}")]
            fn, fr = n, r
        elif form == 2:
            n = R.choice([4, 6]); c = R.choice([1, 2, 3, -1, -2])
            r = n // 2
            v = C(n, r) * c ** r
            cs = f"{{{abs(c)}/x}}"
            q = f"(x {'+' if c > 0 else '−'} {cs})^{{{n}}}의 전개식에서 상수항을 구하세요."
            lines = [L(f"일반항 _{{{n}}}C_{{r}} x^{{{n} − r}} × ({N(c) if c < 0 else c}{'' if True else ''}/x)^{{r}}".replace(f"({N(c) if c < 0 else c}/x)", f"({'−' if c < 0 else ''}{{{abs(c)}/x}})")),
                     L(f"x의 지수 {n} − 2r = 0 → r = {r}"), L(f"_{{{n}}}C_{{{r}}} × {NP(c)}^{{{r}}} = {C(n, r)} × {NP(c ** r)} = {N(v)}" if c != 1 else f"_{{{n}}}C_{{{r}}} = {N(v)}")]
            fn, fr = n, r
        else:
            n = R.choice([3, 6]); c = R.choice([1, 2, -1, -2])
            r = 2 * n // 3
            v = C(n, r) * c ** r
            q = f"(x^{{2}} {'+' if c > 0 else '−'} {{{abs(c)}/x}})^{{{n}}}의 전개식에서 상수항을 구하세요."
            lines = [L(f"일반항 _{{{n}}}C_{{r}} (x^{{2}})^{{{n} − r}} × ({'−' if c < 0 else ''}{{{abs(c)}/x}})^{{r}}"),
                     L(f"x의 지수 2({n} − r) − r = 0 → r = {r}"), L(f"_{{{n}}}C_{{{r}}} × {NP(c)}^{{{r}}} = {C(n, r)} × {NP(c ** r)} = {N(v)}" if c != 1 else f"_{{{n}}}C_{{{r}}} = {N(v)}")]
            fn, fr = n, r
        if abs(v) > 3000:
            return
        S.add(5, q, N(v), "일반항에서 원하는 차수가 되는 r을 찾아요", lines, pascal_fig(fn, fr), sub={"r": fr})
    fill(S, 5, 20, g5)
    return S


# ══════════ ② 여러 가지 미분법 ══════════
def tangent_fig(e, t, m, ft, xr=None, at_tan=1, asym=(), at_pt="q"):
    fn = sp.lambdify(x, e, modules="math")
    xr = xr or (float(t) - 2.4, float(t) + 2.4)
    xr = (min(xr[0], -0.6), max(xr[1], 0.6))
    ys = []
    for i in range(121):
        X = xr[0] + (xr[1] - xr[0]) * i / 120
        try:
            Y = fn(X)
        except (ZeroDivisionError, ValueError, OverflowError):
            continue
        if isinstance(Y, complex) or not math.isfinite(Y):
            continue
        ys.append(Y)
    ft = float(ft)
    span = max(3.0, abs(float(m)) * 2.4 + 1)
    ys = [Y for Y in ys if abs(Y - ft) <= span * 2.5] + [ft, 0]
    lo, hi = min(ys), max(ys)
    pad = (hi - lo) * 0.08 + 0.4
    f = Fig()
    P = Plane(f, xr, (lo - pad, hi + pad), box=(40, 40, 620, 640), square=False)
    P.axes(grid=0)
    for kind, v in asym:
        if kind == "x" and P.xr[0] < v < P.xr[1]:
            f.line(P.X(v), P.Y(P.yr[0]), P.X(v), P.Y(P.yr[1]), at="q", c="soft", w=2, d=True)
        elif kind == "y" and P.yr[0] < v < P.yr[1]:
            f.line(P.X(P.xr[0]), P.Y(v), P.X(P.xr[1]), P.Y(v), at="q", c="soft", w=2, d=True)

    def safe(X):
        try:
            Y = fn(X)
        except (ZeroDivisionError, ValueError, OverflowError):
            return None
        return Y if isinstance(Y, float) or isinstance(Y, int) else None
    P.curve(safe, n=160, at="q", c="sky", w=4.5)
    P.pt(float(t), ft, at=at_pt, f="coral", r=10)
    P.lineq(float(m), ft - float(m) * float(t), at=at_tan, c="coral", w=4)
    return f.out()

def ang(v):
    """π의 유리수배 → 글자: 0 · π · {π/6} · {2π/3} · −{π/2}"""
    v = sp.nsimplify(v / sp.pi)
    if v == 0:
        return "0"
    p, q = sp.fraction(v)
    p, q = int(p), int(q)
    sgn = MI if p < 0 else ""
    p = abs(p)
    num = "π" if p == 1 else f"{p}π"
    return sgn + (num if q == 1 else f"{{{num}/{q}}}")

def chain_fig(inner, outer, din, dout, final):
    f = Fig()
    xs = [110, 330, 550]
    for X, lab in zip(xs, ["x", "u", "y"]):
        f.circ(X, 300, 52, at="q", c="ink", sw=3.5)
        f.text(X, 314, lab, z=40, at="q", c="ink", b=700)
    for i, (top, bot) in enumerate([(inner, din), (outer, dout)]):
        x1, x2 = xs[i] + 58, xs[i + 1] - 58
        f.line(x1, 300, x2, 300, at="q", c="ink", w=3.5, ar=1)
        f.text((x1 + x2) / 2, 250, top, z=26, at="q", c="soft")
        f.text((x1 + x2) / 2, 380, bot, z=28, at=0, c="coral", dl=i * 300)
    f.text(330, 500, "{dy/dx} = {dy/du} × {du/dx}", z=32, at=1, c="ink", b=700)
    f.text(330, 580, final, z=28, at=1, c="soft", dl=300)
    return f.out()

def set_b():
    S = Set("b", "여러 가지 미분법 — 몫 · 합성 · 초월함수", "여러 가지 미분법",
            {1: "몫의 미분법", 2: "합성함수의 미분법", 3: "지수 · 로그함수의 미분", 4: "삼각함수의 미분", 5: "음함수 · 매개변수의 미분"},
            pp=6,
            tips={1: "{f/g}' = {f'g − fg'/g^{2}} — 분모는 제곱, 분자는 ‘위 미분 × 아래 − 위 × 아래 미분’",
                  2: "y = f(u), u = g(x) → {dy/dx} = {dy/du} × {du/dx} — 겉미분 × 속미분",
                  3: "(e^{x})' = e^{x} · (ln x)' = {1/x} — 속에 식이 있으면 속미분을 곱해요",
                  4: "(sin x)' = cos x · (cos x)' = −sin x · (tan x)' = sec^{2} x",
                  5: "음함수: y를 x의 함수로 보고 양변을 미분 · 매개변수: {dy/dx} = {dy/dt} ÷ {dx/dt}"},
            note="합성함수의 미분은 ‘x가 u를 바꾸고, u가 y를 바꾼다’는 두 단계 변화율의 곱이에요. 그림의 화살표 두 개에 변화율을 하나씩 적게 해 주세요.")
    R = rng(2302)

    def lx(d):
        return "x" if d == 0 else (f"x + {d}" if d > 0 else f"x − {-d}")

    # 1단계 — 몫의 미분법
    def g1():
        form = S.count(1) % 2
        d = R.choice([-3, -2, -1, 1, 2, 3])
        t = R.choice([-2, -1, 0, 1, 2, 3])
        if t + d == 0:
            return
        if form == 0:
            a = R.choice([1, 2, 3, -1]); b = R.randint(-4, 4)
            if a * d - b == 0:
                return
            e = (a * x + b) / (x + d)
            num_s = lin(a, b)
            ns = num_s if num_s == "x" else f"({num_s})"
            lines = [L(f"f'(x) = {{{a}({lx(d)}) − {ns} × 1/({lx(d)})^{{2}}}}" if a != 1 else f"f'(x) = {{({lx(d)}) − {ns}/({lx(d)})^{{2}}}}", memo="위 미분 × 아래 − 위 × 아래 미분"),
                     L(f"= {{{N(a * d - b)}/({lx(d)})^{{2}}}}"),
                     L(f"f'({N(t)}) = {{{N(a * d - b)}/{NP(t + d)}^{{2}}}} = {N(Fr(a * d - b, (t + d) ** 2))}")]
            qs = f"{{{num_s}/{lx(d)}}}"
            asym = [("x", -d), ("y", a)]
        else:
            if t == 0:
                return
            e = x ** 2 / (x + d)
            lines = [L(f"f'(x) = {{2x({lx(d)}) − x^{{2}}/({lx(d)})^{{2}}}}", memo="위 미분 × 아래 − 위 × 아래 미분"),
                     L(f"= {{x^{{2}} {'+' if d > 0 else '−'} {abs(2 * d)}x/({lx(d)})^{{2}}}}"),
                     L(f"f'({N(t)}) = {{{NP(t)}^{{2}} {'+' if d > 0 else '−'} {abs(2 * d)} × {NP(t)}/{NP(t + d)}^{{2}}}} = {N(Fr(t * t + 2 * d * t, (t + d) ** 2))}")]
            qs = f"{{x^{{2}}/{lx(d)}}}"
            asym = [("x", -d)]
        dv = sp.diff(e, x).subs(x, t)
        v = Fr(int(sp.fraction(dv)[0]), int(sp.fraction(dv)[1]))
        assert sp.simplify(sp.diff(e, x) - (sp.together(sp.diff(e, x)))) == 0
        ft = e.subs(x, t)
        q = f"함수 f(x) = {qs}에 대하여 f'({N(t)})의 값을 구하세요."
        fig = tangent_fig(e, t, float(dv), float(ft), asym=asym, at_tan=2)
        S.add(1, q, N(v), "{f/g}' = {f'g − fg'/g^{2}}", lines, fig, ap=plain(N(v)))
    fill(S, 1, 20, g1)

    # 2단계 — 합성함수의 미분법
    def g2():
        form = S.count(2) % 3
        if form == 0:
            a = R.choice([2, 3, -1, -2]); b = R.randint(-3, 3); n = R.randint(2, 5); t = R.randint(-1, 2)
            inner = lin(a, b)
            e = (a * x + b) ** n
            u = a * t + b
            v = n * u ** (n - 1) * a
            if abs(v) > 2000 or u == 0:
                return
            q = f"함수 f(x) = ({inner})^{{{n}}}에 대하여 f'({N(t)})의 값을 구하세요."
            pw = f"^{{{n - 1}}}" if n > 2 else ""
            lines = [L(f"f'(x) = {n}({inner}){pw} × {NP(a)}", memo="겉미분 × 속미분"),
                     L(f"f'({N(t)}) = {n} × {NP(u)}{pw} × {NP(a)} = {N(v)}")]
            fig = chain_fig(f"u = {inner}", f"y = u^{{{n}}}", f"{{du/dx}} = {N(a)}", f"{{dy/du}} = {n}u^{{{n - 1}}}" if n > 2 else f"{{dy/du}} = 2u", f"f'(x) = {n}({inner}){pw} × {NP(a)}")
        elif form == 1:
            c = R.choice([-3, -2, -1, 1, 2, 3]); n = R.randint(2, 4); t = R.choice([-2, -1, 1, 2])
            inner = f"x^{{2}} {'+' if c > 0 else '−'} {abs(c)}"
            e = (x ** 2 + c) ** n
            u = t * t + c
            v = n * u ** (n - 1) * 2 * t
            if abs(v) > 2000 or u == 0:
                return
            q = f"함수 f(x) = ({inner})^{{{n}}}에 대하여 f'({N(t)})의 값을 구하세요."
            pw = f"^{{{n - 1}}}" if n > 2 else ""
            lines = [L(f"f'(x) = {n}({inner}){pw} × 2x", memo="겉미분 × 속미분"),
                     L(f"f'({N(t)}) = {n} × {NP(u)}{pw} × 2 × {NP(t)} = {N(v)}")]
            fig = chain_fig(f"u = {inner}", f"y = u^{{{n}}}", "{du/dx} = 2x", f"{{dy/du}} = {n}u^{{{n - 1}}}" if n > 2 else "{dy/du} = 2u", f"f'(x) = {n}({inner}){pw} × 2x")
        else:
            t = R.randint(1, 6); s_ = R.randint(t + 1, t + 6)
            c = s_ * s_ - t * t
            if c > 60:
                return
            e = sp.sqrt(x ** 2 + c)
            v = Fr(t, s_)
            q = f"함수 f(x) = √{{x^{{2}} + {c}}}에 대하여 f'({t})의 값을 구하세요."
            lines = [L(f"f'(x) = {{1/2√{{x^{{2}} + {c}}}}} × 2x = {{x/√{{x^{{2}} + {c}}}}}", memo="(√{u})' = {u'/2√{u}}"),
                     L(f"f'({t}) = {{{t}/√{{{t * t + c}}}}} = {N(v)}")]
            fig = chain_fig(f"u = x^{{2}} + {c}", "y = √{u}", "{du/dx} = 2x", "{dy/du} = {1/2√{u}}", f"f'(x) = {{x/√{{x^{{2}} + {c}}}}}")
        dv = sp.nsimplify(sp.diff(e, x).subs(x, t))
        assert dv == sp.nsimplify(v), (q, dv, v)
        S.add(2, q, N(v), "겉미분 × 속미분", lines, fig, ap=plain(N(v)))
    fill(S, 2, 20, g2)

    # 3단계 — 지수 · 로그함수의 미분
    def g3():
        form = S.count(3) % 4
        if form == 0:
            a = R.choice([2, 3, -1, -2, 4]); t = R.choice([-2, -1, 1, 2, 3])
            b = -a * t
            e = sp.exp(a * x + b)
            ex = lin(a, b)
            v = Fr(a)
            q = f"함수 f(x) = e^{{{ex}}}에 대하여 f'({N(t)})의 값을 구하세요."
            lines = [L(f"f'(x) = e^{{{ex}}} × {NP(a)}", memo="(e^{u})' = e^{u} × u'"), L(f"f'({N(t)}) = e^{{0}} × {NP(a)} = {N(v)}")]
            tt = t
        elif form == 1:
            k = R.choice([1, 2, 3, -1]); c = R.choice([-3, -2, -1, 1, 2, 3])
            e = (x + c) * sp.exp(k * x)
            v = Fr(1 + k * c)
            ks = "x" if k == 1 else ("−x" if k == -1 else f"{k}x")
            q = f"함수 f(x) = ({lx(c)})e^{{{ks}}}에 대하여 f'(0)의 값을 구하세요."
            lines = [L(f"f'(x) = e^{{{ks}}} + ({lx(c)}) × {'' if k == 1 else NP(k)}e^{{{ks}}}".replace("×  ", "× "), memo="곱의 미분"),
                     L(f"f'(0) = 1 + {NP(c)} × {NP(k)} = {N(v)}", memo="e^{0} = 1")]
            tt = 0
        elif form == 2:
            a = R.choice([1, 2, 3, 4]); b = R.randint(-3, 5); t = R.randint(0, 3)
            if a * t + b <= 0:
                return
            e = sp.log(a * x + b)
            v = Fr(a, a * t + b)
            inner = lin(a, b)
            lnq = "ln x" if inner == "x" else f"ln ({inner})"
            q = f"함수 f(x) = {lnq}에 대하여 f'({t})의 값을 구하세요."
            lines = [L(f"f'(x) = {{{a}/{inner}}}", memo="(ln u)' = {u'/u}"), L(f"f'({t}) = {{{a}/{a * t + b}}}" + ("" if Fr(a, a * t + b).denominator == a * t + b and a % (a * t + b) != 0 else f" = {N(v)}"))]
            tt = t
        else:
            c = R.randint(1, 8); t = R.choice([-2, -1, 1, 2, 3])
            e = sp.log(x ** 2 + c)
            v = Fr(2 * t, t * t + c)
            q = f"함수 f(x) = ln (x^{{2}} + {c})에 대하여 f'({N(t)})의 값을 구하세요."
            lines = [L(f"f'(x) = {{2x/x^{{2}} + {c}}}", memo="(ln u)' = {u'/u}"), L(f"f'({N(t)}) = {{2 × {NP(t)}/{t * t + c}}} = {N(v)}")]
            tt = t
        dv = sp.nsimplify(sp.simplify(sp.diff(e, x).subs(x, tt)))
        assert dv == sp.Rational(v.numerator, v.denominator), (q, dv, v)
        ft = float(e.subs(x, tt))
        fig = tangent_fig(e, tt, float(v), ft, at_tan=1)
        S.add(3, q, N(v), "바깥 함수의 미분 × 속미분", lines, fig, ap=plain(N(v)))
    fill(S, 3, 20, g3)

    # 4단계 — 삼각함수의 미분
    pi = sp.pi
    TRIG = []
    for k in (2, 3, 4, 5):
        TRIG.append((f"sin {k}x", sp.sin(k * x), f"{k} cos {k}x", 0, lambda t, k=k: f"{k} cos 0"))
        TRIG.append((f"sin {k}x", sp.sin(k * x), f"{k} cos {k}x", pi / k, lambda t, k=k: f"{k} cos π"))
        TRIG.append((f"cos {k}x", sp.cos(k * x), f"−{k} sin {k}x", pi / (2 * k), lambda t, k=k: f"−{k} sin {{π/2}}"))
    TRIG += [
        ("x sin x", x * sp.sin(x), "sin x + x cos x", pi / 2, lambda t: "sin {π/2} + {π/2} cos {π/2}"),
        ("x sin x", x * sp.sin(x), "sin x + x cos x", 3 * pi / 2, lambda t: "sin {3π/2} + {3π/2} cos {3π/2}"),
        ("x cos x", x * sp.cos(x), "cos x − x sin x", 0, lambda t: "cos 0 − 0 × sin 0"),
        ("x cos x", x * sp.cos(x), "cos x − x sin x", pi, lambda t: "cos π − π sin π"),
        ("sin x cos x", sp.sin(x) * sp.cos(x), "cos^{2} x − sin^{2} x", 0, lambda t: "cos^{2} 0 − sin^{2} 0"),
        ("sin x cos x", sp.sin(x) * sp.cos(x), "cos^{2} x − sin^{2} x", pi / 2, lambda t: "cos^{2} {π/2} − sin^{2} {π/2}"),
        ("sin^{2} x", sp.sin(x) ** 2, "2 sin x cos x", pi / 4, lambda t: "2 sin {π/4} cos {π/4}"),
        ("cos^{2} x", sp.cos(x) ** 2, "−2 cos x sin x", pi / 4, lambda t: "−2 cos {π/4} sin {π/4}"),
        ("tan x", sp.tan(x), "sec^{2} x", pi / 4, lambda t: "{1/cos^{2} {π/4}}"),
        ("tan x", sp.tan(x), "sec^{2} x", pi / 3, lambda t: "{1/cos^{2} {π/3}}"),
        ("tan x", sp.tan(x), "sec^{2} x", pi / 6, lambda t: "{1/cos^{2} {π/6}}"),
        ("e^{x} sin x", sp.exp(x) * sp.sin(x), "e^{x} sin x + e^{x} cos x", 0, lambda t: "e^{0} sin 0 + e^{0} cos 0"),
        ("e^{x} cos x", sp.exp(x) * sp.cos(x), "e^{x} cos x − e^{x} sin x", 0, lambda t: "e^{0} cos 0 − e^{0} sin 0"),
        ("sin x + cos x", sp.sin(x) + sp.cos(x), "cos x − sin x", pi, lambda t: "cos π − sin π"),
        ("sin x − cos x", sp.sin(x) - sp.cos(x), "cos x + sin x", pi / 2, lambda t: "cos {π/2} + sin {π/2}"),
    ]
    RULE = {"sin": "(sin u)' = cos u × u'", "cos": "(cos u)' = −sin u × u'"}
    order = list(range(len(TRIG)))
    R.shuffle(order)
    # 같은 꼴만 몰리지 않게: 앞의 12개 중 꼴이 다른 것부터
    def g4():
        i = order[S.count(4) % len(order)] if S.count(4) < len(order) else R.randrange(len(TRIG))
        qs, e, ds, t, sub = TRIG[i]
        dv = sp.nsimplify(sp.simplify(sp.diff(e, x).subs(x, t)))
        if not dv.is_rational:
            order.remove(i)
            return
        v = Fr(int(sp.fraction(dv)[0]), int(sp.fraction(dv)[1]))
        q = f"함수 f(x) = {qs}에 대하여 f'({ang(t)})의 값을 구하세요."
        memo = RULE.get(qs.split()[0][:3], "곱의 미분" if " x " in f" {qs} " and qs.count("x") > 1 else "기본 공식")
        if qs.startswith("tan"):
            memo = "(tan x)' = sec^{2} x = {1/cos^{2} x}"
        elif qs.endswith("^{2} x"):
            memo = "합성함수: 2 × (속) × (속)'"
        elif qs.startswith("x ") or qs.startswith("e^{x} ") or qs == "sin x cos x":
            memo = "곱의 미분"
        elif " + " in qs or " − " in qs:
            memo = "(sin x)' = cos x, (cos x)' = −sin x"
        lines = [L(f"f'(x) = {ds}", memo=memo), L(f"f'({ang(t)}) = {sub(t)} = {N(v)}")]
        fig = tangent_fig(e, t, float(dv), float(e.subs(x, t)), xr=(float(t) - 2.6, float(t) + 2.6), at_tan=1)
        S.add(4, q, N(v), "삼각함수의 도함수 + 곱 · 합성의 미분", lines, fig, ap=plain(N(v)), key=f"{qs}|{t}")
    fill(S, 4, 20, g4)

    # 5단계 — 음함수 · 매개변수
    PYTH = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13), (12, 5, 13), (0, 5, 5), (1, 1, None)]
    def g5():
        form = S.count(5) % 3
        if form == 0:
            a, b, r = R.choice(PYTH[:6])
            a *= R.choice([1, -1]); b *= R.choice([1, -1])
            r2 = a * a + b * b
            v = Fr(-a, b)
            q = f"원 x^{{2}} + y^{{2}} = {r2} 위의 점 ({N(a)}, {N(b)})에서 {{dy/dx}}의 값을 구하세요."
            lines = [L("2x + 2y{dy/dx} = 0", memo="y를 x의 함수로 보고 양변을 미분"), L("{dy/dx} = −{x/y}"),
                     L((f"−{{{N(a)}/{N(b)}}}" if a >= 0 and b > 0 else f"−{{{NP(a)}/{NP(b)}}}") + ("" if (a > 0 and b > 0 and gcd(a, b) == 1) else f" = {N(v)}"), pre=f"({N(a)}, {N(b)})")]
            f = Fig()
            rr = math.sqrt(r2)
            P = Plane(f, (-rr * 1.35, rr * 1.35), (-rr * 1.35, rr * 1.35), box=(40, 40, 620, 640))
            P.axes(grid=0)
            f.circ(P.X(0), P.Y(0), rr * P.sx, at="q", c="sky", sw=4.5)
            P.pt(a, b, at="q", f="coral", r=10, label=f"({N(a)}, {N(b)})", pos="ne" if a >= 0 else "nw", z=24, c="coral")
            if b != 0:
                P.lineq(float(v), b - float(v) * a, at=2, c="coral", w=4)
            S.add(5, q, N(v), "양변을 x에 대하여 미분해요", lines, f.out(), ap=plain(N(v)), key=f"c|{a}|{b}")
        elif form == 1:
            k = R.choice([1, -1]); a, b = R.choice([(1, 2), (2, 1), (1, 3), (3, 1), (2, 3), (3, 2), (-1, 2), (2, -1), (1, -2)])
            c = a * a + k * a * b + b * b
            den = k * a + 2 * b
            if den == 0:
                return
            v = Fr(-(2 * a + k * b), den)
            ks = "+" if k == 1 else "−"
            q = f"곡선 x^{{2}} {ks} xy + y^{{2}} = {c} 위의 점 ({N(a)}, {N(b)})에서 {{dy/dx}}의 값을 구하세요."
            lines = [L(f"2x {ks} (y + x{{dy/dx}}) + 2y{{dy/dx}} = 0", memo="xy는 곱의 미분"),
                     L(f"{{dy/dx}} = −{{2x {ks} y/{'' if k == 1 else '−'}x + 2y}}"),
                     L(f"−{{2 × {NP(a)} {ks} {NP(b)}/{'' if k == 1 else '−'}{NP(a)} + 2 × {NP(b)}}} = {N(v)}", pre=f"({N(a)}, {N(b)})")]
            # 그림: y = (−kx ± √(k²x² − 4(x² − c)))/2
            f = Fig()
            Rm = math.sqrt(4 * c / (4 - k * k)) * 1.15
            P = Plane(f, (-Rm * 1.2, Rm * 1.2), (-Rm * 1.2, Rm * 1.2), box=(40, 40, 620, 640))
            P.axes(grid=0)
            pts = []
            for i in range(241):
                th = 2 * PI * i / 240
                # 매개화: 회전된 타원 — 반지름 방향으로 풀기 r²(1 + k sinθcosθ) = c
                den_ = 1 + k * math.sin(th) * math.cos(th)
                rr = math.sqrt(c / den_)
                pts.append(P.P(rr * math.cos(th), rr * math.sin(th)))
            f.poly(pts, at="q", c="sky", w=4.5, z=True, dr=True)
            P.pt(a, b, at="q", f="coral", r=10, label=f"({N(a)}, {N(b)})", pos="ne", z=24, c="coral")
            P.lineq(float(v), b - float(v) * a, at=2, c="coral", w=4)
            S.add(5, q, N(v), "xy는 곱의 미분 — y' 를 모아서 풀어요", lines, f.out(), ap=plain(N(v)), key=f"q|{k}|{a}|{b}")
        else:
            p = R.randint(-2, 2); qq = R.randint(-3, 3); t = R.choice([-2, -1, 1, 2])
            v = Fr(3 * t * t + qq, 2 * t)
            xs = f"t^{{2}}" + (f" + {p}" if p > 0 else (f" − {-p}" if p < 0 else ""))
            ys = f"t^{{3}}" + (f" + {qq}t" if qq > 1 else (" + t" if qq == 1 else (f" − {-qq}t" if qq < -1 else (" − t" if qq == -1 else ""))))
            q = f"x = {xs}, y = {ys}일 때 t = {N(t)}에서 {{dy/dx}}의 값을 구하세요."
            dyt = f"3t^{{2}}" + (f" + {qq}" if qq > 0 else (f" − {-qq}" if qq < 0 else ""))
            lines = [L(f"{{dx/dt}} = 2t, {{dy/dt}} = {dyt}"), L(f"{{dy/dx}} = {{{dyt}/2t}}", memo="{dy/dt} ÷ {dx/dt}"),
                     L(f"{{3 × {NP(t)}^{{2}} {'+' if qq >= 0 else '−'} {abs(qq)}/2 × {NP(t)}}} = {N(v)}", pre=f"t = {N(t)}")]
            f = Fig()
            T = [-2.4 + 4.8 * i / 160 for i in range(161)]
            X = [s * s + p for s in T]; Y = [s ** 3 + qq * s for s in T]
            xr = (min(X + [0]) - 0.8, max(X + [0]) + 0.8); yr = (min(Y + [0]) - 1, max(Y + [0]) + 1)
            P = Plane(f, xr, yr, box=(40, 40, 620, 640), square=False)
            P.axes(grid=0)
            f.poly([P.P(a, b) for a, b in zip(X, Y)], at="q", c="sky", w=4.5, z=False, dr=True)
            x0, y0 = t * t + p, t ** 3 + qq * t
            P.pt(x0, y0, at="q", f="coral", r=10, label=f"t = {N(t)}", pos="ne" if t > 0 else "se", z=24, c="coral")
            P.lineq(float(v), y0 - float(v) * x0, at=2, c="coral", w=4)
            S.add(5, q, N(v), "{dy/dx} = {dy/dt} ÷ {dx/dt}", lines, f.out(), ap=plain(N(v)), key=f"p|{p}|{qq}|{t}")
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "h3", "grade": "고3", "level": "고등", "icon": "🎲", "title": "고3 · 경우의 수 · 여러 가지 미분법",
         "desc": "경우의 수 — 세는 원리 100제(칸 · 최단 경로 · 원탁 · ○와 칸막이 · 파스칼 삼각형) · 여러 가지 미분법 100제(몫 · 합성 · 지수로그 · 삼각 · 음함수 · 매개변수).",
         "thumb": ("a", 70), "sets": [set_a, set_b]}
