# 기본기 해설 새 단원들이 함께 쓰는 도우미 — 세로셈(여러 자리 · 0이 있는 받아내림) · 띠 그림 · 시계 · 이름과 조사
from core import *
from fig import Fig, Col, mv, NL, ang_pt, fly

NAME = ["일", "십", "백", "천", "만", "십만"]
HEADS = ("일", "십", "백", "천", "만", "십만")
PEOPLE = ["민수", "지아", "하준", "서윤", "도윤", "하은", "준호", "수아", "예준", "지호", "유나", "시우", "다온", "로운", "채원", "건우"]

def eun(w): return J(w, "은", "는")
def iga(w): return J(w, "이", "가")
def eul(w): return J(w, "을", "를")
def wa(w): return J(w, "과", "와")
def ro(w): return RO(w)

def digits(n):
    return [int(c) for c in reversed(str(n))]

def col(ncol, top=200, heads=HEADS):
    f = Fig()
    cx = 400 if ncol <= 4 else 372
    dx = 118 if ncol <= 4 else 106
    C = Col(f, ncol=ncol, cx=cx, dx=dx, top=top, heads=heads)
    return f, C

def carry_fly(C, p, el):
    """받아올린 수가 일의 자리 합(예: 14의 1)에서 윗자리 위로 날아오른다 — 결과 숫자 왼쪽 옆에서 출발"""
    fly(el, C.x(p) - C.dx * 0.42 - C.x(p + 1), C.rows["r"] - C.rows["carry"], dl=420)
    return el

def carry_down(C, p, el):
    """맨 앞으로 받아올린 수를 답 줄로 그대로 내려 쓴다"""
    fly(el, 0, C.rows["carry"] - C.rows["r"], dl=200)
    return el

def nm0(p):
    return f"{NAME[p]}의 자리"

def col_add(a, b, with_fig=True, nm=nm0, ncol=None, show=None, heads=HEADS):
    """덧셈 세로셈 — 자리마다 한 줄(받아올림 메모) + 마지막 식. (그림 · 줄 · 답)
    nm: 자리 이름(소수 자리에 씀) · ncol: 칸 수 · show: (a 글자, b 글자, 답 글자) 마지막 식에 쓸 글자"""
    res = a + b
    n = len(str(res))
    f, C = col(ncol or max(n, len(str(a)), len(str(b))), heads=heads) if with_fig else (None, None)
    if C:
        C.num("a", a); C.num("b", b); C.op("+")
    da, db = digits(a), digits(b)
    lines, carry = [], 0
    for p in range(max(len(da), len(db))):
        x, y = (da[p] if p < len(da) else 0), (db[p] if p < len(db) else 0)
        s = x + y + carry
        parts = ([str(carry)] if carry else []) + ([str(x)] if p < len(da) else []) + ([str(y)] if p < len(db) else [])
        expr = " + ".join(parts)
        if len(parts) > 1:
            lines.append(L(f"{nm(p)} {expr} = {s}", memo=f"{nm(p + 1)}로 1 받아올림" if s >= 10 else None))
        else:
            lines.append(L(f"{nm(p)} 그대로 {s}"))
        if C:
            k = len(lines) - 1
            C.digit("r", p, s % 10, at=k)
            if s >= 10:
                carry_fly(C, p, C.digit("carry", p + 1, 1, at=k, c="red", z=34, dl=300))
        carry = 1 if s >= 10 else 0
    if carry:
        p = max(len(da), len(db))
        lines.append(L(f"{nm(p)} 1", memo="받아올린 1을 그대로 내려 써요"))
        if C:
            carry_down(C, p, C.digit("r", p, 1, at=len(lines) - 1))
    sa, sb, sr = show or (a, b, res)
    lines.append(L(f"{sa} + {sb} = {sr}"))
    return (f.out() if f else None), lines, res

def borrow_info(a, b):
    """(받아내림 횟수, 0을 건너 빌렸는지)"""
    da, db = digits(a), digits(b)
    cur, n, zero = da[:], 0, False
    for p in range(len(da)):
        y = db[p] if p < len(db) else 0
        if cur[p] < y:
            n += 1
            q = p + 1
            while cur[q] == 0:
                q += 1
                zero = True
            cur[q] -= 1
            for r in range(q - 1, p, -1):
                cur[r] = 9
            cur[p] += 10
    return n, zero

def carry_pos(a, b):
    da, db = digits(a), digits(b)
    c, out = 0, []
    for p in range(max(len(da), len(db))):
        s = (da[p] if p < len(da) else 0) + (db[p] if p < len(db) else 0) + c
        c = 1 if s >= 10 else 0
        if c:
            out.append(p)
    return out

