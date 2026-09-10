# genkit/figspec.py — 생성 문항 도형의 정규 스키마 (v1.6 제안) (v1.0)
#
# 코퍼스의 figure 인자는 느슨하다(문자열 숫자, "[a, b]" 문자열, 한국어 설명).
# 렌더러(figsvg.js)는 그걸 관대하게 받아 주지만, **생성 문항은 정규 인자만** 내보낸다.
# 여기가 그 관문이다 — 통과하지 못하면 그 문항은 저장하지 않는다(P3 오류보다 침묵).
#
# 정규 원칙
#   · 숫자는 숫자로 (문자열 "3" 금지)
#   · 좌표는 [x, y] 배열, 범위는 [lo, hi] 배열
#   · 라벨은 문자열, 수식 라벨은 [[ ]] 마커
#   · 기하 문항은 되도록 scene 으로 — 좌표를 직접 주면 수치변주 시 렌더가 확정적이다

from __future__ import annotations

NUM = (int, float)

# fn → (필수 키, 선택 키)
SPEC = {
    "scene":     ({"pts"}, {"segs", "circles", "marks", "shade", "labels", "axes", "nodot", "aspect_min"}),
    "numline":   ({"min", "max"}, {"points", "segments"}),
    "coordplane":({"x", "y"}, {"points", "lines", "curves", "circles", "labels", "rise_run", "run_label", "rise_label"}),   # rise_run: 기울기 삼각형 (SEEDSPEC·figsvg.js 와 정합, 09-09)
    "funcgraph": ({"expr"}, {"domain", "y_range", "points", "labels"}),
    "tri":       ({"v"}, {"sides", "angles", "marks"}),
    "quad":      ({"v"}, {"sides", "angles", "marks", "vertices"}),
    "polygon":   ({"n"}, {"labels", "vertices", "sides", "angles", "marks", "diagonals"}),
    "rect":      ({"w", "h"}, {"labels"}),
    "circle":    ({"r"}, {"center", "points"}),
    "sector":    ({"r", "angle"}, set()),
    "table":     ({"rows"}, {"head", "caption"}),
    "hist":      ({"bins", "counts"}, {"labels", "title"}),
    "scatter":   ({"points"}, {"x_label", "y_label", "title", "x_range", "y_range"}),
    "stemleaf":  ({"stems"}, {"leaves", "leaves_left", "leaves_right", "labels", "note"}),
    "boxplot":   ({"values"}, set()),
    "solid":     ({"kind"}, {"height", "radius", "labels", "w", "h", "d"}),
    "net":       ({"kind"}, {"labels"}),
    "wire":      ({"kind"}, {"names", "w", "h", "d"}),        # 이름 붙은 입체 골격 (위치관계) — box | triprism
    "crossing":  ({"angles"}, set()),
    "parallel":  ({"angles"}, set()),
    "venn":      ({"sets"}, {"shaded"}),
    "tree":      ({"levels"}, {"labels", "nodes"}),
    "point":     ({"x", "y"}, set()),
    # ── 해설 전용 도식 (손그림 수준). 문항 본문에는 쓰지 않는다.
    "journey":   ({"stops"}, {"legs", "total"}),
    "passing":   ({"obj", "span"}, {"total"}),
    "river":     (set(), {"stops", "span", "flow", "down", "up"}),           # 강 두 줄 — 순방향 위 · 역방향 아래
    "mountain":  (set(), {"base", "peak", "up", "down", "total"}),         # 우상향 초록 직선 — 오를 때 왼쪽 · 내려올 때 반대편
    "bar":       (set(), {"parts", "rows", "total", "name"}),
    "vessel":    (set(), {"parts", "rows", "total", "name", "kind", "capacity"}),   # 용기에 담긴 액체 — 농도·물탱크
    "steps":     ({"lines"}, set()),
}
# 해설에서만 허용 — 문항 figure 에 오면 오류
SOLUTION_ONLY = {"bar", "vessel", "steps"}      # journey·passing 은 상황 묘사라 문항에도 허용
# 생성 금지 — 그릴 스펙이 없거나 코퍼스 전용
FORBIDDEN = {"unsupported", "image", "space", "conic", "vecfig", "normcurve", "unitcircle"}

SOLID_KINDS = {
    "cube", "rectangular_prism", "cylinder", "cone", "sphere",
    "hemisphere", "triangular_prism", "square_pyramid",
}


def _isnum(v):
    return isinstance(v, NUM) and not isinstance(v, bool)


