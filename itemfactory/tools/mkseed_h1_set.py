# itemfactory/tools/mkseed_h1_set.py — 고1 공통수학2 집합·명제·함수 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_h1_set.py
#     → seeds/h1-2-set.json     (집합: 부분집합의 개수·n(A∪B)·서베이·집합 연산의 원소 합·조건제시법 집합, 5틀)
#     → seeds/h1-2-logic.json   (명제: 진리집합·모든/어떤 명제의 참 조건·충분/필요조건 k·산술기하 1변수·2변수, 5틀)
#     → seeds/h1-2-func.json    (함수: 일차함수 값·합성함수 값·역함수 값·합성의 역함수·함수의 개수, 5틀)
#     → seeds/h1-2-ratfn.json   (유리·무리함수: 점근선 교점·평행이동 정/역·무리함수 정의역 치역·무리함수 평행이동, 4틀)
#   집합 표기는 [[set(…)]]·[[setb(x, …)]] 마커(중괄호는 자리표시자와 충돌하므로 문면에 직접 쓰지 않는다). 여집합은 본문에 Aᶜ.
from __future__ import annotations

import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, NZ, SEED, T, run  # noqa: E402
from genkit.expr import eul as _eul, eun as _eun, wa as _wa  # noqa: E402

rng = random.Random(20260914)


def _nums(text):
    import re
    return {int(x) for x in re.findall(r"(?<![\d.])-?\d+(?![\d.])", text)}


def _setm(els):
    return "[[set(" + ", ".join(str(e) for e in els) + ")]]"


# ═══════════════════════════════════════════════════════════════════ 1. 집합
ST = "h1-2-set"
ST_B = {**HS, "prereq": ["집합의 뜻", "약수와 배수"], "ops": ["집합"], "traps": ["원소의 개수와 부분집합의 개수 혼동", "교집합 중복 빼기"], "tags": ["집합", "집합의 연산"]}


def _st1_rows():
    out = {}
    sets = {"n": lambda n: list(range(1, n + 1)), "e": lambda n: [2 * i for i in range(1, n + 1)], "o": lambda n: [2 * i - 1 for i in range(1, n + 1)], "t": lambda n: [3 * i for i in range(1, n + 1)], "a": lambda n: list("abcdefg"[:n]), "x": lambda n: list("xyzwuvt"[:n])}
    for sk, mk in sets.items():
        for n in range(4, 8):
            els = mk(n)
            first, last = els[0], els[-1]
            kinds = {
                "all": ("부분집합의 개수", 0, f"원소가 {n}개이므로 [[pow(2,{n})]]", f"[[pow(2,{n})]]", 2 ** n),
                "inc1": (f"{last}{_eul(last)} 원소로 갖는 부분집합의 개수", 1, f"{last}{_eun(last)} 반드시 넣고 나머지 {n - 1}개의 원소를 넣거나 빼므로 [[pow(2,{n - 1})]]", f"[[pow(2,{n - 1})]]", 2 ** (n - 1)),
                "inc2": (f"{first}, {els[1]}{_eul(els[1])} 모두 원소로 갖는 부분집합의 개수", 2, f"{first}, {els[1]}{_eun(els[1])} 반드시 넣고 나머지 {n - 2}개의 원소를 넣거나 빼므로 [[pow(2,{n - 2})]]", f"[[pow(2,{n - 2})]]", 2 ** (n - 2)),
                "exc1": (f"{first}{_eul(first)} 원소로 갖지 않는 부분집합의 개수", 1, f"{first}{_eun(first)} 빼고 나머지 {n - 1}개의 원소로 만드는 부분집합이므로 [[pow(2,{n - 1})]]", f"[[pow(2,{n - 1})]]", 2 ** (n - 1)),
                "incexc": (f"{first}{_eun(first)} 원소로 갖고 {last}{_eun(last)} 원소로 갖지 않는 부분집합의 개수", 2, f"{first}{_eun(first)} 반드시 넣고 {last}{_eun(last)} 빼면 나머지 {n - 2}개의 원소만 넣거나 빼므로 [[pow(2,{n - 2})]]", f"[[pow(2,{n - 2})]]", 2 ** (n - 2)),
                "proper": ("진부분집합의 개수", 0, f"부분집합 [[pow(2,{n})]]개에서 자기 자신 1개를 뺀 [[pow(2,{n})]] − 1", f"[[pow(2,{n})]] − 1", 2 ** n - 1),
            }
            for kk, (cond, fix, expl, form, v) in kinds.items():
                if sk not in ("a", "x") and v in set(els):
                    continue
                out[f"{sk}{n}_{kk}"] = {"SETS": ", ".join(str(e) for e in els), "COND": cond, "N": n, "FIX": fix, "EXPL": expl, "FORM": form, "V": v}
    return out


ST1_ROWS = _st1_rows()


