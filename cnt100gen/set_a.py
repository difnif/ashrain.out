# 세트 A — 학년별 선발 100제
from common import *

CLUBS = ["방송부", "도서부", "과학 동아리", "합창단", "봉사 동아리", "토론 동아리",
         "댄스 동아리", "밴드부", "학생 기자단", "수학 동아리", "미술부", "환경 동아리",
         "영화 동아리", "축구부", "로봇 동아리", "요리 동아리"]
_ci = [0]


def club():
    c = CLUBS[_ci[0] % len(CLUBS)]
    _ci[0] += 1
    return c


def pop(g):
    return [(gr, i) for gr, n in g.items() for i in range(n)]


def gtxt(g):
    return ", ".join(f"{gr}학년 {n}명" for gr, n in g.items())


def intro(g, cl=None):
    cl = cl or club()
    return f"{josa(cl, '은', '는')} {gtxt(g)}으로 이루어져 있다."


def N(g):
    return sum(g.values())


def G3(a, b, c):
    return {1: a, 2: b, 3: c}


def ALLP(g, extra=""):
    """포지티브 — 「모두 3 + 3 + 2 = 8명」(학년마다 더한 것)"""
    return f"모두 {plus(g.values())} = {N(g)}명" + extra


# ───────────── 1단계 ─────────────
def a_sum_all(g):
    n = N(g)
    return dict(q=f"{intro(g)} 이 중에서 대표 1명을 뽑는 경우의 수를 구하시오.",
                ans=n, chk=cnt(pop(g)),
                pos=gtxt(g), neg="1명만 뽑는다",
                plan="여러 학년에서 동시에 뽑히는 일은 없으므로 더한다(합의 법칙).",
                eq=[L("대표 1명(합의 법칙)", plus(g.values()), n)])


def a_sum_two(g, x, y):
    v = g[x] + g[y]
    return dict(q=f"{intro(g)} {x}학년 또는 {y}학년 학생 중에서 발표자 1명을 뽑는 경우의 수를 구하시오.",
                ans=v, chk=cnt(pop(g), lambda s: s[0] in (x, y)),
                pos=f"{x}학년 {g[x]}명, {y}학년 {g[y]}명", neg=f"{x}학년 또는 {y}학년에서 1명",
                plan="두 학년에서 동시에 뽑히지 않으므로 더한다.",
                eq=[L(f"{x}학년 또는 {y}학년에서 1명(합의 법칙)", plus([g[x], g[y]]), v)])


def a_prod(g):
    v = 1
    for n in g.values():
        v *= n
    ks = list(g)
    chk = cnt(PROD(*[[(k, i) for i in range(g[k])] for k in ks]))
    return dict(q=f"{intro(g)} 각 학년에서 대표를 1명씩 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="학년마다 1명씩",
                plan="한 학년의 대표 각각에 다른 학년의 대표가 짝지어지므로 곱한다(곱의 법칙).",
                eq=[L("학년마다 1명씩(곱의 법칙)", times(g.values()), v)])


def a_sum_then_prod(g):
    a, b, c = g[1], g[2], g[3]
    v = (a + b) * c
    chk = cnt(PROD([s for s in pop(g) if s[0] in (1, 2)], [s for s in pop(g) if s[0] == 3]))
    return dict(q=f"{intro(g)} 1, 2학년 학생 중에서 진행자 1명, 3학년 학생 중에서 심사위원 1명을 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="진행자는 1·2학년에서, 심사위원은 3학년에서",
                plan="진행자 후보를 먼저 더해 구하고(합), 심사위원과 짝지으므로 곱한다(곱).",
                eq=[L("진행자(1 · 2학년에서 1명)", plus([a, b]), a + b), L("심사위원(3학년에서 1명)", c),
                    L("진행자 × 심사위원(곱의 법칙)", times([a + b, c]), v)])


def a_gender(m, f):
    cl = club()
    v = m * f
    return dict(q=f"{josa(cl, '은', '는')} 남학생 {m}명, 여학생 {f}명으로 이루어져 있다. 남학생 대표 1명과 여학생 대표 1명을 뽑는 경우의 수를 구하시오.",
                ans=v, chk=cnt(PROD(range(m), range(f))),
                pos=f"남학생 {m}명, 여학생 {f}명", neg="남녀 각각 1명씩",
                plan="남학생 대표 각각에 여학생 대표가 짝지어지므로 곱한다.",
                eq=[L("남학생 대표 × 여학생 대표(곱의 법칙)", times([m, f]), v)])


# ───────────── 2단계 ─────────────
def a_pres_vice(g):
    n = N(g)
    v = n * (n - 1)
    return dict(q=f"{intro(g)} 이 중에서 회장 1명과 부회장 1명을 뽑는 경우의 수를 구하시오.",
                ans=v, chk=cnt(PERM(pop(g), 2)),
                pos=ALLP(g), neg="회장과 부회장은 다른 사람, 자격이 다르다",
                plan="회장 → 부회장 차례로 뽑아 곱한다. 자격이 다르므로 2로 나누지 않는다.",
                eq=[L(f"모두 {n}명 중 회장 · 부회장(자격이 다름)", chain(n, 2), v)])


def a_two_same(g):
    n = N(g)
    v = c2(n)
    return dict(q=f"{intro(g)} 이 중에서 지역 대회에 나갈 대표 2명을 뽑는 경우의 수를 구하시오.",
                ans=v, chk=cnt(COMB(pop(g), 2)),
                pos=ALLP(g), neg="대표 2명은 자격이 같다",
                plan="차례로 뽑은 수를 구한 뒤, (갑, 을)과 (을, 갑)이 같은 경우이므로 2로 나눈다.",
                eq=[L(f"모두 {n}명 중 대표 2명(자격이 같음)", c2s(n), v)])


