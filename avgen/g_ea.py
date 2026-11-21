# 초등 ① — 큰 수 덧셈 · 뺄셈 · □ 구하기 · 문장제 · 큰 수 · 시각과 시간 · 길이 · 들이 · 무게 (학년을 넘나드는 단원 일곱)
from core import *
from fig import Fig, mv, ang_pt
from kit import *

PLACE = ["일", "십", "백", "천", "만"]

def r100(n):
    return (n + 50) // 100 * 100

def carry_plan(cp):
    if not cp:
        return "자리끼리 더해요"
    names = " · ".join(PLACE[p] for p in cp) + "의 자리"
    return f"{names}에서 받아올림 — 올린 1도 함께 더해요"


# ══════════ 큰 수 덧셈 ══════════
def add():
    S = Set("add", "세 자리 · 네 자리 덧셈", "큰 수 덧셈",
            {1: "받아올림 한 번", 2: "받아올림 두 번", 3: "천의 자리로 받아올림", 4: "네 자리 덧셈", 5: "세 수의 덧셈 · 어림"},
            pp=10,
            tips={1: "자리를 맞춰 쓰고 일의 자리부터 — 10이 넘는 자리만 윗자리로 1을 받아올려요",
                  2: "받아올린 1은 윗자리 위에 작게 써 두고, 그 자리를 더할 때 함께 더해요",
                  3: "백의 자리 합이 10을 넘으면 천의 자리에 1을 써요 — 답은 네 자리 수",
                  4: "네 자리도 똑같이 일의 자리부터. 자리 수가 다르면 오른쪽 끝을 맞춰요",
                  5: "세 수도 한 번에 세로로 — 한 자리 합이 20을 넘으면 2를 받아올려요. 먼저 몇백으로 어림해 두면 답을 확인할 수 있어요"},
            note="받아올림은 ‘10이 모이면 윗자리 1개’라는 뜻이에요. 받아올린 숫자를 작게 남겨 두게 하고, 계산 뒤에는 어림한 값과 견주어 보게 해 주세요.")
    R = rng(311)

    def put(st, a, b, plan):
        fg, lines, res = col_add(a, b)
        q = R.choice([f"{a} + {J(b, '은', '는')} 얼마인가요?", f"{wa(a)} {b}의 합은 얼마인가요?", f"{a} + {eul(b)} 계산하세요."])
        return S.add(st, q, str(res), plan, lines, fg, key=f"{a}+{b}")

    def g1():
        a, b = R.randint(101, 799), R.randint(101, 799)
        cp = carry_pos(a, b)
        if a + b >= 1000 or len(cp) != 1 or cp[0] != (S.count(1) % 2):
            return
        put(1, a, b, carry_plan(cp))
    fill(S, 1, 20, g1)

    def g2():
        a, b = R.randint(118, 789), R.randint(118, 789)
        if a + b >= 1000 or carry_pos(a, b) != [0, 1]:
            return
        put(2, a, b, carry_plan([0, 1]))
    fill(S, 2, 20, g2)

    def g3():
        a, b = R.randint(352, 989), R.randint(208, 989)
        cp = carry_pos(a, b)
        if a + b < 1000 or 2 not in cp or len(cp) != 1 + S.count(3) % 3:
            return
        put(3, a, b, carry_plan(cp) + " → 천의 자리로")
    fill(S, 3, 20, g3)

    def g4():
        n = S.count(4)
        big = n >= 16
        a = R.randint(1203, 8796) if not big else R.randint(4567, 9876)
        b = R.randint(1105, 8899) if (n % 2 == 0 or big) else R.randint(108, 989)
        cp = carry_pos(a, b)
        if len(cp) < 2 or (a + b >= 10000) != big:
            return
        put(4, a, b, carry_plan(cp) + (" → 만의 자리로" if big else ""))
    fill(S, 4, 20, g4)

    def g5():
        a, b, c = R.randint(104, 689), R.randint(104, 689), R.randint(104, 689)
        if len({a, b, c}) < 3 or (a % 10 + b % 10 + c % 10) < 10:
            return
        f, lines, res = col_add3(a, b, c)
        ra, rb, rc = r100(a), r100(b), r100(c)
        lines = [L(f"{ra} + {rb} + {rc} = {ra + rb + rc}", pre="어림", memo="몇백으로 어림해 두기")] + lines
        lines[-1]["memo"] = f"어림한 {J(ra + rb + rc, '과', '와')} 가까워요"
        for el in f.els:
            if isinstance(el.get("at"), int):
                el["at"] += 1
        q = R.choice([f"{a} + {b} + {J(c, '은', '는')} 얼마인가요?", f"세 수 {a}, {b}, {c}의 합은 얼마인가요?"])
        S.add(5, q, str(res), "어림을 먼저 하고, 세 수를 한 번에 세로로 더해요", lines, f.out(), key=f"{a}+{b}+{c}")
    fill(S, 5, 20, g5)
    return S


# ══════════ 큰 수 뺄셈 ══════════
def sub():
    S = Set("sub", "세 자리 · 네 자리 뺄셈", "큰 수 뺄셈",
            {1: "받아내림 한 번", 2: "받아내림 두 번", 3: "0이 있는 수에서 빼기", 4: "네 자리 뺄셈", 5: "몇천에서 빼고 검산"},
            pp=10,
            tips={1: "못 빼는 자리는 바로 윗자리에서 10을 빌려 와요 — 빌려 준 자리 숫자는 1 작아져요",
                  2: "빌려 준 뒤 작아진 숫자로 다음 자리를 빼요. 또 못 빼면 또 빌려요",
                  3: "바로 윗자리가 0이면 빌려 줄 수 없어요 — 그 윗자리에서 빌려 오면 0은 10이 되고, 다시 1을 빌려 주어 9가 돼요",
                  4: "네 자리도 일의 자리부터. 빌려 준 자리에는 작아진 숫자를 위에 써 두어요",
                  5: "5000 − 2378처럼 0이 줄줄이 있으면 0들이 모두 9가 돼요. 답 + 뺀 수 = 처음 수로 검산!"},
            note="뺄셈의 받아내림은 ‘윗자리 1개를 풀어 아랫자리 10개로’예요. 0이 있는 자리는 꼭 그림처럼 차례로 빌려 오는 과정을 말로 따라 하게 해 주세요.")
    R = rng(312)

    def put(st, a, b, plan, check=False):
        fg, lines, res = col_sub(a, b)
        if check:
            lines.append(L(f"{res} + {b} = {a}", pre="검산", memo="답 + 뺀 수 = 처음 수"))
        q = R.choice([f"{a} − {J(b, '은', '는')} 얼마인가요?", f"{wa(a)} {b}의 차는 얼마인가요?", f"{a} − {eul(b)} 계산하세요."])
        return S.add(st, q, str(res), plan, lines, fg, key=f"{a}-{b}")

    def nozero(n):
        return "0" not in str(n)

    def g1():
        a = R.randint(312, 987); b = R.randint(111, a - 50)
        n, z = borrow_info(a, b)
        if not nozero(a) or n != 1 or z:
            return
        put(1, a, b, "일의 자리부터 — 못 빼는 자리는 윗자리에서 10을 빌려 와요")
    fill(S, 1, 20, g1)

    def g2():
        a = R.randint(412, 987); b = R.randint(128, a - 30)
        n, z = borrow_info(a, b)
        if not nozero(a) or n != 2 or z or a - b < 10:
            return
        put(2, a, b, "빌려 준 자리는 1 작아진 숫자로 빼요 — 두 번 빌려 와요")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3)
        h = R.randint(3, 9)
        a = h * 100 if k % 3 == 0 else h * 100 + R.randint(1, 9)
        b = R.randint(101, a - 20)
        n, z = borrow_info(a, b)
        if not z or b % 10 == 0:
            return
        put(3, a, b, "십의 자리가 0이라 백의 자리에서 빌려 와요 — 0은 10이 되었다가 9로")
    fill(S, 3, 20, g3)

    def g4():
        a = R.randint(2113, 9876); b = R.randint(1105, a - 200) if S.count(4) % 2 else R.randint(118, 989)
        n, z = borrow_info(a, b)
        if n < 2 or z or "0" in str(a):
            return
        put(4, a, b, "자리를 맞춰 쓰고 일의 자리부터 — 못 빼면 바로 윗자리에서 빌려요")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5)
        t = R.randint(2, 9)
        if k < 10:
            a = t * 1000
        else:
            a = t * 1000 + R.choice([R.randint(1, 9), R.randint(1, 9) * 10, R.randint(1, 9) * 100 + R.randint(1, 9)])
        b = R.randint(1111, a - 300) if k % 2 else R.randint(123, 987)
        n, z = borrow_info(a, b)
        if not z or b % 10 == 0:
            return
        put(5, a, b, "0이 줄줄이 있으면 0들이 모두 9가 돼요 — 다 빼고 덧셈으로 검산", check=True)
    fill(S, 5, 20, g5)
    return S


