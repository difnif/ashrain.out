# itemfactory/tools/mkseed_motion.py — 상황 도식 시드 생성기: 강물(river) · 등산(mountain) (v1.0)
#
#   python itemfactory/tools/mkseed_motion.py
#     → seeds/m2-1-river-boat.json, seeds/m2-1-mountain-hike.json
#
# 원칙 (Park, 09-07): 상황은 **간단하고 직관적인 그림 하나**로 옮긴다 — 그래야 식이 그대로 읽히고 실수가 줄어든다.
#   강물   두 줄이 강, 강 안에 강물 방향·속력, 위에는 순방향(내려갈 때) 조건, 아래에는 역방향(올라올 때) 조건.
#   등산   우상향 굵은 초록 직선이 산, 오를 때 조건은 왼쪽에 화살표와 함께, 내려올 때는 반대편에.
#   둘 다 전부 한 번에 그리고 애니메이션은 강조만.
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SEEDS = os.path.join(HERE, "..", "seeds")

COMMON = {
    "prereq": ["거리=속력×시간", "연립방정식의 풀이(가감법)"],
    "process": "문제해결",
    "context": "생활맥락",
    "ops": ["방정식", "사칙"],
    "traps": ["부호", "조건누락"],
    "time_limit": 150,
    "points": 5,
}


# ---------------------------------------------------------------- 강물
def river_fig(flow, down_lbl, down_sub, up_lbl, up_sub):
    return [{"fn": "river", "args": {
        "stops": ["A", "B"], "span": "{D} km",
        "flow": {"label": flow, "dir": "right"},
        "down": {"label": down_lbl, "sub": down_sub},
        "up": {"label": up_lbl, "sub": up_sub},
    }}]


