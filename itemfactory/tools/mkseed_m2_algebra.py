# itemfactory/tools/mkseed_m2_algebra.py — 중2-1 대수 시드 3종 (v1.0 · 2026-09-09)
#
#   python itemfactory/tools/mkseed_m2_algebra.py
#     → seeds/m2-1-sys-apply.json (연립방정식 활용 4틀 · 활용)
#     → seeds/m2-1-line-two-points.json (두 점을 지나는 직선 4틀 · 연산)
#     → seeds/m2-1-exponent.json (지수법칙 5틀 · 연산)
#
# 표기 규약
#   · 거듭제곱: 단일 pow 는 [[pow(x, 6)]] 마커(x⁶ 로 렌더). 중첩·곱의 거듭제곱 ((x³)², (2x³y)²) 은 mathir 가 못 그리므로
#     위첨자 문자(²³…)를 표(SUP)로 붙인 평문을 쓴다. 미지수 지수는 평문 'xᵏ'.
#   · 조건 분기 문장은 표 행의 정적 문자열로만(행 문자열엔 {자리표시자} 불가).
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seedlib import dump, hl, reveal, steps, table, with_pitfalls  # noqa: E402

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")


def sup(n: int) -> str:
    return "" if n == 1 else str(n).translate(SUP)


def sup_table(key: str, field: str, lo: int, hi: int) -> dict:
    """지수 파라미터 → 위첨자 문자열 표. 1 은 빈 문자열(x¹ 대신 x)."""
    return {"key": key, "rows": {str(i): {field: sup(i)} for i in range(lo, hi + 1)}}


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def cplane(xs, ys, points, lines, **extra):
    a = {"x": xs, "y": ys, "points": points, "lines": lines}
    a.update(extra)
    return [{"fn": "coordplane", "args": a}]


# ═══════════════════════════════════════════════════════════════════ 1. 연립방정식의 활용
SYS = {"process": "문제해결", "context": "생활맥락", "prereq": ["연립방정식의 풀이"], "ops": ["연립방정식", "사칙"], "traps": ["미지수설정", "식세우기"],
       "time_limit": 150, "points": 5, "tags": ["연립방정식의 활용"], "rubric_total": 8}
SCHEMA_SYS = "b2986510-dfcd-4caa-a1f6-ad7fef7c0082"      # 연립방정식 세우기(문장제)

DIGIT_W = {
    "up": {"sg": 1, "W": "크다", "W2": "큰", "EQ2L": "(10y + x) − (10x + y)", "EQ2S": "9y − 9x", "EQ2R": "y − x", "ADD": "2y", "FIRST": "y", "SECOND": "x"},
    "down": {"sg": -1, "W": "작다", "W2": "작은", "EQ2L": "(10x + y) − (10y + x)", "EQ2S": "9x − 9y", "EQ2R": "x − y", "ADD": "2x", "FIRST": "x", "SECOND": "y"},
}


