# itemfactory/tools/mkseed_m3_circle.py — m3-2 원의 성질 시드 생성기 (v1.0 · 2026-09-13 세션 5)
#
#   python itemfactory/tools/mkseed_m3_circle.py
#     → seeds/m3-2-circle-chord-tangent.json (원의 현·접선: 현의 수직이등분선·접선의 길이·두 접선의 각·삼각형 내접원·외접사각형, 5틀)
#     → seeds/m3-2-circle-angle.json         (원주각: 원주각과 중심각·반원의 원주각·내접사각형·접선과 현·원주각과 호, 5틀)
#
# 원은 scene circles(r 고정 3, 길이는 표에서 3/r 배로 축소) 또는 표에 미리 계산한 내접원 반지름. 각은 derive 의 sin·cos 로 실제 크기.
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mkseed_m2_geo1 import arc, scene  # noqa: E402
from mkseed_m2_geo2 import lseg  # noqa: E402
from seedlib import dump, hl, reveal, steps, with_pitfalls  # noqa: E402


def tpl(seed_id, no, base, **kw):
    t = dict(base)
    t.update(kw)
    t["id"] = f"{seed_id}-t{no}"
    return t


def geo(t: dict) -> dict:
    if t.get("figure"):
        t["geometry"] = True
        if "sol3" in t:
            t["sol_check"] = t.pop("sol3")
        t.pop("sol3_fig", None)
        t.pop("sol3_anim", None)
    else:
        t["geometry"] = False
    return t


def R(v):
    return round(v, 4)


GEO = {"process": "추론", "context": "기하맥락", "points": 4, "time_limit": 90, "qtype": "short", "pool_target": 300, "traps": ["구하는대상혼동"]}
CIRC = [{"c": "O", "r": 3}]

# ═══════════════════════════════════════════════════════════════════ 1. 원의 현과 접선
CT = "m3-2-circle-chord-tangent"
CT_BASE = {**GEO, "prereq": ["피타고라스 정리", "원의 현의 수직이등분선"], "ops": ["원의 성질"], "tags": ["원의 현", "원의 접선"]}
TRI = [(4, 3, 5), (3, 4, 5), (12, 5, 13), (5, 12, 13), (8, 6, 10), (6, 8, 10), (15, 8, 17), (8, 15, 17), (24, 7, 25), (7, 24, 25), (12, 9, 15), (9, 12, 15), (16, 12, 20), (12, 16, 20), (24, 10, 26), (10, 24, 26),
       (20, 21, 29), (21, 20, 29), (9, 40, 41), (40, 9, 41), (12, 35, 37), (35, 12, 37), (28, 21, 35), (21, 28, 35), (15, 20, 25), (20, 15, 25), (18, 24, 30), (24, 18, 30), (30, 16, 34), (16, 30, 34), (36, 15, 39), (15, 36, 39), (40, 30, 50), (30, 40, 50), (32, 24, 40), (24, 32, 40)]


# t1 — 현의 수직이등분선: OM ⊥ AB, AM = MB. (h, d, r)
def _ct1_rows():
    out = {}
    for h, d, r in TRI:
        sc = 3 / r
        base = {"h": h, "d": d, "r": r, "ab": 2 * h, "mx": R(h * sc), "my": R(d * sc)}
        out[f"ab-{h}-{d}"] = {**base, "GIVEN": f"원 O의 반지름의 길이가 {r}, [[seg(OM)]] = {d}", "ASKT": "[[seg(AB)]]", "ans": 2 * h, "LR": r, "LD": d, "LAB": "",
                              "STEP": f"AM = [[sqrt(pow({r},2) − pow({d},2))]] = [[sqrt({h * h})]] = {h}", "FIN": f"AB = 2 × AM = 2 × {h} = {2 * h}", "REL": "OA² = OM² + AM²에서 AM"}
        out[f"r-{h}-{d}"] = {**base, "GIVEN": f"[[seg(AB)]] = {2 * h}, [[seg(OM)]] = {d}", "ASKT": "원 O의 반지름", "ans": r, "LR": "", "LD": d, "LAB": 2 * h,
                             "STEP": f"AM = [[frac(1, 2)]] × AB = {h}", "FIN": f"OA = [[sqrt(pow({d},2) + pow({h},2))]] = [[sqrt({r * r})]] = {r}", "REL": "OA² = OM² + AM²에서 OA"}
        out[f"d-{h}-{d}"] = {**base, "GIVEN": f"원 O의 반지름의 길이가 {r}, [[seg(AB)]] = {2 * h}", "ASKT": "[[seg(OM)]]", "ans": d, "LR": r, "LD": "", "LAB": 2 * h,
                             "STEP": f"AM = [[frac(1, 2)]] × AB = {h}", "FIN": f"OM = [[sqrt(pow({r},2) − pow({h},2))]] = [[sqrt({d * d})]] = {d}", "REL": "OA² = OM² + AM²에서 OM"}
    return out


CT1_ROWS = _ct1_rows()
CT1_PTS = {"O": [0, 0], "M": [0, "{my}"], "A": ["{-mx}", "{my}"], "B": ["{mx}", "{my}"]}
CT1_SEGS = [lseg("A", "B", "{LAB}"), lseg("O", "M", "{LD}"), lseg("O", "A", "{LR}", dash=True)]


def ct_t1():
    return tpl(CT, 1, CT_BASE,
        title="현의 수직이등분선 — 반지름·현의 길이·중심에서 현까지의 거리",
        skill="원의 중심에서 현에 내린 수선은 현을 이등분함을 쓰고 직각삼각형 OAM에 피타고라스 정리 적용하기",
        variant_axis={"(AM, OM, OA)": "피타고라스 수 36쌍", "구하는 것": "현 / 반지름 / 거리"},
        difficulty=2,
        discriminates="AM = ½AB(이등분)를 쓰고 빗변이 반지름 OA임을 지키는가, 현의 길이는 AM의 2배로 답하는가",
        params=[{"name": "f", "values": {"in": list(CT1_ROWS)}}],
        table={"key": "f", "rows": CT1_ROWS},
        cost_values=["h", "d", "r", "ans"],
        answer_var="ans",
        verify=["h*h + d*d == r*r"],
        question="다음 그림의 원 O에서 [[seg(OM)]] ⊥ [[seg(AB)]]이고 {GIVEN}일 때, {ASKT}의 길이를 구하시오.",
        figure=scene(CT1_PTS, CT1_SEGS, circles=CIRC, marks={"right": [["A", "M", "O"]], "eq": [[["A", "M"], ["M", "B"]]]}),
        answer="{ans}", answer_alt=[],
        sol1="원의 중심에서 현에 내린 수선은 그 현을 이등분하므로 M은 AB의 중점이고 AM = MB이다. 직각삼각형 OAM에서 빗변은 반지름 OA이므로 OA² = OM² + AM²이 성립한다. 아는 두 길이로 {REL}{eul(REL)} 구한다.",
        sol1_fig=scene(CT1_PTS, [lseg("A", "B", "{LAB}"), lseg("O", "M", "{d}"), lseg("O", "A", "{r}"), lseg("A", "M", "{h}", dash=True)], circles=CIRC, marks={"right": [["A", "M", "O"]], "eq": [[["A", "M"], ["M", "B"]]]}, shade=[["O", "A", "M"]]),
        sol1_anim=[[hl("eq:A-M", "eq:M-B", keep=True)], [hl("shade:0", "seg:O-A", keep=True)], [hl("seglbl:A-M")]],
        sol2=[
            "OM ⊥ AB이므로 AM = MB",
            "{STEP}",
            "{FIN}",
        ],
        sol2_fig=steps([
            {"text": "AM = MB", "hint": "중심에서 현에 내린 수선"},
            {"text": "{STEP}", "hint": "직각삼각형 OAM", "marks": [{"on": "{h}", "note": "AM"}]},
            {"text": "{FIN}", "hint": "OA² = OM² + AM²"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2), hl("hint:2")]],
        sol3="AM = {h}, OM = {d}, OA = {r}는 {h}² + {d}² = {h*h} + {d*d} = {r*r} = {r}²으로 피타고라스 정리를 만족한다. 현 AB의 길이는 AM의 2배 {ab}이다. 따라서 답은 {ans}이다.",
        model_answer="OM ⊥ AB이므로 AM = MB이다. 직각삼각형 OAM에서 {STEP}이고 {FIN}이다. 따라서 {ASKT}의 길이는 {ans}이다.",
        rubric=[
            {"element": "이등분", "points": 2, "criterion": "OM ⊥ AB에서 AM = MB임을 썼다.", "partial": "AM = AB로 두었으면 인정하지 않는다."},
            {"element": "피타고라스·답", "points": 3, "criterion": "직각삼각형 OAM에서 {FIN}{eul(ans)} 구했다.", "partial": "AM만 구하고 현의 길이를 2배 하지 않았으면 1점."},
        ],
        rubric_total=5,
    )


