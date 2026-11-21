# ashrain.out — 해설 그림 DSL (fig.py) — 무대 오른쪽 그림 칸 660 × 680 (frames/figdsl.jsx 가 그린다)
# 요소마다 at: "q"(문제와 함께) · "p"(방침) · 정수 i(판서 i번째 줄) · "a"(답) — 그때 나타난다.
#   hl: 그 줄일 때 금빛으로 빛남 · dl: 나타나는 늦춤(ms) · dr: 선을 그리듯 · un: 사라지는 때 · mv: {at, dx, dy, r, cx, cy} 옮기기
# 색 c/f 는 무대 팔레트 이름(ink soft red gold teal sky coral lilac leaf blue yellow) — 인쇄(흑백)에서는 회색 단계로 바꾼다.
import math

FW, FH = 660, 680

def R1(v):
    v = round(float(v), 1)
    return int(v) if v == int(v) else v

# 기본값은 적지 않는다(자료 크기) — figdsl.jsx 가 같은 기본값을 쓴다
DEF = {"at": "q", "c": "ink", "sw": 3, "a": "m", "b": 600, "ho": True, "z": 30, "dl": 0, "d": False, "ar": 0, "dr": False, "hl": False}
NUMK = ("x", "y", "x2", "y2", "w", "h", "r", "rx", "a0", "a1", "s", "cw", "ch")

class Fig:
    def __init__(self, note=None):
        self.els = []
        self.note = note

    def _a(self, el, **kw):
        for k, v in kw.items():
            if k == "ho":
                if v is False:
                    el["ho"] = 0
                continue
            if k == "z" and el["k"] == "P":       # 닫힌 꼴이 기본 — 열린 선(곡선 · 경로)만 z: 0
                if v is False:
                    el["z"] = 0
                continue
            if v is None or v is False:
                continue
            if k in DEF and v == DEF[k] and not (k == "c" and el["k"] == "D"):
                continue
            if k in NUMK and not isinstance(v, str):
                v = R1(v)
            if k == "sw" or k == "z" or k == "fo" or k == "o":
                v = R1(v)
            if v is True:
                v = 1
            el[k] = v
        self.els.append(el)
        return el

    def grid(self, x, y, cw, ch, nx, ny, at="q", c="ink", sw=3, rx=0, f=None, fo=None, dl=0, un=None, hl=False, o=None):
        """nx × ny 칸 격자(테두리 + 칸 선) — 10칸 상자 · 자리 표 · 분수 막대"""
        return self._a({"k": "G"}, x=x, y=y, cw=cw, ch=ch, nx=nx, ny=ny, at=at, c=c, sw=sw, rx=rx, f=f, fo=fo, dl=dl, un=un, hl=hl, o=o)

    def rod(self, x, y, w=26, h=230, n=10, at="q", c="ink", f="gold", fo=0.35, dl=0, un=None, hl=False, o=None):
        """십 모형 막대(작은 칸 n 개)"""
        return self._a({"k": "B"}, x=x, y=y, w=w, h=h, n=n, at=at, c=c, f=f, fo=fo, dl=dl, un=un, hl=hl, o=o)

    def line(self, x1, y1, x2, y2, at="q", c="ink", w=3, d=False, ar=0, dr=False, hl=False, dl=0, un=None, o=None):
        return self._a({"k": "L"}, x=x1, y=y1, x2=x2, y2=y2, at=at, c=c, sw=w, d=d, ar=ar, dr=dr, hl=hl, dl=dl, un=un, o=o)

    def poly(self, pts, at="q", c="ink", w=3, f=None, fo=None, z=True, d=False, dr=False, hl=False, dl=0, un=None, ar=0, o=None):
        return self._a({"k": "P", "pts": [[R1(x), R1(y)] for x, y in pts]}, at=at, c=c, sw=w, f=f, fo=fo, z=z, d=d, dr=dr, hl=hl, dl=dl, un=un, ar=ar, o=o)

    def rect(self, x, y, w, h, at="q", c="ink", sw=3, f=None, fo=None, rx=0, d=False, hl=False, dl=0, un=None, o=None):
        return self._a({"k": "R"}, x=x, y=y, w=w, h=h, at=at, c=c, sw=sw, f=f, fo=fo, rx=rx, d=d, hl=hl, dl=dl, un=un, o=o)

    def circ(self, x, y, r, at="q", c="ink", sw=3, f=None, fo=None, d=False, hl=False, dl=0, un=None, o=None):
        return self._a({"k": "C"}, x=x, y=y, r=r, at=at, c=c, sw=sw, f=f, fo=fo, d=d, hl=hl, dl=dl, un=un, o=o)

    def dot(self, x, y, r=8, f="ink", c=None, at="q", dl=0, hl=False, un=None, sw=None, o=None):
        return self._a({"k": "D"}, x=x, y=y, r=r, f=f, c=c, at=at, dl=dl, hl=hl, un=un, sw=sw, o=o)

    def text(self, x, y, s, z=30, c="ink", a="m", b=600, at="q", ho=True, dl=0, hl=False, un=None, o=None):
        return self._a({"k": "T", "s": str(s)}, x=x, y=y, z=z, c=c, a=a, b=b, at=at, ho=ho, dl=dl, hl=hl, un=un, o=o)

    def arc(self, x, y, r, a0, a1, at="q", c="gold", sw=3, f=None, fo=None, hl=False, dl=0, un=None, o=None):
        """각 표시 — a0 → a1 (도, 동쪽 0 · 시계 반대 방향 +)"""
        return self._a({"k": "A"}, x=x, y=y, r=r, a0=a0, a1=a1, at=at, c=c, sw=sw, f=f, fo=fo, hl=hl, dl=dl, un=un, o=o)

    def cross(self, x, y, s=12, at=0, c="red", w=4, dl=0, un=None):
        """× 지우기 표시"""
        return self._a({"k": "X"}, x=x, y=y, s=s, at=at, c=c, sw=w, dl=dl, un=un)

    def out(self):
        d = {"kind": "dsl", "els": self.els}
        if self.note:
            d["note"] = self.note
        return d

