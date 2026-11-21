# 초등 ② — 곱셈 세로셈 · 나눗셈 세로셈 · 혼합 계산 · 약수와 배수 · 분수의 크기 · 분수의 곱셈
from math import gcd
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, fbar, ffill, ang_pt
from kit import *

def F_(n, d):
    return "{%d/%d}" % (n, d)

def FX(v):
    """분수 값 → 글자(가분수는 대분수로) — 3/2 → '1{1/2}'"""
    v = Fr(v)
    return MX(v) if v >= 0 else MI + MX(-v)

def lcm(a, b):
    return a * b // gcd(a, b)

def bat(x):
    from core import _has_batchim
    return _has_batchim(str(x))


# ══════════ 곱셈 세로셈 ══════════
def mul():
    S = Set("mul", "곱셈 세로셈 — 올림을 적으며", "곱셈 세로셈",
            {1: "(두 자리)×(한 자리)", 2: "(세 자리)×(한 자리)", 3: "(몇십)×(몇십) · (몇백)×(몇십)", 4: "(두 자리)×(두 자리)", 5: "(세 자리)×(두 자리)"},
            pp=10,
            tips={1: "일의 자리부터 곱해요. 곱이 10을 넘으면 십의 자리 위에 올림 수를 작게 써 두고, 다음 곱에 더해요",
                  2: "자리마다 곱하고 올림을 더하기 — 마지막 자리의 곱은 그대로 내려 써요",
                  3: "0을 떼고 곱한 다음, 뗀 0의 개수만큼 0을 붙여요. 30 × 40 → 3 × 4 = 12 → 1200",
                  4: "곱하는 수를 일의 자리 · 십의 자리로 나누어 두 번 곱하고 더해요. 십의 자리 곱은 한 칸 왼쪽부터",
                  5: "세 자리 수도 똑같이 — 부분곱 두 줄을 자리 맞춰 더해요"},
            note="곱셈 세로셈은 ‘자리마다 곱하고 올림을 더한다’와 ‘십의 자리 곱은 한 칸 왼쪽’ 두 가지예요. 올림 숫자를 작게 남겨 두게 하면 실수가 크게 줄어요.")
    R = rng(321)

    def put(st, a, b, plan):
        f, lines, res = col_mul(a, b)
        q = R.choice([f"{a} × {J(b, '은', '는')} 얼마인가요?", f"{a} × {eul(b)} 계산하세요."])
        return S.add(st, q, str(res), plan, lines, f.out(), key=f"{a}x{b}")

    def g1():
        a, b = R.randint(13, 98), R.randint(3, 9)
        if a % 10 * b < 10 or a % 10 == 0:
            return
        put(1, a, b, "일의 자리부터 — 올림 수는 위에 작게 써 두고 다음 곱에 더해요")
    fill(S, 1, 20, g1)

    def g2():
        a, b = R.randint(123, 987), R.randint(3, 9)
        if "0" in str(a) and S.count(2) < 14:
            return
        put(2, a, b, "세 자리도 일의 자리부터 — 자리마다 곱하고 올림을 더해요")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 4
        if k == 0:
            x, y = R.randint(2, 9), R.randint(2, 9)
            a, b, z = x * 10, y * 10, 2
        elif k == 1:
            x, y = R.randint(2, 9), R.randint(2, 9)
            a, b, z = x * 100, y * 10, 3
        elif k == 2:
            x, y = R.randint(12, 98), R.randint(2, 9)
            if x % 10 == 0:
                return
            a, b, z = x, y * 10, 1
        else:
            x, y = R.randint(12, 49), R.randint(2, 9)
            if x % 10 == 0:
                return
            a, b, z = x * 10, y * 10, 2
        res = a * b
        f = Fig()
        sa, sb = str(a), str(b)
        txt = [(c, "coral" if (c == "0" and i >= len(sa.rstrip("0"))) else "ink") for i, c in enumerate(sa)] + [(" × ", "ink")] + \
              [(c, "coral" if (c == "0" and i >= len(sb.rstrip("0"))) else "ink") for i, c in enumerate(sb)]
        x0 = 330 - sum(34 if t != " × " else 70 for t, _ in txt) / 2
        for t, c in txt:
            w = 34 if t != " × " else 70
            f.text(x0 + w / 2, 230, t.strip() or "×", z=60, c=c, b=700 if c == "coral" else 600)
            x0 += w
        core_ = int(sa.rstrip("0")) * int(sb.rstrip("0"))
        f.text(330, 380, f"{sa.rstrip('0')} × {sb.rstrip('0')} = {core_}", z=44, at=0)
        f.text(330, 520, str(core_), z=64, at=1, b=700, a="e", c="ink")
        f.text(334, 520, "0" * z, z=64, at=1, b=700, a="s", c="coral", dl=300)
        lines = [L(f"{sa.rstrip('0')} × {sb.rstrip('0')} = {core_}", memo="0을 떼고 곱해요"), L(f"뗀 0이 {z}개 → 0을 {z}개 붙여요", memo="끝의 0의 개수만큼"), L(f"{a} × {b} = {res}")]
        S.add(3, f"{a} × {J(b, '은', '는')} 얼마인가요?", str(res), "0을 떼고 곱한 뒤, 뗀 0의 개수만큼 붙여요", lines, f.out(), key=f"{a}x{b}")
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.randint(13, 98), R.randint(13, 98)
        if a % 10 == 0 or b % 10 == 0:
            return
        put(4, a, b, f"{b}를 {b % 10}와 {b // 10 * 10}으로 나누어 두 번 곱하고 더해요" if not bat(b) else f"{b}을 {b % 10}{'과' if bat(b % 10) else '와'} {b // 10 * 10}으로 나누어 두 번 곱하고 더해요")
    fill(S, 4, 20, g4)

    def g5():
        a, b = R.randint(112, 987), R.randint(13, 98)
        if b % 10 == 0:
            return
        put(5, a, b, "일의 자리 곱 · 십의 자리 곱(한 칸 왼쪽) — 두 줄을 더해요")
    fill(S, 5, 20, g5)
    return S


