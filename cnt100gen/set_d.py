# 세트 D — 한 줄로 세우기 100제 (이웃 · 양 끝 · 섞기)
from common import *
from math import factorial as fac

CTX = ["사진을 찍으려고", "급식 줄을 서려고", "발표 순서를 정하려고", "버스를 기다리며", "놀이기구를 타려고",
       "졸업 사진을 찍으려고", "계주 순서를 정하려고", "공연장 앞줄에 앉으려고", "체육 시간에", "단체 사진을 찍으려고"]
_ci = [0]


def ctx():
    c = CTX[_ci[0] % len(CTX)]
    _ci[0] += 1
    return c


def P(n):
    return [chr(65 + i) for i in range(n)]


def ptxt(n):
    return ", ".join(P(n)) + f" {n}명"


def lines(items):
    return list(PERM(items))


def adj(p, x, y):
    i, j = p.index(x), p.index(y)
    return abs(i - j) == 1


def fac_s(n):
    return " × ".join(str(i) for i in range(n, 0, -1)) if n > 1 else "1"


def mk(q, ans, chk, pos, neg, plan, eq):
    import sys
    f = sys._getframe(1)        # 모니터 그림용: 어느 틀(함수)과 수(n, b, g, k)로 만든 문항인지
    prm = {k: v for k, v in f.f_locals.items() if k in ("n", "b", "g", "k") and isinstance(v, int)}
    return dict(q=q, ans=ans, chk=chk, pos=pos, neg=neg, plan=plan, eq=eq, tpl=f.f_code.co_name, prm=prm)


# ───────── 1단계 ─────────
def d_all(n):
    v = fac(n)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 서는 경우의 수를 구하시오.", v, cnt(lines(P(n))),
              f"{n}명", "모두 한 줄 · 한 사람은 한 자리",
              "맨 앞 자리부터 설 사람을 정하면 한 명씩 줄어든다.", [L(f"{n}명을 한 줄로", fac_s(n), v)])


def d_choose(n, k):
    v = nP(n, k)
    return mk(f"{ptxt(n)} 중에서 {k}명을 뽑아 {ctx()} 한 줄로 세우는 경우의 수를 구하시오.", v, cnt(PERM(P(n), k)),
              f"{n}명 중 {k}명", f"자리는 {k}개뿐",
              f"자리 {k}개를 앞에서부터 채운다.", [L(f"{n}명 중 {k}명을 뽑아 한 줄로(앞자리부터 차례로)", chain(n, k), v)])


def nP(n, k):
    v = 1
    for i in range(k):
        v *= n - i
    return v


def d_fixed_front(n):
    v = fac(n - 1)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A가 맨 앞에 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: p[0] == "A"),
              f"{n}명", "A는 맨 앞에 고정",
              f"A를 먼저 세워 두면 나머지 {n - 1}명만 줄 세우면 된다.", [L(f"A를 빼고 남은 {n - 1}명을 한 줄로", fac_s(n - 1), v)])


def d_fixed_mid(n):
    m = (n + 1) // 2
    v = fac(n - 1)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, C가 한가운데({m}번째)에 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: p[m - 1] == "C"),
              f"{n}명", f"C는 {m}번째에 고정",
              f"C를 고정하면 남은 자리 {n - 1}개에 {n - 1}명.", [L(f"C를 빼고 남은 {n - 1}명을 한 줄로", fac_s(n - 1), v)])


def d_front_back(n):
    v = fac(n - 2)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A는 맨 앞, B는 맨 뒤에 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: p[0] == "A" and p[-1] == "B"),
              f"{n}명", "A 맨 앞 · B 맨 뒤",
              f"두 사람을 고정하면 가운데 {n - 2}자리만 남는다.", [L(f"A, B를 빼고 가운데 {n - 2}명을 한 줄로", fac_s(n - 2), v)])


# ───────── 2단계 ─────────
def d_ends_AB(n):
    v = 2 * fac(n - 2)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A와 B가 양 끝에 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: {p[0], p[-1]} == {"A", "B"}),
              f"{n}명", "A와 B가 양 끝 (A가 앞일 수도, 뒤일 수도)",
              "양 끝에 A, B를 세우는 2가지 각각에 가운데를 세운다.",
              [L("양 끝에 A, B(2명을 한 줄로)", "2 × 1", 2), L(f"가운데 {n - 2}명을 한 줄로", fac_s(n - 2), fac(n - 2)), L("곱의 법칙", times([2, fac(n - 2)]), v)])


