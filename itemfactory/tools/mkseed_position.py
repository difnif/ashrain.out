# itemfactory/tools/mkseed_position.py — 위치관계(m1-2) 시드 생성기 (v1.0)
#
#   python itemfactory/tools/mkseed_position.py      → itemfactory/seeds/m1-2-position-relation.json
#
# 모서리·면의 위치 관계는 문자열 파라미터라 식으로 파생할 수 없다. 그래서 직육면체·삼각기둥의
# 꼭짓점 좌표에서 관계를 **계산해 표(table)로 굽는다** — 시드 JSON 안의 표가 곧 정답 근거이고,
# recheck.py 는 같은 계산을 독립적으로 다시 해서 대조한다.
#
# 이름 규약 (figsvg.js fnWire 와 동일)
#   box      : 윗면 A B C D (앞왼→앞오→뒤오→뒤왼) · 밑면 E F G H — 모서리 AB BC CD DA EF FG GH HE AE BF CG DH
#   triprism : 윗면 A B C (앞왼→앞오→뒤) · 밑면 D E F          — 모서리 AB BC CA DE EF FD AD BE CF
from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "seeds", "m1-2-position-relation.json")

# ---------------------------------------------------------------- 입체 모델
BOX = {
    "pts": {"A": (0, 2, 0), "B": (3, 2, 0), "C": (3, 2, 2), "D": (0, 2, 2),
            "E": (0, 0, 0), "F": (3, 0, 0), "G": (3, 0, 2), "H": (0, 0, 2)},
    "edges": ["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"],
    "faces": ["ABCD", "EFGH", "ABFE", "BCGF", "CDHG", "ADHE"],
}
TRI = {
    "pts": {"A": (0, 2, 0), "B": (3, 2, 0), "C": (1.5, 2, 2), "D": (0, 0, 0), "E": (3, 0, 0), "F": (1.5, 0, 2)},
    "edges": ["AB", "BC", "CA", "DE", "EF", "FD", "AD", "BE", "CF"],
    "faces": ["ABC", "DEF", "ABED", "BCFE", "ACFD"],
}


def sub(p, q):
    return tuple(a - b for a, b in zip(p, q))


def cross(u, v):
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


def dot(u, v):
    return sum(a * b for a, b in zip(u, v))


def is_zero(v):
    return all(abs(x) < 1e-9 for x in v)


def edge_dir(S, e):
    return sub(S["pts"][e[1]], S["pts"][e[0]])


def edge_rel(S, e, f):
    """e 에 대한 f 의 관계: meet | par | skew"""
    if set(e) & set(f):
        return "meet"
    if is_zero(cross(edge_dir(S, e), edge_dir(S, f))):
        return "par"
    return "skew"


def face_normal(S, F):
    p = [S["pts"][c] for c in F[:3]]
    return cross(sub(p[1], p[0]), sub(p[2], p[0]))


def edge_face_rel(S, F, e):
    """면 F 에 대한 모서리 e: inc(포함) | perp(수직) | par(평행)"""
    if set(e) <= set(F):
        return "inc"
    n = face_normal(S, F)
    d = edge_dir(S, e)
    if is_zero(cross(n, d)):            # 방향이 법선과 평행 → 면과 수직 (직기둥이라 반드시 한 점에서 만난다)
        return "perp"
    if abs(dot(n, d)) < 1e-9 and not (set(e) & set(F)):
        return "par"
    return "meet"                        # 직육면체·직삼각기둥에서는 나오지 않음


def lst(xs):
    return ", ".join(xs)


REL_EDGE = {"par": "평행한", "meet": "한 점에서 만나는", "skew": "꼬인 위치에 있는"}
REL_FACE = {"par": ("에 평행한", "평행"), "perp": ("와 수직인", "수직")}
_LATIN_JONG = set("LMNR")        # expr.py 와 같은 규칙 — 엘·엠·엔·알만 받침


