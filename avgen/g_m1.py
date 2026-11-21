# 중1 — ① 정수와 유리수의 계산 — 수직선 위에서 · ② 일차방정식 — 저울과 이항
from math import gcd
from core import *
from fig import Fig, mv, NL

def F_(n, d):
    return "{%d/%d}" % (n, d)

def S_(v):
    """부호 붙인 괄호 (+3) · (−{1/2})"""
    return SG(v)

def nz(R, lo=1, hi=9):
    v = R.randint(lo, hi)
    return v if R.random() < 0.5 else -v

# ══════════ ① 정수와 유리수 ══════════
def set_a():
    S = Set("a", "정수와 유리수의 계산 — 수직선 위에서", "정수와 유리수",
            {1: "수직선 · 절댓값 · 대소", 2: "덧셈", 3: "뺄셈", 4: "곱셈 · 나눗셈 · 거듭제곱", 5: "혼합 계산"},
            mixed=True, pp=10,
            tips={1: "절댓값 = 0에서의 거리 · 음수는 절댓값이 클수록 작아요",
                  2: "부호가 같으면 절댓값의 합에 공통 부호, 다르면 절댓값의 차에 절댓값이 큰 쪽 부호",
                  3: "빼기는 부호를 바꿔 더하기 — (+4) − (−6) = (+4) + (+6)",
                  4: "곱하는 음수가 짝수 개면 +, 홀수 개면 − · (−1)을 곱하면 수직선에서 0을 중심으로 180° 돌아요",
                  5: "거듭제곱 → 괄호 → 곱셈 · 나눗셈 → 덧셈 · 뺄셈 차례로"},
            note="수직선 위 위치를 먼저 떠올리게 해 주세요. 부호 계산 규칙은 ‘오른쪽(+) · 왼쪽(−)으로 가기’와 ‘180° 돌기(× (−1))’ 두 그림으로 설명할 수 있어요.")
    R = rng(1101)

    def g1():
        k = S.count(1) % 4
        f = Fig()
        if k == 0:
            a, b = nz(R), nz(R)
            if a == b:
                return
            nl = NL(f, -10, 10, lab_step=5)
            nl.pt(a, label=N(a))
            nl.pt(b, label=N(b), f_="teal")
            nl.jump(0, a, at=0, c="gold", up=False, label=str(abs(a)))
            nl.jump(0, b, at=1, c="teal", up=False, label=str(abs(b)))
            q = f"|{N(a)}| + |{N(b)}|의 값을 구하세요."
            lines = [L(f"|{N(a)}| = {abs(a)}", memo="0에서의 거리"), L(f"|{N(b)}| = {abs(b)}"), L(f"{abs(a)} + {abs(b)} = {abs(a) + abs(b)}")]
            S.add(1, q, str(abs(a) + abs(b)), "절댓값은 0에서 그 수까지의 거리", lines, f.out(), key=q)
        elif k == 1:
            d1, d2 = R.randint(2, 5), R.randint(2, 5)
            n1, n2 = -R.randint(d1 + 1, 4 * d1), R.randint(1, 3 * d2)
            v1, v2 = Fr(n1, d1), Fr(n2, d2)
            if v1.denominator == 1 or v2.denominator == 1:
                return
            ints = [z for z in range(-12, 13) if v1 < z < v2]
            if not ints or len(ints) > 9:
                return
            lo, hi = min(-5, int(v1) - 2), max(5, int(v2) + 2)
            nl = NL(f, lo, hi, lab_step=1)
            nl.pt(v1, label=N(v1))
            nl.pt(v2, label=N(v2), f_="teal")
            for i, z in enumerate(ints):
                f.dot(nl.X(z), nl.y, r=9, f="coral", at=1, dl=i * 120)
            q = f"{N(v1)}과 {N(v2)} 사이에 있는 정수는 모두 몇 개인가요?" if _bt(v1) else f"{N(v1)}와 {N(v2)} 사이에 있는 정수는 모두 몇 개인가요?"
            lines = [L(f"{N(v1)} = {MX(-v1).join(['−', ''])}" if False else f"{N(v1)} = −{MX(-v1)}, {N(v2)} = {MX(v2)}", memo="대분수로 위치 가늠"),
                     L("사이의 정수: " + ", ".join(N(z) for z in ints)), L(f"모두 {len(ints)}개")]
            S.add(1, q, f"{len(ints)}개", "수직선에 두 수를 찍고 사이의 정수를 세요", lines, f.out(), ap=str(len(ints)), key=q)
        elif k == 2:
            d1, d2 = R.randint(2, 6), R.randint(2, 6)
            n1, n2 = R.randint(1, d1 - 1), R.randint(1, d2 - 1)
            v1, v2 = -Fr(n1, d1), -Fr(n2, d2)
            if v1 == v2 or v1.denominator != d1 or v2.denominator != d2 or d1 == d2:
                return
            L_ = d1 * d2 // gcd(d1, d2)
            sm = min(v1, v2)
            nl = NL(f, -1, 1, step=Fr(1, L_) if L_ <= 12 else 0.25, lab_step=1)
            nl.pt(v1, label=N(v1), up=True)
            nl.pt(v2, label=N(v2), f_="teal", up=False)
            q = f"{N(v1)}, {N(v2)} 중에서 더 작은 수는 무엇인가요?"
            lines = [L(f"통분 −{F_(n1 * L_ // d1, L_)}, −{F_(n2 * L_ // d2, L_)}"), L("음수는 절댓값이 클수록 작아요"), L(f"{N(sm)} < {N(max(v1, v2))}")]
            S.add(1, q, N(sm), "통분해서 절댓값을 비교해요", lines, f.out(), ap=plain(N(sm)), key=q)
        else:
            a = R.randint(2, 9)
            nl = NL(f, -10, 10, lab_step=5)
            nl.pt(a, label=str(a), at=1)
            nl.pt(-a, label=N(-a), f_="teal", at=1)
            nl.jump(0, a, at=1, c="gold", up=False, label=str(a))
            nl.jump(0, -a, at=1, c="teal", up=False, label=str(a))
            q = f"절댓값이 {a}인 수를 모두 구하세요." if not _bti(a) else f"절댓값이 {a}인 수를 모두 구하세요."
            S.add(1, q, f"{a}, {N(-a)}", "0에서 거리가 같은 점은 양쪽에 하나씩",
                  [L(f"0에서 거리가 {a}인 점", memo="오른쪽 · 왼쪽"), L(f"{a}와 {N(-a)}" if not _bti(a) else f"{a}과 {N(-a)}")], f.out(), ap=f"{a}, -{a}", omr="ex", key=q)
    fill(S, 1, 20, g1)

    def addsub(st, op):
        def g():
            frac = S.count(st) >= 14
            if frac:
                d1, d2 = R.randint(2, 6), R.randint(2, 6)
                a, b = Fr(nz(R, 1, 7), d1), Fr(nz(R, 1, 7), d2)
                if a.denominator == 1 or b.denominator == 1:
                    return
            else:
                a, b = nz(R, 1, 12), nz(R, 1, 12)
            bb = b if op == "+" else -b
            v = a + bb
            if v == 0:
                return
            lines = []
            if op == "−":
                lines.append(L(f"{S_(a)} − {S_(b)} = {S_(a)} + {S_(bb)}", memo="빼기 → 부호 바꿔 더하기"))
            if (a > 0) == (bb > 0):
                lines.append(L(f"부호가 같아요 → {N(abs(a))} + {N(abs(bb))} = {N(abs(a) + abs(bb))}", memo=f"공통 부호 {'+' if a > 0 else '−'}"))
            else:
                big = a if abs(a) > abs(bb) else bb
                lines.append(L(f"부호가 달라요 → {N(max(abs(a), abs(bb)))} − {N(min(abs(a), abs(bb)))} = {N(abs(abs(a) - abs(bb)))}", memo=f"절댓값이 큰 쪽 {'+' if big > 0 else '−'}"))
            lines.append(L(f"{S_(a)} + {S_(bb)} = {N(v) if v < 0 else '+' + N(v)}"))
            f = None
            if not frac:
                f = Fig()
                lo, hi = min(0, a, v) - 2, max(0, a, v) + 2
                lo, hi = min(lo, -6), max(hi, 6)
                nl = NL(f, lo, hi, lab_step=5 if hi - lo > 16 else 1, z=24 if hi - lo > 16 else 22)
                nl.jump(0, a, at="q", c="gold", label=N(a))
                nl.jump(a, v, at=len(lines) - 1, c="teal", up=False, label=(("+" if bb > 0 else "") + N(bb)))
                nl.pt(v, label=N(v), f_="coral", at=len(lines) - 1, up=True, dl=700)
            q = f"{S_(a)} {op} {J(S_(b), '을', '를')} 계산하세요."
            S.add(st, q, N(v) if v < 0 else "+" + N(v), "수직선에서 오른쪽(+) · 왼쪽(−)으로 가요" if op == "+" else "빼는 수의 부호를 바꿔 더해요",
                  lines, f.out() if f else None, ap=plain(N(v)), key=q)
        return g
    fill(S, 2, 20, addsub(2, "+"))
    fill(S, 3, 20, addsub(3, "−"))

    def g4():
        k = S.count(4) % 4
        f = None
        if k == 0:
            xs = [nz(R, 1, 6) for _ in range(R.randint(2, 3))]
            v = 1
            for x in xs:
                v *= x
            neg = sum(1 for x in xs if x < 0)
            q = " × ".join(S_(x) for x in xs)
            lines = [L(f"음수가 {neg}개 → 부호 {'+' if neg % 2 == 0 else '−'}", memo="짝수 개 +, 홀수 개 −"),
                     L(" × ".join(str(abs(x)) for x in xs) + f" = {abs(v)}"), L(f"{q} = {N(v) if v < 0 else '+' + N(v)}")]
            if v < 0 and abs(v) <= 30:
                f = Fig()
                nl = NL(f, -32 if abs(v) > 10 else -12, 32 if abs(v) > 10 else 12, lab_step=10 if abs(v) > 10 else 5)
                nl.pt(abs(v), label=str(abs(v)), at=1)
                nl.jump(abs(v), v, at=2, c="red", h=150, label="180° 돌기")
                nl.pt(v, label=N(v), f_="coral", at=2, up=False, dl=700)
            ans, key = N(v) if v < 0 else "+" + N(v), q
        elif k == 1:
            a = R.randint(2, 5); n = R.randint(2, 4)
            if a ** n > 200:
                return
            if R.random() < 0.5:
                q = f"(−{a})^{{{n}}}"
                v = (-a) ** n
                lines = [L(" × ".join([f"(−{a})"] * n), memo=f"−{a}를 {n}번 곱해요" if not _bti(a) else f"−{a}을 {n}번 곱해요"), L(f"음수 {n}개 → 부호 {'+' if n % 2 == 0 else '−'}"), L(f"{q} = {N(v)}")]
            else:
                q = f"−{a}^{{{n}}}"
                v = -(a ** n)
                lines = [L(f"−{a}^{{{n}}} = −({' × '.join([str(a)] * n)})", memo=f"괄호가 없으면 {a}만 거듭제곱"), L(f"{a}^{{{n}}} = {a ** n}"), L(f"{q} = {N(v)}")]
            ans, key = N(v), q
        elif k == 2:
            b = nz(R, 2, 9); c = nz(R, 2, 9)
            a = b * c
            q = f"{S_(a)} ÷ {S_(b)}"
            v = c
            lines = [L(f"부호: {'같아요 → +' if (a > 0) == (b > 0) else '달라요 → −'}", memo="나눗셈도 곱셈과 같은 규칙"), L(f"{abs(a)} ÷ {abs(b)} = {abs(c)}"), L(f"{q} = {N(v) if v < 0 else '+' + N(v)}")]
            ans, key = N(v) if v < 0 else "+" + N(v), q
        else:
            d1, d2 = R.randint(2, 7), R.randint(2, 7)
            a, b = Fr(nz(R, 1, 6), d1), Fr(nz(R, 1, 6), d2)
            if a.denominator == 1 or b.denominator == 1:
                return
            v = a / b
            q = f"{S_(a)} ÷ {S_(b)}"
            inv = 1 / b
            lines = [L(f"÷ {S_(b)} = × {S_(inv)}", memo="역수를 곱해요"), L(f"{S_(a)} × {S_(inv)} = {N(v) if v < 0 else '+' + N(v)}")]
            ans, key = N(v) if v < 0 else "+" + N(v), q
        S.add(4, f"{J(q, '을', '를')} 계산하세요.", ans, "부호를 먼저 정하고 절댓값을 계산해요", lines, f.out() if f else None, ap=plain(ans.lstrip("+")), key=key)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        if k == 0:
            a, n = R.randint(2, 4), 2
            b = R.randint(2, 5); c = nz(R, 2, 6); d = R.choice([2, 3, 4])
            c = c * d
            p1 = -(a ** n)
            v = p1 * b - Fr(c, d)
            q = f"−{a}^{{2}} × {b} − {S_(c)} ÷ {d}"
            lines = [L(f"−{a}^{{2}} = {N(p1)}", memo="거듭제곱 먼저"), L(f"{N(p1)} × {b} = {N(p1 * b)}", memo="곱셈 · 나눗셈"),
                     L(f"{S_(c)} ÷ {d} = {N(Fr(c, d))}"), L(f"{N(p1 * b)} − {S_(Fr(c, d))} = {N(v)}", memo="덧셈 · 뺄셈은 마지막")]
        elif k == 1:
            a = nz(R, 2, 5); b = R.randint(2, 4); c = nz(R, 2, 9); d = nz(R, 2, 9)
            v = (a ** 2) * b + c * d
            q = f"{S_(a)}^{{2}} × {b} + {S_(c)} × {S_(d)}"
            lines = [L(f"{S_(a)}^{{2}} = {a * a}", memo="거듭제곱 먼저"), L(f"{a * a} × {b} = {a * a * b}"), L(f"{S_(c)} × {S_(d)} = {N(c * d)}"),
                     L(f"{a * a * b} + {S_(c * d)} = {N(v)}")]
        elif k == 2:
            a = nz(R, 2, 9); b = nz(R, 2, 9); c = nz(R, 2, 6)
            inner = a + b
            if inner == 0:
                return
            v = c * inner
            q = f"{S_(c)} × ({S_(a)} + {S_(b)})"
            lines = [L(f"{S_(a)} + {S_(b)} = {N(inner)}", memo="괄호 안 먼저"), L(f"{S_(c)} × {S_(inner)} = {N(v)}")]
        else:
            d = R.choice([2, 3, 4, 6]); a = Fr(nz(R, 1, 5), d); b = nz(R, 2, 6) * d; c = nz(R, 1, 9)
            if a.denominator == 1:
                return
            v = a * b - c
            q = f"{S_(a)} × {S_(b)} − {S_(c)}"
            lines = [L(f"{S_(a)} × {S_(b)} = {N(a * b)}", memo="곱셈 먼저"), L(f"{S_(a * b)} − {S_(c)} = {N(v)}")]
        S.add(5, f"{J(q, '을', '를')} 계산하세요.", N(v), "거듭제곱 → 괄호 → 곱셈 · 나눗셈 → 덧셈 · 뺄셈", lines, None, ap=plain(N(v)), key=q)
    fill(S, 5, 20, g5)
    return S

