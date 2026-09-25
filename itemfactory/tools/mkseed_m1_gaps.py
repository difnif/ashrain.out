# itemfactory/tools/mkseed_m1_gaps.py — 문항이 하나도 없던 중1 개념 9개의 시드 생성기 (v1.0 · 2026-09-21)
#
#   python itemfactory/tools/mkseed_m1_gaps.py
#     → seeds/m1-1-power.json           (m1-1-02 거듭제곱: 값·곱을 거듭제곱으로(a+b/a×b)·지수/밑 거꾸로, 3틀)
#     → seeds/m1-1-sign-number.json     (m1-1-09 양수와 음수: 부호로 나타내기·수직선 두 점·양수/음수 개수, 3틀)
#     → seeds/m1-1-int-rational.json    (m1-1-10 정수와 유리수: 분류 개수·두 수 사이의 정수 개수(사이/이상·이하), 3틀)
#     → seeds/m1-1-order.json           (m1-1-13 수의 대소 관계: 부등호로 나타내기·다섯 수의 최대−최소·−a와 −b의 차, 3틀)
#     → seeds/m1-1-ineq-sign.json       (m1-1-14 부등호의 사용: 조건을 만족하는 정수의 개수·합, 2틀)
#     → seeds/m1-1-rational-apply.json  (m1-1-18 유리수 계산의 활용: 온도 변화·수직선 거리·점수 게임, 3틀)
#     → seeds/m1-1-omit-sign.json       (m1-1-19 곱셈·나눗셈 기호의 생략: 계수 ▢·분모(문자/괄호식)·대입 ka²/(ka)²/ka+m, 6틀)
#     → seeds/m1-1-eq-property.json     (m1-1-25 등식의 성질: ax+b=c·x/a+b=c 풀기, 2틀)
#     → seeds/m1-1-graph.json           (m1-1-31 그래프: 물 높이 그래프 읽기·멈춘 시간 읽기, 2틀)
#
# 원칙: 수치는 문면에 둔다(DUP 방지) · 조건은 derive 에서 만족하는 꼴로 만든다 · 답은 verify 로 독립 재현.
from __future__ import annotations

import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, numline, reveal, steps, with_pitfalls  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from genkit.expr import eul, ika, pn, ro, wa  # noqa: E402  — 표에 굽는 문장의 조사 (엔진과 같은 규칙)

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def sup(n: int) -> str:
    return str(n).translate(SUP)


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def seed(seed_id, title, cids, note, templates, *, category="연산", schema_name=None, geometry=False):
    return {"seed_id": seed_id, "category": category, "title": title, "unit_id": seed_id[:4], "concept_ids": cids,
            "schema_id": None, "schema_name": schema_name, "source_item_ids": [], "note": note, "geometry": geometry,
            "templates": templates}


def fr(v) -> str:
    """표에 넣을 표시 문자열 — 분수는 마커."""
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    s = "-" if f < 0 else ""
    return f"[[{s}frac({abs(f.numerator)},{f.denominator})]]"


def frraw(n: int, d: int) -> str:
    """약분하지 않은 분수 표시 — 6/3 처럼 값은 정수인 분수를 그대로 보일 때."""
    s = "-" if n < 0 else ""
    return f"[[{s}frac({abs(n)},{d})]]"


def atoms(vals) -> set:
    """문면에 찍히는 수 원자 — 정수는 그 값, 분수는 분자·분모(절댓값), 소수는 그 값. R-05·감사 F1 회피용."""
    out = set()
    for v in vals:
        if isinstance(v, float):
            out.add(Fraction(str(v)))
        elif isinstance(v, tuple):
            out.add(Fraction(abs(v[0]))); out.add(Fraction(v[1]))
        else:
            f = Fraction(v)
            if f.denominator == 1:
                out.add(f)
            else:
                out.add(Fraction(abs(f.numerator))); out.add(Fraction(f.denominator))
    return out


BASE = {"process": "절차수행", "context": "무맥락", "ops": ["사칙"], "traps": ["부호"], "qtype": "short",
        "time_limit": 60, "points": 4, "pool_target": 200}

# ═══════════════════════════════════════════════════════════════════ 1. 거듭제곱 (m1-1-02)
PW = "m1-1-power"
PW_BASE = {**BASE, "ops": ["지수"], "traps": ["구하는대상혼동"], "prereq": ["자연수의 곱셈"], "tags": ["거듭제곱", "밑", "지수"]}


def _pow_rows():
    rows = {}
    for a in (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12):
        for n in (2, 3, 4, 5):
            N = a ** n
            if N > 3000:
                continue
            rows[f"{a}|{n}"] = {"a": a, "n": n, "N": N, "SN": sup(n), "MUL": " × ".join([str(a)] * n)}
    return rows


POW_ROWS = _pow_rows()