def col_sub(a, b, with_fig=True, nm=nm0, ncol=None, show=None, heads=HEADS):
    """뺄셈 세로셈 — 못 빼면 왼쪽에서 빌려 오기(사이에 0이 있으면 0은 10이 되었다가 9)"""
    assert a > b >= 0
    res = a - b
    da, db = digits(a), digits(b)
    cur = da[:]
    n = len(da)
    f, C = col(ncol or n, heads=heads) if with_fig else (None, None)
    if C:
        C.num("a", a); C.num("b", b); C.op("−")
    top = {}

    def put_top(p, v, k, dl, dx=0, src=None):
        if not C:
            return
        if p in top:
            top[p]["un"] = k
        top[p] = C.digit("carry", p, v, at=k, c="red", z=30 if v >= 10 else 34, dl=dl, dx=dx)
        if src is not None:          # 빌려 온 10 — 빌려 준 자리 위에서 출발해 옆으로 건너온다
            fly(top[p], C.x(src) - (C.x(p) + dx), -40, dl=220)     # 줄인 숫자와 겹치지 않게 조금 위에서

    def strike(p, k, dl):
        if C and p not in top:
            C.f.cross(C.x(p), C.rows["a"] - 24, s=22, at=k, dl=dl)

    lines = []
    for p in range(n):
        x = cur[p]
        y = db[p] if p < len(db) else 0
        if x < y:
            q = p + 1
            while cur[q] == 0:
                q += 1
            if q == p + 1:
                lines.append(L(f"{nm(p)} {x} − {J(y, '은', '는')} 못 빼요", memo=f"{nm(q)}에서 10 빌려 오기"))
            else:
                lines.append(L(f"{nm(p)} {x} − {J(y, '은', '는')} 못 빼요", memo=f"바로 윗자리가 0 → {nm(q)}에서 빌려 오기"))
            k = len(lines) - 1
            strike(q, k, 0)
            put_top(q, cur[q] - 1, k, 200)
            cur[q] -= 1
            for r in range(q - 1, p, -1):
                strike(r, k, 300)
                put_top(r, 9, k, 450)
                cur[r] = 9
            if q > p + 1:
                lines.append(L(f"{nm(q)} {cur[q] + 1} → {cur[q]}, 사이의 0은 10 → 9", memo="빌려 준 10에서 다시 1을 빌려 주고 9"))
            x += 10
            cur[p] = x
            put_top(p, x, k, 600, dx=10, src=q)
            lines.append(L(f"{x} − {y} = {x - y}"))
        elif p < len(db):
            lines.append(L(f"{nm(p)} {x} − {y} = {x - y}", memo=(f"빌려 준 뒤 {x}" if x != da[p] else None)))
        else:
            if p == n - 1 and x == 0:
                continue
            lines.append(L(f"{nm(p)} 그대로 {x}", memo=(f"빌려 준 뒤 {x}" if x != da[p] else None)))
        if C and not (p == n - 1 and x - y == 0):
            C.digit("r", p, x - y, at=len(lines) - 1)
    sa, sb, sr = show or (a, b, res)
    lines.append(L(f"{sa} − {sb} = {sr}"))
    return (f.out() if f else None), lines, res

# ── 띠 그림(전체와 부분) ───────────────────────────────────────────────
def tape(f, parts, total=None, y=250, x0=60, x1=600, h=80, at_parts=None, at_total="q", cols=("teal", "gold", "coral", "sky")):
    """parts: [(값 · 글자)] — 값에 비례해 나눈 띠, total: 위에 괄호 + 글자"""
    tot = sum(max(v, 0.0001) for v, _ in parts)
    x = x0
    at_parts = at_parts or ["q"] * len(parts)
    boxes = []
    for i, (v, lab) in enumerate(parts):
        w = (x1 - x0) * max(v, 0.0001) / tot
        f.rect(x, y, w, h, c="ink", sw=3, f=cols[i % len(cols)], fo=0.35, at=at_parts[i])
        if lab:
            f.text(x + w / 2, y + h / 2 + 12, lab, z=30 if w > 70 else 24, at=at_parts[i], b=700)
        boxes.append((x, w))
        x += w
    if total:
        f.line(x0, y - 22, x1, y - 22, c="ink", w=2.5, at=at_total)
        f.line(x0, y - 34, x0, y - 10, c="ink", w=2.5, at=at_total)
        f.line(x1, y - 34, x1, y - 10, c="ink", w=2.5, at=at_total)
        f.text((x0 + x1) / 2, y - 46, total, z=30, at=at_total, b=700)
    return boxes

