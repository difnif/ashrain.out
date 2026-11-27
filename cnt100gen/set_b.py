# 세트 B — 주머니에서 공 꺼내기 100제
from common import *

COL = ["빨간", "파란", "노란", "흰", "검은", "초록"]


def bag(**kw):
    """bag(빨간=3, 파란=2) → [(색, i)]"""
    return [(c, i) for c, n in kw.items() for i in range(n)]


def btxt(d):
    return ", ".join(f"{c} 공 {n}개" for c, n in d.items())


def bintro(d, name="주머니"):
    return f"{name}에 {btxt(d)}가 들어 있다."


def nintro(n, start=1, name="주머니"):
    return f"{name}에 {start}부터 {n}까지의 자연수가 하나씩 적힌 공 {n - start + 1}개가 들어 있다."


def tot(d):
    return sum(d.values())


def tpos(d, extra="", head="공"):
    """포지티브 — 공의 수는 색마다 더해서(「공 3 + 4 = 7개」)"""
    return (f"{head} {plus(d.values())} = {tot(d)}개" if len(d) > 1 else f"{head} {tot(d)}개") + extra


def tpos_ab(d1, d2, mid=", ", tail2=""):
    """두 주머니 — 「A 7개(5 + 2), B 6개(2 + 4)」(한 줄에 등식을 둘 두지 않는다)"""
    f = lambda h, d: f"{h} {tot(d)}개" + (f"({plus(d.values())})" if len(d) > 1 else "")
    return f("A", d1) + mid + f("B", d2) + tail2


def ttot(d):
    """모든 공의 수 — 색이 여럿이면 더한 식"""
    return plus(d.values()) if len(d) > 1 else str(tot(d))


# ───────────── 1단계 ─────────────
def b_or(d, x, y):
    v = d[x] + d[y]
    return dict(q=f"{bintro(d)} 이 주머니에서 공 1개를 꺼낼 때, {x} 공 또는 {y} 공이 나오는 경우의 수를 구하시오.",
                ans=v, chk=cnt(bag(**d), lambda s: s[0] in (x, y)),
                pos=btxt(d), neg=f"1개만 꺼냄 · {x} 공 또는 {y} 공",
                plan="두 색이 한꺼번에 나올 수 없으므로 더한다(합의 법칙).",
                eq=[L(f"{x} 공 또는 {y} 공(합의 법칙)", plus([d[x], d[y]]), v)])


def b_mult(n, k):
    v = n // k
    return dict(q=f"{nintro(n)} 이 주머니에서 공 1개를 꺼낼 때, {k}의 배수가 적힌 공이 나오는 경우의 수를 구하시오.",
                ans=v, chk=cnt(range(1, n + 1), lambda x: x % k == 0),
                pos=f"1 ~ {n}", neg=f"{k}의 배수",
                plan=f"{k}, {2 * k}, {3 * k}, …처럼 차례로 나열하여 센다.",
                eq=[L(f"{k}의 배수", ", ".join(str(x) for x in range(k, n + 1, k))), f"{k}의 배수의 개수: {v}"])


def b_ranges(n, lo, hi):
    a = lo
    b = n - hi + 1
    v = a + b
    return dict(q=f"{nintro(n)} 이 주머니에서 공 1개를 꺼낼 때, {lo} 이하 또는 {hi} 이상의 수가 적힌 공이 나오는 경우의 수를 구하시오.",
                ans=v, chk=cnt(range(1, n + 1), lambda x: x <= lo or x >= hi),
                pos=f"1 ~ {n}", neg=f"{lo} 이하 또는 {hi} 이상 ('이하'·'이상'은 그 수를 포함)",
                plan="두 범위는 겹치지 않으므로 각각 세어 더한다.",
                eq=[f"1 ~ {lo}: {a}개", f"{hi} ~ {n}: {b}개", L(f"{lo} 이하 또는 {hi} 이상(합의 법칙)", plus([a, b]), v)])


def b_two_bags(d1, d2):
    v = tot(d1) * tot(d2)
    return dict(q=f"주머니 A에는 {btxt(d1)}, 주머니 B에는 {btxt(d2)}가 들어 있다. 두 주머니에서 공을 1개씩 꺼내는 경우의 수를 구하시오. (단, 같은 색의 공도 서로 다른 공으로 본다.)",
                ans=v, chk=cnt(PROD(bag(**d1), bag(**d2))),
                pos=tpos_ab(d1, d2), neg="주머니마다 1개씩 · 공은 모두 구별",
                plan="A에서 꺼낸 공 각각에 B의 공이 짝지어지므로 곱한다.",
                eq=[L("A에서 1개 × B에서 1개(곱의 법칙)", times([tot(d1), tot(d2)]), v)])


def b_two_bags_oe(m, n):
    o = (m + 1) // 2
    e = n // 2
    v = o * e
    return dict(q=f"주머니 A에는 1부터 {m}까지, 주머니 B에는 1부터 {n}까지의 자연수가 하나씩 적힌 공이 들어 있다. 두 주머니에서 공을 1개씩 꺼낼 때, A에서는 홀수, B에서는 짝수가 나오는 경우의 수를 구하시오.",
                ans=v, chk=cnt(PROD(range(1, m + 1), range(1, n + 1)), lambda s: s[0] % 2 == 1 and s[1] % 2 == 0),
                pos=f"A 1 ~ {m}, B 1 ~ {n}", neg="A 홀수 · B 짝수",
                plan="주머니마다 조건에 맞는 공을 세어 곱한다.",
                eq=[L(f"A 홀수 {o}개 × B 짝수 {e}개(곱의 법칙)", times([o, e]), v)])


