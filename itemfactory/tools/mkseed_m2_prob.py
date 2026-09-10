# itemfactory/tools/mkseed_m2_prob.py — 중2-2 경우의 수·확률 시드 (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m2_prob.py
#     → seeds/m2-2-counting.json (경우의 수 8틀 · 활용)
#     → seeds/m2-2-probability.json (확률 7틀 · 활용)
#
# 유형 근거: reference/pubs/TYPES.md (동아 8.1~8.4 · 천재 Ⅵ). 문항 자체는 새로 쓴다.
# 답이 분수인 틀은 derive 로 Fraction 을 만들고 `answer="{ans}"` 로 [[frac]] 마커가 나오게 한다.
from __future__ import annotations

import os
import sys
from math import factorial

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, table, with_pitfalls  # noqa: E402

CNT = {"process": "문제해결", "context": "생활맥락", "prereq": ["경우의 수의 뜻"], "ops": ["경우의 수", "사칙"], "traps": ["합·곱 혼동", "중복"],
       "time_limit": 90, "points": 4, "tags": ["경우의 수"], "rubric_total": 7}
PRB = {"process": "문제해결", "context": "생활맥락", "prereq": ["경우의 수", "확률의 뜻"], "ops": ["확률", "분수"], "traps": ["전체 경우 누락", "여사건"],
       "time_limit": 100, "points": 4, "tags": ["확률"], "rubric_total": 8}
SCHEMA_CNT = "fd679156-ea81-478a-9a7e-ed41751deb63"     # 독립 집합 곱셈 경우의 수
SCHEMA_PRB = "292b51aa-6fc3-46c4-9187-5079b4997b02"     # 두 독립사건 동시발생 확률


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


# ═══════════════════════════════════════════════════════════════════ 1. 경우의 수
SUM_CTX = {
    "1": ("어느 음료 자판기에는", "이온 음료", "과일 음료", "종류"),
    "2": ("어느 문구점에는", "필통", "펜", "종류"),
    "3": ("어느 분식집 메뉴에는", "김밥", "라면", "종류"),
    "4": ("어느 카페 메뉴에는", "커피", "디저트", "종류"),
    "5": ("어느 서점의 진열대에는", "소설책", "만화책", "종류"),
}


def sum_rows():
    rows = {}
    for c, (S, A, B, U) in SUM_CTX.items():
        rows[f"{c}-or"] = {"S": S, "A": A, "B": B, "U": U, "isM": 0, "OP": "+",
                           "Q": f"{A} 또는 {B} 중에서 한 {U}를 고르는 경우의 수를 구하시오.",
                           "RULE": f"{A}를 고르는 것과 {B}를 고르는 것은 동시에 일어나지 않으므로 합의 법칙으로 더한다.",
                           "LAW": "합의 법칙", "CHK": f"{A} 전부와 {B} 전부를 한 줄로 늘어놓으면 겹치는 것이 없으니 개수를 그대로 더한 것과 같다."}
        rows[f"{c}-and"] = {"S": S, "A": A, "B": B, "U": U, "isM": 1, "OP": "×",
                            "Q": f"{A}와 {B}를 각각 한 {U}씩 고르는 경우의 수를 구하시오.",
                            "RULE": f"{A} 하나마다 {B}를 고르는 경우가 그만큼씩 있으므로 곱의 법칙으로 곱한다.",
                            "LAW": "곱의 법칙", "CHK": f"가로에 {A}, 세로에 {B}를 놓고 표를 그리면 칸이 모두 채워지므로 곱이 된다."}
    return rows


SUM_ROWS = sum_rows()