RIVER_SOL1 = (
    "내려갈 때는 강물이 배를 밀어 주므로 실제 속력은 (배의 속력) + (강물의 속력), 거슬러 올라올 때는 강물이 배를 막으므로 "
    "(배의 속력) − (강물의 속력)이다. 두 번 모두 같은 {D} km를 갔으니 (속력) × (시간) = {D}{eul(D)} 두 번 쓰면 미지수가 2개인 연립방정식이 된다. "
    "강을 두 줄로 그리고 강물 방향을 표시한 뒤, 위에는 내려갈 때 조건, 아래에는 올라올 때 조건을 적어 두면 어느 쪽이 +이고 어느 쪽이 −인지 헷갈리지 않는다."
)
RIVER_SOL1_FIG = river_fig("강물 시속 y km", "내려갈 때 {t1}시간", "(x + y) × {t1} = {D}", "올라올 때 {t2}시간", "(x − y) × {t2} = {D}")
RIVER_SOL1_ANIM = [
    [{"act": "hl", "k": ["flow", "flow-lbl"], "keep": True}],
    [{"act": "hl", "k": ["down", "down-lbl", "down-sub"]}],
    [{"act": "hl", "k": ["up", "up-lbl", "up-sub"]}],
]
RIVER_SOL2 = [
    "정지한 물에서 배의 속력을 시속 x km, 강물의 속력을 시속 y km라 하자.",
    "내려갈 때 속력은 시속 (x + y) km이고 {t1}시간 동안 {D} km를 갔으므로 (x + y) × {t1} = {D}, 곧 x + y = {s1}",
    "올라올 때 속력은 시속 (x − y) km이고 {t2}시간 동안 {D} km를 갔으므로 (x − y) × {t2} = {D}, 곧 x − y = {s2}",
    "두 식을 더하면 y가 사라진다: 2x = {s1} + {s2} = {2*b}, 따라서 x = {b}",
    "x = {b}{eul(b)} x + y = {s1}에 넣으면 y = {s1} − {b} = {w}",
]
RIVER_SOL2_FIG = [{"fn": "steps", "args": {"lines": [
    {"text": "(x + y) × {t1} = {D}", "hint": "내려갈 때 — 강물이 밀어 준다 (+)"},
    {"text": "(x − y) × {t2} = {D}", "hint": "올라올 때 — 강물이 막는다 (−)"},
    {"text": "x + y = {s1}", "marks": [{"on": "{s1}", "note": "{D} ÷ {t1}"}]},
    {"text": "x − y = {s2}", "marks": [{"on": "{s2}", "note": "{D} ÷ {t2}"}]},
    {"text": "2x = {2*b}", "hint": "두 식을 더하면 y가 사라진다"},
    "x = {b},  y = {s1} − {b} = {w}",
]}}]
RIVER_SOL2_ANIM = [
    [],
    [{"act": "reveal", "k": "line:0"}, {"act": "hl", "k": "hint:0"}, {"act": "reveal", "k": "line:2"}, {"act": "hl", "k": "mark:2-0"}],
    [{"act": "reveal", "k": "line:1"}, {"act": "hl", "k": "hint:1"}, {"act": "reveal", "k": "line:3"}, {"act": "hl", "k": "mark:3-0"}],
    [{"act": "reveal", "k": "line:4"}, {"act": "hl", "k": "hint:4"}],
    [{"act": "reveal", "k": "line:5"}],
]
RIVER_SOL3_FIG = river_fig("강물 시속 {w} km", "시속 {s1} km · {t1}시간", "{s1} × {t1} = {D}", "시속 {s2} km · {t2}시간", "{s2} × {t2} = {D}")
RIVER_SOL3_ANIM = [
    [{"act": "hl", "k": ["down", "down-lbl", "down-sub"]}],
    [{"act": "hl", "k": ["up", "up-lbl", "up-sub"]}],
]
RIVER_SOL3 = (
    "배 시속 {b} km, 강물 시속 {w} km로 되짚어 본다. 내려갈 때는 시속 {s1} km로 {t1}시간 → {s1} × {t1} = {D} (km), "
    "올라올 때는 시속 {s2} km로 {t2}시간 → {s2} × {t2} = {D} (km)로 두 거리가 모두 {D} km로 같다. "
    "거슬러 올라올 때가 더 오래 걸린 것({t2}시간 > {t1}시간)도 상식에 맞는다. 답은 {ans_text}다."
)
RIVER_MODEL = (
    "정지한 물에서 배의 속력을 시속 x km, 강물의 속력을 시속 y km라 하면 내려갈 때 속력은 시속 (x + y) km, 올라올 때 속력은 시속 (x − y) km이다. "
    "같은 {D} km를 각각 {t1}시간, {t2}시간에 갔으므로 (x + y) × {t1} = {D}, (x − y) × {t2} = {D}, 곧 x + y = {s1}, x − y = {s2}이다. "
    "두 식을 더하면 2x = {2*b}에서 x = {b}이고, y = {s1} − {b} = {w}이다. 따라서 {ans_model}다."
)
RIVER_RUBRIC = [
    {"element": "속력의 합·차 파악", "points": 2, "criterion": "내려갈 때 (배 + 강물), 올라올 때 (배 − 강물)임을 밝혔다.", "partial": "한쪽만 옳으면 1점."},
    {"element": "연립방정식 세우기", "points": 3, "criterion": "(x + y) × {t1} = {D}, (x − y) × {t2} = {D}(또는 x + y = {s1}, x − y = {s2})를 세웠다.", "partial": "한 식만 세웠으면 1점."},
    {"element": "풀이·답", "points": 3, "criterion": "두 식을 더하거나 빼서 x = {b}, y = {w}{eul(w)} 구하고 {ans_rubric}로 썼다.", "partial": "가감법을 시작해 한 미지수를 구했으면 2점."},
]
# 제약은 필터가 아니라 생성 규칙에 내장 (LOCALGUIDE §3): 내려갈 속력 s1·올라올 속력 s2 를 **같은 홀짝의 쌍**으로 미리 골라
# 배 b=(s1+s2)/2, 강물 w=(s1−s2)/2 가 언제나 정수가 되게 한다. 쌍은 ss = s1·100 + s2 한 값으로 넘긴다.
RIVER_PAIRS = [402, 503, 602, 604, 703, 705, 802, 804, 806, 903, 905, 907, 1002, 1004, 1006, 1008, 1204, 1206, 1208, 1210, 1410, 1505, 1509, 1612]
RIVER_PARAMS = [
    {"name": "ss", "values": {"in": RIVER_PAIRS}},
    {"name": "k", "values": {"int": [1, 3]}},
]
RIVER_DERIVE = {"s1": "floor(ss/100)", "s2": "ss % 100", "b": "(floor(ss/100) + ss % 100)/2", "w": "(floor(ss/100) - ss % 100)/2",
                "D": "k*lcm(floor(ss/100), ss % 100)", "t1": "k*lcm(floor(ss/100), ss % 100)/floor(ss/100)", "t2": "k*lcm(floor(ss/100), ss % 100)/(ss % 100)"}
