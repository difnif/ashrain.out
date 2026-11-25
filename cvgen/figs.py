# ashrain.out — 움직이는 예제의 그림 조각 (figs.py) — 그림 DSL(../avgen/fig.py)로 「움직임」을 만든다
# 그림 칸 660 × 680(무대 쪽 FigDsl 이 그린다). at: "q" 문제 · "p" 방침 · 정수 i 판서 i번째 줄 · "a" 답.
#   움직임 수단: fly(나타날 때 떨어진 곳에서 날아오기) · mv(그때 옮기기 · 돌리기) · un(그때 사라지기) · dr(그리듯) · arc rv(시계 방향으로 쓸기)
#   식 띠(Strip): 한 줄 식을 낱말로 늘어놓고, 판서 줄마다 낱말이 날아 옮겨 가며 다음 식이 된다 — 이항(부호가 바뀌며 = 를 넘어감) · 동류항 모으기 · 약분.
import math, os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "avgen"))
from fig import Fig, fly, mv, NL, Plane, ang_pt, dir_deg, angle_mark, R1

CX = 330


def tw(s, z):
    """무대 글자 폭 어림(draw.jsx 의 estimate 와 같은 계수) — {분자/분모} 는 위아래 중 넓은 쪽"""
    s = str(s)
    w = 0.0
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "{":
            d, j = 0, i
            while j < len(s):
                if s[j] == "{":
                    d += 1
                elif s[j] == "}":
                    d -= 1
                    if d == 0:
                        break
                j += 1
            inner = s[i + 1:j]
            k = inner.find("/")
            if k >= 0:
                w += max(tw(inner[:k], z * 0.72), tw(inner[k + 1:], z * 0.72)) / z + 0.32
            else:
                w += tw(inner, z * 0.62) / z
            i = j + 1
            continue
        if ch in "^_" and i + 1 < len(s) and s[i + 1] == "{":
            j = s.index("}", i)
            w += tw(s[i + 2:j], z * 0.62) / z
            i = j + 1
            continue
        c = ord(ch)
        if 0xAC00 <= c <= 0xD7A3:
            w += 0.93
        elif ch == " ":
            w += 0.25
        elif ch.isdigit():
            w += 0.58
        elif "a" <= ch <= "z":
            w += 0.52
        elif "A" <= ch <= "Z":
            w += 0.66
        elif ch in "²³°":
            w += 0.38
        elif ch in "()[],.:":
            w += 0.32
        elif ch in "×÷+−=<>≤≥":
            w += 0.66
        elif ch in "‹›`":
            w += 0
        else:
            w += 0.7
        i += 1
    return w * z