def d_A_an_end(n):
    v = 2 * fac(n - 1)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A가 맨 앞 또는 맨 뒤에 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: p[0] == "A" or p[-1] == "A"),
              f"{n}명", "A는 양 끝 중 한 곳",
              "A가 맨 앞인 경우와 맨 뒤인 경우는 동시에 일어나지 않으므로 더한다.",
              [L(f"A가 맨 앞 — 남은 {n - 1}명을 한 줄로", fac_s(n - 1), fac(n - 1)), L(f"A가 맨 뒤 — 남은 {n - 1}명을 한 줄로", fac_s(n - 1), fac(n - 1)),
               L("합의 법칙", plus([fac(n - 1), fac(n - 1)]), v)])


def d_A_not_front(n):
    v = fac(n) - fac(n - 1)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A가 맨 앞에 서지 않는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: p[0] != "A"),
              f"{n}명", "A는 맨 앞 ✕",
              "전체에서 A가 맨 앞인 경우를 뺀다. (맨 앞에 A 말고 다른 사람을 먼저 세워도 된다.)",
              [L(f"전체({n}명을 한 줄로)", fac_s(n), fac(n)), L(f"A가 맨 앞(남은 {n - 1}명을 한 줄로)", fac_s(n - 1), fac(n - 1)),
               L("A가 맨 앞이 아님(전체 − A가 맨 앞)", f"{fac(n)} − {fac(n - 1)}", v),
               L(f"다른 방법 — 맨 앞에 A가 아닌 {n - 1}명 중 1명 × 나머지 {n - 1}명을 한 줄로", times([n - 1, fac(n - 1)]), v)])


def gl(b, g):
    return [("남", i) for i in range(b)] + [("여", i) for i in range(g)]


def d_ends_boys(b, g):
    n = b + g
    v = b * (b - 1) * fac(n - 2)
    return mk(f"남학생 {b}명과 여학생 {g}명이 {ctx()} 한 줄로 설 때, 양 끝에 남학생이 서는 경우의 수를 구하시오.", v,
              cnt(lines(gl(b, g)), lambda p: p[0][0] == "남" and p[-1][0] == "남"),
              f"남 {b} · 여 {g} → 모두 {b} + {g} = {b + g}명 (모두 서로 다른 사람)", "양 끝은 남학생",
              "양 끝부터 남학생으로 채우고, 가운데에 남은 사람을 세운다.",
              [L(f"양 끝(남학생 {b}명 중 2명을 차례로)", chain(b, 2), b * (b - 1)), L(f"가운데 남은 {n - 2}명을 한 줄로", fac_s(n - 2), fac(n - 2)),
               L("곱의 법칙", times([b * (b - 1), fac(n - 2)]), v)])


def d_ends_girl_one(b, g):
    n = b + g
    v = g * b * fac(n - 2) * 2
    return mk(f"남학생 {b}명과 여학생 {g}명이 {ctx()} 한 줄로 설 때, 한쪽 끝에는 남학생, 다른 쪽 끝에는 여학생이 서는 경우의 수를 구하시오.", v,
              cnt(lines(gl(b, g)), lambda p: {p[0][0], p[-1][0]} == {"남", "여"}),
              f"남 {b} · 여 {g} → 모두 {b} + {g} = {b + g}명", "양 끝이 (남, 여) 또는 (여, 남)",
              "맨 앞이 남·맨 뒤가 여인 경우와 그 반대를 나눠 세어 더한다.",
              [L(f"가운데 {n - 2}명을 한 줄로", fac_s(n - 2), fac(n - 2)),
               L(f"(남, 여) — 맨 앞 남학생 {b}명 중 1명 × 맨 뒤 여학생 {g}명 중 1명 × 가운데", times([b, g, fac(n - 2)]), b * g * fac(n - 2)),
               L(f"(여, 남) — 맨 앞 여학생 {g}명 중 1명 × 맨 뒤 남학생 {b}명 중 1명 × 가운데", times([g, b, fac(n - 2)]), b * g * fac(n - 2)),
               L("합의 법칙", plus([b * g * fac(n - 2)] * 2), v)])


