# itemfactory/tools/mkseed_m1_stat2.py — 통계 시드 생성기 2: 도수분포표 · 상대도수 · 중앙값·최빈값 (v1.0 · 2026-09-11)
#
#   python itemfactory/tools/mkseed_m1_stat2.py
#     → seeds/m1-2-freq-table.json (5틀) · seeds/m1-2-relative-freq.json (5틀) · seeds/m1-2-median-mode.json (5틀)
#
# 통계 도식(막대 강조)은 미구현 — 문항 도형은 table, 해설은 table·steps 로. 자료맥락은 요즘 상황(스마트폰 사용 시간·통학 시간·
# 수행평가·러닝 크루·윗몸 일으키기·독서 쪽수). 문면에 수치가 반드시 있어야 하므로(DUP) 표의 도수를 발문에도 차례로 적는다.
# 중앙값·최빈값은 답이 자료 안의 값이라 단답이면 R-05(정답 노출)에 걸린다 → 그 두 틀은 5지선다(오답 = 정렬 안 함·가운데 자리·평균 등).
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, table, with_pitfalls  # noqa: E402

SCHEMA_FREQ = "0acbe11b-6d61-4d78-8294-b3876d8f3795"      # 도수분포표 특정 계급 백분율 (grade B)
SCHEMA_REL = "42626851-d5ec-4314-bf93-ec6fc25e2e21"       # 도수의 총합이 다른 두 자료의 상대도수의 비 (grade A)
SCHEMA_MED = "a54170b6-d2ce-49db-a2ed-ba80bd1656a9"       # 중앙값 조건으로 미지 변량 구하기 (grade B)

BASE = {"process": "문제해결", "context": "자료맥락", "ops": ["통계", "사칙"], "time_limit": 100, "points": 5}


def tpl(seed_id, no, *bases, **kw):
    t = dict(BASE)
    for b in bases:
        t.update(b)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


# ═══════════════════════════════════════════════════════════════════ 공통 — 자료 맥락 (표 행: 이름·단위·계급 시작·계급 크기만, 수치 자리표시자 금지)
CTX = {
    "1": {"S": "어느 반 학생", "W": "하루 스마트폰 사용 시간", "U": "분", "UH": "분", "UD": "분이다", "UI": "분이", "S0": 0, "CW": 30, "ADJ": "긴"},
    "2": {"S": "어느 학교 학생", "W": "통학 시간", "U": "분", "UH": "분", "UD": "분이다", "UI": "분이", "S0": 0, "CW": 10, "ADJ": "긴"},
    "3": {"S": "어느 반 학생", "W": "수학 수행평가 점수", "U": "점", "UH": "점", "UD": "점이다", "UI": "점이", "S0": 50, "CW": 10, "ADJ": "높은"},
    "4": {"S": "어느 러닝 크루 회원", "W": "일주일 동안 달린 거리", "U": " km", "UH": "km", "UD": " km다", "UI": " km가", "S0": 0, "CW": 5, "ADJ": "긴"},
    "5": {"S": "어느 반 학생", "W": "윗몸 일으키기 횟수", "U": "회", "UH": "회", "UD": "회다", "UI": "회가", "S0": 10, "CW": 10, "ADJ": "많은"},
    "6": {"S": "어느 동아리 회원", "W": "한 달 동안 읽은 책의 쪽수", "U": "쪽", "UH": "쪽", "UD": "쪽이다", "UI": "쪽이", "S0": 100, "CW": 100, "ADJ": "많은"},
}
CLS = ["{S0} 이상 ~ {S0 + CW} 미만", "{S0 + CW} 이상 ~ {S0 + 2*CW} 미만", "{S0 + 2*CW} 이상 ~ {S0 + 3*CW} 미만",
       "{S0 + 3*CW} 이상 ~ {S0 + 4*CW} 미만", "{S0 + 4*CW} 이상 ~ {S0 + 5*CW} 미만"]
CLS_HEAD = ["{W}({UH})", "도수(명)"]


def ftable(cells, total=None, head=None):
    rows = [[c, v] for c, v in zip(CLS, cells)]
    if total is not None:
        rows.append(["합계", total])
    return table(head or CLS_HEAD, rows)


def weights(prefix, on):
    """표 행용 0/1 가중치 — on 에 든 계급 번호(1~5)만 1."""
    return {f"{prefix}{i}": (1 if i in on else 0) for i in range(1, 6)}


FT = dict(prereq=["도수분포표 읽기", "전체 도수 = 각 계급의 도수의 합"], traps=["조건누락", "구하는대상혼동"], tags=["도수분포표", "도수"])


