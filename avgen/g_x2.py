# 초2 채우기 — 세 자리 수 · 네 자리 수 · 길이 재기 · 여러 가지 도형 · 분류하기와 표 · 그래프 · 곱셈 · 규칙 찾기
import math
from core import *
from core import _has_batchim
from fig import Fig, rod
from kit import *

PN = {1000: "천", 100: "백", 10: "십", 1: "일"}
PNAME = ["천", "백", "십", "일"]

def bat(v):
    return _has_batchim(str(v))

def ic(ch, n=1):
    return "".join(f"⟪{ch}⟫" for _ in range(n))

def blocks(f, h, t, o, at="q"):
    """수 모형 — 백 모형(판) · 십 모형(막대) · 일 모형(낱개)"""
    x = 40
    for i in range(h):
        f.grid(x, 170, 9, 9, 10, 10, c="ink", sw=1.2, f="sky", fo=0.3, at=at)
        x += 106
    for i in range(t):
        rod(f, 40 + i * 36, 320, h=230, w=24, at=at)
    x1 = 40 + t * 36 + 30
    for j in range(o):
        f.circ(x1 + (j % 3) * 40 + 14, 340 + (j // 3) * 44, 14, c="ink", sw=2.5, f="gold", fo=0.5, at=at)


# ══════════ 세 자리 수 ══════════
def num1000():
    S = Set("num1000", "세 자리 수 — 백 · 십 · 일의 자리", "세 자리 수",
            {1: "모형으로 수 만들기", 2: "자릿값", 3: "뛰어 세기", 4: "크기 비교", 5: "수 카드로 만들기"},
            pp=10,
            tips={1: "100이 □개, 10이 □개, 1이 □개 → 백 · 십 · 일의 자리에 차례로",
                  2: "같은 숫자도 자리에 따라 나타내는 값이 달라요 — 3이 십의 자리면 30",
                  3: "100씩 뛰면 백의 자리, 10씩 뛰면 십의 자리, 1씩 뛰면 일의 자리가 1씩 커져요",
                  4: "백의 자리부터 견주고, 같으면 십의 자리, 그다음 일의 자리",
                  5: "가장 큰 수는 큰 숫자부터, 가장 작은 수는 작은 숫자부터 — 0은 맨 앞에 못 와요"},
            note="자릿값은 ‘숫자가 어느 자리에 있느냐’예요. 모형을 직접 세어 수로 쓰게 한 뒤 자릿값 표로 옮기게 해 주세요.")
    R = rng(5201)

    def g1():
        h, t, o = R.randint(1, 4), R.randint(0, 9), R.randint(0, 9)
        n = 100 * h + 10 * t + o
        q = f"100이 {h}개, 10이 {t}개, 1이 {o}개인 수는 얼마인가요?"
        f = Fig()
        blocks(f, h, t, o)
        lines = [L(f"{100 * h} + {10 * t} + {o} = {n}", memo="백 · 십 · 일의 자리에 차례로")]
        S.add(1, q, str(n), "자리마다 개수를 차례로 쓰기", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        n = R.randint(102, 987)
        ds = str(n)
        i = R.randint(0, 2)
        d = int(ds[i])
        if d == 0 or ds.count(ds[i]) > 1:
            return
        p = 10 ** (2 - i)
        v = d * p
        q = f"{n}에서 숫자 {eun(d)} 얼마를 나타내나요?"
        lines = [L(f"{eun(d)} {PN[p]}의 자리 숫자"), L(f"{d} × {p} = {v}")]
        f = Fig()
        place_table(f, n, hl=2 - i, hl_at=0)
        S.add(2, q, str(v), "숫자가 있는 자리를 먼저", lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        step = R.choice([1, 10, 100])
        a = R.randint(100, 600)
        k = R.randint(3, 4)
        a2 = a + step * k
        if a2 > 999:
            return
        q = f"{a}부터 {step}씩 {k}번 뛰어 세면 얼마인가요?"
        seq = [a + step * i for i in range(k + 1)]
        lines = [L(" → ".join(map(str, seq)), memo=f"{PN[step]}의 자리가 1씩 커져요")]
        f = Fig()
        jump_line(f, seq, at="q", jumps_at=[0] * k, jlab=f"+{step}")
        S.add(3, q, str(a2), "뛰어 세는 자리의 숫자만 1씩", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.randint(100, 999)
        b = a + R.choice([R.randint(1, 9), R.randint(10, 90), R.randint(100, 300)]) * R.choice([1, -1])
        if not (100 <= b <= 999) or a == b:
            return
        big = R.random() < 0.5
        q = f"{wa(a)} {b} 중에서 더 {'큰' if big else '작은'} 수는 무엇인가요?"
        sa, sb = str(a), str(b)
        i = next(k for k in range(3) if sa[k] != sb[k])
        ans = max(a, b) if big else min(a, b)
        lines = [L(f"{PNAME[i + 1]}의 자리에서 처음 달라요: {wa(sa[i])} {sb[i]}"), L(f"더 {'큰' if big else '작은'} 수 {ans}")]
        S.add(4, q, str(ans), "높은 자리부터 견주기", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        ds = R.sample(range(0, 10), 3)
        big = R.random() < 0.5
        if big:
            v = int("".join(map(str, sorted(ds, reverse=True))))
        else:
            s = sorted(ds)
            if s[0] == 0:
                s = [s[1], 0, s[2]]
            v = int("".join(map(str, s)))
        cards = ", ".join(map(str, ds[:-1])) + ", " + eul(ds[-1])
        q = f"숫자 카드 {cards} 한 번씩 써서 만들 수 있는 가장 {'큰' if big else '작은'} 세 자리 수는 무엇인가요?"
        lines = [L(f"{'큰' if big else '작은'} 숫자부터 백 · 십 · 일의 자리에" + (" — 0은 백의 자리에 못 와요" if (not big and 0 in ds) else "")), L(str(v))]
        S.add(5, q, str(v), "높은 자리에 큰(작은) 숫자부터", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 네 자리 수 ══════════
def num10000():
    S = Set("num10000", "네 자리 수 — 천의 자리까지", "네 자리 수",
            {1: "1000이 □개 …", 2: "자릿값", 3: "뛰어 세기", 4: "크기 비교", 5: "수 카드로 만들기"},
            pp=10,
            tips={1: "1000이 □개, 100이 □개, 10이 □개, 1이 □개 → 천 · 백 · 십 · 일의 자리",
                  2: "천의 자리 숫자 5는 5000을 나타내요",
                  3: "1000씩 뛰면 천의 자리가 1씩 커져요",
                  4: "천의 자리부터 차례로 견주기",
                  5: "높은 자리에 큰 숫자 — 0은 맨 앞에 못 와요"},
            note="세 자리 수에서 한 자리가 늘었을 뿐이에요. 자릿값 표에 천의 자리 칸을 더해 같은 방법으로 읽고 쓰게 해 주세요.")
    R = rng(5202)

    def g1():
        th, h, t, o = R.randint(1, 9), R.randint(0, 9), R.randint(0, 9), R.randint(0, 9)
        n = 1000 * th + 100 * h + 10 * t + o
        q = f"1000이 {th}개, 100이 {h}개, 10이 {t}개, 1이 {o}개인 수는 얼마인가요?"
        lines = [L(f"{1000 * th} + {100 * h} + {10 * t} + {o} = {n}", memo="천 · 백 · 십 · 일의 자리에 차례로")]
        f = Fig()
        place_table(f, n, at=0)
        S.add(1, q, str(n), "자리마다 개수를 차례로", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        n = R.randint(1002, 9987)
        ds = str(n)
        i = R.randint(0, 3)
        d = int(ds[i])
        if d == 0 or ds.count(ds[i]) > 1:
            return
        p = 10 ** (3 - i)
        v = d * p
        q = f"{n}에서 숫자 {eun(d)} 얼마를 나타내나요?"
        lines = [L(f"{eun(d)} {PNAME[i]}의 자리 숫자"), L(f"{d} × {p} = {v}")]
        f = Fig()
        place_table(f, n, hl=3 - i, hl_at=0)
        S.add(2, q, str(v), "숫자가 있는 자리를 먼저", lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        step = R.choice([1000, 100, 10])
        a = R.randint(1000, 5000)
        k = R.randint(3, 4)
        a2 = a + step * k
        if a2 > 9999:
            return
        q = f"{a}부터 {step}씩 {k}번 뛰어 세면 얼마인가요?"
        seq = [a + step * i for i in range(k + 1)]
        lines = [L(" → ".join(map(str, seq)), memo=f"{PN[step]}의 자리가 1씩 커져요")]
        f = Fig()
        jump_line(f, seq, at="q", jumps_at=[0] * k, jlab=f"+{step}")
        S.add(3, q, str(a2), "뛰어 세는 자리의 숫자만 1씩", lines, f.out(), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a = R.randint(1000, 9999)
        b = a + R.choice([R.randint(1, 9), R.randint(10, 90), R.randint(100, 900), R.randint(1000, 3000)]) * R.choice([1, -1])
        if not (1000 <= b <= 9999) or a == b:
            return
        big = R.random() < 0.5
        q = f"{wa(a)} {b} 중에서 더 {'큰' if big else '작은'} 수는 무엇인가요?"
        sa, sb = str(a), str(b)
        i = next(k for k in range(4) if sa[k] != sb[k])
        ans = max(a, b) if big else min(a, b)
        lines = [L(f"{PNAME[i]}의 자리에서 처음 달라요: {wa(sa[i])} {sb[i]}"), L(f"더 {'큰' if big else '작은'} 수 {ans}")]
        S.add(4, q, str(ans), "높은 자리부터 견주기", lines, None, key=q)
    fill(S, 4, 20, g4)

    def g5():
        ds = R.sample(range(0, 10), 4)
        big = R.random() < 0.5
        if big:
            v = int("".join(map(str, sorted(ds, reverse=True))))
        else:
            s = sorted(ds)
            if s[0] == 0:
                s = [s[1], 0] + s[2:]
            v = int("".join(map(str, s)))
        cards = ", ".join(map(str, ds[:-1])) + ", " + eul(ds[-1])
        q = f"숫자 카드 {cards} 한 번씩 써서 만들 수 있는 가장 {'큰' if big else '작은'} 네 자리 수는 무엇인가요?"
        lines = [L(f"{'큰' if big else '작은'} 숫자부터 천 · 백 · 십 · 일의 자리에" + (" — 0은 천의 자리에 못 와요" if (not big and 0 in ds) else "")), L(str(v))]
        S.add(5, q, str(v), "높은 자리에 큰(작은) 숫자부터", lines, None, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 길이 재기 ══════════
THINGS = ["연필", "지우개", "크레파스", "풀", "가위", "머리핀", "숟가락", "빨대", "색연필", "붓", "리본", "못"]
UNITS = [("클립", 3), ("지우개", 4), ("성냥개비", 5), ("풀", 8), ("크레파스", 7), ("볼펜", 14), ("색 테이프 조각", 6)]
def len2():
    S = Set("len2", "길이 재기 — 미터와 센티미터", "길이 재기",
            {1: "자로 길이 재기", 2: "단위길이로 재기", 3: "m와 cm", 4: "길이의 합", 5: "길이의 차"},
            pp=10,
            tips={1: "한끝을 0에 맞추면 다른 끝의 눈금이 길이 — 0이 아니면 (끝 눈금) − (시작 눈금)",
                  2: "단위길이 × 잰 횟수",
                  3: "1 m = 100 cm — 1 m 35 cm = 135 cm",
                  4: "m는 m끼리, cm는 cm끼리 — 100 cm가 넘으면 1 m로",
                  5: "cm끼리 뺄 수 없으면 1 m를 100 cm로 바꿔요"},
            note="길이를 잴 때는 ‘시작점을 0에 맞추기’와 ‘1 cm가 몇 번인가’를 같이 말하게 해 주세요.")
    R = rng(5203)

    def rul(f, s, e, at="q"):
        x0, dx = 70, 50
        f.rect(x0 - 24, 330, 10 * dx + 48, 80, c="ink", sw=3, f="gold", fo=0.15, rx=6, at=at)
        for i in range(0, 11):
            f.line(x0 + i * dx, 330, x0 + i * dx, 360, c="ink", w=3, at=at)
            f.text(x0 + i * dx, 395, str(i), z=24, at=at)
        f.rect(x0 + s * dx, 270, (e - s) * dx, 46, c="ink", sw=3, f="sky", fo=0.5, rx=10, at=at)
        f.line(x0 + s * dx, 250, x0 + s * dx, 330, c="ink", w=2.5, d=True, at=0)
        f.line(x0 + e * dx, 250, x0 + e * dx, 330, c="ink", w=2.5, d=True, at=0)

    def g1():
        th = R.choice(THINGS)
        s = R.choice([0, 0, 1, 2, 3])
        e = R.randint(s + 2, 10)
        q = f"{th}의 한끝을 자의 눈금 {s}에 맞추었더니 다른 끝이 눈금 {e}에 닿았어요. {th}의 길이는 몇 cm인가요?"
        f = Fig()
        rul(f, s, e)
        lines = [L(f"{e} − {s} = {e - s}" if s else f"0에서 {e}까지 — 1 cm가 {e}번", memo="1 cm가 몇 번"), L(f"{e - s} cm")]
        S.add(1, q, f"{e - s} cm", "(끝 눈금) − (시작 눈금)", lines, f.out(), ap=str(e - s), key=q)
    fill(S, 1, 20, g1)

    def g2():
        nm, l = R.choice(UNITS)
        k = R.randint(2, 8)
        q = f"길이가 {l} cm인 {ro(nm)} {k}번 잰 길이는 몇 cm인가요?"
        lines = [L(f"{l} cm가 {k}번"), L(f"{l} × {k} = {l * k}")]
        S.add(2, q, f"{l * k} cm", "단위길이 × 잰 횟수", lines, None, ap=str(l * k), key=q)
    fill(S, 2, 20, g2)

    def g3():
        m, c = R.randint(1, 9), R.randint(1, 99)
        if R.random() < 0.5:
            q = f"{m} m {c} cm는 몇 cm인가요?"
            lines = [L(f"{m} m는 {100 * m} cm", memo="1 m = 100 cm"), L(f"{100 * m} + {c} = {100 * m + c}")]
            S.add(3, q, f"{100 * m + c} cm", "1 m는 100 cm", lines, None, ap=str(100 * m + c), key=q)
        else:
            n = 100 * m + c
            q = f"{n} cm는 몇 m 몇 cm인가요?"
            lines = [L(f"{n} = {100 * m} + {c}"), L(f"{100 * m} cm는 {m} m", memo="100 cm가 1 m"), L(f"{m} m {c} cm")]
            S.add(3, q, f"{m} m {c} cm", "100 cm씩 묶으면 m", lines, None, ap=f"{m} m {c} cm", omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        m1, c1, m2, c2 = R.randint(1, 5), R.randint(5, 95), R.randint(1, 4), R.randint(5, 95)
        cs = c1 + c2
        up = cs >= 100
        mm = m1 + m2 + (1 if up else 0)
        cr = cs % 100
        q = f"{m1} m {c1} cm + {m2} m {c2} cm는 몇 m 몇 cm인가요?"
        lines = [L(f"cm끼리 {c1} + {c2} = {cs}", memo="100 cm가 넘으면 1 m로" if up else "cm끼리")]
        if up:
            lines.append(L(f"{cs} cm는 1 m {cr} cm"))
        lines += [L(f"m끼리 {m1} + {m2}" + (" + 1" if up else "") + f" = {mm}"), L(f"{mm} m {cr} cm")]
        S.add(4, q, f"{mm} m {cr} cm", "m는 m끼리, cm는 cm끼리", lines, None, ap=f"{mm} m {cr} cm", omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        m1, c1 = R.randint(3, 9), R.randint(5, 95)
        m2, c2 = R.randint(1, m1 - 1), R.randint(5, 95)
        borrow = c1 < c2
        cr = c1 + (100 if borrow else 0) - c2
        mm = m1 - m2 - (1 if borrow else 0)
        q = f"{m1} m {c1} cm − {m2} m {c2} cm는 몇 m 몇 cm인가요?"
        lines = ([L(f"{c1}에서 {c2}를 뺄 수 없어요 → 1 m를 100 cm로".replace(f"{c2}를", eul(c2)), memo="받아내림")] if borrow else []) + \
                [L(f"cm끼리 {c1 + (100 if borrow else 0)} − {c2} = {cr}"), L(f"m끼리 {m1}" + (" − 1" if borrow else "") + f" − {m2} = {mm}"), L(f"{mm} m {cr} cm")]
        S.add(5, q, f"{mm} m {cr} cm", "cm끼리 뺄 수 없으면 1 m를 100 cm로", lines, None, ap=f"{mm} m {cr} cm", omr="ex", key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 여러 가지 도형 ══════════
POLY = {3: "삼각형", 4: "사각형", 5: "오각형", 6: "육각형"}
def fig2():
    S = Set("fig2", "여러 가지 도형 — 삼각형 · 사각형 · 원 · 쌓기나무", "여러 가지 도형",
            {1: "변과 꼭짓점", 2: "도형의 이름", 3: "꼭짓점 · 변의 수 모으기", 4: "쌓기나무 세기", 5: "성냥개비로 도형 만들기"},
            pp=10,
            tips={1: "곧은 선이 변, 두 변이 만나는 점이 꼭짓점 — □각형은 변도 꼭짓점도 □개",
                  2: "변(꼭짓점)이 3개면 삼각형, 4개면 사각형, 5개면 오각형, 6개면 육각형",
                  3: "원은 변도 꼭짓점도 없어요",
                  4: "줄마다 나누어 세어 더해요",
                  5: "따로따로 만들면 도형마다 변의 수만큼 필요해요"},
            note="도형의 이름을 ‘변의 수’로 붙인다는 것을 먼저 잡게 해 주세요. 원은 곧은 선이 없어서 변도 꼭짓점도 없어요.")
    R = rng(5204)

    def ngon(f, n, cx=330, cy=340, r=180, at="q", lab_at=None):
        rot = R.uniform(-0.3, 0.3)
        pts = []
        for i in range(n):
            rr = r * (0.85 + 0.15 * R.random())
            a = 2 * math.pi * i / n - math.pi / 2 + rot
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
        f.poly(pts, c="ink", w=4, f="sky", fo=0.25, at=at)
        if lab_at is not None:
            for i, (x, y) in enumerate(pts):
                f.dot(x, y, r=9, f="ink", at=lab_at, dl=i * 120)
        return pts

    def g1():
        n, m = R.sample(list(POLY), 2)
        t = R.randrange(4)
        f = Fig()
        if t == 0:
            q = f"{POLY[n]}의 변과 꼭짓점은 각각 몇 개인가요?"
            ngon(f, n, lab_at=0)
            lines = [L(f"{POLY[n]} → 변 {n}개", memo="곧은 선"), L(f"꼭짓점 {n}개", memo="두 변이 만나는 점")]
            S.add(1, q, f"변 {n}개, 꼭짓점 {n}개", "□각형은 변도 꼭짓점도 □개", lines, f.out(), ap=f"{n}, {n}", omr="ex", key=q)
            return
        ngon(f, n, cx=175, cy=340, r=125, lab_at=0)
        ngon(f, m, cx=490, cy=340, r=125, lab_at=0)
        w1, w2 = R.choice(["변", "꼭짓점"]), R.choice(["변", "꼭짓점"])
        if t in (1, 2):
            q = f"{POLY[n]}의 {w1}의 수와 {POLY[m]}의 {w2}의 수의 합은 몇 개인가요?"
            lines = [L(f"{POLY[n]}의 {w1} {n}개, {POLY[m]}의 {w2} {m}개"), L(f"{n} + {m} = {n + m}")]
            S.add(1, q, f"{n + m}개", "□각형은 변도 꼭짓점도 □개", lines, f.out(), ap=str(n + m), key=q)
        else:
            a, b = max(n, m), min(n, m)
            q = f"{wa(POLY[a])} {POLY[b]}의 {w1}의 수의 차는 몇 개인가요?"
            lines = [L(f"{POLY[a]} {a}개, {POLY[b]} {b}개"), L(f"{a} − {b} = {a - b}")]
            S.add(1, q, f"{a - b}개", "수끼리 빼기", lines, f.out(), ap=str(a - b), key=q)
    fill(S, 1, 20, g1)

    SH = {"△": "삼각형", "□": "사각형", "○": "원"}
    def g2():
        if R.random() < 0.45:
            n = R.choice(list(POLY))
            what = R.choice(["변", "꼭짓점"])
            extra = R.choice(["", " 곧은 선으로만 둘러싸인", " 닫힌"])
            q = f"{what}이 {n}개인{extra} 도형의 이름은 무엇인가요?"
            lines = [L(f"{what} {n}개 → {POLY[n]}")]
            S.add(2, q, POLY[n], "변(꼭짓점)의 수로 이름", lines, None, omr="ex", key=q)
        else:
            row = [R.choice(list(SH)) for _ in range(R.randint(6, 9))]
            t = R.choice(list(SH))
            cnt = row.count(t)
            if not cnt:
                return
            q = f"{''.join(ic(x) for x in row)} 중에서 {eun(SH[t])} 몇 개인가요?"
            lines = [L(f"{SH[t]}만 골라 표시하며 세기"), L(f"{cnt}개")]
            S.add(2, q, f"{cnt}개", "하나씩 표시하며 세기", lines, None, ap=str(cnt), key=q)
    fill(S, 2, 20, g2)

    def g3():
        a, b, c = R.randint(1, 5), R.randint(1, 5), R.randint(1, 3)
        what = R.choice(["꼭짓점", "변"])
        q = f"삼각형 {a}개, 사각형 {b}개, 원 {c}개가 있어요. {what}은 모두 몇 개인가요?"
        lines = [L(f"삼각형은 3개, 사각형은 4개, 원은 0개", memo=f"도형 하나의 {what} 수"), L(f"3 × {a} + 4 × {b} + 0 × {c} = {3 * a + 4 * b}")]
        S.add(3, q, f"{3 * a + 4 * b}개", "원은 변도 꼭짓점도 0개", lines, None, ap=str(3 * a + 4 * b), key=q)
    fill(S, 3, 20, g3)

    def cubes(f, hs, at="q"):
        s, dx, dy = 70, 30, 22
        x0 = 330 - s * len(hs) / 2 - dx / 2
        for i, h in enumerate(hs):
            for j in range(h):
                x, y = x0 + i * s, 560 - (j + 1) * s
                for pts, fo in (([(x, y), (x + s, y), (x + s, y + s), (x, y + s)], 0.45), ([(x, y), (x + dx, y - dy), (x + s + dx, y - dy), (x + s, y)], 0.2),
                                ([(x + s, y), (x + s + dx, y - dy), (x + s + dx, y + s - dy), (x + s, y + s)], 0.7)):
                    f.poly(pts, c="ink", w=0.1, f="paper", fo=1, at=at)
                    f.poly(pts, c="ink", w=2.5, f="gold", fo=fo, at=at)

    def g4():
        k = R.randint(2, 4)
        hs = [R.randint(1, 4) for _ in range(k)]
        q = f"쌓기나무를 한 줄로 놓고 왼쪽부터 {', '.join(f'{h}층' for h in hs)}으로 쌓았어요. 쌓기나무는 모두 몇 개인가요?"
        f = Fig()
        cubes(f, hs)
        lines = [L("줄마다 층 수만큼"), L(f"{' + '.join(map(str, hs))} = {sum(hs)}")]
        S.add(4, q, f"{sum(hs)}개", "줄마다 나누어 세어 더하기", lines, f.out(), ap=str(sum(hs)), key=q)
    fill(S, 4, 20, g4)

    def g5():
        if R.random() < 0.5:
            n = R.choice([3, 4, 5, 6])
            k = R.randint(2, 7)
            q = f"성냥개비로 {POLY[n]} {k}개를 따로따로 만들려고 해요. 성냥개비는 모두 몇 개 필요한가요?"
            lines = [L(f"{POLY[n]} 하나에 {n}개", memo="변의 수"), L(f"{n} × {k} = {n * k}")]
            S.add(5, q, f"{n * k}개", "도형 하나에 변의 수만큼", lines, None, ap=str(n * k), key=q)
        else:
            a, b = R.randint(1, 5), R.randint(1, 5)
            n, m = R.sample([3, 4, 5, 6], 2)
            q = f"성냥개비로 {POLY[n]} {a}개와 {POLY[m]} {b}개를 따로따로 만들려고 해요. 성냥개비는 모두 몇 개 필요한가요?"
            lines = [L(f"{POLY[n]} 하나에 {n}개, {POLY[m]} 하나에 {m}개", memo="변의 수"), L(f"{n} × {a} + {m} × {b} = {n * a + m * b}")]
            S.add(5, q, f"{n * a + m * b}개", "도형마다 변의 수만큼", lines, None, ap=str(n * a + m * b), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 분류하기 · 표와 그래프 ══════════
CATS = {
    "탈것": {"땅에서 다니는 것": ["자동차", "버스", "기차", "자전거", "트럭"], "하늘을 나는 것": ["비행기", "헬리콥터", "열기구"], "물에서 다니는 것": ["배", "요트", "잠수함"]},
    "동물": {"다리가 2개인 동물": ["닭", "오리", "참새", "타조"], "다리가 4개인 동물": ["강아지", "고양이", "소", "말", "토끼"], "다리가 없는 동물": ["뱀", "금붕어", "지렁이"]},
    "먹을거리": {"과일": ["사과", "배", "귤", "포도", "딸기"], "채소": ["당근", "오이", "배추", "무", "가지"]},
}
TOPIC = {"과일": ["사과", "배", "귤", "포도", "딸기"], "계절": ["봄", "여름", "가을", "겨울"], "운동": ["축구", "줄넘기", "수영", "피구", "농구"],
         "색깔": ["빨강", "노랑", "파랑", "초록"], "동물": ["강아지", "고양이", "토끼", "햄스터"], "간식": ["떡볶이", "김밥", "만두", "과자"]}
ICN = {"○": "동그라미", "△": "세모", "□": "네모"}
def sort2():
    S = Set("sort2", "분류하기 · 표와 그래프", "분류·표·그래프",
            {1: "기준에 따라 분류하기", 2: "분류해서 세기", 3: "표 만들기 · 합계", 4: "그래프 읽기", 5: "표와 그래프로 답하기"},
            pp=8,
            tips={1: "누가 분류해도 같은 결과가 나오는 기준(다리 수 · 사는 곳 …)",
                  2: "분류한 뒤 칸마다 세어요 — 센 것은 표시",
                  3: "표의 합계는 칸의 수를 모두 더한 것",
                  4: "○의 수가 많을수록 많이 좋아해요 — 가장 높은 줄",
                  5: "합계에서 아는 칸을 빼면 모르는 칸"},
            note="분류의 기준은 ‘누가 해도 같게’여야 해요. ‘예쁜 것 · 미운 것’ 같은 기준이 왜 안 되는지 먼저 이야기해 보게 해 주세요.")
    R = rng(5205)

    def g1():
        cat = R.choice(list(CATS))
        grp = CATS[cat]
        items = []
        for g, xs in grp.items():
            items += [(x, g) for x in R.sample(xs, R.randint(1, min(len(xs), 3)))]
        R.shuffle(items)
        if len(items) < 4:
            return
        g = R.choice(list(grp))
        cnt = sum(1 for _, gg in items if gg == g)
        q = f"{', '.join(x for x, _ in items)} 중에서 {eun(g)} 몇 가지인가요?"
        lines = [L(" · ".join(x for x, gg in items if gg == g), memo=g), L(f"{cnt}가지")]
        S.add(1, q, f"{cnt}가지", "기준에 맞는 것만 고르기", lines, None, ap=str(cnt), key=q)
    fill(S, 1, 20, g1)

    def g2():
        row = [R.choice(list(ICN)) for _ in range(R.randint(8, 12))]
        cnt = {k: row.count(k) for k in ICN}
        if len(set(cnt.values())) < 3:
            return
        many = R.random() < 0.5
        k = max(cnt, key=cnt.get) if many else min(cnt, key=cnt.get)
        q = f"{''.join(ic(x) for x in row)} — 모양에 따라 분류했을 때 가장 {'많은' if many else '적은'} 모양은 무엇인가요?"
        lines = [L(f"동그라미 {cnt['○']}개, 세모 {cnt['△']}개, 네모 {cnt['□']}개"), L(f"가장 {'많은' if many else '적은'} 모양 → {ICN[k]}")]
        S.add(2, q, ICN[k], "모양마다 세어 견주기", lines, None, omr="ex", key=q)
    fill(S, 2, 20, g2)

    def table(f, names, vals, hide=None, at="q"):
        heads = ["항목"] + names + ["합계"]
        tot = sum(vals)
        row = ["학생 수"] + [("?" if i == hide else str(v)) for i, v in enumerate(vals)] + ["?" if hide == -1 else str(tot)]
        n = len(heads)
        cw = min(112, 600 / (n + 0.4))
        w0 = cw * 1.4
        x = 330 - (w0 + cw * (n - 1)) / 2
        for j in range(n):
            w_ = w0 if j == 0 else cw
            f.rect(x, 220, w_, 86, c="ink", sw=2.5, f="gold" if j == 0 else None, fo=0.15 if j == 0 else None, at=at)
            f.rect(x, 306, w_, 96, c="ink", sw=2.5, at=at)
            f.text(x + w_ / 2, 273, heads[j], z=26 if j == 0 else 27, b=700, at=at)
            f.text(x + w_ / 2, 368, row[j], z=26 if j == 0 else 38, b=700 if j else 600, at=at)
            x += w_

    def g3():
        tp = R.choice(list(TOPIC))
        names = R.sample(TOPIC[tp], R.randint(3, 4))
        vals = [R.randint(2, 9) for _ in names]
        q = f"좋아하는 {eul(tp)} 조사했더니 " + ", ".join(f"{n} {v}명" for n, v in zip(names, vals)) + "이었어요. 표의 합계는 몇 명인가요?"
        f = Fig()
        table(f, names, vals, hide=-1)
        lines = [L(f"{' + '.join(map(str, vals))} = {sum(vals)}", memo="칸의 수를 모두 더하기")]
        S.add(3, q, f"{sum(vals)}명", "합계 = 칸마다의 수의 합", lines, f.out(), ap=str(sum(vals)), key=q)
    fill(S, 3, 20, g3)

    def graph(f, names, vals, at="q"):
        cw = 520 / len(names)
        for i, (nm, v) in enumerate(zip(names, vals)):
            x = 90 + cw * i + cw / 2
            for j in range(v):
                f.circ(x, 515 - j * 40, 16, c="ink", sw=3, at=at)
            f.text(x, 580, nm, z=24, b=700, at=at)
        f.line(70, 545, 620, 545, c="ink", w=3, at=at)

    def g4():
        tp = R.choice(list(TOPIC))
        names = R.sample(TOPIC[tp], R.randint(3, 4))
        vals = R.sample(range(1, 10), len(names))
        t = R.randrange(3)
        f = Fig()
        graph(f, names, vals)
        if t == 0:
            a, b = R.sample(range(len(names)), 2)
            hi, lo = (a, b) if vals[a] > vals[b] else (b, a)
            q = f"좋아하는 {eul(tp)} 조사해 ○ 그래프로 나타냈어요. {eul(names[hi])} 좋아하는 학생은 {eul(names[lo])} 좋아하는 학생보다 몇 명 더 많은가요?"
            lines = [L(f"{names[hi]} {vals[hi]}명, {names[lo]} {vals[lo]}명", memo="○ 세기"), L(f"{vals[hi]} − {vals[lo]} = {vals[hi] - vals[lo]}")]
            S.add(4, q, f"{vals[hi] - vals[lo]}명", "○의 수를 세어 빼기", lines, f.out(), ap=str(vals[hi] - vals[lo]), qfig=True, key=q + str(vals), dupq=True)
        elif t == 1:
            i = max(range(len(names)), key=lambda k: vals[k])
            q = f"좋아하는 {eul(tp)} 조사해 ○ 그래프로 나타냈어요. 가장 많은 학생이 좋아하는 {tp}{'은' if bat(tp) else '는'} 무엇이고, 몇 명인가요?"
            lines = [L("○가 가장 높이 쌓인 줄 찾기"), L(f"{names[i]} {vals[i]}명")]
            S.add(4, q, f"{names[i]}, {vals[i]}명", "가장 높은 줄", lines, f.out(), omr="ex", qfig=True, key=q + str(vals), dupq=True)
        else:
            q = f"좋아하는 {eul(tp)} 조사해 ○ 그래프로 나타냈어요. 조사한 학생은 모두 몇 명인가요?"
            lines = [L(", ".join(f"{n} {v}명" for n, v in zip(names, vals)), memo="줄마다 ○ 세기"), L(f"{' + '.join(map(str, vals))} = {sum(vals)}")]
            S.add(4, q, f"{sum(vals)}명", "줄마다 세어 모두 더하기", lines, f.out(), ap=str(sum(vals)), qfig=True, key=q + str(vals), dupq=True)
    fill(S, 4, 20, g4)

    def g5():
        tp = R.choice(list(TOPIC))
        names = R.sample(TOPIC[tp], R.randint(3, 4))
        vals = [R.randint(2, 9) for _ in names]
        h = R.randrange(len(names))
        tot = sum(vals)
        q = f"좋아하는 {eul(tp)} 조사한 표에서 합계가 {tot}명이에요. " + ", ".join(f"{n} {v}명" for i, (n, v) in enumerate(zip(names, vals)) if i != h) + f"일 때, {eul(names[h])} 좋아하는 학생은 몇 명인가요?"
        f = Fig()
        table(f, names, vals, hide=h)
        known = [v for i, v in enumerate(vals) if i != h]
        lines = [L(f"{tot} − {' − '.join(map(str, known))} = {vals[h]}", memo="합계에서 아는 칸 빼기")]
        S.add(5, q, f"{vals[h]}명", "합계 − 아는 칸", lines, f.out(), ap=str(vals[h]), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 곱셈(2-1) ══════════
GOODS = [("사탕", "개", "봉지"), ("연필", "자루", "묶음"), ("달걀", "개", "판"), ("귤", "개", "상자"), ("구슬", "개", "주머니"), ("과자", "개", "봉지"), ("꽃", "송이", "다발")]
def mul2():
    S = Set("mul2", "곱셈 — 묶어 세기에서 곱셈식으로", "곱셈",
            {1: "묶어 세기", 2: "몇의 몇 배", 3: "덧셈식 ↔ 곱셈식", 4: "배열로 곱하기", 5: "곱셈 이야기"},
            pp=10,
            tips={1: "2씩, 5씩 … 같은 수씩 묶어 뛰어 세기",
                  2: "4의 3배 = 4를 3번 더한 것 = 4 × 3",
                  3: "같은 수를 여러 번 더하면 곱셈식으로 — 5 + 5 + 5 = 5 × 3",
                  4: "한 줄에 □개씩 ○줄 → □ × ○",
                  5: "한 묶음의 수 × 묶음 수"},
            note="곱셈은 ‘같은 수를 여러 번 더하기’예요. 묶어 세기 → 몇의 몇 배 → 곱셈식 순서로 말을 바꿔 가며 같은 상황을 보게 해 주세요.")
    R = rng(5206)

    def groups(f, a, b, at="q"):
        cw = min(120, 580 / b)
        rows = (a + 1) // 2
        h = 44 * rows + 36
        x0 = 330 - cw * b / 2
        for i in range(b):
            x = x0 + i * cw
            f.rect(x + 6, 330 - h / 2, cw - 12, h, c="soft", sw=2.5, rx=18, at=at)
            for j in range(a):
                f.circ(x + cw / 2 + ((j % 2) - 0.5) * 36 * (1 if (j // 2) * 2 + 1 < a or a % 2 == 0 else 0), 330 - h / 2 + 40 + (j // 2) * 44, 15, c="ink", sw=2.5, f="gold", fo=0.5, at=at)

    def g1():
        a, b = R.choice([2, 3, 4, 5]), R.randint(2, 7)
        th = R.choice(["", "사탕을 ", "구슬을 ", "단추를 "])
        q = f"{th}{a}개씩 {b}묶음으로 묶었어요. 모두 몇 개인가요?"
        f = Fig()
        groups(f, a, b)
        seq = [a * i for i in range(1, b + 1)]
        lines = [L(", ".join(map(str, seq)), memo=f"{a}씩 뛰어 세기"), L(f"{a} × {b} = {a * b}")]
        S.add(1, q, f"{a * b}개", "같은 수씩 뛰어 세기", lines, f.out(), ap=str(a * b), key=q)
    fill(S, 1, 20, g1)

    def g2():
        a, b = R.randint(2, 9), R.randint(2, 6)
        q = f"{a}의 {b}배는 얼마인가요?"
        lines = [L(f"{eul(a)} {b}번 더하기"), L(f"{' + '.join([str(a)] * b)} = {a * b}"), L(f"{a} × {b} = {a * b}")]
        S.add(2, q, str(a * b), "몇의 몇 배 = 몇을 몇 번 더하기", lines, None, key=q)
    fill(S, 2, 20, g2)

    def g3():
        a, b = R.randint(2, 9), R.randint(2, 6)
        if R.random() < 0.5:
            e = " + ".join([str(a)] * b)
            q = f"{eul(e)} 곱셈식으로 나타내세요."
            lines = [L(f"{iga(a)} {b}번"), L(f"{a} × {b}")]
            S.add(3, q, f"{a} × {b}", "같은 수를 몇 번 더했는지", lines, None, ap=f"{a}×{b}", omr="ex", key=q)
        else:
            q = f"{eul(f'{a} × {b}')} 덧셈식으로 나타내세요."
            s_ = " + ".join([str(a)] * b)
            lines = [L(f"{eul(a)} {b}번 더하기"), L(s_)]
            S.add(3, q, s_, "곱하는 수만큼 더하기", lines, None, ap=s_.replace(" ", ""), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.randint(2, 9), R.randint(2, 6)
        q = f"바둑돌이 한 줄에 {a}개씩 {b}줄로 놓여 있어요. 바둑돌은 모두 몇 개인가요?"
        f = Fig()
        g = min(62, 560 / a)
        for i in range(b):
            for j in range(a):
                f.circ(330 - (a - 1) * g / 2 + j * g, 340 - (b - 1) * 31 + i * 62, min(24, g * 0.38), c="ink", sw=3, f="ink", fo=0.85 if (i + j) % 2 else 0.08)
        lines = [L(f"{a}개씩 {b}줄 → {a} × {b}"), L(f"{a} × {b} = {a * b}")]
        S.add(4, q, f"{a * b}개", "한 줄의 수 × 줄 수", lines, f.out(), ap=str(a * b), key=q)
    fill(S, 4, 20, g4)

    def g5():
        th, u, pack = R.choice(GOODS)
        a, b = R.randint(2, 9), R.randint(2, 6)
        q = f"{iga(th)} 한 {pack}에 {a}{u}씩 들어 있어요. {b}{pack}에는 {iga(th)} 모두 몇 {u} 있나요?"
        lines = [L(f"{a}{u}씩 {b}{pack}"), L(f"{a} × {b} = {a * b}")]
        S.add(5, q, f"{a * b}{u}", "한 묶음의 수 × 묶음 수", lines, None, ap=str(a * b), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 규칙 찾기(2학년) ══════════
DAYS = ["월", "화", "수", "목", "금", "토", "일"]
def rule2():
    S = Set("rule2", "규칙 찾기 — 덧셈표 · 곱셈표 · 달력 · 쌓은 모양 · 무늬", "규칙 찾기",
            {1: "덧셈표의 규칙", 2: "곱셈표의 규칙", 3: "달력의 규칙", 4: "쌓은 모양의 규칙", 5: "무늬의 규칙"},
            pp=10,
            tips={1: "덧셈표는 오른쪽으로, 아래로 갈수록 1씩 커져요",
                  2: "곱셈표에서 □단은 □씩 커져요 — 곱하는 순서를 바꾸어도 곱은 같아요",
                  3: "달력은 아래 칸이 7 큰 수 — 같은 요일은 7일마다",
                  4: "한 번 쌓을 때마다 몇 개씩 늘어나는지",
                  5: "되풀이되는 마디를 찾고, 마디가 몇 번인지"},
            note="달력 문제는 ‘아래로 한 칸 = 7일 뒤’를 메모하며 옮겨 가게 해 주세요. 셈보다 칸 옮기기가 먼저예요.")
    R = rng(5207)

    def g1():
        a, b = R.randint(1, 9), R.randint(1, 9)
        if R.random() < 0.5:
            q = f"1부터 9까지의 덧셈표에서 가로줄의 {wa(a)} 세로줄의 {iga(b)} 만나는 칸의 수는 무엇인가요?"
            lines = [L(f"{a} + {b} = {a + b}", memo="가로 수 + 세로 수")]
            S.add(1, q, str(a + b), "만나는 칸 = 가로 수 + 세로 수", lines, None, key=q)
        else:
            d = R.choice(["오른쪽", "아래쪽"])
            k2 = R.randint(2, 4)
            if (b if d == "오른쪽" else a) + k2 > 9:
                return
            q = f"덧셈표에서 {a} + {b}의 칸부터 {d}으로 {k2}칸 간 곳의 수는 무엇인가요?"
            lines = [L(f"{a} + {b} = {a + b}"), L(f"{d}으로 한 칸마다 1씩 커져요"), L(f"{a + b} + {k2} = {a + b + k2}")]
            S.add(1, q, str(a + b + k2), "오른쪽 · 아래로 1씩", lines, None, key=q)
    fill(S, 1, 20, g1)

    def reps(p):
        return sum(1 for x in range(1, 10) for y in range(1, 10) if x * y == p)

    def g2():
        a, b = R.randint(2, 9), R.randint(2, 9)
        if R.random() < 0.5:
            q = f"곱셈표에서 {a}단의 수는 몇씩 커지나요? 그리고 {a} × {b}의 칸에는 어떤 수가 있나요?"
            lines = [L(f"{a}단 → {a}씩 커져요"), L(f"{a} × {b} = {a * b}")]
            S.add(2, q, f"{a}씩, {a * b}", "□단은 □씩", lines, None, ap=f"{a}, {a * b}", omr="ex", key=q)
        else:
            if a == b or reps(a * b) != 2:
                return
            q = f"1부터 9까지의 곱셈표에서 {a} × {b}의 칸과 같은 수가 적힌 다른 칸은 몇 × 몇의 칸인가요?"
            lines = [L(f"{a} × {b} = {a * b}"), L("곱하는 두 수의 순서를 바꾸어도 곱은 같아요"), L(f"{b} × {a} = {a * b}")]
            S.add(2, q, f"{b} × {a}", "곱하는 순서를 바꾸어도 같아요", lines, None, ap=f"{b}×{a}", omr="ex", key=q)
    fill(S, 2, 20, g2)

    def g3():
        d1 = R.randint(1, 10)
        w1 = R.randrange(7)
        d2 = R.randint(d1 + 7, 28)
        w2 = (w1 + d2 - d1) % 7
        q = f"어느 달 {d1}일이 {DAYS[w1]}요일이에요. 같은 달 {d2}일은 무슨 요일인가요?"
        k, r = divmod(d2 - d1, 7)
        lines = [L(f"{d2} − {d1} = {d2 - d1} = 7 × {k} + {r}", memo="7일마다 같은 요일"),
                 L(f"{d1}일에서 아래로 {k}칸 → {d1 + 7 * k}일도 {DAYS[w1]}요일", memo="아래로 한 칸 = 7일 뒤")]
        lines.append(L(f"{r}일 더 가면 {DAYS[w2]}요일") if r else L(f"{d2}일 → {DAYS[w2]}요일"))
        S.add(3, q, f"{DAYS[w2]}요일", "같은 요일은 7일마다", lines, None, omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, d = R.randint(1, 4), R.randint(1, 3)
        n = R.randint(4, 7)
        seq = [a + d * i for i in range(n)]
        ORD = ["첫째", "둘째", "셋째", "넷째", "다섯째", "여섯째", "일곱째"]
        q = f"쌓기나무를 규칙에 따라 쌓고 있어요. 첫째에 {a}개, 둘째에 {a + d}개, 셋째에 {a + 2 * d}개를 쌓았다면 {ORD[n - 1]}에는 몇 개를 쌓게 되나요?"
        f = Fig()
        s = 36
        for i in range(3):
            x0 = 25 + i * 215
            for j in range(seq[i]):
                f.rect(x0 + (j % 5) * s, 450 - (j // 5) * s, s, s, c="ink", sw=2.5, f="gold", fo=0.45)
            f.text(x0 + 2.5 * s, 540, ORD[i], z=28, b=700)
        lines = [L(f"{d}개씩 늘어나요"), L(", ".join(map(str, seq)), memo="하나씩 이어 쓰기"), L(f"{ORD[n - 1]} → {seq[-1]}개")]
        S.add(4, q, f"{seq[-1]}개", "몇 개씩 늘어나는지 찾기", lines, f.out(), ap=str(seq[-1]), key=q)
    fill(S, 4, 20, g4)

    def g5():
        m = R.choice([2, 3, 4])
        unit = [R.choice(["○", "●"]) for _ in range(m)]
        if len(set(unit)) < 2:
            return
        n = R.randint(m * 3 + 1, m * 9)
        cnt = sum(1 for i in range(n) if unit[i % m] == "●")
        k, r = divmod(n, m)
        per = unit.count("●")
        extra = sum(1 for i in range(r) if unit[i] == "●")
        q = f"{''.join(ic(x) for x in unit)}의 차례가 되풀이되도록 동그라미 {n}개를 늘어놓았어요. 까만 동그라미는 몇 개인가요?"
        lines = [L(f"마디 {m}개에 ● {per}개"), L(f"{m} × {k} = {m * k}" + (f", 남은 {r}개" if r else ""), memo=f"마디 {k}번"),
                 L(f"{per} × {k} + {extra} = {cnt}" if r else f"{per} × {k} = {cnt}")]
        S.add(5, q, f"{cnt}개", "마디로 묶어 세기", lines, None, ap=str(cnt), key=q)
    fill(S, 5, 20, g5)
    return S