# ══════════ 나눗셈 세로셈 ══════════
def div():
    S = Set("div", "나눗셈 세로셈 — 몫을 한 자리씩", "나눗셈 세로셈",
            {1: "(두 자리)÷(한 자리)", 2: "나머지가 있는 (두 자리)÷(한 자리)", 3: "(세 자리)÷(한 자리)", 4: "÷ (몇십) · (두 자리)", 5: "(세 자리)÷(두 자리)"},
            pp=10,
            tips={1: "높은 자리부터 — 십의 자리를 나누고, 남은 것을 일의 자리와 함께 다시 나눠요",
                  2: "나머지는 나누는 수보다 작아야 해요. 나누는 수 × 몫 + 나머지 = 나누어지는 수로 검산",
                  3: "첫 자리가 나누는 수보다 작으면 두 자리를 함께 봐요. 내린 수가 작아 못 나누면 몫에 0",
                  4: "나누는 수를 몇십으로 어림해 몫을 정해요. 너무 크면 1 줄이고, 나머지가 나누는 수보다 크면 1 늘려요",
                  5: "몫을 한 자리씩 어림 → 곱해서 빼기 → 다음 자리 내리기를 되풀이해요"},
            note="나눗셈 세로셈은 ‘어림 → 곱하기 → 빼기 → 내리기’의 되풀이예요. 몫을 어림한 뒤 곱이 너무 크거나 나머지가 너무 크면 몫을 고치는 과정을 꼭 말로 짚어 주세요.")
    R = rng(322)

    def put(st, n, d, plan, est=False):
        f, lines, Q, Rm = long_div(n, d, est=est)
        if Rm:
            q = f"{n} ÷ {d}의 몫과 나머지를 구하세요."
            return S.add(st, q, f"몫 {Q}, 나머지 {Rm}", plan, lines, f.out(), ap=f"{Q}, {Rm}", omr="ex", key=f"{n}/{d}")
        q = R.choice([f"{n} ÷ {eul(d)} 계산하세요.", f"{n} ÷ {J(d, '은', '는')} 얼마인가요?"])
        return S.add(st, q, str(Q), plan, lines, f.out(), key=f"{n}/{d}")

    def g1():
        d = R.randint(2, 9); Q = R.randint(11, 49)
        n = d * Q
        if n > 99 or n // 10 < d:
            return
        put(1, n, d, "십의 자리부터 나누고, 남은 것은 일의 자리와 함께")
    fill(S, 1, 20, g1)

    def g2():
        d = R.randint(3, 9); Q = R.randint(11, 32); r = R.randint(1, d - 1)
        n = d * Q + r
        if n > 99 or n // 10 < d:
            return
        put(2, n, d, "나머지는 나누는 수보다 작게 — 마지막에 검산")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3)
        d = R.randint(2, 9)
        r = 0 if k % 2 == 0 else R.randint(1, d - 1)
        if k % 4 == 0:
            Q = R.choice([R.randint(101, 109), R.randint(201, 209), R.randint(301, 309), R.randint(401, 409)])
        elif k % 4 == 1:
            Q = R.randint(112, 330)
        else:
            Q = R.randint(12, 99)
        n = d * Q + r
        if n > 999 or n < 100:
            return
        if k % 4 >= 2 and n // 100 >= d:
            return
        put(3, n, d, "첫 자리가 나누는 수보다 작으면 두 자리를 함께 — 못 나누는 자리는 몫에 0")
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4)
        if k < 8:
            d = R.randint(2, 9) * 10; Q = R.randint(2, 9); r = 0 if k % 2 == 0 else R.randint(1, d - 1)
        else:
            d = R.randint(12, 49); Q = R.randint(2, 9); r = R.randint(0, d - 1) if k % 2 else 0
            if d % 10 == 0:
                return
        n = d * Q + r
        if n > 999 or n < 100 and k >= 8 and k % 3 == 0:
            return
        put(4, n, d, f"{d}{'을' if bat(d) else '를'} 몇십으로 어림해 몫을 정하고 — 곱해서 빼요", est=True)
    fill(S, 4, 20, g4)

    def g5():
        d = R.randint(12, 48); Q = R.randint(11, 39); r = R.randint(0, d - 1) if S.count(5) % 2 else 0
        n = d * Q + r
        if n > 999 or d % 10 == 0 or n // 10 < d:
            return
        put(5, n, d, "앞 두 자리부터 — 어림 → 곱하기 → 빼기 → 내리기", est=True)
    fill(S, 5, 20, g5)
    return S


# ══════════ 혼합 계산 ══════════
TPL = {
    1: [["a", "−", "b", "+", "c"], ["a", "+", "b", "−", "c"], ["a", "−", "(", "b", "+", "c", ")"], ["a", "−", "(", "b", "−", "c", ")"], ["a", "+", "b", "−", "c", "+", "d"]],
    2: [["a", "÷", "b", "×", "c"], ["a", "×", "b", "÷", "c"], ["a", "÷", "(", "b", "×", "c", ")"], ["a", "×", "b", "÷", "c", "×", "d"]],
    3: [["a", "+", "b", "×", "c"], ["a", "−", "b", "×", "c"], ["(", "a", "+", "b", ")", "×", "c"], ["a", "×", "(", "b", "−", "c", ")"], ["a", "×", "b", "−", "c", "×", "d"], ["a", "+", "b", "×", "c", "−", "d"]],
    4: [["a", "+", "b", "÷", "c"], ["a", "−", "b", "÷", "c", "+", "d"], ["(", "a", "+", "b", ")", "÷", "c"], ["a", "÷", "(", "b", "−", "c", ")"], ["a", "÷", "b", "+", "c", "÷", "d"]],
    5: [["a", "−", "(", "b", "+", "c", ")", "×", "d", "÷", "e"], ["a", "+", "b", "×", "c", "÷", "d", "−", "e"], ["(", "a", "−", "b", ")", "÷", "c", "×", "d", "+", "e"], ["a", "×", "(", "b", "+", "c", ")", "−", "d", "÷", "e"], ["a", "÷", "b", "+", "(", "c", "−", "d", ")", "×", "e"]],
}

