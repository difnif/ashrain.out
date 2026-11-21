# 고등 ⑤ — 확률 · 확률분포 · 수열의 극한과 급수 · 여러 가지 적분법 · 이차곡선 · 벡터
import math
from math import comb
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, Plane, NL, ang_pt
from kit import *
from g_hc import FR, LIN, TAIL, XM, pcurve, gx, bat, ptj
from g_hd import POLY, integ, ev, mulp, plane, shade, SIG, RP

def RT(n):
    """√n 간단히 — 12 → 2√{3}"""
    o, i = 1, n
    p = 2
    while p * p <= i:
        while i % (p * p) == 0:
            i //= p * p
            o *= p
        p += 1
    return str(o) if i == 1 else f"{'' if o == 1 else o}√{{{i}}}"

def SURD(v):
    """sympy 수 a + b√n → 무대 글자"""
    v = sp.nsimplify(sp.radsimp(sp.expand(v)))
    if v.is_Rational:
        return FR(Fr(int(v.p), int(v.q)))
    const, terms = v.as_coeff_add()
    assert len(terms) == 1, v
    c, r = terms[0].as_coeff_Mul()
    assert r.is_Pow and r.exp == sp.Rational(1, 2), v
    n = int(r.base)
    c = Fr(int(sp.Rational(c).p), int(sp.Rational(c).q))
    ac = abs(c)
    if ac.denominator == 1:
        body = f"{'' if ac == 1 else N(ac)}√{{{n}}}"
    else:
        body = f"{{{'' if ac.numerator == 1 else ac.numerator}√{{{n}}}/{ac.denominator}}}"
    const = Fr(int(sp.Rational(const).p), int(sp.Rational(const).q))
    if const == 0:
        return (MI if c < 0 else "") + body
    return f"{FR(const)} {'+' if c > 0 else MI} {body}"

def DEC4(v):
    return f"{v:.4f}"


# ══════════ 확률 ══════════
CTX3 = [("남학생", "여학생", "안경을 쓴 학생", ("안경 씀", "안 씀")),
        ("1학년", "2학년", "동아리에 가입한 학생", ("가입", "미가입")),
        ("남학생", "여학생", "버스로 통학하는 학생", ("버스", "도보")),
        ("남학생", "여학생", "수학을 좋아하는 학생", ("좋아함", "아님")),
        ("1반", "2반", "방과후 수업을 듣는 학생", ("들음", "안 들음"))]

def ptable(f, rows, cols, vals, hl=(), at="q", hl_at=0):
    """2 × 2 표 + 합계 — vals[r][c]"""
    x0, y0, cw, ch = 40, 150, 145, 78
    heads = [""] + list(cols) + ["합계"]
    tot = [[vals[r][0], vals[r][1], vals[r][0] + vals[r][1]] for r in range(2)]
    tot.append([vals[0][0] + vals[1][0], vals[0][1] + vals[1][1], sum(map(sum, vals))])
    names = list(rows) + ["합계"]
    for j, h in enumerate(heads):
        f.rect(x0 + j * cw, y0, cw, ch, c="ink", sw=2, f="gold" if j else None, fo=0.12 if j else None, at=at)
        f.text(x0 + j * cw + cw / 2, y0 + ch / 2 + 10, h, z=26, b=700, at=at)
    for i in range(3):
        y = y0 + (i + 1) * ch
        f.rect(x0, y, cw, ch, c="ink", sw=2, f="gold", fo=0.12, at=at)
        f.text(x0 + cw / 2, y + ch / 2 + 10, names[i], z=26, b=700, at=at)
        for j in range(3):
            f.rect(x0 + (j + 1) * cw, y, cw, ch, c="ink", sw=2, at=at)
            f.text(x0 + (j + 1) * cw + cw / 2, y + ch / 2 + 10, str(tot[i][j]), z=28, at=at)
    for k, (i, j, a_) in enumerate(hl):
        f.rect(x0 + (j + 1) * cw + 4, y0 + (i + 1) * ch + 4, cw - 8, ch - 8, c="coral", sw=4, rx=8, at=a_)