def wa_of(name):
    return "과" if name[-1].upper() in _LATIN_JONG else "와"


def groups(S, e):
    g = {"par": [], "meet": [], "skew": []}
    for f in S["edges"]:
        if f != e:
            g[edge_rel(S, e, f)].append(f)
    return g


def face_groups(S, F):
    g = {"inc": [], "perp": [], "par": []}
    for e in S["edges"]:
        g[edge_face_rel(S, F, e)].append(e)
    return g


def rot(xs, k):
    k %= len(xs)
    return xs[k:] + xs[:k]


# ---------------------------------------------------------------- 표 굽기
def t1_rows():
    """직육면체 · 모서리 e 와 꼬인 위치 모서리 고르기 — 키 e|t|v"""
    rows = {}
    for e in BOX["edges"]:
        g = groups(BOX, e)
        for t in g["skew"]:
            for v in range(3):
                pars = rot(g["par"], v)[:2]
                meets = rot(g["meet"], v)[:2]
                rows[f"{e}|{t}|{v}"] = {
                    "e": e, "t": t, "e0": e[0], "e1": e[1],
                    "par": lst(g["par"]), "meet": lst(g["meet"]), "skew": lst(g["skew"]),
                    "d1": pars[0], "d2": pars[1], "d3": meets[0], "d4": meets[1],
                }
    return rows


def t2_rows(S, edges):
    """모서리 e 와 rel 관계 모서리 개수 — 키 e|rel"""
    rows = {}
    for e in edges:
        g = groups(S, e)
        for rel, name in REL_EDGE.items():
            rows[f"{e}|{rel}"] = {
                "e": e, "e0": e[0], "e1": e[1], "rel": name, "lst": lst(g[rel]), "n": len(g[rel]),
                "par": lst(g["par"]), "meet": lst(g["meet"]), "skew": lst(g["skew"]),
                "n_par": len(g["par"]), "n_meet": len(g["meet"]), "n_skew": len(g["skew"]),
            }
    return rows


def t3_rows():
    """직육면체 · 면 F 와 rel 관계 모서리 고르기 — 키 F|rel|t|v"""
    rows = {}
    for F in BOX["faces"]:
        g = face_groups(BOX, F)
        for rel, (relq, relw) in REL_FACE.items():
            other = "perp" if rel == "par" else "par"
            for t in g[rel]:
                for v in range(2):
                    inc = rot(g["inc"], v)[:2]
                    oth = rot(g[other], v)[:2]
                    rows[f"{F}|{rel}|{t}|{v}"] = {
                        "F": F, "t": t, "relq": relq.replace("와", wa_of(F)) if rel == "perp" else relq, "relw": relw,
                        "inc": lst(g["inc"]), "perp": lst(g["perp"]), "parf": lst(g["par"]), "lst": lst(g[rel]),
                        "d1": inc[0], "d2": inc[1], "d3": oth[0], "d4": oth[1],
                        "otherw": "수직" if other == "perp" else "평행",
                    }
    return rows


# ---------------------------------------------------------------- 공용 조각
BOX_FIG = [{"fn": "wire", "args": {"kind": "box", "names": "ABCDEFGH"}}]
TRI_FIG = [{"fn": "wire", "args": {"kind": "triprism", "names": "ABCDEF"}}]