_VAR_OK = ("r", "h", "w", "a", "b", "c", "x", "y", "n", "l", "m", "s", "t", "k", "d", "\uc138\ub85c", "\uac00\ub85c")


def _numvar(v):
    """수치 또는 미지수 표시(짧은 변수명) — 구하는 값을 그림에 문자로 둘 때 허용."""
    if _isnum(v):
        return True
    return isinstance(v, str) and 1 <= len(v) <= 3 and v[0].isalpha()


def _coord(v):
    return isinstance(v, (list, tuple)) and len(v) == 2 and all(_isnum(x) for x in v)


def _rng(v):
    return isinstance(v, (list, tuple)) and len(v) == 2 and all(_isnum(x) for x in v) and v[0] <= v[1]


def check_figure_spec(figs, *, where="item") -> list:
    """생성 도형 검사 — 오류 문자열 목록(빈 목록이면 통과). where='solution'이면 해설 도식도 허용."""
    errs = []
    if figs in (None, []):
        return errs
    if not isinstance(figs, list):
        return ["figure는 배열이어야 함"]
    if len(figs) > 3:
        errs.append("도형은 문항당 3개 이하")
    for i, f in enumerate(figs):
        p = f"figure[{i}]"
        if not isinstance(f, dict) or "fn" not in f:
            errs.append(f"{p}: fn 없음")
            continue
        fn, args = f.get("fn"), f.get("args")
        if fn in SOLUTION_ONLY and where != "solution":
            errs.append(f"{p}: {fn}은 해설 전용 도식 — 문항 본문에는 쓸 수 없음")
            continue
        if fn in FORBIDDEN:
            errs.append(f"{p}: {fn}은 생성 금지(그릴 스펙 없음 / 코퍼스 전용)")
            continue
        if fn not in SPEC:
            errs.append(f"{p}: 미지 도형 함수 {fn}")
            continue
        if not isinstance(args, dict):
            errs.append(f"{p}: args 없음")
            continue
        req, opt = SPEC[fn]
        for k in req:
            if k not in args:
                errs.append(f"{p}: {fn}.{k} 누락")
        for k in args:
            if k not in req and k not in opt:
                errs.append(f"{p}: {fn}에 미정의 인자 {k} (v1.6은 정규 인자만 허용)")
        errs += _check_args(p, fn, args)
    return errs