# ───────────── 2단계 ─────────────
def b_or_overlap(n, a, b):
    l = a * b
    ca, cb, cl = n // a, n // b, n // l
    v = ca + cb - cl
    return dict(q=f"{nintro(n)} 이 주머니에서 공 1개를 꺼낼 때, {a}의 배수 또는 {b}의 배수가 적힌 공이 나오는 경우의 수를 구하시오.",
                ans=v, chk=cnt(range(1, n + 1), lambda x: x % a == 0 or x % b == 0),
                pos=f"1 ~ {n}", neg=f"{a}의 배수 또는 {b}의 배수 · 둘 다인 수는 한 번만",
                plan=f"두 배수를 더한 뒤 겹치는 {l}의 배수를 한 번 뺀다.",
                eq=[f"{a}의 배수 {ca}개 · {b}의 배수 {cb}개 · 둘 다인 {l}의 배수 {cl}개",
                    L(f"{a}의 배수 또는 {b}의 배수(둘 다인 수는 한 번 빼기)", f"{ca} + {cb} − {cl}", v)])


def b_two_bags_sum(m, n, k):
    pairs = [(x, y) for x in range(1, m + 1) for y in range(1, n + 1) if x + y == k]
    v = len(pairs)
    return dict(q=f"주머니 A에는 1부터 {m}까지, 주머니 B에는 1부터 {n}까지의 자연수가 하나씩 적힌 공이 들어 있다. 두 주머니에서 공을 1개씩 꺼낼 때, 두 수의 합이 {k}인 경우의 수를 구하시오.",
                ans=v, chk=cnt(PROD(range(1, m + 1), range(1, n + 1)), lambda s: sum(s) == k),
                pos=f"A 1 ~ {m}, B 1 ~ {n}", neg=f"합이 {k}",
                plan="(A의 수, B의 수) 순서쌍으로 A의 수가 작은 것부터 나열한다.",
                eq=[", ".join(f"({x}, {y})" for x, y in pairs), f"합이 {k}인 순서쌍의 개수: {v}"])


def b_twodigit(n):
    v = n * (n - 1)
    return dict(q=f"{nintro(n)} 이 주머니에서 공을 1개씩 두 번 꺼내어, 처음 꺼낸 공의 수를 십의 자리, 두 번째 꺼낸 공의 수를 일의 자리에 놓아 두 자리 자연수를 만든다. 만들 수 있는 두 자리 자연수의 개수를 구하시오. (단, 꺼낸 공은 다시 넣지 않는다.)",
                ans=v, chk=cnt(PERM(range(1, n + 1), 2)),
                pos=f"1 ~ {n}", neg="꺼낸 공은 다시 넣지 않음 → 같은 숫자 두 번 ✕",
                plan="십의 자리 → 일의 자리 차례로 정해 곱한다.",
                eq=[L(f"십의 자리 {n}가지 × 일의 자리 {n - 1}가지(꺼낸 공 빼고)", chain(n, 2), v)])


def b_twodigit0(n):
    v = n * n  # 0 ~ n
    return dict(q=f"주머니에 0부터 {n}까지의 정수가 하나씩 적힌 공 {n + 1}개가 들어 있다. 이 주머니에서 공을 1개씩 두 번 꺼내어, 처음 꺼낸 공의 수를 십의 자리, 두 번째 꺼낸 공의 수를 일의 자리에 놓아 두 자리 자연수를 만든다. 만들 수 있는 두 자리 자연수의 개수를 구하시오. (단, 꺼낸 공은 다시 넣지 않는다.)",
                ans=v, chk=cnt(PERM(range(0, n + 1), 2), lambda s: s[0] != 0),
                pos=f"0 ~ {n}", neg="다시 넣지 않음 · 십의 자리에 0 ✕",
                plan="제약이 많은 십의 자리부터 정한다. 일의 자리에는 0이 올 수 있다.",
                eq=[f"십의 자리: 0 제외 → {n}가지", f"일의 자리: 십의 자리 수 제외, 0 포함 → {n}가지", L("곱의 법칙", times([n, n]), v)])


def b_with_repl(d):
    t = tot(d)
    v = t * t
    return dict(q=f"{bintro(d)} 이 주머니에서 공 1개를 꺼내 색을 확인하고 다시 넣은 뒤, 다시 공 1개를 꺼낸다. 두 번 꺼내는 경우의 수를 구하시오. (단, 같은 색의 공도 서로 다른 공으로 본다.)",
                ans=v, chk=cnt(PROD(bag(**d), bag(**d))),
                pos=tpos(d), neg="다시 넣음 → 두 번째에도 공은 그대로 {0}개".format(t),
                plan="두 번 모두 꺼낼 수 있는 공이 같으므로 곱한다.",
                eq=[L(f"첫 번째 {t}개 × 두 번째 {t}개(다시 넣음)", times([t, t]), v)])


def b_sim2(d):
    t = tot(d)
    v = c2(t)
    return dict(q=f"{bintro(d)} 이 주머니에서 공 2개를 동시에 꺼내는 경우의 수를 구하시오. (단, 같은 색의 공도 서로 다른 공으로 본다.)",
                ans=v, chk=cnt(COMB(bag(**d), 2)),
                pos=tpos(d), neg="'동시에' → 순서가 없다",
                plan="차례로 꺼내는 수를 구한 뒤 2로 나눈다.",
                eq=[L(f"공 {t}개 중 2개(동시에 — 순서 없음)", c2s(t), v)])


def b_twodigit_even(n):
    e = n // 2
    v = e * (n - 1)
    return dict(q=f"{nintro(n)} 이 주머니에서 공을 1개씩 두 번 꺼내어, 처음 꺼낸 공의 수를 십의 자리, 두 번째 꺼낸 공의 수를 일의 자리에 놓아 두 자리 자연수를 만든다. 만들 수 있는 짝수의 개수를 구하시오. (단, 꺼낸 공은 다시 넣지 않는다.)",
                ans=v, chk=cnt(PERM(range(1, n + 1), 2), lambda s: s[1] % 2 == 0),
                pos=f"1 ~ {n}", neg="다시 넣지 않음 · 짝수 → 일의 자리가 짝수",
                plan="제약이 있는 일의 자리부터 정하고, 십의 자리는 남은 수에서 고른다.",
                eq=[L(f"일의 자리 짝수 {e}가지 × 십의 자리 {n - 1}가지(일의 자리 수 빼고)", times([e, n - 1]), v)])


