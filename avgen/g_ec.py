# 초등 ③ — 소수(자릿값 · 덧셈 뺄셈 · 곱셈 · 나눗셈) · 분수와 소수 · 삼각형과 사각형 · 원
import math
from math import gcd
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, fbar, ffill, ang_pt, angle_mark, dir_deg, NL
from kit import *

def F_(n, d):
    return "{%d/%d}" % (n, d)

def D(v):
    return DEC(Fr(v))

def dp(v):
    v = Fr(v)
    for k in range(8):
        if (v * 10 ** k).denominator == 1:
            return k
    raise ValueError

def DK(v, k):
    """소수 k 자리로 — 끝 0도 그대로 (3.6, 2 → '3.60')"""
    v = Fr(v)
    n = int(v * 10 ** k)
    s = str(n).rjust(k + 1, "0")
    return s[:-k] + "." + s[-k:] if k else s

def bat(x):
    from core import _has_batchim
    return _has_batchim(str(x))

ORD = ["첫째", "둘째", "셋째", "넷째"]

def nm_dec(k):
    def nm(p):
        if p < k:
            return f"소수 {ORD[k - 1 - p]} 자리"
        return f"{NAME[p - k]}의 자리"
    return nm

def dec_col(a, b, op):
    """소수 세로셈 — 소수점을 맞추고(빈자리 0) 자연수처럼 계산 · 소수점은 그대로 내려 찍기"""
    a, b = Fr(a), Fr(b)
    k = max(dp(a), dp(b), 1)
    A, B = int(a * 10 ** k), int(b * 10 ** k)
    res = A + B if op == "+" else A - B
    ncol = max(len(str(A)), len(str(B)), len(str(res)), k + 1)
    show = (D(a), D(b), D(a + b if op == "+" else a - b))
    heads = tuple([f"소수 {ORD[k - 1 - p]}" for p in range(k)] + [NAME[p] for p in range(ncol - k)])
    if op == "+":
        f, body, _ = col_add(A, B, nm=nm_dec(k), ncol=ncol, show=show, heads=heads)
    else:
        f, body, _ = col_sub(A, B, nm=nm_dec(k), ncol=ncol, show=show, heads=heads)
    pre = []
    if dp(a) < k or dp(b) < k:
        pre.append(L(f"{D(a)} = {DK(a, k)}" if dp(a) < k else f"{D(b)} = {DK(b, k)}", memo="소수점을 맞추고 빈자리에 0"))
    # 그림: 소수점 · 앞자리 0 · 덧붙인 0
    els = f["els"]
    for el in els:
        if isinstance(el.get("at"), int):
            el["at"] += len(pre)
    nl = len(pre) + len(body)
    cx = 400 if ncol <= 4 else 372
    dx = 118 if ncol <= 4 else 106
    X = lambda p: cx - p * dx + dx * (ncol - 1) / 2
    xp = (X(k) + X(k - 1)) / 2
    for y, at in ((270, "q"), (375, "q"), (500, nl - 1)):
        els.append({"k": "T", "s": ".", "x": round(xp, 1), "y": y, "z": 66, "at": at} if at != "q" else {"k": "T", "s": ".", "x": round(xp, 1), "y": y, "z": 66})
    for row, v, y in (("a", A, 270), ("b", B, 375)):
        if len(str(v)) < k + 1:
            for p in range(len(str(v)), k + 1):
                els.append({"k": "T", "s": "0", "x": round(X(p), 1), "y": y, "z": 66, "c": "soft"})
    for v, y, src in ((a, 270, A), (b, 375, B)):
        for p in range(k - dp(v)):
            els.append({"k": "T", "s": "0", "x": round(X(p), 1), "y": y - 0, "z": 66, "c": "coral", "at": 0})
    if len(str(res)) < k + 1:
        for p in range(len(str(res)), k + 1):
            els.append({"k": "T", "s": "0", "x": round(X(p), 1), "y": 500, "z": 66, "at": nl - 1})
    return f, pre + body


def dnl(f, lo, hi, minor, every, y=360, x0=60, x1=600, at="q", z=24):
    """소수 수직선 — lo, hi, minor: Fraction · every: 몇 눈금마다 글자"""
    lo, hi, minor = Fr(lo), Fr(hi), Fr(minor)
    X = lambda v: x0 + (x1 - x0) * float((Fr(v) - lo) / (hi - lo))
    f.line(x0 - 14, y, x1 + 20, y, c="ink", w=3, ar=1, at=at)
    n = int((hi - lo) / minor)
    for i in range(n + 1):
        v = lo + minor * i
        big = i % every == 0
        f.line(X(v), y - (13 if big else 7), X(v), y + (13 if big else 7), c="ink", w=3 if big else 1.6, at=at)
        if big:
            f.text(X(v), y + 44, D(v), z=z, c="soft", at=at)
    return X

def dpt(f, X, v, lab, y=360, at=0, col="gold", up=True):
    f.dot(X(v), y, r=10, f=col, at=at)
    f.text(X(v), y - 30 if up else y + 84, lab, z=30, c=col, at=at, b=700)

def div_points(f, N_, k, q_lt1=False):
    """long_div 그림에 소수점(나누어지는 수 · 몫) 찍기"""
    nd, dx = len(str(N_)), 70
    xd0 = 330 - dx * (nd - 1) / 2 + 40
    X = lambda i: xd0 + i * dx
    xp = X(nd - k - 1) + dx / 2
    f.text(xp, 232, ".", z=48, c="coral", b=700)
    f.text(xp, 150, ".", z=48, c="coral", b=700, at=0)
    if q_lt1:
        f.text(X(nd - k - 1), 150, "0", z=48, c="coral", b=700, at=0)


# ══════════ 소수의 자릿값 ══════════
def dec_table(f, s, hl=None, at="q", hl_at=0, y=220):
    """소수 자리 표 — s: '4.385' · hl: 빛낼 글자 자리(문자열 안 번호)"""
    ip, fp = s.split(".") if "." in s else (s, "")
    heads = [PL[len(ip) - 1 - i] for i in range(len(ip))] + [f"소수 {ORD[i]}" for i in range(len(fp))]
    cells = list(ip) + list(fp)
    n = len(cells)
    cw = min(120, 600 / n)
    x0 = 330 - cw * n / 2
    f.grid(x0, y, cw, 64, n, 1, at=at, c="soft", sw=2)
    f.grid(x0, y + 64, cw, 100, n, 1, at=at, c="ink", sw=3)
    for i in range(n):
        cx = x0 + cw * i + cw / 2
        f.text(cx, y + 42, heads[i], z=20 if len(heads[i]) > 3 else 24, c="soft", at=at)
        f.text(cx, y + 64 + 72, cells[i], z=56, at=at, b=700)
    xp = x0 + cw * len(ip)
    f.dot(xp, y + 64 + 72, r=7, f="coral", at=at)
    if hl is not None:
        i = hl if hl < len(ip) else hl
        f.rect(x0 + cw * i + 3, y + 3, cw - 6, 158, c="gold", sw=5, rx=8, at=hl_at)
    return x0, cw

