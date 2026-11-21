# 고등 ② (공통수학1 · 2) — 순열과 조합 · 행렬 · 점과 직선 · 원의 방정식 · 도형의 이동 · 집합과 명제
import math
from math import gcd, comb, factorial, perm as mperm
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, Plane, NL, ang_pt
from kit import *

x, y = SYMS["x"], SYMS["y"]

def bat(v):
    from core import _has_batchim
    return _has_batchim(str(v))

def F_(n, d):
    return "{%d/%d}" % (n, d)

def FR(v):
    v = Fr(v)
    if v.denominator == 1:
        return N(v)
    return (MI if v < 0 else "") + F_(abs(v.numerator), v.denominator)

def P_(a, b):
    return f"({FR(a)}, {FR(b)})"

def sq(n):
    o, i = 1, n
    p = 2
    while p * p <= i:
        while i % (p * p) == 0:
            i //= p * p
            o *= p
        p += 1
    return o, i

def RTn(n):
    o, i = sq(n)
    if i == 1:
        return str(o)
    return (str(o) if o > 1 else "") + f"√{{{i}}}"

def plane(f, lo=-7, hi=7, at="q"):
    pl = Plane(f, (lo - 0.5, hi + 0.5), (lo - 0.5, hi + 0.5), box=(40, 30, 620, 650))
    pl.axes(at=at, lab_step=2)
    return pl