# ── 식 띠 ────────────────────────────────────────────────────────────────────
class Strip:
    """한 줄 식의 변신. rows[k] = (at, [낱말 …]) — 낱말은 글자 또는 dict(s, frm=앞 줄 낱말 번호(들), c=색, hop=휘어 넘기).
    앞 줄 낱말은 다음 줄이 나타날 때 사라지고, frm 이 있는 낱말은 그 자리에서 날아온다(여럿이면 가운데에서 — 모으기).
    frm 이 없는 낱말은 그 자리에서 써진다. hop=True 면 = 를 넘어가는 이항 — 금빛 휜 화살이 함께 그어진다."""

    def __init__(self, f, y=330, z=44, cx=CX, gap=None, maxw=620):
        self.f, self.y, self.z, self.cx, self.maxw = f, y, z, cx, maxw
        self.gap = gap if gap is not None else z * 0.32
        self.prev = None          # (xs, toks, y, 사라질 낱말들)
        self.arcs = []

    def _xs(self, toks, z):
        """낱말 가운데 x 목록 · 전체 폭 — 낱말에 g 를 주면 그 앞 틈(0 이면 붙여 쓴다)"""
        ws = [tw(t["s"], z) for t in toks]
        gaps = [0] + [(t.get("g", self.gap / self.z) * z) for t in toks[1:]]
        tot = sum(ws) + sum(gaps)
        x = self.cx - tot / 2
        out = []
        for w, g in zip(ws, gaps):
            x += g
            out.append(x + w / 2)
            x += w
        return out, tot

    def row(self, at, toks, y=None, keep=False, dl0=0, c="ink", z=None):
        """한 줄 놓기. keep — 다음 줄이 와도 사라지지 않는다(마지막 줄)."""
        toks = [t if isinstance(t, dict) else {"s": t} for t in toks]
        z = z or self.z
        xs, tot = self._xs(toks, z)
        if tot > self.maxw:                         # 넘치면 줄인다
            z = z * self.maxw / tot
            xs, tot = self._xs(toks, z)
        y = self.y if y is None else y
        els = []
        for i, (t, x) in enumerate(zip(toks, xs)):
            col = t.get("c", c)
            frm = t.get("frm")
            el = self.f.text(x, y, t["s"], z=z, c=col, at=at, b=700 if col != "ink" else 600,
                             dl=(t.get("dl", dl0 + (1 if frm is not None else 80 * i))))
            if frm is not None and self.prev:
                pxs, ptoks, py, _ = self.prev
                src = frm if isinstance(frm, (list, tuple)) else [frm]
                sx = sum(pxs[j] for j in src) / len(src)
                fly(el, sx - x, py - y, dl=t.get("fdl", 120), ms=t.get("ms", 760 if t.get("hop") else 620))
                if t.get("hop"):
                    # = 를 넘는 금빛 휜 화살(위로 크게) — 다음 줄이 오면 함께 사라진다
                    a, b = sx, x
                    hh = 70 + abs(b - a) * 0.12
                    pts = [(a + (b - a) * k / 16, py - z * 0.95 - hh * 4 * (k / 16) * (1 - k / 16)) for k in range(17)]
                    arc = self.f.poly(pts, at=at, c="gold", w=4, z=False, dr=True, ar=1, dl=60, un=t.get("un_hop"))
                    self.arcs.append(arc)
            els.append(el)
        if self.prev and self.prev[3] is not None:
            for el in self.prev[3]:
                if "un" not in el:
                    el["un"] = at
        for arc in self.arcs:                       # 앞 줄의 넘기기 화살은 다음 줄이 오면 사라진다
            if arc.get("at") != at and "un" not in arc:
                arc["un"] = at
        self.prev = (xs, toks, y, None if keep else els)
        return xs, els

    def note(self, at, x, s, dy=-64, c="coral", z=26, dl=200):
        return self.f.text(x, self.y + dy, s, z=z, c=c, at=at, dl=dl, b=700)


def strike(f, x, y, w, at, c="red", dl=0):
    """빗금(지우기)"""
    return f.line(x - w / 2, y + 8, x + w / 2, y - 30, at=at, c=c, w=4, dl=dl)


# ── 수직선 ───────────────────────────────────────────────────────────────────
def nl_range(nl, a, b=None, at=0, closed_a=True, closed_b=True, right=True, c="sky", up=34, dl=0):
    """수직선 위 범위 — 점 ●/○ + 선 위 굵은 화살(교재식: 점은 선 위, 범위는 선 위 굵은 화살)"""
    f = nl.f
    y = nl.y - up
    xa = nl.X(a)
    if b is None:
        xb = nl.x1 + 10 if right else nl.x0 - 10
        f.line(xa, y, xb, y, at=at, c=c, w=7, ar=1, dr=True, dl=dl + 200)
    else:
        xb = nl.X(b)
        f.line(xa, y, xb, y, at=at, c=c, w=7, dr=True, dl=dl + 200)
    f.line(xa, nl.y, xa, y, at=at, c=c, w=3, dl=dl)
    f.dot(xa, y, r=10, f=c if closed_a else "paper", c=c, sw=4, at=at, dl=dl)
    if b is not None:
        f.line(xb, nl.y, xb, y, at=at, c=c, w=3, dl=dl + 300)
        f.dot(xb, y, r=10, f=c if closed_b else "paper", c=c, sw=4, at=at, dl=dl + 300)


def hop(nl, a, b, at, c="teal", label=None, up=True, dl=0, h=None):
    return nl.jump(a, b, at=at, c=c, label=label, up=up, dl=dl, h=h)


# ── 좌표평면 ─────────────────────────────────────────────────────────────────
def travel(P, x, y, at, c="coral", label=None, pos="ne", dl=0, z=28):
    """원점에서 가로로 x 만큼 → 세로로 y 만큼 찾아가 점을 찍는다(점선 길 + 점 톡)"""
    f = P.f
    O = P.P(0, 0)
    A = P.P(x, 0)
    B = P.P(x, y)
    f.line(O[0], O[1], A[0], A[1], at=at, c=c, w=4, d=True, dr=True, dl=dl, ar=1)
    f.line(A[0], A[1], B[0], B[1], at=at, c=c, w=4, d=True, dr=True, dl=dl + 650, ar=1)
    P.pt(x, y, at=at, f=c, r=10, label=label, pos=pos, z=z, c=c, dl=dl + 1250)
    return B