RIVER_CONSTRAINTS = ["D <= 72", "t2 <= 9", "D != b", "D != w", "t1 != w", "t2 != b", "t1 != b", "t2 != w"]
RIVER_Q = ("배를 타고 강을 따라 {D} km 떨어진 A 지점에서 B 지점까지 내려가는 데 {t1}시간이 걸리고, "
           "B 지점에서 A 지점까지 거슬러 올라오는 데 {t2}시간이 걸렸다. 강물의 속력이 일정할 때, ")


def sub_all(obj, rep):
    if isinstance(obj, str):
        for a, b in rep.items():
            obj = obj.replace(a, b)
        return obj
    if isinstance(obj, list):
        return [sub_all(x, rep) for x in obj]
    if isinstance(obj, dict):
        return {k: sub_all(v, rep) for k, v in obj.items()}
    return obj


def river_tpl(which):
    boat = which == "boat"
    rep = {"{ans_text}": "시속 {b} km" if boat else "시속 {w} km",
           "{ans_model}": "정지한 물에서 배의 속력은 시속 {b} km" if boat else "강물의 속력은 시속 {w} km",
           "{ans_rubric}": "답을 시속 {b} km" if boat else "답을 시속 {w} km"}
    t = {
        **COMMON,
        "id": f"m2-1-river-{which}",
        "title": "강물 — 배의 속력 구하기" if boat else "강물 — 강물의 속력 구하기",
        "skill": "순방향·역방향 속력을 합·차로 놓고 같은 거리로 연립방정식 세우기",
        "variant_axis": {"구하는 것": "배의 속력" if boat else "강물의 속력", "시나리오": "강 내려가기·거슬러 오르기"},
        "discriminates": "강물의 영향을 +와 −로 올바르게 붙이는가, 같은 거리라는 조건을 쓰는가",
        "qtype": "short", "difficulty": 3 if boat else 4, "pool_target": 300,
        "tags": ["거속시", "강물", "연립방정식"],
        "params": RIVER_PARAMS, "derive": RIVER_DERIVE, "constraints": RIVER_CONSTRAINTS,
        "cost_values": ["b", "w", "s1", "s2", "D", "t1", "t2", "2*b"],
        "relation": "(X + w)*t1 - D" if boat else "(b + X)*t1 - D",
        "unknown": "X",
        "answer_var": "b" if boat else "w",
        "verify": ["(b + w)*t1 == D", "(b - w)*t2 == D", "ans == b" if boat else "ans == w"],
        "question": RIVER_Q + ("정지한 물에서의 배의 속력은 시속 몇 km인지 구하시오." if boat else "강물의 속력은 시속 몇 km인지 구하시오."),
        "figure": river_fig("강물", "내려갈 때 {t1}시간", "", "올라올 때 {t2}시간", ""),
        "answer": "{b}" if boat else "{w}",
        "answer_alt": ["시속 {b} km", "{b} km/h"] if boat else ["시속 {w} km", "{w} km/h"],
        "sol1": RIVER_SOL1, "sol1_fig": RIVER_SOL1_FIG, "sol1_anim": RIVER_SOL1_ANIM,
        "sol2": RIVER_SOL2, "sol2_fig": RIVER_SOL2_FIG, "sol2_anim": RIVER_SOL2_ANIM,
        "sol3": RIVER_SOL3, "sol3_fig": RIVER_SOL3_FIG, "sol3_anim": RIVER_SOL3_ANIM,
        "model_answer": RIVER_MODEL, "rubric": RIVER_RUBRIC, "rubric_total": 8,
    }
    return sub_all(t, rep)