def a_in_grade_pv(g, k):
    x = g[k]
    v = x * (x - 1)
    return dict(q=f"{intro(g)} {k}학년 학생 중에서만 부장 1명과 차장 1명을 뽑는 경우의 수를 구하시오.",
                ans=v, chk=cnt(PERM([s for s in pop(g) if s[0] == k], 2)),
                pos=f"{k}학년 {x}명", neg=f"{k}학년에서만 · 부장과 차장은 자격이 다르다",
                plan=f"다른 학년은 지우고 {k}학년 {x}명만 본다. 자격이 다르므로 차례로 곱한다.",
                eq=[L(f"{k}학년 {x}명 중 부장 · 차장(자격이 다름)", chain(x, 2), v)])


def a_in_grade_two(g, k):
    x = g[k]
    v = c2(x)
    return dict(q=f"{intro(g)} {k}학년 학생 중에서 청소 당번 2명을 뽑는 경우의 수를 구하시오.",
                ans=v, chk=cnt(COMB([s for s in pop(g) if s[0] == k], 2)),
                pos=f"{k}학년 {x}명", neg=f"{k}학년에서만 · 당번 2명은 자격이 같다",
                plan=f"{k}학년 {x}명만 보고, 자격이 같으므로 2로 나눈다.",
                eq=[L(f"{k}학년 {x}명 중 당번 2명(자격이 같음)", c2s(x), v)])


def a_p3_v12(g):
    a, b, c = g[1], g[2], g[3]
    v = c * (a + b)
    chk = cnt(PERM(pop(g), 2), lambda s: s[0][0] == 3 and s[1][0] in (1, 2))
    return dict(q=f"{intro(g)} 회장은 3학년에서, 부회장은 1, 2학년에서 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="회장은 3학년 · 부회장은 1·2학년",
                plan="회장 후보와 부회장 후보가 서로 겹치지 않으므로 그대로 곱한다.",
                eq=[L("회장(3학년에서 1명)", c), L("부회장(1 · 2학년에서 1명)", plus([a, b]), a + b),
                    L("회장 × 부회장(곱의 법칙)", times([c, a + b]), v)])


def a_two_grades_two_each(g, x, y):
    v = c2(g[x]) * c2(g[y])
    chk = cnt(PROD(COMB([s for s in pop(g) if s[0] == x], 2), COMB([s for s in pop(g) if s[0] == y], 2)))
    return dict(q=f"{intro(g)} {x}학년에서 2명, {y}학년에서 2명을 뽑아 축제 안내 요원으로 정하는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=f"{x}학년 {g[x]}명, {y}학년 {g[y]}명", neg="학년마다 2명 · 안내 요원은 자격이 같다",
                plan="학년마다 따로 2명을 뽑고(÷ 2), 두 학년은 함께 일어나므로 곱한다.",
                eq=[L(f"{x}학년 {g[x]}명 중 2명(자격이 같음)", c2s(g[x]), c2(g[x])), L(f"{y}학년 {g[y]}명 중 2명(자격이 같음)", c2s(g[y]), c2(g[y])),
                    L("두 학년 함께(곱의 법칙)", times([c2(g[x]), c2(g[y])]), v)])


def a_two_one(g, x, y):
    v = c2(g[x]) * g[y]
    chk = cnt(PROD(COMB([s for s in pop(g) if s[0] == x], 2), [s for s in pop(g) if s[0] == y]))
    return dict(q=f"{intro(g)} {x}학년에서 2명, {y}학년에서 1명을 뽑아 봉사 활동 조를 만드는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=f"{x}학년 {g[x]}명, {y}학년 {g[y]}명", neg=f"{x}학년 2명(자격 같음) · {y}학년 1명",
                plan=f"{x}학년 2명은 ÷ 2, {y}학년 1명은 그대로 세어 곱한다.",
                eq=[L(f"{x}학년 {g[x]}명 중 2명(자격이 같음)", c2s(g[x]), c2(g[x])), L(f"{y}학년 {g[y]}명 중 1명", g[y]),
                    L("두 학년 함께(곱의 법칙)", times([c2(g[x]), g[y]]), v)])


def a_relay(g):
    a, b, c = g[1], g[2], g[3]
    v = a * b * c * 6
    chk = cnt(PROD([s for s in pop(g) if s[0] == 1], [s for s in pop(g) if s[0] == 2], [s for s in pop(g) if s[0] == 3])) * cnt(PERM(range(3)))
    return dict(q=f"{intro(g)} 체육대회 계주에 나갈 선수를 각 학년에서 1명씩 뽑고, 뽑힌 3명이 달리는 순서까지 정하는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="학년마다 1명 · 달리는 순서도 정한다",
                plan="선수 뽑기(곱)와 3명 줄 세우기(3 × 2 × 1)를 차례로 하므로 곱한다.",
                eq=[L("학년마다 선수 1명씩(곱의 법칙)", times([a, b, c]), a * b * c), L("뽑힌 3명이 달리는 순서(3명을 한 줄로)", row(3), 6),
                    L("선수 × 순서(곱의 법칙)", times([a * b * c, 6]), v)])


# ───────────── 3단계 ─────────────
def a_three_roles(g):
    n = N(g)
    v = n * (n - 1) * (n - 2)
    return dict(q=f"{intro(g)} 이 중에서 회장, 부회장, 총무를 1명씩 뽑는 경우의 수를 구하시오.",
                ans=v, chk=cnt(PERM(pop(g), 3)),
                pos=ALLP(g), neg="세 사람은 서로 다르고 자격도 다르다",
                plan="회장 → 부회장 → 총무 차례로 한 명씩 줄여 가며 곱한다.",
                eq=[L(f"모두 {n}명 중 회장 · 부회장 · 총무(자격이 다름)", chain(n, 3), v)])