def prob():
    S = Set("prob", "확률 — 덧셈정리 · 조건부확률 · 독립시행", "확률",
            {1: "확률의 덧셈정리", 2: "여사건 — ‘적어도’", 3: "조건부확률", 4: "확률의 곱셈정리", 5: "독립시행의 확률"},
            pp=8,
            tips={1: "P(A∪B) = P(A) + P(B) − P(A∩B) — 겹친 부분은 한 번 빼요",
                  2: "‘적어도 하나’는 1 − (하나도 없을 확률)",
                  3: "P(B|A) = {P(A∩B)/P(A)} — 조건이 분모",
                  4: "P(A∩B) = P(A)P(B|A) — 꺼낸 것은 되돌리지 않으면 분모가 하나씩 줄어요",
                  5: "_{n}C_{r}p^{r}(1 − p)^{n − r}"},
            note="확률은 ‘전체 중 일부’예요. 덧셈정리에서는 겹친 부분, 조건부확률에서는 분모가 바뀐다는 것을 표나 벤 다이어그램으로 먼저 보여 주세요.")
    R = rng(2501)

    def g1():
        k = S.count(1) % 2
        if k == 0:
            n = R.choice([20, 24, 30, 36, 40, 50, 60])
            p_, q_ = R.sample([2, 3, 4, 5, 6], 2)
            if p_ * q_ > n or p_ % q_ == 0 or q_ % p_ == 0:
                return
            l = p_ * q_ // math.gcd(p_, q_)
            a, b, c = n // p_, n // q_, n // l
            val_ = Fr(a + b - c, n)
            q = f"1부터 {n}까지의 자연수가 하나씩 적힌 {n}장의 카드 중에서 한 장을 뽑을 때, {p_}의 배수 또는 {q_}의 배수가 나올 확률을 구하세요."
            lines = [L(f"{p_}의 배수 {a}장, {q_}의 배수 {b}장, {l}의 배수 {c}장", memo="둘 다인 것 = 공배수"),
                     L(f"{{{a}/{n}}} + {{{b}/{n}}} − {{{c}/{n}}} = {FR(val_)}", memo="겹친 것은 한 번 빼요")]
        else:
            D = R.choice([6, 8, 10, 12, 20])
            pa, pb = R.randint(2, D - 2), R.randint(2, D - 2)
            pc = R.randint(1, min(pa, pb) - 1) if min(pa, pb) > 1 else 1
            if pa + pb - pc > D:
                return
            val_ = Fr(pa + pb - pc, D)
            q = f"두 사건 A, B에 대하여 P(A) = {FR(Fr(pa, D))}, P(B) = {FR(Fr(pb, D))}, P(A∩B) = {FR(Fr(pc, D))}일 때, P(A∪B)를 구하세요."
            lines = [L("P(A∪B) = P(A) + P(B) − P(A∩B)", memo="덧셈정리"),
                     L(f"{FR(Fr(pa, D))} + {FR(Fr(pb, D))} − {FR(Fr(pc, D))} = {FR(val_)}")]
        S.add(1, q, FR(val_), "P(A∪B) = P(A) + P(B) − P(A∩B)", lines, None, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        if k == 0:
            w, b = R.randint(2, 6), R.randint(3, 7)
            m = R.choice([2, 3])
            if b < m:
                return
            n = w + b
            val_ = 1 - Fr(comb(b, m), comb(n, m))
            q = f"흰 공 {w}개와 검은 공 {b}개가 들어 있는 주머니에서 동시에 {m}개의 공을 꺼낼 때, 흰 공이 적어도 1개 나올 확률을 구하세요."
            lines = [L("(적어도 1개 흰 공) = 1 − (모두 검은 공)", memo="여사건"),
                     L(f"1 − {{_{{{b}}}C_{{{m}}}/_{{{n}}}C_{{{m}}}}} = 1 − {{{comb(b, m)}/{comb(n, m)}}} = {FR(val_)}")]
        elif k == 1:
            n = R.randint(3, 6)
            val_ = 1 - Fr(1, 2 ** n)
            what = R.choice(["앞면", "뒷면"])
            q = f"동전 한 개를 {n}번 던질 때, {what}이 적어도 한 번 나올 확률을 구하세요."
            lines = [L(f"(적어도 한 번 {what}) = 1 − (한 번도 {what}이 안 나옴)", memo="여사건"),
                     L(f"1 − ({{1/2}})^{{{n}}} = 1 − {{1/{2 ** n}}} = {FR(val_)}")]
        else:
            ev_ = R.choice([("짝수의 눈", Fr(1, 2)), ("3의 배수의 눈", Fr(1, 3)), ("6의 눈", Fr(1, 6)), ("5 이상의 눈", Fr(1, 3)), ("소수의 눈", Fr(1, 2))])
            n = R.randint(2, 4)
            nm, p_ = ev_
            val_ = 1 - (1 - p_) ** n
            q = f"주사위 한 개를 {n}번 던질 때, {nm}이 적어도 한 번 나올 확률을 구하세요."
            lines = [L(f"한 번 던져 {nm}이 안 나올 확률 1 − {FR(p_)} = {FR(1 - p_)}", memo="여사건"),
                     L(f"1 − ({FR(1 - p_)})^{{{n}}} = {FR(val_)}")]
        S.add(2, q, FR(val_), "‘적어도’는 1 − (하나도 없을 확률)", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        if k < 2:
            r0, r1, word, (c0, c1) = R.choice(CTX3)
            rows = (r0, r1)
            vals = [[R.randint(5, 40), R.randint(5, 40)], [R.randint(5, 40), R.randint(5, 40)]]
            tot = sum(map(sum, vals))
            r = R.randint(0, 1)
            colsum = vals[0][0] + vals[1][0]
            val_ = Fr(vals[r][0], colsum)
            f = Fig()
            ptable(f, rows, (c0, c1), vals, hl=[(2, 0, 0), (r, 0, 1)])
            q = f"어느 학교 학생 {tot}명을 조사한 결과가 표와 같아요. 이 중에서 임의로 뽑은 한 학생이 {word}일 때, 이 학생이 {rows[r]}일 확률을 구하세요."
            lines = [L(f"{word} {colsum}명", memo="조건 — 분모"),
                     L(f"그중 {rows[r]} {vals[r][0]}명", memo="분자"),
                     L(f"{{{vals[r][0]}/{colsum}}}" + (f" = {FR(val_)}" if val_.denominator != colsum else ""))]
            S.add(3, q, FR(val_), "조건이 되는 쪽이 분모", lines, f.out(), qfig=True, key=q + str(vals))
        else:
            D = R.choice([10, 12, 20, 15])
            pa = R.randint(3, D - 1)
            pab = R.randint(1, pa - 1)
            val_ = Fr(pab, pa)
            ask = R.choice(["P(B|A)", "P(A|B)"])
            if ask == "P(A|B)":
                q = f"두 사건 A, B에 대하여 P(B) = {FR(Fr(pa, D))}, P(A∩B) = {FR(Fr(pab, D))}일 때, P(A|B)를 구하세요."
                lines = [L("P(A|B) = {P(A∩B)/P(B)}", memo="조건 B가 분모"), L(f"{FR(Fr(pab, D))} ÷ {FR(Fr(pa, D))} = {FR(val_)}")]
            else:
                q = f"두 사건 A, B에 대하여 P(A) = {FR(Fr(pa, D))}, P(A∩B) = {FR(Fr(pab, D))}일 때, P(B|A)를 구하세요."
                lines = [L("P(B|A) = {P(A∩B)/P(A)}", memo="조건 A가 분모"), L(f"{FR(Fr(pab, D))} ÷ {FR(Fr(pa, D))} = {FR(val_)}")]
            S.add(3, q, FR(val_), "P(B|A) = {P(A∩B)/P(A)}", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 4
        w, b = R.randint(2, 6), R.randint(2, 6)
        n = w + b
        if k == 0:
            val_ = Fr(w, n) * Fr(w - 1, n - 1)
            q = f"흰 공 {w}개와 검은 공 {b}개가 들어 있는 주머니에서 공을 한 개씩 두 번 꺼낼 때, 두 번 모두 흰 공일 확률을 구하세요. (꺼낸 공은 다시 넣지 않아요)"
            lines = [L(f"첫째 흰 공 {{{w}/{n}}}, 둘째도 흰 공 {{{w - 1}/{n - 1}}}", memo="하나 꺼냈으니 하나씩 줄어요"),
                     L(f"{{{w}/{n}}} × {{{w - 1}/{n - 1}}} = {FR(val_)}")]
        elif k == 1:
            val_ = Fr(w, n) * Fr(b, n - 1)
            q = f"흰 공 {w}개와 검은 공 {b}개가 들어 있는 주머니에서 공을 한 개씩 두 번 꺼낼 때, 첫 번째는 흰 공, 두 번째는 검은 공일 확률을 구하세요. (꺼낸 공은 다시 넣지 않아요)"
            lines = [L(f"첫째 흰 공 {{{w}/{n}}}, 그다음 검은 공 {{{b}/{n - 1}}}", memo="곱셈정리"),
                     L(f"{{{w}/{n}}} × {{{b}/{n - 1}}} = {FR(val_)}")]
        elif k == 2:
            m = R.randint(2, 4)
            T = R.randint(m + 4, 12)
            val_ = Fr(m, T)
            q = f"당첨 제비 {m}개를 포함한 {T}개의 제비 중에서 A, B가 차례로 한 개씩 뽑을 때, B가 당첨될 확률을 구하세요. (뽑은 제비는 되돌려 놓지 않아요)"
            lines = [L(f"A 당첨 · B 당첨: {{{m}/{T}}} × {{{m - 1}/{T - 1}}} = {FR(Fr(m, T) * Fr(m - 1, T - 1))}", memo="A가 당첨될 때"),
                     L(f"A 꽝 · B 당첨: {{{T - m}/{T}}} × {{{m}/{T - 1}}} = {FR(Fr(T - m, T) * Fr(m, T - 1))}", memo="A가 꽝일 때"),
                     L(f"{FR(Fr(m, T) * Fr(m - 1, T - 1))} + {FR(Fr(T - m, T) * Fr(m, T - 1))} = {FR(val_)}", memo="순서와 상관없이 같아요")]
        else:
            val_ = Fr(w, n) * Fr(b, n - 1) + Fr(b, n) * Fr(w, n - 1)
            q = f"흰 공 {w}개와 검은 공 {b}개가 들어 있는 주머니에서 공을 한 개씩 두 번 꺼낼 때, 두 공의 색이 서로 다를 확률을 구하세요. (꺼낸 공은 다시 넣지 않아요)"
            lines = [L(f"흰 다음 검 {{{w}/{n}}} × {{{b}/{n - 1}}}, 검 다음 흰 {{{b}/{n}}} × {{{w}/{n - 1}}}", memo="두 경우"),
                     L(f"{{{w}/{n}}} × {{{b}/{n - 1}}} + {{{b}/{n}}} × {{{w}/{n - 1}}} = {FR(val_)}")]
        S.add(4, q, FR(val_), "P(A∩B) = P(A)P(B|A)", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        ctx = R.choice([("주사위 한 개를", "던질 때", "3의 배수의 눈이", Fr(1, 3)), ("주사위 한 개를", "던질 때", "짝수의 눈이", Fr(1, 2)),
                        ("주사위 한 개를", "던질 때", "1의 눈이", Fr(1, 6)), ("동전 한 개를", "던질 때", "앞면이", Fr(1, 2)),
                        ("자유투 성공률이 {3/4}인 선수가 자유투를", "던질 때", "성공이", Fr(3, 4)),
                        ("명중률이 {2/3}인 선수가 활을", "쏠 때", "명중이", Fr(2, 3))])
        a_, verb, ev_, p_ = ctx
        n = R.randint(3, 6)
        r = R.randint(1, n - 1) if R.random() < 0.8 else R.choice([0, n])
        val_ = comb(n, r) * p_ ** r * (1 - p_) ** (n - r)
        nm = ev_[:-1]
        q = f"{a_} {n}번 {verb}, {ev_} 정확히 {r}번 나올 확률을 구하세요." if "성공" not in ev_ and "명중" not in ev_ else f"{a_} {n}번 {verb}, 정확히 {r}번 {nm}할 확률을 구하세요."
        lines = [L(f"한 번에 p = {FR(p_)}, 아닐 확률 {FR(1 - p_)}", memo="독립시행"),
                 L(f"_{{{n}}}C_{{{r}}} × ({FR(p_)})^{{{r}}} × ({FR(1 - p_)})^{{{n - r}}} = {comb(n, r)} × {FR(p_ ** r)} × {FR((1 - p_) ** (n - r))} = {FR(val_)}")]
        if r == 0 or r == n:
            lines[1] = L(f"({FR(p_ if r else 1 - p_)})^{{{n}}} = {FR(val_)}", memo="모두 같은 결과")
        S.add(5, q, FR(val_), "_{n}C_{r}p^{r}(1 − p)^{n − r}", lines, None, sub={"p": p_}, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 확률분포 ══════════
def dtable(f, xs, ps, unk=None, at="q"):
    """확률분포표 — 두 줄"""
    n = len(xs)
    w0, cw, ch = 150, min(110, 440 / (n + 1)), 84
    tot = w0 + (n + 1) * cw
    x0, y0 = 330 - tot / 2, 230
    rows = [["X"] + [N(v) for v in xs] + ["합계"], ["P(X = x)"] + [("a" if unk == i else FR(p)) for i, p in enumerate(ps)] + ["1"]]
    for r, row in enumerate(rows):
        for j, s_ in enumerate(row):
            xx = x0 if j == 0 else x0 + w0 + (j - 1) * cw
            ww = w0 if j == 0 else cw
            f.rect(xx, y0 + r * ch, ww, ch, c="ink", sw=2, f="gold" if j == 0 else None, fo=0.12 if j == 0 else None, at=at)
            f.text(xx + ww / 2, y0 + r * ch + ch / 2 + 11, s_, z=26 if j == 0 else 30, b=700 if j == 0 else 600, at=at,
                   c="coral" if (r == 1 and unk is not None and j == unk + 1) else "ink")

def dist():
    S = Set("dist", "확률분포 — 기댓값 · 이항분포 · 정규분포", "확률분포",
            {1: "확률분포와 기댓값", 2: "분산과 표준편차", 3: "aX + b의 평균 · 분산", 4: "이항분포", 5: "정규분포와 표준화"},
            mixed=True, pp=8,
            tips={1: "확률의 합 = 1, E(X) = Σ(x × P(X = x))",
                  2: "V(X) = E(X^{2}) − {E(X)}^{2}, σ(X) = √{V(X)}",
                  3: "E(aX + b) = aE(X) + b, V(aX + b) = a^{2}V(X), σ(aX + b) = |a|σ(X)",
                  4: "B(n, p): E(X) = np, V(X) = np(1 − p)",
                  5: "Z = {X − m/σ}로 바꿔 표준정규분포표를 읽어요"},
            note="기댓값은 ‘확률을 무게로 한 평균’이에요. 표준화는 평균에서 표준편차 몇 개만큼 떨어졌는지를 재는 것이라는 뜻을 먼저 잡게 해 주세요.")
    R = rng(2502)

    def rand_ps(k):
        D = R.choice([6, 8, 10, 12])
        cut = sorted(R.sample(range(1, D), k - 1))
        parts = [b - a for a, b in zip([0] + cut, cut + [D])]
        return [Fr(p, D) for p in parts]

    def g1():
        k = R.choice([3, 4])
        start = R.randint(-1, 2)
        xs = [start + i for i in range(k)] if R.random() < 0.6 else sorted(R.sample(range(0, 8), k))
        ps = rand_ps(k)
        u = R.randrange(k)
        E = sum(x_ * p for x_, p in zip(xs, ps))
        f = Fig()
        dtable(f, xs, ps, unk=u)
        known = [FR(p) for i, p in enumerate(ps) if i != u]
        q = "확률변수 X의 확률분포가 " + ", ".join(f"P(X = {N(x_)}) = {'a' if i == u else FR(p)}" for i, (x_, p) in enumerate(zip(xs, ps))) + "일 때, E(X)를 구하세요."
        lines = [L(" + ".join(known) + f" + a = 1 → a = {FR(ps[u])}", memo="확률의 합은 1"),
                 L(f"E(X) = " + " + ".join(f"{NP(x_)} × {FR(p)}" for x_, p in zip(xs, ps)) + f" = {FR(E)}")]
        S.add(1, q, FR(E), "확률의 합 = 1로 a부터, E(X) = Σ x P(X = x)", lines, f.out(), sub={"a": ps[u]}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = R.choice([3, 3, 4])
        xs = sorted(R.sample(range(0, 7), k))
        ps = rand_ps(k)
        E = sum(x_ * p for x_, p in zip(xs, ps))
        E2 = sum(x_ * x_ * p for x_, p in zip(xs, ps))
        V = E2 - E * E
        f = Fig()
        dtable(f, xs, ps)
        q = "확률변수 X의 확률분포가 " + ", ".join(f"P(X = {x_}) = {FR(p)}" for x_, p in zip(xs, ps)) + "일 때, V(X)를 구하세요."
        lines = [L(f"E(X) = " + " + ".join(f"{x_} × {FR(p)}" for x_, p in zip(xs, ps)) + f" = {FR(E)}"),
                 L(f"E(X^{{2}}) = " + " + ".join(f"{x_}^{{2}} × {FR(p)}" for x_, p in zip(xs, ps)) + f" = {FR(E2)}"),
                 L(f"V(X) = {FR(E2)} − ({FR(E)})^{{2}} = {FR(V)}", memo="E(X^{2}) − {E(X)}^{2}")]
        S.add(2, q, FR(V), "V(X) = E(X^{2}) − {E(X)}^{2}", lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        m = R.randint(-3, 12)
        sd = R.randint(1, 6)
        V = sd * sd
        a, b = R.choice([2, 3, 4, 5, -2, -3, 10]), R.randint(-10, 10)
        k = S.count(3) % 4
        ex = f"{N(a)}X{TAIL(b)}"
        if k == 0:
            q = f"확률변수 X에 대하여 E(X) = {N(m)}, V(X) = {V}일 때, E({ex})를 구하세요."
            ans = a * m + b
            lines = [L(f"E({ex}) = {N(a)}E(X){TAIL(b)}", memo="E(aX + b) = aE(X) + b"), L(f"{N(a)} × {NP(m)}{TAIL(b)} = {N(ans)}")]
        elif k == 1:
            q = f"확률변수 X에 대하여 E(X) = {N(m)}, V(X) = {V}일 때, V({ex})를 구하세요."
            ans = a * a * V
            lines = [L(f"V({ex}) = {NP(a)}^{{2}}V(X)", memo="b는 흩어짐과 상관없어요"), L(f"{NP(a)}^{{2}} × {V} = {N(ans)}")]
        elif k == 2:
            q = f"확률변수 X에 대하여 E(X) = {N(m)}, V(X) = {V}일 때, σ({ex})를 구하세요."
            ans = abs(a) * sd
            lines = [L(f"σ(X) = √{{{V}}} = {sd}"), L(f"σ({ex}) = |{N(a)}|σ(X) = {abs(a)} × {sd} = {N(ans)}", memo="σ(aX + b) = |a|σ(X)")]
        else:
            q = f"확률변수 X에 대하여 E(X) = {N(m)}, V(X) = {V}일 때, E(X^{{2}})를 구하세요."
            ans = V + m * m
            lines = [L("V(X) = E(X^{2}) − {E(X)}^{2}", memo="거꾸로 쓰기"), L(f"E(X^{{2}}) = {V} + {NP(m)}^{{2}} = {N(ans)}")]
        S.add(3, q, N(ans), "E(aX + b) = aE(X) + b · V(aX + b) = a^{2}V(X)", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        ctx = R.choice([("주사위 한 개를", "1의 눈이 나오는", Fr(1, 6), [36, 72, 180, 360, 720]),
                        ("주사위 한 개를", "3의 배수의 눈이 나오는", Fr(1, 3), [18, 36, 72, 90, 180]),
                        ("동전 한 개를", "앞면이 나오는", Fr(1, 2), [16, 36, 64, 100, 400]),
                        ("성공률이 {1/5}인 시행을", "성공하는", Fr(1, 5), [25, 50, 100, 125, 625]),
                        ("성공률이 {3/4}인 시행을", "성공하는", Fr(3, 4), [16, 48, 64, 192, 400])])
        a_, ev_, p_, ns = ctx
        n = R.choice(ns)
        E, V = n * p_, n * p_ * (1 - p_)
        k = S.count(4) % 4
        lead = f"{a_} {n}번 {'던져서' if '눈' in ev_ or '앞면' in ev_ else '되풀이해서'} {ev_} 횟수를 X라 할 때,"
        if k == 0:
            q = f"{lead} E(X)를 구하세요."
            ans = E
            lines = [L(f"X는 이항분포 B({n}, {FR(p_)})를 따라요"), L(f"E(X) = {n} × {FR(p_)} = {FR(E)}", memo="np")]
        elif k == 1:
            q = f"{lead} V(X)를 구하세요."
            ans = V
            lines = [L(f"X는 이항분포 B({n}, {FR(p_)})를 따라요"), L(f"V(X) = {n} × {FR(p_)} × {FR(1 - p_)} = {FR(V)}", memo="np(1 − p)")]
        elif k == 2:
            if Fr(V).denominator != 1 or math.isqrt(int(V)) ** 2 != V:
                return
            q = f"{lead} σ(X)를 구하세요."
            ans = math.isqrt(int(V))
            lines = [L(f"X는 이항분포 B({n}, {FR(p_)})를 따라요"), L(f"V(X) = {n} × {FR(p_)} × {FR(1 - p_)} = {FR(V)}", memo="np(1 − p)"), L(f"σ(X) = √{{{FR(V)}}} = {ans}")]
        else:
            q = f"{lead} E(X^{{2}})를 구하세요."
            ans = V + E * E
            lines = [L(f"E(X) = {FR(E)}, V(X) = {FR(V)}", memo="B(" + str(n) + ", " + FR(p_) + ")"), L(f"E(X^{{2}}) = V(X) + {{E(X)}}^{{2}} = {FR(V)} + {FR(E)}^{{2}} = {FR(ans)}")]
        S.add(4, q, FR(ans), "B(n, p): E(X) = np, V(X) = np(1 − p)", lines, None, key=q)
    fill(S, 4, 20, g4)

    TZ = {Fr(1): 0.3413, Fr(3, 2): 0.4332, Fr(2): 0.4772, Fr(5, 2): 0.4938, Fr(1, 2): 0.1915}
    def zs(z):
        return DEC(z) if z.denominator != 1 else N(z)

    def g5():
        ctx = R.choice([("어느 고등학교 학생들의 키", "cm", (150, 175), (4, 5, 6, 8)), ("어느 과수원 사과의 무게", "g", (250, 400), (10, 20, 25)),
                        ("어느 시험 점수", "점", (55, 75), (4, 6, 8, 10)), ("어느 공장 건전지의 수명", "시간", (100, 300), (10, 20, 30))])
        nm, u, mr, sds = ctx
        m = R.randint(*mr)
        sd = R.choice(sds)
        zk = list(TZ.keys())
        k = S.count(5) % 4
        f = Fig()
        def bell(lo, hi):
            X0, X1, Y0 = 60, 600, 500
            Z = lambda z: X0 + (X1 - X0) * (z + 3.2) / 6.4
            pts = [(Z(z / 20), Y0 - 330 * math.exp(-(z / 20) ** 2 / 2)) for z in range(-64, 65)]
            f.line(X0 - 10, Y0, X1 + 14, Y0, c="ink", w=3, ar=1)
            f.poly(pts, c="sky", w=4, z=False)
            a_, b_ = max(lo, -3.2), min(hi, 3.2)
            reg = [(Z(a_ + (b_ - a_) * i / 40), Y0 - 330 * math.exp(-(a_ + (b_ - a_) * i / 40) ** 2 / 2)) for i in range(41)]
            f.poly(reg + [(Z(b_), Y0), (Z(a_), Y0)], c="none", f="teal", fo=0.3, at=1)
            f.line(Z(0), Y0, Z(0), Y0 - 330, c="soft", w=2, d=True)
            return Z, Y0
        if k == 0:
            z = R.choice(zk)
            v = m + z * sd
            if v.denominator != 1:
                return
            res = 0.5 - TZ[z]
            Z, Y0 = bell(float(z), 9)
            f.text(Z(float(z)), Y0 + 40, N(v), z=26)
            f.text(Z(0), Y0 + 40, N(m), z=26, c="soft")
            ask = f"P(X ≥ {N(v)})"
            lines = [L(f"{ask} = P(Z ≥ {{{N(v)} − {m}/{sd}}}) = P(Z ≥ {zs(z)})", memo="표준화"),
                     L(f"0.5 − P(0 ≤ Z ≤ {zs(z)}) = 0.5 − {TZ[z]} = {DEC4(res)}", memo="오른쪽 절반에서 빼기")]
            given = [z]
        elif k == 1:
            z1, z2 = R.sample(zk, 2)
            v1, v2 = m - z1 * sd, m + z2 * sd
            if v1.denominator != 1 or v2.denominator != 1:
                return
            res = TZ[z1] + TZ[z2]
            Z, Y0 = bell(-float(z1), float(z2))
            f.text(Z(-float(z1)), Y0 + 40, N(v1), z=26)
            f.text(Z(float(z2)), Y0 + 40, N(v2), z=26)
            ask = f"P({N(v1)} ≤ X ≤ {N(v2)})"
            lines = [L(f"{ask} = P({MI}{zs(z1)} ≤ Z ≤ {zs(z2)})", memo="표준화"),
                     L(f"{TZ[z1]} + {TZ[z2]} = {DEC4(res)}", memo="0을 사이에 두고 두 조각")]
            given = [z1, z2]
        elif k == 2:
            z1, z2 = sorted(R.sample(zk, 2))
            v1, v2 = m + z1 * sd, m + z2 * sd
            if v1.denominator != 1 or v2.denominator != 1:
                return
            res = TZ[z2] - TZ[z1]
            Z, Y0 = bell(float(z1), float(z2))
            f.text(Z(float(z1)), Y0 + 40, N(v1), z=26)
            f.text(Z(float(z2)), Y0 + 40, N(v2), z=26)
            ask = f"P({N(v1)} ≤ X ≤ {N(v2)})"
            lines = [L(f"{ask} = P({zs(z1)} ≤ Z ≤ {zs(z2)})", memo="표준화"),
                     L(f"{TZ[z2]} − {TZ[z1]} = {DEC4(res)}", memo="큰 조각에서 작은 조각 빼기")]
            given = [z1, z2]
        else:
            z = R.choice(zk)
            v = m + z * sd
            if v.denominator != 1:
                return
            res = 0.5 + TZ[z]
            Z, Y0 = bell(-9, float(z))
            f.text(Z(float(z)), Y0 + 40, N(v), z=26)
            f.text(Z(0), Y0 + 40, N(m), z=26, c="soft")
            ask = f"P(X ≤ {N(v)})"
            lines = [L(f"{ask} = P(Z ≤ {zs(z)})", memo="표준화"),
                     L(f"0.5 + {TZ[z]} = {DEC4(res)}", memo="왼쪽 절반 + 조각")]
            given = [z]
        tab = ", ".join(f"P(0 ≤ Z ≤ {zs(z)}) = {TZ[z]}" for z in sorted(set(given)))
        q = f"{nm} X가 평균 {m} {u}, 표준편차 {sd} {u}인 정규분포를 따를 때, {ask}를 구하세요. (단, {tab})"
        S.add(5, q, DEC4(res), "Z = {X − m/σ}로 표준화", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 수열의 극한과 급수 ══════════
def LIMN():
    return "lim_{n→∞}"

def slim():
    S = Set("slim", "수열의 극한과 급수 — 등비급수", "수열의 극한·급수",
            {1: "∞/∞ 꼴의 수열의 극한", 2: "∞ − ∞ 꼴 — 유리화", 3: "등비수열의 극한", 4: "급수 — 부분분수로 합", 5: "등비급수"},
            pp=8,
            tips={1: "분모의 최고차항으로 나눠요 — 차수가 같으면 계수의 비",
                  2: "√ 끼리 빼면 유리화 — 분자를 곱셈 공식으로",
                  3: "밑의 절댓값이 가장 큰 것으로 나눠요 — |r| < 1이면 r^{n} → 0",
                  4: "부분합 S_{n}을 먼저 구하고 n → ∞",
                  5: "Σ_{n=1}^{∞}ar^{n − 1} = {a/1 − r} (−1 < r < 1)"},
            note="급수는 ‘부분합의 극한’이에요. 등비급수 공식도 S_{n} = {a(1 − r^{n})/1 − r}에서 r^{n} → 0이 되는 것으로 설명하게 해 주세요.")
    R = rng(2503)

    def g1():
        k = S.count(1) % 2
        a, d = R.choice([1, 2, 3, 4, 5, 6, -2]), R.choice([1, 2, 3, 4, 5])
        if k == 0:
            num, den = [a, R.randint(-6, 6), R.randint(-6, 6)], [d, R.randint(-6, 6), R.randint(1, 6)]
            val_ = Fr(a, d)
            q = f"{LIMN()} {{{POLY(num, 'n')}/{POLY(den, 'n')}}}의 값을 구하세요."
            lines = [L("분모 · 분자를 n^{2}으로 나누기", memo="∞/∞ 꼴"), L(f"최고차항의 계수의 비 → {FR(val_)}", memo="{1/n} → 0")]
            S.add(1, q, FR(val_), "분모의 최고차항으로 나누기", lines, None, key=q)
        else:
            num, den = [a, R.randint(-6, 6)], [d, R.randint(-6, 6), R.randint(1, 6)]
            q = f"{LIMN()} {{{POLY(num, 'n')}/{POLY(den, 'n')}}}의 값을 구하세요."
            lines = [L("분모 · 분자를 n^{2}으로 나누기", memo="∞/∞ 꼴"), L(f"분자는 0으로, 분모는 {RO(str(d))} 다가가요", memo="분모의 차수가 더 커요"), L("극한값은 0")]
            S.add(1, q, "0", "분모의 차수가 더 크면 0", lines, None, key=q)
    fill(S, 1, 20, g1)

    nn = sp.Symbol("n", positive=True)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            a = R.choice([2, 4, 6, 8, 10, 3, 5])
            form = R.choice([1, 2, 3])
            if form == 1:
                val_ = Fr(a, 2)
                q = f"{LIMN()}(√{{n^{{2}} + {a}n}} − n)의 값을 구하세요."
                lines = [L(f"√{{n^{{2}} + {a}n}} − n = {{{a}n/√{{n^{{2}} + {a}n}} + n}}", memo="분자 유리화"),
                         L(f"분모 · 분자를 n으로 나누면 {{{a}/√{{1 + {{{a}/n}}}} + 1}}"),
                         L(f"{{{a}/1 + 1}} = {FR(val_)}", memo="{1/n} → 0")]
                ex_ = sp.sqrt(nn ** 2 + a * nn) - nn
            elif form == 2:
                val_ = Fr(a, 2)
                q = f"{LIMN()}(n − √{{n^{{2}} − {a}n}})의 값을 구하세요."
                lines = [L(f"n − √{{n^{{2}} − {a}n}} = {{{a}n/n + √{{n^{{2}} − {a}n}}}}", memo="분자 유리화"),
                         L(f"분모 · 분자를 n으로 나누면 {{{a}/1 + √{{1 − {{{a}/n}}}}}}"),
                         L(f"{{{a}/1 + 1}} = {FR(val_)}", memo="{1/n} → 0")]
                ex_ = nn - sp.sqrt(nn ** 2 - a * nn)
            else:
                val_ = Fr(2, a)
                q = f"{LIMN()} {{1/√{{n^{{2}} + {a}n}} − n}}의 값을 구하세요."
                lines = [L(f"{{1/√{{n^{{2}} + {a}n}} − n}} = {{√{{n^{{2}} + {a}n}} + n/{a}n}}", memo="분모 유리화"),
                         L(f"분모 · 분자를 n으로 나누면 {{√{{1 + {{{a}/n}}}} + 1/{a}}}"),
                         L(f"{{1 + 1/{a}}} = {FR(val_)}", memo="{1/n} → 0")]
                ex_ = 1 / (sp.sqrt(nn ** 2 + a * nn) - nn)
        else:
            a, b = R.sample([1, 2, 3, 4, 5, 6, 8], 2)
            val_ = Fr(a - b, 2)
            q = f"{LIMN()}(√{{n^{{2}} + {a}n}} − √{{n^{{2}} + {b}n}})의 값을 구하세요."
            lines = [L(f"(√{{n^{{2}} + {a}n}} − √{{n^{{2}} + {b}n}}) = {{{a - b}n/√{{n^{{2}} + {a}n}} + √{{n^{{2}} + {b}n}}}}", memo="분자 유리화"),
                     L(f"분모 · 분자를 n으로 나누면 {{{a - b}/√{{1 + {{{a}/n}}}} + √{{1 + {{{b}/n}}}}}}"),
                     L(f"{{{a - b}/1 + 1}} = {FR(val_)}", memo="{1/n} → 0")]
            ex_ = sp.sqrt(nn ** 2 + a * nn) - sp.sqrt(nn ** 2 + b * nn)
        assert sp.limit(ex_, nn, sp.oo) == sp.Rational(val_.numerator, val_.denominator)
        S.add(2, q, FR(val_), "∞ − ∞ 꼴은 유리화", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        if k == 0:
            p_, q_ = R.sample([2, 3, 4, 5], 2)
            big, sm = max(p_, q_), min(p_, q_)
            c1, c2 = R.choice([1, 2, 3]), R.choice([1, 2, 3])
            e = R.choice([0, 1, 2])
            # (big^{n+e} + sm^n) / (c1 big^n + c2 sm^n)
            val_ = Fr(big ** e, c1)
            nume = f"{big}^{{n + {e}}} + {sm}^{{n}}" if e else f"{big}^{{n}} + {sm}^{{n}}"
            deno = f"{'' if c1 == 1 else str(c1) + ' × '}{big}^{{n}} + {'' if c2 == 1 else str(c2) + ' × '}{sm}^{{n}}"
            q = f"{LIMN()} {{{nume}/{deno}}}의 값을 구하세요."
            lines = [L(f"분모 · 분자를 {big}^{{n}}으로 나누기", memo="밑이 가장 큰 것"),
                     L(f"({{{sm}/{big}}})^{{n}} → 0", memo=f"|{{{sm}/{big}}}| < 1"),
                     L(f"{big ** e} ÷ {c1} = {FR(val_)}" if c1 != 1 else f"극한값은 {big ** e}")]
            S.add(3, q, FR(val_), "밑의 절댓값이 가장 큰 것으로 나누기", lines, None, key=q)
        else:
            c = R.choice([1, 2, 3, 4, -1, -2])
            d = R.choice([2, 3, 4, 5])
            # 수열 {((x − c)/d)^n} 수렴: −1 < (x − c)/d ≤ 1 → c − d < x ≤ c + d
            lo, hi = c - d, c + d
            cnt = hi - lo
            q = f"수열 {{({{{XM(c)}/{d}}})^{{n}}}}이 수렴하도록 하는 정수 x의 개수를 구하세요."
            lines = [L(f"−1 < {{{XM(c)}/{d}}} ≤ 1", memo="r^{n} 수렴 ⇔ −1 < r ≤ 1"),
                     L(f"{N(lo)} < x ≤ {N(hi)}"),
                     L(f"정수 {N(lo + 1)}, …, {N(hi)} → {cnt}개")]
            S.add(3, q, str(cnt), "r^{n}이 수렴 ⇔ −1 < r ≤ 1", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 4
        c = R.choice([1, 2, 3, 4, 5, 6, 8, 10, 12])
        if k == 0:
            val_ = Fr(c)
            q = f"Σ_{{n=1}}^{{∞}}{{{c}/n(n + 1)}}의 값을 구하세요."
            lines = [L(f"{{{c}/n(n + 1)}} = {c}({{1/n}} − {{1/n + 1}})", memo="부분분수"),
                     L(f"S_{{n}} = {c}(1 − {{1/n + 1}})", memo="이웃끼리 지워져요"),
                     L(f"{LIMN()} S_{{n}} = {c}", memo="{1/n + 1} → 0")]
        elif k == 1:
            val_ = Fr(3 * c, 4)
            q = f"Σ_{{n=1}}^{{∞}}{{{c}/n(n + 2)}}의 값을 구하세요."
            lines = [L(f"{{{c}/n(n + 2)}} = {{{c}/2}}({{1/n}} − {{1/n + 2}})", memo="부분분수"),
                     L(f"S_{{n}} = {{{c}/2}}(1 + {{1/2}} − {{1/n + 1}} − {{1/n + 2}})", memo="앞의 두 개, 뒤의 두 개가 남아요"),
                     L(f"{{{c}/2}} × {{3/2}} = {FR(val_)}", memo="n → ∞")]
        elif k == 2:
            val_ = Fr(c, 2)
            q = f"Σ_{{n=1}}^{{∞}}{{{c}/(2n − 1)(2n + 1)}}의 값을 구하세요."
            lines = [L(f"{{{c}/(2n − 1)(2n + 1)}} = {{{c}/2}}({{1/2n − 1}} − {{1/2n + 1}})", memo="부분분수"),
                     L(f"S_{{n}} = {{{c}/2}}(1 − {{1/2n + 1}})", memo="이웃끼리 지워져요"),
                     L(f"{{{c}/2}} × 1 = {FR(val_)}", memo="n → ∞")]
        else:
            val_ = Fr(c)
            q = f"Σ_{{n=1}}^{{∞}}({{{c}/n}} − {{{c}/n + 1}})의 값을 구하세요."
            lines = [L(f"S_{{n}} = ({c} − {{{c}/2}}) + ({{{c}/2}} − {{{c}/3}}) + … + ({{{c}/n}} − {{{c}/n + 1}})", memo="부분합부터"),
                     L(f"S_{{n}} = {c} − {{{c}/n + 1}}", memo="이웃끼리 지워져요"),
                     L(f"{LIMN()} S_{{n}} = {c}")]
        S.add(4, q, FR(val_), "부분합 S_{n} → 극한", lines, None, ident=True if k < 3 else False, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            a = R.choice([1, 2, 3, 4, 5, 6, 8, 9, 10, 12])
            r = R.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(-1, 2), Fr(-1, 3), Fr(2, 5)])
            val_ = Fr(a) / (1 - r)
            q = f"Σ_{{n=1}}^{{∞}}{a} × ({FR(r)})^{{n − 1}}의 값을 구하세요."
            lines = [L(f"첫째항 {a}, 공비 {FR(r)}", memo="−1 < r < 1 → 수렴"),
                     L(f"{{{a}/1 − ({FR(r)})}} = {FR(val_)}", memo="{a/1 − r}")]
        elif k == 1:
            r = R.choice([Fr(1, 2), Fr(1, 3), Fr(2, 3), Fr(1, 4), Fr(3, 4), Fr(2, 5), Fr(3, 5), Fr(1, 5)])
            val_ = r / (1 - r)
            q = f"Σ_{{n=1}}^{{∞}}({FR(r)})^{{n}}의 값을 구하세요."
            lines = [L(f"첫째항 {FR(r)}, 공비 {FR(r)}", memo="n = 1일 때가 첫째항"),
                     L(f"{{{FR(r)}/1 − {FR(r)}}} = {FR(val_)}", memo="{a/1 − r}")]
        else:
            p_, q_ = R.sample([2, 3, 4, 5], 2)
            D = R.choice([v for v in (6, 10, 12, 15, 20) if v > max(p_, q_) and v % p_ == 0 and v % q_ == 0] or [0])
            if not D:
                return
            r1, r2 = Fr(p_, D), Fr(q_, D)
            val_ = r1 / (1 - r1) + r2 / (1 - r2)
            q = f"Σ_{{n=1}}^{{∞}}{{{p_}^{{n}} + {q_}^{{n}}/{D}^{{n}}}}의 값을 구하세요."
            lines = [L(f"Σ({FR(r1)})^{{n}} + Σ({FR(r2)})^{{n}}", memo="두 등비급수로 나누기"),
                     L(f"{{{FR(r1)}/1 − {FR(r1)}}} + {{{FR(r2)}/1 − {FR(r2)}}} = {FR(r1 / (1 - r1))} + {FR(r2 / (1 - r2))} = {FR(val_)}")]
        S.add(5, q, FR(val_), "Σar^{n − 1} = {a/1 − r} (|r| < 1)", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 여러 가지 적분법 ══════════
X_ = sp.Symbol("x")
E_ = sp.E

def EF(p, q, k=1):
    """p·e^{k} + q (유리수 p, q) → 글자"""
    p, q = Fr(p), Fr(q)
    ek = "e" if k == 1 else f"e^{{{k}}}"
    if p == 0:
        return FR(q)
    if p.denominator == 1:
        head = ("" if abs(p) == 1 else N(abs(p))) + ek
        head = (MI if p < 0 else "") + head
    else:
        head = (MI if p < 0 else "") + f"{{{'' if abs(p.numerator) == 1 else abs(p.numerator)}{ek}/{p.denominator}}}"
    if q == 0:
        return head
    return f"{head} {'+' if q > 0 else MI} {FR(abs(q))}"

def int2():
    S = Set("int2", "여러 가지 적분법 — 치환적분 · 부분적분", "치환·부분적분",
            {1: "여러 가지 함수의 정적분", 2: "치환적분 — 다항식", 3: "치환적분 — 로그 · 지수 · 삼각", 4: "부분적분", 5: "정적분과 급수(구분구적법)"},
            pp=8,
            tips={1: "∫{1/x}dx = ln|x| + C, ∫e^{x}dx = e^{x} + C, ∫sin x dx = −cos x + C, ∫cos x dx = sin x + C",
                  2: "g(x) = t로 놓으면 g'(x)dx = dt — 끝값도 t로 바꿔요",
                  3: "∫{f'(x)/f(x)}dx = ln|f(x)| + C",
                  4: "∫f(x)g'(x)dx = f(x)g(x) − ∫f'(x)g(x)dx — 미분할 것은 다항식 · ln x",
                  5: "lim_{n→∞}Σ_{k=1}^{n}{1/n}f({k/n}) = ∫_{0}^{1}f(x)dx"},
            note="치환은 ‘속에 든 함수의 미분이 밖에 있는지’, 부분적분은 ‘무엇을 미분할지’를 먼저 고르게 해 주세요.")
    R = rng(2504)

    def g1():
        k = S.count(1) % 3
        if k == 0:
            c, m = R.choice([1, 2, 3, 4]), R.choice([1, 2, 3])
            q = f"∫_{{1}}^{{e^{{{m}}}}}{{{c}/x}}dx의 값을 구하세요." if m > 1 else f"∫_{{1}}^{{e}}{{{c}/x}}dx의 값을 구하세요."
            up = f"e^{{{m}}}" if m > 1 else "e"
            ans = c * m
            lines = [L(f"∫_{{1}}^{{{up}}}{{{c}/x}}dx = [{'' if c == 1 else c}ln x]_{{1}}^{{{up}}}", memo="∫{1/x}dx = ln|x| + C"),
                     L(f"{c}(ln {up} − ln 1) = {c} × {m} = {ans}" if c != 1 else f"ln {up} − ln 1 = {ans}", memo=f"ln {up} = {m}")]
            exp_ = sp.integrate(c / X_, (X_, 1, E_ ** m))
            S.add(1, q, str(ans), "∫{1/x}dx = ln|x| + C", lines, None, key=q)
            assert sp.simplify(exp_ - ans) == 0
        elif k == 1:
            a = R.choice([2, 3, 4, 5, 6, 7])
            c = R.choice([1, 2, 3])
            ans = c * (a - 1)
            q = f"∫_{{0}}^{{ln {a}}}{'' if c == 1 else c}e^{{x}}dx의 값을 구하세요."
            lines = [L(f"[{'' if c == 1 else c}e^{{x}}]_{{0}}^{{ln {a}}} = {'' if c == 1 else c}(e^{{ln {a}}} − e^{{0}})", memo="∫e^{x}dx = e^{x} + C"),
                     L(f"{'' if c == 1 else str(c) + ' × '}({a} − 1) = {ans}", memo=f"e^{{ln {a}}} = {a}")]
            assert sp.simplify(sp.integrate(c * sp.exp(X_), (X_, 0, sp.log(a))) - ans) == 0
            S.add(1, q, str(ans), "∫e^{x}dx = e^{x} + C", lines, None, key=q)
        else:
            fn = R.choice(["sin", "cos"])
            up = R.choice([30, 45, 60, 90, 120, 180])
            c = R.choice([1, 2, 4])
            U = sp.pi * up / 180
            val_ = sp.integrate(c * (sp.sin(X_) if fn == "sin" else sp.cos(X_)), (X_, 0, U))
            from g_hc import rad
            us = rad(up)
            if fn == "sin":
                F = f"{MI}{'' if c == 1 else c}cos x"
                mid = f"{MI}{'' if c == 1 else c}(cos {us} − cos 0)"
            else:
                F = f"{'' if c == 1 else c}sin x"
                mid = f"{'' if c == 1 else c}(sin {us} − sin 0)"
            q = f"∫_{{0}}^{{{us}}}{'' if c == 1 else c}{fn} x dx의 값을 구하세요."
            ans = SURD(val_)
            from g_hc import trig_val
            cs_ = "" if c == 1 else str(c)
            if fn == "sin":
                cu = trig_val("cos", up)
                sub_s = f"{MI}{cs_}({cu} − 1)" if c == 1 else f"{MI}{c} × ({cu} − 1)"
            else:
                su = trig_val("sin", up)
                sub_s = su if c == 1 else f"{c} × {su}"
            lines = [L(f"[{F}]_{{0}}^{{{us}}} = {mid}", memo=f"∫{fn} x dx = " + ("−cos x" if fn == "sin" else "sin x") + " + C"),
                     L(f"{sub_s} = {ans}", memo=f"{'cos' if fn == 'sin' else 'sin'} {us} = {trig_val('cos' if fn == 'sin' else 'sin', up)}")]
            S.add(1, q, ans, "삼각함수의 부정적분부터", lines, None, omr="ex" if "√" in ans else "num", key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            p_ = R.choice([1, 2, 3])
            n = R.choice([2, 3, 4])
            b = R.choice([1, 2])
            c = R.choice([1, 2])
            # ∫_0^b c·2x(x^2 + p)^n dx = c[(t)^{n+1}/(n+1)]_{p}^{b^2+p}
            t0, t1 = p_, b * b + p_
            val_ = Fr(c * (t1 ** (n + 1) - t0 ** (n + 1)), n + 1)
            coef = f"{2 * c}x"
            q = f"∫_{{0}}^{{{b}}}{coef}(x^{{2}} + {p_})^{{{n}}}dx의 값을 구하세요."
            lines = [L(f"x^{{2}} + {p_} = t로 놓으면 2x dx = dt", memo="치환"),
                     L(f"x가 0에서 {b}까지 → t는 {t0}에서 {t1}까지", memo="끝값도 바꾸기"),
                     L(f"∫_{{{t0}}}^{{{t1}}}{'' if c == 1 else c}t^{{{n}}}dt = [{FR(Fr(c, n + 1))}t^{{{n + 1}}}]_{{{t0}}}^{{{t1}}}", memo=f"x dx 대신 {{1/2}}dt" if False else None),
                     L(f"{FR(Fr(c, n + 1))}({t1}^{{{n + 1}}} − {t0}^{{{n + 1}}}) = {FR(val_)}")]
            assert sp.integrate(2 * c * X_ * (X_ ** 2 + p_) ** n, (X_, 0, b)) == sp.Rational(val_.numerator, val_.denominator)
        else:
            m, p_ = R.choice([2, 3]), R.choice([-1, 1, 2])
            n = R.choice([2, 3, 4])
            a, b = R.choice([(0, 1), (1, 2), (0, 2)])
            t0, t1 = m * a + p_, m * b + p_
            val_ = Fr(t1 ** (n + 1) - t0 ** (n + 1), m * (n + 1))
            q = f"∫_{{{a}}}^{{{b}}}({LIN(m, p_)})^{{{n}}}dx의 값을 구하세요."
            lines = [L(f"{LIN(m, p_)} = t로 놓으면 {m}dx = dt", memo="치환 — dx = {1/" + str(m) + "}dt"),
                     L(f"x가 {a}에서 {b}까지 → t는 {N(t0)}에서 {N(t1)}까지", memo="끝값도 바꾸기"),
                     L(f"{{1/{m}}}[{{1/{n + 1}}}t^{{{n + 1}}}]_{{{N(t0)}}}^{{{N(t1)}}} = {{1/{m * (n + 1)}}}({RP(t1)}^{{{n + 1}}} − {RP(t0)}^{{{n + 1}}}) = {FR(val_)}")]
            assert sp.integrate((m * X_ + p_) ** n, (X_, a, b)) == sp.Rational(val_.numerator, val_.denominator)
        S.add(2, q, FR(val_), "속 함수를 t로 — 끝값도 t로", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 4
        if k == 0:
            p_, b = R.choice([(1, 1), (1, 2), (1, 3), (2, 2), (3, 3), (4, 2), (2, 4), (5, 2)])
            ratio = Fr(b * b + p_, p_)
            if ratio.denominator != 1:
                return
            c = R.choice([1, 2, 3])
            q = f"∫_{{0}}^{{{b}}}{{{2 * c}x/x^{{2}} + {p_}}}dx의 값을 구하세요."
            ans = f"{'' if c == 1 else c}ln {int(ratio)}"
            lines = [L(f"(x^{{2}} + {p_})' = 2x", memo="분자가 분모의 미분"),
                     L(f"[{'' if c == 1 else c}ln(x^{{2}} + {p_})]_{{0}}^{{{b}}} = {'' if c == 1 else c}(ln {b * b + p_} − ln {p_}) = {ans}", memo="∫{f'/f}dx = ln|f| + C")]
            assert sp.simplify(sp.integrate(2 * c * X_ / (X_ ** 2 + p_), (X_, 0, b)) - c * sp.log(int(ratio))) == 0
            S.add(3, q, ans, "∫{f'(x)/f(x)}dx = ln|f(x)| + C", lines, None, omr="ex", key=q)
        elif k == 1:
            b = R.choice([1, 2])
            c = R.choice([1, 2, 3])
            q = f"∫_{{0}}^{{{b}}}{2 * c}xe^{{x^{{2}}}}dx의 값을 구하세요."
            ans = EF(c, -c, b * b)
            lines = [L("x^{2} = t로 놓으면 2x dx = dt", memo="치환"),
                     L(f"{'' if c == 1 else c}∫_{{0}}^{{{b * b}}}e^{{t}}dt = {'' if c == 1 else c}[e^{{t}}]_{{0}}^{{{b * b}}} = {ans}")]
            assert sp.simplify(sp.integrate(2 * c * X_ * sp.exp(X_ ** 2), (X_, 0, b)) - (c * sp.exp(b * b) - c)) == 0
            S.add(3, q, ans, "x^{2} = t로 치환", lines, None, omr="ex", key=q)
        elif k == 2:
            n = R.choice([1, 2, 3, 4])
            c = R.choice([1, 2, 3, 4, 6])
            fn, other = R.choice([("sin", "cos"), ("cos", "sin")])
            val_ = Fr(c, n + 1)
            pw = "" if n == 1 else f"^{{{n}}}"
            q = f"∫_{{0}}^{{{{π/2}}}}{'' if c == 1 else c}{fn}{pw}x {other} x dx의 값을 구하세요."
            lines = [L(f"{fn} x = t로 놓으면 " + ("cos x dx = dt" if fn == "sin" else "−sin x dx = dt"), memo="치환"),
                     L(f"{'' if c == 1 else c}∫_{{0}}^{{1}}t^{{{n}}}dt = {{{c}/{n + 1}}}" + (f" = {FR(val_)}" if Fr(c, n + 1).denominator != n + 1 else ""), memo="끝값 0 → 1" if fn == "sin" else "끝값 1 → 0, −를 붙여 뒤집기")]
            ex_ = sp.integrate(c * (sp.sin(X_) if fn == "sin" else sp.cos(X_)) ** n * (sp.cos(X_) if fn == "sin" else sp.sin(X_)), (X_, 0, sp.pi / 2))
            assert sp.simplify(ex_ - sp.Rational(val_.numerator, val_.denominator)) == 0
            S.add(3, q, FR(val_), "속 함수 sin x · cos x를 t로", lines, None, key=q)
        else:
            n = R.choice([1, 2, 3, 4])
            c = R.choice([1, 2, 3, 4, 5, 6])
            val_ = Fr(c, n + 1)
            pw = "ln x" if n == 1 else f"(ln x)^{{{n}}}"
            q = f"∫_{{1}}^{{e}}{{{'' if c == 1 else c}{pw}/x}}dx의 값을 구하세요."
            lines = [L("ln x = t로 놓으면 {1/x}dx = dt", memo="치환"),
                     L(f"{'' if c == 1 else c}∫_{{0}}^{{1}}t^{{{n}}}dt = {{{c}/{n + 1}}}" + (f" = {FR(val_)}" if Fr(c, n + 1).denominator != n + 1 else ""), memo="끝값 1 → e가 0 → 1")]
            assert sp.simplify(sp.integrate(c * sp.log(X_) ** n / X_, (X_, 1, sp.E)) - sp.Rational(val_.numerator, val_.denominator)) == 0
            S.add(3, q, FR(val_), "ln x = t로 치환", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 4
        c = R.choice([1, 2, 3])
        cs = "" if c == 1 else str(c)
        if k == 0:
            b = R.choice([1, 2, 3])
            q = f"∫_{{0}}^{{{b}}}{cs}xe^{{x}}dx의 값을 구하세요."
            ans = EF(c * (b - 1), c, b)
            be = "e" if b == 1 else f"e^{{{b}}}"
            lines = [L("f = x, g' = e^{x}로 부분적분", memo="x를 미분"),
                     L(f"{cs}([xe^{{x}}]_{{0}}^{{{b}}} − ∫_{{0}}^{{{b}}}e^{{x}}dx) = {cs}({'' if b == 1 else b}{be} − ({be} − 1))", memo="fg − ∫f'g"),
                     L(f"정적분 값 {ans}")]
            assert sp.simplify(sp.integrate(c * X_ * sp.exp(X_), (X_, 0, b)) - (c * (b - 1) * sp.exp(b) + c)) == 0
        elif k == 1:
            m = R.choice([1, 2])
            up = "e" if m == 1 else f"e^{{{m}}}"
            q = f"∫_{{1}}^{{{up}}}{cs}ln x dx의 값을 구하세요."
            ans = EF(c * (m - 1), c, m)
            lines = [L("f = ln x, g' = 1로 부분적분", memo="ln x를 미분"),
                     L(f"{cs}([x ln x]_{{1}}^{{{up}}} − ∫_{{1}}^{{{up}}}1 dx) = {cs}({'' if m == 1 else m}{up} − ({up} − 1))", memo="fg − ∫f'g"),
                     L(f"정적분 값 {ans}")]
            assert sp.simplify(sp.integrate(c * sp.log(X_), (X_, 1, sp.E ** m)) - (c * (m - 1) * sp.exp(m) + c)) == 0
        elif k == 2:
            fn, up, ex_, ans_s = R.choice([("sin", "π", sp.pi, "π"), ("cos", "{π/2}", sp.pi / 2 - 1, "{π/2} − 1"), ("sin", "{π/2}", sp.Integer(1), "1"), ("cos", "π", sp.Integer(-2), "−2")])
            Ux = sp.pi if up == "π" else sp.pi / 2
            q = f"∫_{{0}}^{{{up}}}{cs}x {fn} x dx의 값을 구하세요."
            ans = {("π", 1): "π", ("π", 2): "2π", ("π", 3): "3π",
                   ("{π/2} − 1", 1): "{π/2} − 1", ("{π/2} − 1", 2): "π − 2", ("{π/2} − 1", 3): "{3π/2} − 3",
                   ("1", 1): "1", ("1", 2): "2", ("1", 3): "3", ("−2", 1): f"{MI}2", ("−2", 2): f"{MI}4", ("−2", 3): f"{MI}6"}[(ans_s, c)]
            lines = [L(f"f = x, g' = {fn} x로 부분적분", memo="x를 미분"),
                     L(f"{cs}([x{'(−cos x)' if fn == 'sin' else ' sin x'}]_{{0}}^{{{up}}} − ∫_{{0}}^{{{up}}}{'(−cos x)' if fn == 'sin' else 'sin x'}dx)", memo="fg − ∫f'g"),
                     L(f"정적분 값 {ans}")]
            assert sp.simplify(sp.integrate(c * X_ * (sp.sin(X_) if fn == "sin" else sp.cos(X_)), (X_, 0, Ux)) - c * ex_) == 0
        else:
            pw = R.choice([1, 2])
            xs_ = "x" if pw == 1 else "x^{2}"
            q = f"∫_{{1}}^{{e}}{cs}{xs_} ln x dx의 값을 구하세요."
            if pw == 1:
                ans = {1: "{e^{2} + 1/4}", 2: "{e^{2} + 1/2}", 3: "{3e^{2} + 3/4}"}[c]
                mid = f"{cs}({{e^{{2}}/2}} − {{e^{{2}} − 1/4}})"
                exv = c * (sp.E ** 2 + 1) / 4
                Fx = "{1/2}x^{2}"
            else:
                ans = {1: "{2e^{3} + 1/9}", 2: "{4e^{3} + 2/9}", 3: "{2e^{3} + 1/3}"}[c]
                mid = f"{cs}({{e^{{3}}/3}} − {{e^{{3}} − 1/9}})"
                exv = c * (2 * sp.E ** 3 + 1) / 9
                Fx = "{1/3}x^{3}"
            lines = [L(f"f = ln x, g' = {xs_}로 부분적분", memo="ln x를 미분"),
                     L(f"{cs}([{Fx}ln x]_{{1}}^{{e}} − ∫_{{1}}^{{e}}{Fx[:5]}{'x' if pw == 1 else 'x^{2}'} dx) = {mid}", memo="fg − ∫f'g"),
                     L(f"정적분 값 {ans}")]
            assert sp.simplify(sp.integrate(c * X_ ** pw * sp.log(X_), (X_, 1, sp.E)) - exv) == 0
        S.add(4, q, ans, "∫fg' = fg − ∫f'g — 다항식 · ln x를 미분", lines, None, omr="ex" if not ans.lstrip(MI).isdigit() else "num", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        if k == 0:
            cs = [R.choice([1, 2, 3, 4, 6]), R.randint(-3, 4), R.randint(-3, 4)][: R.choice([2, 3])]
            if len(cs) == 2:
                cs = [cs[0], 0, cs[1]]
            F = integ(cs)
            val_ = ev(F, 1)
            terms = POLY(cs, "x")
            inner = terms.replace("x^{2}", "({k/n})^{2}").replace("x", "{k/n}")
            q = f"{LIMN()}Σ_{{k=1}}^{{n}}{{1/n}}({inner})의 값을 구하세요."
            lines = [L("{k/n} = x, {1/n} = dx로 보면 0에서 1까지의 정적분", memo="구분구적법"),
                     L(f"∫_{{0}}^{{1}}({terms})dx = [{POLY(F)}]_{{0}}^{{1}} = {FR(val_)}")]
        else:
            cs = [R.choice([1, 3, 6]), 0, 0]
            a, w = R.choice([1, 2]), R.choice([1, 2, 3])
            # Σ (w/n) f(a + wk/n) → ∫_a^{a+w} f(x)dx, f = c x^2
            F = integ(cs)
            val_ = ev(F, a + w) - ev(F, a)
            c0 = cs[0]
            inner = f"{'' if c0 == 1 else c0}({a} + {{{'' if w == 1 else w}k/n}})^{{2}}"
            q = f"{LIMN()}Σ_{{k=1}}^{{n}}{{{w}/n}}{inner}의 값을 구하세요."
            lines = [L(f"{a} + {{{'' if w == 1 else w}k/n}} = x, {{{w}/n}} = dx로 보면 {a}에서 {a + w}까지", memo="구분구적법"),
                     L(f"∫_{{{a}}}^{{{a + w}}}{POLY(cs)}dx = [{POLY(F)}]_{{{a}}}^{{{a + w}}} = {FR(ev(F, a + w))} − {FR(ev(F, a))} = {FR(val_)}")]
        S.add(5, q, FR(val_), "lim Σ{1/n}f({k/n}) = ∫_{0}^{1}f(x)dx", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 이차곡선 ══════════
def conic_plane(f, lo=-8, hi=8, at="q", step=2):
    pl = Plane(f, (lo - 0.5, hi + 0.5), (lo - 0.5, hi + 0.5), box=(40, 30, 620, 650))
    pl.axes(at=at, lab_step=step)
    return pl

def par_pts(pl, p, axis="x", sh=(0, 0), lim=8.4, n=60):
    """y^2 = 4px (axis x) 또는 x^2 = 4py (axis y) — sh 만큼 평행이동"""
    pts = []
    for i in range(n + 1):
        t = -lim + 2 * lim * i / n
        if axis == "x":
            X, Y = t * t / (4 * p) + sh[0], t + sh[1]
        else:
            X, Y = t + sh[0], t * t / (4 * p) + sh[1]
        if abs(X) <= lim and abs(Y) <= lim:
            pts.append(pl.P(X, Y))
    return pts

def conic():
    S = Set("conic", "이차곡선 — 포물선 · 타원 · 쌍곡선의 초점", "이차곡선",
            {1: "포물선의 초점과 준선", 2: "포물선의 정의", 3: "타원의 초점과 축", 4: "쌍곡선의 초점과 점근선", 5: "타원 · 쌍곡선의 정의"},
            pp=8,
            tips={1: "y^{2} = 4px: 초점 (p, 0), 준선 x = −p",
                  2: "포물선 위의 점에서 초점까지 거리 = 준선까지 거리",
                  3: "{x^{2}/a^{2}} + {y^{2}/b^{2}} = 1 (a > b): c^{2} = a^{2} − b^{2}, 초점 (±c, 0)",
                  4: "{x^{2}/a^{2}} − {y^{2}/b^{2}} = 1: c^{2} = a^{2} + b^{2}, 점근선 y = ±{b/a}x",
                  5: "타원 PF + PF' = 2a, 쌍곡선 |PF − PF'| = 2a"},
            note="이차곡선은 ‘거리의 조건’으로 정의된 곡선이에요. 식에서 a, b, c를 읽는 방법보다 정의(거리의 합 · 차 · 같음)를 먼저 그림으로 보여 주세요.")
    R = rng(2505)

    def g1():
        p = R.choice([1, 2, 3, 4, -1, -2, -3])
        axis = R.choice(["x", "y"])
        sh = (0, 0) if S.count(1) % 2 == 0 else (R.randint(-3, 3), R.randint(-3, 3))
        if S.count(1) % 2 == 1 and sh == (0, 0):
            return
        f = Fig()
        pl = conic_plane(f)
        f.poly(par_pts(pl, p, axis, sh), c="sky", w=4.5, z=False, dr=True)
        a, b = sh
        P4 = N(4 * p)
        if axis == "x":
            left = "y^{2}" if b == 0 else f"({XM(b, 'y')})^{{2}}"
            right = f"{P4}x" if a == 0 else f"{P4}({XM(a)})"
            F, dline = (a + p, b), f"x = {N(a - p)}"
            f.line(*pl.P(a - p, -8.4), *pl.P(a - p, 8.4), c="coral", w=2.5, d=True, at=1)
        else:
            left = "x^{2}" if a == 0 else f"({XM(a)})^{{2}}"
            right = f"{P4}y" if b == 0 else f"{P4}({XM(b, 'y')})"
            F, dline = (a, b + p), f"y = {N(b - p)}"
            f.line(*pl.P(-8.4, b - p), *pl.P(8.4, b - p), c="coral", w=2.5, d=True, at=1)
        eq = f"{left} = {right}"
        pl.pt(F[0], F[1], f="coral", label="F", pos="ne", at=1)
        ans = f"초점 ({N(F[0])}, {N(F[1])}), 준선 {dline}"
        base = f"{'y' if axis == 'x' else 'x'}^{{2}} = {P4}{axis}"
        q = f"포물선 {eq}의 초점의 좌표와 준선의 방정식을 구하세요."
        if sh == (0, 0):
            lines = [L(f"{P4} = 4 × {NP(p)} → p = {N(p)}", memo=f"{'y^{2} = 4px' if axis == 'x' else 'x^{2} = 4py'} 꼴"),
                     L(ans)]
        else:
            lines = [L(f"{base}를 x축 방향으로 {N(a)}, y축 방향으로 {N(b)}만큼 평행이동", memo=f"p = {N(p)}"),
                     L(f"{base}의 초점 " + (f"({N(p)}, 0)" if axis == "x" else f"(0, {N(p)})") + ", 준선 " + (f"x = {N(-p)}" if axis == "x" else f"y = {N(-p)}")),
                     L(ans, memo="함께 평행이동")]
        S.add(1, q, ans, "y^{2} = 4px → 초점 (p, 0), 준선 x = −p", lines, f.out(), ap=f"({N(F[0])}, {N(F[1])}); {dline}", omr="ex", sub={"p": p}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        p = R.choice([1, 2, 3, 4])
        axis = R.choice(["x", "y"])
        x0 = R.randint(1, 9)
        sg = R.choice([1, -1])
        y0 = sg * math.sqrt(4 * p * x0)
        k = S.count(2) % 2
        f = Fig()
        lim = max(8, x0 + 2, abs(y0) + 1.5)
        pl = Plane(f, (-lim - 0.5, lim + 0.5), (-lim - 0.5, lim + 0.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=2 if lim <= 9 else 4)
        if axis == "x":
            f.poly(par_pts(pl, p, "x", lim=lim + 0.4, n=80), c="sky", w=4.5, z=False, dr=True)
            f.line(*pl.P(-p, -lim - 0.4), *pl.P(-p, lim + 0.4), c="coral", w=2.5, d=True)
            pl.pt(p, 0, f="coral", label="F", pos="se")
            P_, H_ = (x0, y0), (-p, y0)
        else:
            f.poly(par_pts(pl, p, "y", lim=lim + 0.4, n=80), c="sky", w=4.5, z=False, dr=True)
            f.line(*pl.P(-lim - 0.4, -p), *pl.P(lim + 0.4, -p), c="coral", w=2.5, d=True)
            pl.pt(0, p, f="coral", label="F", pos="nw")
            P_, H_ = (y0, x0), (y0, -p)
        pl.pt(*P_, f="ink", label="P", pos="ne")
        f.line(*pl.P(*P_), *pl.P(*((p, 0) if axis == "x" else (0, p))), c="teal", w=3.5, at=0)
        f.line(*pl.P(*P_), *pl.P(*H_), c="teal", w=3.5, d=True, at=0)
        eq = f"y^{{2}} = {4 * p}x" if axis == "x" else f"x^{{2}} = {4 * p}y"
        co = "x좌표" if axis == "x" else "y좌표"
        drx = f"x = {N(-p)}" if axis == "x" else f"y = {N(-p)}"
        Fs = f"F({p}, 0)" if axis == "x" else f"F(0, {p})"
        if k == 0:
            q = f"포물선 {eq} 위의 점 P의 {co}가 {x0}일 때, 점 P와 초점 F 사이의 거리를 구하세요."
            ans = x0 + p
            lines = [L(f"초점 {Fs}, 준선 {drx}", memo=f"4p = {4 * p}"),
                     L(f"PF = (P에서 준선까지의 거리) = {x0} − ({N(-p)}) = {ans}", memo="포물선의 정의")]
            S.add(2, q, str(ans), "초점까지 거리 = 준선까지 거리", lines, f.out(), key=q)
        else:
            d = x0 + p
            v = "x" if axis == "x" else "y"
            q = f"포물선 {eq} 위의 점 P에서 초점 F까지의 거리가 {d}일 때, 점 P의 {co}를 구하세요."
            lines = [L(f"P에서 준선까지의 거리도 {d}", memo=f"포물선의 정의 · 준선 {drx}"),
                     L(f"{v} + {p} = {d} → {v} = {x0}")]
            S.add(2, q, str(x0), "초점까지 거리 = 준선까지 거리", lines, f.out(), sub={v: x0}, key=q)
    fill(S, 2, 20, g2)

    ELL = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12), (10, 8, 6), (10, 6, 8), (17, 15, 8), (17, 8, 15), (4, 3, None), (3, 2, None), (6, 4, None), (5, 2, None), (4, 2, None)]

    def g3():
        a, b, c = R.choice(ELL)
        c2 = a * a - b * b
        cs_ = RT(c2)
        vert = R.random() < 0.4
        A2, B2 = (b * b, a * a) if vert else (a * a, b * b)
        k = S.count(3) % 3
        f = Fig()
        sc = 8 / a
        pl = conic_plane(f)
        ep = [pl.P(sc * (b if vert else a) * math.cos(2 * math.pi * i / 72), sc * (a if vert else b) * math.sin(2 * math.pi * i / 72)) for i in range(73)]
        f.poly(ep, c="sky", w=4.5, z=False, dr=True)
        cv = math.sqrt(c2) * sc
        for sgn in (1, -1):
            if vert:
                pl.pt(0, sgn * cv, f="coral", at=1)
            else:
                pl.pt(sgn * cv, 0, f="coral", at=1)
        eq = f"{{x^{{2}}/{A2}}} + {{y^{{2}}/{B2}}} = 1"
        if k == 0:
            q = f"타원 {eq}의 두 초점의 좌표를 구하세요."
            ans = f"(0, {cs_}), (0, {MI}{cs_})" if vert else f"({cs_}, 0), ({MI}{cs_}, 0)"
            lines = [L(f"c^{{2}} = {max(A2, B2)} − {min(A2, B2)} = {c2}", memo="큰 쪽 − 작은 쪽"),
                     L(f"c = {cs_} → 초점 {ans}", memo="분모가 큰 쪽 축 위")]
            S.add(3, q, ans, "타원: c^{2} = (큰 분모) − (작은 분모)", lines, f.out(), omr="ex", key=q)
        elif k == 1:
            q = f"타원 {eq}의 장축의 길이와 단축의 길이의 합을 구하세요."
            ans = 2 * a + 2 * b
            lines = [L(f"장축 2√{{{a * a}}} = {2 * a}, 단축 2√{{{b * b}}} = {2 * b}", memo="큰 분모가 장축"),
                     L(f"{2 * a} + {2 * b} = {ans}")]
            S.add(3, q, str(ans), "장축 2a, 단축 2b", lines, f.out(), key=q)
        else:
            q = f"타원 {eq}의 두 초점 사이의 거리를 구하세요."
            ans = RT(4 * c2)
            lines = [L(f"c^{{2}} = {max(A2, B2)} − {min(A2, B2)} = {c2} → c = {cs_}"), L(f"두 초점 사이 2c = {ans}")]
            S.add(3, q, ans, "두 초점 사이의 거리 2c", lines, f.out(), omr="ex" if "√" in ans else "num", key=q)
    fill(S, 3, 20, g3)

    HYP = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10), (1, 2, None), (2, 1, None), (2, 3, None), (3, 1, None), (1, 1, None), (2, 2, None)]

    def g4():
        a, b, c = R.choice(HYP)
        c2 = a * a + b * b
        cs_ = RT(c2)
        k = S.count(4) % 3
        f = Fig()
        pl = conic_plane(f)
        sc = 3 / a
        A, B = a * sc, b * sc
        for sgn in (1, -1):
            pts = [pl.P(sgn * A * math.cosh(u / 20), B * math.sinh(u / 20)) for u in range(-60, 61)]
            pts = [p_ for p_, u in zip(pts, range(-60, 61)) if abs(B * math.sinh(u / 20)) <= 8.4 and abs(A * math.cosh(u / 20)) <= 8.4]
            f.poly(pts, c="sky", w=4.5, z=False, dr=True)
        pl.lineq(B / A, 0, c="coral", w=2.5, d=True, dr=False)
        pl.lineq(-B / A, 0, c="coral", w=2.5, d=True, dr=False)
        cv = math.sqrt(c2) * sc
        pl.pt(cv, 0, f="coral", at=1)
        pl.pt(-cv, 0, f="coral", at=1)
        eq = f"{{x^{{2}}/{a * a}}} − {{y^{{2}}/{b * b}}} = 1"
        if k == 0:
            q = f"쌍곡선 {eq}의 두 초점의 좌표를 구하세요."
            ans = f"({cs_}, 0), ({MI}{cs_}, 0)"
            lines = [L(f"c^{{2}} = {a * a} + {b * b} = {c2}", memo="쌍곡선은 더해요"), L(f"c = {cs_} → 초점 {ans}")]
            S.add(4, q, ans, "쌍곡선: c^{2} = a^{2} + b^{2}", lines, f.out(), omr="ex", key=q)
        elif k == 1:
            q = f"쌍곡선 {eq}의 점근선의 방정식을 구하세요."
            sl = Fr(b, a)
            ans = f"y = {FR(sl) if sl != 1 else ''}x, y = {MI}{FR(sl) if sl != 1 else ''}x"
            lines = [L(f"a = {a}, b = {b}", memo=f"a^{{2}} = {a * a}, b^{{2}} = {b * b}"), L(f"점근선 y = ±{{b/a}}x → {ans}")]
            S.add(4, q, ans, "점근선 y = ±{b/a}x", lines, f.out(), omr="ex", key=q)
        else:
            q = f"쌍곡선 {eq}의 주축의 길이를 구하세요."
            ans = 2 * a
            lines = [L(f"a^{{2}} = {a * a} → a = {a}", memo="x^{2}의 분모"), L(f"주축의 길이 2a = {ans}")]
            S.add(4, q, str(ans), "주축의 길이 2a", lines, f.out(), sub={"a": a}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k < 2:
            a, b, c = R.choice([e for e in ELL if e[2]])
            eq = f"{{x^{{2}}/{a * a}}} + {{y^{{2}}/{b * b}}} = 1"
            if k == 0:
                d = R.randint(a - c + 1, a + c - 1)
                q = f"타원 {eq}의 두 초점을 F, F'이라 하고, 타원 위의 점 P에 대하여 PF = {J(str(d), '일', '일')} 때, PF'의 길이를 구하세요."
                ans = 2 * a - d
                lines = [L(f"PF + PF' = 2 × {a} = {2 * a}", memo="타원의 정의"), L(f"PF' = {2 * a} − {d} = {ans}")]
            else:
                q = f"타원 {eq}의 두 초점을 F, F'이라 하고, 타원 위의 점 P에 대하여 삼각형 PFF'의 둘레의 길이를 구하세요."
                ans = 2 * a + 2 * c
                lines = [L(f"PF + PF' = 2 × {a} = {2 * a}", memo="타원의 정의"),
                         L(f"FF' = 2c = 2 × {c} = {2 * c}", memo=f"c^{{2}} = {a * a} − {b * b}"),
                         L(f"{2 * a} + {2 * c} = {ans}")]
            S.add(5, q, str(ans), "타원 위의 점: PF + PF' = 2a", lines, None, key=q)
        else:
            a, b, c = R.choice([e for e in HYP if e[2]])
            eq = f"{{x^{{2}}/{a * a}}} − {{y^{{2}}/{b * b}}} = 1"
            d = R.randint(c - a + 1, c + 6)
            q = f"쌍곡선 {eq}의 두 초점을 F, F'이라 하고, 쌍곡선 위의 점 P에 대하여 PF = {J(str(d), '일', '일')} 때, PF'의 길이를 구하세요. (단, PF' > PF)"
            ans = d + 2 * a
            lines = [L(f"PF' − PF = 2 × {a} = {2 * a}", memo="쌍곡선의 정의"), L(f"PF' = {d} + {2 * a} = {ans}")]
            S.add(5, q, str(ans), "쌍곡선 위의 점: |PF − PF'| = 2a", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 벡터 ══════════
def V(nm):
    return f"⃗{{{nm}}}"

def VP(a, b):
    return f"({N(a)}, {N(b)})"

def vec():
    S = Set("vec", "벡터 — 성분 · 크기 · 내적", "벡터",
            {1: "벡터의 성분 계산", 2: "벡터의 크기", 3: "성분으로 내적", 4: "크기와 각으로 내적", 5: "수직 · 평행 조건"},
            pp=10,
            tips={1: f"p{V('a')} + q{V('b')} — 성분끼리 곱하고 더해요",
                  2: f"{V('a')} = (x, y) → |{V('a')}| = √{{x^{{2}} + y^{{2}}}}",
                  3: f"{V('a')} · {V('b')} = a_{{1}}b_{{1}} + a_{{2}}b_{{2}}",
                  4: f"{V('a')} · {V('b')} = |{V('a')}||{V('b')}|cos θ, |{V('a')} + {V('b')}|^{{2}} = |{V('a')}|^{{2}} + 2{V('a')} · {V('b')} + |{V('b')}|^{{2}}",
                  5: f"수직 ⇔ {V('a')} · {V('b')} = 0, 평행 ⇔ 성분의 비가 같아요"},
            note="벡터는 ‘크기와 방향’을 함께 가진 화살이에요. 성분 계산은 화살을 이어 붙이는 그림과 함께, 내적은 ‘같은 방향으로 얼마나 겹치는지’로 설명해 주세요.")
    R = rng(2506)

    def arrow(f, pl, x1, y1, x2, y2, c, at="q", lab=None, lp="ne"):
        f.line(*pl.P(x1, y1), *pl.P(x2, y2), c=c, w=4.5, ar=1, at=at)
        if lab:
            mx, my = pl.P((x1 + x2) / 2, (y1 + y2) / 2)
            dx, dy = {"ne": (16, -12), "nw": (-16, -12), "se": (16, 30), "sw": (-16, 30)}[lp]
            f.text(mx + dx, my + dy, lab, z=28, c=c, at=at, b=700, a="s" if dx > 0 else "e")

    def g1():
        a1, a2, b1, b2 = [R.choice([-4, -3, -2, -1, 1, 2, 3, 4]) for _ in range(4)]
        p_, q_ = R.choice([1, 2, 3, -1, -2]), R.choice([1, 2, 3, -1, -2, -3])
        r1, r2 = p_ * a1 + q_ * b1, p_ * a2 + q_ * b2
        if max(abs(r1), abs(r2)) > 12:
            return
        ex = f"{'' if p_ == 1 else (MI if p_ == -1 else N(p_))}{V('a')} {'+' if q_ > 0 else MI} {'' if abs(q_) == 1 else abs(q_)}{V('b')}"
        q = f"두 벡터 {V('a')} = {VP(a1, a2)}, {V('b')} = {VP(b1, b2)}에 대하여 벡터 {ex}의 성분을 구하세요."
        lines = [L(f"{'' if p_ == 1 else (MI if p_ == -1 else N(p_))}{V('a')} = {VP(p_ * a1, p_ * a2)}, {'' if q_ == 1 else (MI if q_ == -1 else N(q_))}{V('b')} = {VP(q_ * b1, q_ * b2)}", memo="수를 성분마다 곱하기"),
                 L(f"({N(p_ * a1)} + {NP(q_ * b1)}, {N(p_ * a2)} + {NP(q_ * b2)}) = {VP(r1, r2)}", memo="성분끼리 더하기")]
        f = Fig()
        lim = max(8, abs(r1) + 1, abs(r2) + 1, abs(p_ * a1) + 1, abs(p_ * a2) + 1)
        pl = Plane(f, (-lim - 0.5, lim + 0.5), (-lim - 0.5, lim + 0.5), box=(40, 30, 620, 650))
        pl.axes(lab_step=2 if lim <= 9 else 4)
        arrow(f, pl, 0, 0, p_ * a1, p_ * a2, "sky", lab=f"{'' if p_ == 1 else (MI if p_ == -1 else N(p_))}{V('a')}")
        arrow(f, pl, p_ * a1, p_ * a2, r1, r2, "teal", at=0, lab=f"{'' if q_ == 1 else (MI if q_ == -1 else N(q_))}{V('b')}", lp="se")
        arrow(f, pl, 0, 0, r1, r2, "coral", at=1)
        S.add(1, q, VP(r1, r2), "실수배는 성분마다, 합은 성분끼리", lines, f.out(), ap=f"({r1}, {r2})".replace("-", MI), omr="pt", key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            x_, y_ = R.choice([(3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (8, 6), (1, 1), (1, 2), (2, 3), (1, 3), (2, 2)])
            x_, y_ = x_ * R.choice([1, -1]), y_ * R.choice([1, -1])
            b1, b2 = R.choice([-3, -2, -1, 1, 2, 3]), R.choice([-3, -2, -1, 1, 2, 3])
            a1, a2 = x_ - b1, y_ - b2
            mag = RT(x_ * x_ + y_ * y_)
            q = f"두 벡터 {V('a')} = {VP(a1, a2)}, {V('b')} = {VP(b1, b2)}에 대하여 |{V('a')} + {V('b')}|를 구하세요."
            lines = [L(f"{V('a')} + {V('b')} = ({N(a1)} + {NP(b1)}, {N(a2)} + {NP(b2)}) = {VP(x_, y_)}", memo="먼저 성분"),
                     L(f"|{V('a')} + {V('b')}| = √{{{NP(x_)}^{{2}} + {NP(y_)}^{{2}}}} = {mag}", memo="√{x^{2} + y^{2}}")]
        else:
            P1 = (R.randint(-4, 4), R.randint(-4, 4))
            d = R.choice([(3, 4), (4, 3), (5, 12), (6, 8), (1, 2), (2, 1), (1, 1), (2, 3), (3, 1)])
            d = (d[0] * R.choice([1, -1]), d[1] * R.choice([1, -1]))
            P2 = (P1[0] + d[0], P1[1] + d[1])
            mag = RT(d[0] ** 2 + d[1] ** 2)
            q = f"두 점 A{VP(*P1)}, B{VP(*P2)}에 대하여 |{V('AB')}|를 구하세요."
            lines = [L(f"{V('AB')} = ({N(P2[0])} − {NP(P1[0])}, {N(P2[1])} − {NP(P1[1])}) = {VP(*d)}", memo="끝점 − 시작점"),
                     L(f"|{V('AB')}| = √{{{NP(d[0])}^{{2}} + {NP(d[1])}^{{2}}}} = {mag}")]
        S.add(2, q, mag, "성분을 구한 뒤 √{x^{2} + y^{2}}", lines, None, omr="ex" if "√" in mag else "num", key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 2
        if k == 0:
            a1, a2, b1, b2 = [R.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]) for _ in range(4)]
            v = a1 * b1 + a2 * b2
            q = f"두 벡터 {V('a')} = {VP(a1, a2)}, {V('b')} = {VP(b1, b2)}의 내적 {V('a')} · {V('b')}를 구하세요."
            lines = [L(f"{V('a')} · {V('b')} = {N(a1)} × {NP(b1)} + {N(a2)} × {NP(b2)} = {N(v)}", memo="같은 자리 성분끼리 곱해 더하기")]
            S.add(3, q, N(v), f"{V('a')} · {V('b')} = a_{{1}}b_{{1}} + a_{{2}}b_{{2}}", lines, None, key=q)
        else:
            choices = [((1, 0), (1, 1), 45), ((1, 1), (0, 1), 45), ((1, 0), (0, 1), 90), ((1, 1), (1, -1), 90), ((1, 0), (-1, 1), 135),
                       ((1, 1), (-1, 0), 135), ((1, 0), (-1, 0), 180), ((0, 1), (1, 1), 45), ((1, -1), (0, 1), 135), ((1, 1), (-1, -1), 180)]
            (u1, u2), (w1, w2), th = R.choice(choices)
            s1, s2 = R.choice([1, 2, 3]), R.choice([1, 2, 3, 4])
            a1, a2, b1, b2 = u1 * s1, u2 * s1, w1 * s2, w2 * s2
            dot = a1 * b1 + a2 * b2
            ma2, mb2 = a1 * a1 + a2 * a2, b1 * b1 + b2 * b2
            q = f"두 벡터 {V('a')} = {VP(a1, a2)}, {V('b')} = {VP(b1, b2)}가 이루는 각의 크기 θ를 구하세요. (0° ≤ θ ≤ 180°)"
            cosv = {45: "{√{2}/2}", 90: "0", 135: f"{MI}{{√{{2}}/2}}", 180: f"{MI}1"}[th]
            lines = [L(f"{V('a')} · {V('b')} = {N(dot)}, |{V('a')}| = {RT(ma2)}, |{V('b')}| = {RT(mb2)}"),
                     L(f"cos θ = {{{N(dot)}/{RT(ma2)} × {RT(mb2)}}} = {cosv}", memo="cos θ = {a · b/|a||b|}"),
                     L(f"θ = {th}°")]
            S.add(3, q, f"{th}°", "cos θ = 내적 ÷ (크기의 곱)", lines, None, ap=str(th), key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 2
        ma, mb = R.randint(1, 6), R.randint(1, 6)
        th = R.choice([60, 120, 90, 45, 135, 30, 150])
        cosv = {60: Fr(1, 2), 120: Fr(-1, 2), 90: Fr(0)}.get(th)
        coss = {60: "{1/2}", 120: f"({MI}{{1/2}})", 90: "0", 45: "{√{2}/2}", 135: f"({MI}{{√{{2}}/2}})", 30: "{√{3}/2}", 150: f"({MI}{{√{{3}}/2}})"}[th]
        dot_sym = ma * mb * {60: sp.Rational(1, 2), 120: -sp.Rational(1, 2), 90: 0, 45: sp.sqrt(2) / 2, 135: -sp.sqrt(2) / 2, 30: sp.sqrt(3) / 2, 150: -sp.sqrt(3) / 2}[th]
        if k == 0:
            q = f"|{V('a')}| = {ma}, |{V('b')}| = {mb}이고 두 벡터 {V('a')}, {V('b')}가 이루는 각의 크기가 {th}°일 때, {V('a')} · {V('b')}를 구하세요."
            ans = SURD(dot_sym)
            lines = [L(f"{V('a')} · {V('b')} = |{V('a')}||{V('b')}|cos {th}°", memo="크기와 각으로"),
                     L(f"{ma} × {mb} × {coss} = {ans}")]
            S.add(4, q, ans, "a · b = |a||b|cos θ", lines, None, omr="ex" if "√" in ans else "num", key=q)
        else:
            if cosv is None:
                return
            s2 = ma * ma + mb * mb + 2 * ma * mb * cosv
            if s2 <= 0:
                return
            ans = RT(int(s2)) if Fr(s2).denominator == 1 else None
            if ans is None:
                return
            q = f"|{V('a')}| = {ma}, |{V('b')}| = {mb}이고 두 벡터 {V('a')}, {V('b')}가 이루는 각의 크기가 {th}°일 때, |{V('a')} + {V('b')}|를 구하세요."
            lines = [L(f"{V('a')} · {V('b')} = {ma} × {mb} × {coss} = {FR(ma * mb * cosv)}"),
                     L(f"|{V('a')} + {V('b')}|^{{2}} = {ma}^{{2}} + 2 × {NP(ma * mb * cosv)} + {mb}^{{2}} = {N(s2)}", memo="전개해서 크기의 제곱"),
                     L(f"|{V('a')} + {V('b')}| = {ans}")]
            S.add(4, q, ans, "|a + b|^{2}을 전개해서", lines, None, omr="ex" if "√" in ans else "num", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 2
        a1 = R.choice([-4, -3, -2, -1, 1, 2, 3, 4])
        b1, b2 = R.choice([-6, -4, -3, -2, 2, 3, 4, 6]), R.choice([-6, -4, -3, -2, 2, 3, 4, 6])
        if k == 0:
            kv = Fr(-a1 * b1, b2)
            if kv.denominator != 1:
                return
            q = f"두 벡터 {V('a')} = ({N(a1)}, k), {V('b')} = {VP(b1, b2)}가 서로 수직일 때, k의 값을 구하세요."
            lines = [L(f"{V('a')} · {V('b')} = {N(a1)} × {NP(b1)} + k × {NP(b2)} = 0", memo="수직 ⇔ 내적 0"),
                     L(f"k = {N(kv)}")]
            S.add(5, q, N(kv), "수직이면 내적이 0", lines, None, sub={"k": kv}, key=q)
        else:
            kv = Fr(a1 * b2, b1)
            if kv.denominator != 1:
                return
            q = f"두 벡터 {V('a')} = ({N(a1)}, k), {V('b')} = {VP(b1, b2)}가 서로 평행할 때, k의 값을 구하세요."
            lines = [L(f"{V('a')} = t{V('b')} → {N(a1)} = {N(b1)}t, k = {N(b2)}t", memo="평행 ⇔ 실수배"),
                     L(f"t = {FR(Fr(a1, b1))} → k = {N(b2)} × {NP(Fr(a1, b1))} = {N(kv)}")]
            S.add(5, q, N(kv), "평행이면 한쪽이 다른 쪽의 실수배", lines, None, sub={"k": kv, "t": Fr(a1, b1)}, key=q)
    fill(S, 5, 20, g5)
    return S