RIVER_SEED = {
    "seed_id": "m2-1-river-boat", "category": "활용",
    "title": "강물 — 내려가기·거슬러 오르기 (연립방정식)",
    "unit_id": "m2-1", "concept_ids": ["m2-1-14"],
    "schema_id": None, "schema_name": "속력의 합·차와 같은 거리 — 배와 강물",
    "source_item_ids": [],
    "note": "관계식 (배 ± 강물) × 시간 = 거리 만 차용. 정수해가 나오도록 거리를 (b+w)·(b−w)의 공배수로 생성한다. 그림은 river(두 줄 강).",
    "geometry": False,
    "templates": [river_tpl("boat"), river_tpl("stream")],
}


# ---------------------------------------------------------------- 등산
def mtn_fig(up_lbl, up_sub, down_lbl, down_sub, total):
    return [{"fn": "mountain", "args": {"base": "출발", "peak": "정상",
                                        "up": {"label": up_lbl, "sub": up_sub}, "down": {"label": down_lbl, "sub": down_sub}, "total": total}}]


MTN_SOL1 = (
    "오르는 길과 내려오는 길이 다르므로 두 거리를 따로 x km, y km로 둔다. 조건은 두 가지다 — 거리: x + y = {D}, "
    "시간: 오를 때 x/{a}시간과 내려올 때 y/{b}시간의 합이 {T}시간. 산을 우상향 직선 하나로 그리고 오를 때 조건은 왼쪽에, "
    "내려올 때 조건은 반대편에 화살표와 함께 적어 두면 두 식이 그림에서 그대로 읽힌다."
)
MTN_SOL1_FIG = mtn_fig("오를 때 시속 {a} km", "x km", "내려올 때 시속 {b} km", "y km", "모두 {D} km · {T}시간")
MTN_SOL1_ANIM = [
    [{"act": "hl", "k": ["base-lbl", "peak-lbl"]}],          # 산(초록 선)은 그대로 두고 출발·정상만 짚는다
    [{"act": "hl", "k": ["up", "up-lbl", "up-sub"]}],
    [{"act": "hl", "k": ["down", "down-lbl", "down-sub"]}],
    [{"act": "hl", "k": "total-lbl"}],
]
MTN_SOL2 = [
    "올라간 거리를 x km, 내려온 거리를 y km라 하자.",
    "거리 조건: 두 길을 합쳐 {D} km이므로 x + y = {D}",
    "시간 조건: 오를 때 x/{a}시간, 내려올 때 y/{b}시간이므로 x/{a} + y/{b} = {T}. 분모의 최소공배수 {L}{eul(L)} 양변에 곱하면 {co(L/a)}x + {co(L/b)}y = {T*L}",
    "x + y = {D}의 양변에 {L/b}{eul(L/b)} 곱해 {co(L/b)}x + {co(L/b)}y = {D*L/b}{eul(D*L/b)} 만들고, 시간 식에서 빼면 y가 사라진다: {co(L/a - L/b)}x = {T*L - D*L/b}",
    "따라서 x = {x}이고, 이를 x + y = {D}에 넣으면 y = {D} − {x} = {y}",
]
MTN_SOL2_FIG = [{"fn": "steps", "args": {"lines": [
    {"text": "x + y = {D}", "hint": "거리 조건"},
    {"text": "x/{a} + y/{b} = {T}", "hint": "시간 조건"},
    {"text": "{co(L/a)}x + {co(L/b)}y = {T*L}", "hint": "양변 × {L}", "marks": [{"on": "{co(L/a)}x", "note": "{L}÷{a}"}, {"on": "{co(L/b)}y", "note": "{L}÷{b}"}]},
    {"text": "{co(L/b)}x + {co(L/b)}y = {D*L/b}", "hint": "거리 식 × {L/b} — y의 계수를 맞춘다"},
    {"text": "{co(L/a - L/b)}x = {T*L - D*L/b}", "hint": "빼면 y가 사라진다"},
    {"text": "y = {D} − {x} = {y}", "hint": "x = {x}를 거리 식에 넣는다"},
]}}]
MTN_SOL2_ANIM = [
    [],
    [{"act": "reveal", "k": "line:0"}, {"act": "hl", "k": "hint:0"}],
    [{"act": "reveal", "k": "line:1"}, {"act": "hl", "k": "hint:1"}, {"act": "reveal", "k": "line:2"}, {"act": "hl", "k": ["hint:2", "mark:2-0", "mark:2-1"]}],
    [{"act": "reveal", "k": "line:3"}, {"act": "hl", "k": "hint:3"}, {"act": "reveal", "k": "line:4"}, {"act": "hl", "k": "hint:4"}],
    [{"act": "reveal", "k": "line:5"}, {"act": "hl", "k": "hint:5"}],
]
MTN_SOL3_FIG = mtn_fig("시속 {a} km · {p}시간", "{x} km", "시속 {b} km · {q}시간", "{y} km", "모두 {D} km · {T}시간")
MTN_SOL3_ANIM = [
    [{"act": "hl", "k": ["up", "up-lbl", "up-sub"]}],
    [{"act": "hl", "k": ["down", "down-lbl", "down-sub"]}],
    [{"act": "hl", "k": "total-lbl"}],
]
MTN_SOL3 = (
    "올라간 {x} km를 시속 {a} km로 가면 {x} ÷ {a} = {p}시간, 내려온 {y} km를 시속 {b} km로 가면 {y} ÷ {b} = {q}시간이다. "
    "시간의 합 {p} + {q} = {T}시간, 거리의 합 {x} + {y} = {D} km로 두 조건이 모두 맞는다. 답은 {ans_text}다."
)
MTN_MODEL = (
    "올라간 거리를 x km, 내려온 거리를 y km라 하면 x + y = {D}이고, 걸린 시간에서 x/{a} + y/{b} = {T}이다. "
    "둘째 식의 양변에 {L}{eul(L)} 곱하면 {co(L/a)}x + {co(L/b)}y = {T*L}이고, 첫째 식의 양변에 {L/b}{eul(L/b)} 곱해 빼면 {co(L/a - L/b)}x = {T*L - D*L/b}에서 x = {x}, y = {y}이다. "
    "실제로 {x} ÷ {a} + {y} ÷ {b} = {p} + {q} = {T}시간이므로 {ans_model}다."
)
MTN_RUBRIC = [
    {"element": "조건 두 개 읽기", "points": 2, "criterion": "거리 조건(합이 {D} km)과 시간 조건(합이 {T}시간)을 구분해 썼다.", "partial": "하나만 썼으면 1점."},
    {"element": "연립방정식 세우기", "points": 3, "criterion": "x + y = {D}{wa(D)} x/{a} + y/{b} = {T}{eul(T)} 세웠다.", "partial": "한 식만 세웠으면 1점."},
    {"element": "풀이·답", "points": 3, "criterion": "분모를 없애고 가감법으로 x = {x}, y = {y}{eul(y)} 구하고 {ans_rubric}로 썼다.", "partial": "분모를 없애는 단계까지 옳으면 1점."},
]
# 속력 쌍 (a, b) 는 a < b 이고 a 가 b 의 약수가 아닌 것만 (그래야 y 의 계수를 맞추는 곱이 1이 아니다). ab = a·10 + b.
MTN_PAIRS = [23, 25, 34, 35, 45, 46, 56]
MTN_PARAMS = [
    {"name": "ab", "values": {"in": MTN_PAIRS}},
    {"name": "p", "values": {"int": [2, 4]}},      # 1시간이면 거리 = 속력 수치라 답이 문면에 노출된다
    {"name": "q", "values": {"int": [2, 4]}},
]
MTN_DERIVE = {"a": "floor(ab/10)", "b": "ab % 10", "L": "lcm(floor(ab/10), ab % 10)", "x": "floor(ab/10)*p", "y": "(ab % 10)*q",
              "D": "floor(ab/10)*p + (ab % 10)*q", "T": "p + q"}
