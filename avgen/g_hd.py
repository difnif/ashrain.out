# 고등 ④ — 등차수열과 등비수열 · 수열의 합 Σ · 함수의 극한과 연속 · 부정적분과 정적분 · 정적분의 활용
import math
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, Plane, NL, ang_pt
from kit import *
from g_hc import FR, LIN, PS, TAIL, AT, XM, pcurve, gx, bat, ptj

x, t_ = SYMS["x"], SYMS["t"]

def RP(v):
    """거듭제곱 밑 — 음수 · 분수면 괄호"""
    v = Fr(v)
    s = FR(v)
    return f"({s})" if (v < 0 or v.denominator != 1) else s

def POLY(cs, var="x"):
    return poly([Fr(c) for c in cs], var)

def integ(cs):
    """∫ 다항식(높은 차수부터) — 상수항 0"""
    n = len(cs)
    return [Fr(c) / (n - i) for i, c in enumerate(cs)] + [Fr(0)]

def ev(cs, v):
    v = Fr(v)
    r = Fr(0)
    for c in cs:
        r = r * v + Fr(c)
    return r

def mulp(p, q):
    out = [Fr(0)] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += Fr(a) * Fr(b)
    return out

def addp(p, q):
    n = max(len(p), len(q))
    p = [Fr(0)] * (n - len(p)) + [Fr(c) for c in p]
    q = [Fr(0)] * (n - len(q)) + [Fr(c) for c in q]
    return [a + b for a, b in zip(p, q)]

def trim(p):
    p = list(p)
    while len(p) > 1 and p[0] == 0:
        p.pop(0)
    return p

def ATF(cs, v):
    """AT 이지만 0 계수는 건너뛰고, 상수항까지(값 넣은 계산 글자) — 0 을 넣으면 값만"""
    if v == 0:
        return N(ev(cs, 0))
    return AT([Fr(c) for c in cs], v)

def plane(f, xr, yr, at="q", step=1, xn="x", yn="y", square=True):
    """square=False 면 칸을 채우고 y 눈금 간격은 범위에 맞춰(1 · 2 · 5 · 10)"""
    pl = Plane(f, xr, yr, box=(40, 40, 620, 640), square=square)
    if square:
        pl.axes(at=at, lab_step=step, xn=xn, yn=yn)
    else:
        span = yr[1] - yr[0]
        ys = 1 if span <= 9 else 2 if span <= 18 else 5 if span <= 45 else 10
        pl.axes(at=at, lab_step=step, xn=xn, yn=yn, ystep=ys, ygrid=ys)
    return pl

def shade(pl, fn, a, b, at, c="teal", fo=0.28, n=40, base=None):
    """y = fn 와 y = base(없으면 x축) 사이를 칠하기"""
    top = [pl.P(a + (b - a) * i / n, fn(a + (b - a) * i / n)) for i in range(n + 1)]
    if base is None:
        bot = [pl.P(b, 0), pl.P(a, 0)]
    else:
        bot = [pl.P(b - (b - a) * i / n, base(b - (b - a) * i / n)) for i in range(n + 1)]
    return pl.f.poly(top + bot, c="none", f=c, fo=fo, at=at)


# ══════════ 등차수열과 등비수열 ══════════
def seq_row(f, cells, subs, arcs, at="q", arcs_at=None, hl=None, y=330):
    """칸 줄 — cells 글자(None 이면 빈칸), subs 칸 아래 이름, arcs [(i, 글자)] i → i+1 화살"""
    n = len(cells)
    bw, gap = 100, 22
    tot = n * bw + (n - 1) * gap
    x0 = 330 - tot / 2
    xs = [x0 + i * (bw + gap) for i in range(n)]
    for i, (c, s) in enumerate(zip(cells, subs)):
        if c == "…":
            f.text(xs[i] + bw / 2, y + 12, "…", z=40, c="soft", at=at)
            continue
        f.rect(xs[i], y - 40, bw, 80, c="coral" if hl == i else "ink", sw=3, rx=10, at=at, f="gold" if hl == i else None, fo=0.15 if hl == i else None)
        if c is not None:
            f.text(xs[i] + bw / 2, y + 13, c, z=34 if len(c) < 5 else 26, b=700, at=at)
        if s:
            f.text(xs[i] + bw / 2, y + 82, s, z=26, c="soft", at=at)
    for k, (i, lab) in enumerate(arcs):
        a, b = xs[i] + bw * 0.62, xs[i + 1] + bw * 0.38
        pp = [(a + (b - a) * j / 12, y - 46 - 50 * 4 * (j / 12) * (1 - j / 12)) for j in range(13)]
        w = arcs_at[k] if arcs_at else at
        f.poly(pp, c="teal", w=4, z=False, dr=True, ar=1, at=w)
        f.text((a + b) / 2, y - 112, lab, z=26, c="teal", b=700, at=w)
    return xs