def a_three_same(g):
    n = N(g)
    v = c3(n)
    return dict(q=f"{intro(g)} 이 중에서 학교 대표로 토론 대회에 나갈 3명을 뽑는 경우의 수를 구하시오.",
                ans=v, chk=cnt(COMB(pop(g), 3)),
                pos=ALLP(g), neg="3명은 자격이 같다",
                plan="차례로 뽑은 수를 구한 뒤, 같은 3명을 줄 세우는 3 × 2 × 1가지가 모두 같은 경우이므로 (3 × 2 × 1)로 나눈다.",
                eq=[L(f"모두 {n}명 중 대표 3명(자격이 같음)", c3s(n), v)])


def a_pv_same_grade(g):
    terms = [g[k] * (g[k] - 1) for k in g]
    v = sum(terms)
    chk = cnt(PERM(pop(g), 2), lambda s: s[0][0] == s[1][0])
    return dict(q=f"{intro(g)} 회장과 부회장을 같은 학년에서 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="회장과 부회장은 같은 학년 · 자격이 다르다",
                plan="어느 학년에서 뽑는지로 나누어 세고 더한다(학년끼리는 동시에 안 일어남).",
                eq=[L(f"{k}학년 {g[k]}명 중 회장 · 부회장", chain(g[k], 2), g[k] * (g[k] - 1)) for k in g]
                   + [L("같은 학년(합의 법칙)", plus(terms), v)])


def a_pv_diff_grade(g):
    n = N(g)
    same = sum(g[k] * (g[k] - 1) for k in g)
    v = n * (n - 1) - same
    chk = cnt(PERM(pop(g), 2), lambda s: s[0][0] != s[1][0])
    return dict(q=f"{intro(g)} 회장과 부회장을 서로 다른 학년에서 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg="회장과 부회장은 다른 학년",
                plan="전체에서 '같은 학년인 경우'를 빼는 것이 빠르다. 회장을 정한 뒤 다른 학년에서 부회장을 고르는 방법으로 확인할 수 있다.",
                eq=[L(f"모두 {n}명 중 회장 · 부회장", chain(n, 2), n * (n - 1))]
                   + [L(f"{k}학년 {g[k]}명 중 회장 · 부회장", chain(g[k], 2), g[k] * (g[k] - 1)) for k in g]
                   + [L("같은 학년(합의 법칙)", plus([g[k] * (g[k] - 1) for k in g]), same), L("다른 학년(전체 − 같은 학년)", f"{n * (n - 1)} − {same}", v)])


def a_two_same_grade_eq(g):
    terms = [c2(g[k]) for k in g]
    v = sum(terms)
    chk = cnt(COMB(pop(g), 2), lambda s: s[0][0] == s[1][0])
    return dict(q=f"{intro(g)} 대표 2명을 뽑을 때, 두 사람이 같은 학년인 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="대표 2명은 자격이 같다 · 같은 학년",
                plan="학년마다 2명 뽑는 수(÷ 2)를 구해 더한다.",
                eq=[L(f"{k}학년 {g[k]}명 중 2명(자격이 같음)", c2s(g[k]), c2(g[k])) for k in g]
                   + [L("같은 학년(합의 법칙)", plus(terms), v)])


def a_two_diff_grade_eq(g):
    ks = list(g)
    pairs = [(x, y) for i, x in enumerate(ks) for y in ks[i + 1:]]
    terms = [g[x] * g[y] for x, y in pairs]
    v = sum(terms)
    chk = cnt(COMB(pop(g), 2), lambda s: s[0][0] != s[1][0])
    return dict(q=f"{intro(g)} 대표 2명을 뽑을 때, 두 사람이 서로 다른 학년인 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="대표 2명은 자격이 같다 · 서로 다른 학년",
                plan="어느 두 학년에서 1명씩 뽑는지로 나눈다. 학년 짝마다 곱하고, 짝끼리는 더한다.",
                eq=[L(f"{x}학년 1명 · {y}학년 1명(곱의 법칙)", times([g[x], g[y]]), g[x] * g[y]) for x, y in pairs]
                   + [L("다른 학년(합의 법칙)", plus(terms), v)])


def a_three_incl(g, k, name):
    n = N(g)
    v = c2(n - 1)
    who = (k, 0)
    chk = cnt(COMB(pop(g), 3), lambda s: who in s)
    return dict(q=f"{intro(g)} 이 중에서 대표 3명을 뽑을 때, {k}학년 {josa(name, '이', '가')} 반드시 뽑히는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg=f"{josa(name, '은', '는')} 반드시 포함 · 3명은 자격이 같다",
                plan=f"{josa(name, '을', '를')} 먼저 넣어 두면 나머지 {n - 1}명 중 2명만 뽑으면 된다.",
                eq=[L(f"{josa(name, '을', '를')} 넣어 두고 남은 {n - 1}명 중 2명(자격이 같음)", c2s(n - 1), v)])


def a_three_incl_excl(g, k1, n1, k2, n2):
    n = N(g)
    v = c2(n - 2)
    A, B = (k1, 0), (k2, 1 if k1 == k2 else 0)
    chk = cnt(COMB(pop(g), 3), lambda s: A in s and B not in s)
    return dict(q=f"{intro(g)} 이 중에서 대표 3명을 뽑을 때, {k1}학년 {josa(n1, '은', '는')} 뽑히고 {k2}학년 {josa(n2, '은', '는')} 뽑히지 않는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg=f"{n1} 포함 · {n2} 제외 · 자격이 같다",
                plan=f"{josa(n1, '을', '를')} 넣어 두고 {josa(n2, '을', '를')} 지우면, 남은 {n - 2}명 중 2명을 뽑으면 된다.",
                eq=[L(f"{josa(n1, '을', '를')} 넣고 {josa(n2, '을', '를')} 빼면 남은 {n - 2}명 중 2명(자격이 같음)", c2s(n - 2), v)])