# ══════════ □ 구하기 — 덧셈과 뺄셈, 곱셈과 나눗셈의 관계 ══════════
def rel():
    S = Set("rel", "□ 구하기 — 거꾸로 셈", "□ 구하기",
            {1: "□ + ○ = △", 2: "○ − □ = △ · □ − ○ = △", 3: "세 자리 수의 □", 4: "□ × ○ = △", 5: "□ ÷ ○ = △ · ○ ÷ □ = △"},
            pp=10,
            tips={1: "전체 − 아는 부분 = 모르는 부분. □ + 25 = 63 → □ = 63 − 25",
                  2: "63 − □ = 25 → □ = 63 − 25 · □ − 25 = 38 → □ = 38 + 25 — 띠 그림에서 전체가 어느 것인지 먼저 찾아요",
                  3: "수가 커져도 방법은 같아요. 덧셈 ↔ 뺄셈으로 바꾸고 마지막에 넣어서 확인",
                  4: "□ × 6 = 84 → □ = 84 ÷ 6 — 곱셈을 거꾸로 하면 나눗셈",
                  5: "□ ÷ 4 = 9 → □ = 9 × 4 · 36 ÷ □ = 4 → □ = 36 ÷ 4"},
            note="□ 문제는 ‘띠 그림에서 전체와 부분 찾기’가 핵심이에요. 식을 바꾼 뒤에는 꼭 □에 답을 넣어 처음 식이 맞는지 확인하게 해 주세요.")
    R = rng(313)

    def put_add(st, A, B):
        # A + B = T 꼴: □ 위치 랜덤
        T = A + B
        side = R.random() < 0.5
        x, known = (A, B) if side else (B, A)
        q = (f"□ + {known} = {T}에서 □는 얼마인가요?" if side else f"{known} + □ = {T}에서 □에 알맞은 수는 얼마인가요?")
        f = Fig()
        parts = [(x, "□"), (known, str(known))] if side else [(known, str(known)), (x, "□")]
        bx = tape(f, parts, total=str(T))
        i = 0 if side else 1
        f.text(bx[i][0] + bx[i][1] / 2, 400, str(x), z=40, c="coral", at=1, b=700)
        lines = [L(f"□ = {T} − {known}", memo="전체에서 아는 부분을 빼요"), L(f"{T} − {known} = {x}"),
                 L(f"{x} + {known} = {T}" if side else f"{known} + {x} = {T}", pre="확인"), L(f"□ = {x}")]
        return S.add(st, q, str(x), "띠 그림에서 전체를 찾고 — 전체 − 아는 부분", lines, f.out(), key=f"+{x}|{known}|{side}")

    def put_sub(st, M, N_):
        # M − □ = R  또는  □ − N = R
        if R.random() < 0.5:
            x = R.randint(N_ // 3 + 1, M - 5)
            r = M - x
            q = f"{M} − □ = {r}에서 □는 얼마인가요?"
            f = Fig()
            bx = tape(f, [(x, "□"), (r, str(r))], total=str(M))
            f.text(bx[0][0] + bx[0][1] / 2, 400, str(x), z=40, c="coral", at=1, b=700)
            lines = [L(f"□ = {M} − {r}", memo=f"전체 {M}에서 남은 {r}를 빼요" if not _has_b(r) else f"전체 {M}에서 남은 {r}을 빼요"),
                     L(f"{M} − {r} = {x}"), L(f"{M} − {x} = {r}", pre="확인"), L(f"□ = {x}")]
            return S.add(st, q, str(x), f"전체는 {M} — 빼는 수 = 전체 − 남은 수", lines, f.out(), key=f"-a{M}|{x}")
        else:
            x = M
            r = M - N_
            q = f"□ − {N_} = {r}에서 □는 얼마인가요?"
            f = Fig()
            bx = tape(f, [(r, str(r)), (N_, str(N_))], total="□")
            f.text(330, 160, str(x), z=40, c="coral", at=1, b=700)
            lines = [L(f"□ = {r} + {N_}", memo="□가 전체 — 두 부분을 더해요"), L(f"{r} + {N_} = {x}"),
                     L(f"{x} − {N_} = {r}", pre="확인"), L(f"□ = {x}")]
            return S.add(st, q, str(x), "□가 전체예요 — 남은 수 + 뺀 수", lines, f.out(), key=f"-b{x}|{N_}")

    def g1():
        A, B = R.randint(11, 69), R.randint(8, 49)
        if A + B > 99 or A == B:
            return
        put_add(1, A, B)
    fill(S, 1, 20, g1)

    def g2():
        M = R.randint(41, 98); N_ = R.randint(12, M - 11)
        put_sub(2, M, N_)
    fill(S, 2, 20, g2)

    def g3():
        if S.count(3) % 2 == 0:
            A, B = R.randint(125, 689), R.randint(108, 389)
            if A + B > 999:
                return
            put_add(3, A, B)
        else:
            M = R.randint(402, 985); N_ = R.randint(115, M - 105)
            put_sub(3, M, N_)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4)
        a = R.randint(2, 9)
        x = R.randint(2, 9) if k < 8 else R.randint(11, 29)
        T = a * x
        f = Fig()
        if k % 2 == 0:
            q = f"□ × {a} = {T}에서 □는 얼마인가요?"
            eq_tape(f, a, "□", str(T))
            f.text(330, 420, f"□ = {x}", z=36, c="coral", at=2, b=700)
            lines = [L(f"□ = {T} ÷ {a}", memo="곱셈을 거꾸로 — 나눗셈"), L(f"{T} ÷ {a} = {x}"), L(f"{x} × {a} = {T}", pre="확인"), L(f"□ = {x}")]
            plan = f"□를 {a}번 더하면 {T} — {T}를 {a}칸으로 똑같이 나눠요"
        else:
            q = f"{a} × □ = {T}에서 □에 알맞은 수는 얼마인가요?"
            eq_tape(f, x, str(a), str(T))
            f.text(330, 420, f"{a}씩 □칸 → □ = {x}", z=34, c="coral", at=2, b=700)
            lines = [L(f"□ = {T} ÷ {a}", memo=f"{T} 안에 {J(a, '이', '가')} 몇 번?"), L(f"{T} ÷ {a} = {x}"), L(f"{a} × {x} = {T}", pre="확인"), L(f"□ = {x}")]
            plan = f"{a}씩 몇 묶음이 {T}인지 — 나눗셈으로"
        S.add(4, q, str(x), plan, lines, f.out(), key=f"x{k % 2}|{a}|{x}")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5)
        f = Fig()
        if k % 2 == 0:
            a = R.randint(2, 9); b = R.randint(3, 9) if k < 8 else R.randint(11, 25)
            x = a * b
            q = f"□ ÷ {a} = {b}에서 □는 얼마인가요?"
            eq_tape(f, a, str(b), "□")
            f.text(330, 420, f"□ = {x}", z=36, c="coral", at=2, b=700)
            lines = [L(f"□ = {b} × {a}", memo=f"{a}칸에 {b}씩 — 곱셈으로"), L(f"{b} × {a} = {x}"), L(f"{x} ÷ {a} = {b}", pre="확인"), L(f"□ = {x}")]
            plan = f"□를 {a}칸으로 나눈 한 칸이 {b} — 거꾸로 곱해요"
        else:
            b = R.randint(2, 9); x = R.randint(2, 9)
            a = b * x
            q = f"{a} ÷ □ = {b}에서 □에 알맞은 수는 얼마인가요?"
            eq_tape(f, x, str(b), str(a))
            f.text(330, 420, f"{b}씩 □칸 → □ = {x}", z=34, c="coral", at=2, b=700)
            lines = [L(f"□ = {a} ÷ {b}", memo=f"한 칸이 {b} — 칸 수를 구해요"), L(f"{a} ÷ {b} = {x}"), L(f"{a} ÷ {x} = {b}", pre="확인"), L(f"□ = {x}")]
            plan = f"{a}를 □칸으로 나누면 한 칸이 {b} — 칸 수 = {a} ÷ {b}" if not _has_b(a) else f"{a}을 □칸으로 나누면 한 칸이 {b} — 칸 수 = {a} ÷ {b}"
        S.add(5, q, str(x), plan, lines, f.out(), key=f"d{k % 2}|{q}")
    fill(S, 5, 20, g5)
    return S

def _has_b(n):
    from core import _has_batchim
    return _has_batchim(str(n))

U_BAT = {"cm": False, "mm": False, "m": False, "`m`": False, "km": False, "mL": False, "L": False, "g": True, "`g`": True, "kg": True, "t": True, "`t`": True}
def uj(u, a, b):
    return u + (a if U_BAT[u] else b)
def uro(u):
    return u + ("으로" if U_BAT[u] else "로")


# ══════════ 문장제 — 문장을 식으로 ══════════
THINGS = [("구슬", "개"), ("딱지", "장"), ("색종이", "장"), ("사탕", "개"), ("연필", "자루"), ("동화책", "권"), ("스티커", "장"), ("귤", "개"), ("공책", "권"), ("단추", "개")]