# ───────── 3단계 ─────────
def d_adj2(n):
    v = fac(n - 1) * 2
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A와 B가 이웃하여 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: adj(p, "A", "B")),
              f"{n}명", "A와 B는 이웃",
              f"A, B를 한 묶음으로 보면 {n - 1}개를 세우고, 묶음 안 순서 2가지를 곱한다.",
              [L(f"A, B 묶음 포함 {n - 1}개를 한 줄로", fac_s(n - 1), fac(n - 1)), L("묶음 안 A, B 자리 바꾸기", "2 × 1", 2), L("곱의 법칙", times([fac(n - 1), 2]), v)])


def d_adj3(n):
    v = fac(n - 2) * 6
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A, B, C가 이웃하여 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: max(p.index(x) for x in "ABC") - min(p.index(x) for x in "ABC") == 2),
              f"{n}명", "A, B, C 세 사람이 붙어 선다",
              f"세 사람을 한 묶음으로 보면 {n - 2}개를 세우고, 묶음 안 순서 3 × 2 × 1을 곱한다.",
              [L(f"A, B, C 묶음 포함 {n - 2}개를 한 줄로", fac_s(n - 2), fac(n - 2)), L("묶음 안 A, B, C를 한 줄로", "3 × 2 × 1", 6), L("곱의 법칙", times([fac(n - 2), 6]), v)])


def d_not_adj(n):
    a = fac(n - 1) * 2
    v = fac(n) - a
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A와 B가 이웃하지 않게 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: not adj(p, "A", "B")),
              f"{n}명", "A와 B는 이웃 ✕",
              "전체에서 이웃하는 경우를 뺀다.",
              [L(f"전체({n}명을 한 줄로)", fac_s(n), fac(n)), L(f"이웃 — A, B 묶음 포함 {n - 1}개를 한 줄로", fac_s(n - 1), fac(n - 1)),
               L("이웃 — 묶음 안 A, B 자리 바꾸기", "2 × 1", 2), L("이웃(곱의 법칙)", times([fac(n - 1), 2]), a), L("이웃하지 않음(전체 − 이웃)", f"{fac(n)} − {a}", v)])


def d_adj_order(n):
    v = fac(n - 1)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, B가 A의 바로 뒤에 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: p.index("B") == p.index("A") + 1),
              f"{n}명", "A 바로 뒤에 B → (A B) 순서가 정해진 묶음",
              "묶음 안 순서가 정해져 있으므로 2를 곱하지 않는다.", [L(f"(A B) 묶음 포함 {n - 1}개를 한 줄로 — 묶음 안 순서는 정해짐", fac_s(n - 1), v)])


def d_groups(b, g):
    v = 2 * fac(b) * fac(g)
    return mk(f"남학생 {b}명과 여학생 {g}명이 {ctx()} 한 줄로 설 때, 남학생은 남학생끼리, 여학생은 여학생끼리 이웃하여 서는 경우의 수를 구하시오.", v,
              cnt(lines(gl(b, g)), lambda p: sum(p[i][0] != p[i + 1][0] for i in range(len(p) - 1)) == 1),
              f"남 {b} · 여 {g}", "남끼리 한 덩어리 · 여끼리 한 덩어리",
              "(남 묶음, 여 묶음) 두 덩어리의 순서 2가지 × 묶음 안 순서.",
              [L("남학생 묶음 · 여학생 묶음, 2개를 한 줄로", "2 × 1", 2), L(f"남학생 묶음 안 {b}명을 한 줄로", fac_s(b), fac(b)),
               L(f"여학생 묶음 안 {g}명을 한 줄로", fac_s(g), fac(g)), L("곱의 법칙", times([2, fac(b), fac(g)]), v)])