SOL1_EDGE = (
    "공간에서 두 직선의 위치 관계는 세 가지뿐이다. ① 한 점에서 만난다 ② 평행하다(만나지 않지만 한 평면 위에 놓인다) "
    "③ 꼬인 위치에 있다(만나지도 않고 평행하지도 않다 — 한 평면 위에 놓을 수 없다). "
    "그림에서 기준 모서리 {e}를 잡고 나머지 모서리를 세 묶음으로 나눈다. {e}와 꼭짓점 {e0} 또는 {e1}을 함께 쓰는 모서리는 '만난다', "
    "{e}와 같은 방향으로 놓인 모서리는 '평행', 그 둘 어디에도 들지 않는 모서리가 '꼬인 위치'다. "
    "평면에서는 만나지 않으면 평행이지만, 공간에서는 만나지 않아도 평행이 아닐 수 있다는 점이 핵심이다."
)
def with_keys(rows, fields):
    """표 행에 par1..par4 같은 큐 키 칼럼을 붙인다 (edge:XX / 빈 문자열)."""
    for r in rows.values():
        for f in fields:
            names = [x for x in r[f].split(", ") if x]
            for i in range(1, 5):
                r[f"{f}{i}"] = f"edge:{names[i - 1]}" if i <= len(names) else ""
    return rows


SOL2_EDGE_STEPS = [
    "기준 모서리 {e}를 표시한다. {e}는 꼭짓점 {e0}과 {e1}을 잇는 모서리다.",
    "{e}와 꼭짓점을 함께 쓰는 모서리 {meet}는 {e}와 한 점에서 만난다.",
    "{e}와 같은 방향으로 놓인 모서리 {par}는 {e}와 평행하다.",
    None,   # 마지막 줄은 틀마다 다르다
]
SOL2_EDGE_ANIM = [
    [{"act": "hl", "k": "edge:{e}", "keep": True}],
    [{"act": "hl", "k": ["{meet1}", "{meet2}", "{meet3}", "{meet4}"]}],
    [{"act": "hl", "k": ["{par1}", "{par2}", "{par3}", "{par4}"]}],
    [{"act": "hl", "k": ["{skew1}", "{skew2}", "{skew3}", "{skew4}"]}],
]

COMMON = {
    "prereq": ["평면에서 두 직선의 위치 관계", "직육면체의 꼭짓점·모서리·면"],
    "process": "개념이해",
    "context": "기하맥락",
    "ops": [],
    "time_limit": 90,
    "points": 5,
}


def tpl_t1():
    rows = with_keys(t1_rows(), ["par", "meet", "skew"])
    return {
        **COMMON,
        "id": "m1-2-position-t1", "title": "직육면체 — 꼬인 위치에 있는 모서리 고르기",
        "skill": "기준 모서리와 만나는 것·평행한 것을 걷어내고 남는 것이 꼬인 위치임을 안다",
        "traps": ["구하는대상혼동"],
        "variant_axis": {"입체": "직육면체", "관계": "꼬인 위치", "형식": "보기 고르기"},
        "discriminates": "만나지 않는 모서리를 전부 평행으로 보는가 (공간과 평면의 차이)",
        "qtype": "choice", "difficulty": 2, "pool_target": 300,
        "tags": ["위치관계", "꼬인위치", "직육면체"],
        "params": [{"name": "c", "values": {"in": sorted(rows)}}],
        "table": {"key": "c", "rows": rows},
        "cost_values": ["1"],
        "math_key_values": ["e", "t"],
        "verify": ["t in skew", "not (t in par)", "not (t in meet)"],
        "question": "다음 그림과 같은 직육면체에서 모서리 {e}와 꼬인 위치에 있는 모서리는?",
        "figure": BOX_FIG,
        "answer": "{t}",
        "answer_alt": ["모서리 {t}"],
        "distractors": [
            {"expr": "d1", "misconception": "MC-POS-01"},
            {"expr": "d2", "misconception": "MC-POS-01"},
            {"expr": "d3", "misconception": "MC-POS-02"},
            {"expr": "d4", "misconception": "MC-POS-02"},
        ],
        "sol1": SOL1_EDGE,
        "sol1_fig": BOX_FIG,
        "sol1_anim": SOL2_EDGE_ANIM,
        "sol2": SOL2_EDGE_STEPS[:3] + [
            "나머지 모서리 {skew}는 {e}와 만나지도 않고 평행하지도 않으므로 꼬인 위치에 있다. 보기 가운데 여기에 드는 것은 {t}이다."
        ],
        "sol2_fig": BOX_FIG,
        "sol2_anim": SOL2_EDGE_ANIM[:3] + [[{"act": "hl", "k": ["{skew1}", "{skew2}", "{skew3}", "{skew4}"]}, {"act": "pulse", "k": "edge:{t}", "keep": True}]],
        "sol_check": "{e}와 {t}를 함께 담는 면이 하나도 없음을 그림에서 확인한다 — 한 평면 위에 놓을 수 없으니 꼬인 위치가 맞다. 답은 {t}다.",
        "model_answer": "모서리 {e}와 한 점에서 만나는 모서리는 {meet}이고, 평행한 모서리는 {par}이다. 나머지 모서리 {skew}는 {e}와 만나지도 않고 평행하지도 않으므로 꼬인 위치에 있다. 따라서 답은 {t}이다.",
        "rubric": [
            {"element": "만나는 모서리 가려내기", "points": 3, "criterion": "{e}와 꼭짓점을 공유하는 모서리({meet})를 만나는 것으로 분류했다."},
            {"element": "평행한 모서리 가려내기", "points": 3, "criterion": "{e}와 방향이 같은 모서리({par})를 평행으로 분류했다.", "partial": "일부만 찾았으면 1점."},
            {"element": "꼬인 위치 판정·답", "points": 4, "criterion": "만나지도 평행하지도 않은 모서리가 꼬인 위치임을 근거로 {t}를 골랐다."},
        ],
    }


