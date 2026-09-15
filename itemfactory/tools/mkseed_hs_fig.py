# itemfactory/tools/mkseed_hs_fig.py — 고등부 2차: 그림이 있는 틀 (v1.0 · 2026-09-15 세션 5c)
#
#   python itemfactory/tools/mkseed_hs_fig.py
#     → seeds/h3-3-solid.json     (직육면체 wire 도형: 대각선 길이·삼수선(점과 직선/평면 거리)·정사영 넓이·이면각, 4틀 — 기하 2단 해설)
#     → seeds/h3-3-conicfig.json  (coordplane 곡선: 포물선 초점거리·타원 둘레/초점거리·쌍곡선 초점거리, 3틀)
#     → seeds/h3-3-vecfig.json    (coordplane 화살표: 벡터 합·차·내적·각, 2틀)
#     → seeds/h2-1-trigfig.json   (coordplane 곡선: 삼각함수 그래프의 최대·최소·주기 → a, b, c, 2틀)
#   09-15 figsvg 확장(wire segs/right, coordplane arrows)을 쓴다. 수치는 모두 문면에(DB 키는 문면만), 그림은 상황을 보여 준다.
from __future__ import annotations

import itertools
import math
import os
import random
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from hsseed import HS, SEED, T, run  # noqa: E402
from genkit.expr import eul as _eul, ika as _ika, ro as _ro, wa as _wa  # noqa: E402

rng = random.Random(20260924)


def _nums(text):
    return {Fraction(x) for x in re.findall(r"(?<![\d.])-?\d+(?![\d.])", text)}


def _fm(v):
    f = Fraction(v)
    if f.denominator == 1:
        return str(f.numerator)
    return f"[[{'-' if f < 0 else ''}frac({abs(f.numerator)},{f.denominator})]]"


def _pick(d, n):
    keys = sorted(d)
    rng.shuffle(keys)
    return {k: d[k] for k in keys[:n]}


def _row(q, v, **kw):
    f = Fraction(v)
    shown = _nums(q) | _nums(kw.get("Q", ""))
    if f == 0 or f in shown or abs(f) in shown:
        return None
    d = {"VN": f.numerator, "VD": f.denominator}
    d.update(kw)
    return d


def _isq(v):
    f = Fraction(v)
    a, b = math.isqrt(f.numerator), math.isqrt(f.denominator)
    return Fraction(a, b) if a * a == f.numerator and b * b == f.denominator else None


# 직육면체 ABCD-EFGH: A(0,h,0) B(w,h,0) C(w,h,d) D(0,h,d) / E(0,0,0) F(w,0,0) G(w,0,d) H(0,0,d) — figsvg wire 와 같은 배치 (AB = w, AD = d, AE = h)
def _P3(w, d, h):
    return {"A": (0, h, 0), "B": (w, h, 0), "C": (w, h, d), "D": (0, h, d), "E": (0, 0, 0), "F": (w, 0, 0), "G": (w, 0, d), "H": (0, 0, d)}


def _dist2(P, a, b):
    return sum((P[a][i] - P[b][i]) ** 2 for i in range(3))


def _dot(P, a, b, c, d):
    """(b − a) · (d − c)"""
    return sum((P[b][i] - P[a][i]) * (P[d][i] - P[c][i]) for i in range(3))


def _ilen(P, a, b):
    """정수 길이(아니면 None)."""
    n = _dist2(P, a, b)
    r = math.isqrt(n)
    return r if r * r == n else None


EDGES = {"AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"}
FACES = {"ABCD": ("y", 1), "EFGH": ("y", 0), "ABFE": ("z", 0), "DCGH": ("z", 1), "AEHD": ("x", 0), "BFGC": ("x", 1)}
DIMNAME = {0: "AB", 1: "AE", 2: "AD"}   # 좌표축 → 치수 이름 (x → AB = w, y → AE = h, z → AD = d)


def _is_edge(s):
    return s in EDGES or s[::-1] in EDGES


def _box_txt(w, d, h):
    return f"그림과 같이 AB = {w}, AD = {d}, AE = {h}인 직육면체 ABCD-EFGH"


def _dims(P, a, b):
    """두 점이 다른 축의 (치수 이름, 길이) — 선분 ab 가 놓인 직각삼각형의 변."""
    return [(DIMNAME[i], abs(P[a][i] - P[b][i])) for i in range(3) if P[a][i] != P[b][i]]


TRIPLES = [(w, d, h) for w in range(2, 14) for d in range(2, 14) for h in range(2, 14)]


# ═══════════════════════════════════════════════════════════════════ 1. 직육면체 (h3-3-08~11)
SD = "h3-3-solid"
SD_B = {**HS, "context": "기하맥락", "prereq": ["피타고라스 정리", "직육면체"], "ops": ["공간도형"], "traps": ["대각선이 놓인 직각삼각형 찾기", "정사영은 수선의 발로 옮긴 도형"], "tags": ["직육면체", "삼수선", "정사영", "이면각"]}


def _face_of(seg):
    """면의 대각선 seg 가 놓인 면 이름과 직각 꼭짓점(삼각형 P R Q 가 R 에서 직각)."""
    P = _P3(3, 5, 7)
    for face in FACES:
        if seg[0] in face and seg[1] in face:
            R = [v for v in face if v not in seg and _dot(P, v, seg[0], v, seg[1]) == 0][0]
            return face, R
    return None, None


def _sd1_rows():
    out = {}
    for w, d, h in TRIPLES:
        P = _P3(w, d, h)
        # 공간 대각선 4종 — 세 모서리
        for seg in ("AG", "BH", "CE", "DF"):
            L = _ilen(P, seg[0], seg[1])
            if L is None:
                continue
            q = f"직육면체 {w} {d} {h} {seg}"
            r = _row(q, L, Q=f"{_box_txt(w, d, h)}에서 선분 {seg}의 길이를 구하시오.", W=w, D=d, H=h, SEGS=[seg], RIGHT=[], SEG=seg,
                     STEP=f"{seg} = [[sqrt(pow({w},2) + pow({d},2) + pow({h},2))]] = [[sqrt({w * w + d * d + h * h})]] = {L}", KIND="공간 대각선",
                     TRI=f"{seg}는 직육면체의 대각선이므로 {seg}² = AB² + AD² + AE²(세 모서리의 제곱의 합)")
            if r: out[f"s{w}_{d}_{h}_{seg}"] = r
        # 면의 대각선 — 그 면의 두 모서리
        for seg in ("AC", "BD", "AF", "BE", "AH", "DE", "CF", "BG", "EG", "FH", "DG", "CH"):
            L = _ilen(P, seg[0], seg[1])
            if L is None:
                continue
            face, R = _face_of(seg)
            (n1, l1), (n2, l2) = _dims(P, seg[0], seg[1])
            q = f"직육면체 {w} {d} {h} {seg}"
            r = _row(q, L, Q=f"{_box_txt(w, d, h)}에서 선분 {seg}의 길이를 구하시오.", W=w, D=d, H=h, SEGS=[seg], RIGHT=[[seg[0], R, seg[1]]], SEG=seg,
                     STEP=f"{seg[0]}{R} = {n1} = {l1}, {R}{seg[1]} = {n2} = {l2}이므로 {seg} = [[sqrt(pow({l1},2) + pow({l2},2))]] = [[sqrt({l1 * l1 + l2 * l2})]] = {L}", KIND="면의 대각선",
                     TRI=f"{seg}는 면 {face}의 대각선이므로 직각삼각형 {seg[0]}{R}{seg[1]}(∠{R} = 90°)에서 {seg}² = {seg[0]}{R}² + {R}{seg[1]}²")
            if r: out[f"f{w}_{d}_{h}_{seg}"] = r
    return _pick(out, 330)


SD1_ROWS = _sd1_rows()


