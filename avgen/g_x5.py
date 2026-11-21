# 초5 · 초6 채우기 — 합동과 대칭 · 여러 가지 그래프(띠 · 원그래프) · 공간과 입체(쌓기나무) · 원기둥 · 원뿔 · 구
import math
from fractions import Fraction as Fr
from core import *
from core import _has_batchim
from fig import Fig
from kit import *

def bat(v):
    return _has_batchim(str(v))

def DEC(v):
    v = Fr(v).limit_denominator(100000)
    if v.denominator == 1:
        return str(v.numerator)
    return f"{float(v):g}"


def ell(cx, cy, rx, ry, a0=0, a1=360, n=48):
    return [(cx + rx * math.cos(math.radians(a0 + (a1 - a0) * k / n)), cy + ry * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]

def tri_pts(a, b, c):
    """변 ㄱㄴ = a, ㄴㄷ = b, ㄷㄱ = c → ㄱ, ㄴ, ㄷ (ㄴ 원점, ㄷ 오른쪽, ㄱ 위)"""
    B = (0.0, 0.0)
    C = (b, 0.0)
    x = (a * a + b * b - c * c) / (2 * b)
    y = math.sqrt(max(a * a - x * x, 0.01))
    return [(x, -y), B, C]

def fit_pts(P, box):
    x0, y0, x1, y1 = box
    xs, ys = [p[0] for p in P], [p[1] for p in P]
    sc = min((x1 - x0) / max(1e-6, max(xs) - min(xs)), (y1 - y0) / max(1e-6, max(ys) - min(ys)))
    ox = (x0 + x1) / 2 - sc * (max(xs) + min(xs)) / 2
    oy = (y0 + y1) / 2 - sc * (max(ys) + min(ys)) / 2
    return [(ox + sc * x, oy + sc * y) for x, y in P]

def lab_poly(f, P, names, at="q", z=28):
    cx = sum(p[0] for p in P) / len(P)
    cy = sum(p[1] for p in P) / len(P)
    for (x, y), nm in zip(P, names):
        dx, dy = x - cx, y - cy
        d = math.hypot(dx, dy) or 1
        f.text(x + dx / d * 26, y + dy / d * 26 + 10, nm, z=z, b=700, at=at)

def side_lab(f, P, Q, txt, inside, at="q", z=24):
    mx, my = (P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2
    dx, dy = Q[0] - P[0], Q[1] - P[1]
    d = math.hypot(dx, dy) or 1
    nx, ny = -dy / d, dx / d
    if (inside[0] - mx) * nx + (inside[1] - my) * ny > 0:
        nx, ny = -nx, -ny
    f.text(mx + nx * 24, my + ny * 24 + 8, txt, z=z, b=700, at=at)

def two_tris(f, sd, known, P1n="ㄱㄴㄷ", P2n="ㄹㅁㅂ", at="q"):
    T = tri_pts(*sd)
    A = fit_pts(T, (40, 200, 300, 470))
    B = fit_pts([(-x, y) for x, y in T], (360, 200, 620, 470))
    for P, nm in ((A, P1n), (B, P2n)):
        f.poly(P, c="ink", w=4, f="sky", fo=0.15, at=at)
        lab_poly(f, P, list(nm), at=at)
    cA = (sum(p[0] for p in A) / 3, sum(p[1] for p in A) / 3)
    cB = (sum(p[0] for p in B) / 3, sum(p[1] for p in B) / 3)
    for i, txt in known:
        side_lab(f, A[i], A[(i + 1) % 3], txt, cA, at=at)
    return A, B, cA, cB

def reg_axes(f, nm, at_shape="q", at_ax=0):
    cx, cy = 330, 350
    if nm.startswith("정") and nm != "정사각형":
        n = {"정삼각형": 3, "정오각형": 5, "정육각형": 6, "정팔각형": 8, "정십각형": 10}[nm]
        r = 210
        P = [(cx + r * math.cos(math.radians(-90 + 360 * i / n)), cy + r * math.sin(math.radians(-90 + 360 * i / n))) for i in range(n)]
        f.poly(P, c="ink", w=4, f="sky", fo=0.15, at=at_shape)
        for k in range(n):
            a = math.radians(-90 + 180 * k / n)
            f.line(cx - 240 * math.cos(a), cy - 240 * math.sin(a), cx + 240 * math.cos(a), cy + 240 * math.sin(a), c="gold", w=3, d=True, at=at_ax, dl=k * 120)
        return
    if nm in ("정사각형", "직사각형"):
        w, h = (380, 380) if nm == "정사각형" else (440, 260)
        f.rect(cx - w / 2, cy - h / 2, w, h, c="ink", sw=4, f="sky", fo=0.15, at=at_shape)
        ax = [(cx - w / 2 - 30, cy, cx + w / 2 + 30, cy), (cx, cy - h / 2 - 30, cx, cy + h / 2 + 30)]
        if nm == "정사각형":
            ax += [(cx - w / 2 - 25, cy - h / 2 - 25, cx + w / 2 + 25, cy + h / 2 + 25), (cx + w / 2 + 25, cy - h / 2 - 25, cx - w / 2 - 25, cy + h / 2 + 25)]
    elif nm == "마름모":
        P = [(cx, cy - 220), (cx + 150, cy), (cx, cy + 220), (cx - 150, cy)]
        f.poly(P, c="ink", w=4, f="sky", fo=0.15, at=at_shape)
        ax = [(cx, cy - 250, cx, cy + 250), (cx - 180, cy, cx + 180, cy)]
    elif nm == "이등변삼각형":
        P = [(cx, cy - 210), (cx + 160, cy + 170), (cx - 160, cy + 170)]
        f.poly(P, c="ink", w=4, f="sky", fo=0.15, at=at_shape)
        ax = [(cx, cy - 240, cx, cy + 200)]
    else:
        P = [(cx - 230, cy + 140), (cx + 110, cy + 140), (cx + 230, cy - 140), (cx - 110, cy - 140)]
        f.poly(P, c="ink", w=4, f="sky", fo=0.15, at=at_shape)
        ax = []
    for k, (x1, y1, x2, y2) in enumerate(ax):
        f.line(x1, y1, x2, y2, c="gold", w=3, d=True, at=at_ax, dl=k * 120)


# ══════════ 합동과 대칭 ══════════
SYMAX = {"정삼각형": 3, "정사각형": 4, "정오각형": 5, "정육각형": 6, "정팔각형": 8, "직사각형": 2, "마름모": 2, "이등변삼각형": 1, "평행사변형": 0, "정십각형": 10}
PTSYM = {"정사각형": True, "정육각형": True, "직사각형": True, "마름모": True, "평행사변형": True, "정팔각형": True,
         "정삼각형": False, "정오각형": False, "이등변삼각형": False, "등변사다리꼴": False}
def cong5():
    S = Set("cong5", "합동과 대칭 — 대응변 · 대응각 · 선대칭 · 점대칭", "합동과 대칭",
            {1: "합동인 도형의 대응변", 2: "합동인 도형의 대응각", 3: "선대칭 도형", 4: "점대칭 도형", 5: "대칭 도형의 둘레"},
            pp=10,
            tips={1: "합동인 두 도형은 대응변의 길이가 같아요 — 꼭짓점을 쓴 차례대로 짝짓기",
                  2: "대응각의 크기도 같아요 — 모르는 각은 삼각형(180°) · 사각형(360°)의 각의 합으로",
                  3: "대칭축은 대응점을 이은 선분을 수직으로 똑같이 둘로 나눠요",
                  4: "대칭의 중심은 대응점을 이은 선분을 똑같이 둘로 나눠요",
                  5: "반쪽의 둘레(대칭축 위 변은 빼고) × 2"},
            note="합동인 도형을 말할 때는 꼭짓점을 ‘대응하는 차례’로 써요. 삼각형 ㄱㄴㄷ ≡ 삼각형 ㄹㅁㅂ이면 ㄱ↔ㄹ, ㄴ↔ㅁ, ㄷ↔ㅂ — 이 짝을 먼저 써 두게 해 주세요.")
    R = rng(5501)
    A, B = "ㄱㄴㄷㄹ", "ㅁㅂㅅㅇ"

    def tri_ok(a, b, c):
        return a + b > c and b + c > a and a + c > b

    def g1():
        n = R.choice([3, 3, 4])
        if n == 3:
            while True:
                sd = [R.randint(3, 15) for _ in range(3)]
                if tri_ok(*sd) and len(set(sd)) == 3:
                    break
            P, Q = "ㄱㄴㄷ", "ㄹㅁㅂ"
            names = [P[0] + P[1], P[1] + P[2], P[2] + P[0]]
            qn = [Q[0] + Q[1], Q[1] + Q[2], Q[2] + Q[0]]
            k = R.randrange(3)
            known = ", ".join(f"변 {names[i]} = {sd[i]} cm" for i in range(3) if i != k)
            q = f"삼각형 {P}과 삼각형 {Q}은 서로 합동이에요. {known}, 변 {qn[k]} = {sd[k]} cm일 때, 삼각형 {P}의 둘레는 몇 cm인가요?"
            lines = [L(f"변 {names[k]}의 대응변은 변 {qn[k]} → {sd[k]} cm", memo="쓴 차례대로 짝"), L(f"{' + '.join(map(str, sd))} = {sum(sd)}")]
            f = Fig()
            A, B_, cA, cB = two_tris(f, sd, [(i, f"{sd[i]} cm") for i in range(3) if i != k])
            side_lab(f, B_[k], B_[(k + 1) % 3], f"{sd[k]} cm", cB)
            side_lab(f, A[k], A[(k + 1) % 3], "?", cA)
            S.add(1, q, f"{sum(sd)} cm", "대응변의 길이는 같아요", lines, f.out(), ap=str(sum(sd)), key=q)
        else:
            sd = [R.randint(3, 15) for _ in range(4)]
            P, Q = "ㄱㄴㄷㄹ", "ㅁㅂㅅㅇ"
            names = [P[i] + P[(i + 1) % 4] for i in range(4)]
            qn = [Q[i] + Q[(i + 1) % 4] for i in range(4)]
            k = R.randrange(4)
            q = f"사각형 {P}과 사각형 {Q}은 서로 합동이에요. 변 {names[k]} = {sd[k]} cm일 때, 변 {qn[k]}의 길이는 몇 cm인가요?"
            lines = [L(f"{P[k]} ↔ {Q[k]}, {P[(k + 1) % 4]} ↔ {Q[(k + 1) % 4]}", memo="쓴 차례대로 짝"), L(f"변 {qn[k]} = 변 {names[k]} = {sd[k]} cm")]
            S.add(1, q, f"{sd[k]} cm", "대응변의 길이는 같아요", lines, None, ap=str(sd[k]), key=q)
    fill(S, 1, 20, g1)

    def g2():
        if R.random() < 0.5:
            a, b = R.randint(30, 100), R.randint(30, 100)
            c = 180 - a - b
            if c < 20:
                return
            q = f"삼각형 ㄱㄴㄷ과 삼각형 ㄹㅁㅂ은 서로 합동이에요. 각 ㄱ = {a}°, 각 ㄴ = {b}°일 때, 각 ㅂ의 크기는 몇 도인가요?"
            lines = [L("각 ㅂ의 대응각은 각 ㄷ", memo="쓴 차례대로 짝"), L(f"180° − {a}° − {b}° = {c}°", memo="삼각형의 세 각의 합 180°")]
            ra, rb, rc = [math.sin(math.radians(x)) for x in (c, a, b)]
            f = Fig()
            A, B_, cA, cB = two_tris(f, (ra, rb, rc), [])
            for P_, V, txt in ((A, 0, f"{a}°"), (A, 1, f"{b}°")):
                x, y = P_[V]
                f.text(x + (cA[0] - x) * 0.32, y + (cA[1] - y) * 0.32 + 9, txt, z=22, b=700)
            x, y = B_[2]
            f.text(x + (cB[0] - x) * 0.32, y + (cB[1] - y) * 0.32 + 9, "?", z=26, b=800)
            S.add(2, q, f"{c}°", "대응각을 찾고 각의 합으로", lines, f.out(), ap=str(c), key=q)
        else:
            a, b, c = R.randint(60, 130), R.randint(60, 130), R.randint(60, 130)
            d = 360 - a - b - c
            if not (30 <= d <= 170):
                return
            q = f"사각형 ㄱㄴㄷㄹ과 사각형 ㅁㅂㅅㅇ은 서로 합동이에요. 각 ㄱ = {a}°, 각 ㄴ = {b}°, 각 ㄷ = {c}°일 때, 각 ㅇ의 크기는 몇 도인가요?"
            lines = [L("각 ㅇ의 대응각은 각 ㄹ", memo="쓴 차례대로 짝"), L(f"360° − {a}° − {b}° − {c}° = {d}°", memo="사각형의 네 각의 합 360°")]
            S.add(2, q, f"{d}°", "대응각을 찾고 각의 합으로", lines, None, ap=str(d), key=q)
    fill(S, 2, 20, g2)

    def g3():
        t = R.randrange(3)
        if t == 0:
            nm = R.choice(list(SYMAX))
            k = SYMAX[nm]
            q = f"{nm}의 대칭축은 모두 몇 개인가요?"
            lines = [L(f"{eul(nm)} 반으로 접어 완전히 겹치는 선을 모두 찾기"), L(f"{k}개")]
            f = Fig()
            reg_axes(f, nm)
            S.add(3, q, f"{k}개", "반으로 접어 완전히 겹치는 선", lines, f.out(), ap=str(k), key=q)
        elif t == 1:
            d = R.randint(2, 20)
            q = f"선대칭 도형에서 대응점 ㄱ과 ㄴ을 이은 선분이 대칭축과 만나는 점을 ㄷ이라고 해요. 선분 ㄱㄷ이 {d} cm이면 선분 ㄱㄴ은 몇 cm인가요?"
            lines = [L("대칭축은 대응점을 이은 선분을 똑같이 둘로 나눠요"), L(f"{d} × 2 = {2 * d}")]
            S.add(3, q, f"{2 * d} cm", "대칭축이 똑같이 둘로 나눠요", lines, None, ap=str(2 * d), key=q)
        else:
            a, b = R.sample(list(SYMAX), 2)
            q = f"{wa(a)} {b}의 대칭축의 수의 합은 몇 개인가요?"
            lines = [L(f"{a} {SYMAX[a]}개, {b} {SYMAX[b]}개"), L(f"{SYMAX[a]} + {SYMAX[b]} = {SYMAX[a] + SYMAX[b]}")]
            S.add(3, q, f"{SYMAX[a] + SYMAX[b]}개", "도형마다 대칭축 세기", lines, None, ap=str(SYMAX[a] + SYMAX[b]), key=q)
    fill(S, 3, 20, g3)

    def g4():
        t = R.randrange(3)
        if t == 0:
            d = R.randint(2, 25)
            q = f"점대칭 도형에서 대칭의 중심부터 한 꼭짓점까지의 거리가 {d} cm예요. 이 꼭짓점과 대응점 사이의 거리는 몇 cm인가요?"
            lines = [L("대칭의 중심은 대응점을 이은 선분을 똑같이 둘로 나눠요"), L(f"{d} × 2 = {2 * d}")]
            S.add(4, q, f"{2 * d} cm", "대칭의 중심이 똑같이 둘로 나눠요", lines, None, ap=str(2 * d), key=q)
        elif t == 1:
            cands = list(PTSYM)
            pick = R.sample(cands, R.randint(4, 6))
            cnt = sum(1 for x in pick if PTSYM[x])
            q = f"{', '.join(pick)} 중에서 점대칭 도형은 몇 개인가요?"
            lines = [L("한 점을 중심으로 180° 돌렸을 때 처음과 완전히 겹치는 도형"), L(", ".join(x for x in pick if PTSYM[x]) or "없음"), L(f"{cnt}개")]
            S.add(4, q, f"{cnt}개", "180° 돌려서 완전히 겹치는지", lines, None, ap=str(cnt), key=q)
        else:
            a, b = R.randint(3, 15), R.randint(3, 15)
            ang = R.randint(40, 140)
            q = f"평행사변형 ㄱㄴㄷㄹ은 점대칭 도형이에요. 변 ㄱㄴ = {a} cm, 변 ㄴㄷ = {b} cm, 각 ㄴ = {ang}°일 때, 변 ㄷㄹ의 길이와 각 ㄹ의 크기를 차례로 쓰세요."
            lines = [L("ㄱ ↔ ㄷ, ㄴ ↔ ㄹ", memo="대칭의 중심을 지나 마주 보는 꼭짓점끼리"), L(f"변 ㄷㄹ = 변 ㄱㄴ = {a} cm"), L(f"각 ㄹ = 각 ㄴ = {ang}°")]
            S.add(4, q, f"{a} cm, {ang}°", "마주 보는 것끼리 대응", lines, None, ap=f"{a}, {ang}", omr="ex", key=q)
    fill(S, 4, 20, g4)

    def g5():
        if R.random() < 0.5:
            k = R.randint(2, 4)
            sd = [R.randint(2, 15) for _ in range(k)]
            ax = R.randint(3, 20)
            q = f"직선을 대칭축으로 하는 선대칭 도형의 반쪽이에요. 대칭축 위의 변은 {ax} cm이고, 나머지 변의 길이는 {', '.join(f'{x} cm' for x in sd)}예요. 선대칭 도형을 완성했을 때 둘레는 몇 cm인가요?"
            lines = [L(f"반쪽에서 대칭축 위 변을 뺀 길이: {' + '.join(map(str, sd))} = {sum(sd)}", memo="대칭축 위 변은 둘레가 아니에요"), L(f"{sum(sd)} × 2 = {2 * sum(sd)}")]
            S.add(5, q, f"{2 * sum(sd)} cm", "반쪽(축 위 변 빼고) × 2", lines, None, ap=str(2 * sum(sd)), key=q)
        else:
            sd = [R.randint(2, 15) for _ in range(R.randint(2, 4))]
            q = f"점대칭 도형의 둘레의 반쪽을 이루는 변의 길이가 차례로 {', '.join(f'{x} cm' for x in sd)}예요. 이 도형의 둘레는 몇 cm인가요?"
            lines = [L(f"{' + '.join(map(str, sd))} = {sum(sd)}", memo="반쪽"), L(f"{sum(sd)} × 2 = {2 * sum(sd)}", memo="대응변의 길이가 같아요")]
            S.add(5, q, f"{2 * sum(sd)} cm", "반쪽 × 2", lines, None, ap=str(2 * sum(sd)), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 여러 가지 그래프 — 띠그래프 · 원그래프 ══════════
GTOP = {"좋아하는 운동": ["축구", "야구", "수영", "배드민턴", "농구"], "좋아하는 과일": ["사과", "배", "귤", "포도", "딸기"],
        "가고 싶은 체험 학습 장소": ["박물관", "과학관", "놀이공원", "동물원", "미술관"], "등교 방법": ["걷기", "버스", "자전거", "자동차"],
        "좋아하는 간식": ["떡볶이", "김밥", "과자", "빵", "아이스크림"]}
def pcts(n):
    """합이 100인 백분율 n 개 — 5의 배수"""
    while True:
        cuts = sorted(R_.sample(range(1, 20), n - 1))
        p = [5 * (b - a) for a, b in zip([0] + cuts, cuts + [20])]
        if min(p) >= 10 and len(set(p)) == n:
            return p
R_ = None
def graph6():
    global R_
    S = Set("graph6", "여러 가지 그래프 — 띠그래프 · 원그래프", "여러 가지 그래프",
            {1: "백분율로 나타내기", 2: "띠그래프의 길이", 3: "원그래프 읽기", 4: "모르는 항목의 비율", 5: "비율로 전체 · 몇 배"},
            pp=8,
            tips={1: "(부분) ÷ (전체) × 100 → %",
                  2: "띠 전체 길이 × 비율 — 전체 20 cm면 5%마다 1 cm",
                  3: "전체 × 백분율 ÷ 100",
                  4: "모든 항목의 백분율의 합은 100%",
                  5: "백분율끼리 견주면 몇 배인지 — 같은 전체에서 나온 비율"},
            note="띠그래프와 원그래프는 전체를 100%로 보고 부분이 얼마를 차지하는지 보여 줘요. 백분율의 합이 100%인지 먼저 확인하게 해 주세요.")
    R = rng(5601)
    R_ = R

    def band(f, names, ps, at="q", hl=None):
        x0, w, y = 40, 580, 300
        x = x0
        for i, (nm, p) in enumerate(zip(names, ps)):
            ww = w * p / 100
            f.rect(x, y, ww, 90, c="ink", sw=3, f="sky" if i % 2 == 0 else "gold", fo=0.12 + 0.13 * (i % 3), at=at)
            fits = ww >= 24 * len(nm) + 10
            yl = y - 18 - (34 if (not fits and i % 2) else 0)
            if fits:
                f.text(x + ww / 2, y + 38, nm, z=22, b=700, at=at)
            else:
                f.text(x + ww / 2, yl, nm, z=21, b=700, at=at)
                f.line(x + ww / 2, yl + 6, x + ww / 2, y, c="soft", w=1.5, at=at)
            f.text(x + ww / 2, y + 72, f"{p}%", z=22, b=700, at=at)
            x += ww
        for k in range(0, 101, 10):
            f.line(x0 + w * k / 100, y + 100, x0 + w * k / 100, y + 112, c="ink", w=2, at=at)
            if k % 20 == 0:
                f.text(x0 + w * k / 100, y + 140, str(k), z=20, at=at)

    def pie(f, names, ps, at="q"):
        cx, cy, r = 330, 360, 220
        a = -90.0
        for i, (nm, p) in enumerate(zip(names, ps)):
            b = a + 360 * p / 100
            pts = [(cx, cy)] + [(cx + r * math.cos(math.radians(a + (b - a) * k / 30)), cy + r * math.sin(math.radians(a + (b - a) * k / 30))) for k in range(31)]
            f.poly(pts, c="ink", w=3, f="sky" if i % 2 == 0 else "gold", fo=0.12 + 0.13 * (i % 3), at=at)
            m = math.radians((a + b) / 2)
            f.text(cx + r * 0.62 * math.cos(m), cy + r * 0.62 * math.sin(m) - 4, nm, z=20 if p < 15 else 23, b=700, at=at)
            f.text(cx + r * 0.62 * math.cos(m), cy + r * 0.62 * math.sin(m) + 22, f"{p}%", z=20, b=700, at=at)
            a = b

    def g1():
        N = R.choice([20, 25, 40, 50, 200, 400, 500])
        a = R.randint(1, N - 1)
        p = Fr(a * 100, N)
        if p.denominator != 1 or p >= 100:
            return
        tp = R.choice(list(GTOP))
        it = R.choice(GTOP[tp])
        q = f"{tp}을 조사했더니 전체 {N}명 중 {it}{'이' if bat(it) else '가'} {a}명이었어요. {it}의 비율은 몇 %인가요?".replace(f"{tp}을", eul(tp))
        lines = [L(f"{a} ÷ {N} × 100 = {p}", memo="(부분) ÷ (전체) × 100")]
        S.add(1, q, f"{p}%", "부분 ÷ 전체 × 100", lines, None, ap=str(p), key=q)
    fill(S, 1, 20, g1)

    def g2():
        tp = R.choice(list(GTOP))
        n = R.randint(3, min(5, len(GTOP[tp])))
        names = R.sample(GTOP[tp], n)
        ps = pcts(n)
        Lt = R.choice([10, 20, 25, 40])
        i = R.randrange(n)
        ln = Fr(Lt * ps[i], 100)
        q = f"{eul(tp)} 조사해 길이가 {Lt} cm인 띠그래프로 나타냈어요. {names[i]}({ps[i]}%)가 차지하는 부분의 길이는 몇 cm인가요?"
        f = Fig()
        band(f, names, ps)
        lines = [L(f"{Lt} × {ps[i]} ÷ 100 = {DEC(ln)}", memo="띠 전체 × 비율")]
        S.add(2, q, f"{DEC(ln)} cm", "띠 전체 길이 × 비율", lines, f.out(), ap=DEC(ln), key=q)
    fill(S, 2, 20, g2)

    def g3():
        tp = R.choice(list(GTOP))
        n = R.randint(3, min(5, len(GTOP[tp])))
        names = R.sample(GTOP[tp], n)
        ps = pcts(n)
        N = R.choice([200, 300, 400, 500, 600, 800, 1000])
        i = R.randrange(n)
        v = Fr(N * ps[i], 100)
        if v.denominator != 1:
            return
        f = Fig()
        pie(f, names, ps)
        q = f"학생 {N}명에게 {eul(tp)} 물어 원그래프로 나타냈어요. {eul(names[i])} 고른 학생은 몇 명인가요?"
        lines = [L(f"{names[i]} {ps[i]}%", memo="원그래프에서 읽기"), L(f"{N} × {ps[i]} ÷ 100 = {v}")]
        S.add(3, q, f"{v}명", "전체 × 백분율 ÷ 100", lines, f.out(), ap=str(v), qfig=True, key=q + str(ps), dupq=True)
    fill(S, 3, 20, g3)

    def g4():
        tp = R.choice(list(GTOP))
        n = R.randint(3, min(5, len(GTOP[tp])))
        names = R.sample(GTOP[tp], n)
        ps = pcts(n)
        h = R.randrange(n)
        known = ", ".join(f"{a} {p}%" for k, (a, p) in enumerate(zip(names, ps)) if k != h)
        q = f"{eul(tp)} 조사한 띠그래프에서 {known}일 때, {names[h]}의 비율은 몇 %인가요?"
        kn = [p for k, p in enumerate(ps) if k != h]
        lines = [L(f"100 − {' − '.join(map(str, kn))} = {ps[h]}", memo="모두 더하면 100%")]
        S.add(4, q, f"{ps[h]}%", "전체 100%에서 빼기", lines, None, ap=str(ps[h]), key=q)
    fill(S, 4, 20, g4)

    def g5():
        tp = R.choice(list(GTOP))
        n = R.randint(3, min(5, len(GTOP[tp])))
        names = R.sample(GTOP[tp], n)
        ps = pcts(n)
        if R.random() < 0.5:
            i = R.randrange(n)
            v = R.randint(2, 30)
            N = Fr(v * 100, ps[i])
            if N.denominator != 1:
                return
            q = f"{eul(tp)} 조사한 원그래프에서 {names[i]}{'이' if bat(names[i]) else '가'} {ps[i]}%이고 {v}명이에요. 조사한 학생은 모두 몇 명인가요?"
            lines = [L(f"{ps[i]}%가 {v}명 → 1%는 {v} ÷ {ps[i]}"), L(f"{v} ÷ {ps[i]} × 100 = {N}")]
            S.add(5, q, f"{N}명", "부분 ÷ 비율 × 100", lines, None, ap=str(N), key=q)
        else:
            pairs = [(i, j) for i in range(n) for j in range(n) if i != j and ps[i] % ps[j] == 0 and ps[i] // ps[j] >= 2]
            if not pairs:
                return
            i, j = R.choice(pairs)
            f = Fig()
            band(f, names, ps)
            q = f"{eul(tp)} 조사해 띠그래프로 나타냈어요. {eul(names[i])} 고른 학생 수는 {eul(names[j])} 고른 학생 수의 몇 배인가요?"
            lines = [L(f"{names[i]} {ps[i]}%, {names[j]} {ps[j]}%", memo="같은 전체의 비율끼리"), L(f"{ps[i]} ÷ {ps[j]} = {ps[i] // ps[j]}")]
            S.add(5, q, f"{ps[i] // ps[j]}배", "비율끼리 나누기", lines, f.out(), ap=str(ps[i] // ps[j]), qfig=True, key=q + str(ps), dupq=True)
    fill(S, 5, 20, g5)
    return S


# ══════════ 공간과 입체 — 쌓기나무 ══════════
def cube6():
    S = Set("cube6", "공간과 입체 — 쌓기나무", "공간과 입체",
            {1: "위에서 본 모양의 수로 세기", 2: "층별로 세기", 3: "앞 · 옆에서 본 모양", 4: "더 필요한 쌓기나무", 5: "빼낸 뒤 남은 쌓기나무"},
            pp=8,
            tips={1: "위에서 본 모양의 각 칸에 쓴 수 = 그 자리에 쌓인 개수 — 모두 더하기",
                  2: "□층에 있는 쌓기나무 = 수가 □ 이상인 칸의 수",
                  3: "앞에서 보면 세로줄마다 가장 높은 층이 보여요",
                  4: "만들 모양의 개수 − 지금 개수",
                  5: "빼낸 칸의 수를 줄여 다시 세기"},
            note="위에서 본 모양에 수를 쓰는 방법은 쌓기나무를 빠짐없이 세는 가장 확실한 방법이에요. 칸마다 수를 소리 내어 읽으며 더하게 해 주세요.")
    R = rng(5602)

    def top(f, G, at="q", hl=None):
        m, n = len(G), len(G[0])
        cs = min(100, 420 / max(m, n))
        x0, y0 = 330 - cs * n / 2, 340 - cs * m / 2
        for i in range(m):
            for j in range(n):
                if G[i][j]:
                    f.rect(x0 + j * cs, y0 + i * cs, cs, cs, c="ink", sw=3, f="gold", fo=0.12 + 0.1 * G[i][j], at=at)
                    f.text(x0 + j * cs + cs / 2, y0 + i * cs + cs / 2 + 14, str(G[i][j]), z=40, b=800, at=at)
        f.text(330, y0 + m * cs + 50, "앞", z=26, b=700, at=at)

    def grid(m, n, lo=0, hi=4):
        while True:
            G = [[R.randint(lo, hi) for _ in range(n)] for _ in range(m)]
            if sum(1 for r in G for v in r if v) >= max(3, m * n - 2) and all(any(r) for r in G) and all(any(G[i][j] for i in range(m)) for j in range(n)):
                return G

    def g1():
        m, n = R.randint(2, 3), R.randint(2, 4)
        G = grid(m, n)
        vals = [v for r in G for v in r if v]
        q = "쌓기나무로 쌓은 모양을 위에서 본 모양에 각 칸에 쌓인 개수를 썼어요. 쌓기나무는 모두 몇 개인가요?"
        f = Fig()
        top(f, G)
        lines = [L(f"{' + '.join(map(str, vals))} = {sum(vals)}", memo="칸마다 쓴 수를 모두 더하기")]
        S.add(1, q, f"{sum(vals)}개", "칸의 수를 모두 더하기", lines, f.out(), ap=str(sum(vals)), qfig=True, key=str(G), dupq=True)
    fill(S, 1, 20, g1)

    def g2():
        m, n = R.randint(2, 3), R.randint(2, 4)
        G = grid(m, n, 0, 4)
        H = max(v for r in G for v in r)
        k = R.randint(2, H) if H >= 2 else 1
        cnt = sum(1 for r in G for v in r if v >= k)
        t = R.randrange(2)
        f = Fig()
        top(f, G)
        if t == 0:
            q = f"위에서 본 모양의 각 칸에 쌓인 개수를 썼어요. {k}층에 있는 쌓기나무는 몇 개인가요?"
            lines = [L(f"{k}층에 쌓기나무가 있는 칸 = 수가 {k} 이상인 칸", memo="칸마다 확인"), L(f"{cnt}개")]
            S.add(2, q, f"{cnt}개", f"수가 {k} 이상인 칸 세기", lines, f.out(), ap=str(cnt), qfig=True, key=q + str(G), dupq=True)
        else:
            c2 = sum(max(0, v - 1) for r in G for v in r)
            q = "위에서 본 모양의 각 칸에 쌓인 개수를 썼어요. 2층 이상에 있는 쌓기나무는 모두 몇 개인가요?"
            tot = sum(v for r in G for v in r)
            c1 = sum(1 for r in G for v in r if v)
            lines = [L(f"모두 {tot}개, 1층 {c1}개", memo="1층 = 수가 쓰인 칸의 수"), L(f"{tot} − {c1} = {c2}")]
            S.add(2, q, f"{c2}개", "전체 − 1층", lines, f.out(), ap=str(c2), qfig=True, key=q + str(G), dupq=True)
    fill(S, 2, 20, g2)

    def g3():
        m, n = R.randint(2, 3), R.randint(2, 4)
        G = grid(m, n, 0, 4)
        side = R.random() < 0.5
        if not side:
            hs = [max(G[i][j] for i in range(m)) for j in range(n)]
            q = "위에서 본 모양의 각 칸에 쌓인 개수를 썼어요. 앞에서 보면 왼쪽 줄부터 차례로 몇 층으로 보이나요?"
            lines = [L("앞에서 보면 세로줄마다 가장 높은 층", memo="줄마다 가장 큰 수"), L(", ".join(f"{j + 1}째 줄 {hs[j]}층" for j in range(n)))]
        else:
            hs = [max(G[i][j] for j in range(n)) for i in range(m)][::-1]
            q = "위에서 본 모양의 각 칸에 쌓인 개수를 썼어요. 오른쪽 옆에서 보면 왼쪽부터 차례로 몇 층으로 보이나요?"
            lines = [L("오른쪽 옆에서 보면 가로줄마다 가장 높은 층 — 앞줄이 왼쪽", memo="줄마다 가장 큰 수"), L(", ".join(f"{hs[j]}층" for j in range(m)))]
        f = Fig()
        top(f, G)
        ans = ", ".join(map(str, hs))
        S.add(3, q, ans, "줄마다 가장 큰 수", lines, f.out(), ap=ans, omr="ex", qfig=True, key=q + str(G), dupq=True)
    fill(S, 3, 20, g3)

    def g4():
        t = R.randrange(2)
        if t == 0:
            m, n = R.randint(2, 3), R.randint(2, 3)
            G = grid(m, n, 1, 3)
            k = R.choice([3, 4])
            have = sum(v for r in G for v in r)
            need = k ** 3 - have
            q = f"위에서 본 모양의 각 칸에 쌓인 개수를 쓴 쌓기나무에 쌓기나무를 더 쌓아 가로, 세로, 높이가 모두 {k}개인 정육면체를 만들려고 해요. 쌓기나무는 적어도 몇 개 더 필요한가요?"
            f = Fig()
            top(f, G)
            lines = [L(f"정육면체: {k} × {k} × {k} = {k ** 3}"), L(f"지금 {' + '.join(str(v) for r in G for v in r)} = {have}"), L(f"{k ** 3} − {have} = {need}")]
            S.add(4, q, f"{need}개", "만들 모양 − 지금", lines, f.out(), ap=str(need), qfig=True, key=q + str(G), dupq=True)
        else:
            a, b, c = R.randint(2, 5), R.randint(2, 5), R.randint(2, 5)
            have = R.randint(a * b, a * b * c - 1)
            q = f"쌓기나무 {have}개가 있어요. 가로 {a}개, 세로 {b}개씩 {c}층으로 쌓은 직육면체 모양을 만들려면 쌓기나무가 몇 개 더 필요한가요?"
            lines = [L(f"한 층에 {a} × {b} = {a * b}"), L(f"{a * b} × {c} = {a * b * c}"), L(f"{a * b * c} − {have} = {a * b * c - have}")]
            S.add(4, q, f"{a * b * c - have}개", "만들 모양 − 지금", lines, None, ap=str(a * b * c - have), key=q)
    fill(S, 4, 20, g4)

    def g5():
        a, b, c = R.randint(2, 5), R.randint(2, 5), R.randint(2, 5)
        t = R.randrange(2)
        if t == 0:
            k = R.randint(1, a * b - 1)
            q = f"가로 {a}개, 세로 {b}개씩 {c}층으로 쌓은 직육면체 모양에서 맨 위층의 쌓기나무 {k}개를 빼냈어요. 남은 쌓기나무는 몇 개인가요?"
            lines = [L(f"{a} × {b} × {c} = {a * b * c}"), L(f"{a * b * c} − {k} = {a * b * c - k}")]
            S.add(5, q, f"{a * b * c - k}개", "처음 개수 − 빼낸 개수", lines, None, ap=str(a * b * c - k), key=q)
        else:
            q = f"가로 {a}개, 세로 {b}개씩 {c}층으로 쌓은 직육면체 모양에서 맨 위층을 모두 빼냈어요. 남은 쌓기나무는 몇 개인가요?"
            lines = [L(f"남은 층은 {c} − 1 = {c - 1}층"), L(f"{a} × {b} × {c - 1} = {a * b * (c - 1)}")]
            S.add(5, q, f"{a * b * (c - 1)}개", "남은 층 수로 세기", lines, None, ap=str(a * b * (c - 1)), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 원기둥 · 원뿔 · 구 ══════════
PI = Fr(314, 100)

def net(f, r, h, at="q"):
    """원기둥 전개도 — 옆면 직사각형 + 위아래 밑면"""
    W = 2 * math.pi * r
    sc = min(560 / W, 400 / (h + 4 * r))
    w, hh, rr = W * sc, h * sc, r * sc
    x0, y0 = 330 - w / 2, 350 - hh / 2
    f.rect(x0, y0, w, hh, c="ink", sw=4, f="sky", fo=0.15, at=at)
    f.circ(x0 + w / 2, y0 - rr, rr, c="ink", sw=4, f="gold", fo=0.2, at=at)
    f.circ(x0 + w / 2, y0 + hh + rr, rr, c="ink", sw=4, f="gold", fo=0.2, at=at)
    f.text(330, y0 + hh / 2 + 10, "옆면", z=26, b=700, at=at)
    f.line(x0, y0 + hh + 2 * rr + 30, x0 + w, y0 + hh + 2 * rr + 30, c="coral", w=3, ar=3, at=0)
    f.text(330, y0 + hh + 2 * rr + 62, "밑면의 둘레", z=24, b=700, c="coral", at=0)

def cone(f, l, d, at="q"):
    hgt = math.sqrt(max(l * l - (d / 2) ** 2, 0.1))
    P = fit_pts([(0, -hgt), (d / 2, 0), (-d / 2, 0)], (170, 170, 490, 500))
    f.poly(P, c="ink", w=4, f="sky", fo=0.15, at=at)
    cx = (P[1][0] + P[2][0]) / 2
    rx = (P[1][0] - P[2][0]) / 2
    f.poly(ell(cx, P[1][1], rx, rx * 0.22, 0, 180), c="ink", w=3, z=False, at=at)
    f.poly(ell(cx, P[1][1], rx, rx * 0.22, 180, 360), c="ink", w=2, z=False, d=True, at=at)
    c0 = (sum(p[0] for p in P) / 3, sum(p[1] for p in P) / 3)
    side_lab(f, P[0], P[1], f"{l} cm", c0)
    f.text(cx, P[1][1] + rx * 0.22 + 36, f"지름 {d} cm", z=24, b=700, at=at)
def cyl6():
    S = Set("cyl6", "원기둥 · 원뿔 · 구 — 전개도와 회전체", "원기둥·원뿔·구",
            {1: "원기둥의 전개도", 2: "원뿔의 모선과 높이", 3: "구의 지름과 둘레", 4: "돌려 만든 입체도형", 5: "옆면의 넓이"},
            pp=10,
            tips={1: "전개도에서 옆면(직사각형)의 가로 = 밑면의 둘레 = 지름 × 3.14, 세로 = 높이",
                  2: "앞에서 본 원뿔은 이등변삼각형 — 두 변이 모선, 밑변이 밑면의 지름",
                  3: "구의 중심에서 겉면까지는 모두 반지름",
                  4: "돌리는 축에 붙은 변이 높이, 축에서 떨어진 쪽 끝까지가 밑면의 반지름",
                  5: "옆면의 넓이 = 밑면의 둘레 × 높이"},
            note="원주율은 3.14로 계산해요. 원기둥의 전개도를 실제로 접어 보며 옆면의 가로가 밑면의 둘레와 맞닿는다는 것을 확인하게 해 주세요.")
    R = rng(5603)

    def g1():
        r, h = R.randint(2, 10), R.randint(3, 20)
        t = R.randrange(2)
        circ = PI * 2 * r
        f = Fig()
        net(f, r, h)
        if t == 0:
            q = f"밑면의 반지름이 {r} cm, 높이가 {h} cm인 원기둥의 전개도에서 옆면의 가로는 몇 cm인가요? (원주율 3.14)"
            lines = [L("옆면의 가로 = 밑면의 둘레", memo="말아서 밑면에 맞닿아요"), L(f"{2 * r} × 3.14 = {DEC(circ)}", memo="지름 × 원주율")]
            S.add(1, q, f"{DEC(circ)} cm", "옆면의 가로 = 밑면의 둘레", lines, f.out(), ap=DEC(circ), key=q)
        else:
            q = f"원기둥의 전개도에서 옆면의 가로가 {DEC(circ)} cm, 세로가 {h} cm예요. 이 원기둥의 밑면의 반지름은 몇 cm인가요? (원주율 3.14)"
            lines = [L(f"밑면의 둘레 = {DEC(circ)}"), L(f"지름 = {DEC(circ)} ÷ 3.14 = {2 * r}"), L(f"반지름 = {2 * r} ÷ 2 = {r}")]
            S.add(1, q, f"{r} cm", "둘레 ÷ 3.14 = 지름", lines, f.out(), ap=str(r), key=q)
    fill(S, 1, 20, g1)

    def g2():
        d = 2 * R.randint(2, 10)
        l = R.randint(d // 2 + 2, d + 10)
        t = R.randrange(2)
        if t == 0:
            q = f"모선의 길이가 {l} cm, 밑면의 지름이 {d} cm인 원뿔을 앞에서 본 모양의 둘레는 몇 cm인가요?"
            lines = [L("앞에서 본 모양: 두 변이 모선, 밑변이 지름인 이등변삼각형"), L(f"{l} × 2 + {d} = {2 * l + d}")]
            f = Fig()
            cone(f, l, d)
            S.add(2, q, f"{2 * l + d} cm", "모선 2개 + 지름", lines, f.out(), ap=str(2 * l + d), key=q)
        else:
            P = 2 * l + d
            q = f"원뿔을 앞에서 본 이등변삼각형의 둘레가 {P} cm이고 밑면의 지름이 {d} cm예요. 모선의 길이는 몇 cm인가요?"
            lines = [L(f"모선 2개 = {P} − {d} = {P - d}"), L(f"모선 = {P - d} ÷ 2 = {l}")]
            S.add(2, q, f"{l} cm", "둘레에서 지름을 빼고 반으로", lines, None, ap=str(l), key=q)
    fill(S, 2, 20, g2)

    def g3():
        r = R.randint(2, 20)
        t = R.randrange(3)
        if t == 0:
            q = f"반지름이 {r} cm인 구를 중심을 지나도록 반으로 잘랐어요. 잘린 면인 원의 지름은 몇 cm인가요?"
            lines = [L("중심을 지나게 자르면 잘린 면의 반지름 = 구의 반지름"), L(f"{r} × 2 = {2 * r}")]
            S.add(3, q, f"{2 * r} cm", "구의 반지름 = 잘린 원의 반지름", lines, None, ap=str(2 * r), key=q)
        elif t == 1:
            q = f"반지름이 {r} cm인 구를 위에서 본 모양의 둘레는 몇 cm인가요? (원주율 3.14)"
            v = PI * 2 * r
            lines = [L(f"위에서 본 모양 = 반지름 {r} cm인 원"), L(f"{2 * r} × 3.14 = {DEC(v)}")]
            S.add(3, q, f"{DEC(v)} cm", "위 · 앞 · 옆 어디서 봐도 같은 원", lines, None, ap=DEC(v), key=q)
        else:
            k = R.randint(2, 4)
            q = f"반지름이 {r} cm인 구 {k}개를 한 줄로 맞닿게 상자에 넣었어요. 상자 안쪽의 길이는 적어도 몇 cm여야 하나요?"
            lines = [L(f"구 하나의 지름 {r} × 2 = {2 * r}"), L(f"{2 * r} × {k} = {2 * r * k}")]
            S.add(3, q, f"{2 * r * k} cm", "지름 × 개수", lines, None, ap=str(2 * r * k), key=q)
    fill(S, 3, 20, g3)

    def g4():
        a, b = R.randint(2, 12), R.randint(2, 12)
        t = R.randrange(3)
        if t == 0:
            q = f"가로 {a} cm, 세로 {b} cm인 직사각형을 세로를 축으로 한 바퀴 돌렸어요. 만들어진 입체도형의 밑면의 지름은 몇 cm인가요?"
            lines = [L("직사각형을 돌리면 원기둥 — 축인 세로가 높이"), L(f"밑면의 반지름 = 가로 = {a}"), L(f"지름 {a} × 2 = {2 * a}")]
            S.add(4, q, f"{2 * a} cm", "축에서 먼 변까지가 반지름", lines, None, ap=str(2 * a), key=q)
        elif t == 1:
            q = f"밑변이 {a} cm, 높이가 {b} cm인 직각삼각형을 높이를 축으로 한 바퀴 돌렸어요. 만들어진 입체도형의 밑면의 지름과 높이를 차례로 쓰세요."
            lines = [L("직각삼각형을 돌리면 원뿔 — 축이 높이"), L(f"밑면의 반지름 = 밑변 = {a} → 지름 {2 * a}"), L(f"높이 = {b}")]
            S.add(4, q, f"{2 * a} cm, {b} cm", "축이 높이, 밑변이 반지름", lines, None, ap=f"{2 * a}, {b}", omr="ex", key=q)
        else:
            q = f"지름이 {2 * a} cm인 반원을 지름을 축으로 한 바퀴 돌렸어요. 만들어진 구의 반지름은 몇 cm인가요?"
            lines = [L("반원을 지름을 축으로 돌리면 구"), L(f"반지름 = {2 * a} ÷ 2 = {a}")]
            S.add(4, q, f"{a} cm", "반원 → 구", lines, None, ap=str(a), key=q)
    fill(S, 4, 20, g4)

    def g5():
        r, h = R.randint(2, 10), R.randint(3, 15)
        circ = PI * 2 * r
        area = circ * h
        f = Fig()
        net(f, r, h)
        q = f"밑면의 반지름이 {r} cm, 높이가 {h} cm인 원기둥의 옆면의 넓이는 몇 cm²인가요? (원주율 3.14)"
        lines = [L(f"옆면의 가로 = {2 * r} × 3.14 = {DEC(circ)}", memo="밑면의 둘레"), L(f"{DEC(circ)} × {h} = {DEC(area)}", memo="가로 × 세로(높이)")]
        S.add(5, q, f"{DEC(area)} cm²", "밑면의 둘레 × 높이", lines, f.out(), ap=DEC(area), key=q)
    fill(S, 5, 20, g5)
    return S