def mv(el, at, dx=0, dy=0, r=0, cx=0, cy=0):
    m = {"at": at}
    if dx:
        m["dx"] = R1(dx)
    if dy:
        m["dy"] = R1(dy)
    if r:
        m["r"] = R1(r)
        m["cx"] = R1(cx)
        m["cy"] = R1(cy)
    el["mv"] = m
    return el

# ── 좌표평면 ────────────────────────────────────────────────────────────────
class Plane:
    """수학 좌표 → 그림 칸. xr, yr: 보이는 범위, box: (x0, y0, x1, y1) 그림 칸 안 자리"""
    def __init__(self, fig, xr, yr, box=(40, 40, 620, 640), square=True):
        self.f = fig
        self.xr, self.yr = xr, yr
        x0, y0, x1, y1 = box
        sx = (x1 - x0) / (xr[1] - xr[0])
        sy = (y1 - y0) / (yr[1] - yr[0])
        if square:
            s = min(sx, sy)
            sx = sy = s
        self.sx, self.sy = sx, sy
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        self.ox = cx - sx * (xr[0] + xr[1]) / 2
        self.oy = cy + sy * (yr[0] + yr[1]) / 2

    def X(self, v):
        return self.ox + self.sx * v

    def Y(self, v):
        return self.oy - self.sy * v

    def P(self, x, y):
        return (self.X(x), self.Y(y))

    def axes(self, at="q", grid=1, labels=True, lab_step=None, ticks=True, c="ink", xn="x", yn="y", ystep=None, ygrid=None):
        f = self.f
        (a, b), (p, q) = self.xr, self.yr
        ystep = ystep or lab_step
        ygrid = ygrid or grid
        if grid:
            k = math.ceil(a / grid) * grid
            while k <= b + 1e-9:
                if abs(k) > 1e-9:
                    f.line(self.X(k), self.Y(q), self.X(k), self.Y(p), at=at, c="soft", w=1, o=0.35)
                k += grid
            k = math.ceil(p / ygrid) * ygrid
            while k <= q + 1e-9:
                if abs(k) > 1e-9:
                    f.line(self.X(a), self.Y(k), self.X(b), self.Y(k), at=at, c="soft", w=1, o=0.35)
                k += ygrid
        f.line(self.X(a), self.Y(0), self.X(b), self.Y(0), at=at, c=c, w=3, ar=1)
        f.line(self.X(0), self.Y(p), self.X(0), self.Y(q), at=at, c=c, w=3, ar=1)
        f.text(self.X(b) - 10, self.Y(0) + 36, xn, z=30, at=at, c=c)
        f.text(self.X(0) + 22, self.Y(q) + 16, yn, z=30, at=at, c=c)
        f.text(self.X(0) - 16, self.Y(0) + 30, "O", z=26, at=at, c="soft", a="e")
        if labels and lab_step:
            k = math.ceil(a / lab_step) * lab_step
            while k <= b - lab_step * 0.5:
                if abs(k) > 1e-9:
                    f.text(self.X(k), self.Y(0) + 30, ("−" if k < 0 else "") + str(abs(int(k)) if float(k).is_integer() else abs(k)), z=22, at=at, c="soft")
                k += lab_step
            k = math.ceil(p / ystep) * ystep
            while k <= q - ystep * 0.5:
                if abs(k) > 1e-9:
                    f.text(self.X(0) - 10, self.Y(k) + 8, ("−" if k < 0 else "") + str(abs(int(k)) if float(k).is_integer() else abs(k)), z=22, at=at, c="soft", a="e")
                k += ystep

    def curve(self, fn, x0=None, x1=None, n=80, at="q", c="sky", w=4.5, dr=True, d=False, hl=False, clip=True):
        x0 = self.xr[0] if x0 is None else x0
        x1 = self.xr[1] if x1 is None else x1
        pts, segs = [], []
        for i in range(n + 1):
            x = x0 + (x1 - x0) * i / n
            try:
                y = fn(x)
            except (ZeroDivisionError, ValueError):
                y = None
            if y is None or (clip and not (self.yr[0] - 0.05 <= y <= self.yr[1] + 0.05)):
                if len(pts) > 1:
                    segs.append(pts)
                pts = []
                continue
            pts.append(self.P(x, y))
        if len(pts) > 1:
            segs.append(pts)
        return [self.f.poly(s, at=at, c=c, w=w, z=False, dr=dr, d=d, hl=hl) for s in segs]

    def lineq(self, m, b, at="q", c="sky", w=4.5, dr=True, d=False, hl=False):
        """y = mx + b 를 보이는 칸으로 자른 선"""
        (a, bb), (p, q) = self.xr, self.yr
        pts = []
        for x in (a, bb):
            y = m * x + b
            if p <= y <= q:
                pts.append((x, y))
        if m != 0:
            for y in (p, q):
                x = (y - b) / m
                if a <= x <= bb:
                    pts.append((x, y))
        pts = sorted(set((round(x, 6), round(y, 6)) for x, y in pts))
        if len(pts) < 2:
            return None
        A, B = pts[0], pts[-1]
        return self.f.line(*self.P(*A), *self.P(*B), at=at, c=c, w=w, dr=dr, d=d, hl=hl)

    def pt(self, x, y, at="q", f="ink", r=8, label=None, pos="ne", z=26, c="ink", dl=0, hl=False):
        X, Y = self.P(x, y)
        self.f.dot(X, Y, r=r, f=f, at=at, dl=dl, hl=hl)
        if label:
            dx, dy, a = {"ne": (12, -14, "s"), "nw": (-12, -14, "e"), "se": (12, 30, "s"), "sw": (-12, 30, "e"),
                         "n": (0, -18, "m"), "s": (0, 36, "m"), "e": (14, 9, "s"), "w": (-14, 9, "e")}[pos]
            self.f.text(X + dx, Y + dy, label, z=z, c=c, a=a, at=at, dl=dl)