# ══════════ 순열과 조합 ══════════
def perm():
    S = Set("perm", "순열과 조합 — _{n}P_{r}와 _{n}C_{r}", "순열과 조합",
            {1: "순열의 수", 2: "조건이 있는 순열", 3: "조합의 수", 4: "조건이 있는 조합", 5: "조합의 활용"},
            pp=10,
            tips={1: "_{n}P_{r} = n(n − 1)…(n − r + 1) — 순서 있게 r개를 뽑아 늘어놓기",
                  2: "이웃하면 한 묶음으로, 이웃하지 않으면 나머지를 먼저 세우고 사이사이에",
                  3: "_{n}C_{r} = {_{n}P_{r}/r!} — 순서 없이 뽑기 · _{n}C_{r} = _{n}C_{n − r}",
                  4: "반드시 포함하면 미리 뽑아 두고, 포함하지 않으면 빼고 뽑아요",
                  5: "직선은 두 점, 삼각형은 세 점(한 직선 위의 세 점은 빼기)"},
            note="순열과 조합의 차이는 ‘순서가 의미 있는가’ 하나예요. 뽑은 뒤 자리를 바꾸면 다른 경우인지를 먼저 묻게 해 주세요.")
    R = rng(2201)

    def g1():
        n = R.randint(4, 9)
        r = R.randint(2, min(4, n))
        k = S.count(1) % 2
        v = mperm(n, r)
        prod = " × ".join(str(n - i) for i in range(r))
        if k == 0:
            q = f"_{{{n}}}P_{{{r}}}의 값을 구하세요."
            lines = [L(f"_{{{n}}}P_{{{r}}} = {prod} = {v}", memo=f"{n}부터 {r}개를 곱해요")]
        else:
            q = f"{n}명의 학생 중에서 {r}명을 뽑아 한 줄로 세우는 경우의 수를 구하세요."
            lines = [L(f"_{{{n}}}P_{{{r}}}", memo="뽑아서 순서 있게"), L(f"_{{{n}}}P_{{{r}}} = {prod} = {v}")]
        S.add(1, q, str(v), "순서 있게 뽑기 → 순열", lines, None, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        n = R.randint(4, 7)
        word = R.choice(["SPRING", "FAMILY", "WINTER", "CANDLE", "MOTHER", "PLANET", "GARDEN", "BRIDGE"])[:n]
        if len(set(word)) < n:
            return
        if k == 0:
            v = factorial(n - 1) * 2
            q = f"{word}의 {n}개 문자를 일렬로 나열할 때, {wa(word[0])} {iga(word[1])} 이웃하는 경우의 수를 구하세요."
            lines = [L(f"{word[0]}{eul(word[1])} 한 묶음 → {n - 1}개 나열: {n - 1}!", memo="묶음 하나를 한 문자처럼"), L(f"묶음 안에서 자리 바꾸기 2!"), L(f"{factorial(n - 1)} × 2 = {v}")]
        elif k == 1:
            v = factorial(n - 2) * mperm(n - 1, 2)
            q = f"{word}의 {n}개 문자를 일렬로 나열할 때, {wa(word[0])} {iga(word[1])} 이웃하지 않는 경우의 수를 구하세요."
            lines = [L(f"나머지 {n - 2}개를 먼저 나열: {factorial(n - 2)}", memo="이웃하지 않을 문자는 나중에"), L(f"사이사이와 양 끝 {n - 1}자리에 두 문자: _{{{n - 1}}}P_{{2}} = {mperm(n - 1, 2)}"), L(f"{factorial(n - 2)} × {mperm(n - 1, 2)} = {v}")]
        else:
            v = 2 * factorial(n - 2)
            q = f"{word}의 {n}개 문자를 일렬로 나열할 때, 양 끝에 {wa(word[0])} {iga(word[-1])} 오는 경우의 수를 구하세요."
            lines = [L(f"양 끝 두 문자 자리 바꾸기 2!", memo="양 끝 고정"), L(f"가운데 {n - 2}개 나열: {n - 2}! = {factorial(n - 2)}"), L(f"2 × {factorial(n - 2)} = {v}")]
        S.add(2, q, str(v), "조건 먼저 — 묶거나, 사이에 넣거나, 고정하거나", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        n = R.randint(5, 12)
        r = R.randint(2, min(5, n - 1))
        k = S.count(3) % 2
        v = comb(n, r)
        if k == 0:
            q = f"_{{{n}}}C_{{{r}}}의 값을 구하세요."
            rr = min(r, n - r)
            lines = ([L(f"_{{{n}}}C_{{{r}}} = _{{{n}}}C_{{{n - r}}}", memo="작은 쪽으로")] if rr != r else []) + [L(f"_{{{n}}}C_{{{rr}}} = {{{' × '.join(str(n - i) for i in range(rr))}/{' × '.join(str(rr - i) for i in range(rr))}}} = {v}")]
        else:
            q = f"{n}명의 학생 중에서 대표 {r}명을 뽑는 경우의 수를 구하세요."
            lines = [L(f"_{{{n}}}C_{{{r}}}", memo="순서 없이 뽑기"), L(f"_{{{n}}}C_{{{r}}} = {{{' × '.join(str(n - i) for i in range(r))}/{' × '.join(str(r - i) for i in range(r))}}} = {v}")]
        S.add(3, q, str(v), "순서 없이 뽑기 → 조합", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        if k == 0:
            n, r = R.randint(6, 12), R.randint(3, 5)
            v = comb(n - 1, r - 1)
            q = f"{n}명 중에서 {r}명을 뽑을 때, 특정한 학생 A가 반드시 뽑히는 경우의 수를 구하세요."
            lines = [L("A를 먼저 뽑아 두기", memo="남은 자리만 고르기"), L(f"_{{{n - 1}}}C_{{{r - 1}}} = {v}")]
        elif k == 1:
            n, r = R.randint(6, 12), R.randint(2, 4)
            v = comb(n - 1, r)
            q = f"{n}명 중에서 {r}명을 뽑을 때, 특정한 학생 A가 뽑히지 않는 경우의 수를 구하세요."
            lines = [L("A를 빼고 나머지에서", memo=f"{n - 1}명 중에서"), L(f"_{{{n - 1}}}C_{{{r}}} = {v}")]
        else:
            m, w = R.randint(3, 7), R.randint(3, 6)
            a, b = R.randint(1, 3), R.randint(1, 2)
            if a > m or b > w:
                return
            v = comb(m, a) * comb(w, b)
            q = f"남학생 {m}명, 여학생 {w}명 중에서 남학생 {a}명과 여학생 {b}명을 뽑는 경우의 수를 구하세요."
            lines = [L(f"_{{{m}}}C_{{{a}}} = {comb(m, a)}", pre="남학생"), L(f"_{{{w}}}C_{{{b}}} = {comb(w, b)}", pre="여학생"), L(f"{comb(m, a)} × {comb(w, b)} = {v}", memo="동시에 → 곱")]
        S.add(4, q, str(v), "꼭 들어갈 것은 먼저, 빠질 것은 빼고", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            n = R.randint(5, 12)
            v = comb(n, 2) - n
            q = f"볼록 {n}각형의 대각선의 개수를 구하세요."
            lines = [L(f"_{{{n}}}C_{{2}} = {comb(n, 2)}", memo="두 꼭짓점을 잇는 선분"), L(f"{comb(n, 2)} − {n} = {v}", memo="변은 빼요")]
            f = None
        elif k == 1:
            n, m = R.randint(5, 10), R.randint(3, 4)
            v = comb(n, 3) - comb(m, 3)
            q = f"서로 다른 {n}개의 점 중에서 {m}개만 한 직선 위에 있고 나머지는 어느 세 점도 한 직선 위에 있지 않을 때, 세 점을 꼭짓점으로 하는 삼각형의 개수를 구하세요."
            lines = [L(f"_{{{n}}}C_{{3}} = {comb(n, 3)}", memo="세 점 고르기"), L(f"_{{{m}}}C_{{3}} = {comb(m, 3)}", memo="한 직선 위의 세 점은 삼각형이 아니에요"), L(f"{comb(n, 3)} − {comb(m, 3)} = {v}")]
            f = None
        else:
            a, b = R.randint(3, 6), R.randint(3, 6)
            v = comb(a, 2) * comb(b, 2)
            q = f"가로선 {a}개와 세로선 {b}개가 서로 수직으로 만날 때, 이 선들로 만들 수 있는 직사각형의 개수를 구하세요."
            lines = [L(f"가로선 2개: _{{{a}}}C_{{2}} = {comb(a, 2)}"), L(f"세로선 2개: _{{{b}}}C_{{2}} = {comb(b, 2)}"), L(f"{comb(a, 2)} × {comb(b, 2)} = {v}")]
            f = Fig()
            for i in range(a):
                f.line(80, 140 + 380 * i / (a - 1), 580, 140 + 380 * i / (a - 1), c="ink", w=3)
            for j in range(b):
                f.line(120 + 420 * j / (b - 1), 100, 120 + 420 * j / (b - 1), 560, c="ink", w=3)
            f.rect(120, 140, 420 / (b - 1), 380 / (a - 1), c="none", f="gold", fo=0.4, at=0)
        S.add(5, q, str(v), "도형을 정하는 점(선)의 조합", lines, f.out() if f else None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 행렬 ══════════
def M2(a):
    """행렬 글자 — 빈칸 없이(물음 줄 바꿈이 행렬을 쪼개지 않게)"""
    return "⟦" + ";".join(",".join(N(v) for v in r) for r in a) + "⟧"

def mat():
    S = Set("matrix", "행렬 — 덧셈 · 실수배 · 곱셈", "행렬",
            {1: "행렬의 성분", 2: "덧셈 · 뺄셈 · 실수배", 3: "행렬의 곱셈", 4: "서로 같은 행렬", 5: "행렬의 거듭제곱"},
            pp=8,
            tips={1: "a_{ij}는 i행 j열의 성분 — 행은 가로줄, 열은 세로줄",
                  2: "같은 자리의 성분끼리 더하고 빼요. 실수배는 모든 성분에 곱해요",
                  3: "AB의 (i, j) 성분 = A의 i행과 B의 j열의 성분을 차례로 곱해 더한 값",
                  4: "크기가 같고 대응하는 성분이 모두 같으면 서로 같은 행렬",
                  5: "A^{2} = AA — 곱셈은 교환법칙이 성립하지 않아요(AB ≠ BA일 수 있어요)"},
            note="행렬의 곱셈은 ‘행 × 열’ 손가락 짚기로 익히게 해 주세요. 성분마다 어느 행과 어느 열을 곱하는지 그림에 화살표로 보여 줘요.")
    R = rng(2202)

    def rm(lo=-5, hi=6):
        return [[R.randint(lo, hi), R.randint(lo, hi)], [R.randint(lo, hi), R.randint(lo, hi)]]

    def mfig(pairs, at="q"):
        f = Fig()
        for i, (nm_, m_) in enumerate(pairs):
            f.text(80, 220 + i * 200, f"{nm_} = {M2(m_)}", z=48, a="s", at=at)
        return f

    def g1():
        k = S.count(1) % 2
        if k == 0:
            r, c = R.choice([(2, 3), (3, 2), (2, 2), (3, 3)])
            p, q_ = R.randint(1, 3), R.randint(-2, 3)
            A = [[p * i + q_ * j for j in range(1, c + 1)] for i in range(1, r + 1)]
            q = f"{r} × {c} 행렬 A의 (i, j) 성분이 a_{{ij}} = {p if p > 1 else ''}i {'+' if q_ >= 0 else MI} {abs(q_) if abs(q_) != 1 else ''}j일 때, 행렬 A를 구하세요." if q_ else f"{r} × {c} 행렬 A의 (i, j) 성분이 a_{{ij}} = {p if p > 1 else ''}i일 때, 행렬 A를 구하세요."
            lines = [L(f"a_{{11}} = {A[0][0]}, a_{{12}} = {A[0][1]}", memo="i행 j열에 i, j를 넣어요"), L(f"A = {M2(A)}")]
            S.add(1, q, M2(A), "성분마다 i, j를 대입", lines, None, omr="ex", key=q)
        else:
            A = [[R.randint(-9, 9) for _ in range(3)] for _ in range(2)]
            i, j = R.randint(1, 2), R.randint(1, 3)
            if (i, j) == (2, 1):
                return
            f = None
            q = f"행렬 A = {M2(A)}에서 a_{{21}} + a_{{{i}{j}}}의 값을 구하세요."
            v = A[1][0] + A[i - 1][j - 1]
            lines = [L(f"a_{{21}} = {N(A[1][0])}", memo="2행 1열"), L(f"a_{{{i}{j}}} = {N(A[i - 1][j - 1])}", memo=f"{i}행 {j}열"), L(f"{N(A[1][0])} + {NP(A[i - 1][j - 1])} = {N(v)}")]
            S.add(1, q, N(v), "행(가로) 먼저, 열(세로) 나중", lines, None, key=q)
    fill(S, 1, 20, g1)

    def g2():
        A, B = rm(), rm()
        p, q_ = R.randint(1, 3), R.randint(1, 3)
        sgn = R.choice([1, -1])
        C = [[p * A[i][j] + sgn * q_ * B[i][j] for j in range(2)] for i in range(2)]
        ex = f"{p if p > 1 else ''}A {'+' if sgn > 0 else MI} {q_ if q_ > 1 else ''}B"
        q = f"A = {M2(A)}, B = {M2(B)}일 때, {J(ex, '을', '를')} 구하세요."
        lines = [L(f"{p if p > 1 else ''}A = {M2([[p * v for v in r] for r in A])}", memo="모든 성분에 곱해요"), L(f"{q_ if q_ > 1 else ''}B = {M2([[q_ * v for v in r] for r in B])}"), L(f"{ex} = {M2(C)}", memo="같은 자리끼리")]
        S.add(2, q, M2(C), "실수배는 모든 성분에, 덧셈은 같은 자리끼리", lines, None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        A = rm(-4, 5)
        if k == 0:
            B = rm(-4, 5)
            C = [[A[i][0] * B[0][j] + A[i][1] * B[1][j] for j in range(2)] for i in range(2)]
            q = f"A = {M2(A)}, B = {M2(B)}일 때, AB를 구하세요."
            el = lambda i, j: f"{NP(A[i][0])} × {NP(B[0][j])} + {NP(A[i][1])} × {NP(B[1][j])} = {N(C[i][j])}"
            lines = [L(el(0, 0), pre="(1, 1)", memo="1행 × 1열"), L(el(0, 1), pre="(1, 2)", memo="1행 × 2열"), L(el(1, 0), pre="(2, 1)"), L(el(1, 1), pre="(2, 2)"), L(f"AB = {M2(C)}")]
            ans = M2(C)
            key = q + M2(A) + M2(B)
        else:
            v = [[R.randint(-5, 5)], [R.randint(-5, 5)]]
            C = [[A[i][0] * v[0][0] + A[i][1] * v[1][0]] for i in range(2)]
            q = f"A = {M2(A)}, X = {M2(v)}일 때, AX를 구하세요."
            lines = [L(f"{NP(A[0][0])} × {NP(v[0][0])} + {NP(A[0][1])} × {NP(v[1][0])} = {N(C[0][0])}", pre="1행", memo="1행 × 열"), L(f"{NP(A[1][0])} × {NP(v[0][0])} + {NP(A[1][1])} × {NP(v[1][0])} = {N(C[1][0])}", pre="2행"), L(f"AX = {M2(C)}")]
            ans = M2(C)
            key = q + M2(A) + M2(v)
        S.add(3, q, ans, "행 × 열 — 짚어 가며 곱해 더해요", lines, None, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        xv, yv = R.randint(-5, 5), R.randint(-5, 5)
        p, q_ = R.randint(1, 3), R.randint(1, 3)
        a11, a22 = xv + yv, p * xv - q_ * yv
        b = R.randint(-6, 6)
        q = f"⟦x+y,{N(b)};3,{p if p > 1 else ''}x−{q_ if q_ > 1 else ''}y⟧ = ⟦{N(a11)},{N(b)};3,{N(a22)}⟧일 때, x, y의 값을 구하세요."
        lines = [L(f"x + y = {N(a11)}", memo="(1, 1) 성분끼리"), L(f"{p if p > 1 else ''}x − {q_ if q_ > 1 else ''}y = {N(a22)}", memo="(2, 2) 성분끼리"), L(f"x = {N(xv)}, y = {N(yv)}", memo="연립")]
        S.add(4, q, f"x = {N(xv)}, y = {N(yv)}", "대응하는 성분끼리 같다고 놓아요", lines, None, ap=f"x={xv}, y={yv}", omr="ex", sub={"x": xv, "y": yv}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        A = rm(-3, 4)
        A2 = [[A[i][0] * A[0][j] + A[i][1] * A[1][j] for j in range(2)] for i in range(2)]
        if k == 0:
            q = f"A = {M2(A)}일 때, A^{{2}}을 구하세요."
            lines = [L("A^{2} = AA", memo="행 × 열"), L(f"{NP(A[0][0])} × {NP(A[0][0])} + {NP(A[0][1])} × {NP(A[1][0])} = {N(A2[0][0])}", pre="(1, 1)"), L(f"A^{{2}} = {M2(A2)}")]
            S.add(5, q, M2(A2), "A^{2} = AA", lines, None, omr="ex", key=q)
        else:
            A3 = [[A2[i][0] * A[0][j] + A2[i][1] * A[1][j] for j in range(2)] for i in range(2)]
            q = f"A = {M2(A)}일 때, A^{{3}}의 (1, 2) 성분을 구하세요."
            lines = [L(f"A^{{2}} = {M2(A2)}"), L(f"A^{{3}} = A^{{2}}A의 (1, 2) 성분: {NP(A2[0][0])} × {NP(A[0][1])} + {NP(A2[0][1])} × {NP(A[1][1])} = {N(A3[0][1])}")]
            S.add(5, q, N(A3[0][1]), "A^{2}을 먼저 — A^{3} = A^{2}A", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 점과 직선 ══════════
def line():
    S = Set("line", "점과 직선 — 거리 · 내분점 · 직선의 방정식", "점과 직선",
            {1: "두 점 사이의 거리", 2: "내분점과 무게중심", 3: "직선의 방정식", 4: "두 직선의 평행과 수직", 5: "점과 직선 사이의 거리"},
            mixed=True, pp=8,
            tips={1: "AB = √{(x_{2} − x_{1})^{2} + (y_{2} − y_{1})^{2}}",
                  2: "m : n 내분점 ({mx_{2} + nx_{1}/m + n}, {my_{2} + ny_{1}/m + n}) · 무게중심은 세 좌표의 평균",
                  3: "기울기 m, 점 (x_{1}, y_{1}) → y − y_{1} = m(x − x_{1})",
                  4: "평행: 기울기가 같고 y절편이 달라요 · 수직: 기울기의 곱이 −1",
                  5: "점 (x_{1}, y_{1})과 직선 ax + by + c = 0 사이의 거리 = {|ax_{1} + by_{1} + c|/√{a^{2} + b^{2}}}"},
            note="좌표평면 위의 거리 · 내분점 · 직선은 모두 그림에서 직각삼각형과 닮음으로 설명할 수 있어요. 공식을 쓰기 전에 그림을 그리게 해 주세요.")
    R = rng(2203)

    def g1():
        x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
        dx, dy = R.randint(-7, 7), R.randint(-7, 7)
        if dx == 0 or dy == 0:
            return
        x2, y2 = x1 + dx, y1 + dy
        if abs(x2) > 7 or abs(y2) > 7:
            return
        d2 = dx * dx + dy * dy
        f = Fig()
        pl = plane(f)
        pl.pt(x1, y1, label=f"A{P_(x1, y1)}", pos="sw" if dx > 0 else "se")
        pl.pt(x2, y2, label=f"B{P_(x2, y2)}", pos="ne" if dx > 0 else "nw")
        f.line(*pl.P(x1, y1), *pl.P(x2, y1), c="teal", w=3, d=True, at=0)
        f.line(*pl.P(x2, y1), *pl.P(x2, y2), c="coral", w=3, d=True, at=0)
        f.line(*pl.P(x1, y1), *pl.P(x2, y2), c="gold", w=3.5, at=1)
        q = f"두 점 A{P_(x1, y1)}, B{P_(x2, y2)} 사이의 거리를 구하세요."
        lines = [L(f"AB^{{2}} = ({N(x2)} − {NP(x1)})^{{2}} + ({N(y2)} − {NP(y1)})^{{2}} = {d2}"), L(f"AB = √{{{d2}}}" + (f" = {RTn(d2)}" if RTn(d2) != f"√{{{d2}}}" else ""))]
        S.add(1, q, RTn(d2), "x좌표의 차, y좌표의 차로 직각삼각형", lines, f.out(), omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            m, n = R.randint(1, 4), R.randint(1, 4)
            x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
            x2, y2 = R.randint(-6, 6), R.randint(-6, 6)
            px, py = Fr(m * x2 + n * x1, m + n), Fr(m * y2 + n * y1, m + n)
            if px.denominator != 1 or py.denominator != 1 or (x1, y1) == (x2, y2):
                return
            q = f"두 점 A{P_(x1, y1)}, B{P_(x2, y2)}에 대하여 선분 AB를 {m} : {n}으로 내분하는 점의 좌표를 구하세요."
            lines = [L(f"x = {{{m} × {NP(x2)} + {n} × {NP(x1)}/{m} + {n}}} = {N(px)}"), L(f"y = {{{m} × {NP(y2)} + {n} × {NP(y1)}/{m} + {n}}} = {N(py)}"), L(f"{P_(px, py)}")]
            f = Fig()
            pl = plane(f)
            pl.pt(x1, y1, label="A", pos="nw"); pl.pt(x2, y2, label="B", pos="ne")
            f.line(*pl.P(x1, y1), *pl.P(x2, y2), c="ink", w=3)
            pl.pt(px, py, label="P", pos="s", f="coral", at=2)
            S.add(2, q, P_(px, py), "m : n 내분점 — 가중 평균", lines, f.out(), omr="pt", key=q)
        else:
            pts = [(R.randint(-6, 6), R.randint(-6, 6)) for _ in range(3)]
            sx, sy = sum(p[0] for p in pts), sum(p[1] for p in pts)
            if sx % 3 or sy % 3:
                return
            gx, gy = sx // 3, sy // 3
            q = f"세 점 A{P_(*pts[0])}, B{P_(*pts[1])}, {J('C' + P_(*pts[2]), '을', '를')} 꼭짓점으로 하는 삼각형 ABC의 무게중심의 좌표를 구하세요."
            lines = [L(f"x = {{{' + '.join(N(p[0]) for p in pts)}/3}} = {N(gx)}"), L(f"y = {{{' + '.join(N(p[1]) for p in pts)}/3}} = {N(gy)}"), L(P_(gx, gy))]
            f = Fig()
            pl = plane(f)
            f.poly([pl.P(*p) for p in pts], c="ink", w=3, f="gold", fo=0.12)
            pl.pt(gx, gy, label="G", pos="ne", f="coral", at=2)
            S.add(2, q, P_(gx, gy), "무게중심 = 세 꼭짓점 좌표의 평균", lines, f.out(), omr="pt", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        m = Fr(R.choice([-3, -2, -1, 1, 2, 3]), R.choice([1, 1, 2]))
        x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
        b = y1 - m * x1
        if b.denominator != 1:
            return
        ans = f"y = {FR(m) if m not in (1, -1) else ('' if m == 1 else MI)}x" + (f" {'+' if b > 0 else MI} {FR(abs(b))}" if b else "")
        if k == 0:
            q = f"점 {P_(x1, y1)}을 지나고 기울기가 {FR(m)}인 직선의 방정식을 구하세요." if bat(N(y1)) else f"점 {P_(x1, y1)}를 지나고 기울기가 {FR(m)}인 직선의 방정식을 구하세요."
            lines = [L(f"y − {NP(y1)} = {FR(m)}(x − {NP(x1)})", memo="y − y_{1} = m(x − x_{1})"), L(ans)]
        else:
            x2 = x1 + R.choice([1, 2, 3, -2])
            y2 = m * x2 + b
            if y2.denominator != 1:
                return
            q = f"두 점 {P_(x1, y1)}, {P_(x2, y2)}{'을' if bat(N(y2)) else '를'} 지나는 직선의 방정식을 구하세요."
            lines = [L(f"기울기 {{{N(y2)} − {NP(y1)}/{N(x2)} − {NP(x1)}}} = {FR(m)}"), L(f"y − {NP(y1)} = {FR(m)}(x − {NP(x1)})"), L(ans)]
        f = Fig()
        pl = plane(f)
        pl.pt(x1, y1, label=P_(x1, y1), pos="ne")
        pl.lineq(float(m), float(b), at=len(lines) - 1)
        S.add(3, q, ans, "y − y_{1} = m(x − x_{1})", lines, f.out(), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        m1 = Fr(R.choice([-3, -2, -1, 1, 2, 3]), R.choice([1, 2]))
        if k == 0:
            a = m1
            q = f"두 직선 y = ax + 3과 y = {FR(m1)}x − 1이 서로 평행할 때, 상수 a의 값을 구하세요."
            lines = [L("평행 → 기울기가 같아요", memo="y절편은 3, −1로 달라요"), L(f"a = {FR(m1)}")]
        else:
            a = -1 / m1
            q = f"두 직선 y = ax + 2와 y = {FR(m1)}x + 5가 서로 수직일 때, 상수 a의 값을 구하세요."
            lines = [L(f"a × {('(' + FR(m1) + ')') if m1 < 0 else FR(m1)} = −1", memo="수직 → 기울기의 곱이 −1"), L(f"a = {FR(a)}")]
        S.add(4, q, FR(a), "평행: 기울기 같음 · 수직: 기울기 곱 −1", lines, None, sub={"a": a}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        a, b = R.choice([(3, 4), (4, 3), (5, 12), (12, 5), (1, 1), (1, 2), (2, 1), (6, 8)])
        a *= R.choice([1, -1])
        c = R.randint(-15, 15)
        x1, y1 = R.randint(-5, 5), R.randint(-5, 5)
        num = abs(a * x1 + b * y1 + c)
        d2 = a * a + b * b
        o, i = sq(d2)
        if num == 0:
            return
        if i == 1:
            v = Fr(num, o)
            ans = FR(v)
        else:
            g = gcd(num, o)
            n2, o2 = num // g, o // g
            if i != 1:
                n3 = num * 1
                den = o * i
                g2 = gcd(n3, den)
                ans = f"{{{n3 // g2 if n3 // g2 > 1 else ''}√{{{i}}}/{den // g2}}}" if den // g2 > 1 else f"{n3 // g2 if n3 // g2 > 1 else ''}√{{{i}}}"
        eq = f"{mono(a, 'x', 1, first=True)}{mono(b, 'y', 1)}{mono(c, '', 1) if c else ''} = 0"
        q = f"점 {P_(x1, y1)}과 직선 {eq} 사이의 거리를 구하세요." if bat(N(y1)) else f"점 {P_(x1, y1)}와 직선 {eq} 사이의 거리를 구하세요."
        lines = [L(f"{{|{N(a)} × {NP(x1)} + {N(b)} × {NP(y1)} + {NP(c)}|/√{{{NP(a)}^{{2}} + {b}^{{2}}}}}}", memo="점과 직선 사이의 거리"), L(f"{{{num}/√{{{d2}}}}} = {ans}")]
        S.add(5, q, ans, "{|ax_{1} + by_{1} + c|/√{a^{2} + b^{2}}}", lines, None, omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 원의 방정식 ══════════
def circ_eq(a, b, r2):
    xa = f"(x {'+' if -a > 0 else MI} {abs(a)})^{{2}}" if a else "x^{2}"
    yb = f"(y {'+' if -b > 0 else MI} {abs(b)})^{{2}}" if b else "y^{2}"
    return f"{xa} + {yb} = {r2}"

def circle():
    S = Set("circle", "원의 방정식 — 중심과 반지름, 원과 직선", "원의 방정식",
            {1: "중심과 반지름으로 방정식", 2: "일반형에서 중심과 반지름", 3: "조건으로 원 정하기", 4: "원과 직선의 위치 관계", 5: "원의 접선의 방정식"},
            mixed=True, pp=8,
            tips={1: "중심 (a, b), 반지름 r → (x − a)^{2} + (y − b)^{2} = r^{2}",
                  2: "x끼리, y끼리 완전제곱식으로 묶어요",
                  3: "지름의 양 끝 → 중심은 중점, 반지름은 거리의 절반 · x축에 접하면 반지름 = |중심의 y좌표|",
                  4: "중심과 직선 사이의 거리 d와 반지름 r — d < r 두 점, d = r 접함, d > r 만나지 않음",
                  5: "원 x^{2} + y^{2} = r^{2} 위의 점 (x_{1}, y_{1})에서의 접선: x_{1}x + y_{1}y = r^{2}"},
            note="원의 방정식은 ‘중심까지의 거리가 r인 점들’이라는 뜻에서 출발해요. 위치 관계는 판별식보다 ‘중심과 직선 사이의 거리’ 그림이 훨씬 빨라요.")
    R = rng(2204)

    def g1():
        a, b, r = R.randint(-5, 5), R.randint(-5, 5), R.randint(1, 6)
        f = Fig()
        pl = plane(f, -8, 8)
        f.circ(*pl.P(a, b), pl.sx * r, c="sky", sw=3.5, at=1)
        pl.pt(a, b, label=f"({N(a)}, {N(b)})", pos="ne")
        q = f"중심이 ({N(a)}, {N(b)})이고 반지름의 길이가 {r}인 원의 방정식을 구하세요."
        lines = [L("(x − a)^{2} + (y − b)^{2} = r^{2}"), L(circ_eq(a, b, r * r))]
        S.add(1, q, circ_eq(a, b, r * r), "중심 (a, b), 반지름 r", lines, f.out(), omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        a, b, r = R.randint(-5, 5), R.randint(-5, 5), R.randint(1, 6)
        if a == 0 and b == 0:
            return
        c = a * a + b * b - r * r
        E = x ** 2 + y ** 2 - 2 * a * x - 2 * b * y + c
        Es = "x^{2} + y^{2}" + "".join(t for t in (mono(-2 * a, "x", 1), mono(-2 * b, "y", 1), mono(c, "", 1)) if t)
        q = f"원 {Es} = 0의 중심의 좌표와 반지름의 길이를 구하세요."
        lines = [L(f"(x^{{2}} {'+' if -2 * a >= 0 else MI} {abs(2 * a)}x + {a * a}) + (y^{{2}} {'+' if -2 * b >= 0 else MI} {abs(2 * b)}y + {b * b}) = {N(-c)} + {a * a} + {b * b}", memo="x끼리, y끼리 완전제곱식"), L(circ_eq(a, b, r * r)), L(f"중심 ({N(a)}, {N(b)}), 반지름 {r}")]
        S.add(2, q, f"중심 ({N(a)}, {N(b)}), 반지름 {r}", "완전제곱식으로 묶어 표준형으로", lines, None, ap=f"({a}, {b}), {r}", omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        if k == 0:
            x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
            x2, y2 = R.randint(-6, 6), R.randint(-6, 6)
            if (x1 + x2) % 2 or (y1 + y2) % 2 or (x1, y1) == (x2, y2):
                return
            a, b = (x1 + x2) // 2, (y1 + y2) // 2
            r2 = (x1 - a) ** 2 + (y1 - b) ** 2
            q = f"두 점 A{P_(x1, y1)}, B{P_(x2, y2)}를 지름의 양 끝으로 하는 원의 방정식을 구하세요." if not bat(N(y2)) else f"두 점 A{P_(x1, y1)}, B{P_(x2, y2)}을 지름의 양 끝으로 하는 원의 방정식을 구하세요."
            lines = [L(f"중심 = AB의 중점 ({N(a)}, {N(b)})"), L(f"r^{{2}} = ({N(x1)} − {NP(a)})^{{2}} + ({N(y1)} − {NP(b)})^{{2}} = {r2}", memo="중심에서 A까지"), L(circ_eq(a, b, r2))]
        else:
            a, b = R.randint(-5, 5), R.choice([v for v in range(-5, 6) if v])
            r2 = b * b
            q = f"중심이 ({N(a)}, {N(b)})이고 x축에 접하는 원의 방정식을 구하세요."
            lines = [L(f"반지름 = |중심의 y좌표| = {abs(b)}", memo="x축에 접해요"), L(circ_eq(a, b, r2))]
        S.add(3, q, circ_eq(a, b, r2), "중심과 반지름부터 정해요", lines, None, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.randint(-3, 3), R.randint(-3, 3)
        r = R.randint(2, 5)
        A_, B_ = R.choice([(3, 4), (4, 3), (1, 0), (0, 1), (5, 12), (12, 5)])
        A_ *= R.choice([1, -1])
        n = math.isqrt(A_ * A_ + B_ * B_)
        dist_num = R.choice([r * n - R.randint(1, 3), r * n, r * n + R.randint(1, 3)])
        sgn = R.choice([1, -1])
        c = sgn * dist_num - A_ * a - B_ * b
        d = Fr(abs(A_ * a + B_ * b + c), n)
        rel = "두 점에서 만나요" if d < r else ("한 점에서 만나요(접해요)" if d == r else "만나지 않아요")
        cnt = 2 if d < r else (1 if d == r else 0)
        eq = f"{mono(A_, 'x', 1, first=True)}{mono(B_, 'y', 1)}{mono(c, '', 1) if c else ''} = 0" if A_ else f"{mono(B_, 'y', 1, first=True)}{mono(c, '', 1) if c else ''} = 0"
        q = f"원 {wa(circ_eq(a, b, r * r))} 직선 {eq}의 교점의 개수를 구하세요."
        lines = [L(f"중심 ({N(a)}, {N(b)}), 반지름 {r}"), L(f"d = {{|{N(A_)} × {NP(a)} + {N(B_)} × {NP(b)} + {NP(c)}|/{n}}} = {FR(d)}", memo="중심과 직선 사이의 거리"), L(f"d {'<' if d < r else ('=' if d == r else '>')} r → {rel}"), L(f"{cnt}개")]
        f = Fig()
        pl = plane(f, -9, 9)
        f.circ(*pl.P(a, b), pl.sx * r, c="sky", sw=3.5)
        if B_:
            pl.lineq(-A_ / B_, -c / B_, c="coral", at=0)
        else:
            f.line(*pl.P(-c / A_, -9), *pl.P(-c / A_, 9), c="coral", w=4, at=0)
        S.add(4, q, f"{cnt}개", "중심과 직선 사이의 거리 d와 반지름 r 비교", lines, f.out(), ap=str(cnt), key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        if k == 0:
            pts = [(3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (8, 6), (1, 2), (2, 1), (1, 1), (2, 2), (1, 3), (3, 1)]
            x1, y1 = R.choice(pts)
            x1 *= R.choice([1, -1]); y1 *= R.choice([1, -1])
            r2 = x1 * x1 + y1 * y1
            q = f"원 x^{{2}} + y^{{2}} = {r2} 위의 점 {P_(x1, y1)}에서의 접선의 방정식을 구하세요."
            ans = f"{mono(x1, 'x', 1, first=True)}{mono(y1, 'y', 1)} = {r2}"
            lines = [L("x_{1}x + y_{1}y = r^{2}", memo="원 위의 점에서의 접선"), L(ans)]
            f = Fig()
            lim = max(abs(x1), abs(y1)) + 4
            pl = plane(f, -lim, lim)
            f.circ(*pl.P(0, 0), pl.sx * math.sqrt(r2), c="sky", sw=3.5)
            pl.pt(x1, y1, label=P_(x1, y1), pos="ne" if x1 > 0 else "nw")
            if y1:
                pl.lineq(-x1 / y1, r2 / y1, c="coral", at=1)
            S.add(5, q, ans, "원 위의 점에서의 접선 x_{1}x + y_{1}y = r^{2}", lines, f.out(), omr="ex", key=q)
        else:
            m = R.choice([1, 2, 3, -1, -2, Fr(3, 4), Fr(4, 3)])
            r = R.randint(1, 5)
            k2 = r * r * (m * m + 1)
            o, i = sq(int(k2)) if Fr(k2).denominator == 1 else (None, None)
            if o is None:
                return
            nm_ = f"{FR(m) if m not in (1, -1) else ('' if m == 1 else MI)}x"
            if i == 1:
                ans = f"y = {nm_} ± {o}"
            else:
                ans = f"y = {nm_} ± {o if o > 1 else ''}√{{{i}}}"
            q = f"원 x^{{2}} + y^{{2}} = {r * r}에 접하고 기울기가 {FR(m)}인 직선의 방정식을 구하세요."
            lines = [L(f"y = {nm_} + n으로 놓기"), L(f"{{|n|/√{{({FR(m)})^{{2}} + 1}}}} = {r}", memo="중심과 직선 사이의 거리 = 반지름"), L(ans)]
            S.add(5, q, ans, "y = mx ± r√{m^{2} + 1}", lines, None, omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 도형의 이동 ══════════
def move():
    S = Set("move", "도형의 이동 — 평행이동과 대칭이동", "도형의 이동",
            {1: "점의 평행이동", 2: "도형의 평행이동", 3: "점의 대칭이동", 4: "도형의 대칭이동", 5: "대칭이동과 최단 거리"},
            pp=8,
            tips={1: "(x, y)를 x축 방향으로 a, y축 방향으로 b만큼 → (x + a, y + b)",
                  2: "도형 f(x, y) = 0을 평행이동 → f(x − a, y − b) = 0 (부호 반대로!)",
                  3: "x축: (x, −y) · y축: (−x, y) · 원점: (−x, −y) · 직선 y = x: (y, x)",
                  4: "도형의 대칭이동도 x, y를 같은 규칙으로 바꿔 넣어요",
                  5: "한쪽 점을 대칭이동하면 꺾인 길이 곧은 선이 돼요"},
            note="점은 ‘더하고’, 도형의 식은 ‘빼서 넣는다’는 차이가 가장 헷갈려요. 이동한 도형 위의 점을 거꾸로 옮기면 원래 도형 위에 있다는 생각으로 설명해 주세요.")
    R = rng(2205)

    def g1():
        x1, y1, a, b = (R.randint(-5, 5) for _ in range(4))
        if a == 0 and b == 0:
            return
        f = Fig()
        m = max(7, abs(x1 + a) + 1, abs(y1 + b) + 1)          # 옮긴 점이 좌표평면 밖으로 나가지 않게
        pl = plane(f, -m, m)
        pl.pt(x1, y1, label=P_(x1, y1), pos="nw")
        pl.pt(x1 + a, y1 + b, label=P_(x1 + a, y1 + b), pos="ne", f="coral", at=1)
        f.line(*pl.P(x1, y1), *pl.P(x1 + a, y1 + b), c="teal", w=3, ar=1, at=0)
        q = f"점 {P_(x1, y1)}를 x축의 방향으로 {N(a)}만큼, y축의 방향으로 {N(b)}만큼 평행이동한 점의 좌표를 구하세요." if not bat(N(y1)) else f"점 {P_(x1, y1)}을 x축의 방향으로 {N(a)}만큼, y축의 방향으로 {N(b)}만큼 평행이동한 점의 좌표를 구하세요."
        lines = [L(f"({N(x1)} + {NP(a)}, {N(y1)} + {NP(b)})", memo="좌표에 더해요"), L(P_(x1 + a, y1 + b))]
        S.add(1, q, P_(x1 + a, y1 + b), "점은 (x + a, y + b)", lines, f.out(), omr="pt", key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        a, b = R.randint(-4, 4), R.randint(-4, 4)
        if a == 0 or b == 0:
            return
        if k == 0:
            m, c = R.choice([-3, -2, -1, 1, 2, 3]), R.randint(-5, 5)
            new_c = c - m * a + b
            q = f"직선 {J('y = ' + mono(m, 'x', 1, first=True) + (mono(c, '', 1) if c else ''), '을', '를')} x축의 방향으로 {N(a)}만큼, y축의 방향으로 {N(b)}만큼 평행이동한 직선의 방정식을 구하세요."
            ans = f"y = {mono(m, 'x', 1, first=True)}{mono(new_c, '', 1) if new_c else ''}"
            lines = [L(f"x 대신 x − {NP(a)}, y 대신 y − {NP(b)}", memo="식은 부호 반대로"), L(f"y − {NP(b)} = {N(m) if m not in (1, -1) else ('' if m == 1 else MI)}(x − {NP(a)}){mono(c, '', 1) if c else ''}"), L(ans)]
        else:
            p, q_, r = R.randint(-3, 3), R.randint(-3, 3), R.randint(1, 5)
            ans = circ_eq(p + a, q_ + b, r * r)
            q = f"원 {J(circ_eq(p, q_, r * r), '을', '를')} x축의 방향으로 {N(a)}만큼, y축의 방향으로 {N(b)}만큼 평행이동한 원의 방정식을 구하세요."
            lines = [L(f"중심 ({N(p)}, {N(q_)}) → ({N(p + a)}, {N(q_ + b)})", memo="원은 중심만 옮겨요"), L("반지름은 그대로"), L(ans)]
        S.add(2, q, ans, "도형의 식 → x − a, y − b를 넣어요", lines, None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        x1, y1 = R.randint(-6, 6), R.randint(-6, 6)
        if x1 == 0 or y1 == 0 or x1 == y1:
            return
        kind = ["x축", "y축", "원점", "직선 y = x"][S.count(3) % 4]
        X, Y = {"x축": (x1, -y1), "y축": (-x1, y1), "원점": (-x1, -y1), "직선 y = x": (y1, x1)}[kind]
        f = Fig()
        pl = plane(f)
        if kind == "직선 y = x":
            pl.lineq(1, 0, c="soft", d=True)
        pl.pt(x1, y1, label=P_(x1, y1), pos="ne" if x1 > 0 else "nw")
        pl.pt(X, Y, label=P_(X, Y), pos="ne" if X > 0 else "nw", f="coral", at=1)
        f.line(*pl.P(x1, y1), *pl.P(X, Y), c="teal", w=2.5, d=True, at=0)
        rule_ = {"x축": "(x, −y)", "y축": "(−x, y)", "원점": "(−x, −y)", "직선 y = x": "(y, x)"}[kind]
        q = f"점 {P_(x1, y1)}를 {kind}에 대하여 대칭이동한 점의 좌표를 구하세요." if not bat(N(y1)) else f"점 {P_(x1, y1)}을 {kind}에 대하여 대칭이동한 점의 좌표를 구하세요."
        lines = [L(f"{kind} 대칭 → {rule_}"), L(P_(X, Y))]
        S.add(3, q, P_(X, Y), f"{kind} 대칭은 {rule_}", lines, f.out(), omr="pt", key=q)
    fill(S, 3, 20, g3)

    def g4():
        kind = ["x축", "y축", "원점", "직선 y = x"][S.count(4) % 4]
        m, c = R.choice([-3, -2, 2, 3, Fr(1, 2)]), R.randint(-5, 5)
        if c == 0:
            return
        # y = mx + c
        if kind == "x축":
            nm, nc = -m, -c
        elif kind == "y축":
            nm, nc = -m, c
        elif kind == "원점":
            nm, nc = m, -c
        else:
            nm, nc = 1 / Fr(m), -Fr(c) / m
        orig = f"y = {FR(m) if m not in (1, -1) else ''}x{mono(c, '', 1)}"
        ans = f"y = {FR(nm) if nm not in (1, -1) else ('' if nm == 1 else MI)}x" + (f" {'+' if nc > 0 else MI} {FR(abs(nc))}" if nc else "")
        sub_rule = {"x축": "y 대신 −y", "y축": "x 대신 −x", "원점": "x 대신 −x, y 대신 −y", "직선 y = x": "x와 y를 바꿔요"}[kind]
        q = f"직선 {J(orig, '을', '를')} {kind}에 대하여 대칭이동한 직선의 방정식을 구하세요."
        lines = [L(sub_rule, memo="도형의 대칭이동"), L(ans)]
        S.add(4, q, ans, "대칭이동 규칙대로 x, y를 바꿔 넣어요", lines, None, omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        ax_, ay_ = R.randint(-4, 2), R.randint(1, 5)
        bx_, by_ = R.randint(1, 6), R.randint(1, 5)
        if ax_ == bx_:
            return
        d2 = (bx_ - ax_) ** 2 + (by_ + ay_) ** 2
        q = f"두 점 A{P_(ax_, ay_)}, {wa('B' + P_(bx_, by_))} x축 위의 점 P에 대하여 AP + PB의 최솟값을 구하세요."
        lines = [L(f"A를 x축에 대칭 → A'{P_(ax_, -ay_)}", memo="AP = A'P"), L(f"AP + PB = A'P + PB ≥ A'B", memo="곧은 선일 때 최소"), L(f"A'B = √{{({N(bx_)} − {NP(ax_)})^{{2}} + ({N(by_)} − {NP(-ay_)})^{{2}}}} = {RTn(d2)}")]
        f = Fig()
        pl = plane(f)
        pl.pt(ax_, ay_, label="A", pos="nw"); pl.pt(bx_, by_, label="B", pos="ne")
        pl.pt(ax_, -ay_, label="A'", pos="sw", f="coral", at=0)
        f.line(*pl.P(ax_, -ay_), *pl.P(bx_, by_), c="gold", w=3.5, at=1)
        S.add(5, q, RTn(d2), "한 점을 대칭이동해 꺾인 길을 곧게", lines, f.out(), omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 집합과 명제 ══════════
def sset(xs):
    return "{" + ", ".join(map(str, sorted(xs))) + "}" if xs else "∅"

def venn(f, at="q", la="A", lb="B"):
    f.rect(70, 110, 520, 440, c="ink", sw=2.5, at=at)
    f.text(90, 145, "U", z=26, c="soft", a="s", at=at)
    f.circ(260, 330, 160, c="gold", sw=3, f="gold", fo=0.12, at=at)
    f.circ(400, 330, 160, c="teal", sw=3, f="teal", fo=0.12, at=at)
    f.text(170, 190, la, z=30, c="gold", b=700, at=at)
    f.text(490, 190, lb, z=30, c="teal", b=700, at=at)

def set_():
    S = Set("set", "집합과 명제 — 원소의 개수 · 연산 · 진리집합", "집합과 명제",
            {1: "합집합의 원소의 개수", 2: "집합의 연산", 3: "부분집합의 개수", 4: "명제와 진리집합", 5: "충분조건 · 필요조건"},
            pp=8,
            tips={1: "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)",
                  2: "A ∩ B 공통 · A ∪ B 모두 · A − B는 A에만 · A^{C}는 U에서 A 빼기",
                  3: "원소가 n개인 집합의 부분집합 2^{n}개 · 특정 원소 k개를 반드시 포함(제외)하면 2^{n − k}개",
                  4: "p → q가 참 ⇔ P ⊂ Q(진리집합)",
                  5: "p ⇒ q면 p는 q이기 위한 충분조건, q는 p이기 위한 필요조건"},
            note="집합 문제는 벤 다이어그램에 원소(또는 개수)를 직접 써 넣게 해 주세요. 명제의 참 · 거짓은 진리집합의 포함 관계(수직선 그림)로 판단하는 것이 가장 확실해요.")
    R = rng(2206)

    def g1():
        k = S.count(1) % 2
        na, nb, ni = R.randint(8, 30), R.randint(8, 30), R.randint(2, 7)
        if ni >= min(na, nb):
            return
        f = Fig()
        venn(f)
        if k == 0:
            v = na + nb - ni
            q = f"두 집합 A, B에 대하여 n(A) = {na}, n(B) = {nb}, n(A ∩ B) = {ni}일 때, n(A ∪ B)를 구하세요."
            f.text(330, 340, str(ni), z=34, b=700, at=0)
            lines = [L("n(A ∪ B) = n(A) + n(B) − n(A ∩ B)", memo="공통부분을 두 번 세지 않게"), L(f"{na} + {nb} − {ni} = {v}")]
        else:
            nu = na + nb - ni
            v = ni
            q = f"어느 반 학생 중 수학을 좋아하는 학생이 {na}명, 과학을 좋아하는 학생이 {nb}명, 둘 중 하나 이상을 좋아하는 학생이 {nu}명일 때, 둘 다 좋아하는 학생은 몇 명인가요?"
            lines = [L(f"n(A ∪ B) = {nu}, n(A) = {na}, n(B) = {nb}"), L(f"n(A ∩ B) = {na} + {nb} − {nu} = {v}")]
        S.add(1, q, str(v) if k == 0 else f"{v}명", "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)", lines, f.out(), ap=str(v), key=q)
    fill(S, 1, 20, g1)

    def g2():
        Uu = list(range(1, R.randint(8, 12) + 1))
        A = set(R.sample(Uu, R.randint(3, 6)))
        B = set(R.sample(Uu, R.randint(3, 6)))
        if not (A & B) or A == B:
            return
        op = ["∩", "∪", "−", "c"][S.count(2) % 4]
        if op == "∩":
            res, expr = A & B, "A ∩ B"
        elif op == "∪":
            res, expr = A | B, "A ∪ B"
        elif op == "−":
            res, expr = A - B, "A − B"
        else:
            res, expr = set(Uu) - (A | B), "(A ∪ B)^{C}"
        q = f"전체집합 U = {sset(Uu)}의 두 부분집합 A = {sset(A)}, B = {sset(B)}에 대하여 집합 {expr}를 구하세요." if op != "c" else f"전체집합 U = {sset(Uu)}의 두 부분집합 A = {sset(A)}, B = {sset(B)}에 대하여 집합 {expr}을 구하세요."
        memo = {"∩": "공통 원소", "∪": "어느 한쪽이라도", "−": "A에는 있고 B에는 없는", "c": "A ∪ B 밖의 원소"}[op]
        lines = [L(f"A ∪ B = {sset(A | B)}") if op == "c" else L(f"{expr}: {memo}"), L(f"{expr} = {sset(res)}")]
        f = Fig()
        venn(f)
        for i, v in enumerate(sorted(A - B)):
            f.text(190 + (i % 3) * 36, 300 + (i // 3) * 40, str(v), z=26, at=0)
        for i, v in enumerate(sorted(A & B)):
            f.text(310 + (i % 2) * 36, 300 + (i // 2) * 40, str(v), z=26, at=0, c="coral")
        for i, v in enumerate(sorted(B - A)):
            f.text(420 + (i % 3) * 36, 300 + (i // 3) * 40, str(v), z=26, at=0)
        for i, v in enumerate(sorted(set(Uu) - A - B)):
            f.text(100 + i * 40, 520, str(v), z=24, c="soft", at=0)
        S.add(2, q, sset(res), "벤 다이어그램에 원소를 써 넣어요", lines, f.out(), omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        n = R.randint(3, 8)
        Aset = sorted(R.sample(range(1, 16), n)) if R.random() < 0.6 else [2 * i for i in range(1, n + 1)]
        if k == 0:
            v = 2 ** n
            q = f"집합 A = {sset(Aset)}의 부분집합의 개수를 구하세요."
            lines = [L(f"원소 {n}개 — 각 원소를 넣거나 빼거나 2가지"), L(f"2^{{{n}}} = {v}")]
        elif k == 1:
            t = R.randint(1, min(3, n - 1))
            inc = Aset[:t]
            v = 2 ** (n - t)
            q = f"집합 A = {sset(Aset)}의 부분집합 중 {', '.join(map(str, inc))}을 반드시 원소로 갖는 부분집합의 개수를 구하세요." if bat(inc[-1]) else f"집합 A = {sset(Aset)}의 부분집합 중 {', '.join(map(str, inc))}를 반드시 원소로 갖는 부분집합의 개수를 구하세요."
            lines = [L(f"{', '.join(map(str, inc))}{'은' if bat(inc[-1]) else '는'} 이미 넣었다고 보고 나머지 {n - t}개만", memo="정해진 원소는 빼고 세요"), L(f"2^{{{n - t}}} = {v}")]
        else:
            v = 2 ** n - 1
            q = f"집합 A = {sset(Aset)}의 진부분집합의 개수를 구하세요."
            lines = [L(f"부분집합 2^{{{n}}} = {2 ** n}"), L(f"{2 ** n} − 1 = {v}", memo="자기 자신 빼기")]
        S.add(3, q, str(v), "원소마다 넣거나 빼거나 — 2의 거듭제곱", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        r1, r2 = sorted(R.sample(range(-4, 7), 2))
        E = sp.expand((x - r1) * (x - r2))
        Es = sym_poly_str(E)
        k = S.count(4) % 2
        if k == 0:
            q = f"명제 ‘{Es} ≤ 0이면 x ≤ a이다.’가 참이 되도록 하는 실수 a의 최솟값을 구하세요."
            lines = [L(f"P = {{x | {N(r1)} ≤ x ≤ {N(r2)}}}", memo="진리집합"), L("P ⊂ Q = {x | x ≤ a}", memo="p → q가 참 ⇔ P ⊂ Q"), L(f"a ≥ {N(r2)} → 최솟값 {N(r2)}")]
            ans = N(r2)
        else:
            q = f"명제 ‘{Es} ≤ 0이면 x ≥ a이다.’가 참이 되도록 하는 실수 a의 최댓값을 구하세요."
            lines = [L(f"P = {{x | {N(r1)} ≤ x ≤ {N(r2)}}}"), L("P ⊂ Q = {x | x ≥ a}"), L(f"a ≤ {N(r1)} → 최댓값 {N(r1)}")]
            ans = N(r1)
        f = Fig()
        nl = NL(f, r1 - 4, r2 + 4, y=400, lab_step=1)
        f.line(nl.X(r1), 360, nl.X(r2), 360, c="gold", w=6)
        S.add(4, q, ans, "진리집합의 포함 관계 P ⊂ Q", lines, f.out(), key=q)
    fill(S, 4, 20, g4)

    def g5():
        a, b = R.randint(-3, 3), R.randint(1, 4)
        # p: |x − a| < b  →  a − b < x < a + b ; q: −k < x − c < k ... use q: x < m
        k = S.count(5) % 2
        if k == 0:
            q = f"두 조건 p: |x {'+' if -a > 0 else MI} {abs(a)}| < {b}, q: x < k에 대하여 p가 q이기 위한 충분조건이 되도록 하는 실수 k의 최솟값을 구하세요." if a else f"두 조건 p: |x| < {b}, q: x < k에 대하여 p가 q이기 위한 충분조건이 되도록 하는 실수 k의 최솟값을 구하세요."
            lines = [L(f"P = {{x | {N(a - b)} < x < {N(a + b)}}}"), L("p ⇒ q → P ⊂ Q", memo="충분조건"), L(f"k ≥ {N(a + b)} → 최솟값 {N(a + b)}")]
            ans = N(a + b)
        else:
            q = f"두 조건 p: x > k, q: |x {'+' if -a > 0 else MI} {abs(a)}| < {b}에 대하여 p가 q이기 위한 필요조건이 되도록 하는 실수 k의 최댓값을 구하세요." if a else f"두 조건 p: x > k, q: |x| < {b}에 대하여 p가 q이기 위한 필요조건이 되도록 하는 실수 k의 최댓값을 구하세요."
            lines = [L(f"Q = {{x | {N(a - b)} < x < {N(a + b)}}}"), L("q ⇒ p → Q ⊂ P", memo="p가 필요조건"), L(f"k ≤ {N(a - b)} → 최댓값 {N(a - b)}")]
            ans = N(a - b)
        S.add(5, q, ans, "충분조건 · 필요조건은 진리집합의 포함 관계로", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S