def slope_tri(P, x0, y0, dx, dy, at, c="gold", dl=0, lab=True, z=26):
    """(x0, y0) 에서 가로 dx → 세로 dy 직각 화살 두 개(기울기 삼각형) — 「x 증가량 · y 증가량」"""
    f = P.f
    A, B, Cc = P.P(x0, y0), P.P(x0 + dx, y0), P.P(x0 + dx, y0 + dy)
    f.line(A[0], A[1], B[0], B[1], at=at, c=c, w=4, dr=True, ar=1, dl=dl)
    f.line(B[0], B[1], Cc[0], Cc[1], at=at, c="coral", w=4, dr=True, ar=1, dl=dl + 650)
    if lab:
        f.text((A[0] + B[0]) / 2, A[1] + (34 if dy >= 0 else -14), f"+{dx}" if dx > 0 else f"{dx}".replace("-", "−"), z=z, c=c, at=at, dl=dl + 300, b=700)
        sy = f"+{dy}" if dy > 0 else (f"{dy}".replace("-", "−") if dy else "0")
        f.text(B[0] + 16, (B[1] + Cc[1]) / 2 + 9, sy, z=z, c="coral", at=at, a="s", dl=dl + 950, b=700)


def parabola(P, a, p=0, q=0, at="q", c="sky", w=4.5, x0=None, x1=None, dr=True, d=False):
    return P.curve(lambda x: a * (x - p) ** 2 + q, x0, x1, at=at, c=c, w=w, dr=dr, d=d)


# ── 넓이 모형 ────────────────────────────────────────────────────────────────
def area_model(f, cols, rows, cells, x0=70, y0=110, W=520, H=480, at_cells=None, heads_at="q", cols_c=("teal", "gold", "coral", "sky")):
    """가로 조각 cols[(폭 비, 글자)] × 세로 조각 rows[(높이 비, 글자)] — 칸 cells[r][c] 글자가 at_cells[r][c] 에 칠해지며 써진다"""
    tw_ = sum(v for v, _ in cols)
    th_ = sum(v for v, _ in rows)
    xs = [x0]
    for v, _ in cols:
        xs.append(xs[-1] + W * v / tw_)
    ys = [y0]
    for v, _ in rows:
        ys.append(ys[-1] + H * v / th_)
    for j, (_, lab) in enumerate(cols):
        f.text((xs[j] + xs[j + 1]) / 2, y0 - 18, lab, z=32, c="soft", at=heads_at, b=700)
    for i, (_, lab) in enumerate(rows):
        f.text(x0 - 16, (ys[i] + ys[i + 1]) / 2 + 11, lab, z=32, c="soft", at=heads_at, a="e", b=700)
    k = 0
    for i in range(len(rows)):
        for j in range(len(cols)):
            at = at_cells[i][j] if at_cells else "q"
            f.rect(xs[j], ys[i], xs[j + 1] - xs[j], ys[i + 1] - ys[i], c="ink", sw=3, f=cols_c[k % len(cols_c)], fo=0.3, at=at, dl=1 + 160 * k)
            f.text((xs[j] + xs[j + 1]) / 2, (ys[i] + ys[i + 1]) / 2 + 13, cells[i][j], z=34, at=at, dl=120 + 160 * k, b=700)
            k += 1
    return xs, ys


# ── 막대 · 띠 ────────────────────────────────────────────────────────────────
def bar_grow(f, x, ybase, w, h, at, c="teal", dl=0, fo=0.45, lab=None, z=24):
    """아래에서 위로 자라는 막대(세로선을 그리듯 + 칠)"""
    f.poly([(x, ybase), (x, ybase - h), (x + w, ybase - h), (x + w, ybase)], at=at, c="ink", w=3, f=c, fo=fo, z=False, dr=True, dl=dl)
    if lab is not None:
        f.text(x + w / 2, ybase - h - 12, lab, z=z, at=at, dl=dl + 500, b=700)