# ───────────── 3단계 ─────────────
def b_sim2_same(d):
    terms = [c2(n) for n in d.values()]
    v = sum(terms)
    return dict(q=f"{bintro(d)} 이 주머니에서 공 2개를 동시에 꺼낼 때, 두 공의 색이 같은 경우의 수를 구하시오. (단, 같은 색의 공도 서로 다른 공으로 본다.)",
                ans=v, chk=cnt(COMB(bag(**d), 2), lambda s: s[0][0] == s[1][0]),
                pos=btxt(d), neg="동시에(순서 없음) · 같은 색",
                plan="색마다 2개를 꺼내는 수(÷ 2)를 구해 더한다.",
                eq=[L(f"{c} 공 {n}개 중 2개", c2s(n), c2(n)) for c, n in d.items()] + [L("같은 색(합의 법칙)", plus(terms), v)])


def b_sim2_diff(d):
    cs = list(d)
    pr = [(x, y) for i, x in enumerate(cs) for y in cs[i + 1:]]
    terms = [d[x] * d[y] for x, y in pr]
    v = sum(terms)
    return dict(q=f"{bintro(d)} 이 주머니에서 공 2개를 동시에 꺼낼 때, 두 공의 색이 서로 다른 경우의 수를 구하시오. (단, 같은 색의 공도 서로 다른 공으로 본다.)",
                ans=v, chk=cnt(COMB(bag(**d), 2), lambda s: s[0][0] != s[1][0]),
                pos=btxt(d), neg="동시에 · 서로 다른 색",
                plan="어느 두 색인지로 나누어, 색 짝마다 곱하고 더한다.",
                eq=[L(f"{x} 공 1개 · {y} 공 1개(곱의 법칙)", times([d[x], d[y]]), d[x] * d[y]) for x, y in pr] + ([L("서로 다른 색(합의 법칙)", plus(terms), v)] if len(pr) > 1 else []))


def b_sim3_all(d):
    a, b, c = d.values()
    v = a * b * c
    return dict(q=f"{bintro(d)} 이 주머니에서 공 3개를 동시에 꺼낼 때, 세 가지 색의 공이 모두 나오는 경우의 수를 구하시오. (단, 같은 색의 공도 서로 다른 공으로 본다.)",
                ans=v, chk=cnt(COMB(bag(**d), 3), lambda s: len({p[0] for p in s}) == 3),
                pos=btxt(d), neg="3개 · 색마다 꼭 1개씩",
                plan="세 색이 모두 나오려면 색마다 1개씩 나와야 한다 → 색마다 고르는 수를 곱한다.",
                eq=[L("색마다 1개씩(곱의 법칙)", times([a, b, c]), v)])


def bp_one(d, x):
    t = tot(d)
    v = F(d[x], t)
    return dict(q=f"{bintro(d)} 이 주머니에서 공 1개를 임의로 꺼낼 때, {x} 공이 나올 확률을 구하시오.",
                ans=v, chk=F(cnt(bag(**d), lambda s: s[0] == x), t),
                pos=tpos(d, ", 어느 공이든 나올 가능성이 같다"), neg=f"{x} 공",
                plan="(일어나는 경우의 수) ÷ (모든 경우의 수)",
                eq=[f"모든 경우 {t}", L(f"{x} 공", d[x]), pfeq(d[x], t)])


def bp_num(n, kind):
    if kind == "소수":
        ok = lambda x: x > 1 and all(x % p for p in range(2, x))
        ex = "1은 소수가 아니다."
    elif kind.endswith("의 약수"):
        m = int(kind.split("의")[0])
        ok = lambda x: m % x == 0
        ex = f"{m}의 약수를 빠짐없이 짝지어 찾는다."
    else:
        raise ValueError
    xs = [x for x in range(1, n + 1) if ok(x)]
    v = F(len(xs), n)
    return dict(q=f"{nintro(n)} 이 주머니에서 공 1개를 임의로 꺼낼 때, {kind}가 적힌 공이 나올 확률을 구하시오.",
                ans=v, chk=F(cnt(range(1, n + 1), ok), n),
                pos=f"1 ~ {n}", neg=kind,
                plan=ex,
                eq=[L(kind, ", ".join(map(str, xs))), f"{kind}의 개수: {len(xs)}", f"모든 경우 {n}", pfeq(len(xs), n)])


def bp_not(d, x):
    t = tot(d)
    v = 1 - F(d[x], t)
    return dict(q=f"{bintro(d)} 이 주머니에서 공 1개를 임의로 꺼낼 때, {x} 공이 나오지 않을 확률을 구하시오.",
                ans=v, chk=F(cnt(bag(**d), lambda s: s[0] != x), t),
                pos=tpos(d), neg=f"{x} 공이 '아님'",
                plan="1 − ({x} 공이 나올 확률)".format(x=x),
                eq=[f"모든 경우 {t}", L(f"{x} 공", d[x]), pnot(d[x], t)])


def bp_zero(d, x):
    return dict(q=f"{bintro(d)} 이 주머니에서 공 1개를 임의로 꺼낼 때, {x} 공이 나올 확률을 구하시오.",
                ans=F(0), chk=F(cnt(bag(**d), lambda s: s[0] == x), tot(d)),
                pos=btxt(d), neg=f"{x} 공은 없다",
                plan="절대 일어나지 않는 사건의 확률은 0이다.",
                eq=[L("모든 경우(공 전체)", ttot(d), tot(d)), f"{x} 공: 0개", f"확률: {{0/{tot(d)}}} = 0"])


def bp_one_sure(n):
    return dict(q=f"{nintro(n)} 이 주머니에서 공 1개를 임의로 꺼낼 때, {n + 1}보다 작은 수가 적힌 공이 나올 확률을 구하시오.",
                ans=F(1), chk=F(cnt(range(1, n + 1), lambda x: x < n + 1), n),
                pos=f"1 ~ {n}", neg=f"{n + 1}보다 작은 수",
                plan="반드시 일어나는 사건의 확률은 1이다.",
                eq=[f"모든 경우 {n}", f"{n + 1}보다 작은 수: 모든 공 {n}개", f"확률: {{{n}/{n}}} = 1"])


