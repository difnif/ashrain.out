# itemfactory/tools/mkseed_h2_calc2.py — 고2 수학II 미분의 활용·적분 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h2_calc2.py
#     → seeds/h2-2-diffapp.json  (미분의 활용: 구간 최대최소·방정식의 실근 개수(k)·극값 조건·극점 조건→계수·속도와 가속도·상자 부피 최대, 6틀)
#     → seeds/h2-2-integ.json    (적분: 부정적분과 함숫값·정적분 계산·정적분의 성질(우함수/기함수·선형)·정적분으로 정의된 함수·넓이(곡선과 x축)·넓이(두 곡선), 6틀)
#   삼차함수는 mkseed_h2_calc1 의 CUBICS(정수 극점) 를 함께 쓴다.
from __future__ import annotations

import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
from mkseed_h2_calc1 import CUBICS, _der, _ev, _fm, _fmp, _nums, _pick, _pm, _pt  # noqa: E402
from genkit.expr import eul as _eul, eun as _eun, ika as _ika, ro as _ro, wa as _wa  # noqa: E402

rng = random.Random(20260919)


# ═══════════════════════════════════════════════════════════════════ 1. 미분의 활용
AP = "h2-2-diffapp"
AP_B = {**HS, "prereq": ["도함수", "극대와 극소"], "ops": ["미분의 활용"], "traps": ["끝점 값 비교 누락", "속도의 부호"], "tags": ["최대최소", "방정식의 실근", "속도와 가속도"]}


def _ap1_rows():
    out = {}
    for r1, r2, p, q in CUBICS:
        for c in (-5, -2, 0, 1, 3, 6):
            f = [1, p, q, c]
            for lo in range(r1 - 2, r1 + 1):
                for hi in range(r2, r2 + 3):
                    if hi - lo > 7 or lo >= hi:
                        continue
                    pts = [lo, hi] + [r for r in (r1, r2) if lo < r < hi]
                    vals = {t: _ev(f, t) for t in pts}
                    M, mn = max(vals.values()), min(vals.values())
                    desc = _pt(f)
                    for kk, ask, v in (("max", "최댓값", M), ("min", "최솟값", mn), ("sum", "최댓값과 최솟값의 합", M + mn)):
                        qtext = f"닫힌구간 [{lo}, {hi}]에서 함수 f(x) = {desc}의 {ask}을 구하시오."
                        if v == 0 or Fraction(v) in _nums(qtext):
                            continue
                        out[f"{r1}_{r2}_{c}_{lo}_{hi}_{kk}"] = {"FX": desc, "LO": lo, "HI": hi, "ASK": ask, "V": int(v), "R1": r1, "R2": r2, "M": int(M), "MN": int(mn),
                                                                  "DF": f"f'(x) = {_pt(_der(f))} = 3(x {'−' if r1 > 0 else '+'} {abs(r1)})(x {'−' if r2 > 0 else '+'} {abs(r2)})".replace("(x − 0)", "x").replace("(x + 0)", "x"),
                                                                  "VALS": ", ".join(f"f({t}) = {vals[t]}" for t in sorted(vals)), "CRIT": ", ".join(str(r) for r in (r1, r2) if lo < r < hi) or "없음"}
    return _pick(out, 330)


AP1_ROWS = _ap1_rows()