def d_girls_together(b, g):
    v = fac(b + 1) * fac(g)
    return mk(f"남학생 {b}명과 여학생 {g}명이 {ctx()} 한 줄로 설 때, 여학생끼리 모두 이웃하여 서는 경우의 수를 구하시오.", v,
              cnt(lines(gl(b, g)), lambda p: (lambda ix: max(ix) - min(ix) == g - 1)([i for i, x in enumerate(p) if x[0] == "여"])),
              f"남 {b} · 여 {g}", "여학생 모두 붙어 선다",
              f"여학생 묶음 1개 + 남학생 {b}명 = {b + 1}개를 세우고, 묶음 안 순서를 곱한다.",
              [L(f"여학생 묶음과 남학생 {b}명, {b + 1}개를 한 줄로", fac_s(b + 1), fac(b + 1)), L(f"묶음 안 여학생 {g}명을 한 줄로", fac_s(g), fac(g)),
               L("곱의 법칙", times([fac(b + 1), fac(g)]), v)])


# ───────── 4단계 (섞기 · 확률) ─────────
def d_ends_and_adj(n):
    v = 2 * fac(n - 3) * 2
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A와 B는 양 끝에 서고, C와 D는 이웃하여 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: {p[0], p[-1]} == {"A", "B"} and adj(p, "C", "D")),
              f"{n}명", "A, B 양 끝 · C, D 이웃",
              f"양 끝(2가지)을 먼저 정하고, 가운데 {n - 2}자리에서 C, D를 묶어 {n - 3}개를 세운 뒤 묶음 안 2가지.",
              [L("양 끝에 A, B(2명을 한 줄로)", "2 × 1", 2), L(f"가운데 — C, D 묶음 포함 {n - 3}개를 한 줄로", fac_s(n - 3), fac(n - 3)),
               L("가운데 — 묶음 안 C, D 자리 바꾸기", "2 × 1", 2), L("곱의 법칙", times([2, fac(n - 3), 2]), v)])


def d_front_and_adj(n):
    v = fac(n - 2) * 2
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A는 맨 앞에 서고, B와 C는 이웃하여 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: p[0] == "A" and adj(p, "B", "C")),
              f"{n}명", "A 맨 앞 · B, C 이웃",
              f"A를 고정하면 남은 {n - 1}명 중 B, C를 묶어 {n - 2}개를 세우고 2를 곱한다.",
              [L(f"A를 맨 앞에 두고, B, C 묶음 포함 {n - 2}개를 한 줄로", fac_s(n - 2), fac(n - 2)), L("묶음 안 B, C 자리 바꾸기", "2 × 1", 2),
               L("곱의 법칙", times([fac(n - 2), 2]), v)])


def d_pair_at_end(n):
    v = 2 * 2 * fac(n - 2)
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A와 B가 이웃하면서 둘 중 한 명이 맨 앞 또는 맨 뒤에 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: adj(p, "A", "B") and ({p[0], p[1]} == {"A", "B"} or {p[-1], p[-2]} == {"A", "B"})),
              f"{n}명", "A, B 이웃 · 그 묶음이 한쪽 끝에 닿는다",
              "묶음이 앞쪽 끝인지 뒤쪽 끝인지(2) × 묶음 안 순서(2) × 나머지 줄 세우기.",
              [L("묶음이 맨 앞 또는 맨 뒤", 2), L("묶음 안 A, B 자리 바꾸기", "2 × 1", 2), L(f"나머지 {n - 2}명을 한 줄로", fac_s(n - 2), fac(n - 2)),
               L("곱의 법칙", times([2, 2, fac(n - 2)]), v)])


def d_alt(b, g):
    if b == g:
        v = 2 * fac(b) * fac(g)
        eq = [L("꼴 — 남이 앞(남여남여…) 또는 여가 앞(여남여남…)", 2), L(f"남학생 {b}명을 남학생 자리에 한 줄로", fac_s(b), fac(b)),
              L(f"여학생 {g}명을 여학생 자리에 한 줄로", fac_s(g), fac(g)), L("곱의 법칙", times([2, fac(b), fac(g)]), v)]
        plan = "자리를 (남, 여, 남, 여, …) 꼴로 먼저 정한다. 수가 같으면 남녀 누가 앞에 서든 된다."
    else:
        v = fac(b) * fac(g)
        eq = ["꼴 — 남여남…남 하나뿐", L(f"남학생 {b}명을 남학생 자리에 한 줄로", fac_s(b), fac(b)), L(f"여학생 {g}명을 여학생 자리에 한 줄로", fac_s(g), fac(g)),
              L("곱의 법칙", times([fac(b), fac(g)]), v)]
        plan = "남학생이 1명 더 많으면 양 끝이 남학생인 (남, 여, 남, …, 남) 꼴 하나뿐이다."
    return mk(f"남학생 {b}명과 여학생 {g}명이 {ctx()} 한 줄로 설 때, 남학생과 여학생이 번갈아 서는 경우의 수를 구하시오.", v,
              cnt(lines(gl(b, g)), lambda p: all(p[i][0] != p[i + 1][0] for i in range(len(p) - 1))),
              f"남 {b} · 여 {g}", "남녀가 번갈아 (같은 성별끼리 이웃 ✕)", plan, eq)


