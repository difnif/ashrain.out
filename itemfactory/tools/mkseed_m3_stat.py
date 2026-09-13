# itemfactory/tools/mkseed_m3_stat.py — m3-2 통계 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m3_stat.py
#     → seeds/m3-2-stat.json (대푯값과 산포도: 평균→미지수·중앙값/최빈값·편차·분산/표준편차·변환 자료의 분산, 5틀)
#
# 자료는 표에서 미리 만든 문자열(DATA)·수치. 산점도·상관관계(m3-2-14)는 그림이 필요해 보류.
from __future__ import annotations

import itertools
import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, table, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


BASE = {"process": "절차수행", "context": "자료맥락", "time_limit": 90, "points": 4, "qtype": "short", "pool_target": 300}
ST = "m3-2-stat"
ST_BASE = {**BASE, "prereq": ["평균", "대푯값"], "ops": ["통계"], "traps": ["편차의 부호", "제곱 누락"], "tags": ["대푯값", "산포도"]}
CTX = {"math": {"S": "수학 점수", "U": "점"}, "book": {"S": "한 달 동안 읽은 책의 수", "U": "권"}, "time": {"S": "하루 운동 시간", "U": "분"}, "shoot": {"S": "자유투 성공 횟수", "U": "회"}, "age": {"S": "회원의 나이", "U": "세"}}
rng = random.Random(20260913)


def _lst(vals):
    return ", ".join(str(v) for v in vals)


def eul_(v):
    return "을" if str(v)[-1] in "013678" else "를"


# t1 — 평균이 주어질 때 미지수 x
def _st1_rows():
    out = {}
    for _ in range(400):
        n = rng.choice([4, 5, 6])
        m = rng.randint(5, 20)
        vals = [rng.randint(max(1, m - 8), m + 8) for _ in range(n - 1)]
        x = n * m - sum(vals)
        if x < 1 or x > 40 or x in vals:
            continue
        pos = rng.randint(0, n - 1)
        shown = vals[:pos] + ["x"] + vals[pos:]
        key = f"{n}-{m}-{'-'.join(str(v) for v in vals)}"
        out[key] = {"n": n, "m": m, "SUM": sum(vals), "x": x, "DATA": _lst(shown), "KNOWN": _lst(vals), "nm": n * m}
        if len(out) >= 160:
            break
    return out


ST1_ROWS = _st1_rows()