def tpl_t2():
    rows = with_keys(t2_rows(BOX, BOX["edges"]), ["par", "meet", "skew"])
    return {
        **COMMON,
        "id": "m1-2-position-t2", "title": "직육면체 — 모서리와의 관계별 개수",
        "skill": "기준 모서리에 대해 12개 모서리를 만남·평행·꼬인 위치로 빠짐없이 분류한다",
        "traps": ["조건누락", "구하는대상혼동"],
        "variant_axis": {"입체": "직육면체", "관계": "평행·만남·꼬인 위치 순환", "형식": "개수"},
        "discriminates": "세 관계로 분류가 빠짐없이 되는가 (합이 11인가)",
        "qtype": "short", "difficulty": 2, "pool_target": 300,
        "tags": ["위치관계", "직육면체", "개수"],
        "params": [{"name": "c", "values": {"in": sorted(rows)}}],
        "table": {"key": "c", "rows": rows},
        "cost_values": ["n"],
        "math_key_values": ["e", "rel", "n"],
        "verify": ["ans == n", "n_par + n_meet + n_skew == 11"],
        "question": "다음 그림과 같은 직육면체에서 모서리 {e}와 {rel} 모서리는 모두 몇 개인지 구하시오.",
        "figure": BOX_FIG,
        "answer": "{n}",
        "answer_alt": ["{n}개"],
        "sol1": SOL1_EDGE,
        "sol1_fig": BOX_FIG,
        "sol1_anim": SOL2_EDGE_ANIM,
        "sol2": SOL2_EDGE_STEPS[:3] + [
            "나머지 모서리 {skew}는 만나지도 평행하지도 않으므로 꼬인 위치에 있다. 따라서 {e}와 {rel} 모서리는 {lst}로 모두 {n}개다."
        ],
        "sol2_fig": BOX_FIG,
        "sol2_anim": SOL2_EDGE_ANIM,
        "sol_check": "만나는 것 {n_meet}개, 평행한 것 {n_par}개, 꼬인 위치 {n_skew}개를 더하면 11개로, 기준 모서리를 뺀 전체 모서리 수와 같다. 빠뜨린 모서리가 없으니 답은 {n}개다.",
        "model_answer": "모서리 {e}와 한 점에서 만나는 모서리는 {meet}의 {n_meet}개, 평행한 모서리는 {par}의 {n_par}개이다. 나머지 {skew}의 {n_skew}개는 만나지도 평행하지도 않으므로 꼬인 위치에 있다. 따라서 {e}와 {rel} 모서리는 {n}개이다.",
        "rubric": [
            {"element": "세 관계로 분류", "points": 4, "criterion": "만남·평행·꼬인 위치의 세 묶음으로 모서리를 나누었다."},
            {"element": "빠짐없이 세기", "points": 3, "criterion": "{rel} 모서리 {lst}를 모두 찾았다.", "partial": "하나 빠뜨리면 1점."},
            {"element": "답", "points": 3, "criterion": "{n}개로 답했다."},
        ],
    }