def mix():
    S = Set("mix", "혼합 계산 — 계산하는 차례", "혼합 계산",
            {1: "덧셈 · 뺄셈 섞인 식", 2: "곱셈 · 나눗셈 섞인 식", 3: "+ − × 섞인 식", 4: "+ − ÷ 섞인 식", 5: "+ − × ÷ 와 괄호"},
            pp=10,
            tips={1: "덧셈과 뺄셈만 있으면 앞에서부터 차례로. 괄호가 있으면 괄호 안을 먼저",
                  2: "곱셈과 나눗셈만 있으면 앞에서부터 차례로. 괄호가 있으면 괄호 안을 먼저",
                  3: "곱셈을 덧셈 · 뺄셈보다 먼저 — 괄호가 있으면 괄호가 가장 먼저",
                  4: "나눗셈을 덧셈 · 뺄셈보다 먼저",
                  5: "괄호 → 곱셈 · 나눗셈(앞에서부터) → 덧셈 · 뺄셈(앞에서부터)"},
            note="혼합 계산은 계산하기 전에 식 아래에 ①, ②, ③ 차례를 먼저 적게 해 주세요. 차례만 맞으면 계산은 쉬운 한 단계씩이에요.")
    R = rng(323)

    def gen(st):
        tpl = R.choice(TPL[st])
        vals = {}
        for v in "abcde":
            vals[v] = R.randint(2, 9) if st in (2, 5) and v in "bcde" else R.randint(2, 60)
        if st in (2, 4, 5):
            for v in "abcde":
                vals[v] = R.choice([R.randint(2, 12), R.randint(12, 96)]) if v == "a" else R.randint(2, 12)
        toks = [vals[t] if t in vals else t for t in tpl]
        steps = reduce_steps(toks)
        if not steps:
            return
        res = steps[-1][2][0]
        if res > 999 or any(isinstance(t, int) and t > 999 for s in steps for t in s[2]):
            return
        if st in (1, 3) and any(isinstance(t, int) and t > 200 for t in toks):
            return
        expr = toks_str(toks)
        lines = []
        for k, (prev, hl, new, span, core_) in enumerate(steps):
            op = prev[core_[0] + 1]
            in_par = hl != core_
            others = [t for i, t in enumerate(prev) if t in ("+", "−") and not (hl[0] <= i <= hl[1])]
            if in_par:
                memo = "괄호 안을 먼저"
            elif op in ("×", "÷") and others:
                memo = f"{'곱셈' if op == '×' else '나눗셈'}을 먼저"
            elif len(new) == 1:
                memo = None
            else:
                memo = "앞에서부터 차례로"
            lines.append(L(f"{toks_str(prev, hl)} = {toks_str(new)}", memo=memo))
        f = Fig()
        order_fig(f, toks, steps)
        f.text(330, 560, f"= {res}", z=52, b=700, at=len(steps) - 1, c="coral")
        has_par = "(" in tpl
        plan = ("괄호 안 → " if has_par else "") + ("× ÷ → + − 차례로" if st >= 3 else "앞에서부터 차례로")
        q = f"{expr}를 계산하세요." if not bat(toks[-1] if toks[-1] != ")" else toks[-2]) else f"{expr}을 계산하세요."
        S.add(st, q, str(res), plan, lines, f.out(), key=expr)

    for st in range(1, 6):
        fill(S, st, 20, lambda st=st: gen(st))
    return S


# ══════════ 약수와 배수 ══════════
def divisors(n):
    return [k for k in range(1, n + 1) if n % k == 0]

def pfs(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p)
            n //= p
        p += 1
    return out

def gcd_steps(a, b):
    """공약수로 차례로 나누기 — 작은 소수부터"""
    divs = []
    while True:
        g = gcd(a, b)
        if g == 1:
            return divs, a, b
        p = pfs(g)[0]
        divs.append(p)
        a, b = a // p, b // p