def d_girls_ends_boys_adj(b):
    g = 3
    n = b + g
    v = 3 * 2 * 2 * fac(b)
    return mk(f"남학생 {b}명과 여학생 3명이 {ctx()} 한 줄로 설 때, 양 끝에는 여학생이 서고 남학생끼리는 모두 이웃하여 서는 경우의 수를 구하시오.", v,
              cnt(lines(gl(b, g)), lambda p: p[0][0] == "여" and p[-1][0] == "여" and (lambda ix: max(ix) - min(ix) == b - 1)([i for i, x in enumerate(p) if x[0] == "남"])),
              f"남 {b} · 여 3", "양 끝 여학생 · 남학생끼리 이웃",
              "양 끝 여학생(3 × 2)을 먼저 세우고, 가운데에 남은 여학생 1명과 남학생 묶음을 세운 뒤 묶음 안 순서.",
              [L("양 끝 여학생(여학생 3명 중 2명을 차례로)", "3 × 2", 6), L("가운데 — 남은 여학생 1명과 남학생 묶음, 2개를 한 줄로", "2 × 1", 2),
               L(f"묶음 안 남학생 {b}명을 한 줄로", fac_s(b), fac(b)), L("곱의 법칙", times([6, 2, fac(b)]), v)])


def p_adj(n):
    a = fac(n - 1) * 2
    v = F(a, fac(n))
    return mk(f"{ptxt(n)}이 제비뽑기로 자리를 정해 한 줄로 설 때, A와 B가 이웃하여 설 확률을 구하시오.", v,
              F(cnt(lines(P(n)), lambda p: adj(p, "A", "B")), fac(n)),
              f"{n}명 · 모든 자리 배치가 같은 가능성", "A와 B 이웃",
              "이웃하는 경우의 수 ÷ 모든 경우의 수.",
              [L(f"모든 경우({n}명을 한 줄로)", fac_s(n), fac(n)), L(f"이웃 — A, B 묶음 포함 {n - 1}개를 한 줄로", fac_s(n - 1), fac(n - 1)),
               L("이웃 — 묶음 안 A, B 자리 바꾸기", "2 × 1", 2), L("이웃(곱의 법칙)", times([fac(n - 1), 2]), a), pfeq(a, fac(n))])


def p_ends(n):
    a = 2 * fac(n - 2)
    v = F(a, fac(n))
    return mk(f"{ptxt(n)}이 제비뽑기로 자리를 정해 한 줄로 설 때, A와 B가 양 끝에 설 확률을 구하시오.", v,
              F(cnt(lines(P(n)), lambda p: {p[0], p[-1]} == {"A", "B"}), fac(n)),
              f"{n}명", "A와 B가 양 끝",
              "양 끝에 A, B(2가지) × 가운데 줄 세우기.",
              [L(f"모든 경우({n}명을 한 줄로)", fac_s(n), fac(n)), L("양 끝에 A, B(2명을 한 줄로)", "2 × 1", 2), L(f"가운데 {n - 2}명을 한 줄로", fac_s(n - 2), fac(n - 2)),
               L("곱의 법칙", times([2, fac(n - 2)]), a), pfeq(a, fac(n))])