def tpl_t3():
    rows = with_keys(t3_rows(), ["inc", "perp", "parf"])
    return {
        **COMMON,
        "id": "m1-2-position-t3", "title": "직육면체 — 면과 평행한/수직인 모서리 고르기",
        "skill": "면에 포함된 모서리·면과 한 점에서 만나는(수직) 모서리·평행한 모서리를 구별한다",
        "prereq": ["직선과 평면의 위치 관계", "직육면체의 꼭짓점·모서리·면"],
        "traps": ["구하는대상혼동"],
        "variant_axis": {"입체": "직육면체", "관계": "면–모서리 평행·수직", "형식": "보기 고르기"},
        "discriminates": "면에 포함된 모서리를 평행으로 잘못 보는가, 수직과 평행을 바꿔 읽는가",
        "qtype": "choice", "difficulty": 3, "pool_target": 300,
        "tags": ["위치관계", "직육면체", "면과모서리"],
        "params": [{"name": "c", "values": {"in": sorted(rows)}}],
        "table": {"key": "c", "rows": rows},
        "cost_values": ["1"],
        "math_key_values": ["F", "relw", "t"],
        "verify": ["t in lst", "not (t in inc)"],
        "question": "다음 그림과 같은 직육면체에서 면 {F}{relq} 모서리는?",
        "figure": BOX_FIG,
        "answer": "{t}",
        "answer_alt": ["모서리 {t}"],
        "distractors": [
            {"expr": "d1", "misconception": "MC-POS-03"},
            {"expr": "d2", "misconception": "MC-POS-03"},
            {"expr": "d3", "misconception": "MC-POS-04"},
            {"expr": "d4", "misconception": "MC-POS-04"},
        ],
        "sol1": (
            "직선과 평면의 위치 관계는 ① 직선이 평면에 포함된다 ② 한 점에서 만난다 ③ 평행하다(만나지 않는다)의 세 가지다. "
            "직육면체에서 면 {F}를 기준으로 보면, 면의 테두리를 이루는 모서리 {inc}는 면에 '포함'되고, 면과 한 점에서 만나는 모서리 {perp}는 "
            "그 점에서 면 위의 두 모서리와 모두 수직이므로 면과 '수직'이다. 남은 모서리 {parf}는 마주보는 면 위에 있어 면 {F}와 '평행'하다. "
            "면 위에 놓인 모서리를 평행으로 세지 않는 것이 핵심이다."
        ),
        "sol1_fig": BOX_FIG,
        "sol1_anim": [
            [{"act": "hl", "k": "face:{F}", "keep": True}],
            [{"act": "hl", "k": ["{inc1}", "{inc2}", "{inc3}", "{inc4}"]}],
            [{"act": "hl", "k": ["{perp1}", "{perp2}", "{perp3}", "{perp4}"]}],
            [{"act": "hl", "k": ["{parf1}", "{parf2}", "{parf3}", "{parf4}"]}],
        ],
        "sol2": [
            "기준이 되는 면 {F}를 표시한다.",
            "면 {F}의 테두리를 이루는 모서리 {inc}는 면에 포함된다 — 평행도 수직도 아니다.",
            "면 {F}와 한 점에서 만나는 모서리 {perp}는 직육면체이므로 면과 수직이다.",
            "면 {F}와 만나지 않는 모서리 {parf}는 마주보는 면 위에 있으므로 면과 평행하다. 따라서 면 {F}{relq} 모서리는 {lst}이고, 보기 가운데 {t}이다.",
        ],
        "sol2_fig": BOX_FIG,
        "sol2_anim": [
            [{"act": "hl", "k": "face:{F}", "keep": True}],
            [{"act": "hl", "k": ["{inc1}", "{inc2}", "{inc3}", "{inc4}"]}],
            [{"act": "hl", "k": ["{perp1}", "{perp2}", "{perp3}", "{perp4}"]}],
            [{"act": "hl", "k": ["{parf1}", "{parf2}", "{parf3}", "{parf4}"]}, {"act": "pulse", "k": "edge:{t}", "keep": True}],
        ],
        "sol_check": "면 {F}{relq} 모서리 {lst} 가운데 {t}가 있고, {t}는 면 {F}의 테두리({inc})에 들지 않으며 {otherw}인 모서리 묶음에도 없다. 답은 {t}다.",
        "model_answer": "면 {F}에 포함된 모서리는 {inc}, 면 {F}와 수직인 모서리는 {perp}, 면 {F}에 평행한 모서리는 {parf}이다. 따라서 면 {F}{relq} 모서리는 {lst}이고, 보기 가운데 {t}이다.",
        "rubric": [
            {"element": "포함된 모서리 구별", "points": 3, "criterion": "면 {F} 위의 모서리({inc})를 포함으로 분류했다."},
            {"element": "수직·평행 구별", "points": 4, "criterion": "면과 한 점에서 만나는 모서리는 수직, 만나지 않는 모서리는 평행으로 나누었다.", "partial": "한쪽만 맞으면 2점."},
            {"element": "답", "points": 3, "criterion": "{relw} 모서리 가운데 {t}를 골랐다."},
        ],
    }