# t2 — 접선의 길이: PA ⊥ OA. (PA, r, OP)
def _ct2_rows():
    out = {}
    for t, r, d in TRI:
        sc = 3 / r
        cph, sph = r / d, t / d
        base = {"t": t, "r": r, "d": d, "px": R(d * sc), "ax": R(3 * cph), "ay": R(3 * sph)}
        out[f"t-{t}-{r}"] = {**base, "GIVEN": f"원 O의 반지름의 길이가 {r}, [[seg(OP)]] = {d}", "ASKT": "[[seg(PA)]]", "ans": t, "LR": r, "LD": d, "LT": "",
                             "FIN": f"PA = [[sqrt(pow({d},2) − pow({r},2))]] = [[sqrt({t * t})]] = {t}"}
        out[f"r-{t}-{r}"] = {**base, "GIVEN": f"[[seg(PA)]] = {t}, [[seg(OP)]] = {d}", "ASKT": "원 O의 반지름", "ans": r, "LR": "", "LD": d, "LT": t,
                             "FIN": f"OA = [[sqrt(pow({d},2) − pow({t},2))]] = [[sqrt({r * r})]] = {r}"}
        out[f"d-{t}-{r}"] = {**base, "GIVEN": f"원 O의 반지름의 길이가 {r}, [[seg(PA)]] = {t}", "ASKT": "[[seg(OP)]]", "ans": d, "LR": r, "LD": "", "LT": t,
                             "FIN": f"OP = [[sqrt(pow({r},2) + pow({t},2))]] = [[sqrt({d * d})]] = {d}"}
    return out


CT2_ROWS = _ct2_rows()
CT2_PTS = {"O": [0, 0], "P": ["{px}", 0], "A": ["{ax}", "{ay}"]}
CT2_SEGS = [lseg("O", "A", "{LR}"), lseg("A", "P", "{LT}"), lseg("O", "P", "{LD}", dash=True)]