def st_t1():
    return tpl(ST, 1, ST_BASE,
        title="평균이 주어진 자료의 미지수",
        skill="(자료의 합) = (평균) × (개수)를 세워 미지수 구하기",
        variant_axis={"개수": "4~6", "평균": "5~20", "맥락": "5가지"},
        difficulty=1,
        discriminates="평균 × 개수가 전체 합임을 알고 이미 아는 값의 합을 빼는가",
        params=[{"name": "f", "values": {"in": list(ST1_ROWS)}}, {"name": "c", "values": {"in": list(CTX)}}],
        table=[{"key": "f", "rows": ST1_ROWS}, {"key": "c", "rows": CTX}],
        derive={"ans": "x"},
        constraints=["ans != m", "ans != SUM"],
        cost_values=["n", "m", "SUM", "ans"],
        answer_var="ans",
        verify=["SUM + ans == nm", "nm == n*m"],
        question="다음은 {S}{eul(S)} 조사하여 나타낸 자료이다. 이 자료의 평균이 {m}{U}일 때, x의 값을 구하시오.  [ {DATA} ]  (단위: {U})",
        figure=table(None, [["{DATA}"]], caption="(단위: {U})"),
        answer="{ans}", answer_alt=[],
        sol1="평균은 (자료의 합) ÷ (개수)이므로 (자료의 합) = (평균) × (개수) = {m} × {n} = {nm}이다. 아는 값 {KNOWN}의 합 {SUM}{eul(SUM)} 빼면 x가 나온다.",
        sol2=[
            "(자료의 합) = {m} × {n} = {nm}",
            "{SUM} + x = {nm}",
            "x = {nm} − {SUM} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "합 = {m} × {n} = {nm}", "hint": "평균 × 개수"},
            {"text": "{SUM} + x = {nm}", "hint": "아는 값의 합 {SUM}", "marks": [{"on": "x", "note": "미지수"}]},
            {"text": "x = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="x = {ans}{eul(ans)} 넣어 평균을 다시 내면 ({SUM} + {ans}) ÷ {n} = {nm} ÷ {n} = {m}{ro(m)} 조건과 맞는다. 따라서 x = {ans}이다.",
        sol3_fig=steps(["({SUM} + {ans}) ÷ {n} = {m} ✓", "x = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="평균이 {m}이므로 자료의 합은 {m} × {n} = {nm}이다. {SUM} + x = {nm}에서 x = {ans}이다.",
        rubric=[
            {"element": "합 구하기", "points": 2, "criterion": "자료의 합이 {m} × {n} = {nm}임을 밝혔다.", "partial": "평균 × 개수를 쓰지 않았으면 인정하지 않는다."},
            {"element": "x 구하기", "points": 3, "criterion": "{SUM} + x = {nm}에서 x = {ans}{eul(ans)} 구했다.", "partial": "아는 값의 합 계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t2 — 중앙값·최빈값
def _st2_rows():
    out = {}
    for _ in range(600):
        n = rng.choice([6, 7, 8])
        base = rng.randint(3, 15)
        vals = sorted(rng.randint(base, base + 9) for _ in range(n - 1))
        mode = rng.choice(vals)
        vals.append(mode)
        vals.sort()
        cnt = {v: vals.count(v) for v in set(vals)}
        modes = [v for v, k in cnt.items() if k == max(cnt.values())]
        if len(modes) != 1 or max(cnt.values()) != 2:
            continue
        shuffled = vals[:]
        rng.shuffle(shuffled)
        if shuffled == vals:
            continue
        if n % 2:
            med = Fraction(vals[n // 2]); mtxt = f"{n}개 중 가운데 {n // 2 + 1}번째 값 {vals[n // 2]}"
        else:
            med = Fraction(vals[n // 2 - 1] + vals[n // 2], 2); mtxt = f"{n}개 중 가운데 두 값 {vals[n // 2 - 1]}, {vals[n // 2]}의 평균 ({vals[n // 2 - 1]} + {vals[n // 2]}) ÷ 2"
        key = "-".join(str(v) for v in shuffled)
        for ask, val in (("sum", med + modes[0]), ("dif", med - modes[0])):
            if val in vals or val == 0:
                continue
            out[f"{key}-{ask}"] = {"n": n, "DATA": _lst(shuffled), "SORTED": _lst(vals), "medn": med.numerator, "medd": med.denominator, "mode": modes[0], "MTXT": mtxt,
                                   "ASK": "a + b" if ask == "sum" else "a − b", "sg": 1 if ask == "sum" else -1, "half": n // 2 + 1}
        if len(out) >= 300:
            break
    return out


ST2_ROWS = _st2_rows()


def st_t2():
    return tpl(ST, 2, ST_BASE,
        title="중앙값과 최빈값",
        skill="크기순으로 나열해 가운데 값(짝수 개면 가운데 두 값의 평균)을 중앙값으로, 가장 많이 나타나는 값을 최빈값으로 읽기",
        variant_axis={"개수": "6~8", "구하는 것": "중앙값 / 최빈값", "맥락": "5가지"},
        difficulty=2,
        discriminates="나열하지 않은 채 가운데를 읽지 않는가, 짝수 개일 때 두 값의 평균을 내는가",
        params=[{"name": "f", "values": {"in": list(ST2_ROWS)}}, {"name": "c", "values": {"in": list(CTX)}}],
        table=[{"key": "f", "rows": ST2_ROWS}, {"key": "c", "rows": CTX}],
        derive={"med": "medn/medd", "ans": "medn/medd + sg*mode"},
        constraints=["ans != n"],
        cost_values=["n", "med", "mode", "ans"],
        answer_var="ans",
        verify=["med*medd == medn"],
        question="다음은 {S}{eul(S)} 조사하여 나타낸 자료이다. 이 자료의 중앙값을 a, 최빈값을 b라 할 때, {ASK}의 값을 구하시오.  [ {DATA} ]  (단위: {U})",
        figure=table(None, [["{DATA}"]], caption="(단위: {U})"),
        answer="{dec(ans)}", answer_alt=[],
        sol1="중앙값은 자료를 크기순으로 나열했을 때 가운데 값(짝수 개면 가운데 두 값의 평균)이고, 최빈값은 가장 많이 나타나는 값이다. 먼저 크기순으로 나열한다: {SORTED}.",
        sol2=[
            "크기순 나열: {SORTED}",
            "중앙값 a: {MTXT} = {dec(med)}, 최빈값 b: 두 번 나타난 {mode}",
            "따라서 {ASK} = {dec(ans)}",
        ],
        sol2_fig=steps([
            {"text": "{SORTED}", "hint": "크기순 나열"},
            {"text": "a = {dec(med)}, b = {mode}", "hint": "가운데 값 · 가장 많이 나타난 값", "marks": [{"on": "b = {mode}", "note": "두 번"}]},
            {"text": "{ASK} = {dec(ans)}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="나열한 {n}개 중 중앙값 {dec(med)}의 앞뒤에 같은 개수의 자료가 있고, {mode}{eun(mode)} 두 번, 나머지는 한 번씩 나타난다. 따라서 {ASK} = {dec(ans)}이다.",
        sol3_fig=steps(["a = {dec(med)} · b = {mode}", "{ASK} = {dec(ans)}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="자료를 크기순으로 나열하면 {SORTED}이다. 중앙값은 {MTXT} = {dec(med)}이고 최빈값은 두 번 나타난 {mode}이다. 따라서 {ASK} = {dec(ans)}이다.",
        rubric=[
            {"element": "나열", "points": 2, "criterion": "자료를 크기순으로 {SORTED}{ro(SORTED)} 나열했다.", "partial": "나열하지 않고 읽었으면 인정하지 않는다."},
            {"element": "중앙값·최빈값", "points": 3, "criterion": "a = {dec(med)}, b = {mode}{ro(mode)} 구해 {ASK} = {dec(ans)}{eul(dec(ans))} 답했다.", "partial": "짝수 개에서 한쪽 값만 중앙값으로 썼으면 1점."},
        ],
        rubric_total=5,
    )


# t3 — 편차: 편차의 합은 0 / 변량 = 평균 + 편차
NAMES = ["A", "B", "C", "D", "E"]


def _st3_rows():
    out = {}
    for _ in range(500):
        devs = [rng.randint(-6, 6) for _ in range(4)]
        x = -sum(devs)
        if abs(x) > 8 or x == 0 or x in devs:
            continue
        pos = rng.randint(0, 4)
        full = devs[:pos] + [x] + devs[pos:]
        m = rng.randint(60, 90)
        key = "-".join(str(v) for v in full)
        cells = [str(v) if i != pos else "x" for i, v in enumerate(full)]
        who = rng.choice([i for i in range(5) if i != pos])
        out[f"{key}-sum"] = {"m": m, "x": x, "pos": pos, "XN": NAMES[pos], "CELLS": " | ".join(cells), "c1": cells[0], "c2": cells[1], "c3": cells[2], "c4": cells[3], "c5": cells[4],
                             "KNOWN": _lst(devs), "KS": sum(devs), "ASK": "x의 값", "isX": 1, "WN": NAMES[who], "wd": full[who], "score": m + full[who], "ans": x,
                             "STEP": f"편차의 합이 0이므로 {sum(devs)} + x = 0, x = {x}", "LAW": "편차의 합은 항상 0"}
        out[f"{key}-score"] = {"m": m, "x": x, "pos": pos, "XN": NAMES[pos], "CELLS": " | ".join(cells), "c1": cells[0], "c2": cells[1], "c3": cells[2], "c4": cells[3], "c5": cells[4],
                               "KNOWN": _lst(devs), "KS": sum(devs), "ASK": f"학생 {NAMES[who]}의 점수", "isX": 0, "WN": NAMES[who], "wd": full[who], "score": m + full[who], "ans": m + full[who],
                               "STEP": f"(변량) = (평균) + (편차)이므로 학생 {NAMES[who]}의 점수는 {m} + ({full[who]}) = {m + full[who]}", "LAW": "편차 = 변량 − 평균"}
        if len(out) >= 300:
            break
    return out


ST3_ROWS = _st3_rows()


def st_t3():
    return tpl(ST, 3, ST_BASE,
        title="편차 — 편차의 합은 0, 변량 = 평균 + 편차",
        skill="편차의 합이 0임을 써서 빈 편차를 구하거나, 평균에 편차를 더해 변량 구하기",
        variant_axis={"구하는 것": "빈 편차 x / 한 학생의 점수", "평균": "60~90"},
        difficulty=2,
        discriminates="편차의 합이 0이라는 성질을 쓰는가, 편차의 부호를 살려 평균에 더하는가",
        params=[{"name": "f", "values": {"in": list(ST3_ROWS)}}],
        table={"key": "f", "rows": ST3_ROWS},
        constraints=["ans != m"],
        cost_values=["m", "x", "ans"],
        answer_var="ans",
        verify=["KS + x == 0", "score == m + wd"],
        question="다음은 학생 5명의 수학 점수의 편차를 나타낸 표이다. 평균이 {m}점일 때, {ASK}을 구하시오.  [ A: {c1}, B: {c2}, C: {c3}, D: {c4}, E: {c5} ]  (단위: 점)",
        figure=table(["학생", "A", "B", "C", "D", "E"], [["편차(점)", "{c1}", "{c2}", "{c3}", "{c4}", "{c5}"]]),
        answer="{ans}", answer_alt=["{ans}점"],
        sol1="편차는 (변량) − (평균)이고, 편차를 모두 더하면 항상 0이다. 아는 편차 {KNOWN}의 합은 {KS}이므로 빈 편차 x는 {KS} + x = 0에서 구한다. 변량은 (평균) + (편차)로 되돌린다. {LAW}{eul(LAW)} 쓴다.",
        sol2=[
            "편차의 합 = 0: {KS} + x = 0 → x = {x}",
            "학생 {WN}의 점수 = {m} + ({wd}) = {score}",
            "따라서 {ASK}은 {ans}",
        ],
        sol2_fig=steps([
            {"text": "{KS} + x = 0 → x = {x}", "hint": "편차의 합은 0"},
            {"text": "{m} + ({wd}) = {score}", "hint": "변량 = 평균 + 편차"},
            {"text": "{ASK} = {ans}", "marks": [{"on": "{ans}", "note": "답"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="x = {x}{eul(x)} 넣으면 다섯 편차의 합이 {KS} + ({x}) = 0으로 맞는다. 편차가 양수면 평균보다 높고 음수면 낮다. 따라서 {ASK}은 {ans}이다.",
        sol3_fig=steps(["편차의 합 {KS} + ({x}) = 0 ✓", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{STEP}이다. 따라서 {ASK}은 {ans}이다.",
        rubric=[
            {"element": "편차의 성질", "points": 3, "criterion": "{LAW}{eul(LAW)} 써서 식을 세웠다.", "partial": "편차의 합을 평균으로 착각했으면 인정하지 않는다."},
            {"element": "값 구하기", "points": 2, "criterion": "{ASK} {ans}{eul(ans)} 구했다.", "partial": "부호 실수면 1점."},
        ],
        rubric_total=5,
    )


# t4 — 분산·표준편차
def _st4_rows():
    out = {}
    seen = set()
    for n in (4, 5, 6):
        for devs in itertools.product(range(-5, 6), repeat=n):
            if sum(devs) != 0 or tuple(sorted(devs)) in seen or len(set(devs)) < 3:
                continue
            ss = sum(d * d for d in devs)
            if ss % n or ss == 0:
                continue
            v = ss // n
            seen.add(tuple(sorted(devs)))
            m = rng.randint(6, 20)
            vals = [m + d for d in devs]
            if min(vals) < 1:
                continue
            shuffled = vals[:]
            rng.shuffle(shuffled)
            dsh = [x - m for x in shuffled]                          # 표시 순서대로의 편차
            sq = " + ".join(f"({d})²" if d < 0 else f"{d}²" for d in dsh)
            key = "-".join(str(x) for x in shuffled)
            base = {"n": n, "m": m, "SUM": sum(vals), "DATA": _lst(shuffled), "DEVS": _lst(dsh), "SQ": sq, "ss": ss, "v": v}
            if v not in vals:
                out[f"{key}-var"] = {**base, "ASK": "분산", "isV": 1, "sd": 0, "ans": v}
            r = int(round(v ** 0.5))
            if r * r == v and r not in vals:
                out[f"{key}-sd"] = {**base, "ASK": "표준편차", "isV": 0, "sd": r, "ans": r}
    keys = list(out)
    rng.shuffle(keys)
    return {k: out[k] for k in keys[:320]}


ST4_ROWS = _st4_rows()


def st_t4():
    return tpl(ST, 4, ST_BASE,
        title="분산과 표준편차",
        skill="평균 → 편차 → (편차)²의 평균(분산) → 제곱근(표준편차) 순서로 계산하기",
        variant_axis={"개수": "4~6", "구하는 것": "분산 / 표준편차", "맥락": "5가지"},
        difficulty=3,
        discriminates="편차를 제곱해 평균을 내는가(편차의 평균은 0), 표준편차는 분산의 양의 제곱근임을 아는가",
        params=[{"name": "f", "values": {"in": list(ST4_ROWS)}}, {"name": "c", "values": {"in": list(CTX)}}],
        table=[{"key": "f", "rows": ST4_ROWS}, {"key": "c", "rows": CTX}],
        constraints=["ans != m", "ans != n"],
        cost_values=["n", "m", "SUM", "ss", "v", "ans"],
        answer_var="ans",
        verify=["SUM == n*m", "ss == n*v", "isV == 1 or sd*sd == v"],
        question="다음은 {S}{eul(S)} 조사하여 나타낸 자료이다. 이 자료의 {ASK}를 구하시오.  [ {DATA} ]  (단위: {U})",
        figure=table(None, [["{DATA}"]], caption="(단위: {U})"),
        answer="{ans}", answer_alt=[],
        sol1="분산은 편차의 제곱의 평균이고, 표준편차는 분산의 양의 제곱근이다. 순서: ① 평균 = {SUM} ÷ {n} = {m}, ② 각 변량에서 평균을 뺀 편차 {DEVS}, ③ (편차)²의 합 {ss}를 개수 {n}으로 나눈 분산 {v}, ④ 표준편차 = [[sqrt({v})]].",
        sol2=[
            "평균 = {SUM} ÷ {n} = {m}, 편차: {DEVS}",
            "분산 = ({SQ}) ÷ {n} = {ss} ÷ {n} = {v}",
            "표준편차 = [[sqrt({v})]] → {ASK}는 {ans}",
        ],
        sol2_fig=steps([
            {"text": "평균 {m}, 편차 {DEVS}", "hint": "편차 = 변량 − 평균"},
            {"text": "분산 = {ss} ÷ {n} = {v}", "hint": "(편차)²의 평균", "marks": [{"on": "{v}", "note": "분산"}]},
            {"text": "표준편차 = [[sqrt({v})]] → {ASK} {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="편차 {DEVS}의 합은 0으로 평균이 맞게 구해졌고, 제곱의 합 {ss}{eul(ss)} {n}으로 나눈 {v}{ika(v)} 분산이다. 표준편차는 그 양의 제곱근이다. 따라서 {ASK}는 {ans}이다.",
        sol3_fig=steps(["편차의 합 0 ✓, 분산 {v}", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="평균은 {SUM} ÷ {n} = {m}이고 편차는 {DEVS}이다. 분산은 ({SQ}) ÷ {n} = {v}이고 표준편차는 [[sqrt({v})]]이다. 따라서 {ASK}는 {ans}이다.",
        rubric=[
            {"element": "평균·편차", "points": 2, "criterion": "평균 {m}{eul(m)} 구하고 편차 {DEVS}{eul(DEVS)} 썼다.", "partial": "편차의 부호 실수면 1점."},
            {"element": "분산·표준편차", "points": 3, "criterion": "(편차)²의 평균 {v}{eul(v)} 구하고 {ASK} {ans}{eul(ans)} 답했다.", "partial": "편차를 제곱하지 않았으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t5 — 변량을 변환한 자료의 평균·분산·표준편차
TR_ROWS = {
    "plus": {"TR": "a + k, b + k, c + k, d + k", "MT": "m + k", "VT": "v", "km": 1, "kv": 1, "WHY": "모든 변량에 같은 수를 더하면 평균도 그만큼 커지지만 편차는 변하지 않으므로 분산·표준편차는 그대로이다"},
    "times": {"TR": "ka, kb, kc, kd", "MT": "km", "VT": "k²v", "km": 2, "kv": 4, "WHY": "모든 변량을 k배 하면 평균도 k배, 편차도 k배가 되어 분산은 k²배, 표준편차는 k배가 된다"},
}


def _st5_rows():
    out = {}
    for kind in ("plus", "times", "affine"):
        for k in (2, 3):
            for kk in (1, 2, 3, 5):
                for m in (4, 5, 6, 8, 10):
                    for v in (1, 4, 9, 16):
                        if kind == "plus":
                            nm, nv, TR, WHY = m + kk, v, f"a + {kk}, b + {kk}, c + {kk}, d + {kk}", "모든 변량에 같은 수를 더하면 평균도 그만큼 커지지만 각 편차는 변하지 않으므로 분산과 표준편차는 그대로이다"
                            if k != 2:
                                continue
                        elif kind == "times":
                            nm, nv, TR, WHY = k * m, k * k * v, f"{k}a, {k}b, {k}c, {k}d", f"모든 변량을 {k}배 하면 평균도 {k}배, 편차도 {k}배가 되어 분산은 {k}² = {k * k}배가 된다"
                            if kk != 1:
                                continue
                        else:
                            nm, nv, TR, WHY = k * m + kk, k * k * v, f"{k}a + {kk}, {k}b + {kk}, {k}c + {kk}, {k}d + {kk}", f"{k}배 하고 {kk}{eul_(kk)} 더하면 평균은 {k}배 하고 {kk}{eul_(kk)} 더한 값이 되고, 편차는 {k}배만 되므로 분산은 {k}² = {k * k}배가 된다"
                        r = int(round(nv ** 0.5))
                        for ask in ("mean", "var", "sd"):
                            if ask == "sd" and r * r != nv:
                                continue
                            ans = {"mean": nm, "var": nv, "sd": r}[ask]
                            if ans in (m, v, k, kk):
                                continue
                            out[f"{kind}-{k}-{kk}-{m}-{v}-{ask}"] = {"m": m, "v": v, "TR": TR, "WHY": WHY, "nm": nm, "nv": nv, "nsd": r, "ASK": {"mean": "평균", "var": "분산", "sd": "표준편차"}[ask], "ans": ans, "isM": int(ask == "mean"), "isV": int(ask == "var"),
                                                                       "SD0": int(round(v ** 0.5)), "STEP": {"mean": f"새 평균 = {nm}", "var": f"새 분산 = {nv}", "sd": f"새 표준편차 = [[sqrt({nv})]] = {r}"}[ask]}
    keys = list(out)
    rng.shuffle(keys)
    return {k: out[k] for k in keys[:360]}


ST5_ROWS = _st5_rows()


def st_t5():
    return tpl(ST, 5, ST_BASE,
        title="변량을 일정하게 바꾼 자료의 평균·분산·표준편차",
        skill="변량에 같은 수를 더하거나 k배 하면 평균은 같은 변환, 분산은 k²배, 표준편차는 k배가 됨을 쓰기",
        variant_axis={"변환": "+k / ×k / ×k + c", "구하는 것": "평균 / 분산 / 표준편차"},
        difficulty=3,
        discriminates="더하는 수는 산포도에 영향이 없고, 곱하는 수는 분산에 제곱으로 들어감을 아는가",
        params=[{"name": "f", "values": {"in": list(ST5_ROWS)}}],
        table={"key": "f", "rows": ST5_ROWS},
        constraints=["ans != m", "ans != v"],
        cost_values=["m", "v", "nm", "nv", "ans"],
        answer_var="ans",
        verify=["isM == 0 or ans == nm", "isV == 0 or ans == nv"],
        question="4개의 변량 a, b, c, d의 평균이 {m}, 분산이 {v}일 때, 변량 {TR}의 {ASK}을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="{WHY}. 원래 자료의 평균 {m}, 분산 {v}(표준편차 [[sqrt({v})]] = {SD0})에 이 규칙을 적용한다.",
        sol2=[
            "{WHY}",
            "새 평균 = {nm}, 새 분산 = {nv}",
            "{STEP} → {ASK}은 {ans}",
        ],
        sol2_fig=steps([
            {"text": "평균 {m} → {nm}", "hint": "변량과 같은 변환"},
            {"text": "분산 {v} → {nv}", "hint": "곱하는 수의 제곱배 (더하는 수는 무관)", "marks": [{"on": "{nv}", "note": "새 분산"}]},
            {"text": "{STEP}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="편차로 확인하면, 각 변량의 편차가 곱하는 수만큼 배가 되고 더하는 수와는 무관하므로 (편차)²의 평균은 곱하는 수의 제곱배가 된다. 따라서 {ASK}은 {ans}이다.",
        sol3_fig=steps(["편차 → 곱하는 수만큼 배", "{ASK} = {ans}"]),
        sol3_anim=[[reveal(0)], [reveal(1)]],
        model_answer="{WHY}. 따라서 새 평균은 {nm}, 새 분산은 {nv}이고 {ASK}은 {ans}이다.",
        rubric=[
            {"element": "변환 규칙", "points": 3, "criterion": "평균·분산이 어떻게 바뀌는지({WHY}) 밝혔다.", "partial": "더하는 수를 분산에 반영했으면 인정하지 않는다."},
            {"element": "값 구하기", "points": 2, "criterion": "{ASK} {ans}{eul(ans)} 구했다.", "partial": "분산과 표준편차를 혼동했으면 1점."},
        ],
        rubric_total=5,
    )


ST_SEED = {
    "seed_id": ST, "category": "확률통계",
    "title": "대푯값과 산포도 — 평균→미지수·중앙값/최빈값·편차·분산/표준편차·변환 자료의 분산",
    "unit_id": "m3-2", "concept_ids": ["m3-2-12", "m3-2-13"],
    "schema_id": None, "schema_name": "대푯값과 산포도",
    "source_item_ids": [],
    "note": "자료·편차·제곱합은 파이썬(seed 고정 난수)으로 미리 만들어 표에 둔다. 분산은 정수, 표준편차 틀은 분산이 완전제곱수인 행만. 산점도·상관관계(14)는 그림이 필요해 보류.",
    "geometry": False,
    "templates": [st_t1(), st_t2(), st_t3(), st_t4(), st_t5()],
}


if __name__ == "__main__":
    with_pitfalls(ST_SEED)
    dump(ST_SEED)