def a_three_atleast(g, k):
    n = N(g)
    rest = n - g[k]
    v = c3(n) - c3(rest)
    chk = cnt(COMB(pop(g), 3), lambda s: any(p[0] == k for p in s))
    return dict(q=f"{intro(g)} 이 중에서 대표 3명을 뽑을 때, {k}학년이 적어도 1명 포함되는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg=f"'적어도 1명' {k}학년 · 자격이 같다",
                plan=f"'적어도'는 반대(= {k}학년이 한 명도 없음)를 세어 전체에서 뺀다.",
                eq=[L(f"모두 {n}명 중 3명(자격이 같음)", c3s(n), c3(n)), L(f"{k}학년이 없음({k}학년이 아닌 {rest}명 중 3명)", c3s(rest), c3(rest)),
                    L(f"{k}학년이 적어도 1명(전체 − 없음)", f"{c3(n)} − {c3(rest)}", v)])


def a_leader_members(g, k):
    n = N(g)
    v = g[k] * c2(n - 1)
    chk = cnt(PROD([s for s in pop(g) if s[0] == k], COMB(pop(g), 2)), lambda t: t[0] not in t[1])
    return dict(q=f"{intro(g)} {k}학년 중에서 조장 1명을 뽑고, 나머지 학생 중에서 조원 2명을 뽑는 경우의 수를 구하시오. (단, 조원 2명은 학년에 관계없이 뽑는다.)",
                ans=v, chk=chk,
                pos=f"{k}학년 {g[k]}명 · " + ALLP(g), neg=f"조장은 {k}학년 · 조원 2명은 자격이 같다 · 조장은 조원이 될 수 없다",
                plan=f"조장을 먼저 정하면 남은 {n - 1}명 중 2명(÷ 2)을 뽑는다. 두 일을 차례로 하므로 곱한다.",
                eq=[L(f"조장({k}학년 {g[k]}명 중 1명)", g[k]), L(f"조원(남은 {n - 1}명 중 2명, 자격이 같음)", c2s(n - 1), c2(n - 1)),
                    L("조장 × 조원(곱의 법칙)", times([g[k], c2(n - 1)]), v)])


# ───────────── 4단계 (확률) ─────────────
def p_one_grade(g, k):
    n = N(g)
    v = F(g[k], n)
    chk = F(cnt(pop(g), lambda s: s[0] == k), n)
    return dict(q=f"{intro(g)} 제비뽑기로 1명을 뽑을 때, {k}학년 학생이 뽑힐 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g, ", 누구나 뽑힐 가능성이 같다"), neg=f"{k}학년이 뽑힘",
                plan="(일어나는 경우의 수) ÷ (모든 경우의 수)",
                eq=[f"모든 경우 {n}", L(f"{k}학년이 뽑힘({k}학년 {g[k]}명)", g[k]), pfeq(g[k], n)])


def p_one_not(g, k):
    n = N(g)
    v = 1 - F(g[k], n)
    chk = F(cnt(pop(g), lambda s: s[0] != k), n)
    return dict(q=f"{intro(g)} 제비뽑기로 1명을 뽑을 때, {k}학년 학생이 뽑히지 않을 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg=f"{k}학년이 '아닌' 학생",
                plan=f"(어떤 사건이 일어나지 않을 확률) = 1 − (일어날 확률)",
                eq=[f"모든 경우 {n}", L(f"{k}학년이 뽑힘({k}학년 {g[k]}명)", g[k]), pnot(g[k], n)])


def _red(x):
    return x


def p_two_both(g, k):
    n = N(g)
    v = F(c2(g[k]), c2(n))
    chk = F(cnt(COMB(pop(g), 2), lambda s: s[0][0] == k and s[1][0] == k), cnt(COMB(pop(g), 2)))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 2명을 뽑을 때, 2명 모두 {k}학년일 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g, " · 대표 2명은 자격이 같다"), neg=f"2명 모두 {k}학년",
                plan="모든 경우와 일어나는 경우를 둘 다 '자격이 같은 2명'으로 센다.",
                eq=[L(f"모든 경우(모두 {n}명 중 2명)", c2s(n), c2(n)), L(f"{k}학년 {g[k]}명 중 2명", c2s(g[k]), c2(g[k])), pfeq(c2(g[k]), c2(n))])