def bp_two_bags_both(d1, d2, x):
    t1, t2 = tot(d1), tot(d2)
    v = F(d1[x] * d2[x], t1 * t2)
    return dict(q=f"주머니 A에는 {btxt(d1)}, 주머니 B에는 {btxt(d2)}가 들어 있다. 두 주머니에서 공을 1개씩 임의로 꺼낼 때, 두 공이 모두 {x} 공일 확률을 구하시오.",
                ans=v, chk=F(cnt(PROD(bag(**d1), bag(**d2)), lambda s: s[0][0] == x and s[1][0] == x), t1 * t2),
                pos=tpos_ab(d1, d2), neg=f"둘 다 {x} 공",
                plan="모든 경우(곱)와 일어나는 경우(곱)를 세어 나눈다.",
                eq=[L(f"모든 경우(A {t1}개 × B {t2}개)", times([t1, t2]), t1 * t2), L(f"둘 다 {x} 공(A {d1[x]}개 × B {d2[x]}개)", times([d1[x], d2[x]]), d1[x] * d2[x]),
                    pfeq(d1[x] * d2[x], t1 * t2)])


def bp_repl_both(d, x):
    t = tot(d)
    v = F(d[x] ** 2, t * t)
    return dict(q=f"{bintro(d)} 이 주머니에서 공 1개를 꺼내 확인하고 다시 넣은 뒤, 다시 공 1개를 꺼낸다. 두 번 모두 {x} 공이 나올 확률을 구하시오.",
                ans=v, chk=F(cnt(PROD(bag(**d), bag(**d)), lambda s: s[0][0] == x and s[1][0] == x), t * t),
                pos=tpos(d, " · 다시 넣음"), neg=f"두 번 모두 {x} 공",
                plan="다시 넣으므로 두 번째도 처음과 똑같은 상태다.",
                eq=[L(f"모든 경우(다시 넣으니 {t}개 × {t}개)", times([t, t]), t * t), L(f"두 번 모두 {x} 공({d[x]}개 × {d[x]}개)", times([d[x], d[x]]), d[x] ** 2),
                    pfeq(d[x] ** 2, t * t)])


# ───────────── 4단계 ─────────────
def bp_sim2_both(d, x):
    t = tot(d)
    v = F(c2(d[x]), c2(t))
    return dict(q=f"{bintro(d)} 이 주머니에서 공 2개를 동시에 꺼낼 때, 2개 모두 {x} 공일 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(bag(**d), 2), lambda s: s[0][0] == x and s[1][0] == x), c2(t)),
                pos=tpos(d, " · 동시에(순서 없음)"), neg=f"2개 모두 {x} 공",
                plan="모든 경우와 일어나는 경우를 둘 다 '순서 없이(÷ 2)' 센다.",
                eq=[L(f"모든 경우(공 {t}개 중 2개)", c2s(t), c2(t)), L(f"{x} 공 {d[x]}개 중 2개", c2s(d[x]), c2(d[x])), pfeq(c2(d[x]), c2(t))])


def bp_sim2_same(d):
    t = tot(d)
    s = sum(c2(n) for n in d.values())
    v = F(s, c2(t))
    return dict(q=f"{bintro(d)} 이 주머니에서 공 2개를 동시에 꺼낼 때, 두 공의 색이 같을 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(bag(**d), 2), lambda p: p[0][0] == p[1][0]), c2(t)),
                pos=btxt(d) + " · " + tpos(d, head="모두"), neg="같은 색",
                plan="색마다 2개를 꺼내는 경우를 더한다.",
                eq=[L(f"모든 경우(공 {t}개 중 2개)", c2s(t), c2(t))] + [L(f"{c} 공 {n}개 중 2개", c2s(n), c2(n)) for c, n in d.items()]
                   + [L("같은 색(합의 법칙)", plus([c2(n) for n in d.values()]), s), pfeq(s, c2(t))])


def bp_sim2_atleast(d, x):
    t = tot(d)
    r = t - d[x]
    v = 1 - F(c2(r), c2(t))
    return dict(q=f"{bintro(d)} 이 주머니에서 공 2개를 동시에 꺼낼 때, {x} 공이 적어도 1개 나올 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(bag(**d), 2), lambda p: any(q[0] == x for q in p)), c2(t)),
                pos=tpos(d), neg=f"'적어도 1개' {x} 공",
                plan=f"{x} 공이 하나도 없는 경우를 세어 1에서 뺀다.",
                eq=[L(f"모든 경우(공 {t}개 중 2개)", c2s(t), c2(t)), L(f"{x} 공이 없음({x} 공이 아닌 {r}개 중 2개)", c2s(r), c2(r)), pnot(c2(r), c2(t))])


def bp_seq_xy(d, x, y):
    t = tot(d)
    same = x == y
    k = d[x] * (d[y] - (1 if same else 0))
    v = F(k, t * (t - 1))
    want = f"두 번 모두 {x} 공이" if same else f"첫 번째는 {x} 공, 두 번째는 {y} 공이"
    sec = f"{d[y] - 1}" if same else f"{d[y]}"
    return dict(q=f"{bintro(d)} 이 주머니에서 공을 1개씩 두 번 꺼낼 때, {want} 나올 확률을 구하시오. (단, 꺼낸 공은 다시 넣지 않는다.)",
                ans=v, chk=F(cnt(PERM(bag(**d), 2), lambda s: s[0][0] == x and s[1][0] == y), t * (t - 1)),
                pos=tpos(d), neg=f"다시 넣지 않음 → 두 번째는 {t - 1}개 중에서" + (f" · 남은 {x} 공은 {d[x] - 1}개" if same else ""),
                plan="차례가 있으므로 모든 경우도 차례로 센다.",
                eq=[L(f"모든 경우(공 {t}개에서 차례로 2번)", chain(t, 2), t * (t - 1)),
                    L(f"{x} 공 → {y} 공" + (f"(남은 {sec}개)" if same else ""), times([d[x], sec]), k), pfeq(k, t * (t - 1))])