def tpl_t4():
    rows = with_keys(t2_rows(TRI, TRI["edges"]), ["par", "meet", "skew"])
    return {
        **COMMON,
        "id": "m1-2-position-t4", "title": "삼각기둥 — 모서리와의 관계별 개수",
        "skill": "직육면체가 아닌 기둥에서도 만남·평행·꼬인 위치를 빠짐없이 분류한다",
        "prereq": ["공간에서 두 직선의 위치 관계", "삼각기둥의 꼭짓점·모서리·면"],
        "traps": ["조건누락", "구하는대상혼동"],
        "variant_axis": {"입체": "삼각기둥", "관계": "평행·만남·꼬인 위치 순환", "형식": "개수"},
        "discriminates": "옆모서리와 밑면 모서리에 따라 평행·꼬인 위치의 개수가 달라짐을 아는가",
        "qtype": "short", "difficulty": 3, "pool_target": 300,
        "tags": ["위치관계", "삼각기둥", "개수"],
        "params": [{"name": "c", "values": {"in": sorted(rows)}}],
        "table": {"key": "c", "rows": rows},
        "cost_values": ["n"],
        "math_key_values": ["e", "rel", "n"],
        "verify": ["ans == n", "n_par + n_meet + n_skew == 8"],
        "question": "다음 그림과 같은 삼각기둥에서 모서리 {e}와 {rel} 모서리는 모두 몇 개인지 구하시오.",
        "figure": TRI_FIG,
        "answer": "{n}",
        "answer_alt": ["{n}개"],
        "sol1": SOL1_EDGE.replace("그림에서 기준 모서리", "삼각기둥은 모서리가 9개다. 그림에서 기준 모서리"),
        "sol1_fig": TRI_FIG,
        "sol1_anim": SOL2_EDGE_ANIM,
        "sol2": SOL2_EDGE_STEPS[:3] + [
            "나머지 모서리 {skew}는 만나지도 평행하지도 않으므로 꼬인 위치에 있다. 따라서 {e}와 {rel} 모서리는 {lst}로 모두 {n}개다."
        ],
        "sol2_fig": TRI_FIG,
        "sol2_anim": SOL2_EDGE_ANIM,
        "sol_check": "만나는 것 {n_meet}개, 평행한 것 {n_par}개, 꼬인 위치 {n_skew}개를 더하면 8개로, 기준 모서리를 뺀 전체 모서리 수와 같다. 답은 {n}개다.",
        "model_answer": "모서리 {e}와 한 점에서 만나는 모서리는 {meet}의 {n_meet}개, 평행한 모서리는 {par}의 {n_par}개이다. 나머지 {skew}의 {n_skew}개는 꼬인 위치에 있다. 따라서 {e}와 {rel} 모서리는 {n}개이다.",
        "rubric": [
            {"element": "세 관계로 분류", "points": 4, "criterion": "만남·평행·꼬인 위치의 세 묶음으로 모서리를 나누었다."},
            {"element": "빠짐없이 세기", "points": 3, "criterion": "{rel} 모서리 {lst}를 모두 찾았다.", "partial": "하나 빠뜨리면 1점."},
            {"element": "답", "points": 3, "criterion": "{n}개로 답했다."},
        ],
    }