# ═══════════════════════════════════════════════════════════════════ 1. 도수분포표
def ft_t1():
    return tpl("m1-2-freq-table", 1, FT,
        title="전체 도수로 빠진 도수 A 구하기",
        skill="(전체 도수) = (각 계급의 도수의 합) — 빠진 도수는 전체에서 나머지를 뺀다",
        variant_axis={"구하는 것": "빠진 도수", "맥락": "스마트폰·통학·수행평가·러닝·윗몸·독서"},
        discriminates="도수의 합이 전체 도수와 같다는 것을 식으로 옮기는가",
        qtype="short", difficulty=1, pool_target=300,
        params=[{"name": "c", "values": {"in": list(CTX)}}, {"name": "f1", "values": {"int": [1, 9]}}, {"name": "f2", "values": {"int": [2, 12]}},
                {"name": "f3", "values": {"int": [2, 12]}}, {"name": "f4", "values": {"int": [1, 9]}}, {"name": "f5", "values": {"int": [1, 6]}}],
        table={"key": "c", "rows": CTX},
        derive={"N": "f1 + f2 + f3 + f4 + f5", "R": "f1 + f2 + f4 + f5"},
        constraints=["f3 != f1", "f3 != f2", "f3 != f4", "f3 != f5", "f3 != N", "N >= 12", "N <= 40", "f1 != f2", "f4 != f5"],
        cost_values=["f1", "f2", "f3", "f4", "f5", "N"],
        relation="X + f1 + f2 + f4 + f5 - N", unknown="X", answer_var="f3",
        verify=["f1 + f2 + ans + f4 + f5 == N"],
        question="다음은 {S} {N}명의 {W}{eul(W)} 조사하여 나타낸 도수분포표이다. 각 계급의 도수가 차례로 {f1}명, {f2}명, A명, {f4}명, {f5}명일 때, A의 값을 구하시오.",
        figure=ftable(["{f1}", "{f2}", "A", "{f4}", "{f5}"], total="{N}"),
        answer="{f3}", answer_alt=["{f3}명"],
        sol1="도수분포표에서 각 계급의 도수를 모두 더하면 전체 도수 {N}{ika(N)} 된다. 도수 하나가 A로 비어 있으므로, 나머지 네 계급의 도수를 더해 전체에서 빼면 A가 나온다.",
        sol1_fig=ftable(["{f1}", "{f2}", "A", "{f4}", "{f5}"], total="{N}"),
        sol2=[
            "전체 도수가 {N}이므로 {f1} + {f2} + A + {f4} + {f5} = {N}",
            "알고 있는 네 계급의 도수의 합은 {f1} + {f2} + {f4} + {f5} = {R}",
            "따라서 A = {N} − {R} = {f3}",
        ],
        sol2_fig=steps([
            {"text": "{f1} + {f2} + A + {f4} + {f5} = {N}", "hint": "도수의 합 = 전체"},
            {"text": "{R} + A = {N}", "hint": "네 계급의 합 {R}"},
            {"text": "A = {f3}", "marks": [{"on": "{f3}", "note": "{N} − {R}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="A = {f3}{eul(f3)} 넣어 도수를 다시 더하면 {f1} + {f2} + {f3} + {f4} + {f5} = {N}{ro(N)} 전체 도수와 같다. 답은 {f3}이다.",
        sol3_fig=steps(["{f1} + {f2} + {f3} + {f4} + {f5} = {N}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="각 계급의 도수의 합은 전체 도수 {N}{wa(N)} 같으므로 {f1} + {f2} + A + {f4} + {f5} = {N}이다. {R} + A = {N}에서 A = {N} − {R} = {f3}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "도수의 합이 전체 도수 {N}{wa(N)} 같음을 이용해 {f1} + {f2} + A + {f4} + {f5} = {N}{eul(N)} 세웠다.", "partial": "합이 전체와 같다는 뜻만 적고 식을 세우지 못했으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "네 계급의 도수의 합 {R}{eul(R)} 구해 A = {N} − {R} = {f3}{eul(f3)} 얻었다.", "partial": "덧셈·뺄셈 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "A = {f3}{ro(f3)} 답했다.", "partial": "다른 값을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


DIR = {"up": {"DIRW": "이상", "isDn": 0}, "dn": {"DIRW": "미만", "isDn": 1}}
KROW = {str(k): weights("w", set(range(k, 6))) for k in (2, 3, 4)}     # w_i = 1 이면 그 계급이 경계 이상


def ft_t2():
    return tpl("m1-2-freq-table", 2, FT,
        title="어떤 값 이상(미만)인 학생의 백분율 구하기",
        skill="해당하는 계급의 도수를 더한 뒤 전체 도수로 나누어 100을 곱한다",
        variant_axis={"구하는 것": "백분율", "경계": "이상·미만 × 세 경계", "맥락": "6가지"},
        discriminates="경계가 속하는 계급을 '이상·미만'에 맞게 고르고 전체 도수로 나누는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "c", "values": {"in": list(CTX)}}, {"name": "d", "values": {"in": list(DIR)}}, {"name": "k", "values": {"in": [2, 3, 4]}},
                {"name": "nn", "values": {"in": [20, 25, 50]}}, {"name": "g1", "values": {"int": [1, 7]}}, {"name": "g2", "values": {"int": [1, 7]}},
                {"name": "g3", "values": {"int": [1, 7]}}, {"name": "g4", "values": {"int": [1, 7]}}],
        table=[{"key": "c", "rows": CTX}, {"key": "d", "rows": DIR}, {"key": "k", "rows": KROW}],
        derive={"m": "1 + floor(nn/50)", "f1": "m*g1", "f2": "m*g2", "f3": "m*g3", "f4": "m*g4", "f5": "nn - m*(g1 + g2 + g3 + g4)",
                "b": "S0 + (k - 1)*CW", "cu": "w1*f1 + w2*f2 + w3*f3 + w4*f4 + w5*f5", "cnt": "cu*(1 - isDn) + (nn - cu)*isDn", "p": "100*cnt/nn"},
        constraints=["f5 >= 1", "f5 <= 18", "p == floor(p)", "p != f1", "p != f2", "p != f3", "p != f4", "p != f5", "p != nn", "p != b", "cnt != nn", "cnt > 0", "p != cnt", "f1 != f2", "f3 != f4"],
        cost_values=["f1", "f2", "f3", "f4", "f5", "nn", "cnt", "p"],
        relation="X*nn - 100*cnt", unknown="X", answer_var="p",
        verify=["ans*nn == 100*cnt"],
        question="다음은 {S} {nn}명의 {W}{eul(W)} 조사하여 나타낸 도수분포표이다. 각 계급의 도수가 차례로 {f1}명, {f2}명, {f3}명, {f4}명, {f5}명일 때, {W}{ika(W)} {b}{U} {DIRW}인 학생은 전체의 몇 %인지 구하시오.",
        figure=ftable(["{f1}", "{f2}", "{f3}", "{f4}", "{f5}"], total="{nn}"),
        answer="{p}", answer_alt=["{p}%", "{p} %"],
        sol1="'{b}{U} {DIRW}'에 해당하는 계급을 표에서 먼저 고른다. 계급은 '이상 ~ 미만'으로 나뉘어 있으므로 {b}{UI} 어느 계급의 어느 쪽 끝인지 보면 된다. 그 계급들의 도수를 더한 값이 {cnt}명이고, 백분율은 (해당 도수) ÷ (전체 도수) × 100이다.",
        sol1_fig=ftable(["{f1}", "{f2}", "{f3}", "{f4}", "{f5}"], total="{nn}"),
        sol2=[
            "{b}{U} {DIRW}인 계급의 도수를 더하면 {cnt}(명)",
            "전체 도수는 {nn}명이므로 백분율은 {cnt} ÷ {nn} × 100 = {p}(%)",
        ],
        sol2_fig=steps([
            {"text": "해당 도수의 합 = {cnt}", "hint": "{b}{U} {DIRW}인 계급만"},
            {"text": "{cnt} ÷ {nn} × 100 = {p} (%)", "marks": [{"on": "{p}", "note": "전체 {nn}으로 나눔"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="전체 {nn}명의 {p} %는 {nn} × {p} ÷ 100 = {cnt}(명)으로, 더한 도수 {cnt}명과 같다. 답은 {p} %이다.",
        sol3_fig=steps(["{nn} × {p} ÷ 100 = {cnt}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="{b}{U} {DIRW}인 학생 수는 해당 계급의 도수를 더한 {cnt}명이다. 전체 학생 수가 {nn}명이므로 전체의 {cnt} ÷ {nn} × 100 = {p}(%)이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "{b}{U} {DIRW}인 계급을 바르게 골라 도수의 합 {cnt}{eul(cnt)} 구했다.", "partial": "계급을 하나 빠뜨리거나 더 넣었으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "{cnt} ÷ {nn} × 100 = {p}{eul(p)} 계산했다.", "partial": "전체가 아닌 다른 수로 나누었으면 인정하지 않고, 계산 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{p} %로 답했다.", "partial": "다른 값을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


JROW = {str(j): {**weights("e", {j}), "J": j} for j in range(1, 6)}


def ft_t3():
    return tpl("m1-2-freq-table", 3, FT,
        title="도수가 가장 큰 계급의 계급값 구하기",
        skill="계급값 = (계급의 양 끝 값의 합) ÷ 2 — 도수가 아니라 계급의 가운데 값",
        variant_axis={"구하는 것": "계급값", "조건": "도수가 가장 큰 계급", "맥락": "6가지"},
        discriminates="도수가 가장 큰 계급을 고른 뒤 그 계급의 '가운데 값'을 구하는가(도수·계급의 크기와 혼동하지 않는가)",
        qtype="short", difficulty=1, pool_target=300,
        params=[{"name": "c", "values": {"in": list(CTX)}}, {"name": "j", "values": {"in": [1, 2, 3, 4, 5]}}, {"name": "g1", "values": {"int": [1, 7]}},
                {"name": "g2", "values": {"int": [1, 7]}}, {"name": "g3", "values": {"int": [1, 7]}}, {"name": "g4", "values": {"int": [1, 7]}},
                {"name": "g5", "values": {"int": [1, 7]}}, {"name": "dd", "values": {"int": [1, 3]}}],
        table=[{"key": "c", "rows": CTX}, {"key": "j", "rows": JROW}],
        derive={"Mx": "max(g1, g2, g3, g4, g5) + dd", "f1": "g1*(1 - e1) + Mx*e1", "f2": "g2*(1 - e2) + Mx*e2", "f3": "g3*(1 - e3) + Mx*e3",
                "f4": "g4*(1 - e4) + Mx*e4", "f5": "g5*(1 - e5) + Mx*e5", "N": "f1 + f2 + f3 + f4 + f5",
                "lo": "S0 + (J - 1)*CW", "hi": "S0 + J*CW", "mid": "S0 + (J - 1)*CW + CW/2"},
        constraints=["N <= 40", "N >= 10", "Mx <= 12"],
        cost_values=["f1", "f2", "f3", "f4", "f5", "mid"],
        relation="2*X - lo - hi", unknown="X", answer_var="mid",
        verify=["2*ans == lo + hi", "Mx > max(g1, g2, g3, g4, g5)"],
        question="다음은 {S} {N}명의 {W}{eul(W)} 조사하여 나타낸 도수분포표이다. 각 계급의 도수가 차례로 {f1}명, {f2}명, {f3}명, {f4}명, {f5}명일 때, 도수가 가장 큰 계급의 계급값을 구하시오.",
        figure=ftable(["{f1}", "{f2}", "{f3}", "{f4}", "{f5}"]),
        answer="{dec(mid)}", answer_alt=["{dec(mid)}{U}"],
        sol1="계급값은 그 계급의 가운데 값, 즉 (양 끝 값의 합) ÷ 2다. 도수가 가장 큰 계급은 도수 {Mx}인 '{lo}{U} 이상 {hi}{U} 미만'이므로, 이 계급의 양 끝 값 {lo}{wa(lo)} {hi}{eul(hi)} 더해 2로 나눈다. 도수 {Mx}{eun(Mx)} 답이 아니다.",
        sol1_fig=ftable(["{f1}", "{f2}", "{f3}", "{f4}", "{f5}"]),
        sol2=[
            "도수를 비교하면 가장 큰 도수는 {Mx}이고, 그 계급은 {lo}{U} 이상 {hi}{U} 미만이다",
            "계급값 = ({lo} + {hi}) ÷ 2 = {lo + hi} ÷ 2 = {dec(mid)}",
        ],
        sol2_fig=steps([
            {"text": "가장 큰 도수 {Mx} → 계급 {lo} 이상 {hi} 미만", "hint": "도수 ≠ 계급값"},
            {"text": "계급값 = ({lo} + {hi}) ÷ 2 = {dec(mid)}", "marks": [{"on": "{dec(mid)}", "note": "가운데 값"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="계급값 {dec(mid)}{eun(dec(mid))} {lo}{wa(lo)} {hi}의 한가운데 있고, 계급의 크기 {CW}의 절반 {dec(CW/2)}{eul(dec(CW/2))} {lo}에 더한 값과 같다. 답은 {dec(mid)}{UD}.",
        sol3_fig=steps(["{lo} + {dec(CW/2)} = {dec(mid)}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="도수가 가장 큰 계급은 도수가 {Mx}인 {lo}{U} 이상 {hi}{U} 미만이다. 계급값은 계급의 양 끝 값의 평균이므로 ({lo} + {hi}) ÷ 2 = {dec(mid)}({U})이다.",
        rubric=[
            {"element": "계급 고르기", "points": 2, "criterion": "도수가 가장 큰 계급이 {lo}{U} 이상 {hi}{U} 미만임을 밝혔다.", "partial": "도수만 {Mx}{ro(Mx)} 적고 계급을 쓰지 않았으면 1점."},
            {"element": "계급값 구하기", "points": 3, "criterion": "계급값 = ({lo} + {hi}) ÷ 2 = {dec(mid)}{eul(dec(mid))} 구했다.", "partial": "계급값의 뜻은 알지만 계산이 틀렸으면 1점."},
        ],
        rubric_total=5,
    )


def ft_t4():
    return tpl("m1-2-freq-table", 4, FT,
        title="백분율이 주어진 계급의 도수 A 를 거쳐 다른 빠진 도수 B 구하기",
        skill="(도수) = (전체 도수) × (백분율) ÷ 100 으로 A를 먼저 구하고, 전체에서 나머지를 빼 B를 구한다",
        variant_axis={"구하는 것": "두 번째 빠진 도수 B", "조건": "한 계급의 백분율", "맥락": "6가지"},
        discriminates="백분율을 도수로 되돌린 뒤 도수의 합이 전체와 같음을 다시 쓰는가(두 단계)",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(CTX)}}, {"name": "nn", "values": {"in": [20, 25, 50]}}, {"name": "ga", "values": {"int": [2, 7]}},
                {"name": "g1", "values": {"int": [1, 6]}}, {"name": "g3", "values": {"int": [2, 7]}}, {"name": "g5", "values": {"int": [1, 5]}}],
        table={"key": "c", "rows": CTX},
        derive={"m": "1 + floor(nn/50)", "a": "m*ga", "f1": "m*g1", "f3": "m*g3", "f5": "m*g5", "p": "100*a/nn", "b": "nn - f1 - a - f3 - f5", "lo": "S0 + CW", "hi": "S0 + 2*CW", "R": "f1 + f3 + f5"},
        constraints=["p == floor(p)", "b >= 1", "b <= 20", "b != a", "b != f1", "b != f3", "b != f5", "b != p", "b != nn", "a != f1", "a != f3", "a != f5", "a != p", "f1 != f5"],
        cost_values=["nn", "p", "a", "f1", "f3", "f5", "b"],
        relation="X + f1 + f3 + f5 + nn*p/100 - nn", unknown="X", answer_var="b",
        verify=["f1 + a + f3 + f5 + ans == nn", "100*a == nn*p"],
        question="다음은 {S} {nn}명의 {W}{eul(W)} 조사하여 나타낸 도수분포표이다. 각 계급의 도수는 차례로 {f1}명, A명, {f3}명, B명, {f5}명이고, {W}{ika(W)} {lo}{U} 이상 {hi}{U} 미만인 학생이 전체의 {p} %일 때, B의 값을 구하시오.",
        figure=ftable(["{f1}", "A", "{f3}", "B", "{f5}"], total="{nn}"),
        answer="{b}", answer_alt=["{b}명"],
        sol1="빠진 도수가 둘(A, B)이므로 도수의 합만으로는 못 구한다. 먼저 백분율이 주어진 계급 '{lo}{U} 이상 {hi}{U} 미만'의 도수 A를 (전체) × (백분율) ÷ 100으로 구한 뒤, 도수의 합이 전체 {nn}{ika(nn)} 되는 조건으로 B를 구한다.",
        sol1_fig=ftable(["{f1}", "A", "{f3}", "B", "{f5}"], total="{nn}"),
        sol2=[
            "전체의 {p} %가 A명이므로 A = {nn} × {p} ÷ 100 = {a}",
            "도수의 합이 전체와 같으므로 {f1} + {a} + {f3} + B + {f5} = {nn}",
            "{R + a} + B = {nn}에서 B = {nn} − {R + a} = {b}",
        ],
        sol2_fig=steps([
            {"text": "A = {nn} × {p} ÷ 100 = {a}", "hint": "백분율 → 도수", "marks": [{"on": "{a}", "note": "전체의 {p}%"}]},
            {"text": "{f1} + {a} + {f3} + B + {f5} = {nn}", "hint": "도수의 합 = 전체"},
            {"text": "B = {nn} − {R + a} = {b}", "marks": [{"on": "{b}", "note": "{nn} − {R + a}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="A = {a}, B = {b}{eul(b)} 넣으면 도수의 합은 {f1} + {a} + {f3} + {b} + {f5} = {nn}{ro(nn)} 전체와 같고, A의 백분율은 {a} ÷ {nn} × 100 = {p} %로 조건과 같다. 답은 {b}이다.",
        sol3_fig=steps(["{f1} + {a} + {f3} + {b} + {f5} = {nn}", "{a} ÷ {nn} × 100 = {p} (%)"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{lo}{U} 이상 {hi}{U} 미만인 계급의 도수는 전체의 {p} %이므로 A = {nn} × {p} ÷ 100 = {a}이다. 도수의 합은 전체 {nn}{wa(nn)} 같으므로 {f1} + {a} + {f3} + B + {f5} = {nn}에서 B = {b}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "A = {nn} × {p} ÷ 100 = {a}{eul(a)} 구하고 도수의 합 {f1} + {a} + {f3} + B + {f5} = {nn}{eul(nn)} 세웠다.", "partial": "A는 구했으나 합의 식을 세우지 못했으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "B = {nn} − {R + a} = {b}{eul(b)} 구했다.", "partial": "덧셈·뺄셈 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "B = {b}{ro(b)} 답했다.", "partial": "A의 값 {a}{eul(a)} 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


TOPROW = {str(j): {**weights("t", set(range(j + 1, 6))), **weights("e", {j}), "J": j} for j in range(1, 5)}   # t_i = 1 이면 j보다 위 계급, e_i = 1 이면 j 계급


def ft_t5():
    return tpl("m1-2-freq-table", 5, FT,
        title="위에서 k번째인 학생이 속하는 계급의 계급값",
        skill="큰 쪽 계급부터 도수를 누적해 k번째가 어느 계급에 드는지 찾고, 그 계급의 계급값을 구한다",
        variant_axis={"구하는 것": "계급값", "조건": "순위(위에서 k번째)", "맥락": "6가지"},
        discriminates="도수를 큰 값 쪽에서부터 누적해 순위가 속한 계급을 찾는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(CTX)}}, {"name": "j", "values": {"in": [1, 2, 3, 4]}}, {"name": "f1", "values": {"int": [1, 8]}},
                {"name": "f2", "values": {"int": [2, 9]}}, {"name": "f3", "values": {"int": [2, 9]}}, {"name": "f4", "values": {"int": [2, 8]}},
                {"name": "f5", "values": {"int": [1, 6]}}, {"name": "o", "values": {"int": [1, 9]}}],
        table=[{"key": "c", "rows": CTX}, {"key": "j", "rows": TOPROW}],
        derive={"N": "f1 + f2 + f3 + f4 + f5", "above": "t1*f1 + t2*f2 + t3*f3 + t4*f4 + t5*f5",
                "fj": "e1*f1 + e2*f2 + e3*f3 + e4*f4 + e5*f5",
                "k": "above + o", "lo": "S0 + (J - 1)*CW", "hi": "S0 + J*CW", "mid": "S0 + (J - 1)*CW + CW/2"},
        constraints=["o <= fj", "N <= 36", "k >= 2", "f1 != f2", "f3 != f4"],
        cost_values=["f1", "f2", "f3", "f4", "f5", "k", "above", "mid"],
        relation="2*X - lo - hi", unknown="X", answer_var="mid",
        verify=["2*ans == lo + hi", "above < k", "k <= above + fj"],
        question="다음은 {S} {N}명의 {W}{eul(W)} 조사하여 나타낸 도수분포표이다. 각 계급의 도수가 차례로 {f1}명, {f2}명, {f3}명, {f4}명, {f5}명일 때, {W}{ika(W)} {ADJ} 쪽에서 {k}번째인 학생이 속하는 계급의 계급값을 구하시오.",
        figure=ftable(["{f1}", "{f2}", "{f3}", "{f4}", "{f5}"]),
        answer="{dec(mid)}", answer_alt=["{dec(mid)}{U}"],
        sol1="{W}{ika(W)} {ADJ} 쪽, 즉 표의 아래쪽(값이 큰 계급)부터 도수를 누적해 간다. 위 계급들의 도수의 합이 {above}명이므로 {above}번째까지는 그 계급들에 있고, {above + 1}번째부터 {above + fj}번째는 그다음 계급 '{lo}{U} 이상 {hi}{U} 미만'에 든다. {k}번째는 여기에 속하므로 이 계급의 계급값을 구한다.",
        sol1_fig=ftable(["{f1}", "{f2}", "{f3}", "{f4}", "{f5}"]),
        sol2=[
            "값이 큰 계급부터 도수를 누적하면 {lo}{U} 이상 {hi}{U} 미만인 계급 바로 위까지의 합이 {above}명",
            "이 계급의 도수가 {fj}명이므로 {above + 1}번째부터 {above + fj}번째까지가 이 계급에 속하고, {k}번째도 여기에 속한다",
            "계급값 = ({lo} + {hi}) ÷ 2 = {dec(mid)}",
        ],
        sol2_fig=steps([
            {"text": "큰 쪽부터 누적: {above}명 → 다음 계급 {above + 1}~{above + fj}번째", "hint": "위 계급부터 센다"},
            {"text": "{k}번째 ∈ {lo} 이상 {hi} 미만", "marks": [{"on": "{k}", "note": "{above} < {k} ≤ {above + fj}"}]},
            {"text": "계급값 = ({lo} + {hi}) ÷ 2 = {dec(mid)}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2)]],
        sol3="{above} < {k} ≤ {above + fj}이므로 {k}번째는 {lo}{U} 이상 {hi}{U} 미만인 계급에 있다. 이 계급의 계급값은 {dec(mid)}{UD}.",
        sol3_fig=steps(["{above} < {k} ≤ {above + fj}  →  {lo} 이상 {hi} 미만", "계급값 {dec(mid)}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{W}{ika(W)} {ADJ} 쪽 계급부터 도수를 누적하면 {lo}{U} 이상 {hi}{U} 미만인 계급 위까지의 합이 {above}명이고 이 계급의 도수가 {fj}명이므로, {ADJ} 쪽에서 {k}번째인 학생은 이 계급에 속한다. 따라서 구하는 계급값은 ({lo} + {hi}) ÷ 2 = {dec(mid)}({U})이다.",
        rubric=[
            {"element": "계급 찾기", "points": 4, "criterion": "{ADJ} 쪽부터 도수를 누적해 {k}번째 학생이 {lo}{U} 이상 {hi}{U} 미만인 계급에 속함을 밝혔다.", "partial": "누적은 했으나 반대쪽(작은 값)부터 세어 계급을 잘못 골랐으면 인정하지 않고, 경계에서 하나 어긋났으면 2점."},
            {"element": "계급값 구하기", "points": 3, "criterion": "그 계급의 계급값 ({lo} + {hi}) ÷ 2 = {dec(mid)}{eul(dec(mid))} 구했다.", "partial": "계급은 맞았으나 계급값 대신 도수나 끝 값을 답했으면 1점."},
        ],
        rubric_total=7,
    )


# ═══════════════════════════════════════════════════════════════════ 2. 상대도수
RCTX = {k: {**v, "P": ("회원" if "회원" in v["S"] else "학생")} for k, v in CTX.items()}
JROW4 = {str(j): {**weights("e", {j}), "J": j} for j in range(1, 5)}
RF = dict(prereq=["상대도수 = (그 계급의 도수) ÷ (전체 도수)", "상대도수의 합은 1"], traps=["구하는대상혼동", "역연산"], tags=["상대도수", "도수분포표"])


def rf_t1():
    return tpl("m1-2-relative-freq", 1, RF,
        title="도수분포표에서 어떤 계급의 상대도수 구하기",
        skill="(상대도수) = (그 계급의 도수) ÷ (전체 도수) — 전체 도수는 도수를 모두 더해 얻는다",
        variant_axis={"구하는 것": "상대도수", "계급": "네 계급 순환", "맥락": "6가지"},
        discriminates="도수를 전체 도수로 나누어 소수로 나타내는가(백분율·도수와 혼동하지 않는가)",
        qtype="short", difficulty=1, pool_target=300,
        params=[{"name": "c", "values": {"in": list(RCTX)}}, {"name": "j", "values": {"in": [1, 2, 3, 4]}}, {"name": "nn", "values": {"in": [20, 25, 40, 50]}},
                {"name": "g1", "values": {"int": [1, 7]}}, {"name": "g2", "values": {"int": [2, 8]}}, {"name": "g3", "values": {"int": [2, 8]}}, {"name": "g4", "values": {"int": [1, 7]}}],
        table=[{"key": "c", "rows": RCTX}, {"key": "j", "rows": JROW4}],
        derive={"m": "1 + floor(nn/40)", "f1": "m*g1", "f2": "m*g2", "f3": "m*g3", "f4": "m*g4", "f5": "nn - m*(g1 + g2 + g3 + g4)",
                "fj": "e1*f1 + e2*f2 + e3*f3 + e4*f4", "r": "fj/nn", "lo": "S0 + (J - 1)*CW", "hi": "S0 + J*CW"},
        constraints=["f5 >= 1", "f5 <= 16", "f1 != f2", "f3 != f4", "1000*r == floor(1000*r)"],
        cost_values=["f1", "f2", "f3", "f4", "f5", "nn", "fj", "r"],
        relation="X*nn - fj", unknown="X", answer_var="r",
        verify=["ans*nn == fj", "ans < 1"],
        question="다음은 {S} {nn}명의 {W}{eul(W)} 조사하여 나타낸 도수분포표이다. 각 계급의 도수가 차례로 {f1}명, {f2}명, {f3}명, {f4}명, {f5}명일 때, {W}{ika(W)} {lo}{U} 이상 {hi}{U} 미만인 계급의 상대도수를 구하시오.",
        figure=ftable(["{f1}", "{f2}", "{f3}", "{f4}", "{f5}"], total="{nn}"),
        answer="{dec(r)}", answer_alt=[],
        sol1="상대도수는 (그 계급의 도수) ÷ (전체 도수)다. 전체 도수는 표의 합계 {nn}명이고, {lo}{U} 이상 {hi}{U} 미만인 계급의 도수는 {fj}명이다. 도수 {fj}{eul(fj)} 그대로 답하거나 100을 곱해 %로 쓰면 안 되고, 0과 1 사이의 소수로 나타낸다.",
        sol1_fig=ftable(["{f1}", "{f2}", "{f3}", "{f4}", "{f5}"], total="{nn}"),
        sol2=[
            "{lo}{U} 이상 {hi}{U} 미만인 계급의 도수는 {fj}, 전체 도수는 {nn}",
            "상대도수 = {fj} ÷ {nn} = {dec(r)}",
        ],
        sol2_fig=steps([
            {"text": "도수 {fj}, 전체 {nn}", "hint": "합계를 전체로"},
            {"text": "상대도수 = {fj} ÷ {nn} = {dec(r)}", "marks": [{"on": "{dec(r)}", "note": "도수 ÷ 전체"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="상대도수 {dec(r)}에 전체 도수 {nn}{eul(nn)} 곱하면 {dec(r)} × {nn} = {fj}{ro(fj)} 그 계급의 도수와 같다. 답은 {dec(r)}이다.",
        sol3_fig=steps(["{dec(r)} × {nn} = {fj}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="전체 도수는 {nn}이고 {lo}{U} 이상 {hi}{U} 미만인 계급의 도수는 {fj}이므로, 이 계급의 상대도수는 {fj} ÷ {nn} = {dec(r)}이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "상대도수 = (계급의 도수) ÷ (전체 도수)로 {fj} ÷ {nn}{eul(nn)} 세웠다.", "partial": "전체 도수를 잘못 잡았으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{fj} ÷ {nn} = {dec(r)}{ro(dec(r))} 답했다.", "partial": "백분율({dec(100*r)} %)이나 분수로만 썼으면 1점."},
        ],
        rubric_total=5,
    )


def rf_t2():
    return tpl("m1-2-relative-freq", 2, RF,
        title="도수와 상대도수로 전체 도수 구하기",
        skill="(전체 도수) = (그 계급의 도수) ÷ (그 계급의 상대도수) — 상대도수의 정의를 거꾸로 쓴다",
        variant_axis={"구하는 것": "전체 도수", "조건": "한 계급의 도수·상대도수", "맥락": "6가지"},
        discriminates="상대도수의 정의 (도수) ÷ (전체)를 전체에 대해 거꾸로 푸는가(곱하지 않는가)",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "c", "values": {"in": list(RCTX)}}, {"name": "j", "values": {"in": [1, 2, 3, 4]}}, {"name": "nn", "values": {"in": [20, 25, 40, 50, 80, 100, 200]}},
                {"name": "f", "values": {"int": [2, 30]}}],
        table=[{"key": "c", "rows": RCTX}, {"key": "j", "rows": JROW4}],
        derive={"r": "f/nn", "lo": "S0 + (J - 1)*CW", "hi": "S0 + J*CW"},
        constraints=["1000*r == floor(1000*r)", "r < 1", "50*r >= 1", "f != nn", "10*f < 7*nn"],
        cost_values=["f", "r", "nn"],
        relation="X*r - f", unknown="X", answer_var="nn",
        verify=["f == ans*r"],
        question="{S} 전체의 {W}{eul(W)} 조사하여 나타낸 도수분포표에서 {W}{ika(W)} {lo}{U} 이상 {hi}{U} 미만인 계급의 도수는 {f}명이고 상대도수는 {dec(r)}이다. 전체 {P} 수를 구하시오.",
        answer="{nn}", answer_alt=["{nn}명"],
        sol1="상대도수는 (도수) ÷ (전체 도수)이므로, 전체 도수를 N이라 하면 {f} ÷ N = {dec(r)}이다. 거꾸로 N = {f} ÷ {dec(r)}{ro(dec(r))} 구한다 — 도수에 상대도수를 곱하는 것이 아니라 나누어야 한다.",
        sol1_fig=steps(["상대도수 = 도수 ÷ 전체", "{dec(r)} = {f} ÷ N"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "전체 {P} 수를 N명이라 하면 상대도수의 뜻에서 {f} ÷ N = {dec(r)}",
            "따라서 N = {f} ÷ {dec(r)} = {nn}",
        ],
        sol2_fig=steps([
            {"text": "{f} ÷ N = {dec(r)}", "hint": "도수 ÷ 전체 = 상대도수"},
            {"text": "N = {f} ÷ {dec(r)} = {nn}", "marks": [{"on": "{nn}", "note": "나눗셈"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="전체가 {nn}명이면 이 계급의 상대도수는 {f} ÷ {nn} = {dec(r)}{ro(dec(r))} 문제의 값과 같다. 답은 {nn}명이다.",
        sol3_fig=steps(["{f} ÷ {nn} = {dec(r)}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="전체 {P} 수를 N명이라 하면 상대도수는 (도수) ÷ (전체 도수)이므로 {f} ÷ N = {dec(r)}이다. 따라서 N = {f} ÷ {dec(r)} = {nn}, 즉 전체 {P} 수는 {nn}명이다.",
        rubric=[
            {"element": "식 세우기", "points": 3, "criterion": "전체를 N으로 두고 상대도수의 뜻으로 {f} ÷ N = {dec(r)}{eul(dec(r))} 세웠다.", "partial": "N × {dec(r)} = {f}{ro(f)} 세워도 인정하고, 곱·나눗셈이 뒤바뀐 식은 인정하지 않는다."},
            {"element": "해 구하기", "points": 3, "criterion": "N = {f} ÷ {dec(r)} = {nn}{eul(nn)} 구했다.", "partial": "소수 나눗셈 실수면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "전체 {P} 수 {nn}명으로 답했다.", "partial": "다른 값을 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


CLS4 = CLS[:4]


def rtable(cells_f, cells_r, total_f="", total_r="1"):
    rows = [[c, f, r] for c, f, r in zip(CLS4, cells_f, cells_r)]
    rows.append(["합계", total_f, total_r])
    return table(["{W}({UH})", "도수(명)", "상대도수"], rows)


def rf_t3():
    return tpl("m1-2-relative-freq", 3, RF,
        title="상대도수의 분포표 완성하기 — 도수 A 구하기",
        skill="한 계급의 도수와 상대도수로 전체 도수를 먼저 구한 뒤, (도수) = (전체) × (상대도수)로 빈칸을 채운다",
        variant_axis={"구하는 것": "빠진 도수 A", "조건": "다른 계급의 도수·상대도수 쌍", "맥락": "6가지"},
        discriminates="전체 도수를 먼저 복원하는가(도수 ÷ 상대도수), 그 뒤 전체 × 상대도수로 도수를 구하는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(RCTX)}}, {"name": "nn", "values": {"in": [20, 25, 40, 50]}}, {"name": "g1", "values": {"int": [1, 6]}},
                {"name": "ga", "values": {"int": [2, 8]}}, {"name": "g3", "values": {"int": [2, 8]}}],
        table={"key": "c", "rows": RCTX},
        derive={"m": "1 + floor(nn/40)", "f1": "m*g1", "a": "m*ga", "f3": "m*g3", "f4": "nn - f1 - a - f3", "r1": "f1/nn", "r2": "a/nn", "r3": "f3/nn", "r4": "f4/nn",
                "lo": "S0 + CW", "hi": "S0 + 2*CW"},
        constraints=["f4 >= 1", "f4 <= 16", "a != f1", "a != f3", "a != f4", "f1 != f3", "f3 != f4", "1000*r1 == floor(1000*r1)", "1000*r2 == floor(1000*r2)", "1000*r3 == floor(1000*r3)", "1000*r4 == floor(1000*r4)"],
        cost_values=["f1", "r1", "r2", "f3", "f4", "r4", "nn", "a"],
        relation="X - (f1/r1)*r2", unknown="X", answer_var="a",
        verify=["ans == nn*r2", "f1 + ans + f3 + f4 == nn"],
        question="다음은 {S}들의 {W}{eul(W)} 조사하여 나타낸 상대도수의 분포표이다. 각 계급의 도수는 차례로 {f1}명, A명, {f3}명, {f4}명이고 상대도수는 차례로 {dec(r1)}, {dec(r2)}, B, {dec(r4)}일 때, A의 값을 구하시오.",
        figure=rtable(["{f1}", "A", "{f3}", "{f4}"], ["{dec(r1)}", "{dec(r2)}", "B", "{dec(r4)}"]),
        answer="{a}", answer_alt=["{a}명"],
        sol1="전체 도수를 모르므로 먼저 도수와 상대도수가 모두 있는 첫 계급에서 전체 도수를 복원한다. (전체 도수) = (도수) ÷ (상대도수) = {f1} ÷ {dec(r1)} = {nn}이다. 그다음 A는 (전체 도수) × (그 계급의 상대도수) = {nn} × {dec(r2)}{ro(dec(r2))} 구한다.",
        sol1_fig=rtable(["{f1}", "A", "{f3}", "{f4}"], ["{dec(r1)}", "{dec(r2)}", "B", "{dec(r4)}"]),
        sol2=[
            "첫 계급에서 전체 도수 = {f1} ÷ {dec(r1)} = {nn}",
            "{lo}{U} 이상 {hi}{U} 미만인 계급의 상대도수가 {dec(r2)}이므로 A = {nn} × {dec(r2)} = {a}",
        ],
        sol2_fig=steps([
            {"text": "전체 = {f1} ÷ {dec(r1)} = {nn}", "hint": "도수 ÷ 상대도수", "marks": [{"on": "{nn}", "note": "전체 도수"}]},
            {"text": "A = {nn} × {dec(r2)} = {a}", "hint": "전체 × 상대도수", "marks": [{"on": "{a}", "note": "{nn}×{dec(r2)}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="A = {a}{eul(a)} 넣으면 도수의 합은 {f1} + {a} + {f3} + {f4} = {nn}{ro(nn)} 전체 도수와 같고, 상대도수의 합도 {dec(r1)} + {dec(r2)} + {dec(r3)} + {dec(r4)} = 1이다. 답은 {a}이다.",
        sol3_fig=steps(["{f1} + {a} + {f3} + {f4} = {nn}", "{dec(r1)} + {dec(r2)} + {dec(r3)} + {dec(r4)} = 1"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="첫 계급의 도수가 {f1}, 상대도수가 {dec(r1)}이므로 전체 도수는 {f1} ÷ {dec(r1)} = {nn}이다. 따라서 A = (전체 도수) × (상대도수) = {nn} × {dec(r2)} = {a}이다.",
        rubric=[
            {"element": "전체 도수 구하기", "points": 3, "criterion": "도수와 상대도수가 모두 있는 계급에서 (전체 도수) = {f1} ÷ {dec(r1)} = {nn}{eul(nn)} 구했다.", "partial": "식은 옳으나 소수 나눗셈이 틀렸으면 1점."},
            {"element": "A 구하기", "points": 3, "criterion": "A = (전체 도수) × (상대도수) = {nn} × {dec(r2)} = {a}{eul(a)} 구했다.", "partial": "전체 도수는 맞았으나 곱셈이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "A = {a}{ro(a)} 답했다.", "partial": "상대도수 {dec(r2)}{eul(dec(r2))} 그대로 답했으면 인정하지 않는다."},
        ],
        rubric_total=8,
    )


def rf_t4():
    return tpl("m1-2-relative-freq", 4, RF,
        title="상대도수의 분포표 완성하기 — 상대도수 B 구하기",
        skill="한 계급의 도수와 상대도수로 전체 도수를 먼저 구한 뒤, (상대도수) = (도수) ÷ (전체)로 빈칸을 채운다",
        variant_axis={"구하는 것": "빠진 상대도수 B", "조건": "다른 계급의 도수·상대도수 쌍", "맥락": "6가지"},
        discriminates="전체 도수를 복원한 뒤 도수를 전체로 나누어 소수로 쓰는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(RCTX)}}, {"name": "nn", "values": {"in": [20, 25, 40, 50]}}, {"name": "g1", "values": {"int": [1, 6]}},
                {"name": "g2", "values": {"int": [2, 8]}}, {"name": "ga", "values": {"int": [2, 8]}}],
        table={"key": "c", "rows": RCTX},
        derive={"m": "1 + floor(nn/40)", "f1": "m*g1", "f2": "m*g2", "a": "m*ga", "f4": "nn - f1 - f2 - a", "r1": "f1/nn", "r2": "f2/nn", "r3": "a/nn", "r4": "f4/nn",
                "lo": "S0 + CW", "hi": "S0 + 2*CW"},
        constraints=["f4 >= 1", "f4 <= 16", "f2 != f1", "f2 != a", "f2 != f4", "f1 != a", "1000*r1 == floor(1000*r1)", "1000*r2 == floor(1000*r2)", "1000*r3 == floor(1000*r3)", "1000*r4 == floor(1000*r4)", "r2 != r1", "r2 != r3", "r2 != r4"],
        cost_values=["f1", "r1", "f2", "r3", "f4", "r4", "nn", "r2"],
        relation="X*(f1/r1) - f2", unknown="X", answer_var="r2",
        verify=["ans*nn == f2", "f1 + f2 + a + f4 == nn"],
        question="다음은 {S}들의 {W}{eul(W)} 조사하여 나타낸 상대도수의 분포표이다. 각 계급의 도수는 차례로 {f1}명, {f2}명, A명, {f4}명이고 상대도수는 차례로 {dec(r1)}, B, {dec(r3)}, {dec(r4)}일 때, B의 값을 구하시오.",
        figure=rtable(["{f1}", "{f2}", "A", "{f4}"], ["{dec(r1)}", "B", "{dec(r3)}", "{dec(r4)}"]),
        answer="{dec(r2)}", answer_alt=[],
        sol1="B는 {lo}{U} 이상 {hi}{U} 미만인 계급의 상대도수이므로 (도수 {f2}) ÷ (전체 도수)인데 전체 도수를 아직 모른다. 먼저 도수와 상대도수가 모두 있는 첫 계급에서 (전체 도수) = {f1} ÷ {dec(r1)} = {nn}{eul(nn)} 구하고, 그 값으로 {f2}{eul(f2)} 나눈다.",
        sol1_fig=rtable(["{f1}", "{f2}", "A", "{f4}"], ["{dec(r1)}", "B", "{dec(r3)}", "{dec(r4)}"]),
        sol2=[
            "첫 계급에서 전체 도수 = {f1} ÷ {dec(r1)} = {nn}",
            "B = (도수) ÷ (전체 도수) = {f2} ÷ {nn} = {dec(r2)}",
        ],
        sol2_fig=steps([
            {"text": "전체 = {f1} ÷ {dec(r1)} = {nn}", "hint": "도수 ÷ 상대도수", "marks": [{"on": "{nn}", "note": "전체 도수"}]},
            {"text": "B = {f2} ÷ {nn} = {dec(r2)}", "hint": "도수 ÷ 전체", "marks": [{"on": "{dec(r2)}", "note": "소수로"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0", "mark:0-0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="상대도수의 합은 1이어야 한다. 빈칸 B = {dec(r2)}{eul(dec(r2))} 넣으면 {dec(r1)} + {dec(r2)} + {dec(r3)} + {dec(r4)} = 1로 맞는다. 답은 {dec(r2)}이다.",
        sol3_fig=steps(["{dec(r1)} + {dec(r2)} + {dec(r3)} + {dec(r4)} = 1"]),
        sol3_anim=[[reveal(0)]],
        model_answer="첫 계급의 도수가 {f1}, 상대도수가 {dec(r1)}이므로 전체 도수는 {f1} ÷ {dec(r1)} = {nn}이다. 따라서 B = (도수) ÷ (전체 도수) = {f2} ÷ {nn} = {dec(r2)}이다.",
        rubric=[
            {"element": "전체 도수 구하기", "points": 3, "criterion": "도수와 상대도수가 모두 있는 계급에서 (전체 도수) = {f1} ÷ {dec(r1)} = {nn}{eul(nn)} 구했다.", "partial": "식은 옳으나 소수 나눗셈이 틀렸으면 1점."},
            {"element": "B 구하기", "points": 3, "criterion": "B = {f2} ÷ {nn} = {dec(r2)}{eul(dec(r2))} 구했다.", "partial": "전체 도수는 맞았으나 나눗셈이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "B = {dec(r2)}{ro(dec(r2))} 답했다.", "partial": "백분율이나 분수로만 썼으면 1점."},
        ],
        rubric_total=8,
    )


GRP = {
    "1": {"G1": "1반", "G2": "2반", "S": "어느 학교 1반과 2반 학생", "W": "하루 스마트폰 사용 시간", "U": "분", "S0": 0, "CW": 30},
    "2": {"G1": "남학생", "G2": "여학생", "S": "어느 반 남학생과 여학생", "W": "통학 시간", "U": "분", "S0": 0, "CW": 10},
    "3": {"G1": "A 동아리", "G2": "B 동아리", "S": "A 동아리와 B 동아리 회원", "W": "한 달 동안 읽은 책의 쪽수", "U": "쪽", "S0": 100, "CW": 100},
    "4": {"G1": "1학년", "G2": "2학년", "S": "어느 학교 1학년과 2학년 학생", "W": "수학 수행평가 점수", "U": "점", "S0": 50, "CW": 10},
}


def rf_t5():
    return tpl("m1-2-relative-freq", 5, RF,
        title="전체 도수가 다른 두 집단의 상대도수 비교 — 몇 배인가",
        skill="집단마다 (도수) ÷ (그 집단의 전체 도수)로 상대도수를 각각 구한 뒤 비교한다 — 도수만 비교하면 안 된다",
        variant_axis={"구하는 것": "상대도수의 배수", "조건": "두 집단의 전체 도수·한 계급의 도수", "맥락": "반·성별·동아리·학년"},
        discriminates="전체 도수가 다르면 도수가 아니라 상대도수로 비교해야 함을 알고, 각 집단의 전체로 나누는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(GRP)}}, {"name": "j", "values": {"in": [2, 3, 4]}}, {"name": "na", "values": {"in": [20, 25, 40, 50]}},
                {"name": "nb", "values": {"in": [20, 25, 40, 50]}}, {"name": "fa", "values": {"int": [2, 20]}}, {"name": "fb", "values": {"int": [2, 20]}}],
        table={"key": "c", "rows": GRP},
        derive={"ra": "fa/na", "rb": "fb/nb", "q": "ra/rb", "lo": "S0 + (j - 1)*CW", "hi": "S0 + j*CW"},
        constraints=["na != nb", "q != 1", "100*q == floor(100*q)", "1000*ra == floor(1000*ra)", "1000*rb == floor(1000*rb)", "10*fa < 6*na", "10*fb < 6*nb", "fa != fb", "q != fa", "q != fb", "q != na", "q != nb"],
        cost_values=["na", "nb", "fa", "fb", "ra", "rb", "q"],
        relation="X*(fb/nb) - fa/na", unknown="X", answer_var="q",
        verify=["ans*fb*na == fa*nb", "ans > 0"],
        question="{S}의 {W}{eul(W)} 조사하였더니 {G1}{eun(G1)} {na}명, {G2}{eun(G2)} {nb}명이었다. {W}{ika(W)} {lo}{U} 이상 {hi}{U} 미만인 계급의 도수가 {G1}{eun(G1)} {fa}명, {G2}{eun(G2)} {fb}명일 때, 이 계급의 상대도수는 {G1}{ika(G1)} {G2}의 몇 배인지 구하시오.",
        answer="{dec(q)}", answer_alt=["{dec(q)}배"],
        sol1="두 집단은 전체 인원이 {na}명, {nb}명으로 다르므로 도수 {fa}{wa(fa)} {fb}{eul(fb)} 그대로 비교하면 안 된다. 각 집단의 상대도수 (도수) ÷ (그 집단의 전체 도수)를 따로 구해 나눈다.",
        sol1_fig=table(["", "전체", "도수", "상대도수"], [["{G1}", "{na}명", "{fa}명", "{fa} ÷ {na} = {dec(ra)}"], ["{G2}", "{nb}명", "{fb}명", "{fb} ÷ {nb} = {dec(rb)}"]]),
        sol2=[
            "{G1}의 상대도수: {fa} ÷ {na} = {dec(ra)}",
            "{G2}의 상대도수: {fb} ÷ {nb} = {dec(rb)}",
            "따라서 {dec(ra)} ÷ {dec(rb)} = {dec(q)}(배)",
        ],
        sol2_fig=steps([
            {"text": "{G1}: {fa} ÷ {na} = {dec(ra)}", "hint": "각자의 전체로 나눈다"},
            {"text": "{G2}: {fb} ÷ {nb} = {dec(rb)}"},
            {"text": "{dec(ra)} ÷ {dec(rb)} = {dec(q)}", "marks": [{"on": "{dec(q)}", "note": "상대도수끼리 비교"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)], [reveal(2), hl("mark:2-0")]],
        sol3="{G2}의 상대도수 {dec(rb)}에 {dec(q)}{eul(dec(q))} 곱하면 {dec(rb)} × {dec(q)} = {dec(ra)}{ro(dec(ra))} {G1}의 상대도수와 같다. 도수만 비교한 {fa} ÷ {fb}{wa(fb)} 다르다는 점에 주의한다. 답은 {dec(q)}배이다.",
        sol3_fig=steps(["{dec(rb)} × {dec(q)} = {dec(ra)}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="{G1}의 이 계급의 상대도수는 {fa} ÷ {na} = {dec(ra)}, {G2}의 상대도수는 {fb} ÷ {nb} = {dec(rb)}이다. 따라서 {G1}의 상대도수는 {G2}의 {dec(ra)} ÷ {dec(rb)} = {dec(q)}(배)이다.",
        rubric=[
            {"element": "상대도수 구하기", "points": 4, "criterion": "각 집단의 상대도수를 {fa} ÷ {na} = {dec(ra)}, {fb} ÷ {nb} = {dec(rb)}{ro(dec(rb))} 구했다.", "partial": "한 집단만 옳으면 2점, 두 집단을 같은 전체로 나누었으면 인정하지 않는다."},
            {"element": "배수 구하기", "points": 3, "criterion": "{dec(ra)} ÷ {dec(rb)} = {dec(q)}(배)로 답했다.", "partial": "도수의 비 {fa} ÷ {fb}{ro(fb)} 답했으면 인정하지 않고, 나눗셈 실수면 1점."},
        ],
        rubric_total=7,
    )


REL_SEED = {
    "seed_id": "m1-2-relative-freq", "category": "활용",
    "title": "상대도수 — 계산·전체 도수 역산·표 완성·두 집단 비교",
    "unit_id": "m1-2", "concept_ids": ["m1-2-21"],
    "schema_id": SCHEMA_REL, "schema_name": "도수의 총합이 다른 두 자료의 상대도수의 비 / 상대도수 분포표 해석",
    "source_item_ids": [],
    "note": "출판사 8.5 유형(상대도수·전체 도수 역산·표 미완성 A·B·두 집단 비교) 차용. 전체 도수를 20·25·40·50(·80·100·200)으로 두어 상대도수가 소수 셋째 자리 안에서 끝난다. 두 집단 비교는 정수비 문자열 대신 '몇 배'(소수)로 묻는다.",
    "geometry": False,
    "templates": [rf_t1(), rf_t2(), rf_t3(), rf_t4(), rf_t5()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 중앙값·최빈값
MCTX = {
    "1": {"S": "어느 학생이 일주일 동안 매일 읽은 책의 쪽수", "U": "쪽", "UH": "쪽", "B": 20},
    "2": {"S": "어느 동아리 회원들의 보드게임 점수", "U": "점", "UH": "점", "B": 60},
    "3": {"S": "어느 학생의 최근 수학 쪽지 시험 점수", "U": "점", "UH": "점", "B": 70},
    "4": {"S": "어느 러닝 크루 회원들이 하루에 달린 거리", "U": " km", "UH": "km", "B": 4},
    "5": {"S": "어느 반 학생들의 하루 스마트폰 사용 시간", "U": "분", "UH": "분", "B": 40},
}
PERMS7 = [(3, 6, 1, 5, 2, 7, 4), (5, 1, 7, 3, 6, 2, 4), (2, 7, 4, 1, 6, 3, 5), (6, 3, 5, 7, 1, 4, 2), (4, 1, 6, 2, 7, 5, 3), (7, 2, 5, 1, 4, 6, 3)]
PERMS6 = [(3, 6, 1, 5, 2, 4), (5, 1, 6, 3, 2, 4), (2, 6, 4, 1, 3, 5), (6, 3, 5, 1, 4, 2), (4, 1, 6, 2, 5, 3), (1, 5, 2, 6, 3, 4)]
PERMS5 = [(3, 5, 1, 4, 2), (5, 1, 4, 2, 3), (2, 5, 3, 1, 4), (4, 2, 5, 3, 1), (1, 4, 2, 5, 3), (5, 3, 1, 2, 4)]


def perm_rows(perms, n_src, idx=lambda pos: pos):
    """표 행: 슬롯 k 에 정렬 순서 idx(perm[k]) 번째 값을 두는 0/1 가중치 w{k}{i}."""
    rows = {}
    for pi, P in enumerate(perms, 1):
        r = {}
        for k, pos in enumerate(P, 1):
            src = idx(pos)
            for i in range(1, n_src + 1):
                r[f"w{k}{i}"] = 1 if src == i else 0
        rows[str(pi)] = r
    return rows


def slot_expr(k, n_src, names):
    return " + ".join(f"w{k}{i}*{names[i - 1]}" for i in range(1, n_src + 1))


MM = dict(prereq=["중앙값: 크기순으로 나열한 가운데 값(짝수 개면 가운데 두 값의 평균)", "최빈값: 가장 많이 나타나는 값"],
          traps=["구하는대상혼동", "조건누락"], tags=["대푯값", "중앙값", "최빈값"])
S6 = ["s1", "s2", "s3", "s4", "s5", "s6"]


def _t1_rows():
    rows = {}
    for m in range(1, 7):
        idx = lambda pos, m=m: pos if pos <= m else pos - 1          # 정렬 7개: s_m 이 두 번
        for pi, P in enumerate(PERMS7, 1):
            r = {}
            for k, pos in enumerate(P, 1):
                src = idx(pos)
                for i in range(1, 7):
                    r[f"w{k}{i}"] = 1 if src == i else 0
            r.update({f"o{i}": (1 if i == m else 0) for i in range(1, 7)})
            r.update({f"u{pos}{i}": (1 if idx(pos) == i else 0) for pos in range(1, 8) for i in range(1, 7)})   # 정렬 7개 t1~t7
            r["wm3"] = 1 if m <= 3 else 0
            rows[f"{m}-{pi}"] = r
    return rows


T1_ROWS = _t1_rows()


def mm_t1():
    return tpl("m1-2-median-mode", 1, MM,
        title="7개 자료의 중앙값과 최빈값 — a + b",
        skill="크기순으로 나열해 가운데(4번째) 값이 중앙값, 두 번 나타난 값이 최빈값",
        variant_axis={"구하는 것": "중앙값 + 최빈값", "자료": "7개(한 값 중복)", "맥락": "5가지"},
        discriminates="나열하지 않은 채 가운데 자리 값을 읽지 않는가, 최빈값을 '가장 큰 값'이나 '횟수'로 오해하지 않는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "c", "values": {"in": list(MCTX)}}, {"name": "mp", "values": {"in": list(T1_ROWS)}}, {"name": "d0", "values": {"int": [0, 3]}},
                {"name": "g1", "values": {"int": [1, 3]}}, {"name": "g2", "values": {"int": [1, 3]}}, {"name": "g3", "values": {"int": [1, 3]}},
                {"name": "g4", "values": {"int": [1, 3]}}, {"name": "g5", "values": {"int": [1, 3]}}],
        table=[{"key": "c", "rows": MCTX}, {"key": "mp", "rows": T1_ROWS}],
        derive={"s1": "B + d0", "s2": "B + d0 + g1", "s3": "B + d0 + g1 + g2", "s4": "B + d0 + g1 + g2 + g3", "s5": "B + d0 + g1 + g2 + g3 + g4", "s6": "B + d0 + g1 + g2 + g3 + g4 + g5",
                **{f"v{k}": slot_expr(k, 6, S6) for k in range(1, 8)},
                **{f"t{pos}": " + ".join(f"u{pos}{i}*s{i}" for i in range(1, 7)) for pos in range(1, 8)},
                "med": "wm3*s3 + (1 - wm3)*s4", "mo": "o1*s1 + o2*s2 + o3*s3 + o4*s4 + o5*s5 + o6*s6", "ab": "wm3*s3 + (1 - wm3)*s4 + o1*s1 + o2*s2 + o3*s3 + o4*s4 + o5*s5 + o6*s6"},
        constraints=["ab != s1", "ab != s2", "ab != s3", "ab != s4", "ab != s5", "ab != s6"],
        cost_values=["s1", "s2", "s3", "s4", "s5", "s6", "med", "mo", "ab"],
        relation="X - med - mo", unknown="X", answer_var="ab",
        verify=["ans == med + mo", "s1 < s2", "s2 < s3", "s3 < s4", "s4 < s5", "s5 < s6"],
        question="다음은 {S}{eul(S)} 조사하여 나타낸 자료이다. 이 자료의 중앙값을 a, 최빈값을 b라 할 때, a + b의 값을 구하시오.  [ {v1}, {v2}, {v3}, {v4}, {v5}, {v6}, {v7} ]  (단위: {UH})",
        figure=table(None, [["{v1}", "{v2}", "{v3}", "{v4}", "{v5}", "{v6}", "{v7}"]], caption="(단위: {UH})"),
        answer="{ab}", answer_alt=[],
        sol1="중앙값은 자료를 크기순으로 나열했을 때 가운데 값이고, 최빈값은 가장 많이 나타나는 값이다. 자료가 7개이므로 나열하면 4번째 값이 중앙값이다. 주어진 순서 그대로 가운데를 읽으면 안 되고 반드시 먼저 나열한다. 최빈값은 두 번 나타난 {mo}{ida(mo)}.",
        sol1_fig=steps(["크기순 나열 → 4번째 값 = 중앙값 a", "두 번 나타난 값 = 최빈값 b"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "크기순으로 나열하면 {t1}, {t2}, {t3}, {t4}, {t5}, {t6}, {t7}의 7개 — {mo}{ika(mo)} 두 번 나타난다",
            "가운데(4번째) 값이 중앙값이므로 a = {med}",
            "가장 많이 나타나는 값은 두 번 나온 {mo}이므로 b = {mo}",
            "따라서 a + b = {med} + {mo} = {ab}",
        ],
        sol2_fig=steps([
            {"text": "{t1}, {t2}, {t3}, {t4}, {t5}, {t6}, {t7}", "hint": "크기순 나열"},
            {"text": "a = {med}", "marks": [{"on": "{med}", "note": "4번째"}]},
            {"text": "b = {mo}", "hint": "두 번 나타난 값"},
            {"text": "a + b = {ab}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3)]],
        sol3="나열한 7개 중 {med}의 앞에 3개, 뒤에 3개가 있으므로 {med}{ika(med)} 가운데 값이 맞고, {mo}{eun(mo)} 두 번, 나머지는 한 번씩이므로 최빈값도 {mo}{ika(mo)} 맞다. 답은 {ab}이다.",
        sol3_fig=steps(["{med}: 앞 3개 · 뒤 3개  ✓", "{mo}: 2번 (나머지 1번)  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="자료를 크기순으로 나열하면 {t1}, {t2}, {t3}, {t4}, {t5}, {t6}, {t7}이고, 7개 중 가운데인 4번째 값은 {med}이므로 중앙값 a = {med}이다. 가장 많이 나타나는 값은 {mo}이므로 최빈값 b = {mo}이다. 따라서 a + b = {med} + {mo} = {ab}이다.",
        rubric=[
            {"element": "중앙값 구하기", "points": 3, "criterion": "자료를 크기순으로 나열하고 4번째 값 {med}{eul(med)} 중앙값으로 구했다.", "partial": "나열은 했으나 다른 자리 값을 읽었으면 1점, 나열하지 않고 주어진 순서의 가운데 값을 답했으면 인정하지 않는다."},
            {"element": "최빈값 구하기", "points": 2, "criterion": "두 번 나타난 {mo}{eul(mo)} 최빈값으로 구했다.", "partial": "가장 큰 값이나 나타난 횟수를 답했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "a + b = {ab}{ro(ab)} 답했다.", "partial": "a, b는 옳으나 합이 틀렸으면 1점."},
        ],
        rubric_total=7,
    )


T2_ROWS = perm_rows(PERMS6, 6)


def mm_t2():
    return tpl("m1-2-median-mode", 2, MM,
        title="짝수 개(6개) 자료의 중앙값 — 가운데 두 값의 평균",
        skill="자료가 짝수 개이면 크기순으로 나열해 가운데 두 값(3번째·4번째)의 평균이 중앙값",
        variant_axis={"구하는 것": "중앙값", "자료": "6개(짝수)", "맥락": "5가지"},
        discriminates="짝수 개일 때 가운데 두 값의 평균을 내는가(한쪽 값만 답하지 않는가)",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "c", "values": {"in": list(MCTX)}}, {"name": "p", "values": {"in": [1, 2, 3, 4, 5, 6]}}, {"name": "d0", "values": {"int": [0, 4]}},
                {"name": "g1", "values": {"int": [1, 3]}}, {"name": "g2", "values": {"int": [1, 3]}}, {"name": "g3", "values": {"in": [1, 3, 5]}},
                {"name": "g4", "values": {"int": [1, 3]}}, {"name": "g5", "values": {"int": [1, 3]}}],
        table=[{"key": "c", "rows": MCTX}, {"key": "p", "rows": T2_ROWS}],
        derive={"s1": "B + d0", "s2": "B + d0 + g1", "s3": "B + d0 + g1 + g2", "s4": "B + d0 + g1 + g2 + g3", "s5": "B + d0 + g1 + g2 + g3 + g4", "s6": "B + d0 + g1 + g2 + g3 + g4 + g5",
                **{f"v{k}": slot_expr(k, 6, S6) for k in range(1, 7)}, "med": "(s3 + s4)/2"},
        constraints=["med != floor(med)"],
        cost_values=["s1", "s2", "s3", "s4", "s5", "s6", "med"],
        relation="2*X - s3 - s4", unknown="X", answer_var="med",
        verify=["2*ans == s3 + s4", "s3 < ans", "ans < s4"],
        question="다음은 {S}{eul(S)} 조사하여 나타낸 자료이다. 이 자료의 중앙값을 구하시오.  [ {v1}, {v2}, {v3}, {v4}, {v5}, {v6} ]  (단위: {UH})",
        figure=table(None, [["{v1}", "{v2}", "{v3}", "{v4}", "{v5}", "{v6}"]], caption="(단위: {UH})"),
        answer="{dec(med)}", answer_alt=["{dec(med)}{U}"],
        sol1="자료가 6개, 즉 짝수 개이므로 크기순으로 나열했을 때 가운데 값이 하나가 아니라 둘(3번째와 4번째)이다. 이때 중앙값은 그 두 값의 평균이다. 먼저 나열하고, 가운데 두 값을 찾아 더해 2로 나눈다.",
        sol1_fig=table(["순서", "1", "2", "3", "4", "5", "6"], [["값", "{s1}", "{s2}", "{s3}", "{s4}", "{s5}", "{s6}"]]),
        sol2=[
            "크기순으로 나열: {s1}, {s2}, {s3}, {s4}, {s5}, {s6}",
            "6개이므로 가운데 두 값은 3번째 {s3}{wa(s3)} 4번째 {s4}",
            "중앙값 = ({s3} + {s4}) ÷ 2 = {s3 + s4} ÷ 2 = {dec(med)}",
        ],
        sol2_fig=steps([
            {"text": "{s1}, {s2}, {s3}, {s4}, {s5}, {s6}", "hint": "크기순 나열"},
            {"text": "가운데 두 값: {s3}, {s4}", "hint": "짝수 개 → 두 값"},
            {"text": "중앙값 = ({s3} + {s4}) ÷ 2 = {dec(med)}", "marks": [{"on": "{dec(med)}", "note": "두 값의 평균"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="중앙값 {dec(med)}{eun(dec(med))} {s3}{wa(s3)} {s4}의 한가운데 있고, 그 앞에 2개·뒤에 2개가 있으므로 자료 전체의 가운데가 맞다. 답은 {dec(med)}이다.",
        sol3_fig=steps(["{s3} < {dec(med)} < {s4}", "앞 2개 · 뒤 2개  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="자료를 크기순으로 나열하면 {s1}, {s2}, {s3}, {s4}, {s5}, {s6}이다. 자료가 6개이므로 중앙값은 3번째와 4번째 값의 평균인 ({s3} + {s4}) ÷ 2 = {dec(med)}이다.",
        rubric=[
            {"element": "나열하기", "points": 2, "criterion": "자료를 크기순으로 {s1}, {s2}, {s3}, {s4}, {s5}, {s6}{ro(s6)} 나열했다.", "partial": "순서가 하나 어긋났으면 1점."},
            {"element": "중앙값 구하기", "points": 3, "criterion": "가운데 두 값 {s3}, {s4}의 평균 {dec(med)}{eul(dec(med))} 중앙값으로 구했다.", "partial": "가운데 두 값은 찾았으나 평균을 내지 않고 한 값을 답했으면 1점."},
        ],
        rubric_total=5,
    )


T3_ROWS = perm_rows(PERMS5, 5)
S5A = ["v", "v", "o1", "o2", "o3"]


def mm_t3():
    return tpl("m1-2-median-mode", 3, MM,
        title="평균과 최빈값이 같을 때 미지수 x 구하기",
        skill="두 번 나타난 값이 최빈값 → (평균) = (최빈값) 으로 식을 세워 x를 구한다",
        variant_axis={"구하는 것": "미지 변량 x", "조건": "평균 = 최빈값", "맥락": "5가지"},
        discriminates="x가 무엇이든 최빈값은 두 번 나타난 값임을 알고, 평균 식 (총합) ÷ 6 = (최빈값)을 세우는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(MCTX)}}, {"name": "p", "values": {"in": [1, 2, 3, 4, 5, 6]}}, {"name": "dv", "values": {"int": [2, 8]}},
                {"name": "a1", "values": {"int": [0, 4]}}, {"name": "h1", "values": {"int": [1, 4]}}, {"name": "h2", "values": {"int": [1, 4]}}],
        table=[{"key": "c", "rows": MCTX}, {"key": "p", "rows": T3_ROWS}],
        derive={"v": "B + dv", "o1": "B + a1", "o2": "B + a1 + h1", "o3": "B + a1 + h1 + h2", "SM": "2*(B + dv) + 3*B + 3*a1 + 2*h1 + h2",
                **{f"d{k}": slot_expr(k, 5, S5A) for k in range(1, 6)}, "x": "6*(B + dv) - (2*(B + dv) + 3*B + 3*a1 + 2*h1 + h2)"},
        constraints=["o1 != v", "o2 != v", "o3 != v", "x != v", "x != o1", "x != o2", "x != o3", "x >= 1", "x <= B + 20"],
        cost_values=["v", "o1", "o2", "o3", "x"],
        relation="(SM + X)/6 - v", unknown="X", answer_var="x",
        verify=["SM + ans == 6*v"],
        question="다음은 {S}{eul(S)} 조사하여 나타낸 자료이다. 이 자료의 평균과 최빈값이 같을 때, x의 값을 구하시오.  [ {d1}, {d2}, x, {d3}, {d4}, {d5} ]  (단위: {UH})",
        figure=table(None, [["{d1}", "{d2}", "x", "{d3}", "{d4}", "{d5}"]], caption="(단위: {UH})"),
        answer="{x}", answer_alt=["{x}{U}"],
        sol1="x를 뺀 나머지 자료에서 {v}{eun(v)} 두 번, 다른 값은 한 번씩 나타나므로 최빈값은 x의 값과 관계없이 {v}{ida(v)}(x가 다른 값과 같아지면 최빈값이 둘이 되므로 그 경우는 제외한다). 평균이 최빈값 {v}{wa(v)} 같아야 하므로 (총합) ÷ 6 = {v}{ro(v)} 식을 세운다.",
        sol1_fig=steps(["최빈값 = {v}  (두 번 나타남)", "평균 = (총합) ÷ 6 = {v}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "{v}{ika(v)} 두 번 나타나므로 최빈값은 {v}",
            "평균이 {v}이므로 ({SM} + x) ÷ 6 = {v}",
            "{SM} + x = {6*v}이므로 x = {6*v} − {SM} = {x}",
        ],
        sol2_fig=steps([
            {"text": "최빈값 = {v}", "hint": "두 번 나타난 값"},
            {"text": "({SM} + x) ÷ 6 = {v}", "hint": "자료 6개의 평균", "marks": [{"on": "{SM}", "note": "x를 뺀 합"}]},
            {"text": "x = {6*v} − {SM} = {x}", "marks": [{"on": "{x}", "note": "{6*v} − {SM}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("mark:2-0")]],
        sol3="x = {x}{eul(x)} 넣으면 총합은 {SM} + {x} = {6*v}, 평균은 {6*v} ÷ 6 = {v}{ro(v)} 최빈값 {v}{wa(v)} 같다. 또 {x}{eun(x)} 다른 값과 겹치지 않으므로 최빈값은 여전히 {v} 하나다. 답은 {x}이다.",
        sol3_fig=steps(["({SM} + {x}) ÷ 6 = {6*v} ÷ 6 = {v}"]),
        sol3_anim=[[reveal(0)]],
        model_answer="{v}{ika(v)} 두 번 나타나므로 최빈값은 {v}이다. 평균이 최빈값과 같으므로 ({SM} + x) ÷ 6 = {v}, 즉 {SM} + x = {6*v}에서 x = {x}이다.",
        rubric=[
            {"element": "최빈값 알기", "points": 2, "criterion": "두 번 나타난 {v}{ika(v)} 최빈값임을 밝혔다.", "partial": "최빈값을 다른 값으로 잡았으면 인정하지 않는다."},
            {"element": "식 세우기", "points": 3, "criterion": "(평균) = (최빈값)에서 ({SM} + x) ÷ 6 = {v}{eul(v)} 세웠다.", "partial": "총합을 6이 아닌 5로 나누었으면 1점."},
            {"element": "해 구하기", "points": 3, "criterion": "{SM} + x = {6*v}에서 x = {x}{eul(x)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=8,
    )


T4_ROWS = perm_rows(PERMS5, 5)
S5B = ["s1", "s2", "s3", "s4", "s5"]


def mm_t4():
    return tpl("m1-2-median-mode", 4, MM,
        title="중앙값이 주어진 짝수 개 자료에서 미지수 x 구하기",
        skill="나머지를 나열해 x가 들어갈 자리를 정하고 (3번째 + 4번째) ÷ 2 = (중앙값) 으로 x를 구한다",
        variant_axis={"구하는 것": "미지 변량 x", "조건": "중앙값", "맥락": "5가지"},
        discriminates="중앙값의 위치로 x의 자리를 판단하고 가운데 두 값의 평균 식을 세우는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(MCTX)}}, {"name": "p", "values": {"in": [1, 2, 3, 4, 5, 6]}}, {"name": "d0", "values": {"int": [0, 4]}},
                {"name": "g1", "values": {"int": [1, 3]}}, {"name": "g2", "values": {"int": [1, 3]}}, {"name": "g3", "values": {"int": [3, 6]}},
                {"name": "g4", "values": {"int": [1, 3]}}, {"name": "e", "values": {"int": [1, 5]}}],
        table=[{"key": "c", "rows": MCTX}, {"key": "p", "rows": T4_ROWS}],
        derive={"s1": "B + d0", "s2": "B + d0 + g1", "s3": "B + d0 + g1 + g2", "s4": "B + d0 + g1 + g2 + g3", "s5": "B + d0 + g1 + g2 + g3 + g4",
                **{f"d{k}": slot_expr(k, 5, S5B) for k in range(1, 6)}, "x": "B + d0 + g1 + g2 + e", "m": "(2*(B + d0 + g1 + g2) + e)/2", "mm": "(s3 + s4)/2"},
        constraints=["e <= g3 - 1", "x != m"],
        cost_values=["s1", "s2", "s3", "s4", "s5", "m", "x"],
        relation="(s3 + X)/2 - m", unknown="X", answer_var="x",
        verify=["s3 + ans == 2*m", "s3 < ans", "ans < s4"],
        question="다음은 {S}{eul(S)} 조사하여 나타낸 자료이다. 이 자료의 중앙값이 {dec(m)}일 때, x의 값을 구하시오.  [ {d1}, {d2}, x, {d3}, {d4}, {d5} ]  (단위: {UH})",
        figure=table(None, [["{d1}", "{d2}", "x", "{d3}", "{d4}", "{d5}"]], caption="(단위: {UH})"),
        answer="{x}", answer_alt=["{x}{U}"],
        sol1="자료가 6개이므로 중앙값은 크기순으로 3번째와 4번째 값의 평균이다. x를 뺀 나머지 5개를 나열하면 {s1}, {s2}, {s3}, {s4}, {s5}이다. 중앙값 {dec(m)}{eun(dec(m))} {s3}보다 크고 {s3}{wa(s3)} {s4}의 평균 {dec(mm)}보다 작으므로, x는 {s3}{wa(s3)} {s4} 사이에 들어가 3번째 값이 {s3}, 4번째 값이 x가 된다.",
        sol1_fig=table(["순서", "1", "2", "3", "4", "5", "6"], [["값", "{s1}", "{s2}", "{s3}", "x", "{s4}", "{s5}"]]),
        sol2=[
            "x를 뺀 나머지를 크기순으로 나열: {s1}, {s2}, {s3}, {s4}, {s5}",
            "중앙값 {dec(m)}{ika(dec(m))} {s3}{wa(s3)} {dec(mm)} 사이에 있으므로 x는 {s3}{wa(s3)} {s4} 사이 — 나열하면 {s1}, {s2}, {s3}, x, {s4}, {s5}",
            "가운데 두 값의 평균이 중앙값이므로 ({s3} + x) ÷ 2 = {dec(m)}",
            "{s3} + x = {2*m}이므로 x = {2*m} − {s3} = {x}",
        ],
        sol2_fig=steps([
            {"text": "{s1}, {s2}, {s3}, {s4}, {s5}", "hint": "x 빼고 나열"},
            {"text": "{s3} < {dec(m)} < {dec(mm)} → x는 {s3}{wa(s3)} {s4} 사이", "hint": "x의 자리"},
            {"text": "({s3} + x) ÷ 2 = {dec(m)}", "marks": [{"on": "{dec(m)}", "note": "3번째·4번째 평균"}]},
            {"text": "x = {2*m} − {s3} = {x}", "marks": [{"on": "{x}", "note": "{2*m} − {s3}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")], [reveal(3), hl("mark:3-0")]],
        sol3="x = {x}{eul(x)} 넣어 나열하면 {s1}, {s2}, {s3}, {x}, {s4}, {s5}이고 가운데 두 값 {s3}, {x}의 평균은 ({s3} + {x}) ÷ 2 = {dec(m)}{ro(dec(m))} 조건과 같다. 답은 {x}이다.",
        sol3_fig=steps(["{s1}, {s2}, {s3}, {x}, {s4}, {s5}", "({s3} + {x}) ÷ 2 = {dec(m)}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="x를 뺀 나머지 자료를 크기순으로 나열하면 {s1}, {s2}, {s3}, {s4}, {s5}이다. 중앙값 {dec(m)}{eun(dec(m))} {s3}보다 크고 {dec(mm)}보다 작으므로 x는 {s3}{wa(s3)} {s4} 사이에 있고, 나열하면 {s1}, {s2}, {s3}, x, {s4}, {s5}이다. 따라서 ({s3} + x) ÷ 2 = {dec(m)}에서 x = {x}이다.",
        rubric=[
            {"element": "자리 정하기", "points": 3, "criterion": "나머지를 나열하고 중앙값의 크기로 x가 {s3}{wa(s3)} {s4} 사이에 있음을 밝혔다.", "partial": "나열은 했으나 x의 자리를 근거 없이 정했으면 1점."},
            {"element": "식 세우기", "points": 2, "criterion": "가운데 두 값의 평균으로 ({s3} + x) ÷ 2 = {dec(m)}{eul(dec(m))} 세웠다.", "partial": "한 값만 중앙값으로 놓은 식은 인정하지 않는다."},
            {"element": "해 구하기", "points": 2, "criterion": "x = {2*m} − {s3} = {x}{eul(x)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=7,
    )


T5_ROWS = perm_rows(PERMS6, 6)


def mm_t5():
    return tpl("m1-2-median-mode", 5, MM,
        title="평균으로 미지수 x를 구한 뒤 중앙값 구하기",
        skill="(총합) = (평균) × 7 로 x를 먼저 구하고, x를 포함해 나열한 뒤 4번째 값을 읽는다",
        variant_axis={"구하는 것": "중앙값", "조건": "평균(x 미지)", "맥락": "5가지"},
        discriminates="평균으로 x를 되살린 뒤 x까지 넣어 다시 나열하는가(x를 빼고 나열하지 않는가)",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(MCTX)}}, {"name": "p", "values": {"in": [1, 2, 3, 4, 5, 6]}}, {"name": "d0", "values": {"int": [0, 3]}},
                {"name": "g1", "values": {"int": [1, 3]}}, {"name": "g2", "values": {"int": [1, 3]}}, {"name": "g4", "values": {"int": [1, 3]}}, {"name": "g5", "values": {"int": [1, 3]}}],
        table=[{"key": "c", "rows": MCTX}, {"key": "p", "rows": T5_ROWS}],
        derive={"s1": "B + d0", "s2": "B + d0 + g1", "s3": "B + d0 + g1 + g2", "s4": "B + d0 + g1 + g2 + 8", "s5": "B + d0 + g1 + g2 + 8 + g4", "s6": "B + d0 + g1 + g2 + 8 + g4 + g5",
                "SM": "s1 + s2 + s3 + s4 + s5 + s6", "x": "s3 + 1 + ((-SM - s3 - 1) % 7)", "m": "(SM + x)/7",
                **{f"d{k}": slot_expr(k, 6, S6) for k in range(1, 7)}},
        constraints=["m != x", "m == floor(m)"],
        cost_values=["s1", "s2", "s3", "s4", "s5", "s6", "m", "x"],
        relation="X - (7*m - SM)", unknown="X", answer_var="x",
        verify=["SM + ans == 7*m", "s3 < ans", "ans < s4"],
        question="다음은 {S}{eul(S)} 조사하여 나타낸 자료이다. 이 자료의 평균이 {m}{U}일 때, 중앙값을 구하시오.  [ {d1}, {d2}, x, {d3}, {d4}, {d5}, {d6} ]  (단위: {UH})",
        figure=table(None, [["{d1}", "{d2}", "x", "{d3}", "{d4}", "{d5}", "{d6}"]], caption="(단위: {UH})"),
        answer="{x}", answer_alt=["{x}{U}"],
        sol1="x를 모르면 나열할 수 없으므로 평균부터 쓴다. 자료 7개의 평균이 {m}이므로 총합은 {m} × 7 = {7*m}이고, x를 뺀 여섯 값의 합 {SM}{eul(SM)} 빼면 x가 나온다. 그다음 x를 넣어 7개를 크기순으로 나열하고 가운데(4번째) 값을 읽는다.",
        sol1_fig=steps(["총합 = {m} × 7 = {7*m}", "x = {7*m} − {SM}", "x를 넣어 나열 → 4번째 값"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "총합은 (평균) × (개수) = {m} × 7 = {7*m}",
            "x를 뺀 여섯 값의 합은 {SM}이므로 x = {7*m} − {SM} = {x}",
            "x = {x}{eul(x)} 넣어 크기순으로 나열: {s1}, {s2}, {s3}, {x}, {s4}, {s5}, {s6}",
            "7개의 가운데인 4번째 값이 중앙값이므로 중앙값은 {x}",
        ],
        sol2_fig=steps([
            {"text": "총합 = {m} × 7 = {7*m}", "hint": "평균 × 개수"},
            {"text": "x = {7*m} − {SM} = {x}", "marks": [{"on": "{x}", "note": "여섯 값의 합 {SM}"}]},
            {"text": "{s1}, {s2}, {s3}, {x}, {s4}, {s5}, {s6}", "hint": "x를 넣어 나열"},
            {"text": "중앙값 = 4번째 값 = {x}", "marks": [{"on": "{x}", "note": "가운데"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")], [reveal(2), hl("hint:2")], [reveal(3), hl("mark:3-0")]],
        sol3="나열한 7개에서 {x}의 앞에 {s1}, {s2}, {s3}의 3개, 뒤에 {s4}, {s5}, {s6}의 3개가 있으므로 {x}{ika(x)} 가운데 값이 맞다. 평균도 ({SM} + {x}) ÷ 7 = {m}{ro(m)} 조건과 같다. 답은 {x}이다.",
        sol3_fig=steps(["앞 3개 · {x} · 뒤 3개", "({SM} + {x}) ÷ 7 = {m}  ✓"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="평균이 {m}이고 자료가 7개이므로 총합은 {m} × 7 = {7*m}이다. x를 뺀 여섯 값의 합이 {SM}이므로 x = {7*m} − {SM} = {x}이다. x를 넣어 크기순으로 나열하면 {s1}, {s2}, {s3}, {x}, {s4}, {s5}, {s6}이고 가운데인 4번째 값이 {x}이므로 중앙값은 {x}이다.",
        rubric=[
            {"element": "x 구하기", "points": 3, "criterion": "(총합) = {m} × 7 = {7*m}에서 x = {7*m} − {SM} = {x}{eul(x)} 구했다.", "partial": "총합을 평균으로 놓는 등 7을 곱하지 않았으면 인정하지 않고, 뺄셈 실수면 1점."},
            {"element": "나열하기", "points": 2, "criterion": "x = {x}{eul(x)} 포함해 7개를 크기순으로 나열했다.", "partial": "x를 빼고 나열했으면 인정하지 않는다."},
            {"element": "중앙값 구하기", "points": 2, "criterion": "4번째 값 {x}{eul(x)} 중앙값으로 답했다.", "partial": "다른 자리 값을 답했으면 인정하지 않는다."},
        ],
        rubric_total=7,
    )


MED_SEED = {
    "seed_id": "m1-2-median-mode", "category": "활용",
    "title": "중앙값·최빈값 — a + b·짝수 개 중앙값·평균=최빈값·중앙값 조건·평균→중앙값",
    "unit_id": "m1-2", "concept_ids": ["m1-2-17"],
    "schema_id": SCHEMA_MED, "schema_name": "중앙값 조건으로 미지 변량 구하기 / 최빈값 조건으로 미지 변량 역산",
    "source_item_ids": [],
    "note": "출판사 8.1 유형(중앙값·최빈값·평균=최빈값·중앙값 조건 x) 차용. '중앙값을 구하시오'는 답이 자료 안의 값이라 R-05에 걸려 a + b·짝수 개(.5)·미지수 x 꼴로만 묻는다. 나열 순서는 표 행(순열 6벌 × 0/1 가중치)으로 섞는다.",
    "geometry": False,
    "templates": [mm_t1(), mm_t2(), mm_t3(), mm_t4(), mm_t5()],
}


FREQ_SEED = {
    "seed_id": "m1-2-freq-table", "category": "활용",
    "title": "도수분포표 — 빠진 도수·백분율·계급값·순위",
    "unit_id": "m1-2", "concept_ids": ["m1-2-19"],
    "schema_id": SCHEMA_FREQ, "schema_name": "도수분포표 특정 계급 백분율 / 도수분포표의 이해",
    "source_item_ids": [],
    "note": "출판사 8.3 유형(미지 도수 A·백분율·계급값·이상/미만 개수·순위) 차용. 계급은 표 행(시작값·크기)에서 파생, 도수는 문면에도 차례로 적어 DUP 방지. 백분율 틀은 전체 20·25·50명으로 정수 %.",
    "geometry": False,
    "templates": [ft_t1(), ft_t2(), ft_t3(), ft_t4(), ft_t5()],
}


if __name__ == "__main__":
    with_pitfalls(FREQ_SEED)
    dump(FREQ_SEED)
    with_pitfalls(REL_SEED)
    dump(REL_SEED)
    with_pitfalls(MED_SEED)
    dump(MED_SEED)