def tree(f, levels, x0=60, x1=620, y0=90, dy=150, at_levels=None, z=30):
    """가지 그림: levels = [[이름…], [이름…] …] — 아래 단은 위 단의 모든 가지에서 뻗는다. 단마다 at_levels[k] 에 그어진다"""
    pos = [[((x0 + x1) / 2, y0 - 50)]]
    cnt = 1
    for k, names in enumerate(levels):
        cnt *= len(names)
        row = []
        n = cnt
        for i in range(n):
            row.append((x0 + (x1 - x0) * (i + 0.5) / n, y0 + dy * k))
        at = at_levels[k] if at_levels else k
        for i, (x, y) in enumerate(row):
            px, py = pos[-1][i // len(names)]
            f.line(px, py + 18, x, y - 22, at=at, c="soft", w=2.5, dr=True, dl=1 + i * 70)
            f.text(x, y + 10, names[i % len(names)], z=z if n <= 12 else 22, at=at, dl=200 + i * 70, b=700)
        pos.append(row)
    return pos


def venn2(f, la="A", lb="B", cx=330, cy=340, r=150, d=95, at="q"):
    f.rect(70, 120, 520, 440, c="soft", sw=2.5, rx=14, at=at)
    f.text(96, 156, "U", z=28, c="soft", at=at, a="s")
    f.circ(cx - d, cy, r, c="teal", sw=4, at=at)
    f.circ(cx + d, cy, r, c="coral", sw=4, at=at)
    f.text(cx - d - r * 0.72, cy - r * 0.78, la, z=34, c="teal", at=at, b=800)
    f.text(cx + d + r * 0.72, cy - r * 0.78, lb, z=34, c="coral", at=at, b=800)
    return (cx - d, cy), (cx + d, cy)


def table(f, heads, rows, x0=60, y0=110, cw=None, rh=70, at_rows=None, z=30, hl=None):
    """표 — 머리 줄 + 줄마다 at_rows[i] 에 써진다(칸마다 조금씩 늦게)"""
    n = len(heads)
    cw = cw or [540 / n] * n
    xs = [x0]
    for w in cw:
        xs.append(xs[-1] + w)
    f.rect(x0, y0, xs[-1] - x0, rh, c="ink", sw=3, f="gold", fo=0.18, at="q")
    for j, h in enumerate(heads):
        f.text((xs[j] + xs[j + 1]) / 2, y0 + rh / 2 + 10, h, z=z - 2, at="q", b=700)
    for i, r in enumerate(rows):
        at = at_rows[i] if at_rows else "q"
        y = y0 + rh * (i + 1)
        f.rect(x0, y, xs[-1] - x0, rh, c="ink", sw=2, at=at)
        for j, v in enumerate(r):
            f.text((xs[j] + xs[j + 1]) / 2, y + rh / 2 + 10, v, z=z, at=at, dl=1 + 120 * j, c=("coral" if hl and (i, j) in hl else "ink"), b=700 if hl and (i, j) in hl else 600)
    for x in xs[1:-1]:
        f.line(x, y0, x, y0 + rh * (len(rows) + 1), c="ink", w=2, at="q")
    return xs


def poly_pts(cx, cy, r, n, rot=90):
    return [(cx + r * math.cos(math.radians(rot + 360 * k / n)), cy - r * math.sin(math.radians(rot + 360 * k / n))) for k in range(n)]


# ── 점 배열 · 칩 · 톱니 · 저울 ─────────────────────────────────────────────────
def dot_grid(f, n, cols, at, cx=CX, cy=330, gap=46, r=13, c="teal", src=None, un=None, dl=0, step=40):
    """n 개 점을 cols 칸씩 — src(앞 배치 점 자리)가 있으면 거기서 날아와 다시 선다"""
    rows = (n + cols - 1) // cols
    pts = [(cx - (cols - 1) * gap / 2 + (i % cols) * gap, cy - (rows - 1) * gap / 2 + (i // cols) * gap) for i in range(n)]
    for i, (x, y) in enumerate(pts):
        el = f.dot(x, y, r=r, f=c, at=at, dl=dl + (1 + 12 * i if src else step * i), un=un)
        if src:
            fly(el, src[i][0] - x, src[i][1] - y, dl=90, ms=720)
    return pts


def chip(f, x, y, s, at, c="coral", z=32, dl=0, un=None, w=None, fill=None):
    """둥근 칸 안 글자 하나(소인수 · 부호 칩)"""
    w = w or max(z * 1.25, tw(s, z) + z * 0.6)
    f.rect(x - w / 2, y - z * 0.98, w, z * 1.4, c=c, sw=3, rx=z * 0.42, f=fill or c, fo=0.16, at=at, dl=dl, un=un)
    t = f.text(x, y, s, z=z, c=c if c != "ink" else "ink", at=at, dl=dl + 60, un=un, b=700)
    return t


def gear_pts(cx, cy, n, R, r=None, phase=0.0):
    """톱니바퀴 바깥 선 — n 개 이(사다리꼴)"""
    r = r or R * 0.84
    pts = []
    for k in range(n):
        a0 = 2 * math.pi * k / n + phase
        da = 2 * math.pi / n
        for fr, rr in ((0.0, r), (0.18, R), (0.5, R), (0.68, r)):
            a = a0 + da * fr
            pts.append((cx + rr * math.cos(a), cy - rr * math.sin(a)))
    return pts


def vnl(f, lo, hi, x=200, y0=600, y1=90, at="q", step=1, lab_step=1, z=24):
    """세로 수직선(온도계 눈금) — 위가 +. 값 → y 를 돌려주는 함수"""
    Y = lambda v: y0 + (y1 - y0) * (v - lo) / (hi - lo)
    f.line(x, y0 + 20, x, y1 - 24, at=at, c="ink", w=3, ar=1)
    k = lo
    while k <= hi + 1e-9:
        big = abs(k / lab_step - round(k / lab_step)) < 1e-9
        f.line(x - (12 if big else 7), Y(k), x + (12 if big else 7), Y(k), at=at, c="ink", w=3 if big else 2)
        if big:
            f.text(x - 22, Y(k) + 8, ("−" if k < 0 else ("+" if k > 0 else "")) + str(abs(int(k))), z=z, c="soft", at=at, a="e")
        k += step
    return Y


def balance(f, at="q", cx=CX, y=250, half=230, tilt=0):
    """양팔 저울 — 받침 · 막대 · 두 접시. 접시 윗면 y 두 개(왼 · 오) 를 돌려준다"""
    f.poly([(cx - 70, 640), (cx + 70, 640), (cx, y + 8)], at=at, c="ink", w=3, f="wood", fo=0.35)
    f.line(cx - half, y, cx + half, y, at=at, c="ink", w=6)
    f.dot(cx, y, r=9, f="gold", at=at)
    py = y + 170
    for s in (-1, 1):
        x = cx + s * half
        f.line(x, y, x - 80, py, at=at, c="soft", w=2.5)
        f.line(x, y, x + 80, py, at=at, c="soft", w=2.5)
        f.line(x - 120, py, x + 120, py, at=at, c="ink", w=5)
    return py


def order_arcs(f, spans, y, labels, ats, c="teal", z=34):
    """식 아래 계산 차례 — spans[(x0, x1)] 마다 휜 선 + ①② … (ats[k] 에)"""
    NUMS = "①②③④⑤⑥⑦"
    for k, (a, b) in enumerate(spans):
        dep = 40 + 26 * (labels[k] if isinstance(labels[k], int) else 0)
        pts = [(a + (b - a) * i / 16, y + 16 + dep * 4 * (i / 16) * (1 - i / 16)) for i in range(17)]
        f.poly(pts, c=c, w=3.5, z=False, dr=True, at=ats[k])
        f.text((a + b) / 2, y + 16 + dep + 36, NUMS[k], z=z, c=c, at=ats[k], b=700, dl=300)


# ── 도형 조각 ────────────────────────────────────────────────────────────────
def ell_pts(cx, cy, rx, ry, a0=0, a1=360, n=48):
    """타원(호) 점 — 각은 도(동쪽 0, 시계 반대 +)"""
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy - ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def sector_pts(cx, cy, r, a0, a1, n=24):
    """부채꼴(중심 포함) 다각형 점"""
    return [(cx, cy)] + [(cx + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy - r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def oblique(p, dx=0.5, dy=0.42):
    """(x, y, z) → 그림 칸 — 겨냥도식: 안쪽(z)은 오른쪽 위로"""
    x, y, z = p
    return (x + z * dx, y - z * dy)


def solid(f, V, E, hidden=(), at="q", c="ink", w=3, dl=0):
    """꼭짓점 V{이름: (x, y)} · 모서리 E[(a, b)] — hidden 모서리는 점선"""
    out = {}
    for i, (a, b) in enumerate(E):
        d = (a, b) in hidden or (b, a) in hidden
        out[(a, b)] = f.line(V[a][0], V[a][1], V[b][0], V[b][1], at=at, c=c, w=w, d=d, dl=dl)
    return out


def lab_pts(f, V, names=None, at="q", z=28, c="ink", off=None, dl=0):
    for k in (names or V):
        dx, dy = (off or {}).get(k, (0, -14))
        f.text(V[k][0] + dx, V[k][1] + dy, k, z=z, c=c, at=at, b=700, dl=dl)


def seg_ticks(f, A, B, n=1, at="q", c="coral", s=12, dl=0):
    """선분 가운데 같은 길이 표시(짧은 금 n 개)"""
    mx, my = (A[0] + B[0]) / 2, (A[1] + B[1]) / 2
    ang = math.atan2(B[1] - A[1], B[0] - A[0]) + math.pi / 2
    ux, uy = math.cos(ang), math.sin(ang)
    tx, ty = math.cos(ang - math.pi / 2), math.sin(ang - math.pi / 2)
    for k in range(n):
        o = (k - (n - 1) / 2) * 8
        f.line(mx + tx * o - ux * s, my + ty * o - uy * s, mx + tx * o + ux * s, my + ty * o + uy * s, at=at, c=c, w=3, dl=dl)


def tri_from(B, C, angB, angC):
    """밑변 B → C(화면 가로) 위로 각 B, 각 C 인 삼각형의 꼭짓점 A"""
    bx, by = B
    cx_, cy_ = C
    L_ = math.hypot(cx_ - bx, cy_ - by)
    A_ = 180 - angB - angC
    b = L_ * math.sin(math.radians(angB)) / math.sin(math.radians(A_))  # AC
    c = L_ * math.sin(math.radians(angC)) / math.sin(math.radians(A_))  # AB
    return (bx + c * math.cos(math.radians(angB)), by - c * math.sin(math.radians(angB)))


def rot(p, c, deg):
    """화면 좌표에서 c 를 중심으로 deg 만큼(그림 DSL mv r 과 같은 방향 — 화면에서 시계 방향 +)"""
    th = math.radians(deg)
    x, y = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(th) - y * math.sin(th), c[1] + x * math.sin(th) + y * math.cos(th))


def slide(el, at, dx=0, dy=0, dl=0):
    """뜨지 않고 곧게 옮기기(선 · 축을 따라 미끄러지기). 그리는 쪽은 회전 없는 옮기기를 위로 살짝 띄우는데(lift),
    아주 작은 회전(0.1°, 제자리 중심)을 넣으면 띄우지 않는다."""
    k = el.get("k")
    if k == "L":
        cx, cy = (el["x"] + el["x2"]) / 2, (el["y"] + el["y2"]) / 2
    elif k == "P":
        xs = [p[0] for p in el["pts"]]
        ys = [p[1] for p in el["pts"]]
        cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    elif k == "R":
        cx, cy = el["x"] + el["w"] / 2, el["y"] + el["h"] / 2
    else:
        cx, cy = el.get("x", 0), el.get("y", 0)
    m = {"at": at, "r": 0.1, "cx": R1(cx), "cy": R1(cy)}
    if dx:
        m["dx"] = R1(dx)
    if dy:
        m["dy"] = R1(dy)
    if dl:
        m["dl"] = int(dl)
    el["mv"] = m
    return el


def slides(els, at, dx=0, dy=0, dl=0):
    for el in els:
        slide(el, at, dx, dy, dl)
    return els


def arcp(f, cx, cy, r, a0, a1, at="q", c="gold", sw=3, rv=False, dl=0, un=None, n=None, fill=None, fo=0.2):
    """큰 반지름의 호는 꺾은선으로 — 그리는 쪽이 호(A)의 크기를 원 전체로 어림해 그림이 작아지지 않게.
    fill 이 있으면 부채꼴 칠을 먼저 깐다. rv: a1 쪽에서 a0 쪽으로(시계 방향) 그려진다."""
    n = n or max(8, int(abs(a1 - a0) / 3))
    pts = ell_pts(cx, cy, r, r, a0, a1, n)
    if fill:
        f.poly(sector_pts(cx, cy, r, a0, a1, n), at=at, c="none", f=fill, fo=fo, dl=dl, un=un)
    if rv:
        pts = pts[::-1]
    return f.poly(pts, at=at, c=c, w=sw, z=False, dr=True, dl=dl, un=un)