def eq_tape(f, n, unit_lab, total_lab, at_total="q", y=260, x0=60, x1=600, h=78, at_parts="q", hl_first=None):
    """똑같이 n칸 — 곱셈 · 나눗셈 띠"""
    w = (x1 - x0) / n
    for i in range(n):
        f.rect(x0 + i * w, y, w, h, c="ink", sw=3, f="teal" if i else "gold", fo=0.3 if i else 0.45, at=at_parts)
        if n <= 8 or i == 0:
            f.text(x0 + i * w + w / 2, y + h / 2 + 11, unit_lab, z=26 if n > 5 else 30, at=at_parts if i else (hl_first if hl_first is not None else at_parts), b=700)
    f.line(x0, y - 22, x1, y - 22, c="ink", w=2.5, at=at_total)
    f.line(x0, y - 34, x0, y - 10, c="ink", w=2.5, at=at_total)
    f.line(x1, y - 34, x1, y - 10, c="ink", w=2.5, at=at_total)
    f.text((x0 + x1) / 2, y - 46, total_lab, z=30, at=at_total, b=700)

# ── 시계 ──────────────────────────────────────────────────────────────
def clock(f, h, m, cx=330, cy=330, rr=250, at="q", hand_at=None, minor=True):
    k = rr / 250
    f.circ(cx, cy, rr, c="ink", sw=4 if k > 0.7 else 3, at=at)
    for i in range(60):
        ang = 90 - 6 * i
        big = i % 5 == 0
        if not big and not minor:
            continue
        p1, p2 = ang_pt(cx, cy, rr - 6 * k, ang), ang_pt(cx, cy, rr - (26 if big else 14) * k, ang)
        f.line(*p1, *p2, c="ink", w=(4 if big else 2) * max(k, 0.6), at=at)
    for i in range(12):
        tx, ty = ang_pt(cx, cy, rr - 58 * k, 90 - 30 * i)
        f.text(tx, ty + 12 * k, str(12 if i == 0 else i), z=34 * k if k > 0.7 else 22, c="soft", ho=False, at=at)
    ha = 90 - 30 * ((h % 12) + m / 60)
    ma = 90 - 6 * m
    ha_at = at if hand_at is None else hand_at
    f.line(cx, cy, *ang_pt(cx, cy, rr * 0.52, ha), c="ink", w=10 * max(k, 0.65), at=ha_at)
    f.line(cx, cy, *ang_pt(cx, cy, rr * 0.8, ma), c="coral", w=6 * max(k, 0.7), at=ha_at)
    f.dot(cx, cy, r=11 * max(k, 0.7), f="ink", at=at)

def clock_read(f, h, m, at_h, at_m, at_r=None, cx=330, cy=330, rr=250):
    """시계 읽기 움직임 — 짧은바늘이 지난 숫자 사이가 금빛으로 쓸리고(at_h),
    긴바늘 자리까지 12에서 시계 방향으로 쓸며 숫자마다 5, 10, 15 … 를 세고(at_m), 남은 작은 눈금은 한 칸씩 점(at_r)"""
    a_h = 90 - 30 * (h % 12)
    f.arc(cx, cy, rr * 0.62, a_h - 30, a_h, at=at_h, c="gold", sw=5, f="gold", fo=0.22, rv=True)
    n = m // 5
    if n:
        span = 30 * n
        sweep = max(340, min(760, 300 + span * 1.6))
        f.arc(cx, cy, rr * 0.86, 90 - span, 90, at=at_m, c="coral", sw=6, f="coral", fo=0.1, rv=True)
        for i in range(1, n + 1):
            x, y = ang_pt(cx, cy, rr + 38, 90 - 30 * i)
            f.text(x, y + 11, str(5 * i), z=30, c="coral", b=800, at=at_m, dl=int(sweep * i / n))
    r = m % 5
    if r and at_r is not None:
        a0 = 90 - 6 * m
        f.arc(cx, cy, rr * 0.86, a0, 90 - 30 * n, at=at_r, c="coral", sw=6, f="coral", fo=0.1, rv=True)
        for j in range(1, r + 1):
            x, y = ang_pt(cx, cy, rr - 10, 90 - 6 * (5 * n + j))
            f.dot(x, y, r=7, f="coral", at=at_r, dl=260 + j * 200)

def hm(t):
    """분(0시부터) → '3시 15분' """
    h, m = divmod(t, 60)
    h = h % 24
    hh = h if h <= 12 else h - 12
    if h == 0:
        hh = 12
    return f"{hh}시" + (f" {m}분" if m else "")

def dur(t):
    h, m = divmod(t, 60)
    return (f"{h}시간" if h else "") + (" " if h and m else "") + (f"{m}분" if m else "")

def ms(t):
    m, s = divmod(t, 60)
    return (f"{m}분" if m else "") + (" " if m and s else "") + (f"{s}초" if s else "")