MTN_CONSTRAINTS = ["x != y", "D <= 40", "T <= 8", "x != a", "y != b", "x != T", "y != T", "x != D", "y != D"]
MTN_Q = ("등산을 하는데 올라갈 때는 시속 {a} km로, 내려올 때는 다른 길을 시속 {b} km로 걸어서 모두 {D} km를 {T}시간 만에 다녀왔다. ")


def mtn_tpl(which):
    up = which == "up"
    rep = {"{ans_text}": "{x} km" if up else "{y} km",
           "{ans_model}": "올라간 거리는 {x} km" if up else "내려온 거리는 {y} km",
           "{ans_rubric}": "답을 {x} km" if up else "답을 {y} km"}
    t = {
        **COMMON,
        "id": f"m2-1-mountain-{which}",
        "title": "등산 — 올라간 거리 구하기" if up else "등산 — 내려온 거리 구하기",
        "skill": "거리 조건과 시간 조건 두 개로 연립방정식 세우기",
        "variant_axis": {"구하는 것": "올라간 거리" if up else "내려온 거리", "시나리오": "다른 길로 오르고 내리기"},
        "discriminates": "총 시간을 구간별 시간의 합으로 쪼개고, 총 거리 조건을 함께 쓰는가",
        "qtype": "short", "difficulty": 3, "pool_target": 300,
        "tags": ["거속시", "등산", "연립방정식"],
        "params": MTN_PARAMS, "derive": MTN_DERIVE, "constraints": MTN_CONSTRAINTS,
        "cost_values": ["a", "b", "x", "y", "D", "T", "L", "T*L", "D*L/b"],
        "relation": "X/a + (D - X)/b - T" if up else "(D - X)/a + X/b - T",
        "unknown": "X",
        "answer_var": "x" if up else "y",
        "verify": ["x/a + y/b == T", "x + y == D", "ans == x" if up else "ans == y"],
        "question": MTN_Q + ("올라간 거리는 몇 km인지 구하시오." if up else "내려온 거리는 몇 km인지 구하시오."),
        "figure": mtn_fig("오를 때 시속 {a} km", "", "내려올 때 시속 {b} km", "", "모두 {D} km · {T}시간"),
        "answer": "{x}" if up else "{y}",
        "answer_alt": ["{x} km"] if up else ["{y} km"],
        "sol1": MTN_SOL1, "sol1_fig": MTN_SOL1_FIG, "sol1_anim": MTN_SOL1_ANIM,
        "sol2": MTN_SOL2, "sol2_fig": MTN_SOL2_FIG, "sol2_anim": MTN_SOL2_ANIM,
        "sol3": MTN_SOL3, "sol3_fig": MTN_SOL3_FIG, "sol3_anim": MTN_SOL3_ANIM,
        "model_answer": MTN_MODEL, "rubric": MTN_RUBRIC, "rubric_total": 8,
    }
    return sub_all(t, rep)