def bp_sum_even(n):
    e, o = n // 2, (n + 1) // 2
    num = c2(e) + c2(o)
    v = F(num, c2(n))
    return dict(q=f"{nintro(n)} 이 주머니에서 공 2개를 동시에 꺼낼 때, 두 수의 합이 짝수일 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(range(1, n + 1), 2), lambda s: sum(s) % 2 == 0), c2(n)),
                pos=f"1 ~ {n} (짝수 {e}개, 홀수 {o}개)", neg="합이 짝수 = (짝, 짝) 또는 (홀, 홀)",
                plan="짝수끼리 2개, 홀수끼리 2개를 나눠 세어 더한다.",
                eq=[L(f"모든 경우(공 {n}개 중 2개)", c2s(n), c2(n)), L(f"짝수 {e}개 중 2개", c2s(e), c2(e)), L(f"홀수 {o}개 중 2개", c2s(o), c2(o)),
                    L("합이 짝수(합의 법칙)", plus([c2(e), c2(o)]), num), pfeq(num, c2(n))])


def bp_prod_even(n):
    o = (n + 1) // 2
    v = 1 - F(c2(o), c2(n))
    return dict(q=f"{nintro(n)} 이 주머니에서 공 2개를 동시에 꺼낼 때, 두 수의 곱이 짝수일 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(range(1, n + 1), 2), lambda s: s[0] * s[1] % 2 == 0), c2(n)),
                pos=f"1 ~ {n} (홀수 {o}개)", neg="곱이 짝수 = 짝수가 '적어도 1개'",
                plan="곱이 홀수(= 둘 다 홀수)인 경우를 1에서 뺀다.",
                eq=[L(f"모든 경우(공 {n}개 중 2개)", c2s(n), c2(n)), L(f"둘 다 홀수(홀수 {o}개 중 2개)", c2s(o), c2(o)), pnot(c2(o), c2(n))])


def bp_twodigit_mult3(n):
    ps = [10 * x + y for x, y in PERM(range(1, n + 1), 2)]
    good = [p for p in ps if p % 3 == 0]
    v = F(len(good), len(ps))
    return dict(q=f"{nintro(n)} 이 주머니에서 공을 1개씩 두 번 꺼내어, 처음 꺼낸 공의 수를 십의 자리, 두 번째 꺼낸 공의 수를 일의 자리에 놓아 두 자리 자연수를 만든다. 이 수가 3의 배수일 확률을 구하시오. (단, 꺼낸 공은 다시 넣지 않는다.)",
                ans=v, chk=F(cnt(PERM(range(1, n + 1), 2), lambda s: (10 * s[0] + s[1]) % 3 == 0), n * (n - 1)),
                pos=f"1 ~ {n}", neg="다시 넣지 않음 · 3의 배수 = 각 자리 숫자의 합이 3의 배수",
                plan="두 숫자의 합이 3의 배수가 되는 수를 십의 자리가 작은 것부터 나열한다.",
                eq=[L("3의 배수", ", ".join(map(str, good))), f"3의 배수의 개수: {len(good)}",
                    L(f"모든 경우(십의 자리 {n}가지 × 일의 자리 {n - 1}가지)", chain(n, 2), n * (n - 1)), pfeq(len(good), n * (n - 1))])


def bp_add_red(r, b, p_num, p_den):
    # (r + x)/(r + b + x) = p → x
    x = None
    for k in range(0, 200):
        if F(r + k, r + b + k) == F(p_num, p_den):
            x = k
            break
    assert x is not None and x > 0
    return dict(q=f"주머니에 빨간 공 {r}개와 파란 공 {b}개가 들어 있다. 이 주머니에 빨간 공을 몇 개 더 넣었더니, 공 1개를 임의로 꺼낼 때 빨간 공이 나올 확률이 {{{p_num}/{p_den}}}{josa(str(p_num), '이', '가')[len(str(p_num)):]} 되었다. 더 넣은 빨간 공은 몇 개인지 구하시오.",
                ans=x, chk=x if F(r + x, r + b + x) == F(p_num, p_den) else -1,
                pos=f"빨강 {r}, 파랑 {b} · 빨강을 $x$개 더 넣음", neg=f"빨간 공이 나올 확률 = {{{p_num}/{p_den}}}",
                plan=f"파란 공은 그대로 {b}개이므로, 파란 공이 나올 확률 {{{p_den - p_num}/{p_den}}}을 이용하면 전체 공의 수가 바로 나온다.",
                eq=[f"파란 공 {b}개가 전체의 {{{p_den - p_num}/{p_den}}}",
                    L(f"전체 공({p_den}칸 중 {p_den - p_num}칸이 파란 공 {b}개)", (f"{b} × {p_den}" if p_den - p_num == 1 else f"{b} ÷ {p_den - p_num} × {p_den}"), r + b + x),
                    L("더 넣은 빨간 공(전체 − 처음 공)", f"{r + b + x} − ({r} + {b}) = {r + b + x} − {r + b}", x)],
                unit="개")


def bp_bags_sum_ge(m, n, k):
    ps = [(x, y) for x in range(1, m + 1) for y in range(1, n + 1) if x + y >= k]
    v = F(len(ps), m * n)
    by = {}
    for x, y in ps:
        by.setdefault(x, []).append(y)
    parts = [f"A {x}: {len(ys)}가지" for x, ys in by.items()]
    return dict(q=f"주머니 A에는 1부터 {m}까지, 주머니 B에는 1부터 {n}까지의 자연수가 하나씩 적힌 공이 들어 있다. 두 주머니에서 공을 1개씩 임의로 꺼낼 때, 두 수의 합이 {k} 이상일 확률을 구하시오.",
                ans=v, chk=F(cnt(PROD(range(1, m + 1), range(1, n + 1)), lambda s: sum(s) >= k), m * n),
                pos=f"A 1 ~ {m}, B 1 ~ {n}", neg=f"합이 {k} 이상 ({k} 포함)",
                plan="A의 수로 나누어 B에 올 수 있는 수의 개수를 센다.",
                eq=[f"A가 {x}일 때 B: {', '.join(map(str, ys))} → {len(ys)}가지" for x, ys in by.items()]
                   + [L(f"합이 {k} 이상(합의 법칙)", plus([len(ys) for ys in by.values()]), len(ps)), L(f"모든 경우(A {m}개 × B {n}개)", times([m, n]), m * n),
                      pfeq(len(ps), m * n)])