def p_end_and_adj(n):
    a = fac(n - 2) * 2
    v = F(a, fac(n))
    return mk(f"{ptxt(n)}이 제비뽑기로 자리를 정해 한 줄로 설 때, A가 맨 앞에 서고 B와 C가 이웃하여 설 확률을 구하시오.", v,
              F(cnt(lines(P(n)), lambda p: p[0] == "A" and adj(p, "B", "C")), fac(n)),
              f"{n}명", "A 맨 앞 · B, C 이웃",
              f"A를 고정하고 B, C를 묶어 {n - 2}개를 세운 뒤 2를 곱한다.",
              [L(f"모든 경우({n}명을 한 줄로)", fac_s(n), fac(n)), L(f"A를 맨 앞에 두고, B, C 묶음 포함 {n - 2}개를 한 줄로", fac_s(n - 2), fac(n - 2)),
               L("묶음 안 B, C 자리 바꾸기", "2 × 1", 2), L("곱의 법칙", times([fac(n - 2), 2]), a), pfeq(a, fac(n))])


# ───────── 5단계 ─────────
def d_gap(b, g):
    v = fac(b) * nP(b + 1, g)
    return mk(f"남학생 {b}명과 여학생 {g}명이 {ctx()} 한 줄로 설 때, 여학생끼리는 서로 이웃하지 않게 서는 경우의 수를 구하시오.", v,
              cnt(lines(gl(b, g)), lambda p: all(not (p[i][0] == "여" and p[i + 1][0] == "여") for i in range(len(p) - 1))),
              f"남 {b} · 여 {g}", "여학생끼리 이웃 ✕",
              f"남학생을 먼저 세우고, 남학생 사이와 양 끝의 빈자리 {b + 1}곳 중 서로 다른 곳에 여학생을 한 명씩.",
              [L(f"남학생 {b}명을 한 줄로", fac_s(b), fac(b)), L(f"빈자리 {b + 1}곳(사이와 양 끝)에 여학생 {g}명을 차례로", chain(b + 1, g), nP(b + 1, g)),
               L("곱의 법칙", times([fac(b), nP(b + 1, g)]), v)])


def d_adj_not_end(n):
    a = fac(n - 1) * 2
    e = 2 * 2 * fac(n - 2)
    v = a - e
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A와 B는 이웃하여 서되 두 사람 모두 양 끝에는 서지 않는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: adj(p, "A", "B") and p[0] not in "AB" and p[-1] not in "AB"),
              f"{n}명", "A, B 이웃 · A, B는 양 끝 ✕",
              "이웃하는 경우에서, 묶음이 한쪽 끝에 닿는 경우를 뺀다.",
              [L(f"이웃 — A, B 묶음 포함 {n - 1}개를 한 줄로", fac_s(n - 1), fac(n - 1)), L("이웃 — 묶음 안 A, B 자리 바꾸기", "2 × 1", 2),
               L("이웃(곱의 법칙)", times([fac(n - 1), 2]), a), L(f"끝에 닿음 — 나머지 {n - 2}명을 한 줄로", fac_s(n - 2), fac(n - 2)),
               L("끝에 닿음 — 맨 앞 또는 맨 뒤 2 × 묶음 안 2 × 나머지", times([2, 2, fac(n - 2)]), e), L("끝에 안 닿음(이웃 − 끝에 닿음)", f"{a} − {e}", v)])


def d_two_pairs(n):
    v = fac(n - 2) * 4
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A와 B가 이웃하고, C와 D도 이웃하여 서는 경우의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: adj(p, "A", "B") and adj(p, "C", "D")),
              f"{n}명", "A·B 이웃 · C·D 이웃",
              f"묶음 두 개 → 모두 {n - 2}개를 세우고, 묶음마다 순서 2가지씩.",
              [L(f"A, B 묶음 · C, D 묶음 포함 {n - 2}개를 한 줄로", fac_s(n - 2), fac(n - 2)), L("묶음 안 A, B 자리 바꾸기", "2 × 1", 2),
               L("묶음 안 C, D 자리 바꾸기", "2 × 1", 2), L("곱의 법칙", times([fac(n - 2), 2, 2]), v)])


def d_before(n):
    v = fac(n) // 2
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A가 B보다 앞에 서는 경우의 수를 구하시오. (단, A와 B가 이웃하지 않아도 된다.)", v,
              cnt(lines(P(n)), lambda p: p.index("A") < p.index("B")),
              f"{n}명", "A가 B보다 앞 (붙어 있지 않아도 됨)",
              "어떤 줄이든 A와 B의 자리만 바꾸면 'A가 앞'과 'B가 앞'이 하나씩 짝지어진다 → 전체의 절반.",
              [L(f"전체({n}명을 한 줄로)", fac_s(n), fac(n)), L("A가 B보다 앞(전체의 절반)", f"{fac(n)} ÷ 2", v)])