def ap_t1():
    return T(AP, 1, AP_B, title="닫힌구간에서 삼차함수의 최댓값·최솟값",
        skill="구간 안의 극점과 양 끝점에서의 함숫값을 모두 비교해 최대·최소 정하기", axis={"f": "x³ + px² + qx + c (정수 극점)", "구간": "극점 주변 길이 ≤ 7", "묻는 것": "최댓값 / 최솟값 / 합"}, disc="극값만 보지 않고 구간의 끝점 값도 함께 비교하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(AP1_ROWS)}}], table={"key": "f", "rows": AP1_ROWS},
        derive={"ans": "V"}, cost=["LO", "HI", "M", "MN", "ans"], verify=["ans == V"],
        q="닫힌구간 [{LO}, {HI}]에서 함수 f(x) = {FX}의 {ASK}을 구하시오.", answer="{ans}",
        sol1="닫힌구간에서 연속함수의 최댓값·최솟값은 구간 안의 극점 또는 구간의 양 끝에서 생긴다. {DF}이므로 극점 후보는 x = {R1}, {R2}이고 구간 안에 있는 것은 {CRIT}이다. 끝점 {LO}, {HI}와 함께 함숫값을 비교한다.",
        sol2=[("{DF} → 구간 안의 극점: {CRIT}", "극점"), ("{VALS}", "후보의 함숫값"), ("최댓값 {M}, 최솟값 {MN} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["극점이 구간 밖에 있으면 후보에서 빼고, 끝점 값을 반드시 넣었는지 확인한다. 따라서 {ASK} = {ans}이다.", "{VALS}", "{ASK} = {ans}"],
        model="{DF}에서 구간 안의 극점은 {CRIT}이고 {VALS}이므로 최댓값 {M}, 최솟값 {MN}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("후보 비교", 3, "극점과 끝점의 함숫값 {VALS}{eul(VALS)} 비교했다.", "끝점을 빠뜨렸으면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("끝점 값을 비교하지 않고 극값을 최대·최소로 답함", "후보 비교", "불인정"), ("구간 밖의 극점을 후보에 넣음", "후보 비교", "부분"), ("함숫값 계산 실수", "답", "부분")])


def _ap2_rows():
    out = {}
    for r1, r2, p, q in CUBICS:
        for c in (-4, -1, 0, 2, 5):
            f = [1, p, q, c]
            M, mn = _ev(f, r1), _ev(f, r2)
            desc = _pt(f)
            v = int(M - mn - 1)
            qtext = f"방정식 {desc} = k가 서로 다른 세 실근을 갖도록 하는 정수 k의 개수를 구하시오."
            if v >= 1 and Fraction(v) not in _nums(qtext):
                out[f"{r1}_{r2}_{c}_3"] = {"FX": desc, "ASK": "서로 다른 세 실근을 갖도록 하는 정수 k의 개수", "V": v, "M": int(M), "MN": int(mn), "R1": r1, "R2": r2, "COND": f"{int(mn)} < k < {int(M)}", "WHY": "y = k가 극댓값과 극솟값 사이를 지나야 세 점에서 만난다", "DF": f"f'(x) = 3(x {'−' if r1 > 0 else '+'} {abs(r1)})(x {'−' if r2 > 0 else '+'} {abs(r2)})".replace("(x − 0)", "x").replace("(x + 0)", "x")}
            for kk, ask, v2, cond, why in (("one_min", "오직 하나의 실근을 갖도록 하는 정수 k의 최솟값", int(M) + 1, f"k > {int(M)} 또는 k < {int(mn)}", "y = k가 극댓값보다 위이거나 극솟값보다 아래이면 한 점에서만 만난다"),
                                           ("two", "서로 다른 두 실근을 갖는 모든 k의 값의 합", int(M + mn), f"k = {int(M)} 또는 k = {int(mn)}", "y = k가 극댓값 또는 극솟값과 같으면 접해서 두 실근(중근 포함)")):
                qtext = f"방정식 {desc} = k가 {ask}를 구하시오."
                if v2 == 0 or Fraction(v2) in _nums(qtext):
                    continue
                out[f"{r1}_{r2}_{c}_{kk}"] = {"FX": desc, "ASK": ask, "V": v2, "M": int(M), "MN": int(mn), "R1": r1, "R2": r2, "COND": cond, "WHY": why, "DF": f"f'(x) = 3(x {'−' if r1 > 0 else '+'} {abs(r1)})(x {'−' if r2 > 0 else '+'} {abs(r2)})".replace("(x − 0)", "x").replace("(x + 0)", "x")}
    return _pick(out, 330)


AP2_ROWS = _ap2_rows()


def ap_t2():
    return T(AP, 2, AP_B, title="방정식의 실근의 개수 — y = f(x)와 y = k의 교점",
        skill="삼차함수의 극댓값·극솟값과 직선 y = k의 위치 관계로 실근의 개수를 판단하기", axis={"f": "x³ + px² + qx + c (정수 극점)", "묻는 것": "세 실근 k의 개수 / 한 실근 k의 최솟값 / 두 실근 k의 합"}, disc="실근의 개수를 그래프의 교점 개수로 바꾸고 극값을 경계로 쓰는가", diff=3,
        params=[{"name": "f", "values": {"in": list(AP2_ROWS)}}], table={"key": "f", "rows": AP2_ROWS},
        derive={"ans": "V"}, cost=["M", "MN", "ans"], verify=["ans == V"],
        q="방정식 {FX} = k가 {ASK}{eul(ASK)} 구하시오.", answer="{ans}",
        sol1="방정식 f(x) = k의 실근은 곡선 y = f(x)와 직선 y = k의 교점의 x좌표이다. {DF}이므로 극댓값 f({R1}) = {M}, 극솟값 f({R2}) = {MN}이다. {WHY}.",
        sol2=[("극댓값 {M}, 극솟값 {MN}", "극값"), ("{WHY}: {COND}", "직선 y = k의 위치"), ("답: {ans}", None, ("{ans}", "답"))],
        sol3=["k가 극값과 같을 때는 접하므로 실근이 2개(중근 포함)임을 경계에서 확인한다. 따라서 답은 {ans}이다.", "{COND}", "답 {ans}"],
        model="극댓값 {M}, 극솟값 {MN}이고 {WHY}이므로 {COND}. 따라서 답은 {ans}이다.",
        rubric=[("극값·위치 관계", 3, "극댓값 {M}, 극솟값 {MN}{eul(MN)} 구해 {COND}{eul(COND)} 세웠다.", "경계(등호) 처리를 틀리면 1점."), ("답", 2, "{ans}{eul(ans)} 구했다.", "정수 세기 실수면 1점.")],
        pitfalls=[("극값을 실근의 개수로 착각", "극값·위치 관계", "불인정"), ("경계 k = 극값을 세 실근에 포함", "극값·위치 관계", "부분"), ("정수 개수 세기 실수", "답", "부분")])


def ap_t3():
    return T(AP, 3, AP_B, title="극값을 가질 조건 — f'(x) = 0의 판별식",
        skill="삼차함수가 극값을 가지려면 f'(x) = 0이 서로 다른 두 실근을 가져야 함(D > 0)을 쓰기", axis={"f": "x³ + ax² + bx (b: 1~12)", "묻는 것": "극값을 갖지 않는 정수 a의 개수 / 극값을 갖는 자연수 a의 최솟값"}, disc="극값의 존재를 도함수의 판별식 부호로 옮기는가", diff=3,
        params=[{"name": "b", "values": {"int": [1, 30]}}, {"name": "k", "values": {"in": ["none", "min"]}}],
        table={"key": "k", "rows": {"none": {"ASK": "극값을 갖지 않도록 하는 정수 a의 개수", "COND": "D/4 = a² − 3b ≤ 0", "w": 1}, "min": {"ASK": "극값을 갖도록 하는 자연수 a의 최솟값", "COND": "D/4 = a² − 3b > 0", "w": 0}}},
        derive={"b3": "3*b", "r": "floor(sqrt(3*b))", "ans": "w*(2*floor(sqrt(3*b)) + 1) + (1 - w)*(floor(sqrt(3*b)) + 1)", "exact": "floor(sqrt(3*b))*floor(sqrt(3*b)) == 3*b"},
        constraints=["ans not in (b, b3)", "not exact"], cost=["b", "b3", "r", "ans"], verify=["r*r < b3", "(r + 1)*(r + 1) > b3"],
        q="함수 f(x) = x³ + ax² + {b}x가 {ASK}{eul(ASK)} 구하시오.", answer="{ans}",
        sol1="f'(x) = 3x² + 2ax + {b}이고, 삼차함수가 극값을 가지려면 f'(x) = 0이 서로 다른 두 실근을 가져야 한다(판별식 D > 0). 극값을 갖지 않으려면 D ≤ 0이다. D/4 = a² − 3 × {b} = a² − {b3}.",
        sol2=[("f'(x) = 3x² + 2ax + {b}, D/4 = a² − {b3}", "도함수의 판별식"), ("{COND} → a² {OPS} {b3}", "조건"), ("답: {ans}", None, ("{ans}", "답"))],
        sol3=["a² = {b3}이 되는 정수 a는 없으므로({r}² = {r*r} < {b3} < {(r + 1)*(r + 1)} = {r + 1}²) 경계에서 세는 실수가 없는지 확인한다. 따라서 답은 {ans}이다.", "{r}² < {b3} < {r + 1}²", "답 {ans}"],
        model="D/4 = a² − {b3}에서 {COND}이므로 a² {OPS} {b3}이고, {r}² < {b3} < {r + 1}²이므로 답은 {ans}이다.",
        rubric=[("판별식 조건", 3, "판별식 조건 {COND} 꼴의 부등식을 세웠다.", "부등호 방향이 반대면 인정하지 않는다."), ("정수 세기", 2, "{ans}{eul(ans)} 구했다.", "경계 처리 실수면 1점.")],
        pitfalls=[("극값 조건을 D ≥ 0으로 둠(중근 포함)", "판별식 조건", "부분"), ("D 대신 D/4 계산에서 2a를 a로 둠", "판별식 조건", "불인정"), ("정수 개수 세기 실수", "정수 세기", "부분")])


def _ap3_fix(t):
    t["table"]["rows"]["none"]["OPS"] = "≤"
    t["table"]["rows"]["min"]["OPS"] = ">"
    return t


def _cubics_wide():
    out = []
    for r1 in range(-6, 6):
        for r2 in range(r1 + 1, 7):
            if (r1 + r2) % 2 or r1 == 0 or r2 == 0:
                continue
            out.append((r1, r2, -3 * (r1 + r2) // 2, 3 * r1 * r2))
    return out


CUBICS_W = _cubics_wide()


def ap_t4():
    return T(AP, 4, AP_B, title="극점의 위치로 계수 정하기 — x = r₁에서 극대, x = r₂에서 극소",
        skill="f'(x) = 3(x − r₁)(x − r₂)이 되도록 계수를 정해 a, b 구하기", axis={"극점": "−4~4 (r₁ < r₂)", "묻는 것": "a + b / ab / a − b"}, disc="극점이 f'(x) = 0의 근임을 써서 f'(x)를 인수분해 꼴로 놓고 계수를 비교하는가", diff=3,
        params=[{"name": "i", "values": {"in": [str(n) for n in range(len(CUBICS_W))]}}, {"name": "k", "values": {"in": ["sum", "prod", "diff"]}}],
        table=[{"key": "i", "rows": {str(n): {"R1": r1, "R2": r2, "A": p, "B": q, "DF": f"3(x {'−' if r1 > 0 else '+'} {abs(r1)})(x {'−' if r2 > 0 else '+'} {abs(r2)})"} for n, (r1, r2, p, q) in enumerate(CUBICS_W)}},
               {"key": "k", "rows": {"sum": {"ASK": "a + b", "wa": 1, "wb": 0, "wc": 0}, "prod": {"ASK": "ab", "wa": 0, "wb": 1, "wc": 0}, "diff": {"ASK": "a − b", "wa": 0, "wb": 0, "wc": 1}}}],
        derive={"ans": "wa*(A + B) + wb*A*B + wc*(A - B)", "A2": "2*A"},
        constraints=["A != 0", "B != 0", "ans != 0", "ans not in (R1, R2, A, B)"], cost=["R1", "R2", "A", "B", "ans"], verify=["3*R1*R2 == B", "-3*(R1 + R2) == 2*A"],
        q="함수 f(x) = x³ + ax² + bx가 x = {R1}에서 극댓값, x = {R2}에서 극솟값을 가질 때, 상수 a, b에 대하여 {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="x = {R1}, {R2}에서 극값을 가지므로 f'(x) = 3x² + 2ax + b는 x = {R1}, {R2}를 근으로 갖는다. 최고차항의 계수가 3이므로 f'(x) = {DF}로 놓고 전개해 계수를 비교한다.",
        sol2=[("f'(x) = 3x² + 2ax + b = {DF}", "극점 = f'의 근"), ("전개: 3x² {sgt(A2)}x {sgn(B)} → 2a = {A2}, b = {B}", "계수 비교"), ("a = {A}, b = {B} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["f'(x)의 부호가 x = {R1}에서 + → −(극대), x = {R2}에서 − → +(극소)임을 인수분해 꼴에서 확인한다. 따라서 {ASK} = {ans}이다.", "a = {A}, b = {B}", "{ASK} = {ans}"],
        model="f'(x) = {DF} = 3x² {sgt(A2)}x {sgn(B)}이므로 a = {A}, b = {B}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("계수 비교", 3, "f'(x) = {DF}에서 a = {A}, b = {B}{eul(B)} 구했다.", "최고차항 계수 3을 빠뜨렸으면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("f'(x) = (x − r₁)(x − r₂)로 두고 3을 빠뜨림", "계수 비교", "불인정"), ("2a와 a를 혼동", "계수 비교", "부분"), ("극대·극소의 순서를 바꿔 근을 배치", "계수 비교", "부분")])


def _ap5_rows():
    out = {}
    for r1 in range(0, 5):
        for r2 in range(r1 + 1, 7):
            if (r1 + r2) % 2:
                continue
            p = -3 * (r1 + r2) // 2
            q = 3 * r1 * r2
            for c in (0, 2, 5):
                xf = [1, p, q, c]
                vf = _der(xf)
                af = _der(vf)
                desc = _pt(xf, "t")
                asks = []
                for t0 in range(0, 6):
                    v0, a0 = _ev(vf, t0), _ev(af, t0)
                    asks.append((f"v{t0}", f"t = {t0}에서의 속도", int(v0), f"v(t) = {_pt(vf, 't')}에 t = {t0} 대입"))
                    asks.append((f"a{t0}", f"t = {t0}에서의 가속도", int(a0), f"a(t) = {_pt(af, 't')}에 t = {t0} 대입"))
                if r1 > 0:
                    asks.append(("turn", "처음으로 운동 방향을 바꾸는 시각", r1, f"v(t) = {_pt(vf, 't')} = 3(t − {r1})(t − {r2})의 부호가 처음 바뀌는 t = {r1}"))
                asks.append(("stop", "속도가 0이 되는 모든 시각의 합", r1 + r2, f"v(t) = 3(t − {r1})(t − {r2}) = 0에서 t = {r1}, {r2}"))
                for kk, ask, v, expl in asks:
                    qtext = f"수직선 위를 움직이는 점 P의 시각 t에서의 위치 x가 x = {desc}일 때, {ask}를 구하시오."
                    if v == 0 or Fraction(v) in _nums(qtext):
                        continue
                    out[f"{r1}_{r2}_{c}_{kk}"] = {"XT": desc, "ASK": ask, "V": v, "VT": _pt(vf, "t"), "AT": _pt(af, "t"), "EXPL": expl}
    return _pick(out, 330)


AP5_ROWS = _ap5_rows()


def ap_t5():
    return T(AP, 5, AP_B, title="속도와 가속도 — 위치 x(t)의 미분",
        skill="속도 v = dx/dt, 가속도 a = dv/dt임을 써서 시각의 값·방향 전환 시각 구하기", axis={"x(t)": "t³ + pt² + qt + c", "묻는 것": "속도 / 가속도 / 방향 전환 시각 / 속도 0인 시각의 합"}, disc="위치를 미분한 것이 속도, 속도를 미분한 것이 가속도임을 알고 부호 변화로 방향 전환을 읽는가", diff=2,
        params=[{"name": "f", "values": {"in": list(AP5_ROWS)}}], table={"key": "f", "rows": AP5_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="수직선 위를 움직이는 점 P의 시각 t에서의 위치 x가 x = {XT}일 때, {ASK}{eul(ASK)} 구하시오.", answer="{ans}",
        sol1="위치 x(t)를 t로 미분하면 속도 v(t) = {VT}, 다시 미분하면 가속도 a(t) = {AT}이다. 운동 방향이 바뀌는 순간은 속도의 부호가 바뀌는 순간(v = 0을 지나며 부호 변화)이다.",
        sol2=[("v(t) = {VT}, a(t) = {AT}", "미분"), ("{EXPL}", "{ASK}"), ("답: {ans}", None, ("{ans}", "답"))],
        sol3=["속도가 0이라고 반드시 방향이 바뀌는 것은 아니므로(부호 변화 확인) 인수분해 꼴에서 부호를 살핀다. 따라서 답은 {ans}이다.", "{EXPL}", "답 {ans}"],
        model="v(t) = {VT}, a(t) = {AT}이고 {EXPL}이므로 답은 {ans}이다.",
        rubric=[("미분", 3, "v(t) = {VT}, a(t) = {AT}{eul(AT)} 구했다.", "가속도를 위치의 미분으로 두었으면 1점."), ("답", 2, "{ans}{eul(ans)} 구했다.", "대입·부호 실수면 1점.")],
        pitfalls=[("가속도를 x(t)를 한 번만 미분한 것으로 둠", "미분", "불인정"), ("속도 0인 시각을 모두 방향 전환 시각으로 봄", "답", "부분"), ("대입 계산 실수", "답", "부분")])


def _ap6_rows():
    out = {}
    for L in (6, 9, 12, 15, 18, 21, 24, 30, 36):
        k = L // 3
        v = 2 * k ** 3
        x0 = L // 6 if L % 6 == 0 else None
        qtext = f"한 변의 길이가 {L}인 정사각형 모양의 종이의 네 귀퉁이에서 한 변의 길이가 x인 정사각형을 잘라내고 남은 부분을 접어 뚜껑이 없는 상자를 만들 때, 상자의 부피의 최댓값을 구하시오."
        if Fraction(v) in _nums(qtext):
            continue
        out[f"box{L}"] = {"DESC": qtext, "V": v, "SET": f"V(x) = x({L} − 2x)² (0 < x < {L // 2 if L % 2 == 0 else Fraction(L, 2)})", "DV": f"V'(x) = ({L} − 2x)² − 4x({L} − 2x) = ({L} − 2x)({L} − 6x)", "CRIT": f"V'(x) = 0에서 x = {_fm(Fraction(L, 6))} (x = {_fm(Fraction(L, 2))}{_eun(Fraction(L, 2))} 범위 밖), x = {_fm(Fraction(L, 6))}에서 극대이자 최대", "RES": f"V({_fm(Fraction(L, 6))}) = {_fm(Fraction(L, 6))} × ({_fm(Fraction(2 * L, 3))})² = {v}"}
    for a in range(2, 13):
        # 직사각형: 둘레 2a... 대신 y = 12 − x² 아래 내접 직사각형은 무리수 → 생략. 대신 x + y = 3a (양수) 에서 x²y 의 최댓값 = (2a)²·a = 4a³
        v = 4 * a ** 3
        s = 3 * a
        qtext = f"두 양수 x, y에 대하여 x + y = {s}일 때, x²y의 최댓값을 구하시오."
        if Fraction(v) in _nums(qtext):
            continue
        out[f"xy{a}"] = {"DESC": qtext, "V": v, "SET": f"y = {s} − x이므로 f(x) = x²({s} − x) (0 < x < {s})", "DV": f"f'(x) = {2 * s}x − 3x² = 3x({2 * a} − x)", "CRIT": f"f'(x) = 0에서 x = {2 * a} (x = 0은 범위 밖), x = {2 * a}에서 극대이자 최대", "RES": f"f({2 * a}) = {2 * a}² × {a} = {v}"}
    return out


AP6_ROWS = _ap6_rows()


def ap_t6():
    return T(AP, 6, AP_B, title="최대·최소의 활용 — 부피·곱의 최댓값",
        skill="변수 하나의 함수로 식을 세우고 미분해 극대점이 최댓값임을 확인하기", axis={"상황": "상자의 부피 / x + y 일정할 때 x²y", "크기": "L = 6~36, 합 6~36"}, disc="정의역을 정하고 f'(x) = 0의 근 중 범위 안의 극대점에서 최댓값을 읽는가", diff=3,
        params=[{"name": "f", "values": {"in": list(AP6_ROWS)}}], table={"key": "f", "rows": AP6_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="{DESC}", answer="{ans}",
        sol1="구하려는 양을 변수 x의 함수로 나타내고 x의 범위(정의역)를 정한다. 미분해 f'(x) = 0인 점을 찾고, 범위 안에서 증가에서 감소로 바뀌는 점(극대)이 하나뿐이면 그 점에서 최댓값을 가진다. {SET}.",
        sol2=[("{SET}", "식 세우기"), ("{DV}; {CRIT}", "미분·극대"), ("{RES}", None, ("{ans}", "최댓값"))],
        sol3=["범위의 양 끝에서 값이 0에 가까워지므로 안쪽의 극대점이 최댓값임을 확인한다. 따라서 최댓값은 {ans}이다.", "{CRIT}", "최댓값 {ans}"],
        model="{SET}. {DV}, {CRIT}. {RES}이므로 최댓값은 {ans}이다.",
        rubric=[("식·미분", 3, "{SET}, {DV} 꼴로 세웠다.", "정의역을 정하지 않았으면 1점."), ("최댓값", 2, "{ans}{eul(ans)} 구했다.", "극대점 판단 없이 답만 썼으면 1점.")],
        pitfalls=[("정의역 밖의 근을 채택", "식·미분", "불인정"), ("극대점의 x값을 최댓값으로 답함", "최댓값", "불인정"), ("전개·미분 실수", "식·미분", "부분")])


AP_SEED = SEED(AP, category="해석", title="미분의 활용 — 구간 최대최소·실근의 개수·극값 조건·극점→계수·속도와 가속도·최대최소 활용", unit_id="h2-2", concept_ids=["h2-2-09", "h2-2-10", "h2-2-11", "h2-2-12"],
               schema_name="도함수의 활용", note="삼차함수는 CUBICS(정수 극점) 표. 상자 부피는 L이 3의 배수일 때 2(L/3)³.",
               templates=[ap_t1(), ap_t2(), _ap3_fix(ap_t3()), ap_t4(), ap_t5(), ap_t6()])


# ═══════════════════════════════════════════════════════════════════ 2. 적분
IN = "h2-2-integ"
IN_B = {**HS, "prereq": ["도함수", "다항식의 계산"], "ops": ["적분"], "traps": ["적분상수", "위끝·아래끝 대입 순서"], "tags": ["부정적분", "정적분", "넓이"]}


def in_t1():
    return T(IN, 1, IN_B, title="부정적분 — 도함수와 한 점의 값으로 함숫값 구하기",
        skill="f'(x)를 적분해 적분상수 C를 f(p) = v로 정한 뒤 f(q) 구하기", axis={"f'": "3ax² + 2bx + c", "p, q": "−3~4"}, disc="적분상수를 조건으로 정하고 원함수의 값을 계산하는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-2, 3)}}, {"name": "b", "values": {"in": NZ(-4, 4)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "p", "values": {"int": [-3, 4]}}, {"name": "v", "values": {"int": [-6, 8]}}, {"name": "qq", "values": {"int": [-3, 4]}}],
        derive={"a3": "3*a", "b2": "2*b", "Fp": "a*p**3 + b*p*p + c*p", "C": "v - (a*p**3 + b*p*p + c*p)", "ans": "a*qq**3 + b*qq*qq + c*qq + v - (a*p**3 + b*p*p + c*p)"},
        constraints=["p != qq", "C != 0", "ans != 0", "ans not in (a3, b2, c, p, v, qq, C)"], cost=["a", "b", "c", "p", "v", "qq", "C", "ans"], verify=["ans == a*qq**3 + b*qq**2 + c*qq + C"],
        q="함수 f(x)의 도함수가 f'(x) = {co(a3)}x² {sgt(b2)}x {sgn(c)}이고 f({p}) = {v}일 때, f({qq})의 값을 구하시오.", answer="{ans}",
        sol1="f(x) = [[integ({co(a3)}pow(x,2) {sgt(b2)}x {sgn(c)}, x)]] = {co(a)}x³ {sgt(b)}x² {sgt(c)}x + C이다(적분상수 C). f({p}) = {v}를 넣어 C를 정한 뒤 x = {qq}를 대입한다.",
        sol2=[("f(x) = {co(a)}x³ {sgt(b)}x² {sgt(c)}x + C", "부정적분"), ("f({p}) = {Fp} + C = {v} → C = {C}", "적분상수"), ("f({qq}) = {ans}", None, ("{ans}", "f({qq})"))],
        sol3=["구한 f(x)를 미분하면 f'(x)가 다시 나오는지 확인한다. 따라서 f({qq}) = {ans}이다.", "f(x) = {co(a)}x³ {sgt(b)}x² {sgt(c)}x {sgn(C)}", "f({qq}) = {ans}"],
        model="f(x) = {co(a)}x³ {sgt(b)}x² {sgt(c)}x + C이고 f({p}) = {v}에서 C = {C}이므로 f({qq}) = {ans}이다.",
        rubric=[("부정적분·C", 3, "f(x) = {co(a)}x³ {sgt(b)}x² {sgt(c)}x {sgn(C)}{eul(C)} 구했다.", "적분상수를 빠뜨렸으면 1점."), ("함숫값", 2, "f({qq}) = {ans}{eul(ans)} 구했다.", "대입 계산 실수면 1점.")],
        pitfalls=[("적분상수 C를 0으로 둠", "부정적분·C", "불인정"), ("적분에서 지수를 나누지 않음", "부정적분·C", "불인정"), ("대입 계산 실수", "함숫값", "부분")])


def in_t2():
    return T(IN, 2, IN_B, title="정적분의 계산 — 다항함수",
        skill="부정적분 F(x)를 구해 F(b) − F(a)로 계산하기", axis={"피적분함수": "3px² + 2qx + r", "구간": "[a, b] (−2~4)"}, disc="위끝 값에서 아래끝 값을 빼는 순서를 지키고 항별로 적분하는가", diff=2,
        params=[{"name": "p", "values": {"in": NZ(-2, 3)}}, {"name": "qv", "values": {"in": NZ(-4, 4)}}, {"name": "r", "values": {"in": NZ(-5, 5)}}, {"name": "lo", "values": {"int": [-2, 3]}}, {"name": "hi", "values": {"int": [-1, 4]}}],
        derive={"p3": "3*p", "q2": "2*qv", "Fhi": "p*hi**3 + qv*hi*hi + r*hi", "Flo": "p*lo**3 + qv*lo*lo + r*lo", "ans": "p*hi**3 + qv*hi*hi + r*hi - (p*lo**3 + qv*lo*lo + r*lo)"},
        constraints=["lo < hi", "ans != 0", "ans not in (p3, q2, r, lo, hi)"], cost=["p", "qv", "r", "lo", "hi", "Fhi", "Flo", "ans"], verify=["ans == Fhi - Flo"],
        q="[[dinteg({lo}, {hi}, {co(p3)}pow(x,2) {sgt(q2)}x {sgn(r)}, x)]]의 값을 구하시오.", answer="{ans}",
        sol1="정적분은 부정적분 F(x)를 구해 F(위끝) − F(아래끝)으로 계산한다. F(x) = {co(p)}x³ {sgt(qv)}x² {sgt(r)}x이므로 F({hi}) − F({lo})를 계산한다.",
        sol2=[("F(x) = {co(p)}x³ {sgt(qv)}x² {sgt(r)}x", "부정적분"), ("F({hi}) = {Fhi}, F({lo}) = {Flo}", "위끝·아래끝"), ("{Fhi} − {pn(Flo)} = {ans}", None, ("{ans}", "정적분"))],
        sol3=["F(x)를 미분하면 피적분함수가 되는지, 빼는 순서(위끝 − 아래끝)가 맞는지 확인한다. 따라서 값은 {ans}이다.", "F({hi}) − F({lo})", "답 {ans}"],
        model="F(x) = {co(p)}x³ {sgt(qv)}x² {sgt(r)}x이므로 정적분은 F({hi}) − F({lo}) = {Fhi} − {pn(Flo)} = {ans}이다.",
        rubric=[("부정적분", 3, "F(x) = {co(p)}x³ {sgt(qv)}x² {sgt(r)}x{eul(r)} 구했다.", "한 항의 적분 실수면 1점."), ("계산", 2, "F({hi}) − F({lo}) = {ans}{eul(ans)} 구했다.", "빼는 순서를 바꿨으면 인정하지 않는다.")],
        pitfalls=[("F(아래끝) − F(위끝)으로 뺌", "계산", "불인정"), ("적분에서 지수만 올리고 나누지 않음", "부정적분", "불인정"), ("음수 대입 부호 실수", "계산", "부분")])


def _in3_rows():
    out = {}
    for a in range(1, 5):
        for p in NZ(-2, 3):
            for s in (-3, -1, 2, 4):
                for r in NZ(-5, 5):
                    for od in (-2, -1, 1, 3):
                        # ∫_{-a}^{a} (od x³ + 3p x² + s x + r) dx = 2(p a³ + r a)
                        v = 2 * (p * a ** 3 + r * a)
                        f = f"{'' if od == 1 else ('-' if od == -1 else od)}pow(x,3) {'+' if 3 * p > 0 else '−'} {abs(3 * p)}pow(x,2) {'+' if s > 0 else '−'} {'' if abs(s) == 1 else abs(s)}x {'+' if r > 0 else '−'} {abs(r)}"
                        q = f"[[dinteg(-{a}, {a}, {f}, x)]]"
                        if v == 0 or Fraction(v) in _nums(q):
                            continue
                        out[f"o{a}_{p}_{s}_{r}_{od}"] = {"EXPR": q, "V": v, "LAW": "기함수(홀수 차수)의 대칭구간 적분은 0, 우함수(짝수 차수)는 [0, a]의 2배", "STEP": f"= 2[[dinteg(0, {a}, {abs(3 * p)}pow(x,2) {'+' if r > 0 else '−'} {abs(r)}, x)]]" if p > 0 else f"= 2[[dinteg(0, {a}, -{abs(3 * p)}pow(x,2) {'+' if r > 0 else '−'} {abs(r)}, x)]]", "RES": f"= 2({p} × {a ** 3} {'+' if r > 0 else '−'} {abs(r)} × {a}) = {v}", "KIND": "대칭구간"}
    for fa in range(-6, 8):
        for ga in range(-5, 7):
            for c1 in (1, 2, 3, -1):
                for c2 in (1, 2, -1, -2, 3):
                    v = c1 * fa + c2 * ga
                    lin = f"{'' if c1 == 1 else ('-' if c1 == -1 else c1)}f(x) {'+' if c2 > 0 else '−'} {'' if abs(c2) == 1 else abs(c2)}g(x)"
                    q = f"[[dinteg(1, 3, f(x), x)]] = {fa}, [[dinteg(1, 3, g(x), x)]] = {ga}일 때, [[dinteg(1, 3, {lin}, x)]]"
                    if v == 0 or Fraction(v) in _nums(q) or fa == 0 or ga == 0:
                        continue
                    out[f"l{fa}_{ga}_{c1}_{c2}"] = {"EXPR": q, "V": v, "LAW": "정적분의 선형성: ∫(kf + lg) = k∫f + l∫g", "STEP": f"= {c1} × [[dinteg(1, 3, f(x), x)]] + ({c2}) × [[dinteg(1, 3, g(x), x)]]", "RES": f"= {c1} × {_fmp(fa)} + ({c2}) × {_fmp(ga)} = {v}", "KIND": "선형성"}
    for a in range(-3, 3):
        for b in range(a + 1, 5):
            for c in range(b + 1, 7):
                for v1 in NZ(-6, 6):
                    for v2 in NZ(-6, 6):
                        v = v1 + v2
                        q = f"[[dinteg({a}, {b}, f(x), x)]] = {v1}, [[dinteg({b}, {c}, f(x), x)]] = {v2}일 때, [[dinteg({a}, {c}, f(x), x)]]"
                        if v == 0 or Fraction(v) in _nums(q):
                            continue
                        out[f"c{a}_{b}_{c}_{v1}_{v2}"] = {"EXPR": q, "V": v, "LAW": "구간 나누기: ∫ₐᶜ = ∫ₐᵇ + ∫ᵇᶜ", "STEP": f"= [[dinteg({a}, {b}, f(x), x)]] + [[dinteg({b}, {c}, f(x), x)]]", "RES": f"= {v1} + {_fmp(v2)} = {v}", "KIND": "구간 나누기"}
    return _pick(out, 330)


IN3_ROWS = _in3_rows()


def in_t3():
    return T(IN, 3, IN_B, title="정적분의 성질 — 대칭구간·선형성·구간 나누기",
        skill="기함수/우함수의 대칭구간 적분, ∫(kf + lg) = k∫f + l∫g, ∫ₐᶜ = ∫ₐᵇ + ∫ᵇᶜ 쓰기", axis={"성질": "대칭구간 / 선형성 / 구간 나누기"}, disc="홀수 차수 항이 대칭구간에서 사라짐과 정적분의 선형성·구간 합을 정확히 적용하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(IN3_ROWS)}}], table={"key": "f", "rows": IN3_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="{EXPR}의 값을 구하시오.", answer="{ans}",
        sol1="정적분의 성질을 쓴다: {LAW}. 이 문제는 {KIND} 유형이다.",
        sol2=[("{LAW}", "성질"), ("{STEP}", "적용"), ("{RES}", None, ("{ans}", "값"))],
        sol3=["성질을 쓰지 않고 직접 계산해도 같은 값이 나오는지(대칭구간이면 홀수 항이 0인지) 확인한다. 따라서 값은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}이므로 {STEP} {RES}. 따라서 값은 {ans}이다.",
        rubric=[("성질 적용", 3, "{STEP} 꼴로 바꿨다.", "홀수 차수 항을 남겼거나 계수를 안으로 넣지 않았으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("우함수 부분을 2배 하지 않음", "성질 적용", "불인정"), ("∫(f + g)를 ∫f × ∫g로 계산", "성질 적용", "불인정"), ("구간을 이어 붙일 때 부호 실수", "계산", "부분")])


def _in4_rows():
    out = {}
    for p in NZ(-2, 3):
        for qv in NZ(-4, 4):
            for r in NZ(-5, 5):
                ip = p + qv + r        # ∫_0^1 (3p t² + 2q t + r) dt
                for c in (2, 3, -1, -2, -3):
                    if (1 - c) == 0 or ip % (1 - c):
                        continue
                    k = ip // (1 - c)
                    f1 = 3 * p + 2 * qv + r + c * k
                    P = f"{'' if 3 * p == 1 else ('-' if 3 * p == -1 else 3 * p)}pow(x,2) {'+' if 2 * qv > 0 else '−'} {abs(2 * qv)}x {'+' if r > 0 else '−'} {abs(r)}"
                    cs = f"{'+' if c > 0 else '−'} {'' if abs(c) == 1 else abs(c)}"
                    q = f"함수 f(x) = {P.replace('pow(x,2)', 'x²')} {cs}[[dinteg(0, 1, f(t), t)]]일 때, f(1)"
                    if f1 == 0 or k == 0 or Fraction(f1) in _nums(q):
                        continue
                    out[f"k{p}_{qv}_{r}_{c}"] = {"P": P, "PT": P.replace("pow(x,2)", "x²"), "C": c, "CS": cs, "V": f1, "K": k, "IP": ip, "KIND": "정적분 = 상수", "STEP": f"[[dinteg(0, 1, f(t), t)]] = k(상수)로 놓으면 f(x) = {P.replace('pow(x,2)', 'x²')} {cs}k, 양변을 0에서 1까지 적분하면 k = {ip} {cs}k", "RES": f"k = {k}, f(x) = {P.replace('pow(x,2)', 'x²')} {'+' if c * k > 0 else '−'} {abs(c * k)}, f(1) = {f1}"}
    for p in NZ(-2, 3):
        for qv in NZ(-4, 4):
            for a in range(-2, 4):
                for x0 in range(-2, 5):
                    if x0 == a:
                        continue
                    fx0 = 3 * p * x0 * x0 + 2 * qv * x0
                    q = f"F(x) = [[dinteg({a}, x, {3 * p}pow(t,2) + {2 * qv}t, t)]] F'({x0})"
                    if fx0 == 0 or Fraction(fx0) in _nums(q):
                        continue
                    integrand = f"{'' if 3 * p == 1 else ('-' if 3 * p == -1 else 3 * p)}pow(t,2) {'+' if 2 * qv > 0 else '−'} {abs(2 * qv)}t"
                    out[f"d{p}_{qv}_{a}_{x0}"] = {"P": integrand, "PT": integrand.replace("pow(t,2)", "t²"), "C": 0, "V": fx0, "K": 0, "IP": 0, "KIND": "정적분으로 정의된 함수의 미분", "STEP": f"d/dx [[dinteg({a}, x, f(t), t)]] = f(x)이므로 F'(x) = {integrand.replace('pow(t,2)', 'x²').replace('t', 'x')}", "RES": f"F'({x0}) = {fx0}", "A": a, "X0": x0}
    return _pick(out, 330)


IN4_ROWS = _in4_rows()


def in_t4():
    return T(IN, 4, IN_B, title="정적분으로 정의된 함수 — 상수 취급·미분",
        skill="∫₀¹ f(t)dt는 상수 k로 놓고 적분해 k를 정하기, d/dx ∫ₐˣ f(t)dt = f(x) 쓰기", axis={"형태": "f(x) = P(x) + c∫₀¹f(t)dt / F(x) = ∫ₐˣ P(t)dt"}, disc="정적분이 상수임을 알고 방정식으로 k를 정하거나, 적분 위끝의 함수를 미분하면 피적분함수임을 쓰는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IN4_ROWS)}}], table={"key": "f", "rows": IN4_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="{Q}", answer="{ans}",
        sol1="{KIND}: 정적분 ∫₀¹ f(t)dt는 t에 대해 적분한 뒤 수가 되므로 상수 k로 둘 수 있고, 위끝이 x인 정적분 F(x) = ∫ₐˣ f(t)dt는 미분하면 F'(x) = f(x)이다.",
        sol2=[("{KIND}", "원리"), ("{STEP}", "적용"), ("{RES}", None, ("{ans}", "답"))],
        sol3=["구한 k를 다시 정적분에 넣어 등식이 맞는지(또는 F'(x)를 다시 적분해 F(x)가 되는지) 확인한다. 따라서 답은 {ans}이다.", "{STEP}", "답 {ans}"],
        model="{STEP}. {RES}. 따라서 답은 {ans}이다.",
        rubric=[("원리 적용", 3, "{STEP} 꼴로 세웠다.", "정적분을 함수로 취급했으면 인정하지 않는다."), ("답", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("∫₀¹ f(t)dt를 x의 함수로 봄", "원리 적용", "불인정"), ("F'(x)를 구할 때 아래끝 a를 대입한 값을 뺌", "원리 적용", "부분"), ("k의 방정식 풀이 실수", "답", "부분")])


def _in4_fix(t):
    for key, row in t["table"]["rows"].items():
        if key.startswith("k"):
            row["Q"] = f"함수 f(x) = {row['PT']} {row['CS']}[[dinteg(0, 1, f(t), t)]]일 때, f(1)의 값을 구하시오."
        else:
            row["Q"] = f"함수 F(x) = [[dinteg({row['A']}, x, {row['P']}, t)]]에 대하여 F'({row['X0']})의 값을 구하시오."
    return t


def _in5_rows():
    out = {}
    for p in range(-4, 5):
        for qv in range(p + 1, 7):
            for m in (1, -1, 2, -2):
                # y = m(x − p)(x − q) 와 x축: 넓이 = |m|(q − p)³/6
                v = Fraction(abs(m) * (qv - p) ** 3, 6)
                co = [m, -m * (p + qv), m * p * qv]
                desc = _pt(co)
                q = f"곡선 y = {desc}{_wa(desc)} x축으로 둘러싸인 부분의 넓이"
                if v in _nums(q):
                    continue
                out[f"a{p}_{qv}_{m}"] = {"DESC": q, "VN": v.numerator, "VD": v.denominator, "KIND": "곡선과 x축", "ROOTS": f"x = {p}, {qv}", "INT": f"[[dinteg({p}, {qv}, abs({_pm(co)}), x)]]", "STEP": f"{p} ≤ x ≤ {qv}에서 y {'≤' if m > 0 else '≥'} 0이므로 넓이 = {'−' if m > 0 else ''}[[dinteg({p}, {qv}, {_pm(co)}, x)]]", "RES": f"= [[frac({abs(m)} × pow({qv - p},3), 6)]] = {_fm(v)}"}
    for p in range(-3, 4):
        for qv in range(p + 1, 6):
            for a in (1, 2, -1, -3):
                # y = x² + a x + ... 와 직선: 차 = (x − p)(x − q) 꼴이 되게: 곡선 y = x² + c1 x + c0, 직선 y = m x + n: x² + (c1 − m)x + (c0 − n) = (x − p)(x − q)
                c1 = a
                m_ = c1 + (p + qv)
                c0 = 3
                n = c0 - p * qv
                v = Fraction((qv - p) ** 3, 6)
                curve = _pt([1, c1, c0])
                line = _pt([m_, n])
                q = f"곡선 y = {curve}{_wa(curve)} 직선 y = {line}{_ro(line)} 둘러싸인 부분의 넓이"
                if v in _nums(q) or m_ == 0:
                    continue
                out[f"b{p}_{qv}_{a}"] = {"DESC": q, "VN": v.numerator, "VD": v.denominator, "KIND": "곡선과 직선", "ROOTS": f"x = {p}, {qv}", "INT": f"[[dinteg({p}, {qv}, ({_pm([m_, n])}) − ({_pm([1, c1, c0])}), x)]]", "STEP": f"교점: {curve} = {line}에서 {_pt([1, -(p + qv), p * qv])} = 0, x = {p}, {qv}; {p} ≤ x ≤ {qv}에서 직선이 위이므로 넓이 = [[dinteg({p}, {qv}, -(x − {p})(x − {qv}), x)]]".replace("(x − -", "(x + "), "RES": f"= [[frac(pow({qv} − {_fmp(p)}, 3), 6)]] = {_fm(v)}"}
    return _pick(out, 330)


IN5_ROWS = _in5_rows()


def in_t5():
    return T(IN, 5, IN_B, title="넓이 — 곡선과 x축·곡선과 직선 사이",
        skill="교점을 구해 적분 구간을 정하고 (위 − 아래)를 적분해 넓이 구하기 (포물선: (β − α)³/6)", axis={"형태": "이차곡선과 x축 / 이차곡선과 직선", "교점": "−4~6"}, disc="어느 쪽이 위인지 판단해 부호를 맞추고 교점 사이를 적분하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IN5_ROWS)}}], table={"key": "f", "rows": IN5_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{DESC}를 구하시오.", answer="{ans}",
        sol1="두 그래프 사이의 넓이는 교점을 구해 구간을 정한 뒤 (위쪽 식 − 아래쪽 식)을 적분한다({KIND}). 교점은 {ROOTS}이다. 최고차항 계수가 a인 이차식이 두 근 α, β 사이에서 만드는 넓이는 |a|(β − α)³/6이다.",
        sol2=[("교점: {ROOTS}", "구간"), ("{STEP}", "위 − 아래"), ("{RES}", None, ("{ans}", "넓이"))],
        sol3=["적분 결과가 양수인지, 공식 |a|(β − α)³/6과 일치하는지 확인한다. 따라서 넓이는 {ans}이다.", "{INT}", "넓이 {ans}"],
        model="교점은 {ROOTS}이고 {STEP} {RES}. 따라서 넓이는 {ans}이다.",
        rubric=[("구간·부호", 3, "{STEP} 꼴로 세웠다.", "위·아래를 바꿔 음수가 나왔으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "적분 계산 실수면 1점.")],
        pitfalls=[("음수 넓이를 그대로 답함", "구간·부호", "부분"), ("교점을 잘못 구함", "구간·부호", "불인정"), ("적분 계산 실수", "계산", "부분")])


def _in6_rows():
    out = {}
    for k in range(1, 5):
        for a in range(1, 6):
            v = Fraction(k * a ** 3, 3)
            q = f"곡선 y = {'' if k == 1 else k}x², x축 및 직선 x = {a}{_ro(a)} 둘러싸인 부분의 넓이"
            if v in _nums(q):
                continue
            out[f"p{k}_{a}"] = {"DESC": q, "VN": v.numerator, "VD": v.denominator, "KIND": "곡선·x축·세로선", "INT": f"[[dinteg(0, {a}, {'' if k == 1 else k}pow(x,2), x)]]", "STEP": f"0 ≤ x ≤ {a}에서 y ≥ 0이므로 넓이 = [[dinteg(0, {a}, {'' if k == 1 else k}pow(x,2), x)]] = [[frac({k}, 3)]] × [[pow({a},3)]]", "RES": f"= {_fm(v)}"}
    for c in range(1, 7):
        v = Fraction(4 * c ** 3, 3)
        q = f"곡선 y = x²과 직선 y = {c * c}{_ro(c * c)} 둘러싸인 부분의 넓이"
        if v in _nums(q):
            continue
        out[f"h{c}"] = {"DESC": q, "VN": v.numerator, "VD": v.denominator, "KIND": "포물선과 수평선", "INT": f"[[dinteg(-{c}, {c}, {c * c} − pow(x,2), x)]]", "STEP": f"교점 x = ±{c}; −{c} ≤ x ≤ {c}에서 직선이 위이므로 넓이 = [[dinteg(-{c}, {c}, {c * c} − pow(x,2), x)]] = 2[[dinteg(0, {c}, {c * c} − pow(x,2), x)]]", "RES": f"= 2({c * c} × {c} − [[frac(pow({c},3), 3)]]) = {_fm(v)}"}
    for a in range(1, 6):
        # y = x³ 과 x축, x = -a, x = a: 2·a⁴/4 = a⁴/2
        v = Fraction(a ** 4, 2)
        q = f"곡선 y = x³, x축 및 두 직선 x = -{a}, x = {a}{_ro(a)} 둘러싸인 부분의 넓이"
        if v in _nums(q):
            continue
        out[f"c{a}"] = {"DESC": q, "VN": v.numerator, "VD": v.denominator, "KIND": "기함수 — 양쪽 넓이 합", "INT": f"2[[dinteg(0, {a}, pow(x,3), x)]]", "STEP": f"−{a} ≤ x ≤ 0에서 y ≤ 0, 0 ≤ x ≤ {a}에서 y ≥ 0이므로 넓이 = 2[[dinteg(0, {a}, pow(x,3), x)]] = 2 × [[frac(pow({a},4), 4)]]", "RES": f"= {_fm(v)}"}
    for p in range(1, 5):
        for qv in range(p + 1, 6):
            # y = x(x − p)(x − q)?? 3차는 넓이 복잡 → 대신 y = x² 과 y = 2px − p² + q? 생략. 두 포물선: y = x² 과 y = -x² + 2c: 교점 ±√c → c 제곱수
            pass
    for s in range(1, 5):
        c = s * s
        v = Fraction(8 * s ** 3, 3)
        q = f"두 곡선 y = x²과 y = -x² + {2 * c}{_ro(2 * c)} 둘러싸인 부분의 넓이"
        if v in _nums(q):
            continue
        out[f"t{s}"] = {"DESC": q, "VN": v.numerator, "VD": v.denominator, "KIND": "두 포물선", "INT": f"[[dinteg(-{s}, {s}, ({2 * c} − 2pow(x,2)), x)]]", "STEP": f"교점: x² = −x² + {2 * c}에서 x = ±{s}; −{s} ≤ x ≤ {s}에서 −x² + {2 * c}{_ika(2 * c)} 위이므로 넓이 = [[dinteg(-{s}, {s}, {2 * c} − 2pow(x,2), x)]] = 2[[dinteg(0, {s}, {2 * c} − 2pow(x,2), x)]]", "RES": f"= 2({2 * c} × {s} − [[frac(2 × pow({s},3), 3)]]) = {_fm(v)}"}
    return out


IN6_ROWS = _in6_rows()


def in_t6():
    return T(IN, 6, IN_B, title="넓이 — 대칭·기함수·두 곡선",
        skill="대칭성을 이용해 절반을 2배 하거나 x축 아래 부분의 부호를 바꿔 넓이 구하기", axis={"형태": "y = kx²와 x = a / y = x²과 y = c² / y = x³ 양쪽 / 두 포물선"}, disc="x축 아래 부분은 −∫로 더하고 대칭이면 2배 하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(IN6_ROWS)}}], table={"key": "f", "rows": IN6_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{DESC}를 구하시오.", answer="{ans}",
        sol1="넓이는 항상 양수이므로 x축 아래 부분은 −∫f(x)dx로 더하고, 그래프가 y축에 대칭이면 0에서 a까지의 2배로 계산한다({KIND}).",
        sol2=[("{KIND}", "형태"), ("{STEP}", "적분 세우기"), ("{RES}", None, ("{ans}", "넓이"))],
        sol3=["그래프를 그려 x축 아래 부분과 대칭을 확인하고, 계산 결과가 양수인지 본다. 따라서 넓이는 {ans}이다.", "{INT}", "넓이 {ans}"],
        model="{STEP} {RES}. 따라서 넓이는 {ans}이다.",
        rubric=[("적분 세우기", 3, "{STEP} 꼴로 세웠다.", "x축 아래 부분의 부호를 바꾸지 않았으면 1점."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "적분 계산 실수면 1점.")],
        pitfalls=[("y = x³을 −a에서 a까지 그대로 적분해 0으로 답함", "적분 세우기", "불인정"), ("두 곡선의 위아래를 바꿈", "적분 세우기", "부분"), ("적분 계산 실수", "계산", "부분")])


IN_SEED = SEED(IN, category="해석", title="적분 — 부정적분·정적분 계산·정적분의 성질·정적분으로 정의된 함수·넓이(곡선과 축/직선)·넓이(대칭·두 곡선)", unit_id="h2-2", concept_ids=["h2-2-13", "h2-2-14", "h2-2-15"],
               schema_name="부정적분과 정적분", note="피적분함수는 3px² + 2qx + r 꼴로 정수 결과 보장. 넓이는 (β − α)³/6 계열과 대칭 계열.",
               templates=[in_t1(), in_t2(), in_t3(), _in4_fix(in_t4()), in_t5(), in_t6()])


if __name__ == "__main__":
    run(AP_SEED, IN_SEED)