# ───────────── 5단계 ─────────────
def bp_sim3_atleast(d, x):
    t = tot(d)
    r = t - d[x]
    v = 1 - F(c3(r), c3(t))
    return dict(q=f"{bintro(d)} 이 주머니에서 공 3개를 동시에 꺼낼 때, {x} 공이 적어도 1개 나올 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(bag(**d), 3), lambda p: any(q[0] == x for q in p)), c3(t)),
                pos=tpos(d, " · 3개 동시에"), neg=f"'적어도 1개' {x} 공",
                plan=f"{x} 공이 하나도 없는 경우를 세어 1에서 뺀다.",
                eq=[L(f"모든 경우(공 {t}개 중 3개)", c3s(t), c3(t)), L(f"{x} 공이 없음({x} 공이 아닌 {r}개 중 3개)", c3s(r), c3(r)), pnot(c3(r), c3(t))])


def bp_max_k(n, k):
    num = c2(k - 1)
    v = F(num, c3(n))
    return dict(q=f"{nintro(n)} 이 주머니에서 공 3개를 동시에 꺼낼 때, 꺼낸 공에 적힌 수 중 가장 큰 수가 {k}일 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(range(1, n + 1), 3), lambda s: max(s) == k), c3(n)),
                pos=f"1 ~ {n} · 3개 동시에", neg=f"가장 큰 수가 {k} → {k}는 꼭 나오고, 나머지 2개는 {k}보다 작다",
                plan=f"{k}를 넣어 두고, 1 ~ {k - 1}의 {k - 1}개 중 2개를 고른다.",
                eq=[L(f"모든 경우(공 {n}개 중 3개)", c3s(n), c3(n)), L(f"{k}를 넣고 1 ~ {k - 1} 중 2개", c2s(k - 1), num), pfeq(num, c3(n))])


def bp_sum3_odd(n):
    e, o = n // 2, (n + 1) // 2
    num = o * c2(e) + c3(o)
    v = F(num, c3(n))
    return dict(q=f"{nintro(n)} 이 주머니에서 공 3개를 동시에 꺼낼 때, 세 수의 합이 홀수일 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(range(1, n + 1), 3), lambda s: sum(s) % 2 == 1), c3(n)),
                pos=f"1 ~ {n} (홀수 {o}개, 짝수 {e}개)", neg="합이 홀수 → 홀수가 1개 또는 3개",
                plan="(홀 1, 짝 2)와 (홀 3)으로 나누어 센다.",
                eq=[L(f"모든 경우(공 {n}개 중 3개)", c3s(n), c3(n)), L(f"짝수 {e}개 중 2개", c2s(e), c2(e)), L(f"홀수 1개 · 짝수 2개(홀수 {o}개 중 1개 × 짝수 2개 고르기)", times([o, c2(e)]), o * c2(e)),
                    L(f"홀수 3개(홀수 {o}개 중 3개)", c3s(o), c3(o)), L("합이 홀수(합의 법칙)", plus([o * c2(e), c3(o)]), num), pfeq(num, c3(n))])


def bp_third_first(d, x):
    t = tot(d)
    r = t - d[x]
    num = r * (r - 1) * d[x]
    den = t * (t - 1) * (t - 2)
    v = F(num, den)
    return dict(q=f"{bintro(d)} 이 주머니에서 공을 1개씩 세 번 꺼낼 때, 세 번째에 처음으로 {x} 공이 나올 확률을 구하시오. (단, 꺼낸 공은 다시 넣지 않는다.)",
                ans=v, chk=F(cnt(PERM(bag(**d), 3), lambda s: s[0][0] != x and s[1][0] != x and s[2][0] == x), den),
                pos=tpos(d, " · 차례로 3번 · 다시 넣지 않음"), neg=f"'처음으로' → 첫째·둘째는 {x} 공이 아니고 셋째가 {x} 공",
                plan="차례가 있으므로 모든 경우도 차례로 센다.",
                eq=[L(f"모든 경우(공 {t}개에서 차례로 3번)", chain(t, 3), den), L(f"(아님, 아님, {x} 공) — {x} 공이 아닌 {r}개부터", times([r, r - 1, d[x]]), num),
                    pfeq(num, den)])


def bp_coin_bag(d1, d2, x):
    t = tot(d1)
    assert t == tot(d2)
    num = d1.get(x, 0) + d2.get(x, 0)
    v = F(num, 2 * t)
    P = [("A", s) for s in bag(**d1)] + [("B", s) for s in bag(**d2)]
    return dict(q=f"주머니 A에는 {btxt(d1)}, 주머니 B에는 {btxt(d2)}가 들어 있다. 동전 1개를 던져 앞면이 나오면 주머니 A에서, 뒷면이 나오면 주머니 B에서 공 1개를 임의로 꺼낼 때, {x} 공이 나올 확률을 구하시오.",
                ans=v, chk=F(cnt(P, lambda s: s[1][0] == x), len(P)),
                pos=f"동전 2가지 · 두 주머니 모두 공 {ttot(d1)} = {t}개" if len(d1) > 1 else f"동전 2가지 · 두 주머니 모두 공 {t}개", neg=f"{x} 공",
                plan=f"두 주머니의 공 수가 {t}개로 같으므로, (동전 면, 공) {2 * t}가지가 모두 같은 가능성이다.",
                eq=[L(f"모든 경우(동전 2가지 × 공 {t}개)", times([2, t]), 2 * t), L(f"{x} 공(A의 {d1.get(x, 0)}개 + B의 {d2.get(x, 0)}개)", plus([d1.get(x, 0), d2.get(x, 0)]), num),
                    pfeq(num, 2 * t)])