def d_three_sep(n):
    a = fac(n - 2) * 2
    v = a
    return mk(f"{ptxt(n)}이 {ctx()} 한 줄로 설 때, A가 B와 C 사이에 바로 붙어 서는 경우(B A C 또는 C A B)의 수를 구하시오.", v,
              cnt(lines(P(n)), lambda p: (lambda i: 0 < i < n - 1 and {p[i - 1], p[i + 1]} == {"B", "C"})(p.index("A"))),
              f"{n}명", "B A C 또는 C A B로 붙어 선다",
              f"세 사람 묶음(가운데는 A로 고정)으로 {n - 2}개를 세우고, 양옆 B, C의 순서 2가지.",
              [L(f"(B A C) 묶음 포함 {n - 2}개를 한 줄로", fac_s(n - 2), fac(n - 2)), L("묶음 양옆 B, C 자리 바꾸기", "2 × 1", 2), L("곱의 법칙", times([fac(n - 2), 2]), v)])


def p_gap(b, g):
    n = b + g
    a = fac(b) * nP(b + 1, g)
    v = F(a, fac(n))
    return mk(f"남학생 {b}명과 여학생 {g}명이 제비뽑기로 자리를 정해 한 줄로 설 때, 여학생끼리 이웃하지 않을 확률을 구하시오.", v,
              F(cnt(lines(gl(b, g)), lambda p: all(not (p[i][0] == "여" and p[i + 1][0] == "여") for i in range(len(p) - 1))), fac(n)),
              f"남 {b} · 여 {g} → 모두 {b} + {g} = {b + g}명 · 모든 배치가 같은 가능성", "여학생끼리 이웃 ✕",
              "남학생을 먼저 세우고 빈자리에 여학생을 넣어 센다.",
              [L(f"모든 경우({n}명을 한 줄로)", fac_s(n), fac(n)), L(f"남학생 {b}명을 한 줄로", fac_s(b), fac(b)),
               L(f"빈자리 {b + 1}곳(사이와 양 끝)에 여학생 {g}명을 차례로", chain(b + 1, g), nP(b + 1, g)), L("곱의 법칙", times([fac(b), nP(b + 1, g)]), a), pfeq(a, fac(n))])


def p_end_girl(b, g):
    n = b + g
    bad = b * (b - 1) * fac(n - 2)
    v = 1 - F(bad, fac(n))
    return mk(f"남학생 {b}명과 여학생 {g}명이 제비뽑기로 자리를 정해 한 줄로 설 때, 양 끝 중 적어도 한쪽에 여학생이 설 확률을 구하시오.", v,
              F(cnt(lines(gl(b, g)), lambda p: p[0][0] == "여" or p[-1][0] == "여"), fac(n)),
              f"남 {b} · 여 {g} → 모두 {b} + {g} = {b + g}명", "'적어도 한쪽' 여학생 ↔ 반대는 양 끝 모두 남학생",
              "양 끝이 모두 남학생일 확률을 1에서 뺀다.",
              [L(f"모든 경우({n}명을 한 줄로)", fac_s(n), fac(n)), L(f"양 끝 남(남학생 {b}명 중 2명을 차례로)", chain(b, 2), b * (b - 1)),
               L(f"가운데 {n - 2}명을 한 줄로", fac_s(n - 2), fac(n - 2)), L("양 끝 모두 남(곱의 법칙)", times([b * (b - 1), fac(n - 2)]), bad), pnot(bad, fac(n))])