def _check_args(p, fn, a):                                      # noqa: C901
    e = []
    if fn == "scene":
        pts = a.get("pts")
        if not isinstance(pts, dict) or not pts:
            return [f"{p}: scene.pts는 {{이름: [x,y]}} 형식"]
        for k, v in pts.items():
            if not _coord(v):
                e.append(f"{p}: scene.pts.{k}는 [x, y] 숫자쌍이어야 함")
        names = set(pts)
        for s in a.get("segs", []) or []:
            pair = (s[0], s[1]) if isinstance(s, list) else (s.get("a"), s.get("b"))
            if pair[0] not in names or pair[1] not in names:
                e.append(f"{p}: scene.segs에 없는 점 {pair}")
        for c in a.get("circles", []) or []:
            if not isinstance(c, dict) or not _isnum(c.get("r")):
                e.append(f"{p}: scene.circles[].r은 숫자")
            cc = c.get("c") if isinstance(c, dict) else None
            if not (isinstance(cc, str) and cc in names) and not _coord(cc):
                e.append(f"{p}: scene.circles[].c는 점 이름 또는 [x,y]")
        m = a.get("marks", {}) or {}
        if not isinstance(m, dict):
            e.append(f"{p}: scene.marks는 객체")
        else:
            for r in m.get("right", []) or []:
                if not (isinstance(r, list) and len(r) == 3 and all(x in names for x in r)):
                    e.append(f"{p}: marks.right는 [점,꼭짓점,점] 3개 이름")
            for g in m.get("arc", []) or []:
                if not (isinstance(g, dict) and g.get("at") in names):
                    e.append(f"{p}: marks.arc[].at은 점 이름")
    elif fn == "numline":
        if not (_isnum(a.get("min")) and _isnum(a.get("max"))):
            e.append(f"{p}: numline.min/max는 숫자")
        elif a["min"] >= a["max"]:
            e.append(f"{p}: numline.min < max 여야 함")
        for q in a.get("points", []) or []:
            if not isinstance(q, dict) or not _isnum(q.get("x")):
                e.append(f"{p}: numline.points[]는 {{x: 숫자, label: 문자열}}")
    elif fn == "coordplane":
        for k in ("x", "y"):
            if not _rng(a.get(k)):
                e.append(f"{p}: coordplane.{k}는 [lo, hi] 숫자쌍")
        for q in a.get("points", []) or []:
            c = q.get("coord") if isinstance(q, dict) else q
            if not _coord(c):
                e.append(f"{p}: coordplane.points[].coord는 [x, y]")
    elif fn == "funcgraph":
        if not isinstance(a.get("expr"), str) or not a["expr"].strip():
            e.append(f"{p}: funcgraph.expr는 식 문자열")
        if "domain" in a and not _rng(a["domain"]):
            e.append(f"{p}: funcgraph.domain은 [lo, hi]")
    elif fn in ("tri", "quad"):
        v = a.get("v") or a.get("vertices")
        need = 3 if fn == "tri" else 4
        if not (isinstance(v, list) and len(v) == need and all(isinstance(x, str) and x for x in v)):
            e.append(f"{p}: {fn}.v는 꼭짓점 이름 {need}개")
        for k in ("sides", "angles"):
            if k in a and not isinstance(a[k], list):
                e.append(f"{p}: {fn}.{k}는 배열")
    elif fn == "polygon":
        if not (isinstance(a.get("n"), int) and 3 <= a["n"] <= 12):
            e.append(f"{p}: polygon.n은 3~12 정수")
        d = a.get("diagonals")
        if d is not None and d != "fan" and not isinstance(d, list):
            e.append(f"{p}: polygon.diagonals는 'fan' 또는 변 이름 배열")
    elif fn == "rect":
        for k in ("w", "h"):
            if not _numvar(a.get(k)) or (_isnum(a.get(k)) and a[k] <= 0):
                e.append(f"{p}: rect.{k}는 양수 또는 미지수 표시")
    elif fn in ("circle", "sector"):
        if not _numvar(a.get("r")) or (_isnum(a.get("r")) and a["r"] <= 0):
            e.append(f"{p}: {fn}.r은 양수 또는 미지수 표시(한 글자 변수)")
        if fn == "sector":
            ang = a.get("angle")
            if not _numvar(ang) or (_isnum(ang) and not 0 < ang < 360):
                e.append(f"{p}: sector.angle은 0~360 또는 미지수 표시")
    elif fn == "table":
        rows = a.get("rows")
        if not (isinstance(rows, list) and rows and all(isinstance(r, list) for r in rows)):
            e.append(f"{p}: table.rows는 배열의 배열")
        elif len({len(r) for r in rows}) > 1:
            e.append(f"{p}: table.rows의 열 수가 서로 다름")
        elif "head" in a and isinstance(a["head"], list) and len(a["head"]) != len(rows[0]):
            e.append(f"{p}: table.head와 rows의 열 수 불일치")
    elif fn == "hist":
        b, c = a.get("bins"), a.get("counts")
        if not (isinstance(b, list) and isinstance(c, list) and len(b) == len(c)):
            e.append(f"{p}: hist.bins와 counts의 길이가 같아야 함")
        elif not all(_isnum(x) for x in c):
            e.append(f"{p}: hist.counts는 숫자 배열")
    elif fn == "scatter":
        ps = a.get("points")
        if not (isinstance(ps, list) and len(ps) >= 2):
            e.append(f"{p}: scatter.points는 2개 이상")
        elif not all(_coord(q) or (isinstance(q, dict) and _isnum(q.get("x")) and _isnum(q.get("y"))) for q in ps):
            e.append(f"{p}: scatter.points[]는 [x,y] 또는 {{x,y}}")
    elif fn == "boxplot":
        v = a.get("values")
        if not (isinstance(v, list) and len(v) >= 5 and all(_isnum(x) for x in v)):
            e.append(f"{p}: boxplot.values는 숫자 5개 이상")
    elif fn == "stemleaf":
        st = a.get("stems")
        if not (isinstance(st, list) and st):
            e.append(f"{p}: stemleaf.stems 필요")
        else:
            for k in ("leaves", "leaves_left", "leaves_right"):
                if k in a and (not isinstance(a[k], list) or len(a[k]) != len(st)):
                    e.append(f"{p}: stemleaf.{k}의 길이는 stems와 같아야 함")
    elif fn in ("solid", "net"):
        if a.get("kind") not in SOLID_KINDS:
            e.append(f"{p}: {fn}.kind는 {sorted(SOLID_KINDS)} 중 하나(한국어·자유표기 금지)")
    elif fn == "wire":
        kind = a.get("kind")
        if kind not in ("box", "triprism"):
            e.append(f"{p}: wire.kind는 box | triprism")
        nm = a.get("names")
        need = 8 if kind == "box" else 6
        if nm is not None and not (isinstance(nm, str) and len(nm) == need and nm.isalpha() and len(set(nm)) == need):
            e.append(f"{p}: wire.names는 서로 다른 영문 {need}글자")
        for k in ("w", "h", "d"):
            if k in a and not _isnum(a[k]):
                e.append(f"{p}: wire.{k}는 숫자")
    elif fn in ("crossing", "parallel"):
        ang = a.get("angles")
        if not (isinstance(ang, list) and ang):
            e.append(f"{p}: {fn}.angles는 배열")
    elif fn == "venn":
        s = a.get("sets")
        if not (isinstance(s, list) and 2 <= len(s) <= 4 and all(isinstance(x, str) for x in s)):
            e.append(f"{p}: venn.sets는 집합 이름 2~4개")
    elif fn == "tree":
        if not (isinstance(a.get("levels"), int) and 2 <= a["levels"] <= 5):
            e.append(f"{p}: tree.levels는 2~5 정수")
    elif fn == "point":
        if not (_isnum(a.get("x")) and _isnum(a.get("y"))):
            e.append(f"{p}: point.x/y는 숫자")
    elif fn == "journey":
        st = a.get("stops")
        if not (isinstance(st, list) and len(st) >= 2 and all(isinstance(x, str) for x in st)):
            e.append(f"{p}: journey.stops는 지점 이름 2개 이상")
        for g in a.get("legs", []) or []:
            if not isinstance(g, dict):
                e.append(f"{p}: journey.legs[]는 객체")
    elif fn == "passing":
        for k in ("obj", "span"):
            if not isinstance(a.get(k), dict):
                e.append(f"{p}: passing.{k}는 {{label, len}} 객체")
    elif fn in ("river", "mountain"):
        for k in ("up", "down", "flow"):
            if k in a and not isinstance(a[k], dict):
                e.append(f"{p}: {fn}.{k}는 {{label, sub}} 객체")
    elif fn in ("bar", "vessel"):
        rows = a.get("rows") if a.get("rows") else ([{"parts": a.get("parts")}] if a.get("parts") else None)
        if not rows:
            e.append(f"{p}: {fn}는 parts 또는 rows 필요")
        else:
            for r in rows:
                ps = (r or {}).get("parts")
                if not (isinstance(ps, list) and ps and all(_isnum((q or {}).get("value")) for q in ps)):
                    e.append(f"{p}: {fn}.parts[].value는 숫자")
                    break
        if fn == "vessel":
            if a.get("kind") not in (None, "beaker", "cylinder", "tank"):
                e.append(f"{p}: vessel.kind는 beaker | cylinder | tank")
            for r in rows or []:
                for q in (r or {}).get("parts") or []:
                    if isinstance(q, dict) and q.get("kind") not in (None, "water", "salt", "other"):
                        e.append(f"{p}: vessel.parts[].kind는 water | salt | other")
    elif fn == "steps":
        ls = a.get("lines")
        if not (isinstance(ls, list) and ls):
            e.append(f"{p}: steps.lines는 배열")
        else:
            for ln in ls:
                if isinstance(ln, dict):
                    if not isinstance(ln.get("text"), str):
                        e.append(f"{p}: steps.lines[] 객체에는 text 필요")
                    for m in ln.get("marks", []) or []:
                        if not (isinstance(m, dict) and m.get("on")):
                            e.append(f"{p}: steps.lines[].marks[]는 {{on, note}}")
                elif not isinstance(ln, str):
                    e.append(f"{p}: steps.lines[]는 문자열 또는 {{text, marks, hint}}")
    return e


def figure_fns(figs) -> list:
    return [f.get("fn") for f in (figs or []) if isinstance(f, dict)]


def is_geometry(figs, tags=None) -> bool:
    """기하 문항 판정 — 해설 단수(2단/3단)를 가르는 기준."""
    geo = {"scene", "tri", "quad", "polygon", "rect", "circle", "sector",
           "solid", "net", "wire", "crossing", "parallel", "point"}
    if any(f in geo for f in figure_fns(figs)):
        return True
    return bool(tags) and any(t in {"기하", "도형", "닮음", "합동", "각", "넓이", "부피"} for t in tags)
