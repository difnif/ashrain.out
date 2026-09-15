# itemfactory/tools/mkseed_h3_prob.py — 고3 확률과 통계 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h3_prob.py
#     → seeds/h3-2-count.json  (경우의 수: 원순열·중복순열·같은 것이 있는 순열·중복조합·이항정리 계수, 5틀)
#     → seeds/h3-2-prob.json   (확률: 주사위 두 개·덧셈정리·여사건·조건부확률(표)·독립사건, 5틀)
#     → seeds/h3-2-stat.json   (통계: 확률분포표 E/V·이항분포·정규분포(표준화)·표본평균·모평균 신뢰구간·모비율, 6틀)
#   확률은 분수 답(VN/VD). 정규분포는 발문에 표준정규분포표 값을 준다(0.3413·0.4772·0.4987 등).
from __future__ import annotations

import itertools
import math
import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
from genkit.expr import eul as _eul, ika as _ika, ro as _ro, wa as _wa  # noqa: E402

rng = random.Random(20260921)


def _nums(text):
    return {Fraction(x) for x in re.findall(r"(?<![\d.])-?\d+(?![\d.])", text)}


def _fm(v):
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"[[{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})]]"


def _fi(v):
    """마커 안에 넣는 분수 표기 — frac(a,b) (대괄호 없음)"""
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})"


def _pick(d, n):
    keys = sorted(d)
    rng.shuffle(keys)
    return {k: d[k] for k in keys[:n]}


def _row(q, v, **kw):
    f = Fraction(v)
    if f == 0 or f in _nums(q) or abs(f) in _nums(q):
        return None
    d = {"VN": f.numerator, "VD": f.denominator}
    d.update(kw)
    return d


# ═══════════════════════════════════════════════════════════════════ 1. 경우의 수
CB = "h3-2-count"
CB_B = {**HS, "prereq": ["순열과 조합"], "ops": ["경우의 수"], "traps": ["원순열의 (n − 1)!", "같은 것의 개수로 나누기"], "tags": ["원순열", "중복순열", "중복조합", "이항정리"]}


def _cb1_rows():
    out = {}
    for n in range(4, 11):
        v = math.factorial(n - 1)
        q = f"{n}명이 원탁에 둘러앉는 경우의 수"
        r = _row(q, v, Q=f"{n}명의 학생이 원탁에 둘러앉는 경우의 수를 구하시오.", LAW="원순열: 서로 다른 n개를 원형으로 배열하는 경우의 수는 (n − 1)!", STEP=f"({n} − 1)! = {n - 1}! = {v}", KIND="원순열")
        if r: out[f"c{n}"] = r
        # 특정 2명이 이웃: 2 × (n−2)!
        v2 = 2 * math.factorial(n - 2)
        r2 = _row(q, v2, Q=f"{n}명의 학생이 원탁에 둘러앉을 때, 특정한 2명이 서로 이웃하게 앉는 경우의 수를 구하시오.", LAW="이웃하는 2명을 한 묶음으로 보면 (n − 1)명의 원순열, 묶음 안의 순서 2!", STEP=f"({n} − 2)! × 2! = {n - 2}! × 2 = {v2}", KIND="원순열(이웃)")
        if r2: out[f"a{n}"] = r2
        # 특정 2명이 이웃하지 않음: (n−1)! − 2(n−2)!
        v3 = v - v2
        r3 = _row(q, v3, Q=f"{n}명의 학생이 원탁에 둘러앉을 때, 특정한 2명이 서로 이웃하지 않게 앉는 경우의 수를 구하시오.", LAW="전체 원순열 (n − 1)!에서 두 사람이 이웃하는 경우 2 × (n − 2)!을 뺀다", STEP=f"({n} − 1)! − 2 × ({n} − 2)! = {v} − {v2} = {v3}", KIND="원순열(이웃하지 않음)")
        if r3: out[f"n{n}"] = r3
        # 목걸이(뒤집어 같은 것): (n−1)!/2
        v4 = v // 2
        r4 = _row(q, v4, Q=f"서로 다른 {n}개의 구슬을 모두 꿰어 목걸이를 만드는 경우의 수를 구하시오. (단, 뒤집어서 같은 것은 같은 것으로 본다.)", LAW="목걸이는 원순열 (n − 1)!을 뒤집어 같은 것 2가지로 나눈다", STEP=f"[[frac(fact({n - 1}), 2)]] = [[frac({v}, 2)]] = {v4}", KIND="목걸이(원순열/2)")
        if r4: out[f"k{n}"] = r4
        # 특정 2명이 마주 보고 앉음(n 짝수): 한 명을 고정하면 맞은편이 정해지고 나머지 (n−2)!
        if n % 2 == 0:
            v6 = math.factorial(n - 2)
            r6 = _row(q, v6, Q=f"{n}명의 학생이 원탁에 둘러앉을 때, 특정한 2명이 서로 마주 보고 앉는 경우의 수를 구하시오.", LAW="한 명의 자리를 고정하면 마주 보는 자리는 하나로 정해지고, 나머지 (n − 2)명을 일렬로 배열한다", STEP=f"({n} − 2)! = {n - 2}! = {v6}", KIND="원순열(마주 보기)")
            if r6: out[f"o{n}"] = r6
    for kp in range(2, 7):
        # 부부 kp 쌍이 부부끼리 이웃하게 원탁: (kp − 1)! × 2^kp
        v = math.factorial(kp - 1) * 2 ** kp
        q = f"부부 {kp}쌍 원탁"
        r = _row(q, v, Q=f"부부 {kp}쌍이 원탁에 둘러앉을 때, 부부끼리 서로 이웃하게 앉는 경우의 수를 구하시오.", LAW=f"각 부부를 한 묶음으로 보면 {kp}묶음의 원순열 ({kp} − 1)!, 각 묶음 안의 순서 2!씩", STEP=f"({kp} − 1)! × [[pow(2, {kp})]] = {math.factorial(kp - 1)} × {2 ** kp} = {v}", KIND="원순열(묶음)")
        if r: out[f"w{kp}"] = r
        # 특정 3명이 이웃: 3! × (n−3)!
        if n >= 5:
            v5 = 6 * math.factorial(n - 3)
            r5 = _row(q, v5, Q=f"{n}명의 학생이 원탁에 둘러앉을 때, 특정한 3명이 모두 서로 이웃하게 앉는 경우의 수를 구하시오.", LAW="이웃하는 3명을 한 묶음으로 보면 (n − 2)명의 원순열, 묶음 안의 순서 3!", STEP=f"({n} − 3)! × 3! = {n - 3}! × 6 = {v5}", KIND="원순열(이웃)")
            if r5: out[f"t{n}"] = r5
    for n in range(5, 10):
        for r_ in (3, 4, 5):
            if r_ >= n:
                continue
            v = math.comb(n, r_) * math.factorial(r_ - 1)
            q = f"{n}명 중 {r_}명 원탁"
            r = _row(q, v, Q=f"{n}명의 학생 중에서 {r_}명을 뽑아 원탁에 둘러앉히는 경우의 수를 구하시오.", LAW="뽑는 조합 C(n, r)에 뽑힌 r명의 원순열 (r − 1)!을 곱한다", STEP=f"[[comb({n}, {r_})]] × ({r_} − 1)! = {math.comb(n, r_)} × {math.factorial(r_ - 1)} = {v}", KIND="조합 × 원순열")
            if r: out[f"s{n}_{r_}"] = r
    for n in range(2, 7):
        for r_ in range(2, 6):
            v = n ** r_
            q = f"숫자 {n}개로 {r_}자리 자연수 중복"
            digs = ", ".join(str(i) for i in range(1, n + 1))
            r = _row(q, v, Q=f"{n}개의 숫자 {digs} 중에서 중복을 허락하여 {r_}개를 택해 만들 수 있는 {r_}자리 자연수의 개수를 구하시오.", LAW=f"자리마다 {n}가지씩 고르므로 중복순열 [[pperm({n}, {r_})]]", STEP=f"[[pperm({n}, {r_})]] = [[pow({n}, {r_})]] = {v}", KIND="중복순열(자연수)")
            if r: out[f"d{n}_{r_}"] = r
    for n in range(2, 8):
        for r_ in range(2, 6):
            v = n ** r_
            q = f"서로 다른 {n}개에서 중복을 허락하여 {r_}개를 택하는 순열"
            r = _row(q, v, Q=f"서로 다른 {n}개의 문자에서 중복을 허락하여 {r_}개를 택해 일렬로 나열하는 경우의 수를 구하시오.", LAW=f"중복순열: [[pperm({n}, {r_})]] = nʳ", STEP=f"[[pperm({n}, {r_})]] = [[pow({n}, {r_})]] = {v}", KIND="중복순열")
            if r: out[f"p{n}_{r_}"] = r
            v2 = n ** r_
            r2 = _row(q, v2, Q=f"{r_}명의 학생이 {n}개의 동아리 중 하나에 각각 가입하는 경우의 수를 구하시오. (단, 한 동아리에 여러 명이 가입해도 된다.)", LAW=f"학생마다 동아리를 고르므로 중복순열 [[pperm({n}, {r_})]]", STEP=f"[[pow({n}, {r_})]] = {v2}", KIND="중복순열(함수의 개수)")
            if r2: out[f"q{n}_{r_}"] = r2
    return out


CB1_ROWS = _cb1_rows()