# ── 10칸 상자 · 십 모형 ─────────────────────────────────────────────────────
def ten_frame(f, x0, y0, cell=96, at="q", c="soft"):
    """2줄 × 5칸 — 칸 가운데 좌표 10개(윗줄 왼쪽부터)"""
    f.grid(x0, y0, cell, cell, 5, 2, at=at, c=c, sw=3, rx=8)
    return [(x0 + cell * (i % 5) + cell / 2, y0 + cell * (i // 5) + cell / 2) for i in range(10)]

def rod(f, x, y, at="q", w=26, h=230, c="ink", f_="gold", fo=0.35, dl=0, un=None, hl=False):
    return f.rod(x, y, w=w, h=h, at=at, c=c, f=f_, fo=fo, dl=dl, un=un, hl=hl)

def cube(f, x, y, at="q", s=23, c="ink", f_="teal", fo=0.4, dl=0, un=None, hl=False):
    return f.rect(x, y, s, s, at=at, c=c, sw=2.5, f=f_, fo=fo, dl=dl, un=un, hl=hl)


# ── 세로셈 ─────────────────────────────────────────────────────────────────
class Col:
    """세로셈 판: 자리마다 x, 줄마다 y. digit(행, 자리, 글자, at) 로 쓴다. 자리 0 = 일의 자리."""
    def __init__(self, f, ncol=3, cx=400, dx=118, top=200, z=66, heads=("일", "십", "백", "천")):
        self.f, self.ncol, self.cx, self.dx, self.z = f, ncol, cx, dx, z
        self.top = top
        self.rows = {"carry": top - 36, "a": top + 70, "b": top + 175, "line": top + 205, "r": top + 300}
        for p in range(ncol):
            f.text(self.x(p), top - 92, heads[p], z=24, c="soft", at="q")

    def x(self, p):
        return self.cx - p * self.dx + self.dx * (self.ncol - 1) / 2

    def num(self, row, n, at="q", c="ink", z=None, dl=0, skip=()):
        s = str(n)
        for i, ch in enumerate(reversed(s)):
            if i in skip:
                continue
            self.f.text(self.x(i), self.rows[row], ch, z=z or self.z, c=c, at=at, b=600, dl=dl)

    def digit(self, row, p, ch, at=0, c="ink", z=None, dy=0, dx=0, dl=0):
        y = self.rows[row] if isinstance(row, str) else row
        return self.f.text(self.x(p) + dx, y + dy, str(ch), z=z or self.z, c=c, at=at, b=600 if c == "ink" else 700, dl=dl)

    def op(self, sym, at="q"):
        self.f.text(self.x(self.ncol - 1) - self.dx * 0.9, self.rows["b"], sym, z=self.z, at=at)
        x0, x1 = self.x(self.ncol - 1) - self.dx * 1.25, self.x(0) + self.dx * 0.55
        self.f.line(x0, self.rows["line"], x1, self.rows["line"], at=at, c="ink", w=4)


# ── 분수 막대 ───────────────────────────────────────────────────────────────
def fbar(f, x, y, w, h, d, at="q", c="ink", sw=3):
    """1을 d 칸으로 나눈 막대 — 칸 왼쪽 x 목록"""
    f.grid(x, y, w / d, h, d, 1, at=at, c=c, sw=sw, rx=4)
    return [x + w * i / d for i in range(d)]

def ffill(f, x, y, w, h, d, i0, n, col, at, fo=0.55, dl=0, step=90):
    """막대의 i0 번째 칸부터 n 칸 칠하기"""
    cw = w / d
    for i in range(n):
        f.rect(x + cw * (i0 + i) + 2, y + 2, cw - 4, h - 4, at=at, c="none", f=col, fo=fo, dl=dl + i * step)

# ── 각 · 다각형 ─────────────────────────────────────────────────────────────
def ang_pt(cx, cy, r, deg):
    return (cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg)))

def dir_deg(p, q):
    """p 에서 q 쪽 방향(도, 동쪽 0 · 시계 반대 +, 화면 y 는 아래로)"""
    return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0])) % 360