def man(n):
    """큰 수를 만 · 억 · 조 단위로 읽기 — 230000000 → '2억 3000만'"""
    parts = []
    for unit, v in (("조", 10 ** 12), ("억", 10 ** 8), ("만", 10 ** 4)):
        q, n = divmod(n, v)
        if q:
            parts.append(f"{q}{unit}")
    if n:
        parts.append(str(n))
    return " ".join(parts) if parts else "0"

# ── 큰 수 읽기 · 자리 이름 ───────────────────────────────────────────────
PL = ["일", "십", "백", "천", "만", "십만", "백만", "천만", "억", "십억", "백억", "천억", "조", "십조", "백조", "천조"]
KR_D = "영일이삼사오육칠팔구"

def read4(n):
    s = ""
    for unit, v in (("천", 1000), ("백", 100), ("십", 10), ("", 1)):
        q, n = divmod(n, v)
        if q:
            s += ("" if (q == 1 and unit) else KR_D[q]) + unit
    return s

def read_kr(n):
    """34020 → '삼만 사천이십' · 10000 → '만' · 100000000 → '일억'"""
    if n == 0:
        return "영"
    parts = []
    for unit, v in (("조", 10 ** 12), ("억", 10 ** 8), ("만", 10 ** 4), ("", 1)):
        q, n = divmod(n, v)
        if q:
            parts.append(("" if (q == 1 and unit == "만") else read4(q)) + unit)
    return " ".join(parts)

def place_table(f, n, hl=None, at="q", hl_at=0, y=210, nd=None, hl_c="gold"):
    """자리 표 — 머리(자리 이름) + 숫자. hl: 빛낼 자리(0 = 일의 자리)"""
    s = str(n)
    nd = nd or len(s)
    s = s.rjust(nd)
    cw = min(118, 600 / nd)
    x0 = 330 - cw * nd / 2
    zh = 26 if cw >= 70 else (21 if cw >= 50 else 17)
    zd = 60 if cw >= 70 else (46 if cw >= 50 else 36)
    f.grid(x0, y, cw, 64, nd, 1, at=at, c="soft", sw=2)
    f.grid(x0, y + 64, cw, 100, nd, 1, at=at, c="ink", sw=3)
    for i in range(nd):
        p = nd - 1 - i
        cx = x0 + cw * i + cw / 2
        f.text(cx, y + 42, PL[p], z=zh, c="soft", at=at)
        if s[i] != " ":
            f.text(cx, y + 64 + 50 + zd * 0.36, s[i], z=zd, at=at, b=700)
    if hl is not None:
        i = nd - 1 - hl
        f.rect(x0 + cw * i + 3, y + 3, cw - 6, 158, c=hl_c, sw=5, rx=8, at=hl_at)
    return x0, cw

def compare_bars(f, a, b, la, lb, at="q", diff_at=0, x0=70, x1=600, y=230, h=70, diff_lab="?"):
    """두 양을 나란히 — 더 긴 쪽의 남는 부분(차)을 점선으로"""
    m = max(a, b)
    wa_, wb_ = (x1 - x0) * a / m, (x1 - x0) * b / m
    f.rect(x0, y, wa_, h, c="ink", sw=3, f="teal", fo=0.35, at=at)
    f.text(x0 - 12, y + h / 2 + 10, la, z=26, a="e", at=at, b=700)
    f.text(x0 + wa_ / 2, y + h / 2 + 11, str(a), z=30, at=at, b=700)
    f.rect(x0, y + h + 50, wb_, h, c="ink", sw=3, f="gold", fo=0.35, at=at)
    f.text(x0 - 12, y + h + 50 + h / 2 + 10, lb, z=26, a="e", at=at, b=700)
    f.text(x0 + wb_ / 2, y + h + 50 + h / 2 + 11, str(b), z=30, at=at, b=700)
    lo, hi = (wb_, wa_) if a > b else (wa_, wb_)
    yy = y + h + 50 if a > b else y
    f.rect(x0 + lo, yy, hi - lo, h, c="coral", sw=3, d=True, at=diff_at)
    f.text(x0 + (lo + hi) / 2, yy + h / 2 + 11, diff_lab, z=30, c="coral", at=diff_at, b=700)