def ct_t2():
    return tpl(CT, 2, CT_BASE,
        title="원의 접선의 길이 — 접선 ⊥ 반지름과 피타고라스 정리",
        skill="접점에서 접선은 반지름에 수직임을 써서 직각삼각형 OAP에 피타고라스 정리 적용하기",
        variant_axis={"(PA, OA, OP)": "피타고라스 수 36쌍", "구하는 것": "접선의 길이 / 반지름 / OP"},
        difficulty=2,
        discriminates="∠OAP = 90°임을 알고 빗변이 OP(중심과 외부 점을 잇는 선분)임을 지키는가",
        params=[{"name": "f", "values": {"in": list(CT2_ROWS)}}],
        table={"key": "f", "rows": CT2_ROWS},
        cost_values=["t", "r", "d", "ans"],
        answer_var="ans",
        verify=["t*t + r*r == d*d"],
        question="다음 그림에서 [[seg(PA)]]는 점 P에서 원 O에 그은 접선이고 점 A는 접점이다. {GIVEN}일 때, {ASKT}의 길이를 구하시오.",
        figure=scene(CT2_PTS, CT2_SEGS, circles=CIRC, marks={"right": [["O", "A", "P"]]}),
        answer="{ans}", answer_alt=[],
        sol1="원의 접선은 접점을 지나는 반지름에 수직이다: OA ⊥ PA, 즉 ∠OAP = 90°. 따라서 △OAP는 빗변이 OP인 직각삼각형이고 OP² = OA² + PA²이 성립한다.",
        sol1_fig=scene(CT2_PTS, [lseg("O", "A", "{r}"), lseg("A", "P", "{t}"), lseg("O", "P", "{d}", dash=True)], circles=CIRC, marks={"right": [["O", "A", "P"]]}, shade=[["O", "A", "P"]]),
        sol1_anim=[[hl("right:A", keep=True)], [hl("shade:0", "seg:O-P")]],
        sol2=[
            "OA ⊥ PA이므로 ∠OAP = 90°",
            "OP² = OA² + PA²",
            "{FIN}",
        ],
        sol2_fig=steps([
            {"text": "∠OAP = 90°", "hint": "접선 ⊥ 반지름"},
            {"text": "OP² = OA² + PA²", "hint": "빗변은 OP"},
            {"text": "{FIN}", "marks": [{"on": "{ans}", "note": "{ASKT}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="PA = {t}, OA = {r}, OP = {d}는 {t}² + {r}² = {t*t} + {r*r} = {d*d} = {d}²으로 피타고라스 정리를 만족한다. 따라서 답은 {ans}이다.",
        model_answer="OA ⊥ PA이므로 직각삼각형 OAP에서 OP² = OA² + PA²이다. 따라서 {FIN}이다.",
        rubric=[
            {"element": "접선 ⊥ 반지름", "points": 2, "criterion": "∠OAP = 90°임을 썼다.", "partial": "근거 없이 직각삼각형이라고만 했으면 1점."},
            {"element": "피타고라스·답", "points": 3, "criterion": "{FIN}{eul(ans)} 구했다.", "partial": "빗변을 잘못 잡았으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t3 — 한 점에서 그은 두 접선: PA = PB, ∠APB + ∠AOB = 180°, ∠PAB = 90° − ∠APB/2
CT3_ROWS = {
    "APB-AOB": {"GQ": "APB", "XQ": "AOB", "GA": "P", "GF": "A", "GT": "B", "XA": "O", "XF": "A", "XT": "B", "isG": 1, "kind": 0,
                "LAW": "∠APB + ∠AOB = 180° (사각형 PAOB의 두 직각)", "STEP": "∠AOB = 180° − ∠APB"},
    "AOB-APB": {"GQ": "AOB", "XQ": "APB", "GA": "O", "GF": "A", "GT": "B", "XA": "P", "XF": "A", "XT": "B", "isG": 0, "kind": 0,
                "LAW": "∠APB + ∠AOB = 180° (사각형 PAOB의 두 직각)", "STEP": "∠APB = 180° − ∠AOB"},
    "APB-PAB": {"GQ": "APB", "XQ": "PAB", "GA": "P", "GF": "A", "GT": "B", "XA": "A", "XF": "P", "XT": "B", "isG": 1, "kind": 1,
                "LAW": "PA = PB이므로 △PAB는 이등변삼각형 — ∠PAB = ∠PBA", "STEP": "∠PAB = (180° − ∠APB) ÷ 2"},
}


def ct_t3():
    return tpl(CT, 3, CT_BASE,
        title="원 밖의 한 점에서 그은 두 접선 — ∠APB, ∠AOB, ∠PAB",
        skill="두 접선의 길이가 같음(PA = PB)과 접선 ⊥ 반지름을 써서 사각형 PAOB·이등변삼각형 PAB에서 각 구하기",
        variant_axis={"주어진 각": "∠APB / ∠AOB", "구하는 각": "∠AOB / ∠APB / ∠PAB", "∠APB": "20°~140° (짝수)"},
        difficulty=3,
        discriminates="∠OAP = ∠OBP = 90°에서 ∠APB + ∠AOB = 180°를 끌어내거나, PA = PB에서 밑각을 구하는가",
        params=[{"name": "v", "values": {"in": list(CT3_ROWS)}}, {"name": "a", "values": {"in": list(range(20, 142, 2))}}],
        table={"key": "v", "rows": CT3_ROWS},
        derive={"o": "180 - a", "half": "(180 - a)/2", "gv": "a*isG + (180 - a)*(1 - isG)", "ans": "(180 - a)*(1 - kind)*isG + a*(1 - isG) + (180 - a)/2*kind",
                "ph": "90 - a/2", "ax": "3*cos(pi*(90 - a/2)/180)", "ay": "3*sin(pi*(90 - a/2)/180)", "px": "3/cos(pi*(90 - a/2)/180)"},
        constraints=["ans != gv", "px <= 12"],
        cost_values=["a", "o", "ans"],
        answer_var="ans",
        verify=["o == 180 - a", "2*half == o"],
        question="다음 그림에서 두 점 A, B는 점 P에서 원 O에 그은 두 접선의 접점이다. [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene({"O": [0, 0], "P": ["{px}", 0], "A": ["{ax}", "{ay}"], "B": ["{ax}", "{-ay}"]}, [["P", "A"], ["P", "B"], ["O", "A"], ["O", "B"]], circles=CIRC,
                     marks={"arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}),
        answer="[[deg({ans})]]", answer_alt=["{ans}°", "{ans}"],
        sol1="접선은 접점에서 반지름과 수직이므로 ∠OAP = ∠OBP = 90°이다. 사각형 PAOB의 내각의 합이 360°이므로 ∠APB + ∠AOB = 180°이다. 또 한 점에서 그은 두 접선의 길이는 같으므로(PA = PB) △PAB는 이등변삼각형이고 두 밑각 ∠PAB = ∠PBA이다. {LAW}{eul(LAW)} 쓴다.",
        sol1_fig=scene({"O": [0, 0], "P": ["{px}", 0], "A": ["{ax}", "{ay}"], "B": ["{ax}", "{-ay}"]}, [["P", "A"], ["P", "B"], ["O", "A"], ["O", "B"], {"a": "A", "b": "B", "dash": True}], circles=CIRC,
                       marks={"right": [["O", "A", "P"], ["O", "B", "P"]], "eq": [[["P", "A"], ["P", "B"]]], "arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}),
        sol1_anim=[[hl("right:A", "right:B", keep=True)], [hl("eq:P-A", "eq:P-B", keep=True)], [hl("arc:ask")]],
        sol2=[
            "∠OAP = ∠OBP = 90° (접선 ⊥ 반지름), PA = PB (두 접선의 길이)",
            "{LAW}",
            "{STEP} = {ans}°",
        ],
        sol2_fig=steps([
            {"text": "∠OAP = ∠OBP = 90°, PA = PB", "hint": "접선의 성질"},
            {"text": "{LAW}", "hint": "각의 관계"},
            {"text": "{STEP} = {ans}°", "marks": [{"on": "{ans}°", "note": "∠{XQ}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="∠APB = {a}°, ∠AOB = {o}°이면 사각형 PAOB의 내각의 합 90° + 90° + {a}° + {o}° = 360°가 맞고, △PAB의 밑각은 각각 ({half})°로 두 밑각과 꼭지각의 합이 180°이다. 따라서 ∠{XQ} = {ans}이다.",
        model_answer="접선은 반지름에 수직이므로 ∠OAP = ∠OBP = 90°이고, PA = PB이다. {LAW}이므로 {STEP} = {ans}°이다.",
        rubric=[
            {"element": "접선의 성질", "points": 2, "criterion": "∠OAP = ∠OBP = 90° 또는 PA = PB를 근거로 밝혔다.", "partial": "근거 없이 각을 옮겼으면 1점."},
            {"element": "각 구하기", "points": 3, "criterion": "{STEP} = {ans}°를 구했다.", "partial": "다른 각을 답했으면 인정하지 않는다."},
        ],
        rubric_total=5,
    )


# t4 — 삼각형의 내접원과 접선의 길이: AD = AF = (b + c − a)/2 …
def _ct4_rows():
    out = {}
    for a in range(4, 13):                # BC
        for b in range(4, 13):            # CA
            for c in range(4, 13):        # AB
                if not (a < b + c and b < a + c and c < a + b) or (a + b + c) % 2 or min(abs(a - b), abs(b - c), abs(a - c)) < 2:
                    continue                                    # 접점이 변의 중점 근처면 변 라벨과 겹친다
                x, y, z = (b + c - a) // 2, (a + c - b) // 2, (a + b - c) // 2      # AD=AF, BD=BE, CE=CF
                xa = (c * c - b * b + a * a) / (2 * a); ya = math.sqrt(max(c * c - xa * xa, 0))
                s = a + b + c
                ix, iy = (a * xa + c * a) / s, (a * ya) / s
                area = a * ya / 2; ir = 2 * area / s
                D = (xa + (0 - xa) * x / c, ya + (0 - ya) * x / c)
                E = (y, 0)
                F = (a + (xa - a) * z / b, (ya) * z / b)
                base = {"a": a, "b": b, "c": c, "x": x, "y": y, "z": z, "xa": R(xa), "ya": R(ya), "ix": R(ix), "iy": R(iy), "ir": R(ir), "dx": R(D[0]), "dy": R(D[1]), "ex": R(E[0]), "fx": R(F[0]), "fy": R(F[1])}
                for ask, v, expl in (("AD", x, f"AD = AF = x라 하면 BD = BE = {c} − x, CE = CF = {b} − x이고 BE + CE = BC: ({c} − x) + ({b} − x) = {a}"),
                                     ("BE", y, f"BE = BD = y라 하면 AD = AF = {c} − y, CE = CF = {a} − y이고 AF + CF = CA: ({c} − y) + ({a} − y) = {b}"),
                                     ("CF", z, f"CF = CE = z라 하면 AF = AD = {b} − z, BE = BD = {a} − z이고 AD + BD = AB: ({b} − z) + ({a} − z) = {c}")):
                    if v in (a, b, c):
                        continue
                    out[f"{a}-{b}-{c}-{ask}"] = {**base, "ASK": ask, "ans": v, "EXPL": expl, "VAR": {"AD": "x", "BE": "y", "CF": "z"}[ask],
                                                 "EQ": {"AD": f"{b + c} − 2x = {a}", "BE": f"{a + c} − 2y = {b}", "CF": f"{a + b} − 2z = {c}"}[ask]}
    return out


CT4_ROWS = _ct4_rows()
CT4_PTS = {"A": ["{xa}", "{ya}"], "B": [0, 0], "C": ["{a}", 0], "O": ["{ix}", "{iy}"], "D": ["{dx}", "{dy}"], "E": ["{ex}", 0], "F": ["{fx}", "{fy}"]}
CT4_SEGS = [lseg("A", "B", "{c}"), lseg("B", "C", "{a}"), lseg("C", "A", "{b}")]


def ct_t4():
    return tpl(CT, 4, CT_BASE,
        title="삼각형의 내접원과 접선의 길이",
        skill="한 꼭짓점에서 두 접점까지의 길이가 같음을 써서 미지수 하나로 세 변을 표현하고 방정식 세우기",
        variant_axis={"세 변": "4~12 (둘레 짝수)", "구하는 것": "AD / BE / CF"},
        difficulty=3,
        discriminates="AD = AF, BD = BE, CE = CF 세 쌍을 모두 쓰고 한 변의 길이로 방정식을 세우는가",
        params=[{"name": "f", "values": {"in": list(CT4_ROWS)}}],
        table={"key": "f", "rows": CT4_ROWS},
        constraints=["ir >= 1", "ya >= 2.5"],
        cost_values=["a", "b", "c", "ans"],
        answer_var="ans",
        verify=["2*x == b + c - a", "2*y == a + c - b", "2*z == a + b - c"],
        question="다음 그림에서 원 O는 △ABC의 내접원이고 세 점 D, E, F는 접점이다. [[seg(AB)]] = {c}, [[seg(BC)]] = {a}, [[seg(CA)]] = {b}일 때, [[seg({ASK})]]의 길이를 구하시오.",
        figure=scene(CT4_PTS, CT4_SEGS, circles=[{"c": "O", "r": "{ir}"}]),
        answer="{ans}", answer_alt=[],
        sol1="원 밖의 한 점에서 원에 그은 두 접선의 길이는 같다. 꼭짓점 A에서는 AD = AF, B에서는 BD = BE, C에서는 CE = CF이다. {EXPL}에서 방정식을 세운다.",
        sol1_fig=scene(CT4_PTS, CT4_SEGS, circles=[{"c": "O", "r": "{ir}"}], marks={"eq": [[["A", "D"], ["A", "F"]], [["B", "D"], ["B", "E"]], [["C", "E"], ["C", "F"]]]}),
        sol1_anim=[[hl("eq:A-D", "eq:A-F", keep=True)], [hl("eq:B-D", "eq:B-E", keep=True)], [hl("eq:C-E", "eq:C-F")]],
        sol2=[
            "{EXPL}",
            "{EQ}",
            "{VAR} = {ans}, 즉 {ASK} = {ans}",
        ],
        sol2_fig=steps([
            {"text": "AD = AF, BD = BE, CE = CF", "hint": "두 접선의 길이"},
            {"text": "{EQ}", "hint": "한 변의 길이로 방정식", "marks": [{"on": "{EQ}", "note": "{ASK} = {VAR}"}]},
            {"text": "{ASK} = {ans}"},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")], [reveal(2)]],
        sol3="AD = AF = {x}, BD = BE = {y}, CE = CF = {z}로 놓으면 AB = {x} + {y} = {c}, BC = {y} + {z} = {a}, CA = {z} + {x} = {b}{ro(b)} 세 변이 모두 맞는다. 따라서 {ASK} = {ans}이다.",
        model_answer="{EXPL}이므로 {EQ}, {VAR} = {ans}이다. 따라서 {ASK} = {ans}이다.",
        rubric=[
            {"element": "접선의 길이 상등", "points": 2, "criterion": "AD = AF, BD = BE, CE = CF를 썼다.", "partial": "한 쌍만 썼으면 1점."},
            {"element": "방정식·답", "points": 3, "criterion": "{EQ}{eul(EQ)} 세워 {ASK} = {ans}{eul(ans)} 구했다.", "partial": "다른 접선의 길이를 답했으면 1점."},
        ],
        rubric_total=5,
    )


# t5 — 원에 외접하는 사각형: AB + CD = BC + DA
def _rho(ts):
    lo, hi = 0.01, 100.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if sum(math.atan(t / mid) for t in ts) > math.pi:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _ct5_rows():
    out = {}
    import itertools
    for tA, tB, tC, tD in itertools.product(range(1, 7), repeat=4):
        AB, BC, CD, DA = tA + tB, tB + tC, tC + tD, tD + tA
        if len({AB, BC, CD, DA}) < 3 or max(tA, tB, tC, tD) > 3 * min(tA, tB, tC, tD):
            continue
        rho = _rho((tA, tB, tC, tD))
        al = {n: math.atan(t / rho) for n, t in zip("ABCD", (tA, tB, tC, tD))}
        # T_AB 를 각 0 에 두고 반시계로 B, T_BC, C, T_CD, D, T_DA, A
        ang = 0.0
        P = {}
        for v in "BCDA":
            ang += al[v]
            P[v] = (R(rho / math.cos(al[v]) * math.cos(ang)), R(rho / math.cos(al[v]) * math.sin(ang)))
            ang += al[v]
        base = {"tA": tA, "tB": tB, "tC": tC, "tD": tD, "ab": AB, "bc": BC, "cd": CD, "da": DA, "rho": R(rho),
                "ax": P["A"][0], "ay": P["A"][1], "bx": P["B"][0], "by": P["B"][1], "cx": P["C"][0], "cy": P["C"][1], "dx": P["D"][0], "dy": P["D"][1]}
        sides = {"AB": AB, "BC": BC, "CD": CD, "DA": DA}
        for ask in sides:
            others = [k for k in sides if k != ask]
            given = ", ".join(f"[[seg({k})]] = {sides[k]}" for k in others)
            if ask in ("AB", "CD"):
                eq = f"AB + CD = BC + DA에서 {ask} + {sides['CD'] if ask == 'AB' else sides['AB']} = {BC} + {DA}"
                calc = f"{ask} = {BC + DA} − {sides['CD'] if ask == 'AB' else sides['AB']} = {sides[ask]}"
            else:
                eq = f"AB + CD = BC + DA에서 {AB} + {CD} = {ask} + {sides['DA'] if ask == 'BC' else sides['BC']}"
                calc = f"{ask} = {AB + CD} − {sides['DA'] if ask == 'BC' else sides['BC']} = {sides[ask]}"
            if sides[ask] in [sides[k] for k in others]:
                continue
            out[f"{tA}{tB}{tC}{tD}-{ask}"] = {**base, "ASK": ask, "GIVEN": given, "ans": sides[ask], "EQ": eq, "CALC": calc,
                                              "LAB": "" if ask == "AB" else AB, "LBC": "" if ask == "BC" else BC, "LCD": "" if ask == "CD" else CD, "LDA": "" if ask == "DA" else DA}
    return out


CT5_ROWS = _ct5_rows()
CT5_PTS = {"A": ["{ax}", "{ay}"], "B": ["{bx}", "{by}"], "C": ["{cx}", "{cy}"], "D": ["{dx}", "{dy}"], "O": [0, 0]}
CT5_SEGS = [lseg("A", "B", "{LAB}"), lseg("B", "C", "{LBC}"), lseg("C", "D", "{LCD}"), lseg("D", "A", "{LDA}")]


def ct_t5():
    return tpl(CT, 5, CT_BASE,
        title="원에 외접하는 사각형 — 두 쌍의 대변의 길이의 합이 같다",
        skill="AB + CD = BC + DA를 세워 모르는 한 변의 길이 구하기",
        variant_axis={"접선의 길이": "1~6 (네 꼭짓점)", "구하는 변": "AB / BC / CD / DA"},
        difficulty=2,
        discriminates="이웃한 변이 아니라 마주 보는 두 변의 합끼리 같음을 아는가",
        params=[{"name": "f", "values": {"in": list(CT5_ROWS)}}],
        table={"key": "f", "rows": CT5_ROWS},
        cost_values=["ab", "bc", "cd", "da", "ans"],
        answer_var="ans",
        verify=["ab + cd == bc + da"],
        question="다음 그림과 같이 사각형 ABCD가 원 O에 외접하고 {GIVEN}일 때, [[seg({ASK})]]의 길이를 구하시오.",
        figure=scene(CT5_PTS, CT5_SEGS, circles=[{"c": "O", "r": "{rho}"}]),
        answer="{ans}", answer_alt=[],
        sol1="원에 외접하는 사각형에서는 한 꼭짓점에서 두 접점까지의 길이가 같으므로, 네 변을 접선의 길이로 나누어 더하면 마주 보는 두 변의 길이의 합이 서로 같다: AB + CD = BC + DA. 아는 세 변을 넣어 나머지 한 변을 구한다.",
        sol1_fig=scene(CT5_PTS, [lseg("A", "B", "{ab}"), lseg("B", "C", "{bc}"), lseg("C", "D", "{cd}"), lseg("D", "A", "{da}")], circles=[{"c": "O", "r": "{rho}"}]),
        sol1_anim=[[hl("seg:A-B", "seg:C-D", keep=True)], [hl("seg:B-C", "seg:D-A")]],
        sol2=[
            "AB + CD = BC + DA (외접사각형의 성질)",
            "{EQ}",
            "{CALC}",
        ],
        sol2_fig=steps([
            {"text": "AB + CD = BC + DA", "hint": "대변의 합"},
            {"text": "{EQ}", "hint": "아는 세 변 대입"},
            {"text": "{CALC}", "marks": [{"on": "{ans}", "note": "{ASK}"}]},
        ]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1")], [reveal(2), hl("mark:2-0")]],
        sol3="AB + CD = {ab} + {cd} = {ab + cd}, BC + DA = {bc} + {da} = {bc + da}{ro(bc + da)} 두 합이 같다. 따라서 {ASK} = {ans}이다.",
        model_answer="원에 외접하는 사각형에서 AB + CD = BC + DA이므로 {EQ}, {CALC}이다.",
        rubric=[
            {"element": "외접사각형의 성질", "points": 3, "criterion": "AB + CD = BC + DA를 세웠다.", "partial": "이웃한 변끼리 더했으면 인정하지 않는다."},
            {"element": "계산", "points": 2, "criterion": "{ASK} = {ans}{eul(ans)} 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


CT_SEED = {
    "seed_id": CT, "category": "도형",
    "title": "원의 현과 접선 — 현의 수직이등분선·접선의 길이·두 접선의 각·삼각형의 내접원·외접사각형",
    "unit_id": "m3-2", "concept_ids": ["m3-2-06", "m3-2-07", "m3-2-08"],
    "schema_id": None, "schema_name": "원의 현과 접선의 성질",
    "source_item_ids": [],
    "note": "길이는 피타고라스 수 표(TRI). 그림은 반지름 3 으로 축소하거나(현·접선) 실제 좌표(내접원·외접사각형: 반지름은 표의 float).",
    "geometry": True,
    "templates": [geo(t) for t in (ct_t1(), ct_t2(), ct_t3(), ct_t4(), ct_t5())],
}


# ═══════════════════════════════════════════════════════════════════ 2. 원주각
CA = "m3-2-circle-angle"
CA_BASE = {**GEO, "prereq": ["원주각과 중심각의 관계", "삼각형의 내각의 합"], "ops": ["원의 성질"], "tags": ["원주각"]}


def P3(deg_expr: str):
    """중심 O, 반지름 3 인 원 위의 점 — 각(도) 식으로 좌표"""
    return [f"{{3*cos(pi*({deg_expr})/180)}}", f"{{3*sin(pi*({deg_expr})/180)}}"]


# t1 — 원주각 = ½ 중심각
CA1_ROWS = {
    "AOB-APB": {"GQ": "AOB", "XQ": "APB", "GA": "O", "XA": "P", "isC": 1, "STEP": "∠APB = ½ × ∠AOB", "LAW": "원주각은 중심각의 ½"},
    "APB-AOB": {"GQ": "APB", "XQ": "AOB", "GA": "P", "XA": "O", "isC": 0, "STEP": "∠AOB = 2 × ∠APB", "LAW": "중심각은 원주각의 2배"},
}


def ca_t1():
    return tpl(CA, 1, CA_BASE,
        title="원주각과 중심각 — 한 호에 대한 원주각은 중심각의 ½",
        skill="같은 호 AB에 대한 원주각 ∠APB와 중심각 ∠AOB의 관계 ∠APB = ½∠AOB 쓰기",
        variant_axis={"주어진 각": "중심각 / 원주각", "원주각": "15°~85°"},
        difficulty=1,
        discriminates="원주각과 중심각을 구별하고 2배·½의 방향을 바르게 쓰는가",
        params=[{"name": "v", "values": {"in": list(CA1_ROWS)}}, {"name": "x", "values": {"int": [15, 85]}}],
        table={"key": "v", "rows": CA1_ROWS},
        derive={"c": "2*x", "gv": "2*x*isC + x*(1 - isC)", "ans": "x*isC + 2*x*(1 - isC)"},
        cost_values=["x", "c", "ans"],
        answer_var="ans",
        verify=["c == 2*x", "ans != gv"],
        question="다음 그림에서 점 O는 원의 중심이고 [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene({"O": [0, 0], "A": P3("270 - x"), "B": P3("270 + x"), "P": [0, 3]}, [["O", "A"], ["O", "B"], ["P", "A"], ["P", "B"]], circles=CIRC,
                     marks={"arc": [arc("{GA}", "A", "B", "{gv}°", "arc:given"), arc("{XA}", "A", "B", None, "arc:ask")]}),
        answer="[[deg({ans})]]", answer_alt=["{ans}°", "{ans}"],
        sol1="호 AB에 대한 중심각은 ∠AOB, 원주각은 ∠APB이다. 한 호에 대한 원주각의 크기는 그 호에 대한 중심각의 크기의 ½이다: ∠APB = ½∠AOB. {LAW}이므로 {STEP}로 구한다.",
        sol1_fig=scene({"O": [0, 0], "A": P3("270 - x"), "B": P3("270 + x"), "P": [0, 3]}, [["O", "A"], ["O", "B"], ["P", "A"], ["P", "B"]], circles=CIRC,
                       marks={"arc": [arc("O", "A", "B", "{c}°", "arc:o"), arc("P", "A", "B", "{x}°", "arc:p")]}),
        sol1_anim=[[hl("arc:o", keep=True)], [hl("arc:p")]],
        sol2=[
            "호 AB에 대한 중심각 ∠AOB = {c}°, 원주각 ∠APB = {x}°의 관계: ∠APB = ½∠AOB",
            "{STEP} = {ans}°",
        ],
        sol2_fig=steps([{"text": "∠APB = ½ × ∠AOB", "hint": "{LAW}"}, {"text": "{STEP} = {ans}°", "marks": [{"on": "{ans}°", "note": "∠{XQ}"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="중심각 {c}°는 원주각 {x}°의 2배로 관계가 맞는다. 원주각은 항상 중심각보다 작다는 점으로 방향을 확인하면 ∠{XQ} = {ans}이다.",
        model_answer="한 호에 대한 원주각은 중심각의 ½이므로 {STEP} = {ans}°이다.",
        rubric=[
            {"element": "원주각·중심각의 관계", "points": 3, "criterion": "∠APB = ½∠AOB(또는 ∠AOB = 2∠APB)를 썼다.", "partial": "관계를 반대로 썼으면 인정하지 않는다."},
            {"element": "각 구하기", "points": 2, "criterion": "∠{XQ} = {ans}°를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t2 — 반원에 대한 원주각은 90°: AB 지름, ∠CAB = a → ∠ABC = 90° − a
CA2_ROWS = {"A-B": {"GQ": "CAB", "XQ": "ABC", "GA": "A", "GF": "B", "GT": "C", "XA": "B", "XF": "A", "XT": "C", "isA": 1},
            "B-A": {"GQ": "ABC", "XQ": "CAB", "GA": "B", "GF": "A", "GT": "C", "XA": "A", "XF": "B", "XT": "C", "isA": 0}}


def ca_t2():
    return tpl(CA, 2, CA_BASE,
        title="반원에 대한 원주각 — 지름 AB, ∠ACB = 90°",
        skill="지름에 대한 원주각이 90°임을 써서 직각삼각형 ABC의 나머지 예각 구하기",
        variant_axis={"주어진 각": "∠CAB / ∠ABC", "각": "15°~75°"},
        difficulty=2,
        discriminates="AB가 지름이면 ∠ACB = 90°임을 알고 두 예각의 합이 90°임을 쓰는가",
        params=[{"name": "v", "values": {"in": list(CA2_ROWS)}}, {"name": "a", "values": {"int": [15, 75]}}],
        table={"key": "v", "rows": CA2_ROWS},
        derive={"gv": "a", "ans": "90 - a", "cang": "2*a*isA + (180 - 2*a)*(1 - isA)"},
        constraints=["ans != a"],
        cost_values=["a", "ans"],
        answer_var="ans",
        verify=["ans + a == 90"],
        question="다음 그림에서 [[seg(AB)]]는 원 O의 지름이고 [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene({"O": [0, 0], "A": [-3, 0], "B": [3, 0], "C": P3("cang")}, [["A", "B"], ["A", "C"], ["B", "C"]], circles=CIRC,
                     marks={"arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}),
        answer="[[deg({ans})]]", answer_alt=["{ans}°", "{ans}"],
        sol1="AB가 지름이므로 호 AB(반원)에 대한 중심각은 180°이고, 그 원주각 ∠ACB는 그 ½인 90°이다. 따라서 △ABC는 ∠C = 90°인 직각삼각형이고 나머지 두 각의 합은 90°이다: ∠CAB + ∠ABC = 90°.",
        sol1_fig=scene({"O": [0, 0], "A": [-3, 0], "B": [3, 0], "C": P3("cang")}, [["A", "B"], ["A", "C"], ["B", "C"]], circles=CIRC,
                       marks={"right": [["A", "C", "B"]], "arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}),
        sol1_anim=[[hl("seg:A-B", keep=True)], [hl("right:C", keep=True)], [hl("arc:ask")]],
        sol2=[
            "AB가 지름이므로 ∠ACB = 90° (반원에 대한 원주각)",
            "∠{XQ} = 90° − {gv}° = {ans}°",
        ],
        sol2_fig=steps([{"text": "∠ACB = 90°", "hint": "지름 → 반원의 원주각"}, {"text": "90° − {gv}° = {ans}°", "hint": "직각삼각형의 두 예각", "marks": [{"on": "{ans}°", "note": "∠{XQ}"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="세 각 {gv}° + {ans} + 90° = 180°로 삼각형의 내각의 합이 맞는다. 따라서 ∠{XQ} = {ans}이다.",
        model_answer="AB가 지름이므로 ∠ACB = 90°이다. 따라서 ∠{XQ} = 90° − {gv}° = {ans}°이다.",
        rubric=[
            {"element": "반원의 원주각", "points": 3, "criterion": "AB가 지름이므로 ∠ACB = 90°임을 밝혔다.", "partial": "근거 없이 직각이라 했으면 1점."},
            {"element": "각 구하기", "points": 2, "criterion": "∠{XQ} = {ans}°를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t3 — 원에 내접하는 사각형: 대각의 합 180°
CA3_ROWS = {
    "A-C": {"GQ": "A", "XQ": "BCD", "GA": "A", "GF": "B", "GT": "D", "XA": "C", "XF": "B", "XT": "D", "useA": 1, "LAW": "∠A + ∠C = 180° (마주 보는 두 각의 합)", "STEP": "∠BCD = 180° − ∠A"},
    "B-D": {"GQ": "B", "XQ": "ADC", "GA": "B", "GF": "A", "GT": "C", "XA": "D", "XF": "A", "XT": "C", "useA": 0, "LAW": "∠B + ∠D = 180° (마주 보는 두 각의 합)", "STEP": "∠ADC = 180° − ∠B"},
}
QUAD_PTS = {"A": P3("240 + u + w2 + w"), "B": P3("240"), "C": P3("240 + u"), "D": P3("240 + u + w2")}
QUAD_SEGS = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"]]


def ca_t3():
    return tpl(CA, 3, CA_BASE,
        title="원에 내접하는 사각형 — 마주 보는 두 각의 합은 180°",
        skill="원에 내접하는 사각형의 대각의 합이 180°임을 써서 나머지 각 구하기",
        variant_axis={"주어진 각": "∠A / ∠B", "호": "세 호 40°~"},
        difficulty=2,
        discriminates="마주 보는 각(이웃한 각이 아님)의 합이 180°임을 지키는가",
        params=[{"name": "v", "values": {"in": list(CA3_ROWS)}}, {"name": "u", "values": {"in": list(range(40, 150, 2))}}, {"name": "w2", "values": {"in": list(range(40, 150, 2))}}, {"name": "w", "values": {"in": list(range(40, 150, 2))}}],
        table={"key": "v", "rows": CA3_ROWS},
        derive={"angA": "(u + w2)/2", "angB": "(w2 + w)/2", "gv": "(u + w2)/2*useA + (w2 + w)/2*(1 - useA)", "ans": "(180 - (u + w2)/2)*useA + (180 - (w2 + w)/2)*(1 - useA)"},
        constraints=["u + w2 + w <= 300", "ans != gv", "angA != angB"],
        cost_values=["u", "w2", "w", "gv", "ans"],
        answer_var="ans",
        verify=["2*angA == u + w2", "2*angB == w2 + w", "ans + gv == 180"],
        question="다음 그림에서 사각형 ABCD는 원에 내접하고 [[angle({GQ})]] = [[deg({gv})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(QUAD_PTS, QUAD_SEGS, circles=[{"c": [0, 0], "r": 3}],
                     marks={"arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}),
        answer="[[deg({ans})]]", answer_alt=["{ans}°", "{ans}"],
        sol1="원에 내접하는 사각형에서 마주 보는 두 각은 원을 둘로 나누는 두 호에 대한 원주각이다. 두 호의 중심각의 합이 360°이므로 두 원주각의 합은 그 ½인 180°이다: ∠A + ∠C = 180°, ∠B + ∠D = 180°. {LAW}{eul(LAW)} 쓴다.",
        sol1_fig=scene(QUAD_PTS, QUAD_SEGS, circles=[{"c": [0, 0], "r": 3}],
                       marks={"arc": [arc("{GA}", "{GF}", "{GT}", "{gv}°", "arc:given"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}),
        sol1_anim=[[hl("arc:given", keep=True)], [hl("arc:ask")]],
        sol2=[
            "{LAW}",
            "{STEP} = 180° − {gv}° = {ans}°",
        ],
        sol2_fig=steps([{"text": "{LAW}", "hint": "내접사각형의 성질"}, {"text": "180° − {gv}° = {ans}°", "marks": [{"on": "{ans}°", "note": "∠{XQ}"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="∠A = {angA}°, ∠B = {angB}°이면 ∠C = {180 - angA}°, ∠D = {180 - angB}°로 네 각의 합이 360°이고 대각의 합은 각각 180°이다. 따라서 ∠{XQ} = {ans}이다.",
        model_answer="{LAW}이므로 {STEP} = 180° − {gv}° = {ans}°이다.",
        rubric=[
            {"element": "내접사각형의 성질", "points": 3, "criterion": "{LAW}{eul(LAW)} 근거로 썼다.", "partial": "이웃한 각의 합을 180°로 썼으면 인정하지 않는다."},
            {"element": "각 구하기", "points": 2, "criterion": "∠{XQ} = {ans}°를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t6 — 내접사각형의 외각은 내대각과 같다: ∠DCE = ∠A, 대각선 BD 와 △ABD 의 내각의 합
QUAD_PTS_E = {**QUAD_PTS, "E": ["{cx + 0.7*(cx - bx)}", "{cy + 0.7*(cy - by)}"]}
QUAD_SEGS_E = [["A", "B"], ["B", "C"], ["C", "D"], ["D", "A"], ["B", "D"], {"a": "C", "b": "E", "dash": True}]


def ca_t6():
    return tpl(CA, 6, CA_BASE,
        title="원에 내접하는 사각형의 외각 — ∠DCE = ∠A와 △ABD의 내각의 합",
        skill="한 외각이 그 내대각과 같음(∠DCE = ∠A)을 쓰고 대각선 BD로 만든 △ABD에서 나머지 각 구하기",
        variant_axis={"외각": "40°~110°", "∠ABD": "20°~70°"},
        difficulty=3,
        discriminates="외각이 이웃한 내각이 아니라 내대각 ∠A와 같음을 알고, △ABD에서 내각의 합을 쓰는가",
        params=[{"name": "u", "values": {"in": list(range(40, 150, 2))}}, {"name": "w2", "values": {"in": list(range(40, 150, 2))}}, {"name": "b", "values": {"int": [20, 70]}}],
        derive={"w": "2*b", "e": "(u + w2)/2", "angC": "180 - (u + w2)/2", "ans": "180 - (u + w2)/2 - b",
                "cx": "3*cos(pi*(240 + u)/180)", "cy": "3*sin(pi*(240 + u)/180)", "bx": "3*cos(pi*240/180)", "by": "3*sin(pi*240/180)"},
        constraints=["u + w2 + w <= 300", "ans not in (e, b, angC)", "ans >= 20", "e != b"],
        cost_values=["u", "w2", "b", "e", "ans"],
        answer_var="ans",
        verify=["e + angC == 180", "e + b + ans == 180"],
        question="다음 그림에서 사각형 ABCD는 원에 내접하고 점 E는 변 BC의 연장선 위의 점이다. [[angle(DCE)]] = [[deg({e})]], [[angle(ABD)]] = [[deg({b})]]일 때, [[angle(ADB)]]의 크기를 구하시오.",
        figure=scene(QUAD_PTS_E, QUAD_SEGS_E, circles=[{"c": [0, 0], "r": 3}],
                     marks={"arc": [arc("C", "D", "E", "{e}°", "arc:e"), arc("B", "A", "D", "{b}°", "arc:b"), arc("D", "A", "B", None, "arc:ask")]}),
        answer="[[deg({ans})]]", answer_alt=["{ans}°", "{ans}"],
        sol1="외각 ∠DCE와 이웃한 내각 ∠BCD는 합이 180°이고, 원에 내접하는 사각형에서 ∠A + ∠BCD = 180°이므로 ∠DCE = ∠A — 외각은 그 내대각과 같다. 따라서 ∠BAD = {e}°이고, △ABD에서 세 내각의 합 180°로 ∠ADB를 구한다.",
        sol1_fig=scene(QUAD_PTS_E, QUAD_SEGS_E, circles=[{"c": [0, 0], "r": 3}],
                       marks={"arc": [arc("C", "D", "E", "{e}°", "arc:e"), arc("A", "B", "D", "{e}°", "arc:a"), arc("B", "A", "D", "{b}°", "arc:b"), arc("D", "A", "B", None, "arc:ask")]}),
        sol1_anim=[[hl("arc:e", keep=True)], [hl("arc:a", keep=True)], [hl("arc:b", keep=True)], [hl("arc:ask")]],
        sol2=[
            "∠BAD = ∠DCE = {e}° (외각 = 내대각)",
            "△ABD에서 ∠ADB = 180° − {e}° − {b}° = {ans}°",
        ],
        sol2_fig=steps([{"text": "∠BAD = {e}°", "hint": "외각 = 내대각"}, {"text": "180° − {e}° − {b}° = {ans}°", "hint": "△ABD의 내각의 합", "marks": [{"on": "{ans}°", "note": "∠ADB"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="∠BCD = 180° − {e}° = {angC}°이고 ∠A + ∠BCD = {e}° + {angC}° = 180°로 내접사각형의 성질에 맞는다. △ABD의 세 각 {e}° + {b}° + {ans} = 180°. 따라서 ∠ADB = {ans}이다.",
        model_answer="원에 내접하는 사각형의 한 외각은 그 내대각과 같으므로 ∠BAD = ∠DCE = {e}°이다. △ABD에서 ∠ADB = 180° − {e}° − {b}° = {ans}°이다.",
        rubric=[
            {"element": "외각 = 내대각", "points": 3, "criterion": "∠BAD = ∠DCE = {e}°임을 밝혔다.", "partial": "이웃한 내각 ∠BCD와 같다고 했으면 인정하지 않는다."},
            {"element": "각 구하기", "points": 2, "criterion": "△ABD의 내각의 합으로 ∠ADB = {ans}°를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t4 — 접선과 현이 이루는 각: ∠BAT = ∠ACB, 삼각형의 내각의 합
CA4_ROWS = {
    "B→BAC": {"G2Q": "ABC", "XQ": "BAC", "useB": 1, "G2A": "B", "G2F": "A", "G2T": "C", "XA": "A", "XF": "B", "XT": "C", "STEP": "∠BAC = 180° − ∠ACB − ∠ABC"},
    "C→ABC": {"G2Q": "BAC", "XQ": "ABC", "useB": 0, "G2A": "A", "G2F": "B", "G2T": "C", "XA": "B", "XF": "A", "XT": "C", "STEP": "∠ABC = 180° − ∠ACB − ∠BAC"},
}
TAN_PTS = {"A": [0, -3], "T": [2.6, -3], "B": ["{bx}", "{by}"], "C": ["{cx}", "{cy}"]}
TAN_SEGS = [["A", "T"], ["A", "B"], ["B", "C"], ["C", "A"]]


def ca_t4():
    return tpl(CA, 4, CA_BASE,
        title="원의 접선과 현이 이루는 각 — ∠BAT = ∠ACB",
        skill="접선 AT와 현 AB가 이루는 각이 호 AB에 대한 원주각 ∠ACB와 같음을 쓰고 삼각형의 내각의 합으로 나머지 각 구하기",
        variant_axis={"구하는 각": "∠BAC / ∠ABC", "∠BAT": "20°~80°", "다른 각": "20°~80°"},
        difficulty=3,
        discriminates="접선과 현이 이루는 각이 반대쪽 호의 원주각 ∠ACB와 같음을 알고, △ABC에서 나머지 각을 구하는가",
        params=[{"name": "v", "values": {"in": list(CA4_ROWS)}}, {"name": "a", "values": {"int": [20, 80]}}, {"name": "b", "values": {"int": [20, 80]}}],
        table={"key": "v", "rows": CA4_ROWS},
        derive={"c": "180 - a - b", "g2": "b*useB + (180 - a - b)*(1 - useB)", "ans": "(180 - a - b)*useB + b*(1 - useB)",
                "bx": "3*cos(pi*(2*a - 90)/180)", "by": "3*sin(pi*(2*a - 90)/180)", "cx": "3*cos(pi*(-90 - 2*b)/180)", "cy": "3*sin(pi*(-90 - 2*b)/180)"},
        constraints=["a + b <= 150", "ans != a", "ans != g2", "a != b"],
        cost_values=["a", "b", "c", "ans"],
        answer_var="ans",
        verify=["a + b + c == 180", "ans + g2 + a == 180"],
        question="다음 그림에서 직선 AT는 원의 접선이고 점 A는 접점이다. [[angle(BAT)]] = [[deg({a})]], [[angle({G2Q})]] = [[deg({g2})]]일 때, [[angle({XQ})]]의 크기를 구하시오.",
        figure=scene(TAN_PTS, TAN_SEGS, circles=[{"c": [0, 0], "r": 3}],
                     marks={"arc": [arc("A", "T", "B", "{a}°", "arc:a"), arc("{G2A}", "{G2F}", "{G2T}", "{g2}°", "arc:g2"), arc("{XA}", "{XF}", "{XT}", None, "arc:ask")]}),
        answer="[[deg({ans})]]", answer_alt=["{ans}°", "{ans}"],
        sol1="접선과 현이 이루는 각 ∠BAT는 그 현 AB에 대한 원주각(현의 반대쪽 점 C에서 본 각) ∠ACB와 같다: ∠ACB = ∠BAT = {a}°. 그러면 △ABC의 세 각 중 둘을 알게 되므로 내각의 합 180°로 나머지 각을 구한다.",
        sol1_fig=scene(TAN_PTS, TAN_SEGS, circles=[{"c": [0, 0], "r": 3}],
                       marks={"arc": [arc("A", "T", "B", "{a}°", "arc:a"), arc("C", "A", "B", "{a}°", "arc:c"), arc("{G2A}", "{G2F}", "{G2T}", "{g2}°", "arc:g2")]}),
        sol1_anim=[[hl("arc:a", keep=True)], [hl("arc:c", keep=True)], [hl("arc:g2")]],
        sol2=[
            "∠ACB = ∠BAT = {a}° (접선과 현이 이루는 각)",
            "△ABC에서 {STEP} = 180° − {a}° − {g2}° = {ans}°",
        ],
        sol2_fig=steps([{"text": "∠ACB = {a}°", "hint": "접선과 현이 이루는 각 = 원주각"}, {"text": "{STEP} = {ans}°", "hint": "내각의 합 180°", "marks": [{"on": "{ans}°", "note": "∠{XQ}"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("hint:1", "mark:1-0")]],
        sol3="△ABC의 세 각 ∠ACB = {a}°, ∠ABC = {b}°, ∠BAC = {c}°의 합은 180°로 맞는다. 따라서 ∠{XQ} = {ans}이다.",
        model_answer="접선과 현이 이루는 각은 그 현에 대한 원주각과 같으므로 ∠ACB = ∠BAT = {a}°이다. 따라서 {STEP} = {ans}°이다.",
        rubric=[
            {"element": "접선과 현의 각", "points": 3, "criterion": "∠ACB = ∠BAT = {a}°임을 밝혔다.", "partial": "다른 각과 같다고 했으면 인정하지 않는다."},
            {"element": "각 구하기", "points": 2, "criterion": "∠{XQ} = {ans}°를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


# t5·t7 — 원주각의 크기는 호의 길이에 비례 (t5: 작은 호의 원주각 → 큰 호, t7: 반대)
ARC_PTS = {"A": P3("0"), "B": P3("2*n*x"), "C": P3("2*n*x + 70"), "D": P3("2*n*x + 70 + 2*x"), "Q": P3("2*n*x + 35"), "P": P3("(2*n*x + 70 + 2*x)/2 + 180")}
ARC_SEGS = [["P", "A"], ["P", "B"], ["Q", "C"], ["Q", "D"]]


def _ca_arc(no, given_q, ask_q, step, marks_q, marks_s, title, skill, disc, ans_expr, gv_expr):
    return tpl(CA, no, CA_BASE,
        title=title,
        skill=skill,
        variant_axis={"배수": "2·3·4", "각": "8°~30°"},
        difficulty=2,
        discriminates=disc,
        params=[{"name": "n", "values": {"in": [2, 3, 4]}}, {"name": "x", "values": {"int": [8, 30]}}],
        derive={"big": "n*x", "gv": gv_expr, "ans": ans_expr},
        constraints=["n*x <= 90"],
        cost_values=["n", "x", "big", "ans"],
        answer_var="ans",
        verify=["big == n*x"],
        question=f"다음 그림의 원에서 호 AB의 길이는 호 CD의 길이의 {{n}}배이다. [[angle({given_q})]] = [[deg({{gv}})]]일 때, [[angle({ask_q})]]의 크기를 구하시오.",
        figure=scene(ARC_PTS, ARC_SEGS, circles=[{"c": [0, 0], "r": 3}], marks={"arc": marks_q}),
        answer="[[deg({ans})]]", answer_alt=["{ans}°", "{ans}"],
        sol1="한 원에서 호의 길이는 중심각의 크기에 정비례하고, 원주각은 중심각의 ½이므로 원주각의 크기도 호의 길이에 정비례한다. 호 AB가 호 CD의 {n}배이면 ∠APB도 ∠CQD의 {n}배이다: ∠APB = {n} × ∠CQD.",
        sol1_fig=scene(ARC_PTS, ARC_SEGS, circles=[{"c": [0, 0], "r": 3}], marks={"arc": marks_s}),
        sol1_anim=[[hl("arc:q", keep=True)], [hl("arc:p")]],
        sol2=[
            "호 AB : 호 CD = {n} : 1이므로 ∠APB : ∠CQD = {n} : 1",
            f"{step} = {{ans}}°",
        ],
        sol2_fig=steps([{"text": "∠APB : ∠CQD = {n} : 1", "hint": "원주각 ∝ 호의 길이"}, {"text": f"{step} = {{ans}}°", "marks": [{"on": "{ans}°", "note": f"∠{ask_q}"}]}]),
        sol2_anim=[[reveal(0), hl("hint:0")], [reveal(1), hl("mark:1-0")]],
        sol3="∠APB = {big}°는 ∠CQD = {x}°의 {n}배로 호의 길이의 비 {n} : 1과 맞는다. 따라서 ∠" + ask_q + " = {ans}이다.",
        model_answer="원주각의 크기는 호의 길이에 정비례하므로 ∠APB = {n} × ∠CQD이다. 따라서 " + step + " = {ans}°이다.",
        rubric=[
            {"element": "비례 관계", "points": 3, "criterion": "원주각의 크기가 호의 길이에 정비례함을 써서 ∠APB = {n}∠CQD를 세웠다.", "partial": "비를 반대로 세웠으면 인정하지 않는다."},
            {"element": "각 구하기", "points": 2, "criterion": "∠" + ask_q + " = {ans}°를 구했다.", "partial": "계산 실수면 1점."},
        ],
        rubric_total=5,
    )


def ca_t5():
    return _ca_arc(5, "CQD", "APB", "∠APB = {n} × {x}°", [arc("Q", "C", "D", "{x}°", "arc:q"), arc("P", "A", "B", None, "arc:p")], [arc("Q", "C", "D", "{x}°", "arc:q"), arc("P", "A", "B", "{big}°", "arc:p")],
                   "원주각과 호의 길이 — 호가 n배이면 원주각도 n배", "호의 길이의 비로 큰 호의 원주각 구하기", "호의 길이의 비가 원주각의 비와 같음을 알고 곱하는가", "n*x", "x")


def ca_t7():
    return _ca_arc(7, "APB", "CQD", "∠CQD = {big}° ÷ {n}", [arc("P", "A", "B", "{big}°", "arc:p"), arc("Q", "C", "D", None, "arc:q")], [arc("Q", "C", "D", "{x}°", "arc:q"), arc("P", "A", "B", "{big}°", "arc:p")],
                   "원주각과 호의 길이 — 큰 호의 원주각으로 작은 호의 원주각 구하기", "호의 길이의 비로 작은 호의 원주각 구하기", "호의 길이의 비가 원주각의 비와 같음을 알고 나누는가", "x", "n*x")


CA_SEED = {
    "seed_id": CA, "category": "도형",
    "title": "원주각 — 원주각과 중심각·반원의 원주각·내접사각형(대각·외각)·접선과 현이 이루는 각·원주각과 호의 길이(×n·÷n)",
    "unit_id": "m3-2", "concept_ids": ["m3-2-09", "m3-2-10", "m3-2-11"],
    "schema_id": None, "schema_name": "원주각의 성질",
    "source_item_ids": [],
    "note": "원 위의 점은 P3(각 식) 로 실제 각에 맞게 배치(반지름 3). 각 라벨 '{gv}°' 는 recheck F1 이 좌표로 실측·대조한다.",
    "geometry": True,
    "templates": [geo(t) for t in (ca_t1(), ca_t2(), ca_t3(), ca_t4(), ca_t5(), ca_t6(), ca_t7())],
}


if __name__ == "__main__":
    for seed in (CT_SEED, CA_SEED):
        with_pitfalls(seed)
        dump(seed)