def sd_t1():
    return T(SD, 1, SD_B, title="직육면체의 대각선의 길이",
        skill="직육면체의 세 모서리로 직각삼각형을 두 번 만들어 면의 대각선·공간 대각선의 길이를 √(a² + b²), √(a² + b² + c²)로 구하기", axis={"선분": "공간 대각선 AG·BH·CE·DF / 면의 대각선 AC·AF·AH·…", "치수": "2~13 (길이가 정수가 되는 조합)"}, disc="구하는 대각선이 놓인 직각삼각형(면 또는 대각선 단면)을 찾는가", diff=2,
        params=[{"name": "f", "values": {"in": list(SD1_ROWS)}}], table={"key": "f", "rows": SD1_ROWS},
        derive={"ans": "VN/VD"}, cost=["W", "D", "H", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        figure=[{"fn": "wire", "args": {"kind": "box", "names": "ABCDEFGH", "w": "{W}", "h": "{H}", "d": "{D}", "segs": "{SEGS}", "right": "{RIGHT}"}}],
        sol1="{TRI}. 직각삼각형에서 피타고라스 정리를 쓴다.",
        sol2=[("{TRI}", "직각삼각형 찾기"), ("{STEP}", "피타고라스 정리"), ("{SEG} = {ans}", None, ("{ans}", "{SEG}"))],
        sol3=["대각선은 모서리보다 길어야 하므로 {ans}가 관련된 모서리보다 큰지 확인한다. 따라서 {SEG} = {ans}이다."],
        model="{TRI}. {STEP}이므로 {SEG} = {ans}이다.",
        rubric=[("직각삼각형", 2, "{TRI}.", "다른 면의 모서리를 썼으면 인정하지 않는다."), ("값 구하기", 3, "{STEP} 꼴로 {ans}{eul(ans)} 구했다.", "제곱근 계산 실수면 1점.")],
        pitfalls=[("공간 대각선을 두 모서리로만 계산", "직각삼각형", "불인정"), ("제곱근을 빠뜨리고 제곱의 합을 답함", "값 구하기", "불인정"), ("면의 대각선에 세 모서리를 모두 더함", "직각삼각형", "불인정")], geo=True)


# 점과 직선(모서리) 사이의 거리 — (점, 직선, 직선을 품은 면, 점의 그 면 위 수선의 발 P, P 에서 직선에 내린 수선의 발 Q): 삼수선의 정리로 점Q ⊥ 직선
SD2_LINE = [("A", "FG", "EFGH", "E", "F"), ("A", "CG", "BFGC", "B", "C"), ("E", "BC", "ABCD", "A", "B"), ("A", "GH", "EFGH", "E", "H"),
            ("B", "DH", "AEHD", "A", "D"), ("D", "FG", "BFGC", "C", "G"), ("E", "CD", "ABCD", "A", "D"), ("F", "AD", "AEHD", "E", "A"),
            ("C", "EH", "AEHD", "D", "H"), ("B", "GH", "EFGH", "F", "G"), ("H", "AB", "ABCD", "D", "A"), ("G", "AE", "ABFE", "F", "E")]
# 점과 대각선 평면 사이의 거리 — (점, 평면, 대각선(교선), 점과 대각선이 놓인 면, 면에 수직인 평면의 모서리)
SD2_PLANE = [("A", "BFHD", "BD", "ABCD", "BF"), ("B", "AEGC", "AC", "ABCD", "AE"), ("A", "BCHE", "BE", "ABFE", "BC"), ("A", "DCFE", "DE", "AEHD", "DC"),
             ("C", "BFHD", "BD", "ABCD", "BF"), ("D", "AEGC", "AC", "ABCD", "AE"), ("F", "BCHE", "BE", "ABFE", "BC"), ("E", "ABGH", "AH", "AEHD", "AB")]


def _sd2_rows():
    out = {}
    P0 = _P3(3, 5, 7)
    for pt, line, plane, Pf, Q in SD2_LINE:     # 기하 검증(치수와 무관): pt-Pf ⊥ 면, Pf-Q ⊥ 직선, pt-Q ⊥ 직선
        assert Pf in plane and Q in line and _is_edge(pt + Pf) and _dot(P0, Pf, Q, line[0], line[1]) == 0 and _dot(P0, pt, Q, line[0], line[1]) == 0, (pt, line)
    for w, d, h in TRIPLES:
        P = _P3(w, d, h)
        for pt, line, plane, Pf, Q in SD2_LINE:
            hyp = _ilen(P, pt, Q)
            if hyp is None:
                continue
            l1, l2 = math.isqrt(_dist2(P, pt, Pf)), math.isqrt(_dist2(P, Pf, Q))
            other = line[0] if line[1] == Q else line[1]
            q = f"삼수선 {w} {d} {h} {pt} {line}"
            r = _row(q, hyp, Q=f"{_box_txt(w, d, h)}에서 꼭짓점 {pt}와 직선 {line} 사이의 거리를 구하시오.", W=w, D=d, H=h,
                     SEGS=[pt + Q, {"a": pt, "b": other, "dash": True}], RIGHT=[[pt, Q, other]], PERP=pt + Q, PT=pt, LINE=line,
                     WHY=f"꼭짓점 {pt}에서 평면 {plane}에 내린 수선의 발은 {Pf}이고, {Pf}에서 직선 {line}에 내린 수선의 발은 {Q}이므로 삼수선의 정리에 의하여 {pt}{Q} ⊥ {line}이다. 따라서 점 {pt}와 직선 {line} 사이의 거리는 선분 {pt}{Q}의 길이이다",
                     STEP=f"직각삼각형 {pt}{Pf}{Q}에서 {pt}{Pf} = {l1}, {Pf}{Q} = {l2}이므로 {pt}{Q} = [[sqrt(pow({l1},2) + pow({l2},2))]] = [[sqrt({l1 * l1 + l2 * l2})]] = {hyp}", KIND="점과 직선")
            if r: out[f"l{w}_{d}_{h}_{pt}{line}"] = r
        for pt, plane, diag, face, vedge in SD2_PLANE:
            hyp = _ilen(P, diag[0], diag[1])
            if hyp is None:
                continue
            assert pt in face and diag[0] in face and diag[1] in face and vedge[0] in plane and vedge[1] in plane and _is_edge(vedge)
            l1, l2 = math.isqrt(_dist2(P, pt, diag[0])), math.isqrt(_dist2(P, pt, diag[1]))
            assert l1 * l1 + l2 * l2 == hyp * hyp   # pt 에서 직각
            v = Fraction(l1 * l2, hyp)
            q = f"평면거리 {w} {d} {h} {pt} {plane}"
            segs = [diag, {"a": plane[1], "b": plane[2], "dash": True}] if plane[0] + plane[3] == diag or plane[3] + plane[0] == diag else [diag, {"a": plane[0], "b": plane[3], "dash": True}]
            r = _row(q, v, Q=f"{_box_txt(w, d, h)}에서 꼭짓점 {pt}와 평면 {plane} 사이의 거리를 구하시오.", W=w, D=d, H=h, SEGS=segs, RIGHT=[], PERP=f"{pt}I", PT=pt, LINE=diag,
                     WHY=f"모서리 {vedge}는 면 {face}에 수직이고 평면 {plane}에 포함되므로 평면 {plane} ⊥ 면 {face}이다. 꼭짓점 {pt}에서 두 평면의 교선 {diag}에 내린 수선의 발을 I라 하면 {pt}I ⊥ {diag}이므로 {pt}I ⊥ 평면 {plane}(수직인 두 평면에서 교선에 수직인 직선은 다른 평면에 수직)이고, 구하는 거리는 {pt}I의 길이이다",
                     STEP=f"직각삼각형 {pt}{diag[0]}{diag[1]}(∠{pt} = 90°)에서 {pt}{diag[0]} = {l1}, {pt}{diag[1]} = {l2}, {diag} = {hyp}이고 넓이 관계 {pt}{diag[0]} × {pt}{diag[1]} = {diag} × {pt}I에서 {pt}I = [[frac({l1} × {l2}, {hyp})]] = {_fm(v)}", KIND="점과 평면")
            if r: out[f"p{w}_{d}_{h}_{pt}{plane}"] = r
    return _pick(out, 330)


SD2_ROWS = _sd2_rows()


def sd_t2():
    return T(SD, 2, SD_B, title="삼수선의 정리 — 직육면체에서 점과 직선·평면 사이의 거리",
        skill="삼수선의 정리(또는 수직인 두 평면)로 수직인 선분을 찾아 점과 직선(모서리) 사이의 거리, 점과 대각선 평면 사이의 거리를 직각삼각형으로 구하기", axis={"묻는 것": "점과 모서리 사이의 거리 12종 / 점과 대각선 평면 사이의 거리 8종", "치수": "2~13 (거리가 정수·분수가 되는 조합)"}, disc="거리를 재는 수선이 어느 선분인지(삼수선) 판단하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(SD2_ROWS)}}], table={"key": "f", "rows": SD2_ROWS},
        derive={"ans": "VN/VD"}, cost=["W", "D", "H", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        figure=[{"fn": "wire", "args": {"kind": "box", "names": "ABCDEFGH", "w": "{W}", "h": "{H}", "d": "{D}", "segs": "{SEGS}", "right": "{RIGHT}"}}],
        sol1="{WHY}. 직각삼각형에서 피타고라스 정리(또는 넓이 관계)로 그 길이를 구한다.",
        sol2=[("{WHY}", "수직인 선분 찾기"), ("{STEP}", "계산"), ("거리 = {ans}", None, ("{ans}", "거리"))],
        sol3=["수선이 실제로 그 직선(평면)과 수직인지 삼수선의 정리의 조건을 다시 확인한다. 따라서 거리는 {ans}이다."],
        model="{WHY}. {STEP}이므로 거리는 {ans}이다.",
        rubric=[("수직인 선분 찾기", 3, "{WHY}를 밝혔다.", "수직인 선분을 잘못 잡았으면 인정하지 않는다."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("점에서 직선 위 꼭짓점까지의 거리(모서리)를 답함", "수직인 선분 찾기", "불인정"), ("수선의 발을 잘못 잡음", "수직인 선분 찾기", "불인정"), ("제곱근·분수 계산 실수", "값 구하기", "부분")], geo=True)


def _proj(P, v, face):
    """꼭짓점 v 의 면 face 위로의 수선의 발(꼭짓점 이름)."""
    ax, _ = FACES[face]
    i = "xyz".index(ax)
    return [u for u in face if all(P[u][j] == P[v][j] for j in range(3) if j != i)][0]


def _area2(P, names):
    """다각형(꼭짓점 이름, 순서대로)의 넓이 × 2 — 직육면체 면 위의 직각 다각형이므로 정수."""
    pts = [P[n] for n in names]
    # 면 위(한 좌표 공통) → 그 좌표를 빼고 신발끈
    const = [i for i in range(3) if len({p[i] for p in pts}) == 1][0]
    ij = [i for i in range(3) if i != const]
    s = 0
    for k in range(len(pts)):
        x1, y1 = pts[k][ij[0]], pts[k][ij[1]]
        x2, y2 = pts[(k + 1) % len(pts)][ij[0]], pts[(k + 1) % len(pts)][ij[1]]
        s += x1 * y2 - x2 * y1
    return abs(s)


SD3_FIGS = [("AFC", "EFGH"), ("BDG", "EFGH"), ("AFH", "EFGH"), ("ACF", "ABCD"), ("BGD", "ABCD"), ("AFG", "ABCD"), ("AEG", "ABFE"), ("ACH", "AEHD"), ("BDH", "ABFE"),
            ("AFGD", "EFGH"), ("ABGH", "EFGH"), ("BCHE", "ABCD"), ("ACGE", "ABFE"), ("CEH", "ABCD"), ("BHG", "ABCD"), ("DEF", "ABFE"), ("AGF", "AEHD")]


def _sd3_rows():
    out = {}
    for w, d, h in TRIPLES:
        if w == d or w > 12 or d > 12 or h > 8:
            continue
        P = _P3(w, d, h)
        for fig, plane in SD3_FIGS:
            proj = "".join(_proj(P, v, plane) for v in fig)
            if len(set(proj)) < len(proj):
                continue
            mapping = ", ".join(f"{v} → {p}" for v, p in zip(fig, proj))
            a2 = _area2(P, proj)
            v = Fraction(a2, 2)
            name = "삼각형" if len(fig) == 3 else "사각형"
            # 넓이 식: 직각삼각형(두 변) 또는 직사각형(두 변)
            if len(proj) == 3:
                R = [u for u in proj if _dot(P, u, [x for x in proj if x != u][0], u, [x for x in proj if x != u][1]) == 0][0]
                o1, o2 = [u for u in proj if u != R]
                n1, n2 = math.isqrt(_dist2(P, R, o1)), math.isqrt(_dist2(P, R, o2))
                step = f"{name} {proj}는 ∠{R} = 90°인 직각삼각형이고 {R}{o1} = {n1}, {R}{o2} = {n2}이므로 넓이 = [[frac(1, 2)]] × {n1} × {n2} = {_fm(v)}"
            else:
                n1, n2 = math.isqrt(_dist2(P, proj[0], proj[1])), math.isqrt(_dist2(P, proj[1], proj[2]))
                step = f"{name} {proj}는 {proj[0]}{proj[1]} = {n1}, {proj[1]}{proj[2]} = {n2}인 직사각형이므로 넓이 = {n1} × {n2} = {v}"
            segs = [fig[i] + fig[(i + 1) % len(fig)] for i in range(len(fig))]
            q = f"정사영 {w} {d} {h} {fig} {plane}"
            r = _row(q, v, Q=f"{_box_txt(w, d, h)}에서 {name} {fig}의 평면 {plane} 위로의 정사영의 넓이를 구하시오.", W=w, D=d, H=h, SEGS=segs, RIGHT=[], FIG=fig, PLANE=plane, PROJ=proj, MAP=mapping, STEP=step, KIND=name)
            if r: out[f"{w}_{d}_{h}_{fig}_{plane}"] = r
    return _pick(out, 330)


SD3_ROWS = _sd3_rows()


def sd_t3():
    return T(SD, 3, SD_B, title="직육면체에서 정사영의 넓이",
        skill="각 꼭짓점에서 평면에 내린 수선의 발로 도형을 옮겨 정사영을 찾고, 그 넓이를 직사각형·직각삼각형으로 계산하기", axis={"도형": "대각선으로 만든 삼각형 13종·사각형 4종", "평면": "밑면·윗면·옆면"}, disc="정사영은 꼭짓점을 수선의 발로 옮긴 도형임을 알고 넓이를 세는가", diff=3,
        params=[{"name": "f", "values": {"in": list(SD3_ROWS)}}], table={"key": "f", "rows": SD3_ROWS},
        derive={"ans": "VN/VD"}, cost=["W", "D", "H", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        figure=[{"fn": "wire", "args": {"kind": "box", "names": "ABCDEFGH", "w": "{W}", "h": "{H}", "d": "{D}", "segs": "{SEGS}", "right": "{RIGHT}"}}],
        sol1="정사영은 도형의 각 점에서 평면에 내린 수선의 발을 모은 도형이다. 직육면체에서 꼭짓점의 수선의 발은 그 평면 위의 꼭짓점이므로 {MAP}으로 옮기면 {KIND} {PROJ}가 된다.",
        sol2=[("{MAP} → 정사영은 {KIND} {PROJ}", "정사영 찾기"), ("{STEP}", "넓이"), ("정사영의 넓이 = {ans}", None, ("{ans}", "넓이"))],
        sol3=["정사영의 넓이가 원래 도형의 넓이보다 크지 않은지(S' = S cos θ ≤ S) 확인한다. 따라서 정사영의 넓이는 {ans}이다."],
        model="꼭짓점을 수선의 발로 옮기면({MAP}) 정사영은 {KIND} {PROJ}이고, {STEP}이다. 따라서 답은 {ans}이다.",
        rubric=[("정사영 찾기", 3, "정사영이 {KIND} {PROJ}임을 밝혔다.", "한 꼭짓점을 잘못 옮겼으면 1점."), ("넓이", 2, "{ans}{eul(ans)} 구했다.", "삼각형의 넓이를 2로 나누지 않았으면 1점.")],
        pitfalls=[("원래 도형의 넓이를 답함", "정사영 찾기", "불인정"), ("수선의 발을 다른 면의 꼭짓점으로 잡음", "정사영 찾기", "불인정"), ("삼각형 넓이의 1/2 누락", "넓이", "부분")], geo=True)


# 이면각 — (평면 1(대각선 단면), 평면 2(면), 평면각 (A_, V_, B_): V_ 는 교선 위, A_ ∈ 평면 1, B_ ∈ 평면 2, 직각삼각형 A_ B_ V_ 는 B_ 에서 직각)
SD4_KINDS = [("AFGD", "EFGH", ("A", "F", "E")), ("ABGH", "EFGH", ("B", "G", "F")), ("AFGD", "ABCD", ("F", "A", "B")), ("BCHE", "EFGH", ("B", "E", "F")),
             ("ACGE", "ABFE", ("C", "A", "B")), ("BDHF", "ABFE", ("D", "B", "A")), ("CDEF", "ABFE", ("D", "E", "A")), ("CDEF", "EFGH", ("D", "E", "H")),
             ("ABGH", "ABCD", ("G", "B", "C")), ("BCHE", "ABCD", ("E", "B", "A"))]


def _sd4_rows():
    out = {}
    P0 = _P3(3, 5, 7)
    for p1, p2, (A_, V_, B_) in SD4_KINDS:
        edge = "".join(v for v in p1 if v in p2)
        assert len(edge) == 2 and V_ in edge and A_ in p1 and B_ in p2 and _dot(P0, V_, A_, edge[0], edge[1]) == 0 and _dot(P0, V_, B_, edge[0], edge[1]) == 0 and _dot(P0, B_, A_, B_, V_) == 0, (p1, p2)
    for w, d, h in TRIPLES:
        P = _P3(w, d, h)
        for p1, p2, (A_, V_, B_) in SD4_KINDS:
            hyp = _ilen(P, A_, V_)
            if hyp is None:
                continue
            adj, opp = math.isqrt(_dist2(P, B_, V_)), math.isqrt(_dist2(P, A_, B_))
            edge = "".join(v for v in p1 if v in p2)
            cosv, tanv = Fraction(adj, hyp), Fraction(opp, adj)
            q = f"이면각 {w} {d} {h} {p1} {p2}"
            base = f"{_box_txt(w, d, h)}에서 두 평면 {p1}{_wa(p1)} {p2}가 이루는 각의 크기를 θ라 할 때"
            why = f"두 평면의 교선은 {edge}이고, 평면 {p1} 위의 {A_}{V_}와 평면 {p2} 위의 {B_}{V_}가 모두 교선 {edge}와 수직이므로 θ = ∠{A_}{V_}{B_}"
            segs = [s for s in (p1[i] + p1[(i + 1) % 4] for i in range(4)) if not _is_edge(s)]
            right = [[A_, B_, V_]]
            r = _row(q, cosv, Q=f"{base}, cos θ의 값을 구하시오.", W=w, D=d, H=h, SEGS=segs, RIGHT=right, WHY=why, ANG=f"∠{A_}{V_}{B_}",
                     STEP=f"직각삼각형 {A_}{B_}{V_}(∠{B_} = 90°)에서 {B_}{V_} = {adj}, {A_}{B_} = {opp}이므로 {A_}{V_} = [[sqrt(pow({adj},2) + pow({opp},2))]] = {hyp}이고 cos θ = {B_}{V_}/{A_}{V_} = [[frac({adj}, {hyp})]]", ASK="cos θ")
            if r: out[f"c{w}_{d}_{h}_{p1}{p2}"] = r
            r2 = _row(q, tanv, Q=f"{base}, tan θ의 값을 구하시오.", W=w, D=d, H=h, SEGS=segs, RIGHT=right, WHY=why, ANG=f"∠{A_}{V_}{B_}",
                      STEP=f"직각삼각형 {A_}{B_}{V_}(∠{B_} = 90°)에서 {B_}{V_} = {adj}, {A_}{B_} = {opp}이므로 tan θ = {A_}{B_}/{B_}{V_} = [[frac({opp}, {adj})]]" + (f" = {_fm(tanv)}" if Fraction(opp, adj).denominator != adj else ""), ASK="tan θ")
            if r2: out[f"t{w}_{d}_{h}_{p1}{p2}"] = r2
    return _pick(out, 330)


SD4_ROWS = _sd4_rows()


def sd_t4():
    return T(SD, 4, SD_B, title="직육면체에서 두 평면이 이루는 각(이면각)",
        skill="두 평면의 교선에 수직인 두 선분을 각 평면에서 찾아 이면각을 평면각으로 바꾸고, 직각삼각형에서 cos·tan 구하기", axis={"평면": "대각선 단면과 면 10종", "묻는 것": "cos θ / tan θ"}, disc="교선에 수직인 선분을 각 평면에서 잡아 평면각으로 옮기는가", diff=3,
        params=[{"name": "f", "values": {"in": list(SD4_ROWS)}}], table={"key": "f", "rows": SD4_ROWS},
        derive={"ans": "VN/VD"}, cost=["W", "D", "H", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}",
        figure=[{"fn": "wire", "args": {"kind": "box", "names": "ABCDEFGH", "w": "{W}", "h": "{H}", "d": "{D}", "segs": "{SEGS}", "right": "{RIGHT}"}}],
        sol1="이면각의 크기는 교선 위의 한 점에서 각 평면 안에 교선과 수직으로 그은 두 반직선이 이루는 각이다. {WHY}.",
        sol2=[("{WHY}", "평면각 찾기"), ("{STEP}", "직각삼각형"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["두 선분이 정말 교선과 수직인지(모서리와의 수직 관계) 확인한다. 따라서 {ASK} = {ans}이다."],
        model="{WHY}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("평면각 찾기", 3, "θ = {ANG}임을 밝혔다.", "교선에 수직이 아닌 선분으로 각을 잡았으면 인정하지 않는다."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "빗변·밑변을 바꿨으면 1점.")],
        pitfalls=[("교선에 수직이 아닌 선분으로 각을 잡음", "평면각 찾기", "불인정"), ("cos에서 빗변과 밑변을 바꿈", "값 구하기", "불인정"), ("빗변 계산(피타고라스) 실수", "값 구하기", "부분")], geo=True)


SD_SEED = SEED(SD, category="도형", title="직육면체 — 대각선·삼수선·정사영·이면각 (wire 도형)", unit_id="h3-3", concept_ids=["h3-3-08", "h3-3-09", "h3-3-10", "h3-3-11"],
               schema_name="공간도형(직육면체)", note="wire 도형(segs·right 확장) 위에 대각선·수선을 표시. 치수는 문면에(AB = w, AD = d, AE = h). 모든 길이·넓이는 좌표(_P3)로 계산해 검증(정수·분수).",
               templates=[sd_t1(), sd_t2(), sd_t3(), sd_t4()], geometry=True)


# ═══════════════════════════════════════════════════════════════════ 2. 이차곡선 그래프 (h3-3-01~03)
CF = "h3-3-conicfig"
CF_B = {**HS, "prereq": ["이차곡선의 정의"], "ops": ["이차곡선"], "traps": ["초점까지 거리 = 준선까지 거리", "거리의 합·차는 2a"], "tags": ["포물선", "타원", "쌍곡선", "그래프"]}
EL = [(5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12), (10, 8, 6), (10, 6, 8), (17, 15, 8), (17, 8, 15), (15, 12, 9), (15, 9, 12)]
HY = [(3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10)]


def _cf1_rows():
    out = {}
    for p in (1, 2, 3, 4, 5, 6):
        curves = [f"sqrt({4 * p}*x)", f"-sqrt({4 * p}*x)"]
        for t1, t2, sg in itertools.product((1, 2, 3), (1, 2, 3), (-1, 1)):
                if t1 == t2 or p * max(t1, t2) ** 2 > 40:
                    continue
                x1, y1 = p * t1 * t1, 2 * p * t1
                x2, y2 = p * t2 * t2, sg * 2 * p * t2      # B 는 x축 아래(sg = −1) 또는 위
                xhi = max(x1, x2) + 2; yh = max(abs(y1), abs(y2)) + 2
                lines = curves + [{"points": [[-p, -yh], [-p, yh]], "style": "dashed", "label": "l"}]
                pts = [{"coord": [p, 0], "name": "F"}, {"coord": [x1, y1], "name": "A"}, {"coord": [x2, y2], "name": "B"}]
                fig = {"XLO": -p - 1, "XHI": xhi, "YLO": -yh, "YHI": yh, "LINES": lines, "PTS": pts}
                base = f"그림과 같이 포물선 [[pow(y,2) = {4 * p}x]]의 초점을 F, 준선을 l이라 하고, 포물선 위의 두 점 A({x1}, {y1}), B({x2}, {y2})를 잡았다."
                law = f"포물선 위의 점에서 초점까지의 거리는 준선 x = {-p}까지의 거리와 같다"
                for kk, v, ask, step in (("sum", x1 + x2 + 2 * p, "AF + BF의 값", f"AF = {x1} + {p} = {x1 + p}, BF = {x2} + {p} = {x2 + p}이므로 AF + BF = {x1 + p} + {x2 + p}"),
                                          ("prod", (x1 + p) * (x2 + p), "AF × BF의 값", f"AF = {x1 + p}, BF = {x2 + p}이므로 AF × BF = {x1 + p} × {x2 + p}"),
                                          ("diff", abs(x1 - x2), "|AF − BF|의 값", f"AF = {x1 + p}, BF = {x2 + p}이므로 |AF − BF| = |{x1 + p} − {x2 + p}|")):
                    q = f"포물선 {p} {t1} {t2} {sg} {kk}"
                    r = _row(q, v, Q=f"{base} {ask}을 구하시오.", LAW=law, STEP=step, ASK=ask.replace("의 값", ""), P=p, **fig)
                    if r: out[f"{p}_{t1}_{t2}_{sg}_{kk}"] = r
    return _pick(out, 330)


CF1_ROWS = _cf1_rows()


def _cf_fig():
    return [{"fn": "coordplane", "args": {"x": ["{XLO}", "{XHI}"], "y": ["{YLO}", "{YHI}"], "lines": "{LINES}", "points": "{PTS}", "equal": True}}]


def cf_t1():
    return T(CF, 1, CF_B, title="포물선 그래프 — 초점까지의 거리",
        skill="포물선의 정의(초점까지의 거리 = 준선까지의 거리)로 그래프 위의 점과 초점 사이의 거리를 x좌표 + p로 구하기", axis={"p": "1~4", "묻는 것": "AF + BF / AF × BF / |AF − BF|"}, disc="초점 거리를 좌표로 직접 계산하지 않고 준선까지의 거리로 바꾸는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CF1_ROWS)}}], table={"key": "f", "rows": CF1_ROWS},
        derive={"ans": "VN/VD"}, cost=["P", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}", figure=_cf_fig(),
        sol1="{LAW}. 그림에서 점 A, B의 x좌표에 p를 더하면 각각 초점까지의 거리가 된다.",
        sol2=[("{LAW}", "포물선의 정의"), ("{STEP}", "거리 계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["한 점에 대해 좌표로 직접 거리를 계산해 같은 값이 나오는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP} = {ans}이다.",
        rubric=[("정의 적용", 3, "{STEP} 꼴로 세웠다.", "준선까지의 거리를 x좌표로만 두었으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("초점까지의 거리를 x좌표 그대로 둠(+p 누락)", "정의 적용", "불인정"), ("준선을 x = p로 둠", "정의 적용", "불인정"), ("덧셈·곱셈 실수", "값 구하기", "부분")])


def _cf2_rows():
    out = {}
    for a, b, c in EL:
        curves = [f"{b}*sqrt(1 - pow(x,2)/{a * a})", f"-{b}*sqrt(1 - pow(x,2)/{a * a})"]
        e = f"[[frac(pow(x,2), {a * a}) + frac(pow(y,2), {b * b}) = 1]]"
        base = f"그림과 같이 타원 {e}의 두 초점을 F({c}, 0), F'(-{c}, 0)이라 하자."
        fig0 = {"XLO": -a - 1, "XHI": a + 1, "YLO": -b - 1, "YHI": b + 1, "LINES": curves}
        # P: x = c 위의 점 (c, b²/a)
        py = Fraction(b * b, a)
        pts = [{"coord": [c, 0], "name": "F"}, {"coord": [-c, 0], "name": "F'"}, {"coord": [c, float(py)], "name": "P"}]
        q = f"타원 {a} {b} 위 초점"
        r = _row(q, py, Q=f"{base} 타원 위의 점 P의 x좌표가 {c}일 때, 선분 PF의 길이를 구하시오.", LAW="타원의 정의: PF + PF' = 2a, 그리고 PF ⊥ x축이면 PF'는 직각삼각형 PFF'의 빗변", STEP=f"PF = t라 하면 PF' = {2 * a} − t이고 (PF')² = PF² + FF'²에서 ({2 * a} − t)² = t² + {2 * c}², t = {_fm(py)}", ASK="PF", A=a, PTS=pts, **fig0)
        if r: out[f"v{a}_{b}"] = r
        # 둘레
        t = 0.8
        pts2 = [{"coord": [c, 0], "name": "F"}, {"coord": [-c, 0], "name": "F'"}, {"coord": [round(a * math.cos(t), 2), round(b * math.sin(t), 2)], "name": "P"}]
        r2 = _row(q, 2 * a + 2 * c, Q=f"{base} 타원 위의 점 P에 대하여 삼각형 PFF'의 둘레의 길이를 구하시오.", LAW="타원의 정의: PF + PF' = 2a (장축의 길이)", STEP=f"PF + PF' = {2 * a}, FF' = 2c = {2 * c}이므로 둘레는 {2 * a} + {2 * c}", ASK="삼각형 PFF'의 둘레", A=a, PTS=pts2, **fig0)
        if r2: out[f"p{a}_{b}"] = r2
        for k in range(a - c + 1, a + c):
            if k == a:
                continue
            r3 = _row(f"{q} {k}", 2 * a - k, Q=f"{base} 타원 위의 점 P에 대하여 PF = {k}일 때, 선분 PF'의 길이를 구하시오.", LAW="타원의 정의: PF + PF' = 2a (장축의 길이)", STEP=f"PF' = {2 * a} − PF = {2 * a} − {k}", ASK="PF'", A=a, PTS=pts2, **fig0)
            if r3: out[f"d{a}_{b}_{k}"] = r3
            r4 = _row(f"{q} {k}", 2 * a - k, Q=f"{base} 타원 위의 점 P에 대하여 PF' = {k}일 때, 선분 PF의 길이를 구하시오.", LAW="타원의 정의: PF + PF' = 2a (장축의 길이)", STEP=f"PF = {2 * a} − PF' = {2 * a} − {k}", ASK="PF", A=a, PTS=pts2, **fig0)
            if r4: out[f"e{a}_{b}_{k}"] = r4
    return _pick(out, 330)


CF2_ROWS = _cf2_rows()


def cf_t2():
    return T(CF, 2, CF_B, title="타원 그래프 — 초점까지의 거리와 삼각형의 둘레",
        skill="타원의 정의 PF + PF' = 2a와 초점의 위치를 그래프에서 읽어 거리·둘레를 구하기", axis={"(a, b, c)": "(5,4,3)·(13,12,5)·(10,8,6)…", "묻는 것": "PF(x = c) / 삼각형 PFF' 둘레 / PF'"}, disc="정의(합이 2a)를 쓰고 초점 사이 거리 2c를 더하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(CF2_ROWS)}}], table={"key": "f", "rows": CF2_ROWS},
        derive={"ans": "VN/VD"}, cost=["A", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}", figure=_cf_fig(),
        sol1="{LAW}. 그림의 두 초점과 점 P로 삼각형 PFF'를 생각한다.",
        sol2=[("{LAW}", "타원의 정의"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["PF, PF'가 모두 a − c 이상 a + c 이하인지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("정의 적용", 3, "{STEP} 꼴로 세웠다.", "합을 a로 두었으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("PF + PF' = a로 둠", "정의 적용", "불인정"), ("FF' = c로 둠(2c 누락)", "정의 적용", "부분"), ("이차방정식 풀이 실수", "값 구하기", "부분")])


def _cf3_rows():
    out = {}
    for a, b, c in HY:
        curves = [f"{b}*sqrt(pow(x,2)/{a * a} - 1)", f"-{b}*sqrt(pow(x,2)/{a * a} - 1)", {"expr": f"{b}*x/{a}", "style": "dashed"}, {"expr": f"-{b}*x/{a}", "style": "dashed"}]
        e = f"[[frac(pow(x,2), {a * a}) − frac(pow(y,2), {b * b}) = 1]]"
        base = f"그림과 같이 쌍곡선 {e}의 두 초점을 F({c}, 0), F'(-{c}, 0)이라 하자."
        xr = c + 3
        fig0 = {"XLO": -xr, "XHI": xr, "YLO": -(b * xr // a + 1), "YHI": b * xr // a + 1, "LINES": curves}
        px = a + 2
        pyv = b * math.sqrt(px * px / (a * a) - 1)
        pts = [{"coord": [c, 0], "name": "F"}, {"coord": [-c, 0], "name": "F'"}, {"coord": [px, round(pyv, 2)], "name": "P"}]
        q = f"쌍곡선 {a} {b}"
        for k in range(1, 2 * a + 4):
            r = _row(f"{q} {k}", k + 2 * a, Q=f"{base} 쌍곡선 위의 점 P가 x > 0인 부분에 있고 PF = {k}일 때, 선분 PF'의 길이를 구하시오.", LAW="쌍곡선의 정의: |PF − PF'| = 2a (주축의 길이), x > 0인 부분에서는 PF' − PF = 2a", STEP=f"PF' = PF + {2 * a} = {k} + {2 * a}", ASK="PF'", A=a, PTS=pts, **fig0)
            if r: out[f"d{a}_{b}_{k}"] = r
            r2 = _row(f"{q} {k} 둘레", 2 * k + 2 * a + 2 * c, Q=f"{base} 쌍곡선 위의 점 P가 x > 0인 부분에 있고 PF = {k}일 때, 삼각형 PFF'의 둘레의 길이를 구하시오.", LAW="쌍곡선의 정의: x > 0인 부분에서 PF' − PF = 2a, FF' = 2c", STEP=f"PF' = {k} + {2 * a} = {k + 2 * a}, FF' = {2 * c}이므로 둘레는 {k} + {k + 2 * a} + {2 * c}", ASK="삼각형 PFF'의 둘레", A=a, PTS=pts, **fig0)
            if r2: out[f"p{a}_{b}_{k}"] = r2
        py = Fraction(b * b, a)
        pts3 = [{"coord": [c, 0], "name": "F"}, {"coord": [-c, 0], "name": "F'"}, {"coord": [c, float(py)], "name": "P"}]
        r3 = _row(q, py, Q=f"{base} 쌍곡선 위의 점 P의 x좌표가 {c}일 때, 선분 PF의 길이를 구하시오.", LAW="쌍곡선의 정의: PF' − PF = 2a, 그리고 PF ⊥ x축이면 PF'는 직각삼각형 PFF'의 빗변", STEP=f"PF = t라 하면 PF' = t + {2 * a}이고 (t + {2 * a})² = t² + {2 * c}²에서 t = {_fm(py)}", ASK="PF", A=a, PTS=pts3, **fig0)
        if r3: out[f"v{a}_{b}"] = r3
    return _pick(out, 330)


CF3_ROWS = _cf3_rows()


def cf_t3():
    return T(CF, 3, CF_B, title="쌍곡선 그래프 — 초점까지의 거리와 삼각형의 둘레",
        skill="쌍곡선의 정의 |PF − PF'| = 2a와 점이 놓인 가지(x > 0)로 부호를 정해 거리·둘레를 구하기", axis={"(a, b, c)": "(3,4,5)·(5,12,13)·(6,8,10)…", "묻는 것": "PF' / 삼각형 PFF' 둘레 / PF(x = c)"}, disc="어느 초점이 더 먼지(가지)를 보고 차의 부호를 정하는가", diff=3,
        params=[{"name": "f", "values": {"in": list(CF3_ROWS)}}], table={"key": "f", "rows": CF3_ROWS},
        derive={"ans": "VN/VD"}, cost=["A", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}", figure=_cf_fig(),
        sol1="{LAW}. 그림에서 점 P는 초점 F에 가까운 가지 위에 있으므로 PF' 가 더 길다.",
        sol2=[("{LAW}", "쌍곡선의 정의"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["PF' − PF가 정확히 2a가 되는지, 삼각형 부등식 PF + PF' > FF'가 성립하는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("정의 적용", 3, "{STEP} 꼴로 세웠다.", "차의 부호를 반대로 두었으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "계산 실수면 1점.")],
        pitfalls=[("PF' = PF − 2a로 둠(가지 반대)", "정의 적용", "불인정"), ("차를 2c로 둠", "정의 적용", "불인정"), ("둘레에서 FF'를 빠뜨림", "값 구하기", "부분")])


CF_SEED = SEED(CF, category="도형", title="이차곡선 그래프 — 포물선·타원·쌍곡선의 초점까지의 거리 (coordplane 곡선)", unit_id="h3-3", concept_ids=["h3-3-01", "h3-3-02", "h3-3-03"],
               schema_name="이차곡선의 정의", note="coordplane 의 expr 곡선(±sqrt)·점선 준선/점근선·초점 표시. 수치는 문면에.",
               templates=[cf_t1(), cf_t2(), cf_t3()])


# ═══════════════════════════════════════════════════════════════════ 3. 벡터 그림 (h3-3-15·19)
VF = "h3-3-vecfig"
VF_B = {**HS, "prereq": ["평면좌표"], "ops": ["벡터"], "traps": ["합 벡터는 평행사변형의 대각선", "내적은 스칼라"], "tags": ["벡터", "합", "내적", "그림"]}


def _vf_fig():
    return [{"fn": "coordplane", "args": {"x": ["{XLO}", "{XHI}"], "y": ["{YLO}", "{YHI}"], "points": "{PTS}", "arrows": "{ARR}", "lines": "{LINES}", "equal": True}}]


def _rangeof(vs):
    xs = [0] + [v[0] for v in vs]; ys = [0] + [v[1] for v in vs]
    return {"XLO": min(xs) - 1, "XHI": max(xs) + 1, "YLO": min(ys) - 1, "YHI": max(ys) + 1}


def _vf1_rows():
    out = {}
    for _ in range(900):
        a = (rng.randint(-5, 6), rng.randint(-4, 6)); b = (rng.randint(-5, 6), rng.randint(-4, 6))
        if 0 in a or 0 in b or a == b or a[0] * b[1] == a[1] * b[0]:     # 축 위의 벡터(라벨 겹침)·평행 제외
            continue
        s = (a[0] + b[0], a[1] + b[1]); dd = (a[0] - b[0], a[1] - b[1])
        pts = []
        arr = [{"from": [0, 0], "to": list(a), "label": "a"}, {"from": [0, 0], "to": list(b), "label": "b"}, {"from": [0, 0], "to": list(s), "label": "a + b"}]
        lines = [{"points": [list(a), list(s)], "style": "dashed"}, {"points": [list(b), list(s)], "style": "dashed"}]
        fig = {**_rangeof([a, b, s]), "PTS": pts, "ARR": arr, "LINES": lines}
        base = f"그림과 같이 두 벡터 [[vec(a)]] = [[vcomp({a[0]}, {a[1]})]], [[vec(b)]] = [[vcomp({b[0]}, {b[1]})]]와 그 합 [[vec(a) + vec(b)]]을 좌표평면에 나타내었다."
        na2 = s[0] ** 2 + s[1] ** 2; nd2 = dd[0] ** 2 + dd[1] ** 2
        asks = [("sum", Fraction(s[0] + s[1]), "[[vec(a) + vec(b)]]의 모든 성분의 합", f"[[vec(a) + vec(b)]] = ({a[0]} + ({b[0]}), {a[1]} + ({b[1]})) = ({s[0]}, {s[1]})"),
                ("dot", Fraction(a[0] * b[0] + a[1] * b[1]), "[[dot(vec(a), vec(b))]]의 값", f"[[dot(vec(a), vec(b))]] = {a[0]} × ({b[0]}) + ({a[1]}) × ({b[1]})"),
                ("n2", Fraction(na2), "[[pow(abs(vec(a) + vec(b)), 2)]]의 값", f"[[vec(a) + vec(b)]] = ({s[0]}, {s[1]})이므로 |a + b|² = {s[0]}² + ({s[1]})²"),
                ("pm", Fraction(a[0] ** 2 + a[1] ** 2 - b[0] ** 2 - b[1] ** 2), "[[dot((vec(a) + vec(b)), (vec(a) − vec(b)))]]의 값", f"(a + b)·(a − b) = |a|² − |b|² = ({a[0] ** 2 + a[1] ** 2}) − ({b[0] ** 2 + b[1] ** 2})")]
        na = _isq(na2)
        if na: asks.append(("n", na, "[[abs(vec(a) + vec(b))]]의 값", f"[[vec(a) + vec(b)]] = ({s[0]}, {s[1]})이므로 |a + b| = [[sqrt({na2})]]"))
        for kk, v, ask, step in asks:
            q = f"벡터그림 {a} {b} {kk}"
            r = _row(q, v, Q=f"{base} {ask}을 구하시오.", STEP=step, ASK=ask.replace("의 값", "").replace("의 모든 성분의 합", "의 성분의 합"), **fig)
            if r: out[f"{a}_{b}_{kk}"] = r
    return _pick(out, 330)


VF1_ROWS = _vf1_rows()


def vf_t1():
    return T(VF, 1, VF_B, title="벡터의 합 그림 — 성분·크기·내적",
        skill="그림의 두 벡터와 평행사변형의 대각선(합)을 성분으로 옮겨 성분의 합·크기·내적을 계산하기", axis={"묻는 것": "합의 성분 합 / 내적 / |a + b|² / (a + b)·(a − b) / |a + b|", "성분": "−5~6"}, disc="합 벡터가 평행사변형의 대각선임을 그림에서 확인하고 성분으로 계산하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(VF1_ROWS)}}], table={"key": "f", "rows": VF1_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}", figure=_vf_fig(),
        sol1="그림에서 [[vec(a) + vec(b)]]는 두 벡터를 이웃한 변으로 하는 평행사변형의 대각선이다. 계산은 성분으로: 합은 성분끼리 더하고, 내적은 대응 성분의 곱의 합, 크기는 √(x² + y²)이다.",
        sol2=[("합 벡터 = 평행사변형의 대각선(점선 참고)", "그림 읽기"), ("{STEP}", "성분 계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["그림의 화살표 방향·길이와 계산한 성분의 부호·크기가 맞는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("성분 계산", 3, "{STEP} 꼴로 계산했다.", "성분 하나가 틀렸으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "부호 실수면 1점.")],
        pitfalls=[("합 벡터를 두 벡터의 크기의 합으로 봄", "성분 계산", "불인정"), ("내적을 벡터로 답함", "값 구하기", "불인정"), ("음수 성분의 부호 실수", "성분 계산", "부분")])


def _vf2_rows():
    out = {}
    T2 = [(3, 4), (4, 3), (-3, 4), (3, -4), (5, 12), (12, 5), (-5, 12), (8, 15), (15, 8), (6, 8), (8, -6), (-4, 3), (12, -5), (-8, 6)]
    for a in T2:
        for b in T2:
            if a == b or a == (-b[0], -b[1]):
                continue
            na, nb = math.isqrt(a[0] ** 2 + a[1] ** 2), math.isqrt(b[0] ** 2 + b[1] ** 2)
            dot = a[0] * b[0] + a[1] * b[1]
            if dot == 0:
                continue
            cs = Fraction(dot, na * nb)
            pts = []
            arr = [{"from": [0, 0], "to": list(a), "label": "a"}, {"from": [0, 0], "to": list(b), "label": "b"}]
            fig = {**_rangeof([a, b]), "PTS": pts, "ARR": arr, "LINES": []}
            base = f"그림과 같이 두 벡터 [[vec(a)]] = [[vcomp({a[0]}, {a[1]})]], [[vec(b)]] = [[vcomp({b[0]}, {b[1]})]]가 이루는 각의 크기를 θ라 하자."
            q = f"벡터각 {a} {b}"
            r = _row(q, cs, Q=f"{base} cos θ의 값을 구하시오.", STEP=f"[[dot(vec(a), vec(b))]] = {dot}, [[abs(vec(a))]] = {na}, [[abs(vec(b))]] = {nb}이므로 cos θ = [[frac({dot}, {na * nb})]]", ASK="cos θ", **fig)
            if r: out[f"c{a}_{b}"] = r
            # a 의 b 위로의 정사영 벡터의 크기 |a| cos θ = dot/|b| (양수일 때)
            if dot > 0:
                pr = Fraction(dot, nb)
                r2 = _row(q, pr, Q=f"{base} [[abs(vec(a))]] cos θ의 값을 구하시오.", STEP=f"[[abs(vec(a))]] cos θ = [[frac(dot(vec(a), vec(b)), abs(vec(b)))]] = [[frac({dot}, {nb})]]", ASK="|a| cos θ", **fig)
                if r2: out[f"p{a}_{b}"] = r2
    return _pick(out, 330)


VF2_ROWS = _vf2_rows()


def vf_t2():
    return T(VF, 2, VF_B, title="그림의 두 벡터가 이루는 각 — cos θ와 정사영 길이",
        skill="성분으로 내적과 크기를 구해 cos θ = a·b/(|a||b|)와 정사영의 길이 |a| cos θ = a·b/|b|를 계산하기", axis={"묻는 것": "cos θ / |a| cos θ", "벡터": "크기가 정수인 (3,4)·(5,12)·(8,15)…"}, disc="cos θ 공식의 분모가 두 크기의 곱임을 알고 정사영 길이를 내적으로 바꾸는가", diff=3,
        params=[{"name": "f", "values": {"in": list(VF2_ROWS)}}], table={"key": "f", "rows": VF2_ROWS},
        derive={"ans": "VN/VD"}, cost=["ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}", figure=_vf_fig(),
        sol1="두 벡터가 이루는 각 θ에 대하여 a·b = |a||b|cos θ이다. 그림의 두 화살표 사이의 각이 θ이고, 성분으로 내적과 크기를 구하면 cos θ가 나온다.",
        sol2=[("a·b = |a||b|cos θ", "내적과 각"), ("{STEP}", "계산"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["그림에서 각이 예각이면 cos θ > 0, 둔각이면 cos θ < 0인지 부호를 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("식 세우기", 3, "{STEP} 꼴로 세웠다.", "분모를 |a|²으로 두었으면 1점."), ("값 구하기", 2, "{ans}{eul(ans)} 구했다.", "약분 실수면 1점.")],
        pitfalls=[("cos θ의 분모를 |a| + |b|로 둠", "식 세우기", "불인정"), ("내적의 부호 실수로 예각·둔각이 바뀜", "값 구하기", "부분"), ("정사영 길이를 |b| cos θ로 둠", "식 세우기", "불인정")])


VF_SEED = SEED(VF, category="도형", title="벡터 그림 — 합의 평행사변형·내적·각 (coordplane 화살표)", unit_id="h3-3", concept_ids=["h3-3-15", "h3-3-18", "h3-3-19"],
               schema_name="평면벡터의 연산·내적", note="coordplane arrows 확장(09-15). 합 벡터는 점선 평행사변형과 함께.",
               templates=[vf_t1(), vf_t2()])


# ═══════════════════════════════════════════════════════════════════ 4. 삼각함수 그래프 (h2-1-10)
TG = "h2-1-trigfig"
TG_B = {**HS, "prereq": ["삼각함수의 그래프"], "ops": ["삼각함수"], "traps": ["주기 = 2π/b", "최댓값 = |a| + c"], "tags": ["삼각함수", "그래프", "주기"]}
PER = {"π": (2, Fraction(1), "pi"), "2π": (1, Fraction(2), "2pi"), "[[frac(pi, 2)]]": (4, Fraction(1, 2), "frac(pi, 2)"), "4π": (Fraction(1, 2), Fraction(4), "4pi"), "3π": (Fraction(2, 3), Fraction(3), "3pi")}


def _tg_rows(fn):
    out = {}
    for a in (1, 2, 3, 4):
        for c in (-2, -1, 0, 1, 2, 3):
            for ptxt, (b, tpi, pmk) in PER.items():
                M, m = a + c, -a + c
                bexp = f"{float(b):g}*x" if b != 1 else "x"
                expr = f"{a}*{fn}({bexp})" + (f"+{c}" if c > 0 else f"{c}" if c < 0 else "")
                T_ = float(tpi) * math.pi
                xhi = 2 * T_ + 0.3
                lines = [expr]
                pts = ([{"coord": [round(T_ / 4, 2), M], "name": "M"}, {"coord": [round(3 * T_ / 4, 2), m], "name": "m"}] if fn == "sin" else
                       [{"coord": [0, M], "name": "M"}, {"coord": [round(T_ / 2, 2), m], "name": "m"}])
                fig = {"XLO": -0.5, "XHI": round(xhi, 2), "YLO": m - 1, "YHI": M + 1, "LINES": lines, "PTS": pts}
                base = f"그림은 함수 y = a {fn} bx + c (a > 0, b > 0)의 그래프이다. 최댓값이 {M}, 최솟값이 {m}이고 주기가 {ptxt}일 때"
                law = f"최댓값 = a + c, 최솟값 = −a + c, 주기 = [[frac(2 pi, b)]]"
                step = f"a = [[frac({M} − ({m}), 2)]] = {a}, c = [[frac({M} + ({m}), 2)]] = {c}, b = [[frac(2pi, {pmk})]] = {_fm(b)}"
                for kk, v, ask in (("sum", a + b + c, "a + b + c"), ("prod", a * b * c, "abc"), ("ab", a * b, "ab"), ("bc", b + c, "b + c")):
                    if v == 0:
                        continue
                    q = f"{fn} {a} {c} {ptxt} {kk}"
                    r = _row(q, v, Q=f"{base}, 상수 a, b, c에 대하여 {ask}의 값을 구하시오.", LAW=law, STEP=step, ASK=ask, AV=a, BV=_fm(b), CV=c, **fig)
                    if r: out[f"{a}_{c}_{ptxt}_{kk}"] = r
    return _pick(out, 330)


TG1_ROWS = _tg_rows("sin")
TG2_ROWS = _tg_rows("cos")


def _tg_fig():
    return [{"fn": "coordplane", "args": {"x": ["{XLO}", "{XHI}"], "y": ["{YLO}", "{YHI}"], "lines": "{LINES}", "points": "{PTS}"}}]


def tg_t(no, fn, rows):
    return T(TG, no, TG_B, title=f"삼각함수의 그래프 — y = a {fn} bx + c의 최대·최소·주기에서 a, b, c",
        skill=f"y = a {fn} bx + c의 그래프에서 최댓값 a + c, 최솟값 −a + c, 주기 2π/b를 읽어 상수를 정하기", axis={"a": "1~4", "c": "−2~3", "주기": "π/2·π·2π·3π·4π", "묻는 것": "a + b + c / abc / ab / b + c"}, disc="최댓값·최솟값의 합과 차로 a, c를 가르고 주기에서 b를 구하는가", diff=2,
        params=[{"name": "f", "values": {"in": list(rows)}}], table={"key": "f", "rows": rows},
        derive={"ans": "VN/VD"}, cost=["AV", "CV", "ans"], verify=["ans*VD == VN"],
        q="{Q}", answer="{ans}", figure=_tg_fig(),
        sol1="{LAW}. 최댓값과 최솟값을 더하면 2c, 빼면 2a이고, 주기로 b를 구한다.",
        sol2=[("{LAW}", "그래프의 성질"), ("{STEP}", "a, b, c 구하기"), ("{ASK} = {ans}", None, ("{ans}", "{ASK}"))],
        sol3=["구한 a, b, c로 최댓값·최솟값·주기를 다시 계산해 그림과 맞는지 확인한다. 따라서 {ASK} = {ans}이다.", "{STEP}", "답 {ans}"],
        model="{LAW}. {STEP}이므로 {ASK} = {ans}이다.",
        rubric=[("a, c 구하기", 2, "a = {AV}, c = {CV}로 구했다.", "a와 c를 바꿨으면 1점."), ("b 구하기", 2, "b = {BV}로 구했다.", "b를 주기로 두었으면 인정하지 않는다."), ("값 구하기", 1, "{ans}{eul(ans)} 구했다.", "계산 실수면 인정하지 않는다.")],
        pitfalls=[("최댓값을 a로 봄(c 무시)", "a, c 구하기", "불인정"), ("b를 주기 그대로 둠", "b 구하기", "불인정"), ("주기 = 2π/b에서 b = 주기/2π로 뒤집음", "b 구하기", "불인정")])


TG_SEED = SEED(TG, category="함수", title="삼각함수의 그래프 — 최대·최소·주기에서 a, b, c (coordplane 곡선)", unit_id="h2-1", concept_ids=["h2-1-10"],
               schema_name="삼각함수의 그래프", note="coordplane expr 곡선으로 그래프를 그리고 최대·최소점을 M, m 으로 표시. 수치(최댓값·최솟값·주기)는 문면에.",
               templates=[tg_t(1, "sin", TG1_ROWS), tg_t(2, "cos", TG2_ROWS)])


if __name__ == "__main__":
    run(SD_SEED, CF_SEED, VF_SEED, TG_SEED)