def cb_t1():
    return T(CB, 1, CB_B, title="원순열과 중복순열",
        skill="원순열 (n − 1)!, 중복순열 nʳ을 상황에 맞게 적용하기", axis={"원순열": "4~10명(이웃·비이웃·3명 이웃·목걸이·뽑아서 원탁)", "중복순열": "n = 2~6, r = 2~5(문자·자연수·동아리)"}, disc="원형 배열에서 회전을 같은 것으로 보아 (n − 1)!로 세고, 중복 허용이면 nʳ임을 아는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CB1_ROWS)}}], table={"key": "f", "rows": CB1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {KIND}이다.",
        sol2=[("{KIND}", "유형"), ("{STEP}", "공식"), ("답: {ans}", None, ("{ans}", "경우의 수"))],
        sol3=["원순열은 한 사람을 고정하고 나머지를 나열한 것과 같고, 중복순열은 각 자리마다 n가지가 독립적으로 정해짐을 확인한다. 따라서 답은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP}. 따라서 답은 {ans}이다.",
        rubric=[("공식 선택", 3, "{STEP} 꼴로 세웠다.", "원순열을 n!로 두었으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "계승·거듭제곱 계산 실수면 1점.")],
        pitfalls=[("원순열을 n!로 셈", "공식 선택", "불인정"), ("중복순열을 nPr로 셈", "공식 선택", "불인정"), ("이웃 조건에서 묶음 안의 순서 2!을 빠뜨림", "공식 선택", "부분")])


def _cb2_rows():
    out = {}
    words = [("aabbc", "a, a, b, b, c"), ("aaabb", "a, a, a, b, b"), ("aabcc", "a, a, b, c, c"), ("aaabc", "a, a, a, b, c"), ("aabbcc", "a, a, b, b, c, c"), ("aaaabb", "a, a, a, a, b, b"), ("aabbccd", "a, a, b, b, c, c, d"), ("aaabbc", "a, a, a, b, b, c"), ("aaaabbc", "a, a, a, a, b, b, c"), ("aabbb", "a, a, b, b, b"),
             ("aabb", "a, a, b, b"), ("aaab", "a, a, a, b"), ("aabbbc", "a, a, b, b, b, c"), ("aaabbb", "a, a, a, b, b, b"), ("aabbcd", "a, a, b, b, c, d"), ("aaabbcd", "a, a, a, b, b, c, d"), ("aabccd", "a, a, b, c, c, d"), ("abbcc", "a, b, b, c, c"), ("aaaab", "a, a, a, a, b"), ("aaabbbc", "a, a, a, b, b, b, c"),
             ("banana", "b, a, n, a, n, a"), ("level", "l, e, v, e, l"), ("letter", "l, e, t, t, e, r"), ("coffee", "c, o, f, f, e, e"), ("google", "g, o, o, g, l, e"), ("balloon", "b, a, l, l, o, o, n"), ("success", "s, u, c, c, e, s, s"), ("little", "l, i, t, t, l, e"), ("happy", "h, a, p, p, y"), ("apple", "a, p, p, l, e"),
             ("cheese", "c, h, e, e, s, e"), ("pepper", "p, e, p, p, e, r"), ("summer", "s, u, m, m, e, r"), ("school", "s, c, h, o, o, l"), ("tomato", "t, o, m, a, t, o"), ("bubble", "b, u, b, b, l, e"), ("puppy", "p, u, p, p, y"), ("sweet", "s, w, e, e, t"), ("mammal", "m, a, m, m, a, l"), ("dessert", "d, e, s, s, e, r, t")]
    for w, disp in words:
        n = len(w)
        cnt = {ch: w.count(ch) for ch in set(w)}
        v = math.factorial(n)
        for c in cnt.values():
            v //= math.factorial(c)
        dens = " ".join(f"fact({c})" for c in sorted(cnt.values(), reverse=True) if c > 1)
        q = f"{n}개의 문자 {disp}를 일렬로 나열하는 경우의 수"
        r = _row(q, v, Q=f"{n}개의 문자 {disp}를 모두 일렬로 나열하는 경우의 수를 구하시오.", LAW=f"같은 것이 있는 순열: n!/(p! q! ⋯)", STEP=f"[[frac(fact({n}), {dens})]] = {v}", KIND="같은 것이 있는 순열", N=n)
        if r: out[f"w{w}"] = r
    for a in range(2, 8):
        for b in range(2, 8):
            v = math.comb(a + b, a)
            q = f"오른쪽으로 {a}칸, 위쪽으로 {b}칸 최단 경로"
            r = _row(q, v, Q=f"바둑판 모양의 도로망에서 A 지점에서 B 지점까지 가려면 오른쪽으로 {a}칸, 위쪽으로 {b}칸 가야 한다. A에서 B까지 최단 거리로 가는 경우의 수를 구하시오.", LAW="최단 경로: 오른쪽 a개와 위쪽 b개를 나열하는 같은 것이 있는 순열 (a + b)!/(a! b!)", STEP=f"[[frac(fact({a + b}), fact({a}) fact({b}))]] = {v}", KIND="최단 경로", N=a + b)
            if r: out[f"g{a}_{b}"] = r
            # 경유점 P: A 에서 오른쪽 a1, 위 b1 인 지점을 거쳐 B 로
            if a >= 3 and b >= 3:
                for a1, b1 in ((1, 1), (a - 1, b - 1), (1, b - 1), (2, 1)):
                    if not (0 < a1 < a and 0 < b1 < b):
                        continue
                    v2 = math.comb(a1 + b1, a1) * math.comb(a - a1 + b - b1, a - a1)
                    q2 = f"오른쪽으로 {a}칸, 위쪽으로 {b}칸 최단 경로 경유 {a1} {b1}"
                    r2 = _row(q2, v2, Q=f"바둑판 모양의 도로망에서 A 지점에서 B 지점까지 가려면 오른쪽으로 {a}칸, 위쪽으로 {b}칸 가야 한다. A에서 오른쪽으로 {a1}칸, 위쪽으로 {b1}칸 간 지점을 P라 할 때, A에서 P를 거쳐 B까지 최단 거리로 가는 경우의 수를 구하시오.", LAW="P를 거치는 최단 경로: (A → P의 경우의 수) × (P → B의 경우의 수)", STEP=f"[[frac(fact({a1 + b1}), fact({a1}) fact({b1}))]] × [[frac(fact({a - a1 + b - b1}), fact({a - a1}) fact({b - b1}))]] = {math.comb(a1 + b1, a1)} × {math.comb(a - a1 + b - b1, a - a1)} = {v2}", KIND="최단 경로(경유점)", N=a + b)
                    if r2: out[f"g{a}_{b}_{a1}_{b1}"] = r2
    return _pick(out, 330)


CB2_ROWS = _cb2_rows()


def cb_t2():
    return T(CB, 2, CB_B, title="같은 것이 있는 순열 — 문자 나열과 최단 경로",
        skill="n!/(p! q! ⋯)으로 같은 것이 있는 순열 세기", axis={"문자": "4~7개(같은 문자 2~4개, 영단어 포함)", "최단 경로": "a, b = 2~7, 경유점"}, disc="같은 것의 개수의 계승으로 나누고, 최단 경로를 문자 나열로 옮기는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CB2_ROWS)}}], table={"key": "f", "rows": CB2_ROWS},
        derive={"ans": "VN/VD"}, cost=["N", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {KIND}이다.",
        sol2=[("{KIND}", "유형"), ("{STEP}", "공식"), ("답: {ans}", None, ("{ans}", "경우의 수"))],
        sol3=["같은 것을 서로 다르게 보고 센 n!에서 같은 것끼리의 순서 p!만큼 중복되었음을 확인한다. 따라서 답은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP}. 따라서 답은 {ans}이다.",
        rubric=[("공식", 3, "{STEP} 꼴로 세웠다.", "한 종류의 계승을 빠뜨렸으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "계승 계산 실수면 1점.")],
        pitfalls=[("같은 것의 계승으로 나누지 않음", "공식", "불인정"), ("최단 경로를 a × b로 셈", "공식", "불인정"), ("계승 계산 실수", "계산", "부분")])


VARS = ("x", "y", "z", "w", "u", "v")


def _cb3_rows():
    out = {}
    for n in range(2, 7):
        for r_ in range(2, 9):
            v = math.comb(n + r_ - 1, r_)
            q = f"서로 다른 {n}개에서 중복을 허락하여 {r_}개를 택하는 조합"
            r = _row(q, v, Q=f"서로 다른 {n}종류의 과일 중에서 중복을 허락하여 {r_}개를 택하는 경우의 수를 구하시오. (단, 각 종류의 과일은 {r_}개 이상 있다.)", LAW=f"중복조합 [[hcomb({n}, {r_})]] = [[comb({n + r_ - 1}, {r_})]]", STEP=f"[[hcomb({n}, {r_})]] = [[comb({n + r_ - 1}, {r_})]] = {v}", KIND="중복조합")
            if r: out[f"h{n}_{r_}"] = r
            vars_ = ", ".join(VARS[:n])
            eq = " + ".join(VARS[:n]) + f" = {r_}"
            # 방정식 x + y + ⋯ = r 의 음이 아닌 정수해: H(n, r)
            r2 = _row(q, v, Q=f"방정식 {eq}{_eul(r_)} 만족시키는 음이 아닌 정수 {vars_}의 순서쌍의 개수를 구하시오.", LAW=f"{r_}개의 1을 {n}개의 변수에 나누어 주는 중복조합 [[hcomb({n}, {r_})]]", STEP=f"[[hcomb({n}, {r_})]] = [[comb({n + r_ - 1}, {r_})]] = {v}", KIND="방정식의 정수해")
            if r2: out[f"e{n}_{r_}"] = r2
            # 양의 정수해: H(n, r − n) = C(r − 1, n − 1) (r > n)
            if r_ > n:
                v3 = math.comb(r_ - 1, n - 1)
                r3 = _row(q, v3, Q=f"방정식 {eq}{_eul(r_)} 만족시키는 양의 정수 {vars_}의 순서쌍의 개수를 구하시오.", LAW=f"각 변수에서 1씩 빼면 음이 아닌 정수해 문제: [[hcomb({n}, {r_ - n})]]", STEP=f"[[hcomb({n}, {r_ - n})]] = [[comb({r_ - 1}, {r_ - n})]] = {v3}", KIND="방정식의 양의 정수해")
                if r3: out[f"f{n}_{r_}"] = r3
                # 각 종류를 적어도 1개씩 포함: H(n, r − n)
                r5 = _row(q, v3, Q=f"서로 다른 {n}종류의 과일 중에서 각 종류를 적어도 1개씩 포함하여 {r_}개를 택하는 경우의 수를 구하시오. (단, 각 종류의 과일은 {r_}개 이상 있다.)", LAW=f"먼저 종류별로 1개씩 {n}개를 택해 두고 남은 {r_ - n}개를 중복조합으로 택한다: [[hcomb({n}, {r_ - n})]]", STEP=f"[[hcomb({n}, {r_ - n})]] = [[comb({r_ - 1}, {r_ - n})]] = {v3}", KIND="중복조합(적어도 1개)")
                if r5: out[f"a{n}_{r_}"] = r5
            # 부등식 x + y + ⋯ ≤ r 의 음이 아닌 정수해: 여유 변수를 더해 H(n + 1, r)
            if n <= 4:
                v4 = math.comb(n + r_, r_)
                ineq = " + ".join(VARS[:n]) + f" ≤ {r_}"
                r4 = _row(q, v4, Q=f"부등식 {ineq}{_eul(r_)} 만족시키는 음이 아닌 정수 {vars_}의 순서쌍의 개수를 구하시오.", LAW=f"부족한 양을 나타내는 변수를 하나 더하면 방정식 {' + '.join(VARS[:n])} + t = {r_}의 음이 아닌 정수해: [[hcomb({n + 1}, {r_})]]", STEP=f"[[hcomb({n + 1}, {r_})]] = [[comb({n + r_}, {r_})]] = {v4}", KIND="부등식의 정수해")
                if r4: out[f"i{n}_{r_}"] = r4
    return _pick(out, 330)


CB3_ROWS = _cb3_rows()


def cb_t3():
    return T(CB, 3, CB_B, title="중복조합 — 종류 고르기와 방정식의 정수해",
        skill="H(n, r) = C(n + r − 1, r)로 중복조합을 세고, 양의 정수해는 1씩 빼서 옮기기", axis={"n": "2~6", "r": "2~8", "형태": "과일 고르기(적어도 1개) / 음이 아닌 정수해 / 양의 정수해 / 부등식의 정수해"}, disc="순서 없는 중복 선택을 H로 옮기고 양의 정수 조건을 변환하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CB3_ROWS)}}], table={"key": "f", "rows": CB3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 중복조합 [[hcomb(n, r)]]는 r개의 ○와 (n − 1)개의 칸막이 |를 나열하는 경우의 수 [[comb(n + r − 1, r)]]와 같다. 이 문제는 {KIND}이다.",
        sol2=[("{KIND}", "유형"), ("{STEP}", "중복조합"), ("답: {ans}", None, ("{ans}", "경우의 수"))],
        sol3=["○와 | 나열로 세어도 같은 값이 나오는지 확인한다. 따라서 답은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP}. 따라서 답은 {ans}이다.",
        rubric=[("중복조합", 3, "{STEP} 꼴로 세웠다.", "H를 C로 바꿀 때 n + r − 1을 틀리면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "조합 계산 실수면 1점.")],
        pitfalls=[("중복조합을 nCr로 셈", "중복조합", "불인정"), ("양의 정수해를 변환 없이 H(n, r)로 셈", "중복조합", "불인정"), ("조합 계산 실수", "계산", "부분")])


def _cb4_rows():
    out = {}
    for n in range(3, 8):
        for a in NZ(-3, 3):
            for k in range(1, n):
                coef = math.comb(n, k) * a ** (n - k)
                q = f"pow(x {'+' if a > 0 else '−'} {abs(a)}, {n}) x^{k} 계수"
                xk = f"[[pow(x,{k})]]" if k > 1 else "x"
                r = _row(q, coef, Q=f"[[pow(x {'+' if a > 0 else '−'} {abs(a)}, {n})]]의 전개식에서 [[pow(x,{k})]]의 계수를 구하시오." if k > 1 else f"[[pow(x {'+' if a > 0 else '−'} {abs(a)}, {n})]]의 전개식에서 x의 계수를 구하시오.", LAW=f"이항정리: (x + a)ⁿ의 전개식의 일반항은 [[comb(n, r)]] xʳ aⁿ⁻ʳ (여기서 n = {n}, a = {a})", STEP=(f"{xk}의 항: [[comb({n}, {k})]] × [[pow({a}, {n - k})]] = {math.comb(n, k)} × ({a ** (n - k)})" if a ** (n - k) != 1 else f"{xk}의 항: [[comb({n}, {k})]] × [[pow({a}, {n - k})]] = [[comb({n}, {k})]] = {coef}"), KIND="계수", N=n)
                if r: out[f"c{n}_{a}_{k}"] = r
    for n in range(3, 11):
        v = 2 ** n
        q = f"comb(n,0) + comb(n,1) + ... + comb(n,n), n = {n}"
        r = _row(q, v, Q=f"[[comb({n}, 0)]] + [[comb({n}, 1)]] + [[comb({n}, 2)]] + ⋯ + [[comb({n}, {n})]]의 값을 구하시오.", LAW="이항계수의 합: (1 + 1)ⁿ = 2ⁿ", STEP=f"[[pow(2, {n})]] = {v}", KIND="이항계수의 합", N=n)
        if r: out[f"s{n}"] = r
        v2 = 2 ** (n - 1)
        r2 = _row(q, v2, Q=f"[[comb({n}, 1)]] + [[comb({n}, 3)]] + [[comb({n}, 5)]] + ⋯ (홀수 번째 이항계수의 합)의 값을 구하시오.", LAW="홀수 번째 이항계수의 합 = 짝수 번째의 합 = 2ⁿ⁻¹", STEP=f"[[pow(2, {n - 1})]] = {v2}", KIND="이항계수의 합(홀수)", N=n)
        if r2: out[f"o{n}"] = r2
    return _pick(out, 330)


CB4_ROWS = _cb4_rows()


def cb_t4():
    return T(CB, 4, CB_B, title="이항정리 — 전개식의 계수와 이항계수의 합",
        skill="(x + a)ⁿ의 일반항 C(n, r)xʳaⁿ⁻ʳ로 특정 항의 계수를 구하고, 이항계수의 합 2ⁿ 쓰기", axis={"n": "3~10", "a": "±1~±3", "묻는 것": "xᵏ의 계수 / 이항계수의 합"}, disc="일반항에서 r를 정확히 정하고 a의 거듭제곱 부호를 맞추는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CB4_ROWS)}}], table={"key": "f", "rows": CB4_ROWS},
        derive={"ans": "VN/VD"}, cost=["N", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {KIND} 유형이다.",
        sol2=[("{LAW}", "이항정리"), ("{STEP}", "계산"), ("답: {ans}", None, ("{ans}", "답"))],
        sol3=["n = 2, 3 같은 작은 경우로 전개해 규칙이 맞는지 확인할 수 있다. 따라서 답은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP}. 따라서 답은 {ans}이다.",
        rubric=[("일반항·공식", 3, "{STEP} 꼴로 세웠다.", "r를 잘못 잡았으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "부호·거듭제곱 실수면 1점.")],
        pitfalls=[("aⁿ⁻ʳ의 부호를 무시", "계산", "부분"), ("C(n, r)에서 r와 n − r 혼동(값은 같음)", "일반항·공식", "부분"), ("이항계수의 합을 n!로 둠", "일반항·공식", "불인정")])


CB_SEED = SEED(CB, category="확률", title="여러 가지 순열·중복조합·이항정리 — 원순열·중복순열·같은 것이 있는 순열·최단 경로·중복조합·정수해·이항계수", unit_id="h3-2", concept_ids=["h3-2-01", "h3-2-02", "h3-2-03"],
               schema_name="순열과 조합의 확장", note="경우의 수는 파이썬 math 로 계산. perm/comb/pperm/hcomb 마커 사용.",
               templates=[cb_t1(), cb_t2(), cb_t3(), cb_t4()])


# ═══════════════════════════════════════════════════════════════════ 2. 확률
PR = "h3-2-prob"
PR_B = {**HS, "prereq": ["경우의 수", "집합"], "ops": ["확률"], "traps": ["여사건 1 − p", "조건부확률의 분모"], "tags": ["확률", "덧셈정리", "조건부확률", "독립"]}


def _pr1_rows():
    out = {}
    pairs = [(i, j) for i in range(1, 7) for j in range(1, 7)]
    conds = []
    for s_ in range(3, 12):
        conds.append((f"두 눈의 수의 합이 {s_}", lambda i, j, s_=s_: i + j == s_))
    for s_ in (5, 6, 8, 9, 10):
        conds.append((f"두 눈의 수의 합이 {s_} 이상", lambda i, j, s_=s_: i + j >= s_))
    for p in (4, 6, 12):
        conds.append((f"두 눈의 수의 곱이 {p}", lambda i, j, p=p: i * j == p))
    conds.append(("두 눈의 수의 곱이 홀수", lambda i, j: (i * j) % 2 == 1))
    conds.append(("두 눈의 수가 서로 같음", lambda i, j: i == j))
    conds.append(("두 눈의 수의 차가 2", lambda i, j: abs(i - j) == 2))
    conds.append(("두 눈의 수의 차가 1", lambda i, j: abs(i - j) == 1))
    conds.append(("두 눈의 수의 차가 3", lambda i, j: abs(i - j) == 3))
    for d in (2, 3, 4, 5):
        conds.append((f"두 눈의 수의 합이 {d}의 배수", lambda i, j, d=d: (i + j) % d == 0))
    for s_ in (4, 5, 6, 7):
        conds.append((f"두 눈의 수의 합이 {s_} 이하", lambda i, j, s_=s_: i + j <= s_))
    conds.append(("두 눈의 수의 곱이 짝수", lambda i, j: (i * j) % 2 == 0))
    conds.append(("두 눈의 수가 모두 홀수", lambda i, j: i % 2 == 1 and j % 2 == 1))
    conds.append(("두 눈의 수가 모두 짝수", lambda i, j: i % 2 == 0 and j % 2 == 0))
    for mx in (2, 3, 4, 5, 6):
        conds.append((f"두 눈의 수 중 큰 수가 {mx}", lambda i, j, mx=mx: max(i, j) == mx))
    for d in (3, 4, 6):
        conds.append((f"두 눈의 수의 곱이 {d}의 배수", lambda i, j, d=d: (i * j) % d == 0))
    for desc, fn in conds:
        cnt = sum(1 for i, j in pairs if fn(i, j))
        v = Fraction(cnt, 36)
        q = f"주사위 두 개 {desc}"
        phr = "두 눈의 수가 서로 같을 확률" if desc.endswith("같음") else f"{desc}일 확률"
        r = _row(q, v, Q=f"서로 다른 두 개의 주사위를 동시에 던질 때, {phr}을 구하시오.", CNT=cnt, STEP=f"전체 경우 6 × 6 = 36가지, 조건을 만족하는 경우 {cnt}가지", RES=f"[[frac({cnt}, 36)]] = {_fm(v)}", DESC=desc)
        if r: out[f"d{desc}"] = r
    for n in (4, 5, 6, 7, 8, 9):
        for k in (2, 3, 4):
            for b in range(1, n):
                w = n - b
                if k > n:
                    continue
                cnt_all = math.comb(n, k)
                cnt_w = math.comb(w, k) if w >= k else 0
                if cnt_w:
                    v = Fraction(cnt_w, cnt_all)
                    q = f"흰 공 {w}개 검은 공 {b}개 {k}개 모두 흰"
                    r = _row(q, v, Q=f"흰 공 {w}개와 검은 공 {b}개가 들어 있는 주머니에서 임의로 {k}개의 공을 동시에 꺼낼 때, {k}개 모두 흰 공일 확률을 구하시오.", CNT=cnt_w, STEP=f"전체 경우 [[comb({n}, {k})]] = {cnt_all}가지, 모두 흰 공 [[comb({w}, {k})]] = {cnt_w}가지", RES=f"[[frac({cnt_w}, {cnt_all})]] = {_fm(v)}", DESC=f"{k}개 모두 흰 공")
                    if r: out[f"b{w}_{b}_{k}"] = r
                cnt_b = math.comb(b, k) if b >= k else 0
                if cnt_b:
                    v = Fraction(cnt_all - cnt_b, cnt_all)
                    q = f"흰 공 {w}개 검은 공 {b}개 {k}개 적어도 하나 흰"
                    r = _row(q, v, Q=f"흰 공 {w}개와 검은 공 {b}개가 들어 있는 주머니에서 임의로 {k}개의 공을 동시에 꺼낼 때, 흰 공이 적어도 한 개 나올 확률을 구하시오.", CNT=cnt_all - cnt_b, STEP=f"전체 경우 [[comb({n}, {k})]] = {cnt_all}가지, 여사건(모두 검은 공) [[comb({b}, {k})]] = {cnt_b}가지이므로 1 − [[frac({cnt_b}, {cnt_all})]]", RES=f"[[frac({cnt_all - cnt_b}, {cnt_all})]] = {_fm(v)}", DESC="흰 공이 적어도 한 개")
                    if r: out[f"l{w}_{b}_{k}"] = r
                if k == 2 and w >= 1 and b >= 1:
                    cnt_m = w * b
                    v = Fraction(cnt_m, cnt_all)
                    q = f"흰 공 {w}개 검은 공 {b}개 2개 색 다름"
                    r = _row(q, v, Q=f"흰 공 {w}개와 검은 공 {b}개가 들어 있는 주머니에서 임의로 2개의 공을 동시에 꺼낼 때, 두 공의 색이 서로 다를 확률을 구하시오.", CNT=cnt_m, STEP=f"전체 경우 [[comb({n}, 2)]] = {cnt_all}가지, 흰 공 1개와 검은 공 1개 [[comb({w}, 1)]] × [[comb({b}, 1)]] = {cnt_m}가지", RES=f"[[frac({cnt_m}, {cnt_all})]] = {_fm(v)}", DESC="두 공의 색이 서로 다름")
                    if r: out[f"m{w}_{b}"] = r
    return _pick(out, 330)


PR1_ROWS = _pr1_rows()


def pr_t1():
    return T(PR, 1, PR_B, title="확률의 뜻 — 주사위 두 개·공 꺼내기",
        skill="전체 경우의 수와 조건을 만족하는 경우의 수를 세어 수학적 확률 구하기", axis={"상황": "주사위 두 개(합·곱·차·배수) / 주머니에서 공 꺼내기"}, disc="전체 경우를 순서쌍 36가지 또는 조합으로 정확히 세는가", diff=2,
        params=[{"name": "f", "values": {"in": list(PR1_ROWS)}}], table={"key": "f", "rows": PR1_ROWS},
        derive={"ans": "VN/VD"}, cost=["CNT", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="수학적 확률 = (사건의 경우의 수)/(전체 경우의 수). {STEP}. 이때 두 주사위는 서로 다르므로 (1, 2)와 (2, 1)은 다른 경우이고, 공을 동시에 꺼내는 것은 조합으로 센다.",
        sol2=[("{STEP}", "경우의 수"), ("확률 = {RES}", "비율"), ("답: {ans}", None, ("{ans}", "확률"))],
        sol3=["조건을 만족하는 경우를 순서쌍으로 직접 나열해 개수를 확인한다. 따라서 확률은 {ans}이다.", "{RES}", "답 {ans}"],
        model="{STEP}이므로 확률은 {RES}이다.",
        rubric=[("경우의 수", 3, "{STEP}{ro(CNT)} 세었다.", "전체 경우를 잘못 세었으면 1점."), ("확률", 2, "{ans}{eul(ans)} 구했다.", "약분 실수면 1점.")],
        pitfalls=[("(1, 2)와 (2, 1)을 같은 경우로 봄", "경우의 수", "불인정"), ("전체 경우를 21가지로 둠", "경우의 수", "불인정"), ("약분 실수", "확률", "부분")])


def _pr2_rows():
    out = {}
    fr = [Fraction(a, b) for b in (4, 5, 6, 8, 10, 12) for a in range(1, b)]
    fr = sorted(set(fr))
    for pa in fr:
        for pb in fr:
            for pab in fr:
                if pab >= min(pa, pb) or pa + pb - pab > 1:
                    continue
                pu = pa + pb - pab
                q = f"P(A) = {_fm(pa)}, P(B) = {_fm(pb)}, P(A ∩ B) = {_fm(pab)}"
                r = _row(q, pu, Q=f"두 사건 A, B에 대하여 [[prob(A)]] = {_fm(pa)}, [[prob(B)]] = {_fm(pb)}, [[prob(inter(A, B))]] = {_fm(pab)}일 때, [[prob(union(A, B))]]의 값을 구하시오.", LAW="덧셈정리: P(A ∪ B) = P(A) + P(B) − P(A ∩ B)", STEP=f"{_fm(pa)} + {_fm(pb)} − {_fm(pab)}", KIND="합사건")
                if r: out[f"u{pa}_{pb}_{pab}"] = r
                r2 = _row(q, pab, Q=f"두 사건 A, B에 대하여 [[prob(A)]] = {_fm(pa)}, [[prob(B)]] = {_fm(pb)}, [[prob(union(A, B))]] = {_fm(pu)}일 때, [[prob(inter(A, B))]]의 값을 구하시오.", LAW="덧셈정리: P(A ∩ B) = P(A) + P(B) − P(A ∪ B)", STEP=f"{_fm(pa)} + {_fm(pb)} − {_fm(pu)}", KIND="곱사건")
                if r2: out[f"i{pa}_{pb}_{pab}"] = r2
                # 여사건: P(Aᶜ ∩ Bᶜ) = 1 − P(A ∪ B)
                r3 = _row(q, 1 - pu, Q=f"두 사건 A, B에 대하여 [[prob(A)]] = {_fm(pa)}, [[prob(B)]] = {_fm(pb)}, [[prob(inter(A, B))]] = {_fm(pab)}일 때, [[prob(inter(comp(A), comp(B)))]]의 값을 구하시오.", LAW="드모르간: Aᶜ ∩ Bᶜ = (A ∪ B)ᶜ, 여사건: P((A ∪ B)ᶜ) = 1 − P(A ∪ B)", STEP=f"1 − ({_fm(pa)} + {_fm(pb)} − {_fm(pab)}) = 1 − {_fm(pu)}", KIND="여사건")
                if r3: out[f"c{pa}_{pb}_{pab}"] = r3
    # 배반사건
    for pa in fr:
        for pb in fr:
            if pa + pb >= 1:
                continue
            q = f"배반 P(A) = {_fm(pa)}, P(B) = {_fm(pb)}"
            r = _row(q, pa + pb, Q=f"두 사건 A, B가 서로 배반사건이고 [[prob(A)]] = {_fm(pa)}, [[prob(B)]] = {_fm(pb)}일 때, [[prob(union(A, B))]]의 값을 구하시오.", LAW="배반사건이면 P(A ∩ B) = 0이므로 P(A ∪ B) = P(A) + P(B)", STEP=f"{_fm(pa)} + {_fm(pb)}", KIND="배반사건")
            if r: out[f"m{pa}_{pb}"] = r
    return _pick(out, 330)


PR2_ROWS = _pr2_rows()


def pr_t2():
    return T(PR, 2, PR_B, title="확률의 덧셈정리와 여사건",
        skill="P(A ∪ B) = P(A) + P(B) − P(A ∩ B), 배반사건, 여사건 P(Aᶜ) = 1 − P(A)를 적용하기", axis={"확률": "분모 4~12의 분수", "묻는 것": "합사건 / 곱사건 / 여사건(둘 다 아님) / 배반사건"}, disc="덧셈정리에서 교집합을 한 번 빼고, 드모르간으로 여사건을 옮기는가", diff=2,
        params=[{"name": "f", "values": {"in": list(PR2_ROWS)}}], table={"key": "f", "rows": PR2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {KIND} 유형이다.",
        sol2=[("{LAW}", "정리"), ("{STEP}", "대입"), ("= {ans}", None, ("{ans}", "확률"))],
        sol3=["결과가 0과 1 사이인지, P(A ∪ B) ≥ P(A), P(B)인지 확인한다. 따라서 답은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP} = {ans}이다.",
        rubric=[("정리 적용", 3, "{STEP} 꼴로 세웠다.", "교집합을 빼지 않았으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "분수 계산 실수면 1점.")],
        pitfalls=[("P(A ∪ B) = P(A) + P(B)로 둠(배반이 아닌데)", "정리 적용", "불인정"), ("Aᶜ ∩ Bᶜ를 1 − P(A ∩ B)로 봄", "정리 적용", "불인정"), ("분수 통분 실수", "계산", "부분")])


def _pr3_rows():
    out = {}
    for a in range(2, 9):
        for b in range(1, 8):
            for c in range(1, 8):
                for d in range(2, 9):
                    n = a + b + c + d
                    if n > 30:
                        continue
                    q = f"남 {a} {b} 여 {c} {d}"
                    desc = f"어느 학급 학생 {n}명 중 남학생은 {a + b}명, 여학생은 {c + d}명이다. 안경을 쓴 남학생은 {a}명, 안경을 쓴 여학생은 {c}명이다."
                    asks = [("mg", "남학생일 때 안경을 쓴 학생일 확률", Fraction(a, a + b), f"P(안경 | 남) = [[frac({a}, {a + b})]]", "남학생 중 안경 쓴 학생의 비율"),
                            ("gm", "안경을 쓴 학생일 때 남학생일 확률", Fraction(a, a + c), f"P(남 | 안경) = [[frac({a}, {a + c})]]", "안경 쓴 학생 중 남학생의 비율"),
                            ("fn", "여학생일 때 안경을 쓰지 않은 학생일 확률", Fraction(d, c + d), f"P(안경 아님 | 여) = [[frac({d}, {c + d})]]", "여학생 중 안경 쓰지 않은 학생의 비율"),
                            ("ng", "안경을 쓰지 않은 학생일 때 여학생일 확률", Fraction(d, b + d), f"P(여 | 안경 아님) = [[frac({d}, {b + d})]]", "안경 쓰지 않은 학생 중 여학생의 비율")]
                    for kk, ask, v, step, expl in asks:
                        r = _row(desc, v, Q=f"{desc} 이 학급에서 임의로 뽑은 한 학생이 {ask}을 구하시오.", STEP=step, EXPL=expl, ASK=ask)
                        if r: out[f"{a}_{b}_{c}_{d}_{kk}"] = r
    return _pick(out, 330)


PR3_ROWS = _pr3_rows()


def pr_t3():
    return T(PR, 3, PR_B, title="조건부확률 — 표로 주어진 인원",
        skill="P(B|A) = P(A ∩ B)/P(A) = n(A ∩ B)/n(A)로 조건이 붙은 확률 구하기", axis={"인원": "남·여 × 안경 유무 (합 ≤ 30)", "묻는 것": "4가지 조건부확률"}, disc="조건(주어진 사건)을 분모로 잡아 그 안에서 비율을 세는가", diff=3,
        params=[{"name": "f", "values": {"in": list(PR3_ROWS)}}], table={"key": "f", "rows": PR3_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="조건부확률 P(B|A)는 사건 A가 일어났다는 조건에서 B가 일어날 확률로, P(A ∩ B)/P(A) = n(A ∩ B)/n(A)이다. 조건에 해당하는 학생들만 분모로 잡고 그중 묻는 학생 수를 분자로 놓는다: {EXPL}.",
        sol2=[("조건이 되는 사건이 분모", "조건부확률의 뜻"), ("{STEP}", "비율"), ("= {ans}", None, ("{ans}", "확률"))],
        sol3=["분모가 전체 인원이 아니라 조건에 해당하는 인원인지 확인한다. 따라서 확률은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{EXPL}이므로 {STEP} = {ans}이다.",
        rubric=[("조건부확률", 3, "{STEP} 꼴로 세웠다.", "분모를 전체 인원으로 두었으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "약분 실수면 1점.")],
        pitfalls=[("분모를 전체 인원으로 둠", "조건부확률", "불인정"), ("조건과 결과를 바꿔 P(A|B)를 구함", "조건부확률", "불인정"), ("약분 실수", "계산", "부분")])


def _pr4_rows():
    out = {}
    fr = sorted(set(Fraction(a, b) for b in (2, 3, 4, 5, 6, 8, 10) for a in range(1, b)))
    for pa in fr:
        for pb in fr:
            if pa >= pb:
                continue
            q = f"독립 P(A) = {_fm(pa)}, P(B) = {_fm(pb)}"
            r = _row(q, pa * pb, Q=f"두 사건 A, B가 서로 독립이고 [[prob(A)]] = {_fm(pa)}, [[prob(B)]] = {_fm(pb)}일 때, [[prob(inter(A, B))]]의 값을 구하시오.", LAW="독립이면 P(A ∩ B) = P(A)P(B)", STEP=f"{_fm(pa)} × {_fm(pb)}", KIND="곱사건")
            if r: out[f"i{pa}_{pb}"] = r
            r2 = _row(q, pa + pb - pa * pb, Q=f"두 사건 A, B가 서로 독립이고 [[prob(A)]] = {_fm(pa)}, [[prob(B)]] = {_fm(pb)}일 때, [[prob(union(A, B))]]의 값을 구하시오.", LAW="독립이면 P(A ∩ B) = P(A)P(B), 덧셈정리 P(A ∪ B) = P(A) + P(B) − P(A)P(B)", STEP=f"{_fm(pa)} + {_fm(pb)} − {_fm(pa)} × {_fm(pb)}", KIND="합사건")
            if r2: out[f"u{pa}_{pb}"] = r2
            r3 = _row(q, (1 - pa) * (1 - pb), Q=f"두 사건 A, B가 서로 독립이고 [[prob(A)]] = {_fm(pa)}, [[prob(B)]] = {_fm(pb)}일 때, 두 사건이 모두 일어나지 않을 확률을 구하시오.", LAW="A, B가 독립이면 Aᶜ, Bᶜ도 독립: P(Aᶜ ∩ Bᶜ) = (1 − P(A))(1 − P(B))", STEP=f"(1 − {_fm(pa)})(1 − {_fm(pb)}) = {_fm(1 - pa)} × {_fm(1 - pb)}", KIND="여사건의 곱")
            if r3: out[f"c{pa}_{pb}"] = r3
            # P(B|A) 주어짐 → 독립 판단은 문자열; 대신 P(A ∩ B) 와 P(A) 로 P(B) 구하기(독립)
            pab = pa * pb
            r4 = _row(q, pb, Q=f"두 사건 A, B가 서로 독립이고 [[prob(A)]] = {_fm(pa)}, [[prob(inter(A, B))]] = {_fm(pab)}일 때, [[prob(B)]]의 값을 구하시오.", LAW="독립이면 P(A ∩ B) = P(A)P(B)이므로 P(B) = P(A ∩ B)/P(A)", STEP=f"{_fm(pab)} ÷ {_fm(pa)}", KIND="독립에서 P(B)")
            if r4: out[f"b{pa}_{pb}"] = r4
    for n in (2, 3, 4):
        for p in (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5)):
            v = 1 - (1 - p) ** n
            q = f"독립시행 {n}회 성공 확률 {_fm(p)} 적어도 한 번"
            r = _row(q, v, Q=f"한 번의 시행에서 사건 A가 일어날 확률이 {_fm(p)}이다. 이 시행을 {n}번 독립적으로 반복할 때, 사건 A가 적어도 한 번 일어날 확률을 구하시오.", LAW="여사건: 1 − (한 번도 일어나지 않을 확률) = 1 − (1 − p)ⁿ", STEP=f"1 − [[pow({_fi(1 - p)}, {n})]] = 1 − {_fm((1 - p) ** n)}", KIND="적어도 한 번")
            if r: out[f"r{n}_{p}"] = r
    return _pick(out, 330)


PR4_ROWS = _pr4_rows()


def pr_t4():
    return T(PR, 4, PR_B, title="사건의 독립 — 곱셈정리와 적어도 한 번",
        skill="독립사건의 P(A ∩ B) = P(A)P(B)와 여사건을 결합해 확률 구하기", axis={"확률": "분모 2~10의 분수", "묻는 것": "곱사건 / 합사건 / 둘 다 아님 / P(B) / 적어도 한 번"}, disc="독립일 때 곱셈으로 교집합을 구하고 여사건을 정확히 세우는가", diff=3,
        params=[{"name": "f", "values": {"in": list(PR4_ROWS)}}], table={"key": "f", "rows": PR4_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="{LAW}. 이 문제는 {KIND} 유형이다.",
        sol2=[("{LAW}", "독립의 성질"), ("{STEP}", "대입"), ("= {ans}", None, ("{ans}", "확률"))],
        sol3=["독립이면 P(B|A) = P(B)가 되는지로 곱셈 관계를 확인할 수 있다. 따라서 답은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP} = {ans}이다.",
        rubric=[("독립의 성질", 3, "{STEP} 꼴로 세웠다.", "독립을 배반으로 착각했으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "분수 계산 실수면 1점.")],
        pitfalls=[("독립을 배반(P(A ∩ B) = 0)으로 착각", "독립의 성질", "불인정"), ("적어도 한 번을 n × p로 계산", "독립의 성질", "불인정"), ("여사건 1 − p 계산 실수", "계산", "부분")])


def _pr5_rows():
    out = {}
    for n in (3, 4, 5):
        for p in (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(1, 6)):
            for k in range(0, n + 1):
                v = math.comb(n, k) * p ** k * (1 - p) ** (n - k)
                q = f"독립시행 {n}회 p = {_fm(p)} 정확히 {k}번"
                facs = [str(math.comb(n, k))] if math.comb(n, k) != 1 else []
                facs += [_fm(p ** k)] if k else []
                facs += [_fm((1 - p) ** (n - k))] if n - k else []
                r = _row(q, v, Q=f"한 번의 시행에서 사건 A가 일어날 확률이 {_fm(p)}이다. 이 시행을 {n}번 독립적으로 반복할 때, 사건 A가 정확히 {k}번 일어날 확률을 구하시오.", LAW=f"독립시행의 확률: [[comb({n}, {k})]] pᵏ(1 − p)ⁿ⁻ᵏ", STEP=f"[[comb({n}, {k})]] × [[pow({_fi(p)}, {k})]] × [[pow({_fi(1 - p)}, {n - k})]] = " + " × ".join(facs), KIND="정확히 k번")
                if r: out[f"e{n}_{p}_{k}"] = r
            for k in (n - 1,):
                v = sum(math.comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(k, n + 1))
                q = f"독립시행 {n}회 p = {_fm(p)} {k}번 이상"
                r = _row(q, v, Q=f"한 번의 시행에서 사건 A가 일어날 확률이 {_fm(p)}이다. 이 시행을 {n}번 독립적으로 반복할 때, 사건 A가 {k}번 이상 일어날 확률을 구하시오.", LAW=f"{k}번과 {n}번 일어날 확률의 합", STEP=f"[[comb({n}, {k})]] × [[pow({_fi(p)}, {k})]] × {_fm(1 - p)} + [[pow({_fi(p)}, {n})]] = {_fm(math.comb(n, k) * p ** k * (1 - p))} + {_fm(p ** n)}", KIND="k번 이상")
                if r: out[f"g{n}_{p}_{k}"] = r
    return _pick(out, 300)


PR5_ROWS = _pr5_rows()


def pr_t5():
    return T(PR, 5, PR_B, title="독립시행의 확률 — C(n, k)pᵏqⁿ⁻ᵏ",
        skill="같은 시행을 n번 반복할 때 사건이 k번 일어날 확률 C(n, k)pᵏ(1 − p)ⁿ⁻ᵏ 계산하기", axis={"n": "3~5", "p": "1/2, 1/3, 2/3, 1/4, 1/6", "묻는 것": "정확히 k번 / k번 이상"}, disc="순서를 고려한 조합 계수 C(n, k)를 곱하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(PR5_ROWS)}}], table={"key": "f", "rows": PR5_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="독립시행에서 사건이 k번 일어날 확률은 어느 k번인지 고르는 경우의 수 [[comb(n, k)]]에 pᵏ(1 − p)ⁿ⁻ᵏ를 곱한 것이다({LAW}). 이 문제는 {KIND} 유형이다.",
        sol2=[("{LAW}", "공식"), ("{STEP}", "대입"), ("= {ans}", None, ("{ans}", "확률"))],
        sol3=["k = 0부터 n까지의 확률을 모두 더하면 1이 됨을 이용해 검산할 수 있다. 따라서 답은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP} = {ans}이다.",
        rubric=[("공식", 3, "{STEP} 꼴로 세웠다.", "C(n, k)를 빠뜨렸으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "거듭제곱·분수 계산 실수면 1점.")],
        pitfalls=[("C(n, k)를 곱하지 않음", "공식", "부분"), ("(1 − p)의 지수를 k로 둠", "공식", "불인정"), ("'이상'을 '정확히'로 계산", "공식", "불인정")])


PR_SEED = SEED(PR, category="확률", title="확률 — 수학적 확률·덧셈정리와 여사건·조건부확률·독립사건·독립시행", unit_id="h3-2", concept_ids=["h3-2-04", "h3-2-05", "h3-2-06", "h3-2-07"],
               schema_name="확률의 뜻과 계산", note="확률은 분수 답(VN/VD). 조건부확률은 남·여 × 안경 유무 인원표.",
               templates=[pr_t1(), pr_t2(), pr_t3(), pr_t4(), pr_t5()])


# ═══════════════════════════════════════════════════════════════════ 3. 통계
ST = "h3-2-stat"
ST_B = {**HS, "prereq": ["확률", "평균과 분산"], "ops": ["통계"], "traps": ["V(aX + b) = a²V(X)", "표준화 Z = (X − m)/σ"], "tags": ["확률분포", "이항분포", "정규분포", "추정"]}


def _st1_rows():
    out = {}
    tries = 0
    while len(out) < 330 and tries < 30000:
        tries += 1
        k = rng.choice((3, 4))
        xs = sorted(rng.sample(range(0, 7), k))
        den = rng.choice((4, 5, 6, 8, 10))
        parts = [rng.randint(1, den - 1) for _ in range(k)]
        tot = sum(parts)
        probs = [Fraction(p_, tot) for p_ in parts]
        if any(pr.denominator > 12 for pr in probs) or len(set(probs)) == 1:
            continue
        E = sum(x * p_ for x, p_ in zip(xs, probs))
        E2 = sum(x * x * p_ for x, p_ in zip(xs, probs))
        V = E2 - E * E
        tbl = "[[mat(2, " + str(k + 1) + ", X, " + ", ".join(str(x) for x in xs) + ", P(X = x), " + ", ".join(_fi(p_) for p_ in probs) + ")]]"
        a, b = rng.choice((2, 3, -2, 4)), rng.choice((1, -1, 3, -3, 5))
        for kk, ask, v, step in (("E", "[[ev(X)]]", E, "E(X) = Σ x·P(X = x) = " + " + ".join(f"{x} × {_fm(p_)}" for x, p_ in zip(xs, probs))),
                                 ("V", "[[var(X)]]", V, f"V(X) = E(X²) − (E(X))² = {_fm(E2)} − ({_fm(E)})²"),
                                 ("EL", f"[[ev({a}X {'+' if b > 0 else '−'} {abs(b)})]]", a * E + b, f"E(aX + b) = aE(X) + b = {a} × {_fm(E)} {'+' if b > 0 else '−'} {abs(b)}"),
                                 ("VL", f"[[var({a}X {'+' if b > 0 else '−'} {abs(b)})]]", a * a * V, f"V(aX + b) = a²V(X) = {a * a} × {_fm(V)}")):
            if v == 0:
                continue
            q = f"{tbl} {ask}"
            r = _row(q, v, Q=f"확률변수 X의 확률분포가 다음 표와 같을 때, {ask}의 값을 구하시오. {tbl}", TBL=tbl, STEP=step, EV=_fm(E), VV=_fm(V), E2=_fm(E2), ASK=ask)
            if r: out[f"{len(out)}_{kk}"] = r
    return out


ST1_ROWS = _st1_rows()


def st_t1():
    return T(ST, 1, ST_B, title="이산확률변수의 평균과 분산 — 확률분포표",
        skill="E(X) = Σx·p, V(X) = E(X²) − (E(X))², E(aX + b) = aE(X) + b, V(aX + b) = a²V(X) 쓰기", axis={"X": "0~6 중 3~4개 값", "묻는 것": "E(X) / V(X) / E(aX + b) / V(aX + b)"}, disc="분산은 제곱의 평균에서 평균의 제곱을 빼고, 일차변환에서 분산은 a²배임을 아는가", diff=3,
        params=[{"name": "f", "values": {"in": list(ST1_ROWS)}}], table={"key": "f", "rows": ST1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="확률분포표에서 평균 E(X) = Σ x·P(X = x), 분산 V(X) = E(X²) − (E(X))²이다. 일차변환 Y = aX + b에서는 E(Y) = aE(X) + b, V(Y) = a²V(X)이다. 여기서 E(X) = {EV}, E(X²) = {E2}, V(X) = {VV}.",
        sol2=[("E(X) = {EV}, E(X²) = {E2}, V(X) = {VV}", "기본값"), ("{STEP}", "공식"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["확률의 합이 1인지, 분산이 0 이상인지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="E(X) = {EV}, E(X²) = {E2}, V(X) = {VV}이고 {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("공식", 3, "{STEP} 꼴로 세웠다.", "분산에서 (E(X))²을 빼지 않았으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "분수 계산 실수면 1점.")],
        pitfalls=[("V(aX + b)를 aV(X)로 둠", "공식", "불인정"), ("V(X) = E(X²)으로 둠", "공식", "불인정"), ("E(aX + b)에서 b를 a배 함", "공식", "부분")])


def _st2_rows():
    out = {}
    for n in (10, 12, 16, 18, 20, 24, 25, 30, 36, 40, 48, 50, 60, 72, 100):
        for p in (Fraction(1, 2), Fraction(1, 3), Fraction(2, 3), Fraction(1, 4), Fraction(3, 4), Fraction(1, 5), Fraction(2, 5), Fraction(1, 6)):
            E, V = n * p, n * p * (1 - p)
            sd2 = V
            sd = math.isqrt(V.numerator) if V.denominator == 1 and math.isqrt(V.numerator) ** 2 == V.numerator else None
            for kk, ask, v, step in (("E", "[[ev(X)]]", E, f"E(X) = np = {n} × {_fm(p)}"), ("V", "[[var(X)]]", V, f"V(X) = np(1 − p) = {n} × {_fm(p)} × {_fm(1 - p)}"), ("S", "[[sd(X)]]", Fraction(sd) if sd else None, f"σ(X) = [[sqrt({_fm(V)})]]"), ("VL", "[[var(2X + 1)]]", 4 * V, f"V(2X + 1) = 4V(X) = 4 × {_fm(V)}")):
                if v is None or v == 0:
                    continue
                q = f"B({n}, {_fm(p)}) {ask}"
                r = _row(q, v, Q=f"확률변수 X가 이항분포 [[binomd({n}, {_fi(p)})]]을 따를 때, {ask}의 값을 구하시오.", STEP=step, ASK=ask, N=n)
                if r: out[f"{n}_{p}_{kk}"] = r
    return _pick(out, 330)


ST2_ROWS = _st2_rows()


def st_t2():
    return T(ST, 2, ST_B, title="이항분포의 평균·분산·표준편차",
        skill="X ~ B(n, p)이면 E(X) = np, V(X) = np(1 − p), σ(X) = √(np(1 − p))임을 쓰기", axis={"n": "10~100", "p": "1/2, 1/3, 2/3, 1/4, 3/4, 1/5, 2/5, 1/6", "묻는 것": "E / V / σ / V(2X + 1)"}, disc="분산에 (1 − p)를 곱하고 표준편차는 제곱근임을 아는가", diff=2,
        params=[{"name": "f", "values": {"in": list(ST2_ROWS)}}], table={"key": "f", "rows": ST2_ROWS},
        derive={"ans": "VN/VD"}, cost=["N", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="이항분포 B(n, p)는 성공 확률 p인 독립시행을 n번 할 때 성공 횟수의 분포이고, 평균 np, 분산 np(1 − p), 표준편차 √(np(1 − p))이다.",
        sol2=[("E(X) = np, V(X) = np(1 − p)", "이항분포의 평균·분산"), ("{STEP}", "대입"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["V(X) ≤ E(X)(1 − p < 1)인지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("공식", 3, "{STEP} 꼴로 세웠다.", "분산에 (1 − p)를 빠뜨렸으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("V(X) = np로 둠", "공식", "불인정"), ("σ(X)를 분산으로 답함", "공식", "불인정"), ("V(2X + 1) = 2V(X)로 둠", "공식", "불인정")])


ZT = {0.5: "0.1915", 1.0: "0.3413", 1.5: "0.4332", 2.0: "0.4772", 2.5: "0.4938", 3.0: "0.4987"}


def _st3_rows():
    out = {}
    for m in (50, 60, 70, 100, 170, 200):
        for sd in (2, 4, 5, 10, 20):
            for z1, z2 in ((0, 1), (0, 2), (1, 2), (-1, 1), (-2, 2), (-1, 2), (0, 1.5), (0.5, 1.5), (1, 3), (-1.5, 0.5), (-2, 1)):
                a, b = m + z1 * sd, m + z2 * sd
                if a != int(a) or b != int(b):
                    continue
                a, b = int(a), int(b)
                def area(z):
                    return Fraction(ZT[abs(z)]) if z != 0 else Fraction(0)
                if z1 * z2 <= 0:
                    v = area(z1) + area(z2)
                else:
                    v = abs(area(z2) - area(z1))
                zs = sorted({abs(z1), abs(z2)} - {0})
                given = ", ".join(f"P(0 ≤ Z ≤ {z:g}) = {ZT[z]}" for z in zs) + _ro(ZT[zs[-1]])
                q = f"정규분포 N({m}, {sd}²) P({a} ≤ X ≤ {b})"
                if v in _nums(q):
                    continue
                r = {"VN": v.numerator, "VD": v.denominator, "Q": f"확률변수 X가 정규분포 [[normald({m}, pow({sd},2))]]을 따를 때, P({a} ≤ X ≤ {b})의 값을 구하시오. (단, Z가 표준정규분포를 따를 때 {given} 계산한다.)", "STD": f"Z = [[frac(X − {m}, {sd})]]로 표준화하면 P({a} ≤ X ≤ {b}) = P({z1:g} ≤ Z ≤ {z2:g})", "STEP": (f"P({z1:g} ≤ Z ≤ 0) + P(0 ≤ Z ≤ {z2:g}) = {ZT[abs(z1)] if z1 else '0'} + {ZT[abs(z2)] if z2 else '0'}" if z1 * z2 <= 0 else f"P(0 ≤ Z ≤ {max(abs(z1), abs(z2)):g}) − P(0 ≤ Z ≤ {min(abs(z1), abs(z2)):g}) = {ZT[max(abs(z1), abs(z2))]} − {ZT[min(abs(z1), abs(z2))]}"), "M": m, "SD": sd, "A": a, "B": b}
                out[f"{m}_{sd}_{z1}_{z2}"] = r
    return _pick(out, 330)


ST3_ROWS = _st3_rows()


def st_t3():
    return T(ST, 3, ST_B, title="정규분포 — 표준화하여 확률 구하기",
        skill="Z = (X − m)/σ로 표준화하고 표준정규분포표의 값으로 P(a ≤ X ≤ b) 계산하기", axis={"m": "50~200", "σ": "2~20", "구간": "z = −2~3"}, disc="표준화한 뒤 0을 기준으로 대칭성을 써서 표의 값을 더하거나 빼는가", diff=3,
        params=[{"name": "f", "values": {"in": list(ST3_ROWS)}}], table={"key": "f", "rows": ST3_ROWS},
        derive={"ans": "VN/VD"}, cost=["M", "SD", "A", "B", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{dec(ans)}",
        sol1="정규분포 N(m, σ²)을 따르는 X는 Z = (X − m)/σ로 표준화하면 표준정규분포 N(0, 1)을 따른다. {STD}. 표준정규분포는 0에 대해 대칭이므로 P(−a ≤ Z ≤ 0) = P(0 ≤ Z ≤ a)이다.",
        sol2=[("{STD}", "표준화"), ("{STEP}", "표의 값"), ("= {dec(ans)}", None, ("{dec(ans)}", "확률"))],
        sol3=["구간이 0을 포함하면 두 값을 더하고, 한쪽에 치우쳐 있으면 큰 값에서 작은 값을 뺐는지 확인한다. 따라서 확률은 {dec(ans)}이다.", "{STEP}", "답 {dec(ans)}"],
        model="{STD}이고 {STEP} = {dec(ans)}이다.",
        rubric=[("표준화", 3, "{STD} 꼴로 바꿨다.", "σ 대신 σ²으로 나눴으면 인정하지 않는다."), ("표 읽기", 2, "{dec(ans)}{eul(dec(ans))} 구했다.", "대칭성 처리(더하기·빼기) 실수면 1점.")],
        pitfalls=[("분산 σ²으로 나눠 표준화", "표준화", "불인정"), ("0을 포함하는 구간에서 두 값을 뺌", "표 읽기", "불인정"), ("표의 값 잘못 읽음", "표 읽기", "부분")])


def _st4_rows():
    out = {}
    for m in (20, 30, 50, 60, 80, 100):
        for sd in (2, 3, 4, 6, 8, 10, 12):
            for n in (4, 9, 16, 25, 36, 64, 100):
                sn = math.isqrt(n)
                for kk, ask, v, step in (("E", "E(X̄)", Fraction(m), f"E(X̄) = m = {m}"), ("V", "V(X̄)", Fraction(sd * sd, n), f"V(X̄) = σ²/n = [[frac({sd * sd}, {n})]]"), ("S", "σ(X̄)", Fraction(sd, sn), f"σ(X̄) = σ/√n = [[frac({sd}, {sn})]]")):
                    q = f"모집단 N({m}, {sd}²) 크기 {n} 표본평균 {ask}"
                    r = _row(q, v, Q=f"정규분포 [[normald({m}, pow({sd},2))]]을 따르는 모집단에서 크기가 {n}인 표본을 임의추출할 때, 표본평균 X̄에 대하여 {ask}의 값을 구하시오.", STEP=step, ASK=ask, N=n)
                    if r: out[f"{m}_{sd}_{n}_{kk}"] = r
    return _pick(out, 330)


ST4_ROWS = _st4_rows()


def st_t4():
    return T(ST, 4, ST_B, title="표본평균의 분포 — E(X̄) = m, V(X̄) = σ²/n",
        skill="모평균 m, 모분산 σ², 표본의 크기 n에서 표본평균의 평균·분산·표준편차 구하기", axis={"m": "20~100", "σ": "2~12", "n": "4~100(제곱수)"}, disc="표본평균의 분산이 σ²/n(표준편차는 σ/√n)임을 아는가", diff=2,
        params=[{"name": "f", "values": {"in": list(ST4_ROWS)}}], table={"key": "f", "rows": ST4_ROWS},
        derive={"ans": "VN/VD"}, cost=["N", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        sol1="모평균 m, 모표준편차 σ인 모집단에서 크기 n인 표본의 표본평균 X̄는 E(X̄) = m, V(X̄) = σ²/n, σ(X̄) = σ/√n이다(정규모집단이면 X̄도 정규분포).",
        sol2=[("E(X̄) = m, V(X̄) = σ²/n", "표본평균의 분포"), ("{STEP}", "대입"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["n이 커질수록 분산이 작아지는지(σ²/n) 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("공식", 3, "{STEP} 꼴로 세웠다.", "σ/n으로 두었으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "제곱근 계산 실수면 1점.")],
        pitfalls=[("V(X̄) = σ²으로 둠", "공식", "불인정"), ("σ(X̄) = σ/n으로 둠", "공식", "불인정"), ("√n 계산 실수", "계산", "부분")])


def _termdec(v):
    """소수 넷째 자리까지로 정확히 표기되는가 — dec(v)는 4자리에서 반올림하므로 그 안에서 떨어지는 값만 쓴다."""
    return (Fraction(v) * 10000).denominator == 1


def _st5_rows():
    out = {}
    for sd in (2, 3, 4, 5, 6, 8, 10, 12, 15, 20):
        for n in (4, 9, 16, 25, 36, 64, 100, 400):
            sn = math.isqrt(n)
            for zs, conf in (("1.96", 95), ("2.58", 99)):
                z = Fraction(zs)
                half = z * Fraction(sd, sn)
                L = 2 * half
                if not _termdec(half):
                    continue
                q = f"σ = {sd} n = {n} {conf}% 신뢰구간 길이"
                r = _row(q, L, Q=f"모표준편차가 {sd}인 정규모집단에서 크기가 {n}인 표본을 임의추출하여 모평균 m을 신뢰도 {conf}%로 추정할 때, 신뢰구간의 길이를 구하시오. (단, Z가 표준정규분포를 따를 때 P(|Z| ≤ {zs}) = {conf / 100:.2f}로 계산한다.)", STEP=f"신뢰구간 x̄ − {zs} × [[frac({sd}, sqrt({n}))]] ≤ m ≤ x̄ + {zs} × [[frac({sd}, sqrt({n}))]], 길이 = 2 × {zs} × [[frac({sd}, {sn})]]", KIND="신뢰구간의 길이", N=n)
                if r: out[f"L{sd}_{n}_{conf}"] = r
                for xbar in (50, 60, 100, 120):
                    hi = xbar + half
                    q2 = f"x̄ = {xbar} σ = {sd} n = {n} {conf}% 상한"
                    r2 = _row(q2, hi, Q=f"모표준편차가 {sd}인 정규모집단에서 크기가 {n}인 표본을 임의추출하여 얻은 표본평균이 {xbar}이다. 모평균 m에 대한 신뢰도 {conf}%의 신뢰구간이 a ≤ m ≤ b일 때, b의 값을 구하시오. (단, Z가 표준정규분포를 따를 때 P(|Z| ≤ {zs}) = {conf / 100:.2f}로 계산한다.)", STEP=f"b = x̄ + {zs} × [[frac({sd}, sqrt({n}))]] = {xbar} + {zs} × [[frac({sd}, {sn})]] = {xbar} + {_fm(half)}", KIND="신뢰구간의 상한", N=n)
                    if r2: out[f"U{sd}_{n}_{conf}_{xbar}"] = r2
    return _pick(out, 330)


ST5_ROWS = _st5_rows()


def st_t5():
    return T(ST, 5, ST_B, title="모평균의 추정 — 신뢰구간의 길이와 끝점",
        skill="신뢰구간 x̄ ± k·σ/√n(k = 1.96 또는 2.58)에서 길이 2kσ/√n과 끝점 계산하기", axis={"σ": "2~20", "n": "4~400(제곱수)", "신뢰도": "95% / 99%", "묻는 것": "길이 / 상한"}, disc="σ/√n에 신뢰도에 맞는 k를 곱하고 길이는 그 2배임을 아는가", diff=3,
        params=[{"name": "f", "values": {"in": list(ST5_ROWS)}}], table={"key": "f", "rows": ST5_ROWS},
        derive={"ans": "VN/VD"}, cost=["N", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{dec(ans)}",
        sol1="모표준편차 σ를 알 때 모평균 m의 신뢰구간은 x̄ − k·σ/√n ≤ m ≤ x̄ + k·σ/√n이다(신뢰도 95%: k = 1.96, 99%: k = 2.58). 신뢰구간의 길이는 2k·σ/√n이다. 이 문제는 {KIND}을 묻는다.",
        sol2=[("신뢰구간 x̄ ± k·σ/√n", "공식"), ("{STEP}", "대입"), ("= {dec(ans)}", None, ("{dec(ans)}", "{KIND}"))],
        sol3=["n이 커지면 구간이 짧아지고 신뢰도가 높아지면 길어지는지 확인한다. 따라서 {KIND}은 {dec(ans)}이다.", "{STEP}", "답 {dec(ans)}"],
        model="{STEP} = {dec(ans)}이다.",
        rubric=[("공식", 3, "{STEP} 꼴로 세웠다.", "k를 신뢰도에 맞지 않게 썼으면 1점."), ("계산", 2, "{dec(ans)}{eul(dec(ans))} 구했다.", "√n 계산 실수면 1점.")],
        pitfalls=[("길이를 k·σ/√n(반쪽)으로 둠", "공식", "부분"), ("σ/n으로 둠", "공식", "불인정"), ("1.96과 2.58 혼동", "공식", "부분")])


def _st6_rows():
    out = {}
    for n in (100, 400, 900, 1600, 2500):
        for pn, pd in ((1, 2), (1, 4), (3, 4), (1, 5), (2, 5), (3, 5), (4, 5), (1, 10), (3, 10), (7, 10), (9, 10)):
            p = Fraction(pn, pd)
            V = p * (1 - p) / n
            sd = None
            sn = math.isqrt(n)
            num = p * (1 - p)
            # sd = sqrt(p(1-p))/sqrt(n): sqrt(p(1-p)) rational iff numerator/denominator squares
            if math.isqrt(num.numerator) ** 2 == num.numerator and math.isqrt(num.denominator) ** 2 == num.denominator:
                sd = Fraction(math.isqrt(num.numerator), math.isqrt(num.denominator) * sn)
            for kk, ask, v, step in (("E", "E(p̂)", p, f"E(p̂) = p = {_fm(p)}"), ("V", "V(p̂)", V, f"V(p̂) = [[frac(p(1 − p), n)]] = [[frac({_fi(p)} × {_fi(1 - p)}, {n})]]"), ("S", "σ(p̂)", sd, f"σ(p̂) = [[sqrt(frac(p(1 − p), n))]] = [[sqrt(frac({_fi(num)}, {n}))]]")):
                if v is None or v == 0 or not _termdec(v):
                    continue
                q = f"모비율 {_fm(p)} n = {n} {ask}"
                r = _row(q, v, Q=f"모비율이 {_fm(p)}인 모집단에서 크기가 {n}인 표본을 임의추출할 때, 표본비율 p̂에 대하여 {ask}의 값을 구하시오.", STEP=step, ASK=ask, N=n)
                if r: out[f"{n}_{p}_{kk}"] = r
    for n in (100, 400, 900, 1600, 2500):
        for pn, pd in ((1, 2), (1, 5), (4, 5), (3, 10), (2, 5)):
            p = Fraction(pn, pd)
            num = p * (1 - p)
            sn = math.isqrt(n)
            if not (math.isqrt(num.numerator) ** 2 == num.numerator and math.isqrt(num.denominator) ** 2 == num.denominator):
                continue
            sd = Fraction(math.isqrt(num.numerator), math.isqrt(num.denominator) * sn)
            L = 2 * Fraction("1.96") * sd
            if not _termdec(L):
                continue
            q = f"표본비율 {_fm(p)} n = {n} 95% 신뢰구간 길이"
            r = _row(q, L, Q=f"크기가 {n}인 표본에서 표본비율이 {_fm(p)}일 때, 모비율 p에 대한 신뢰도 95%의 신뢰구간의 길이를 구하시오. (단, Z가 표준정규분포를 따를 때 P(|Z| ≤ 1.96) = 0.95로 계산한다.)", STEP=f"길이 = 2 × 1.96 × √(p̂(1 − p̂)/n) = 2 × 1.96 × [[sqrt(frac({_fi(num)}, {n}))]] = 2 × 1.96 × {_fm(sd)}", ASK="신뢰구간의 길이", N=n)
            if r: out[f"L{n}_{p}"] = r
    return _pick(out, 330)


ST6_ROWS = _st6_rows()


def st_t6():
    return T(ST, 6, ST_B, title="표본비율의 분포와 모비율의 추정",
        skill="E(p̂) = p, V(p̂) = p(1 − p)/n, 모비율의 95% 신뢰구간 길이 2 × 1.96 × √(p̂(1 − p̂)/n) 쓰기", axis={"p": "1/10~9/10", "n": "100~2500", "묻는 것": "E / V / σ / 신뢰구간 길이"}, disc="표본비율의 분산이 p(1 − p)/n임을 알고 신뢰구간 길이를 세우는가", diff=3,
        params=[{"name": "f", "values": {"in": list(ST6_ROWS)}}], table={"key": "f", "rows": ST6_ROWS},
        derive={"ans": "VN/VD"}, cost=["N", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{dec(ans)}",
        sol1="모비율 p인 모집단에서 크기 n인 표본의 표본비율 p̂는 E(p̂) = p, V(p̂) = p(1 − p)/n이고, n이 충분히 크면 정규분포에 가깝다. 모비율의 신뢰도 95% 신뢰구간은 p̂ ± 1.96√(p̂(1 − p̂)/n)이다.",
        sol2=[("E(p̂) = p, V(p̂) = p(1 − p)/n", "표본비율의 분포"), ("{STEP}", "대입"), ("{ASK} = {dec(ans)}", None, ("{dec(ans)}", "{ASK}"))],
        sol3=["p(1 − p) ≤ 1/4이므로 분산이 1/(4n) 이하인지 확인한다. 따라서 {ASK} = {dec(ans)}이다.", "{STEP}", "답 {dec(ans)}"],
        model="{STEP}이므로 {ASK} = {dec(ans)}이다.",
        rubric=[("공식", 3, "{STEP} 꼴로 세웠다.", "분산을 p(1 − p)로 두었으면(n으로 나누지 않음) 인정하지 않는다."), ("계산", 2, "{dec(ans)}{eul(dec(ans))} 구했다.", "제곱근 계산 실수면 1점.")],
        pitfalls=[("V(p̂) = p(1 − p)로 둠", "공식", "불인정"), ("신뢰구간 길이를 반쪽만 구함", "계산", "부분"), ("√(p(1 − p)/n) 계산 실수", "계산", "부분")])


ST_SEED = SEED(ST, category="확률", title="통계 — 확률분포표의 평균·분산·이항분포·정규분포 표준화·표본평균·모평균 추정·모비율", unit_id="h3-2", concept_ids=["h3-2-08", "h3-2-09", "h3-2-10", "h3-2-11", "h3-2-12", "h3-2-13", "h3-2-14"],
               schema_name="통계적 추정", note="정규분포는 발문에 표준정규분포표 값(0.3413·0.4772·…)을 주고 소수 답(dec). 신뢰구간은 1.96·2.58 을 분수로 정확히 계산.",
               templates=[st_t1(), st_t2(), st_t3(), st_t4(), st_t5(), st_t6()])


if __name__ == "__main__":
    run(CB_SEED, PR_SEED, ST_SEED)