def st_t1():
    return T(ST, 1, ST_B, title="부분집합의 개수 — 특정 원소를 포함하거나 제외",
        skill="원소 n개인 집합의 부분집합은 2ⁿ개, 특정 원소 k개의 포함·제외를 고정하면 2ⁿ⁻ᵏ개임을 쓰기", axis={"집합": "원소 4~7개(자연수·짝수·문자)", "조건": "전체·포함·제외·진부분집합"}, disc="고정된 원소를 제외한 나머지 원소의 개수를 지수로 놓는가", diff=2,
        params=[{"name": "f", "values": {"in": list(ST1_ROWS)}}], table={"key": "f", "rows": ST1_ROWS},
        derive={"ans": "V", "E": "N - FIX"}, cost=["N", "FIX", "ans"], verify=["ans == V"],
        q="집합 A = [[set({SETS})]]의 {COND}를 구하시오.", answer="{ans}",
        sol1="원소가 n개인 집합의 부분집합의 개수는 각 원소를 '넣는다/뺀다' 두 가지씩 고르므로 2ⁿ이다. 특정 원소의 포함·제외가 정해지면 그 원소는 고를 수 없으므로 나머지 원소의 개수만 지수에 넣는다.",
        sol2=[("집합 A의 원소는 {N}개", "원소 세기"), ("{EXPL}", "고정 원소 제외"), ("{FORM} = {ans}", None, ("{ans}", "개수"))],
        sol3=["고정되지 않은 원소가 {E}개이면 부분집합은 [[pow(2,{E})]]개다. 따라서 {COND}는 {ans}이다.", "고정 {FIX}개, 자유 {E}개", "답 {ans}"],
        model="집합 A의 원소는 {N}개이고 {EXPL}이므로 {FORM} = {ans}이다.",
        rubric=[("지수 세우기", 3, "{FORM}{ro(FORM)} 세웠다.", "고정 원소를 지수에서 빼지 않았으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "거듭제곱 계산 실수면 1점.")],
        pitfalls=[("특정 원소를 포함하는 부분집합을 2ⁿ으로 셈", "지수 세우기", "불인정"), ("진부분집합에서 자기 자신을 빼지 않음", "지수 세우기", "불인정"), ("2의 거듭제곱 계산 실수", "계산", "부분")])


def st_t2():
    return T(ST, 2, ST_B, title="n(A ∪ B) = n(A) + n(B) − n(A ∩ B)",
        skill="합집합의 원소의 개수 공식에서 모르는 값 하나 구하기", axis={"n(A), n(B)": "5~12, 4~12", "묻는 것": "합집합·교집합·차집합"}, disc="합집합의 개수에서 교집합을 한 번 빼며, n(A − B) = n(A) − n(A ∩ B)임을 아는가", diff=2,
        params=[{"name": "a", "values": {"int": [5, 12]}}, {"name": "b", "values": {"int": [4, 12]}}, {"name": "c", "values": {"int": [1, 4]}}, {"name": "k", "values": {"in": ["union", "inter", "diff", "diffu"]}}],
        table={"key": "k", "rows": {"union": {"G3": "n(A ∩ B)", "ASK": "n(A ∪ B)", "EXPL": "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)", "wg": 1, "wa": 1, "wb": 0, "wc": 0},
                                    "inter": {"G3": "n(A ∪ B)", "ASK": "n(A ∩ B)", "EXPL": "n(A ∩ B) = n(A) + n(B) − n(A ∪ B)", "wg": 0, "wa": 0, "wb": 1, "wc": 0},
                                    "diff": {"G3": "n(A ∩ B)", "ASK": "n(A − B)", "EXPL": "n(A − B) = n(A) − n(A ∩ B)", "wg": 1, "wa": 0, "wb": 0, "wc": 1},
                                    "diffu": {"G3": "n(A ∪ B)", "ASK": "n(A − B)", "EXPL": "n(A ∩ B) = n(A) + n(B) − n(A ∪ B), n(A − B) = n(A) − n(A ∩ B)", "wg": 0, "wa": 0, "wb": 0, "wc": 1}}},
        derive={"u": "a + b - c", "g3": "wg*c + (1 - wg)*(a + b - c)", "ans": "wa*(a + b - c) + wb*c + wc*(a - c)"},
        constraints=["c < a", "c < b", "ans not in (a, b, g3)", "ans != 0"], cost=["a", "b", "c", "u", "ans"], verify=["u == a + b - c", "g3 == wg*c + (1 - wg)*u"],
        q="두 집합 A, B에 대하여 n(A) = {a}, n(B) = {b}, {G3} = {g3}일 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="합집합의 원소의 개수는 n(A ∪ B) = n(A) + n(B) − n(A ∩ B)이다 — 두 집합의 원소를 그냥 더하면 교집합의 원소가 두 번 세어지므로 한 번 뺀다. 차집합은 n(A − B) = n(A) − n(A ∩ B)이다.",
        sol2=[("n(A ∪ B) = n(A) + n(B) − n(A ∩ B)", "합집합 공식"), ("{u} = {a} + {b} − {c}, 즉 n(A ∩ B) = {c}, n(A ∪ B) = {u}", "대입"), ("{EXPL} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["n(A) = {a}, n(B) = {b}, n(A ∩ B) = {c}, n(A ∪ B) = {u}{ika(u)} 공식 {a} + {b} − {c} = {u}{eul(u)} 만족한다. 따라서 {ASK} = {ans}이다.", "{a} + {b} − {c} = {u} ✓", "{ASK} = {ans}"],
        model="n(A ∪ B) = n(A) + n(B) − n(A ∩ B)에서 n(A ∩ B) = {c}, n(A ∪ B) = {u}이므로 {ASK} = {ans}이다.",
        rubric=[("합집합 공식", 3, "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)를 세워 n(A ∩ B) = {c}, n(A ∪ B) = {u}{eul(u)} 얻었다.", "교집합을 빼지 않았으면 인정하지 않는다."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "차집합을 n(A) − n(B)로 두었으면 인정하지 않는다.")],
        pitfalls=[("n(A ∪ B) = n(A) + n(B)로 둠", "합집합 공식", "불인정"), ("n(A − B) = n(A) − n(B)로 둠", "답", "불인정"), ("이항 부호 실수", "답", "부분")])


SUBJ = {"math": {"S1": "수학", "S2": "영어", "S1E": "수학을", "S2E": "영어를", "BOTH": "수학과 영어를", "ATL": "수학과 영어 중 적어도 하나를", "ONLY": "수학만"},
        "soccer": {"S1": "축구", "S2": "농구", "S1E": "축구를", "S2E": "농구를", "BOTH": "축구와 농구를", "ATL": "축구와 농구 중 적어도 하나를", "ONLY": "축구만"},
        "piano": {"S1": "피아노", "S2": "바이올린", "S1E": "피아노를", "S2E": "바이올린을", "BOTH": "피아노와 바이올린을", "ATL": "피아노와 바이올린 중 적어도 하나를", "ONLY": "피아노만"}}
ST3_KINDS = {"atl": {"ASKKEY": "ATL", "TAIL": "좋아하는 학생 수", "EXPL": "n(A ∪ B) = n(A) + n(B) − n(A ∩ B)", "wa": 1, "wn": 0, "wo": 0},
             "none": {"ASKKEY": "BOTH", "TAIL": "모두 좋아하지 않는 학생 수", "EXPL": "n((A ∪ B)ᶜ) = n(U) − n(A ∪ B)", "wa": 0, "wn": 1, "wo": 0},
             "only": {"ASKKEY": "ONLY", "TAIL": "좋아하는 학생 수", "EXPL": "n(A − B) = n(A) − n(A ∩ B)", "wa": 0, "wn": 0, "wo": 1}}
ST3_ROWS = {f"{sk}_{kk}": {**sv, **{k: v for k, v in kv.items() if k != "ASKKEY"}, "ASKS": sv[kv["ASKKEY"]]} for sk, sv in SUBJ.items() for kk, kv in ST3_KINDS.items()}


def st_t3():
    return T(ST, 3, ST_B, title="집합의 원소의 개수 활용 — 두 가지 중 적어도 하나·둘 다 아님·한쪽만",
        skill="전체·A·B·A∩B의 인원에서 n(A ∪ B), n((A ∪ B)ᶜ), n(A − B)를 구하기", axis={"전체 인원": "20~40", "묻는 것": "적어도 하나 / 둘 다 아님 / 한쪽만"}, disc="'둘 다 좋아하지 않는' = 전체 − n(A ∪ B), '한쪽만' = n(A) − n(A ∩ B)로 옮기는가", diff=2,
        params=[{"name": "f", "values": {"in": list(ST3_ROWS)}}, {"name": "N", "values": {"int": [20, 40]}}, {"name": "a", "values": {"int": [8, 25]}}, {"name": "b", "values": {"int": [6, 22]}}, {"name": "c", "values": {"int": [2, 9]}}],
        table={"key": "f", "rows": ST3_ROWS},
        derive={"u": "a + b - c", "ans": "wa*(a + b - c) + wn*(N - a - b + c) + wo*(a - c)", "rest": "N - a - b + c"},
        constraints=["c < a", "c < b", "a + b - c < N", "ans not in (N, a, b, c)", "ans != 0"], cost=["N", "a", "b", "c", "u", "ans"], verify=["u == a + b - c", "rest == N - u"],
        q="어느 반 학생 {N}명 중에서 {S1E} 좋아하는 학생이 {a}명, {S2E} 좋아하는 학생이 {b}명, {BOTH} 모두 좋아하는 학생이 {c}명이다. {ASKS} {TAIL}를 구하시오.", answer="{ans}",
        sol1="{S1E} 좋아하는 학생의 집합을 A, {S2E} 좋아하는 학생의 집합을 B라 하면 n(A) = {a}, n(B) = {b}, n(A ∩ B) = {c}이다. 적어도 하나는 n(A ∪ B), 둘 다 아님은 전체에서 n(A ∪ B)를 뺀 것, 한쪽만은 n(A) − n(A ∩ B)이다.",
        sol2=[("n(A ∪ B) = {a} + {b} − {c} = {u}", "적어도 하나"), ("둘 다 아님: {N} − {u} = {rest}, {S1}만: {a} − {c} = {a - c}", "여집합·차집합"), ("{EXPL} → {ans}", None, ("{ans}", "답"))],
        sol3=["네 부분(둘 다 {c}, {S1}만 {a - c}, {S2}만 {b - c}, 둘 다 아님 {rest})을 더하면 {N}{ika(N)} 되어 전체와 맞는다. 따라서 답은 {ans}이다.", "{c} + {a - c} + {b - c} + {rest} = {N} ✓", "답 {ans}"],
        model="n(A ∪ B) = {a} + {b} − {c} = {u}이고 {EXPL}이므로 구하는 학생 수는 {ans}이다.",
        rubric=[("집합으로 옮기기", 3, "n(A ∪ B) = {u}{eul(u)} 구했다.", "교집합을 빼지 않았으면 인정하지 않는다."), ("답", 2, "{ans}명을 구했다.", "묻는 부분을 잘못 골랐으면 인정하지 않는다.")],
        pitfalls=[("적어도 하나를 n(A) + n(B)로 셈", "집합으로 옮기기", "불인정"), ("둘 다 아님을 n(A ∪ B)로 답함", "답", "불인정"), ("한쪽만을 n(A)로 답함", "답", "불인정")])


def _st4_rows():
    out = {}
    U = list(range(1, 10))
    asks = [("Aᶜ ∩ B의 모든 원소의 합", lambda A, B: sorted(set(B) - set(A)), "Aᶜ ∩ B = B − A"),
            ("(A ∪ B)ᶜ의 모든 원소의 합", lambda A, B: sorted(set(U) - set(A) - set(B)), "(A ∪ B)ᶜ = U − (A ∪ B)"),
            ("A − B의 모든 원소의 합", lambda A, B: sorted(set(A) - set(B)), "A − B: A에만 있는 원소"),
            ("A ∩ Bᶜ의 모든 원소의 합", lambda A, B: sorted(set(A) - set(B)), "A ∩ Bᶜ = A − B"),
            ("(A ∩ B)ᶜ의 모든 원소의 합", lambda A, B: sorted(set(U) - (set(A) & set(B))), "(A ∩ B)ᶜ = U − (A ∩ B)")]
    tries = 0
    while len(out) < 240 and tries < 20000:
        tries += 1
        A = sorted(rng.sample(U, rng.choice([4, 5])))
        B = sorted(rng.sample(U, rng.choice([4, 5])))
        inter = sorted(set(A) & set(B))
        if not 1 <= len(inter) <= 3:
            continue
        ai = rng.randrange(len(asks))
        ask, fn, expl = asks[ai]
        res = fn(A, B)
        v = sum(res)
        if not res or v < 10:
            continue
        key = f"{''.join(map(str, A))}_{''.join(map(str, B))}_{ai}"
        if key in out:
            continue
        out[key] = {"SETA": ", ".join(map(str, A)), "SETB": ", ".join(map(str, B)), "ASK": ask, "EXPL": expl, "RES": _setm(res), "INTER": _setm(inter), "UNION": _setm(sorted(set(A) | set(B))),
                    "V": v, "SUMS": " + ".join(map(str, res))}
    return out


ST4_ROWS = _st4_rows()


def st_t4():
    return T(ST, 4, ST_B, title="집합의 연산 — 여집합·차집합의 원소의 합",
        skill="전체집합 U = {1, …, 9}에서 A, B의 여집합·차집합·합집합·교집합을 원소로 나열해 합 구하기", axis={"A, B": "원소 4~5개의 부분집합", "연산": "Aᶜ ∩ B, (A ∪ B)ᶜ, A − B, A ∩ Bᶜ, (A ∩ B)ᶜ"}, disc="드모르간·차집합 관계로 연산 결과를 원소로 정확히 나열하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(ST4_ROWS)}}], table={"key": "f", "rows": ST4_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="9 이하의 자연수 전체의 집합 U의 두 부분집합 A = [[set({SETA})]], B = [[set({SETB})]]에 대하여 {ASK}을 구하시오.", answer="{ans}",
        sol1="여집합 Xᶜ은 U에서 X의 원소를 뺀 것, 차집합 A − B는 A에는 있고 B에는 없는 원소의 집합이다. Aᶜ ∩ B = B − A, A ∩ Bᶜ = A − B이고 드모르간 법칙 (A ∪ B)ᶜ = Aᶜ ∩ Bᶜ, (A ∩ B)ᶜ = Aᶜ ∪ Bᶜ을 쓰면 원소를 나열하기 쉽다.",
        sol2=[("A ∩ B = {INTER}, A ∪ B = {UNION}", "교집합·합집합"), ("{EXPL} → {RES}", "원소 나열"), ("합: {SUMS} = {ans}", None, ("{ans}", "원소의 합"))],
        sol3=["나열한 집합 {RES}의 원소가 모두 U의 원소이고 조건에 맞는지 A, B와 대조해 확인한다. 따라서 답은 {ans}이다.", "{RES}", "합 {ans}"],
        model="{EXPL}이므로 구하는 집합은 {RES}이고 원소의 합은 {SUMS} = {ans}이다.",
        rubric=[("원소 나열", 3, "{RES}{eul(ans)} 바르게 나열했다.", "원소 하나가 빠지거나 더해졌으면 1점."), ("합", 2, "{ans}{eul(ans)} 구했다.", "덧셈 실수면 1점.")],
        pitfalls=[("Aᶜ ∩ B를 A − B로 봄", "원소 나열", "불인정"), ("(A ∪ B)ᶜ을 Aᶜ ∪ Bᶜ으로 봄", "원소 나열", "불인정"), ("덧셈 실수", "합", "부분")])


def _divs(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def _st5_rows():
    out = {}
    for n1 in range(12, 49):
        for n2 in range(12, 49):
            if n1 == n2 or math.gcd(n1, n2) < 4:
                continue
            A, B = _divs(n1), _divs(n2)
            inter = sorted(set(A) & set(B))
            desc = f"{n1}의 양의 약수 전체의 집합을 A, {n2}의 양의 약수 전체의 집합을 B라 할 때"
            for kk, ask, v, expl in [("i", "n(A ∩ B)", len(inter), f"A ∩ B는 {n1}{_wa(n1)} {n2}의 공약수의 집합, 즉 최대공약수 {math.gcd(n1, n2)}의 약수의 집합"),
                                     ("u", "n(A ∪ B)", len(A) + len(B) - len(inter), f"n(A ∪ B) = n(A) + n(B) − n(A ∩ B), A ∩ B는 최대공약수 {math.gcd(n1, n2)}의 약수의 집합"),
                                     ("d", "n(A − B)", len(A) - len(inter), f"n(A − B) = n(A) − n(A ∩ B), A ∩ B는 최대공약수 {math.gcd(n1, n2)}의 약수의 집합")]:
                if v in _nums(desc) or v < 2:
                    continue
                out[f"d{n1}_{n2}_{kk}"] = {"DESC": desc, "ASK": ask, "V": v, "EXPL": expl, "SETA": _setm(A), "SETB": _setm(B), "INTER": _setm(inter), "NA": len(A), "NB": len(B), "NI": len(inter)}
    keys = sorted(out)
    rng.shuffle(keys)
    out = {k: out[k] for k in keys[:180]}
    for lim in (20, 24, 30, 36, 40, 48, 50, 60):
        for p in (2, 3, 4, 5, 6):
            for q in (2, 3, 4, 5, 6, 7):
                if p >= q or math.gcd(p, q) != 1:
                    continue
                A = [x for x in range(1, lim + 1) if x % p == 0]
                B = [x for x in range(1, lim + 1) if x % q == 0]
                inter = sorted(set(A) & set(B))
                if len(inter) < 1:
                    continue
                desc = f"{lim} 이하의 자연수 중 {p}의 배수 전체의 집합을 A, {q}의 배수 전체의 집합을 B라 할 때"
                for kk, ask, v, expl in [("u", "n(A ∪ B)", len(A) + len(B) - len(inter), f"n(A ∪ B) = n(A) + n(B) − n(A ∩ B), A ∩ B는 {p * q}의 배수의 집합"),
                                         ("d", "n(A − B)", len(A) - len(inter), f"n(A − B) = n(A) − n(A ∩ B), A ∩ B는 {p * q}의 배수의 집합")]:
                    if v in _nums(desc) or v < 2:
                        continue
                    out[f"m{lim}_{p}_{q}_{kk}"] = {"DESC": desc, "ASK": ask, "V": v, "EXPL": expl, "SETA": _setm(A), "SETB": _setm(B), "INTER": _setm(inter), "NA": len(A), "NB": len(B), "NI": len(inter)}
    return out


ST5_ROWS = _st5_rows()


def st_t5():
    return T(ST, 5, ST_B, title="조건으로 주어진 집합 — 약수·배수 집합의 연산",
        skill="약수·배수의 집합을 원소나열법으로 바꾸고 교집합(공약수·공배수)을 이용해 원소의 개수 구하기", axis={"집합": "약수 집합 두 개 / 배수 집합 두 개", "묻는 것": "n(A ∩ B), n(A ∪ B), n(A − B)"}, disc="공약수는 최대공약수의 약수, 공배수는 최소공배수의 배수임을 써서 교집합을 세는가", diff=3,
        params=[{"name": "f", "values": {"in": list(ST5_ROWS)}}], table={"key": "f", "rows": ST5_ROWS},
        derive={"ans": "V"}, cost=["NA", "NB", "NI", "ans"], verify=["ans == V"],
        q="{DESC}, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="두 집합을 원소나열법으로 쓰면 A = {SETA}, B = {SETB}이다. 두 수의 공약수는 최대공약수의 약수이고, 공배수는 최소공배수의 배수이므로 교집합을 바로 셀 수 있다.",
        sol2=[("n(A) = {NA}, n(B) = {NB}", "각 집합의 원소 세기"), ("A ∩ B = {INTER}, n(A ∩ B) = {NI}", "교집합"), ("{EXPL} → {ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["n(A ∪ B) = {NA} + {NB} − {NI}, n(A − B) = {NA} − {NI}{ro(NI)} 검산할 수 있다. 따라서 {ASK} = {ans}이다.", "n(A) = {NA}, n(B) = {NB}, n(A ∩ B) = {NI}", "{ASK} = {ans}"],
        model="A = {SETA}, B = {SETB}, A ∩ B = {INTER}이고 {EXPL}이므로 {ASK} = {ans}이다.",
        rubric=[("원소나열·교집합", 3, "A ∩ B = {INTER}{ro(NI)} 구했다.", "원소를 하나 빠뜨렸으면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "공식 적용 실수면 1점.")],
        pitfalls=[("공약수를 두 수의 약수 전체로 봄", "원소나열·교집합", "불인정"), ("합집합에서 교집합을 빼지 않음", "답", "불인정"), ("약수·배수를 빠뜨림", "원소나열·교집합", "부분")])


ST_SEED = SEED(ST, category="대수", title="집합 — 부분집합의 개수·합집합의 원소의 개수·서베이·연산의 원소 합·약수와 배수의 집합", unit_id="h1-2", concept_ids=["h1-2-08", "h1-2-09", "h1-2-10"],
               schema_name="집합의 뜻과 연산", note="집합 표기는 [[set(…)]] 마커. 연산 결과 합·개수는 파이썬 행에서 미리 계산(V)하고 노출(R-05)은 행 생성 시 걸렀다.",
               templates=[st_t1(), st_t2(), st_t3(), st_t4(), st_t5()])


# ═══════════════════════════════════════════════════════════════════ 2. 명제
LG = "h1-2-logic"
LG_B = {**HS, "prereq": ["집합", "이차방정식의 판별식", "절댓값"], "ops": ["명제"], "traps": ["부정과 여집합", "충분·필요의 방향"], "tags": ["명제", "진리집합", "절대부등식"]}


def _lg1_rows():
    out = {}
    for N in range(6, 13):
        U = list(range(1, N + 1))
        conds = []
        for r1 in range(1, 8):
            for r2 in range(r1 + 1, 10):
                s, p = r1 + r2, r1 * r2
                conds.append((f"x² − {s}x + {p} = 0", [r for r in (r1, r2) if r <= N], f"(x − {r1})(x − {r2}) = 0에서 x = {r1} 또는 x = {r2}"))
        for k in (12, 16, 18, 20, 24, 28, 30, 36):
            conds.append((f"x는 {k}의 약수이다", [d for d in _divs(k) if d <= N], f"{k}의 약수 중 U의 원소인 것"))
        for c, w in [(4, 1), (5, 2), (6, 2), (7, 3), (8, 3), (5, 1), (6, 1), (7, 2), (8, 2), (9, 3)]:
            conds.append((f"[[abs(x − {c})]] ≤ {w}", [x for x in U if abs(x - c) <= w], f"{c - w} ≤ x ≤ {c + w}"))
        for cond, P, expl in conds:
            if not P or len(P) == N:
                continue
            Pc = [x for x in U if x not in P]
            for kk, aske, v, form in [("cnt", "P의 원소의 개수를", len(P), "n(P)"), ("sum", "P의 모든 원소의 합을", sum(P), "P의 원소의 합"),
                                      ("ccnt", "Pᶜ의 원소의 개수를", len(Pc), "n(Pᶜ) = n(U) − n(P)"), ("csum", "Pᶜ의 모든 원소의 합을", sum(Pc), "Pᶜ의 원소의 합")]:
                q = f"{N} 이하의 자연수 전체의 집합 U에서 조건 p: '{cond}'의 진리집합을 P라 할 때, {aske} 구하시오."
                if v in _nums(q) or v == 0:
                    continue
                out[f"{N}_{cond}_{kk}"] = {"N": N, "COND": cond, "ASKE": aske, "V": v, "EXPL": expl, "SETP": _setm(P), "SETPC": _setm(Pc), "FORM": form, "NP": len(P)}
    keys = sorted(out)
    rng.shuffle(keys)
    return {f"r{i}": out[k] for i, k in enumerate(keys[:260])}


LG1_ROWS = _lg1_rows()


def lg_t1():
    return T(LG, 1, LG_B, title="조건의 진리집합 — 원소의 개수와 합",
        skill="전체집합 안에서 조건을 만족하는 원소를 모두 나열해 진리집합과 그 여집합 읽기", axis={"U": "6~12 이하의 자연수", "조건": "이차방정식·약수·절댓값 부등식", "묻는 것": "P·Pᶜ의 개수·합"}, disc="조건을 푼 해 중 전체집합에 속하는 것만 진리집합에 넣고, ~p의 진리집합은 Pᶜ임을 아는가", diff=2,
        params=[{"name": "f", "values": {"in": list(LG1_ROWS)}}], table={"key": "f", "rows": LG1_ROWS},
        derive={"ans": "V"}, cost=["N", "NP", "ans"], verify=["ans == V"],
        q="{N} 이하의 자연수 전체의 집합 U에서 조건 p: '{COND}'의 진리집합을 P라 할 때, {ASKE} 구하시오.", answer="{ans}",
        sol1="진리집합은 전체집합 U의 원소 중 조건 p를 참이 되게 하는 것 전체의 집합이다. 조건을 풀어 {EXPL}이고, 이 중 U의 원소(1부터 {N}까지의 자연수)인 것만 모으면 P = {SETP}이다. ~p의 진리집합은 Pᶜ = {SETPC}이다.",
        sol2=[("조건 풀기: {EXPL}", "조건 → 해"), ("P = {SETP} (U의 원소만), Pᶜ = {SETPC}", "진리집합·여집합"), ("{FORM} = {ans}", None, ("{ans}", "답"))],
        sol3=["n(P) + n(Pᶜ) = {N}{ika(N)} 되는지로 나열이 빠짐없는지 확인한다. 따라서 답은 {ans}이다.", "P = {SETP}, Pᶜ = {SETPC}", "답 {ans}"],
        model="조건을 풀면 {EXPL}이므로 P = {SETP}, Pᶜ = {SETPC}이다. 따라서 {FORM} = {ans}이다.",
        rubric=[("진리집합", 3, "진리집합 P = {SETP}(원소 {NP}개)를 구했다.", "U에 없는 해를 넣었으면 1점."), ("답", 2, "{ans}{eul(ans)} 구했다.", "개수·합을 바꿔 답했으면 인정하지 않는다.")],
        pitfalls=[("U 밖의 해를 진리집합에 넣음", "진리집합", "부분"), ("Pᶜ 대신 P로 답함", "답", "불인정"), ("원소 나열 누락", "진리집합", "부분")])


def _lg2_rows():
    out = {}
    for c in range(2, 41):
        r1 = math.isqrt(c - 1)          # k² < c  ⇔ |k| ≤ r1
        r2 = math.isqrt(4 * c - 1)      # k² < 4c
        r3 = math.isqrt(c)              # k² ≤ c
        r4 = math.isqrt(4 * c)          # k² ≤ 4c
        kinds = [
            ("all2", f"모든 실수 x에 대하여 x² + 2kx + {c} > 0", "정수 k의 개수", f"D/4 = k² − {c} < 0", f"k² < {c}, 즉 −{r1} ≤ k ≤ {r1}", 2 * r1 + 1, "판별식 D < 0"),
            ("all1", f"모든 실수 x에 대하여 x² + kx + {c} > 0", "정수 k의 개수", f"D = k² − {4 * c} < 0", f"k² < {4 * c}, 즉 −{r2} ≤ k ≤ {r2}", 2 * r2 + 1, "판별식 D < 0"),
            ("alle", f"모든 실수 x에 대하여 x² + 2kx + {c} ≥ 0", "정수 k의 개수", f"D/4 = k² − {c} ≤ 0", f"k² ≤ {c}, 즉 −{r3} ≤ k ≤ {r3}", 2 * r3 + 1, "판별식 D ≤ 0"),
            ("some2", f"어떤 실수 x에 대하여 x² + 2kx + {c} < 0", "자연수 k의 최솟값", f"D/4 = k² − {c} > 0", f"k² > {c}, 자연수 k는 {r3 + 1} 이상", r3 + 1, "판별식 D > 0"),
            ("some1", f"어떤 실수 x에 대하여 x² − kx + {c} < 0", "자연수 k의 최솟값", f"D = k² − {4 * c} > 0", f"k² > {4 * c}, 자연수 k는 {r4 + 1} 이상", r4 + 1, "판별식 D > 0"),
        ]
        for kk, stmt, qty, dcond, rng_, v, law in kinds:
            q = f"명제 '{stmt}이다.'가 참이 되도록 하는 {qty}를 구하시오."
            if v in _nums(q) or v < 2:
                continue
            out[f"{c}_{kk}"] = {"STMT": stmt, "QTY": qty, "DCOND": dcond, "RANGE": rng_, "V": v, "LAW": law, "C": c}
    return out


LG2_ROWS = _lg2_rows()


def lg_t2():
    return T(LG, 2, LG_B, title="'모든'·'어떤' 명제가 참일 조건 — 이차식의 판별식",
        skill="'모든 x에 대해 f(x) > 0' ⇔ D < 0, '어떤 x에 대해 f(x) < 0' ⇔ D > 0으로 옮겨 정수 k 세기", axis={"상수항": "2~40", "명제": "모든(>, ≥) / 어떤(<)", "계수": "2kx / kx"}, disc="'모든'은 판별식 음수, '어떤'은 판별식 양수임을 알고 k의 정수 범위를 정확히 세는가", diff=3,
        params=[{"name": "f", "values": {"in": list(LG2_ROWS)}}], table={"key": "f", "rows": LG2_ROWS},
        derive={"ans": "V"}, cost=["C", "ans"], verify=["ans == V"],
        q="명제 '{STMT}이다.'가 참이 되도록 하는 {QTY}를 구하시오.", answer="{ans}",
        sol1="x²의 계수가 양수인 이차식이 모든 실수 x에서 양수이려면 그래프가 x축과 만나지 않아야 하므로 판별식이 음수(≥ 0이면 D ≤ 0)이고, 어떤 실수 x에서 음수이려면 x축과 두 점에서 만나야 하므로 판별식이 양수이다. 여기서는 {LAW}.",
        sol2=[("{LAW}: {DCOND}", "명제 → 판별식"), ("{RANGE}", "k의 범위"), ("{QTY} = {ans}", None, ("{ans}", "답"))],
        sol3=["경계의 k 값을 넣어 판별식의 부호가 바뀌는지 확인하면 범위의 끝을 잘못 세지 않았는지 알 수 있다. 따라서 {QTY}는 {ans}이다.", "{DCOND}", "답 {ans}"],
        model="{LAW}이어야 하므로 {DCOND}, 즉 {RANGE}이다. 따라서 {QTY}는 {ans}이다.",
        rubric=[("판별식 조건", 3, "판별식 조건으로 {DCOND} 꼴의 부등식을 세웠다.", "'모든'과 '어떤'의 부호를 바꿨으면 인정하지 않는다."), ("k 세기", 2, "{ans}{eul(ans)} 구했다.", "경계를 잘못 넣거나 빼면 1점.")],
        pitfalls=[("'어떤'에 D < 0을 씀", "판별식 조건", "불인정"), ("2kx의 판별식에서 D/4 = k² − c 대신 4k² − c로 계산 실수", "판별식 조건", "부분"), ("정수 개수에 경계 포함 여부 실수", "k 세기", "부분")])


def lg_t3():
    return T(LG, 3, LG_B, title="충분조건·필요조건이 되도록 하는 k — 절댓값 부등식과 구간",
        skill="p ⇒ q는 P ⊂ Q(충분), q ⇒ p는 Q ⊂ P(필요)로 옮겨 구간의 포함 관계로 k의 범위 정하기", axis={"p": "|x − a| ≤ k (a: ±1~±4)", "q": "구간 lo ≤ x ≤ hi", "조건": "충분 / 필요"}, disc="충분조건은 P가 Q 안에, 필요조건은 Q가 P 안에 들어가도록 두 끝을 모두 비교하는가", diff=3,
        params=[{"name": "a", "values": {"in": NZ(-4, 4)}}, {"name": "d1", "values": {"int": [1, 6]}}, {"name": "d2", "values": {"int": [1, 6]}}, {"name": "k", "values": {"in": ["suf", "nec"]}}],
        table={"key": "k", "rows": {"suf": {"COND": "충분", "EXT": "최댓값", "REL": "P ⊂ Q", "LAW": "p ⇒ q, 즉 P ⊂ Q이므로 P의 양 끝이 Q 안에 있어야 한다", "w": 1},
                                    "nec": {"COND": "필요", "EXT": "최솟값", "REL": "Q ⊂ P", "LAW": "q ⇒ p, 즉 Q ⊂ P이므로 Q의 양 끝이 P 안에 있어야 한다", "w": 0}}},
        derive={"na": "-a", "lo": "a - d1", "hi": "a + d2", "mn": "min(d1, d2)", "mx": "max(d1, d2)", "ans": "w*min(d1, d2) + (1 - w)*max(d1, d2)"},
        constraints=["d1 != d2", "ans not in (a, lo, hi, -a, -lo, -hi)"], cost=["a", "lo", "hi", "d1", "d2", "ans"], verify=["lo == a - d1", "hi == a + d2"],
        q="실수 x에 대한 두 조건 p: [[abs(x {sgn(na)})]] ≤ k, q: {lo} ≤ x ≤ {hi}에 대하여 p가 q이기 위한 {COND}조건이 되도록 하는 자연수 k의 {EXT}을 구하시오.", answer="{ans}",
        sol1="p의 진리집합은 P: {a} − k ≤ x ≤ {a} + k(중심 {a}, 반지름 k), q의 진리집합은 Q: {lo} ≤ x ≤ {hi}이다. {LAW}. 중심 {a}에서 Q의 양 끝까지의 거리는 각각 {d1}, {d2}이다.",
        sol2=[("P: {a} − k ≤ x ≤ {a} + k, Q: {lo} ≤ x ≤ {hi}", "진리집합"), ("{REL}: 중심 {a}에서 양 끝까지 거리 {d1}, {d2}와 k 비교", "{COND}조건"), ("k의 {EXT} = {ans}", None, ("{ans}", "k"))],
        sol3=["k = {ans}일 때 P: {a - ans} ≤ x ≤ {a + ans}{ika(a + ans)} 되어 {REL}{ika(REL)} 성립하고, {EXT}에서 1만큼 벗어나면 성립하지 않는다. 따라서 k의 {EXT}은 {ans}이다.", "k = {ans}: P = [{a - ans}, {a + ans}]", "{EXT} {ans}"],
        model="P: {a} − k ≤ x ≤ {a} + k, Q: {lo} ≤ x ≤ {hi}이고 {LAW}. 중심 {a}에서 양 끝까지의 거리가 {d1}, {d2}이므로 k의 {EXT}은 {ans}이다.",
        rubric=[("포함 관계", 3, "{REL}{ro(REL)} 옮겨 양 끝의 거리 {d1}, {d2}와 k를 비교했다.", "충분·필요를 반대로 두었으면 인정하지 않는다."), ("k 구하기", 2, "k의 {EXT} {ans}{eul(ans)} 구했다.", "한쪽 끝만 비교했으면 1점.")],
        pitfalls=[("충분조건을 Q ⊂ P로 둠", "포함 관계", "불인정"), ("절댓값 부등식을 한쪽 부등식으로만 풂", "포함 관계", "부분"), ("한쪽 끝만 비교", "k 구하기", "부분")])


def _lg4_rows():
    out = {}
    # (1) Ax + B/x
    for A in range(1, 13):
        for B in range(1, 61):
            s = math.isqrt(A * B)
            if s * s != A * B:
                continue
            v = 2 * s
            expr = f"{'' if A == 1 else A}x + [[frac({B}, x)]]"
            g = math.gcd(s, A); xe = f"[[frac({s // g},{A // g})]]" if s % A else str(s // A)
            q = f"x > 0일 때, {expr}의 최솟값"
            if v in _nums(q):
                continue
            out[f"a{A}_{B}"] = {"COND": "x > 0", "EXPR": expr, "V": v, "AM": f"{expr} ≥ 2[[sqrt({A * B})]] = {v}", "EQ": f"{'' if A == 1 else A}x = [[frac({B}, x)]], 즉 x = {xe}", "TERMS": f"{'' if A == 1 else A}x와 [[frac({B}, x)]]", "PROD": f"{A * B}"}
    # (2) x + B/(x − p)  (x > p)
    for p in range(1, 9):
        for B in (1, 4, 9, 16, 25, 36, 49):
            s = math.isqrt(B)
            v = p + 2 * s
            expr = f"x + [[frac({B}, x − {p})]]"
            q = f"x > {p}일 때, {expr}의 최솟값"
            if v in _nums(q):
                continue
            out[f"p{p}_{B}"] = {"COND": f"x > {p}", "EXPR": expr, "V": v, "AM": f"(x − {p}) + [[frac({B}, x − {p})]] + {p} ≥ 2[[sqrt({B})]] + {p} = {v}", "EQ": f"x − {p} = [[frac({B}, x − {p})]], 즉 x = {p + s}", "TERMS": f"x − {p}{_wa(p)} [[frac({B}, x − {p})]]", "PROD": f"{B}"}
    # (3) (x + a)(x + b)/x
    for a in range(1, 10):
        for b in range(a, 19):
            s = math.isqrt(a * b)
            if s * s != a * b:
                continue
            v = a + b + 2 * s
            expr = f"[[frac((x + {a})(x + {b}), x)]]"
            q = f"x > 0일 때, {expr}의 최솟값"
            if v in _nums(q):
                continue
            out[f"q{a}_{b}"] = {"COND": "x > 0", "EXPR": expr, "V": v, "AM": f"x + [[frac({a * b}, x)]] + {a + b} ≥ 2[[sqrt({a * b})]] + {a + b} = {v}", "EQ": f"x = [[frac({a * b}, x)]], 즉 x = {s}", "TERMS": f"x와 [[frac({a * b}, x)]]", "PROD": f"{a * b}"}
    return out


LG4_ROWS = _lg4_rows()


def lg_t4():
    return T(LG, 4, LG_B, title="산술평균과 기하평균 — 한 변수 식의 최솟값",
        skill="양수 a, b에 대해 a + b ≥ 2√(ab)(등호는 a = b)를 곱이 상수가 되는 두 항에 적용하기", axis={"식": "Ax + B/x, x + B/(x − p), (x + a)(x + b)/x", "조건": "x > 0 또는 x > p"}, disc="곱이 상수가 되도록 항을 짝짓고, 등호 성립 조건을 확인하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(LG4_ROWS)}}], table={"key": "f", "rows": LG4_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="{COND}일 때, {EXPR}의 최솟값을 구하시오.", answer="{ans}",
        sol1="두 양수의 합은 기하평균의 2배 이상이다: a + b ≥ 2√(ab), 등호는 a = b일 때. 곱이 상수가 되는 두 항 {TERMS}에 적용한다(곱 = {PROD}).",
        sol2=[("{TERMS}는 모두 양수이고 곱이 {PROD}", "짝짓기"), ("{AM}", "산술·기하평균"), ("등호: {EQ} → 최솟값 {ans}", None, ("{ans}", "최솟값"))],
        sol3=["등호 조건 {EQ}에서 x가 조건 범위 안에 있으므로 최솟값 {ans}{ika(ans)} 실제로 얻어진다. 따라서 최솟값은 {ans}이다.", "등호: {EQ}", "최솟값 {ans}"],
        model="{TERMS}에 산술평균과 기하평균의 관계를 쓰면 {AM}이고 등호는 {EQ}일 때 성립하므로 최솟값은 {ans}이다.",
        rubric=[("부등식 적용", 3, "{AM}{eul(ans)} 얻었다.", "곱이 상수가 아닌 항에 적용했으면 인정하지 않는다."), ("등호 조건", 2, "{EQ}{ro(EQ)} 등호 조건을 밝혔다.", "등호 조건이 없으면 1점.")],
        pitfalls=[("곱이 상수가 아닌 항에 산술기하 적용", "부등식 적용", "불인정"), ("상수항을 옮기지 않고 적용", "부등식 적용", "부분"), ("등호 성립 조건 생략", "등호 조건", "부분")])


def _lg5_rows():
    out = {}
    # (1) xy = c, Ax + By min
    for A in range(1, 5):
        for B in range(1, 5):
            for c in range(1, 37):
                s = math.isqrt(A * B * c)
                if s * s != A * B * c or s < 2:
                    continue
                v = 2 * s
                expr = f"{'' if A == 1 else A}x + {'' if B == 1 else B}y"
                q = f"x > 0, y > 0이고 xy = {c}일 때, {expr}의 최솟값"
                if v in _nums(q):
                    continue
                out[f"m{A}_{B}_{c}"] = {"COND": f"xy = {c}", "ASK": f"{expr}의 최솟값", "V": v, "AM": f"{expr} ≥ 2√({'' if A * B == 1 else A * B}xy) = 2[[sqrt({A * B * c})]] = {v}", "EQ": f"{'' if A == 1 else A}x = {'' if B == 1 else B}y", "TERMS": f"{'' if A == 1 else A}x와 {'' if B == 1 else B}y", "LAW": "합 ≥ 2√(곱)"}
    # (2) x + y = s, xy max
    for s in range(4, 31, 2):
        v = (s // 2) ** 2
        q = f"x > 0, y > 0이고 x + y = {s}일 때, xy의 최댓값"
        if v in _nums(q):
            continue
        out[f"s{s}"] = {"COND": f"x + y = {s}", "ASK": "xy의 최댓값", "V": v, "AM": f"{s} = x + y ≥ 2√(xy), 즉 √(xy) ≤ {s // 2}, xy ≤ {v}", "EQ": f"x = y = {s // 2}", "TERMS": "x와 y", "LAW": "합 ≥ 2√(곱) → 곱 ≤ (합/2)²"}
    # (3) Ax + By = s, xy max  (AB 제곱수)
    for A in range(1, 10):
        for B in range(1, 10):
            r = math.isqrt(A * B)
            if r * r != A * B or (A, B) == (1, 1):
                continue
            for k in range(1, 7):
                s = 2 * k * r
                v = k * k
                expr = f"{'' if A == 1 else A}x + {'' if B == 1 else B}y"
                q = f"x > 0, y > 0이고 {expr} = {s}일 때, xy의 최댓값"
                if v in _nums(q) or v < 2:
                    continue
                out[f"l{A}_{B}_{k}"] = {"COND": f"{expr} = {s}", "ASK": "xy의 최댓값", "V": v, "AM": f"{s} = {expr} ≥ 2√({A * B}xy) = {2 * r}√(xy), 즉 √(xy) ≤ {k}, xy ≤ {v}", "EQ": f"{'' if A == 1 else A}x = {'' if B == 1 else B}y = {k * r}", "TERMS": f"{'' if A == 1 else A}x와 {'' if B == 1 else B}y", "LAW": "합 ≥ 2√(곱) → 곱 ≤ (합/2)²"}
    # (4) a/x + b/y = 1 → x + y min = (√a + √b)²
    for a in (1, 4, 9):
        for b in (1, 4, 9, 16):
            if a > b:
                continue
            ra, rb = math.isqrt(a), math.isqrt(b)
            v = (ra + rb) ** 2
            fa = "[[frac(1, x)]]" if a == 1 else f"[[frac({a}, x)]]"
            fb = "[[frac(1, y)]]" if b == 1 else f"[[frac({b}, y)]]"
            ta = "[[frac(y, x)]]" if a == 1 else f"[[frac({a}y, x)]]"
            tb = "[[frac(x, y)]]" if b == 1 else f"[[frac({b}x, y)]]"
            q = f"x > 0, y > 0이고 {fa} + {fb} = 1일 때, x + y의 최솟값"
            if v in _nums(q):
                continue
            eq = f"{ta} = {tb}, 즉 " + (f"y = {'' if rb == 1 else rb}x" if ra == 1 else f"{ra}y = {rb}x")
            out[f"h{a}_{b}"] = {"COND": f"{fa} + {fb} = 1", "ASK": "x + y의 최솟값", "V": v, "AM": f"x + y = (x + y)({fa} + {fb}) = {a} + {b} + {ta} + {tb} ≥ {a + b} + 2[[sqrt({a * b})]] = {v}", "EQ": eq, "TERMS": f"{ta}와 {tb}", "LAW": "1을 곱해 전개한 뒤 합 ≥ 2√(곱)"}
    return out


LG5_ROWS = _lg5_rows()


def lg_t5():
    return T(LG, 5, LG_B, title="산술평균과 기하평균 — 두 변수의 합·곱의 최대·최소",
        skill="xy가 일정하면 합의 최솟값, 합이 일정하면 곱의 최댓값을 a + b ≥ 2√(ab)로 구하기", axis={"조건": "xy = c / x + y = s / Ax + By = s / 1/x + b/y = 1", "묻는 것": "합의 최솟값 / 곱의 최댓값"}, disc="일정한 것(합·곱)을 판단해 부등식을 알맞은 방향으로 쓰고 등호 조건을 확인하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(LG5_ROWS)}}], table={"key": "f", "rows": LG5_ROWS},
        derive={"ans": "V"}, cost=["ans"], verify=["ans == V"],
        q="x > 0, y > 0이고 {COND}일 때, {ASK}을 구하시오.", answer="{ans}",
        sol1="양수 a, b에 대하여 a + b ≥ 2√(ab)(등호는 a = b)이다. 곱이 일정하면 합의 최솟값이, 합이 일정하면 곱의 최댓값이 나온다. 여기서는 {LAW}.",
        sol2=[("{TERMS}에 산술·기하평균 적용", "짝짓기"), ("{AM}", "부등식"), ("등호: {EQ} → {ASK} {ans}", None, ("{ans}", "답"))],
        sol3=["등호 조건 {EQ}{ro(EQ)} 잡은 x, y가 주어진 조건을 만족하므로 {ans}{ika(ans)} 실제로 얻어진다. 따라서 {ASK}은 {ans}이다.", "등호: {EQ}", "답 {ans}"],
        model="{TERMS}에 산술평균과 기하평균의 관계를 쓰면 {AM}이고, 등호는 {EQ}일 때 성립한다. 따라서 {ASK}은 {ans}이다.",
        rubric=[("부등식 적용", 3, "{AM}{eul(ans)} 얻었다.", "부등식 방향이 반대면 인정하지 않는다."), ("등호 조건", 2, "{EQ}{ro(EQ)} 등호 조건을 밝혔다.", "등호 조건이 없으면 1점.")],
        pitfalls=[("합이 일정한데 합의 최솟값을 구함(방향 혼동)", "부등식 적용", "불인정"), ("계수를 곱 안에 넣지 않음", "부등식 적용", "부분"), ("등호 조건 생략", "등호 조건", "부분")])


LG_SEED = SEED(LG, category="대수", title="명제 — 진리집합·'모든/어떤' 명제와 판별식·충분필요조건 k·산술기하평균(1변수·2변수)", unit_id="h1-2", concept_ids=["h1-2-11", "h1-2-12", "h1-2-13", "h1-2-14", "h1-2-15"],
               schema_name="명제와 절대부등식", note="역·대우·귀류법(12·14)은 수치 답 틀이 어려워 진리집합·조건 k 틀에 포함 관계로 녹였다. 산술기하는 곱이 제곱수인 행만 생성.",
               templates=[lg_t1(), lg_t2(), lg_t3(), lg_t4(), lg_t5()])


# ═══════════════════════════════════════════════════════════════════ 3. 함수
FN = "h1-2-func"
FN_B = {**HS, "prereq": ["일차함수", "연립방정식"], "ops": ["함수"], "traps": ["합성 순서", "역함수 = 1/f 오해"], "tags": ["함수", "합성함수", "역함수"]}


def fn_t1():
    return T(FN, 1, FN_B, title="일차함수의 함숫값 — 두 값으로 f(x) 결정",
        skill="f(x) = ax + b에 두 함숫값을 넣어 연립방정식으로 a, b를 정한 뒤 다른 함숫값 구하기", axis={"기울기": "±1~±4", "x": "−4~6"}, disc="두 조건으로 a, b를 정하는 연립방정식을 세우고 푸는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-4, 4)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "x1", "values": {"in": NZ(-3, 4)}}, {"name": "x2", "values": {"in": NZ(-2, 6)}}, {"name": "x3", "values": {"int": [-4, 8]}}],
        derive={"v1": "a*x1 + b", "v2": "a*x2 + b", "ans": "a*x3 + b", "dx": "x2 - x1", "dv": "a*x2 - a*x1"},
        constraints=["x1 < x2", "x3 != x1", "x3 != x2", "ans != 0", "ans not in (x1, x2, x3, v1, v2)", "v1 != v2"], cost=["a", "b", "x1", "x2", "x3", "v1", "v2", "ans"], verify=["dv == a*dx", "v1 == a*x1 + b"],
        q="함수 f(x) = ax + b에 대하여 f({x1}) = {v1}, f({x2}) = {v2}일 때, f({x3})의 값을 구하시오. (단, a, b는 상수이다.)", answer="{ans}",
        sol1="f({x1}) = {v1}, f({x2}) = {v2}를 f(x) = ax + b에 넣으면 a, b에 대한 연립방정식 {co(x1)}a + b = {v1}, {co(x2)}a + b = {v2}{ika(v2)} 된다. 두 식을 빼면 a가, 대입하면 b가 나온다.",
        sol2=[("{co(x1)}a + b = {v1}, {co(x2)}a + b = {v2}", "함숫값 대입"), ("빼면 {co(dx)}a = {dv} → a = {a}, b = {b}", "연립방정식"), ("f({x3}) = {a} × {pn(x3)} {sgn(b)} = {ans}", None, ("{ans}", "f({x3})"))],
        sol3=["f(x) = {co(a)}x {sgn(b)}에 x = {x1}, {x2}를 넣으면 {v1}, {v2}{ika(v2)} 되어 조건과 맞는다. 따라서 f({x3}) = {ans}이다.", "f(x) = {co(a)}x {sgn(b)}", "f({x3}) = {ans}"],
        model="{co(x1)}a + b = {v1}, {co(x2)}a + b = {v2}에서 a = {a}, b = {b}이므로 f(x) = {co(a)}x {sgn(b)}이고 f({x3}) = {ans}이다.",
        rubric=[("a, b 구하기", 3, "a = {a}, b = {b}{eul(b)} 구했다.", "둘 중 하나만 맞으면 1점."), ("함숫값", 2, "f({x3}) = {ans}{eul(ans)} 구했다.", "대입 실수면 1점.")],
        pitfalls=[("연립방정식에서 뺄 때 부호 실수", "a, b 구하기", "부분"), ("a와 b를 바꿔 씀", "a, b 구하기", "불인정"), ("대입 계산 실수", "함숫값", "부분")])


def fn_t2():
    return T(FN, 2, FN_B, title="합성함수의 함숫값 — (f∘g)(k), (g∘f)(k), (f∘f)(k)",
        skill="(f∘g)(k) = f(g(k))이므로 안쪽 함수의 값을 먼저 구해 바깥 함수에 넣기", axis={"f": "ax + b", "g": "x² + c", "합성": "f∘g / g∘f / f∘f", "k": "−3~4"}, disc="합성 순서(오른쪽 함수를 먼저 적용)를 지키는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-3, 3)}}, {"name": "b", "values": {"in": NZ(-5, 5)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "k", "values": {"in": NZ(-3, 4)}}, {"name": "m", "values": {"in": ["fg", "gf", "ff"]}}],
        table={"key": "m", "rows": {"fg": {"ASK": "(f∘g)", "INNER": "g", "OUTER": "f", "ORDER": "g를 먼저, f를 나중에", "w1": 1, "w2": 0, "w3": 0},
                                    "gf": {"ASK": "(g∘f)", "INNER": "f", "OUTER": "g", "ORDER": "f를 먼저, g를 나중에", "w1": 0, "w2": 1, "w3": 0},
                                    "ff": {"ASK": "(f∘f)", "INNER": "f", "OUTER": "f", "ORDER": "f를 두 번", "w1": 0, "w2": 0, "w3": 1}}},
        derive={"inner": "w1*(k*k + c) + (1 - w1)*(a*k + b)", "ans": "w1*(a*(k*k + c) + b) + w2*((a*k + b)**2 + c) + w3*(a*(a*k + b) + b)"},
        constraints=["ans != 0", "ans not in (a, b, c, k, inner)", "inner != 0", "inner != k"], cost=["a", "b", "c", "k", "inner", "ans"], verify=["w1 == 0 or inner == k*k + c", "w1 == 1 or inner == a*k + b"],
        q="두 함수 f(x) = {co(a)}x {sgn(b)}, g(x) = x² {sgn(c)}에 대하여 {ASK}({k})의 값을 구하시오.", answer="{ans}",
        sol1="{ASK}({k}) = {OUTER}({INNER}({k}))이다 — {ORDER} 적용한다. 안쪽 {INNER}({k})의 값을 먼저 구하고 그 값을 {OUTER}에 넣는다.",
        sol2=[("{ASK}({k}) = {OUTER}({INNER}({k}))", "합성의 뜻"), ("{INNER}({k}) = {inner}", "안쪽 함숫값"), ("{OUTER}({inner}) = {ans}", None, ("{ans}", "{ASK}({k})"))],
        sol3=["합성 순서를 바꾸면 값이 달라지므로 {ORDER} 적용했는지 확인한다. 따라서 {ASK}({k}) = {ans}이다.", "{INNER}({k}) = {inner} → {OUTER}({inner})", "{ASK}({k}) = {ans}"],
        model="{ASK}({k}) = {OUTER}({INNER}({k}))이고 {INNER}({k}) = {inner}이므로 {OUTER}({inner}) = {ans}이다.",
        rubric=[("합성 순서", 3, "{INNER}({k}) = {inner}{eul(inner)} 먼저 구했다.", "순서를 바꿨으면 인정하지 않는다."), ("함숫값", 2, "{ans}{eul(ans)} 구했다.", "대입 계산 실수면 1점.")],
        pitfalls=[("(f∘g)(k)를 g(f(k))로 계산", "합성 순서", "불인정"), ("f(x)g(x)의 곱으로 계산", "합성 순서", "불인정"), ("제곱·부호 계산 실수", "함숫값", "부분")])


def fn_t3():
    return T(FN, 3, FN_B, title="역함수의 함숫값 — f⁻¹(k)",
        skill="f⁻¹(k) = m ⇔ f(m) = k이므로 방정식 f(x) = k를 풀어 역함수의 값 구하기", axis={"f": "ax + b (a: ±1~±4)", "k": "함숫값"}, disc="역함수의 값을 구할 때 역함수 식을 구하지 않고도 f(x) = k를 풀면 됨을 아는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-4, 4)}}, {"name": "b", "values": {"in": NZ(-7, 7)}}, {"name": "x0", "values": {"in": NZ(-6, 6)}}],
        derive={"k": "a*x0 + b", "ans": "x0", "nb": "-b"},
        constraints=["k != 0", "ans not in (a, b, k)", "k != x0"], cost=["a", "b", "k", "ans"], verify=["a*ans + b == k"],
        q="함수 f(x) = {co(a)}x {sgn(b)}에 대하여 f⁻¹({k})의 값을 구하시오.", answer="{ans}",
        sol1="f⁻¹({k}) = m이라 하면 역함수의 뜻에서 f(m) = {k}이다. 즉 {co(a)}m {sgn(b)} = {k}{eul(k)} 풀면 된다.",
        sol2=[("f⁻¹({k}) = m ⇔ f(m) = {k}", "역함수의 뜻"), ("{co(a)}m {sgn(b)} = {k} → {co(a)}m = {k - b}", "방정식"), ("m = {ans}", None, ("{ans}", "f⁻¹({k})"))],
        sol3=["f({ans}) = {a} × {pn(ans)} {sgn(b)} = {k}{ika(k)} 되어 f⁻¹({k}) = {ans}{ika(ans)} 맞다.", "f({ans}) = {k} ✓", "f⁻¹({k}) = {ans}"],
        model="f⁻¹({k}) = m이라 하면 f(m) = {k}이므로 {co(a)}m {sgn(b)} = {k}, m = {ans}이다.",
        rubric=[("역함수의 뜻", 3, "f(m) = {k}{ro(k)} 바꿔 세웠다.", "f⁻¹을 1/f로 두었으면 인정하지 않는다."), ("계산", 2, "m = {ans}{eul(ans)} 구했다.", "이항·나눗셈 실수면 1점.")],
        pitfalls=[("f⁻¹(k)를 1/f(k)로 계산", "역함수의 뜻", "불인정"), ("f(k)를 구함", "역함수의 뜻", "불인정"), ("이항 부호 실수", "계산", "부분")])


def fn_t4():
    return T(FN, 4, FN_B, title="합성함수의 역함수의 값 — (f∘g)⁻¹(k)",
        skill="(f∘g)⁻¹(k) = m ⇔ (f∘g)(m) = k이므로 합성함수의 식을 만들어 방정식 풀기", axis={"f": "ax + b", "g": "x + c", "합성": "f∘g / g∘f"}, disc="합성의 역함수 값을 '합성 = k'의 방정식으로 바꾸고, 합성 순서를 지키는가", diff=3,
        params=[{"name": "a", "values": {"in": NZ(-3, 3)}}, {"name": "b", "values": {"in": NZ(-5, 5)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "x0", "values": {"in": NZ(-5, 5)}}, {"name": "m", "values": {"in": ["fg", "gf"]}}],
        table={"key": "m", "rows": {"fg": {"ASK": "(f∘g)⁻¹", "COMP": "(f∘g)(x) = f(g(x)) = f(x + c)", "w": 1}, "gf": {"ASK": "(g∘f)⁻¹", "COMP": "(g∘f)(x) = g(f(x)) = f(x) + c", "w": 0}}},
        derive={"k": "w*(a*(x0 + c) + b) + (1 - w)*(a*x0 + b + c)", "ans": "x0", "cc": "w*(a*c + b) + (1 - w)*(b + c)"},
        constraints=["k != 0", "ans not in (a, b, c, k)", "a != 1", "cc != 0"], cost=["a", "b", "c", "k", "ans"], verify=["w == 0 or a*(ans + c) + b == k", "w == 1 or a*ans + b + c == k"],
        q="두 함수 f(x) = {co(a)}x {sgn(b)}, g(x) = x {sgn(c)}에 대하여 {ASK}({k})의 값을 구하시오.", answer="{ans}",
        sol1="{ASK}({k}) = m이라 하면 역함수의 뜻에서 합성함수의 값이 {k}인 m을 찾으면 된다. 합성함수의 식은 {COMP} = {co(a)}x {sgn(cc)}이다.",
        sol2=[("{ASK}({k}) = m ⇔ (합성함수)(m) = {k}", "역함수의 뜻"), ("합성: {COMP} = {co(a)}x {sgn(cc)}", "합성함수의 식"), ("{co(a)}m {sgn(cc)} = {k} → m = {ans}", None, ("{ans}", "m"))],
        sol3=["m = {ans}{eul(ans)} 합성함수에 넣으면 {a} × {pn(ans)} {sgn(cc)} = {k}{ika(k)} 되어 맞다. 따라서 {ASK}({k}) = {ans}이다.", "합성함수({ans}) = {k} ✓", "{ASK}({k}) = {ans}"],
        model="{COMP} = {co(a)}x {sgn(cc)}이므로 {ASK}({k}) = m은 {co(a)}m {sgn(cc)} = {k}의 해 m = {ans}이다.",
        rubric=[("합성함수의 식", 3, "{COMP} = {co(a)}x {sgn(cc)}{eul(cc)} 구했다.", "합성 순서를 바꿨으면 인정하지 않는다."), ("역함수 값", 2, "m = {ans}{eul(ans)} 구했다.", "방정식 풀이 실수면 1점.")],
        pitfalls=[("합성 순서를 바꿈", "합성함수의 식", "불인정"), ("(f∘g)⁻¹을 f⁻¹∘g⁻¹로 계산", "합성함수의 식", "불인정"), ("방정식 풀이 실수", "역함수 값", "부분")])


def _fn5_rows():
    out = {}
    letters = "abcdefgh"
    for m in range(2, 7):
        X = list(range(1, m + 1))
        for n in range(2, 9):
            Y = list(letters[:n])
            kinds = [("all", f"X에서 Y로의 함수의 개수", n ** m, f"X의 원소 {m}개가 각각 Y의 원소 {n}개 중 하나를 택하므로 [[pow({n},{m})]]", f"[[pow({n},{m})]]"),
                     ("const", f"X에서 Y로의 상수함수의 개수", n, f"함숫값 하나를 Y의 원소 {n}개 중에서 고르므로 {n}", f"{n}"),
                     ("fix", f"X에서 Y로의 함수 f 중 f(1) = a인 함수의 개수", n ** (m - 1), f"f(1) = a로 정해졌고 나머지 원소 {m - 1}개가 각각 Y의 원소 {n}개 중 하나를 택하므로 [[pow({n},{m - 1})]]", f"[[pow({n},{m - 1})]]"),
                     ("nfix", f"X에서 Y로의 함수 f 중 f(1) ≠ a인 함수의 개수", (n - 1) * n ** (m - 1), f"f(1)은 a를 뺀 {n - 1}가지, 나머지 원소 {m - 1}개는 각각 {n}가지이므로 {n - 1} × [[pow({n},{m - 1})]]", f"{n - 1} × [[pow({n},{m - 1})]]")]
            if n >= m:
                kinds.append(("inj", f"X에서 Y로의 일대일함수의 개수", math.perm(n, m), f"X의 원소 {m}개가 서로 다른 함숫값을 가지므로 [[perm({n},{m})]]", f"[[perm({n},{m})]] = {' × '.join(str(n - i) for i in range(m))}" if n > m else f"[[perm({n},{m})]] = {n}!"))
            for kk, desc, v, expl, form in kinds:
                q = f"두 집합 X = {_setm(X)}, Y = {_setm(Y)}에 대하여 {desc}를 구하시오."
                if v in _nums(q) or v < 2:
                    continue
                out[f"{m}_{n}_{kk}"] = {"SETX": ", ".join(map(str, X)), "SETY": ", ".join(Y), "DESC": desc, "V": v, "EXPL": expl, "FORM": form, "NX": m, "NY": n}
        if m >= 3:
            v = math.factorial(m)
            out[f"{m}_bij"] = {"SETX": ", ".join(map(str, X)), "SETY": ", ".join(map(str, X)), "DESC": "X에서 X로의 일대일대응의 개수", "V": v, "EXPL": f"X의 원소 {m}개를 자기 자신의 원소에 빠짐없이 하나씩 짝지으므로 {m}! = {' × '.join(str(m - i) for i in range(m))} = {v}", "FORM": f"{m}!", "NX": m, "NY": m}
    return out


FN5_ROWS = _fn5_rows()


def fn_t5():
    return T(FN, 5, FN_B, title="함수의 개수 — 함수·상수함수·일대일함수·일대일대응",
        skill="정의역의 각 원소가 택할 수 있는 함숫값의 가짓수를 곱해 함수의 개수 세기", axis={"X": "원소 2~6개", "Y": "원소 2~8개", "종류": "함수 / 상수함수 / f(1) = a 고정·제외 / 일대일함수 / 일대일대응"}, disc="함수는 nᵐ, 일대일함수는 nPm, 일대일대응은 m!임을 정의에서 이끌어내는가", diff=2,
        params=[{"name": "f", "values": {"in": list(FN5_ROWS)}}], table={"key": "f", "rows": FN5_ROWS},
        derive={"ans": "V"}, cost=["NX", "NY", "ans"], verify=["ans == V"],
        q="두 집합 X = [[set({SETX})]], Y = [[set({SETY})]]에 대하여 {DESC}를 구하시오.", answer="{ans}",
        sol1="함수는 정의역의 각 원소에 공역의 원소를 하나씩 대응시키는 것이다. 정의역 X의 원소 {NX}개마다 택할 수 있는 함숫값의 가짓수를 곱하면 함수의 개수가 된다. 일대일함수는 함숫값이 서로 달라야 하므로 가짓수가 하나씩 줄고, 일대일대응은 공역 전체를 빠짐없이 쓴다.",
        sol2=[("n(X) = {NX}, n(Y) = {NY}", "원소의 개수"), ("{EXPL}", "가짓수 곱하기"), ("{FORM} = {ans}", None, ("{ans}", "개수"))],
        sol3=["함수 하나를 실제로 적어 보면 정의역의 원소마다 함숫값을 하나씩 고르는 과정과 같음을 알 수 있다. 따라서 {DESC}는 {ans}이다.", "{FORM}", "답 {ans}"],
        model="{EXPL}이므로 {FORM} = {ans}이다.",
        rubric=[("가짓수 세기", 3, "{FORM}{ro(FORM)} 세웠다.", "함수와 일대일함수를 혼동했으면 인정하지 않는다."), ("계산", 2, "{ans}{eul(ans)} 구했다.", "곱셈 실수면 1점.")],
        pitfalls=[("함수의 개수를 mⁿ으로 셈(지수·밑 바꿈)", "가짓수 세기", "불인정"), ("일대일함수를 nᵐ으로 셈", "가짓수 세기", "불인정"), ("곱셈 실수", "계산", "부분")])


FN_SEED = SEED(FN, category="함수", title="함수 — 일차함수 값·합성함수 값·역함수 값·합성의 역함수·함수의 개수", unit_id="h1-2", concept_ids=["h1-2-16", "h1-2-17", "h1-2-18"],
               schema_name="함수·합성함수·역함수", note="역함수 값은 f(m) = k 방정식으로. 함수의 개수 행은 파이썬에서 nᵐ·nPm·m! 계산.",
               templates=[fn_t1(), fn_t2(), fn_t3(), fn_t4(), fn_t5()])


# ═══════════════════════════════════════════════════════════════════ 4. 유리함수·무리함수
RF = "h1-2-ratfn"
RF_B = {**HS, "prereq": ["평행이동", "분수식"], "ops": ["유리함수", "무리함수"], "traps": ["점근선 부호", "정의역 부등호 방향"], "tags": ["유리함수", "무리함수"]}


def rf_t1():
    return T(RF, 1, RF_B, title="유리함수의 점근선 — 두 점근선의 교점",
        skill="y = (ax + b)/(x + c)를 y = k/(x + c) + a 꼴로 고쳐 점근선 x = −c, y = a 읽기", axis={"a": "±1~±4", "b": "±1~±6", "c": "±1~±5", "묻는 것": "p + q / pq"}, disc="분자를 분모로 나눠 상수를 분리하면 점근선이 (−c, a)임을 아는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-4, 4)}}, {"name": "b", "values": {"in": NZ(-6, 6)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}, {"name": "m", "values": {"in": ["sum", "prod"]}}],
        table={"key": "m", "rows": {"sum": {"ASK": "p + q", "w": 1}, "prod": {"ASK": "pq", "w": 0}}},
        derive={"kk": "b - a*c", "p": "-c", "ans": "w*(a - c) + (1 - w)*(-a*c)"},
        constraints=["kk != 0", "ans != 0", "ans not in (a, b, c)"], cost=["a", "b", "c", "kk", "ans"], verify=["kk == b - a*c"],
        q="함수 y = [[frac({co(a)}x {sgn(b)}, x {sgn(c)})]]의 그래프의 두 점근선의 교점의 좌표를 (p, q)라 할 때, {ASK}의 값을 구하시오.", answer="{ans}",
        sol1="분자를 분모로 나누면 [[frac({co(a)}x {sgn(b)}, x {sgn(c)})]] = {a} + [[frac({kk}, x {sgn(c)})]]이다. 이는 y = [[frac({kk}, x)]]의 그래프를 x축 방향으로 {p}, y축 방향으로 {a}만큼 옮긴 것이므로 점근선은 x = {p}, y = {a}이다.",
        sol2=[("y = {a} + [[frac({kk}, x {sgn(c)})]]", "상수 분리"), ("점근선 x = {p}, y = {a} → 교점 ({p}, {a})", "점근선"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["분모가 0이 되는 x = {p}에서 세로 점근선, x가 커질 때 y가 가까워지는 값 {a}에서 가로 점근선이 생긴다. 따라서 {ASK} = {ans}이다.", "점근선 x = {p}, y = {a}", "{ASK} = {ans}"],
        model="y = {a} + [[frac({kk}, x {sgn(c)})]]이므로 점근선은 x = {p}, y = {a}이고 교점은 ({p}, {a})이다. 따라서 {ASK} = {ans}이다.",
        rubric=[("점근선", 3, "점근선 x = {p}, y = {a}{eul(a)} 구했다.", "부호가 반대면 1점."), ("답", 2, "{ASK} = {ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("세로 점근선을 x = c로 둠(부호 반대)", "점근선", "부분"), ("가로 점근선을 y = b로 둠", "점근선", "불인정"), ("계산 실수", "답", "부분")])


def rf_t2():
    return T(RF, 2, RF_B, title="유리함수의 평행이동 — y = k/x를 옮긴 식의 계수",
        skill="y = k/x를 x축 m, y축 n만큼 옮기면 y = k/(x − m) + n이고, 통분하면 (nx + k − mn)/(x − m)임을 쓰기", axis={"k": "±1~±6", "이동": "±1~±4"}, disc="평행이동 후 통분해 일반형의 계수를 읽는가", diff=3,
        params=[{"name": "k", "values": {"in": NZ(-6, 6)}}, {"name": "m", "values": {"in": NZ(-4, 4)}}, {"name": "n", "values": {"in": NZ(-4, 4)}}],
        derive={"a": "n", "b": "k - m*n", "c": "-m", "ans": "n + k - m*n - m"},
        constraints=["b != 0", "ans != 0", "ans not in (k, m, n)"], cost=["k", "m", "n", "a", "b", "c", "ans"], verify=["b == k - m*n", "a + b + c == ans"],
        q="함수 y = [[frac({k}, x)]]의 그래프를 x축의 방향으로 {m}만큼, y축의 방향으로 {n}만큼 평행이동한 그래프가 함수 y = [[frac(a x + b, x + c)]]의 그래프와 일치할 때, 상수 a, b, c에 대하여 a + b + c의 값을 구하시오.", answer="{ans}",
        sol1="x축 방향으로 m, y축 방향으로 n만큼 평행이동하면 x 대신 x − m, y 대신 y − n을 넣는다: y = [[frac({k}, x {sgn(c)})]] {sgn(n)}. 통분해 한 분수로 만들면 [[frac({co(a)}x {sgn(b)}, x {sgn(c)})]]이다.",
        sol2=[("y = [[frac({k}, x {sgn(c)})]] {sgn(n)}", "평행이동"), ("= [[frac({n}(x {sgn(c)}) + {pn(k)}, x {sgn(c)})]] = [[frac({co(a)}x {sgn(b)}, x {sgn(c)})]]", "통분"), ("a = {a}, b = {b}, c = {c} → a + b + c = {ans}", None, ("{ans}", "a + b + c"))],
        sol3=["옮긴 함수의 점근선은 x = {m}, y = {n}이어야 하는데 [[frac({co(a)}x {sgn(b)}, x {sgn(c)})]]의 점근선도 x = {m}, y = {a}{ro(a)} 같다. 따라서 a + b + c = {ans}이다.", "점근선 x = {m}, y = {n} ✓", "a + b + c = {ans}"],
        model="평행이동하면 y = [[frac({k}, x {sgn(c)})]] {sgn(n)} = [[frac({co(a)}x {sgn(b)}, x {sgn(c)})]]이므로 a + b + c = {ans}이다.",
        rubric=[("평행이동·통분", 3, "[[frac({co(a)}x {sgn(b)}, x {sgn(c)})]]{eul(b)} 얻었다.", "이동 방향 부호가 반대면 인정하지 않는다."), ("합", 2, "a + b + c = {ans}{eul(ans)} 구했다.", "계수를 하나 잘못 읽었으면 1점.")],
        pitfalls=[("x 대신 x + m을 넣음", "평행이동·통분", "불인정"), ("통분 없이 계수를 읽음", "평행이동·통분", "부분"), ("합 계산 실수", "합", "부분")])


def rf_t3():
    return T(RF, 3, RF_B, title="유리함수의 평행이동 (역방향) — 일반형에서 k, m, n 읽기",
        skill="y = (ax + b)/(x + c)를 a + (b − ac)/(x + c)로 고쳐 y = k/x를 어떻게 옮긴 것인지 읽기", axis={"a": "±1~±4", "c": "±1~±5", "b": "±1~±7"}, disc="분자를 분모로 나눈 나머지가 k, 점근선이 이동량임을 아는가", diff=3,
        params=[{"name": "a", "values": {"in": NZ(-4, 4)}}, {"name": "b", "values": {"in": NZ(-7, 7)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}],
        derive={"kk": "b - a*c", "m": "-c", "n": "a", "ans": "b - a*c - c + a"},
        constraints=["kk != 0", "ans != 0", "ans not in (a, b, c)"], cost=["a", "b", "c", "kk", "m", "n", "ans"], verify=["kk == b - a*c", "kk + m + n == ans"],
        q="함수 y = [[frac({co(a)}x {sgn(b)}, x {sgn(c)})]]의 그래프는 함수 y = [[frac(k, x)]]의 그래프를 x축의 방향으로 m만큼, y축의 방향으로 n만큼 평행이동한 것이다. 상수 k, m, n에 대하여 k + m + n의 값을 구하시오.", answer="{ans}",
        sol1="분자를 분모로 나누면 [[frac({co(a)}x {sgn(b)}, x {sgn(c)})]] = {a} + [[frac({kk}, x {sgn(c)})]]이다. 이는 y = [[frac({kk}, x)]]를 x축 방향으로 {m}, y축 방향으로 {n}만큼 옮긴 것이므로 k = {kk}, m = {m}, n = {n}이다.",
        sol2=[("{co(a)}x {sgn(b)} = {a}(x {sgn(c)}) {sgn(kk)}", "분자 나누기"), ("y = [[frac({kk}, x {sgn(c)})]] {sgn(a)} → k = {kk}, m = {m}, n = {n}", "이동량 읽기"), ("k + m + n = {ans}", None, ("{ans}", "k + m + n"))],
        sol3=["y = [[frac({kk}, x)]]에 x 대신 x {sgn(c)}, y 대신 y {sgn(-a)}{eul(a)} 넣어 다시 통분하면 원래 식이 나온다. 따라서 k + m + n = {ans}이다.", "역으로 통분 ✓", "k + m + n = {ans}"],
        model="[[frac({co(a)}x {sgn(b)}, x {sgn(c)})]] = {a} + [[frac({kk}, x {sgn(c)})]]이므로 k = {kk}, m = {m}, n = {n}이고 k + m + n = {ans}이다.",
        rubric=[("상수 분리", 3, "y = {a} + [[frac({kk}, x {sgn(c)})]]{ro(kk)} 고쳤다.", "나머지 k가 틀리면 1점."), ("이동량·합", 2, "k + m + n = {ans}{eul(ans)} 구했다.", "m의 부호가 반대면 1점.")],
        pitfalls=[("m = c로 둠(부호 반대)", "이동량·합", "부분"), ("k = b로 둠(나누지 않음)", "상수 분리", "불인정"), ("n을 b/c로 둠", "상수 분리", "불인정")])


def rf_t4():
    return T(RF, 4, RF_B, title="무리함수의 정의역과 치역 — y = √(ax + b) + c",
        skill="근호 안이 0 이상인 x의 범위가 정의역, 근호의 값이 0 이상이므로 y ≥ c가 치역임을 읽기", axis={"a": "±1~±3", "b": "a의 배수", "c": "±1~±5"}, disc="a < 0이면 정의역이 x ≤ −b/a로 방향이 바뀌고, 치역의 경계는 c임을 아는가", diff=2,
        params=[{"name": "s", "values": {"in": ["pos", "neg"]}}, {"name": "u", "values": {"int": [1, 3]}}, {"name": "t", "values": {"in": NZ(-5, 5)}}, {"name": "c", "values": {"in": NZ(-5, 5)}}],
        table={"key": "s", "rows": {"pos": {"DIR": "≥", "SIGN": "양수", "sa": 1}, "neg": {"DIR": "≤", "SIGN": "음수", "sa": -1}}},
        derive={"a": "sa*u", "b": "sa*u*t", "p": "-t", "ans": "-t + c"},
        constraints=["ans != 0", "ans not in (a, b, c)"], cost=["a", "b", "c", "p", "ans"], verify=["a*p + b == 0"],
        q="함수 y = [[sqrt({co(a)}x {sgn(b)})]] {sgn(c)}의 정의역이 [[setb(x, x {DIR} p)]], 치역이 [[setb(y, y ≥ q)]]일 때, 상수 p, q에 대하여 p + q의 값을 구하시오.", answer="{ans}",
        sol1="근호 안은 0 이상이어야 하므로 {co(a)}x {sgn(b)} ≥ 0, 즉 x {DIR} {p}가 정의역이다(x의 계수가 {SIGN}이므로 부등호 방향에 주의). 근호의 값은 0 이상이므로 y = [[sqrt({co(a)}x {sgn(b)})]] {sgn(c)} ≥ {c}, 치역은 y ≥ {c}이다.",
        sol2=[("{co(a)}x {sgn(b)} ≥ 0 → x {DIR} {p}", "정의역"), ("[[sqrt({co(a)}x {sgn(b)})]] ≥ 0 → y ≥ {c}", "치역"), ("p = {p}, q = {c} → p + q = {ans}", None, ("{ans}", "p + q"))],
        sol3=["x = {p}를 넣으면 근호 안이 0이 되어 y = {c}, 즉 그래프의 시작점이 ({p}, {c})이다. 따라서 p + q = {ans}이다.", "시작점 ({p}, {c})", "p + q = {ans}"],
        model="근호 안 {co(a)}x {sgn(b)} ≥ 0에서 x {DIR} {p}, 근호의 값이 0 이상이므로 y ≥ {c}이다. 따라서 p + q = {ans}이다.",
        rubric=[("정의역", 3, "x {DIR} {p}{eul(p)} 구했다.", "부등호 방향이 반대면 1점."), ("치역·답", 2, "y ≥ {c}에서 p + q = {ans}{eul(ans)} 구했다.", "치역을 y ≥ 0으로 두었으면 인정하지 않는다.")],
        pitfalls=[("a < 0일 때 부등호 방향을 바꾸지 않음", "정의역", "부분"), ("치역을 y ≥ 0으로 둠", "치역·답", "불인정"), ("정의역 경계 부호 실수", "정의역", "부분")])


def rf_t5():
    return T(RF, 5, RF_B, title="무리함수의 평행이동 — y = √(ax)를 옮긴 식의 상수",
        skill="y = √(ax)를 x축 m, y축 n만큼 옮기면 y = √(a(x − m)) + n = √(ax − am) + n임을 쓰기", axis={"a": "±1~±3", "이동": "±1~±5"}, disc="x 대신 x − m을 근호 안에 넣고 전개해 상수를 읽는가", diff=2,
        params=[{"name": "a", "values": {"in": NZ(-3, 3)}}, {"name": "m", "values": {"in": NZ(-5, 5)}}, {"name": "n", "values": {"in": NZ(-5, 5)}}],
        derive={"b": "-a*m", "c": "n", "ans": "-a*m + n", "nm": "-m"},
        constraints=["ans != 0", "ans not in (a, m, n)"], cost=["a", "m", "n", "b", "ans"], verify=["b == -a*m", "b + c == ans"],
        q="함수 y = [[sqrt({co(a)}x)]]의 그래프를 x축의 방향으로 {m}만큼, y축의 방향으로 {n}만큼 평행이동한 그래프가 함수 y = [[sqrt({co(a)}x + b)]] + c의 그래프와 일치할 때, 상수 b, c에 대하여 b + c의 값을 구하시오.", answer="{ans}",
        sol1="평행이동은 x 대신 x − m, y 대신 y − n을 넣는 것이다: y − {pn(n)} = [[sqrt({co(a)}(x {sgn(nm)}))]], 즉 y = [[sqrt({co(a)}x {sgn(b)})]] {sgn(n)}. 근호 안을 전개해 b를, 바깥 상수에서 c를 읽는다.",
        sol2=[("y = [[sqrt({co(a)}(x {sgn(nm)}))]] {sgn(n)}", "평행이동"), ("근호 안 전개: [[sqrt({co(a)}x {sgn(b)})]] {sgn(n)} → b = {b}, c = {c}", "상수 읽기"), ("b + c = {ans}", None, ("{ans}", "b + c"))],
        sol3=["옮긴 그래프의 시작점은 원래 시작점 (0, 0)을 옮긴 ({m}, {n})이어야 하는데, y = [[sqrt({co(a)}x {sgn(b)})]] {sgn(n)}의 시작점도 ({m}, {n})이다. 따라서 b + c = {ans}이다.", "시작점 ({m}, {n}) ✓", "b + c = {ans}"],
        model="평행이동하면 y = [[sqrt({co(a)}(x {sgn(nm)}))]] {sgn(n)} = [[sqrt({co(a)}x {sgn(b)})]] {sgn(n)}이므로 b = {b}, c = {c}이고 b + c = {ans}이다.",
        rubric=[("평행이동 식", 3, "y = [[sqrt({co(a)}x {sgn(b)})]] {sgn(n)}{eul(n)} 얻었다.", "x − m 대신 x + m을 넣었으면 인정하지 않는다."), ("합", 2, "b + c = {ans}{eul(ans)} 구했다.", "근호 안 전개 실수면 1점.")],
        pitfalls=[("근호 안에 x − m 대신 x + m", "평행이동 식", "불인정"), ("근호 안 전개에서 a를 곱하지 않음(b = −m)", "평행이동 식", "부분"), ("합 계산 실수", "합", "부분")])


RF_SEED = SEED(RF, category="함수", title="유리함수·무리함수 — 점근선 교점·평행이동 정/역·정의역과 치역·무리함수의 평행이동", unit_id="h1-2", concept_ids=["h1-2-19", "h1-2-20"],
               schema_name="유리함수와 무리함수", note="유리함수는 y = (ax+b)/(x+c) ↔ a + (b−ac)/(x+c) 변환. 무리함수 정의역은 a의 부호를 파라미터로 나눠 부등호 방향을 행에서 읽는다.",
               templates=[rf_t1(), rf_t2(), rf_t3(), rf_t4(), rf_t5()])


if __name__ == "__main__":
    run(ST_SEED, LG_SEED, FN_SEED, RF_SEED)