MTN_SEED = {
    "seed_id": "m2-1-mountain-hike", "category": "활용",
    "title": "등산 — 다른 길로 오르고 내리기 (연립방정식)",
    "unit_id": "m2-1", "concept_ids": ["m2-1-14"],
    "schema_id": None, "schema_name": "구간별 속력이 다른 이동 — 거리 조건 + 시간 조건",
    "source_item_ids": [],
    "note": "관계식 x + y = D, x/a + y/b = T 만 차용. 정수해가 나오도록 x = a·p, y = b·q 로 생성한다. 그림은 mountain(우상향 초록 직선).",
    "geometry": False,
    "templates": [mtn_tpl("up"), mtn_tpl("down")],
}

def _with_pitfalls(seed):
    """틀별 실수거리는 tools/pitfalls.py 등록부에서 가져온다 (재생성해도 유지)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("pitfalls", os.path.join(HERE, "pitfalls.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    for t in seed["templates"]:
        if t["id"] in mod.P:
            t["pitfalls"] = mod.P[t["id"]]
    return seed


if __name__ == "__main__":
    for seed in (RIVER_SEED, MTN_SEED):
        _with_pitfalls(seed)
        path = os.path.join(SEEDS, seed["seed_id"] + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(seed, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print("→", os.path.relpath(path))