def bp_move(dA, dB, x):
    A, B = bag(**dA), [("B",) + s for s in bag(**dB)]
    tA, tB = len(A), len(B)
    num = 0
    total = 0
    for m in A:
        nb = B + [("A",) + m]
        for s in nb:
            total += 1
            if s[1] == x:
                num += 1
    v = F(num, total)
    rA, rB = dA.get(x, 0), dB.get(x, 0)
    eq_num = rA * (rB + 1) + (tA - rA) * rB
    assert eq_num == num and total == tA * (tB + 1)
    return dict(q=f"주머니 A에는 {btxt(dA)}, 주머니 B에는 {btxt(dB)}가 들어 있다. 주머니 A에서 공 1개를 임의로 꺼내 주머니 B에 넣은 뒤, 주머니 B에서 공 1개를 임의로 꺼낼 때, {x} 공이 나올 확률을 구하시오.",
                ans=F(eq_num, tA * (tB + 1)), chk=v,
                pos=tpos_ab(dA, dB, " · ", f" → 옮긴 뒤 B {tB + 1}개"), neg=f"B에서 꺼낸 공이 {x} 공",
                plan=f"옮기는 공 {tA}가지 각각에 B에서 꺼내는 공 {tB + 1}가지가 짝지어진다. 옮긴 공이 {x} 공인지 아닌지로 나눈다.",
                eq=[L(f"모든 경우 — A에서 옮길 공 {tA}개 × 옮긴 뒤 B의 공 {tB + 1}개", times([tA, tB + 1]), total),
                    L(f"{x} 공을 옮김 — A의 {x} 공 {rA}개 × 옮긴 뒤 B의 {x} 공 {rB + 1}개", times([rA, rB + 1]), rA * (rB + 1)),
                    L(f"다른 색을 옮김 — A의 다른 색 {tA - rA}개 × B의 {x} 공 {rB}개 그대로", times([tA - rA, rB]), (tA - rA) * rB),
                    L(f"B에서 {x} 공(합의 법칙)", plus([rA * (rB + 1), (tA - rA) * rB]), num), pfeq(num, total)])


def bp_sim3_allcol(d):
    t = tot(d)
    a, b, c = d.values()
    v = F(a * b * c, c3(t))
    return dict(q=f"{bintro(d)} 이 주머니에서 공 3개를 동시에 꺼낼 때, 세 공의 색이 모두 다를 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(bag(**d), 3), lambda p: len({q[0] for q in p}) == 3), c3(t)),
                pos=btxt(d) + " · " + tpos(d, head="모두"), neg="세 색이 모두 다름 = 색마다 1개씩",
                plan="색마다 1개씩 고르는 수를 곱한다.",
                eq=[L(f"모든 경우(공 {t}개 중 3개)", c3s(t), c3(t)), L("색마다 1개씩(곱의 법칙)", times([a, b, c]), a * b * c), pfeq(a * b * c, c3(t))])


def bp_sim3_some_same(d):
    t = tot(d)
    a, b, c = d.values()
    v = 1 - F(a * b * c, c3(t))
    return dict(q=f"{bintro(d)} 이 주머니에서 공 3개를 동시에 꺼낼 때, 같은 색의 공이 적어도 2개 나올 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(bag(**d), 3), lambda p: len({q[0] for q in p}) < 3), c3(t)),
                pos=btxt(d) + " · " + tpos(d, head="모두"), neg="'적어도 2개' 같은 색 ↔ 반대는 세 색이 모두 다름",
                plan="세 색이 모두 다를 확률을 1에서 뺀다.",
                eq=[L(f"모든 경우(공 {t}개 중 3개)", c3s(t), c3(t)), L("세 색이 모두 다름(색마다 1개씩)", times([a, b, c]), a * b * c), pnot(a * b * c, c3(t))])


def bp_diff_ge(n, k):
    ps = [s for s in COMB(range(1, n + 1), 2) if s[1] - s[0] >= k]
    small = c2(n) - len(ps)
    v = F(len(ps), c2(n))
    return dict(q=f"{nintro(n)} 이 주머니에서 공 2개를 동시에 꺼낼 때, 두 수의 차가 {k} 이상일 확률을 구하시오.",
                ans=v, chk=F(cnt(COMB(range(1, n + 1), 2), lambda s: s[1] - s[0] >= k), c2(n)),
                pos=f"1 ~ {n}", neg=f"차가 {k} 이상",
                plan=f"반대(차가 1 ~ {k - 1})를 센다. 차가 $d$인 짝은 {n} − $d$개다.",
                eq=[L(f"모든 경우(공 {n}개 중 2개)", c2s(n), c2(n))] + [L(f"차가 {dd}인 짝(1과 {1 + dd}, 2와 {2 + dd}, …)", f"{n} − {dd}", n - dd) for dd in range(1, k)]
                   + [L(f"차가 {k - 1} 이하(합의 법칙)", plus([n - dd for dd in range(1, k)]), small), pnot(small, c2(n))])