def word():
    S = Set("word", "문장제 — 문장을 식으로 옮기기", "문장제",
            {1: "모두 몇 — 더하기", 2: "남은 것 · 차 — 빼기", 3: "몇씩 몇 묶음 · 몇 배 — 곱하기", 4: "똑같이 나누기 — 나누기", 5: "두 번 계산하는 문장제"},
            pp=6,
            tips={1: "‘모두’, ‘더 ~하면’은 두 양을 합치는 말 — 덧셈",
                  2: "‘남은’, ‘~보다 몇 더 많은’은 빼기 — 큰 수에서 작은 수를 빼요",
                  3: "‘한 상자에 6개씩 8상자’ = 6 × 8 · ‘~의 3배’ = ~ × 3",
                  4: "‘똑같이 나누어 주면 한 명에 몇 개’ · ‘몇 개씩 담으면 몇 봉지’ — 둘 다 나눗셈",
                  5: "먼저 구할 것을 정하고(중간 답), 그것으로 다시 계산해요. 식 두 개를 차례로"},
            note="문장제는 계산보다 ‘무엇을 구하는지 · 어떤 셈인지’를 고르는 연습이에요. 그림(띠)으로 먼저 나타내고 식을 세운 뒤, 답에 단위를 붙여 문장으로 말하게 해 주세요.")
    R = rng(314)

    def name():
        return R.choice(PEOPLE)

    def g1():
        k = S.count(1) % 4
        t, u = R.choice(THINGS)
        a, b = R.randint(18, 389), R.randint(15, 289)
        if a == b or (a % 10 + b % 10) < 10:
            return
        n1, n2 = R.sample(PEOPLE, 2)
        if k == 0:
            q = f"{eun(n1)} {eul(t)} {a}{u}, {eun(n2)} {b}{u} 가지고 있어요. 두 사람이 가진 {eun(t)} 모두 몇 {u}인가요?"
        elif k == 1:
            a, b = R.randint(15, 45), R.randint(6, 28)
            if (a % 10 + b % 10) < 10:
                return
            q = f"버스에 {a}명이 타고 있었는데, 정류장에서 {b}명이 더 탔어요. 버스에 탄 사람은 모두 몇 명인가요?"
            u = "명"
        elif k == 2:
            q = f"{eun(n1)} 줄넘기를 어제 {a}번, 오늘 {b}번 했어요. 이틀 동안 모두 몇 번 했나요?"
            u = "번"
        else:
            q = f"가게에 {t} {a}{u}{'이' if _has_b(u) else '가'} 있었는데, {b}{u}{'을' if _has_b(u) else '를'} 더 들여왔어요. 가게에 있는 {eun(t)} 모두 몇 {u}인가요?"
        f = Fig()
        bx = tape(f, [(a, str(a)), (b, str(b))], total="?")
        f.text(330, 160, f"{a + b}{u}", z=36, c="coral", at=2, b=700)
        lines = [L("모두 → 두 양을 합쳐요", memo="덧셈"), L(f"{a} + {b} = {a + b}"), L(f"모두 {a + b}{u}")]
        S.add(1, q, f"{a + b}{u}", "‘모두’ — 두 양을 더해요", lines, f.out(), ap=str(a + b), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 4
        t, u = R.choice(THINGS)
        a = R.randint(52, 480); b = R.randint(17, a - 12)
        if a % 10 >= b % 10:
            return
        n1, n2 = R.sample(PEOPLE, 2)
        f = Fig()
        if k == 0:
            q = f"{eun(n1)} {t} {a}{u} 중에서 {b}{u}{'을' if _has_b(u) else '를'} 동생에게 주었어요. 남은 {J(t, '은', '는')} 몇 {u}인가요?"
            tape(f, [(b, f"준 {b}"), (a - b, "?")], total=str(a))
            lines = [L("남은 것 → 전체에서 준 것을 빼요", memo="뺄셈"), L(f"{a} − {b} = {a - b}"), L(f"남은 {t} {a - b}{u}")]
            plan = "‘남은’ — 전체 − 준 것"
        elif k == 1:
            q = f"{eun(n1)} {eul(t)} {a}{u}, {eun(n2)} {b}{u} 가지고 있어요. {eun(n1)} {n2}보다 {eul(t)} 몇 {u} 더 많이 가지고 있나요?"
            compare_bars(f, a, b, n1, n2, diff_at=1)
            lines = [L("~보다 몇 더 → 두 양의 차", memo="큰 수 − 작은 수"), L(f"{a} − {b} = {a - b}"), L(f"{a - b}{u} 더 많아요")]
            plan = "‘~보다 몇 더 많은’ — 큰 수에서 작은 수를 빼요"
        elif k == 2:
            q = f"운동장에 학생 {a}명이 있었는데, {b}명이 교실로 들어갔어요. 운동장에 남은 학생은 몇 명인가요?"
            u = "명"
            tape(f, [(b, f"들어간 {b}"), (a - b, "?")], total=str(a))
            lines = [L("남은 사람 → 처음 − 들어간 사람", memo="뺄셈"), L(f"{a} − {b} = {a - b}"), L(f"남은 학생 {a - b}명")]
            plan = "‘남은’ — 처음 수에서 빠져나간 수를 빼요"
        else:
            q = f"줄넘기 기록이 {eun(n1)} {a}번, {eun(n2)} {b}번이에요. 두 사람의 기록은 몇 번 차이가 나나요?"
            u = "번"
            compare_bars(f, a, b, n1, n2, diff_at=1)
            lines = [L("차이 → 큰 수 − 작은 수", memo="뺄셈"), L(f"{a} − {b} = {a - b}"), L(f"{a - b}번 차이")]
            plan = "‘차이’ — 두 기록의 차"
        S.add(2, q, f"{a - b}{u}", plan, lines, f.out(), ap=str(a - b), key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 4
        a, b = R.randint(12, 48), R.randint(3, 9)
        n1 = name()
        f = Fig()
        if k == 0:
            t, u = R.choice([("귤", "개"), ("사과", "개"), ("초콜릿", "개"), ("구슬", "개")])
            q = f"한 상자에 {iga(t)} {a}개씩 들어 있어요. {b}상자에 들어 있는 {J(t, '은', '는')} 모두 몇 개인가요?"
            eq_tape(f, b, str(a), "?")
            lines = [L(f"{a}개씩 {b}상자 → {a} × {b}", memo="같은 수를 여러 번"), L(f"{a} × {b} = {a * b}"), L(f"모두 {a * b}개")]
            ans, plan = f"{a * b}개", f"{a}씩 {b}묶음 — 곱셈"
        elif k == 1:
            q = f"{eun(n1)} 하루에 책을 {a}쪽씩 읽어요. {b}일 동안 읽는 책은 모두 몇 쪽인가요?"
            eq_tape(f, b, str(a), "?")
            lines = [L(f"{a}쪽씩 {b}일 → {a} × {b}", memo="하루치가 날마다 같아요"), L(f"{a} × {b} = {a * b}"), L(f"모두 {a * b}쪽")]
            ans, plan = f"{a * b}쪽", f"{a}쪽씩 {b}번 — 곱셈"
        elif k == 2:
            q = f"강당에 의자가 한 줄에 {a}개씩 {b}줄 놓여 있어요. 의자는 모두 몇 개인가요?"
            eq_tape(f, b, str(a), "?")
            lines = [L(f"한 줄 {a}개 × {b}줄", memo="줄마다 같은 수"), L(f"{a} × {b} = {a * b}"), L(f"의자 {a * b}개")]
            ans, plan = f"{a * b}개", f"{a}개씩 {b}줄 — 곱셈"
        else:
            a, b = R.randint(8, 13), R.randint(3, 5)
            q = f"{n1}의 나이는 {a}살이에요. 삼촌의 나이는 {n1} 나이의 {b}배예요. 삼촌은 몇 살인가요?"
            eq_tape(f, b, f"{a}살", "삼촌")
            lines = [L(f"{a}살의 {b}배 → {a} × {b}", memo="~의 몇 배는 곱셈"), L(f"{a} × {b} = {a * b}"), L(f"삼촌 {a * b}살")]
            ans, plan = f"{a * b}살", f"‘{a}의 {b}배’ — {a} × {b}"
        S.add(3, q, ans, plan, lines, f.out(), ap=str(a * b), key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 4
        a, b = R.randint(3, 9), R.randint(4, 16)
        T = a * b
        f = Fig()
        if k == 0:
            t, u = R.choice([("사탕", "개"), ("색종이", "장"), ("구슬", "개"), ("연필", "자루")])
            q = f"{t} {T}{u}{'을' if _has_b(u) else '를'} {a}명에게 똑같이 나누어 주면 한 명이 몇 {u}씩 받나요?"
            eq_tape(f, a, "?", f"{T}{u}")
            lines = [L(f"{T}{u}{'을' if _has_b(u) else '를'} {a}명에게 똑같이 → {T} ÷ {a}", memo="똑같이 나누기"), L(f"{T} ÷ {a} = {b}"), L(f"{b} × {a} = {T}", pre="확인"), L(f"한 명에 {b}{u}")]
            ans, plan, ap = f"{b}{u}", f"{a}명에게 똑같이 — {T} ÷ {a}", str(b)
        elif k == 1:
            q = f"구슬 {T}개를 한 봉지에 {a}개씩 담으면 몇 봉지가 되나요?"
            eq_tape(f, b, str(a), f"{T}개")
            f.text(330, 420, "몇 칸?", z=30, c="coral", at="q", b=700)
            lines = [L(f"{T}개를 {a}개씩 → {T} ÷ {a}", memo=f"{T} 안에 {J(a, '이', '가')} 몇 번"), L(f"{T} ÷ {a} = {b}"), L(f"{a} × {b} = {T}", pre="확인"), L(f"{b}봉지")]
            ans, plan, ap = f"{b}봉지", f"{a}개씩 묶어 세기 — {T} ÷ {a}", str(b)
        elif k == 2:
            q = f"길이가 {T} cm인 끈을 {a} cm씩 자르면 몇 도막이 되나요?"
            eq_tape(f, b, f"{a}", f"{T} cm")
            lines = [L(f"{T} cm를 {a} cm씩 → {T} ÷ {a}", memo="같은 길이로 자르기"), L(f"{T} ÷ {a} = {b}"), L(f"{a} × {b} = {T}", pre="확인"), L(f"{b}도막")]
            ans, plan, ap = f"{b}도막", f"{a} cm씩 몇 번 — {T} ÷ {a}", str(b)
        else:
            q = f"학생 {T}명이 한 모둠에 {a}명씩 앉으면 모둠은 몇 개가 되나요?"
            eq_tape(f, b, f"{a}", f"{T}명")
            lines = [L(f"{T}명을 {a}명씩 → {T} ÷ {a}", memo="묶음의 수"), L(f"{T} ÷ {a} = {b}"), L(f"{a} × {b} = {T}", pre="확인"), L(f"모둠 {b}개")]
            ans, plan, ap = f"{b}개", f"{a}명씩 묶기 — {T} ÷ {a}", str(b)
        S.add(4, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        n1 = name()
        f = None
        if k == 0:
            p = R.randint(3, 9) * 100 + R.choice([0, 50])
            c = R.randint(2, 4)
            pay = ((p * c) // 1000 + 1) * 1000
            if pay - p * c < 100:
                return
            q = f"{eun(n1)} {p}원짜리 공책 {c}권을 사고 {pay}원을 냈어요. 거스름돈은 얼마인가요?"
            lines = [L(f"{p} × {c} = {p * c}", pre="공책값", memo="먼저 낼 돈"), L(f"{pay} − {p * c} = {pay - p * c}", pre="거스름돈"), L(f"거스름돈 {pay - p * c}원")]
            ans, ap, plan = f"{pay - p * c}원", str(pay - p * c), "① 공책값(곱셈) → ② 낸 돈 − 공책값"
            f = Fig()
            tape(f, [(p * c, f"공책값 {p * c}"), (pay - p * c, "?")], total=f"{pay}원")
        elif k == 1:
            a, b = R.randint(12, 25), R.randint(3, 6)
            c = R.randint(5, a * b // 3)
            q = f"한 상자에 {a}개씩 들어 있는 사과가 {b}상자 있었어요. 그중 {c}개를 팔았다면 남은 사과는 몇 개인가요?"
            lines = [L(f"{a} × {b} = {a * b}", pre="처음 사과", memo="몇씩 몇 상자"), L(f"{a * b} − {c} = {a * b - c}", pre="남은 사과"), L(f"{a * b - c}개")]
            ans, ap, plan = f"{a * b - c}개", str(a * b - c), "① 처음 사과(곱셈) → ② 판 것을 빼요"
            f = Fig()
            tape(f, [(c, f"판 {c}"), (a * b - c, "?")], total=f"{a}개씩 {b}상자")
        elif k == 2:
            a, b = R.randint(3, 8), R.randint(6, 15)
            c = R.randint(1, b - 2)
            T = a * b
            q = f"색종이 {T}장을 {a}명이 똑같이 나누어 가졌어요. {eun(n1)} 받은 색종이 중에서 {c}장을 썼어요. {n1}에게 남은 색종이는 몇 장인가요?"
            lines = [L(f"{T} ÷ {a} = {b}", pre="한 명 몫", memo="똑같이 나누기"), L(f"{b} − {c} = {b - c}", pre="남은 것"), L(f"{b - c}장")]
            ans, ap, plan = f"{b - c}장", str(b - c), "① 한 명이 받은 양(나눗셈) → ② 쓴 것을 빼요"
            f = Fig()
            eq_tape(f, a, "?", f"{T}장")
        else:
            a = R.randint(25, 48); b = R.randint(6, a - 8); c = R.randint(5, 19)
            q = f"버스에 {a}명이 타고 있었어요. 정류장에서 {b}명이 내리고 {c}명이 탔어요. 지금 버스에 탄 사람은 몇 명인가요?"
            lines = [L(f"{a} − {b} = {a - b}", pre="내린 뒤", memo="먼저 내리고"), L(f"{a - b} + {c} = {a - b + c}", pre="탄 뒤"), L(f"{a - b + c}명")]
            ans, ap, plan = f"{a - b + c}명", str(a - b + c), "① 내린 사람 빼기 → ② 탄 사람 더하기"
        S.add(5, q, ans, plan, lines, f.out() if f else None, ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 큰 수 ══════════
def big():
    S = Set("big", "큰 수 — 자릿값에서 조까지", "큰 수",
            {1: "네 자리 수의 자릿값", 2: "다섯 자리 수 · 만", 3: "억과 조", 4: "뛰어 세기 · 10배", 5: "크기 비교"},
            pp=10,
            tips={1: "4736 = 4000 + 700 + 30 + 6 — 숫자가 놓인 자리가 값을 정해요",
                  2: "10000은 ‘만’. 47205 = 4만 7천 2백 5 — 만의 자리부터 읽어요",
                  3: "만이 10000개면 1억, 억이 10000개면 1조 — 네 자리씩 끊어 읽어요",
                  4: "몇씩 뛰어 세는지 보려면 바뀌는 자리를 찾아요. 10배 하면 숫자가 한 자리씩 왼쪽으로",
                  5: "자리 수가 많은 쪽이 커요. 자리 수가 같으면 가장 높은 자리부터 차례로 비교"},
            note="큰 수는 ‘네 자리씩 끊기’와 ‘자리 이름’이 전부예요. 자리 표를 직접 그려 숫자를 넣어 보게 하면 0이 있는 수도 헷갈리지 않아요.")
    R = rng(315)

    def g1():
        k = S.count(1)
        n = R.randint(1023, 9987)
        s = str(n)
        f = Fig()
        if k % 2 == 0:
            p = R.randint(1, 3)
            d = int(s[3 - p])
            if d == 0 or s.count(str(d)) > 1:
                return
            place_table(f, n, hl=p, hl_at=1)
            parts = [str(int(c) * 10 ** (3 - i)) for i, c in enumerate(s) if c != "0"]
            q = f"{n}에서 숫자 {iga(d)} 나타내는 값은 얼마인가요?"
            lines = [L(f"{n} = {' + '.join(parts)}", memo="자리마다 나누기"), L(f"{d}는 {PL[p]}의 자리 숫자" if not _has_b(d) else f"{d}은 {PL[p]}의 자리 숫자"), L(f"{d} × {10 ** p} = {d * 10 ** p}")]
            S.add(1, q, str(d * 10 ** p), "숫자가 놓인 자리를 찾아요", lines, f.out(), key=f"v{n}|{d}")
        else:
            ds = [int(c) for c in s]
            q = f"1000이 {ds[0]}개, 100이 {ds[1]}개, 10이 {ds[2]}개, 1이 {ds[3]}개인 수는 얼마인가요?"
            place_table(f, n, at=1)
            lines = [L(f"{ds[0] * 1000} + {ds[1] * 100} + {ds[2] * 10} + {ds[3]} = {n}", memo="자리마다 모아요"), L(f"천 · 백 · 십 · 일의 자리에 {ds[0]}, {ds[1]}, {ds[2]}, {ds[3]}"), L(f"{n}")]
            S.add(1, q, str(n), "개수를 자리마다 차례로 써요", lines, f.out(), key=f"m{n}")
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        n = R.randint(10203, 98760)
        s = str(n)
        if "0" not in s[1:] and k == 2:
            return
        f = Fig()
        if k == 0:
            p = R.randint(2, 4)
            d = int(s[4 - p])
            if d == 0 or s.count(str(d)) > 1:
                return
            place_table(f, n, hl=p, hl_at=1)
            q = f"{n}에서 숫자 {d}{'이' if _has_b(d) else '가'} 나타내는 값은 얼마인가요?"
            lines = [L(f"{d}{'은' if _has_b(d) else '는'} {PL[p]}의 자리 숫자", memo="오른쪽에서 몇째 자리?"), L(f"{d} × {10 ** p} = {d * 10 ** p}"), L(f"{com(d * 10 ** p)}")]
            S.add(2, q, com(d * 10 ** p), "자리 표에 넣어 자리를 찾아요", lines, f.out(), key=f"v{n}|{d}")
        elif k == 1:
            ds = [int(c) for c in s]
            q = f"10000이 {ds[0]}개, 1000이 {ds[1]}개, 100이 {ds[2]}개, 10이 {ds[3]}개, 1이 {ds[4]}개인 수는 얼마인가요?"
            place_table(f, n, at=1)
            lines = [L(f"만의 자리부터 {', '.join(map(str, ds))}", memo="개수를 그대로 자리에"), L(f"{n}"), L(f"{read_kr(n)}", memo="읽기")]
            S.add(2, q, str(n), "10000이 몇 개 → 만의 자리 숫자", lines, f.out(), key=f"m{n}")
        else:
            q = f"‘{read_kr(n)}’을 숫자로 쓰면 얼마인가요?" if _has_b(read_kr(n)) else f"‘{read_kr(n)}’를 숫자로 쓰면 얼마인가요?"
            place_table(f, n, at=1)
            miss = [PL[4 - i] for i, c in enumerate(s) if c == "0"]
            lines = [L(f"만 앞은 {s[0]}, 만 뒤 네 자리 {s[1:]}", memo="네 자리씩 끊기"), L(f"읽지 않은 {', '.join(miss)}의 자리에는 0", memo="빈자리 0"), L(f"{n}")]
            S.add(2, q, str(n), "만을 기준으로 앞과 뒤를 나누어 써요", lines, f.out(), key=f"r{n}")
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 4
        if k == 0:
            e, m = R.randint(1, 9), R.randint(1, 99) * 100
            n = e * 10 ** 8 + m * 10 ** 4
            q = f"{e}억 {m}만을 숫자로 쓰면 얼마인가요?"
            lines = [L(f"{e}억 = {com(e * 10 ** 8)}", memo="억은 0이 8개"), L(f"{m}만 = {com(m * 10 ** 4)}", memo="만은 0이 4개"), L(f"{com(e * 10 ** 8)} + {com(m * 10 ** 4)} = {com(n)}")]
            ans = com(n)
        elif k == 1:
            jo, eok = R.randint(1, 9), R.randint(1, 99) * 100
            n = jo * 10 ** 12 + eok * 10 ** 8
            q = f"1조가 {jo}개, 1억이 {eok}개인 수를 ‘조’와 ‘억’을 써서 나타내면 얼마인가요?"
            lines = [L(f"1조 {jo}개 → {jo}조", memo="조 자리"), L(f"1억 {eok}개 → {eok}억", memo="억이 10000개면 1조"), L(f"{man(n)}")]
            ans = man(n)
        elif k == 2:
            n = R.randint(10 ** 8, 99 * 10 ** 8)
            s = str(n)
            p = R.randint(5, len(s) - 1)
            d = int(s[len(s) - 1 - p])
            if d == 0 or s.count(str(d)) > 2:
                return
            q = f"{com(n)}에서 숫자 {d}{'이' if _has_b(d) else '가'} 나타내는 값은 얼마인가요?"
            lines = [L(f"{man(n)}", memo="네 자리씩 끊어 읽기"), L(f"{d}{'은' if _has_b(d) else '는'} {PL[p]}의 자리"), L(f"{d} × {com(10 ** p)} = {com(d * 10 ** p)}")]
            ans = com(d * 10 ** p)
        else:
            n = R.randint(1, 9) * 10 ** 8 + R.randint(1, 9999) * 10 ** 4 + R.choice([0, R.randint(1, 9999)])
            q = f"{com(n)}을 읽으면 어떻게 되나요? (‘억’, ‘만’을 써서)" if _has_b(str(n)) else f"{com(n)}를 읽으면 어떻게 되나요? (‘억’, ‘만’을 써서)"
            lines = [L(f"뒤에서부터 네 자리씩 끊기", memo="만 · 억 자리 찾기"), L(f"{man(n)}"), L(f"{read_kr(n)}")]
            ans = read_kr(n)
        f = Fig()
        place_table(f, n, at=1 if k in (0, 1) else "q", hl=(p if k == 2 else None), hl_at=1)
        S.add(3, q, ans, "네 자리씩 끊어 — 만 · 억 · 조", lines, f.out(), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4)
        f = Fig()
        if k < 14:
            step = R.choice([1000, 10000, 100000, 10 ** 6, 10 ** 7, 10 ** 8])
            st0 = R.randint(1, 9) * step * 10 + R.randint(1, 9) * step + R.randint(0, 9) * (step // 10)
            n = R.randint(3, 5)
            vals = [st0 + step * i for i in range(n + 1)]
            fmt = man if step >= 10 ** 4 else com
            if k % 2 == 0:
                q = f"{fmt(st0)}에서 {fmt(step)}씩 {n}번 뛰어 센 수는 얼마인가요?"
                jump_line(f, vals, fmt=fmt, jumps_at=list(range(n)), jlab=f"+{fmt(step)}", z=18)
                lines = [L(f"{fmt(step)}씩 → {PL[len(str(step)) - 1]}의 자리 숫자가 1씩 커져요", memo="바뀌는 자리")] + \
                        [L(f"{com(vals[i])} + {com(step)} = {com(vals[i + 1])}") for i in range(n - 1)] + [L(f"{com(vals[n - 1])} + {com(step)} = {com(vals[n])}", memo=f"{n}번째")]
                lines = lines[:1] + lines[1:]
                for el in f.els:
                    if isinstance(el.get("at"), int):
                        el["at"] += 1
                S.add(4, q, fmt(vals[-1]), f"{PL[len(str(step)) - 1]}의 자리를 하나씩 올려요", lines[:n + 1], f.out(), omr="ex", key=q)
            else:
                show = ", ".join(fmt(v) for v in vals[:4])
                q = f"{show}, …은 얼마씩 뛰어 센 것인가요?"
                jump_line(f, vals[:4], fmt=fmt, jumps_at=[0, 0, 0], z=18)
                lines = [L(f"{com(vals[1])} − {com(vals[0])} = {com(step)}", memo="이웃한 두 수의 차"), L(f"{PL[len(str(step)) - 1]}의 자리 숫자만 1씩 커져요"), L(f"{fmt(step)}씩")]
                S.add(4, q, f"{fmt(step)}씩", "이웃한 수끼리 빼 보거나 바뀌는 자리를 찾아요", lines, f.out(), ap=com(step), omr="ex", key=q)
        else:
            a = R.randint(12, 980) * R.choice([10 ** 4, 10 ** 5])
            m = R.choice([10, 100, 1000])
            q = f"{man(a)}의 {m}배는 얼마인가요?"
            zeros = len(str(m)) - 1
            lines = [L(f"{m}배 → 끝에 0을 {zeros}개 더 붙여요", memo="숫자가 왼쪽으로 한 자리씩"), L(f"{com(a)} × {m} = {com(a * m)}"), L(f"{man(a * m)}")]
            place_table(f, a * m, at=2)
            S.add(4, q, man(a * m), f"{m}배 하면 자리가 {zeros}칸 올라가요", lines, f.out(), ap=com(a * m), omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        if k == 0:
            n = R.randint(10 ** 6, 10 ** 8 - 1)
            s = list(str(n))
            i = R.randint(1, len(s) - 2)
            t = s[:]
            t[i] = str((int(s[i]) + R.randint(1, 8)) % 10)
            m = int("".join(t))
            if m == n:
                return
        elif k == 1:
            n = R.randint(10 ** 7, 10 ** 9)
            m = R.randint(10 ** 6, 10 ** 8)
            if len(str(n)) == len(str(m)):
                return
        else:
            base = R.randint(10, 99) * 10 ** 8
            n = base + R.randint(1, 9999) * 10 ** 4
            m = base + R.randint(1, 9999) * 10 ** 4 + R.randint(1, 9999)
            if n // 10 ** 4 == m // 10 ** 4:
                return
        a, b = (n, m) if R.random() < 0.5 else (m, n)
        sa, sb = str(a), str(b)
        big_ = max(a, b)
        if len(sa) != len(sb):
            lines = [L(f"자리 수: {len(sa)}자리, {len(sb)}자리", memo="자리 수가 많은 쪽이 커요"), L(f"{com(big_)}이 더 커요" if _has_b(str(big_)) else f"{com(big_)}가 더 커요")]
            plan = "먼저 자리 수를 세요"
        else:
            j = next(i for i in range(len(sa)) if sa[i] != sb[i])
            p = len(sa) - 1 - j
            same = f"{PL[len(sa) - 1]}의 자리부터 {PL[p + 1]}의 자리까지 같아요" if j > 0 else ""
            lines = [L(f"둘 다 {len(sa)}자리", memo="자리 수가 같으면 높은 자리부터")] + ([L(same)] if same else []) + \
                    [L(f"{PL[p]}의 자리: {sa[j]}, {sb[j]}", memo="처음으로 다른 자리"), L(f"{com(big_)}이 더 커요" if _has_b(str(big_)) else f"{com(big_)}가 더 커요")]
            plan = "자리 수가 같으면 가장 높은 자리부터 차례로"
        q = f"두 수 {com(a)}{'과' if _has_b(str(a)) else '와'} {com(b)} 중에서 더 큰 수는 무엇인가요?"
        f = Fig()
        nd = max(len(sa), len(sb))
        place_table(f, a, at="q", nd=nd, y=120)
        place_table(f, b, at="q", nd=nd, y=360)
        if len(sa) == len(sb):
            x0, cw = 330 - min(118, 600 / nd) * nd / 2, min(118, 600 / nd)
            f.rect(x0 + cw * j + 3, 123, cw - 6, 158, c="gold", sw=5, rx=8, at=len(lines) - 2)
            f.rect(x0 + cw * j + 3, 363, cw - 6, 158, c="gold", sw=5, rx=8, at=len(lines) - 2)
        S.add(5, q, com(big_), plan, lines, f.out(), omr="ex", key=f"{min(a, b)}|{max(a, b)}")
    fill(S, 5, 20, g5)
    return S


# ══════════ 시각과 시간 ══════════
EVENTS = ["아침에 일어난", "학교에 도착한", "점심을 먹기 시작한", "숙제를 시작한", "피아노 학원에 간", "놀이터에 나간", "저녁을 먹은", "잠자리에 든", "책을 읽기 시작한", "축구를 시작한"]

def time():
    S = Set("time", "시각과 시간 — 시계 읽기에서 시간 계산까지", "시각과 시간",
            {1: "몇 시 · 몇 시 30분", 2: "몇 시 몇 분", 3: "시각 + 시간", 4: "걸린 시간", 5: "분과 초"},
            pp=8,
            tips={1: "짧은바늘은 ‘시’, 긴바늘은 ‘분’. 긴바늘이 12면 정각, 6이면 30분",
                  2: "긴바늘이 가리키는 숫자 × 5 = 분 · 작은 눈금 한 칸은 1분",
                  3: "분끼리 더해 60분이 넘으면 1시간으로 올려요",
                  4: "정각까지 · 정각에서 정각까지 · 정각부터 끝까지 — 끊어 세면 쉬워요",
                  5: "1분 = 60초. 초끼리 더해 60초가 넘으면 1분으로, 모자라면 1분을 60초로 바꿔 와요"},
            note="시각은 ‘한 순간’, 시간은 ‘두 시각 사이의 길이’예요. 시간 띠를 정각마다 끊어 그려 보게 하면 받아올림 · 받아내림 없이도 걸린 시간을 셀 수 있어요.")
    R = rng(316)
    used = set()

    def who():
        for _ in range(50):
            n, e = R.choice(PEOPLE), R.choice(EVENTS)
            if (n, e) not in used:
                used.add((n, e))
                return n, e
        return R.choice(PEOPLE), R.choice(EVENTS)

    def g1():
        k = S.count(1)
        h = R.randint(1, 12)
        m = 0 if k % 2 == 0 else 30
        n, e = who()
        f = Fig()
        clock(f, h, m)
        q = f"{iga(n)} {e} 시각이에요. 시계를 보고 시각을 읽어 보세요."
        hh = h % 12 + 1
        lines = ([L(f"짧은바늘 → {h}", memo="짧은바늘은 시"), L("긴바늘 → 12", memo="12를 가리키면 정각"), L(f"{h}시")] if m == 0 else
                 [L(f"짧은바늘 → {h}와 {hh} 사이" if not _has_b(h) else f"짧은바늘 → {h}과 {hh} 사이", memo="지난 숫자가 시"), L("긴바늘 → 6", memo="6을 가리키면 30분"), L(f"{h}시 30분")])
        S.add(1, q, f"{h}시" + (" 30분" if m else ""), "짧은바늘로 시, 긴바늘로 분", lines, f.out(), omr="ex", key=f"{h}:{m}", qfig=True)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2)
        h = R.randint(1, 12)
        m = R.randint(1, 11) * 5 if k < 12 else R.choice([x for x in range(1, 60) if x % 5])
        if m == 30:
            return
        n, e = who()
        f = Fig()
        clock(f, h, m)
        q = f"{iga(n)} {e} 시각이에요. 시계를 보고 몇 시 몇 분인지 읽어 보세요."
        hh = h % 12 + 1
        big_n = m // 5
        lines = [L(f"짧은바늘 → {h}와 {hh} 사이" if not _has_b(h) else f"짧은바늘 → {h}과 {hh} 사이", memo=f"{h}시")]
        if m % 5 == 0:
            lines += [L(f"5 × {big_n} = {m}", pre=f"긴바늘 {big_n}", memo="숫자 하나에 5분"), L(f"{h}시 {m}분")]
        else:
            r = m % 5
            lines += [L(f"5 × {big_n} = {5 * big_n}", pre=f"긴바늘 {big_n}을 지나" if _has_b(big_n) else f"긴바늘 {big_n}를 지나", memo="숫자 하나에 5분") if big_n else L("긴바늘 12를 지나", memo="0분부터"),
                      L(f"{5 * big_n} + {r} = {m}", pre=f"작은 눈금 {r}칸 더", memo="작은 눈금 한 칸 1분"), L(f"{h}시 {m}분")]
        S.add(2, q, f"{h}시 {m}분", "긴바늘이 가리키는 숫자 × 5, 작은 눈금은 1분씩", lines, f.out(), omr="ex", key=f"{h}:{m}", qfig=True)
    fill(S, 2, 20, g2)

    def g3():
        h0 = R.randint(1, 8); m0 = R.randint(1, 11) * 5
        dh = R.randint(1, 3); dm = R.randint(1, 11) * 5
        if m0 + dm < 60 and S.count(3) % 3 != 0:
            return
        if m0 + dm == 60:
            return
        t0 = h0 * 60 + m0
        t1 = t0 + dh * 60 + dm
        if t1 >= 12 * 60:
            return
        ctx = R.choice([("영화가 시작했어요", "영화가 끝나는 시각"), ("기차가 출발했어요", "기차가 도착하는 시각"), ("등산을 시작했어요", "등산을 마친 시각"), ("박물관 관람을 시작했어요", "관람을 마친 시각"), ("수영을 시작했어요", "수영을 마친 시각")])
        q = f"{hm(t0)}에 {ctx[0]}. {dur(dh * 60 + dm)}이 걸린다면 {ctx[1]}은 몇 시 몇 분인가요?"
        s = m0 + dm
        if s >= 60:
            lines = [L(f"{m0} + {dm} = {s}", pre="분끼리", memo="60분이 넘어요"), L(f"{s} − 60 = {s - 60}", pre="60분 = 1시간 올리기", memo="1시간 받아올림"),
                     L(f"{h0} + {dh} + 1 = {h0 + dh + 1}", pre="시끼리", memo="올린 1시간도"), L(f"{hm(t1)}")]
        else:
            lines = [L(f"{m0} + {dm} = {s}", pre="분끼리"), L(f"{h0} + {dh} = {h0 + dh}", pre="시끼리"), L(f"{hm(t1)}")]
        f = Fig()
        clock(f, h0, m0, cx=170, cy=290, rr=140)
        f.text(170, 480, f"시작 {hm(t0)}", z=26, b=700)
        clock(f, t1 // 60, t1 % 60, cx=490, cy=290, rr=140, at=len(lines) - 1)
        f.text(490, 480, f"끝 {hm(t1)}", z=26, b=700, at=len(lines) - 1, c="coral")
        f.text(330, 560, f"+ {dur(dh * 60 + dm)}", z=30, c="teal", b=700)
        S.add(3, q, hm(t1), "시는 시끼리, 분은 분끼리 — 60분은 1시간으로", lines, f.out(), omr="ex", key=f"{t0}+{t1}")
    fill(S, 3, 20, g3)

    def g4():
        h0 = R.randint(1, 8); m0 = R.randint(1, 11) * 5
        span = R.randint(70, 230)
        t0 = h0 * 60 + m0
        t1 = t0 + span
        if t1 % 60 == 0 or t1 >= 12 * 60:
            return
        if t1 % 5:
            t1 += 5 - t1 % 5
        span = t1 - t0
        pts = [t0] + [h * 60 for h in range(t0 // 60 + 1, (t1 - 1) // 60 + 1)] + [t1]
        if len(pts) > 6 or len(pts) < 3:
            return
        ctx = R.choice(["도서관에 있었어요", "체험 학습을 했어요", "공원에서 놀았어요", "미술관을 구경했어요", "할머니 댁에 머물렀어요", "운동을 했어요"])
        n = R.choice(PEOPLE)
        q = f"{eun(n)} {hm(t0)}부터 {hm(t1)}까지 {ctx}. 걸린 시간은 몇 시간 몇 분인가요?"
        segs = [pts[i + 1] - pts[i] for i in range(len(pts) - 1)]
        full = len(segs) - 2
        lines = [L(f"{hm(pts[0])} → {hm(pts[1])}: {dur(segs[0])}", memo="정각까지")]
        if full > 0:
            lines.append(L(f"{hm(pts[1])} → {hm(pts[-2])}: {full}시간", memo="정각에서 정각까지"))
        lines.append(L(f"{hm(pts[-2])} → {hm(pts[-1])}: {dur(segs[-1])}", memo="정각부터"))
        mm = segs[0] + segs[-1]
        if mm >= 60:
            lines.append(L(f"{segs[0]} + {segs[-1]} = {mm}", pre="분 모으기", memo="60분 = 1시간"))
            lines.append(L(f"{full} + 1 = {full + 1}", pre="시간 모으기"))
        else:
            lines.append(L(f"{segs[0]} + {segs[-1]} = {mm}", pre="분 모으기"))
        lines.append(L(f"{dur(span)}"))
        arcs = [0] + [1] * full + [2 if full > 0 else 1]
        f = Fig()
        timeline(f, t0, t1, arcs_at=arcs)
        S.add(4, q, dur(span), "정각마다 끊어 세요 — 정각까지 · 정각 사이 · 정각부터", lines, f.out(), omr="ex", key=f"{t0}-{t1}")
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        if k == 0:
            t = R.randint(65, 590)
            if t % 60 == 0:
                return
            q = f"{t}초는 몇 분 몇 초인가요?"
            m, s_ = divmod(t, 60)
            lines = [L(f"60 × {m} = {60 * m}", memo=f"{m}분 = {60 * m}초"), L(f"{t} − {60 * m} = {s_}", pre="남은 초"), L(f"{ms(t)}")]
            ans, ap = ms(t), ms(t)
            plan = "60초씩 묶어 분으로"
        elif k == 1:
            m, s_ = R.randint(1, 9), R.randint(1, 59)
            t = 60 * m + s_
            q = f"{m}분 {s_}초는 몇 초인가요?"
            lines = [L(f"{m} × 60 = {60 * m}", pre=f"{m}분", memo="1분 = 60초"), L(f"{60 * m} + {s_} = {t}"), L(f"{t}초")]
            ans, ap = f"{t}초", str(t)
            plan = "분을 초로 바꾸어 더해요"
        elif k == 2:
            a, b = R.randint(70, 400), R.randint(70, 400)
            if a % 60 + b % 60 < 60 or a % 60 == 0 or b % 60 == 0:
                return
            q = f"{ms(a)} + {ms(b)}는 몇 분 몇 초인가요?"
            sa, sb = a % 60, b % 60
            lines = [L(f"{sa} + {sb} = {sa + sb}", pre="초끼리", memo="60초가 넘어요"), L(f"{sa + sb} − 60 = {sa + sb - 60}", pre="60초 = 1분 올리기"),
                     L(f"{a // 60} + {b // 60} + 1 = {a // 60 + b // 60 + 1}", pre="분끼리"), L(f"{ms(a + b)}")]
            ans, ap = ms(a + b), ms(a + b)
            plan = "초끼리 더해 60초가 넘으면 1분으로"
        else:
            a = R.randint(200, 590); b = R.randint(65, a - 30)
            if a % 60 >= b % 60 or b % 60 == 0:
                return
            q = f"{ms(a)} − {ms(b)}는 몇 분 몇 초인가요?"
            sa, sb = a % 60, b % 60
            lines = [L(f"{sa} − {sb} 못 빼요", pre="초끼리", memo="1분 = 60초 빌려 오기"), L(f"60 + {sa} − {sb} = {60 + sa - sb}", pre="초"),
                     L(f"{a // 60} − 1 − {b // 60} = {a // 60 - 1 - b // 60}", pre="분"), L(f"{ms(a - b)}")]
            ans, ap = ms(a - b), ms(a - b)
            plan = "초끼리 못 빼면 1분을 60초로 바꿔 와요"
        S.add(5, q, ans, plan, lines, None, ap=ap, omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 길이 · 들이 · 무게 ══════════
def unit():
    S = Set("unit", "길이 · 들이 · 무게 — 단위 바꾸기와 계산", "단위",
            {1: "cm · mm, m · cm", 2: "km · m", 3: "길이의 덧셈 · 뺄셈", 4: "들이 — L · mL", 5: "무게 — kg · g"},
            pp=10,
            tips={1: "1 cm = 10 mm, 1 `m` = 100 cm — 큰 단위 하나를 작은 단위 몇 개로",
                  2: "1 km = 1000 `m`. 2 km 350 `m` = 2000 `m` + 350 `m` = 2350 `m`",
                  3: "같은 단위끼리 계산 — cm끼리 더해 100이 넘으면 1 `m`로 올려요",
                  4: "1 L = 1000 mL. mL끼리 1000이 넘으면 1 L로, 모자라면 1 L를 1000 mL로",
                  5: "1 kg = 1000 `g`, 1 `t` = 1000 kg — 계산 방법은 들이와 같아요"},
            note="단위 바꾸기는 ‘큰 단위 1 = 작은 단위 몇’을 먼저 말하게 해 주세요. 단위가 둘인 계산은 세로로 단위 칸을 나누어 쓰면 받아올림 · 받아내림이 자연스러워요.")
    R = rng(317)

    def g1():
        k = S.count(1) % 4
        f = Fig()
        if k == 0:
            c, mm = R.randint(2, 8), R.randint(1, 9)
            q = f"{c} cm {mm} mm는 몇 mm인가요?"
            ruler(f, (c + 1) * 10, c * 10 + mm)
            lines = [L(f"{c} × 10 = {c * 10}", pre=f"{c} cm", memo="1 cm = 10 mm"), L(f"{c * 10} + {mm} = {c * 10 + mm}"), L(f"{c * 10 + mm} mm")]
            ans, ap, plan, omr = f"{c * 10 + mm} mm", str(c * 10 + mm), "cm를 mm로 바꾸어 더해요", "num"
        elif k == 1:
            t = R.randint(21, 89)
            if t % 10 == 0:
                return
            q = f"{t} mm는 몇 cm 몇 mm인가요?"
            ruler(f, (t // 10 + 1) * 10, t)
            lines = [L(f"{t} = {t // 10 * 10} + {t % 10}", memo="10 mm씩 묶기"), L(f"{t // 10 * 10} mm → {t // 10} cm"), L(f"{t // 10} cm {t % 10} mm")]
            ans, ap, plan, omr = f"{t // 10} cm {t % 10} mm", f"{t // 10} cm {t % 10} mm", "10 mm마다 1 cm", "ex"
        elif k == 2:
            m, c = R.randint(1, 9), R.randint(1, 99)
            q = f"{m} `m` {c} cm는 몇 cm인가요?"
            tape(f, [(100 * m, f"{m} `m` = {100 * m} cm"), (max(c, 25), f"{c} cm")], total="? cm")
            lines = [L(f"{m} × 100 = {100 * m}", pre=f"{m} `m`", memo="1 `m` = 100 cm"), L(f"{100 * m} + {c} = {100 * m + c}"), L(f"{100 * m + c} cm")]
            ans, ap, plan, omr = f"{100 * m + c} cm", str(100 * m + c), "`m`를 cm로 바꾸어 더해요", "num"
        else:
            t = R.randint(105, 980)
            if t % 100 == 0:
                return
            q = f"{t} cm는 몇 `m` 몇 cm인가요?"
            tape(f, [(t // 100 * 100, f"{t // 100 * 100} cm = {t // 100} `m`"), (max(t % 100, 25), f"{t % 100} cm")], total=f"{t} cm")
            lines = [L(f"{t} = {t // 100 * 100} + {t % 100}", memo="100 cm씩 묶기"), L(f"{t // 100 * 100} cm → {t // 100} `m`"), L(f"{t // 100} `m` {t % 100} cm")]
            ans, ap, plan, omr = f"{t // 100} `m` {t % 100} cm", f"{t // 100} `m` {t % 100} cm", "100 cm마다 1 `m`", "ex"
        S.add(1, q, ans, plan, lines, f.out(), ap=ap, omr=omr, key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        km = R.randint(1, 9); m = R.choice([R.randint(1, 99), R.randint(100, 999)])
        t = km * 1000 + m
        f = Fig()
        tape(f, [(1000 * km, f"{km} km = {com(1000 * km)} `m`"), (max(m, 300), f"{m} `m`")], total=(f"? `m`" if k == 0 else f"{t} `m`"))
        if k == 0:
            q = f"{km} km {m} `m`는 몇 `m`인가요?"
            lines = [L(f"{km} × 1000 = {1000 * km}", pre=f"{km} km", memo="1 km = 1000 `m`"), L(f"{1000 * km} + {m} = {t}", memo="자리를 맞춰 — 0에 주의" if m < 100 else None), L(f"{t} `m`")]
            ans, ap, omr = f"{t} `m`", str(t), "num"
        else:
            q = f"{t} `m`는 몇 km 몇 `m`인가요?"
            lines = [L(f"{t} = {1000 * km} + {m}", memo="1000 `m`씩 묶기"), L(f"{1000 * km} `m` → {km} km"), L(f"{km} km {m} `m`")]
            ans, ap, omr = f"{km} km {m} `m`", f"{km} km {m} `m`", "ex"
        S.add(2, q, ans, "1 km = 1000 `m` — 천의 자리에서 끊어요", lines, f.out(), ap=ap, omr=omr, key=q)
    fill(S, 2, 20, g2)

    def two_unit(st, U, base, a, b, op):
        """a, b = (큰, 작은) — 단위 둘 세로셈"""
        A = a[0] * base + a[1]
        B = b[0] * base + b[1]
        f = Fig()
        XB, XS = unit_col(f, U, a, b, op)
        if op == "+":
            T = A + B
            s = a[1] + b[1]
            if s >= base:
                lines = [L(f"{a[1]} + {b[1]} = {s}", pre=f"{U[1]}끼리", memo=f"{base} {U[1]} = 1 {U[0]} 받아올림"),
                         L(f"{s} − {base} = {s - base}", pre=f"{U[1]} 남은 것"),
                         L(f"1 + {a[0]} + {b[0]} = {a[0] + b[0] + 1}", pre=f"{U[0]}끼리"), L(f"{T // base} {U[0]} {T % base} {U[1]}")]
                f.text(XB, 175, "1", z=34, c="red", at=0, b=700)
                f.text(XS, 490, str(s - base), z=58, at=1)
                f.text(XB, 490, str(a[0] + b[0] + 1), z=58, at=2)
            else:
                lines = [L(f"{a[1]} + {b[1]} = {s}", pre=f"{U[1]}끼리"), L(f"{a[0]} + {b[0]} = {a[0] + b[0]}", pre=f"{U[0]}끼리"), L(f"{T // base} {U[0]} {T % base} {U[1]}")]
                f.text(XS, 490, str(s), z=58, at=0)
                f.text(XB, 490, str(a[0] + b[0]), z=58, at=1)
            plan = f"{U[1]}끼리, {U[0]}끼리 — {base} {uj(U[1], '이', '가')} 넘으면 1 {uro(U[0])}"
        else:
            T = A - B
            if a[1] < b[1]:
                lines = [L(f"{a[1]} − {b[1]} 못 빼요", pre=f"{U[1]}끼리", memo=f"1 {U[0]} = {base} {U[1]} 빌려 오기"),
                         L(f"{base} + {a[1]} − {b[1]} = {base + a[1] - b[1]}", pre=f"{U[1]}"),
                         L(f"{a[0]} − 1 − {b[0]} = {a[0] - 1 - b[0]}", pre=f"{U[0]}끼리"), L(f"{T // base} {U[0]} {T % base} {U[1]}")]
                f.cross(XB, 230, s=24, at=0)
                f.text(XB + 4, 175, str(a[0] - 1), z=34, c="red", at=0, b=700, dl=200)
                f.text(XS + 6, 175, f"+{base}", z=30, c="red", at=0, b=700, dl=400)
                f.text(XS, 490, str(base + a[1] - b[1]), z=58, at=1)
                f.text(XB, 490, str(a[0] - 1 - b[0]), z=58, at=2)
            else:
                lines = [L(f"{a[1]} − {b[1]} = {a[1] - b[1]}", pre=f"{U[1]}끼리"), L(f"{a[0]} − {b[0]} = {a[0] - b[0]}", pre=f"{U[0]}끼리"), L(f"{T // base} {U[0]} {T % base} {U[1]}")]
                f.text(XS, 490, str(a[1] - b[1]), z=58, at=0)
                f.text(XB, 490, str(a[0] - b[0]), z=58, at=1)
            plan = f"{U[1]}끼리 못 빼면 1 {uj(U[0], '을', '를')} {base} {uro(U[1])} 바꿔 와요"
        ans = f"{T // base} {U[0]} {T % base} {U[1]}"
        return f, lines, ans, plan

    def g3():
        k = S.count(3)
        if k % 2 == 0:
            U, base = ("`m`", "cm"), 100
            a, b = (R.randint(1, 8), R.randint(10, 95)), (R.randint(1, 6), R.randint(10, 95))
        else:
            U, base = ("km", "`m`"), 1000
            a, b = (R.randint(1, 8), R.randint(100, 950)), (R.randint(1, 6), R.randint(100, 950))
        op = "+" if k % 4 < 2 else "−"
        if op == "−" and a[0] * base + a[1] <= b[0] * base + b[1] + base:
            return
        if (op == "+" and a[1] + b[1] < base and R.random() < 0.7) or (op == "−" and a[1] >= b[1] and R.random() < 0.7):
            return
        f, lines, ans, plan = two_unit(3, U, base, a, b, op)
        q = f"{a[0]} {U[0]} {a[1]} {U[1]} {op} {b[0]} {U[0]} {b[1]} {uj(U[1], '은', '는')} 몇 {U[0]} 몇 {U[1]}인가요?"
        S.add(3, q, ans, plan, lines, f.out(), ap=ans, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def conv(st, U, base, big_unit_max):
        k = S.count(st)
        a = R.randint(1, big_unit_max); b = R.randint(50, base - 50)
        t = a * base + b
        if k % 2 == 0:
            q = f"{a} {U[0]} {b} {uj(U[1], '은', '는')} 몇 {U[1]}인가요?"
            lines = [L(f"{a} × {base} = {a * base}", pre=f"{a} {U[0]}", memo=f"1 {U[0]} = {base} {U[1]}"), L(f"{a * base} + {b} = {t}"), L(f"{t} {U[1]}")]
            return q, f"{t} {U[1]}", str(t), lines, "num"
        q = f"{t} {uj(U[1], '은', '는')} 몇 {U[0]} 몇 {U[1]}인가요?"
        lines = [L(f"{t} = {a * base} + {b}", memo=f"{base} {U[1]}씩 묶기"), L(f"{a * base} {U[1]} → {a} {U[0]}"), L(f"{a} {U[0]} {b} {U[1]}")]
        return q, f"{a} {U[0]} {b} {U[1]}", f"{a} {U[0]} {b} {U[1]}", lines, "ex"

    def g45(st, U, base, things):
        k = S.count(st)
        if k < 6:
            q, ans, ap, lines, omr = conv(st, U, base, 9)
            f = Fig()
            S.add(st, q, ans, f"1 {uj(U[0], '은', '는')} {base} {U[1]} — {base} {U[1]}씩 묶거나 풀어요", lines, None, ap=ap, omr=omr, key=q)
            return
        op = "+" if k % 2 == 0 else "−"
        a, b = (R.randint(1, 7), R.randint(100, 900)), (R.randint(1, 5), R.randint(100, 900))
        if op == "−" and a[0] * base + a[1] <= b[0] * base + b[1] + 100:
            return
        if (op == "+" and a[1] + b[1] < base) or (op == "−" and a[1] >= b[1]):
            if R.random() < 0.75:
                return
        f, lines, ans, plan = two_unit(st, U, base, a, b, op)
        t1, t2 = R.sample(things, 2)
        if op == "+":
            q = f"{t1}에 {a[0]} {U[0]} {a[1]} {U[1]}, {t2}에 {b[0]} {U[0]} {b[1]} {uj(U[1], '이', '가')} 있어요. 모두 몇 {U[0]} 몇 {U[1]}인가요?" if st == 4 else \
                f"{t1}의 무게는 {a[0]} {U[0]} {a[1]} {U[1]}, {t2}의 무게는 {b[0]} {U[0]} {b[1]} {uj(U[1], '이에요', '예요')}. 두 무게의 합은 몇 {U[0]} 몇 {U[1]}인가요?"
        else:
            q = f"{t1}에 {a[0]} {U[0]} {a[1]} {uj(U[1], '이', '가')} 있었는데 {b[0]} {U[0]} {b[1]} {uj(U[1], '을', '를')} 썼어요. 남은 양은 몇 {U[0]} 몇 {U[1]}인가요?" if st == 4 else \
                f"{t1}의 무게는 {a[0]} {U[0]} {a[1]} {U[1]}, {t2}의 무게는 {b[0]} {U[0]} {b[1]} {uj(U[1], '이에요', '예요')}. {iga(t1)} 몇 {U[0]} 몇 {U[1]} 더 무겁나요?"
        S.add(st, q, ans, plan, lines, f.out(), ap=ans, omr="ex", key=q)

    fill(S, 4, 20, lambda: g45(4, ("L", "mL"), 1000, ["물통", "주전자", "어항", "냄비", "물병", "양동이"]))
    fill(S, 5, 20, lambda: g45(5, ("kg", "`g`"), 1000, ["수박", "호박", "책가방", "강아지", "쌀 봉지", "상자"]))
    return S