def pw_t1():
    return tpl(PW, 1, PW_BASE,
        title="거듭제곱의 값 — aⁿ 을 곱셈으로 풀어 계산하기",
        skill="거듭제곱에서 밑과 지수를 구분하고, 밑을 지수만큼 곱해 값을 구하기",
        variant_axis={"밑": "2~12", "지수": "2~5"},
        discriminates="aⁿ 을 a × n 으로 잘못 계산하지 않고, 밑을 지수만큼 곱하는가",
        difficulty=1,
        params=[{"name": "k", "values": {"in": list(POW_ROWS)}}],
        table={"key": "k", "rows": POW_ROWS},
        derive={"ans": "N", "wrong": "a*n"},
        constraints=["N != a*n"],
        cost_values=["a", "n", "N"],
        answer_var="ans",
        verify=["ans == a**n", "ans == N"],
        question="{a}{SN}의 값을 구하시오.",
        answer="{N}", answer_alt=[],
        sol1="거듭제곱 {a}{SN}은 밑 {a}{eul(a)} 지수 {n}만큼, 즉 {n}번 곱한 것을 간단히 나타낸 것이다. {a} × {n}{ika(n)} 아니라 {a}{eul(a)} {n}번 곱해야 한다.",
        sol2=["{a}{SN} = {MUL}", "차례로 곱하면 {a}{SN} = {N}"],
        sol2_fig=steps([{"text": "{a}{SN} = {MUL}", "hint": "밑 {a}{eul(a)} {n}번 곱한다", "marks": [{"on": "{SN}", "note": "지수 = 곱하는 횟수"}]},
                        {"text": "= {N}"}]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1)]],
        sol3="{a} × {n} = {wrong}{wa(wrong)} 혼동하기 쉽다. {MUL} = {N}{eul(N)} 다시 곱해 확인하면 답은 {N}이다.",
        sol3_fig=steps(["{MUL} = {N}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="{a}{SN}은 {a}{eul(a)} {n}번 곱한 것이므로 {a}{SN} = {MUL} = {N}이다.",
        rubric=[
            {"element": "거듭제곱의 뜻", "points": 3, "criterion": "{a}{SN}을 {a}{eul(a)} {n}번 곱한 것({MUL})으로 나타냈다.", "partial": "{a} × {n}{ro(n)} 썼으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "곱하여 {N}{eul(N)} 구했다.", "partial": "곱셈 실수면 1점."},
        ],
        rubric_total=5,
    )


def _pw2_rows():
    rows = {}
    for p, q in ((2, 3), (2, 5), (3, 5), (2, 7), (3, 7), (5, 7)):
        for a in (1, 2, 3, 4):
            for b in (1, 2, 3):
                if a + b < 3:
                    continue
                rows[f"{p}|{q}|{a}|{b}"] = {"p": p, "q": q, "a": a, "b": b, "PROD": " × ".join([str(p)] * a + [str(q)] * b),
                                            "PA": f"{p}{sup(a) if a > 1 else ''}", "QB": f"{q}{sup(b) if b > 1 else ''}"}
    return rows


PW2_ROWS = _pw2_rows()
PW2_Q = {"sum": {"QT": "a + b", "m1": 1}, "prod": {"QT": "a × b", "m1": 0}}


def pw_t2():
    return tpl(PW, 2, PW_BASE,
        title="같은 수의 곱을 거듭제곱으로 — 2 × 2 × 2 × 5 × 5 = 2ᵃ × 5ᵇ 에서 a, b 읽기",
        skill="같은 수가 반복해서 곱해진 식을 거듭제곱으로 나타내고 지수를 읽어 a + b, a × b 의 값을 구하기",
        variant_axis={"구하는 것": "a + b / a × b", "밑": "(2,3)·(2,5)·(3,5)·(2,7)·(3,7)·(5,7)", "지수": "a 1~4 · b 1~3"},
        discriminates="곱해진 횟수를 지수로 옮기는가 (밑끼리 곱하거나 횟수를 세다 빠뜨리지 않는가)",
        difficulty=2,
        params=[{"name": "q1", "values": {"in": list(PW2_Q)}}, {"name": "k", "values": {"in": list(PW2_ROWS)}}],
        table=[{"key": "q1", "rows": PW2_Q}, {"key": "k", "rows": PW2_ROWS}],
        derive={"ans": "m1*(a + b) + (1 - m1)*a*b", "V": "p**a * q**b"},
        constraints=["ans != p", "ans != q", "V <= 20000"],
        cost_values=["a", "b", "p", "q", "ans"],
        answer_var="ans",
        verify=["ans == m1*(a + b) + (1 - m1)*a*b", "a + b >= 3"],
        question="{PROD}{eul(PROD)} 거듭제곱을 사용하여 나타내면 {p}ᵃ × {q}ᵇ (a, b는 자연수)이다. 이때 {QT}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="같은 수를 여러 번 곱한 것은 거듭제곱으로 간단히 쓴다. {p}{ika(p)} 몇 번, {q}{ika(q)} 몇 번 곱해졌는지 세어 각각 지수로 올리면 a와 b가 정해진다.",
        sol2=["{p}{eun(p)} {a}번 곱해졌으므로 {PA}, {q}{eun(q)} {b}번 곱해졌으므로 {QB}",
              "따라서 {PROD} = {PA} × {QB}이고 a = {a}, b = {b}",
              "{QT} = {ans}"],
        sol2_fig=steps([{"text": "{PROD}", "hint": "{p}{ika(p)} {a}번, {q}{ika(q)} {b}번"},
                        {"text": "= {PA} × {QB}", "marks": [{"on": "{PA}", "note": "곱한 횟수가 지수"}]},
                        {"text": "a = {a}, b = {b} → {QT} = {ans}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)]],
        sol3="{PA} × {QB}{eul(QB)} 다시 풀어 쓰면 {PROD}{ika(PROD)} 되어 처음 식과 같다. 따라서 a = {a}, b = {b}이고 {QT} = {ans}이다.",
        sol3_fig=steps(["{PA} × {QB} = {PROD}", "{QT} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{PROD} = {PA} × {QB}이므로 a = {a}, b = {b}이다. 따라서 {QT} = {ans}이다.",
        rubric=[
            {"element": "거듭제곱으로 나타내기", "points": 3, "criterion": "{PROD}{eul(PROD)} {PA} × {QB}{ro(QB)} 나타냈다.", "partial": "지수 하나를 잘못 셌으면 1점."},
            {"element": "지수 읽기", "points": 2, "criterion": "a = {a}, b = {b}{ro(b)} 읽었다.", "partial": "밑과 지수를 바꿔 읽었으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{QT} = {ans}{eul(ans)} 구했다.", "partial": "다른 식의 값을 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def _pw3_rows():
    rows = {}
    for a in (2, 3, 4, 5, 6, 7, 10):
        for n in (2, 3, 4, 5, 6):
            N = a ** n
            if N > 10000 or (a, n) in ((4, 2), (4, 3)):      # 4² = 2⁴ 처럼 밑이 둘로 읽히는 것은 뺀다
                continue
            if a in (4, 9) or (a == 8) or (a == 6 and n > 4):
                continue
            if a == n:                                          # 2² = 4, 3³ = 27 — 밑과 지수가 같으면 '밑·지수를 바꿔 답함' 실수거리가 정답을 가리킨다
                continue
            rows[f"{a}|{n}|e"] = {"a": a, "n": n, "N": N, "mode": 0, "AV": n, "SN": sup(n), "MUL": " × ".join([str(a)] * n)}
            rows[f"{a}|{n}|b"] = {"a": a, "n": n, "N": N, "mode": 1, "AV": a, "SN": sup(n), "MUL": " × ".join([str(a)] * n)}
    return rows


PW3_ROWS = _pw3_rows()


def pw_t3():
    return tpl(PW, 3, PW_BASE,
        title="지수·밑 거꾸로 구하기 — aⁿ = N 에서 n 또는 a",
        skill="거듭제곱의 값이 주어졌을 때 밑을 반복해서 곱하거나 소인수분해하여 지수 또는 밑을 구하기",
        variant_axis={"구하는 것": "지수 n / 밑 a", "밑": "2·3·5·6·7·10", "값": "10000 이하"},
        discriminates="N을 같은 수의 곱으로 분해해 곱한 횟수를 지수로 읽는가",
        difficulty=2,
        params=[{"name": "k", "values": {"in": list(PW3_ROWS)}}],
        table={"key": "k", "rows": PW3_ROWS},
        derive={"ans": "AV", "wrong": "N/a"},
        constraints=["n >= 2"],
        cost_values=["a", "n", "N"],
        answer_var="ans",
        verify=["a**n == N", "(mode == 0 and ans == n) or (mode == 1 and ans == a)"],
        question=None,   # 표의 QTEXT (mode 별 문면) — pw_t3_fix
        answer="{ans}", answer_alt=[],
        sol1="{N}{eul(N)} {a}로 계속 나누어(같은 수의 곱으로 분해하여) 몇 번 곱해졌는지 세면 지수를 알 수 있고, 반대로 지수를 알면 어떤 수를 그만큼 곱해 {N}{ika(N)} 되는지 찾으면 밑을 알 수 있다.",
        sol2=["{N} = {MUL}", "{a}{ika(a)} {n}번 곱해졌으므로 {N} = {a}{SN}", "따라서 구하는 값은 {ans}"],
        sol2_fig=steps([{"text": "{N} = {MUL}", "hint": "{a}로 계속 나누어 본다"},
                        {"text": "= {a}{SN}", "marks": [{"on": "{SN}", "note": "곱한 횟수"}]},
                        {"text": "답: {ans}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)]],
        sol3="{a}{SN} = {MUL} = {N}{ro(N)} 다시 계산해 보면 값이 맞는다. 따라서 답은 {ans}이다.",
        sol3_fig=steps(["{a}{SN} = {N}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="{N} = {MUL} = {a}{SN}이므로 구하는 값은 {ans}이다.",
        rubric=[
            {"element": "같은 수의 곱으로 분해", "points": 3, "criterion": "{N}{eul(N)} {MUL}{ro(MUL)} 나타냈다.", "partial": "일부만 분해했으면 1점."},
            {"element": "거듭제곱으로 쓰기", "points": 2, "criterion": "{N} = {a}{SN}{ro(SN)} 나타냈다.", "partial": "밑과 지수를 바꿔 썼으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "구하는 값 {ans}{eul(ans)} 답했다.", "partial": "지수와 밑을 바꿔 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


def _pw3_texts(r):
    """t3 해설 — 지수를 구할 때(밑을 안다)는 N 을 밑으로 1이 될 때까지 나누고,
    밑을 구할 때(밑을 모른다)는 N 을 소인수분해해 똑같은 묶음 n개로 나눈다 (답인 밑을 미리 쓰지 않는다)."""
    a, n, N, SN, MUL = r["a"], r["n"], r["N"], r["SN"], r["MUL"]
    if r["mode"] == 0:
        chain = " → ".join(str(a ** k) for k in range(n, -1, -1))
        return {
            "SOL1": f"{a}ⁿ은 {a}{eul(a)} n번 곱한 수이다. {N}{eul(N)} {a}{ro(a)} 1이 될 때까지 나누어 몇 번 나누어지는지 세면, "
                    f"{N}{ika(N)} {a}{eul(a)} 몇 번 곱한 수인지, 즉 지수 n을 알 수 있다.",
            "S1": f"{N}{eul(N)} {a}{ro(a)} 1이 될 때까지 나누면 {chain}, 모두 {n}번 나누어진다",
            "S2": f"즉 {a}{ika(a)} {n}번 곱해진 수이므로 {N} = {MUL} = {a}{SN}",
            "S3": f"따라서 n = {n}",
            "F1": chain, "FH": f"{a}{ro(a)} {n}번 나누어진다", "F2": f"{N} = {a}{SN}", "FN": "나눈 횟수 = 지수", "F3": f"n = {n}",
            "MA": f"{N}{eul(N)} {a}{ro(a)} 1이 될 때까지 나누면 {n}번 나누어지므로 {N} = {MUL} = {a}{SN}이다. 따라서 n = {n}이다.",
            "PITA": f"{N}{eul(N)} {a}{ro(a)} 1이 될 때까지 나눈 횟수를 하나 적게 세어 지수를 1 작게 씀",
            "PITB": f"지수 n 대신 밑 {a}{eul(a)} 답으로 씀",
        }
    sol1 = (f"x{SN}은 같은 수 x를 {n}번 곱한 수이다. x를 모르므로 먼저 {N}{eul(N)} 소인수분해하고, "
            f"곱해진 수들을 똑같은 묶음 {n}개로 나누면 한 묶음의 값이 x이다.")
    if a in (6, 10):                                  # 합성수 밑 — 두 소인수를 하나씩 묶는다
        p, q = (2, 3) if a == 6 else (2, 5)
        pf = " × ".join([str(p)] * n + [str(q)] * n)
        gr = " × ".join([f"({p} × {q})"] * n)
        s2 = f"{p}{wa(p)} {q}{eul(q)} 하나씩 묶으면 {N} = {gr} = {MUL} = {a}{SN}"
        f2 = f"= {gr} = {a}{SN}"
        ma = f"{N}{eul(N)} 소인수분해하면 {N} = {pf} = {gr} = {a}{SN}이므로 x = {a}이다."
    else:                                             # 소수 밑 — 소인수분해가 곧 같은 수의 곱
        pf = MUL
        s2 = f"{a}{ika(a)} {n}번 곱해졌으므로 {N} = {a}{SN}"
        f2 = f"= {a}{SN}"
        ma = f"{N}{eul(N)} 소인수분해하면 {N} = {MUL} = {a}{SN}이므로 x = {a}이다."
    return {"SOL1": sol1, "S1": f"{N}{eul(N)} 소인수분해하면 {N} = {pf}", "S2": s2, "S3": f"따라서 x = {a}",
            "F1": f"{N} = {pf}", "FH": "소인수분해", "F2": f2, "FN": f"같은 수를 {n}번 곱함", "F3": f"x = {a}", "MA": ma,
            "PITA": f"x{SN}을 x × {n}{ro(n)} 착각해 {N}{eul(N)} {n}{ro(n)} 나눔",
            "PITB": f"밑 x 대신 지수 {n}{eul(n)} 답으로 씀"}


def pw_t3_fix(t):
    """question 은 mode 별로 다르다 — 표에 QTEXT 를 두고 문면은 {QTEXT} 하나로. 해설도 mode 별로 표에 굽는다."""
    for r in PW3_ROWS.values():
        r["QTEXT"] = (f"{r['a']}ⁿ = {r['N']}일 때, 자연수 n의 값을 구하시오." if r["mode"] == 0
                      else f"x{r['SN']} = {r['N']}일 때, 자연수 x의 값을 구하시오.")
        r.update(_pw3_texts(r))
    t["question"] = "{QTEXT}"
    t["sol1"] = "{SOL1}"
    t["sol2"] = ["{S1}", "{S2}", "{S3}"]
    t["sol2_fig"] = steps([{"text": "{F1}", "hint": "{FH}"},
                           {"text": "{F2}", "marks": [{"on": "{SN}", "note": "{FN}"}]},
                           {"text": "{F3}"}])
    t["model_answer"] = "{MA}"
    return t


# ═══════════════════════════════════════════════════════════════════ 2. 양수와 음수 (m1-1-09)
SG = "m1-1-sign-number"
SG_BASE = {**BASE, "process": "표현", "context": "생활맥락", "ops": ["사칙"], "traps": ["부호"], "prereq": ["자연수와 0"], "tags": ["양수", "음수", "부호"], "difficulty": 1}

CTX_ROWS = {                                            # 조사는 단위를 읽는 소리로 굳혀 둔다 (℃ 도·m 미터·km 킬로미터 → 는/로, 원·명 → 은/으로)
    #  UQ: 수 뒤에 붙는 단위(기호 단위는 띄어 씀) · AQ2: 묻는 양의 꼬리 · AE: 그 뒤 은/는 · AJ: 을/를 · UR: 답 뒤 (으)로
    "temp": {"POS": "영상", "NEG": "영하", "U": "℃", "UQ": " ℃", "EX": 5, "PEX": "영상 5 ℃를 +5 ℃로",
             "ASK1": "영하 ", "AQ2": " ℃", "AE": "는", "AJ": "를", "UR": "로"},
    "sea": {"POS": "해발", "NEG": "해저", "U": "m", "UQ": " m", "EX": 100, "PEX": "해발 100 m를 +100 m로",
            "ASK1": "해저 ", "AQ2": " m", "AE": "는", "AJ": "를", "UR": "로"},
    "money": {"POS": "수입", "NEG": "지출", "U": "원", "UQ": "원", "EX": 1000, "PEX": "수입 1000원을 +1000원으로",
              "ASK1": "지출 ", "AQ2": "원", "AE": "은", "AJ": "을", "UR": "으로"},
    "profit": {"POS": "이익", "NEG": "손해", "U": "원", "UQ": "원", "EX": 500, "PEX": "이익 500원을 +500원으로",
               "ASK1": "손해 ", "AQ2": "원", "AE": "은", "AJ": "을", "UR": "으로"},
    "east": {"POS": "동쪽", "NEG": "서쪽", "U": "km", "UQ": " km", "EX": 3, "PEX": "동쪽으로 3 km 이동한 것을 +3 km로",
             "ASK1": "서쪽으로 ", "AQ2": " km 이동한 것", "AE": "은", "AJ": "을", "UR": "로"},
    "gain": {"POS": "증가", "NEG": "감소", "U": "명", "UQ": "명", "EX": 10, "PEX": "10명 증가를 +10명으로",
             "ASK1": "", "AQ2": "명 감소", "AE": "는", "AJ": "를", "UR": "으로"},
}
SIDE_ROWS = {"neg": {"s": -1, "SIDE": "NEG"}}          # 양수 쪽을 묻는 변주는 답의 수가 문면에 그대로 있어 뺐다 (R-05)


SG1_VALS = {                                            # 맥락마다 현실적인 크기 (영하 3000 ℃·서쪽 3000 km·지출 1원 같은 수치를 막는다)
    "temp": [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 20, 25, 30],
    "sea": [1, 2, 3, 4, 6, 7, 8, 9, 12, 15, 20, 25, 30, 40, 50, 200, 300, 2000, 3000],
    "money": [10, 20, 30, 40, 50, 200, 300, 400, 600, 700, 800, 2000, 3000, 5000],
    "profit": [10, 20, 30, 40, 50, 100, 200, 300, 400, 600, 700, 800, 2000, 3000],
    "east": [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 20, 25, 30, 40, 50],
    "gain": [1, 2, 3, 4, 6, 7, 8, 9, 12, 15, 20, 25, 30, 40, 50, 200, 300, 2000, 3000],
}


def _sg1_rows():
    """맥락 × 묻는 쪽 × 크기 — 묻는 양은 '{ASK1}{v}{AQ2}' 로 쓰고 뒤 조사(AE·AJ·UR)는 표에서 받는다 (단위 기호는 조사 함수가 못 읽는다)."""
    rows = {}
    for ck, c in CTX_ROWS.items():
        for sk, sd in SIDE_ROWS.items():
            sw = "−" if sd["s"] < 0 else "+"
            for v in SG1_VALS[ck]:
                rows[f"{ck}|{sk}|{v}"] = {**c, "s": sd["s"], "SW": sw, "NUL": "", "v": v}
    return rows


SG1_ROWS = _sg1_rows()


def sg_t1():
    return tpl(SG, 1, SG_BASE,
        title="서로 반대되는 성질의 양을 부호 +, − 로 나타내기",
        skill="영상/영하, 수입/지출처럼 반대되는 두 양을 기준(0)에 대해 양의 부호와 음의 부호로 나타내기",
        variant_axis={"맥락": "온도·해발·수입/지출·이익/손해·동/서·증가/감소", "묻는 쪽": "음수"},
        discriminates="반대되는 양은 반대 부호로 나타냄을 알고, 값의 크기는 그대로 두는가",
        params=[{"name": "c", "values": {"in": list(SG1_ROWS)}}],
        table={"key": "c", "rows": SG1_ROWS},
        derive={"ansv": "s*v"},
        constraints=["v != EX"],
        cost_values=["v"],
        answer_var="ansv",
        verify=["ansv == s*v", "abs(ansv) == v", "s == -1"],
        question="{PEX} 나타낼 때, {ASK1}{v}{AQ2}{AJ} 부호를 사용하여 나타내시오.",
        answer="{ansv}", answer_alt=["{ansv}{U}", "{ansv} {U}"],
        sol1="서로 반대되는 성질의 두 양은 한쪽을 양의 부호 +로 나타내면 다른 쪽은 음의 부호 −로 나타낸다. 부호만 정하면 되고 크기(수)는 그대로 쓴다.",
        sol2=["{PEX} 나타냈으므로 {POS}{eun(POS)} +, {NEG}{eun(NEG)} −", "따라서 {ASK1}{v}{AQ2}{AE} {ansv}{UQ}"],
        sol2_fig=steps([{"text": "{POS} → +,  {NEG} → −", "hint": "반대되는 양은 반대 부호"},
                        {"text": "{ASK1}{v}{AQ2} → {ansv}{UQ}", "marks": [{"on": "{ansv}", "note": "크기 {v}{eun(v)} 그대로"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="0을 기준으로 {POS}{eul(POS)} +로 나타냈으니 반대인 {NEG}{eun(NEG)} −이고, 크기 {v}{eun(v)} 그대로이다. 답은 {ansv}{UQ}이다.",
        sol3_fig=steps(["0을 기준으로 {POS}: +  /  {NEG}: −", "답: {ansv}{UQ}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{POS}{eul(POS)} +로 나타내므로 반대인 {NEG}{eun(NEG)} −로 나타낸다. 따라서 {ASK1}{v}{AQ2}{AE} {ansv}{UQ}이다.",
        rubric=[
            {"element": "부호 정하기", "points": 3, "criterion": "반대되는 양이므로 음의 부호 −를 붙였다.", "partial": "부호가 반대면 인정하지 않는다."},
            {"element": "답 쓰기", "points": 2, "criterion": "{ansv}{UQ}{UR} 크기와 부호를 함께 썼다.", "partial": "부호 없이 {v}만 썼으면 1점."},
        ],
        rubric_total=5,
    )


def sg_t2():
    return tpl(SG, 2, SG_BASE,
        title="수직선 위에서 원점으로부터의 방향과 거리로 수 읽기",
        skill="수직선에서 원점의 오른쪽은 양수, 왼쪽은 음수임을 알고 두 점이 나타내는 수를 읽어 합을 구하기",
        variant_axis={"방향": "오른쪽·왼쪽", "거리": "1~9"},
        discriminates="왼쪽으로 떨어진 점을 음수로 읽고, 두 수의 합에서 부호를 유지하는가",
        context="무맥락", difficulty=2,
        params=[{"name": "a", "values": {"int": [1, 9]}}, {"name": "b", "values": {"int": [1, 9]}}],
        derive={"A": "a", "B": "-b", "ans": "a - b"},
        constraints=["a != b"],
        cost_values=["a", "b", "ans"],
        answer_var="ans",
        verify=["ans == a + (-b)", "A > 0", "B < 0"],
        question="수직선에서 점 A는 원점의 오른쪽으로 {a}만큼, 점 B는 원점의 왼쪽으로 {b}만큼 떨어져 있다. 두 점 A, B가 나타내는 수의 합을 구하시오.",
        figure=numline("{-b-2}", "{a+2}", [{"x": "{a}", "label": "A"}, {"x": "{-b}", "label": "B"}]),
        answer="{ans}", answer_alt=[],
        sol1="수직선에서 원점 0의 오른쪽에 있는 점은 양수, 왼쪽에 있는 점은 음수를 나타내고, 원점에서 떨어진 거리가 그 수의 크기다. 먼저 두 점이 나타내는 수를 읽은 뒤 더한다.",
        sol2=["점 A는 오른쪽으로 {a}만큼 → A = {A}", "점 B는 왼쪽으로 {b}만큼 → B = {B}", "합은 {A} + ({B}) = {ans}"],
        sol2_fig=steps([{"text": "A = {A}", "hint": "오른쪽 → 양수"}, {"text": "B = {B}", "hint": "왼쪽 → 음수"},
                        {"text": "{A} + ({B}) = {ans}", "marks": [{"on": "({B})", "note": "음수는 괄호"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="{A}에서 왼쪽으로 {b}만큼 가면 {ans}{ika(ans)} 되므로 합이 맞다. 답은 {ans}이다.",
        sol3_fig=numline("{-b-2}", "{a+2}", [{"x": "{a}", "label": "A"}, {"x": "{-b}", "label": "B"}, {"x": "{a-b}", "label": "합"}]),
        sol3_anim=[[hl("pt:합")]],
        model_answer="점 A는 원점의 오른쪽에 있으므로 {A}, 점 B는 왼쪽에 있으므로 {B}{eul(B)} 나타낸다. 따라서 두 수의 합은 {A} + ({B}) = {ans}이다.",
        rubric=[
            {"element": "두 점이 나타내는 수", "points": 3, "criterion": "A = {A}, B = {B}{ro(B)} 읽었다.", "partial": "B의 부호를 빠뜨렸으면 1점."},
            {"element": "합 구하기", "points": 2, "criterion": "{A} + ({B}) = {ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def _sg3_rows():
    rnd = random.Random(20260921)
    pool_pos = [7, 8, 12, 15, 20, Fraction(7, 9), Fraction(11, 8), Fraction(13, 7), 0.7, 2.25, 4.2, 9.5]
    pool_neg = [-7, -9, -10, -13, -15, Fraction(-7, 8), Fraction(-11, 9), Fraction(-13, 10), -0.7, -3.5, -1.2, -8.5]
    rows = {}
    i = 0
    while len(rows) < 80:
        np_ = rnd.choice([1, 2, 3, 4])
        nn = rnd.choice([1, 2, 3, 4])
        has0 = rnd.random() < 0.5
        lst = rnd.sample(pool_pos, np_) + rnd.sample(pool_neg, nn) + ([0] if has0 else [])
        rnd.shuffle(lst)
        at = atoms(lst)
        for qk, qw, m1, cnt in (("pos", "양수", 1, np_), ("neg", "음수", 0, nn)):
            if Fraction(cnt) in at:
                continue
            i += 1
            rows[f"L{i}"] = {"L": ",  ".join(str(v) if isinstance(v, float) else fr(v) for v in lst), "QW": qw, "m1": m1,
                             "NP": np_, "NN": nn, "NZ": 1 if has0 else 0, "NT": len(lst)}
    return rows


SG3_ROWS = _sg3_rows()


def sg_t3():
    return tpl(SG, 3, SG_BASE,
        title="여러 수 가운데 양수·음수의 개수 세기 (0은 양수도 음수도 아니다)",
        skill="주어진 수들에서 부호를 보고 양수와 음수를 가르며, 0은 어느 쪽에도 들지 않음을 알기",
        variant_axis={"묻는 것": "양수의 개수 / 음수의 개수", "0 포함": "있음/없음", "수의 꼴": "정수·분수·소수 섞임"},
        discriminates="분수·소수도 부호로 판단하고, 0을 양수나 음수로 세지 않는가",
        process="개념이해", context="무맥락", difficulty=1,
        params=[{"name": "k", "values": {"in": list(SG3_ROWS)}}],
        table={"key": "k", "rows": SG3_ROWS},
        derive={"ansv": "m1*NP + (1 - m1)*NN"},
        constraints=["NT >= 3"],
        cost_values=["NT", "NP", "NN"],
        answer_var="ansv",
        verify=["ansv == m1*NP + (1 - m1)*NN", "NP + NN + NZ == NT", "NP >= 1", "NN >= 1"],
        question="다음 수 {L} 중에서 {QW}{eun(QW)} 모두 몇 개인지 구하시오.",
        answer="{ansv}", answer_alt=["{ansv}개"],
        sol1="양수는 0보다 큰 수로 부호 +가 붙거나 부호가 없는 수이고, 음수는 0보다 작은 수로 부호 −가 붙은 수다. 분수나 소수도 마찬가지로 부호로 판단하며, 0은 양수도 음수도 아니다.",
        sol2=["부호 −가 붙은 수는 음수이고, 그 개수는 {NN}개", "나머지 가운데 0을 뺀 수가 양수이고, 그 개수는 {NP}개", "따라서 {QW}{eun(QW)} {ansv}개"],
        sol2_fig=steps([{"text": "음수(−): {NN}개", "hint": "부호 −"}, {"text": "양수: {NP}개", "hint": "0은 제외", "marks": [{"on": "0", "note": "0은 양수도 음수도 아님"}]}, {"text": "{QW}: {ansv}개"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="양수 {NP}개, 음수 {NN}개, 0이 {NZ}개이면 모두 {NT}개가 되어 주어진 수의 개수와 같다. 따라서 {QW}{eun(QW)} {ansv}개다.",
        sol3_fig=steps(["{NP} + {NN} + {NZ} = {NT}", "{QW}: {ansv}개"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="주어진 수 중 음수는 부호 −가 붙은 {NN}개, 양수는 0을 제외한 나머지 {NP}개이다. 따라서 {QW}{eun(QW)} {ansv}개이다.",
        rubric=[
            {"element": "부호로 가르기", "points": 3, "criterion": "양수 {NP}개, 음수 {NN}개로 갈랐다.", "partial": "분수·소수를 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QW}의 개수 {ansv}개를 답했다.", "partial": "0을 세어 넣었으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# ═══════════════════════════════════════════════════════════════════ 3. 정수와 유리수 (m1-1-10)
IR = "m1-1-int-rational"
IR_BASE = {**BASE, "process": "개념이해", "ops": ["사칙"], "traps": ["조건누락"], "prereq": ["양수와 음수", "분수"], "tags": ["정수", "유리수"]}


def _ir1_rows():
    rnd = random.Random(1010)
    nat = [7, 8, 12, 15, 20, 9]
    negint = [-7, -9, -10, -13, -8]
    disint = [(18, 9), (-24, 8), (30, 15), (-28, 7)]                                    # 정수인 분수 (약분하면 정수) — 튜플로 두어 약분 전 꼴을 보인다
    nonint = [Fraction(7, 9), Fraction(-11, 8), Fraction(13, 7), Fraction(-9, 10), 0.7, -1.5, 2.25, -0.8]
    Q = (("nat", "자연수", 1, 0, 0, 0), ("negi", "음의 정수", 0, 1, 0, 0), ("int", "정수", 0, 0, 1, 0), ("non", "정수가 아닌 유리수", 0, 0, 0, 1))
    rows = {}
    i = 0
    while len(rows) < 120:
        a, b, c, d, z = rnd.choice([1, 2]), rnd.choice([1, 2]), rnd.choice([0, 1]), rnd.choice([1, 2, 3]), rnd.choice([0, 1])
        lst = rnd.sample(nat, a) + rnd.sample(negint, b) + rnd.sample(disint, c) + rnd.sample(nonint, d) + ([0] if z else [])
        rnd.shuffle(lst)
        at = atoms(lst)
        NAT = a + sum(1 for v in lst if isinstance(v, tuple) and v[0] > 0)
        NEGI = b + sum(1 for v in lst if isinstance(v, tuple) and v[0] < 0)
        INT, NON = a + b + c + z, d
        for qk, qw, w1, w2, w3, w4 in Q:
            cnt = w1 * NAT + w2 * NEGI + w3 * INT + w4 * NON
            if cnt < 1 or Fraction(cnt) in at:
                continue
            i += 1
            rows[f"L{i}"] = {"L": ",  ".join(str(v) if isinstance(v, float) else (frraw(*v) if isinstance(v, tuple) else fr(v)) for v in lst),
                             "QW": qw, "w1": w1, "w2": w2, "w3": w3, "w4": w4, "NAT": NAT, "NEGI": NEGI, "INT": INT, "NON": NON, "NT": len(lst),
                             "ZW": "0 1개, " if z else ""}
    return rows


IR1_ROWS = _ir1_rows()


def ir_t1():
    return tpl(IR, 1, IR_BASE,
        title="주어진 수를 자연수·정수·정수가 아닌 유리수로 분류하기",
        skill="분수·소수 꼴의 수도 값으로 판단하여 자연수, 음의 정수, 정수, 정수가 아닌 유리수로 분류하고 개수 세기",
        variant_axis={"묻는 것": "자연수 / 음의 정수 / 정수 / 정수가 아닌 유리수", "함정": "6/3 처럼 정수인 분수, 0"},
        discriminates="[[frac(6,3)]] = 2 처럼 분수 꼴이라도 값이 정수이면 정수로 분류하고, 0을 정수에 넣는가",
        difficulty=2,
        params=[{"name": "k", "values": {"in": list(IR1_ROWS)}}],
        table={"key": "k", "rows": IR1_ROWS},
        derive={"ansv": "w1*NAT + w2*NEGI + w3*INT + w4*NON"},
        constraints=["ansv >= 1"],
        cost_values=["NT", "ansv"],
        answer_var="ansv",
        verify=["ansv == w1*NAT + w2*NEGI + w3*INT + w4*NON", "INT + NON == NT", "NAT + NEGI <= INT", "w1 + w2 + w3 + w4 == 1"],
        question="다음 수 {L} 중에서 {QW}{eun(QW)} 모두 몇 개인지 구하시오.",
        answer="{ansv}", answer_alt=["{ansv}개"],
        sol1="정수는 양의 정수(자연수), 0, 음의 정수를 통틀어 말하고, 유리수는 (정수)/(0이 아닌 정수) 꼴로 나타낼 수 있는 수다. 분수나 소수는 값을 따져야 한다 — 약분해서 정수가 되면 정수이고, 그렇지 않으면 정수가 아닌 유리수다.",
        sol2=["분수는 약분해 값을 확인한다. 정수인 것: 자연수 {NAT}개, {ZW}음의 정수 {NEGI}개 → 정수 {INT}개",
              "정수가 아닌 유리수는 나머지 {NON}개",
              "따라서 {QW}{eun(QW)} {ansv}개"],
        sol2_fig=steps([{"text": "정수: 자연수 {NAT}개 + {ZW}음의 정수 {NEGI}개 = {INT}개", "hint": "약분하면 정수인 분수 포함", "marks": [{"on": "정수", "note": "0도 정수"}]},
                        {"text": "정수가 아닌 유리수: {NON}개", "hint": "약분해도 분수·소수"},
                        {"text": "{QW}: {ansv}개"}]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="정수 {INT}개와 정수가 아닌 유리수 {NON}개를 더하면 {NT}개로 주어진 수의 개수와 같다. 따라서 {QW}{eun(QW)} {ansv}개다.",
        sol3_fig=steps(["{INT} + {NON} = {NT}", "{QW}: {ansv}개"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="분수는 약분하여 값을 확인하면 정수는 {INT}개(자연수 {NAT}개, 음의 정수 {NEGI}개)이고 정수가 아닌 유리수는 {NON}개이다. 따라서 {QW}{eun(QW)} {ansv}개이다.",
        rubric=[
            {"element": "정수 가려내기", "points": 3, "criterion": "약분하여 정수인 것과 0까지 정수로 분류했다.", "partial": "분수 꼴의 정수를 놓쳤으면 1점."},
            {"element": "정수가 아닌 유리수", "points": 2, "criterion": "나머지를 정수가 아닌 유리수로 분류했다.", "partial": "소수를 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{QW}의 개수 {ansv}개를 답했다.", "partial": "다른 분류의 개수를 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )




def ir_t2():
    return tpl(IR, 2, IR_BASE,
        title="두 수 사이에 있는 정수의 개수 — 음수·양수를 걸치는 구간",
        skill="음수 a와 양수 b 사이에 있는 정수를 빠짐없이 세어 개수를 구하기 (0을 잊지 않기)",
        variant_axis={"구간": "사이 / 이상 이하", "a": "−9~−1", "b": "1~9"},
        discriminates="구간에 0이 포함됨을 알고, 양 끝을 포함하는지에 따라 개수를 맞게 세는가",
        process="절차수행", difficulty=2,
        params=[{"name": "q1", "values": {"in": ["open", "ge"]}}, {"name": "m", "values": {"int": [1, 9]}}, {"name": "b", "values": {"int": [1, 9]}}],
        table={"key": "q1", "rows": {"open": {"QW": "사이에 있는", "iA": 0, "iB": 0, "QE": "사이에 있는"}, "ge": {"QW": "이상", "iA": 1, "iB": 1, "QE": "이하인"}}},
        derive={"a": "-m", "ans": "b - a - 1 + iA + iB", "NNEG": "m - 1 + iA", "NPOS": "b - 1 + iB"},
        constraints=["ans >= 2"],
        cost_values=["m", "b", "ans"],
        answer_var="ans",
        verify=["ans == (b - 1 + iB) + 1 + (m - 1 + iA)", "a < 0", "b > 0"],
        question=None,   # 구간 종류별 문면 — ir_t2_split
        answer="{ans}", answer_alt=["{ans}개"],
        sol1="수직선에서 {a}{wa(a)} {b} 사이를 생각하면 음의 정수, 0, 양의 정수가 차례로 놓인다. 0을 빠뜨리기 쉬우므로 음수 쪽, 0, 양수 쪽으로 나누어 센다.",
        sol2=["음의 정수: {NNEG}개", "0: 1개", "양의 정수: {NPOS}개 → 모두 {ans}개"],
        sol2_fig=steps([{"text": "음의 정수 {NNEG}개", "hint": "{a} 쪽"}, {"text": "0 (1개)", "marks": [{"on": "0", "note": "0을 잊지 말 것"}]}, {"text": "양의 정수 {NPOS}개 → {NNEG} + 1 + {NPOS} = {ans}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)]],
        sol3="수직선에 {a}부터 {b}까지 정수를 찍어 세어 보면 조건에 맞는 정수는 {ans}개다.",
        sol3_fig=numline("{a-1}", "{b+1}", [{"x": "{a}", "label": "a"}, {"x": 0, "label": "0"}, {"x": "{b}", "label": "b"}]),
        sol3_anim=[[hl("pt:0")]],
        model_answer="{a}{wa(a)} {b} 사이의 정수를 음의 정수 {NNEG}개, 0 한 개, 양의 정수 {NPOS}개로 나누어 세면 모두 {ans}개이다.",
        rubric=[
            {"element": "구간 읽기", "points": 2, "criterion": "양 끝 {a}, {b}의 포함 여부를 바르게 판단했다.", "partial": "한쪽만 잘못 판단했으면 1점."},
            {"element": "정수 세기", "points": 3, "criterion": "음의 정수·0·양의 정수로 나누어 빠짐없이 셌다.", "partial": "0을 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}개를 답했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


def ir_t2_split(t):
    """문면이 구간 종류에 따라 다르므로 q1 을 고정한 틀 두 개(t2·t3)로 나눈다."""
    out = []
    for no, key, qtext in ((2, "open", "{a}{wa(a)} {b} 사이에 있는 정수는 모두 몇 개인지 구하시오."),
                           (3, "ge", "{a} 이상 {b} 이하인 정수는 모두 몇 개인지 구하시오.")):
        u = dict(t)
        u["id"] = f"{IR}-t{no}"
        u["params"] = [p for p in t["params"] if p["name"] != "q1"] + [{"name": "q1", "values": {"in": [key]}}]
        u["question"] = qtext
        u["title"] = t["title"] + (" (사이)" if key == "open" else " (이상·이하)")
        if key == "ge":                                   # '이상·이하' 는 양 끝을 포함한다 — '사이' 로 풀지 않는다
            u["sol1"] = ("'{a} 이상'은 {a}도 포함하고 '{b} 이하'는 {b}도 포함한다. 수직선에서 {a}부터 {b}까지 음의 정수, 0, 양의 정수가 "
                         "차례로 놓이므로, 0을 빠뜨리지 않도록 음수 쪽, 0, 양수 쪽으로 나누어 센다.")
            u["sol2"] = ["음의 정수: {NNEG}개 ({a}도 포함)", "0: 1개", "양의 정수: {NPOS}개 ({b}도 포함) → 모두 {ans}개"]
            u["sol2_fig"] = steps([{"text": "음의 정수 {NNEG}개", "hint": "{a}도 포함"}, {"text": "0 (1개)", "marks": [{"on": "0", "note": "0을 잊지 말 것"}]},
                                   {"text": "양의 정수 {NPOS}개 → {NNEG} + 1 + {NPOS} = {ans}", "hint": "{b}도 포함"}])
            u["sol2_anim"] = [[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2), hl("hint:2")]]
            u["sol3"] = "수직선에 양 끝 {a}, {b}까지 포함하여 {a}부터 {b}까지의 정수를 찍어 세어 보면 조건에 맞는 정수는 {ans}개다."
            u["sol3_fig"] = numline("{a-1}", "{b+1}", [{"x": "{a}", "label": "{dec(a)}"}, {"x": 0, "label": "0"}, {"x": "{b}", "label": "{dec(b)}"}])
            u["model_answer"] = ("{a} 이상 {b} 이하인 정수는 양 끝 {a}{wa(a)} {b}{eul(b)} 포함한다. 이 정수들을 음의 정수 {NNEG}개, 0 한 개, "
                                 "양의 정수 {NPOS}개로 나누어 세면 모두 {ans}개이다.")
        out.append(u)
    return out


# ═══════════════════════════════════════════════════════════════════ 4. 수의 대소 관계 (m1-1-13)
OD = "m1-1-order"
OD_BASE = {**BASE, "process": "개념이해", "ops": ["사칙"], "traps": ["부호"], "prereq": ["양수와 음수", "절댓값"], "tags": ["대소 관계", "부등호"]}


def _od1_rows():
    """두 수의 대소 — 정수·소수만(분수 마커는 답으로 칠 수 없다). 절반은 둘 다 음수, 나머지 절반은 음수 하나와 0 또는 양수 하나
    (둘 다 0 이상인 쌍은 '음수의 대소'를 재지 못하므로 뺀다)."""
    rnd = random.Random(1313)
    vals = [-7, -3, -1, 0, 1, 3, 7, 12, -2.5, -0.4, 0.75, 3.5, -4, -9, 2, -5.5, 6, -12]
    rows = {}
    i = 0
    pairs = set()
    while len(rows) < 60:
        x, y = rnd.sample(vals, 2)
        if (x, y) in pairs:
            continue
        if len(rows) < 30 and not (x < 0 and y < 0):
            continue
        if len(rows) >= 30 and not (min(x, y) < 0 <= max(x, y)):
            continue
        pairs.add((x, y))
        i += 1
        big, small = (x, y) if x > y else (y, x)
        rows[f"P{i}"] = {"X": str(x), "Y": str(y), "BIG": str(big), "SMALL": str(small), "xv": x, "yv": y, "bv": big, "sv": small,
                         "bothneg": 1 if (x < 0 and y < 0) else 0}
    return rows


OD1_ROWS = _od1_rows()


def od_t1():
    return tpl(OD, 1, OD_BASE,
        title="두 수의 대소 관계를 부등호 < 로 나타내기 — 음수끼리는 절댓값이 큰 쪽이 작다",
        skill="수직선에서 오른쪽에 있는 수가 크다는 것과, 음수끼리는 절댓값이 클수록 작다는 것을 써서 두 수의 대소를 부등호로 나타내기",
        variant_axis={"부호": "둘 다 음수 / 섞임", "꼴": "정수·소수"},
        discriminates="음수는 절댓값이 클수록 작음을 알고, 부등호의 벌어진 쪽이 큰 수임을 지키는가",
        difficulty=2,
        params=[{"name": "k", "values": {"in": list(OD1_ROWS)}}],
        table={"key": "k", "rows": OD1_ROWS},
        derive={"d": "bv - sv"},
        constraints=["d > 0"],
        cost_values=["xv", "yv", "bothneg"],
        answer_var=None,                      # 답이 부등식(문자열) — 값은 verify 로 대조
        verify=["bv == max(xv, yv)", "sv == min(xv, yv)", "bv > sv"],
        question="두 수 {X}, {Y}의 대소 관계를 부등호 <를 사용하여 나타내시오.",
        answer="{SMALL} < {BIG}", answer_alt=["{BIG} > {SMALL}"],
        sol1="수는 수직선에서 오른쪽에 있을수록 크다. 양수는 0보다 크고 음수는 0보다 작으며, 음수끼리는 절댓값이 큰 수가 더 작다. 부등호는 벌어진 쪽이 큰 수를 향하도록 쓴다.",
        sol2=["두 수를 수직선 위에 놓아 어느 쪽이 오른쪽인지 본다", "더 작은 수는 {SMALL}, 더 큰 수는 {BIG}", "따라서 {SMALL} < {BIG}"],
        sol2_fig=steps([{"text": "{X}  vs  {Y}", "hint": "음수·0·양수 순으로, 음수끼리는 절댓값으로"},
                        {"text": "{SMALL} < {BIG}", "marks": [{"on": "<", "note": "벌어진 쪽이 큰 수"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="수직선에 두 수를 찍으면 {SMALL}{ika(SMALL)} 왼쪽, {BIG}{ika(BIG)} 오른쪽에 온다. 따라서 {SMALL} < {BIG}이다.",
        sol3_fig=numline("{min(xv, yv) - 2}", "{max(xv, yv) + 2}", [{"x": "{xv}", "label": "A"}, {"x": "{yv}", "label": "B"}]),
        sol3_anim=[[hl("pt:A", "pt:B")]],
        model_answer="두 수 중 더 작은 수는 {SMALL}, 더 큰 수는 {BIG}이므로 대소 관계는 {SMALL} < {BIG}이다.",
        rubric=[
            {"element": "대소 비교", "points": 3, "criterion": "{SMALL}{ika(SMALL)} {BIG}보다 작음을 바르게 판단했다.", "partial": "음수의 대소를 절댓값 순으로 뒤집었으면 인정하지 않는다."},
            {"element": "부등호로 나타내기", "points": 2, "criterion": "{SMALL} < {BIG}{ro(BIG)} 나타냈다.", "partial": "부등호 방향이 반대면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def _od2_rows():
    rnd = random.Random(2222)
    vals = [Fraction(-7, 2), -3, Fraction(-5, 3), -1, Fraction(-1, 4), 0, Fraction(2, 3), 1, Fraction(9, 4), 3, -2.5, -4, 2, Fraction(-13, 4), 0.5, -0.5, 5, -6]
    rows = {}
    i = 0
    seen = set()
    while len(rows) < 60:
        lst = rnd.sample(vals, 5)
        key = tuple(sorted(Fraction(str(v)) if isinstance(v, float) else Fraction(v) for v in lst))
        if key in seen or len(set(key)) < 5:
            continue
        seen.add(key)
        srt = sorted(lst, key=lambda v: Fraction(str(v)) if isinstance(v, float) else Fraction(v))
        gap = key[-1] - key[0]
        if gap in atoms(lst):
            continue
        i += 1
        row = {"L": ",  ".join(fr(v) if not isinstance(v, float) else str(v) for v in lst),
               "ORD": " < ".join(fr(v) if not isinstance(v, float) else str(v) for v in srt),
               "MAXS": fr(srt[-1]) if not isinstance(srt[-1], float) else str(srt[-1]), "MINS": fr(srt[0]) if not isinstance(srt[0], float) else str(srt[0])}
        for j, v in enumerate(srt, 1):
            f = Fraction(str(v)) if isinstance(v, float) else Fraction(v)
            row[f"S{j}n"], row[f"S{j}d"] = f.numerator, f.denominator
        rows[f"S{i}"] = row
    return rows


OD2_ROWS = _od2_rows()


def od_t2():
    return tpl(OD, 2, OD_BASE,
        title="다섯 수를 작은 것부터 나열해 가장 큰 수와 가장 작은 수의 차 구하기",
        skill="여러 수를 수직선 순서로 나열해 가장 큰 수와 가장 작은 수를 찾고 그 차를 구하기",
        variant_axis={"꼴": "정수·분수·소수 섞임", "부호": "음수 포함"},
        discriminates="음수·0·양수를 한 줄로 세우면서 음수끼리의 순서를 절댓값으로 뒤집지 않고, 음수를 뺄 때 부호를 바르게 처리하는가",
        process="절차수행", difficulty=3, time_limit=90, points=5,
        params=[{"name": "k", "values": {"in": list(OD2_ROWS)}}],
        table={"key": "k", "rows": OD2_ROWS},
        derive={"S1": "S1n/S1d", "S2": "S2n/S2d", "S3": "S3n/S3d", "S4": "S4n/S4d", "S5": "S5n/S5d", "ans": "S5n/S5d - S1n/S1d"},
        constraints=["S1 < S2", "S2 < S3", "S3 < S4", "S4 < S5"],
        cost_values=["S1", "S5", "ans"],
        answer_var="ans",
        verify=["ans == max(S1, S2, S3, S4, S5) - min(S1, S2, S3, S4, S5)", "S1 < S2", "S2 < S3", "S3 < S4", "S4 < S5", "ans > 0"],
        question="다섯 수 {L}{eul(L)} 작은 것부터 차례로 나열할 때, 가장 큰 수와 가장 작은 수의 차를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="음수는 0보다 작고 양수는 0보다 크므로 먼저 음수, 0, 양수로 나눈다. 음수끼리는 절댓값이 큰 수가 더 작고 양수끼리는 절댓값이 큰 수가 더 크다. 분수와 소수는 같은 꼴로 바꾸어 비교한 뒤, 가장 큰 수에서 가장 작은 수를 뺀다.",
        sol2=["음수·0·양수로 나누고 각각 절댓값으로 순서를 정한다", "작은 것부터 나열하면 {ORD}", "가장 큰 수 {MAXS}에서 가장 작은 수 {MINS}{eul(MINS)} 빼면 {ans}"],
        sol2_fig=steps([{"text": "음수 → 0 → 양수", "hint": "음수끼리는 절댓값이 클수록 작다"},
                        {"text": "{ORD}", "marks": [{"on": "<", "note": "왼쪽이 작다"}]},
                        {"text": "{MAXS} − ({MINS}) = {ans}", "marks": [{"on": "({MINS})", "note": "음수를 빼면 더하는 것"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2), hl("mark:2-0")]],
        sol3="나열한 순서 {ORD}에서 양 끝의 두 수가 가장 작은 수와 가장 큰 수다. 두 수 사이의 거리 {ans}{ika(ans)} 곧 차이므로 답은 {ans}이다.",
        sol3_fig=steps(["{ORD}", "{MAXS} − ({MINS}) = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="주어진 수를 작은 것부터 나열하면 {ORD}이다. 가장 큰 수는 {MAXS}, 가장 작은 수는 {MINS}이므로 그 차는 {MAXS} − ({MINS}) = {ans}이다.",
        rubric=[
            {"element": "차례로 나열", "points": 3, "criterion": "{ORD}{ro(ORD)} 바르게 나열했다.", "partial": "한 쌍의 순서만 틀렸으면 1점."},
            {"element": "가장 큰 수·작은 수", "points": 2, "criterion": "가장 큰 수 {MAXS}, 가장 작은 수 {MINS}{eul(MINS)} 골랐다.", "partial": "하나만 맞으면 1점."},
            {"element": "차 구하기", "points": 2, "criterion": "{MAXS} − ({MINS}) = {ans}{eul(ans)} 구했다.", "partial": "부호 처리 실수면 1점."},
        ],
        rubric_total=7,
    )


def od_t3():
    return tpl(OD, 3, OD_BASE,
        title="−a 와 −b 의 대소 — 절댓값이 큰 음수가 더 작다, 큰 수에서 작은 수 빼기",
        skill="두 양수 a < b 에 대해 −a 와 −b 의 대소를 판단하고 큰 수에서 작은 수를 뺀 값을 구하기",
        variant_axis={"간격": "1~12", "a": "1~15"},
        discriminates="음수끼리의 비교에서 절댓값의 순서를 그대로 옮기지 않고, 뺄셈의 순서를 지키는가",
        difficulty=2,
        params=[{"name": "a", "values": {"int": [1, 15]}}, {"name": "h", "values": {"int": [1, 12]}}],
        derive={"b": "a + h", "na": "-a", "nb": "-(a + h)", "ans": "h"},
        constraints=["b <= 27", "h != a", "h != b"],
        cost_values=["a", "b", "ans"],
        answer_var="ans",
        verify=["ans == max(na, nb) - min(na, nb)", "na > nb", "abs(nb) > abs(na)"],
        question="두 수 {na}{wa(na)} {nb}에 대하여 큰 수에서 작은 수를 뺀 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 음수를 비교할 때는 절댓값을 본다. 절댓값이 큰 음수는 수직선에서 0으로부터 더 멀리 왼쪽에 있으므로 더 작다. |{nb}| = {b}{ika(b)} |{na}| = {a}보다 크므로 {nb}{ika(nb)} 더 작고, 큰 수 {na}에서 작은 수 {nb}{eul(nb)} 뺀다.",
        sol2=["|{na}| = {a}, |{nb}| = {b}이고 {a} < {b}", "절댓값이 큰 {nb}{ika(nb)} 더 작다 → {nb} < {na}", "큰 수 − 작은 수 = {na} − {pn(nb)} = {ans}"],
        sol2_fig=numline("{-b-2}", 2, [{"x": "{-a}", "label": "A"}, {"x": "{-b}", "label": "B"}]),
        sol2_anim=[[hl("pt:A", "pt:B")], [hl("pt:B")], []],
        sol3="수직선에서 {nb}{eun(nb)} {na}보다 왼쪽에 있으므로 {nb} < {na}{ika(na)} 맞고, 두 점 사이의 거리가 {h}이므로 {na} − {pn(nb)} = {ans}이다.",
        sol3_fig=steps(["{nb} < {na}", "{na} − {pn(nb)} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="|{na}| = {a} < {b} = |{nb}|이므로 절댓값이 큰 {nb}{ika(nb)} 더 작다. 즉 {nb} < {na}이고, 큰 수에서 작은 수를 빼면 {na} − {pn(nb)} = {ans}이다.",
        rubric=[
            {"element": "절댓값 비교", "points": 2, "criterion": "|{na}| = {a}, |{nb}| = {b}{eul(b)} 비교했다.", "partial": "절댓값을 잘못 썼으면 인정하지 않는다."},
            {"element": "대소 판단", "points": 3, "criterion": "절댓값이 큰 음수가 더 작음을 써서 {nb} < {na}{ro(na)} 판단했다.", "partial": "부등호 방향이 반대면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{na} − {pn(nb)} = {ans}{eul(ans)} 구했다.", "partial": "차의 부호가 틀렸으면 1점."},
        ],
        rubric_total=7,
    )


# ═══════════════════════════════════════════════════════════════════ 5. 부등호의 사용 (m1-1-14)
IS = "m1-1-ineq-sign"
IS_BASE = {**BASE, "process": "표현", "ops": ["부등식"], "traps": ["조건누락"], "prereq": ["수의 대소 관계", "정수"], "tags": ["부등호", "이상", "이하", "초과", "미만"]}
PH_ROWS = {                                             # QA·QB: 문면용 — '이상·초과' 는 수와 띄우고 조사 '보다' 는 붙인다
    "ge_le": {"PH": "이상", "PH2": "이하인", "QA": " 이상", "QB": " 이하인", "iA": 1, "iB": 1, "SA": "≤", "SB": "≤"},
    "ge_lt": {"PH": "이상", "PH2": "미만인", "QA": " 이상", "QB": " 미만인", "iA": 1, "iB": 0, "SA": "≤", "SB": "<"},
    "gt_le": {"PH": "초과", "PH2": "이하인", "QA": " 초과", "QB": " 이하인", "iA": 0, "iB": 1, "SA": "<", "SB": "≤"},
    "gt_lt": {"PH": "초과", "PH2": "미만인", "QA": " 초과", "QB": " 미만인", "iA": 0, "iB": 0, "SA": "<", "SB": "<"},
    "big_le": {"PH": "보다 크고", "PH2": "보다 크지 않은", "QA": "보다 크고", "QB": "보다 크지 않은", "iA": 0, "iB": 1, "SA": "<", "SB": "≤"},
    "ge_lt2": {"PH": "보다 작지 않고", "PH2": "보다 작은", "QA": "보다 작지 않고", "QB": "보다 작은", "iA": 1, "iB": 0, "SA": "≤", "SB": "<"},
}


def _is2_rows():
    """t2 — (표현, m, b) 조합마다 범위의 부호 구성에 맞춘 방침·합 계산 문장을 굽는다.
    음수·양수가 함께 있으면 절댓값이 같은 수끼리 짝지어 0, 한쪽 부호뿐이면(0부터 / 0까지) 짝짓기 없이 그대로 더한다."""
    rows = {}
    for pk, p in PH_ROWS.items():
        for m in range(1, 7):
            for b in range(1, 10):
                a = -m
                lo, hi = a + 1 - p["iA"], b - 1 + p["iB"]
                n = hi - lo + 1
                ans = sum(range(lo, hi + 1))
                if n < 3 or ans == 0 or abs(ans) > 45:
                    continue
                if lo < 0 < hi:
                    c = min(-lo, hi)
                    pairs = "-1과 1" if c == 1 else ("-2와 2, -1과 1" if c == 2 else f"{-c}{wa(-c)} {c}, …, -1과 1")
                    rest = list(range(c + 1, hi + 1)) if hi > -lo else list(range(lo, -c))
                    zero = f"{pairs}은 {'각각 ' if c > 1 else ''}더하면 0이 되고 0은 더해도 합이 변하지 않으니"
                    if len(rest) == 1:
                        s3 = f"{zero}, 남는 수는 {rest[0]}뿐이므로 합은 {ans}"
                    else:
                        s3 = f"{zero}, 남는 수만 더하면 " \
                             + " + ".join([str(rest[0])] + [pn(r) for r in rest[1:]]) + f" = {ans}"
                    s1b = "범위에 음수와 양수가 함께 있으므로, 절댓값이 같은 음수와 양수를 짝지어 더하면 0이 되는 것을 이용하면 계산이 빠르다."
                    mk = "(−k) + k = 0 이용"
                    pit3 = "음수와 양수를 더하면서 부호를 잃음"
                    pp3 = "부호 처리 실수면 1점."
                elif lo == 0:
                    s3 = "0은 더해도 합이 그대로이므로 " + " + ".join(str(r) for r in range(1, hi + 1)) + f" = {ans}"
                    s1b = "이 범위에는 음수가 없어 짝지어 0을 만들 수 없다. 0은 더해도 합이 그대로이므로 양수만 차례로 더한다."
                    mk = "음수가 없으니 그대로 더한다"
                    pit3 = f"1부터 {hi}까지 더하다가 수를 빠뜨리거나 두 번 더함"
                    pp3 = "더하다가 수를 빠뜨리거나 두 번 더했으면 1점."
                else:                                   # hi == 0 — 음수와 0뿐
                    s3 = "0은 더해도 합이 그대로이므로 " + " + ".join([str(lo)] + [pn(r) for r in range(lo + 1, 0)]) + f" = {ans}"
                    s1b = "이 범위에는 양수가 없어 짝지어 0을 만들 수 없다. 0은 더해도 합이 그대로이므로 음수만 차례로 더한다."
                    mk = "양수가 없으니 그대로 더한다"
                    pit3 = "음수끼리 더한 합을 양수로 씀"
                    pp3 = "합의 부호를 +로 썼으면 1점."
                xl = ", ".join(str(v) for v in range(lo, hi + 1)) if n <= 6 else f"{lo}, {lo + 1}, …, {hi}"
                rows[f"{pk}|{m}|{b}"] = {**p, "m": m, "b": b, "S1B": s1b, "S3": s3, "MK": mk, "XL": xl, "PIT3": pit3, "PP3": pp3}
    return rows


IS2_ROWS = _is2_rows()


def is_t1():
    return tpl(IS, 1, IS_BASE,
        title="'이상·이하·초과·미만'을 부등호로 옮겨 조건을 만족하는 정수의 개수 세기",
        skill="말로 주어진 범위를 a ≤ x < b 꼴로 옮기고, 양 끝의 포함 여부에 맞게 정수의 개수를 세기",
        variant_axis={"표현": "이상/이하 · 초과/미만 · 크고/크지 않은 · 작지 않고/작은", "구간": "음수~양수"},
        discriminates="'초과·미만·크지 않다·작지 않다'를 부등호의 종류(≤, <)로 정확히 옮기는가",
        difficulty=2,
        params=[{"name": "ph", "values": {"in": list(PH_ROWS)}}, {"name": "m", "values": {"int": [1, 7]}}, {"name": "b", "values": {"int": [1, 8]}}],
        table={"key": "ph", "rows": PH_ROWS},
        derive={"a": "-m", "ans": "b - a - 1 + iA + iB", "lo": "a + 1 - iA", "hi": "b - 1 + iB"},
        constraints=["ans >= 2"],
        cost_values=["m", "b", "ans"],
        answer_var="ans",
        verify=["ans == hi - lo + 1", "lo >= a", "hi <= b"],
        question="x는 {a}{QA} {b}{QB} 수이다. 이 조건을 만족하는 정수 x는 모두 몇 개인지 구하시오.",
        answer="{ans}", answer_alt=["{ans}개"],
        sol1="'이상·이하·크지 않다·작지 않다'는 그 수를 포함하므로 ≤, ≥를 쓰고, '초과·미만·크다·작다'는 포함하지 않으므로 <, >를 쓴다. 조건을 부등호로 옮긴 뒤 그 범위의 정수를 센다.",
        sol2=["조건을 부등호로 나타내면 {a} {SA} x {SB} {b}", "이 범위의 정수는 {lo}부터 {hi}까지", "따라서 정수 x는 {hi} − {pn(lo)} + 1 = {ans}개"],
        sol2_fig=steps([{"text": "{a} {SA} x {SB} {b}", "hint": "포함하면 ≤, 포함하지 않으면 <", "marks": [{"on": "{a} {SA}", "note": "'{PH}'"}, {"on": "{SB} {b}", "note": "'{PH2}'"}]},   # 옆 수까지 — 렌더러는 첫 일치만 바꾸므로 ≤ ≤ 가 겹치지 않게
                        {"text": "정수 x: {lo}부터 {hi}까지"},
                        {"text": "개수: {hi} − {pn(lo)} + 1 = {ans}"}]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0", "mark:0-1")], [reveal(1)], [reveal(2)]],
        sol3="수직선에 {a}부터 {b}까지 구간을 그리고 양 끝을 포함하면 ●, 포함하지 않으면 ○로 표시한 뒤 그 안의 정수를 세어 보면 {lo}부터 {hi}까지 {ans}개다.",
        # 렌더러(numline)는 점을 늘 ●로 그리고 구간 끝만 ●/○(inclusive)를 가른다 — 끝점은 점으로 찍지 않고 구간 [a, b] 를 ○로 그린 뒤,
        # 포함하는 끝에만 길이 0 구간을 ●로 덧그린다 (seg:0 이 본 구간).
        sol3_fig=numline("{a-1}", "{b+1}", [], [{"from": "{a}", "to": "{b}", "inclusive": False},
                                                 {"from": "{a}", "to": "{a}", "inclusive": "{iA == 1}"},
                                                 {"from": "{b}", "to": "{b}", "inclusive": "{iB == 1}"}]),
        sol3_anim=[[hl("seg:0")]],
        model_answer="조건을 부등호로 나타내면 {a} {SA} x {SB} {b}이다. 이를 만족하는 정수는 {lo}부터 {hi}까지이므로 모두 {ans}개이다.",
        rubric=[
            {"element": "부등호로 나타내기", "points": 3, "criterion": "조건을 {a} {SA} x {SB} {b}{ro(b)} 옮겼다.", "partial": "한쪽 부등호의 종류만 틀렸으면 1점."},
            {"element": "정수 세기", "points": 2, "criterion": "범위의 정수 {lo}~{hi}{eul(hi)} 빠짐없이 셌다.", "partial": "양 끝 처리를 틀렸거나 0을 빠뜨렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}개를 답했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


def is_t2():
    return tpl(IS, 2, IS_BASE,
        title="조건을 만족하는 정수의 합 — 부등호로 옮긴 뒤 모두 더하기",
        skill="말로 주어진 범위를 부등호로 옮기고 그 범위의 정수를 모두 더하기",
        variant_axis={"표현": "이상/이하 · 초과/미만 · 크고/크지 않은 · 작지 않고/작은", "구간": "음수~양수 · 0~양수 · 음수~0 (합이 0이 아닌 것)"},
        discriminates="양 끝의 포함 여부를 정확히 옮기고, 음수와 양수가 함께 있으면 절댓값이 같은 수끼리 상쇄됨을 이용해 합을 구하는가",
        process="절차수행", difficulty=3, time_limit=90, points=5,
        params=[{"name": "k", "values": {"in": list(IS2_ROWS)}}],
        table={"key": "k", "rows": IS2_ROWS},
        derive={"a": "-m", "lo": "a + 1 - iA", "hi": "b - 1 + iB", "n": "hi - lo + 1", "ans": "(lo + hi)*(hi - lo + 1)/2"},
        constraints=["n >= 3", "ans != 0", "abs(ans) <= 45"],
        cost_values=["m", "b", "n", "ans"],
        answer_var="ans",
        verify=["2*ans == (lo + hi)*n", "n == hi - lo + 1"],
        question="x는 {a}{QA} {b}{QB} 수이다. 이 조건을 만족하는 정수 x의 값을 모두 더한 것을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="먼저 조건을 부등호로 옮겨 정수의 범위를 정한다. {S1B}",
        sol2=["조건을 부등호로 나타내면 {a} {SA} x {SB} {b}", "정수 x는 {lo}부터 {hi}까지 {n}개", "{S3}"],
        sol2_fig=steps([{"text": "{a} {SA} x {SB} {b}", "hint": "'{PH}' → {SA}, '{PH2}' → {SB}"},
                        {"text": "x = {XL}  ({n}개)"},
                        {"text": "합 = {ans}", "marks": [{"on": "{ans}", "note": "{MK}"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("mark:2-0")]],
        sol3="{lo}부터 {hi}까지 {n}개의 정수를 순서대로 더하면 (처음 수 + 마지막 수) × 개수 ÷ 2 = ({lo} + {hi}) × {n} ÷ 2 = {ans}{ro(ans)} 같다. 답은 {ans}이다.",
        sol3_fig=steps(["({lo} + {hi}) × {n} ÷ 2 = {ans}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="조건을 부등호로 나타내면 {a} {SA} x {SB} {b}이므로 정수 x는 {lo}부터 {hi}까지 {n}개이다. 이를 모두 더하면 {ans}이다.",
        rubric=[
            {"element": "부등호로 나타내기", "points": 3, "criterion": "조건을 {a} {SA} x {SB} {b}{ro(b)} 옮겼다.", "partial": "한쪽 부등호의 종류만 틀렸으면 1점."},
            {"element": "정수 나열", "points": 2, "criterion": "{lo}부터 {hi}까지 {n}개를 빠짐없이 나열했다.", "partial": "양 끝 처리를 틀렸으면 1점."},
            {"element": "합 구하기", "points": 3, "criterion": "합 {ans}{eul(ans)} 구했다.", "partial": "{PP3}"},      # 갈래별 — pitfalls {PIT3} 와 같은 실수
        ],
        rubric_total=8,
    )


# ═══════════════════════════════════════════════════════════════════ 6. 유리수 계산의 활용 (m1-1-18)
RA = "m1-1-rational-apply"
RA_BASE = {**BASE, "process": "문제해결", "context": "생활맥락", "ops": ["사칙"], "traps": ["부호", "단위"], "prereq": ["유리수의 덧셈과 뺄셈"], "tags": ["유리수의 활용", "온도", "수직선"], "time_limit": 90, "points": 5}


def ra_t1():
    return tpl(RA, 1, RA_BASE,
        title="온도의 변화 — 영하에서 출발해 오르고 내린 뒤의 온도",
        skill="영하 온도를 음수로 나타내고, 오른 만큼 더하고 내린 만큼 빼서 최종 온도를 구하기",
        variant_axis={"시작 온도": "−12~−1 ℃", "변화": "오름 2~15 · 내림 1~12", "결과 부호": "양·음"},
        discriminates="'내려갔다'를 뺄셈으로, 음수에서 시작하는 덧셈·뺄셈을 부호까지 바르게 하는가",
        difficulty=2,
        params=[{"name": "m", "values": {"int": [1, 12]}}, {"name": "u", "values": {"int": [2, 15]}}, {"name": "d", "values": {"int": [1, 12]}}],
        derive={"a": "-m", "mid": "-m + u", "ans": "-m + u - d"},
        constraints=["u != d", "ans != a", "ans != 0"],
        cost_values=["m", "u", "d", "ans"],
        answer_var="ans",
        verify=["ans == a + u - d", "mid == a + u"],
        question="어느 날 아침 기온은 영하 {m} ℃였다. 낮에는 아침보다 {u} ℃ 올랐고, 밤에는 낮보다 {d} ℃ 내려갔다. 밤의 기온은 몇 ℃인지 구하시오.",
        answer="{ans}", answer_alt=["{ans} ℃", "{ans}℃"],
        sol1="영하 {m} ℃는 {a} ℃다. 온도가 오르면 더하고 내리면 빼면 되므로 아침 온도에서 {u}{eul(u)} 더하고 {d}{eul(d)} 빼면 밤의 온도가 된다.",
        sol2=["아침: 영하 {m} ℃ = {a} ℃", "낮: {a} + {u} = {mid} (℃)", "밤: {mid} − {d} = {ans} (℃)"],
        sol2_fig=steps([{"text": "아침 {a} ℃", "hint": "영하 → 음수"}, {"text": "낮: {a} + {u} = {mid}", "hint": "올랐다 → +"}, {"text": "밤: {mid} − {d} = {ans}", "hint": "내려갔다 → −", "marks": [{"on": "{ans}", "note": "부호 확인"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="수직선에서 {a}에서 오른쪽으로 {u}칸, 다시 왼쪽으로 {d}칸 가면 {ans}에 닿는다. 밤의 기온은 {ans} ℃다.",
        sol3_fig=numline("{min(a, ans) - 2}", "{max(mid, 0) + 2}", [{"x": "{a}", "label": "아침"}, {"x": "{mid}", "label": "낮"}, {"x": "{ans}", "label": "밤"}]),
        sol3_anim=[[hl("pt:아침")], [hl("pt:낮")], [hl("pt:밤")]],
        model_answer="아침 기온 영하 {m} ℃는 {a} ℃이다. 낮의 기온은 {a} + {u} = {mid} (℃)이고, 밤의 기온은 {mid} − {d} = {ans} (℃)이다.",
        rubric=[
            {"element": "온도를 유리수로 나타내기", "points": 2, "criterion": "영하 {m} ℃를 {a} ℃로 나타냈다.", "partial": "부호를 빠뜨렸으면 인정하지 않는다."},
            {"element": "변화를 식으로", "points": 3, "criterion": "오른 것은 더하고 내린 것은 빼서 {a} + {u} − {d}{ro(d)} 나타냈다.", "partial": "한 변화의 부호만 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans} ℃를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


def ra_t2():
    return tpl(RA, 2, RA_BASE,
        title="수직선 위 두 점 사이의 거리 — 음수를 나타내는 점을 포함",
        skill="수직선에서 두 수 사이의 거리는 큰 수에서 작은 수를 뺀 값(차의 절댓값)임을 이용해 구하기",
        variant_axis={"두 점": "음수·양수 / 둘 다 음수", "꼴": "정수"},
        discriminates="음수를 나타내는 점까지의 거리를 뺄셈(큰 수 − 작은 수)으로 구하며 부호 처리를 바르게 하는가",
        context="무맥락", process="절차수행", difficulty=2,
        params=[{"name": "sgn", "values": {"in": ["mix", "neg"]}}, {"name": "m", "values": {"int": [1, 12]}}, {"name": "h", "values": {"int": [1, 14]}}],
        table={"key": "sgn", "rows": {"mix": {"isN": 0}, "neg": {"isN": 1}}},
        derive={"a": "-m", "b": "(1 - isN)*(-m + h) + isN*(-m - h)", "big": "max(a, b)", "small": "min(a, b)", "ans": "h"},
        constraints=["b != 0", "abs(b) <= 15", "(isN == 1) or (b > 0)"],
        cost_values=["a", "b", "ans"],
        answer_var="ans",
        verify=["ans == abs(a - b)", "ans == big - small", "ans > 0"],
        question="수직선 위에서 두 수 {a}{wa(a)} {b}{eul(b)} 나타내는 두 점 사이의 거리를 구하시오.",
        figure=numline("{min(a, b) - 2}", "{max(a, b) + 2}", [{"x": "{a}", "label": "A"}, {"x": "{b}", "label": "B"}]),
        answer="{ans}", answer_alt=[],
        sol1="수직선에서 두 점 사이의 거리는 오른쪽 수(큰 수)에서 왼쪽 수(작은 수)를 뺀 값이다. 음수를 뺄 때는 부호에 주의한다.",
        sol2=["두 수 중 큰 수는 {big}, 작은 수는 {small}", "거리 = (큰 수) − (작은 수) = {big} − {pn(small)} = {ans}"],
        sol2_fig=steps([{"text": "{small} < {big}", "hint": "수직선에서 오른쪽이 큰 수"}, {"text": "{big} − {pn(small)} = {ans}", "marks": [{"on": "{pn(small)}", "note": "음수를 빼면 더하는 것"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="{small}에서 오른쪽으로 {ans}칸 가면 {big}에 닿으므로 두 점 사이의 거리는 {ans}이다.",
        sol3_fig=numline("{min(a, b) - 2}", "{max(a, b) + 2}", [{"x": "{a}", "label": "A"}, {"x": "{b}", "label": "B"}], [{"from": "{small}", "to": "{big}"}]),
        sol3_anim=[[hl("seg:0")]],
        model_answer="두 수 중 큰 수는 {big}, 작은 수는 {small}이므로 두 점 사이의 거리는 {big} − {pn(small)} = {ans}이다.",
        rubric=[
            {"element": "큰 수·작은 수 정하기", "points": 2, "criterion": "{small} < {big}{ro(big)} 판단했다.", "partial": "대소를 뒤집었으면 인정하지 않는다."},
            {"element": "거리 구하기", "points": 3, "criterion": "{big} − {pn(small)} = {ans}{ro(ans)} 계산했다.", "partial": "음수를 빼는 부호 처리를 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


def ra_t3():
    return tpl(RA, 3, RA_BASE,
        title="맞히면 +, 틀리면 − 인 점수 게임의 최종 점수",
        skill="맞힌 문제는 양수, 틀린 문제는 음수로 점수를 매겨 최종 점수를 구하기 (음수도 답이 될 수 있음)",
        variant_axis={"배점": "맞힘 2~5 · 틀림 1~4", "문제 수": "8~15", "결과 부호": "양·음"},
        discriminates="틀린 문제의 감점을 음수의 곱으로 나타내고 양수 점수와 합쳐 부호까지 바르게 구하는가",
        difficulty=2,
        params=[{"name": "p", "values": {"int": [2, 5]}}, {"name": "q", "values": {"int": [1, 4]}}, {"name": "n", "values": {"int": [8, 15]}}, {"name": "w", "values": {"int": [1, 14]}}],
        derive={"l": "n - w", "gain": "p*w", "loss": "-q*(n - w)", "ans": "p*w - q*(n - w)"},
        constraints=["l >= 2", "ans != 0", "abs(ans) <= 60"],
        cost_values=["p", "q", "n", "w", "ans"],
        answer_var="ans",
        verify=["ans == p*w - q*l", "w + l == n"],
        question="{n}문제를 푸는 게임에서 한 문제를 맞히면 {p}점을 얻고 틀리면 {q}점을 잃는다. 0점에서 시작하여 {w}문제를 맞히고 나머지를 모두 틀렸을 때, 최종 점수를 구하시오.",
        answer="{ans}", answer_alt=["{ans}점"],
        sol1="얻은 점수는 +, 잃은 점수는 −로 나타낸다. 맞힌 문제 수에 {p}{eul(p)} 곱해 얻은 점수를, 틀린 문제 수에 (−{q})를 곱해 잃은 점수를 구한 뒤 더한다.",
        sol2=["틀린 문제 수: {n} − {w} = {l} (문제)", "얻은 점수: (+{p}) × {w} = {gain}, 잃은 점수: (−{q}) × {l} = {loss}", "최종 점수: {gain} + {pn(loss)} = {ans} (점)"],
        sol2_fig=steps([{"text": "틀린 문제: {n} − {w} = {l}", "hint": "나머지"}, {"text": "(+{p}) × {w} = {gain},  (−{q}) × {l} = {loss}", "hint": "잃은 점수는 음수"}, {"text": "{gain} + {pn(loss)} = {ans}", "marks": [{"on": "{ans}", "note": "부호 확인"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="얻은 {gain}점에서 잃은 {q} × {l} = {abs(loss)}점을 빼면 {ans}점이므로 계산이 맞다. 최종 점수는 {ans}점이다.",
        sol3_fig=steps(["{gain} − {abs(loss)} = {ans}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="틀린 문제는 {n} − {w} = {l}문제이다. 얻은 점수는 (+{p}) × {w} = {gain}(점), 잃은 점수는 (−{q}) × {l} = {loss}(점)이므로 최종 점수는 {gain} + {pn(loss)} = {ans}(점)이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "얻은 점수 (+{p}) × {w}, 잃은 점수 (−{q}) × {l}{ro(l)} 나타냈다.", "partial": "틀린 문제 수를 잘못 구했으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "{gain} + {pn(loss)} = {ans}{eul(ans)} 계산했다.", "partial": "부호 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "최종 점수 {ans}점을 답했다.", "partial": "얻은 점수만 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


# ═══════════════════════════════════════════════════════════════════ 7. 곱셈·나눗셈 기호의 생략 (m1-1-19)
OS = "m1-1-omit-sign"
OS_BASE = {**BASE, "process": "표현", "ops": ["사칙"], "traps": ["구하는대상혼동"], "prereq": ["문자의 사용"], "tags": ["기호의 생략", "문자와 식"]}


def _os1_rows():
    """k1 × a × k2 × b 꼴 — 곱셈 기호를 생략해 ▢ab 로 쓸 때 ▢(계수) = k1 × k2. 같은 문자가 두 번이면 ▢a²b."""
    rows = {}
    letters = [("a", "b"), ("x", "y"), ("a", "c"), ("b", "y")]
    forms = [("k1×a×k2×b", 1, 1), ("a×k1×b×k2", 1, 1), ("k1×a×b×k2", 1, 1), ("a×k1×a×k2", 2, 0), ("k1×b×a×k2×a", 2, 1)]
    for (L1, L2) in letters:
        for fm, e1, e2 in forms:
            toks = fm.split("×")
            lets = "".join(f"{L}{'' if c == 1 else '²'}" for L, c in ((L1, e1), (L2, e2)) if c)
            rows[f"{L1}{L2}|{fm}"] = {"FM": fm, "L1": L1, "L2": L2, "E1": e1, "E2": e2, "LETS": lets, "TOKS": toks}
    return rows


OS1_ROWS = _os1_rows()


def _os1_expr_rows():
    """수까지 넣은 표 — k1, k2 를 파라미터 대신 표에 넣어 EXPR 문자열을 굽는다."""
    rows = {}
    for key, r in OS1_ROWS.items():
        for k1 in (-4, -3, -2, 2, 3, 5):
            for k2 in (-3, -2, 2, 3, 4):
                parts = []
                for t in r["TOKS"]:
                    v = {"k1": k1, "k2": k2}.get(t)
                    parts.append((f"({v})" if v < 0 else str(v)) if v is not None else (r["L1"] if t == "a" else r["L2"]))
                rows[f"{key}|{k1}|{k2}"] = {"EXPR": " × ".join(parts), "k1": k1, "k2": k2, "LETS": r["LETS"], "L1": r["L1"], "E1": r["E1"]}
    return rows


OS1X_ROWS = _os1_expr_rows()


def os_t1():
    return tpl(OS, 1, OS_BASE,
        title="곱셈 기호 생략 — 수는 앞으로 모아 곱하고 문자는 거듭제곱으로: ▢ab 의 ▢",
        skill="문자와 수의 곱에서 × 를 생략할 때 수끼리 먼저 곱해 문자 앞에 쓰고 같은 문자의 곱은 거듭제곱으로 쓰기",
        variant_axis={"수": "k1 −4~5 · k2 −3~4", "문자": "a·b·c·x·y", "꼴": "수·문자 섞인 순서 · 같은 문자 두 번"},
        discriminates="곱셈 기호를 생략할 때 흩어진 수를 모아 한 번 곱해 계수로 쓰고 부호까지 정하는가",
        difficulty=2,
        params=[{"name": "r", "values": {"in": list(OS1X_ROWS)}}],
        table={"key": "r", "rows": OS1X_ROWS},
        derive={"ans": "k1*k2"},
        constraints=["ans != k1", "ans != k2", "abs(ans) <= 20"],
        cost_values=["k1", "k2", "ans"],
        answer_var="ans",
        verify=["ans == k1*k2", "E1 >= 1"],
        question="{EXPR}{eul(EXPR)} 곱셈 기호 ×를 생략하여 나타내면 ▢{LETS}이다. ▢에 알맞은 수를 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="곱셈에서는 곱하는 순서를 바꾸어도 결과가 같으므로 수는 수끼리, 문자는 문자끼리 모을 수 있다. 곱셈 기호를 생략할 때는 수를 먼저 곱해 문자 앞에 쓰고, 같은 문자의 곱은 거듭제곱으로 나타낸다.",
        sol2=["수끼리 모아 곱한다: {k1} × {k2} = {ans}", "문자는 알파벳 순으로, 같은 문자는 거듭제곱으로: {LETS}", "따라서 {EXPR} = {ans}{LETS}이고 ▢ = {ans}"],
        sol2_fig=steps([{"text": "{k1} × {k2} = {ans}", "hint": "수는 수끼리 (부호 주의)", "marks": [{"on": "{ans}", "note": "음수 × 음수 = 양수"}]},
                        {"text": "문자: {LETS}", "hint": "같은 문자는 거듭제곱"},
                        {"text": "{EXPR} = {ans}{LETS}"}]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="{ans}{LETS}에 곱셈 기호를 다시 넣으면 {ans} × {LETS}이고, {ans} = {k1} × {k2}이므로 원래 식과 같다. 답은 {ans}이다.",
        sol3_fig=steps(["{ans}{LETS} = ({k1} × {k2}) × {LETS}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="수끼리 모아 곱하면 {k1} × {k2} = {ans}이고 문자는 {LETS}{ro(LETS)} 묶이므로 {EXPR} = {ans}{LETS}이다. 따라서 ▢ = {ans}이다.",
        rubric=[
            {"element": "수 모으기", "points": 3, "criterion": "흩어진 두 수를 모아 {k1} × {k2} = {ans}{ro(ans)} 계수를 구했다.", "partial": "부호가 틀렸으면 1점."},
            {"element": "답 쓰기", "points": 2, "criterion": "▢ = {ans}{eul(ans)} 답했다.", "partial": "수 하나만 계수로 썼으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


def os_t2():
    return tpl(OS, 2, OS_BASE,
        title="나눗셈 기호 생략 — x ÷ a ÷ b 를 분수로 쓸 때 분모",
        skill="나눗셈을 분수로 바꾸어 ÷ 를 생략할 때 두 번 나눈 것은 분모에 곱해짐을 알기",
        variant_axis={"나누는 수": "2~9 두 개", "문자": "x·a·y", "괄호 식": "있음/없음"},
        discriminates="x ÷ a ÷ b 의 분모가 a × b 임을 알고, 괄호 식은 통째로 분자에 두는가",
        difficulty=2,
        params=[{"name": "L", "values": {"in": ["x", "a", "y"]}}, {"name": "p", "values": {"int": [2, 9]}}, {"name": "q", "values": {"int": [2, 9]}}, {"name": "c", "values": {"in": [0, 1, 3, 5]}}],
        table={"key": "L", "rows": {"x": {"LT": "x"}, "a": {"LT": "a"}, "y": {"LT": "y"}}},
        derive={"ans": "p*q"},
        constraints=["p <= q", "ans != p", "ans != q", "ans != c"],
        cost_values=["p", "q", "ans"],
        answer_var="ans",
        verify=["ans == p*q", "ans > q"],
        question="{QTEXT}" if False else None,   # os_t2_split 에서 괄호 유무별 문면
        answer="{ans}", answer_alt=[],
        sol1="나눗셈은 분수로 나타낼 수 있다. ÷ {p}{eun(p)} 분모에 {p}{eul(p)} 쓰는 것이고, 다시 ÷ {q}{eul(q)} 하면 분모에 {q}{eul(q)} 한 번 더 곱한다. 괄호로 묶인 식은 그 전체가 분자다.",
        sol2=["÷ {p} → 분모에 {p}", "÷ {q} → 분모에 {q}{eul(q)} 곱함: 분모 = {p} × {q} = {ans}", "따라서 ▢ = {ans}"],
        sol2_fig=steps([{"text": "÷ {p} ÷ {q}", "hint": "나눌 때마다 분모에 곱한다"}, {"text": "분모 = {p} × {q} = {ans}", "marks": [{"on": "{ans}", "note": "더하지 말고 곱한다"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="분모가 {ans}인 분수에 ÷ 를 다시 넣어 읽으면 {p}로 나누고 {q}로 나눈 것이므로 처음 식과 같다. 답은 {ans}이다.",
        sol3_fig=steps(["1/{ans} = (1/{p}) × (1/{q})"]),
        sol3_anim=[[reveal(0)]],
        model_answer="÷ {p} ÷ {q}{eun(q)} 분모에 {p}{wa(p)} {q}{eul(q)} 곱하는 것이므로 분모는 {p} × {q} = {ans}이다. 따라서 ▢ = {ans}이다.",
        rubric=[
            {"element": "분수로 나타내기", "points": 3, "criterion": "두 번 나눈 것을 분모의 곱 {p} × {q}{ro(q)} 나타냈다.", "partial": "분모를 {p} + {q}{ro(q)} 썼으면 인정하지 않는다."},
            {"element": "답 쓰기", "points": 2, "criterion": "▢ = {ans}{eul(ans)} 답했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def os_t2_split(t):
    """괄호 식 유무로 문면이 다르다 → t2(문자 하나)·t6(괄호 식)."""
    out = []
    for no, cs, q in ((2, [0], "{LT} ÷ {p} ÷ {q}{eul(q)} 나눗셈 기호 ÷를 생략하여 분수 꼴로 나타내면 분자는 {LT}, 분모는 ▢이다. ▢에 알맞은 수를 구하시오."),
                      (6, [1, 3, 5], "({LT} + {c}) ÷ {p} ÷ {q}{eul(q)} 나눗셈 기호 ÷를 생략하여 분수 꼴로 나타내면 분자는 {LT} + {c}, 분모는 ▢이다. ▢에 알맞은 수를 구하시오.")):
        u = dict(t)
        u["id"] = f"{OS}-t{no}"
        u["params"] = [p for p in t["params"] if p["name"] != "c"] + [{"name": "c", "values": {"in": cs}}]
        u["question"] = q
        u["title"] = t["title"] + (" (문자 하나)" if no == 2 else " (괄호 식)")
        out.append(u)
    return out


def os_t3():
    return tpl(OS, 3, OS_BASE,
        title="기호를 생략한 식에 수 대입하기 — 3a² 과 (3a)² 의 구분",
        skill="기호가 생략된 식의 뜻을 되살려 문자에 수를 대입해 값을 구하기 (음수는 괄호로 대입)",
        variant_axis={"꼴": "ka² / (ka)² / ka + m / k/a", "대입 값": "−6~6 (0 제외)"},
        discriminates="ka² 은 k × a × a, (ka)² 은 (k × a) × (k × a) 임을 구분하고 음수를 괄호로 대입하는가",
        process="절차수행", difficulty=2,
        params=[{"name": "f", "values": {"in": ["sq", "psq", "lin"]}}, {"name": "k", "values": {"int": [2, 5]}}, {"name": "a", "values": {"int": [-6, 6]}}, {"name": "m", "values": {"int": [1, 9]}}],
        table={"key": "f", "rows": {"sq": {"w1": 1, "w2": 0, "w3": 0, "FT": "sq"}, "psq": {"w1": 0, "w2": 1, "w3": 0, "FT": "psq"}, "lin": {"w1": 0, "w2": 0, "w3": 1, "FT": "lin"}}},
        derive={"ans": "w1*k*a*a + w2*(k*a)**2 + w3*(k*a + m)", "v1": "k*a*a", "v2": "(k*a)**2", "v3": "k*a + m"},
        constraints=["a != 0", "abs(ans) <= 400", "abs(a) != 1"],
        cost_values=["k", "a", "ans"],
        answer_var="ans",
        verify=["ans == w1*v1 + w2*v2 + w3*v3", "v1 != v2"],
        question=None,   # 꼴별 문면 — os_t3_split
        answer="{ans}", answer_alt=[],
        sol1="기호가 생략된 식은 원래의 곱셈·나눗셈으로 되돌려 읽는다. {k}a²은 {k} × a × a이고 ({k}a)²은 ({k} × a) × ({k} × a)이며, 문자에 음수를 대입할 때는 반드시 괄호를 쓴다.",
        sol2=["식의 뜻을 되살린다: {k}a² = {k} × a × a,  ({k}a)² = ({k} × a)²,  {k}a + {m} = {k} × a + {m}", "a = {a}{eul(a)} 괄호를 써서 대입한다", "계산하면 구하는 값은 {ans}"],
        sol2_fig=steps([{"text": "{k}a² = {k} × a × a  /  ({k}a)² = ({k} × a) × ({k} × a)", "hint": "제곱이 붙는 범위가 다르다"},
                        {"text": "a = {pn(a)} 대입", "marks": [{"on": "{pn(a)}", "note": "음수는 괄호"}]},
                        {"text": "값 = {ans}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)]],
        sol3="세 식의 값을 모두 구해 보면 {k}a² = {v1}, ({k}a)² = {v2}, {k}a + {m} = {v3}{ro(v3)} 서로 다르다. 묻는 식의 값은 {ans}이다.",
        sol3_fig=steps(["{k}a² = {v1},  ({k}a)² = {v2},  {k}a + {m} = {v3}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="기호를 되살려 a = {a}{eul(a)} 괄호를 써서 대입하면 구하는 식의 값은 {ans}이다.",
        rubric=[
            {"element": "식의 뜻 되살리기", "points": 3, "criterion": "생략된 곱셈을 되살려 식을 바르게 읽었다.", "partial": "{k}a²과 ({k}a)²을 혼동했으면 인정하지 않는다."},
            {"element": "대입과 계산", "points": 2, "criterion": "a = {a}{eul(a)} 괄호를 써서 대입해 {ans}{eul(ans)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


def os_t3_split(t):
    """묻는 식이 꼴마다 달라 문면을 세 틀(t3·t4·t5)로 나눈다."""
    out = []
    for no, key, q in ((3, "sq", "a = {a}일 때, {k}a²의 값을 구하시오."),
                       (4, "psq", "a = {a}일 때, ({k}a)²의 값을 구하시오."),
                       (5, "lin", "a = {a}일 때, {k}a + {m}의 값을 구하시오.")):
        u = dict(t)
        u["id"] = f"{OS}-t{no}"
        u["params"] = [p for p in t["params"] if p["name"] not in ("f", "m")] + [{"name": "f", "values": {"in": [key]}}, {"name": "m", "values": {"in": [1] if key != "lin" else [1, 2, 3, 4, 5, 6, 7, 8, 9]}}]
        u["question"] = q
        u["title"] = t["title"] + {"sq": " — ka²", "psq": " — (ka)²", "lin": " — ka + m"}[key]
        out.append(u)
    return out


# ═══════════════════════════════════════════════════════════════════ 8. 등식의 성질 (m1-1-25)
EP = "m1-1-eq-property"
EP_BASE = {**BASE, "process": "절차수행", "ops": ["방정식"], "traps": ["부호", "역연산"], "prereq": ["등식", "문자와 식"], "tags": ["등식의 성질", "방정식"], "time_limit": 90}


def ep_t1():
    return tpl(EP, 1, EP_BASE,
        title="등식의 성질로 ax + b = c 풀기 — 양변에 같은 수를 더하고(빼고) 같은 수로 나누기",
        skill="등식의 양변에 같은 수를 더하거나 빼고, 0이 아닌 같은 수로 나누어도 등식이 성립함을 이용해 일차방정식의 해 구하기",
        variant_axis={"계수": "a 2~9", "상수": "b −12~12", "해": "−8~8"},
        discriminates="'양변에 같은 수를 더하거나 빼기 → 양변을 같은 수로 나누기'의 순서로 등식의 성질을 적용하는가",
        difficulty=2,
        params=[{"name": "a", "values": {"int": [2, 9]}}, {"name": "b", "values": {"int": [-12, 12]}}, {"name": "x", "values": {"int": [-8, 8]}}],
        derive={"c": "a*x + b", "nb": "-b", "ax": "a*x"},
        constraints=["b != 0", "x != 0", "c != 0", "abs(c) <= 60"],
        cost_values=["a", "b", "c", "x"],
        answer_var="x",
        verify=["a*ans + b == c", "ans*a == ax"],
        question="등식의 성질을 이용하여 방정식 {a}x {sgn(b)} = {c}{eul(c)} 푸시오.",
        answer="{x}", answer_alt=["x = {x}"],
        sol1="등식의 양변에 같은 수를 더하거나 빼도, 0이 아닌 같은 수를 곱하거나 나누어도 등식은 성립한다. 먼저 상수항 {b}{eul(b)} 없애기 위해 양변에 {nb}{eul(nb)} 더하고(즉 {b}{eul(b)} 빼고), 그다음 x의 계수 {a}로 양변을 나눈다.",
        sol2=["양변에 {nb}{eul(nb)} 더하면 {a}x {sgn(b)} {sgn(nb)} = {c} {sgn(nb)}", "정리하면 {a}x = {ax}", "양변을 {a}로 나누면 x = {x}"],
        sol2_fig=steps([{"text": "{a}x {sgn(b)} = {c}", "hint": "상수항부터 없앤다"},
                        {"text": "{a}x = {ax}", "hint": "양변에 {nb}{eul(nb)} 더함", "marks": [{"on": "{ax}", "note": "양변에 같은 수"}]},
                        {"text": "x = {x}", "hint": "양변을 {a}로 나눔"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")]],
        sol3="x = {x}{eul(x)} 원래 등식에 대입하면 {a} × {pn(x)} {sgn(b)} = {c}{ro(c)} 양변이 같다. 따라서 해는 x = {x}이다.",
        sol3_fig=steps(["{a} × {pn(x)} {sgn(b)} = {c}  ✓"]),
        sol3_anim=[[reveal(0)]],
        model_answer="양변에 {nb}{eul(nb)} 더하면 {a}x = {ax}이고, 양변을 {a}로 나누면 x = {x}이다.",
        rubric=[
            {"element": "상수항 없애기", "points": 3, "criterion": "양변에 같은 수 {nb}{eul(nb)} 더해 {a}x = {ax}{eul(ax)} 얻었다.", "partial": "한쪽 변에만 더했으면 인정하지 않는다."},
            {"element": "계수로 나누기", "points": 2, "criterion": "양변을 {a}로 나누어 x = {x}{eul(x)} 얻었다.", "partial": "계수를 빼거나 곱했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "해 x = {x}{eul(x)} 답했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


def ep_t2():
    return tpl(EP, 2, EP_BASE,
        title="등식의 성질로 x/a + b = c 풀기 — 양변에서 빼고 같은 수를 곱하기",
        skill="분모가 있는 방정식에서 양변에 같은 수를 빼고 같은 수를 곱해 해를 구하기",
        variant_axis={"분모": "2~9", "상수": "−9~9", "해": "분모의 배수"},
        discriminates="양변을 같은 수로 곱할 때 상수항까지 함께 곱하지 않도록 먼저 상수항을 옮기는가",
        difficulty=2,
        params=[{"name": "a", "values": {"int": [2, 9]}}, {"name": "b", "values": {"int": [-9, 9]}}, {"name": "q", "values": {"int": [-7, 7]}}],
        derive={"x": "a*q", "c": "q + b", "nb": "-b", "cb": "c - b"},
        constraints=["b != 0", "q != 0", "c != 0", "abs(x) <= 60"],
        cost_values=["a", "b", "c", "x"],
        answer_var="x",
        verify=["ans/a + b == c", "ans == a*q"],
        question="등식의 성질을 이용하여 방정식 x/{a} {sgn(b)} = {c}{eul(c)} 푸시오.",
        answer="{x}", answer_alt=["x = {x}"],
        sol1="양변에 같은 수를 더하거나 빼고, 같은 수를 곱해도 등식은 성립한다. 먼저 양변에 {nb}{eul(nb)} 더해 상수항을 없앤 뒤, 분모 {a}{eul(a)} 없애기 위해 양변에 {a}{eul(a)} 곱한다. 곱하기 전에 상수항을 먼저 옮기는 것이 실수를 줄인다.",
        sol2=["양변에 {nb}{eul(nb)} 더하면 x/{a} = {cb}", "양변에 {a}{eul(a)} 곱하면 x = {cb} × {a}", "따라서 x = {x}"],
        sol2_fig=steps([{"text": "x/{a} {sgn(b)} = {c}", "hint": "상수항부터"},
                        {"text": "x/{a} = {cb}", "hint": "양변에 {nb}{eul(nb)} 더함"},
                        {"text": "x = {cb} × {a} = {x}", "hint": "양변에 {a}{eul(a)} 곱함", "marks": [{"on": "× {a}", "note": "양변 모두에"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")]],
        sol3="x = {x}{eul(x)} 대입하면 {x} ÷ {a} {sgn(b)} = {q} {sgn(b)} = {c}{ro(c)} 양변이 같다. 따라서 해는 x = {x}이다.",
        sol3_fig=steps(["{x} ÷ {a} {sgn(b)} = {c}  ✓"]),
        sol3_anim=[[reveal(0)]],
        model_answer="양변에 {nb}{eul(nb)} 더하면 x/{a} = {cb}이고, 양변에 {a}{eul(a)} 곱하면 x = {x}이다.",
        rubric=[
            {"element": "상수항 없애기", "points": 3, "criterion": "양변에 {nb}{eul(nb)} 더해 x/{a} = {cb}{eul(cb)} 얻었다.", "partial": "한쪽 변에만 더했으면 인정하지 않는다."},
            {"element": "같은 수 곱하기", "points": 2, "criterion": "양변에 {a}{eul(a)} 곱해 x = {x}{eul(x)} 얻었다.", "partial": "상수항을 옮기기 전에 곱하면서 상수항에는 곱하지 않았으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "해 x = {x}{eul(x)} 답했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


# ═══════════════════════════════════════════════════════════════════ 9. 그래프 (m1-1-31)
GR = "m1-1-graph"
GR_BASE = {**BASE, "process": "추론", "context": "생활맥락", "ops": ["비례"], "traps": ["구하는대상혼동", "단위"], "prereq": ["좌표평면", "정비례"], "tags": ["그래프", "그래프의 해석"], "time_limit": 90, "points": 5}


def gr_t1():
    return tpl(GR, 1, GR_BASE,
        title="물통에 물을 채우는 그래프 읽기 — 일정하게 늘어나는 높이",
        skill="시간에 따라 일정하게 늘어나는 양의 그래프(원점을 지나는 직선)에서 주어진 시각의 값을 읽어 내기",
        variant_axis={"채우는 시간": "4~12분", "최종 높이": "분당 2~6 cm", "묻는 시각": "중간 시각"},
        discriminates="그래프가 원점을 지나는 직선일 때 1분당 늘어나는 양이 일정함을 써서 중간 값을 구하는가",
        difficulty=2,
        params=[{"name": "T", "values": {"int": [4, 12]}}, {"name": "r", "values": {"int": [2, 6]}}, {"name": "t", "values": {"int": [1, 11]}}],
        derive={"H": "r*T", "ans": "r*t"},
        constraints=["t < T", "t != 1", "H <= 60"],
        cost_values=["T", "H", "t", "ans"],
        answer_var="ans",
        verify=["ans*T == H*t", "ans == r*t"],
        question="빈 물통에 일정한 빠르기로 물을 넣는다. 물을 넣기 시작한 지 x분 후의 물의 높이를 y cm라 할 때, 그래프는 원점을 지나는 직선이고 {T}분 후의 높이는 {H} cm였다. 물을 넣기 시작한 지 {t}분 후의 물의 높이를 구하시오.",
        figure=[{"fn": "coordplane", "args": {"x": [0, "{T + 1}"], "y": [0, "{H + r}"], "points": [{"name": "A", "coord": ["{T}", "{H}"]}],
                                             "lines": [{"points": [[0, 0], ["{T}", "{H}"]]}], "labels": []}}],
        answer="{ans}", answer_alt=["{ans}cm", "{ans} cm"],
        sol1="그래프가 원점을 지나는 직선이면 물의 높이는 시간에 정비례한다. {T}분에 {H} cm이므로 1분에 {r} cm씩 높아지고, {t}분 후에는 그 {t}배가 된다.",
        sol2=["1분 동안 높아지는 높이: {H} ÷ {T} = {r} (cm)", "{t}분 후의 높이: {r} × {t} = {ans} (cm)"],
        sol2_fig=steps([{"text": "{H} ÷ {T} = {r}", "hint": "1분당 높이"}, {"text": "{r} × {t} = {ans}", "marks": [{"on": "{ans}", "note": "그래프에서 x = {t}인 점의 y"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="{t} : {T} = {ans} : {H}{ika(H)} 되어 두 비가 같으므로 정비례 관계에 맞는다. 답은 {ans} cm이다.",
        sol3_fig=steps(["{t} : {T} = {ans} : {H}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="그래프가 원점을 지나는 직선이므로 높이는 시간에 정비례한다. 1분에 {H} ÷ {T} = {r} (cm)씩 높아지므로 {t}분 후의 높이는 {r} × {t} = {ans} (cm)이다.",
        rubric=[
            {"element": "그래프 해석", "points": 3, "criterion": "원점을 지나는 직선이므로 1분당 {r} cm씩 일정하게 높아짐을 밝혔다.", "partial": "정비례임을 쓰지 않고 값만 구했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{t}분 후의 높이 {ans} cm를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def gr_t2():
    return tpl(GR, 2, GR_BASE,
        title="거리–시간 그래프에서 멈춰 있던 시간 읽기",
        skill="시간에 따른 거리 그래프에서 수평인 부분이 '멈춤'을 뜻함을 알고 그 시간을 읽기",
        variant_axis={"전체 거리": "600~1500 m", "전체 시간": "12~30분", "멈춘 구간": "2~8분"},
        discriminates="그래프가 수평인 구간에서는 거리가 변하지 않으므로 멈춘 것임을 읽고, 그 구간의 길이를 시간으로 구하는가",
        difficulty=2,
        params=[{"name": "T", "values": {"int": [12, 30]}}, {"name": "D", "values": {"in": [600, 800, 900, 1000, 1200, 1500]}}, {"name": "t1", "values": {"int": [3, 12]}}, {"name": "s", "values": {"int": [2, 8]}}],
        derive={"t2": "t1 + s", "rest": "T - t1 - s", "d1": "floor(D*t1/(T - s)/10)*10", "ans": "s"},
        constraints=["rest >= 3", "d1 >= 100", "D - d1 >= 100"],
        cost_values=["T", "D", "s"],
        answer_var="ans",
        verify=["ans == t2 - t1", "t1 + ans + rest == T"],
        question="지우가 집에서 출발하여 {D} m 떨어진 도서관까지 걸어가는 데 {T}분이 걸렸다. 다음은 출발한 지 x분 후 집에서 떨어진 거리를 y m라 할 때의 그래프이다. 지우가 도중에 멈춰 있던 시간은 몇 분인지 구하시오.",
        figure=[{"fn": "coordplane", "args": {"x": [0, "{T + 2}"], "y": [0, "{D + 100}"],
                                             "points": [{"name": "P", "coord": ["{t1}", "{d1}"]}, {"name": "Q", "coord": ["{t2}", "{d1}"]}, {"name": "R", "coord": ["{T}", "{D}"]}],
                                             "lines": [{"points": [[0, 0], ["{t1}", "{d1}"], ["{t2}", "{d1}"], ["{T}", "{D}"]]}]}}],
        answer="{ans}", answer_alt=["{ans}분"],
        sol1="거리–시간 그래프에서 선이 오른쪽 위로 올라가면 움직이는 것이고, 수평이면 거리가 변하지 않으므로 멈춰 있는 것이다. 수평인 부분이 x축에서 차지하는 길이가 멈춰 있던 시간이다.",
        sol2=["그래프가 수평인 구간은 x = {t1}부터 x = {t2}까지 (거리 {d1} m 그대로)", "멈춰 있던 시간: {t2} − {t1} = {ans} (분)"],
        sol2_fig=steps([{"text": "수평 구간: {t1}분 ~ {t2}분", "hint": "거리가 {d1} m로 변하지 않음"}, {"text": "{t2} − {t1} = {ans}", "marks": [{"on": "{ans}", "note": "y의 차가 아니라 x의 차"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="멈추기 전에 걸은 {t1}분, 멈춰 있던 {ans}분, 다시 걸은 {rest}분을 모두 더하면 {t1} + {ans} + {rest} = {T}(분)으로 전체 걸린 시간과 같다. 답은 {ans}분이다.",
        sol3_fig=steps(["{t1} + {ans} + {rest} = {T}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="그래프가 수평인 x = {t1}부터 x = {t2}까지는 거리가 {d1} m로 변하지 않으므로 멈춰 있던 것이다. 따라서 멈춰 있던 시간은 {t2} − {t1} = {ans}(분)이다.",
        rubric=[
            {"element": "그래프 해석", "points": 3, "criterion": "수평인 구간이 멈춘 것임을 밝히고 그 구간 {t1}~{t2}분을 찾았다.", "partial": "구간의 한쪽 끝만 맞게 읽었으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{t2} − {t1} = {ans}분을 구했다.", "partial": "거리의 차를 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# ═══════════════════════════════════════════════════════════════════ 생성
def main():
    out = []
    t3 = pw_t3_fix(pw_t3())
    out.append(seed(PW, "거듭제곱 — 값·곱을 거듭제곱으로·지수/밑 거꾸로", ["m1-1-02"], "교과서 기본 예제 유형. 값·표기·역산의 세 축.", [pw_t1(), pw_t2(), t3], schema_name="거듭제곱의 뜻과 표현"))
    out.append(seed(SG, "양수와 음수 — 부호로 나타내기·수직선·개수 세기", ["m1-1-09"], "반대되는 양의 표현, 수직선 위치, 부호로 가르기. 0은 어느 쪽도 아님을 판별 포인트로.", [sg_t1(), sg_t2(), sg_t3()], schema_name="양수와 음수의 뜻"))
    ir2 = ir_t2()
    out.append(seed(IR, "정수와 유리수 — 분류·두 수 사이의 정수", ["m1-1-10"], "정수인 분수(6/3)·0을 함정으로 둔 분류 세기와 두 정수 사이의 정수 개수(사이/이상 이하).", [ir_t1()] + ir_t2_split(ir2), schema_name="정수와 유리수의 분류"))
    out.append(seed(OD, "수의 대소 관계 — 두 수 비교·순서 나열·음수의 대소", ["m1-1-13"], "음수끼리는 절댓값이 클수록 작다는 점을 세 축(둘 비교·다섯 수 나열·−a와 −b)으로.", [od_t1(), od_t2(), od_t3()], schema_name="유리수의 대소 관계"))
    out.append(seed(IS, "부등호의 사용 — 조건을 만족하는 정수의 개수·합", ["m1-1-14"], "이상·이하·초과·미만·크지 않다·작지 않다를 부등호로 옮기는 훈련. 답은 정수의 개수와 합.", [is_t1(), is_t2()], schema_name="부등호로 나타내기"))
    out.append(seed(RA, "유리수 계산의 활용 — 온도 변화·수직선 거리·점수 게임", ["m1-1-18"], "실생활 맥락(온도·게임)과 수직선 거리. 음수 결과도 답이 된다.", [ra_t1(), ra_t2(), ra_t3()], schema_name="유리수의 덧셈과 뺄셈의 활용"))
    os3 = os_t3()
    out.append(seed(OS, "곱셈·나눗셈 기호의 생략 — 계수 모으기·분모·대입", ["m1-1-19"], "생성기가 식 답을 검산하지 못하므로(3ab 파싱 불가) ▢ 를 묻는 수치 답으로 설계: 계수(t1)·분모(t2·t6)·대입(t3~t5).", [os_t1()] + os_t2_split(os_t2()) + os_t3_split(os3), schema_name="곱셈과 나눗셈 기호의 생략"))
    out.append(seed(EP, "등식의 성질 — 성질을 이용해 방정식 풀기", ["m1-1-25"], "'양변에 같은 수' 를 명시한 단계 해설. ax + b = c 와 x/a + b = c 두 꼴.", [ep_t1(), ep_t2()], schema_name="등식의 성질"))
    out.append(seed(GR, "그래프 — 물 높이 그래프·멈춘 시간 읽기", ["m1-1-31"], "원점을 지나는 직선(정비례)과 꺾인 선(멈춤) 두 유형. 수치는 문면에 두어 그림만 다른 문항이 겹치지 않게 했다.", [gr_t1(), gr_t2()], schema_name="그래프의 해석"))
    for s in out:
        dump(with_pitfalls(s))


if __name__ == "__main__":
    main()