def timeline(f, t0, t1, at="q", y=400, x0=60, x1=600, arcs_at=None, labs=None):
    """t0 → t1(분) — 정각마다 끊어 세는 시간 띠. arcs_at: 마디마다 나타날 때, labs: 마디 글자"""
    pts = [t0] + [h * 60 for h in range(t0 // 60 + 1, (t1 - 1) // 60 + 1)] + [t1]
    wts = []
    for i in range(len(pts) - 1):
        d = pts[i + 1] - pts[i]
        wts.append(1.0 if d < 60 else 1.5)
    tot = sum(wts)
    xs = [x0]
    for w in wts:
        xs.append(xs[-1] + (x1 - x0) * w / tot)
    f.line(x0 - 20, y, x1 + 26, y, c="ink", w=3, ar=1, at=at)
    for i, (t, X) in enumerate(zip(pts, xs)):
        f.line(X, y - 14, X, y + 14, c="ink", w=3, at=at)
        f.text(X, y + 50 + (26 if (i % 2 and len(pts) > 4) else 0), hm(t), z=22 if len(pts) > 4 else 24, c="soft" if 0 < i < len(pts) - 1 else "ink", at=at, b=700 if i in (0, len(pts) - 1) else 600)
    for i in range(len(pts) - 1):
        a, b = xs[i], xs[i + 1]
        hh = 46 + (b - a) * 0.18
        pp = [(a + (b - a) * k / 16, y - 10 - hh * 4 * (k / 16) * (1 - k / 16)) for k in range(17)]
        when = arcs_at[i] if arcs_at else 0
        f.poly(pp, c="teal", w=4, z=False, dr=True, ar=1, at=when)
        lab = labs[i] if labs else dur(pts[i + 1] - pts[i])
        f.text((a + b) / 2, y - 26 - hh, lab, z=24, c="teal", at=when, b=700)
    return pts

def unit_col(f, units, a, b, op, at="q"):
    """두 단위 세로셈 판 — 자리 x: 큰 단위 220, 작은 단위 470 · 줄 y: 머리 140 · a 250 · b 360 · 선 395 · 답 490"""
    XB, XS = 230, 470
    f.text(XB, 140, units[0], z=28, c="soft", at=at)
    f.text(XS, 140, units[1], z=28, c="soft", at=at)
    f.line(350, 160, 350, 520, c="soft", w=2, d=True, at=at)
    f.text(XB, 250, str(a[0]), z=58, at=at)
    f.text(XS, 250, str(a[1]), z=58, at=at)
    f.text(90, 360, op, z=58, at=at)
    f.text(XB, 360, str(b[0]), z=58, at=at)
    f.text(XS, 360, str(b[1]), z=58, at=at)
    f.line(60, 395, 620, 395, c="ink", w=4, at=at)
    return XB, XS

def ruler(f, total_mm, mark_mm, at="q", mark_at="q", y=330, x0=50, x1=610):
    """자 — 0부터 total_mm 까지(cm 큰 눈금 · mm 작은 눈금), mark_mm 만큼 금빛 막대"""
    s = (x1 - x0) / total_mm
    f.rect(x0 - 16, y - 10, (x1 - x0) + 32, 92, c="ink", sw=3, f="yellow", fo=0.18, rx=6, at=at)
    for i in range(total_mm + 1):
        X = x0 + i * s
        big = i % 10 == 0
        mid = i % 5 == 0
        f.line(X, y - 10, X, y - 10 + (40 if big else (26 if mid else 16)), c="ink", w=3 if big else 1.5, at=at)
        if big:
            f.text(X, y + 64, str(i // 10), z=24, c="soft", at=at)
    f.rect(x0, y - 70, mark_mm * s, 40, c="ink", sw=3, f="gold", fo=0.5, at=mark_at)

def jump_line(f, vals, fmt=str, at="q", jumps_at=None, y=380, x0=70, x1=590, jlab=None, z=22):
    """같은 간격 수직선 — vals 마다 눈금 · 글자, 사이를 뛰는 화살"""
    n = len(vals)
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    f.line(x0 - 40, y, x1 + 40, y, c="ink", w=3, ar=1, at=at)
    for i, (v, X) in enumerate(zip(vals, xs)):
        f.line(X, y - 12, X, y + 12, c="ink", w=3, at=at if i == 0 else (jumps_at[i - 1] if jumps_at else at))
        f.text(X, y + 46 + (28 if i % 2 else 0), fmt(v), z=z, c="ink" if i in (0, n - 1) else "soft", at=at if i == 0 else (jumps_at[i - 1] if jumps_at else at), b=700)
    for i in range(n - 1):
        a, b = xs[i], xs[i + 1]
        pp = [(a + (b - a) * k / 14, y - 10 - 70 * 4 * (k / 14) * (1 - k / 14)) for k in range(15)]
        w = jumps_at[i] if jumps_at else at
        f.poly(pp, c="teal", w=4, z=False, dr=True, ar=1, at=w)
        if jlab:
            f.text((a + b) / 2, y - 92, jlab, z=20, c="teal", at=w, b=700)
    return xs

def col_add3(a, b, c):
    """세 수 세로 덧셈 — 한 자리 합이 20을 넘으면 2를 받아올린다"""
    res = a + b + c
    n = len(str(res))
    f = Fig()
    C = Col(f, ncol=n, cx=400 if n <= 4 else 372, dx=118 if n <= 4 else 106, top=150, heads=HEADS)
    C.rows.update({"c": 150 + 280, "line": 150 + 312, "r": 150 + 405})
    C.num("a", a); C.num("b", b); C.num("c", c)
    xo = C.x(n - 1) - C.dx * 0.9
    f.text(xo, C.rows["c"], "+", z=C.z)
    f.line(C.x(n - 1) - C.dx * 1.25, C.rows["line"], C.x(0) + C.dx * 0.55, C.rows["line"], c="ink", w=4)
    ds = [digits(a), digits(b), digits(c)]
    lines, carry = [], 0
    for p in range(max(len(d) for d in ds)):
        xs = [d[p] for d in ds if p < len(d)]
        s = sum(xs) + carry
        parts = ([str(carry)] if carry else []) + [str(v) for v in xs]
        memo = f"{NAME[p + 1]}의 자리로 {s // 10} 받아올림" if s >= 10 else None
        lines.append(L(f"{NAME[p]}의 자리 {' + '.join(parts)} = {s}", memo=memo))
        k = len(lines) - 1
        C.digit("r", p, s % 10, at=k)
        if s >= 10:
            carry_fly(C, p, C.digit("carry", p + 1, s // 10, at=k, c="red", z=34, dl=300))
        carry = s // 10
    if carry:
        p = max(len(d) for d in ds)
        lines.append(L(f"{NAME[p]}의 자리 {carry}", memo="받아올린 수를 그대로 내려 써요"))
        carry_down(C, p, C.digit("r", p, carry, at=len(lines) - 1))
    lines.append(L(f"{a} + {b} + {c} = {res}"))
    return f, lines, res

# ── 곱셈 세로셈 ─────────────────────────────────────────────────────────
def col_mul(a, b):
    """(여러 자리) × (한 자리 · 두 자리) 세로셈 — 한 자리면 자리마다 올림, 두 자리면 부분곱 두 줄"""
    res = a * b
    n = len(str(res))
    f = Fig()
    lines = []
    if b < 10:
        C = Col(f, ncol=max(n, len(str(a))), cx=400 if n <= 4 else 372, dx=118 if n <= 4 else 106, top=200, heads=HEADS)
        C.num("a", a); C.num("b", b); C.op("×")
        da = digits(a)
        carry = 0
        for p in range(len(da)):
            s = da[p] * b + carry
            expr = f"{da[p]} × {b}" + (f" + {carry}" if carry else "")
            last = p == len(da) - 1
            lines.append(L(f"{NAME[p]}의 자리 {expr} = {s}", memo=(f"{NAME[p + 1]}의 자리로 {s // 10} 올림" if (s >= 10 and not last) else ("올린 수를 더했어요" if carry else None))))
            k = len(lines) - 1
            if last:
                for i, ch in enumerate(reversed(str(s))):
                    C.digit("r", p + i, ch, at=k)
            else:
                C.digit("r", p, s % 10, at=k)
                if s >= 10:
                    carry_fly(C, p, C.digit("carry", p + 1, s // 10, at=k, c="red", z=34, dl=300))
            carry = s // 10
        lines.append(L(f"{a} × {b} = {res}"))
        return f, lines, res
    b1, b2 = b % 10, b // 10
    assert b < 100 and b1
    p1, p2 = a * b1, a * b2
    dx = 92 if n <= 5 else 80
    C = Col(f, ncol=n, cx=380, dx=dx, top=140, z=54, heads=HEADS)
    C.rows.update({"a": 205, "b": 292, "line": 318, "p1": 392, "p2": 474, "line2": 500, "r": 578})
    C.num("a", a); C.num("b", b)
    f.text(C.x(n - 1) - dx * 0.4, 292, "×", z=54)
    f.line(C.x(n - 1) - dx * 0.75, 318, C.x(0) + dx * 0.55, 318, c="ink", w=4)
    lines.append(L(f"{a} × {b1} = {p1}", pre="일의 자리 수 곱하기"))
    C.num("p1", p1, at=0)
    lines.append(L(f"{a} × {b2 * 10} = {p2 * 10}", pre="십의 자리 수 곱하기", memo="한 칸 왼쪽부터 써요(끝의 0 생략)"))
    for i, ch in enumerate(reversed(str(p2))):
        C.digit("p2", i + 1, ch, at=1)
    C.digit("p2", 0, 0, at=1, c="soft", dl=200)
    f.line(C.x(n - 1) - dx * 0.75, 500, C.x(0) + dx * 0.55, 500, c="ink", w=3, at=2)
    lines.append(L(f"{p1} + {p2 * 10} = {res}", pre="두 곱을 더하기"))
    C.num("r", res, at=2)
    lines.append(L(f"{a} × {b} = {res}"))
    return f, lines, res

# ── 나눗셈 세로셈(긴 나눗셈) ─────────────────────────────────────────────
def long_div(n, d, est=False):
    """n ÷ d — 몫을 한 자리씩. (그림, 판서 줄, 몫, 나머지)"""
    s = str(n)
    nd = len(s)
    f = Fig()
    dx, rh, z = 70, 62, 48
    cur0, nz = 0, 0                     # 몫이 0이 아닌 자리 수 — 줄이 많으면 줄 사이를 좁혀 그림 칸 안에
    for ch in s:
        cur0 = cur0 * 10 + int(ch)
        if cur0 // d:
            nz += 1
            cur0 %= d
    rh = min(rh, (690 - 232) / (2 * max(nz, 1)))
    xd0 = 330 - dx * (nd - 1) / 2 + 40
    X = lambda i: xd0 + i * dx
    yq, ybar, yn = 150, 172, 232
    xb = X(0) - dx * 0.62
    f.text(xb - 22, yn, str(d), z=z, a="e")
    f.poly([(xb, ybar), (xb + 10, ybar + 30), (xb + 12, ybar + 52), (xb + 6, yn + 16)], z=False, c="ink", w=4)
    f.line(xb, ybar, X(nd - 1) + dx * 0.55, ybar, c="ink", w=4)
    for i, ch in enumerate(s):
        f.text(X(i), yn, ch, z=z)
    lines = []
    cur, started, row = 0, False, 0
    Q = ""
    for i, ch in enumerate(s):
        cur = cur * 10 + int(ch)
        q = cur // d
        if q == 0 and not started:
            continue
        if q == 0:
            Q += "0"
            lines.append(L(f"{cur}{'은' if _bat_num(cur) else '는'} {d}보다 작아요", memo=f"몫 자리에 0 — 다음 자리를 내려요"))
            f.text(X(i), yq, "0", z=z, c="coral", at=len(lines) - 1, b=700)
            if i < nd - 1:
                yr = yn + rh * (2 * row) if row else yn
                f.text(X(i + 1), yr, s[i + 1], z=z, at=len(lines) - 1, c="teal", dl=300)
            continue
        started = True
        Q += str(q)
        prod, rem = q * d, cur - q * d
        memo = f"{PL[nd - 1 - i]}의 자리에 몫 {q}"
        if est and d >= 10:
            memo = f"{d} × {q + 1} = {d * (q + 1)}{'은' if _bat_num(d * (q + 1)) else '는'} {cur}보다 커요 → 몫 {q}"
        lines.append(L(f"{d} × {q} = {prod}", pre=f"{cur} 안에 {iga(d)} 몇 번?", memo=memo))
        k = len(lines) - 1
        f.text(X(i), yq, str(q), z=z, c="coral", at=k, b=700)
        y1 = yn + rh * (2 * row + 1)
        for j, c2 in enumerate(reversed(str(prod))):
            f.text(X(i - j), y1, c2, z=z, at=k)
        f.line(X(i - len(str(prod)) + 1) - dx * 0.45, y1 + 12, X(i) + dx * 0.45, y1 + 12, c="ink", w=3, at=k)
        more = i < nd - 1
        lines.append(L(f"{cur} − {prod} = {rem}", memo=("다음 자리 숫자를 내려요" if more else ("나머지" if rem else "나누어떨어져요"))))
        k = len(lines) - 1
        y2 = yn + rh * (2 * row + 2)
        rs = str(rem) if (rem or not more) else ""
        for j, c2 in enumerate(reversed(rs)):
            f.text(X(i - j), y2, c2, z=z, at=k)
        if more:
            f.text(X(i + 1), y2, s[i + 1], z=z, at=k, c="teal", dl=300)
            f.line(X(i + 1), yn + 20, X(i + 1), y2 - 44, c="teal", w=2, d=True, ar=1, at=k, dl=200)
        row += 1
        cur = rem
    R_ = cur
    Qn = int(Q)
    assert Qn * d + R_ == n
    if R_:
        lines.append(L(f"{n} ÷ {d} = {Qn} … {R_}", memo=f"나머지 {R_} < {d}"))
        lines.append(L(f"{d} × {Qn} + {R_} = {n}", pre="검산"))
    else:
        lines.append(L(f"{n} ÷ {d} = {Qn}"))
    return f, lines, Qn, R_

def _bat_num(n):
    from core import _has_batchim
    return _has_batchim(str(n))

# ── 사다리 나눗셈(공약수로 나누기) ────────────────────────────────────────
def ladder(f, nums, divs, at0="q", x_num=330, gap=150, y0=170, rh=86, z=46):
    """nums 를 divs 로 차례로 나눈 사다리 — 줄 i 는 판서 i 번째에 나타난다. (마지막 줄 수, 줄 y 목록)"""
    k = len(nums)
    xs = [x_num - gap * (k - 1) / 2 + gap * j for j in range(k)]
    xl = xs[0] - gap * 0.55
    cur = list(nums)
    ys = []
    for j, v in enumerate(cur):
        f.text(xs[j], y0, str(v), z=z, at=at0)
    for i, dv in enumerate(divs):
        y = y0 + rh * i
        f.text(xl - 24, y, str(dv), z=z, a="e", at=i, c="coral", b=700)
        f.poly([(xl, y - 44), (xl + 8, y - 20), (xl + 8, y + 2), (xl + 2, y + 16)], z=False, c="ink", w=3, at=i)
        f.line(xl, y + 16, xs[-1] + gap * 0.4, y + 16, c="ink", w=3, at=i)
        cur = [v // dv for v in cur]
        for j, v in enumerate(cur):
            f.text(xs[j], y + rh, str(v), z=z, at=i, dl=250)
        ys.append(y)
    return cur, xs, xl, ys

# ── 혼합 계산 — 계산 순서 ─────────────────────────────────────────────────
OPS = {"+": lambda a, b: a + b, "−": lambda a, b: a - b, "×": lambda a, b: a * b, "÷": lambda a, b: a // b if b and a % b == 0 else None}

def reduce_steps(toks):
    """toks: 수(int) · 연산 · 괄호 목록 → 한 번에 하나씩 계산한 단계들 [(앞 식 toks, 계산한 자리 (i, j), 뒤 식 toks, 원래 구간)]"""
    cur = [(t, (i, i)) for i, t in enumerate(toks)]
    steps = []
    while len(cur) > 1:
        lo, hi = 0, len(cur)
        # 가장 안쪽 괄호
        opn = None
        for i, (t, _) in enumerate(cur):
            if t == "(":
                opn = i
            elif t == ")" and opn is not None:
                lo, hi = opn + 1, i
                break
        seg = cur[lo:hi]
        idx = next((i for i, (t, _) in enumerate(seg) if t in ("×", "÷")), None)
        if idx is None:
            idx = next((i for i, (t, _) in enumerate(seg) if t in ("+", "−")), None)
        i = lo + idx
        a, op, b = cur[i - 1][0], cur[i][0], cur[i + 1][0]
        v = OPS[op](a, b)
        if v is None or v < 0:
            return None
        span = (cur[i - 1][1][0], cur[i + 1][1][1])
        new = cur[:i - 1] + [(v, span)] + cur[i + 2:]
        j0, j1 = i - 1, i + 1
        # 괄호 안이 수 하나가 되면 괄호를 벗긴다
        if lo > 0 and hi - lo == 3:
            new = cur[:lo - 1] + [(v, (cur[lo - 1][1][0], cur[hi][1][1]))] + cur[hi + 1:]
            span = (cur[lo - 1][1][0], cur[hi][1][1])
            j0, j1 = lo - 1, hi
        steps.append(([t for t, _ in cur], (j0, j1), [t for t, _ in new], span, (i - 1, i + 1)))
        cur = new
    return steps

def toks_str(toks, hl=None):
    s = ""
    for i, t in enumerate(toks):
        t = str(t)
        s += "" if (i == 0 or toks[i - 1] == "(" or t == ")") else " "
        if hl and i == hl[0]:
            s += "‹"
        s += t
        if hl and i == hl[1]:
            s += "›"
    return s

def order_fig(f, toks, steps, y=250, at="q", z=40):
    """식을 한 줄로 쓰고, 계산하는 차례를 아래 호와 ①②③으로"""
    W = []
    for t in toks:
        if isinstance(t, int):
            W.append(z * 0.6 * len(str(t)) + 4)
        elif t in "()":
            W.append(z * 0.42)
        else:
            W.append(z * 0.95)
    tot = sum(W) + 10 * (len(W) - 1)
    sc = min(1.0, 600 / tot)
    zz = z * sc
    x = 330 - tot * sc / 2
    xs = []
    for t, w in zip(toks, W):
        xs.append((x, x + w * sc))
        f.text(x + w * sc / 2, y, str(t), z=zz, at=at)
        x += (w + 10) * sc
    NUMS = "①②③④⑤⑥⑦"
    deep = []
    for k, st in enumerate(steps):
        s0, s1 = st[3]
        a, b = xs[s0][0] + 2, xs[s1][1] - 2
        inner = sum(1 for d0 in deep if d0[0] >= s0 and d0[1] <= s1)
        dep = 34 + 30 * inner
        deep.append((s0, s1))
        pts = [(a + (b - a) * i / 16, y + 14 + dep * 4 * (i / 16) * (1 - i / 16)) for i in range(17)]
        f.poly(pts, c="teal", w=3.5, z=False, dr=True, at=k)
        f.text((a + b) / 2, y + 14 + dep + 34, NUMS[k], z=36, c="teal", at=k, b=700)