def angle_mark(f, V, A, B, r=46, at="q", c="gold", label=None, z=28, lr=None, f_="gold", fo=0.22, hl=False, dl=0):
    """꼭짓점 V 에서 VA → VB 사이 작은 쪽 각 표시 + 이름"""
    a0, a1 = dir_deg(V, A), dir_deg(V, B)
    d = (a1 - a0) % 360
    if d > 180:
        a0, a1 = a1, a0
        d = 360 - d
    if abs(d - 90) < 0.5 and label is None:
        s = r * 0.42
        u = ang_pt(0, 0, s, a0); v = ang_pt(0, 0, s, a1)
        f.poly([(V[0] + u[0], V[1] + u[1]), (V[0] + u[0] + v[0], V[1] + u[1] + v[1]), (V[0] + v[0], V[1] + v[1])], at=at, c=c, w=3, z=False, dl=dl)
        return
    f.arc(V[0], V[1], r, a0, a0 + d, at=at, c=c, sw=3, f=f_, fo=fo, hl=hl, dl=dl)
    if label is not None:
        mid = a0 + d / 2
        lx, ly = ang_pt(V[0], V[1], lr or (r + 30 + max(0, 30 - d) * 0.9), mid)
        f.text(lx, ly + z * 0.34, label, z=z, c=c if c != "gold" else "ink", at=at, b=700, dl=dl)