def p_adj_and_end(n):
    a = 2 * fac(n - 3) * 2
    v = F(a, fac(n))
    return mk(f"{ptxt(n)}이 제비뽑기로 자리를 정해 한 줄로 설 때, A와 B는 양 끝에 서고 C와 D는 이웃하여 설 확률을 구하시오.", v,
              F(cnt(lines(P(n)), lambda p: {p[0], p[-1]} == {"A", "B"} and adj(p, "C", "D")), fac(n)),
              f"{n}명", "A, B 양 끝 · C, D 이웃",
              "양 끝을 먼저 정하고 가운데에서 C, D를 묶는다.",
              [L(f"모든 경우({n}명을 한 줄로)", fac_s(n), fac(n)), L("양 끝에 A, B(2명을 한 줄로)", "2 × 1", 2),
               L(f"가운데 — C, D 묶음 포함 {n - 3}개를 한 줄로", fac_s(n - 3), fac(n - 3)), L("가운데 — 묶음 안 C, D 자리 바꾸기", "2 × 1", 2),
               L("곱의 법칙", times([2, fac(n - 3), 2]), a), pfeq(a, fac(n))])


def build():
    I = []

    def add(lv, d):
        d["lv"] = lv
        I.append(d)

    # 1단계 (15)
    for n in (3, 4, 5):
        add(1, d_all(n))
    add(1, d_all(6))
    for n, k in ((5, 2), (5, 3), (6, 2), (6, 3), (7, 3)):
        add(1, d_choose(n, k))
    add(1, d_fixed_front(4))
    add(1, d_fixed_front(5))
    add(1, d_fixed_mid(5))
    add(1, d_fixed_mid(7))
    add(1, d_front_back(5))
    add(1, d_front_back(6))
    # 2단계 (20)
    for n in (4, 5, 6):
        add(2, d_ends_AB(n))
    for n in (4, 5, 6):
        add(2, d_A_an_end(n))
    for n in (4, 5, 6):
        add(2, d_A_not_front(n))
    for b, g in ((3, 2), (3, 3), (4, 2), (4, 3)):
        add(2, d_ends_boys(b, g))
    for b, g in ((2, 2), (3, 2), (2, 3)):
        add(2, d_ends_girl_one(b, g))
    add(2, d_choose(7, 4))
    add(2, d_choose(8, 3))
    add(2, d_fixed_front(7))
    add(2, d_ends_AB(7))
    # 3단계 (25)
    for n in (4, 5, 6, 7):
        add(3, d_adj2(n))
    for n in (4, 5, 6):
        add(3, d_adj3(n))
    for n in (4, 5, 6):
        add(3, d_not_adj(n))
    for n in (4, 5, 6):
        add(3, d_adj_order(n))
    for b, g in ((2, 2), (3, 2), (3, 3), (4, 2)):
        add(3, d_groups(b, g))
    for b, g in ((2, 2), (3, 2), (3, 3), (4, 2), (4, 3)):
        add(3, d_girls_together(b, g))
    add(3, d_not_adj(7))
    add(3, d_adj3(7))
    add(3, d_groups(4, 3))
    # 4단계 (22)
    for n in (5, 6, 7):
        add(4, d_ends_and_adj(n))
    for n in (4, 5, 6):
        add(4, d_front_and_adj(n))
    for n in (4, 5, 6):
        add(4, d_pair_at_end(n))
    for b, g in ((2, 2), (3, 2), (3, 3), (4, 3)):
        add(4, d_alt(b, g))
    for b in (2, 3):
        add(4, d_girls_ends_boys_adj(b))
    for n in (4, 5, 6):
        add(4, p_adj(n))
    for n in (5, 6):
        add(4, p_ends(n))
    for n in (5, 6):
        add(4, p_end_and_adj(n))
    # 5단계 (18)
    for b, g in ((3, 2), (3, 3), (4, 3)):
        add(5, d_gap(b, g))
    for n in (5, 6):
        add(5, d_adj_not_end(n))
    for n in (5, 6, 7):
        add(5, d_two_pairs(n))
    for n in (4, 6):
        add(5, d_before(n))
    for n in (5, 6):
        add(5, d_three_sep(n))
    for b, g in ((3, 2), (4, 3)):
        add(5, p_gap(b, g))
    for b, g in ((3, 2), (4, 2)):
        add(5, p_end_girl(b, g))
    for n in (6, 7):
        add(5, p_adj_and_end(n))
    return I


if __name__ == "__main__":
    I = build()
    from collections import Counter
    print(len(I), Counter(d["lv"] for d in I))
    for i, d in enumerate(I, 1):
        assert d["ans"] == d["chk"], (i, d["q"], d["ans"], d["chk"])
    print("all ok")
