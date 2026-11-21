# 초6 — ① 분수의 나눗셈 — 몇 번 들어가나 · ② 비와 비율 · 비례식과 비례배분
from math import gcd
from core import *
from fig import Fig, mv, fbar, ffill

def F_(n, d):
    return "{%d/%d}" % (n, d)

def lcm(a, b):
    return a * b // gcd(a, b)

# ══════════ ① 분수의 나눗셈 ══════════
def set_a():
    S = Set("a", "분수의 나눗셈 — 몇 번 들어가나", "분수의 나눗셈",
            {1: "(자연수)÷(자연수)", 2: "(분수)÷(자연수)", 3: "분모가 같은 (분수)÷(분수)", 4: "분모가 다른 (분수)÷(분수)", 5: "대분수 · 자연수 ÷ 분수 · 문장제"},
            mixed=True, pp=10,
            tips={1: "■ ÷ ● = {■/●} — 3 ÷ 5 = {3/5}",
                  2: "분자가 나누어떨어지면 분자를 나누고, 아니면 ÷ 3 = × {1/3}",
                  3: "분모가 같으면 분자끼리 나눠요 — {6/7} ÷ {2/7} = 6 ÷ 2",
                  4: "통분하면 분자끼리 나누기 — 결국 나누는 분수를 뒤집어 곱하는 것과 같아요",
                  5: "대분수는 가분수로 바꾸고, 나누는 분수를 뒤집어 곱해요"},
            note="‘몇 번 들어가나(포함)’와 ‘똑같이 나누기(등분)’ 두 그림으로 나눗셈을 보게 해 주세요. 뒤집어 곱하는 이유는 통분해서 분자끼리 나누는 것과 같기 때문이에요.")
    R = rng(601)

    def g1():
        a = R.randint(1, 9); b = R.randint(2, 9)
        if a == b or a % b == 0:
            return
        f = Fig()
        BX, BW, BH, Y = 40, 580, 80, 230
        unit = BW / max(a, b) if a > b else BW / b
        tot = unit * a
        f.grid(BX, Y, unit, BH, a, 1, c="ink", sw=3)
        for i in range(a):
            f.text(BX + unit * i + unit / 2, Y - 16, "1", z=26, c="soft")
        for i in range(1, b):
            x = BX + tot * i / b
            f.line(x, Y - 6, x, Y + BH + 6, at=0, c="red", w=3, d=True, dl=i * 120)
        f.rect(BX + 2, Y + 2, tot / b - 4, BH - 4, at=1, c="none", f="gold", fo=0.55)
        v = Fr(a, b)
        f.text(BX + tot / (2 * b), Y + BH + 60, F_(a, b), z=44, c="gold", at=1, b=700)
        lines = [L(f"1 ÷ {b} = {F_(1, b)}", memo=f"1을 {RO(b)} 똑같이"), L(f"{a} ÷ {b} = {F_(1, b)} × {a} = {F_(a, b)}")]
        if a > b:
            lines.append(L(f"{F_(a, b)} = {MX(v)}", memo="대분수로"))
        S.add(1, f"{a} ÷ {J(b, '을', '를')} 분수로 나타내세요.", MX(v), f"{J(a, '을', '를')} {RO(b)} 똑같이 나눈 한 칸", lines, f.out(), ap=plain(MX(v)), key=f"{a}/{b}")
    fill(S, 1, 20, g1)

    def g2():
        d = R.randint(2, 9); n = R.randint(1, 3 * d); k = R.randint(2, 6)
        if gcd(n, d) != 1 or n >= d and R.random() < 0.6:
            return
        v = Fr(n, d) / k
        if n % k == 0:
            lines = [L(f"분자 {J(n, '을', '를')} {RO(k)} 나눌 수 있어요"), L(f"{F_(n, d)} ÷ {k} = {{{n} ÷ {k}/{d}}} = {F_(n // k, d)}")]
            plan, f = "분자를 나누어요", None
        else:
            lines = [L(f"÷ {k} = × {F_(1, k)}", memo=f"{F_(1, k)}만큼"), L(f"{F_(n, d)} ÷ {k} = {F_(n, d)} × {F_(1, k)} = {F_(n, d * k)}")]
            plan = f"{RO(k)} 나누기 = {F_(1, k)} 곱하기"
            f = None
            if n < d and d * k <= 40:
                f = Fig()
                BX, BY, BW, BH = 60, 140, 540, 340
                f.grid(BX, BY, BW / d, BH, d, 1, c="ink", sw=3)
                for i in range(n):
                    f.rect(BX + BW / d * i + 2, BY + 2, BW / d - 4, BH - 4, c="none", f="gold", fo=0.4)
                for j in range(1, k):
                    f.line(BX, BY + BH * j / k, BX + BW, BY + BH * j / k, at=0, c="red", w=3, d=True)
                for i in range(n):
                    f.rect(BX + BW / d * i + 4, BY + 4, BW / d - 8, BH / k - 8, at=1, c="none", f="teal", fo=0.6, dl=i * 80)
                f.text(330, BY + BH + 70, f"전체 {d * k}칸 중 {n}칸 → {F_(n, d * k)}", z=34, c="teal", at=1, b=700)
        v2 = Fr(n, d * k) if n % k else Fr(n // k, d)
        assert v2 == v
        ans = N(v2) if v2.denominator != 1 else str(v2)
        S.add(2, f"{F_(n, d)} ÷ {J(k, '은', '는')} 얼마인가요?", F_(v2.numerator, v2.denominator) if v2.denominator != 1 else str(v2.numerator), plan, lines, f.out() if f else None, key=f"{n}/{d}÷{k}")
    fill(S, 2, 20, g2)

    def g3():
        d = R.randint(3, 12); a = R.randint(2, d - 1); b = R.randint(1, d - 1)
        if a == b:
            return
        v = Fr(a, b)
        f = Fig()
        BX, BY, BW, BH = 40, 220, 580, 80
        fbar(f, BX, BY, BW, BH, d)
        ffill(f, BX, BY, BW, BH, d, 0, a, "gold", "q", fo=0.45, step=50)
        cw = BW / d
        for g in range(a // b):
            f.rect(BX + cw * b * g + 3, BY - 8, cw * b - 6, BH + 16, at=0, c="teal", sw=4, rx=10, dl=g * 250)
        if a % b:
            f.rect(BX + cw * b * (a // b) + 3, BY - 8, cw * (a % b) - 6, BH + 16, at=0, c="red", sw=3, rx=10, d=True, dl=(a // b) * 250)
        f.text(330, BY + BH + 80, f"{F_(b, d)}" + (f" 묶음 {a // b}개" if a % b == 0 else f" 묶음 {a // b}개와 조금 더"), z=34, c="teal", at=0, dl=(a // b) * 250 + 300)
        lines = [L(f"{F_(1, d)}이 {a}개 ÷ {F_(1, d)}이 {b}개", memo="분자끼리"), L(f"{F_(a, d)} ÷ {F_(b, d)} = {a} ÷ {b} = {F_(a, b) if a % b else a // b}")]
        if a % b and a > b:
            lines.append(L(f"{F_(a, b)} = {MX(v)}"))
        ans = MX(v)
        S.add(3, f"{F_(a, d)} ÷ {J(F_(b, d), '은', '는')} 얼마인가요?", ans, f"{F_(a, d)}에 {F_(b, d)}" + ("이 몇 번 들어가는지" if True else ""), lines, f.out(), ap=plain(ans), key=f"{a}/{b}/{d}")
    fill(S, 3, 20, g3)

    def g4():
        b = R.randint(2, 9); d = R.randint(2, 9)
        if b == d:
            return
        a = R.randint(1, b - 1); c = R.randint(1, d - 1)
        if gcd(a, b) != 1 or gcd(c, d) != 1:
            return
        L_ = lcm(b, d)
        A, C = a * L_ // b, c * L_ // d
        v = Fr(a, b) / Fr(c, d)
        lines = [L(f"통분 {F_(a, b)} ÷ {F_(c, d)} = {F_(A, L_)} ÷ {F_(C, L_)}", memo="분모를 같게"), L(f"{A} ÷ {C} = {F_(A, C)}"),
                 L(f"{F_(a, b)} × {F_(d, c)} = {F_(a * d, b * c)}", memo="뒤집어 곱해도 같아요")]
        if v.denominator != v.numerator and (v.denominator != A and Fr(A, C) != v or True):
            tail = [x for x in dict.fromkeys([N(v), MX(v)]) if x not in (F_(a * d, b * c),)]
            if tail and (Fr(a * d, b * c).denominator != v.denominator or v > 1):
                lines.append(L(f"{F_(a * d, b * c)} = " + " = ".join(tail)))
        ans = MX(v)
        S.add(4, f"{F_(a, b)} ÷ {J(F_(c, d), '은', '는')} 얼마인가요?", ans, "통분해서 분자끼리 나누거나, 뒤집어 곱해요", lines, None, ap=plain(ans), key=f"{a}/{b}÷{c}/{d}")
    fill(S, 4, 20, g4)

    CTX = [("주스 {A} L를 {B} L씩 컵에 나누어 담으면 몇 컵이 되나요?", "컵"), ("리본 {A} m를 {B} m씩 자르면 몇 도막이 되나요?", "도막"),
           ("밀가루 {A} kg을 한 번에 {B} kg씩 쓰면 몇 번 쓸 수 있나요?", "번")]
    def g5():
        k = S.count(5) % 4
        if k in (0, 1):
            w = R.randint(1, 4); d = R.randint(2, 8); n = R.randint(1, d - 1)
            c = R.randint(1, 7); e = R.randint(c + 1, 9)
            if gcd(n, d) != 1 or gcd(c, e) != 1:
                return
            A = w * d + n
            v = Fr(A, d) / Fr(c, e)
            lines = [L(f"{w}{F_(n, d)} = {F_(A, d)}", memo="가분수로"), L(f"{F_(A, d)} ÷ {F_(c, e)} = {F_(A, d)} × {F_(e, c)} = {F_(A * e, d * c)}")]
            if Fr(A * e, d * c).denominator != d * c or v > 1:
                tail = [x for x in dict.fromkeys([N(v), MX(v)]) if x != F_(A * e, d * c)]
                if tail:
                    lines.append(L(f"{F_(A * e, d * c)} = " + " = ".join(tail)))
            q = f"{w}{F_(n, d)} ÷ {J(F_(c, e), '은', '는')} 얼마인가요?"
        elif k == 2:
            m = R.randint(2, 12); c = R.randint(1, 8); e = R.randint(c + 1, 9)
            if gcd(c, e) != 1:
                return
            v = Fr(m) / Fr(c, e)
            lines = [L(f"{m} ÷ {F_(c, e)} = {m} × {F_(e, c)}", memo="뒤집어 곱하기"), L(f"{m} × {F_(e, c)} = {F_(m * e, c)}")]
            if v.denominator != c or v > 1:
                tail = [x for x in dict.fromkeys([N(v), MX(v)]) if x != F_(m * e, c)]
                if tail:
                    lines.append(L(f"{F_(m * e, c)} = " + " = ".join(tail)))
            q = f"{m} ÷ {J(F_(c, e), '은', '는')} 얼마인가요?"
        else:
            t, u = CTX[R.randint(0, len(CTX) - 1)]
            d = R.randint(3, 12); b = R.randint(2, 4); kk = R.randint(2, 6)
            a = b * kk
            if a >= 3 * d:
                return
            Av, Bv = Fr(a, d), Fr(b, d)
            if Av.denominator != d or Bv.denominator != d:
                return
            v = Av / Bv
            lines = [L(f"{F_(a, d)} ÷ {F_(b, d)}", memo="몇 번 들어가나"), L(f"{a} ÷ {b} = {kk}", memo="분모가 같으면 분자끼리")]
            q = t.format(A=MX(Av), B=F_(b, d))
            S.add(5, q, f"{kk}{u}", "‘몇 번 들어가나’는 나눗셈", lines, None, ap=str(kk), key=q)
            return
        ans = MX(v)
        S.add(5, q, ans, "대분수는 가분수로, 나누는 분수는 뒤집어 곱해요", lines, None, ap=plain(ans), key=q)
    fill(S, 5, 20, g5)
    return S

def _bat(n):
    return str(n)[-1] in "013678"


# ══════════ ② 비와 비율 ══════════
def tape(f, parts, total=None, at_split=0, labels=None, lab_at=None, cols=("gold", "teal", "lilac")):
    """띠 그림 — parts: 칸 수 목록(비) · labels: 각 부분 아래 글자"""
    n = sum(parts)
    BX, BY, BW, BH = 40, 250, 580, 90
    cw = BW / n
    f.rect(BX, BY, BW, BH, c="ink", sw=3, rx=6)
    if total is not None:
        f.line(BX, BY - 40, BX + BW, BY - 40, c="soft", w=2, ar=2)
        f.text(BX + BW / 2, BY - 52, str(total), z=36, b=700)
    x = BX
    for i, p in enumerate(parts):
        f.rect(x + 2, BY + 2, cw * p - 4, BH - 4, at="q", c="none", f=cols[i % 3], fo=0.35)
        for j in range(1, p):
            f.line(x + cw * j, BY, x + cw * j, BY + BH, at=at_split, c="ink", w=1.6, d=True)
        if i:
            f.line(x, BY - 8, x, BY + BH + 8, c="ink", w=4)
        if labels:
            f.text(x + cw * p / 2, BY + BH + 60, labels[i], z=38, c=cols[i % 3], at=lab_at if lab_at is not None else 1, b=700)
        x += cw * p
    return BX, BY, cw

def set_b():
    S = Set("b", "비와 비율 · 비례식과 비례배분", "비와 비율",
            {1: "비율 — 분수 · 소수 · 백분율", 2: "가장 간단한 자연수의 비", 3: "비례식", 4: "비례배분", 5: "비율이 쓰이는 곳"},
            pp=10,
            tips={1: "(비율) = (비교하는 양) ÷ (기준량) · 백분율은 × 100 %",
                  2: "비의 앞뒤에 0이 아닌 같은 수를 곱하거나 나누어도 비율은 같아요",
                  3: "외항의 곱 = 내항의 곱 — 3 : 5 = □ : 20 → 3 × 20 = 5 × □",
                  4: "전체를 (앞 + 뒤)칸으로 나누어 한 칸의 크기부터",
                  5: "할인 = 정가 × 할인율 · 실제 거리 = 지도 거리 × 축척의 뒤 수"},
            note="비는 ‘기준량에 대한 비교하는 양’이에요. 띠 그림으로 한 칸의 크기를 먼저 구하게 하면 비례배분 · 비례식이 한 가지 생각으로 이어져요.")
    R = rng(602)

    def g1():
        b = R.choice([2, 4, 5, 8, 10, 20, 25, 40, 50]); a = R.randint(1, b * 2)
        v = Fr(a, b)
        if a == b or v.denominator == 1:
            return
        k = S.count(1) % 3
        dec = DEC(v)
        pct = v * 100
        if pct.denominator != 1:
            return
        pct = pct.numerator
        q = (f"{J(b, '에', '에')} 대한 {a}의 비율을 기약분수로 나타내세요." if k == 0 else
             f"{a} : {b}의 비율을 소수로 나타내세요." if k == 1 else
             f"{b}에 대한 {a}의 비율은 몇 %인가요?")
        lines = [L(f"기준량 {b}, 비교하는 양 {a}"), L(f"(비율) = {F_(a, b)} = {N(v)}" if v.denominator != b else f"(비율) = {F_(a, b)}")]
        if k >= 1:
            lines.append(L(f"{N(v)} = {dec}", memo="소수로"))
        if k == 2:
            lines.append(L(f"{dec} × 100 = {pct}", memo="백분율은 × 100"))
        ans = N(v) if k == 0 else dec if k == 1 else f"{pct} %"
        S.add(1, q.replace(f"{b}에 대한", f"{b}에 대한"), ans, "(비율) = (비교하는 양) ÷ (기준량)", lines, None, ap=str(pct) if k == 2 else plain(ans), key=f"{k}{a}/{b}")
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 4
        if k in (0, 1):
            g = R.randint(2, 12); a = R.randint(1, 9); b = R.randint(1, 9)
            if gcd(a, b) != 1 or a == b:
                return
            A, B = a * g, b * g
            q = f"{A} : {J(B, '을', '를')} 가장 간단한 자연수의 비로 나타내세요."
            lines = [L(f"{A}과 {B}의 최대공약수 {g}" if _bat(A) else f"{A}와 {B}의 최대공약수 {g}"), L(f"{A} ÷ {g} = {a}, {B} ÷ {g} = {b}"), L(f"→ {a} : {b}")]
        elif k == 2:
            a = R.randint(1, 9); b = R.randint(1, 9); g = R.randint(1, 4)
            if gcd(a, b) != 1 or a == b:
                return
            A, B = Fr(a * g, 10), Fr(b * g, 10)
            q = f"{DEC(A)} : {J(DEC(B), '을', '를')} 가장 간단한 자연수의 비로 나타내세요."
            lines = [L(f"× 10 → {a * g} : {b * g}", memo="소수는 10을 곱해요")]
            if g > 1:
                lines.append(L(f"÷ {g} → {a} : {b}"))
        else:
            p, r = R.randint(2, 9), R.randint(2, 9)
            if p == r:
                return
            m = lcm(p, r)
            a, b = m // p, m // r
            g = gcd(a, b)
            a, b = a // g, b // g
            q = f"{F_(1, p)} : {J(F_(1, r), '을', '를')} 가장 간단한 자연수의 비로 나타내세요."
            lines = [L(f"× {m} → {m // p} : {m // r}", memo="분모의 최소공배수를 곱해요")]
            if g > 1:
                lines.append(L(f"÷ {g} → {a} : {b}"))
        S.add(2, q, f"{a} : {b}", "비의 앞과 뒤에 같은 수를 곱하거나 나눠요", lines, None, ap=f"{a}:{b}", omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        a = R.randint(1, 9); b = R.randint(2, 12); k = R.randint(2, 8)
        if gcd(a, b) != 1:
            return
        c, d = a * k, b * k
        pos = S.count(3) % 4
        terms = [str(a), str(b), str(c), str(d)]
        ans = terms[pos]
        terms[pos] = "□"
        q = f"비례식 {terms[0]} : {terms[1]} = {terms[2]} : {terms[3]}에서 □에 알맞은 수는?"
        outer = f"{terms[0]} × {terms[3]}"
        inner = f"{terms[1]} × {terms[2]}"
        known = (b * c) if pos in (0, 3) else (a * d)
        other = [x for x in ([terms[0], terms[3]] if pos in (0, 3) else [terms[1], terms[2]]) if x != "□"][0]
        lines = [L("외항의 곱 = 내항의 곱"), L(f"{outer} = {inner}"), L(f"{other} × □ = {known}"), L(f"□ = {known} ÷ {other} = {ans}")]
        S.add(3, q, ans, "외항의 곱과 내항의 곱이 같아요", lines, None, key=q)
    fill(S, 3, 20, g3)

    NAMES = [("형", "동생"), ("언니", "동생"), ("1반", "2반"), ("민서", "지호"), ("빨간 구슬", "파란 구슬")]
    def g4():
        a = R.randint(1, 7); b = R.randint(1, 7)
        if gcd(a, b) != 1 or a == b:
            return
        u = R.randint(2, 15); T = (a + b) * u
        nm = NAMES[S.count(4) % len(NAMES)]
        f = Fig()
        tape(f, [a, b], total=T, labels=[str(a * u), str(b * u)], lab_at=2)
        if S.count(4) % 2 == 0:
            q = f"{J(T, '을', '를')} {a} : {b}로 비례배분하세요."
            ans, ap = f"{a * u}, {b * u}", f"{a * u}, {b * u}"
            lines = [L(f"전체 {a} + {b} = {a + b}칸"), L(f"한 칸 {T} ÷ {a + b} = {u}"), L(f"{a}칸 {u} × {a} = {a * u}, {b}칸 {u} × {b} = {b * u}")]
        else:
            q = f"{nm[0]}와 {nm[1]}가 {T}개를 {a} : {b}로 나누어 가지면 {nm[0]}는 몇 개를 가지나요?" if not _batw(nm[0]) else f"{nm[0]}과 {nm[1]}가 {T}개를 {a} : {b}로 나누어 가지면 {nm[0]}은 몇 개를 가지나요?"
            ans, ap = f"{a * u}개", str(a * u)
            lines = [L(f"전체 {a} + {b} = {a + b}칸"), L(f"한 칸 {T} ÷ {a + b} = {u}"), L(f"{nm[0]} {a}칸 → {u} × {a} = {a * u}")]
        S.add(4, q, ans, "전체를 칸으로 나누어 한 칸부터", lines, f.out(), ap=ap, omr="ex" if "," in ans else "num", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        if k == 0:
            p = R.choice([10, 15, 20, 25, 30, 40]); price = R.randint(4, 40) * 1000
            dc = price * p // 100
            q = f"정가 {com(price)}원인 물건을 {p} % 할인해서 사면 얼마를 내야 하나요?"
            lines = [L(f"할인 금액 {com(price)} × {DEC(Fr(p, 100))} = {com(dc)}"), L(f"{com(price)} − {com(dc)} = {com(price - dc)}")]
            S.add(5, q, f"{com(price - dc)}원", "할인 금액 = 정가 × 할인율", lines, None, ap=str(price - dc), key=q)
        elif k == 1:
            sc = R.choice([10000, 20000, 25000, 50000, 100000]); cm = R.randint(2, 9)
            real = cm * sc
            q = f"축척이 1 : {sc}인 지도에서 {cm} cm는 실제로 몇 m인가요?"
            lines = [L(f"실제 거리 = {cm} × {sc} = {real}", memo="cm"), L(f"{real} cm → {real // 100} m", memo="100 cm = 1 m")]
            S.add(5, q, f"{com(real // 100)} m", "실제 거리 = 지도의 거리 × 축척의 뒤 수", lines, None, ap=str(real // 100), key=q)
        elif k == 2:
            h = R.randint(2, 5); v = R.randint(4, 12) * 10
            q = f"{h}시간 동안 {h * v} km를 달린 자동차의 속력은 시속 몇 km인가요?"
            lines = [L("(속력) = (거리) ÷ (시간)"), L(f"{h * v} ÷ {h} = {v}")]
            S.add(5, q, f"시속 {v} km", "1시간에 가는 거리", lines, None, ap=str(v), key=q)
        else:
            n = R.randint(20, 50); hit = R.randint(5, n // 2)
            v = Fr(hit, n)
            if (v * 1000).denominator != 1:
                return
            q = f"{n}타수 {hit}안타를 친 타자의 타율을 소수로 나타내세요."
            lines = [L("(타율) = (안타 수) ÷ (타수)"), L(f"{hit} ÷ {n} = {F_(hit, n)} = {DEC(v)}")]
            S.add(5, q, DEC(v), "기준량 = 타수, 비교하는 양 = 안타 수", lines, None, ap=DEC(v), key=q)
    fill(S, 5, 20, g5)
    return S

def _batw(w):
    ch = w[-1]
    return "가" <= ch <= "힣" and (ord(ch) - 0xAC00) % 28 != 0

GRADE = {"key": "e6", "grade": "초6", "level": "초등", "icon": "⚖️", "title": "초6 · 분수의 나눗셈 · 비와 비율",
         "desc": "분수의 나눗셈 — 몇 번 들어가나 100제 · 비와 비율 · 비례식과 비례배분 100제(띠 그림).",
         "thumb": ("a", 50), "sets": [set_a, set_b]}