def _bt(v):
    s = N(v)
    m = __import__("re").search(r"\{(\d+)/\d+\}$", s)
    ch = (m.group(1) if m else s)[-1]
    return ch in "013678"

def _bti(n):
    return str(abs(n))[-1] in "013678"


# ══════════ ② 일차방정식 ══════════
def balance(f, left, right, at_cross=None, cross=0, xw="x"):
    """저울: left/right = (x 상자 수, 추 수). cross 만큼 양쪽 추에 × (at_cross 줄)"""
    cx, by = 330, 300
    f.line(cx, by + 30, cx, 560, c="soft", w=6)
    f.poly([(cx - 70, 600), (cx + 70, 600), (cx, 540)], c="soft", w=3, f="soft", fo=0.25)
    f.line(60, by, 600, by, c="ink", w=6)
    for side, (nx, nw) in ((-1, left), (1, right)):
        px = cx + side * 170
        f.line(px, by, px, by + 40, c="soft", w=2)
        f.poly([(px - 140, by + 40), (px + 140, by + 40), (px + 110, by + 70), (px - 110, by + 70)], c="ink", w=3, f="card", fo=1)
        items = [("x", i) for i in range(nx)] + [("w", i) for i in range(nw)]
        per = 6
        for j, (kind, i) in enumerate(items):
            col, row = j % per, j // per
            x = px - 125 + col * 44
            y = by + 10 - row * 44
            if kind == "x":
                f.rect(x, y - 30, 40, 40, c="ink", sw=2.5, f="gold", fo=0.6, rx=6)
                f.text(x + 20, y - 2, xw, z=28, b=700, ho=False)
            else:
                f.dot(x + 20, y - 10, r=17, f="teal")
                if at_cross is not None and i >= nw - cross:
                    f.cross(x + 20, y - 10, s=15, at=at_cross, dl=(nw - 1 - i) * 90)

