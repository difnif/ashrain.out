# itemfactory/tools/mkseed_h2_calc1.py — 고2 수학II 극한·연속·미분 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h2_calc1.py
#     → seeds/h2-2-lim.json    (극한·연속: 극한값 계산·극한의 성질·미정계수·연속 조건·사잇값 정리·좌우극한, 6틀)
#     → seeds/h2-2-diff.json   (미분: 미분계수 정의·도함수 값·접선·평균값 정리·증감 구간·극대극소, 6틀)
#   다항식은 _pm(계수)로 마커 안 문법(pow), _pt(계수)로 본문 표기(위첨자)를 만든다.
from __future__ import annotations

import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
from genkit.expr import eul as _eul, ika as _ika  # noqa: E402

rng = random.Random(20260918)
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def _nums(text):
    return {Fraction(x) for x in re.findall(r"(?<![\d.])-?\d+(?![\d.])", text)}


def _fm(v):
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"[[{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})]]"


def _fmp(v):
    return f"({_fm(v)})" if Fraction(v) < 0 else _fm(v)


def _pick(d, n):
    keys = sorted(d)
    rng.shuffle(keys)
    return {k: d[k] for k in keys[:n]}


def _poly(coefs, var="x", marker=False):
    """coefs: 최고차부터 [a_n, …, a_0]. marker=True 면 pow(x,n) 문법, 아니면 위첨자."""
    n = len(coefs) - 1
    parts = []
    for i, c in enumerate(coefs):
        d = n - i
        if c == 0:
            continue
        c = Fraction(c)
        sign = "−" if c < 0 else "+"
        a = abs(c)
        if d == 0:
            body = _fm(a) if not marker else (str(a) if a.denominator == 1 else f"frac({a.numerator},{a.denominator})")
        else:
            co = "" if a == 1 else (_fm(a) if not marker else (str(a) if a.denominator == 1 else f"frac({a.numerator},{a.denominator})"))
            if d == 1:
                body = f"{co}{var}"
            else:
                body = f"{co}pow({var},{d})" if marker else f"{co}{var}{str(d).translate(SUP)}"
        if not parts:
            parts.append(("-" if c < 0 else "") + body if marker else ("−" if c < 0 else "") + body)
        else:
            parts.append(f"{sign} {body}")
    return " ".join(parts) if parts else "0"


def _pm(coefs, var="x"):
    return _poly(coefs, var, marker=True)


def _pt(coefs, var="x"):
    return _poly(coefs, var, marker=False)


def _ev(coefs, x):
    v = Fraction(0)
    for c in coefs:
        v = v * x + c
    return v


def _der(coefs):
    n = len(coefs) - 1
    return [c * (n - i) for i, c in enumerate(coefs[:-1])] or [0]


# ═══════════════════════════════════════════════════════════════════ 1. 극한·연속
LM = "h2-2-lim"
LM_B = {**HS, "prereq": ["인수분해", "유리식"], "ops": ["극한"], "traps": ["0/0 꼴 약분", "좌우극한 구분"], "tags": ["함수의 극한", "연속"]}


def _lm1_rows():
    out = {}
    for a in range(-4, 6):
        for b in range(-6, 7):
            if a == b:
                continue
            num = [1, -(a + b), a * b]
            v = a - b
            q = f"[[lim(x, {a}, frac({_pm(num)}, x − {a}))]]" if a >= 0 else f"[[lim(x, {a}, frac({_pm(num)}, x + {-a}))]]"
            if v == 0 or Fraction(v) in _nums(q):
                continue
            out[f"r{a}_{b}"] = {"EXPR": q, "VN": v, "VD": 1, "KIND": "0/0 꼴 — 인수분해 후 약분", "STEP": f"분자 = (x {'−' if a > 0 else '+'} {abs(a)})(x {'−' if b > 0 else '+'} {abs(b)})이므로 약분하면 x {'−' if b > 0 else '+'} {abs(b)}" if b != 0 else f"분자 = x(x {'−' if a > 0 else '+'} {abs(a)})이므로 약분하면 x", "RES": f"x → {a}{_eul(a)} 대입: {a} {'−' if b > 0 else '+'} {abs(b)} = {v}" if b != 0 else f"x → {a}{_eul(a)} 대입: {v}"}
    for p in range(1, 7):
        for qd in range(1, 7):
            for s2 in (-5, -3, -1, 2, 4, 5):
                num = [p, s2, 1]
                den = [qd, 0, -3] if p != qd else [qd, 1, -3]
                v = Fraction(p, qd)
                q = f"[[lim(x, inf, frac({_pm(num)}, {_pm(den)}))]]"
                if v in _nums(q):
                    continue
                out[f"i{p}_{qd}_{s2}"] = {"EXPR": q, "VN": v.numerator, "VD": v.denominator, "KIND": "∞/∞ 꼴 — 최고차항으로 나눔", "STEP": f"분모·분자를 x²으로 나누면 [[frac({p} + frac({s2}, x) + frac(1, pow(x,2)), {qd} {'+ frac(1, x) ' if p == qd else ''}− frac(3, pow(x,2)))]]", "RES": f"x → ∞이면 1/x, 1/x² → 0이므로 극한값은 [[frac({p}, {qd})]] = {_fm(v)}"}
    for s in (1, 2, 3, 4, 5, 6):
        a = s * s
        v = Fraction(1, 2 * s)
        q = f"[[lim(x, 0, frac(sqrt(x + {a}) − {s}, x))]]"
        out[f"s{a}"] = {"EXPR": q, "VN": v.numerator, "VD": v.denominator, "KIND": "0/0 꼴 — 분자 유리화", "STEP": f"분자·분모에 [[sqrt(x + {a})]] + {s}{_eul(s)} 곱하면 [[frac(x, x(sqrt(x + {a}) + {s}))]] = [[frac(1, sqrt(x + {a}) + {s})]]", "RES": f"x → 0을 대입: [[frac(1, {s} + {s})]] = {_fm(v)}"}
        for c in range(1, 5):
            v2 = Fraction(c, 2 * s)
            q2 = f"[[lim(x, 0, frac(sqrt({c}x + {a}) − {s}, x))]]" if c > 1 else None
            if q2 and v2 not in _nums(q2):
                out[f"s{a}_{c}"] = {"EXPR": q2, "VN": v2.numerator, "VD": v2.denominator, "KIND": "0/0 꼴 — 분자 유리화", "STEP": f"분자·분모에 [[sqrt({c}x + {a})]] + {s}{_eul(s)} 곱하면 [[frac({c}x, x(sqrt({c}x + {a}) + {s}))]] = [[frac({c}, sqrt({c}x + {a}) + {s})]]", "RES": f"x → 0을 대입: [[frac({c}, {s} + {s})]] = {_fm(v2)}"}
    for a in range(1, 13):
        v = Fraction(a, 2)
        q = f"[[lim(x, inf, sqrt(pow(x,2) + {'' if a == 1 else a}x) − x)]]"
        if v in _nums(q):
            continue
        out[f"d{a}"] = {"EXPR": q, "VN": v.numerator, "VD": v.denominator, "KIND": "∞ − ∞ 꼴 — 유리화", "STEP": f"[[sqrt(pow(x,2) + {'' if a == 1 else a}x)]] + x를 곱하고 나누면 [[frac({'' if a == 1 else a}x, sqrt(pow(x,2) + {'' if a == 1 else a}x) + x)]], 분모·분자를 x로 나누면 [[frac({a}, sqrt(1 + frac({a}, x)) + 1)]]", "RES": f"x → ∞이면 {a}/x → 0이므로 [[frac({a}, 1 + 1)]] = {_fm(v)}"}
    return _pick(out, 330)