def dec():
    S = Set("dec", "소수 — 0.1, 0.01, 0.001의 자릿값", "소수의 자릿값",
            {1: "소수 한 자리", 2: "소수 두 자리", 3: "소수 세 자리 · 자릿값", 4: "소수의 크기 비교", 5: "10배 · 100배 · {1/10} · {1/100}"},
            pp=10,
            tips={1: "{1/10} = 0.1 — 0.1이 7개면 0.7, 1이 2개 · 0.1이 5개면 2.5",
                  2: "{1/100} = 0.01 — 0.01이 37개면 0.37",
                  3: "소수점 아래 첫째 · 둘째 · 셋째 자리 — 4.385의 8은 0.08",
                  4: "자연수 부분부터, 같으면 소수 첫째 자리 · 둘째 자리 차례로 비교. 0.7 = 0.70",
                  5: "10배 하면 소수점이 오른쪽으로 한 칸, {1/10}이면 왼쪽으로 한 칸"},
            note="소수는 ‘0.1이 몇 개’로 세는 수예요. 자리 표에 숫자를 넣어 보게 하면 0.7과 0.65 같은 비교에서 자릿수가 많은 쪽이 크다는 오해를 바로잡을 수 있어요.")
    R = rng(331)

    def g1():
        k = S.count(1) % 3
        f = Fig()
        if k == 0:
            n = R.randint(1, 9)
            q = f"0.1이 {n}개인 수는 얼마인가요?"
            fbar(f, 50, 260, 560, 80, 10)
            ffill(f, 50, 260, 560, 80, 10, 0, n, "gold", 0)
            f.text(50, 236, "0", z=26, c="soft"); f.text(610, 236, "1", z=26, c="soft")
            lines = [L(f"0.1 × {n} = {D(Fr(n, 10))}", memo="0.1이 몇 개"), L(f"{D(Fr(n, 10))}")]
            ans = D(Fr(n, 10))
        elif k == 1:
            w, n = R.randint(1, 9), R.randint(1, 9)
            v = w + Fr(n, 10)
            q = f"1이 {w}개, 0.1이 {n}개인 수는 얼마인가요?"
            dec_table(f, D(v), at=1)
            lines = [L(f"{w} + {D(Fr(n, 10))} = {D(v)}", memo="자연수 부분 + 소수 부분"), L(f"{D(v)}")]
            ans = D(v)
        else:
            n = R.randint(11, 59)
            if n % 10 == 0:
                return
            q = f"0.1이 {n}개인 수는 얼마인가요?"
            X = dnl(f, 0, n // 10 + 1, Fr(1, 10), 10, y=330)
            dpt(f, X, Fr(n, 10), D(Fr(n, 10)), y=330, at=1)
            lines = [L(f"0.1이 10개 → 1", memo="10개씩 묶기"), L(f"0.1 × {n} = {D(Fr(n, 10))}", memo=f"1이 {n // 10}개, 0.1이 {n % 10}개"), L(f"{D(Fr(n, 10))}")]
            ans = D(Fr(n, 10))
        S.add(1, q, ans, "0.1이 10개면 1 — 0.1이 몇 개인지 세요", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        f = Fig()
        if k == 0:
            n = R.randint(11, 99)
            if n % 10 == 0:
                return
            q = f"0.01이 {n}개인 수는 얼마인가요?"
            f.grid(130, 130, 40, 40, 10, 10, c="soft", sw=1.5)
            for i in range(n):
                r_, c_ = divmod(i, 10)
                f.rect(130 + c_ * 40 + 2, 130 + r_ * 40 + 2, 36, 36, c="none", f="gold", fo=0.5, at=0, dl=(i // 10) * 120)
            lines = [L(f"0.01 × {n} = {D(Fr(n, 100))}", memo="0.01이 몇 개"), L(f"0.1이 {n // 10}개, 0.01이 {n % 10}개"), L(f"{D(Fr(n, 100))}")]
            ans = D(Fr(n, 100))
        elif k == 1:
            w, a, b = R.randint(1, 9), R.randint(0, 9), R.randint(1, 9)
            v = w + Fr(a, 10) + Fr(b, 100)
            q = f"1이 {w}개, 0.1이 {a}개, 0.01이 {b}개인 수는 얼마인가요?"
            dec_table(f, D(v), at=1)
            lines = [L(f"{w} + {D(Fr(a, 10)) if a else 0} + {D(Fr(b, 100))} = {D(v)}", memo="자리마다 모아요"), L(f"{D(v)}")]
            ans = D(v)
        else:
            n = R.randint(101, 999)
            if n % 10 == 0:
                return
            q = f"{J(F_(n, 100), '을', '를')} 소수로 나타내세요."
            dec_table(f, D(Fr(n, 100)), at=1)
            lines = [L(f"{F_(1, 100)} = 0.01", memo="분모 100 → 소수 두 자리"), L(f"{F_(n, 100)} = {D(Fr(n, 100))}", memo="0.01이 몇 개"), L(f"{D(Fr(n, 100))}")]
            ans = D(Fr(n, 100))
        S.add(2, q, ans, "0.01이 몇 개인지 — 소수 둘째 자리까지", lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        s = f"{R.randint(1, 99)}.{R.randint(100, 999)}"
        if s.endswith("0") or len(set(s.replace(".", ""))) < len(s) - 1:
            return
        f = Fig()
        if k == 0:
            ip, fp = s.split(".")
            j = R.randint(0, 2)
            dgt = fp[j]
            if s.count(dgt) > 1:
                return
            v = Fr(int(dgt), 10 ** (j + 1))
            dec_table(f, s, hl=len(ip) + j, hl_at=0)
            q = f"{s}에서 숫자 {iga(dgt)} 나타내는 수는 얼마인가요?"
            lines = [L(f"{dgt}{'은' if bat(dgt) else '는'} 소수 {ORD[j]} 자리 숫자", memo="소수점 아래 몇째?"), L(f"{dgt} × {D(Fr(1, 10 ** (j + 1)))} = {D(v)}"), L(f"{D(v)}")]
            ans = D(v)
        else:
            v = Fr(s)
            ip, fp = s.split(".")
            q = f"{s}{'은' if bat(fp[-1]) else '는'} 0.001이 몇 개인 수인가요?"
            dec_table(f, s, at="q")
            lines = [L(f"0.001이 1000개 → 1", memo="1 = 0.001 × 1000"), L(f"{s} × 1000 = {int(v * 1000)}", memo="소수점을 오른쪽으로 세 칸"), L(f"{int(v * 1000)}개")]
            ans = f"{int(v * 1000)}개"
            S.add(3, q, ans, "0.001이 몇 개 — 소수점을 오른쪽으로 세 칸", lines, f.out(), ap=str(int(v * 1000)), key=q)
            return
        S.add(3, q, ans, "자리 표에 넣어 몇째 자리인지 찾아요", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        if k == 0:
            a = Fr(R.randint(1, 9), 10)
            b = a - Fr(1, 10) + Fr(R.randint(1, 9), 100)
        else:
            w = R.randint(0, 5)
            a = w + Fr(R.randint(10, 99), 100)
            b = w + Fr(R.randint(100, 999), 1000)
            if abs(a - b) > Fr(1, 10):
                return
        if a == b:
            return
        x, y = (a, b) if R.random() < 0.5 else (b, a)
        big = max(a, b)
        k2 = max(dp(a), dp(b))
        q = f"{wa(D(x))} {D(y)} 중에서 더 큰 수는 무엇인가요?"
        sx, sy = DK(x, k2), DK(y, k2)
        j = next(i for i in range(len(sx)) if sx[i] != sy[i])
        ip_len = sx.index(".")
        place = PL[ip_len - 1 - j] + "의 자리" if j < ip_len else f"소수 {ORD[j - ip_len - 1]} 자리"
        f = Fig()
        lo = Fr(math.floor(min(a, b) * 10), 10)
        hi = lo + Fr(1, 10) if max(a, b) <= lo + Fr(1, 10) else Fr(math.ceil(max(a, b) * 10), 10)
        X = dnl(f, lo, hi, Fr(1, 100), 10)
        lines = [L(f"{D(x)} = {sx}, {D(y)} = {sy}" if (sx != D(x) or sy != D(y)) else f"자릿수 맞추기: {sx}, {sy}", memo="끝에 0을 붙여 자릿수를 맞춰요"),
                 L(f"{place}: {sx[j]}, {sy[j]}", memo="처음으로 다른 자리"), L(f"{D(big)}{'이' if bat(D(big)) else '가'} 더 커요")]
        dpt(f, X, x, D(x), at=0, col="gold", up=True)
        dpt(f, X, y, D(y), at=0, col="teal", up=False)
        S.add(4, q, D(big), "자릿수를 맞추고 높은 자리부터 비교해요", lines, f.out(), key=f"{min(a, b)}|{max(a, b)}")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        v = Fr(R.randint(11, 9999), R.choice([10, 100, 1000]))
        if v.denominator == 1 or v > 100:
            return
        m, word = [(10, "10배"), (100, "100배"), (Fr(1, 10), F_(1, 10)), (Fr(1, 100), F_(1, 100))][k]
        r = v * m
        if dp(r) > 3 or r < Fr(1, 1000):
            return
        q = f"{D(v)}의 {word}{'는' if k < 2 else '은'} 얼마인가요?"
        sh = {0: 1, 1: 2, 2: -1, 3: -2}[k]
        f = Fig()
        dec_table(f, D(v), y=120, at="q")
        dec_table(f, D(r), y=380, at=1)
        lines = [L(f"{word} → 소수점이 {'오른쪽' if sh > 0 else '왼쪽'}으로 {abs(sh)}칸", memo="숫자는 그대로, 자리만 옮겨요"),
                 L(f"{D(v)} × {D(m) if k < 2 else F_(1, 10 ** abs(sh))} = {D(r)}")]
        S.add(5, q, D(r), f"{word} 하면 소수점이 {'오른쪽' if sh > 0 else '왼쪽'}으로 {abs(sh)}칸", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 소수의 덧셈 · 뺄셈 ══════════
def dadd():
    S = Set("dadd", "소수의 덧셈 · 뺄셈 — 소수점을 맞추어", "소수 덧셈·뺄셈",
            {1: "소수 한 자리 덧셈", 2: "소수 두 자리 덧셈", 3: "자릿수가 다른 덧셈", 4: "소수의 뺄셈", 5: "자릿수가 다른 뺄셈"},
            pp=10,
            tips={1: "소수점을 맞추어 쓰고 자연수처럼 더한 뒤, 소수점을 그대로 내려 찍어요",
                  2: "소수 둘째 자리부터 — 받아올림은 자연수와 같아요",
                  3: "자릿수가 다르면 끝에 0을 붙여 맞춰요. 3.6 + 1.25 → 3.60 + 1.25",
                  4: "소수 둘째 자리부터 빼고, 못 빼면 윗자리에서 10을 빌려요",
                  5: "4 − 1.38 → 4.00 − 1.38 — 0을 붙이면 받아내림이 보여요"},
            note="소수의 덧셈 · 뺄셈은 ‘소수점 맞추기’가 전부예요. 끝자리를 맞추는 실수(3.6 + 1.25를 오른쪽 끝에 맞추기)가 가장 흔하니 0을 붙여 자릿수를 맞추게 해 주세요.")
    R = rng(332)

    def put(st, a, b, op, plan):
        f, lines = dec_col(a, b, op)
        r = a + b if op == "+" else a - b
        q = R.choice([f"{D(a)} {op} {J(D(b), '은', '는')} 얼마인가요?", f"{D(a)} {op} {eul(D(b))} 계산하세요."])
        return S.add(st, q, D(r), plan, lines, f, key=f"{a}{op}{b}")

    def g1():
        a, b = Fr(R.randint(3, 89), 10), Fr(R.randint(3, 89), 10)
        if a.denominator == 1 or b.denominator == 1 or (a * 10 % 10 + b * 10 % 10) < 10:
            return
        put(1, a, b, "+", "소수점을 맞추고 자연수처럼 — 0.1이 10개면 1")
    fill(S, 1, 20, g1)

    def g2():
        a, b = Fr(R.randint(101, 899), 100), Fr(R.randint(101, 899), 100)
        if dp(a) != 2 or dp(b) != 2:
            return
        put(2, a, b, "+", "소수 둘째 자리부터 — 받아올림은 자연수처럼")
    fill(S, 2, 20, g2)

    def g3():
        if S.count(3) % 2:
            a, b = Fr(R.randint(11, 99), 10), Fr(R.randint(101, 999), 100)
        else:
            a, b = Fr(R.randint(101, 999), 100), Fr(R.randint(11, 99), 10)
        if dp(a) == dp(b) or 0 in (dp(a), dp(b)):
            return
        put(3, a, b, "+", "끝에 0을 붙여 자릿수를 맞추고 더해요")
    fill(S, 3, 20, g3)

    def g4():
        a = Fr(R.randint(210, 980), 100); b = Fr(R.randint(105, int(a * 100) - 20), 100)
        if dp(a) != 2 or dp(b) != 2 or borrow_info(int(a * 100), int(b * 100))[0] < 1:
            return
        put(4, a, b, "−", "소수 둘째 자리부터 — 못 빼면 윗자리에서 빌려요")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            a = Fr(R.randint(2, 9)); b = Fr(R.randint(101, int(a * 100) - 30), 100)
        elif k == 1:
            a = Fr(R.randint(21, 98), 10); b = Fr(R.randint(101, int(a * 100) - 20), 100)
        else:
            a = Fr(R.randint(101, 989), 100)
        if int(a * 10) - 2 < 11:
            return
        b = Fr(R.randint(11, int(a * 10) - 2), 10)
        if a <= b or dp(b) == 0 or dp(a) == dp(b) and k < 2:
            return
        put(5, a, b, "−", "0을 붙여 자릿수를 맞추고 빼요 — 받아내림 주의")
    fill(S, 5, 20, g5)
    return S


# ══════════ 소수의 곱셈 ══════════
def point_fig(a, b, ia, ib, p, k, at_mul=0, at_pt=1):
    """소수점 떼고 곱하기 → 소수점 아래 자리 수만큼 왼쪽으로"""
    f = Fig()
    f.text(330, 170, f"{D(a)} × {D(b)}", z=54, b=700)
    f.text(330, 300, f"{ia} × {ib} = {p}", z=46, at=at_mul)
    f.line(330, 190, 330, 250, c="teal", w=3, ar=1, at=at_mul)
    s = str(p).rjust(k + 1, "0")
    shown = s[:-k] + "." + s[-k:] if k else s
    f.text(330, 470, shown, z=64, b=700, at=at_pt, c="coral")
    f.text(330, 560, f"소수점 아래 {k}자리", z=28, c="soft", at=at_pt)
    return f

def dmul():
    S = Set("dmul", "소수의 곱셈 — 자연수처럼 곱하고 소수점 자리 세기", "소수의 곱셈",
            {1: "(소수) × (자연수)", 2: "(자연수) × (소수)", 3: "(소수) × (소수)", 4: "자릿수가 많은 소수의 곱셈", 5: "곱의 소수점 위치"},
            pp=10,
            tips={1: "0.6 × 4 → 0.1이 6 × 4 = 24개 → 2.4",
                  2: "3 × 0.27 → 3 × 27 = 81 → 0.01이 81개 → 0.81",
                  3: "0.3 × 0.7 → 3 × 7 = 21 → 소수점 아래 1 + 1 = 2자리 → 0.21",
                  4: "자연수처럼 곱한 뒤, 두 수의 소수점 아래 자리 수를 더한 만큼 왼쪽에서 소수점",
                  5: "× 10 · × 100이면 소수점이 오른쪽으로, × 0.1 · × 0.01이면 왼쪽으로 옮겨요"},
            note="소수의 곱셈은 ‘자연수처럼 곱하기’와 ‘소수점 아래 자리 수 더하기’로 나누어 생각하게 해 주세요. 어림(2.35 × 1.4 ≈ 2 × 1.5)으로 소수점 위치를 확인하는 습관도 좋아요.")
    R = rng(333)

    def put(st, a, b, plan, fig=None):
        ka, kb = dp(a), dp(b)
        ia, ib = int(a * 10 ** ka), int(b * 10 ** kb)
        p = ia * ib
        k = ka + kb
        r = a * b
        lines = [L(f"{ia} × {ib} = {p}", memo="소수점을 떼고 자연수처럼"), L(f"{ka} + {kb} = {k}", pre="소수점 아래 자리 수", memo="두 수의 자리 수를 더해요"),
                 L(f"{D(a)} × {D(b)} = {D(r)}", memo=("끝의 0은 지워요" if p % 10 == 0 and k else None))]
        f = fig or point_fig(a, b, ia, ib, p, k)
        q = R.choice([f"{D(a)} × {J(D(b), '은', '는')} 얼마인가요?", f"{D(a)} × {eul(D(b))} 계산하세요."])
        return S.add(st, q, D(r), plan, lines, f.out(), key=f"{a}x{b}")

    def g1():
        a = Fr(R.randint(2, 99), 10) if S.count(1) % 2 else Fr(R.randint(11, 99), 100)
        b = Fr(R.randint(2, 9)) if S.count(1) < 12 else Fr(R.randint(11, 25))
        if dp(a) == 0:
            return
        put(1, a, b, "자연수처럼 곱하고 — 0.1(0.01)이 몇 개인지로")
    fill(S, 1, 20, g1)

    def g2():
        a = Fr(R.randint(2, 9)) if S.count(2) < 12 else Fr(R.randint(11, 40))
        b = Fr(R.randint(2, 99), 10) if S.count(2) % 2 else Fr(R.randint(11, 99), 100)
        if dp(b) == 0:
            return
        put(2, a, b, "자연수 × 자연수로 곱하고 — 소수점 아래 자리 수만큼")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3)
        if k < 8:
            x, y = R.randint(1, 9), R.randint(1, 9)
            a, b = Fr(x, 10), Fr(y, 10)
            f = Fig()
            X0, Y0, W = 140, 110, 400
            f.grid(X0, Y0, W / 10, W / 10, 10, 10, c="soft", sw=1.2)
            f.rect(X0, Y0, W, W, c="ink", sw=3)
            f.rect(X0 + 2, Y0 + 2, W * x / 10 - 4, W - 4, c="none", f="gold", fo=0.3)
            f.rect(X0 + 2, Y0 + 2, W - 4, W * y / 10 - 4, c="none", f="teal", fo=0.3, at=0)
            f.rect(X0, Y0, W * x / 10, W * y / 10, c="coral", sw=5, at=1)
            f.text(330, 600, f"100칸 중 {x * y}칸 = {D(a * b)}", z=30, c="coral", b=700, at=2)
            put(3, a, b, "0.1 × 0.1 = 0.01 — 넓이 그림에서 겹친 칸", fig=f)
        else:
            a, b = Fr(R.randint(11, 99), 10), Fr(R.randint(2, 99), 10)
            if dp(a) == 0 or dp(b) == 0:
                return
            put(3, a, b, "자연수처럼 곱하고 — 소수점 아래 1 + 1 = 2자리")
    fill(S, 3, 20, g3)

    def g4():
        a, b = Fr(R.randint(101, 999), 100), Fr(R.randint(11, 99), 10)
        if dp(a) != 2 or dp(b) != 1:
            return
        if S.count(4) % 2:
            a, b = b, a
        put(4, a, b, "자연수처럼 곱하고 — 소수점 아래 2 + 1 = 3자리(끝의 0은 지우기)")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        v = Fr(R.randint(11, 9999), R.choice([10, 100]))
        if v.denominator == 1:
            return
        m = [Fr(10), Fr(100), Fr(1, 10), Fr(1, 100)][k] if R.random() < 0.6 else [Fr(1000), Fr(1, 1000)][k % 2]
        r = v * m
        if dp(r) > 3 or len(D(r).replace(".", "")) > 7:
            return
        sh = round(math.log10(m))
        q = f"{D(v)} × {J(D(m), '은', '는')} 얼마인가요?"
        f = Fig()
        dec_table(f, D(v), y=120)
        dec_table(f, D(r) if "." in D(r) else D(r) + ".0", y=380, at=1)
        lines = [L(f"× {D(m)} → 소수점이 {'오른쪽' if sh > 0 else '왼쪽'}으로 {abs(sh)}칸", memo="숫자 배열은 그대로"), L(f"{D(v)} × {D(m)} = {D(r)}")]
        S.add(5, q, D(r), f"곱하는 수의 0의 개수(소수점 아래 자리 수)만큼 소수점을 옮겨요", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 소수의 나눗셈 ══════════
def shift_fig(a, b, k, at=0):
    """두 수의 소수점을 같은 칸만큼 오른쪽으로"""
    f = Fig()
    f.text(330, 190, f"{D(a)} ÷ {D(b)}", z=56, b=700)
    A, B = a * 10 ** k, b * 10 ** k
    f.text(330, 360, f"{D(A)} ÷ {D(B)}", z=56, b=700, at=at, c="teal")
    f.text(330, 270, f"× {10 ** k}         × {10 ** k}", z=26, c="coral", at=at)
    f.line(250, 215, 250, 315, c="coral", w=3, ar=1, at=at)
    f.line(420, 215, 420, 315, c="coral", w=3, ar=1, at=at)
    f.text(330, 470, f"소수점을 {k}칸씩 오른쪽으로", z=28, c="soft", at=at)
    return f

def ddiv():
    S = Set("ddiv", "소수의 나눗셈 — 소수점을 옮겨 자연수로", "소수의 나눗셈",
            {1: "(소수) ÷ (자연수)", 2: "몫이 1보다 작은 나눗셈", 3: "(자연수) ÷ (자연수)를 소수로", 4: "(소수) ÷ (소수)", 5: "자릿수가 다른 소수의 나눗셈"},
            pp=10,
            tips={1: "7.2 ÷ 3 → 0.1이 72개를 3으로 → 0.1이 24개 → 2.4. 몫의 소수점은 나누어지는 수의 소수점 위에",
                  2: "몫의 자연수 부분이 0이면 0을 쓰고 소수점을 찍어요 — 2.24 ÷ 4 = 0.56",
                  3: "나누어떨어지지 않으면 0을 붙여 계속 나눠요 — 7 ÷ 4 = 7.00 ÷ 4 = 1.75",
                  4: "나누는 수가 자연수가 되도록 두 수의 소수점을 같은 칸만큼 오른쪽으로 — 몫은 그대로",
                  5: "나누는 수의 소수점 아래 자리 수만큼 옮겨요. 5.22 ÷ 0.9 = 52.2 ÷ 9"},
            note="소수의 나눗셈은 ‘나누는 수를 자연수로 만들기(두 수 같은 배)’와 ‘몫의 소수점 위치’ 두 가지예요. 두 수에 같은 수를 곱해도 몫이 그대로라는 점을 먼저 확인하게 해 주세요.")
    R = rng(334)

    def remap(f, n_lines):
        for el in f.els:
            if isinstance(el.get("at"), int):
                el["dl"] = el.get("dl", 0) + 450 * el["at"]
                el["at"] = 0

    def g1():
        d = R.randint(2, 9); Q = R.randint(12, 99) if S.count(1) % 2 else R.randint(102, 399)
        k = 1 if S.count(1) % 2 else 2
        N_ = d * Q
        n, q_ = Fr(N_, 10 ** k), Fr(Q, 10 ** k)
        if dp(n) != k or n < 1:
            return
        f, _, _, _ = long_div(N_, d)
        remap(f, 3)
        div_points(f, N_, k, q_lt1=Q < 10 ** k)
        lines = [L(f"{N_} ÷ {d} = {Q}", pre="자연수처럼", memo=f"{D(Fr(1, 10 ** k))}이 {N_}개"), L(f"{D(n)} ÷ {d} = {D(q_)}", memo=f"{D(Fr(1, 10 ** k))}이 {Q}개 → 소수점은 나누어지는 수의 소수점 위")]
        S.add(1, f"{D(n)} ÷ {J(d, '은', '는')} 얼마인가요?", D(q_), "자연수처럼 나누고 — 소수점은 나누어지는 수의 소수점 위", lines, f.out(), key=f"{n}/{d}")
    fill(S, 1, 20, g1)

    def g2():
        d = R.randint(2, 9); Q = R.randint(11, 99)
        k = 2
        N_ = d * Q
        n, q_ = Fr(N_, 100), Fr(Q, 100)
        if n >= d or dp(q_) != 2:
            return
        f, _, _, _ = long_div(N_, d)
        remap(f, 3)
        div_points(f, N_, k, q_lt1=True)
        lines = [L(f"{D(n)}{'은' if bat(D(n)) else '는'} {d}보다 작아요", memo="몫의 자연수 부분은 0"), L(f"{N_} ÷ {d} = {Q}", pre="자연수처럼"), L(f"{D(n)} ÷ {d} = {D(q_)}", memo="0.01이 몇 개")]
        S.add(2, f"{D(n)} ÷ {J(d, '은', '는')} 얼마인가요?", D(q_), "몫의 자연수 자리에 0 — 소수점을 찍고 계속", lines, f.out(), key=f"{n}/{d}")
    fill(S, 2, 20, g2)

    def g3():
        a, d = R.randint(2, 30), R.choice([2, 4, 5, 8, 20, 25, 40])
        if a % d == 0 or a > 3 * d and d > 8:
            return
        q_ = Fr(a, d)
        k = dp(q_)
        if k == 0 or k > 3:
            return
        N_ = a * 10 ** k
        f, _, _, _ = long_div(N_, d)
        remap(f, 3)
        div_points(f, N_, k, q_lt1=a < d)
        lines = [L(f"{a} = {DK(Fr(a), k)}", memo="0을 붙여 계속 나눠요"), L(f"{N_} ÷ {d} = {N_ // d}", pre=f"{D(Fr(1, 10 ** k))}이 {N_}개"), L(f"{a} ÷ {d} = {D(q_)}")]
        S.add(3, f"{a} ÷ {d}의 몫을 소수로 나타내세요.", D(q_), "나누어떨어질 때까지 0을 붙여 나눠요", lines, f.out(), key=f"{a}/{d}")
    fill(S, 3, 20, g3)

    def g4():
        k = R.choice([1, 2])
        b = Fr(R.randint(2, 9), 10) if k == 1 else Fr(R.randint(11, 99), 100) if R.random() < 0.5 else Fr(R.randint(11, 49), 10)
        k = dp(b)
        Q = Fr(R.randint(2, 30)) if S.count(4) % 2 == 0 else Fr(R.randint(12, 95), 10)
        a = b * Q
        if dp(a) > 2 or dp(a) == 0 or k == 0:
            return
        A, B = a * 10 ** k, b * 10 ** k
        f = shift_fig(a, b, k)
        lines = [L(f"{D(a)} ÷ {D(b)} = {D(A)} ÷ {D(B)}", memo=f"두 수에 {10 ** k}{'을' if bat(10 ** k) else '를'} 곱해도 몫은 같아요"), L(f"{D(A)} ÷ {D(B)} = {D(Q)}"), L(f"{D(b)} × {D(Q)} = {D(a)}", pre="검산")]
        S.add(4, f"{D(a)} ÷ {J(D(b), '은', '는')} 얼마인가요?", D(Q), "나누는 수가 자연수가 되도록 두 수의 소수점을 같이 옮겨요", lines, f.out(), key=f"{a}/{b}")
    fill(S, 4, 20, g4)

    def g5():
        b = Fr(R.randint(2, 9), 10) if S.count(5) % 2 else Fr(R.randint(12, 48), 10)
        Q = Fr(R.randint(12, 99), 10) if S.count(5) % 3 else Fr(R.randint(102, 999), 100)
        a = b * Q
        if dp(a) <= dp(b) or dp(a) > 3:
            return
        k = dp(b)
        A, B = a * 10 ** k, b * 10 ** k
        f = shift_fig(a, b, k)
        lines = [L(f"{D(a)} ÷ {D(b)} = {D(A)} ÷ {D(B)}", memo=f"나누는 수 기준 — 소수점을 {k}칸씩"), L(f"{D(A)} ÷ {D(B)} = {D(Q)}", memo="몫의 소수점은 옮긴 소수점 위"), L(f"{D(b)} × {D(Q)} = {D(a)}", pre="검산")]
        S.add(5, f"{D(a)} ÷ {J(D(b), '은', '는')} 얼마인가요?", D(Q), "나누는 수의 소수점 아래 자리 수만큼 두 수를 옮겨요", lines, f.out(), key=f"{a}/{b}")
    fill(S, 5, 20, g5)
    return S


# ══════════ 분수와 소수 ══════════
def fdec():
    S = Set("fdec", "분수와 소수 — 서로 바꾸고 견주기", "분수와 소수",
            {1: "분모가 10 · 100 · 1000인 분수", 2: "분수를 소수로", 3: "소수를 기약분수로", 4: "분수와 소수의 크기 비교", 5: "분수와 소수가 섞인 계산"},
            mixed=True, pp=10,
            tips={1: "{7/10} = 0.7 · {37/100} = 0.37 · {123/1000} = 0.123",
                  2: "분모를 10, 100, 1000으로 만들어요 — {3/4} = {75/100} = 0.75. 안 되면 분자 ÷ 분모",
                  3: "0.45 = {45/100} → 최대공약수 5로 약분 → {9/20}",
                  4: "모두 소수로(또는 모두 분수로) 바꾸어 비교해요",
                  5: "계산하기 편한 쪽으로 통일 — 소수로 끝나면 소수로, 아니면 분수로"},
            note="분수와 소수는 같은 수의 두 가지 모습이에요. 분모를 10, 100, 1000으로 만들 수 있는지(분모에 2와 5만 있는지)를 먼저 살피게 해 주세요.")
    R = rng(335)

    def g1():
        k = S.count(1) % 3
        dden = [10, 100, 1000][k]
        n = R.randint(1, dden * 3)
        if n % 10 == 0:
            return
        v = Fr(n, dden)
        f = Fig()
        if S.count(1) % 2 == 0:
            q = f"{J(F_(n, dden), '을', '를')} 소수로 나타내세요."
            lines = [L(f"{F_(1, dden)} = {D(Fr(1, dden))}", memo=f"분모 {dden} → 소수 {['한', '두', '세'][len(str(dden)) - 2]} 자리"), L(f"{F_(n, dden)} = {D(v)}")]
            ans = D(v)
        else:
            q = f"{D(v)}{'을' if bat(D(v)) else '를'} 분모가 {dden}인 분수로 나타내세요."
            lines = [L(f"{D(v)}{'은' if bat(D(v)) else '는'} {D(Fr(1, dden))}이 {n}개", memo="소수 자리 수만큼 분모의 0"), L(f"{D(v)} = {F_(n, dden)}")]
            ans = F_(n, dden)
        dec_table(f, D(v), at=0)
        S.add(1, q, ans, f"소수 {['한', '두', '세'][len(str(dden)) - 2]} 자리 ↔ 분모 {dden}", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        d = R.choice([2, 4, 5, 8, 20, 25, 40, 50]) if k < 2 else R.choice([4, 8, 16, 20, 25])
        n = R.randint(1, d - 1) if k < 2 else R.randint(d + 1, 3 * d)
        if gcd(n, d) != 1:
            return
        v = Fr(n, d)
        kk = dp(v)
        dden = 10 ** kk
        m = dden // d
        f = Fig()
        if k < 2 and dden in (10, 100) and n * m <= 100:
            f.grid(130, 130, 40, 40, 10, 10, c="soft", sw=1.5)
            cells = n * m * (100 // dden)
            for i in range(cells):
                r_, c_ = divmod(i, 10)
                f.rect(130 + c_ * 40 + 2, 130 + r_ * 40 + 2, 36, 36, c="none", f="gold", fo=0.5, at=1, dl=(i // 10) * 90)
        lines = [L(f"{F_(n, d)} = {{{n} × {m}/{d} × {m}}}", memo=f"분모를 {RO(dden)} 만들기"), L(f"{{{n} × {m}/{d} × {m}}} = {F_(n * m, dden)}"), L(f"{F_(n * m, dden)} = {D(v)}")]
        S.add(2, f"{J(F_(n, d), '을', '를')} 소수로 나타내세요.", D(v), f"분모 {d}에 {m}{'을' if bat(m) else '를'} 곱해 {RO(dden)}", lines, f.out() if f.els else None, key=f"{n}/{d}")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        v = Fr(R.randint(1, 99), 100) if k == 0 else Fr(R.randint(101, 499), 100)
        if dp(v) != 2 or gcd(int(v * 100), 100) == 1:
            return
        N_ = int(v * 100)
        g = gcd(N_, 100)
        a, b = N_ // g, 100 // g
        lines = [L(f"{D(v)} = {F_(N_, 100)}", memo="소수 두 자리 → 분모 100"), L(f"{F_(N_, 100)} = {{{N_} ÷ {g}/100 ÷ {g}}}", memo=f"최대공약수 {RO(g)} 약분"), L(f"{{{N_} ÷ {g}/100 ÷ {g}}} = {F_(a, b)}" + (f" = {MX(Fr(a, b))}" if a > b else ""))]
        ans = MX(Fr(a, b)) if a > b else F_(a, b)
        S.add(3, f"{D(v)}{'을' if bat(D(v)) else '를'} 기약분수로 나타내세요.", ans, "분모 100인 분수로 쓰고 — 최대공약수로 약분", lines, None, key=f"{v}")
    fill(S, 3, 20, g3)

    def g4():
        d = R.choice([2, 4, 5, 8, 20, 25])
        n = R.randint(1, d - 1)
        if gcd(n, d) != 1:
            return
        v = Fr(n, d)
        w = v + Fr(R.choice([-1, 1]) * R.randint(1, 9), 100)
        if w <= 0 or w >= 1 or w == v or dp(w) > 2:
            return
        x, y = (F_(n, d), D(w)) if R.random() < 0.5 else (D(w), F_(n, d))
        big = F_(n, d) if v > w else D(w)
        f = Fig()
        X = dnl(f, 0, 1, Fr(1, 10), 5)
        dpt(f, X, v, F_(n, d), at=1, col="gold", up=True)
        dpt(f, X, w, D(w), at=1, col="teal", up=False)
        q = f"{J(x, '과', '와')} {y} 중에서 더 큰 수는 무엇인가요?"
        gt = ">" if v > w else "<"
        lines = [L(f"{F_(n, d)} = {D(v)}", memo="분수를 소수로"), L(f"{D(v)} {gt} {D(w)}", memo="소수끼리 비교"), L(f"{J(big, '이', '가')} 더 커요")]
        S.add(4, q, big, "한쪽으로 통일 — 분수를 소수로 바꾸어 비교해요", lines, f.out(), key=f"{n}/{d}|{w}")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            d = R.choice([2, 4, 5, 8, 20, 25]); n = R.randint(1, d - 1)
            if gcd(n, d) != 1:
                return
            b = Fr(R.randint(1, 99), 100)
            if dp(b) == 0:
                return
            v = Fr(n, d) + b
            q = f"{F_(n, d)} + {J(D(b), '은', '는')} 얼마인가요? (소수로)"
            lines = [L(f"{F_(n, d)} = {D(Fr(n, d))}", memo="분수를 소수로"), L(f"{D(Fr(n, d))} + {D(b)} = {D(v)}")]
            ans = D(v)
            plan = "분수를 소수로 바꾸어 더해요"
        elif k == 1:
            d = R.choice([3, 6, 7, 9]); n = R.randint(1, d - 1)
            b = Fr(R.randint(1, 9), 10)
            if gcd(n, d) != 1:
                return
            v = Fr(n, d) + b
            bf = Fr(b)
            q = f"{F_(n, d)} + {J(D(b), '은', '는')} 얼마인가요? (분수로)"
            l = d * 10 // gcd(d, 10)
            lines = [L(f"{D(b)} = {F_(int(bf * 10), 10)}", memo=f"{J(F_(n, d), '은', '는')} 소수로 끝나지 않아요 → 분수로"), L(f"{F_(n, d)} + {F_(int(bf * 10), 10)} = {F_(n * (l // d), l)} + {F_(int(bf * 10) * (l // 10), l)}", memo="통분"),
                     L(f"{F_(n * (l // d), l)} + {F_(int(bf * 10) * (l // 10), l)} = {F_(v.numerator, v.denominator) if v < 1 else MX(v)}" if (v.denominator == l) else f"{F_(n * (l // d), l)} + {F_(int(bf * 10) * (l // 10), l)} = {F_(n * (l // d) + int(bf * 10) * (l // 10), l)} = {MX(v)}")]
            ans = MX(v)
            plan = "소수로 끝나지 않는 분수가 있으면 분수로 통일"
        else:
            d = R.choice([3, 4, 5, 6, 8]); n = R.randint(1, d - 1)
            b = Fr(R.randint(1, 9), 10) * R.choice([1, 2, 3])
            if gcd(n, d) != 1 or b >= 2 or dp(b) == 0:
                return
            v = Fr(n, d) * b
            bn, bd = b.numerator, b.denominator
            q = f"{D(b)} × {J(F_(n, d), '은', '는')} 얼마인가요? (기약분수로)"
            lines = [L(f"{D(b)} = {F_(bn, bd)}", memo="소수를 기약분수로"), L(f"{F_(bn, bd)} × {F_(n, d)} = {{{bn} × {n}/{bd} × {d}}}"), L(f"{{{bn} × {n}/{bd} × {d}}} = {MX(v) if v.denominator > 1 else v}")]
            ans = MX(v)
            plan = "소수를 분수로 바꾸어 곱해요"
        S.add(5, q, ans, plan, lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 삼각형과 사각형 ══════════
def fit(pts, box=(90, 90, 570, 560)):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    s = min((box[2] - box[0]) / max(w, 1e-9), (box[3] - box[1]) / max(h, 1e-9))
    ox = (box[0] + box[2]) / 2 - s * (min(xs) + max(xs)) / 2
    oy = (box[1] + box[3]) / 2 + s * (min(ys) + max(ys)) / 2
    return [(ox + s * x, oy - s * y) for x, y in pts]

def side_lab(f, A, B, s, at="q", c="ink", z=30, off=30, inside=None):
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    dx, dy = B[0] - A[0], B[1] - A[1]
    L_ = math.hypot(dx, dy) or 1
    nx, ny = dy / L_, -dx / L_
    if inside is not None:
        cx, cy = inside
        if (mx + nx * 10 - cx) ** 2 + (my + ny * 10 - cy) ** 2 < (mx - cx) ** 2 + (my - cy) ** 2:
            nx, ny = -nx, -ny
    f.text(mx + nx * off, my + ny * off + z * 0.35, s, z=z, c=c, at=at, b=700)

def tick(f, A, B, n=1, at="q", c="ink"):
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    dx, dy = B[0] - A[0], B[1] - A[1]
    L_ = math.hypot(dx, dy)
    ux, uy = dx / L_, dy / L_
    nx, ny = -uy, ux
    for i in range(n):
        o = (i - (n - 1) / 2) * 9
        cx, cy = mx + ux * o, my + uy * o
        f.line(cx - nx * 11, cy - ny * 11, cx + nx * 11, cy + ny * 11, c=c, w=3, at=at)

def shape():
    S = Set("shape", "삼각형과 사각형 — 변과 각의 성질", "삼각형·사각형",
            {1: "이등변삼각형", 2: "정삼각형 · 둘레", 3: "평행사변형", 4: "마름모", 5: "직사각형 · 사다리꼴"},
            pp=8,
            tips={1: "두 변의 길이가 같으면 두 각의 크기도 같아요 — 밑각 = (180° − 꼭지각) ÷ 2",
                  2: "세 변이 같고 세 각이 모두 60°. 둘레 = 한 변 × 3",
                  3: "마주 보는 변 · 마주 보는 각이 같고, 이웃한 두 각의 합은 180°",
                  4: "네 변이 모두 같아요. 마주 보는 각이 같고, 두 대각선은 수직으로 만나 서로 반으로 나눠요",
                  5: "직사각형 둘레 = (가로 + 세로) × 2. 사다리꼴은 평행한 두 변 사이의 이웃한 두 각의 합이 180°"},
            note="도형의 성질은 ‘같은 것 찾기’로 정리하게 해 주세요. 그림에 같은 변은 같은 눈금 표시를, 같은 각은 같은 호를 그려 넣는 습관이 문제 해결로 이어져요.")
    R = rng(336)

    def tri(A, B, C):
        return fit([A, B, C])

    def g1():
        k = S.count(1) % 3
        f = Fig()
        top = R.choice([20, 30, 40, 50, 70, 80, 100, 110, 120])
        base = (180 - top) // 2
        h = 1 / math.tan(math.radians(top / 2)) if top < 175 else 0.1
        P = tri((0, h), (-1, 0), (1, 0))
        f.poly(P, c="ink", w=3)
        tick(f, P[0], P[1]); tick(f, P[0], P[2])
        cen = ((P[0][0] + P[1][0] + P[2][0]) / 3, (P[0][1] + P[1][1] + P[2][1]) / 3)
        if k == 0:
            angle_mark(f, P[0], P[1], P[2], label=f"{top}°", r=40)
            angle_mark(f, P[1], P[2], P[0], label="?", r=40, at=0, c="coral", f_="coral")
            q = f"이등변삼각형에서 길이가 같은 두 변 사이의 각(꼭지각)이 {top}°예요. 나머지 한 각의 크기는 몇 도인가요?"
            lines = [L(f"180 − {top} = {180 - top}", memo="두 밑각의 합"), L(f"{180 - top} ÷ 2 = {base}", memo="두 밑각은 크기가 같아요"), L(f"{base}°")]
            ans, ap, plan = f"{base}°", str(base), "세 각의 합 180° — 두 밑각은 같아요"
        elif k == 1:
            angle_mark(f, P[1], P[2], P[0], label=f"{base}°", r=40)
            angle_mark(f, P[0], P[1], P[2], label="?", r=40, at=0, c="coral", f_="coral")
            q = f"이등변삼각형의 한 밑각이 {base}°예요. 길이가 같은 두 변 사이의 각은 몇 도인가요?"
            lines = [L(f"{base} × 2 = {base * 2}", memo="두 밑각은 같아요"), L(f"180 − {base * 2} = {top}", memo="세 각의 합 180°"), L(f"{top}°")]
            ans, ap, plan = f"{top}°", str(top), "두 밑각의 합을 180°에서 빼요"
        else:
            s, b = R.randint(5, 15), R.randint(4, 14)
            if b >= 2 * s:
                return
            hh = math.sqrt(s * s - (b / 2) ** 2)
            P = fit([(0, hh), (-b / 2, 0), (b / 2, 0)])
            f = Fig()
            f.poly(P, c="ink", w=3)
            tick(f, P[0], P[1]); tick(f, P[0], P[2])
            cen = ((P[0][0] + P[1][0] + P[2][0]) / 3, (P[0][1] + P[1][1] + P[2][1]) / 3)
            side_lab(f, P[0], P[1], f"{s} cm", inside=cen)
            side_lab(f, P[1], P[2], f"{b} cm", inside=cen)
            q = f"길이가 같은 두 변이 각각 {s} cm이고 나머지 한 변이 {b} cm인 이등변삼각형의 세 변의 길이의 합은 몇 cm인가요?"
            lines = [L(f"{s} + {s} + {b} = {2 * s + b}", memo="같은 변 두 개 + 밑변"), L(f"{2 * s + b} cm")]
            ans, ap, plan = f"{2 * s + b} cm", str(2 * s + b), "같은 길이의 두 변을 잊지 말고 더해요"
        S.add(1, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 4
        f = Fig()
        P = fit([(0, math.sqrt(3)), (-1, 0), (1, 0)])
        f.poly(P, c="ink", w=3)
        for i in range(3):
            tick(f, P[i], P[(i + 1) % 3])
        cen = ((P[0][0] + P[1][0] + P[2][0]) / 3, (P[0][1] + P[1][1] + P[2][1]) / 3)
        if k == 0:
            s = R.randint(4, 25)
            side_lab(f, P[1], P[2], f"{s} cm", inside=cen)
            q = f"한 변이 {s} cm인 정삼각형의 둘레는 몇 cm인가요?"
            lines = [L("세 변의 길이가 모두 같아요", memo="정삼각형"), L(f"{s} × 3 = {3 * s}"), L(f"{3 * s} cm")]
            ans, ap = f"{3 * s} cm", str(3 * s)
        elif k == 1:
            s = R.randint(4, 30)
            side_lab(f, P[1], P[2], "? cm", inside=cen, c="coral")
            q = f"둘레가 {3 * s} cm인 정삼각형의 한 변은 몇 cm인가요?"
            lines = [L("세 변이 같으니 둘레를 3으로 나눠요"), L(f"{3 * s} ÷ 3 = {s}"), L(f"{s} cm")]
            ans, ap = f"{s} cm", str(s)
        elif k == 2:
            s = R.randint(1, 7) * 4
            sq = s * 3
            side_lab(f, P[1], P[2], f"{s} cm", inside=cen)
            q = f"한 변이 {s} cm인 정삼각형과 둘레가 같은 정사각형의 한 변은 몇 cm인가요?"
            lines = [L(f"{s} × 3 = {sq}", pre="정삼각형의 둘레"), L(f"{sq} ÷ 4 = {sq // 4}", pre="정사각형의 한 변", memo="네 변이 같아요"), L(f"{sq // 4} cm")]
            ans, ap = f"{sq // 4} cm", str(sq // 4)
        else:
            n = R.randint(2, 5); s = R.randint(3, 9)
            q = f"한 변이 {s} cm인 정삼각형 {n}개를 겹치지 않게 한 줄로 이어 붙여 만든 도형의 둘레는 몇 cm인가요? (이웃한 정삼각형은 한 변씩 맞닿아요)"
            outer = n + 2
            f = Fig()
            pts = []
            for i in range(n):
                up = i % 2 == 0
                x0 = i * 0.5
                tri_ = [(x0, 0), (x0 + 1, 0), (x0 + 0.5, math.sqrt(3) / 2)] if up else [(x0, math.sqrt(3) / 2), (x0 + 1, math.sqrt(3) / 2), (x0 + 0.5, 0)]
                pts.append(tri_)
            allp = [p for t in pts for p in t]
            box = (60, 160, 600, 500)
            xs, ys = [p[0] for p in allp], [p[1] for p in allp]
            sc = min((box[2] - box[0]) / (max(xs) - min(xs)), (box[3] - box[1]) / (max(ys) - min(ys)))
            for t in pts:
                f.poly([(box[0] + sc * (x - min(xs)), box[3] - sc * (y - min(ys))) for x, y in t], c="ink", w=3, f="gold", fo=0.15)
            lines = [L(f"바깥 테두리의 변: {outer}개", memo=f"맞닿은 변 {n - 1}개는 둘레가 아니에요"), L(f"{s} × {outer} = {s * outer}"), L(f"{s * outer} cm")]
            ans, ap = f"{s * outer} cm", str(s * outer)
        S.add(2, q, ans, "정삼각형은 세 변이 모두 같아요", lines, f.out(), ap=ap, key=q)
    fill(S, 2, 20, g2)

    def para(a_deg, sk=0.0):
        t = math.radians(a_deg)
        w, s = 1.6, 1.0
        A, B = (0, 0), (w, 0)
        C, Dd = (w + s * math.cos(t), s * math.sin(t)), (s * math.cos(t), s * math.sin(t))
        return fit([A, B, C, Dd])

    def g3():
        k = S.count(3) % 3
        a = R.choice([50, 55, 60, 65, 70, 75, 80, 110, 115, 120, 125, 130])
        P = para(a)
        f = Fig()
        f.poly(P, c="ink", w=3)
        if k == 0:
            angle_mark(f, P[0], P[1], P[3], label=f"{a}°", r=44)
            angle_mark(f, P[1], P[2], P[0], label="?", r=44, at=0, c="coral", f_="coral")
            q = f"평행사변형에서 한 각이 {a}°예요. 이 각과 이웃한 각의 크기는 몇 도인가요?"
            lines = [L("이웃한 두 각의 합은 180°", memo="평행사변형"), L(f"180 − {a} = {180 - a}"), L(f"{180 - a}°")]
            ans, ap = f"{180 - a}°", str(180 - a)
            plan = "이웃한 두 각의 합 180°"
        elif k == 1:
            angle_mark(f, P[0], P[1], P[3], label=f"{a}°", r=44)
            angle_mark(f, P[2], P[3], P[1], label="?", r=44, at=0, c="coral", f_="coral")
            q = f"평행사변형에서 한 각이 {a}°예요. 이 각과 마주 보는 각의 크기는 몇 도인가요?"
            lines = [L("마주 보는 두 각의 크기는 같아요", memo="평행사변형"), L(f"{a}°")]
            ans, ap = f"{a}°", str(a)
            plan = "마주 보는 각은 같아요"
        else:
            x, y = R.randint(5, 20), R.randint(4, 15)
            if x == y:
                return
            cen = (sum(p[0] for p in P) / 4, sum(p[1] for p in P) / 4)
            side_lab(f, P[0], P[1], f"{x} cm", inside=cen)
            side_lab(f, P[3], P[0], f"{y} cm", inside=cen)
            q = f"이웃한 두 변의 길이가 {x} cm, {y} cm인 평행사변형의 네 변의 길이의 합은 몇 cm인가요?"
            lines = [L("마주 보는 변의 길이가 같아요", memo="두 쌍"), L(f"({x} + {y}) × 2 = {2 * (x + y)}"), L(f"{2 * (x + y)} cm")]
            ans, ap = f"{2 * (x + y)} cm", str(2 * (x + y))
            plan = "마주 보는 변이 같으니 (이웃한 두 변의 합) × 2"
        S.add(3, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        a = R.choice([50, 60, 70, 80, 100, 110, 120, 130])
        t = math.radians(a)
        P = fit([(0, 0), (1, 0), (1 + math.cos(t), math.sin(t)), (math.cos(t), math.sin(t))])
        f = Fig()
        f.poly(P, c="ink", w=3)
        for i in range(4):
            tick(f, P[i], P[(i + 1) % 4])
        if k == 0:
            s = R.randint(3, 25)
            cen = (sum(p[0] for p in P) / 4, sum(p[1] for p in P) / 4)
            side_lab(f, P[0], P[1], f"{s} cm", inside=cen)
            q = f"한 변이 {s} cm인 마름모의 둘레는 몇 cm인가요?"
            lines = [L("네 변의 길이가 모두 같아요", memo="마름모"), L(f"{s} × 4 = {4 * s}"), L(f"{4 * s} cm")]
            ans, ap, plan = f"{4 * s} cm", str(4 * s), "마름모는 네 변이 모두 같아요"
        elif k == 1:
            angle_mark(f, P[0], P[1], P[3], label=f"{a}°", r=44)
            angle_mark(f, P[1], P[2], P[0], label="?", r=44, at=0, c="coral", f_="coral")
            q = f"마름모에서 한 각이 {a}°예요. 이 각과 이웃한 각의 크기는 몇 도인가요?"
            lines = [L("마름모도 평행사변형 — 이웃한 두 각의 합 180°"), L(f"180 − {a} = {180 - a}"), L(f"{180 - a}°")]
            ans, ap, plan = f"{180 - a}°", str(180 - a), "이웃한 두 각의 합 180°"
        else:
            d1, d2 = R.randint(3, 12) * 2, R.randint(3, 12) * 2
            if d1 == d2:
                return
            P = fit([(0, d2 / 2), (-d1 / 2, 0), (0, -d2 / 2), (d1 / 2, 0)])
            f = Fig()
            f.poly(P, c="ink", w=3)
            f.line(*P[0], *P[2], c="teal", w=2.5, d=True)
            f.line(*P[1], *P[3], c="teal", w=2.5, d=True)
            O = ((P[0][0] + P[2][0]) / 2, (P[0][1] + P[2][1]) / 2)
            angle_mark(f, O, P[3], P[0], r=26, at=0)
            f.text((P[1][0] + P[3][0]) / 2 + 60, (P[1][1] + P[3][1]) / 2 + 40, f"{d1} cm", z=26, c="teal", b=700)
            f.text(O[0] + 16, (P[0][1] + O[1]) / 2, f"{d2} cm", z=26, c="teal", b=700, a="s")
            q = f"두 대각선의 길이가 {d1} cm, {d2} cm인 마름모에서 두 대각선이 만나는 점부터 각 꼭짓점까지의 거리는 각각 몇 cm인가요? (짧은 것부터)"
            a1, a2 = sorted([d1 // 2, d2 // 2])
            lines = [L("두 대각선은 서로를 반으로 나눠요", memo="마름모의 대각선"), L(f"{d1} ÷ 2 = {d1 // 2}, {d2} ÷ 2 = {d2 // 2}"), L(f"{a1} cm, {a2} cm")]
            ans, ap, plan = f"{a1} cm, {a2} cm", f"{a1}, {a2}", "대각선은 수직으로 만나 서로를 반으로 나눠요"
            S.add(4, q, ans, plan, lines, f.out(), ap=ap, omr="ex", key=q)
            return
        S.add(4, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        f = Fig()
        if k == 0:
            w, h = R.randint(5, 25), R.randint(3, 18)
            if w == h:
                return
            P = fit([(0, 0), (w, 0), (w, h), (0, h)], box=(110, 140, 550, 520))
            f.poly(P, c="ink", w=3)
            cen = (330, 330)
            side_lab(f, P[0], P[1], f"{w} cm", inside=cen)
            side_lab(f, P[1], P[2], f"{h} cm", inside=cen)
            q = f"가로 {w} cm, 세로 {h} cm인 직사각형의 둘레는 몇 cm인가요?"
            lines = [L(f"({w} + {h}) × 2 = {2 * (w + h)}", memo="가로 + 세로가 두 번"), L(f"{2 * (w + h)} cm")]
            ans, ap, plan = f"{2 * (w + h)} cm", str(2 * (w + h)), "둘레 = (가로 + 세로) × 2"
        elif k == 1:
            w, h = R.randint(5, 25), R.randint(3, 18)
            if w == h:
                return
            Pm = 2 * (w + h)
            P = fit([(0, 0), (w, 0), (w, h), (0, h)], box=(110, 140, 550, 520))
            f.poly(P, c="ink", w=3)
            side_lab(f, P[0], P[1], f"{w} cm", inside=(330, 330))
            side_lab(f, P[1], P[2], "? cm", inside=(330, 330), c="coral")
            q = f"둘레가 {Pm} cm이고 가로가 {w} cm인 직사각형의 세로는 몇 cm인가요?"
            lines = [L(f"{Pm} ÷ 2 = {w + h}", memo="가로 + 세로"), L(f"{w + h} − {w} = {h}"), L(f"{h} cm")]
            ans, ap, plan = f"{h} cm", str(h), "둘레의 반 = 가로 + 세로"
        elif k == 2:
            a = R.choice([55, 60, 65, 70, 75, 80, 105, 110, 115, 120])
            t = math.radians(a)
            P = fit([(0, 0), (2.4, 0), (2.4 - 0.9 * math.cos(math.radians(70)), 0.9 * math.sin(math.radians(70))), (0.9 * math.cos(t), 0.9 * math.sin(t))])
            f.poly(P, c="ink", w=3)
            angle_mark(f, P[0], P[1], P[3], label=f"{a}°", r=44)
            angle_mark(f, P[3], P[0], P[2], label="?", r=44, at=0, c="coral", f_="coral")
            q = f"사다리꼴에서 평행한 두 변 사이에 있는 이웃한 두 각 중 한 각이 {a}°예요. 다른 한 각의 크기는 몇 도인가요?"
            lines = [L("평행한 두 변 사이의 이웃한 두 각의 합은 180°", memo="평행선과 한 직선"), L(f"180 − {a} = {180 - a}"), L(f"{180 - a}°")]
            ans, ap, plan = f"{180 - a}°", str(180 - a), "평행선 사이의 이웃한 두 각의 합 180°"
        else:
            s = R.randint(4, 15); w = R.randint(s + 2, 30)
            P = fit([(0, 0), (w, 0), (w, s), (0, s)], box=(90, 200, 570, 460))
            f.poly(P, c="ink", w=3)
            sq = fit([(0, 0), (w, 0), (w, s), (0, s)], box=(90, 200, 570, 460))
            f.line(P[0][0] + (P[1][0] - P[0][0]) * s / w, P[0][1], P[0][0] + (P[1][0] - P[0][0]) * s / w, P[3][1], c="teal", w=3, d=True)
            q = f"가로 {w} cm, 세로 {s} cm인 직사각형 종이에서 한 변이 {s} cm인 가장 큰 정사각형을 잘라 냈어요. 남은 직사각형의 둘레는 몇 cm인가요?"
            r = w - s
            lines = [L(f"{w} − {s} = {r}", pre="남은 가로"), L(f"({r} + {s}) × 2 = {2 * (r + s)}", memo="세로는 그대로"), L(f"{2 * (r + s)} cm")]
            ans, ap, plan = f"{2 * (r + s)} cm", str(2 * (r + s)), "남은 직사각형의 가로 · 세로를 먼저"
        S.add(5, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 원 ══════════
def circle():
    S = Set("circle", "원 — 반지름 · 지름에서 원주와 넓이까지", "원",
            {1: "반지름과 지름", 2: "원주 구하기", 3: "원주로 지름 구하기", 4: "원의 넓이", 5: "원이 들어간 도형"},
            pp=8,
            tips={1: "지름 = 반지름 × 2 — 한 원에서 반지름은 모두 같아요",
                  2: "원주 = 지름 × 원주율(3.14)",
                  3: "지름 = 원주 ÷ 3.14 · 반지름 = 지름 ÷ 2",
                  4: "원의 넓이 = 반지름 × 반지름 × 3.14",
                  5: "전체에서 빼거나 반으로 나누어 — 반원의 둘레에는 지름도 들어가요"},
            note="원주율은 ‘원주가 지름의 약 3.14배’라는 뜻이에요. 넓이 공식은 원을 잘게 잘라 직사각형처럼 늘어놓는 그림으로 이해시키고, 반지름 · 지름을 헷갈리지 않게 늘 먼저 확인하게 해 주세요.")
    R = rng(337)
    PI = Fr(314, 100)

    def cfig(r_lab=None, d_lab=None, at="q", r_at="q", d_at="q", n=1):
        f = Fig()
        if n == 1:
            f.circ(330, 330, 220, c="ink", sw=3, at=at)
            f.dot(330, 330, r=7, at=at)
            if r_lab:
                f.line(330, 330, 330 + 220 * math.cos(math.radians(35)), 330 - 220 * math.sin(math.radians(35)), c="teal", w=4, at=r_at)
                f.text(330 + 110 * math.cos(math.radians(35)) + 20, 330 - 110 * math.sin(math.radians(35)) - 14, r_lab, z=30, c="teal", b=700, at=r_at)
            if d_lab:
                f.line(110, 330, 550, 330, c="coral", w=4, at=d_at)
                f.text(330, 380, d_lab, z=30, c="coral", b=700, at=d_at)
        return f

    def g1():
        k = S.count(1) % 4
        if k == 0:
            r = R.randint(3, 30)
            f = cfig(r_lab=f"{r} cm", d_lab="?", d_at=0)
            q = f"반지름이 {r} cm인 원의 지름은 몇 cm인가요?"
            lines = [L("지름 = 반지름 × 2", memo="지름은 반지름 두 개"), L(f"{r} × 2 = {2 * r}"), L(f"{2 * r} cm")]
            ans, ap = f"{2 * r} cm", str(2 * r)
        elif k == 1:
            r = R.randint(3, 30)
            f = cfig(r_lab="?", d_lab=f"{2 * r} cm", r_at=0)
            q = f"지름이 {2 * r} cm인 원의 반지름은 몇 cm인가요?"
            lines = [L("반지름 = 지름 ÷ 2"), L(f"{2 * r} ÷ 2 = {r}"), L(f"{r} cm")]
            ans, ap = f"{r} cm", str(r)
        elif k == 2:
            r, n = R.randint(2, 9), R.randint(3, 6)
            f = Fig()
            rr = min(270 / n, 120)
            x0 = 330 - rr * n
            for i in range(n):
                f.circ(x0 + rr + 2 * rr * i, 330, rr, c="ink", sw=3)
            f.line(x0, 330, x0 + 2 * rr * n, 330, c="coral", w=4, at=0)
            q = f"반지름이 {r} cm인 원 {n}개를 한 줄로 맞닿게 놓았어요. 양 끝을 잇는 선분(원의 중심을 지나는)의 길이는 몇 cm인가요?"
            lines = [L(f"{r} × 2 = {2 * r}", pre="지름"), L(f"{2 * r} × {n} = {2 * r * n}", memo=f"지름 {n}개"), L(f"{2 * r * n} cm")]
            ans, ap = f"{2 * r * n} cm", str(2 * r * n)
        else:
            s = R.randint(3, 15) * 2
            f = Fig()
            f.rect(130, 130, 400, 400, c="ink", sw=3)
            f.circ(330, 330, 200, c="teal", sw=3)
            q = f"한 변이 {s} cm인 정사각형 안에 꼭 맞게 그린 가장 큰 원의 반지름은 몇 cm인가요?"
            lines = [L("원의 지름 = 정사각형의 한 변", memo="꼭 맞게"), L(f"{s} ÷ 2 = {s // 2}"), L(f"{s // 2} cm")]
            ans, ap = f"{s // 2} cm", str(s // 2)
        S.add(1, q, ans, "지름 = 반지름 × 2", lines, f.out(), ap=ap, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            d = R.randint(2, 40)
            f = cfig(d_lab=f"{d} cm")
            C = d * PI
            q = f"지름이 {d} cm인 원의 원주는 몇 cm인가요? (원주율 3.14)"
            lines = [L("원주 = 지름 × 3.14"), L(f"{d} × 3.14 = {D(C)}"), L(f"{D(C)} cm")]
        else:
            r = R.randint(2, 25)
            f = cfig(r_lab=f"{r} cm")
            C = 2 * r * PI
            q = f"반지름이 {r} cm인 원의 원주는 몇 cm인가요? (원주율 3.14)"
            lines = [L(f"{r} × 2 = {2 * r}", pre="지름", memo="반지름이 아니라 지름으로"), L(f"{2 * r} × 3.14 = {D(C)}"), L(f"{D(C)} cm")]
        S.add(2, q, f"{D(C)} cm", "원주 = 지름 × 원주율", lines, f.out(), ap=D(C), key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        d = R.randint(3, 40)
        C = d * PI
        f = cfig(d_lab="?", d_at=0)
        if k == 0:
            q = f"원주가 {D(C)} cm인 원의 지름은 몇 cm인가요? (원주율 3.14)"
            lines = [L("지름 = 원주 ÷ 3.14", memo="원주 = 지름 × 3.14를 거꾸로"), L(f"{D(C)} ÷ 3.14 = {d}"), L(f"{d} cm")]
            ans, ap = f"{d} cm", str(d)
        else:
            if d % 2:
                return
            q = f"원주가 {D(C)} cm인 원의 반지름은 몇 cm인가요? (원주율 3.14)"
            lines = [L(f"{D(C)} ÷ 3.14 = {d}", pre="지름"), L(f"{d} ÷ 2 = {d // 2}", pre="반지름"), L(f"{d // 2} cm")]
            ans, ap = f"{d // 2} cm", str(d // 2)
        S.add(3, q, ans, "원주 ÷ 원주율 = 지름", lines, f.out(), ap=ap, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        r = R.randint(2, 20)
        A = r * r * PI
        if k == 0:
            f = cfig(r_lab=f"{r} cm")
            q = f"반지름이 {r} cm인 원의 넓이는 몇 cm²인가요? (원주율 3.14)"
            lines = [L("넓이 = 반지름 × 반지름 × 3.14"), L(f"{r} × {r} × 3.14 = {D(A)}"), L(f"{D(A)} cm²")]
        elif k == 1:
            f = cfig(d_lab=f"{2 * r} cm")
            q = f"지름이 {2 * r} cm인 원의 넓이는 몇 cm²인가요? (원주율 3.14)"
            lines = [L(f"{2 * r} ÷ 2 = {r}", pre="반지름", memo="넓이는 반지름으로"), L(f"{r} × {r} × 3.14 = {D(A)}"), L(f"{D(A)} cm²")]
        else:
            C = 2 * r * PI
            f = cfig(r_lab="?", r_at=0)
            q = f"원주가 {D(C)} cm인 원의 넓이는 몇 cm²인가요? (원주율 3.14)"
            lines = [L(f"{D(C)} ÷ 3.14 = {2 * r}", pre="지름"), L(f"{2 * r} ÷ 2 = {r}", pre="반지름"), L(f"{r} × {r} × 3.14 = {D(A)}"), L(f"{D(A)} cm²")]
        S.add(4, q, f"{D(A)} cm²", "반지름 × 반지름 × 3.14", lines, f.out(), ap=D(A), key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        f = Fig()
        if k == 0:
            s = R.randint(2, 15) * 2
            r = s // 2
            f.rect(130, 130, 400, 400, c="ink", sw=3, f="gold", fo=0.35)
            f.circ(330, 330, 200, c="ink", sw=3, f="paper", fo=1)
            q = f"한 변이 {s} cm인 정사각형 안에 꼭 맞는 원을 그렸어요. 정사각형에서 원을 뺀 부분의 넓이는 몇 cm²인가요? (원주율 3.14)"
            A = s * s - r * r * PI
            lines = [L(f"{s} × {s} = {s * s}", pre="정사각형"), L(f"{r} × {r} × 3.14 = {D(r * r * PI)}", pre="원", memo="반지름은 한 변의 반"), L(f"{s * s} − {D(r * r * PI)} = {D(A)}"), L(f"{D(A)} cm²")]
            ans, ap = f"{D(A)} cm²", D(A)
        elif k == 1:
            d = R.randint(2, 20) * 2
            f.poly([(110 + 440 * (0.5 - 0.5 * math.cos(math.radians(t))), 420 - 220 * math.sin(math.radians(t))) for t in range(0, 181, 6)], c="ink", w=3, z=True)
            q = f"지름이 {d} cm인 반원의 둘레는 몇 cm인가요? (원주율 3.14)"
            arc = d * PI / 2
            lines = [L(f"{d} × 3.14 ÷ 2 = {D(arc)}", pre="곡선 부분", memo="원주의 반"), L(f"{D(arc)} + {d} = {D(arc + d)}", memo="지름(곧은 선)도 더해요"), L(f"{D(arc + d)} cm")]
            ans, ap = f"{D(arc + d)} cm", D(arc + d)
        elif k == 2:
            r1, r2 = sorted(R.sample(range(2, 16), 2))
            f.circ(330, 330, 240, c="ink", sw=3, f="teal", fo=0.35)
            f.circ(330, 330, 240 * r1 / r2, c="ink", sw=3, f="paper", fo=1)
            f.dot(330, 330, r=6)
            q = f"반지름이 {r2} cm인 원 안에, 중심이 같고 반지름이 {r1} cm인 원을 그렸어요. 두 원 사이(고리 모양)의 넓이는 몇 cm²인가요? (원주율 3.14)"
            A = (r2 * r2 - r1 * r1) * PI
            lines = [L(f"{r2} × {r2} × 3.14 = {D(r2 * r2 * PI)}", pre="큰 원"), L(f"{r1} × {r1} × 3.14 = {D(r1 * r1 * PI)}", pre="작은 원"), L(f"{D(r2 * r2 * PI)} − {D(r1 * r1 * PI)} = {D(A)}"), L(f"{D(A)} cm²")]
            ans, ap = f"{D(A)} cm²", D(A)
        else:
            r = R.randint(2, 20)
            f.poly([(330 + 240 * math.cos(math.radians(t)), 330 - 240 * math.sin(math.radians(t))) for t in range(0, 91, 5)] + [(330, 330)], c="ink", w=3, f="gold", fo=0.35)
            q = f"반지름이 {r} cm인 원을 똑같이 4조각으로 나눈 것 중 한 조각의 넓이는 몇 cm²인가요? (원주율 3.14)"
            A = r * r * PI / 4
            lines = [L(f"{r} × {r} × 3.14 = {D(r * r * PI)}", pre="원 전체"), L(f"{D(r * r * PI)} ÷ 4 = {D(A)}", memo="4조각 중 하나"), L(f"{D(A)} cm²")]
            ans, ap = f"{D(A)} cm²", D(A)
        S.add(5, q, ans, "전체에서 빼거나 나누어 — 반지름부터 확인", lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S