def cnt_t1():
    return tpl("m2-2-counting", 1, CNT,
        title="합의 법칙과 곱의 법칙 — '또는'과 '각각 하나씩'",
        skill="두 사건이 동시에 일어나지 않으면 더하고(합), 짝을 이루면 곱한다(곱)",
        variant_axis={"법칙": "합 / 곱", "맥락": "자판기·문구점·분식집·카페·서점"},
        discriminates="'또는'과 '각각'을 읽고 합·곱을 바르게 고르는가",
        qtype="short", difficulty=1, pool_target=300, time_limit=60,
        params=[{"name": "cq", "values": {"in": list(SUM_ROWS)}}, {"name": "a", "values": {"int": [2, 7]}}, {"name": "b", "values": {"int": [2, 8]}}],
        table={"key": "cq", "rows": SUM_ROWS},
        derive={"ans": "(1 - isM)*(a + b) + isM*a*b"},
        constraints=["a != b", "ans != a", "ans != b"],
        cost_values=["a", "b", "ans"],
        verify=["isM == 0 or ans == a*b", "isM == 1 or ans == a + b"],
        question="{S} {A} {a}{U}, {B} {b}{U}가 있다. {Q}",
        answer="{ans}", answer_alt=["{ans}가지"],
        sol1="'또는'이면 두 사건이 동시에 일어나지 않으므로 경우의 수를 더하고(합의 법칙), '각각 하나씩'이면 앞의 선택 하나마다 뒤의 선택이 따라붙으므로 곱한다(곱의 법칙). {RULE}",
        sol1_fig=steps(["{A} {a}{U}, {B} {b}{U}", "{LAW}: {a} {OP} {b} = {ans}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "{A}를 고르는 경우의 수는 {a}, {B}를 고르는 경우의 수는 {b}이다.",
            "{RULE}",
            "따라서 구하는 경우의 수는 {a} {OP} {b} = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "{a} {OP} {b} = {ans}", "hint": "{LAW}"}]),
        sol2_anim=[[], [hl("hint:0")], [reveal(0)]],
        sol3="{CHK} 답은 {ans}이다.",
        model_answer="{A}를 고르는 경우의 수는 {a}, {B}를 고르는 경우의 수는 {b}이다. {RULE} 따라서 경우의 수는 {a} {OP} {b} = {ans}이다.",
        rubric=[
            {"element": "법칙 고르기", "points": 3, "criterion": "'{LAW}'을 써야 하는 까닭(동시에 일어나는지)을 밝혔다.", "partial": "법칙 이름만 쓰고 까닭이 없으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{a} {OP} {b} = {ans}{eul(ans)} 계산했다.", "partial": "식은 옳고 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "경우의 수 {ans}{eul(ans)} 답했다.", "partial": ""},
        ],
    )


Q2 = {"all": {"Q": "만들 수 있는 두 자리 자연수는 모두 몇 개인지", "i1": 1, "i2": 0, "i3": 0, "STEP": "십의 자리에는 어느 카드든 올 수 있고, 일의 자리에는 남은 카드가 온다.", "WHAT": "두 자리 자연수 전체"},
      "even": {"Q": "만들 수 있는 두 자리 자연수 중 짝수는 몇 개인지", "i1": 0, "i2": 1, "i3": 0, "STEP": "짝수이려면 일의 자리가 짝수여야 하므로 일의 자리부터 정한 뒤, 십의 자리에는 남은 카드를 놓는다.", "WHAT": "짝수"},
      "odd": {"Q": "만들 수 있는 두 자리 자연수 중 홀수는 몇 개인지", "i1": 0, "i2": 0, "i3": 1, "STEP": "홀수이려면 일의 자리가 홀수여야 하므로 일의 자리부터 정한 뒤, 십의 자리에는 남은 카드를 놓는다.", "WHAT": "홀수"}}


def cnt_t2():
    return tpl("m2-2-counting", 2, CNT,
        title="1부터 n까지의 카드로 만드는 두 자리 자연수 — 전체·짝수·홀수",
        skill="조건이 있는 자리(일의 자리)부터 정하고 곱의 법칙 쓰기",
        variant_axis={"구하는 것": "전체 / 짝수 / 홀수", "카드 수": "4~9"},
        discriminates="조건이 걸린 자리를 먼저 정하고 남은 카드 수로 곱하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "q", "values": {"in": list(Q2)}}, {"name": "n", "values": {"int": [4, 9]}}, {"name": "c", "values": {"in": ["1", "2"]}}],
        table=[{"key": "q", "rows": Q2}, {"key": "c", "rows": {"1": {"OBJ": "카드", "U": "장"}, "2": {"OBJ": "공", "U": "개"}}}],
        derive={"total": "n*(n - 1)", "fe": "floor(n/2)", "fo": "ceiling(n/2)", "ev": "floor(n/2)*(n - 1)", "od": "ceiling(n/2)*(n - 1)",
                "F": "i1*n + i2*floor(n/2) + i3*ceiling(n/2)", "ans": "i1*n*(n - 1) + i2*floor(n/2)*(n - 1) + i3*ceiling(n/2)*(n - 1)"},
        constraints=["ans != n"],
        cost_values=["n", "F", "ans"],
        verify=["ev + od == total", "ans == F*(n - 1)"],
        question="1부터 {n}까지의 자연수가 각각 하나씩 적힌 {n}{U}의 {OBJ}{ika(OBJ)} 있다. 이 중에서 두 {U}{eul(U)} 뽑아 두 자리 자연수를 만들 때, {Q} 구하시오.",
        answer="{ans}", answer_alt=["{ans}개"],
        sol1="자리마다 놓을 수 있는 {OBJ}의 수를 세어 곱한다. {STEP} 하나를 쓰면 다른 자리에는 그것을 다시 쓸 수 없으므로 남은 {OBJ}는 {n - 1}{U}이다.",
        sol1_fig=table(["", "일의 자리", "십의 자리"], [["{WHAT}", "{F}가지", "{n - 1}가지"]]),
        sol2=[
            "{STEP}",
            "먼저 정하는 자리에 올 수 있는 카드는 {F}장, 나머지 자리에는 남은 {n - 1}장 중 하나가 온다.",
            "곱의 법칙으로 {F} × {n - 1} = {ans}(개)",
        ],
        sol2_fig=steps([{"text": "{F} × {n - 1} = {ans}", "hint": "먼저 정하는 자리 × 남은 카드"}]),
        sol2_anim=[[], [hl("hint:0")], [reveal(0)]],
        sol3="두 자리 자연수는 전부 {n} × {n - 1} = {total}개이고, 그중 짝수 {ev}개와 홀수 {od}개를 더하면 {total}개로 맞아떨어진다. 답은 {ans}이다.",
        model_answer="{STEP} 먼저 정하는 자리에 {F}가지, 나머지 자리에 남은 {n - 1}가지가 올 수 있으므로 {F} × {n - 1} = {ans}(개)이다.",
        rubric=[
            {"element": "자리 정하기", "points": 3, "criterion": "조건이 있는 자리부터 정해 각 자리에 올 수 있는 카드의 수 {F}, {n - 1}{eul(n - 1)} 밝혔다.", "partial": "한 자리의 가짓수만 옳으면 1점."},
            {"element": "곱의 법칙", "points": 2, "criterion": "{F} × {n - 1} = {ans}{eul(ans)} 계산했다.", "partial": "더해서 구했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}개를 답했다.", "partial": ""},
        ],
    )


def cnt_t3():
    return tpl("m2-2-counting", 3, CNT,
        title="0을 포함한 카드로 만드는 두 자리 자연수의 개수",
        skill="십의 자리에 0이 올 수 없음을 먼저 처리하기",
        variant_axis={"카드": "0~m (m 3~8)"},
        discriminates="십의 자리에서 0을 빼고 세는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "m", "values": {"int": [3, 8]}}, {"name": "c", "values": {"in": ["1", "2"]}}],
        table={"key": "c", "rows": {"1": {"OBJ": "카드", "V": "적힌", "U": "장"}, "2": {"OBJ": "공", "V": "적힌", "U": "개"}}},
        derive={"total": "m*m", "wrong": "(m + 1)*m"},
        constraints=["total != m", "total != m + 1"],
        cost_values=["m", "total"],
        answer_var="total",
        verify=["ans == m*m", "ans < (m + 1)*m"],
        question="0부터 {m}까지의 정수가 각각 하나씩 {V} {m + 1}{U}의 {OBJ}{ika(OBJ)} 있다. 이 중에서 두 {U}{eul(U)} 뽑아 두 자리 자연수를 만들 때, 만들 수 있는 두 자리 자연수는 모두 몇 개인지 구하시오.",
        answer="{total}", answer_alt=["{total}개"],
        sol1="0이 십의 자리에 오면 두 자리 수가 되지 않는다. 그래서 십의 자리에는 0을 뺀 {m}개 중 하나가 오고, 일의 자리에는 십의 자리에 쓴 것을 뺀 나머지 {m}개(0 포함) 중 하나가 온다.",
        sol1_fig=table(["", "십의 자리", "일의 자리"], [["올 수 있는 {OBJ}", "0을 뺀 {m}개", "쓴 것을 뺀 {m}개"]]),
        sol2=[
            "십의 자리에 0은 올 수 없으므로 십의 자리에 올 수 있는 {OBJ}는 {m}개",
            "일의 자리에는 십의 자리에 쓴 {OBJ}를 뺀 나머지 {m}개(0 포함)가 올 수 있다.",
            "곱의 법칙으로 {m} × {m} = {total}(개)",
        ],
        sol2_fig=steps([{"text": "{m} × {m} = {total}", "hint": "십의 자리(0 제외) × 일의 자리(남은 것)"}]),
        sol2_anim=[[], [hl("hint:0")], [reveal(0)]],
        sol3="0을 십의 자리에도 허용하면 {m + 1} × {m} = {wrong}개인데, 그중 십의 자리가 0인 {m}개는 두 자리 수가 아니므로 {wrong} − {m} = {total}개로 같은 답이 나온다. 답은 {total}이다.",
        model_answer="십의 자리에는 0이 올 수 없으므로 {m}가지, 일의 자리에는 남은 {m}가지가 올 수 있다. 따라서 {m} × {m} = {total}(개)이다.",
        rubric=[
            {"element": "0의 처리", "points": 3, "criterion": "십의 자리에 0이 올 수 없음을 밝히고 십의 자리 {m}가지를 구했다.", "partial": "0을 빼지 않고 {m + 1}가지로 두었으면 인정하지 않는다."},
            {"element": "곱의 법칙", "points": 2, "criterion": "일의 자리 {m}가지와 곱해 {total}{eul(total)} 구했다.", "partial": "일의 자리에서 0을 또 빼서 {m - 1}가지로 두었으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{total}개를 답했다.", "partial": ""},
        ],
    )


NAMES = {"1": ["지우", "서준", "하린", "도윤", "유나"], "2": ["민준", "서아", "시우", "하은", "지호"], "3": ["예린", "준서", "수아", "현우", "다은"]}


def line_rows():
    rows = {}
    for s, nm in NAMES.items():
        for n in (3, 4, 5):
            names = nm[:n]
            base = {"NM": ", ".join(names), "N": n, "A": names[0], "B": names[1]}
            prod = lambda hi: " × ".join(str(i) for i in range(hi, 0, -1))   # noqa: E731 — 3 × 2 × 1 (교과서 표기; '× 1 =' '× 1)' 은 recheck T3 예외)
            fa = prod(n)
            fn = factorial(n)
            ja = "이" if (ord(names[0][-1]) - 0xAC00) % 28 else "가"
            jb = "이" if (ord(names[1][-1]) - 0xAC00) % 28 else "가"
            wa = "과" if (ord(names[0][-1]) - 0xAC00) % 28 else "와"
            ignore = f"조건을 무시하고 {n}명 전체를 세우는 {fn}가지로 답함"
            rows[f"{s}-{n}-all"] = {**base, "f": 1, "d": 0, "Q": f"{n}명이 한 줄로 서는 경우의 수",
                "EXPL": f"맨 앞부터 차례로 세우면 첫 자리에 {n}명, 다음 자리에 남은 {n - 1}명, … 이 올 수 있다.", "FORM": fa, "ans": fn,
                "ELM": "자리 처리", "RUB": f"맨 앞부터 차례로 놓을 수 있는 사람 수 {n}, {n - 1}, …을 세었다.", "RUBP": "첫 자리만 세고 그 뒤 자리를 빠뜨렸으면 1점.",
                "PF1": f"첫 자리의 {n}가지만 세고 뒤 자리를 세지 않음", "PF2": f"자리마다 {n}명이 다 올 수 있다고 보고 {n} × {n}{'' if n == 3 else ' × …'}으로 곱함",
                "CHK": f"맨 앞을 {names[0]}{'으로' if (ord(names[0][-1]) - 0xAC00) % 28 not in (0, 8) else '로'} 정하면 나머지 {n - 1}명을 세우는 경우가 {factorial(n - 1)}가지이고, 맨 앞에 올 수 있는 사람이 {n}명이므로 {n} × {factorial(n - 1)} = {fn}{'이' if fn % 10 in (1, 3, 6, 7, 8) or fn % 10 == 0 else '가'} 되어 같은 값이 나온다."}
            fb = prod(n - 1)
            rows[f"{s}-{n}-front"] = {**base, "f": 1, "d": 1, "Q": f"{names[0]}{ja} 맨 앞에 서는 경우의 수",
                "EXPL": f"{names[0]}의 자리를 맨 앞으로 고정하면 나머지 {n - 1}명을 한 줄로 세우는 경우의 수와 같다.", "FORM": fb, "ans": factorial(n - 1),
                "ELM": "고정 처리", "RUB": f"{names[0]}{'을' if ja == '이' else '를'} 맨 앞에 고정하고 나머지 {n - 1}명을 세우는 것으로 바꾸었다.", "RUBP": "고정한 사람을 빼지 않고 세웠으면 인정하지 않는다.",
                "PF1": f"고정한 사람을 뺀 뒤 남은 {n - 1}명을 끝까지 세우지 않고 {n - 1}가지로만 답함", "PF2": ignore,
                "CHK": f"{n}명을 아무 조건 없이 세우는 경우의 수 {fn}보다 크지 않은지 확인한다: {factorial(n - 1)} ≤ {fn}."}
            rows[f"{s}-{n}-adj"] = {**base, "f": 2, "d": 1, "Q": f"{names[0]}{wa} {names[1]}{jb} 서로 이웃하여 서는 경우의 수",
                "EXPL": f"{names[0]}, {names[1]}을 한 묶음으로 보면 {n - 1}묶음을 한 줄로 세우는 것이고, 묶음 안에서 두 사람이 자리를 바꾸는 경우가 2가지 있다.", "FORM": f"({fb}) × 2", "ans": 2 * factorial(n - 1),
                "ELM": "묶음 처리", "RUB": f"두 사람을 한 묶음으로 보고 {n - 1}묶음을 세운 뒤 묶음 안의 순서 2를 곱했다.", "RUBP": "묶음 안의 순서 2를 빠뜨렸으면 1점.",
                "PF1": "이웃하는 두 사람을 한 묶음으로 본 뒤 묶음 안에서 자리를 바꾸는 2가지를 곱하지 않음", "PF2": ignore,
                "CHK": f"{n}명을 아무 조건 없이 세우는 경우의 수 {fn}보다 크지 않은지 확인한다: {2 * factorial(n - 1)} ≤ {fn}."}
            fc = prod(n - 2)
            rows[f"{s}-{n}-ends"] = {**base, "f": 2, "d": 2, "Q": f"{names[0]}{wa} {names[1]}{jb} 양 끝에 서는 경우의 수",
                "EXPL": f"양 끝에 {names[0]}, {names[1]}을 세우는 방법이 2가지이고, 그 사이에 나머지 {n - 2}명을 한 줄로 세운다.", "FORM": (f"2 × ({fc})" if "×" in fc else f"2 × {fc}"), "ans": 2 * factorial(n - 2),
                "ELM": "양 끝 처리", "RUB": f"양 끝의 두 사람을 세우는 2가지를 먼저 처리하고 그 사이 {n - 2}명을 세웠다.", "RUBP": "양 끝의 2가지를 빠뜨렸으면 1점.",
                "PF1": "양 끝에 서는 두 사람의 자리 바꿈 2가지를 빠뜨림", "PF2": ignore,
                "CHK": f"{n}명을 아무 조건 없이 세우는 경우의 수 {fn}보다 크지 않은지 확인한다: {2 * factorial(n - 2)} ≤ {fn}."}
    return rows


LINE_ROWS = line_rows()


def cnt_t4():
    return tpl("m2-2-counting", 4, CNT,
        title="한 줄로 서기 — 전체·맨 앞 고정·이웃·양 끝",
        skill="고정할 사람을 먼저 세우고 나머지를 한 줄로 세우는 경우의 수를 곱하기",
        variant_axis={"조건": "없음 / 맨 앞 / 이웃 / 양 끝", "인원": "3~5명", "이름": "3벌"},
        discriminates="조건(고정·묶음)을 먼저 처리하고 남은 사람을 세우는가, 묶음 안 순서 2를 곱하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "r", "values": {"in": list(LINE_ROWS)}}],
        table={"key": "r", "rows": LINE_ROWS},
        derive={"chk": "f*factorial(N - d)"},
        constraints=["ans != N"],
        cost_values=["N", "f", "d", "ans"],
        answer_var="ans",
        verify=["ans == f*factorial(N - d)"],
        question="{NM} {N}명이 한 줄로 서려고 한다. {Q}를 구하시오.",
        answer="{ans}", answer_alt=["{ans}가지"],
        sol1="한 줄로 세우는 경우의 수는 앞자리부터 놓을 수 있는 사람 수를 차례로 곱해서 구한다. 조건이 있으면 조건에 걸린 사람(고정·묶음·양 끝)을 먼저 처리하고 나머지를 세운다. {EXPL}",
        sol1_fig=steps(["{NM}", "{Q}: {FORM} = {ans}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "{EXPL}",
            "따라서 경우의 수는 {FORM} = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "{FORM} = {ans}", "hint": "곱의 법칙"}]),
        sol2_anim=[[hl("hint:0")], [reveal(0)]],
        sol3="{CHK} 답은 {ans}이다.",
        model_answer="{EXPL} 따라서 경우의 수는 {FORM} = {ans}이다.",
        rubric=[
            {"element": "{ELM}", "points": 3, "criterion": "{RUB}", "partial": "{RUBP}"},
            {"element": "곱의 법칙", "points": 2, "criterion": "{FORM} = {ans}{eul(ans)} 계산했다.", "partial": "식은 옳고 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}가지를 답했다.", "partial": ""},
        ],
    )


Q5 = {"same": {"Q": "대표 2명", "isD": 0, "EXPL": "대표 2명은 자격이 같으므로 (A, B)와 (B, A)는 같은 경우이다. 순서를 생각해 뽑은 뒤 2로 나눈다.", "DIVT": " ÷ 2", "LAW": "순서를 생각하지 않으므로 2로 나눈다"},
      "diff": {"Q": "회장 1명과 부회장 1명", "isD": 1, "EXPL": "회장과 부회장은 자격이 다르므로 (A, B)와 (B, A)는 다른 경우이다. 순서를 생각해 뽑는다.", "DIVT": "", "LAW": "순서를 생각한다"}}


def cnt_t5():
    return tpl("m2-2-counting", 5, CNT,
        title="대표 뽑기 — 자격이 같을 때와 다를 때",
        skill="자격이 다르면 n × (n − 1), 자격이 같으면 그것을 2로 나누기",
        variant_axis={"자격": "대표 2명 / 회장·부회장", "후보": "4~9명"},
        discriminates="자격이 같은 두 명을 뽑을 때 2로 나누는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70,
        params=[{"name": "q", "values": {"in": list(Q5)}}, {"name": "n", "values": {"int": [4, 9]}}, {"name": "c", "values": {"in": ["1", "2", "3"]}}],
        table=[{"key": "q", "rows": Q5}, {"key": "c", "rows": {"1": {"G": "학급 회의에서 학생"}, "2": {"G": "독서 동아리에서 회원"}, "3": {"G": "축구부에서 선수"}}}],
        derive={"P": "n*(n - 1)", "ans": "n*(n - 1)/(2 - isD)"},
        constraints=["ans != n"],
        cost_values=["n", "P", "ans"],
        verify=["isD == 1 or 2*ans == n*(n - 1)", "isD == 0 or ans == n*(n - 1)"],
        question="{G} {n}명 중에서 {Q}을 뽑는 경우의 수를 구하시오.",
        answer="{ans}", answer_alt=["{ans}가지"],
        sol1="한 명씩 차례로 뽑으면 첫 번째에 {n}명, 두 번째에 남은 {n - 1}명이 될 수 있으므로 순서를 생각한 경우의 수는 {n} × {n - 1} = {P}이다. {EXPL}",
        sol1_fig=steps(["순서를 생각해 뽑기: {n} × {n - 1} = {P}", "{Q}: {P}{DIVT} = {ans}"]),
        sol1_anim=[[reveal(0)], [reveal(1)]],
        sol2=[
            "첫 번째로 뽑는 경우 {n}가지, 두 번째로 뽑는 경우 {n - 1}가지이므로 순서를 생각하면 {n} × {n - 1} = {P}",
            "{EXPL}",
            "따라서 경우의 수는 {P}{DIVT} = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "{n} × {n - 1} = {P}", "hint": "순서를 생각해 뽑기"}, {"text": "{P}{DIVT} = {ans}", "hint": "{LAW}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [hl("hint:1")], [reveal(1)]],
        sol3="자격이 같은 대표 2명의 경우의 수 {n*(n - 1)/2}{wa(n*(n - 1)/2)} 자격이 다른 회장·부회장의 경우의 수 {n*(n - 1)}{eun(n*(n - 1))} 2배 차이가 난다. 묻는 것은 {Q}이므로 답은 {ans}이다.",
        model_answer="순서를 생각해 두 명을 뽑는 경우의 수는 {n} × {n - 1} = {P}이다. {EXPL} 따라서 {P}{DIVT} = {ans}이다.",
        rubric=[
            {"element": "자격 판단", "points": 3, "criterion": "{Q}의 자격이 {LAW}는 것을 밝혔다.", "partial": "자격 구분 없이 {n} × {n - 1}만 썼으면 1점."},
            {"element": "계산", "points": 2, "criterion": "{P}{DIVT} = {ans}{eul(ans)} 계산했다.", "partial": "식은 옳고 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}가지를 답했다.", "partial": ""},
        ],
    )


Q6 = {"sum": {"Q": "합이", "isS": 1, "EXPL": "합이 정해지면 첫 번째 눈 a를 1부터 6까지 넣어 두 번째 눈 b가 1 이상 6 이하인 것만 센다.", "TB": "a를 1, 2, …, 6으로 놓고 b = (합) − a"},
      "diff": {"Q": "차가", "isS": 0, "EXPL": "차가 정해지면 (큰 눈, 작은 눈)의 짝을 세고, 두 주사위가 서로 다르므로 순서를 바꾼 경우도 센다.", "TB": "(큰 눈, 작은 눈) 짝을 세고 × 2"}}


def cnt_t6():
    return tpl("m2-2-counting", 6, CNT,
        title="서로 다른 두 주사위 — 눈의 합·차가 정해진 경우의 수",
        skill="순서쌍 (a, b)로 빠짐없이 세기",
        variant_axis={"조건": "합 / 차", "값": "합 2~12, 차 1~5"},
        discriminates="두 주사위를 구별해 (a, b)와 (b, a)를 따로 세는가, 범위 밖의 눈을 걸러 내는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=80,
        params=[{"name": "q", "values": {"in": list(Q6)}}, {"name": "k", "values": {"int": [1, 12]}}],
        table={"key": "q", "rows": Q6},
        derive={"cs": "min(k - 1, 13 - k)", "cd": "2*(6 - k)", "ans": "isS*min(k - 1, 13 - k) + (1 - isS)*2*(6 - k)"},
        constraints=["isS == 0 or k >= 2", "isS == 1 or k <= 5", "ans != k"],
        cost_values=["k", "ans"],
        verify=["isS == 0 or ans == min(k - 1, 13 - k)", "isS == 1 or ans == 2*(6 - k)"],
        question="서로 다른 두 개의 주사위를 동시에 던질 때, 나오는 두 눈의 수의 {Q} {k}인 경우의 수를 구하시오.",
        answer="{ans}", answer_alt=["{ans}가지"],
        sol1="두 주사위를 구별해 (첫 번째 눈, 두 번째 눈)의 순서쌍으로 센다 — (1, 3)과 (3, 1)은 다른 경우다. {EXPL} 눈의 수는 1부터 6까지뿐이므로 범위를 벗어나는 짝은 버린다.",
        sol1_fig=steps(["(a, b), 1 ≤ a ≤ 6, 1 ≤ b ≤ 6", "{TB}", "경우의 수 {ans}"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "{EXPL}",
            "조건을 만족시키는 순서쌍 (a, b)를 빠짐없이 나열해 세면 {ans}가지이다.",
        ],
        sol2_fig=steps([{"text": "{TB}", "hint": "순서쌍으로 세기"}, {"text": "경우의 수 = {ans}"}]),
        sol2_anim=[[hl("hint:0")], [reveal(1)]],
        sol3="두 주사위의 눈이 나오는 전체 경우의 수 36 안에서 센 것이므로 {ans}는 36보다 작다. 합은 7일 때 6가지로 가장 많고 2나 12에서 1가지로 줄어들며, 차는 0일 때 6가지, 1씩 커질 때마다 2가지씩 줄어든다는 규칙과도 맞는다. 답은 {ans}이다.",
        model_answer="두 주사위를 구별해 순서쌍 (a, b)로 나타내면 {EXPL} 조건을 만족시키는 순서쌍은 모두 {ans}가지이다.",
        rubric=[
            {"element": "순서쌍 세기", "points": 3, "criterion": "(a, b)로 조건을 만족시키는 경우를 빠짐없이 나열했다.", "partial": "(a, b)와 (b, a)를 하나로 세었으면 1점."},
            {"element": "범위 판단", "points": 2, "criterion": "눈의 수가 1 이상 6 이하인 것만 세었다.", "partial": "범위 밖의 짝을 포함했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}가지를 답했다.", "partial": ""},
        ],
    )


Q7 = {"via": {"Q": "B 지점을 거쳐 C 지점까지 가는", "isV": 1, "EXPL": "A에서 B로 가는 길 하나마다 B에서 C로 가는 길이 그만큼씩 있으므로 곱한다."},
      "all": {"Q": "C 지점까지 가는", "isV": 0, "EXPL": "B를 거쳐 가는 경우(곱)와 바로 가는 경우는 동시에 일어나지 않으므로 더한다."}}


def cnt_t7():
    return tpl("m2-2-counting", 7, CNT,
        title="길의 경우의 수 — 거쳐 가기(곱)와 바로 가기(합)",
        skill="경유하는 길은 곱하고, 다른 경로는 더하기",
        variant_axis={"구하는 것": "B 경유 / 전체", "길의 수": "2~4가지씩"},
        discriminates="경유는 곱, 별개의 경로는 합으로 구별하는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=70,
        params=[{"name": "q", "values": {"in": list(Q7)}}, {"name": "m", "values": {"int": [2, 4]}}, {"name": "n", "values": {"int": [2, 4]}}, {"name": "p", "values": {"int": [1, 3]}}],
        table={"key": "q", "rows": Q7},
        derive={"via": "m*n", "ans": "m*n + (1 - isV)*p"},
        constraints=["ans != m", "ans != n", "ans != p"],
        cost_values=["m", "n", "p", "ans"],
        verify=["isV == 0 or ans == m*n", "isV == 1 or ans == m*n + p"],
        question="A 지점에서 B 지점으로 가는 길은 {m}가지, B 지점에서 C 지점으로 가는 길은 {n}가지, A 지점에서 C 지점으로 바로 가는 길은 {p}가지가 있다. A 지점에서 출발하여 {Q} 경우의 수를 구하시오. (단, 한 번 지나간 지점은 다시 지나가지 않는다.)",
        answer="{ans}", answer_alt=["{ans}가지"],
        sol1="B를 거쳐 가는 길은 A→B와 B→C를 이어 붙이므로 곱의 법칙으로 {m} × {n} = {via}가지이다. {EXPL}",
        sol1_fig=table(["경로", "경우의 수"], [["A → B → C", "{m} × {n} = {via}"], ["A → C 바로", "{p}"]]),
        sol2=[
            "A→B {m}가지, B→C {n}가지를 이어 가므로 B를 거쳐 가는 경우의 수는 {m} × {n} = {via}",
            "{EXPL}",
            "따라서 구하는 경우의 수는 {ans}이다.",
        ],
        sol2_fig=steps([{"text": "{m} × {n} = {via}", "hint": "B 경유: 곱"}, {"text": "경우의 수 = {ans}", "hint": "{Q}"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [hl("hint:1")], [reveal(1)]],
        sol3="A에서 C로 가는 모든 길은 B 경유 {via}가지와 직행 {p}가지를 합한 {via + p}가지이고, B를 거치는 길만 세면 {via}가지이다. 묻는 것에 맞는 값은 {ans}이다.",
        model_answer="B를 거쳐 가는 경우의 수는 {m} × {n} = {via}이다. {EXPL} 따라서 경우의 수는 {ans}이다.",
        rubric=[
            {"element": "경유 경로 곱하기", "points": 3, "criterion": "A→B→C 경로를 곱의 법칙으로 {m} × {n} = {via}{ro(via)} 구했다.", "partial": "더해서 {m + n}{ro(m + n)} 구했으면 인정하지 않는다."},
            {"element": "경로 합치기", "points": 2, "criterion": "바로 가는 길을 더할지 말지 문제에 맞게 판단했다.", "partial": "직행을 곱했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}가지를 답했다.", "partial": ""},
        ],
    )


COUNT_SEED = {
    "seed_id": "m2-2-counting", "category": "활용",
    "title": "경우의 수 — 합·곱의 법칙·카드 자연수·한 줄 서기·대표·주사위·길",
    "unit_id": "m2-2", "concept_ids": ["m2-2-12"],
    "schema_id": SCHEMA_CNT, "schema_name": "독립 집합 곱셈 경우의 수 / 자격이 다른 대표 선출 / 두 지점 이동 경로",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(reference/pubs/TYPES.md 8.1)을 참고해 새로 씀. 한 줄 서기는 (이름 벌 × 인원 × 조건) 합성 키 표 — 수식·답까지 행에 고정.",
    "geometry": False,
    "templates": [cnt_t1(), cnt_t2(), cnt_t3(), cnt_t4(), cnt_t5(), cnt_t6(), cnt_t7()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 확률
BAG_CTX = {"1": {"OBJ": "장의 카드 중에서", "ONE": "한 장", "V": "뽑을"}, "2": {"OBJ": "개의 공이 들어 있는 주머니에서", "ONE": "한 개", "V": "꺼낼"}}


def prb_t1():
    return tpl("m2-2-probability", 1, PRB,
        title="1부터 N까지 중 하나를 뽑을 때 k의 배수일 확률",
        skill="전체 경우의 수 N과 사건의 경우의 수(N 이하의 k의 배수 개수)로 확률 만들기",
        variant_axis={"N": "10~40", "k": "2~7", "맥락": "카드 / 공"},
        note="m/N이 약분되는 경우만 (gcd(m, N) > 1) — 풀이·채점 요소가 '약분'을 전제로 쓰였다.",
        discriminates="k의 배수의 개수를 N ÷ k의 몫으로 세고 약분하는가",
        qtype="short", difficulty=1, pool_target=300, time_limit=70,
        params=[{"name": "c", "values": {"in": list(BAG_CTX)}}, {"name": "N", "values": {"int": [10, 40]}}, {"name": "k", "values": {"in": [2, 3, 4, 5, 6, 7]}}],
        table={"key": "c", "rows": BAG_CTX},
        derive={"m": "floor(N/k)", "ans": "floor(N/k)/N"},
        constraints=["m >= 3", "gcd(m, N) > 1"],   # m = 2면 "k, 2k, …, 2k" 꼴의 나열이 어색하다
        cost_values=["N", "k", "m", "ans"],
        answer_var="ans",
        verify=["ans == floor(N/k)/N", "ans*N == m"],
        question="1부터 {N}까지의 자연수가 각각 하나씩 적힌 {N}{OBJ} {ONE}{eul(ONE)} 임의로 {V} 때, {k}의 배수가 적힌 것이 나올 확률을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="확률은 (사건의 경우의 수) ÷ (전체 경우의 수)이다. 전체는 {N}가지이고, {k}의 배수는 {k}, {2*k}, …, {k*m}의 {m}개이므로 {m}/{N}을 약분한다. {N}을 {k}로 나눈 몫이 그대로 배수의 개수임을 이용하면 빠르다.",
        sol1_fig=steps(["전체 경우의 수: {N}", "{k}의 배수: {k}, {2*k}, …, {k*m} → {m}개", "확률 = [[frac({m}, {N})]] = [[{ans}]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "모든 경우의 수는 {N}이다.",
            "{N} 이하의 {k}의 배수는 {k}, {2*k}, …, {k*m}의 {m}개이다.",
            "따라서 확률은 [[frac({m}, {N})]] = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "{N} ÷ {k} = {m} …", "hint": "몫이 배수의 개수"}, {"text": "[[frac({m}, {N})]] = [[{ans}]]", "hint": "약분"}]),
        sol2_anim=[[], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")]],
        sol3="{k} × {m} = {k*m} ≤ {N}이고 {k} × {m + 1} = {k*(m + 1)} > {N}이므로 배수는 {m}개가 맞다. 확률 {ans}{eun(ans)} 0과 1 사이의 값이다. 답은 {ans}이다.",
        model_answer="모든 경우의 수는 {N}이고, {N} 이하의 {k}의 배수는 {m}개이다. 따라서 확률은 [[frac({m}, {N})]] = {ans}이다.",
        rubric=[
            {"element": "전체 경우의 수", "points": 3, "criterion": "모든 경우의 수가 {N}임을 밝혔다.", "partial": ""},
            {"element": "사건의 경우의 수·확률", "points": 3, "criterion": "{k}의 배수가 {m}개임을 세고 [[frac({m}, {N})]]{eul(m)} 만들었다.", "partial": "배수의 개수가 하나 어긋나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "약분한 {ans}{eul(ans)} 답했다.", "partial": "약분하지 않았으면 1점."},
        ],
    )


def prb_t8():
    # t1의 짝 — m/N이 이미 기약분수인 경우(gcd(m, N) = 1). 풀이·채점에 '약분' 단계가 없고, 답이 분수 그대로임을 확인하는 요소를 둔다.
    return tpl("m2-2-probability", 8, PRB,
        title="1부터 N까지 중 하나를 뽑을 때 k의 배수일 확률 — 기약분수 그대로인 경우",
        skill="전체 경우의 수 N과 사건의 경우의 수(N 이하의 k의 배수 개수)로 확률을 만들고, 더 약분되지 않음을 확인하기",
        variant_axis={"N": "10~40", "k": "2~7", "맥락": "카드 / 공"},
        note="m/N이 기약분수인 경우만 (gcd(m, N) = 1) — t1과 짝을 이룬다. 약분 단계가 없으므로 '약분' 문구를 쓰지 않는다.",
        discriminates="k의 배수의 개수를 N ÷ k의 몫으로 세고, 분수가 이미 기약분수임을 확인하는가",
        qtype="short", difficulty=1, pool_target=300, time_limit=70,
        params=[{"name": "c", "values": {"in": list(BAG_CTX)}}, {"name": "N", "values": {"int": [10, 40]}}, {"name": "k", "values": {"in": [2, 3, 4, 5, 6, 7]}}],
        table={"key": "c", "rows": BAG_CTX},
        derive={"m": "floor(N/k)", "ans": "floor(N/k)/N"},
        constraints=["m >= 3", "gcd(m, N) == 1"],
        cost_values=["N", "k", "m", "ans"],
        answer_var="ans",
        verify=["ans == floor(N/k)/N", "ans*N == m"],
        question="1부터 {N}까지의 자연수가 각각 하나씩 적힌 {N}{OBJ} {ONE}{eul(ONE)} 임의로 {V} 때, {k}의 배수가 적힌 것이 나올 확률을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="확률은 (사건의 경우의 수) ÷ (전체 경우의 수)이다. 전체는 {N}가지이고, {k}의 배수는 {k}, {2*k}, …, {k*m}의 {m}개이므로 확률은 [[frac({m}, {N})]]이다. {m}과 {N}은 1 이외의 공약수가 없어 더 약분되지 않는다. {N}을 {k}로 나눈 몫이 그대로 배수의 개수임을 이용하면 빠르다.",
        sol1_fig=steps(["전체 경우의 수: {N}", "{k}의 배수: {k}, {2*k}, …, {k*m} → {m}개", "확률 = [[frac({m}, {N})]] (기약분수)"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "모든 경우의 수는 {N}이다.",
            "{N} 이하의 {k}의 배수는 {k}, {2*k}, …, {k*m}의 {m}개이다.",
            "따라서 확률은 [[frac({m}, {N})]]이고, {m}과 {N}의 최대공약수가 1이므로 이것이 기약분수이다.",
        ],
        sol2_fig=steps([{"text": "{N} ÷ {k} = {m} …", "hint": "몫이 배수의 개수"}, {"text": "확률 = [[frac({m}, {N})]]", "hint": "기약분수 확인"}]),
        sol2_anim=[[], [reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")]],
        sol3="{k} × {m} = {k*m} ≤ {N}이고 {k} × {m + 1} = {k*(m + 1)} > {N}이므로 배수는 {m}개가 맞다. {m}과 {N}의 최대공약수는 1이다. 답은 {ans}이다.",
        model_answer="모든 경우의 수는 {N}이고, {N} 이하의 {k}의 배수는 {m}개이다. 따라서 확률은 {ans}이다.",
        rubric=[
            {"element": "전체 경우의 수", "points": 3, "criterion": "모든 경우의 수가 {N}임을 밝혔다.", "partial": ""},
            {"element": "사건의 경우의 수·확률", "points": 3, "criterion": "{k}의 배수가 {m}개임을 세고 [[frac({m}, {N})]]{eul(m)} 만들었다.", "partial": "배수의 개수가 하나 어긋나면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}{eul(ans)} 답했다.", "partial": "분수를 소수로 어림해 답했으면 1점."},
        ],
    )


def prb_t2():
    return tpl("m2-2-probability", 2, PRB,
        title="서로 다른 두 주사위 — 눈의 합이 k일 확률",
        skill="전체 36가지와 합이 k인 순서쌍의 개수로 확률 만들기",
        variant_axis={"k": "3~11 (c/36이 약분되는 것만: 6, 8 제외)"},
        discriminates="전체 경우 36을 쓰고 순서쌍을 빠짐없이 세는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=80,
        params=[{"name": "k", "values": {"int": [3, 11]}}],
        derive={"c": "min(k - 1, 13 - k)", "ans": "min(k - 1, 13 - k)/36"},
        constraints=["gcd(c, 36) > 1"],
        cost_values=["k", "c", "ans"],
        answer_var="ans",
        verify=["ans*36 == c"],
        question="서로 다른 두 개의 주사위를 동시에 던질 때, 나오는 두 눈의 수의 합이 {k}일 확률을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 주사위를 구별하면 모든 경우의 수는 6 × 6 = 36이다. 합이 {k}인 순서쌍 (a, b)는 a = 1, 2, …를 넣어 b = {k} − a가 1 이상 6 이하인 것을 세면 {c}개다. 확률은 {c}/36을 약분한 값이다.",
        sol1_fig=steps(["전체: 6 × 6 = 36", "합이 {k}: (a, {k} − a) 꼴 → {c}개", "확률 = [[frac({c}, 36)]] = [[{ans}]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "모든 경우의 수는 6 × 6 = 36이다.",
            "합이 {k}인 순서쌍은 (a, {k} − a)에서 a와 {k} − a가 모두 1 이상 6 이하인 것이므로 {c}개이다.",
            "따라서 확률은 [[frac({c}, 36)]] = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "36", "hint": "전체"}, {"text": "합 {k}: {c}가지", "hint": "순서쌍"}, {"text": "[[frac({c}, 36)]] = [[{ans}]]"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="합이 2부터 12까지인 경우의 수는 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1로 모두 더하면 36이 되고, 합 {k}에 해당하는 값은 {c}이다. 답은 {ans}이다.",
        model_answer="모든 경우의 수는 36이고, 합이 {k}인 경우는 {c}가지이다. 따라서 확률은 [[frac({c}, 36)]] = {ans}이다.",
        rubric=[
            {"element": "전체 경우의 수", "points": 3, "criterion": "두 주사위를 구별해 모든 경우의 수 36을 밝혔다.", "partial": "6 + 6 = 12 등으로 잘못 세었으면 인정하지 않는다."},
            {"element": "사건의 경우의 수·확률", "points": 3, "criterion": "합이 {k}인 순서쌍 {c}개를 세고 [[frac({c}, 36)]]{eul(c)} 만들었다.", "partial": "순서쌍을 하나 빠뜨리거나 더 세었으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "약분한 {ans}{eul(ans)} 답했다.", "partial": "약분하지 않았으면 1점."},
        ],
    )


Q3 = {"least": {"Q": "적어도 한 개는 앞면이 나올", "isL": 1, "EXPL": "'적어도 한 개는 앞면'의 반대는 '모두 뒷면'이다. 여사건의 확률을 1에서 뺀다.", "FORM": "1 − (모두 뒷면일 확률)"},
      "all": {"Q": "모두 앞면이 나올", "isL": 0, "EXPL": "모두 앞면인 경우는 한 가지뿐이다.", "FORM": "(모두 앞면인 경우 1가지) ÷ (전체)"}}


def coin_rows():
    rows = {}
    for q, qr in Q3.items():
        for n in (2, 3, 4):
            T = 2 ** n
            rows[f"{q}-{n}"] = {**qr, "n": n, "T": T, "PROD": " × ".join(["2"] * n),
                                "FORMN": (f"1 − [[frac(1, {T})]]" if q == "least" else f"1 ÷ {T}")}
    return rows


COIN_ROWS = coin_rows()


def prb_t3():
    return tpl("m2-2-probability", 3, PRB,
        title="동전 n개 — '적어도 한 개는 앞면'과 '모두 앞면'",
        skill="'적어도'는 여사건(모두 뒷면)의 확률을 1에서 빼기",
        variant_axis={"구하는 것": "적어도 한 개 앞면 / 모두 앞면", "동전 수": "2~4개"},
        discriminates="'적어도'를 여사건으로 바꾸어 1 − p로 구하는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=80,
        params=[{"name": "r", "values": {"in": list(COIN_ROWS)}}],
        table={"key": "r", "rows": COIN_ROWS},
        derive={"p1": "1/2**n", "ans": "isL*(1 - 1/2**n) + (1 - isL)/2**n"},
        constraints=[],
        cost_values=["n", "T", "ans"],
        answer_var="ans",
        verify=["isL == 0 or ans == 1 - 1/2**n", "isL == 1 or ans == 1/2**n"],
        question="서로 다른 {n}개의 동전을 동시에 던질 때, {Q} 확률을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="동전 하나마다 앞·뒤 2가지이므로 모든 경우의 수는 {PROD} = {T}이다. 모두 앞면(또는 모두 뒷면)인 경우는 1가지뿐이므로 그 확률은 1/{T}이다. {EXPL}",
        sol1_fig=steps(["전체: {PROD} = {T}", "모두 뒷면(또는 모두 앞면): 1가지 → [[frac(1, {T})]]", "{FORMN} = [[{ans}]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "모든 경우의 수는 {PROD} = {T}이다.",
            "{EXPL}",
            "따라서 확률은 {FORMN} = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "전체 {PROD} = {T}", "hint": "동전마다 2가지"}, {"text": "{FORM}", "hint": "{Q} 확률"}, {"text": "{FORMN} = [[{ans}]]"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="'적어도 한 개는 앞면'과 '모두 뒷면'은 서로 여사건이므로 두 확률을 더하면 1이 되어야 한다: {1 - p1} + {p1} = 1. 묻는 것에 맞는 값은 {ans}이다.",
        model_answer="모든 경우의 수는 {PROD} = {T}이다. {EXPL} 따라서 확률은 {FORMN} = {ans}이다.",
        rubric=[
            {"element": "전체 경우의 수", "points": 3, "criterion": "모든 경우의 수 {T}{eul(T)} 밝혔다.", "partial": "2 × {n}으로 잘못 세었으면 인정하지 않는다."},
            {"element": "여사건·확률", "points": 3, "criterion": "{FORM}으로 확률을 세웠다.", "partial": "모두 뒷면일 확률까지만 구했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}{eul(ans)} 답했다.", "partial": ""},
        ],
    )


def prb_t4():
    return tpl("m2-2-probability", 4, PRB,
        title="두 주사위 — 적어도 하나는 k 이상의 눈이 나올 확률",
        skill="여사건(두 눈이 모두 k − 1 이하)의 확률을 1에서 빼기",
        variant_axis={"k": "2~6"},
        discriminates="여사건 '둘 다 k − 1 이하'를 세워 1 − p로 구하는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=90,
        params=[{"name": "k", "values": {"int": [2, 6]}}],
        derive={"j": "k - 1", "cc": "(k - 1)**2", "pc": "(k - 1)**2/36", "ans": "1 - (k - 1)**2/36"},
        constraints=[],
        cost_values=["k", "cc", "ans"],
        answer_var="ans",
        verify=["ans == 1 - (k - 1)**2/36"],
        question="서로 다른 두 개의 주사위를 동시에 던질 때, 적어도 하나는 {k} 이상의 눈이 나올 확률을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="'적어도 하나는 {k} 이상'의 반대(여사건)는 '두 눈이 모두 {j} 이하'이다. 두 눈이 모두 {j} 이하인 경우는 {j} × {j} = {cc}가지이므로 그 확률을 1에서 뺀다. 직접 세면 경우가 많아 여사건이 훨씬 빠르다.",
        sol1_fig=steps(["전체: 36", "여사건 — 둘 다 {j} 이하: {j} × {j} = {cc}가지 → [[frac({cc}, 36)]]", "1 − [[frac({cc}, 36)]] = [[{ans}]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "모든 경우의 수는 6 × 6 = 36이다.",
            "여사건 '두 눈이 모두 {j} 이하'인 경우의 수는 {j} × {j} = {cc}이므로 그 확률은 36가지 중 {cc}가지, 곧 {pc}이다.",
            "따라서 구하는 확률은 1 − {pc} = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "36", "hint": "전체"}, {"text": "{j} × {j} = {cc}", "hint": "여사건: 둘 다 {j} 이하"}, {"text": "1 − [[frac({cc}, 36)]] = [[{ans}]]"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="직접 세면 적어도 하나가 {k} 이상인 경우의 수는 36 − {cc} = {36 - cc}가지이고, 이를 36으로 나눈 값은 {ans}{wa(ans)} 같다. 답은 {ans}이다.",
        model_answer="모든 경우의 수는 36이고, 여사건인 두 눈이 모두 {j} 이하인 경우의 수는 {j} × {j} = {cc}이다. 따라서 확률은 1 − [[frac({cc}, 36)]] = {ans}이다.",
        rubric=[
            {"element": "여사건 세우기", "points": 3, "criterion": "'적어도 하나는 {k} 이상'의 여사건이 '둘 다 {j} 이하'임을 밝혔다.", "partial": "여사건을 '둘 다 {k} 이상'으로 잘못 잡았으면 인정하지 않는다."},
            {"element": "확률 계산", "points": 3, "criterion": "여사건의 경우의 수 {cc}와 확률 [[frac({cc}, 36)]]{eul(cc)} 구해 1에서 뺐다.", "partial": "여사건 확률까지만 구했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}{eul(ans)} 답했다.", "partial": "약분하지 않았으면 1점."},
        ],
    )


def prb_t5():
    return tpl("m2-2-probability", 5, PRB,
        title="a의 배수 또는 b의 배수일 확률 (서로 배반)",
        skill="두 사건이 동시에 일어나지 않으면 확률을 더하기",
        variant_axis={"N": "20~50", "a, b": "서로 겹치지 않는 배수(ab > N)"},
        discriminates="두 사건이 겹치지 않음을 확인하고 확률을 더하는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=90,
        params=[{"name": "N", "values": {"int": [20, 50]}}, {"name": "a", "values": {"in": [3, 4, 5, 6, 7]}}, {"name": "b", "values": {"in": [7, 9, 11, 13, 17]}}],
        derive={"ma": "floor(N/a)", "mb": "floor(N/b)", "ans": "(floor(N/a) + floor(N/b))/N"},
        constraints=["a*b > N", "a < b", "mb >= 1"],
        cost_values=["N", "a", "b", "ma", "mb", "ans"],
        answer_var="ans",
        verify=["ans*N == ma + mb", "a*b > N"],
        question="1부터 {N}까지의 자연수가 각각 하나씩 적힌 {N}장의 카드 중에서 한 장을 임의로 뽑을 때, {a}의 배수 또는 {b}의 배수가 적힌 카드가 나올 확률을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{a}의 배수이면서 {b}의 배수인 수는 {a} × {b} = {a*b}의 배수인데 {a*b} > {N}이므로 {N} 이하에는 없다. 두 사건이 동시에 일어나지 않으므로(서로 배반) '또는'의 확률은 각각의 확률을 더한 것이다.",
        sol1_fig=steps(["{a}의 배수: {ma}개, {b}의 배수: {mb}개", "겹치는 수(공배수 {a*b}의 배수): 없음", "[[frac({ma}, {N})]] + [[frac({mb}, {N})]] = [[{ans}]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "모든 경우의 수는 {N}이다. {a}의 배수는 {ma}개, {b}의 배수는 {mb}개이다.",
            "{a}와 {b}의 공배수 {a*b}{eun(a*b)} {N}보다 크므로 두 사건은 동시에 일어나지 않는다.",
            "따라서 확률은 [[frac({ma}, {N})]] + [[frac({mb}, {N})]] = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "{ma}개, {mb}개", "hint": "각 배수의 개수"}, {"text": "공배수 없음 ({a*b} > {N})", "hint": "서로 배반"}, {"text": "[[frac({ma}, {N})]] + [[frac({mb}, {N})]] = [[{ans}]]"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="{a}의 배수 {ma}개와 {b}의 배수 {mb}개를 나열하면 같은 수가 없으므로 사건의 경우의 수는 {ma + mb}이고, 확률 {ans}{eun(ans)} 1을 넘지 않는다. 답은 {ans}이다.",
        model_answer="모든 경우의 수는 {N}이고, {a}의 배수는 {ma}개, {b}의 배수는 {mb}개이며 두 사건은 동시에 일어나지 않는다. 따라서 확률은 [[frac({ma}, {N})]] + [[frac({mb}, {N})]] = {ans}이다.",
        rubric=[
            {"element": "배반 판단", "points": 3, "criterion": "두 사건이 동시에 일어나지 않음(공배수가 {N} 이하에 없음)을 밝혔다.", "partial": "확인 없이 더하기만 했으면 1점."},
            {"element": "확률 더하기", "points": 3, "criterion": "각 배수의 개수 {ma}, {mb}{eul(mb)} 세어 확률을 더했다.", "partial": "한쪽 개수만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "약분한 {ans}{eul(ans)} 답했다.", "partial": "약분하지 않았으면 1점."},
        ],
    )


PAIRS = {"1": {"n1": 1, "d1": 2}, "2": {"n1": 2, "d1": 3}, "3": {"n1": 3, "d1": 4}, "4": {"n1": 3, "d1": 5}, "5": {"n1": 4, "d1": 5}, "6": {"n1": 5, "d1": 6}, "7": {"n1": 2, "d1": 5}, "8": {"n1": 1, "d1": 3}}
PAIRS2 = {k: {"n2": v["n1"], "d2": v["d1"]} for k, v in PAIRS.items()}
IND_CTX = {
    "1": {"S": "지우와 서준이가 다트를 던져 풍선을 터뜨릴 확률이 각각", "A": "지우", "B": "서준", "E": "풍선을 터뜨릴", "ACT": "두 사람이 각각 한 번씩 다트를 던질 때", "NOTE": "두 사람의 결과는 서로 영향을 끼치지 않는다"},
    "2": {"S": "두 농구 선수 A, B가 자유투를 성공할 확률이 각각", "A": "A", "B": "B", "E": "자유투를 성공할", "ACT": "두 선수가 각각 한 번씩 자유투를 던질 때", "NOTE": "두 선수의 결과는 서로 영향을 끼치지 않는다"},
    "3": {"S": "두 씨앗 A, B가 같은 조건에서 싹이 틀 확률이 각각", "A": "A", "B": "B", "E": "싹이 틀", "ACT": "두 씨앗을 하나씩 심을 때", "NOTE": "두 씨앗이 싹이 트는 것은 서로 영향을 끼치지 않는다"},
}
QI = {"both": {"iB": 1, "iA": 0, "iL": 0, "iN": 0, "FORM": "p × q", "PRE": "", "EXPL": "둘 다 일어나야 하므로 두 확률을 곱한다.",
               "ELM1": "쓸 확률 고르기", "WHICH": "둘 다 성공하므로 성공할", "STEP1": "둘 다 성공해야 하므로 곱할 성공", "HINT1": "성공, 성공", "PF1": "성공 확률 대신 실패 확률 1 − p를 곱함"},
      "onlyA": {"iB": 0, "iA": 1, "iL": 0, "iN": 0, "FORM": "p × (1 − q)", "PRE": "", "EXPL": "앞쪽은 성공하고 뒤쪽은 실패해야 하므로 p와 (1 − q)를 곱한다.",
                "ELM1": "실패 확률", "HINT1": "성공, 실패 = 1 − q", "PF1": "실패할 확률을 1 − q가 아니라 q로 씀"},
      "least": {"iB": 0, "iA": 0, "iL": 1, "iN": 0, "FORM": "1 − (1 − p)(1 − q)", "PRE": "1 − ", "EXPL": "여사건 '둘 다 실패'의 확률 (1 − p)(1 − q)를 1에서 뺀다.",
                "ELM1": "실패 확률", "WHICH": "여사건 '둘 다 실패'에 쓸 실패", "STEP1": "여사건 '둘 다 실패'에 쓸 실패(1 − p, 1 − q)", "HINT1": "실패, 실패 (여사건)", "PF1": "실패할 확률을 1 − p가 아니라 p로 씀"},
      "none": {"iB": 0, "iA": 0, "iL": 0, "iN": 1, "FORM": "(1 − p)(1 − q)", "PRE": "", "EXPL": "둘 다 실패해야 하므로 실패할 확률끼리 곱한다.",
               "ELM1": "실패 확률", "WHICH": "둘 다 실패하므로 실패할", "STEP1": "둘 다 실패해야 하므로 곱할 실패(1 − p, 1 − q)", "HINT1": "실패, 실패", "PF1": "실패할 확률을 1 − p가 아니라 p로 씀"}}


def ind_rows():
    rows = {}
    for c, ctx in IND_CTX.items():
        A, B, E = ctx["A"], ctx["B"], ctx["E"]
        neg = E.replace("터뜨릴", "터뜨리지 못할").replace("성공할", "실패할").replace("싹이 틀", "싹이 트지 않을")
        qs = {"both": f"둘 다 {E}", "onlyA": f"{A}만 {E}", "least": f"적어도 한쪽은 {E}", "none": f"둘 다 {neg}"}
        for q, qrow in QI.items():
            row = {**ctx, **qrow, "Q": qs[q]}
            if q == "onlyA":
                row["WHICH"] = f"{A}의 성공과 {B}의 실패"
                row["STEP1"] = f"{A}의 성공, {B}의 실패(1 − q)"
            rows[f"{c}-{q}"] = row
    return rows


IND_ROWS = ind_rows()


def prb_t6():
    return tpl("m2-2-probability", 6, PRB,
        title="두 사람의 독립 시행 — 둘 다·한 쪽만·적어도 한 쪽·둘 다 실패",
        skill="서로 영향을 주지 않는 두 사건은 확률을 곱하고, '적어도'는 여사건으로",
        variant_axis={"구하는 것": "둘 다 / A만 / 적어도 / 둘 다 실패", "확률": "분수 8종 × 8종", "맥락": "다트·자유투·씨앗"},
        discriminates="실패 확률 1 − p를 쓰는가, '적어도'를 여사건으로 처리하는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=110,
        params=[{"name": "cq", "values": {"in": list(IND_ROWS)}}, {"name": "p1", "values": {"in": list(PAIRS)}}, {"name": "p2", "values": {"in": list(PAIRS2)}}],
        table=[{"key": "cq", "rows": IND_ROWS}, {"key": "p1", "rows": PAIRS}, {"key": "p2", "rows": PAIRS2}],
        derive={"p": "n1/d1", "qq": "n2/d2", "fp": "1 - n1/d1", "fq": "1 - n2/d2",
                "x1": "(iB + iA)*n1/d1 + (iL + iN)*(1 - n1/d1)", "x2": "iB*n2/d2 + (iA + iL + iN)*(1 - n2/d2)",
                "ans": "iB*(n1/d1)*(n2/d2) + iA*(n1/d1)*(1 - n2/d2) + iL*(1 - (1 - n1/d1)*(1 - n2/d2)) + iN*(1 - n1/d1)*(1 - n2/d2)"},
        constraints=["p1 != p2"],
        cost_values=["n1", "d1", "n2", "d2", "ans"],
        answer_var="ans",
        verify=["ans > 0", "ans < 1", "iL == 0 or ans == 1 - x1*x2", "iL == 1 or ans == x1*x2", "iB == 0 or ans == (n1/d1)*(n2/d2)"],
        question="{S} {p}, {qq}이다. {ACT}, {Q} 확률을 구하시오. (단, {NOTE}.)",
        answer="{ans}", answer_alt=[],
        sol1="한쪽이 성공할 확률이 p이면 실패할 확률은 1 − p이다. 두 시행이 서로 영향을 주지 않으므로 '그리고'는 확률의 곱이다. {EXPL}",
        sol1_fig=table(["", "{A}", "{B}"], [["성공", "{n1}/{d1}", "{n2}/{d2}"], ["실패", "{d1 - n1}/{d1}", "{d2 - n2}/{d2}"]]),
        sol2=[
            "성공할 확률이 p이면 실패할 확률은 1 − p이다. {STEP1} 확률은 {x1}, {x2}이다.",
            "{EXPL}",
            "따라서 확률은 {PRE}{x1} × {x2} = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "[[{x1}]], [[{x2}]]", "hint": "{HINT1}"}, {"text": "{FORM}", "hint": "{Q} 확률"}, {"text": "{PRE}[[{x1}]] × [[{x2}]] = [[{ans}]]"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="네 경우(둘 다 성공 {p*qq}, {A}만 {p*fq}, {B}만 {fp*qq}, 둘 다 실패 {fp*fq})의 확률을 모두 더하면 1이 된다. 묻는 것에 맞는 값은 {ans}이다.",
        model_answer="{STEP1} 확률은 {x1}, {x2}이다. {EXPL} 따라서 확률은 {PRE}{x1} × {x2} = {ans}이다.",
        rubric=[
            {"element": "{ELM1}", "points": 3, "criterion": "{WHICH} 확률 {x1}, {x2}{eul(x2)} 구했다.", "partial": "한쪽만 옳으면 1점."},
            {"element": "곱·여사건", "points": 3, "criterion": "{FORM}으로 식을 세웠다.", "partial": "곱 대신 더했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "{ans}{eul(ans)} 답했다.", "partial": "약분하지 않았으면 1점."},
        ],
    )


QR = {"rep": {"Q": "확인하고 다시 넣은 후", "isR": 1, "EXPL": "다시 넣으므로 두 번째에도 공의 수가 처음과 같다. 두 번의 확률이 같으므로 곱한다.", "SECOND": "두 번째도 처음과 같은 확률"},
      "norep": {"Q": "확인하고 다시 넣지 않고", "isR": 0, "EXPL": "다시 넣지 않으므로 두 번째에는 흰 공이 한 개 줄고 전체도 한 개 준다. 바뀐 확률을 곱한다.", "SECOND": "두 번째는 공이 하나 줄어든 확률"}}


def prb_t7():
    return tpl("m2-2-probability", 7, PRB,
        title="연속하여 두 번 꺼내기 — 다시 넣을 때와 넣지 않을 때",
        skill="복원이면 같은 확률의 곱, 비복원이면 줄어든 개수로 두 번째 확률을 고쳐 곱하기",
        variant_axis={"복원": "다시 넣음 / 넣지 않음", "공": "흰 2~6, 검은 2~6"},
        discriminates="비복원에서 두 번째 확률의 분자·분모를 모두 1씩 줄이는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=100,
        params=[{"name": "q", "values": {"in": list(QR)}}, {"name": "a", "values": {"int": [2, 6]}}, {"name": "b", "values": {"int": [2, 6]}}],
        table={"key": "q", "rows": QR},
        derive={"T": "a + b", "p1": "a/(a + b)", "p2": "isR*a/(a + b) + (1 - isR)*(a - 1)/(a + b - 1)", "ans": "(a/(a + b))*(isR*a/(a + b) + (1 - isR)*(a - 1)/(a + b - 1))"},
        constraints=["a != b"],
        cost_values=["a", "b", "T", "p1", "p2", "ans"],
        answer_var="ans",
        verify=["ans == p1*p2", "isR == 1 or ans == a*(a - 1)/((a + b)*(a + b - 1))"],
        question="주머니에 흰 공 {a}개, 검은 공 {b}개가 들어 있다. 이 주머니에서 공 한 개를 임의로 꺼내 색을 {Q} 다시 한 개를 임의로 꺼낼 때, 두 번 모두 흰 공이 나올 확률을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="첫 번째에는 전체 {T}개 중 흰 공이 {a}개이므로 흰 공이 나올 확률은 {p1}이다. {EXPL} 두 번째 확률은 {p2}이고, 두 번 모두 일어나야 하므로 두 확률을 곱한다.",
        sol1_fig=table(["", "흰 공", "전체", "확률"], [["첫 번째", "{a}", "{T}", "{a}/{T}"], ["두 번째", "{a - 1 + isR}", "{T - 1 + isR}", "{a - 1 + isR}/{T - 1 + isR}"]]),
        sol2=[
            "첫 번째에는 전체 {T}개 중 흰 공이 {a}개이므로 흰 공이 나올 확률은 {p1}이다.",
            "{EXPL} 두 번째에는 전체 {T - 1 + isR}개 중 흰 공이 {a - 1 + isR}개이므로 확률은 {p2}이다.",
            "따라서 확률은 {p1} × {p2} = {ans}이다.",
        ],
        sol2_fig=steps([{"text": "첫 번째 [[{p1}]]", "hint": "흰 {a} / 전체 {T}"}, {"text": "두 번째 [[{p2}]]", "hint": "{SECOND}"}, {"text": "[[{p1}]] × [[{p2}]] = [[{ans}]]"}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="다시 넣으면 [[frac({a}, {T})]] × [[frac({a}, {T})]] = {a*a/(T*T)}, 넣지 않으면 [[frac({a}, {T})]] × [[frac({a - 1}, {T - 1})]] = {a*(a - 1)/(T*(T - 1))}로 서로 다르며, 넣지 않을 때가 더 작다(흰 공이 하나 줄었으므로). 문제의 조건에 맞는 값은 {ans}이다.",
        model_answer="첫 번째에 흰 공이 나올 확률은 {p1}이고, {EXPL} 두 번째 확률은 {p2}이다. 따라서 두 번 모두 흰 공이 나올 확률은 {p1} × {p2} = {ans}이다.",
        rubric=[
            {"element": "두 번째 확률", "points": 3, "criterion": "{SECOND}로 {p2}{eul(p2)} 구했다.", "partial": "복원·비복원을 반대로 처리했으면 인정하지 않는다."},
            {"element": "확률의 곱", "points": 3, "criterion": "{p1} × {p2}{ro(p2)} 곱했다.", "partial": "곱 대신 더했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "약분한 {ans}{eul(ans)} 답했다.", "partial": "약분하지 않았으면 1점."},
        ],
    )


PROB_SEED = {
    "seed_id": "m2-2-probability", "category": "활용",
    "title": "확률 — 배수·주사위 합·여사건(동전·주사위)·또는·독립 시행·복원/비복원",
    "unit_id": "m2-2", "concept_ids": ["m2-2-13", "m2-2-14"],
    "schema_id": SCHEMA_PRB, "schema_name": "두 독립사건 동시발생 확률 / 여사건 확률 / 사건 A 또는 B / 복원추출·비복원 연속추출",
    "source_item_ids": [],
    "note": "출판사 평가자료 유형(reference/pubs/TYPES.md 8.2~8.4)을 참고해 새로 씀. 답은 Fraction 파생 → [[frac]] 마커. 확률 값(p, q)은 분수 표(PAIRS).",
    "geometry": False,
    "templates": [prb_t1(), prb_t2(), prb_t3(), prb_t4(), prb_t5(), prb_t6(), prb_t7(), prb_t8()],
}


if __name__ == "__main__":
    for seed in (COUNT_SEED, PROB_SEED):
        with_pitfalls(seed)
        dump(seed)