# ── 수직선 ─────────────────────────────────────────────────────────────────
class NL:
    def __init__(self, f, lo, hi, y=360, x0=40, x1=620, step=1, at="q", lab_step=1, fr_lab=None, z=26):
        self.f, self.lo, self.hi, self.y, self.x0, self.x1 = f, lo, hi, y, x0, x1
        f.line(x0 - 10, y, x1 + 14, y, at=at, c="ink", w=3, ar=1)
        k = math.ceil(lo / step) * step
        i = 0
        while k <= hi + 1e-9:
            X = self.X(k)
            big = abs(k / lab_step - round(k / lab_step)) < 1e-9
            f.line(X, y - (12 if big else 7), X, y + (12 if big else 7), at=at, c="ink", w=3 if big else 2)
            if big:
                kk = int(round(k)) if abs(k - round(k)) < 1e-9 else k
                f.text(X, y + 44, ("−" if kk < 0 else "") + str(abs(kk)), z=z, c="soft", at=at)
            k += step
            i += 1

    def X(self, v):
        return self.x0 + (self.x1 - self.x0) * (float(v) - self.lo) / (self.hi - self.lo)

    def pt(self, v, label=None, at="q", f_="gold", up=True, z=30, r=10, dl=0):
        X = self.X(v)
        self.f.dot(X, self.y, r=r, f=f_, at=at, dl=dl)
        if label:
            self.f.text(X, self.y - 28 if up else self.y + 80, label, z=z, c=f_ if f_ != "ink" else "ink", at=at, b=700, dl=dl)

    def jump(self, a, b, at=0, c="teal", h=None, up=True, label=None, dl=0, w=4):
        Xa, Xb = self.X(a), self.X(b)
        hh = h or min(140, 40 + abs(Xb - Xa) * 0.35)
        sgn = -1 if up else 1
        pts = []
        for i in range(21):
            t = i / 20
            pts.append((Xa + (Xb - Xa) * t, self.y + sgn * (8 + hh * 4 * t * (1 - t))))
        self.f.poly(pts, at=at, c=c, w=w, z=False, dr=True, ar=1, dl=dl)
        if label:
            self.f.text((Xa + Xb) / 2, self.y + sgn * (hh + 26) + (0 if up else 22), label, z=28, c=c, at=at, b=700, dl=dl)