def set_b():
    S = Set("b", "일차방정식 — 저울과 이항", "일차방정식",
            {1: "등식의 성질", 2: "이항 — ax + b = c", 3: "양변에 x가 있는 식", 4: "괄호 · 분수 · 소수", 5: "일차방정식의 활용"},
            pp=10,
            tips={1: "양변에 같은 수를 더하거나 빼거나 곱하거나 나누어도 등식은 그대로(저울이 수평)",
                  2: "한 변의 항을 부호를 바꿔 다른 변으로 옮기는 것이 이항",
                  3: "x가 있는 항은 왼쪽, 수는 오른쪽으로 이항해서 정리",
                  4: "괄호는 풀고, 분수는 분모의 최소공배수를, 소수는 10 · 100을 양변에 곱해요",
                  5: "구하는 것을 x로 놓고 → 식 세우기 → 풀기 → 확인"},
            note="방정식은 ‘저울이 수평을 유지하도록 양쪽에 같은 일을 하는 것’이에요. 이항은 그 결과를 빠르게 쓰는 방법이라는 것을 1단계 그림으로 보여 주세요.")
    R = rng(1102)

    def g1():
        k = S.count(1) % 4
        x = R.randint(1, 9)
        f = Fig()
        if k == 0:
            b = R.randint(1, 8)
            c = x + b
            if c > 12:
                return
            balance(f, (1, b), (0, c), at_cross=1, cross=b)
            q, lines, plan = f"x + {b} = {c}", [L(f"양변에서 {J(b, '을', '를')} 빼요", memo="저울은 그대로 수평"), L(f"x + {b} − {b} = {c} − {b}"), L(f"x = {x}")], f"양변에서 {J(b, '을', '를')} 빼요"
        elif k == 1:
            b = R.randint(1, 9)
            c = x - b
            if c == 0:
                return
            f = None
            q, lines, plan = f"x − {b} = {N(c)}", [L(f"양변에 {J(b, '을', '를')} 더해요"), L(f"x − {b} + {b} = {N(c)} + {b}"), L(f"x = {x}")], f"양변에 {J(b, '을', '를')} 더해요"
        elif k == 2:
            a = R.randint(2, 4)
            if a * x > 12:
                return
            balance(f, (a, 0), (0, a * x))
            q, lines, plan = f"{a}x = {a * x}", [L(f"양변을 {RO(a)} 나눠요", memo=f"x 한 개에 추 {x}개"), L(f"{{{a}x/{a}}} = {{{a * x}/{a}}}"), L(f"x = {x}")], f"양변을 {RO(a)} 나눠요"
        else:
            a = R.randint(2, 6); c = R.randint(1, 9)
            x = a * c
            f = None
            q, lines, plan = f"{{x/{a}}} = {c}", [L(f"양변에 {J(a, '을', '를')} 곱해요"), L(f"{{x/{a}}} × {a} = {c} × {a}"), L(f"x = {x}")], f"양변에 {J(a, '을', '를')} 곱해요"
        S.add(1, f"방정식 {J(q, '을', '를')} 푸세요.", f"x = {x}", plan, lines, f.out() if f else None, ap=str(x), sub={"x": x}, key=q)
    fill(S, 1, 20, g1)

    def g2():
        a = nz(R, 2, 9); x = nz(R, 1, 9); b = nz(R, 1, 15)
        c = a * x + b
        q = f"{lin(a, b)} = {N(c)}"
        lines = [L(f"{N(b)}{'을' if _bti(b) else '를'} 이항 → {N(-b)}" if b > 0 else f"{N(b)}{'을' if _bti(b) else '를'} 이항 → +{-b}", memo="부호가 바뀌어요"),
                 L(f"{mono(a, 'x', 1, first=True)} = {N(c)} {('−' if b > 0 else '+')} {abs(b)} = {N(c - b)}"), L(f"x = {N(c - b)} ÷ {NP(a)} = {N(x)}")]
        S.add(2, f"방정식 {J(q, '을', '를')} 푸세요.", f"x = {N(x)}", "상수항을 이항한 뒤 x의 계수로 나눠요", lines, None, ap=N(x).replace("−", "-"), sub={"x": x}, key=q)
    fill(S, 2, 20, g2)

    def g3():
        a, c = nz(R, 1, 9), nz(R, 1, 9)
        if a == c:
            return
        x = nz(R, 1, 9); b = nz(R, 1, 12)
        d = (a - c) * x + b
        if d == 0:
            return
        q = f"{lin(a, b)} = {lin(c, d)}"
        lines = [L("x는 왼쪽, 수는 오른쪽으로 이항", memo="부호를 바꿔 옮겨요"), L(f"{mono(a, 'x', 1, first=True)}{mono(-c, 'x')} = {N(d)}{mono(-b, '', 0)}"),
                 L(f"{mono(a - c, 'x', 1, first=True)} = {N(d - b)}"), L(f"x = {N(x)}")]
        S.add(3, f"방정식 {J(q, '을', '를')} 푸세요.", f"x = {N(x)}", "x항끼리, 수끼리 모아요", lines, None, ap=N(x).replace("−", "-"), sub={"x": x}, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        x = nz(R, 1, 9)
        if k == 0:
            a = R.randint(2, 5); p = nz(R, 1, 6); c = nz(R, 1, 4)
            if a == c:
                return
            d = a * (x + p) - c * x
            q = f"{a}({lin(1, p)}) = {lin(c, d)}"
            lines = [L(f"괄호 풀기: {lin(a, a * p)} = {lin(c, d)}", memo="분배법칙"), L(f"{mono(a, 'x', 1, True)}{mono(-c, 'x')} = {N(d)}{mono(-a * p, '', 0)}"),
                     L(f"{mono(a - c, 'x', 1, True)} = {N(d - a * p)}"), L(f"x = {N(x)}")]
            plan = "괄호를 먼저 풀어요"
        elif k == 1:
            p, r = R.choice([(2, 3), (3, 4), (2, 5), (4, 3), (3, 2), (6, 4)])
            m = p * r // gcd(p, r)
            b = nz(R, 1, 5)
            # x/p − (x − b)/r = c → c 정수가 되게
            val = Fr(x, p) - Fr(x - b, r)
            if val.denominator != 1:
                return
            c = val.numerator
            q = f"{{x/{p}}} − {{x {'−' if b > 0 else '+'} {abs(b)}/{r}}} = {N(c)}"
            lines = [L(f"양변 × {m}", memo=f"분모 {p}, {r}의 최소공배수"), L(f"{m // p}x − {m // r}(x {'−' if b > 0 else '+'} {abs(b)}) = {N(c * m)}"),
                     L(f"{lin(m // p - m // r, m // r * b)} = {N(c * m)}"), L(f"x = {N(x)}")]
            plan = "분모의 최소공배수를 양변에 곱해요"
        else:
            a, c = R.randint(1, 9), R.randint(1, 9)
            if a == c:
                return
            b = R.randint(1, 30) * (1 if R.random() < 0.5 else -1)
            d = (a - c) * x * 1 + b
            # 0.a x + 0.b = 0.c x + 0.d  (계수 /10)
            A, B, C, D = Fr(a, 10), Fr(b, 10), Fr(c, 10), Fr(d, 10)
            if abs(b) >= 10 and b % 10 == 0 or abs(d) > 99:
                return
            q = f"{DEC(A)}x {'+' if B > 0 else '−'} {DEC(abs(B))} = {DEC(C)}x {'+' if D > 0 else '−'} {DEC(abs(D))}" if D != 0 else None
            if not q:
                return
            lines = [L("양변 × 10", memo="소수를 자연수로"), L(f"{lin(a, b)} = {lin(c, d)}"), L(f"{mono(a - c, 'x', 1, True)} = {N(d - b)}"), L(f"x = {N(x)}")]
            plan = "양변에 10을 곱해 계수를 자연수로"
        S.add(4, f"방정식 {J(q, '을', '를')} 푸세요.", f"x = {N(x)}", plan, lines, None, ap=N(x).replace("−", "-"), sub={"x": x}, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        if k == 0:
            m = R.randint(6, 40)
            s = 3 * m
            q = f"연속하는 세 자연수의 합이 {s}일 때, 세 수를 구하세요."
            lines = [L("가운데 수를 x", memo="세 수 x − 1, x, x + 1"), L(f"(x − 1) + x + (x + 1) = {s}"), L(f"3x = {s} → x = {m}"), L(f"세 수: {m - 1}, {m}, {m + 1}")]
            S.add(5, q, f"{m - 1}, {m}, {m + 1}", "가운데 수를 x로 놓으면 식이 간단해요", lines, None, ap=f"{m - 1}, {m}, {m + 1}", omr="ex", sub={"x": m}, key=q)
        elif k == 1:
            son = R.randint(6, 15); k2 = R.choice([2, 3]); x = R.randint(2, 20)
            dad = k2 * (son + x) - x
            if dad - son < 20 or dad > 60:
                return
            q = f"현재 아버지는 {dad}살, 아들은 {son}살이에요. 아버지의 나이가 아들의 나이의 {k2}배가 되는 것은 몇 년 후인가요?"
            lines = [L("x년 후", memo=f"아버지 {dad} + x · 아들 {son} + x"), L(f"{dad} + x = {k2}({son} + x)"), L(f"{dad} + x = {k2 * son} + {k2}x"),
                     L(f"{dad - k2 * son} = {k2 - 1}x" if k2 > 2 else f"{dad - k2 * son} = x"), L(f"x = {x}")]
            S.add(5, q, f"{x}년 후", "x년 뒤의 두 사람 나이를 식으로", lines, None, ap=str(x), sub={"x": x}, key=q)
        elif k == 2:
            p1, p2 = R.choice([(500, 800), (300, 700), (600, 900), (400, 1000), (700, 1200)])
            n = R.randint(8, 20); x = R.randint(1, n - 1)
            T = p1 * x + p2 * (n - x)
            q = f"한 개에 {com(p1)}원인 사탕과 {com(p2)}원인 초콜릿을 합하여 {n}개 사고 {com(T)}원을 냈어요. 사탕은 몇 개 샀나요?"
            lines = [L("사탕 x개", memo=f"초콜릿 {n} − x개"), L(f"{p1}x + {p2}({n} − x) = {T}"), L(f"{p1}x + {p2 * n} − {p2}x = {T}"),
                     L(f"−{p2 - p1}x = {N(T - p2 * n)}"), L(f"x = {x}")]
            S.add(5, q, f"{x}개", "개수를 x로 놓고 금액으로 식을 세워요", lines, None, ap=str(x), sub={"x": x}, key=q)
        else:
            a, b = R.choice([(2, 3), (3, 4), (4, 6), (3, 6), (4, 5), (2, 4)])
            m = a * b // gcd(a, b)
            x = m * R.randint(1, 3)
            t = Fr(x, a) + Fr(x, b)
            if t.denominator != 1:
                return
            t = t.numerator
            q = f"집에서 도서관까지 갈 때는 시속 {a} km로, 올 때는 같은 길을 시속 {b} km로 걸었더니 모두 {t}시간이 걸렸어요. 집에서 도서관까지의 거리는 몇 km인가요?"
            lines = [L("거리 x km", memo="시간 = 거리 ÷ 속력"), L(f"{{x/{a}}} + {{x/{b}}} = {t}"), L(f"양변 × {m}: {m // a}x + {m // b}x = {t * m}"), L(f"{m // a + m // b}x = {t * m} → x = {x}")]
            S.add(5, q, f"{x} km", "시간 = 거리 ÷ 속력으로 식을 세워요", lines, None, ap=str(x), sub={"x": x}, key=q)
    fill(S, 5, 20, g5)
    return S

GRADE = {"key": "m1", "grade": "중1", "level": "중등", "icon": "🌡️", "title": "중1 · 정수와 유리수 · 일차방정식",
         "desc": "정수와 유리수의 계산 100제(수직선 위 이동 · 180° 돌기) · 일차방정식 — 저울과 이항 100제.",
         "thumb": ("a", 30), "sets": [set_a, set_b]}