def build():
    I = []

    def add(lv, d):
        d["lv"] = lv
        I.append(d)

    D = lambda **kw: kw
    # 1단계 (15)
    add(1, b_or(D(빨간=3, 파란=4, 노란=2), "빨간", "파란"))
    add(1, b_or(D(빨간=5, 흰=2, 검은=6), "흰", "검은"))
    add(1, b_or(D(파란=4, 노란=7, 초록=3), "파란", "초록"))
    add(1, b_mult(20, 3))
    add(1, b_mult(30, 4))
    add(1, b_mult(25, 6))
    add(1, b_ranges(15, 3, 13))
    add(1, b_ranges(20, 4, 17))
    add(1, b_ranges(30, 5, 26))
    add(1, b_two_bags(D(빨간=2, 파란=3), D(노란=4, 흰=1)))
    add(1, b_two_bags(D(빨간=4, 파란=2), D(빨간=3, 파란=3)))
    add(1, b_two_bags(D(흰=5, 검은=2), D(흰=2, 검은=4)))
    add(1, b_two_bags_oe(5, 6))
    add(1, b_two_bags_oe(7, 8))
    add(1, b_two_bags_oe(9, 4))
    # 2단계 (20)
    add(2, b_or_overlap(20, 2, 3))
    add(2, b_or_overlap(30, 3, 5))
    add(2, b_or_overlap(40, 4, 5))
    add(2, b_two_bags_sum(5, 5, 7))
    add(2, b_two_bags_sum(6, 4, 6))
    add(2, b_two_bags_sum(8, 6, 10))
    add(2, b_twodigit(5))
    add(2, b_twodigit(7))
    add(2, b_twodigit(9))
    add(2, b_twodigit0(4))
    add(2, b_twodigit0(5))
    add(2, b_twodigit0(7))
    add(2, b_with_repl(D(빨간=3, 파란=2)))
    add(2, b_with_repl(D(흰=4, 검은=3, 노란=1)))
    add(2, b_sim2(D(빨간=3, 파란=3)))
    add(2, b_sim2(D(흰=4, 검은=3)))
    add(2, b_sim2(D(빨간=5, 파란=2, 노란=3)))
    add(2, b_twodigit_even(5))
    add(2, b_twodigit_even(6))
    add(2, b_twodigit_even(8))
    # 3단계 (25)
    add(3, b_sim2_same(D(빨간=3, 파란=2)))
    add(3, b_sim2_same(D(빨간=4, 파란=3, 노란=2)))
    add(3, b_sim2_same(D(흰=5, 검은=4, 초록=3)))
    add(3, b_sim2_diff(D(빨간=3, 파란=4)))
    add(3, b_sim2_diff(D(빨간=2, 파란=3, 노란=4)))
    add(3, b_sim2_diff(D(흰=5, 검은=2, 노란=3)))
    add(3, b_sim3_all(D(빨간=2, 파란=3, 노란=4)))
    add(3, b_sim3_all(D(흰=3, 검은=3, 초록=5)))
    add(3, b_sim3_all(D(빨간=4, 파란=5, 노란=6)))
    add(3, bp_one(D(빨간=3, 파란=5), "빨간"))
    add(3, bp_one(D(빨간=4, 파란=6, 노란=2), "파란"))
    add(3, bp_one(D(흰=6, 검은=4, 초록=5), "흰"))
    add(3, bp_num(20, "소수"))
    add(3, bp_num(15, "24의 약수"))
    add(3, bp_num(30, "36의 약수"))
    add(3, bp_not(D(빨간=3, 파란=4, 노란=5), "노란"))
    add(3, bp_not(D(흰=2, 검은=7, 초록=1), "검은"))
    add(3, bp_zero(D(빨간=4, 파란=3), "노란"))
    add(3, bp_one_sure(12))
    add(3, bp_two_bags_both(D(빨간=2, 파란=3), D(빨간=4, 파란=2), "빨간"))
    add(3, bp_two_bags_both(D(흰=3, 검은=5), D(흰=2, 검은=2), "검은"))
    add(3, bp_two_bags_both(D(빨간=1, 노란=4, 파란=3), D(빨간=3, 노란=2, 파란=1), "노란"))
    add(3, bp_repl_both(D(빨간=2, 파란=3), "빨간"))
    add(3, bp_repl_both(D(흰=4, 검은=2), "흰"))
    add(3, bp_repl_both(D(빨간=3, 파란=3, 노란=2), "파란"))
    # 4단계 (22)
    add(4, bp_sim2_both(D(빨간=3, 파란=2), "빨간"))
    add(4, bp_sim2_both(D(빨간=4, 파란=5), "파란"))
    add(4, bp_sim2_both(D(흰=5, 검은=3, 노란=2), "흰"))
    add(4, bp_sim2_same(D(빨간=4, 파란=3)))
    add(4, bp_sim2_same(D(빨간=2, 파란=3, 노란=4)))
    add(4, bp_sim2_same(D(흰=5, 검은=5)))
    add(4, bp_sim2_atleast(D(빨간=2, 파란=4), "빨간"))
    add(4, bp_sim2_atleast(D(빨간=3, 파란=3, 노란=2), "노란"))
    add(4, bp_sim2_atleast(D(흰=4, 검은=6), "흰"))
    add(4, bp_seq_xy(D(빨간=3, 파란=2), "빨간", "파란"))
    add(4, bp_seq_xy(D(빨간=4, 파란=3, 노란=1), "파란", "파란"))
    add(4, bp_seq_xy(D(흰=5, 검은=4), "검은", "흰"))
    add(4, bp_sum_even(8))
    add(4, bp_sum_even(9))
    add(4, bp_prod_even(7))
    add(4, bp_prod_even(10))
    add(4, bp_twodigit_mult3(4))
    add(4, bp_twodigit_mult3(6))
    add(4, bp_add_red(2, 6, 1, 2))
    add(4, bp_add_red(3, 4, 2, 3))
    add(4, bp_bags_sum_ge(4, 5, 8))
    add(4, bp_bags_sum_ge(6, 6, 10))
    # 5단계 (18)
    add(5, bp_sim3_atleast(D(빨간=3, 파란=4), "빨간"))
    add(5, bp_sim3_atleast(D(빨간=2, 파란=3, 노란=4), "빨간"))
    add(5, bp_max_k(7, 5))
    add(5, bp_max_k(10, 7))
    add(5, bp_sum3_odd(6))
    add(5, bp_sum3_odd(9))
    add(5, bp_third_first(D(빨간=2, 파란=4), "빨간"))
    add(5, bp_third_first(D(빨간=3, 파란=3, 노란=1), "노란"))
    add(5, bp_coin_bag(D(빨간=2, 파란=4), D(빨간=5, 파란=1), "빨간"))
    add(5, bp_coin_bag(D(흰=3, 검은=5), D(흰=6, 검은=2), "검은"))
    add(5, bp_move(D(빨간=2, 파란=3), D(빨간=3, 파란=1), "빨간"))
    add(5, bp_move(D(흰=1, 검은=3), D(흰=2, 검은=4), "흰"))
    add(5, bp_sim3_allcol(D(빨간=2, 파란=2, 노란=3)))
    add(5, bp_sim3_allcol(D(빨간=3, 파란=4, 노란=5)))
    add(5, bp_sim3_some_same(D(빨간=2, 파란=3, 노란=3)))
    add(5, bp_sim3_some_same(D(흰=4, 검은=4, 초록=2)))
    add(5, bp_diff_ge(8, 3))
    add(5, bp_diff_ge(10, 4))
    return I


if __name__ == "__main__":
    I = build()
    from collections import Counter
    print(len(I), Counter(d["lv"] for d in I))
    for i, d in enumerate(I, 1):
        assert d["ans"] == d["chk"], (i, d["q"], d["ans"], d["chk"])
    print("all ok")