# ---------------------------------------------------------------- 조사 자동화
# 문자열 파라미터(모서리·면 이름, 목록) 뒤의 조사는 소리에 따라 달라진다(AB와 / EF과, CD는 / FG은).
# 시드 텍스트는 편의상 "…{e}와 …" 로 쓰고, 여기서 {e}{wa(e)} 꼴로 바꿔 둔다 (expr.py 의 조사 함수가 영문자 끝소리를 안다).
_STR_VARS = "e|t|e0|e1|F|meet|par|skew|inc|perp|parf|lst"
_JOSA = [("이다", "ida"), ("으로", "ro"), ("와", "wa"), ("과", "wa"), ("는", "eun"), ("은", "eun"),
         ("를", "eul"), ("을", "eul"), ("가", "ika"), ("이", "ika"), ("로", "ro"), ("다", "ida")]
_JOSA_RE = re.compile(r"\{(" + _STR_VARS + r")\}(이다|으로|와|과|는|은|를|을|가|이|로|다)(?=[\s.,!?)]|$)")


def fix_josa(obj):
    if isinstance(obj, str):
        return _JOSA_RE.sub(lambda m: "{%s}{%s(%s)}" % (m.group(1), dict(_JOSA)[m.group(2)], m.group(1)), obj)
    if isinstance(obj, list):
        return [fix_josa(x) for x in obj]
    if isinstance(obj, dict):
        return {k: (v if k in ("table", "params", "figure", "sol1_fig", "sol2_fig") else fix_josa(v)) for k, v in obj.items()}
    return obj


SEED = {
    "seed_id": "m1-2-position-relation",
    "category": "도형",
    "title": "공간에서의 위치 관계 — 직육면체·삼각기둥의 모서리와 면",
    "unit_id": "m1-2",
    "concept_ids": ["m1-2-03"],
    "schema_id": None,
    "schema_name": "공간에서 두 직선·직선과 평면의 위치 관계",
    "source_item_ids": [],
    "note": "표(table) 기반 시드. 관계는 tools/mkseed_position.py 가 꼭짓점 좌표에서 계산해 굽고, recheck.py 가 독립 재계산으로 대조한다. "
            "그림은 wire(입체 골격) — 전부 한 번에 그리고 애니메이션은 모서리·면을 색으로만 강조한다.",
    "geometry": True,
    "templates": [fix_josa(tpl_t1()), fix_josa(tpl_t2()), fix_josa(tpl_t3()), fix_josa(tpl_t4())],
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
    _with_pitfalls(SEED)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(SEED, f, ensure_ascii=False, indent=1)
    for t in SEED["templates"]:
        print(t["id"], "rows =", len(t["table"]["rows"]))
    print("→", os.path.relpath(OUT))
