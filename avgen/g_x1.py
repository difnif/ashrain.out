# 초1 채우기 — 9까지의 수 · 50까지의 수 · 덧셈과 뺄셈(모으기 · 가르기) · 비교하기 · 여러 가지 모양 · 규칙 찾기
from fractions import Fraction as Fr
from core import *
from fig import Fig, rod
from kit import *

ICONS = {"○": "동그라미", "△": "세모", "□": "네모", "●": "까만 동그라미"}
KO = ["영", "하나", "둘", "셋", "넷", "다섯", "여섯", "일곱", "여덟", "아홉"]
ORD = ["", "첫째", "둘째", "셋째", "넷째", "다섯째", "여섯째", "일곱째", "여덟째", "아홉째"]

def ic(ch, n=1):
    return "".join(f"⟪{ch}⟫" for _ in range(n))

def dots(f, n, kind="●", at="q", y=300, lab_at=None, m=None):
    """n 개를 5개씩 두 줄(10칸 틀)로 — m 개(앞에서부터)는 다른 모양"""
    cw = 96
    x0 = 330 - cw * 2.5
    f.grid(x0, y - cw, cw, cw, 5, 2, c="soft", sw=2, at=at)
    for i in range(n):
        cx, cy = x0 + cw * (i % 5) + cw / 2, y - cw + cw * (i // 5) + cw / 2
        k = kind if (m is None or i < m) else "○"
        if k in ("●", "○"):
            f.circ(cx, cy, 30, c="ink", sw=3, f="sky" if k == "●" else None, fo=0.8 if k == "●" else None, at=at)
        elif k == "△":
            f.poly([(cx, cy - 32), (cx - 32, cy + 26), (cx + 32, cy + 26)], c="ink", w=3, f="gold", fo=0.5, at=at)
        else:
            f.rect(cx - 28, cy - 28, 56, 56, c="ink", sw=3, f="teal", fo=0.4, at=at)
        if lab_at is not None:
            f.text(cx, cy + 58, str(i + 1), z=22, c="coral", at=lab_at, dl=i * 90, b=700)


# ══════════ 9까지의 수 ══════════
def num9():
    S = Set("num9", "9까지의 수 — 세기 · 순서 · 크기", "9까지의 수",
            {1: "수 세기", 2: "수의 순서", 3: "1 큰 수 · 1 작은 수", 4: "크기 비교", 5: "몇째"},
            pp=10,
            tips={1: "하나씩 짚으며 하나, 둘, 셋 … 마지막에 센 수가 모두의 개수",
                  2: "1, 2, 3, … 9 — 바로 앞의 수는 1 작고, 바로 뒤의 수는 1 커요",
                  3: "1 큰 수는 바로 뒤의 수, 1 작은 수는 바로 앞의 수",
                  4: "수를 차례로 셀 때 뒤에 나오는 수가 더 커요",
                  5: "앞에서부터 첫째, 둘째, 셋째 … — 몇째는 순서, 몇은 개수"},
            note="1학년 첫 단원이에요. 물건을 하나씩 짚으며 세는 것과, 마지막에 센 수가 전체 개수라는 것을 꼭 같이 말하게 해 주세요.")
    R = rng(5101)

    def g1():
        n = R.randint(1, 9)
        k = R.choice(list(ICONS))
        tail = R.choice(["모두 몇 개인가요?", "몇 개 있나요?"])
        q = f"{ic(k, n)} — {tail}"
        f = Fig()
        dots(f, n, k, lab_at=0)
        lines = [L(" , ".join(KO[1:n + 1]).replace(" ,", ","), memo="하나씩 짚으며 세어요"), L(f"모두 {n}개", memo=f"마지막에 센 수 {KO[n]}")]
        S.add(1, q, str(n), "하나씩 세고 마지막 수가 개수", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        t = S.count(2) % 3
        if t == 0:
            n = R.randint(0, 8)
            q, a = f"{n} 바로 뒤의 수는 무엇인가요?", n + 1
            lines = [L(f"{n} 다음에 세는 수 → {a}", memo="1 커요")]
        elif t == 1:
            n = R.randint(1, 9)
            q, a = f"{n} 바로 앞의 수는 무엇인가요?", n - 1
            lines = [L(f"{n} 바로 전에 세는 수 → {a}", memo="1 작아요")]
        else:
            n = R.randint(0, 7)
            q, a = f"{wa(n)} {n + 2} 사이에 있는 수는 무엇인가요?", n + 1
            lines = [L(f"{n}, □, {n + 2} → □ = {a}", memo="차례로 세어 보기")]
        f = Fig()
        xs = jump_line(f, list(range(0, 10)), at="q", y=380)
        f.dot(xs[a], 380, r=14, f="coral", at=0)
        S.add(2, q, str(a), "수를 차례로 세어 보기", lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        big = S.count(3) % 2 == 0
        n = R.randint(0, 8) if big else R.randint(1, 9)
        a = n + 1 if big else n - 1
        word = R.choice(["1 큰 수", "1만큼 더 큰 수"]) if big else R.choice(["1 작은 수", "1만큼 더 작은 수"])
        q = f"{n}보다 {word}는 무엇인가요?"
        lines = [L(f"{n}보다 {'1 큰 수는 바로 뒤의 수' if big else '1 작은 수는 바로 앞의 수'}"), L(f"{a}")]
        f = Fig()
        dots(f, max(n, a), m=min(n, a) if big else None, kind="●")
        S.add(3, q, str(a), "1 큰 수 = 바로 뒤 · 1 작은 수 = 바로 앞", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        t = S.count(4) % 2
        if t == 0:
            a, b = R.sample(range(0, 10), 2)
            big = R.random() < 0.5
            q = f"{wa(a)} {b} 중에서 더 {'큰' if big else '작은'} 수는 무엇인가요?"
            ans = max(a, b) if big else min(a, b)
            lines = [L(f"차례로 세면 {min(a, b)} 다음에 {max(a, b)}", memo="뒤에 세는 수가 커요"), L(f"{'큰' if big else '작은'} 수 {ans}")]
        else:
            a, b, c = R.sample(range(0, 10), 3)
            big = R.random() < 0.5
            q = f"{a}, {b}, {c} 중에서 가장 {'큰' if big else '작은'} 수는 무엇인가요?"
            ans = max(a, b, c) if big else min(a, b, c)
            lines = [L(f"작은 수부터 {', '.join(map(str, sorted([a, b, c])))}"), L(f"가장 {'큰' if big else '작은'} 수 {ans}")]
        S.add(4, q, str(ans), "차례로 셀 때 뒤에 나오는 수가 더 커요", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        n = R.randint(4, 7)
        row = [R.choice(list(ICONS)) for _ in range(n)]
        if len(set(row)) < 3:
            return
        t = S.count(5) % 2
        if t == 0:
            i = R.randint(1, n)
            q = f"{ic(row[0])}{''.join(ic(x) for x in row[1:])}에서 앞(왼쪽)에서부터 {ORD[i]}에 있는 모양은 무엇인가요?"
            ans = ICONS[row[i - 1]]
            lines = [L(f"왼쪽부터 첫째, 둘째, … {ORD[i]}"), L(f"{ORD[i]} → {ans}")]
            S.add(5, q, ans, "앞에서부터 첫째, 둘째, 셋째 …", lines, None, omr="ex", key=q)
        else:
            uniq = [k for k in ICONS if row.count(k) == 1]
            if not uniq:
                return
            k = uniq[0]
            i = row.index(k) + 1
            q = f"{''.join(ic(x) for x in row)}에서 {ICONS[k]}({ic(k)})는 앞(왼쪽)에서부터 몇째에 있나요?"
            lines = [L(f"왼쪽부터 하나씩 → {ORD[i]}")]
            S.add(5, q, ORD[i], "몇째는 순서 — 왼쪽부터 세어요", lines, None, ap=str(i), omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 50까지의 수 ══════════
def num50():
    S = Set("num50", "50까지의 수 — 10개씩 묶음과 낱개", "50까지의 수",
            {1: "10개씩 묶음과 낱개 → 수", 2: "수 → 10개씩 묶음과 낱개", 3: "수의 순서", 4: "크기 비교", 5: "짝수와 홀수"},
            pp=10,
            tips={1: "10개씩 묶음 3개와 낱개 4개 → 34",
                  2: "34 → 10개씩 묶음 3개, 낱개 4개 — 앞 숫자가 묶음, 뒤 숫자가 낱개",
                  3: "바로 뒤의 수는 1 큰 수, 바로 앞의 수는 1 작은 수",
                  4: "10개씩 묶음의 수부터 — 같으면 낱개의 수로",
                  5: "둘씩 짝을 지어 남는 것이 없으면 짝수, 하나가 남으면 홀수"},
            note="10개씩 묶음이 ‘십의 자리’의 뜻이에요. 모형이나 그림으로 묶음과 낱개를 먼저 보고 수로 쓰게 해 주세요.")
    R = rng(5102)

    def bundles(f, t, o, at="q"):
        x = 60
        for i in range(t):
            rod(f, x + i * 40, 160, h=230, at=at)
        for j in range(o):
            f.circ(x + t * 40 + 40 + (j % 5) * 44, 220 + (j // 5) * 50, 16, c="ink", sw=3, f="gold", fo=0.5, at=at)

    def g1():
        t, o = R.randint(1, 4), R.randint(0, 9)
        n = 10 * t + o
        q = f"10개씩 묶음 {t}개와 낱개 {o}개는 얼마인가요?"
        f = Fig()
        bundles(f, t, o)
        lines = [L(f"10개씩 묶음 {t}개 → {10 * t}"), L(f"{10 * t} + {o} = {n}", memo="낱개를 더해요")]
        S.add(1, q, str(n), "묶음은 앞 숫자, 낱개는 뒤 숫자", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        n = R.randint(10, 50)
        t, o = divmod(n, 10)
        q = f"{eun(n)} 10개씩 묶음 몇 개와 낱개 몇 개인가요?"
        f = Fig()
        bundles(f, t, o, at=0)
        lines = [L(f"{n} = {10 * t} + {o}"), L(f"10개씩 묶음 {t}개, 낱개 {o}개")]
        S.add(2, q, f"묶음 {t}개, 낱개 {o}개", "앞 숫자는 10개씩 묶음, 뒤 숫자는 낱개", lines, f.out(), ap=f"{t}, {o}", omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        t = S.count(3) % 3
        if t == 0:
            n = R.randint(10, 49)
            q, a = f"{n} 바로 뒤의 수는 무엇인가요?", n + 1
        elif t == 1:
            n = R.randint(11, 50)
            q, a = f"{n} 바로 앞의 수는 무엇인가요?", n - 1
        else:
            n = R.randint(10, 48)
            q, a = f"{wa(n)} {n + 2} 사이에 있는 수는 무엇인가요?", n + 1
        lines = [L(f"{a - 1}, {a}, {a + 1} — 차례로 세면", memo="1씩 커져요"), L(str(a))]
        f = Fig()
        xs = jump_line(f, list(range(a - 3, a + 4)), at="q", y=380)
        f.dot(xs[3], 380, r=14, f="coral", at=1)
        S.add(3, q, str(a), "차례로 세어 보기", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.sample(range(10, 51), 2)
        big = R.random() < 0.5
        q = f"{wa(a)} {b} 중에서 더 {'큰' if big else '작은'} 수는 무엇인가요?"
        ans = max(a, b) if big else min(a, b)
        if a // 10 != b // 10:
            lines = [L(f"10개씩 묶음 {a // 10}개와 {b // 10}개", memo="묶음의 수부터"), L(f"{'큰' if big else '작은'} 수 {ans}")]
        else:
            lines = [L(f"묶음이 {a // 10}개로 같아요 → 낱개 {a % 10}개와 {b % 10}개", memo="낱개의 수로"), L(f"{'큰' if big else '작은'} 수 {ans}")]
        S.add(4, q, str(ans), "10개씩 묶음의 수 → 낱개의 수", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        t = S.count(5) % 2
        if t == 0:
            n = R.randint(1, 50)
            ev = n % 2 == 0
            q = f"{eun(n)} 짝수인가요, 홀수인가요?"
            lines = [L(f"낱개의 수 {n % 10} → 둘씩 짝을 지으면 {'남는 것이 없어요' if ev else '하나가 남아요'}"), L("짝수" if ev else "홀수")]
            S.add(5, q, "짝수" if ev else "홀수", "끝자리가 0, 2, 4, 6, 8이면 짝수", lines, None, omr="ex", key=q)
        else:
            a = R.randint(1, 30)
            b = a + R.randint(5, 15)
            if b > 50:
                return
            ev = R.random() < 0.5
            cnt = sum(1 for k in range(a, b + 1) if (k % 2 == 0) == ev)
            q = f"{a}부터 {b}까지의 수 중에서 {'짝수' if ev else '홀수'}는 모두 몇 개인가요?"
            first = a if (a % 2 == 0) == ev else a + 1
            lines = [L(f"{first}, {first + 2}, {first + 4}, … 2씩 뛰어 세기"), L(f"모두 {cnt}개")]
            S.add(5, q, str(cnt), "짝수 · 홀수는 2씩 뛰어 세기", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 덧셈과 뺄셈(모으기 · 가르기) ══════════
def add9():
    S = Set("add9", "덧셈과 뺄셈 — 모으기와 가르기", "모으기·가르기",
            {1: "모으기", 2: "가르기", 3: "한 자리 덧셈", 4: "한 자리 뺄셈", 5: "0이 있는 계산 · 이야기"},
            pp=10,
            tips={1: "두 수를 모으면 한 수 — 3과 4를 모으면 7",
                  2: "한 수를 두 수로 — 7은 3과 4로 가를 수 있어요",
                  3: "모으기가 덧셈 — 3 + 4 = 7",
                  4: "가르기가 뺄셈 — 7 − 3 = 4",
                  5: "0을 더하거나 빼도 그대로, 같은 수를 빼면 0"},
            note="덧셈 · 뺄셈 기호를 쓰기 전에 모으기 · 가르기를 손가락이나 구슬로 충분히 해 보게 해 주세요.")
    R = rng(5103)

    def g1():
        a, b = R.randint(1, 8), R.randint(1, 8)
        if a + b > 9:
            return
        q = f"{wa(a)} {eul(b)} 모으면 얼마인가요?"
        f = Fig()
        dots(f, a + b, "●", m=a, lab_at=0)
        lines = [L(f"{a}개와 {b}개를 모아서 세면", memo="모으기"), L(f"{a} + {b} = {a + b}")]
        S.add(1, q, str(a + b), "모아서 처음부터 세어요", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        n = R.randint(2, 9)
        a = R.randint(1, n - 1)
        q = f"{eun(n)} {wa(a)} 몇으로 가를 수 있나요?"
        f = Fig()
        dots(f, n, "●", m=a)
        lines = [L(f"{n}개에서 {a}개를 떼어 놓으면", memo="가르기"), L(f"{n} − {a} = {n - a}")]
        S.add(2, q, str(n - a), "가르기는 남은 것 세기", lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        a, b = R.randint(1, 8), R.randint(1, 8)
        if a + b > 9:
            return
        q = f"{a} + {b}의 값은 얼마인가요?" if R.random() < 0.5 else f"{a} + {b} = □에서 □에 알맞은 수는 무엇인가요?"
        lines = [L(f"{a}에서 {b}만큼 이어 세기", memo=" → ".join(str(a + i) for i in range(1, b + 1))), L(f"{a} + {b} = {a + b}")]
        S.add(3, q, str(a + b), "큰 수에서 작은 수만큼 이어 세기", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        n = R.randint(2, 9)
        a = R.randint(1, n - 1)
        q = f"{n} − {a}의 값은 얼마인가요?" if R.random() < 0.5 else f"{n} − {a} = □에서 □에 알맞은 수는 무엇인가요?"
        lines = [L(f"{n}에서 {a}만큼 거꾸로 세기", memo=" → ".join(str(n - i) for i in range(1, a + 1))), L(f"{n} − {a} = {n - a}")]
        S.add(4, q, str(n - a), "빼는 수만큼 거꾸로 세기", lines, None, key=q)
    fill(S, 4, 20, g4)

    THINGS = [("사탕", "개"), ("연필", "자루"), ("구슬", "개"), ("딱지", "장"), ("공", "개"), ("풍선", "개"), ("붕어빵", "개"), ("색종이", "장")]
    def g5():
        t = S.count(5) % 3
        if t == 0:
            a = R.randint(0, 9)
            op = R.choice(["+ 0", "− 0", f"− {a}", "0 +"])
            if op == "0 +":
                q, v = f"0 + {a}의 값은 얼마인가요?", a
            elif op == "+ 0":
                q, v = f"{a} + 0의 값은 얼마인가요?", a
            elif op == "− 0":
                q, v = f"{a} − 0의 값은 얼마인가요?", a
            else:
                q, v = f"{a} − {a}의 값은 얼마인가요?", 0
            lines = [L(q.replace("의 값은 얼마인가요?", "") + f" = {v}", memo="0을 더하거나 빼면 그대로 · 같은 수를 빼면 0")]
            S.add(5, q, str(v), "0의 덧셈 · 뺄셈", lines, None, key=q)
        else:
            th, u = R.choice(THINGS)
            if t == 1:
                a, b = R.randint(1, 6), R.randint(1, 5)
                if a + b > 9:
                    return
                q = f"{th} {a}{u}에 {b}{u}를 더 받았어요. {th}는 모두 몇 {u}인가요?".replace(f"{b}{u}를", f"{b}{u}{'을' if u in ('장',) else '를'}")
                lines = [L(f"모두 → 더하기"), L(f"{a} + {b} = {a + b}")]
                S.add(5, q, f"{a + b}{u}", "‘모두’는 덧셈", lines, None, ap=str(a + b), key=q)
            else:
                a = R.randint(3, 9)
                b = R.randint(1, a - 1)
                q = f"{th} {a}{u} 중에서 {b}{u}를 친구에게 주었어요. 남은 {th}는 몇 {u}인가요?".replace(f"{b}{u}를", f"{b}{u}{'을' if u in ('장',) else '를'}")
                lines = [L(f"남은 것 → 빼기"), L(f"{a} − {b} = {a - b}")]
                S.add(5, q, f"{a - b}{u}", "‘남은’은 뺄셈", lines, None, ap=str(a - b), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 비교하기 ══════════
LONG = ["연필", "붓", "크레파스", "막대", "줄넘기", "리본", "끈", "빨대", "자", "젓가락"]
BOX = ["상자", "가방", "주머니", "바구니", "봉지"]
def comp():
    S = Set("comp", "비교하기 — 길이 · 무게 · 넓이 · 담을 수 있는 양", "비교하기",
            {1: "더 긴 것 · 더 짧은 것", 2: "가장 긴 것 · 가장 짧은 것", 3: "더 무거운 것", 4: "더 넓은 것", 5: "더 많이 담을 수 있는 것"},
            pp=8,
            tips={1: "한쪽 끝을 맞추고 다른 쪽 끝을 견주어요",
                  2: "셋을 한쪽 끝에 맞추면 가장 많이 나온 것이 가장 길어요",
                  3: "같은 구슬이면 개수가 많은 쪽이 무거워요 — 시소는 무거운 쪽이 내려가요",
                  4: "같은 크기 칸으로 나누어 칸 수를 세면 넓이를 견줄 수 있어요",
                  5: "같은 컵으로 몇 번 부었는지 — 많이 부은 그릇이 더 많이 담아요"},
            note="‘더 길다 · 더 짧다’처럼 비교하는 말을 짝으로 쓰게 해 주세요. 끝을 맞추는 것이 길이 비교의 시작이에요.")
    R = rng(5104)

    def bars(f, names, lens, at="q"):
        y0 = 200
        for i, (nm, ln) in enumerate(zip(names, lens)):
            y = y0 + i * 120
            f.text(110, y + 12, nm, z=28, b=700, at=at, a="e")
            f.rect(130, y - 22, ln * 46, 44, c="ink", sw=3, f=["sky", "gold", "teal"][i], fo=0.45, rx=8, at=at)
        f.line(130, y0 - 60, 130, y0 + 120 * len(names) - 50, c="coral", w=3, d=True, at=at)

    def g1():
        a, b = R.sample(LONG, 2)
        la, lb = R.sample(range(4, 11), 2)
        big = R.random() < 0.5
        q = f"그림에서 {wa(a)} {b} 중에서 더 {'긴' if big else '짧은'} 것은 무엇인가요?"
        f = Fig()
        bars(f, [a, b], [la, lb])
        ans = (a if la > lb else b) if big else (a if la < lb else b)
        lines = [L("왼쪽 끝이 맞추어져 있어요", memo="한쪽 끝 맞추기"), L(f"오른쪽 끝이 더 {'많이' if big else '적게'} 나온 것 → {ans}")]
        S.add(1, q, ans, "한쪽 끝을 맞추고 다른 쪽 끝 견주기", lines, f.out(), omr="ex", qfig=True, key=q)
    fill(S, 1, 20, g1)

    def g2():
        ns = R.sample(LONG, 3)
        ls = R.sample(range(3, 12), 3)
        big = R.random() < 0.5
        q = f"그림에서 {ns[0]}, {ns[1]}, {ns[2]} 중에서 가장 {'긴' if big else '짧은'} 것은 무엇인가요?"
        f = Fig()
        bars(f, ns, ls)
        i = ls.index(max(ls) if big else min(ls))
        lines = [L("셋 모두 왼쪽 끝이 맞추어져 있어요"), L(f"가장 {'많이' if big else '적게'} 나온 것 → {ns[i]}")]
        S.add(2, q, ns[i], "끝을 맞추고 셋을 한꺼번에", lines, f.out(), omr="ex", qfig=True, key=q)
    fill(S, 2, 20, g2)

    def g3():
        bx = R.choice(BOX)
        a, b = R.sample(range(2, 15), 2)
        heavy = R.random() < 0.5
        q = f"똑같은 구슬이 가 {bx}에는 {a}개, 나 {bx}에는 {b}개 들어 있어요. 더 {'무거운' if heavy else '가벼운'} {bx}는 어느 것인가요? ({bx}의 무게는 같아요)"
        ans = ("가" if a > b else "나") if heavy else ("가" if a < b else "나")
        f = Fig()
        tilt = 30 if a > b else -30
        f.line(330, 470, 330, 520, c="ink", w=6)
        f.poly([(300, 540), (360, 540), (330, 500)], c="ink", w=3, f="soft", fo=0.4)
        f.line(130, 470 + tilt, 530, 470 - tilt, c="ink", w=8)
        f.rect(140, 470 + tilt - 110, 120, 100, c="ink", sw=3, f="sky", fo=0.3, rx=10)
        f.rect(400, 470 - tilt - 110, 120, 100, c="ink", sw=3, f="gold", fo=0.3, rx=10)
        f.text(200, 470 + tilt - 50, f"가 {a}개", z=26, b=700)
        f.text(460, 470 - tilt - 50, f"나 {b}개", z=26, b=700)
        lines = [L(f"구슬이 {max(a, b)}개인 쪽이 더 무거워요", memo="시소는 무거운 쪽이 내려가요"), L(f"더 {'무거운' if heavy else '가벼운'} {bx} → {ans}")]
        S.add(3, q, ans, "같은 것이 많을수록 무거워요", lines, f.out(), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.sample(range(4, 16), 2)
        wide = R.random() < 0.5
        q = f"똑같은 크기의 작은 칸으로 가는 {a}칸, 나는 {b}칸이에요. 더 {'넓은' if wide else '좁은'} 것은 어느 것인가요?"
        ans = ("가" if a > b else "나") if wide else ("가" if a < b else "나")
        f = Fig()
        for x0, n, nm, col in ((70, a, "가", "sky"), (370, b, "나", "gold")):
            for i in range(n):
                f.rect(x0 + (i % 4) * 56, 200 + (i // 4) * 56, 56, 56, c="ink", sw=2, f=col, fo=0.35, at=0)
            f.text(x0 + 112, 180, nm, z=30, b=700)
        lines = [L(f"칸 수 {a}칸과 {b}칸", memo="같은 크기 칸 세기"), L(f"칸이 {'많은' if wide else '적은'} 쪽 → {ans}")]
        S.add(4, q, ans, "같은 크기 칸으로 세어 견주기", lines, f.out(), omr="ex", key=q)
    fill(S, 4, 20, g4)

    CUP = ["그릇", "물통", "냄비", "주전자", "병"]
    def g5():
        c = R.choice(CUP)
        a, b = R.sample(range(2, 12), 2)
        more = R.random() < 0.5
        q = f"같은 컵으로 물을 가 {c}에 {a}컵, 나 {c}에 {b}컵 부었더니 가득 찼어요. {'더 많이' if more else '더 적게'} 담을 수 있는 {eun(c)} 어느 것인가요?"
        ans = ("가" if a > b else "나") if more else ("가" if a < b else "나")
        lines = [L(f"부은 컵 수 {a}컵과 {b}컵"), L(f"컵 수가 {'많은' if more else '적은'} 쪽 → {ans}")]
        S.add(5, q, ans, "같은 컵으로 부은 횟수로 견주기", lines, None, omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 여러 가지 모양 ══════════
SHAPES3 = {"상자 모양": ["필통", "과자 상자", "주사위", "냉장고", "책", "지우개", "벽돌", "휴지 상자", "우유갑"],
           "둥근기둥 모양": ["음료수 캔", "풀", "북", "두루마리 휴지", "통조림", "연필꽂이", "케이크", "물통"],
           "공 모양": ["축구공", "구슬", "수박", "지구본", "오렌지", "테니스공", "농구공", "방울"]}
OBJ = {o: k for k, v in SHAPES3.items() for o in v}
PLANE = {"□": ("네모", 4), "△": ("세모", 3), "○": ("동그라미", 0)}
def shape1():
    S = Set("shape1", "여러 가지 모양 — 상자 · 둥근기둥 · 공, 네모 · 세모 · 동그라미", "여러 가지 모양",
            {1: "어떤 모양일까?", 2: "같은 모양 세기", 3: "평면 모양 세기", 4: "뾰족한 곳 세기", 5: "가장 많이 쓴 모양"},
            pp=10,
            tips={1: "평평한 면만 있으면 상자, 둥근 면과 평평한 면이 있으면 둥근기둥, 둥근 면만 있으면 공 모양",
                  2: "하나씩 모양을 정하고 같은 모양끼리 세어요",
                  3: "네모(□) · 세모(△) · 동그라미(○)를 하나씩 지우며 세어요",
                  4: "세모는 뾰족한 곳 3개, 네모는 4개, 동그라미는 0개",
                  5: "모양마다 세어서 가장 큰 수"},
            note="모양의 이름보다 ‘굴러간다 · 쌓을 수 있다 · 뾰족하다’ 같은 특징을 먼저 말하게 해 주세요.")
    R = rng(5105)

    def g1():
        o = R.choice(list(OBJ))
        tail = R.choice(["어떤 모양인가요?", "상자 · 둥근기둥 · 공 모양 중 어떤 모양인가요?"])
        q = f"{eun(o)} {tail}"
        k = OBJ[o]
        why = {"상자 모양": "평평한 면만 있고 뾰족한 곳이 있어요", "둥근기둥 모양": "둥근 면과 평평한 면이 있어요", "공 모양": "어느 쪽으로나 둥글어요"}[k]
        lines = [L(why), L(k)]
        S.add(1, q, k, "면이 평평한지 둥근지", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        objs = R.sample(list(OBJ), 5)
        k = R.choice(list(SHAPES3))
        cnt = sum(1 for o in objs if OBJ[o] == k)
        if cnt == 0:
            return
        q = f"{', '.join(objs)} 중에서 {eun(k)} 몇 개인가요?"
        lines = [L(" · ".join(f"{o}({OBJ[o].split()[0]})" for o in objs)), L(f"{k} {cnt}개")]
        S.add(2, q, str(cnt), "하나씩 모양을 정하고 세기", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        row = [R.choice(list(PLANE)) for _ in range(R.randint(6, 9))]
        k = R.choice(list(PLANE))
        cnt = row.count(k)
        if cnt == 0:
            return
        q = f"{''.join(ic(x) for x in row)} 중에서 {PLANE[k][0]} 모양({ic(k)})은 몇 개인가요?"
        lines = [L(f"{PLANE[k][0]}만 골라 세기", memo="센 것은 표시"), L(f"{cnt}개")]
        S.add(3, q, str(cnt), "하나씩 표시하며 세기", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b, c = R.randint(0, 4), R.randint(0, 4), R.randint(0, 3)
        if a + b == 0:
            return
        parts = [x for x in ((a, "세모", 3), (b, "네모", 4), (c, "동그라미", 0)) if x[0]]
        q = "그림이 " + ", ".join(f"{nm} {n}개" for n, nm, _ in parts) + "로 되어 있어요. 뾰족한 곳은 모두 몇 개인가요?"
        tot = 3 * a + 4 * b
        expr = " + ".join(f"{k} × {n}" for n, nm, k in parts if k)
        lines = [L("세모 3개 · 네모 4개 · 동그라미 0개", memo="뾰족한 곳"), L(f"{expr} = {tot}" if "+" in expr or "×" in expr else str(tot))]
        S.add(4, q, str(tot), "모양마다 뾰족한 곳의 수", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        ns = R.sample(range(1, 8), 3)
        q = f"네모 {ns[0]}개, 세모 {ns[1]}개, 동그라미 {ns[2]}개로 꾸민 그림에서 가장 많이 쓴 모양은 무엇인가요?"
        nm = ["네모", "세모", "동그라미"][ns.index(max(ns))]
        lines = [L(f"{ns[0]}, {ns[1]}, {ns[2]} 중 가장 큰 수 {max(ns)}"), L(nm)]
        S.add(5, q, nm, "모양마다 센 수를 견주기", lines, None, omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 규칙 찾기(1학년) ══════════
def rule1():
    S = Set("rule1", "규칙 찾기 — 되풀이되는 모양과 수", "규칙 찾기",
            {1: "다음에 올 모양", 2: "되풀이 규칙의 몇째", 3: "커지는 수 배열", 4: "작아지는 수 배열", 5: "수 배열표"},
            pp=10,
            tips={1: "되풀이되는 마디를 찾아 묶어 보세요",
                  2: "마디의 길이로 나누어 남는 자리를 찾아요",
                  3: "옆 수와의 차이 — 몇씩 커지나요?",
                  4: "몇씩 작아지는지 거꾸로 세어요",
                  5: "오른쪽은 1 큰 수, 아래쪽은 10 큰 수"},
            note="규칙은 ‘되풀이되는 마디’를 찾는 것에서 시작해요. 마디에 동그라미를 치게 하면 다음 것이 바로 보여요.")
    R = rng(5106)
    KS = list(PLANE) + ["●"]

    def g1():
        m = R.choice([2, 3])
        unit = R.sample(KS, m) if R.random() < 0.6 else [R.choice(KS)] * 2 + [R.choice(KS)]
        if len(set(unit)) < 2:
            return
        n = R.randint(m + 2, m * 3)
        row = [unit[i % len(unit)] for i in range(n)]
        nxt = unit[n % len(unit)]
        q = f"{''.join(ic(x) for x in row)} 다음에 올 모양은 무엇인가요?"
        nm = PLANE.get(nxt, ("까만 동그라미",))[0]
        lines = [L(f"{''.join(ic(x) for x in unit)} 되풀이", memo="마디 묶기"), L(f"다음 → {ic(nxt)} {nm}")]
        S.add(1, q, nm, "되풀이 마디를 묶어 보기", lines, None, omr="ex", key=q)
    fill(S, 1, 20, g1)

    def g2():
        m = R.choice([2, 3, 4])
        unit = [R.choice(KS) for _ in range(m)]
        if len(set(unit)) < 2:
            return
        k = R.randint(m + 3, 15)
        q = f"{''.join(ic(x) for x in unit)}가 차례로 되풀이될 때, {k}째 모양은 무엇인가요?"
        r = (k - 1) % m + 1
        nm = PLANE.get(unit[r - 1], ("까만 동그라미",))[0]
        lines = [L(f"{m}개씩 되풀이 → {k} = {m} × {(k - 1) // m} + {r}", memo=f"마디 {(k - 1) // m}번 뒤 {r}째"), L(f"{r}째 모양 {ic(unit[r - 1])} {nm}")]
        S.add(2, q, nm, "마디 길이로 묶어 세기", lines, None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        d = R.randint(1, 5)
        a = R.randint(1, 30)
        seq = [a + d * i for i in range(5)]
        if seq[-1] > 99:
            return
        k = R.randint(2, 4)
        shown = [str(v) if i != k else "□" for i, v in enumerate(seq)]
        q = f"규칙에 따라 수를 늘어놓았어요. {', '.join(shown)}에서 □에 알맞은 수는 무엇인가요?"
        lines = [L(f"{seq[0]} → {seq[1]}: {d}씩 커져요"), L(f"□ = {seq[k - 1]} + {d} = {seq[k]}")]
        S.add(3, q, str(seq[k]), "몇씩 커지는지 찾기", lines, None, key=q)
    fill(S, 3, 20, g3)

    def g4():
        d = R.randint(1, 5)
        a = R.randint(20, 60)
        seq = [a - d * i for i in range(5)]
        if seq[-1] < 0:
            return
        k = R.randint(2, 4)
        shown = [str(v) if i != k else "□" for i, v in enumerate(seq)]
        q = f"규칙에 따라 수를 늘어놓았어요. {', '.join(shown)}에서 □에 알맞은 수는 무엇인가요?"
        lines = [L(f"{seq[0]} → {seq[1]}: {d}씩 작아져요"), L(f"□ = {seq[k - 1]} − {d} = {seq[k]}")]
        S.add(4, q, str(seq[k]), "몇씩 작아지는지 찾기", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        n = R.randint(12, 88)
        if n % 10 in (0, 9) and R.random() < 0.7:
            return
        d, word = R.choice([(1, "바로 오른쪽"), (-1, "바로 왼쪽"), (10, "바로 아래"), (-10, "바로 위")])
        a = n + d
        if not (1 <= a <= 100) or (abs(d) == 1 and (n - 1) // 10 != (a - 1) // 10):
            return
        q = f"1부터 100까지의 수 배열표에서 {n}의 {word} 칸에 있는 수는 무엇인가요?"
        f = Fig()
        r0, c0 = (n - 1) // 10, (n - 1) % 10
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                r, c = r0 + dr, c0 + dc
                if 0 <= r <= 9 and 0 <= c <= 9:
                    v = r * 10 + c + 1
                    x, y = 200 + dc * 120, 330 + dr * 100
                    hl = v == a
                    f.rect(x, y, 120, 100, c="ink", sw=2, f="gold" if v == n else ("coral" if hl else None), fo=0.3 if (v == n or hl) else None, at=0 if hl else "q")
                    f.text(x + 60, y + 62, "?" if hl else str(v), z=34, b=700, at=0 if hl else "q")
        lines = [L(f"{word} 칸 → {'1' if abs(d) == 1 else '10'} {'큰' if d > 0 else '작은'} 수"), L(f"{n} {'+' if d > 0 else MI} {abs(d)} = {a}")]
        S.add(5, q, str(a), "오른쪽 +1 · 아래 +10", lines, f.out(), key=q)
    fill(S, 5, 20, g5)
    return S