LM1_ROWS = _lm1_rows()


def lm_t1():
    return T(LM, 1, LM_B, title="함수의 극한값 계산 — 0/0, ∞/∞, ∞ − ∞",
        skill="0/0은 인수분해·유리화로 약분, ∞/∞는 최고차항으로 나누기, ∞ − ∞는 유리화로 극한값 구하기", axis={"꼴": "0/0(인수분해·유리화) / ∞/∞ / ∞ − ∞", "값": "정수·분수"}, disc="꼴을 판단해 알맞은 변형(약분·유리화·최고차항)을 고르는가", diff=2,
        params=[{"name": "f", "values": {"in": list(LM1_ROWS)}}], table={"key": "f", "rows": LM1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="그대로 대입하면 0/0, ∞/∞, ∞ − ∞ 같은 부정형이 된다. 0/0은 분모를 0으로 만드는 인수를 약분(인수분해 또는 유리화)하고, ∞/∞는 분모의 최고차항으로 나누며, ∞ − ∞는 유리화해 ∞/∞ 꼴로 바꾼다. 이 문제는 {KIND}이다.",
        sol2=[("꼴 판단: {KIND}", "부정형"), ("{STEP}", "변형"), ("{RES} → {ans}", None, ("{ans}", "극한값"))],
        sol3=["변형 전후의 식이 극한을 구하는 점 근처(그 점 제외)에서 같은 함수인지 확인한다. 따라서 극한값은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{KIND}이다. {STEP}. {RES}. 따라서 극한값은 {ans}이다.",
        rubric=[("변형", 3, "{STEP} 꼴로 변형했다.", "약분·유리화 없이 대입만 했으면 인정하지 않는다."), ("극한값", 2, "{ans}{eul(ans)} 구했다.", "대입 계산 실수면 1점.")],
        pitfalls=[("0/0을 0으로 답함", "변형", "불인정"), ("∞/∞에서 최고차항의 계수비 대신 상수항 비를 씀", "변형", "불인정"), ("유리화 후 부호 실수", "극한값", "부분")])


def lm_t2():
    return T(LM, 2, LM_B, title="함수의 극한의 성질 — 주어진 극한으로 다른 극한 구하기",
        skill="lim f(x)/(x − a) = L(즉 f(x) → 0)를 써서 f(x)가 들어간 다른 극한을 계산하기", axis={"a": "1~4", "L": "±1~±6", "묻는 것": "(x + c)f/(x − a), (x² − a²)f/(x − a)², f/(x² − a²)"}, disc="극한의 곱·몫의 성질로 나누어 알고 있는 극한을 끼워 넣는가", diff=3,
        params=[{"name": "a", "values": {"int": [1, 4]}}, {"name": "L", "values": {"in": NZ(-6, 6)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "k", "values": {"in": ["mul", "sq", "div"]}}],
        table={"key": "k", "rows": {"mul": {"ASK": "frac((x + c) f(x), x − a)", "LAW": "(x + c) × f(x)/(x − a)로 쪼갠다", "w1": 1, "w2": 0, "w3": 0},
                                    "sq": {"ASK": "frac((pow(x,2) − pow(a,2)) f(x), pow(x − a, 2))", "LAW": "(x² − a²)/(x − a) = x + a 와 f(x)/(x − a)로 쪼갠다", "w1": 0, "w2": 1, "w3": 0},
                                    "div": {"ASK": "frac(f(x), pow(x,2) − pow(a,2))", "LAW": "f(x)/(x − a) × 1/(x + a)로 쪼갠다", "w1": 0, "w2": 0, "w3": 1}}},
        derive={"a2": "a*a", "ans": "w1*(a + c)*L + w2*2*a*L + w3*L/(2*a)", "fac": "w1*(a + c) + w2*2*a + w3*1/(2*a)"},
        constraints=["a + c != 0", "ans != 0", "ans not in (a, L, c, a2)"], cost=["a", "L", "c", "ans"], verify=["ans == fac*L"],
        q="함수 f(x)에 대하여 [[lim(x, {a}, frac(f(x), x − {a}))]] = {L}일 때, [[lim(x, {a}, {ASK})]]의 값을 구하시오. (단, 식의 a는 {a}, c는 {c}이다.)", answer="{ans}",
        sol1="극한의 성질: 두 함수의 극한이 존재하면 곱·몫(분모 ≠ 0)의 극한은 극한의 곱·몫이다. 주어진 f(x)/(x − {a}) → {L}을 인수로 남기고 나머지를 따로 대입한다. {LAW}.",
        sol2=[("{LAW}", "쪼개기"), ("남은 인수의 극한: {fac}, 알고 있는 극한: {L}", "각각의 극한"), ("곱하면 {fac} × {pn(L)} = {ans}", None, ("{ans}", "극한값"))],
        sol3=["쪼갠 두 인수가 각각 극한을 가지는지(분모가 0이 되지 않는지) 확인한다. 따라서 극한값은 {ans}이다.", "{fac} × {pn(L)}", "답 {ans}"],
        model="{LAW}. 남은 인수는 x → {a}에서 {fac}, 주어진 극한은 {L}이므로 곱은 {ans}이다.",
        rubric=[("쪼개기", 3, "주어진 극한 f(x)/(x − {a})를 인수로 분리했다.", "f(x) → 0을 모르고 f({a})로 대입했으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "남은 인수의 극한 실수면 1점.")],
        pitfalls=[("f(a)를 임의로 정해 대입", "쪼개기", "불인정"), ("(x² − a²)/(x − a)를 x − a로 약분", "쪼개기", "불인정"), ("남은 인수의 대입 실수", "계산", "부분")])


def _lm2_fix(t):
    """ASK 행 문자열의 a, c 는 실제 수로 채워야 한다 — 마커 안에 자리표시자를 둘 수 없으므로 세 갈래를 파생 대신 행에서 정적 fragment 로 조합한다."""
    t["table"] = {"key": "k", "rows": {"mul": {"LAW": "(x + c) × f(x)/(x − a)로 쪼갠다", "PRE": "((x ", "MID": ") f(x), x − ", "POST": ")", "w1": 1, "w2": 0, "w3": 0},
                                       "sq": {"LAW": "(x² − a²)/(x − a) = x + a 와 f(x)/(x − a)로 쪼갠다", "PRE": "((pow(x,2) ", "MID": ") f(x), pow(x − ", "POST": ", 2))", "w1": 0, "w2": 1, "w3": 0},
                                       "div": {"LAW": "f(x)/(x − a) × 1/(x + a)로 쪼갠다", "PRE": "(f(x), (x ", "MID": ")(x + ", "POST": "))", "w1": 0, "w2": 0, "w3": 1}}}
    t["derive"] = {"a2": "a*a", "ans": "w1*(a + c)*L + w2*2*a*L + w3*L/(2*a)", "fac": "w1*(a + c) + w2*2*a + w3*1/(2*a)", "arg1": "w1*c - w2*a*a - w3*a", "arg2": "a"}
    t["question"] = "함수 f(x)에 대하여 [[lim(x, {a}, frac(f(x), x − {a}))]] = {L}일 때, [[lim(x, {a}, frac{PRE}{sgn(arg1)}{MID}{arg2}{POST})]]의 값을 구하시오."
    return t


def lm_t3():
    return T(LM, 3, LM_B, title="극한값으로 미정계수 정하기 — 분모 → 0이면 분자 → 0",
        skill="lim (x² + ax + b)/(x − p) = L에서 분자가 x = p를 근으로 가짐을 써서 a, b 구하기", axis={"p": "−3~4", "L": "다른 근 q로 결정", "묻는 것": "a + b / ab / b − a"}, disc="극한이 존재하고 분모 → 0이면 분자 → 0이어야 함을 쓰고, 약분 후 대입해 L과 맞추는가", diff=3,
        params=[{"name": "p", "values": {"int": [-4, 5]}}, {"name": "qv", "values": {"int": [-7, 7]}}, {"name": "k", "values": {"in": ["sum", "prod", "diff"]}}],
        table={"key": "k", "rows": {"sum": {"ASK": "a + b", "wa": 1, "wb": 0, "wc": 0}, "prod": {"ASK": "ab", "wa": 0, "wb": 1, "wc": 0}, "diff": {"ASK": "b − a", "wa": 0, "wb": 0, "wc": 1}}},
        derive={"a": "-(p + qv)", "b": "p*qv", "L": "p - qv", "np": "-p", "nq": "-qv", "ans": "wa*(a + b) + wb*a*b + wc*(b - a)"},
        constraints=["p != qv", "L != 0", "a != 0", "b != 0", "ans != 0", "ans not in (p, L, a, b)"], cost=["p", "qv", "a", "b", "L", "ans"], verify=["p*p + a*p + b == 0", "2*p + a == L"],
        q="[[lim(x, {p}, frac(pow(x,2) + a x + b, x {sgn(np)}))]] = {L}일 때, 상수 a, b에 대하여 {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="x → {p}에서 분모 x {sgn(np)} → 0인데 극한값이 존재하므로 분자도 → 0이어야 한다: {pn(p)}² + {pn(p)}a + b = 0. 그러면 분자는 (x {sgn(np)})(x {sgn(nq)}) 꼴로 인수분해되고, 약분한 뒤 x = {p}를 넣은 값이 {L}이 되어야 한다.",
        sol2=[("분자 → 0: {pn(p)}² + {pn(p)}a + b = 0 → b = {pn(-p*p)} − {pn(p)}a", "필요조건"), ("약분 후 x → {p}: 분자 = (x {sgn(np)})(x {sgn(nq)}), 극한 = {p} {sgn(nq)} = {L}", "L과 맞추기"), ("a = {a}, b = {b} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["a = {a}, b = {b}를 넣으면 분자 x² {sgt(a)}x {sgn(b)} = (x {sgn(np)})(x {sgn(nq)})이고 약분하면 x {sgn(nq)} → {L}{ika(L)} 되어 조건에 맞는다. 따라서 {ASK} = {ans}이다.", "(x {sgn(np)})(x {sgn(nq)})", "{ASK} = {ans}"],
        model="분모 → 0이므로 분자 → 0: b = {pn(-p*p)} − {pn(p)}a. 분자 = (x {sgn(np)})(x {sgn(nq)})이 되어 극한 {p} {sgn(nq)} = {L}에서 a = {a}, b = {b}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("필요조건", 3, "분자 → 0 조건 {pn(p)}² + {pn(p)}a + b = 0을 세웠다.", "이 조건 없이 값을 맞췄으면 1점."), ("a, b·답", 2, "a = {a}, b = {b}, {ASK} = {ans}{eul(ans)} 구했다.", "약분 후 대입 실수면 1점.")],
        pitfalls=[("분자 → 0 조건을 쓰지 않음", "필요조건", "불인정"), ("약분하지 않고 분자만으로 L을 맞춤", "a, b·답", "불인정"), ("계산 실수", "a, b·답", "부분")])


def lm_t5():
    return T(LM, 5, LM_B, title="사잇값 정리 — 열린구간에서 실근을 갖는 정수 k의 개수",
        skill="증가하는 연속함수 f(x) = x³ + cx − k가 (p, p + 1)에서 근을 가질 조건 f(p) < 0 < f(p + 1) 세우기", axis={"c": "1~6", "p": "−2~3"}, disc="구간 양 끝의 함숫값의 부호가 다르면 사잇값 정리로 근이 존재함을 쓰고, 부등식에서 정수 k를 세는가", diff=3,
        params=[{"name": "c", "values": {"int": [1, 9]}}, {"name": "d", "values": {"in": NZ(-4, 4)}}, {"name": "p", "values": {"int": [-3, 4]}}],
        derive={"p1": "p + 1", "fp": "p**3 + c*p + d", "fp1": "(p + 1)**3 + c*(p + 1) + d", "ans": "3*p*p + 3*p + c"},
        constraints=["ans not in (c, d, p, p1, fp, fp1)"], cost=["c", "d", "p", "fp", "fp1", "ans"], verify=["ans == fp1 - fp - 1"],
        q="함수 f(x) = x³ {sgt(c)}x {sgn(d)} − k에 대하여 방정식 f(x) = 0이 열린구간 ({p}, {p1})에서 실근을 갖도록 하는 정수 k의 개수를 구하시오.", answer="{ans}",
        sol1="f(x)는 연속이고 f'(x) = 3x² + {c} > 0이므로 증가함수이다. 따라서 (p, p + 1)에서 실근을 가질 필요충분조건은 사잇값 정리에 의해 f({p}) < 0 < f({p1}), 즉 {fp} − k < 0 < {fp1} − k이다.",
        sol2=[("f({p}) = {fp} − k, f({p1}) = {fp1} − k", "구간 끝의 값"), ("f({p}) < 0 < f({p1}) → {fp} < k < {fp1}", "부호가 달라야 함"), ("정수 k의 개수 = {ans}", None, ("{ans}", "개수"))],
        sol3=["k = {fp}이나 k = {fp1}이면 근이 구간의 끝에 놓여 열린구간 안에 없으므로 경계는 제외한다. 따라서 개수는 {fp1} − {pn(fp)} − 1 = {ans}이다.", "{fp} < k < {fp1}", "개수 {ans}"],
        model="f는 증가하는 연속함수이므로 f({p}) < 0 < f({p1}), 즉 {fp} < k < {fp1}이어야 한다. 따라서 정수 k의 개수는 {ans}이다.",
        rubric=[("사잇값 정리", 3, "f({p}) < 0 < f({p1}){eul(fp1)} 세웠다.", "부등호 방향이 반대면 인정하지 않는다."), ("개수", 2, "{ans}개를 구했다.", "경계를 포함해 세었으면 1점.")],
        pitfalls=[("f(p)f(p + 1) ≤ 0으로 등호 포함", "개수", "부분"), ("증가함수임을 확인하지 않고 충분조건만 씀", "사잇값 정리", "부분"), ("함숫값 계산 실수", "사잇값 정리", "부분")])


def lm_t6():
    return T(LM, 6, LM_B, title="좌극한과 우극한 — 조각 정의 함수",
        skill="x = p의 양쪽에서 각각 해당 조각의 식으로 극한을 구해 더하기", axis={"p": "−3~4", "조각": "x² + a / bx + c"}, disc="x → p+와 x → p−에서 어느 식을 써야 하는지 구별하는가", diff=2,
        params=[{"name": "p", "values": {"int": [-3, 4]}}, {"name": "a", "values": {"in": NZ(-5, 5)}}, {"name": "b", "values": {"in": NZ(-4, 4)}}, {"name": "c", "values": {"in": NZ(-6, 6)}}],
        derive={"R": "p*p + a", "Lf": "b*p + c", "ans": "p*p + a + b*p + c"},
        constraints=["R != Lf", "ans != 0", "ans not in (p, a, b, c, R, Lf)"], cost=["p", "a", "b", "c", "R", "Lf", "ans"], verify=["ans == R + Lf"],
        q="함수 f(x) = [[cases(pow(x,2) {sgn(a)}, x ≥ {p}, {co(b)}x {sgn(c)}, x < {p})]]에 대하여 [[lim(x, {p}, f(x), +)]] + [[lim(x, {p}, f(x), -)]]의 값을 구하시오.", answer="{ans}",
        sol1="우극한 x → {p}+는 x ≥ {p}인 쪽의 식 x² {sgn(a)}에, 좌극한 x → {p}−는 x < {p}인 쪽의 식 {co(b)}x {sgn(c)}에 x = {p}를 대입해 구한다(다항식은 연속이므로 대입으로 극한을 얻는다).",
        sol2=[("우극한: [[lim(x, {p}, pow(x,2) {sgn(a)}, +)]] = {pn(p)}² {sgn(a)} = {R}", "x ≥ {p} 쪽"), ("좌극한: [[lim(x, {p}, {co(b)}x {sgn(c)}, -)]] = {b*p} {sgn(c)} = {Lf}", "x < {p} 쪽"), ("합: {R} + {pn(Lf)} = {ans}", None, ("{ans}", "합"))],
        sol3=["좌극한과 우극한이 다르므로({R} ≠ {Lf}) x = {p}에서 극한값은 존재하지 않지만, 각각의 값은 정해진다. 따라서 합은 {ans}이다.", "우극한 {R}, 좌극한 {Lf}", "합 {ans}"],
        model="우극한은 x² {sgn(a)}에 대입한 {R}, 좌극한은 {co(b)}x {sgn(c)}에 대입한 {Lf}이므로 합은 {ans}이다.",
        rubric=[("좌·우극한", 3, "우극한 {R}, 좌극한 {Lf}{eul(Lf)} 구했다.", "식을 바꿔 대입했으면 인정하지 않는다."), ("합", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("x ≥ p 쪽 식으로 좌극한을 구함", "좌·우극한", "불인정"), ("극한값이 없다고 답함", "합", "불인정"), ("대입 계산 실수", "합", "부분")])


def _lm4_frac():
    """t4: 0/0 꼴 분수 + 한 점 정의 — 연속이 되도록 하는 k"""
    return T(LM, 4, LM_B, title="함수의 연속 — 0/0 꼴 분수 함수가 연속이 되도록 하는 k",
        skill="x = p에서 연속 ⇔ lim f(x) = f(p)를 써서 약분한 극한값을 k로 놓기", axis={"p": "−3~4", "다른 근": "−5~5"}, disc="분수식을 약분해 극한값을 구하고 그것을 f(p) = k와 같다고 놓는가", diff=2,
        params=[{"name": "p", "values": {"int": [-3, 4]}}, {"name": "qv", "values": {"int": [-5, 5]}}, {"name": "m", "values": {"int": [1, 3]}}],
        derive={"s": "-m*(p + qv)", "pr": "m*p*qv", "np": "-p", "nq": "-qv", "ans": "m*(p - qv)"},
        constraints=["p != qv", "ans != 0", "pr != 0", "ans not in (p, qv, s, pr, m)"], cost=["p", "qv", "m", "ans"], verify=["m*p*p + s*p + pr == 0"],
        q="함수 f(x) = [[cases(frac({co(m)}pow(x,2) {sgt(s)}x {sgn(pr)}, x {sgn(np)}), x ≠ {p}, k, x = {p})]]가 x = {p}에서 연속이 되도록 하는 상수 k의 값을 구하시오.", answer="{ans}",
        sol1="x = {p}에서 연속이려면 [[lim(x, {p}, f(x))]] = f({p}) = k이어야 한다. x ≠ {p}에서 f(x)의 분자는 {m}(x {sgn(np)})(x {sgn(nq)})이므로 약분하면 {m}(x {sgn(nq)})이고, x → {p}일 때 극한값은 {m} × ({p} {sgn(nq)}) = {ans}이다.",
        sol2=[("연속 ⇔ [[lim(x, {p}, f(x))]] = f({p}) = k", "연속의 뜻"), ("[[lim(x, {p}, frac({m}(x {sgn(np)})(x {sgn(nq)}), x {sgn(np)}))]] = [[lim(x, {p}, {m}(x {sgn(nq)}))]] = {ans}", "약분 후 대입"), ("k = {ans}", None, ("{ans}", "k"))],
        sol3=["약분 전의 식은 x = {p}에서 정의되지 않지만 극한은 약분한 식으로 구할 수 있다. 따라서 k = {ans}이다.", "극한값 {ans} = k", "k = {ans}"],
        model="[[lim(x, {p}, f(x))]] = [[lim(x, {p}, {m}(x {sgn(nq)}))]] = {ans}이고 연속이려면 이 값이 f({p}) = k와 같아야 하므로 k = {ans}이다.",
        rubric=[("연속 조건·극한값", 3, "약분해 극한값 {ans}{eul(ans)} 구했다.", "약분 없이 0/0으로 두었으면 인정하지 않는다."), ("답", 2, "k = {ans}{eul(ans)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("0/0 꼴에서 극한값을 0으로 둠", "연속 조건·극한값", "불인정"), ("인수분해 실수", "연속 조건·극한값", "부분"), ("k를 다른 근으로 답함", "답", "불인정")])


def _lm7_piece():
    """t7: 두 조각 다항식이 연속이 되도록 하는 a"""
    return T(LM, 7, LM_B, title="함수의 연속 — 두 조각 다항식이 연속이 되도록 하는 상수",
        skill="이음점 x = p에서 두 조각의 값이 같아야 연속임을 써서 상수 정하기", axis={"p": "−3~4", "조각": "x² + a / bx + c"}, disc="이음점에서 좌극한 = 우극한 = 함숫값을 세우는가", diff=2,
        params=[{"name": "p", "values": {"int": [-3, 4]}}, {"name": "b", "values": {"in": NZ(-4, 4)}}, {"name": "c", "values": {"in": NZ(-6, 6)}}],
        derive={"Lf": "b*p + c", "p2": "p*p", "ans": "b*p + c - p*p"},
        constraints=["ans != 0", "ans not in (p, b, c, Lf, p2)"], cost=["p", "b", "c", "Lf", "ans"], verify=["p2 + ans == Lf"],
        q="함수 f(x) = [[cases(pow(x,2) + a, x ≥ {p}, {co(b)}x {sgn(c)}, x < {p})]]가 x = {p}에서 연속이 되도록 하는 상수 a의 값을 구하시오.", answer="{ans}",
        sol1="두 조각 모두 다항식이므로 x = {p}가 아닌 곳에서는 연속이다. x = {p}에서 연속이려면 좌극한(x < {p} 쪽 {co(b)}x {sgn(c)})과 우극한·함숫값(x ≥ {p} 쪽 x² + a)이 같아야 한다.",
        sol2=[("좌극한: {co(b)}x {sgn(c)}에 x = {p}{eul(p)} 대입하면 {b*p} {sgn(c)} = {Lf}", "x < {p} 쪽"), ("우극한 = 함숫값: {pn(p)}² + a = {p2} + a", "x ≥ {p} 쪽"), ("{p2} + a = {Lf} → a = {ans}", None, ("{ans}", "a"))],
        sol3=["a = {ans}일 때 두 조각의 x = {p}에서의 값이 모두 {Lf}{ro(Lf)} 같다. 따라서 a = {ans}이다.", "{p2} + {pn(ans)} = {Lf} ✓", "a = {ans}"],
        model="x = {p}에서 좌극한 {Lf}와 우극한·함숫값 {p2} + a가 같아야 하므로 a = {ans}이다.",
        rubric=[("연속 조건", 3, "{p2} + a = {Lf}{eul(Lf)} 세웠다.", "한쪽 조각의 값을 잘못 구했으면 1점."), ("답", 2, "a = {ans}{eul(ans)} 구했다.", "이항 실수면 1점.")],
        pitfalls=[("이음점이 아닌 곳의 값을 비교", "연속 조건", "불인정"), ("부호 실수", "답", "부분"), ("좌·우 조각을 바꿔 대입", "연속 조건", "불인정")])


LM_SEED = SEED(LM, category="해석", title="함수의 극한과 연속 — 극한값 계산·극한의 성질·미정계수·연속 조건(분수/조각)·사잇값 정리·좌우극한", unit_id="h2-2", concept_ids=["h2-2-01", "h2-2-02", "h2-2-03", "h2-2-04"],
               schema_name="함수의 극한과 연속", note="극한 식은 lim/frac/sqrt/cases 마커. 극한값 행은 파이썬에서 계산. 연속 조건은 분수형(t4)·조각형(t7)으로 나눔.",
               templates=[lm_t1(), _lm2_fix(lm_t2()), lm_t3(), _lm4_frac(), lm_t5(), lm_t6(), _lm7_piece()])


# ═══════════════════════════════════════════════════════════════════ 2. 미분
DF = "h2-2-diff"
DF_B = {**HS, "prereq": ["함수의 극한", "다항식의 연산"], "ops": ["미분"], "traps": ["미분계수 정의의 계수", "접선의 기울기와 접점"], "tags": ["미분계수", "도함수", "접선", "극값"]}


def df_t1():
    return T(DF, 1, DF_B, title="미분계수의 정의 — h → 0 꼴의 극한",
        skill="lim (f(p + h) − f(p))/h = f'(p)를 알고, h의 계수가 있으면 그만큼 곱해 미분계수로 옮기기", axis={"f": "x² + ax + b", "형태": "(f(p+h) − f(p))/h, (f(p+2h) − f(p))/h, (f(p+h) − f(p−h))/h"}, disc="극한식을 미분계수 정의와 비교해 계수를 정확히 붙이는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-5, 5)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "p", "values": {"in": NZ(-3, 4)}}, {"name": "k", "values": {"in": ["h", "2h", "sym"]}}],
        table={"key": "k", "rows": {"h": {"PRE": "lim(h, 0, frac(f(", "MID": " + h) − f(", "POST": "), h))", "MUL": 1, "LAW": "정의 그대로 f'(p)"},
                                    "2h": {"PRE": "lim(h, 0, frac(f(", "MID": " + 2h) − f(", "POST": "), h))", "MUL": 2, "LAW": "2h = t로 놓으면 2 × (f(p + t) − f(p))/t → 2f'(p)"},
                                    "sym": {"PRE": "lim(h, 0, frac(f(", "MID": " + h) − f(", "POST": " − h), h))", "MUL": 2, "LAW": "f(p)를 빼고 더하면 (f(p + h) − f(p))/h + (f(p − h) − f(p))/(−h) → f'(p) + f'(p) = 2f'(p)"}}},
        derive={"fp": "2*p + a", "ans": "MUL*(2*p + a)"},
        constraints=["fp != 0", "ans != 0", "ans not in (a, b, p)"], cost=["a", "b", "p", "fp", "ans"], verify=["ans == MUL*fp"],
        q="함수 f(x) = x² {sgt(a)}x {sgn(b)}에 대하여 [[{PRE}{p}{MID}{p}{POST}]]의 값을 구하시오.", answer="{ans}",
        sol1="미분계수의 정의는 f'(p) = [[lim(h, 0, frac(f(p + h) − f(p), h))]]이다. 주어진 극한을 이 꼴로 맞추면 {LAW}. f'(x) = 2x {sgn(a)}이므로 f'({p}) = {fp}이다.",
        sol2=[("f'(x) = 2x {sgn(a)}, f'({p}) = {fp}", "도함수"), ("{LAW}", "정의와 비교"), ("{MUL} × {pn(fp)} = {ans}", None, ("{ans}", "극한값"))],
        sol3=["h의 계수가 있을 때 그 계수를 극한 앞으로 빼는 과정을 되짚어 확인한다(2h = t 치환). 따라서 값은 {ans}이다.", "{MUL} × f'({p})", "답 {ans}"],
        model="f'(x) = 2x {sgn(a)}이므로 f'({p}) = {fp}이고, 주어진 극한은 {LAW}이므로 {ans}이다.",
        rubric=[("정의와 비교", 3, "극한식을 {MUL} × f'({p}) 꼴로 옮겼다.", "계수를 빠뜨렸으면 1점."), ("미분계수", 2, "f'({p}) = {fp}, 답 {ans}{eul(ans)} 구했다.", "도함수 계산 실수면 1점.")],
        pitfalls=[("2h의 계수 2를 빠뜨림", "정의와 비교", "부분"), ("f(p + h) − f(p − h)를 f'(p)로 봄", "정의와 비교", "부분"), ("f'(p) 계산 실수", "미분계수", "부분")])


def df_t7():
    return T(DF, 7, DF_B, title="미분계수의 정의 — x → p 꼴의 극한",
        skill="lim (f(x) − f(p))/(x − p) = f'(p)를 알고, 분모가 x² − p²이면 (x + p)로 나뉜 만큼 보정하기", axis={"f": "x² + ax + b", "형태": "(f(x) − f(p))/(x − p), (f(x) − f(p))/(x² − p²)"}, disc="x → p 꼴의 정의를 알아보고 분모를 (x − p)(x + p)로 쪼개는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-5, 5)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "p", "values": {"int": [1, 4]}}, {"name": "k", "values": {"in": ["lin", "sq"]}}],
        table={"key": "k", "rows": {"lin": {"POST": "), x − ", "END": ")", "LAW": "정의 그대로 f'(p)", "w": 1}, "sq": {"POST": "), pow(x,2) − pow(", "END": ",2))", "LAW": "x² − p² = (x − p)(x + p)이므로 f'(p)/(2p)", "w": 0}}},
        derive={"fp": "2*p + a", "ans": "w*(2*p + a) + (1 - w)*(2*p + a)/(2*p)", "p2": "2*p"},
        constraints=["fp != 0", "ans != 0", "ans not in (a, b, p)"], cost=["a", "b", "p", "fp", "ans"], verify=["w == 0 or ans == fp", "w == 1 or ans*p2 == fp"],
        q="함수 f(x) = x² {sgt(a)}x {sgn(b)}에 대하여 [[lim(x, {p}, frac(f(x) − f({p}{POST}{p}{END})]]의 값을 구하시오.", answer="{ans}",
        sol1="미분계수의 정의 f'(p) = [[lim(x, p, frac(f(x) − f(p), x − p))]]이다. {LAW}. f'(x) = 2x {sgn(a)}이므로 f'({p}) = {fp}이다.",
        sol2=[("f'(x) = 2x {sgn(a)}, f'({p}) = {fp}", "도함수"), ("{LAW}", "정의와 비교"), ("값 = {ans}", None, ("{ans}", "극한값"))],
        sol3=["분모가 x² − p²이면 (x − p)(x + p)로 쪼개 (x + p) → 2p를 따로 대입했는지 확인한다. 따라서 값은 {ans}이다.", "f'({p}) = {fp}", "답 {ans}"],
        model="f'(x) = 2x {sgn(a)}이므로 f'({p}) = {fp}이고, {LAW}이므로 값은 {ans}이다.",
        rubric=[("정의와 비교", 3, "극한식을 f'({p})로 옮겼다(x² − p²이면 2p로 나눔).", "보정을 빠뜨렸으면 1점."), ("미분계수", 2, "f'({p}) = {fp}, 답 {ans}{eul(ans)} 구했다.", "도함수 계산 실수면 1점.")],
        pitfalls=[("x² − p²을 x − p로 약분", "정의와 비교", "불인정"), ("f'(p) 계산 실수", "미분계수", "부분"), ("f(p)를 f'(p)로 착각", "정의와 비교", "불인정")])


def df_t2_cubic():
    return T(DF, 2, DF_B, title="도함수 계산 — 삼차 다항함수의 미분계수",
        skill="(xⁿ)' = nxⁿ⁻¹로 항별 미분해 f'(p) 계산하기", axis={"계수": "±1~±5", "p": "−3~3"}, disc="각 항을 지수·계수 규칙대로 미분하고 상수항은 0이 됨을 아는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-3, 3)}}, {"name": "b", "values": {"in": NZ(-4, 4)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "d", "values": {"in": NZ(-5, 5)}}, {"name": "p", "values": {"int": [-3, 3]}}],
        derive={"a3": "3*a", "b2": "2*b", "ans": "3*a*p*p + 2*b*p + c"},
        constraints=["ans != 0", "ans not in (a, b, c, d, p)"], cost=["a", "b", "c", "d", "p", "ans"], verify=["ans == a3*p*p + b2*p + c"],
        q="함수 f(x) = {co(a)}x³ {sgt(b)}x² {sgt(c)}x {sgn(d)}에 대하여 f'({p})의 값을 구하시오.", answer="{ans}",
        sol1="다항함수의 도함수는 (xⁿ)' = nxⁿ⁻¹, (상수)' = 0을 항별로 적용한다: f'(x) = {co(a3)}x² {sgt(b2)}x {sgn(c)}. 여기에 x = {p}를 대입한다.",
        sol2=[("f'(x) = {co(a3)}x² {sgt(b2)}x {sgn(c)}", "항별 미분"), ("f'({p}) = {a3} × {pn(p*p)} {sgt(b2)} × {pn(p)} {sgn(c)}", "대입"), ("= {ans}", None, ("{ans}", "f'({p})"))],
        sol3=["도함수의 차수가 2로 하나 낮아졌고 각 계수가 (지수 × 계수)인지, 상수항 {d}{ika(d)} 사라졌는지 확인한다. 따라서 f'({p}) = {ans}이다.", "f'(x) = {co(a3)}x² {sgt(b2)}x {sgn(c)}", "f'({p}) = {ans}"],
        model="f'(x) = {co(a3)}x² {sgt(b2)}x {sgn(c)}이므로 f'({p}) = {ans}이다.",
        rubric=[("도함수", 3, "f'(x) = {co(a3)}x² {sgt(b2)}x {sgn(c)}{eul(c)} 구했다.", "한 항의 미분 실수면 1점."), ("대입", 2, "f'({p}) = {ans}{eul(ans)} 구했다.", "대입 계산 실수면 1점.")],
        pitfalls=[("상수항을 미분하면 상수라고 둠", "도함수", "불인정"), ("지수를 곱하지 않고 내리기만 함", "도함수", "불인정"), ("대입 부호 실수(음수의 제곱)", "대입", "부분")])


def df_t3():
    return T(DF, 3, DF_B, title="접선의 방정식 — 곡선 위의 점에서의 접선 y = mx + n",
        skill="접점에서의 미분계수가 접선의 기울기임을 써서 y − f(p) = f'(p)(x − p)를 세우기", axis={"곡선": "x³ + ax² + bx", "접점": "x = −2~3", "묻는 것": "m + n / n"}, disc="기울기는 f'(p), 접선은 접점 (p, f(p))를 지남을 함께 쓰는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-3, 3)}}, {"name": "b", "values": {"in": NZ(-5, 5)}}, {"name": "p", "values": {"int": [-2, 3]}}, {"name": "k", "values": {"in": ["sum", "icpt"]}}],
        table={"key": "k", "rows": {"sum": {"ASK": "m + n", "w": 1}, "icpt": {"ASK": "n", "w": 0}}},
        derive={"fp": "p**3 + a*p*p + b*p", "m": "3*p*p + 2*a*p + b", "n": "p**3 + a*p*p + b*p - (3*p*p + 2*a*p + b)*p", "ans": "w*(3*p*p + 2*a*p + b + p**3 + a*p*p + b*p - (3*p*p + 2*a*p + b)*p) + (1 - w)*(p**3 + a*p*p + b*p - (3*p*p + 2*a*p + b)*p)", "a2": "2*a"},
        constraints=["m != 0", "n != 0", "ans != 0", "ans not in (a, b, p, fp, m)"], cost=["a", "b", "p", "fp", "m", "n", "ans"], verify=["n == fp - m*p", "w == 0 or ans == m + n", "w == 1 or ans == n"],
        q="곡선 y = x³ {sgt(a)}x² {sgt(b)}x 위의 점 ({p}, {fp})에서의 접선의 방정식이 y = mx + n일 때, 상수 m, n에 대하여 {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="곡선 y = f(x) 위의 점 (p, f(p))에서의 접선의 기울기는 f'(p)이고 접선은 y − f(p) = f'(p)(x − p)이다. f'(x) = 3x² {sgt(a2)}x {sgn(b)}이므로 f'({p}) = {m}이다.",
        sol2=[("f'(x) = 3x² {sgt(a2)}x {sgn(b)}, 기울기 m = f'({p}) = {m}", "기울기"), ("y − {pn(fp)} = {m}(x − {pn(p)}) → y = {co(m)}x {sgn(n)}", "접선"), ("m = {m}, n = {n} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["접선 y = {co(m)}x {sgn(n)}에 x = {p}를 넣으면 {fp}{ika(fp)} 나와 접점을 지난다. 따라서 {ASK} = {ans}이다.", "x = {p} → y = {fp} ✓", "{ASK} = {ans}"],
        model="기울기 f'({p}) = {m}이고 접점 ({p}, {fp})를 지나므로 접선은 y = {co(m)}x {sgn(n)}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("기울기·접선", 3, "m = f'({p}) = {m}, 접선 y = {co(m)}x {sgn(n)}{eul(n)} 세웠다.", "접점을 지나지 않는 직선을 세웠으면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("기울기를 f(p)로 둠", "기울기·접선", "불인정"), ("접선이 원점을 지난다고 둠", "기울기·접선", "불인정"), ("n 계산 실수", "답", "부분")])


def df_t4():
    return T(DF, 4, DF_B, title="평균값 정리·롤의 정리 — 상수 c",
        skill="f'(c) = (f(b) − f(a))/(b − a)를 만족하는 c를 구하기(이차함수는 구간의 중점)", axis={"f": "x² + ax + b", "구간": "[p, q]", "형태": "평균값 정리 / 롤의 정리"}, disc="평균변화율을 구해 f'(c)와 같다고 놓고 c를 구하는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-6, 6)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "p", "values": {"int": [-5, 3]}}, {"name": "dq", "values": {"in": [2, 4, 6]}}, {"name": "k", "values": {"in": ["mvt", "rolle"]}}],
        table={"key": "k", "rows": {"mvt": {"KIND": "평균값 정리", "COND": "f'(c) = (f(q) − f(p))/(q − p)", "w": 1}, "rolle": {"KIND": "롤의 정리", "COND": "f(p) = f(q)이면 f'(c) = 0", "w": 0}}},
        derive={"qq": "p + dq", "fp": "p*p + a*p + b", "fq": "(p + dq)**2 + a*(p + dq) + b", "avg": "((p + dq)**2 + a*(p + dq) - p*p - a*p)/dq", "ans": "(2*p + dq)/2"},
        constraints=["w == 1 or fp == fq", "w == 0 or fp != fq", "ans != 0", "ans not in (a, b, p, qq, fp, fq)"], cost=["a", "b", "p", "qq", "avg", "ans"], verify=["2*ans + a == avg"],
        q="함수 f(x) = x² {sgt(a)}x {sgn(b)}에 대하여 닫힌구간 [{p}, {qq}]에서 {KIND}를 만족시키는 상수 c의 값을 구하시오.", answer="{ans}",
        sol1="{KIND}: {COND}. f(x)는 다항함수이므로 [{p}, {qq}]에서 연속이고 ({p}, {qq})에서 미분가능하다. 평균변화율은 (f({qq}) − f({p}))/({qq} − {pn(p)}) = ({fq} − {pn(fp)})/{dq} = {avg}이고 f'(x) = 2x {sgn(a)}이다.",
        sol2=[("f({p}) = {fp}, f({qq}) = {fq}, 평균변화율 = {avg}", "평균변화율"), ("f'(c) = 2c {sgn(a)} = {avg}", "{KIND}"), ("c = {ans}", None, ("{ans}", "c"))],
        sol3=["c = {ans}{ika(ans)} 열린구간 ({p}, {qq}) 안에 있고, 이차함수에서는 c가 항상 구간의 중점 ({p} + {pn(qq)})/2임을 확인할 수 있다. 따라서 c = {ans}이다.", "c = ({p} + {pn(qq)})/2", "c = {ans}"],
        model="평균변화율은 ({fq} − {pn(fp)})/{dq} = {avg}이고 f'(c) = 2c {sgn(a)} = {avg}에서 c = {ans}이다.",
        rubric=[("평균변화율", 3, "f'(c) = {avg}{eul(avg)} 세웠다.", "함숫값 계산 실수면 1점."), ("c", 2, "c = {ans}{eul(ans)} 구했다.", "구간 밖의 값을 답했으면 인정하지 않는다.")],
        pitfalls=[("평균변화율을 f(q) − f(p)로만 둠(구간 길이로 나누지 않음)", "평균변화율", "불인정"), ("f'(c)를 f(c)로 둠", "c", "불인정"), ("계산 실수", "c", "부분")])


def _rows_cubic():
    """f'(x) = 3(x − r1)(x − r2) 가 되는 f(x) = x³ + px² + qx (+ c): p = −3(r1 + r2)/2 (r1 + r2 짝수), q = 3 r1 r2"""
    out = []
    for r1 in range(-4, 4):
        for r2 in range(r1 + 1, 5):
            if (r1 + r2) % 2:
                continue
            p = -3 * (r1 + r2) // 2
            q = 3 * r1 * r2
            out.append((r1, r2, p, q))
    return out


CUBICS = _rows_cubic()


def df_t5():
    rows = {}
    for r1, r2, p, q in CUBICS:
        for c in (-4, -2, -1, 0, 1, 2, 3, 5):
            for kk, ask, v in (("sum", "α + β", r1 + r2), ("len", "β − α", r2 - r1)):
                desc = _pt([1, p, q, c])
                qtext = f"함수 f(x) = {desc}가 감소하는 구간이 [α, β]일 때, {ask}의 값을 구하시오."
                if v == 0 or Fraction(v) in _nums(qtext):
                    continue
                rows[f"{r1}_{r2}_{c}_{kk}"] = {"FX": desc, "ASK": ask, "V": v, "R1": r1, "R2": r2, "DF": f"f'(x) = 3x² {'+' if 2 * p > 0 else '−'} {abs(2 * p)}x {'+' if q > 0 else '−'} {abs(q)} = 3(x {'−' if r1 > 0 else '+'} {abs(r1)})(x {'−' if r2 > 0 else '+'} {abs(r2)})".replace("− 0x ", "").replace("+ 0x ", "").replace(" 1x ", " x ").replace("(x − 0)", "x").replace("(x + 0)", "x")}
    ROWS = rows

    return T(DF, 5, DF_B, title="함수의 증가와 감소 — 감소하는 구간의 양 끝",
        skill="f'(x) = 0의 두 근 사이(f' < 0)가 감소 구간임을 써서 α, β 구하기", axis={"근": "−4~4", "묻는 것": "α + β / β − α"}, disc="f'(x)를 인수분해해 부호가 음인 구간을 정확히 읽는가", diff=2,
        params=[{"name": "f", "values": {"in": list(ROWS)}}], table={"key": "f", "rows": ROWS},
        derive={"ans": "V"}, cost=["R1", "R2", "ans"], verify=["ans == V"],
        q="함수 f(x) = {FX}가 감소하는 구간이 [α, β]일 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="함수는 f'(x) < 0인 구간에서 감소한다. {DF}이므로 f'(x) < 0인 범위는 두 근 사이 {R1} < x < {R2}이고, 감소하는 구간은 [{R1}, {R2}]이다.",
        sol2=[("{DF}", "도함수 인수분해"), ("f'(x) < 0 ⇔ {R1} < x < {R2} → 감소 구간 [{R1}, {R2}]", "부호"), ("α = {R1}, β = {R2} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["두 근 사이의 값(예: 중점)을 f'(x)에 넣어 음수인지 확인한다. 따라서 {ASK} = {ans}이다.", "f'(중점) < 0 ✓", "{ASK} = {ans}"],
        model="{DF}이고 f'(x) < 0인 구간은 {R1} < x < {R2}이므로 α = {R1}, β = {R2}, {ASK} = {ans}이다.",
        rubric=[("도함수·부호", 3, "{DF}에서 감소 구간 [{R1}, {R2}]{eul(R2)} 구했다.", "증가 구간과 바꿨으면 인정하지 않는다."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("f' > 0인 구간을 감소로 봄", "도함수·부호", "불인정"), ("도함수 인수분해 실수", "도함수·부호", "부분"), ("α, β를 바꿔 뺌", "답", "부분")])


def df_t6():
    rows = {}
    for r1, r2, p, q in CUBICS:
        for c in range(-6, 7):
            f = [1, p, q, c]
            M, m = _ev(f, r1), _ev(f, r2)
            desc = _pt(f)
            for kk, ask, v in (("max", "극댓값", M), ("min", "극솟값", m), ("diff", "극댓값과 극솟값의 차", M - m), ("sum", "극댓값과 극솟값의 합", M + m)):
                qtext = f"함수 f(x) = {desc}의 {ask}을 구하시오."
                if v == 0 or Fraction(v) in _nums(qtext):
                    continue
                rows[f"{r1}_{r2}_{c}_{kk}"] = {"FX": desc, "ASK": ask, "V": int(v), "R1": r1, "R2": r2, "M": int(M), "MN": int(m), "DF": f"f'(x) = {_pt(_der(f))} = 3(x {'−' if r1 > 0 else '+'} {abs(r1)})(x {'−' if r2 > 0 else '+'} {abs(r2)})".replace("(x − 0)", "x").replace("(x + 0)", "x")}
    ROWS = _pick(rows, 330)

    return T(DF, 6, DF_B, title="극대와 극소 — 삼차함수의 극값",
        skill="f'(x) = 0의 근에서 f'의 부호 변화로 극대(+ → −)·극소(− → +)를 판단하고 극값 계산하기", axis={"f": "x³ + px² + qx + c (근 −4~4)", "묻는 것": "극댓값 / 극솟값 / 차 / 합"}, disc="최고차항 양수인 삼차함수에서 작은 근이 극대, 큰 근이 극소임을 부호 변화로 확인하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(ROWS)}}], table={"key": "f", "rows": ROWS},
        derive={"ans": "V"}, cost=["R1", "R2", "M", "MN", "ans"], verify=["ans == V"],
        q="함수 f(x) = {FX}의 {ASK}을 구하시오.", answer="{ans}",
        sol1="{DF}이므로 f'(x) = 0의 근은 x = {R1}, {R2}이다. x = {R1}의 좌우에서 f'의 부호가 + → −이므로 극대, x = {R2}에서 − → +이므로 극소이다. 극댓값 f({R1}) = {M}, 극솟값 f({R2}) = {MN}.",
        sol2=[("{DF} → f'(x) = 0: x = {R1}, {R2}", "도함수"), ("x = {R1}: 극대 f({R1}) = {M}, x = {R2}: 극소 f({R2}) = {MN}", "증감표"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["극댓값이 극솟값보다 큰지({M} > {MN}) 확인하면 극대·극소를 바꾸지 않았음을 알 수 있다. 따라서 {ASK} = {ans}이다.", "극대 {M}, 극소 {MN}", "{ASK} = {ans}"],
        model="{DF}이고 x = {R1}에서 극대, x = {R2}에서 극소이므로 극댓값 {M}, 극솟값 {MN}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("극점 판단", 3, "f'(x) = 0의 근 {R1}, {R2}에서 극대·극소를 판단해 극댓값 {M}, 극솟값 {MN}{eul(MN)} 구했다.", "극대·극소를 바꿨으면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("f'(x) = 0의 근을 극값으로 답함(x좌표와 함숫값 혼동)", "극점 판단", "불인정"), ("극대·극소를 바꿈", "극점 판단", "부분"), ("함숫값 계산 실수", "답", "부분")])


DF_SEED = SEED(DF, category="해석", title="미분 — 미분계수 정의·도함수 값·접선·평균값 정리·증감 구간·극대극소", unit_id="h2-2", concept_ids=["h2-2-05", "h2-2-06", "h2-2-07", "h2-2-08", "h2-2-09"],
               schema_name="미분계수와 도함수의 활용", note="삼차함수는 f'(x) = 3(x − r1)(x − r2)가 되도록 (r1 + r2 짝수) 계수를 잡아 극점이 정수가 되게 했다.",
               templates=[df_t1(), df_t2_cubic(), df_t3(), df_t4(), df_t5(), df_t6(), df_t7()])


if __name__ == "__main__":
    run(LM_SEED, DF_SEED)