def sys_t1():
    return tpl("m2-1-sys-apply", 1, SYS,
        title="자리를 바꾼 두 자리 자연수 — 자릿수의 합과 두 수의 차",
        skill="십의 자리 x, 일의 자리 y로 놓아 처음 수 10x + y, 바꾼 수 10y + x를 쓰고 두 조건을 연립방정식으로 옮기기",
        variant_axis={"대소": "바꾼 수가 크다/작다", "자릿수": "합 3~17, 차 1~8"},
        discriminates="두 자리 수를 10x + y로 나타내는가, 바꾼 수와의 차를 부호까지 맞게 식으로 옮기는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "w", "values": {"in": list(DIGIT_W)}}, {"name": "x", "values": {"int": [1, 8]}}, {"name": "k", "values": {"int": [1, 8]}}],
        table={"key": "w", "rows": DIGIT_W},
        derive={"y": "x + sg*k", "s": "x + y", "d": "9*k", "N": "10*x + y", "M": "10*y + x"},
        constraints=["y >= 1", "y <= 9", "s != d", "N != s", "N != d", "s != k"],
        cost_values=["s", "d", "x", "y", "N"],
        verify=["ans == 10*x + y", "(ans % 10) + floor(ans/10) == s", "sg*((ans % 10)*10 + floor(ans/10) - ans) == d"],
        answer_var="N",
        question="각 자리의 숫자의 합이 {s}인 두 자리 자연수가 있다. 이 수의 십의 자리 숫자와 일의 자리 숫자를 바꾼 수는 처음 수보다 {d}만큼 {W}고 한다. 처음 수를 구하시오.",
        answer="{N}", answer_alt=[],
        sol1="십의 자리 숫자를 x, 일의 자리 숫자를 y라 하면 처음 수는 10x + y, 자리를 바꾼 수는 10y + x다(xy라고 쓰면 곱이 되므로 안 된다). 모르는 것이 둘이니 조건도 둘을 식으로 옮긴다: 자릿수의 합 x + y = {s}, 두 수의 차 {EQ2L} = {d}. 두 번째 식은 정리하면 {EQ2S} = {d}, 곧 {EQ2R} = {k}로 아주 간단해진다.",
        sol1_fig=table(["", "십의 자리", "일의 자리", "수"], [["처음 수", "x", "y", "10x + y"], ["바꾼 수", "y", "x", "10y + x"]]),
        sol2=[
            "십의 자리 숫자를 x, 일의 자리 숫자를 y라 하면 자릿수의 합에서 x + y = {s} … ①",
            "바꾼 수가 처음 수보다 {d}만큼 {W}므로 {EQ2L} = {d}, 정리하면 {EQ2S} = {d}, 곧 {EQ2R} = {k} … ②",
            "①과 ②를 변끼리 더하면 {ADD} = {s + k}, {FIRST} = {(s + k)/2}이고, ①에서 {SECOND} = {s} − {(s + k)/2} = {(s - k)/2}",
            "따라서 십의 자리 숫자는 {x}, 일의 자리 숫자는 {y}이므로 처음 수는 {N}이다.",
        ],
        sol2_fig=steps([
            {"text": "x + y = {s}", "hint": "자릿수의 합"},
            {"text": "{EQ2R} = {k}", "hint": "{EQ2L} = {d} 를 9로 나눔"},
            {"text": "{ADD} = {s + k}  →  {FIRST} = {(s + k)/2}, {SECOND} = {(s - k)/2}", "hint": "① + ②"},
            {"text": "처음 수 = 10 × {x} + {y} = {N}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3)]],
        sol3="{N}의 자릿수의 합은 {x} + {y} = {s}이고, 자리를 바꾼 수 {M}{eun(M)} {N}보다 {d}만큼 {W2} 수다({max(N, M)} − {min(N, M)} = {d}). 두 조건에 모두 맞으므로 답은 {N}이다.",
        model_answer="십의 자리 숫자를 x, 일의 자리 숫자를 y라 하면 x + y = {s}, {EQ2L} = {d}이다. 두 번째 식을 정리하면 {EQ2R} = {k}이고, 두 식을 더하면 {FIRST} = {(s + k)/2}, {SECOND} = {(s - k)/2}이다. 따라서 처음 수는 {N}이다.",
        rubric=[
            {"element": "미지수·식 세우기", "points": 3, "criterion": "십의 자리 x, 일의 자리 y로 놓고 처음 수 10x + y, 바꾼 수 10y + x를 써서 x + y = {s}, {EQ2L} = {d}{eul(d)} 세웠다.", "partial": "처음 수를 xy처럼 쓰거나 두 식 중 하나만 세웠으면 1점."},
            {"element": "연립방정식 풀기", "points": 3, "criterion": "가감법 또는 대입법으로 x = {x}, y = {y}{eul(y)} 구했다.", "partial": "한 문자만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "처음 수 {N}{eul(N)} 답했다.", "partial": "x = {x}, y = {y}만 쓰고 수를 만들지 않았거나 바꾼 수 {M}{eul(M)} 답했으면 1점."},
        ],
    )


QUIZ_CTX = {
    "1": {"S": "학급 골든벨 퀴즈에서", "P": "지우"},
    "2": {"S": "영어 단어 시험에서", "P": "서준"},
    "3": {"S": "보드게임 카페의 퀴즈 이벤트에서", "P": "하린"},
    "4": {"S": "수학 동아리 퀴즈 대결에서", "P": "도윤"},
}


def sys_t2():
    return tpl("m2-1-sys-apply", 2, SYS,
        title="맞히면 득점, 틀리면 감점 — 맞힌 문제 수",
        skill="맞힌 문제 x, 틀린 문제 y로 놓고 개수의 식과 점수의 식(감점은 빼기)을 세워 가감법으로 풀기",
        variant_axis={"문제 수": "10·12·15·20", "배점": "득점 3~10, 감점 1~3", "맥락": "골든벨·단어 시험·보드게임·동아리"},
        discriminates="틀린 문제의 점수를 '빼는' 식으로 세우는가, 가감법에서 곱한 수를 양변에 모두 적용하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "c", "values": {"in": list(QUIZ_CTX)}}, {"name": "n", "values": {"in": [10, 12, 15, 20]}}, {"name": "p", "values": {"in": [3, 4, 5, 10]}}, {"name": "q", "values": {"in": [1, 2, 3]}}, {"name": "x", "values": {"int": [3, 18]}}],
        table={"key": "c", "rows": QUIZ_CTX},
        derive={"y": "n - x", "T": "p*x - q*(n - x)"},
        constraints=["y >= 1", "T > 0", "p > q", "T != x", "T != n", "T != p", "x != n", "x != p", "x != q"],
        cost_values=["n", "p", "q", "T", "x", "y"],
        relation="p*X - q*(n - X) - T", unknown="X", answer_var="x",
        verify=["p*ans - q*(n - ans) == T", "ans < n"],
        question="{S} {P}가 {n}문제를 풀었다. 한 문제를 맞히면 {p}점을 얻고 틀리면 {q}점을 잃는데, {P}가 얻은 점수는 모두 {T}점이었다. {P}가 맞힌 문제는 몇 개인지 구하시오.",
        answer="{x}", answer_alt=["{x}개"],
        sol1="맞힌 문제 수를 x, 틀린 문제 수를 y라 하면 문제 수에서 x + y = {n}, 점수에서 {p}x − {co(q)}y = {T}. 틀리면 점수를 잃으므로 빼는 항이 되는 것이 핵심이다. 두 식을 연립해 x를 구한다(첫 식에 {q}를 곱해 더하면 y가 사라진다).",
        sol1_fig=table(["", "맞힌 문제", "틀린 문제", "합계"], [["개수", "x", "y", "{n}"], ["점수", "{p}x", "−{co(q)}y", "{T}"]]),
        sol2=[
            "맞힌 문제 수를 x, 틀린 문제 수를 y라 하면 x + y = {n} … ①",
            "점수는 얻은 점수에서 잃은 점수를 빼므로 {p}x − {co(q)}y = {T} … ②",
            "①의 양변에 {q}{eul(q)} 곱해 ②와 더하면 {p + q}x = {T + q*n}, x = {x}",
            "y = {n} − {x} = {y}이므로 맞힌 문제는 {x}개이다.",
        ],
        sol2_fig=steps([
            {"text": "x + y = {n}", "hint": "문제 수"},
            {"text": "{p}x − {co(q)}y = {T}", "hint": "점수 — 틀리면 −{q}"},
            {"text": "{p + q}x = {T + q*n}", "hint": "① × {q} + ②", "marks": [{"on": "{T + q*n}", "note": "{T} + {q}×{n}"}]},
            {"text": "x = {x}, y = {y}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]],
        sol3="맞힌 문제 {x}개로 {p} × {x} = {p*x}점을 얻고 틀린 문제 {y}개로 {q} × {y} = {q*y}점을 잃으면 {p*x} − {q*y} = {T}점으로 문제와 맞는다. 답은 {x}개이다.",
        model_answer="맞힌 문제 수를 x, 틀린 문제 수를 y라 하면 x + y = {n}, {p}x − {co(q)}y = {T}이다. 첫 식에 {q}{eul(q)} 곱해 더하면 {p + q}x = {T + q*n}, x = {x}이고 y = {y}이다. 따라서 맞힌 문제는 {x}개이다.",
        rubric=[
            {"element": "미지수·식 세우기", "points": 3, "criterion": "맞힌 문제 x, 틀린 문제 y로 놓고 x + y = {n}, {p}x − {co(q)}y = {T}{eul(T)} 세웠다.", "partial": "틀린 문제의 점수를 더하는 식으로 세웠으면 1점."},
            {"element": "연립방정식 풀기", "points": 3, "criterion": "가감법 또는 대입법으로 x = {x}, y = {y}{eul(y)} 구했다.", "partial": "한 문자만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "맞힌 문제 {x}개를 답했다.", "partial": "틀린 문제 수 {y}개를 답했으면 인정하지 않는다."},
        ],
    )


RATE_CTX = {
    "1": {"ORG": "어느 중학교의", "P": "학생", "M": "남학생", "F": "여학생", "U": "명"},
    "2": {"ORG": "어느 초등학교의", "P": "학생", "M": "남학생", "F": "여학생", "U": "명"},
    "3": {"ORG": "어느 청소년 축구 클럽의", "P": "회원", "M": "남자 회원", "F": "여자 회원", "U": "명"},
}
RATE_W = {"up": {"sg": 1, "W": "늘었다", "W2": "증가"}, "down": {"sg": -1, "W": "줄었다", "W2": "감소"}}


def rate_rows():
    """맥락 × 구하는 것(올해/작년) 합성 키 — 질문 문장에 남학생/남자 회원 이름이 들어가야 해서 합친다."""
    rows = {}
    for c, r in RATE_CTX.items():
        for q, qq in (("this", {"isT": 1, "Q": f"올해 {r['M']} 수"}), ("last", {"isT": 0, "Q": f"작년 {r['M']} 수"})):
            rows[f"{c}-{q}"] = {**r, **qq}
    return rows


RATE_ROWS = rate_rows()


def sys_t3():
    return tpl("m2-1-sys-apply", 3, SYS,
        title="증가·감소 백분율 — 작년·올해의 남녀 수",
        skill="작년 수를 x, y로 놓고 전체의 식과 변화량의 식(증가는 +, 감소는 −)을 세워 풀고, 묻는 것이 올해인지 작년인지 확인하기",
        variant_axis={"변화": "전체가 늘었다/줄었다", "구하는 것": "올해/작년의 남자 쪽 수", "맥락": "중학교·초등학교·축구 클럽"},
        discriminates="백분율을 100으로 나눈 변화량으로 식을 세우는가, 작년 값을 구한 뒤 올해 값(늘어난 수를 더한 것)으로 바꾸는가",
        qtype="short", difficulty=4, pool_target=300, time_limit=180,
        params=[{"name": "cq", "values": {"in": list(RATE_ROWS)}}, {"name": "w", "values": {"in": list(RATE_W)}}, {"name": "i", "values": {"int": [4, 14]}}, {"name": "j", "values": {"int": [4, 14]}}, {"name": "a", "values": {"in": [4, 5, 8, 10, 12, 15, 20]}}, {"name": "b", "values": {"in": [4, 5, 8, 10, 15, 20]}}],
        table=[{"key": "cq", "rows": RATE_ROWS}, {"key": "w", "rows": RATE_W}],
        derive={"x": "50*i", "y": "50*j", "S": "50*i + 50*j", "dx": "a*50*i/100", "dy": "b*50*j/100", "dd": "a*50*i/100 - b*50*j/100", "D": "abs(a*50*i/100 - b*50*j/100)", "X2": "50*i + a*50*i/100", "ans": "50*i + isT*a*50*i/100"},
        constraints=["sg*dd > 0", "dx == floor(dx)", "dy == floor(dy)", "D >= 5", "D != a", "D != b", "a != b", "ans != S", "ans != D", "S <= 1200"],
        cost_values=["S", "a", "b", "D", "x", "y", "ans"],
        answer_var="ans",
        verify=["a*x/100 - b*y/100 == sg*D", "x + y == S", "ans == x + isT*a*x/100",
                "a*(ans/(1 + isT*a/100))/100 - b*(S - ans/(1 + isT*a/100))/100 == sg*D"],
        question="{ORG} 작년 전체 {P}의 수는 {S}{U}이었다. 올해는 작년에 비해 {M}이 {a}% 늘고 {F}가 {b}% 줄어서 전체 {P}의 수가 {D}{U} {W}. {Q}를 구하시오.",
        answer="{ans}", answer_alt=["{ans}{U}"],
        sol1="작년 {M} 수를 x{U}, {F} 수를 y{U}이라 하면 작년 전체에서 x + y = {S}. 올해 {M}은 {a}% 늘었으니 [[frac({a},100)]]x{U} 늘고, {F}는 {b}% 줄었으니 [[frac({b},100)]]y{U} 줄었다. 전체가 {D}{U} {W}는 것은 (늘어난 수) − (줄어든 수) = {sg*D}{ida(sg*D)}. 그래서 [[frac({a},100)]]x − [[frac({b},100)]]y = {sg*D}. 두 식을 연립해 작년 값을 구한 뒤, 묻는 것이 {Q}인지 확인해서 답한다.",
        sol1_fig=table(["", "{M}", "{F}", "전체"], [["작년", "x", "y", "{S}"], ["올해의 변화", "{a}% 증가", "{b}% 감소", "{D}{U} {W2}"]]),
        sol2=[
            "작년 {M} 수를 x{U}, {F} 수를 y{U}이라 하면 x + y = {S} … ①",
            "올해 {M}은 [[frac({a},100)]]x{U} 늘고 {F}는 [[frac({b},100)]]y{U} 줄었으므로 전체의 변화는 [[frac({a},100)]]x − [[frac({b},100)]]y = {sg*D} … ②",
            "②의 양변에 100을 곱하면 {a}x − {b}y = {sg*100*D}이고, ①의 양변에 {b}{eul(b)} 곱해 더하면 {a + b}x = {sg*100*D + b*S}, x = {x}",
            "y = {S} − {x} = {y}이다. 작년 {M} 수는 {x}{U}, 올해 {M} 수는 {x} + {dx} = {X2}{U}이므로 {Q}는 {ans}{U}이다.",
        ],
        sol2_fig=steps([
            {"text": "x + y = {S}", "hint": "작년 전체"},
            {"text": "{a}x − {b}y = {sg*100*D}", "hint": "변화량 × 100 (늘면 +, 줄면 −)"},
            {"text": "{a + b}x = {sg*100*D + b*S}", "hint": "① × {b} + ②", "marks": [{"on": "{sg*100*D + b*S}", "note": "{sg*100*D} + {b}×{S}"}]},
            {"text": "x = {x}, y = {y}  →  {Q} {ans}{U}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2", "mark:2-0")], [reveal(3)]],
        sol3="작년 {M} {x}{U}의 {a}%는 {dx}{U}, {F} {y}{U}의 {b}%는 {dy}{U}이므로 올해 전체는 {x} + {dx} + {y} − {dy} = {S + dd}{U}로 작년보다 {D}{U} {W}. {Q}는 {ans}{U}이다.",
        model_answer="작년 {M} 수를 x{U}, {F} 수를 y{U}이라 하면 x + y = {S}, [[frac({a},100)]]x − [[frac({b},100)]]y = {sg*D}이다. 두 번째 식에 100을 곱하면 {a}x − {b}y = {sg*100*D}이고, 첫 식에 {b}{eul(b)} 곱해 더하면 {a + b}x = {sg*100*D + b*S}, x = {x}, y = {y}이다. 따라서 {Q}는 {ans}{U}이다.",
        rubric=[
            {"element": "미지수·식 세우기", "points": 3, "criterion": "작년 {M} x, {F} y로 놓고 x + y = {S}, [[frac({a},100)]]x − [[frac({b},100)]]y = {sg*D}{eul(sg*D)} 세웠다.", "partial": "증가·감소의 부호를 바꿔 세웠거나 한 식만 세웠으면 1점."},
            {"element": "연립방정식 풀기", "points": 3, "criterion": "x = {x}, y = {y}{eul(y)} 구했다.", "partial": "한 문자만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q}를 물었음을 확인하고 {ans}{U}을 답했다.", "partial": "작년·올해를 바꿔 {x + X2 - ans}{U}을 답했으면 1점."},
        ],
    )


PRICE_CTX = {
    "1": {"SH": "편의점", "A": "삼각김밥", "B": "음료수", "U": "개"},
    "2": {"SH": "문구점", "A": "볼펜", "B": "형광펜", "U": "자루"},
    "3": {"SH": "카페", "A": "마카롱", "B": "쿠키", "U": "개"},
    "4": {"SH": "분식집", "A": "떡꼬치", "B": "어묵", "U": "개"},
    "5": {"SH": "빵집", "A": "소금빵", "B": "크루아상", "U": "개"},
    "6": {"SH": "문구점", "A": "노트", "B": "지우개", "U": "개"},
}


def sys_t4():
    return tpl("m2-1-sys-apply", 4, SYS,
        title="두 번의 구매 금액으로 두 품목의 단가 구하기",
        skill="두 단가를 x, y로 놓고 (개수 × 단가)의 합으로 두 식을 세운 뒤 계수를 맞춰 가감법으로 풀기",
        variant_axis={"개수 조합": "1~4개씩 두 번", "맥락": "편의점·문구점·카페·분식집·빵집"},
        discriminates="개수와 단가를 곱한 식을 세우는가, 가감법에서 두 식에 각각 알맞은 수를 곱해 한 문자를 없애는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "c", "values": {"in": list(PRICE_CTX)}}, {"name": "pa", "values": {"in": [800, 1000, 1200, 1500, 1800, 2000, 2500]}}, {"name": "pb", "values": {"in": [500, 700, 900, 1000, 1300, 1500, 2000]}},
                {"name": "m1", "values": {"int": [2, 4]}}, {"name": "n1", "values": {"int": [1, 4]}}, {"name": "m2", "values": {"int": [2, 4]}}, {"name": "n2", "values": {"int": [1, 4]}}],
        table={"key": "c", "rows": PRICE_CTX},
        derive={"T1": "m1*pa + n1*pb", "T2": "m2*pa + n2*pb", "det": "m1*n2 - m2*n1", "cy": "n1*m2 - n2*m1", "ry": "m2*T1 - m1*T2"},
        constraints=["det != 0", "pa != pb", "T1 != T2", "m1 != m2 or n1 != n2", "pa != T1", "pa != T2", "T1 < 20000", "T2 < 20000"],
        cost_values=["m1", "n1", "m2", "n2", "T1", "T2", "pa", "pb"],
        relation="X*(m1*n2 - m2*n1) - (T1*n2 - T2*n1)", unknown="X", answer_var="pa",
        verify=["m1*ans + n1*pb == T1", "m2*ans + n2*pb == T2"],
        question="어느 {SH}에서 {A} {m1}{U}와 {B} {n1}{U}를 사면 {T1}원이고, {A} {m2}{U}와 {B} {n2}{U}를 사면 {T2}원이다. {A} 한 {U}의 가격을 구하시오.",
        answer="{pa}", answer_alt=["{pa}원"],
        sol1="{A} 한 {U}의 가격을 x원, {B} 한 {U}의 가격을 y원이라 하면 두 번의 구매가 각각 식이 된다: {co(m1)}x + {co(n1)}y = {T1}, {co(m2)}x + {co(n2)}y = {T2}. 모르는 값이 둘이고 식도 둘이므로 연립방정식으로 푼다. 한 문자의 계수를 같게 맞춘 뒤 빼서(가감법) 그 문자를 없앤다.",
        sol1_fig=table(["", "{A}", "{B}", "금액"], [["첫 번째", "{m1}{U}", "{n1}{U}", "{T1}원"], ["두 번째", "{m2}{U}", "{n2}{U}", "{T2}원"]]),
        sol2=[
            "{A} 한 {U}를 x원, {B} 한 {U}를 y원이라 하면 {co(m1)}x + {co(n1)}y = {T1} … ①, {co(m2)}x + {co(n2)}y = {T2} … ②",
            "x를 없애기 위해 ① × {m2} − ② × {m1}을 하면 {co(cy)}y = {ry}, y = {pb}",
            "y = {pb}{eul(pb)} ①에 대입하면 {co(m1)}x + {n1*pb} = {T1}, {co(m1)}x = {T1 - n1*pb}, x = {pa}",
            "따라서 {A} 한 {U}의 가격은 {pa}원이다.",
        ],
        sol2_fig=steps([
            {"text": "{co(m1)}x + {co(n1)}y = {T1}", "hint": "첫 번째 구매"},
            {"text": "{co(m2)}x + {co(n2)}y = {T2}", "hint": "두 번째 구매"},
            {"text": "{co(cy)}y = {ry}  →  y = {pb}", "hint": "① × {m2} − ② × {m1}"},
            {"text": "{co(m1)}x + {n1*pb} = {T1}  →  x = {pa}", "hint": "y 대입"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")], [reveal(3), hl("hint:3")]],
        sol3="{A} {pa}원, {B} {pb}원이면 첫 번째는 {m1} × {pa} + {n1} × {pb} = {T1}원, 두 번째는 {m2} × {pa} + {n2} × {pb} = {T2}원으로 둘 다 맞는다. 답은 {pa}원이다.",
        model_answer="{A} 한 {U}의 가격을 x원, {B} 한 {U}의 가격을 y원이라 하면 {co(m1)}x + {co(n1)}y = {T1}, {co(m2)}x + {co(n2)}y = {T2}이다. 첫 식에 {m2}, 둘째 식에 {m1}을 곱해 빼면 {co(cy)}y = {ry}에서 y = {pb}이고, 이를 대입하면 x = {pa}이다. 따라서 {A} 한 {U}의 가격은 {pa}원이다.",
        rubric=[
            {"element": "미지수·식 세우기", "points": 3, "criterion": "두 가격을 x, y로 놓고 {co(m1)}x + {co(n1)}y = {T1}, {co(m2)}x + {co(n2)}y = {T2}{eul(T2)} 세웠다.", "partial": "한 식만 옳으면 1점."},
            {"element": "연립방정식 풀기", "points": 3, "criterion": "가감법 또는 대입법으로 y = {pb}, x = {pa}{eul(pa)} 구했다.", "partial": "한 문자만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{A} 한 {U}의 가격 {pa}원을 답했다.", "partial": "{B}의 가격 {pb}원을 답했으면 인정하지 않는다."},
        ],
    )


SYS_SEED = {
    "seed_id": "m2-1-sys-apply", "category": "활용",
    "title": "연립방정식의 활용 — 자릿수·득점 감점·증감률·두 품목 단가",
    "unit_id": "m2-1", "concept_ids": ["m2-1-14"],
    "schema_id": SCHEMA_SYS, "schema_name": "연립방정식 세우기(문장제)",
    "source_item_ids": [],
    "note": "관계식(두 조건 → 두 일차식)만 차용. 답은 한 수치(처음 수·맞힌 문제 수·올해/작년 남자 쪽 수·단가). 자릿수 틀은 x, k 로 생성해 두 자리 조건을 제약으로 보장.",
    "geometry": False,
    "templates": [sys_t1(), sys_t2(), sys_t3(), sys_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 2. 두 점을 지나는 직선
LINE = {"process": "절차수행", "context": "무맥락", "prereq": ["일차함수의 그래프", "기울기"], "ops": ["함수", "사칙"], "traps": ["기울기 계산", "부호"],
        "time_limit": 80, "points": 4, "tags": ["일차함수", "일차함수의 식"]}
SCHEMA_LINE = "8dea0362-a176-42f3-a743-98a70f3780c6"     # 두 점을 지나는 일차함수 식 구하기

SLOPES = [-4, -3, -2, -1, 1, 2, 3, 4]
FRAC_A = "[[frac({y2} − {pn(y1)}, {x2} − {pn(x1)})]]"     # 기울기 = y의 증가량 / x의 증가량


def frame_derive(xlist: str, ylist: str, lines=(("b", ""),)) -> dict:
    """좌표평면 틀(xlo·xhi·ylo·yhi)과, 직선 y = a x + n 이 틀 안에 머무는 구간의 두 끝점(xs·xe·ys·ye).
    expr 표본화는 틀 밖에서 y를 눌러 수평 꼬리가 생기고, 선분을 틀 밖까지 그리면 SVG 밖으로 삐져나온다 — 그래서 끝점을 직접 자른다."""
    d = {"xlo": f"min({xlist}) - 2", "xhi": f"max({xlist}) + 2", "ylo": f"min({ylist}) - 2", "yhi": f"max({ylist}) + 2"}
    for n, suf in lines:
        d[f"xs{suf}"] = f"max(xlo, min((ylo - {n})/a, (yhi - {n})/a))"
        d[f"xe{suf}"] = f"min(xhi, max((ylo - {n})/a, (yhi - {n})/a))"
        d[f"ys{suf}"] = f"a*xs{suf} + {n}"
        d[f"ye{suf}"] = f"a*xe{suf} + {n}"
    return d


def line_fig(extra_points=None, **kw):
    pts = [{"name": "A", "coord": ["{x1}", "{y1}"]}, {"name": "B", "coord": ["{x2}", "{y2}"]}] + (extra_points or [])
    lines = [{"points": [["{xs}", "{ys}"], ["{xe}", "{ye}"]]}]
    return cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"], pts, lines, **kw)


LINE_BASE_PARAMS = [{"name": "a", "values": {"in": SLOPES}}, {"name": "x1", "values": {"int": [-5, 4]}}, {"name": "dx", "values": {"in": [1, 2, 3, 4]}}, {"name": "b", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}]
LINE_DERIVE = {"x2": "x1 + dx", "y1": "a*x1 + b", "y2": "a*(x1 + dx) + b", "dy": "a*dx"}
LINE_CONS = ["x1 != 0", "x2 != 0", "abs(y1) <= 18", "abs(y2) <= 18", "y1 != y2"]

Q1 = {"sum": {"Q": "a + b", "c1": 1, "c2": 1, "cp": 0}, "diff": {"Q": "a − b", "c1": 1, "c2": -1, "cp": 0}, "prod": {"Q": "ab", "c1": 0, "c2": 0, "cp": 1}}


def line_t1():
    return tpl("m2-1-line-two-points", 1, LINE,
        title="두 점을 지나는 일차함수 y = ax + b — a + b, a − b, ab",
        skill="두 점으로 기울기를 구하고 한 점을 대입해 y절편을 구한 뒤, 묻는 식의 값을 계산하기",
        variant_axis={"구하는 것": "a + b / a − b / ab", "기울기": "±1~±4", "점": "x좌표 −5~8"},
        discriminates="증가량의 순서를 맞춰 기울기의 부호를 바르게 구하는가, 마지막에 묻는 식을 확인하는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "q", "values": {"in": list(Q1)}}] + LINE_BASE_PARAMS,
        table={"key": "q", "rows": Q1},
        derive={**LINE_DERIVE, "ans": "c1*a + c2*b + cp*a*b", **frame_derive("x1, x2, 0", "y1, y2, 0")},
        constraints=LINE_CONS + ["ans != 0", "a != b"],
        cost_values=["x1", "y1", "x2", "y2", "a", "b", "ans"],
        answer_var="ans",
        verify=["(y2 - y1)/(x2 - x1) == a", "y1 - a*x1 == b", "ans == c1*a + c2*b + cp*a*b"],
        question="두 점 ({x1}, {y1}), ({x2}, {y2}){eul(y2)} 지나는 일차함수의 식을 y = ax + b라 할 때, {Q}의 값을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 점을 지나는 직선의 기울기는 (y의 증가량) ÷ (x의 증가량)이다: a = " + FRAC_A + " — 어느 점을 먼저 빼든 분자와 분모의 순서만 같으면 된다. 기울기를 알면 y = {co(a)}x + b에 한 점을 넣어 b를 구한다. 마지막에 묻는 것이 {Q}임을 확인한다.",
        sol1_fig=line_fig(rise_run=["A", "B"], run_label="x의 증가량 {dx}", rise_label="y의 증가량 {dy}"),
        sol2=[
            "기울기 a = " + FRAC_A + " = [[frac({dy}, {dx})]] = {a}",
            "y = {co(a)}x + b에 점 ({x1}, {y1}){eul(y1)} 대입하면 {y1} = {a} × {pn(x1)} + b, b = {y1} − {pn(a*x1)} = {b}",
            "따라서 y = {co(a)}x {sgn(b)}이고, {Q} = {ans}이다.",
        ],
        sol2_fig=steps([
            {"text": "a = " + FRAC_A + " = {a}", "hint": "기울기 = y의 증가량 ÷ x의 증가량"},
            {"text": "{y1} = {a} × {pn(x1)} + b  →  b = {b}", "hint": "점 ({x1}, {y1}) 대입"},
            {"text": "y = {co(a)}x {sgn(b)}  →  {Q} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="구한 식 y = {co(a)}x {sgn(b)}에 다른 점 ({x2}, {y2}){eul(y2)} 넣으면 {a} × {pn(x2)} {sgn(b)} = {y2}로 맞는다. 따라서 a = {a}, b = {b}이고 {Q} = {ans}이다.",
        sol3_fig=line_fig(),
        model_answer="기울기는 a = " + FRAC_A + " = {a}이고, y = {co(a)}x + b에 ({x1}, {y1}){eul(y1)} 대입하면 b = {b}이다. 따라서 {Q} = {ans}이다.",
        rubric=[
            {"element": "기울기 구하기", "points": 3, "criterion": "두 점으로 기울기 a = {a}{eul(a)} 구했다.", "partial": "증가량의 순서를 어긋나게 빼 부호가 반대({-a})이면 1점."},
            {"element": "y절편 구하기", "points": 2, "criterion": "한 점을 대입해 b = {b}{eul(b)} 구했다.", "partial": "대입은 옳고 계산이 틀렸으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "{Q} = {ans}{eul(ans)} 답했다.", "partial": "a, b는 옳은데 {Q}를 잘못 계산했으면 1점."},
        ],
    )


Q2 = {"y": {"Q": "y절편", "isX": 0, "STEP3": "y절편은 x = 0을 대입한 y의 값, 곧 상수항 b이다.", "EQ3": "x = 0  →  y = b", "HINT3": "y축과 만나는 점", "CHECK3": "x = 0을 넣으면 y = b이므로 y절편은 상수항과 같다."},
      "x": {"Q": "x절편", "isX": 1, "STEP3": "x절편은 y = 0을 대입해 0 = ax + b를 푼 x의 값이다.", "EQ3": "y = 0  →  0 = ax + b", "HINT3": "x축과 만나는 점", "CHECK3": "구한 x절편을 넣으면 y = 0이 되어 x축 위의 점임을 확인할 수 있다."}}


def line_t2():
    return tpl("m2-1-line-two-points", 2, LINE,
        title="두 점을 지나는 직선의 x절편·y절편",
        skill="직선의 식을 구한 뒤 y절편은 상수항, x절편은 y = 0을 풀어 구하기",
        variant_axis={"구하는 것": "y절편 / x절편", "기울기": "±1~±4"},
        discriminates="x절편(y = 0)과 y절편(x = 0)을 구별하는가, x절편의 부호(−b/a)를 바르게 처리하는가",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "q", "values": {"in": list(Q2)}}] + LINE_BASE_PARAMS,
        table={"key": "q", "rows": Q2},
        derive={**LINE_DERIVE, "xi": "-b/a", "ans": "isX*(-b/a) + (1 - isX)*b", **frame_derive("x1, x2, 0, isX*xi", "y1, y2, 0, b")},
        constraints=LINE_CONS + ["isX == 0 or b/a == floor(b/a)", "ans != 0"],
        cost_values=["x1", "y1", "x2", "y2", "a", "b", "ans"],
        answer_var="ans",
        verify=["(y2 - y1)/(x2 - x1) == a", "y1 - a*x1 == b", "isX == 0 or a*ans + b == 0", "isX == 1 or ans == b"],
        question="두 점 ({x1}, {y1}), ({x2}, {y2}){eul(y2)} 지나는 직선의 {Q}을 구하시오.",
        answer="{ans}", answer_alt=[],
        sol1="두 점으로 기울기를 구하고 y = ax + b에 한 점을 넣어 b를 구하면 직선의 식이 나온다. y절편은 x = 0일 때의 y값, 곧 b이고, x절편은 y = 0일 때의 x값이므로 0 = ax + b를 풀어 x = −b/a를 구한다. 둘을 혼동하지 않도록 '어느 축과 만나는가'를 먼저 확인한다.",
        sol1_fig=line_fig(extra_points=[{"name": "{Q}", "coord": ["{isX*xi}", "{(1 - isX)*b}"]}]),
        sol2=[
            "기울기 a = " + FRAC_A + " = {a}",
            "y = {co(a)}x + b에 ({x1}, {y1}){eul(y1)} 대입하면 {y1} = {pn(a*x1)} + b, b = {b}이므로 직선의 식은 y = {co(a)}x {sgn(b)}",
            "{STEP3} 따라서 {Q}은 {ans}이다.",
        ],
        sol2_fig=steps([
            {"text": "a = " + FRAC_A + " = {a}", "hint": "기울기"},
            {"text": "y = {co(a)}x {sgn(b)}", "hint": "b = {y1} − {pn(a*x1)}"},
            {"text": "{EQ3}  →  {Q} = {ans}", "hint": "{HINT3}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")]],
        sol3="y = {co(a)}x {sgn(b)}에 x = {x2}를 넣으면 {a} × {pn(x2)} {sgn(b)} = {y2}로 두 번째 점도 지난다. {CHECK3} 답은 {ans}이다.",
        model_answer="a = " + FRAC_A + " = {a}, b = {b}이므로 직선의 식은 y = {co(a)}x {sgn(b)}이다. {STEP3} 따라서 {Q}은 {ans}이다.",
        rubric=[
            {"element": "직선의 식 구하기", "points": 4, "criterion": "기울기 {a}와 y절편 {b}로 y = {co(a)}x {sgn(b)}{eul(b)} 구했다.", "partial": "기울기만 옳으면 2점, 대입 실수로 b가 틀렸으면 2점."},
            {"element": "절편 구하기", "points": 3, "criterion": "{STEP3} {Q} {ans}{eul(ans)} 구했다.", "partial": "x절편과 y절편을 바꿔 구했으면 1점."},
        ],
    )


def line_t3():
    return tpl("m2-1-line-two-points", 3, LINE,
        title="두 점을 지나는 직선 위의 또 다른 점 — (k, m)의 m",
        skill="직선의 식을 구해 x = k를 대입하기(또는 어느 두 점이든 기울기가 같다는 성질 쓰기)",
        variant_axis={"기울기": "±1~±4", "k": "−6~6"},
        discriminates="세 점이 한 직선 위에 있다는 조건을 '직선의 식에 대입' 또는 '기울기가 같다'로 옮기는가",
        qtype="short", difficulty=3, pool_target=300,
        params=LINE_BASE_PARAMS + [{"name": "k", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}],
        derive={**LINE_DERIVE, "m": "a*k + b", **frame_derive("x1, x2, 0, k", "y1, y2, 0, m")},
        constraints=LINE_CONS + ["k != x1", "k != x2", "abs(m) <= 25", "m != k", "m != 0"],
        cost_values=["x1", "y1", "x2", "y2", "a", "b", "k", "m"],
        relation="X - ((y2 - y1)/(x2 - x1)*k + (y1 - (y2 - y1)/(x2 - x1)*x1))", unknown="X", answer_var="m",
        verify=["ans == a*k + b", "(ans - y1)*(x2 - x1) == (y2 - y1)*(k - x1)"],
        question="두 점 ({x1}, {y1}), ({x2}, {y2}){eul(y2)} 지나는 직선이 점 ({k}, m)을 지날 때, m의 값을 구하시오.",
        answer="{m}", answer_alt=[],
        sol1="세 점이 한 직선 위에 있으려면 두 점으로 구한 직선의 식이 세 번째 점도 만족해야 한다. 먼저 기울기 a = " + FRAC_A + "를 구하고 한 점을 대입해 b를 구한 뒤, x = {k}일 때의 y값이 m이다. (어느 두 점을 잡아도 기울기가 같다는 성질로 바로 세울 수도 있다.)",
        sol1_fig=line_fig(extra_points=[{"name": "P", "coord": ["{k}", "{m}"]}]),
        sol2=[
            "기울기 a = " + FRAC_A + " = {a}",
            "y = {co(a)}x + b에 ({x1}, {y1}){eul(y1)} 대입하면 b = {y1} − {pn(a*x1)} = {b}이므로 직선의 식은 y = {co(a)}x {sgn(b)}",
            "x = {k}를 대입하면 m = {a} × {pn(k)} {sgn(b)} = {m}",
        ],
        sol2_fig=steps([
            {"text": "a = " + FRAC_A + " = {a}", "hint": "기울기"},
            {"text": "y = {co(a)}x {sgn(b)}", "hint": "b = {y1} − {pn(a*x1)}"},
            {"text": "m = {a} × {pn(k)} {sgn(b)} = {m}", "hint": "x = {k} 대입"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")]],
        sol3="기울기로 확인: 점 ({x1}, {y1})과 ({k}, {m})의 기울기는 [[frac({m} − {pn(y1)}, {k} − {pn(x1)})]] = {a}로 처음 두 점의 기울기 {a}와 같으므로 세 점은 한 직선 위에 있다. 답은 {m}이다.",
        model_answer="a = " + FRAC_A + " = {a}, b = {b}이므로 직선의 식은 y = {co(a)}x {sgn(b)}이다. x = {k}를 대입하면 m = {m}이다.",
        rubric=[
            {"element": "직선의 식 구하기", "points": 4, "criterion": "기울기 {a}, y절편 {b}로 y = {co(a)}x {sgn(b)}{eul(b)} 구했다.", "partial": "기울기만 옳으면 2점."},
            {"element": "m 구하기", "points": 3, "criterion": "x = {k}를 대입해 m = {m}{eul(m)} 구했다.", "partial": "대입은 옳고 계산이 틀렸으면 1점."},
        ],
    )


def line_t4():
    return tpl("m2-1-line-two-points", 4, LINE,
        title="평행한 직선 + 한 점 — y절편 구하기",
        skill="평행하면 기울기가 같다는 성질로 기울기를 정하고, 점을 대입해 y절편 구하기",
        variant_axis={"기울기": "±1~±4", "주어진 직선의 y절편": "−6~6"},
        discriminates="'평행 → 기울기 같음'을 근거로 쓰는가, 주어진 직선의 y절편을 그대로 답하지 않는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "a", "values": {"in": SLOPES}}, {"name": "c", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}, {"name": "px", "values": {"in": [-5, -4, -3, -2, -1, 1, 2, 3, 4, 5]}}, {"name": "b", "values": {"in": [-6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6]}}],
        derive={"py": "a*px + b", "apx": "a*px", **frame_derive("px, 0", "py, b, c, 0", lines=(("b", ""), ("c", "2")))},
        constraints=["b != c", "abs(py) <= 20", "b != px", "b != py", "b != a", "py != 0"],
        cost_values=["a", "c", "px", "py", "b"],
        relation="a*px + X - py", unknown="X", answer_var="b",
        verify=["py == a*px + ans", "ans != c"],
        question="일차함수 y = {co(a)}x {sgn(c)}의 그래프와 평행하고 점 ({px}, {py}){eul(py)} 지나는 직선의 y절편을 구하시오.",
        answer="{b}", answer_alt=[],
        sol1="평행한 두 직선은 기울기가 같다. 따라서 구하는 직선의 기울기는 {a}이고, y = {co(a)}x + b에 점 ({px}, {py}){eul(py)} 대입해 b를 구한다. y절편은 b이다. (y절편 {c}까지 같으면 평행이 아니라 같은 직선이 된다.)",
        sol1_fig=cplane(["{xlo}", "{xhi}"], ["{ylo}", "{yhi}"],
                        [{"name": "P", "coord": ["{px}", "{py}"]}, {"name": "y절편", "coord": [0, "{b}"]}],
                        [{"points": [["{xs2}", "{ys2}"], ["{xe2}", "{ye2}"]], "style": "dashed"}, {"points": [["{xs}", "{ys}"], ["{xe}", "{ye}"]]}]),
        sol2=[
            "평행하므로 기울기가 같다: a = {a}, 구하는 직선은 y = {co(a)}x + b",
            "점 ({px}, {py}){eul(py)} 대입하면 {py} = {a} × {pn(px)} + b = {apx} + b",
            "b = {py} − {pn(apx)} = {b}이므로 y절편은 {b}이다.",
        ],
        sol2_fig=steps([
            {"text": "y = {co(a)}x + b", "hint": "평행 → 기울기 {a} 그대로"},
            {"text": "{py} = {apx} + b", "hint": "점 ({px}, {py}) 대입"},
            {"text": "b = {b}", "hint": "y절편"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("hint:2")]],
        sol3="y = {co(a)}x {sgn(b)}{eun(b)} 기울기가 {a}로 주어진 직선과 같고 y절편 {b}{eun(b)} {c}{wa(c)} 다르므로 평행하며, x = {px}를 넣으면 {apx} {sgn(b)} = {py}로 점을 지난다. 답은 {b}이다.",
        model_answer="평행한 직선은 기울기가 같으므로 구하는 직선은 y = {co(a)}x + b이다. 점 ({px}, {py}){eul(py)} 대입하면 {py} = {apx} + b, b = {b}이다. 따라서 y절편은 {b}이다.",
        rubric=[
            {"element": "기울기 판단", "points": 3, "criterion": "평행하므로 기울기가 {a}로 같음을 근거와 함께 밝혔다.", "partial": "기울기만 쓰고 근거(평행)가 없으면 1점."},
            {"element": "y절편 구하기", "points": 4, "criterion": "점을 대입해 b = {b}{eul(b)} 구했다.", "partial": "대입은 옳고 계산이 틀렸으면 2점."},
        ],
    )


LINE_SEED = {
    "seed_id": "m2-1-line-two-points", "category": "연산",
    "title": "두 점을 지나는 직선 — a + b·절편·직선 위의 점·평행 조건",
    "unit_id": "m2-1", "concept_ids": ["m2-1-19"],
    "schema_id": SCHEMA_LINE, "schema_name": "두 점을 지나는 일차함수 식 구하기",
    "source_item_ids": [],
    "note": "관계식 a = (y2 − y1)/(x2 − x1), b = y1 − a x1 만 차용. 기울기는 정수(±1~±4)로 두어 답을 정수로 유지. 좌표평면은 해설 도식에만 둔다(문항 도형 없음).",
    "geometry": False,
    "templates": [line_t1(), line_t2(), line_t3(), line_t4()],
}


# ═══════════════════════════════════════════════════════════════════ 3. 지수법칙
EXP = {"process": "절차수행", "context": "무맥락", "prereq": ["거듭제곱"], "ops": ["지수법칙"], "traps": ["지수의 곱·합 혼동"],
       "time_limit": 60, "points": 3, "tags": ["지수법칙"]}
SCHEMA_EXP = "a761a97b-7891-432f-96e6-683bd59c4f20"      # 지수법칙 거듭제곱의 거듭제곱 (곱셈 6dd14896 · 나눗셈 9f470890 · 곱의 거듭제곱 4edae164 · 동수덧셈 942041c3)

VAR = {"x": {"V": "x", "W": "y"}, "a": {"V": "a", "W": "b"}}


def exp_t1():
    return tpl("m2-1-exponent", 1, EXP,
        title="(xᵐ)ⁿ × xᵖ = xᵏ — 거듭제곱의 거듭제곱과 곱셈",
        skill="괄호의 거듭제곱은 지수를 곱하고, 같은 밑의 곱셈은 지수를 더하기",
        variant_axis={"문자": "x / a", "지수": "m 2~6, n 2~4, p 2~7"},
        discriminates="'괄호는 곱, 곱셈은 합'을 구별하는가 — 지수를 전부 더하거나 전부 곱하지 않는가",
        qtype="short", difficulty=2, pool_target=300,
        params=[{"name": "v", "values": {"in": list(VAR)}}, {"name": "m", "values": {"int": [2, 6]}}, {"name": "n", "values": {"int": [2, 4]}}, {"name": "p", "values": {"int": [2, 7]}}],
        table=[{"key": "v", "rows": VAR}, sup_table("m", "SM", 2, 6), sup_table("n", "SN", 2, 4), sup_table("p", "SP", 2, 7)],
        derive={"mn": "m*n", "k": "m*n + p"},
        constraints=["k != m", "k != n", "k != p", "k != m + n + p", "k != m*n*p", "k <= 30"],
        cost_values=["m", "n", "p", "mn", "k"],
        verify=["ans == m*n + p", "ans > m*n"],
        question="({V}{SM}){SN} × {V}{SP} = {V}ᵏ일 때, 자연수 k의 값을 구하시오.",
        answer="{k}", answer_alt=[],
        sol1="거듭제곱의 거듭제곱은 지수를 곱한다: ({V}{SM}){SN} = [[pow({V}, {mn})]] ({V}{SM}을 {n}번 곱한 것이므로 지수 {m}이 {n}번 더해진다). 같은 밑의 곱셈은 지수를 더한다: [[pow({V}, {mn})]] × {V}{SP} = [[pow({V}, {k})]]. '괄호는 곱, 곱셈은 합'을 헷갈리지 않는 것이 핵심이다.",
        sol1_fig=steps(["({V}{SM}){SN} × {V}{SP}", "= [[pow({V}, {mn})]] × {V}{SP}", "= [[pow({V}, {k})]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "({V}{SM}){SN} = [[pow({V}, {mn})]] — 거듭제곱의 거듭제곱은 지수의 곱 {m} × {n} = {mn}",
            "[[pow({V}, {mn})]] × {V}{SP} = [[pow({V}, {k})]] — 같은 밑의 곱은 지수의 합 {mn} + {p} = {k}",
            "따라서 k = {k}이다.",
        ],
        sol2_fig=steps([
            {"text": "({V}{SM}){SN} = [[pow({V}, {mn})]]", "hint": "지수의 곱 {m} × {n}"},
            {"text": "[[pow({V}, {mn})]] × {V}{SP} = [[pow({V}, {k})]]", "hint": "지수의 합 {mn} + {p}"},
            {"text": "k = {k}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="{V}{SM}이 {n}번 곱해지면 지수는 {m}이 {n}번 더해진 {mn}이고, 거기에 {V}{SP}를 곱하면 지수는 {mn} + {p} = {k}이다. 지수를 모두 더하면 {m + n + p}, 모두 곱하면 {m*n*p}{ika(m*n*p)} 되어 틀린다. 답은 {k}이다.",
        model_answer="({V}{SM}){SN} = [[pow({V}, {mn})]]이고 [[pow({V}, {mn})]] × {V}{SP} = [[pow({V}, {k})]]이므로 k = {k}이다.",
        rubric=[
            {"element": "거듭제곱의 거듭제곱", "points": 3, "criterion": "({V}{SM}){SN} = [[pow({V}, {mn})]]으로 지수를 곱했다.", "partial": "지수를 더해 [[pow({V}, {m + n})]]으로 썼으면 인정하지 않는다."},
            {"element": "지수의 합", "points": 2, "criterion": "같은 밑의 곱에서 지수를 더해 [[pow({V}, {k})]]를 얻고 k = {k}{eul(k)} 답했다.", "partial": "지수를 곱해 [[pow({V}, {m*n*p})]]로 썼으면 인정하지 않는다."},
        ],
    )


def exp_t2():
    return tpl("m2-1-exponent", 2, EXP,
        title="xᵐ ÷ xⁿ = xᵏ (m > n) — 같은 밑의 나눗셈",
        skill="같은 밑의 나눗셈은 지수의 차(약분하고 남는 개수)",
        variant_axis={"문자": "x / a", "지수": "m 3~12, n 2~9"},
        discriminates="지수를 빼는가 — 나누거나 더하지 않는가",
        qtype="short", difficulty=1, pool_target=300, time_limit=45,
        params=[{"name": "v", "values": {"in": list(VAR)}}, {"name": "m", "values": {"int": [3, 12]}}, {"name": "n", "values": {"int": [2, 9]}}],
        table={"key": "v", "rows": VAR},
        derive={"k": "m - n"},
        constraints=["m > n", "k >= 2", "k != n", "k != m", "k * n != m"],
        cost_values=["m", "n", "k"],
        verify=["ans == m - n", "ans + n == m"],
        question="[[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = {V}ᵏ일 때, 자연수 k의 값을 구하시오.",
        answer="{k}", answer_alt=[],
        sol1="같은 밑끼리의 나눗셈은 지수를 뺀다 — 분자·분모에서 {V}를 약분하고 남는 개수가 지수가 된다: [[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = [[pow({V}, {k})]]. 앞의 지수가 크면 {V}의 거듭제곱이 남고, 작으면 1/({V}의 거듭제곱)이 되며, 같으면 1이다.",
        sol1_fig=steps(["[[pow({V}, {m})]] ÷ [[pow({V}, {n})]]", "= [[frac(pow({V}, {m}), pow({V}, {n}))]]", "= [[pow({V}, {k})]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "[[pow({V}, {m})]]은 {V}를 {m}번, [[pow({V}, {n})]]은 {V}를 {n}번 곱한 것이므로 나누면 {V}가 {m} − {n} = {k}번 남는다.",
            "[[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = [[pow({V}, {k})]], 따라서 k = {k}이다.",
        ],
        sol2_fig=steps([
            {"text": "[[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = [[pow({V}, {k})]]", "hint": "지수의 차 {m} − {n}"},
            {"text": "k = {k}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)]],
        sol3="[[pow({V}, {n})]] × [[pow({V}, {k})]] = [[pow({V}, {m})]] (지수의 합 {n} + {k} = {m})이므로 나눗셈의 결과가 맞다. 지수를 나누어 {m} ÷ {n}으로 하거나 더해서 {m + n}{ro(m + n)} 하면 틀린다. 답은 {k}이다.",
        model_answer="같은 밑의 나눗셈은 지수를 빼므로 [[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = [[pow({V}, {k})]]이다. 따라서 k = {k}이다.",
        rubric=[
            {"element": "지수의 차", "points": 3, "criterion": "나눗셈에서 지수를 빼 [[pow({V}, {k})]]를 얻었다.", "partial": "지수를 나누거나 더했으면 인정하지 않는다."},
            {"element": "답 구하기", "points": 2, "criterion": "k = {k}{eul(k)} 답했다.", "partial": "부호가 반대인 {-k}{eul(-k)} 답했으면 인정하지 않는다."},
        ],
    )


def exp_t3():
    return tpl("m2-1-exponent", 3, EXP,
        title="xᵐ ÷ xⁿ = 1/xᵏ (m < n) — 분모에 남는 나눗셈",
        skill="지수가 작은 쪽을 큰 쪽으로 나누면 분모에 거듭제곱이 남는다(지수의 차)",
        variant_axis={"문자": "x / a", "지수": "m 2~8, n 3~12"},
        discriminates="m < n일 때 결과가 분수 꼴임을 알고 분모의 지수를 n − m으로 구하는가",
        qtype="short", difficulty=2, pool_target=300, time_limit=50,
        params=[{"name": "v", "values": {"in": list(VAR)}}, {"name": "m", "values": {"int": [2, 8]}}, {"name": "n", "values": {"int": [3, 12]}}],
        table={"key": "v", "rows": VAR},
        derive={"k": "n - m"},
        constraints=["m < n", "k >= 2", "k != n", "k != m", "k * m != n"],
        cost_values=["m", "n", "k"],
        verify=["ans == n - m", "ans + m == n"],
        question="[[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = 1/{V}ᵏ일 때, 자연수 k의 값을 구하시오.",
        answer="{k}", answer_alt=[],
        sol1="지수가 작은 쪽을 큰 쪽으로 나누면 분모에 {V}가 남는다: [[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = [[frac(pow({V}, {m}), pow({V}, {n}))]] = [[frac(1, pow({V}, {k}))]]. 분자·분모에서 {V}를 {m}개씩 약분하면 분모에 {n} − {m} = {k}개가 남는다.",
        sol1_fig=steps(["[[pow({V}, {m})]] ÷ [[pow({V}, {n})]]", "= [[frac(pow({V}, {m}), pow({V}, {n}))]]", "= [[frac(1, pow({V}, {k}))]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "[[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = [[frac(pow({V}, {m}), pow({V}, {n}))]] — 분자·분모에서 {V}를 {m}개씩 약분하면 분모에 {V}가 {n} − {m} = {k}개 남는다.",
            "= [[frac(1, pow({V}, {k}))]], 따라서 k = {k}이다.",
        ],
        sol2_fig=steps([
            {"text": "[[frac(pow({V}, {m}), pow({V}, {n}))]] = [[frac(1, pow({V}, {k}))]]", "hint": "약분 후 분모에 {n} − {m}개"},
            {"text": "k = {k}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1)]],
        sol3="[[frac(1, pow({V}, {k}))]] × [[pow({V}, {n})]] = [[pow({V}, {m})]] (지수 {n} − {k} = {m})이므로 맞다. 분모·분자를 바꿔 [[pow({V}, {k})]]로 답하거나 지수를 더해 {m + n}{ro(m + n)} 하면 틀린다. 답은 {k}이다.",
        model_answer="[[pow({V}, {m})]] ÷ [[pow({V}, {n})]] = [[frac(pow({V}, {m}), pow({V}, {n}))]]에서 분자·분모를 약분하면 [[frac(1, pow({V}, {k}))]]이다. 따라서 k = {k}이다.",
        rubric=[
            {"element": "지수의 차", "points": 3, "criterion": "약분하여 분모에 [[pow({V}, {k})]]가 남음을 밝혔다.", "partial": "[[pow({V}, {k})]]로 분모·분자를 바꿔 답했으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "k = {k}{eul(k)} 답했다.", "partial": "{m} − {n} = {m - n}{ro(m - n)} 음수를 답했으면 인정하지 않는다."},
        ],
    )


def exp_t4():
    return tpl("m2-1-exponent", 4, EXP,
        title="(cxⁱyʲ)ᵖ = Axᵐyⁿ — 곱의 거듭제곱과 A + m + n",
        skill="괄호 안 각 인수에 지수를 나누어 주기 — 계수도 p제곱, 문자의 지수는 p배",
        variant_axis={"문자": "x, y / a, b", "계수": "±2, ±3, 5", "지수": "i, j 1~5 · p 2, 3"},
        discriminates="계수에도 거듭제곱을 하는가(p배가 아니라), 문자의 지수를 곱하는가(더하지 않고)",
        qtype="short", difficulty=3, pool_target=300,
        params=[{"name": "v", "values": {"in": list(VAR)}}, {"name": "c", "values": {"in": [2, 3, -2, -3, 5]}}, {"name": "i", "values": {"int": [1, 5]}}, {"name": "j", "values": {"int": [1, 5]}}, {"name": "p", "values": {"in": [2, 3]}}],
        table=[{"key": "v", "rows": VAR}, sup_table("i", "SI", 1, 5), sup_table("j", "SJ", 1, 5), sup_table("p", "SP", 2, 3)],
        derive={"A": "c**p", "m2": "i*p", "n2": "j*p", "S": "c**p + i*p + j*p"},
        constraints=["S != i", "S != j", "S != p", "S != c", "i != j", "S != 0"],
        cost_values=["c", "i", "j", "p", "A", "m2", "n2", "S"],
        verify=["ans == c**p + i*p + j*p", "A == c**p"],
        question="({co(c)}{V}{SI}{W}{SJ}){SP} = A{V}ᵐ{W}ⁿ일 때, 상수 A, m, n에 대하여 A + m + n의 값을 구하시오.",
        answer="{S}", answer_alt=[],
        sol1="곱의 거듭제곱은 괄호 안의 각 인수에 지수를 나누어 준다: ({co(c)}{V}{SI}{W}{SJ}){SP} = {pn(c)}{SP} × ({V}{SI}){SP} × ({W}{SJ}){SP}. 계수 {c}에도 {p}제곱을 해야 하고({p}배가 아니다), 문자의 지수는 곱해서 {i} × {p}, {j} × {p}가 된다.",
        sol1_fig=steps(["({co(c)}{V}{SI}{W}{SJ}){SP}", "= {pn(c)}{SP} × ({V}{SI}){SP} × ({W}{SJ}){SP}", "= {A}[[pow({V}, {m2})]][[pow({W}, {n2})]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "계수: {pn(c)}{SP} = {A}",
            "{V}의 지수: {i} × {p} = {m2}, {W}의 지수: {j} × {p} = {n2}",
            "({co(c)}{V}{SI}{W}{SJ}){SP} = {A}[[pow({V}, {m2})]][[pow({W}, {n2})]]이므로 A = {A}, m = {m2}, n = {n2}",
            "따라서 A + m + n = {A} + {m2} + {n2} = {S}이다.",
        ],
        sol2_fig=steps([
            {"text": "{pn(c)}{SP} = {A}", "hint": "계수도 {p}제곱"},
            {"text": "({V}{SI}){SP} = [[pow({V}, {m2})]],  ({W}{SJ}){SP} = [[pow({W}, {n2})]]", "hint": "지수 × {p}"},
            {"text": "A + m + n = {A} + {m2} + {n2} = {S}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)], []],
        sol3="{A}[[pow({V}, {m2})]][[pow({W}, {n2})]]는 {co(c)}{V}{SI}{W}{SJ}를 {p}번 곱한 것과 같다: 계수 {c}가 {p}번 곱해져 {A}, {V}는 {i}개씩 {p}묶음이라 {m2}개, {W}는 {j}개씩 {p}묶음이라 {n2}개. 계수를 {p}배 한 {c*p}{ro(c*p)} 쓰면 틀린다. 답은 {S}이다.",
        model_answer="({co(c)}{V}{SI}{W}{SJ}){SP} = {pn(c)}{SP}[[pow({V}, {m2})]][[pow({W}, {n2})]] = {A}[[pow({V}, {m2})]][[pow({W}, {n2})]]이므로 A = {A}, m = {m2}, n = {n2}이다. 따라서 A + m + n = {S}이다.",
        rubric=[
            {"element": "계수의 거듭제곱", "points": 2, "criterion": "계수에도 {p}제곱을 하여 A = {A}{eul(A)} 얻었다.", "partial": "계수를 {p}배 하여 {c*p}{ro(c*p)} 썼으면 인정하지 않는다."},
            {"element": "지수의 곱", "points": 3, "criterion": "각 문자의 지수에 {p}{eul(p)} 곱해 m = {m2}, n = {n2}{eul(n2)} 얻었다.", "partial": "한 문자만 옳으면 1점."},
            {"element": "답 구하기", "points": 2, "criterion": "A + m + n = {S}{eul(S)} 답했다.", "partial": "A, m, n은 옳은데 합을 잘못 계산했으면 1점."},
        ],
    )


def add_rows():
    """같은 거듭제곱의 덧셈 — 밑 B 를 B 번 더하면 지수 +1, 2 를 4 번 더하면 +2. 행마다 식 문자열을 미리 만든다."""
    rows = {}
    for B in (2, 3, 4, 5):
        for m in range(2, 10):
            term = f"{B}{sup(m)}"
            rows[f"{B}-{m}"] = {"B": B, "m": m, "cnt": B, "e": 1, "k": m + 1, "SUM": " + ".join([term] * B), "CP": str(B)}
    for m in range(2, 10):
        term = f"2{sup(m)}"
        rows[f"2x4-{m}"] = {"B": 2, "m": m, "cnt": 4, "e": 2, "k": m + 2, "SUM": " + ".join([term] * 4), "CP": "2²"}
    return rows


ADD_ROWS = add_rows()


def exp_t5():
    return tpl("m2-1-exponent", 5, EXP,
        title="2ᵐ + 2ᵐ = 2ᵏ — 같은 거듭제곱의 덧셈",
        skill="같은 항의 덧셈은 '몇 배'로 바꾸고, 그 배수를 밑의 거듭제곱으로 고쳐 지수를 더하기",
        variant_axis={"밑": "2·3·4·5", "개수": "밑과 같은 개수(지수 +1) / 2를 4개(지수 +2)", "지수": "2~9"},
        discriminates="덧셈을 곱셈으로 착각해 지수를 더하지 않는가 — n × aᵐ 을 a의 거듭제곱으로 바꾸는가",
        qtype="short", difficulty=3, pool_target=300, time_limit=70,
        params=[{"name": "r", "values": {"in": list(ADD_ROWS)}}],
        table={"key": "r", "rows": ADD_ROWS},
        derive={"km": "cnt*m"},
        constraints=["k != B", "k != m"],
        cost_values=["B", "m", "cnt", "k"],
        verify=["B**ans == cnt*B**m", "ans == m + e"],
        answer_var="k",
        question="{SUM} = {B}ᵏ일 때, 자연수 k의 값을 구하시오.",
        answer="{k}", answer_alt=[],
        sol1="같은 수를 {cnt}번 더한 것은 {cnt}배와 같다: {SUM} = {cnt} × [[pow({B}, {m})]]. 그런데 {cnt} = {CP}이므로 {cnt} × [[pow({B}, {m})]] = {CP} × [[pow({B}, {m})]] = [[pow({B}, {k})]] (같은 밑의 곱 → 지수의 합 {e} + {m}). 덧셈을 곱셈으로 착각해 지수를 더하면 안 된다.",
        sol1_fig=steps(["{SUM}", "= {cnt} × [[pow({B}, {m})]]", "= {CP} × [[pow({B}, {m})]] = [[pow({B}, {k})]]"]),
        sol1_anim=[[reveal(0)], [reveal(1)], [reveal(2)]],
        sol2=[
            "같은 항을 {cnt}번 더하면 {cnt}배이다: {SUM} = {cnt} × [[pow({B}, {m})]]",
            "{cnt} = {CP}이므로 {CP} × [[pow({B}, {m})]] = [[pow({B}, {k})]] (지수의 합 {e} + {m} = {k})",
            "따라서 k = {k}이다.",
        ],
        sol2_fig=steps([
            {"text": "{SUM} = {cnt} × [[pow({B}, {m})]]", "hint": "같은 항 {cnt}개 = {cnt}배"},
            {"text": "= {CP} × [[pow({B}, {m})]] = [[pow({B}, {k})]]", "hint": "{cnt} = {CP} → 지수 {e} + {m}"},
            {"text": "k = {k}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2)]],
        sol3="[[pow({B}, {k})]] = [[pow({B}, {m})]] × {CP}, 곧 [[pow({B}, {m})]]을 {cnt}번 더한 것과 같으므로 맞다. 지수를 더해 {km}으로 답하면 [[pow({B}, {m})]]을 {cnt}번 곱한 것이 되어 틀린다. 답은 {k}이다.",
        model_answer="{SUM} = {cnt} × [[pow({B}, {m})]] = {CP} × [[pow({B}, {m})]] = [[pow({B}, {k})]]이므로 k = {k}이다.",
        rubric=[
            {"element": "덧셈을 곱셈으로", "points": 3, "criterion": "{SUM} = {cnt} × [[pow({B}, {m})]]임을 밝혔다.", "partial": "지수를 더해 [[pow({B}, {km})]]으로 썼으면 인정하지 않는다."},
            {"element": "지수의 합", "points": 2, "criterion": "{cnt} = {CP}로 고쳐 [[pow({B}, {k})]]를 얻고 k = {k}{eul(k)} 답했다.", "partial": "{cnt} × [[pow({B}, {m})]]까지만 옳으면 1점."},
        ],
    )


EXP_SEED = {
    "seed_id": "m2-1-exponent", "category": "연산",
    "title": "지수법칙 — 거듭제곱의 거듭제곱·나눗셈(두 꼴)·곱의 거듭제곱·같은 거듭제곱의 덧셈",
    "unit_id": "m2-1", "concept_ids": ["m2-1-03"],
    "schema_id": SCHEMA_EXP, "schema_name": "지수법칙 거듭제곱의 거듭제곱 / 곱셈·나눗셈 / 곱의 거듭제곱 / 동수덧셈변환",
    "source_item_ids": [],
    "note": "답은 지수(자연수)나 계수·지수의 합. 단일 거듭제곱은 [[pow(x, k)]] 마커, 중첩·곱의 거듭제곱은 표의 위첨자 평문. 미지수 지수는 평문 xᵏ.",
    "geometry": False,
    "templates": [exp_t1(), exp_t2(), exp_t3(), exp_t4(), exp_t5()],
}


if __name__ == "__main__":
    for seed in (SYS_SEED, LINE_SEED, EXP_SEED):
        with_pitfalls(seed)
        dump(seed)