def gcd_set():
    S = Set("gcd", "약수와 배수 — 최대공약수 · 최소공배수", "약수와 배수",
            {1: "약수 모두 찾기", 2: "배수 · 공배수 세기", 3: "최대공약수", 4: "최소공배수", 5: "최대공약수 · 최소공배수의 활용"},
            pp=10,
            tips={1: "곱해서 그 수가 되는 두 수를 짝지어 찾아요 — 36 = 1 × 36 = 2 × 18 = 3 × 12 = 4 × 9 = 6 × 6",
                  2: "100까지 7의 배수의 개수 = 100 ÷ 7의 몫. 공배수는 두 배수 목록에 함께 있는 수",
                  3: "두 수를 공약수로 계속 나누어 더 나눌 수 없을 때, 왼쪽에 나눈 수들의 곱이 최대공약수",
                  4: "왼쪽에 나눈 수들과 아래에 남은 수들을 모두 곱하면 최소공배수",
                  5: "‘똑같이 최대한 많이 나누기’ · ‘가장 큰 정사각형’은 최대공약수, ‘다시 동시에’ · ‘가장 작은 정사각형’은 최소공배수"},
            note="최대공약수와 최소공배수는 공약수로 나누는 그림(사다리) 하나로 함께 구해요. 활용 문제는 ‘나누는 이야기(약수)’인지 ‘늘어나는 이야기(배수)’인지 먼저 가르게 해 주세요.")
    R = rng(324)

    def g1():
        n = R.choice([k for k in range(12, 101) if len(divisors(k)) >= 6])
        ds = divisors(n)
        pairs = [(a, n // a) for a in ds if a * a <= n]
        f = Fig()
        m = len(ds)
        xs = [60 + 540 * i / (m - 1) for i in range(m)]
        for i, v in enumerate(ds):
            f.text(xs[i], 330, str(v), z=30 if m <= 10 else 24, at=0, b=700)
        for k, (a, b) in enumerate(pairs):
            i, j = ds.index(a), ds.index(b)
            if i == j:
                f.circ(xs[i], 320, 26, c="gold", sw=3, at=0, dl=200 * k)
                continue
            A, B = xs[i], xs[j]
            h = 30 + (B - A) * 0.32
            pts = [(A + (B - A) * t / 16, 300 - h * 4 * (t / 16) * (1 - t / 16)) for t in range(17)]
            f.poly(pts, c="teal", w=3, z=False, dr=True, at=0, dl=200 * k)
        q = f"{n}의 약수는 모두 몇 개인가요?"
        lines = [L(f"{n} = " + " = ".join(f"{a} × {b}" for a, b in pairs), memo=f"곱해서 {iga(n)} 되는 두 수"), L(f"약수: {', '.join(map(str, ds))}", memo="짝을 모두 펼쳐 쓰기"), L(f"모두 {m}개")]
        S.add(1, q, f"{m}개", "곱해서 그 수가 되는 두 수를 짝지어 찾아요", lines, f.out(), ap=str(m), key=f"d{n}")
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        if k == 0:
            d, N = R.randint(3, 13), R.choice([50, 60, 80, 100, 120, 150, 200])
            q = f"1부터 {N}까지의 자연수 중에서 {d}의 배수는 모두 몇 개인가요?"
            c, r = divmod(N, d)
            lines = [L(f"{N} ÷ {d} = {c} … {r}", memo=f"{d} × {c} = {d * c}까지"), L(f"{d} × 1, {d} × 2, …, {d} × {c}"), L(f"{c}개")]
            ans = c
            plan = f"{N} 안에 {iga(d)} 몇 번 — 몫이 배수의 개수"
        elif k == 1:
            d = R.randint(3, 9); lo = R.randint(20, 60); hi = lo + R.randint(30, 90)
            c1, r1 = divmod(hi, d)
            c0, r0 = divmod(lo - 1, d)
            q = f"{lo}부터 {hi}까지의 자연수 중에서 {d}의 배수는 모두 몇 개인가요?"
            lines = [L(f"{hi} ÷ {d} = {c1} … {r1}", memo=f"1부터 {hi}까지 {c1}개"), L(f"{lo - 1} ÷ {d} = {c0} … {r0}", memo=f"1부터 {lo - 1}까지 {c0}개"), L(f"{c1} − {c0} = {c1 - c0}", memo="빼면 사이에 있는 개수"), L(f"{c1 - c0}개")]
            ans = c1 - c0
            plan = "1부터 끝까지의 개수 − 1부터 시작 전까지의 개수"
        else:
            a, b = R.sample([2, 3, 4, 5, 6, 8, 9, 10, 12, 15], 2)
            l = lcm(a, b)
            N = R.choice([50, 60, 80, 100])
            if l > N // 2 or l in (a, b):
                return
            c = N // l
            q = f"{N}보다 작거나 같은 자연수 중에서 {a}의 배수도 되고 {b}의 배수도 되는 수는 모두 몇 개인가요?"
            la = ", ".join(str(a * i) for i in range(1, min(l // a * 2, 8) + 1))
            lb = ", ".join(str(b * i) for i in range(1, min(l // b * 2, 8) + 1))
            lines = [L(f"{a}의 배수: {la}, …"), L(f"{b}의 배수: {lb}, …"), L(f"함께 있는 수: {l}, {2 * l}, … → {l}의 배수", memo="공배수 = 최소공배수의 배수"), L(f"{N} ÷ {l} = {c} … {N % l}"), L(f"{c}개")]
            ans = c
            plan = "공배수는 가장 작은 공배수의 배수 — 그 개수를 세요"
        S.add(2, q, f"{ans}개", plan, lines, None, ap=str(ans), key=q)
    fill(S, 2, 20, g2)

    def pick_pair(lo=12, hi=120):
        g = R.choice([4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24])
        x, y = R.sample(range(2, 9), 2)
        if gcd(x, y) != 1:
            return None
        a, b = g * x, g * y
        if not (lo <= a <= hi and lo <= b <= hi):
            return None
        return min(a, b), max(a, b)

    def ladder_fig(a, b, divs, x, y, show):
        f = Fig()
        cur, xs, xl, ys = ladder(f, [a, b], divs)
        k = len(divs)
        if show == "gcd":
            f.rect(xl - 70, 120, 64, 86 * k + 4, c="gold", sw=4, rx=10, at=k)
        else:
            f.rect(xl - 70, 120, 64, 86 * k + 4, c="gold", sw=4, rx=10, at=k)
            f.rect(xs[0] - 60, 170 + 86 * k - 52, xs[1] - xs[0] + 120, 70, c="coral", sw=4, rx=10, at=k)
        return f

    def g3():
        pr = pick_pair()
        if not pr:
            return
        a, b = pr
        divs, x, y = gcd_steps(a, b)
        if len(divs) < 2:
            return
        g = gcd(a, b)
        f = ladder_fig(a, b, divs, x, y, "gcd")
        lines = []
        ca, cb = a, b
        for p in divs:
            ca, cb = ca // p, cb // p
            lines.append(L(f"{RO(p)} 나누면 {ca}, {cb}", memo="두 수를 모두 나누는 수"))
        lines.append(L(f"{ca}, {cb}{'은' if bat(cb) else '는'} 1 말고는 공약수가 없어요", memo="더 나눌 수 없음"))
        lines.append(L(f"{' × '.join(map(str, divs))} = {g}", pre="최대공약수", memo="왼쪽 수들의 곱"))
        S.add(3, f"{wa(a)} {b}의 최대공약수를 구하세요.", str(g), "두 수를 공약수로 계속 나누어요 — 왼쪽 수들의 곱", lines, f.out(), key=f"g{a}|{b}")
    fill(S, 3, 20, g3)

    def g4():
        pr = pick_pair(8, 90)
        if not pr:
            return
        a, b = pr
        divs, x, y = gcd_steps(a, b)
        if len(divs) < 1:
            return
        l = lcm(a, b)
        if l > 600:
            return
        f = ladder_fig(a, b, divs, x, y, "lcm")
        lines = []
        ca, cb = a, b
        for p in divs:
            ca, cb = ca // p, cb // p
            lines.append(L(f"{RO(p)} 나누면 {ca}, {cb}", memo="공약수로 나누기"))
        lines.append(L(f"{' × '.join(map(str, divs + [ca, cb]))} = {l}", pre="최소공배수", memo="왼쪽 수와 아래 수를 모두 곱해요"))
        lines.append(L(f"{l} ÷ {a} = {l // a}, {l} ÷ {b} = {l // b}", pre="확인", memo="둘 다 나누어떨어져요"))
        S.add(4, f"{wa(a)} {b}의 최소공배수를 구하세요.", str(l), "공약수로 나눈 사다리 — 왼쪽 수와 아래 수를 모두 곱해요", lines, f.out(), key=f"l{a}|{b}")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        pr = pick_pair(12, 72) if k in (0, 2) else pick_pair(6, 30)
        if not pr:
            return
        a, b = pr
        divs, x, y = gcd_steps(a, b)
        g, l = gcd(a, b), lcm(a, b)
        f = ladder_fig(a, b, divs, x, y, "gcd" if k in (0, 2) else "lcm")
        steps = []
        ca, cb = a, b
        for p in divs:
            ca, cb = ca // p, cb // p
            steps.append(L(f"{RO(p)} 나누면 {ca}, {cb}"))
        if k == 0:
            t1, t2 = R.sample(["사탕", "초콜릿", "젤리", "쿠키", "귤", "연필"], 2)
            q = f"{t1} {a}개와 {t2} {b}개를 남김없이 최대한 많은 친구에게 똑같이 나누어 주려고 해요. 몇 명에게 나누어 줄 수 있나요?"
            lines = [L("둘 다 남김없이 똑같이 → 공약수", memo="최대한 많이 → 최대공약수")] + steps + [L(f"{' × '.join(map(str, divs))} = {g}", pre="최대공약수"), L(f"{g}명")]
            ans, ap, plan = f"{g}명", str(g), "똑같이 최대한 많이 나누기 → 최대공약수"
        elif k == 1:
            q = f"두 버스가 같은 정류장에서 오전 9시에 함께 출발했어요. 한 버스는 {a}분마다, 다른 버스는 {b}분마다 출발한다면 처음으로 다시 함께 출발하는 것은 몇 분 뒤인가요?"
            lines = [L(f"{a}의 배수 · {b}의 배수에 함께 출발", memo="처음으로 다시 → 최소공배수")] + steps + [L(f"{' × '.join(map(str, divs + [ca, cb]))} = {l}", pre="최소공배수"), L(f"{l}분 뒤")]
            ans, ap, plan = f"{l}분 뒤", str(l), "‘다시 함께’ → 공배수, 처음으로 → 최소공배수"
        elif k == 2:
            q = f"가로 {a} cm, 세로 {b} cm인 직사각형 종이를 남는 부분 없이 똑같은 크기의 가장 큰 정사각형으로 자르려고 해요. 정사각형의 한 변은 몇 cm인가요?"
            lines = [L("가로 · 세로를 모두 나누어떨어지게 → 공약수", memo="가장 큰 → 최대공약수")] + steps + [L(f"{' × '.join(map(str, divs))} = {g}", pre="최대공약수"), L(f"한 변 {g} cm")]
            ans, ap, plan = f"{g} cm", str(g), "가장 큰 정사각형 조각 → 최대공약수"
        else:
            q = f"가로 {a} cm, 세로 {b} cm인 직사각형 카드를 같은 방향으로 겹치지 않게 늘어놓아 가장 작은 정사각형을 만들려고 해요. 정사각형의 한 변은 몇 cm인가요?"
            lines = [L(f"한 변은 {a}의 배수이면서 {b}의 배수", memo="가장 작은 → 최소공배수")] + steps + [L(f"{' × '.join(map(str, divs + [ca, cb]))} = {l}", pre="최소공배수"), L(f"한 변 {l} cm")]
            ans, ap, plan = f"{l} cm", str(l), "카드를 늘어놓아 만드는 가장 작은 정사각형 → 최소공배수"
        for el in f.els:
            if isinstance(el.get("at"), int):
                el["at"] += 1
        S.add(5, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 분수의 크기 ══════════
def pie(f, d, n, cx=330, cy=330, r=210, at="q", col="gold", fill_at=None):
    f.circ(cx, cy, r, c="ink", sw=3, at=at)
    for i in range(d):
        f.line(cx, cy, *ang_pt(cx, cy, r, 90 - 360 * i / d), c="ink", w=2.5, at=at)
    for i in range(n):
        f.arc(cx, cy, r - 3, 90 - 360 * (i + 1) / d, 90 - 360 * i / d, c="none", sw=0, f=col, fo=0.5, at=at if fill_at is None else fill_at, dl=i * 80)

def fsize():
    S = Set("fsize", "분수 — 나타내기에서 크기 비교까지", "분수의 크기",
            {1: "분수로 나타내기", 2: "단위분수 · 분자가 같은 분수 비교", 3: "가분수 ↔ 대분수", 4: "크기가 같은 분수", 5: "분모가 다른 분수의 크기 비교"},
            mixed=True, pp=8,
            tips={1: "전체를 똑같이 몇으로 나누었는지가 분모, 그중 몇 개인지가 분자",
                  2: "분자가 같으면 분모가 작을수록(크게 나눌수록) 커요 — {1/3} > {1/5}",
                  3: "{17/5} → 17 ÷ 5 = 3 … 2 → 3{2/5} · 2{3/4} → 4 × 2 + 3 = 11 → {11/4}",
                  4: "분모와 분자에 같은 수를 곱하거나 같은 수로 나누면 크기가 같은 분수",
                  5: "분모를 같게(통분) 한 뒤 분자끼리 비교해요"},
            note="분수의 크기는 그림(막대 · 원)으로 먼저 보고 규칙으로 옮겨 가게 해 주세요. ‘분모가 크면 더 크다’는 흔한 오해를 단위분수 그림으로 바로잡아요.")
    R = rng(325)
    BX, BW, BH = 50, 560, 70

    def g1():
        k = S.count(1) % 4
        d = R.randint(3, 12); n = R.randint(1, d - 1)
        f = Fig()
        if k % 2 == 0:
            fbar(f, BX, 260, BW, BH + 10, d)
            ffill(f, BX, 260, BW, BH + 10, d, 0, n, "gold", "q")
            what = "막대를"
        else:
            if d > 10:
                return
            pie(f, d, n)
            what = "원을"
        if k < 2:
            q = f"{what} 똑같이 {d}칸으로 나누어 {n}칸을 색칠했어요. 색칠한 부분은 전체의 몇 분의 몇인가요?"
            lines = [L(f"전체를 똑같이 {d}칸 → 분모 {d}"), L(f"색칠한 칸 {n}개 → 분자 {n}"), L(f"{F_(n, d)}")]
            ans = F_(n, d)
        else:
            q = f"{what} 똑같이 {d}칸으로 나누어 {n}칸을 색칠했어요. 색칠하지 않은 부분은 전체의 몇 분의 몇인가요?"
            lines = [L(f"전체를 똑같이 {d}칸 → 분모 {d}"), L(f"{d} − {n} = {d - n}", pre="색칠하지 않은 칸"), L(f"{F_(d - n, d)}")]
            ans = F_(d - n, d)
        S.add(1, q, ans, "똑같이 나눈 수가 분모, 가리키는 칸 수가 분자", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        d1, d2 = R.sample(range(2, 13), 2)
        n = 1 if k == 0 else R.randint(2, min(d1, d2) - 1) if min(d1, d2) > 2 else None
        if n is None:
            return
        a, b = F_(n, d1), F_(n, d2)
        big, small = (a, b) if d1 < d2 else (b, a)
        f = Fig()
        for i, (d, y, col) in enumerate(((d1, 170, "gold"), (d2, 380, "teal"))):
            fbar(f, BX, y, BW, BH, d)
            ffill(f, BX, y, BW, BH, d, 0, n, col, 0)
            f.text(BX, y - 20, F_(n, d), z=34, c=col, b=700, a="s")
        q = f"{wa(a)} {b} 중에서 더 큰 분수는 무엇인가요?"
        lines = [L(f"분자가 {RO(n)} 같아요", memo="같은 개수의 조각"),
                 L(f"분모가 작을수록 한 조각이 커요", memo=f"{min(d1, d2)}칸 조각 > {max(d1, d2)}칸 조각"), L(f"{big} > {small}")]
        S.add(2, q, big, "분자가 같으면 분모가 작은 쪽이 커요", lines, f.out(), key=f"{min(d1, d2)}|{max(d1, d2)}|{n}")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        d = R.randint(2, 9); w = R.randint(1, 4); r = R.randint(1, d - 1)
        n = w * d + r
        f = Fig()
        rows = w + 1
        bh = min(70, 420 / rows - 16)
        for i in range(rows):
            y = 130 + i * (bh + 18)
            fbar(f, BX, y, BW, bh, d)
            ffill(f, BX, y, BW, bh, d, 0, d if i < w else r, "gold" if i < w else "teal", "q", step=30)
        if k == 0:
            q = f"{J(F_(n, d), '을', '를')} 대분수로 나타내세요."
            lines = [L(f"{n} ÷ {d} = {w} … {r}", memo="몫은 자연수, 나머지는 분자"), L(f"{F_(n, d)} = {w}{F_(r, d)}")]
            ans = f"{w}{F_(r, d)}"
            plan = "분자를 분모로 나누어 — 몫은 자연수, 나머지는 분자"
        else:
            q = f"{J(f'{w}{F_(r, d)}', '을', '를')} 가분수로 나타내세요."
            lines = [L(f"{d} × {w} + {r} = {n}", memo=f"자연수 {w} = {F_(d * w, d)}"), L(f"{w}{F_(r, d)} = {F_(n, d)}")]
            ans = F_(n, d)
            plan = f"자연수를 {F_(1, d)}이 몇 개인지로 바꾸어 분자에 더해요"
        f.text(330, 600, ans, z=56, at=len(lines) - 1, b=700, c="coral")
        S.add(3, q, ans, plan, lines, f.out(), key=f"{k}|{n}/{d}")
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        d = R.randint(2, 7); n = R.randint(1, d - 1)
        if gcd(n, d) != 1:
            return
        m = R.randint(2, 6)
        N_, D_ = n * m, d * m
        f = Fig()
        fbar(f, BX, 180, BW, BH, d)
        ffill(f, BX, 180, BW, BH, d, 0, n, "gold", "q")
        fbar(f, BX, 360, BW, BH, D_)
        ffill(f, BX, 360, BW, BH, D_, 0, N_, "teal", 1, step=40)
        f.line(BX + BW * n / d, 150, BX + BW * n / d, 460, c="red", w=3, d=True, at=1)
        if k == 0:
            q = f"{F_(n, d)} = {{□/{D_}}}일 때 □에 알맞은 수는 얼마인가요?"
            lines = [L(f"{d} × {m} = {D_}", memo=f"분모에 {m}{'을' if bat(m) else '를'} 곱했으니"), L(f"{n} × {m} = {N_}", memo="분자에도 똑같이"), L(f"{F_(n, d)} = {F_(N_, D_)}")]
            ans = str(N_)
        else:
            q = f"{F_(N_, D_)} = {{{n}/□}}일 때 □에 알맞은 수는 얼마인가요?"
            lines = [L(f"{N_} ÷ {m} = {n}", memo=f"분자를 {RO(m)} 나누었으니"), L(f"{D_} ÷ {m} = {d}", memo="분모도 똑같이"), L(f"{F_(N_, D_)} = {F_(n, d)}")]
            ans = str(d)
        S.add(4, q, ans, "분모 · 분자에 같은 수를 곱하거나 같은 수로 나눠요", lines, f.out(), key=f"{k}|{n}/{d}|{m}")
    fill(S, 4, 20, g4)

    def g5():
        d1, d2 = R.sample(range(2, 11), 2)
        n1, n2 = R.randint(1, d1 - 1), R.randint(1, d2 - 1)
        if gcd(n1, d1) != 1 or gcd(n2, d2) != 1 or Fr(n1, d1) == Fr(n2, d2) or d1 % d2 == 0 or d2 % d1 == 0:
            return
        if abs(Fr(n1, d1) - Fr(n2, d2)) > Fr(1, 4):
            return
        l = lcm(d1, d2)
        a, b = F_(n1, d1), F_(n2, d2)
        A, B = F_(n1 * l // d1, l), F_(n2 * l // d2, l)
        big = a if Fr(n1, d1) > Fr(n2, d2) else b
        f = Fig()
        for i, (n, d, y, col) in enumerate(((n1, d1, 170, "gold"), (n2, d2, 390, "teal"))):
            fbar(f, BX, y, BW, BH, d)
            ffill(f, BX, y, BW, BH, d, 0, n, col, "q")
            f.text(BX, y - 20, F_(n, d), z=34, c=col, b=700, a="s")
            sub = l // d
            if sub > 1 and l <= 40:
                for j in range(1, l):
                    if j % sub:
                        f.line(BX + BW * j / l, y + 4, BX + BW * j / l, y + BH - 4, c="red", w=1.5, d=True, at=0)
        q = f"{wa(a)} {b} 중에서 더 큰 분수는 무엇인가요?"
        gt = ">" if Fr(n1, d1) > Fr(n2, d2) else "<"
        lines = [L(f"{a} = {A}", memo=f"분모 {RO(l)} 통분"), L(f"{b} = {B}"), L(f"{A} {gt} {B}", memo="분자끼리 비교"), L(f"{J(big, '이', '가')} 더 커요")]
        S.add(5, q, big, "분모를 같게 한 뒤 분자끼리 비교해요", lines, f.out(), key=f"{min(a, b)}|{max(a, b)}")
    fill(S, 5, 20, g5)
    return S


# ══════════ 분수의 곱셈 ══════════
def cancel(nums, dens):
    """분자들 · 분모들 약분 — (약분 뒤 분자들, 분모들, 메모 목록)"""
    nums, dens = list(nums), list(dens)
    memo = []
    for i in range(len(nums)):
        for j in range(len(dens)):
            g = gcd(nums[i], dens[j])
            if g > 1:
                memo.append(f"{nums[i]}{'과' if bat(nums[i]) else '와'} {dens[j]}")
                nums[i] //= g
                dens[j] //= g
    return nums, dens, memo

def prod_str(xs):
    return " × ".join(map(str, xs))

def fmul():
    S = Set("fmul", "분수의 곱셈 — 분자끼리 분모끼리", "분수의 곱셈",
            {1: "(분수) × (자연수)", 2: "(자연수) × (분수)", 3: "(진분수) × (진분수)", 4: "(대분수)의 곱셈", 5: "세 분수의 곱 · 문장제"},
            mixed=True, pp=10,
            tips={1: "분자에 자연수를 곱해요. 곱하기 전에 자연수와 분모를 약분하면 수가 작아져요",
                  2: "자연수 × 분수도 자연수를 분자에 곱해요 — 8 × {5/6} = {8 × 5/6}",
                  3: "분자끼리, 분모끼리 곱해요. 넓이 그림에서 겹친 칸이 곱이에요",
                  4: "대분수는 가분수로 바꾼 뒤 곱해요",
                  5: "세 분수도 분자끼리 · 분모끼리 한 번에 — 약분을 먼저 하면 편해요. ‘~의 {2/3}’은 × {2/3}"},
            note="분수의 곱셈은 ‘약분 먼저’가 계산을 쉽게 만들어요. 약분할 짝을 선으로 이어 표시하게 하고, 대분수는 반드시 가분수로 바꾼 뒤 곱하게 해 주세요.")
    R = rng(326)

    def finish(nums, dens, lines, start_str):
        """start_str = {a × b/c × d} 꼴 — 약분 · 곱 · 대분수"""
        n2, d2, memo = cancel(nums, dens)
        cur = start_str
        if memo:
            nxt = "{%s/%s}" % (prod_str(n2), prod_str(d2)) if len(d2) > 1 or len(n2) > 1 else F_(n2[0], d2[0])
            if prod_str(d2) == "1" and len(n2) == 1:
                nxt = "{%s/1}" % n2[0]
            lines.append(L(f"{cur} = {nxt}", memo=" · ".join(memo) + " 약분"))
            cur = nxt
        N_, D_ = 1, 1
        for x in n2:
            N_ *= x
        for x in d2:
            D_ *= x
        v = Fr(N_, D_)
        tail = F_(N_, D_) if D_ != 1 else str(N_)
        if v.denominator == 1:
            if cur != str(N_):
                lines.append(L(f"{cur} = {N_}"))
        elif v > 1:
            lines.append(L(f"{cur} = {F_(N_, D_)} = {MX(v)}" if cur != F_(N_, D_) else f"{cur} = {MX(v)}"))
        else:
            if cur != F_(N_, D_):
                lines.append(L(f"{cur} = {F_(N_, D_)}"))
        return v

    def g1():
        n, d = R.randint(1, 11), R.randint(2, 12)
        if n >= d or gcd(n, d) != 1:
            return
        c = R.randint(2, 15)
        if gcd(c, d) == 1 and S.count(1) % 3:
            return
        lines = [L(f"{F_(n, d)} × {c} = {{{n} × {c}/{d}}}", memo="분자에 자연수를 곱해요")]
        v = finish([n, c], [d], lines, f"{{{n} × {c}/{d}}}")
        f = Fig()
        k = min(c, 5)
        for i in range(k):
            y = 90 + i * 100
            fbar(f, 50, y, 560, 58, d)
            ffill(f, 50, y, 560, 58, d, 0, n, "gold", "q", step=40)
        if c > 5:
            f.text(330, 600, f"… 모두 {c}번", z=28, c="soft")
        S.add(1, f"{F_(n, d)} × {J(c, '은', '는')} 얼마인가요?", FX(v), "분자에 자연수를 곱해요 — 약분할 수 있으면 먼저", lines, f.out(), key=f"{n}/{d}x{c}")
    fill(S, 1, 20, g1)

    def g2():
        n, d = R.randint(1, 11), R.randint(2, 12)
        if n >= d or gcd(n, d) != 1:
            return
        c = R.randint(2, 24)
        if gcd(c, d) == 1 and S.count(2) % 3:
            return
        lines = [L(f"{c} × {F_(n, d)} = {{{c} × {n}/{d}}}", memo="자연수를 분자에 곱해요")]
        v = finish([c, n], [d], lines, f"{{{c} × {n}/{d}}}")
        f = Fig()
        fbar(f, 50, 250, 560, 80, d)
        ffill(f, 50, 250, 560, 80, d, 0, n, "teal", "q")
        f.text(330, 210, f"{c}의 {F_(n, d)}", z=34, b=700)
        S.add(2, f"{c} × {J(F_(n, d), '은', '는')} 얼마인가요?", FX(v), f"{c}의 {F_(n, d)} — 자연수를 분자에 곱해요", lines, f.out(), key=f"{c}x{n}/{d}")
    fill(S, 2, 20, g2)

    def g3():
        a, b, c, d = R.randint(1, 7), R.randint(2, 8), R.randint(1, 7), R.randint(2, 8)
        if a >= b or c >= d or gcd(a, b) != 1 or gcd(c, d) != 1:
            return
        lines = [L(f"{F_(a, b)} × {F_(c, d)} = {{{a} × {c}/{b} × {d}}}", memo="분자끼리 · 분모끼리")]
        v = finish([a, c], [b, d], lines, f"{{{a} × {c}/{b} × {d}}}")
        f = Fig()
        X0, Y0, W = 130, 110, 420
        f.rect(X0, Y0, W, W, c="ink", sw=3)
        for i in range(1, b):
            f.line(X0 + W * i / b, Y0, X0 + W * i / b, Y0 + W, c="ink", w=2)
        f.rect(X0 + 2, Y0 + 2, W * a / b - 4, W - 4, c="none", f="gold", fo=0.35, at="q")
        for j in range(1, d):
            f.line(X0, Y0 + W * j / d, X0 + W, Y0 + W * j / d, c="ink", w=2, at=0)
        f.rect(X0 + 2, Y0 + 2, W - 4, W * c / d - 4, c="none", f="teal", fo=0.3, at=0)
        f.rect(X0, Y0, W * a / b, W * c / d, c="coral", sw=5, at=len(lines) - 1)
        f.text(X0 + W * a / b / 2, Y0 - 16, F_(a, b), z=30, c="gold", b=700)
        f.text(X0 - 14, Y0 + W * c / d / 2 + 10, F_(c, d), z=30, c="teal", b=700, a="e", at=0)
        f.text(330, 610, f"전체 {b * d}칸 중 {a * c}칸", z=28, at=len(lines) - 1, c="coral", b=700)
        S.add(3, f"{F_(a, b)} × {J(F_(c, d), '은', '는')} 얼마인가요?", FX(v), "분자끼리, 분모끼리 곱해요", lines, f.out(), key=f"{a}/{b}x{c}/{d}")
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        w1, n1, d1 = R.randint(1, 3), R.randint(1, 5), R.randint(2, 6)
        if n1 >= d1 or gcd(n1, d1) != 1:
            return
        if k == 0:
            w2, n2, d2 = R.randint(1, 3), R.randint(1, 5), R.randint(2, 6)
        else:
            w2, n2, d2 = 0, R.randint(1, 7), R.randint(2, 9)
        if n2 >= d2 or gcd(n2, d2) != 1:
            return
        A, B = w1 * d1 + n1, w2 * d2 + n2
        s1 = f"{w1}{F_(n1, d1)}"
        s2 = f"{w2}{F_(n2, d2)}" if w2 else F_(n2, d2)
        lines = [L(f"{s1} × {s2} = {F_(A, d1)} × {F_(B, d2)}", memo="대분수를 가분수로"), L(f"{F_(A, d1)} × {F_(B, d2)} = {{{A} × {B}/{d1} × {d2}}}")]
        v = finish([A, B], [d1, d2], lines, f"{{{A} × {B}/{d1} × {d2}}}")
        if len(lines) > 5:
            return
        S.add(4, f"{s1} × {J(s2, '은', '는')} 얼마인가요?", FX(v), "대분수를 가분수로 바꾸고 — 약분 먼저", lines, None, key=f"{s1}x{s2}")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            fr = []
            for _ in range(3):
                d = R.randint(2, 9); n = R.randint(1, d - 1)
                if gcd(n, d) != 1:
                    return
                fr.append((n, d))
            ns, ds = [x[0] for x in fr], [x[1] for x in fr]
            n2, d2, memo = cancel(ns, ds)
            if len(memo) < 2:
                return
            ex = " × ".join(F_(n, d) for n, d in fr)
            lines = [L(f"{ex} = {{{prod_str(ns)}/{prod_str(ds)}}}", memo="분자끼리 · 분모끼리 한 번에")]
            v = finish(ns, ds, lines, f"{{{prod_str(ns)}/{prod_str(ds)}}}")
            S.add(5, f"{J(ex, '을', '를')} 계산하세요.", FX(v), "세 분수도 한 번에 — 약분을 먼저", lines, None, key=ex)
        elif k == 1:
            L0n, L0d = R.randint(1, 9), R.randint(2, 10)
            n, d = R.randint(1, 5), R.randint(2, 8)
            if L0n >= L0d or gcd(L0n, L0d) != 1 or n >= d or gcd(n, d) != 1 or gcd(L0n * n, L0d * d) == 1:
                return
            q = f"길이가 {F_(L0n, L0d)} `m`인 리본의 {F_(n, d)}만큼을 잘라 썼어요. 잘라 쓴 리본은 몇 `m`인가요?"
            lines = [L(f"{F_(L0n, L0d)}의 {F_(n, d)} → {F_(L0n, L0d)} × {F_(n, d)}", memo="~의 몇 분의 몇은 곱셈"), L(f"{F_(L0n, L0d)} × {F_(n, d)} = {{{L0n} × {n}/{L0d} × {d}}}")]
            v = finish([L0n, n], [L0d, d], lines, f"{{{L0n} × {n}/{L0d} × {d}}}")
            S.add(5, q, f"{FX(v)} `m`", "‘~의 {2/3}’ → × {2/3}", lines, None, ap=FX(v), key=q)
        else:
            w, n, d = R.randint(2, 5), R.randint(1, 3), R.randint(2, 4)
            w2, n2, d2 = R.randint(1, 3), R.randint(1, 2), R.randint(2, 3)
            if n >= d or n2 >= d2 or gcd(n, d) != 1 or gcd(n2, d2) != 1:
                return
            A, B = w * d + n, w2 * d2 + n2
            if gcd(A, d2) == 1 and gcd(B, d) == 1:
                return
            q = f"한 시간에 {w}{F_(n, d)} km씩 걷는 빠르기로 {w2}{F_(n2, d2)}시간 동안 걸으면 몇 km를 걷나요?"
            lines = [L(f"{w}{F_(n, d)} × {w2}{F_(n2, d2)}", memo="한 시간 거리 × 시간"), L(f"{w}{F_(n, d)} × {w2}{F_(n2, d2)} = {F_(A, d)} × {F_(B, d2)}", memo="가분수로"), L(f"{F_(A, d)} × {F_(B, d2)} = {{{A} × {B}/{d} × {d2}}}")]
            v = finish([A, B], [d, d2], lines, f"{{{A} × {B}/{d} × {d2}}}")
            S.add(5, q, f"{FX(v)} km", "거리 = 한 시간에 가는 거리 × 걸린 시간", lines, None, ap=FX(v), key=q)
    fill(S, 5, 20, g5)
    return S