def p_two_same(g):
    n = N(g)
    s = sum(c2(g[k]) for k in g)
    v = F(s, c2(n))
    chk = F(cnt(COMB(pop(g), 2), lambda t: t[0][0] == t[1][0]), c2(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 2명을 뽑을 때, 두 사람이 같은 학년일 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg="두 사람이 같은 학년",
                plan="학년마다 2명 뽑는 수를 더해 일어나는 경우를 센다.",
                eq=[L(f"모든 경우(모두 {n}명 중 2명)", c2s(n), c2(n))] + [L(f"{k}학년 {g[k]}명 중 2명", c2s(g[k]), c2(g[k])) for k in g]
                   + [L("같은 학년(합의 법칙)", plus([c2(g[k]) for k in g]), s), pfeq(s, c2(n))])


def p_two_diff(g):
    n = N(g)
    s = sum(c2(g[k]) for k in g)
    v = 1 - F(s, c2(n))
    chk = F(cnt(COMB(pop(g), 2), lambda t: t[0][0] != t[1][0]), c2(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 2명을 뽑을 때, 두 사람이 서로 다른 학년일 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg="두 사람이 서로 다른 학년",
                plan="같은 학년일 확률을 구해 1에서 뺀다.",
                eq=[L(f"모든 경우(모두 {n}명 중 2명)", c2s(n), c2(n))] + [L(f"{k}학년 {g[k]}명 중 2명", c2s(g[k]), c2(g[k])) for k in g]
                   + [L("같은 학년(합의 법칙)", plus([c2(g[k]) for k in g]), s), pnot(s, c2(n))])


def p_named_in_two(g, k, name):
    n = N(g)
    v = F(n - 1, c2(n))
    who = (k, 0)
    chk = F(cnt(COMB(pop(g), 2), lambda s: who in s), c2(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 2명을 뽑을 때, {k}학년 {josa(name, '이', '가')} 뽑힐 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g, " · 대표 2명은 자격이 같다"), neg=f"{name} 포함",
                plan=f"{josa(name, '을', '를')} 넣어 두면 짝이 될 사람만 고르면 된다 → {n - 1}가지.",
                eq=[L(f"모든 경우(모두 {n}명 중 2명)", c2s(n), c2(n)), L(f"{name}의 짝(남은 {n - 1}명 중 1명)", n - 1), pfeq(n - 1, c2(n))])


def p_pv_grades(g, x, y):
    n = N(g)
    v = F(g[x] * g[y], n * (n - 1))
    chk = F(cnt(PERM(pop(g), 2), lambda s: s[0][0] == x and s[1][0] == y), n * (n - 1))
    return dict(q=f"{intro(g)} 제비뽑기로 회장 1명과 부회장 1명을 차례로 뽑을 때, 회장은 {x}학년, 부회장은 {y}학년에서 뽑힐 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g, " · 자격이 다르다"), neg=f"회장 {x}학년 · 부회장 {y}학년",
                plan="모든 경우와 일어나는 경우를 둘 다 '차례가 있는' 방법으로 센다.",
                eq=[L(f"모든 경우(모두 {n}명 중 회장 · 부회장)", chain(n, 2), n * (n - 1)), L(f"회장 {x}학년 · 부회장 {y}학년", times([g[x], g[y]]), g[x] * g[y]),
                    pfeq(g[x] * g[y], n * (n - 1))])


def p_three_all_grades(g):
    n = N(g)
    a, b, c = g[1], g[2], g[3]
    v = F(a * b * c, c3(n))
    chk = F(cnt(COMB(pop(g), 3), lambda s: len({p[0] for p in s}) == 3), c3(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 3명을 뽑을 때, 세 학년이 모두 포함될 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g, " · 3명은 자격이 같다"), neg="학년마다 꼭 1명씩",
                plan="세 학년이 모두 포함되려면 학년마다 1명씩 뽑혀야 한다.",
                eq=[L(f"모든 경우(모두 {n}명 중 3명)", c3s(n), c3(n)), L("학년마다 1명씩(곱의 법칙)", times([a, b, c]), a * b * c), pfeq(a * b * c, c3(n))])


def p_three_atleast(g, k):
    n = N(g)
    rest = n - g[k]
    v = 1 - F(c3(rest), c3(n))
    chk = F(cnt(COMB(pop(g), 3), lambda s: any(p[0] == k for p in s)), c3(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 3명을 뽑을 때, {k}학년이 적어도 1명 뽑힐 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg=f"'적어도 1명' {k}학년",
                plan=f"{k}학년이 한 명도 안 뽑힐 확률을 1에서 뺀다.",
                eq=[L(f"모든 경우(모두 {n}명 중 3명)", c3s(n), c3(n)), L(f"{k}학년이 없음({k}학년이 아닌 {rest}명 중 3명)", c3s(rest), c3(rest)), pnot(c3(rest), c3(n))])


def p_zero(g, k):
    n = N(g)
    chk = F(cnt(COMB(pop(g), 3), lambda s: all(p[0] == k for p in s)), c3(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 3명을 뽑을 때, 3명 모두 {k}학년일 확률을 구하시오.",
                ans=F(0), chk=chk,
                pos=f"{k}학년은 {g[k]}명뿐", neg=f"3명 모두 {k}학년",
                plan="절대 일어날 수 없는 사건의 확률은 0이다.",
                eq=[f"{k}학년이 {g[k]}명뿐 → 3명을 채울 수 없다", "확률: 0"])


def p_one(g):
    n = N(g)
    mx = max(g.values())
    chk = F(cnt(COMB(pop(g), mx + 1), lambda s: len({p[0] for p in s}) >= 2), cnt(COMB(pop(g), mx + 1)))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 {mx + 1}명을 뽑을 때, 뽑힌 학생 중에 서로 다른 학년의 학생이 있을 확률을 구하시오.",
                ans=F(1), chk=chk,
                pos=f"학년마다 많아야 {mx}명", neg=f"{mx + 1}명 중 다른 학년이 섞임",
                plan="반드시 일어나는 사건의 확률은 1이다.",
                eq=[f"한 학년에 많아야 {mx}명 → {mx + 1}명이면 반드시 두 학년 이상이 섞인다", "확률: 1"])


# ───────────── 5단계 ─────────────
def a_three_roles_diff_grades(g):
    a, b, c = g[1], g[2], g[3]
    v = a * b * c * 6
    chk = cnt(PERM(pop(g), 3), lambda s: len({p[0] for p in s}) == 3)
    return dict(q=f"{intro(g)} 회장, 부회장, 총무를 1명씩 뽑되, 세 사람이 모두 서로 다른 학년이 되도록 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="세 사람의 학년이 모두 다르다 · 자격이 다르다",
                plan="학년마다 1명씩 뽑은 뒤, 3명에게 회장·부회장·총무를 나눠 주는 방법(3 × 2 × 1)을 곱한다.",
                eq=[L("학년마다 1명씩(곱의 법칙)", times([a, b, c]), a * b * c), L("3명에게 회장 · 부회장 · 총무(3명을 한 줄로)", row(3), 6),
                    L("곱의 법칙", times([a * b * c, 6]), v)])


def a_four_all_grades(g):
    a, b, c = g[1], g[2], g[3]
    t = [c2(a) * b * c, a * c2(b) * c, a * b * c2(c)]
    v = sum(t)
    chk = cnt(COMB(pop(g), 4), lambda s: len({p[0] for p in s}) == 3)
    return dict(q=f"{intro(g)} 대표 4명을 뽑을 때, 세 학년이 모두 적어도 1명씩 포함되도록 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="4명 · 학년마다 적어도 1명 · 자격이 같다",
                plan="4명을 세 학년에 나누면 (2, 1, 1)꼴뿐이다. 2명이 나오는 학년으로 나누어 센다.",
                eq=[L(f"1학년 {a}명 중 2명(자격이 같음)", c2s(a), c2(a)), L(f"2학년 {b}명 중 2명(자격이 같음)", c2s(b), c2(b)), L(f"3학년 {c}명 중 2명(자격이 같음)", c2s(c), c2(c)),
                    L("1학년이 2명 · 2학년 1명 · 3학년 1명", times([c2(a), b, c]), t[0]), L("2학년이 2명 · 1학년 1명 · 3학년 1명", times([a, c2(b), c]), t[1]),
                    L("3학년이 2명 · 1학년 1명 · 2학년 1명", times([a, b, c2(c)]), t[2]), L("합의 법칙", plus(t), v)])


def p_three_exact2(g, k):
    n = N(g)
    rest = n - g[k]
    num = c2(g[k]) * rest
    v = F(num, c3(n))
    chk = F(cnt(COMB(pop(g), 3), lambda s: sum(p[0] == k for p in s) == 2), c3(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 3명을 뽑을 때, {k}학년이 정확히 2명 뽑힐 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg=f"{k}학년 '정확히' 2명 → 나머지 1명은 다른 학년",
                plan=f"{k}학년에서 2명(÷ 2), {k}학년이 아닌 {rest}명에서 1명을 뽑아 곱한다.",
                eq=[L(f"모든 경우(모두 {n}명 중 3명)", c3s(n), c3(n)), L(f"{k}학년 {g[k]}명 중 2명(자격이 같음)", c2s(g[k]), c2(g[k])),
                    L(f"{k}학년이 아닌 {rest}명 중 1명", rest), L("곱의 법칙", times([c2(g[k]), rest]), num), pfeq(num, c3(n))])


def p_three_same_grade(g):
    n = N(g)
    s = sum(c3(g[k]) for k in g)
    v = F(s, c3(n))
    chk = F(cnt(COMB(pop(g), 3), lambda t: len({p[0] for p in t}) == 1), c3(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 3명을 뽑을 때, 3명이 모두 같은 학년일 확률을 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="3명 모두 같은 학년",
                plan="학년마다 3명을 뽑는 수를 구해 더한다. 2명 이하인 학년은 0가지.",
                eq=[L(f"모든 경우(모두 {n}명 중 3명)", c3s(n), c3(n))]
                   + [(L(f"{k}학년 {g[k]}명 중 3명", c3s(g[k]), c3(g[k])) if g[k] >= 3 else f"{k}학년 {g[k]}명 중 3명: 0(3명이 안 됨)") for k in g]
                   + [L("같은 학년(합의 법칙)", plus([c3(g[k]) for k in g]), s), pfeq(s, c3(n))])


def p_three_incl_excl(g, k1, n1, k2, n2):
    n = N(g)
    num = c2(n - 2)
    v = F(num, c3(n))
    A, B = (k1, 0), (k2, 1 if k1 == k2 else 0)
    chk = F(cnt(COMB(pop(g), 3), lambda s: A in s and B not in s), c3(n))
    return dict(q=f"{intro(g)} 제비뽑기로 대표 3명을 뽑을 때, {k1}학년 {josa(n1, '은', '는')} 뽑히고 {k2}학년 {josa(n2, '은', '는')} 뽑히지 않을 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g), neg=f"{n1} 포함 · {n2} 제외",
                plan=f"{josa(n1, '을', '를')} 넣고 {josa(n2, '을', '를')} 지운 뒤 남은 {n - 2}명 중 2명을 뽑는다.",
                eq=[L(f"모든 경우(모두 {n}명 중 3명)", c3s(n), c3(n)), L(f"{josa(n1, '을', '를')} 넣고 {josa(n2, '을', '를')} 빼면 남은 {n - 2}명 중 2명(자격이 같음)", c2s(n - 2), num), pfeq(num, c3(n))])


def popg(gg):
    """gg = {grade: (남, 여)} → [(grade, 성별, i)]"""
    return [(gr, s, i) for gr, (m, f) in gg.items() for s, k in (("남", m), ("여", f)) for i in range(k)]


def ggtxt(gg):
    return ", ".join(f"{gr}학년 남학생 {m}명·여학생 {f}명" for gr, (m, f) in gg.items())


def ggpos(gg):
    """포지티브 — 학년마다 남 · 여와 그 학년 사람 수(「1학년 남 2 · 여 1(3명)」)"""
    return ", ".join(f"{gr}학년 남 {m} · 여 {f}({m + f}명)" for gr, (m, f) in gg.items())


def a_two_diff_both(gg):
    P = popg(gg)
    ks = list(gg)
    terms = []
    v = 0
    for i, x in enumerate(ks):
        for y in ks[i + 1:]:
            t = gg[x][0] * gg[y][1] + gg[x][1] * gg[y][0]
            terms.append((x, y, t))
            v += t
    chk = cnt(COMB(P, 2), lambda s: s[0][0] != s[1][0] and s[0][1] != s[1][1])
    cl = club()
    return dict(q=f"{josa(cl, '은', '는')} {ggtxt(gg)}으로 이루어져 있다. 대표 2명을 뽑을 때, 두 사람의 학년도 다르고 성별도 다르게 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=ggtxt(gg), neg="학년도 다름 · 성별도 다름 · 자격이 같다",
                plan="두 학년을 먼저 고르고, (앞 학년 남, 뒤 학년 여) 또는 (앞 학년 여, 뒤 학년 남)으로 나눠 센다.",
                eq=[L(f"{x} · {y}학년(남여 + 여남)", f"{gg[x][0]} × {gg[y][1]} + {gg[x][1]} × {gg[y][0]}", t) for x, y, t in terms]
                   + [L("합의 법칙", plus([t for x, y, t in terms]), v)])


def p_mixed_gender(gg):
    P = popg(gg)
    ks = list(gg)
    tot = 1
    mm = 1
    ff = 1
    for k in ks:
        tot *= sum(gg[k])
        mm *= gg[k][0]
        ff *= gg[k][1]
    v = 1 - F(mm + ff, tot)
    groups = [[p for p in P if p[0] == k] for k in ks]
    chk = F(cnt(PROD(*groups), lambda s: len({p[1] for p in s}) == 2), tot)
    cl = club()
    return dict(q=f"{josa(cl, '은', '는')} {ggtxt(gg)}으로 이루어져 있다. 제비뽑기로 각 학년에서 대표를 1명씩 뽑을 때, 뽑힌 3명 중에 남학생과 여학생이 모두 있을 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ggpos(gg), neg="남녀가 모두 있음 = '모두 남' 도 '모두 여' 도 아님",
                plan="모두 남학생인 경우와 모두 여학생인 경우를 세어 1에서 뺀다.",
                eq=[L("모든 경우(학년마다 1명씩)", times([sum(gg[k]) for k in ks]), tot), L("모두 남", times([gg[k][0] for k in ks]), mm),
                    L("모두 여", times([gg[k][1] for k in ks]), ff), L("모두 남 또는 모두 여", plus([mm, ff]), mm + ff), pnot(mm + ff, tot)])


def a_pv_diff_no1pres(g):
    a, b, c = g[1], g[2], g[3]
    n = N(g)
    v = b * (n - b) + c * (n - c)
    chk = cnt(PERM(pop(g), 2), lambda s: s[0][0] != 1 and s[0][0] != s[1][0])
    return dict(q=f"{intro(g)} 회장과 부회장을 서로 다른 학년에서 뽑으려고 한다. 1학년은 회장이 될 수 없을 때, 뽑는 경우의 수를 구하시오.",
                ans=v, chk=chk,
                pos=gtxt(g), neg="회장은 2·3학년 · 부회장은 회장과 다른 학년",
                plan="회장의 학년으로 나눈다. 회장이 정해지면 부회장은 '회장 학년이 아닌' 학생 중에서 고른다.",
                eq=[L("회장 2학년 · 부회장 1 · 3학년", f"{b} × ({a} + {c})", f"{b} × {a + c} = {b * (a + c)}"), L("회장 3학년 · 부회장 1 · 2학년", f"{c} × ({a} + {b})", f"{c} × {a + b} = {c * (a + b)}"),
                    L("합의 법칙", plus([b * (a + c), c * (a + b)]), v)])


def p_pres_higher(g):
    n = N(g)
    ks = list(g)
    num = sum(g[x] * g[y] for x in ks for y in ks if x > y)
    v = F(num, n * (n - 1))
    chk = F(cnt(PERM(pop(g), 2), lambda s: s[0][0] > s[1][0]), n * (n - 1))
    pairs = [(x, y) for x in ks for y in ks if x > y]
    return dict(q=f"{intro(g)} 제비뽑기로 회장과 부회장을 차례로 뽑을 때, 회장의 학년이 부회장의 학년보다 높을 확률을 구하시오.",
                ans=v, chk=chk,
                pos=ALLP(g, " · 자격이 다르다"), neg="회장 학년 > 부회장 학년 (같은 학년은 안 됨)",
                plan="(회장 학년, 부회장 학년)을 (2, 1), (3, 1), (3, 2)로 나눠 센다.",
                eq=[L(f"(회장 {x}학년, 부회장 {y}학년)", times([g[x], g[y]]), g[x] * g[y]) for x, y in pairs]
                   + [L("일어나는 경우(합의 법칙)", plus([g[x] * g[y] for x, y in pairs]), num), L(f"모든 경우(모두 {n}명 중 회장 · 부회장)", chain(n, 2), n * (n - 1)),
                      pfeq(num, n * (n - 1))])


def build():
    I = []

    def add(lv, d):
        d["lv"] = lv
        I.append(d)

    # 1단계 (15)
    for g in [G3(4, 3, 5), G3(6, 7, 4), G3(8, 5, 9)]:
        add(1, a_sum_all(g))
    add(1, a_sum_two(G3(5, 6, 3), 2, 3))
    add(1, a_sum_two(G3(7, 4, 6), 1, 3))
    for g in [{1: 3, 2: 4}, {2: 5, 3: 6}, {1: 7, 3: 4}]:
        add(1, a_prod(g))
    for g in [G3(2, 3, 4), G3(3, 5, 2), G3(4, 4, 3)]:
        add(1, a_prod(g))
    add(1, a_sum_then_prod(G3(3, 4, 5)))
    add(1, a_sum_then_prod(G3(6, 2, 4)))
    add(1, a_gender(6, 5))
    add(1, a_gender(9, 7))
    # 2단계 (20)
    for g in [G3(3, 3, 2), G3(4, 3, 3), G3(5, 4, 3)]:
        add(2, a_pres_vice(g))
    for g in [G3(2, 3, 2), G3(4, 3, 2), G3(5, 5, 4)]:
        add(2, a_two_same(g))
    add(2, a_in_grade_pv(G3(4, 6, 3), 2))
    add(2, a_in_grade_pv(G3(5, 3, 7), 3))
    add(2, a_in_grade_two(G3(6, 4, 3), 1))
    add(2, a_in_grade_two(G3(3, 5, 8), 3))
    for g in [G3(3, 2, 4), G3(5, 4, 2), G3(4, 5, 3)]:
        add(2, a_p3_v12(g))
    add(2, a_two_grades_two_each(G3(4, 5, 3), 1, 2))
    add(2, a_two_grades_two_each(G3(3, 4, 6), 2, 3))
    add(2, a_two_grades_two_each(G3(5, 2, 4), 1, 3))
    add(2, a_two_one(G3(5, 3, 2), 2, 1) if False else a_two_one(G3(3, 5, 2), 2, 1))
    add(2, a_two_one(G3(4, 2, 6), 3, 2))
    add(2, a_relay(G3(2, 3, 2)))
    add(2, a_relay(G3(3, 3, 4)))
    # 3단계 (25)
    for g in [G3(2, 2, 2), G3(3, 2, 2), G3(3, 3, 3)]:
        add(3, a_three_roles(g))
    for g in [G3(2, 2, 3), G3(3, 3, 2), G3(4, 3, 3)]:
        add(3, a_three_same(g))
    for g in [G3(3, 2, 4), G3(4, 3, 2), G3(5, 3, 3)]:
        add(3, a_pv_same_grade(g))
    for g in [G3(2, 3, 2), G3(3, 4, 2), G3(4, 3, 5)]:
        add(3, a_pv_diff_grade(g))
    add(3, a_two_same_grade_eq(G3(4, 5, 3)))
    add(3, a_two_diff_grade_eq(G3(3, 4, 2)))
    add(3, a_two_diff_grade_eq(G3(5, 2, 4)))
    add(3, a_three_incl(G3(3, 3, 3), 2, "민준"))
    add(3, a_three_incl(G3(4, 3, 4), 1, "서연"))
    add(3, a_three_incl_excl(G3(3, 4, 3), 3, "하준", 1, "지우"))
    add(3, a_three_incl_excl(G3(4, 4, 2), 2, "도윤", 2, "수아"))
    add(3, a_three_atleast(G3(3, 3, 2), 3))
    add(3, a_three_atleast(G3(4, 2, 3), 2))
    add(3, a_three_atleast(G3(3, 4, 3), 1))
    add(3, a_leader_members(G3(3, 3, 2), 3))
    add(3, a_leader_members(G3(2, 4, 3), 2))
    add(3, a_leader_members(G3(4, 3, 3), 1))
    # 4단계 (22)
    add(4, p_one_grade(G3(4, 5, 3), 3))
    add(4, p_one_grade(G3(6, 4, 5), 2))
    add(4, p_one_not(G3(5, 3, 4), 1))
    add(4, p_one_not(G3(4, 6, 5), 2))
    add(4, p_two_both(G3(3, 4, 2), 2))
    add(4, p_two_both(G3(5, 3, 2), 1))
    add(4, p_two_same(G3(2, 3, 3)))
    add(4, p_two_same(G3(4, 2, 3)))
    add(4, p_two_same(G3(3, 4, 5)))
    add(4, p_two_diff(G3(3, 2, 3)))
    add(4, p_two_diff(G3(4, 4, 2)))
    add(4, p_named_in_two(G3(3, 2, 3), 1, "예준"))
    add(4, p_named_in_two(G3(4, 4, 4), 3, "하은"))
    add(4, p_pv_grades(G3(3, 2, 4), 1, 3))
    add(4, p_pv_grades(G3(4, 3, 3), 3, 2))
    add(4, p_three_all_grades(G3(2, 3, 3)))
    add(4, p_three_all_grades(G3(3, 3, 4)))
    add(4, p_three_atleast(G3(3, 2, 3), 1))
    add(4, p_three_atleast(G3(4, 3, 2), 3))
    add(4, p_three_atleast(G3(2, 4, 4), 1))
    add(4, p_zero(G3(4, 2, 3), 2))
    add(4, p_one(G3(3, 3, 2)))
    # 5단계 (18)
    add(5, a_three_roles_diff_grades(G3(3, 2, 4)))
    add(5, a_three_roles_diff_grades(G3(4, 3, 3)))
    add(5, a_four_all_grades(G3(2, 3, 2)))
    add(5, a_four_all_grades(G3(3, 2, 4)))
    add(5, p_three_exact2(G3(3, 2, 4), 3))
    add(5, p_three_exact2(G3(3, 5, 2), 2))
    add(5, p_three_same_grade(G3(2, 3, 4)))
    add(5, p_three_same_grade(G3(3, 3, 3)))
    add(5, p_three_incl_excl(G3(3, 3, 2), 1, "시우", 3, "유나"))
    add(5, p_three_incl_excl(G3(4, 3, 3), 2, "주원", 2, "채원"))
    add(5, a_two_diff_both({1: (2, 1), 2: (1, 2), 3: (2, 2)}))
    add(5, a_two_diff_both({1: (3, 2), 2: (2, 2), 3: (1, 3)}))
    add(5, p_mixed_gender({1: (2, 1), 2: (1, 2), 3: (2, 2)}))
    add(5, p_mixed_gender({1: (3, 1), 2: (2, 2), 3: (1, 3)}))
    add(5, a_pv_diff_no1pres(G3(3, 2, 4)))
    add(5, a_pv_diff_no1pres(G3(4, 3, 3)))
    add(5, p_pres_higher(G3(2, 3, 3)))
    add(5, p_pres_higher(G3(3, 3, 4)))
    return I


if __name__ == "__main__":
    I = build()
    from collections import Counter
    print(len(I), Counter(d["lv"] for d in I))
    for i, d in enumerate(I, 1):
        assert d["ans"] == d["chk"], (i, d["q"], d["ans"], d["chk"])
    print("all ok")