def seq():
    S = Set("seq", "등차수열과 등비수열 — 일반항과 합", "등차·등비수열",
            {1: "등차수열의 일반항", 2: "등차수열의 합", 3: "등비수열의 일반항", 4: "등비수열의 합", 5: "합과 일반항 · 중항"},
            pp=10,
            tips={1: "a_{n} = a + (n − 1)d — 첫째항에 공차를 (n − 1)번",
                  2: "S_{n} = {n(a + l)/2} = {n{2a + (n − 1)d}/2}",
                  3: "a_{n} = ar^{n − 1} — 첫째항에 공비를 (n − 1)번 곱해요",
                  4: "S_{n} = {a(r^{n} − 1)/r − 1} (r ≠ 1)",
                  5: "a_{n} = S_{n} − S_{n − 1} (n ≥ 2) · 등차중항 2b = a + c · 등비중항 b^{2} = ac"},
            note="등차수열은 ‘같은 수를 더하고’, 등비수열은 ‘같은 수를 곱해요’. 칸 사이 화살에 +d, ×r을 적어 보게 하면 일반항의 (n − 1)이 왜 나오는지 바로 보여요.")
    R = rng(2401)

    def g1():
        a1 = R.randint(-10, 20)
        d = R.choice([-5, -4, -3, -2, 2, 3, 4, 5, 6, 7])
        n = R.randint(8, 30)
        an = a1 + (n - 1) * d
        f = Fig()
        if S.count(1) % 2 == 0:
            q = f"첫째항이 {N(a1)}, 공차가 {N(d)}인 등차수열의 제{n}항을 구하세요."
            lines = [L("a_{n} = a + (n − 1)d", memo="등차수열의 일반항"),
                     L(f"a_{{{n}}} = {N(a1)} + ({n} − 1) × {NP(d)} = {N(an)}")]
            seq_row(f, [N(a1), N(a1 + d), N(a1 + 2 * d), "…", None], ["a_{1}", "a_{2}", "a_{3}", "", f"a_{{{n}}}"], [(0, f"+{N(d)}" if d > 0 else N(d)), (1, f"+{N(d)}" if d > 0 else N(d))], hl=4)
            S.add(1, q, N(an), "a_{n} = a + (n − 1)d", lines, f.out(), key=q)
        else:
            m = R.randint(2, 5)
            k = m + R.randint(2, 6)
            A, B = a1 + (m - 1) * d, a1 + (k - 1) * d
            if n <= k:
                return
            q = f"a_{{{m}}} = {N(A)}, a_{{{k}}} = {N(B)}인 등차수열 {{a_{{n}}}}의 제{n}항을 구하세요."
            lines = [L(f"{k - m}d = {N(B)} − {NP(A)} = {N(B - A)}", memo=f"a_{{{k}}} − a_{{{m}}} = ({k} − {m})d"),
                     L(f"d = {N(d)}, a_{{1}} = {N(A)} − {m - 1} × {NP(d)} = {N(a1)}"),
                     L(f"a_{{{n}}} = {N(a1)} + {n - 1} × {NP(d)} = {N(an)}")]
            S.add(1, q, N(an), "두 항의 차로 공차부터", lines, None, sub={"d": d}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        a = R.randint(-8, 15)
        d = R.choice([-4, -3, -2, 2, 3, 4, 5, 6])
        n = R.randint(8, 30)
        l = a + (n - 1) * d
        if (n * (a + l)) % 2:
            return
        Sn = n * (a + l) // 2
        if S.count(2) % 2 == 0:
            q = f"첫째항이 {N(a)}, 공차가 {N(d)}인 등차수열의 첫째항부터 제{n}항까지의 합을 구하세요."
            lines = [L("S_{n} = {n{2a + (n − 1)d}/2}", memo="첫째항과 공차로"),
                     L(f"S_{{{n}}} = {{{n}(2 × {NP(a)} + {n - 1} × {NP(d)})/2}} = {N(Sn)}")]
            S.add(2, q, N(Sn), "S_{n} = {n{2a + (n − 1)d}/2}", lines, None, key=q)
        else:
            q = f"등차수열 {N(a)}, {N(a + d)}, {N(a + 2 * d)}, …, {N(l)}의 합을 구하세요."
            lines = [L(f"{N(l)} = {N(a)} + (n − 1) × {NP(d)} → n = {n}", memo="항의 개수부터"),
                     L(f"S = {{{n}({N(a)} + {NP(l)})/2}} = {N(Sn)}", memo="S_{n} = {n(a + l)/2}")]
            S.add(2, q, N(Sn), "항의 개수 n을 구한 뒤 {n(a + l)/2}", lines, None, sub={"n": n}, key=q)
    fill(S, 2, 20, g2)

    def g3():
        a1 = R.choice([1, 2, 3, 4, 5, -1, -2, -3])
        r = R.choice([2, 3, -2, -3, 2, 4])
        f = Fig()
        if S.count(3) % 2 == 0:
            n = R.randint(4, 8 if abs(r) == 2 else 6)
            an = a1 * r ** (n - 1)
            q = f"첫째항이 {N(a1)}, 공비가 {N(r)}인 등비수열의 제{n}항을 구하세요."
            lines = [L("a_{n} = ar^{n − 1}", memo="등비수열의 일반항"),
                     L(f"a_{{{n}}} = {N(a1)} × {RP(r)}^{{{n - 1}}} = {N(an)}")]
            seq_row(f, [N(a1), N(a1 * r), N(a1 * r * r), "…", None], ["a_{1}", "a_{2}", "a_{3}", "", f"a_{{{n}}}"], [(0, f"×{RP(r)}"), (1, f"×{RP(r)}")], hl=4)
            S.add(3, q, N(an), "a_{n} = ar^{n − 1}", lines, f.out(), key=q)
        else:
            m = R.randint(1, 3)
            k = m + R.choice([1, 3])
            n = k + R.randint(1, 3)
            A, B = a1 * r ** (m - 1), a1 * r ** (k - 1)
            an = a1 * r ** (n - 1)
            if abs(an) > 5000:
                return
            q = f"a_{{{m}}} = {N(A)}, a_{{{k}}} = {N(B)}인 등비수열 {{a_{{n}}}}의 제{n}항을 구하세요. (공비는 실수)"
            lines = [L(f"r^{{{k - m}}} = {{{N(B)}/{N(A)}}} = {N(r ** (k - m))} → r = {N(r)}", memo=f"a_{{{k}}} ÷ a_{{{m}}}"),
                     L(f"a_{{{n}}} = a_{{{k}}} × r^{{{n - k}}} = {N(B)} × {RP(r)}^{{{n - k}}} = {N(an)}")]
            S.add(3, q, N(an), "두 항의 비로 공비부터", lines, None, sub={"r": r}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.choice([1, 2, 3, 4, 5, -2, -3])
        r = R.choice([2, 3, -2, 2, 3, 4])
        n = R.randint(4, 8 if abs(r) == 2 else 6)
        Sn = a * (r ** n - 1) // (r - 1)
        if S.count(4) % 2 == 0:
            q = f"첫째항이 {N(a)}, 공비가 {N(r)}인 등비수열의 첫째항부터 제{n}항까지의 합을 구하세요."
            lines = [L("S_{n} = {a(r^{n} − 1)/r − 1}", memo="r ≠ 1"),
                     L(f"S_{{{n}}} = {{{N(a)}({RP(r)}^{{{n}}} − 1)/{RP(r)} − 1}} = {N(Sn)}")]
            S.add(4, q, N(Sn), "S_{n} = {a(r^{n} − 1)/r − 1}", lines, None, key=q)
        else:
            l = a * r ** (n - 1)
            q = f"등비수열 {N(a)}, {N(a * r)}, {N(a * r * r)}, …, {N(l)}의 합을 구하세요."
            lines = [L(f"{N(a)} × {RP(r)}^{{n − 1}} = {N(l)} → {RP(r)}^{{n − 1}} = {N(l // a)} → n = {n}", memo="항의 개수부터"),
                     L(f"S = {{{N(a)}({RP(r)}^{{{n}}} − 1)/{RP(r)} − 1}} = {N(Sn)}")]
            S.add(4, q, N(Sn), "항의 개수 n을 구한 뒤 등비수열의 합", lines, None, sub={"n": n}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            p_, q_, c = R.choice([1, 2, 3, -1]), R.randint(-5, 5), R.choice([0, 0, 1, -2, 3])
            m = R.randint(4, 15)
            cs = [p_, q_, c]
            am = ev(cs, m) - ev(cs, m - 1)
            q = f"수열 {{a_{{n}}}}의 첫째항부터 제n항까지의 합 S_{{n}}이 S_{{n}} = {POLY(cs, 'n')}일 때, a_{{{m}}}의 값을 구하세요."
            lines = [L(f"a_{{{m}}} = S_{{{m}}} − S_{{{m - 1}}}", memo="a_{n} = S_{n} − S_{n − 1}"),
                     L(f"({ATF(cs, m)}) − ({ATF(cs, m - 1)}) = {N(am)}")]
            S.add(5, q, N(am), "a_{n} = S_{n} − S_{n − 1} (n ≥ 2)", lines, None, key=q)
        elif k == 1:
            a, c = R.randint(-10, 20), R.randint(-10, 30)
            if (a + c) % 2 or a == c:
                return
            b = (a + c) // 2
            q = f"세 수 {N(a)}, x, {J(N(c), '이', '가')} 이 순서로 등차수열을 이룰 때, x의 값을 구하세요."
            lines = [L(f"2x = {N(a)} + {NP(c)}", memo="등차중항 — 가운데 항의 2배 = 양 끝의 합"), L(f"x = {N(b)}")]
            S.add(5, q, N(b), "등차중항 2b = a + c", lines, None, sub={"x": b}, key=q)
        else:
            b0 = R.choice([2, 3, 4, 5, 6, 8, 10, 12])
            r = R.choice([2, 3, Fr(1, 2), Fr(3, 2), 4])
            a, c = Fr(b0) / r, Fr(b0) * r
            if a.denominator != 1 or c.denominator != 1:
                return
            a, c = int(a), int(c)
            q = f"세 양수 {N(a)}, x, {J(N(c), '이', '가')} 이 순서로 등비수열을 이룰 때, x의 값을 구하세요."
            lines = [L(f"x^{{2}} = {N(a)} × {N(c)} = {N(a * c)}", memo="등비중항 — 가운데 항의 제곱 = 양 끝의 곱"), L(f"x > 0 → x = {N(b0)}")]
            S.add(5, q, N(b0), "등비중항 b^{2} = ac", lines, None, sub={"x": b0}, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 수열의 합 Σ ══════════
def SIG(a, b, var="k"):
    return f"Σ_{{{var}={a}}}^{{{b}}}"

def sigma():
    S = Set("sigma", "수열의 합 — Σ의 성질과 자연수 거듭제곱의 합", "Σ와 수열의 합",
            {1: "Σ를 풀어 쓰기", 2: "Σ의 성질", 3: "거듭제곱의 합 공식", 4: "여러 가지 수열의 합", 5: "분수꼴 — 부분분수로"},
            pp=10,
            tips={1: "Σ_{k=1}^{n}a_{k} = a_{1} + a_{2} + … + a_{n} — k에 1, 2, …, n을 차례로",
                  2: "Σ(a_{k} ± b_{k}) = Σa_{k} ± Σb_{k}, Σca_{k} = cΣa_{k}, Σ_{k=1}^{n}c = cn",
                  3: "Σk = {n(n + 1)/2}, Σk^{2} = {n(n + 1)(2n + 1)/6}, Σk^{3} = ({n(n + 1)/2})^{2}",
                  4: "식을 전개해 k^{2}, k, 상수로 나눈 뒤 공식",
                  5: "{1/k(k + 1)} = {1/k} − {1/k + 1} — 이웃끼리 지워져요"},
            note="Σ는 ‘k에 수를 차례로 넣어 더하라’는 약속이에요. 먼저 한두 문제는 풀어 쓴 뒤, 성질과 공식으로 넘어가게 해 주세요.")
    R = rng(2402)

    def g1():
        k = S.count(1) % 3
        if k == 0:
            a, b = R.choice([2, 3, 4, -2, 5]), R.randint(-5, 6)
            lo, n = R.choice([1, 1, 2]), R.randint(4, 6)
            terms = [a * i + b for i in range(lo, n + 1)]
            q = f"{SIG(lo, n)}({LIN(a, b, 'k')})의 값을 구하세요."
            lines = [L(f"{SIG(lo, n)}({LIN(a, b, 'k')}) = " + " + ".join(NP(v) for v in terms) + f" = {N(sum(terms))}", memo=f"k에 {lo}부터 {n}까지")]
        elif k == 1:
            lo, n = R.randint(1, 3), R.randint(4, 7)
            terms = [i * i for i in range(lo, n + 1)]
            q = f"{SIG(lo, n)}k^{{2}}의 값을 구하세요."
            lines = [L(f"{SIG(lo, n)}k^{{2}} = " + " + ".join(f"{i}^{{2}}" for i in range(lo, n + 1)) + f" = {N(sum(terms))}", memo=f"k에 {lo}부터 {n}까지")]
        else:
            b = R.choice([2, 3])
            lo, n = R.randint(1, 2), R.randint(3, 5 if b == 2 else 4)
            terms = [b ** i for i in range(lo, n + 1)]
            q = f"{SIG(lo, n)}{b}^{{k}}의 값을 구하세요."
            lines = [L(f"{SIG(lo, n)}{b}^{{k}} = " + " + ".join(str(v) for v in terms) + f" = {N(sum(terms))}", memo=f"k에 {lo}부터 {n}까지")]
        S.add(1, q, N(sum(terms)), "k에 수를 차례로 넣어 더하기", lines, None, key=q)
    fill(S, 1, 20, g1)

    def g2():
        n = R.choice([10, 15, 20, 8, 12])
        A, B = R.randint(-10, 30), R.randint(-10, 30)
        p_, q_, c = R.choice([1, 2, 3, -1, -2]), R.choice([1, 2, 3, -1, -3]), R.randint(-3, 4)
        val_ = p_ * A + q_ * B + c * n
        inner = f"{'' if p_ == 1 else (MI if p_ == -1 else N(p_))}a_{{k}} {'+' if q_ > 0 else MI} {'' if abs(q_) == 1 else abs(q_)}b_{{k}}" + TAIL(c)
        q = f"{SIG(1, n)}a_{{k}} = {N(A)}, {SIG(1, n)}b_{{k}} = {N(B)}일 때, {SIG(1, n)}({inner})의 값을 구하세요."
        parts = f"{N(p_)} × {NP(A)} {'+' if q_ > 0 else MI} {abs(q_)} × {NP(B)}" + (f" + {N(c)} × {n}" if c > 0 else (f" − {abs(c)} × {n}" if c < 0 else ""))
        lines = [L(f"{SIG(1, n)}({inner}) = {'' if p_ == 1 else (MI if p_ == -1 else N(p_))}Σa_{{k}} {'+' if q_ > 0 else MI} {'' if abs(q_) == 1 else abs(q_)}Σb_{{k}}" + (f" {'+' if c > 0 else MI} Σ{abs(c)}" if c else ""), memo="Σ의 성질로 나누기"),
                 L(f"{parts} = {N(val_)}", memo=f"Σ_{{k=1}}^{{{n}}}{abs(c)} = {abs(c)} × {n}" if c else None)]
        S.add(2, q, N(val_), "Σ(pa_{k} + qb_{k} + c) = pΣa_{k} + qΣb_{k} + cn", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 4
        n = R.randint(5, 20)
        if k == 0:
            v = n * (n + 1) // 2
            q = f"{SIG(1, n)}k의 값을 구하세요."
            lines = [L(f"{SIG(1, n)}k = {{{n} × {n + 1}/2}} = {v}", memo="Σk = {n(n + 1)/2}")]
        elif k == 1:
            v = n * (n + 1) * (2 * n + 1) // 6
            q = f"{SIG(1, n)}k^{{2}}의 값을 구하세요."
            lines = [L(f"{SIG(1, n)}k^{{2}} = {{{n} × {n + 1} × {2 * n + 1}/6}} = {v}", memo="Σk^{2} = {n(n + 1)(2n + 1)/6}")]
        elif k == 2:
            n = R.randint(4, 12)
            v = (n * (n + 1) // 2) ** 2
            q = f"{SIG(1, n)}k^{{3}}의 값을 구하세요."
            lines = [L(f"{SIG(1, n)}k^{{3}} = ({{{n} × {n + 1}/2}})^{{2}} = {n * (n + 1) // 2}^{{2}} = {v}", memo="Σk^{3} = ({n(n + 1)/2})^{2}")]
        else:
            m = R.randint(4, 12)
            n = m + R.randint(4, 12)
            v = n * (n + 1) // 2 - (m - 1) * m // 2
            q = f"{SIG(m, n)}k의 값을 구하세요."
            lines = [L(f"{SIG(m, n)}k = {SIG(1, n)}k − {SIG(1, m - 1)}k", memo=f"1부터 {m - 1}까지를 빼요"),
                     L(f"{{{n} × {n + 1}/2}} − {{{m - 1} × {m}/2}} = {n * (n + 1) // 2} − {(m - 1) * m // 2} = {v}")]
        S.add(3, q, N(v), "자연수 거듭제곱의 합 공식", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        n = R.choice([5, 6, 8, 10, 12, 15, 20])
        s1, s2 = n * (n + 1) // 2, n * (n + 1) * (2 * n + 1) // 6
        if k == 0:
            a, b, c = R.choice([1, 2, 3, 6]), R.randint(-4, 4), R.randint(-3, 3)
            inner = POLY([a, b, c], "k")
        else:
            p_, r_ = R.choice([-3, -2, -1, 1, 2, 3]), R.choice([-3, -2, -1, 1, 2, 3])
            sp1 = R.choice([1, 2])
            # (sp1 k + p)(k + r) = sp1 k^2 + (sp1 r + p) k + p r
            a, b, c = sp1, sp1 * r_ + p_, p_ * r_
            inner = f"({LIN(sp1, p_, 'k')})({LIN(1, r_, 'k')})"
        val_ = a * s2 + b * s1 + c * n
        q = f"{SIG(1, n)}{inner}의 값을 구하세요." if k else f"{SIG(1, n)}({inner})의 값을 구하세요."
        parts = [f"{N(a)} × {{{n} × {n + 1} × {2 * n + 1}/6}}"]
        if b:
            parts.append(f"{'+' if b > 0 else MI} {abs(b)} × {{{n} × {n + 1}/2}}")
        if c:
            parts.append(f"{'+' if c > 0 else MI} {abs(c)} × {n}")
        lines = ([L(f"{inner} = {POLY([a, b, c], 'k')}", memo="전개")] if k else []) + \
                [L(f"{SIG(1, n)}({POLY([a, b, c], 'k')}) = {'' if a == 1 else N(a)}Σk^{{2}}" + (f" {'+' if b > 0 else MI} {'' if abs(b) == 1 else abs(b)}Σk" if b else "") + (f" {'+' if c > 0 else MI} Σ{abs(c)}" if c else ""), memo="Σ의 성질"),
                 L(" ".join(parts) + f" = {N(val_)}")]
        S.add(4, q, N(val_), "전개해서 Σk^{2}, Σk, Σc로", lines, None, ident=True, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        n = R.randint(5, 30)
        if k == 0:
            val_ = Fr(n, n + 1)
            q = f"{SIG(1, n)}{{1/k(k + 1)}}의 값을 구하세요."
            lines = [L("{1/k(k + 1)} = {1/k} − {1/k + 1}", memo="부분분수"),
                     L(f"(1 − {{1/2}}) + ({{1/2}} − {{1/3}}) + … + ({{1/{n}}} − {{1/{n + 1}}})", memo="이웃끼리 지워져요"),
                     L(f"1 − {{1/{n + 1}}} = {FR(val_)}")]
        elif k == 1:
            val_ = Fr(n, 2 * n + 1)
            q = f"{SIG(1, n)}{{1/(2k − 1)(2k + 1)}}의 값을 구하세요."
            lines = [L("{1/(2k − 1)(2k + 1)} = {1/2}({1/2k − 1} − {1/2k + 1})", memo="부분분수"),
                     L(f"{{1/2}}{{(1 − {{1/3}}) + ({{1/3}} − {{1/5}}) + … + ({{1/{2 * n - 1}}} − {{1/{2 * n + 1}}})}}", memo="이웃끼리 지워져요"),
                     L(f"{{1/2}}(1 − {{1/{2 * n + 1}}}) = {FR(val_)}")]
        else:
            val_ = Fr(1, 2) * (1 + Fr(1, 2) - Fr(1, n + 1) - Fr(1, n + 2))
            q = f"{SIG(1, n)}{{1/k(k + 2)}}의 값을 구하세요."
            lines = [L("{1/k(k + 2)} = {1/2}({1/k} − {1/k + 2})", memo="부분분수"),
                     L(f"앞의 1, {wa('{1/2}')} 뒤의 {MI}{{1/{n + 1}}}, {MI}{{1/{n + 2}}}만 남아요", memo="두 칸 건너 지워져요"),
                     L(f"{{1/2}}(1 + {{1/2}} − {{1/{n + 1}}} − {{1/{n + 2}}}) = {FR(val_)}")]
        S.add(5, q, FR(val_), "부분분수로 나누면 이웃끼리 지워져요", lines, None, ident=True, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 함수의 극한과 연속 ══════════
def LIM(a, side=""):
    return f"lim_{{x→{N(a)}{side}}}"

def lim():
    S = Set("lim", "함수의 극한과 연속 — 0/0 · ∞/∞ · 미정계수", "함수의 극한",
            {1: "그래프로 보는 좌극한 · 우극한", 2: "0/0 꼴 — 인수분해 · 유리화", 3: "∞/∞ 꼴 · ∞ − ∞ 꼴", 4: "극한값으로 미정계수", 5: "함수의 연속"},
            pp=8,
            tips={1: "왼쪽에서 다가갈 때(x→a−)와 오른쪽에서 다가갈 때(x→a+)의 y값",
                  2: "분자 · 분모를 인수분해해 (x − a)를 약분하거나, 근호는 유리화",
                  3: "최고차항으로 분모 · 분자를 나눠요 — 차수가 같으면 계수의 비",
                  4: "분모 → 0인데 극한값이 있으면 분자 → 0",
                  5: "연속 ⇔ 좌극한 = 우극한 = 함숫값"},
            note="극한은 ‘가까이 갈 때의 값’이지 ‘그 점의 값’이 아니에요. 그래프에서 빈 동그라미와 찬 동그라미를 먼저 구별하게 해 주세요.")
    R = rng(2403)

    def g1():
        a = R.randint(-2, 3)
        Lv, Rv, Fv = R.randint(-1, 4), R.randint(-1, 4), R.randint(-1, 4)
        if Lv == Rv:
            return
        sl, sr = R.choice([-1, 1, 0, 2, -2]) * Fr(1, 2), R.choice([-1, 1, 0, 2, -2]) * Fr(1, 2)
        f = Fig()
        pl = plane(f, (a - 4.5, a + 4.5), (-2.5, 6.5))
        fl = lambda t: Lv + float(sl) * (t - a)
        fr = lambda t: Rv + float(sr) * (t - a)
        pcurve(pl, fl, [a - 4.5 + 4.5 * i / 20 for i in range(21)], c="sky")
        pcurve(pl, fr, [a + 4.5 * i / 20 for i in range(21)], c="sky")
        for yy in (Lv, Rv):
            if yy != Fv:
                f.circ(*pl.P(a, yy), 8, c="sky", sw=3, f="paper", fo=1)
        f.dot(*pl.P(a, Fv), r=8, f="sky")
        kind = S.count(1) % 5
        fn = R.choice("fgh")
        F_ = f"{fn}(x)"
        Fa = f"{fn}({N(a)})"
        LL, RR = f"{LIM(a, '−')} {F_}", f"{LIM(a, '+')} {F_}"
        full = f"{Fa} = {N(Fv)} — 찬 동그라미"
        if kind == 0:
            ask, ans, last = f"{LL} + {RR}", Lv + Rv, L(f"{N(Lv)} + {NP(Rv)} = {N(Lv + Rv)}")
        elif kind == 1:
            ask, ans, last = f"{LL} − {RR} + {Fa}", Lv - Rv + Fv, L(f"{N(Lv)} − {NP(Rv)} + {NP(Fv)} = {N(Lv - Rv + Fv)}", memo=full)
        elif kind == 2:
            ask, ans, last = f"{RR} × {Fa}", Rv * Fv, L(f"{N(Rv)} × {NP(Fv)} = {N(Rv * Fv)}", memo=full)
        elif kind == 3:
            ask, ans, last = f"{LL} × {RR}", Lv * Rv, L(f"{N(Lv)} × {NP(Rv)} = {N(Lv * Rv)}")
        else:
            ask, ans, last = f"{Fa} + {LL}", Fv + Lv, L(f"{N(Fv)} + {NP(Lv)} = {N(Fv + Lv)}", memo=full)
        q = f"함수 y = {F_}의 그래프가 그림과 같을 때, {ask}의 값을 구하세요."
        lines = [L(f"{LL} = {N(Lv)}", memo="왼쪽에서 다가갈 때"),
                 L(f"{RR} = {N(Rv)}", memo="오른쪽에서 다가갈 때"), last]
        f.line(*pl.P(a - 1.6, Lv - float(sl) * 1.6 + 0.0), *pl.P(a - 0.25, Lv - float(sl) * 0.25), c="coral", w=5, ar=1, at=0)
        f.line(*pl.P(a + 1.6, Rv + float(sr) * 1.6), *pl.P(a + 0.25, Rv + float(sr) * 0.25), c="coral", w=5, ar=1, at=1)
        S.add(1, q, N(ans), "좌극한 · 우극한은 빈 동그라미 쪽으로 다가가는 높이", lines, f.out(), qfig=True, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        a = R.choice([-3, -2, -1, 1, 2, 3, 4])
        if k < 2:
            m = R.choice([v for v in range(-5, 6) if v not in (-a, 0)])
            num = mulp([1, -a], [1, m])
            if k == 0:
                den = [1, -a]
                val_ = Fr(a + m)
                q = f"{LIM(a)} {{{POLY(num)}/{XM(a)}}}의 값을 구하세요."
                lines = [L(f"{{{POLY(num)}/{XM(a)}}} = {{({XM(a)})({XM(-m)})/{XM(a)}}} = {XM(-m)}", memo="인수분해 → 약분"),
                         L(f"{LIM(a)}({XM(-m)}) = {NP(a)}{TAIL(m)} = {FR(val_)}")]
            else:
                nn = R.choice([v for v in range(-5, 6) if v not in (-a, m, 0)])
                den = mulp([1, -a], [1, nn])
                val_ = Fr(a + m, a + nn)
                q = f"{LIM(a)} {{{POLY(num)}/{POLY(den)}}}의 값을 구하세요."
                lines = [L(f"{{{POLY(num)}/{POLY(den)}}} = {{({XM(a)})({XM(-m)})/({XM(a)})({XM(-nn)})}} = {{{XM(-m)}/{XM(-nn)}}}", memo="인수분해 → 약분"),
                         L(f"{LIM(a)} {{{XM(-m)}/{XM(-nn)}}} = {{{NP(a)}{TAIL(m)}/{NP(a)}{TAIL(nn)}}} = {FR(val_)}")]
            S.add(2, q, FR(val_), "0/0 꼴 — 인수분해해서 약분", lines, None, ident=True, key=q)
        else:
            c = R.choice([1, 2, 3, 4])
            b = c * c - a
            if b < -2:
                return
            val_ = Fr(1, 2 * c)
            q = f"{LIM(a)} {{√{{{XM(-b)}}} − {c}/{XM(a)}}}의 값을 구하세요."
            lines = [L(f"{{√{{{XM(-b)}}} − {c}/{XM(a)}}} = {{({XM(-b)}) − {c * c}/({XM(a)})(√{{{XM(-b)}}} + {c})}} = {{1/√{{{XM(-b)}}} + {c}}}", memo="분자 유리화"),
                     L(f"{LIM(a)} {{1/√{{{XM(-b)}}} + {c}}} = {{1/√{{{c * c}}} + {c}}} = {FR(val_)}")]
            S.add(2, q, FR(val_), "0/0 꼴 — 근호는 유리화", lines, None, ident=True, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        if k == 0:
            a, d = R.choice([1, 2, 3, 4, 6, -2, 5]), R.choice([1, 2, 3, 4])
            b, c, e = R.randint(-5, 5), R.randint(-5, 5), R.randint(-6, 6)
            deg = R.choice([2, 3])
            num = [a, b, c] if deg == 2 else [a, b, 0, c]
            den = [d, 0, e] if deg == 2 else [d, 0, e, 1]
            val_ = Fr(a, d)
            q = f"lim_{{x→∞}} {{{POLY(num)}/{POLY(den)}}}의 값을 구하세요."
            lines = [L(f"분모 · 분자를 {RO('x^{' + str(deg) + '}')} 나누기", memo="∞/∞ 꼴"),
                     L(f"최고차항의 계수의 비 → {FR(val_)}", memo="차수가 같아요 · {1/x} → 0")]
            S.add(3, q, FR(val_), "∞/∞ 꼴 — 최고차항으로 나누기", lines, None, key=q)
        elif k == 1:
            a, d = R.choice([1, 2, 3, 5]), R.choice([1, 2, 3, 4])
            num = [a, R.randint(-5, 5)]
            den = [d, R.randint(-5, 5), R.randint(1, 6)]
            q = f"lim_{{x→∞}} {{{POLY(num)}/{POLY(den)}}}의 값을 구하세요."
            lines = [L("분모 · 분자를 x^{2}으로 나누기", memo="∞/∞ 꼴"),
                     L(f"분자는 0으로, 분모는 {RO(str(d))} 다가가요", memo="분모의 차수가 더 커요"),
                     L("극한값은 0")]
            S.add(3, q, "0", "분모의 차수가 더 크면 0", lines, None, key=q)
        else:
            a = R.choice([2, 4, 6, 8, 3, 5, -2, 10])
            val_ = Fr(a, 2)
            q = f"lim_{{x→∞}}(√{{x^{{2}}{TAIL(a)}x}} − x)의 값을 구하세요."
            lines = [L(f"√{{x^{{2}}{TAIL(a)}x}} − x = {{{N(a)}x/√{{x^{{2}}{TAIL(a)}x}} + x}}", memo="분자 유리화 — ∞ − ∞ 꼴"),
                     L(f"분모 · 분자를 x로 나누면 {{{N(a)}/√{{1 {'+' if a > 0 else MI} {{{abs(a)}/x}}}} + 1}}"),
                     L(f"{{{N(a)}/√{{1}} + 1}} = {FR(val_)}", memo="x → ∞이면 {1/x} → 0")]
            S.add(3, q, FR(val_), "∞ − ∞ 꼴 — 유리화한 뒤 최고차항으로", lines, None, ident=True, key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.choice([-3, -2, -1, 1, 2, 3, 4])
        Lv = R.choice([v for v in range(-6, 9) if v != 0])
        m = Lv - a
        cs = mulp([1, -a], [1, m])
        p_, q_ = int(cs[1]), int(cs[2])
        k = S.count(4) % 2
        ask = "p + q" if k == 0 else "pq"
        ans = p_ + q_ if k == 0 else p_ * q_
        q = f"{LIM(a)} {{x^{{2}} + px + q/{XM(a)}}} = {J(N(Lv), '일', '일')} 때, 상수 p, q에 대하여 {ask}의 값을 구하세요."
        lines = [L(f"x → {N(a)}일 때 분모 → 0이니 분자도 → 0", memo="극한값이 있으려면"),
                 L(f"분자 = ({XM(a)})(x + m)으로 놓으면 {NP(a)} + m = {N(Lv)} → m = {N(m)}"),
                 L(f"({XM(a)})({XM(-m)}) = {POLY(cs)} → p = {N(p_)}, q = {N(q_)}"),
                 L(f"{N(p_)} + {NP(q_)} = {N(ans)}" if k == 0 else f"{N(p_)} × {NP(q_)} = {N(ans)}")]
        S.add(4, q, N(ans), "분모 → 0이면 분자 → 0 — 분자를 (x − a)(x + m)으로", lines, None, sub={"m": m, "p": p_, "q": q_}, ident=True, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        a = R.choice([-2, -1, 1, 2, 3])
        f = Fig()
        if k == 0:
            m2, b2 = R.choice([1, 2, 3, -1, -2]), R.randint(-3, 4)
            right = m2 * a + b2
            c1 = R.choice([1, -1, 2])
            kv = right - c1 * a * a
            q = f"x < {N(a)}일 때 f(x) = {'' if c1 == 1 else (MI if c1 == -1 else N(c1))}x^{{2}} + k, x ≥ {N(a)}일 때 f(x) = {LIN(m2, b2)}인 함수 f(x)가 x = {N(a)}에서 연속일 때, 상수 k의 값을 구하세요."
            lines = [L(f"좌극한 {ATF([c1, 0, 0], a)} + k = {N(c1 * a * a)} + k", memo=f"x → {N(a)}−"),
                     L(f"우극한 = 함숫값 f({N(a)}) = {ATF([m2, b2], a)} = {N(right)}", memo=f"x → {N(a)}+"),
                     L(f"{N(c1 * a * a)} + k = {N(right)} → k = {N(kv)}", memo="좌극한 = 우극한 = 함숫값")]
            pl = plane(f, (a - 4.5, a + 4.5), (min(-2.5, right - 5), max(6.5, right + 4)), step=2)
            pcurve(pl, lambda t: c1 * t * t + kv, [a - 4.5 + 4.5 * i / 40 for i in range(41)], at=2)
            pcurve(pl, lambda t: m2 * t + b2, [a + 4.5 * i / 20 for i in range(21)], at=2)
            pl.pt(a, right, f="coral", at=2, label=f"({N(a)}, {N(right)})", pos="nw" if m2 > 0 else "ne")
            S.add(5, q, N(kv), "연속 ⇔ 좌극한 = 우극한 = 함숫값", lines, f.out(), sub={"k": kv}, key=q)
        else:
            m = R.choice([v for v in range(-4, 6) if v != -a])
            num = mulp([1, -a], [1, m])
            kv = a + m
            q = f"x ≠ {N(a)}일 때 f(x) = {{{POLY(num)}/{XM(a)}}}, f({N(a)}) = k인 함수 f(x)가 x = {N(a)}에서 연속일 때, 상수 k의 값을 구하세요."
            lines = [L(f"{LIM(a)} {{{POLY(num)}/{XM(a)}}} = {LIM(a)}({XM(-m)}) = {N(kv)}", memo="인수분해 → 약분"),
                     L(f"k = f({N(a)}) = {N(kv)}", memo="극한값 = 함숫값")]
            S.add(5, q, N(kv), "연속이면 함숫값 = 극한값", lines, None, sub={"k": kv}, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 부정적분과 정적분 ══════════
def FSTR(cs, var="x"):
    return POLY(cs, var)

def int_():
    S = Set("int", "부정적분과 정적분 — 다항함수", "부정·정적분",
            {1: "부정적분", 2: "조건으로 F(x) 구하기", 3: "정적분 계산", 4: "정적분의 성질", 5: "정적분으로 정의된 함수"},
            pp=8,
            tips={1: "∫x^{n}dx = {1/n + 1}x^{n + 1} + C — 차수를 하나 올리고 그 수로 나눠요",
                  2: "F(x) = ∫f(x)dx + C, 주어진 값으로 C를 정해요",
                  3: "∫_{a}^{b}f(x)dx = [F(x)]_{a}^{b} = F(b) − F(a)",
                  4: "∫_{−a}^{a}에서 홀수 차수 항은 0 · 구간은 이어 붙일 수 있어요",
                  5: "∫_{a}^{x}f(t)dt는 x = a에서 0, 미분하면 f(x) · 정적분은 상수 k로"},
            note="부정적분은 미분의 거꾸로예요. 답을 미분해서 원래 식이 나오는지 늘 확인하게 해 주세요. 정적분은 C가 지워져서 넣지 않아도 돼요.")
    R = rng(2404)

    def rpoly(deg, lead=(1, 2, 3, 4, 6, -3)):
        cs = [R.choice(lead)] + [R.randint(-6, 6) for _ in range(deg)]
        return cs

    def g1():
        deg = R.choice([1, 2, 2, 3])
        cs = [c * (deg + 1 - i) for i, c in enumerate(rpoly(deg, (1, 2, -1, 3)))]
        if S.count(1) % 3 == 2 and deg >= 2:
            p_, q_ = R.randint(-4, 4), R.randint(-4, 4)
            cs = mulp([1, p_], [1, q_])
            shown = f"({XM(-p_)})({XM(-q_)})"
            F = integ(cs)
            q = f"부정적분 ∫{shown}dx를 구하세요."
            lines = [L(f"{shown} = {POLY(cs)}", memo="먼저 전개"),
                     L(f"∫({POLY(cs)})dx = {FSTR(F)} + C", memo="항마다 차수 + 1, 그 수로 나누기")]
        else:
            F = integ(cs)
            q = f"부정적분 ∫({POLY(cs)})dx를 구하세요."
            lines = [L(f"∫({POLY(cs)})dx = {FSTR(F)} + C", memo="항마다 차수 + 1, 그 수로 나누기")]
        X = sp.Symbol("x")
        assert sp.expand(sp.diff(sum(sp.Rational(c.numerator, c.denominator) * X ** (len(F) - 1 - i) for i, c in enumerate(F)), X) - sum(sp.Rational(Fr(c).numerator, Fr(c).denominator) * X ** (len(cs) - 1 - i) for i, c in enumerate(cs))) == 0
        S.add(1, q, f"{FSTR(F)} + C", "∫x^{n}dx = {1/n + 1}x^{n + 1} + C", lines, None, omr="ex", ident=True, key=q)
    fill(S, 1, 20, g1)

    def g2():
        deg = R.choice([1, 2, 2])
        cs = [c * (deg + 1 - i) for i, c in enumerate(rpoly(deg, (1, 2, -1, 3)))]
        F0 = integ(cs)
        a = R.randint(-2, 2)
        C = R.randint(-6, 8)
        v = ev(F0, a) + C
        b = R.choice([u for u in range(-2, 4) if u not in (a, 0)])
        ans = ev(F0, b) + C
        q = f"F'(x) = {POLY(cs)}이고 F({N(a)}) = {J(N(v), '일', '일')} 때, F({N(b)})의 값을 구하세요."
        Fs = FSTR(F0)
        lines = [L(f"F(x) = {Fs} + C", memo="F(x) = ∫F'(x)dx"),
                 L(f"F(0) = C = {N(v)}" if a == 0 else f"F({N(a)}) = {ATF(F0, a)} + C = {N(v)} → C = {N(C)}"),
                 L(f"F({N(b)}) = {ATF(F0, b)}{TAIL(C)} = {N(ans)}")]
        S.add(2, q, N(ans), "부정적분 + C, 주어진 값으로 C", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        deg = R.choice([1, 2, 2, 3])
        cs = [c * (deg + 1 - i) for i, c in enumerate(rpoly(deg, (1, 2, -1, 3, 4)))]
        a, b = sorted(R.sample(range(-2, 4), 2))
        F = integ(cs)
        val_ = ev(F, b) - ev(F, a)
        Fs = FSTR(F)
        q = f"정적분 ∫_{{{N(a)}}}^{{{N(b)}}}({POLY(cs)})dx의 값을 구하세요."
        lines = [L(f"∫_{{{N(a)}}}^{{{N(b)}}}({POLY(cs)})dx = [{Fs}]_{{{N(a)}}}^{{{N(b)}}}", memo="부정적분 하나 — C는 지워져요"),
                 L(f"({ATF(F, b)}) − ({ATF(F, a)}) = {FR(val_)}", memo="F(b) − F(a)")]
        S.add(3, q, FR(val_), "[F(x)]_{a}^{b} = F(b) − F(a)", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        if k == 0:
            a = R.choice([1, 2, 3])
            e2, e0 = R.choice([3, 6, -3, 9]), R.randint(-4, 6)
            o3, o1 = R.choice([1, 2, 4, -1, -4]), R.randint(-5, 5)
            cs = [o3, e2, o1, e0]
            even = [e2, 0, e0]
            Fe = integ(even)
            val_ = 2 * ev(Fe, a)
            q = f"정적분 ∫_{{{MI}{a}}}^{{{a}}}({POLY(cs)})dx의 값을 구하세요."
            lines = [L(f"홀수 차수 항 {POLY([o3, 0, o1, 0])}의 적분은 0", memo=f"∫_{{−a}}^{{a}} — 원점 대칭은 지워져요"),
                     L(f"2∫_{{0}}^{{{a}}}({POLY(even)})dx = 2[{FSTR(Fe)}]_{{0}}^{{{a}}}", memo="y축 대칭은 두 배"),
                     L(f"2 × ({ATF(Fe, a)}) = {FR(val_)}")]
            S.add(4, q, FR(val_), "∫_{−a}^{a} — 짝수 차수만 2∫_{0}^{a}", lines, None, key=q)
        else:
            a, b, c = sorted(R.sample(range(-3, 7), 3))
            I1, I2 = R.randint(-6, 12), R.randint(-6, 12)
            kind = R.choice([0, 1])
            if kind == 0:
                q = f"∫_{{{N(a)}}}^{{{N(b)}}} f(x)dx = {N(I1)}, ∫_{{{N(b)}}}^{{{N(c)}}} f(x)dx = {J(N(I2), '일', '일')} 때, ∫_{{{N(a)}}}^{{{N(c)}}} f(x)dx의 값을 구하세요."
                ans = I1 + I2
                lines = [L(f"∫_{{{N(a)}}}^{{{N(c)}}} = ∫_{{{N(a)}}}^{{{N(b)}}} + ∫_{{{N(b)}}}^{{{N(c)}}}", memo="구간 이어 붙이기"),
                         L(f"{N(I1)} + {NP(I2)} = {N(ans)}")]
            else:
                q = f"∫_{{{N(a)}}}^{{{N(c)}}} f(x)dx = {N(I1)}, ∫_{{{N(b)}}}^{{{N(c)}}} f(x)dx = {J(N(I2), '일', '일')} 때, ∫_{{{N(a)}}}^{{{N(b)}}} f(x)dx의 값을 구하세요."
                ans = I1 - I2
                lines = [L(f"∫_{{{N(a)}}}^{{{N(b)}}} = ∫_{{{N(a)}}}^{{{N(c)}}} − ∫_{{{N(b)}}}^{{{N(c)}}}", memo="구간 이어 붙이기의 거꾸로"),
                         L(f"{N(I1)} − {NP(I2)} = {N(ans)}")]
            S.add(4, q, N(ans), "∫_{a}^{b} + ∫_{b}^{c} = ∫_{a}^{c}", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        if k == 0:
            a = R.choice([1, 2, -1])
            c2 = R.choice([1, 2, -1, 3])
            c1 = R.randint(-4, 4)
            # ∫_a^x f(t)dt = c2 x^3 + c1 x^2 + kx + d — x = a 에서 0, d = 0 으로 두고 k 를 미지수
            kv = Fr(-(c2 * a ** 3 + c1 * a * a), a)
            if kv.denominator != 1:
                return
            kv = int(kv)
            cs = [c2, c1, kv, 0]
            fcs = [3 * c2, 2 * c1, kv]
            cc = R.choice([u for u in range(-2, 4)])
            ans = ev(fcs, cc)
            rhs = POLY([c2, c1, 0, 0]) + " + kx"
            q = f"∫_{{{N(a)}}}^{{x}} f(t)dt = {rhs}일 때, f({N(cc)})의 값을 구하세요. (k는 상수)"
            kt = {1: " + k", -1: f" {MI} k"}.get(a, f" + {N(a)}k" if a > 0 else f" {MI} {abs(a)}k")
            lines = [L(f"x = {J(N(a), '을', '를')} 넣으면 0 = {ATF([c2, c1, 0, 0], a)}{kt} → k = {N(kv)}", memo="∫_{a}^{a} = 0"),
                     L(f"양변을 x에 대하여 미분 → f(x) = {POLY(fcs)}"),
                     L(f"f({N(cc)}) = {ATF(fcs, cc)} = {N(ans)}" if cc else f"f(0) = {N(ans)}")]
            S.add(5, q, N(ans), "x = a를 넣고, 미분해서 f(x)", lines, None, sub={"k": kv}, key=q)
        else:
            b = R.choice([1, 2, 3])
            cs = [R.choice([3, 6, 2, -3]), R.randint(-4, 4)]
            # f(x) = cs[0]x^2 + cs[1]x + k,  k = ∫_0^b f = P + b k → k = P/(1 − b)
            P = ev(integ([cs[0], cs[1], 0]), b)
            if b == 1:
                return
            kv = P / (1 - b)
            if kv.denominator != 1:
                return
            body = POLY([cs[0], cs[1], 0])
            cc = R.choice([-2, -1, 1, 2, 3])
            ans = ev([cs[0], cs[1], kv], cc)
            q = f"f(x) = {body} + ∫_{{0}}^{{{b}}} f(t)dt일 때, f({N(cc)})의 값을 구하세요."
            lines = [L(f"∫_{{0}}^{{{b}}} f(t)dt = k로 놓으면 f(x) = {body} + k", memo="정적분은 상수"),
                     L(f"k = ∫_{{0}}^{{{b}}}({POLY([cs[0], cs[1], 0], 't')} + k)dt = {FR(P)} + {b}k", memo="f(t)를 넣고 적분"),
                     L(f"k = {N(kv)}"),
                     L(f"f({N(cc)}) = {ATF([cs[0], cs[1], 0], cc)} + {NP(kv)} = {N(ans)}")]
            S.add(5, q, N(ans), "정적분을 상수 k로 놓기", lines, None, sub={"k": kv}, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 정적분의 활용 ══════════
def iarea():
    S = Set("iarea", "정적분의 활용 — 넓이 · 속도와 거리", "넓이·속도와 거리",
            {1: "곡선과 x축 사이의 넓이", 2: "부호가 바뀌는 곡선의 넓이", 3: "두 곡선 사이의 넓이", 4: "속도와 위치", 5: "속도와 움직인 거리"},
            mixed=True, pp=6,
            tips={1: "x축 위에 있으면 넓이 = ∫_{a}^{b}f(x)dx",
                  2: "x축 아래 부분은 −를 붙여 더해요 — 넓이 = ∫|f(x)|dx",
                  3: "(위 곡선) − (아래 곡선)을 만나는 점 사이에서 적분",
                  4: "위치 = 처음 위치 + ∫_{0}^{t}v(t)dt",
                  5: "움직인 거리 = ∫|v(t)|dt — 방향이 바뀌는 때에서 나눠요"},
            note="정적분은 ‘부호 있는 넓이’예요. x축 아래는 음수로 계산되니, 넓이와 거리를 구할 때는 그래프부터 그려 부호가 바뀌는 곳을 찾게 해 주세요.")
    R = rng(2405)

    def g1():
        r1 = R.randint(-3, 1)
        r2 = r1 + R.randint(2, 4)
        lead = R.choice([1, 1, 2, 3])
        cs = [-lead * c for c in mulp([1, -r1], [1, -r2])]
        F = integ(cs)
        val_ = ev(F, r2) - ev(F, r1)
        assert val_ == Fr(lead * (r2 - r1) ** 3, 6)
        f = Fig()
        top = max(ev(cs, Fr(r1 + r2, 2)), 1)
        pl = plane(f, (min(r1 - 1.5, -1.5), max(r2 + 1.5, 1.5)), (-2.5, float(top) + 1.5), square=False)
        fn = lambda t: float(ev(cs, t))
        pl.curve(fn, n=60)
        shade(pl, fn, r1, r2, at=0)
        q = f"곡선 y = {wa(POLY(cs))} x축으로 둘러싸인 부분의 넓이를 구하세요."
        lines = [L(f"{POLY(cs)} = 0 → x = {N(r1)}, {N(r2)}", memo="x축과 만나는 점"),
                 L(f"넓이 = ∫_{{{N(r1)}}}^{{{N(r2)}}}({POLY(cs)})dx", memo="x축 위"),
                 L(f"[{FSTR(F)}]_{{{N(r1)}}}^{{{N(r2)}}} = {FR(ev(F, r2))} − {NP(ev(F, r1))} = {FR(val_)}", memo=f"F({N(r2)}) − F({N(r1)})")]
        S.add(1, q, FR(val_), "x축 위 부분의 넓이 = ∫_{a}^{b}f(x)dx", lines, f.out(), qfig=False, key=q)
    fill(S, 1, 20, g1)

    def g2():
        s0 = R.randint(-2, 1)
        c = R.randint(1, 3)
        b = c + R.randint(1, 2)
        lead, sg = R.choice([1, 2, 3]), R.choice([1, -1])
        cs = [sg * lead * v for v in mulp([1, -s0], [1, -(s0 + c)])]
        F = integ(cs)
        x1, x2 = s0 + c, s0 + b
        A1 = abs(ev(F, x1) - ev(F, s0))
        A2 = abs(ev(F, x2) - ev(F, x1))
        f = Fig()
        fn = lambda t: float(ev(cs, t))
        ys = [fn(s0 + (b) * i / 20) for i in range(21)]
        lo, hi = min(min(ys), -1), max(max(ys), 1)
        pl = plane(f, (min(s0 - 1.5, -1.5), max(x2 + 1.5, 1.5)), (lo - 1.5, hi + 1.5), square=False)
        pl.curve(fn, s0 - 1.0, x2 + 0.8, n=60)
        shade(pl, fn, s0, x1, at=0, c="coral", fo=0.25)
        shade(pl, fn, x1, x2, at=0, c="teal", fo=0.28)
        f.line(*pl.P(x2, 0), *pl.P(x2, fn(x2)), c="soft", w=2, d=True)
        P = POLY(cs)
        q = f"곡선 y = {wa(P)} x축 및 직선 {RO(f'x = {N(x2)}')} 둘러싸인 두 부분의 넓이의 합을 구하세요."
        up = "≥" if sg < 0 else "≤"
        dn = "≤" if sg < 0 else "≥"
        I1, I2 = ev(F, x1) - ev(F, s0), ev(F, x2) - ev(F, x1)
        lines = [L(f"{N(s0)} ≤ x ≤ {N(x1)}에서 y {up} 0, {N(x1)} ≤ x ≤ {N(x2)}에서 y {dn} 0", memo="부호가 바뀌는 곳"),
                 L(f"∫_{{{N(s0)}}}^{{{N(x1)}}}y dx = {FR(I1)}, ∫_{{{N(x1)}}}^{{{N(x2)}}}y dx = {FR(I2)}", memo=f"F(x) = {FSTR(F)}"),
                 L(f"넓이 = {FR(A1)} + {FR(A2)} = {FR(A1 + A2)}", memo="x축 아래쪽은 부호를 바꿔 더하기")]
        S.add(2, q, FR(A1 + A2), "x축 아래 부분은 −∫로 바꿔 더하기", lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        al = R.randint(-3, 1)
        be = al + R.randint(2, 4)
        lead = R.choice([1, 1, 2])
        # 아래 y = lead x^2 + c0, 위 y = m x + n 이 x = al, be 에서 만나도록
        c0 = R.randint(-3, 2)
        m = lead * (al + be)
        n = -lead * al * be + c0
        low = [lead, 0, c0]
        up = [m, n]
        diff = [-lead, m, n - c0]
        F = integ(diff)
        val_ = ev(F, be) - ev(F, al)
        assert val_ == Fr(lead * (be - al) ** 3, 6)
        f = Fig()
        fl = lambda t: float(ev(low, t))
        fu = lambda t: float(ev(up, t))
        ys = [fl(al), fl(be), fu(al), fu(be), c0]
        pl = plane(f, (min(al - 1.5, -1.5), max(be + 1.5, 1.5)), (min(min(ys) - 1.5, -1.5), max(max(ys) + 1.5, 1.5)), square=False)
        pl.curve(fl, n=70)
        pl.lineq(m, n, c="coral")
        shade(pl, fu, al, be, at=1, base=fl)
        q = f"곡선 y = {wa(POLY(low))} 직선 y = {RO(LIN(m, n))} 둘러싸인 부분의 넓이를 구하세요."
        lines = [L(f"{POLY(low)} = {LIN(m, n)} → x = {N(al)}, {N(be)}", memo="만나는 점"),
                 L(f"넓이 = ∫_{{{N(al)}}}^{{{N(be)}}}({POLY(diff)})dx", memo="(위) − (아래)"),
                 L(f"[{FSTR(F)}]_{{{N(al)}}}^{{{N(be)}}} = {FR(ev(F, be))} − {NP(ev(F, al))} = {FR(val_)}", memo=f"F({N(be)}) − F({N(al)})")]
        S.add(3, q, FR(val_), "(위 곡선 − 아래 곡선)을 만나는 점 사이에서 적분", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        T = R.randint(2, 5)
        x0 = R.randint(-5, 5)
        if k == 0:
            a, b = R.choice([2, 4, 6, -2, -4]), R.randint(-6, 8)
            vcs = [a, b]
        else:
            vcs = [R.choice([3, 6, -3]), R.choice([2, 4, -2, 0]), R.randint(-4, 4)]
        V = integ(vcs)
        dx = ev(V, T)
        ans = x0 + dx
        q = f"시각 t = 0일 때 위치가 {N(x0)}인 점 P가 수직선 위를 움직여요. 시각 t에서의 속도가 v(t) = {POLY(vcs, 't')}일 때, t = {T}에서 점 P의 위치를 구하세요."
        lines = [L(f"(위치) = {N(x0)} + ∫_{{0}}^{{{T}}}({POLY(vcs, 't')})dt", memo="처음 위치 + 위치의 변화량"),
                 L(f"{N(x0)} + [{FSTR(V, 't')}]_{{0}}^{{{T}}} = {N(x0)} + ({ATF(V, T)}) = {FR(ans)}")]
        S.add(4, q, FR(ans), "위치 = 처음 위치 + ∫v(t)dt", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        r = R.randint(1, 3)
        T = r + R.randint(1, 3)
        a = R.choice([1, 2, 3, 4])
        sg = R.choice([1, -1])
        vcs = [-sg * a, sg * a * r]            # v = sg·a(r − t)
        V = integ(vcs)
        D1 = abs(ev(V, r) - ev(V, 0))
        D2 = abs(ev(V, T) - ev(V, r))
        D = D1 + D2
        disp = ev(V, T)
        k = S.count(5) % 2
        f = Fig()
        fn = lambda tt: float(ev(vcs, tt))
        vmax = max(abs(fn(0)), abs(fn(T)), 1)
        pl = plane(f, (-0.8, T + 1.2), (-vmax - 1.5, vmax + 1.5), xn="t", yn="v", square=False)
        pl.curve(fn, 0, T, n=10)
        shade(pl, fn, 0, r, at=1, c="teal")
        shade(pl, fn, r, T, at=1, c="coral", fo=0.25)
        if k == 0:
            q = f"수직선 위를 움직이는 점 P의 시각 t에서의 속도가 v(t) = {POLY(vcs, 't')}일 때, t = 0부터 t = {T}까지 점 P가 움직인 거리를 구하세요."
            lines = [L(f"v(t) = 0 → t = {r}", memo="움직이는 방향이 바뀌는 때"),
                     L(f"거리 = ∫_{{0}}^{{{r}}}|v(t)|dt + ∫_{{{r}}}^{{{T}}}|v(t)|dt", memo="넓이를 더해요"),
                     L(f"{FR(D1)} + {FR(D2)} = {FR(D)}")]
            S.add(5, q, FR(D), "움직인 거리 = ∫|v(t)|dt", lines, f.out(), sub={"t": r}, key=q)
        else:
            q = f"수직선 위를 움직이는 점 P의 시각 t에서의 속도가 v(t) = {POLY(vcs, 't')}일 때, t = 0부터 t = {T}까지 점 P의 위치의 변화량과 움직인 거리의 합을 구하세요."
            lines = [L(f"변화량 ∫_{{0}}^{{{T}}}({POLY(vcs, 't')})dt = {FR(disp)}", memo="부호 그대로"),
                     L(f"거리 {FR(D1)} + {FR(D2)} = {FR(D)}", memo=f"t = {r}에서 방향이 바뀌어요"),
                     L(f"{FR(disp)} + {FR(D)} = {FR(disp + D)}")]
            S.add(5, q, FR(disp + D), "변화량은 ∫v(t)dt, 거리는 ∫|v(t)|dt", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S
