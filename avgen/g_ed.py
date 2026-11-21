# 초등 ④ — 직육면체 · 각기둥과 각뿔 · 규칙과 대응 · 어림과 평균
import math
from fractions import Fraction as Fr
from core import *
from fig import Fig, mv, NL, ang_pt
from kit import *

KN = {3: "삼", 4: "사", 5: "오", 6: "육", 7: "칠", 8: "팔", 9: "구", 10: "십", 11: "십일", 12: "십이"}

def bat(x):
    from core import _has_batchim
    return _has_batchim(str(x))


# ══════════ 직육면체 ══════════
def box_fig(w, d, h, at="q", labs=None, lab_at="q", fill=None, fill_at=None, box=(80, 130, 600, 600)):
    """사선 투영 직육면체 — 앞면 w × h, 깊이 d. labs = (가로, 세로(깊이), 높이) 글자"""
    k = 0.55
    ux, uy = math.cos(math.radians(35)) * k, -math.sin(math.radians(35)) * k
    W, Dx, Dy, H = w, d * ux, d * uy, h
    xs = [0, W, W + Dx, Dx]
    ys = [0, H, H - Dy]
    tw, th = W + Dx, H - Dy
    s = min((box[2] - box[0]) / tw, (box[3] - box[1]) / th)
    ox = (box[0] + box[2]) / 2 - s * tw / 2
    oy = (box[1] + box[3]) / 2 + s * th / 2
    P = lambda x, y: (ox + s * x, oy - s * y)
    A, B, C, D_ = P(0, 0), P(W, 0), P(W, H), P(0, H)
    E, F_, G, Hh = P(Dx, -Dy), P(W + Dx, -Dy), P(W + Dx, H - Dy), P(Dx, H - Dy)
    return (A, B, C, D_, E, F_, G, Hh), s

def draw_box(f, w, d, h, at="q", labs=None, lab_at="q", face=None, face_at=0, box=(80, 140, 600, 600)):
    (A, B, C, D_, E, F_, G, Hh), s = box_fig(w, d, h, box=box)
    if face == "front":
        f.poly([A, B, C, D_], c="none", w=0, f="gold", fo=0.35, at=face_at)
    elif face == "top":
        f.poly([D_, C, G, Hh], c="none", w=0, f="teal", fo=0.35, at=face_at)
    elif face == "side":
        f.poly([B, F_, G, C], c="none", w=0, f="coral", fo=0.3, at=face_at)
    for p, q in ((A, B), (B, C), (C, D_), (D_, A), (B, F_), (F_, G), (G, C), (G, Hh), (Hh, D_)):
        f.line(*p, *q, c="ink", w=3, at=at)
    for p, q in ((A, E), (E, F_), (E, Hh)):
        f.line(*p, *q, c="soft", w=2, d=True, at=at)
    if labs:
        lw, ld, lh = labs
        if lw:
            f.text((A[0] + B[0]) / 2, A[1] + 42, lw, z=28, b=700, at=lab_at)
        if ld:
            f.text((B[0] + F_[0]) / 2 + 26, (B[1] + F_[1]) / 2 + 22, ld, z=28, b=700, a="s", at=lab_at)
        if lh:
            f.text(A[0] - 14, (A[1] + D_[1]) / 2 + 10, lh, z=28, b=700, a="e", at=lab_at)
    return (A, B, C, D_, E, F_, G, Hh)

def box():
    S = Set("box", "직육면체 — 모서리 · 겉넓이 · 부피", "직육면체",
            {1: "면 · 모서리 · 꼭짓점", 2: "모서리 길이의 합", 3: "겉넓이", 4: "부피", 5: "부피의 활용"},
            pp=8,
            tips={1: "직육면체: 면 6개 · 모서리 12개 · 꼭짓점 8개. 같은 길이의 모서리가 4개씩 세 묶음",
                  2: "모든 모서리 길이의 합 = (가로 + 세로 + 높이) × 4",
                  3: "겉넓이 = (가로 × 세로 + 세로 × 높이 + 가로 × 높이) × 2 · 정육면체는 한 면 × 6",
                  4: "부피 = 가로 × 세로 × 높이 — 1 cm³ 쌓기나무가 몇 개인지. 1 `m`³ = 1000000 cm³",
                  5: "부피를 알면 높이 = 부피 ÷ (가로 × 세로). 물에 잠긴 돌의 부피 = 늘어난 물의 부피"},
            note="겉넓이와 부피를 헷갈리지 않게 ‘포장지(겉넓이) · 쌓기나무(부피)’로 구분하게 해 주세요. 전개도를 펼쳐 같은 모양의 면이 두 개씩 있다는 것을 확인하면 공식이 자연스러워요.")
    R = rng(341)

    def g1():
        k = S.count(1) % 3
        f = Fig()
        if k == 0:
            what, per = R.choice([("면", 6), ("모서리", 12), ("꼭짓점", 8)])
            shape_, n = R.choice(["직육면체", "정육면체"]), R.randint(2, 12)
            a = R.randint(3, 8)
            P = draw_box(f, a + (3 if shape_ == "직육면체" else 0), a, a - (1 if shape_ == "직육면체" else 0))
            if what == "꼭짓점":
                for i, p in enumerate(P):
                    f.dot(*p, r=7, f="coral", at=0, dl=i * 80)
            q = f"{shape_} 모양 상자 {n}개의 {what}{'은' if what == '면' else '는'} 모두 몇 개인가요?"
            lines = [L(f"{shape_} 한 개의 {what} {per}개", memo="면 6 · 모서리 12 · 꼭짓점 8"), L(f"{per} × {n} = {per * n}"), L(f"{per * n}개")]
            S.add(1, q, f"{per * n}개", "한 개의 수 × 상자 수", lines, f.out(), ap=str(per * n), key=q)
        elif k == 1:
            w, d, h = R.randint(3, 12), R.randint(2, 10), R.randint(2, 10)
            if R.random() < 0.5:
                d = w
            if len({w, d, h}) == 1:
                return
            x = R.choice([w, d, h])
            cnt = 4 * [w, d, h].count(x)
            draw_box(f, w, d, h, labs=(f"{w} cm", f"{d} cm", f"{h} cm"))
            q = f"가로 {w} cm, 세로 {d} cm, 높이 {h} cm인 직육면체에서 길이가 {x} cm인 모서리는 모두 몇 개인가요?"
            lines = [L("같은 방향의 모서리 4개는 길이가 같아요", memo="가로 4 · 세로 4 · 높이 4"), L(f"길이가 {x} cm인 방향 {[w, d, h].count(x)}개"), L(f"4 × {[w, d, h].count(x)} = {cnt}"), L(f"{cnt}개")]
            S.add(1, q, f"{cnt}개", "같은 방향의 모서리는 4개씩 — 같은 길이의 방향이 몇 개인지", lines, f.out(), ap=str(cnt), key=q)
        else:
            n = R.randint(2, 12)
            solid = R.random() < 0.5
            P = draw_box(f, 7, 5, 4)
            A, B, C, D_, E, F_, G, Hh = P
            for i, (p, q_) in enumerate(((A, E), (E, F_), (E, Hh)) if not solid else ((A, B), (B, C), (C, D_), (D_, A), (B, F_), (F_, G), (G, C), (G, Hh), (Hh, D_))):
                f.line(*p, *q_, c="coral", w=5, at=0, dl=i * 90)
            per = 9 if solid else 3
            what = "실선(보이는 모서리)" if solid else "점선(보이지 않는 모서리)"
            q = f"직육면체의 겨냥도를 {n}개 그릴 때 {what}은 모두 몇 개 그려야 하나요?"
            lines = [L(f"겨냥도 한 개: 보이는 모서리 9개, 보이지 않는 모서리 3개", memo="9 + 3 = 12"), L(f"{per} × {n} = {per * n}"), L(f"{per * n}개")]
            S.add(1, q, f"{per * n}개", "겨냥도에서 보이는 모서리 9 · 보이지 않는 모서리 3", lines, f.out(), ap=str(per * n), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 3
        w, d, h = R.randint(3, 15), R.randint(2, 12), R.randint(2, 12)
        f = Fig()
        if k == 0:
            draw_box(f, w, d, h, labs=(f"{w} cm", f"{d} cm", f"{h} cm"))
            T = (w + d + h) * 4
            q = f"가로 {w} cm, 세로 {d} cm, 높이 {h} cm인 직육면체의 모든 모서리 길이의 합은 몇 cm인가요?"
            lines = [L(f"{w} + {d} + {h} = {w + d + h}", memo="길이가 다른 세 모서리"), L(f"{w + d + h} × 4 = {T}", memo="같은 길이가 4개씩"), L(f"{T} cm")]
            ans, ap, plan = f"{T} cm", str(T), "(가로 + 세로 + 높이) × 4"
        elif k == 1:
            a = R.randint(2, 20)
            draw_box(f, a, a, a, labs=(None, None, "? cm"))
            q = f"모든 모서리 길이의 합이 {12 * a} cm인 정육면체의 한 모서리는 몇 cm인가요?"
            lines = [L("정육면체는 모서리 12개가 모두 같아요"), L(f"{12 * a} ÷ 12 = {a}"), L(f"{a} cm")]
            ans, ap, plan = f"{a} cm", str(a), "모서리 12개가 모두 같아요"
        else:
            T = (w + d + h) * 4
            draw_box(f, w, d, h, labs=(f"{w} cm", f"{d} cm", "? cm"))
            q = f"모든 모서리 길이의 합이 {T} cm이고, 가로가 {w} cm, 세로가 {d} cm인 직육면체의 높이는 몇 cm인가요?"
            lines = [L(f"{T} ÷ 4 = {w + d + h}", memo="가로 + 세로 + 높이"), L(f"{w + d + h} − {w} − {d} = {h}"), L(f"{h} cm")]
            ans, ap, plan = f"{h} cm", str(h), "모서리 합 ÷ 4 = 가로 + 세로 + 높이"
        S.add(2, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        w, d, h = R.randint(3, 12), R.randint(2, 10), R.randint(2, 10)
        f = Fig()
        if k < 2:
            draw_box(f, w, d, h, labs=(f"{w} cm", f"{d} cm", f"{h} cm"), face="front", face_at=0)
            A1, A2, A3 = w * d, d * h, w * h
            T = 2 * (A1 + A2 + A3)
            q = f"가로 {w} cm, 세로 {d} cm, 높이 {h} cm인 직육면체의 겉넓이는 몇 cm²인가요?"
            lines = [L(f"{w} × {d} = {A1}", pre="윗면"), L(f"{d} × {h} = {A2}", pre="옆면"), L(f"{w} × {h} = {A3}", pre="앞면"),
                     L(f"({A1} + {A2} + {A3}) × 2 = {T}", memo="같은 면이 두 개씩"), L(f"{T} cm²")]
            ans, ap, plan = f"{T} cm²", str(T), "서로 다른 세 면의 넓이의 합 × 2"
        else:
            a = R.randint(2, 15)
            draw_box(f, a, a, a, labs=(f"{a} cm", None, None), face="front", face_at=0)
            T = 6 * a * a
            q = f"한 모서리가 {a} cm인 정육면체의 겉넓이는 몇 cm²인가요?"
            lines = [L(f"{a} × {a} = {a * a}", pre="한 면"), L(f"{a * a} × 6 = {T}", memo="여섯 면이 모두 같아요"), L(f"{T} cm²")]
            ans, ap, plan = f"{T} cm²", str(T), "한 면의 넓이 × 6"
        S.add(3, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        f = Fig()
        if k == 0:
            w, d, h = R.randint(2, 15), R.randint(2, 12), R.randint(2, 12)
            V = w * d * h
            draw_box(f, w, d, h, labs=(f"{w} cm", f"{d} cm", f"{h} cm"))
            q = f"가로 {w} cm, 세로 {d} cm, 높이 {h} cm인 직육면체의 부피는 몇 cm³인가요?"
            lines = [L("부피 = 가로 × 세로 × 높이", memo="1 cm³ 쌓기나무의 개수"), L(f"{w} × {d} × {h} = {V}"), L(f"{V} cm³")]
            ans, ap = f"{V} cm³", str(V)
        elif k == 1:
            a = R.randint(2, 15)
            draw_box(f, a, a, a, labs=(f"{a} cm", None, None))
            V = a ** 3
            q = f"한 모서리가 {a} cm인 정육면체의 부피는 몇 cm³인가요?"
            lines = [L(f"{a} × {a} × {a} = {V}", memo="정육면체 = 세 모서리가 같은 직육면체"), L(f"{V} cm³")]
            ans, ap = f"{V} cm³", str(V)
        else:
            w, d, h = R.randint(2, 9), R.randint(2, 9), R.randint(2, 9)
            V = w * d * h
            draw_box(f, w, d, h, labs=(f"{w} `m`", f"{d} `m`", f"{h} `m`"))
            q = f"가로 {w} `m`, 세로 {d} `m`, 높이 {h} `m`인 직육면체의 부피는 몇 cm³인가요?"
            lines = [L(f"{w} × {d} × {h} = {V}", pre="`m`³로", memo="먼저 `m`³로"), L(f"{V} × 1000000 = {V * 1000000}", memo="1 `m`³ = 1000000 cm³"), L(f"{com(V * 1000000)} cm³")]
            ans, ap = f"{com(V * 1000000)} cm³", str(V * 1000000)
        S.add(4, q, ans, "부피 = 가로 × 세로 × 높이", lines, f.out(), ap=ap, key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        f = Fig()
        if k == 0:
            w, d, h = R.randint(2, 12), R.randint(2, 12), R.randint(2, 12)
            V = w * d * h
            draw_box(f, w, d, h, labs=(f"{w} cm", f"{d} cm", "? cm"))
            q = f"부피가 {V} cm³이고 가로가 {w} cm, 세로가 {d} cm인 직육면체의 높이는 몇 cm인가요?"
            lines = [L(f"{w} × {d} = {w * d}", pre="밑면의 넓이"), L(f"{V} ÷ {w * d} = {h}", memo="부피 ÷ 밑면의 넓이"), L(f"{h} cm")]
            ans, ap, plan = f"{h} cm", str(h), "높이 = 부피 ÷ (가로 × 세로)"
        elif k == 1:
            w, d = R.randint(10, 30), R.randint(10, 30)
            rise = R.randint(1, 6)
            V = w * d * rise
            draw_box(f, w, d, 14, labs=(f"{w} cm", f"{d} cm", None))
            q = f"가로 {w} cm, 세로 {d} cm인 직육면체 모양 수조에 돌을 완전히 넣었더니 물의 높이가 {rise} cm 높아졌어요. 돌의 부피는 몇 cm³인가요?"
            lines = [L("돌의 부피 = 늘어난 물의 부피", memo="물이 돌만큼 밀려 올라와요"), L(f"{w} × {d} × {rise} = {V}"), L(f"{V} cm³")]
            ans, ap, plan = f"{V} cm³", str(V), "늘어난 물의 부피 = 밑면 × 늘어난 높이"
        else:
            a = R.randint(2, 6)
            w, d, h = a * R.randint(2, 5), a * R.randint(2, 5), a * R.randint(1, 4)
            n = (w // a) * (d // a) * (h // a)
            draw_box(f, w, d, h, labs=(f"{w} cm", f"{d} cm", f"{h} cm"))
            q = f"가로 {w} cm, 세로 {d} cm, 높이 {h} cm인 직육면체 상자에 한 모서리가 {a} cm인 정육면체를 빈틈없이 채우면 모두 몇 개 들어가나요?"
            lines = [L(f"{w} ÷ {a} = {w // a}, {d} ÷ {a} = {d // a}, {h} ÷ {a} = {h // a}", memo="방향마다 몇 개"), L(f"{w // a} × {d // a} × {h // a} = {n}"), L(f"{n}개")]
            ans, ap, plan = f"{n}개", str(n), "가로 · 세로 · 높이로 각각 몇 개씩 들어가는지 곱해요"
        S.add(5, q, ans, plan, lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 각기둥과 각뿔 ══════════
def prism_fig(f, n, kind, at="q", hl=None, hl_at=0):
    """n각기둥(kind='p') · n각뿔(kind='y') — 밑면을 기울여 본 모습"""
    cx, rx, ry = 330, 200, 62
    yb, yt = 520, 190
    base = [(cx + rx * math.cos(2 * math.pi * i / n + 0.35), yb + ry * math.sin(2 * math.pi * i / n + 0.35)) for i in range(n)]
    front = lambda p: p[1] >= yb - 4
    if kind == "p":
        top = [(x, y - (yb - yt)) for x, y in base]
        for i in range(n):
            j = (i + 1) % n
            back = not (front(base[i]) or front(base[j])) or (base[i][1] < yb and base[j][1] < yb and False)
            hid = base[i][1] < yb - 5 and base[j][1] < yb - 5
            f.line(*base[i], *base[j], c="soft" if hid else "ink", w=2 if hid else 3, d=hid, at=at)
            f.line(*top[i], *top[j], c="ink", w=3, at=at)
            vh = base[i][1] < yb - 5 and not (base[i][0] == min(p[0] for p in base) or base[i][0] == max(p[0] for p in base))
            f.line(*base[i], *top[i], c="soft" if vh else "ink", w=2 if vh else 3, d=vh, at=at)
        if hl == "v":
            for i, p in enumerate(base + top):
                f.dot(*p, r=8, f="coral", at=hl_at, dl=i * 60)
        return base, top
    apex = (cx, 120)
    for i in range(n):
        j = (i + 1) % n
        hid = base[i][1] < yb - 5 and base[j][1] < yb - 5
        f.line(*base[i], *base[j], c="soft" if hid else "ink", w=2 if hid else 3, d=hid, at=at)
        vh = base[i][1] < yb - 5 and not (base[i][0] == min(p[0] for p in base) or base[i][0] == max(p[0] for p in base))
        f.line(*base[i], *apex, c="soft" if vh else "ink", w=2 if vh else 3, d=vh, at=at)
    if hl == "v":
        for i, p in enumerate(base + [apex]):
            f.dot(*p, r=8, f="coral", at=hl_at, dl=i * 60)
    return base, [apex]

def prism():
    S = Set("prism", "각기둥과 각뿔 — 면 · 모서리 · 꼭짓점", "각기둥·각뿔",
            {1: "각기둥의 구성 요소", 2: "각뿔의 구성 요소", 3: "수로 입체도형 찾기", 4: "각기둥과 각뿔 견주기", 5: "모서리 길이의 합"},
            pp=8,
            tips={1: "n각기둥: 면 n + 2 · 모서리 n × 3 · 꼭짓점 n × 2",
                  2: "n각뿔: 면 n + 1 · 모서리 n × 2 · 꼭짓점 n + 1",
                  3: "모서리 수 ÷ 3(각기둥) 또는 ÷ 2(각뿔)로 밑면의 변의 수 n을 찾아요",
                  4: "같은 n이면 각기둥과 각뿔의 차이는 밑면 하나 · 꼭짓점 한 개의 차이",
                  5: "밑면 모서리 n개(각기둥은 두 밑면) + 옆 모서리 n개"},
            note="각기둥 · 각뿔의 수는 외우기보다 ‘밑면의 변의 수 n’으로 세는 방법을 익히게 해 주세요. 겨냥도에서 밑면 · 옆면 · 꼭짓점을 직접 세어 규칙을 확인하면 오래 남아요.")
    R = rng(342)

    def g1():
        n = R.randint(3, 10)
        what = R.choice(["면", "모서리", "꼭짓점"])
        f = Fig()
        prism_fig(f, n, "p", hl="v" if what == "꼭짓점" else None)
        v = {"면": n + 2, "모서리": 3 * n, "꼭짓점": 2 * n}[what]
        rule = {"면": f"{n} + 2 = {n + 2}", "모서리": f"{n} × 3 = {3 * n}", "꼭짓점": f"{n} × 2 = {2 * n}"}[what]
        memo = {"면": "옆면 n개 + 밑면 2개", "모서리": "위 n · 아래 n · 옆 n", "꼭짓점": "위 n개 + 아래 n개"}[what]
        q = f"{KN[n]}각기둥의 {what}{'은' if what == '면' else '는'} 몇 개인가요?"
        lines = [L(f"밑면의 변의 수 n = {n}", memo=f"{KN[n]}각형 밑면"), L(rule, memo=memo), L(f"{v}개")]
        S.add(1, q, f"{v}개", "밑면의 변의 수 n으로 세요", lines, f.out(), ap=str(v), key=q)
    fill(S, 1, 20, g1)

    def g2():
        n = R.randint(3, 10)
        what = R.choice(["면", "모서리", "꼭짓점"])
        f = Fig()
        prism_fig(f, n, "y", hl="v" if what == "꼭짓점" else None)
        v = {"면": n + 1, "모서리": 2 * n, "꼭짓점": n + 1}[what]
        rule = {"면": f"{n} + 1 = {n + 1}", "모서리": f"{n} × 2 = {2 * n}", "꼭짓점": f"{n} + 1 = {n + 1}"}[what]
        memo = {"면": "옆면 n개 + 밑면 1개", "모서리": "밑면 n · 옆 n", "꼭짓점": "밑면 n개 + 꼭대기 1개"}[what]
        q = f"{KN[n]}각뿔의 {what}{'은' if what == '면' else '는'} 몇 개인가요?"
        lines = [L(f"밑면의 변의 수 n = {n}", memo=f"{KN[n]}각형 밑면"), L(rule, memo=memo), L(f"{v}개")]
        S.add(2, q, f"{v}개", "각뿔은 밑면이 1개, 꼭대기 꼭짓점이 1개", lines, f.out(), ap=str(v), key=q)
    fill(S, 2, 20, g2)

    def g3():
        n = R.randint(3, 12)
        kind = R.choice(["p", "y"])
        what = R.choice(["모서리", "꼭짓점", "면"])
        if kind == "p":
            v = {"면": n + 2, "모서리": 3 * n, "꼭짓점": 2 * n}[what]
            inv = {"면": f"{v} − 2 = {n}", "모서리": f"{v} ÷ 3 = {n}", "꼭짓점": f"{v} ÷ 2 = {n}"}[what]
            name = f"{KN[n]}각기둥"
            rule = {"면": "n + 2", "모서리": "n × 3", "꼭짓점": "n × 2"}[what]
            q = f"{what}{'이' if what == '면' else '가'} {v}개인 각기둥의 이름은 무엇인가요?"
        else:
            v = {"면": n + 1, "모서리": 2 * n, "꼭짓점": n + 1}[what]
            inv = {"면": f"{v} − 1 = {n}", "모서리": f"{v} ÷ 2 = {n}", "꼭짓점": f"{v} − 1 = {n}"}[what]
            name = f"{KN[n]}각뿔"
            rule = {"면": "n + 1", "모서리": "n × 2", "꼭짓점": "n + 1"}[what]
            q = f"{what}{'이' if what == '면' else '가'} {v}개인 각뿔의 이름은 무엇인가요?"
        f = Fig()
        prism_fig(f, n, kind, at=1)
        lines = [L(f"{what} 수 = {rule}", memo="규칙을 거꾸로"), L(inv, pre="n"), L(name)]
        S.add(3, q, name, "규칙을 거꾸로 써서 밑면의 변의 수 n을 구해요", lines, f.out(), omr="ex", key=q)
    fill(S, 3, 20, g3)

    def g4():
        n = R.randint(3, 10)
        k = S.count(4) % 3
        f = Fig()
        if k == 0:
            q = f"{KN[n]}각기둥과 {KN[n]}각뿔의 꼭짓점 수의 차는 몇 개인가요?"
            lines = [L(f"{n} × 2 = {2 * n}", pre="각기둥"), L(f"{n} + 1 = {n + 1}", pre="각뿔"), L(f"{2 * n} − {n + 1} = {n - 1}"), L(f"{n - 1}개")]
            v = n - 1
        elif k == 1:
            q = f"{KN[n]}각기둥의 모서리 수와 {KN[n]}각뿔의 모서리 수의 합은 몇 개인가요?"
            lines = [L(f"{n} × 3 = {3 * n}", pre="각기둥"), L(f"{n} × 2 = {2 * n}", pre="각뿔"), L(f"{3 * n} + {2 * n} = {5 * n}"), L(f"{5 * n}개")]
            v = 5 * n
        else:
            m = R.randint(3, 10)
            if m == n:
                return
            q = f"{KN[n]}각기둥의 면의 수와 {KN[m]}각뿔의 꼭짓점의 수의 합은 몇 개인가요?"
            lines = [L(f"{n} + 2 = {n + 2}", pre=f"{KN[n]}각기둥 면"), L(f"{m} + 1 = {m + 1}", pre=f"{KN[m]}각뿔 꼭짓점"), L(f"{n + 2} + {m + 1} = {n + m + 3}"), L(f"{n + m + 3}개")]
            v = n + m + 3
        S.add(4, q, f"{v}개", "각각 규칙으로 센 뒤 계산해요", lines, None, ap=str(v), key=q)
    fill(S, 4, 20, g4)

    def g5():
        n = R.randint(3, 8)
        k = S.count(5) % 2
        a, h = R.randint(2, 12), R.randint(3, 15)
        f = Fig()
        if k == 0:
            prism_fig(f, n, "p")
            T = 2 * n * a + n * h
            q = f"밑면이 한 변 {a} cm인 정{KN[n]}각형이고 높이가 {h} cm인 {KN[n]}각기둥의 모든 모서리 길이의 합은 몇 cm인가요?"
            lines = [L(f"{a} × {n} × 2 = {2 * n * a}", pre="두 밑면의 모서리", memo=f"밑면 모서리 {n}개씩 2개"), L(f"{h} × {n} = {n * h}", pre="옆 모서리", memo=f"높이와 같은 모서리 {n}개"), L(f"{2 * n * a} + {n * h} = {T}"), L(f"{T} cm")]
        else:
            prism_fig(f, n, "y")
            T = n * a + n * h
            q = f"밑면이 한 변 {a} cm인 정{KN[n]}각형이고 옆 모서리가 모두 {h} cm인 {KN[n]}각뿔의 모든 모서리 길이의 합은 몇 cm인가요?"
            lines = [L(f"{a} × {n} = {n * a}", pre="밑면의 모서리"), L(f"{h} × {n} = {n * h}", pre="옆 모서리"), L(f"{n * a} + {n * h} = {T}"), L(f"{T} cm")]
        S.add(5, q, f"{T} cm", "밑면 모서리와 옆 모서리를 나누어 세요", lines, f.out(), ap=str(T), key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 규칙과 대응 ══════════
def seq_fig(f, vals, labs, q_idx, jumps_at=0):
    xs = jump_line(f, vals, fmt=lambda v: "□" if v is None else str(v), jumps_at=[jumps_at] * (len(vals) - 1), jlab=None, z=30)
    for i, lb in enumerate(labs):
        a, b = xs[i], xs[i + 1]
        f.text((a + b) / 2, 290, lb, z=24, c="teal", at=jumps_at, b=700)
    return xs

def match_fig(f, n, at="q"):
    """성냥개비 삼각형 n개 이어 붙이기"""
    s = min(110, 520 / ((n + 1) / 2 + 0.5))
    x0 = 330 - s * (n + 1) / 4
    y0 = 400
    h = s * math.sqrt(3) / 2
    for i in range(n):
        up = i % 2 == 0
        xb = x0 + s * (i // 2) + (0 if up else s / 2)
        if up:
            pts = [(xb, y0), (xb + s, y0), (xb + s / 2, y0 - h)]
        else:
            pts = [(xb, y0 - h), (xb + s, y0 - h), (xb + s / 2, y0)]
        f.poly(pts, c="gold", w=6, at=at, dl=i * 120, f="gold", fo=0.08)

def table_fig(f, heads, rows, at="q", y=200, hl_col=None, hl_at=0, cell=None):
    """대응표 — heads: 두 줄 머리 · rows: [[첫 줄 값들], [둘째 줄 값들]]"""
    n = len(rows[0])
    cw = cell or min(100, 460 / n)
    hw = 120
    x0 = 330 - (hw + cw * n) / 2
    for r_ in range(2):
        yy = y + r_ * 80
        f.rect(x0, yy, hw, 80, c="ink", sw=2.5, f="sky", fo=0.15, at=at)
        f.text(x0 + hw / 2, yy + 50, heads[r_], z=26, b=700, at=at)
        for i, v in enumerate(rows[r_]):
            f.rect(x0 + hw + cw * i, yy, cw, 80, c="ink", sw=2.5, at=at)
            f.text(x0 + hw + cw * i + cw / 2, yy + 52, str(v), z=30 if len(str(v)) < 4 else 22, at=at, c="coral" if v == "?" else "ink", b=700 if v == "?" else 600)
    if hl_col is not None:
        f.rect(x0 + hw + cw * hl_col + 3, y + 3, cw - 6, 154, c="gold", sw=5, rx=6, at=hl_at)
    return x0, hw, cw

def rule():
    S = Set("rule", "규칙과 대응 — 수의 배열에서 대응 관계식까지", "규칙과 대응",
            {1: "더해 가는 규칙", 2: "곱하거나 커지는 차이 규칙", 3: "도형 배열의 규칙", 4: "대응표에서 식으로", 5: "대응 관계의 활용"},
            pp=8,
            tips={1: "이웃한 두 수의 차를 구해 보면 규칙이 보여요 — 3, 7, 11, 15 → 4씩 커져요",
                  2: "차가 일정하지 않으면 몫(몇 배)이나 차의 변화를 살펴요",
                  3: "1번째, 2번째, 3번째의 개수를 표로 만들어 늘어나는 수를 찾아요",
                  4: "대응표의 위 수와 아래 수 사이의 관계(× · +)를 찾아 △ = □ × 5처럼 식으로",
                  5: "두 양을 □와 △로 정하고 표를 만든 뒤 식을 세워요"},
            note="규칙 찾기는 ‘차 → 몫 → 차의 차’ 순서로 살피게 하고, 대응 관계는 표 → 식 → 계산의 흐름을 지키게 해 주세요. 식에 쓰는 기호(□, △)의 뜻을 말로 먼저 정하게 하면 좋아요.")
    R = rng(343)

    def g1():
        a, d = R.randint(1, 40), R.randint(2, 15) * (1 if S.count(1) % 4 else -1)
        n = 5
        vals = [a + d * i for i in range(n + 1)]
        if min(vals) < 0:
            a = -d * n + R.randint(1, 20)
            vals = [a + d * i for i in range(n + 1)]
        miss = R.choice([n, n - 1, 2]) if S.count(1) >= 10 else n
        shown = [v if i != miss else None for i, v in enumerate(vals)]
        q = "다음 수의 배열에서 □에 알맞은 수는 얼마인가요?  " + ", ".join("□" if v is None else str(v) for v in shown)
        f = Fig()
        seq_fig(f, shown, [f"{'+' if d > 0 else MI}{abs(d)}"] * n, miss)
        if miss == n:
            lines = [L(f"{vals[1]} − {vals[0]} = {d}" if d > 0 else f"{vals[0]} − {vals[1]} = {-d}", memo="이웃한 두 수의 차"), L(f"{abs(d)}씩 {'커져요' if d > 0 else '작아져요'}"), L(f"{vals[n - 1]} {'+' if d > 0 else MI} {abs(d)} = {vals[n]}")]
        else:
            lines = [L(f"{vals[1]} − {vals[0]} = {d}" if d > 0 and miss > 1 else f"{abs(vals[n] - vals[n - 1])}씩 {'커져요' if d > 0 else '작아져요'}", memo="이웃한 두 수의 차"), L(f"{vals[miss - 1]} {'+' if d > 0 else MI} {abs(d)} = {vals[miss]}"), L(f"□ = {vals[miss]}")]
        S.add(1, q, str(vals[miss]), "이웃한 두 수의 차를 구해 규칙을 찾아요", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 2
        if k == 0:
            a, r = R.randint(1, 5), R.randint(2, 4)
            vals = [a * r ** i for i in range(5)]
            if vals[-1] > 2000:
                return
            labs = [f"× {r}"] * 4
            q = "다음 수의 배열에서 □에 알맞은 수는 얼마인가요?  " + ", ".join(map(str, vals[:4])) + ", □"
            lines = [L(f"{vals[1]} ÷ {vals[0]} = {r}", memo="이웃한 두 수의 몫"), L(f"{r}배씩 커져요"), L(f"{vals[3]} × {r} = {vals[4]}")]
            plan = "차가 일정하지 않으면 몇 배인지 살펴요"
        else:
            a, d0, dd = R.randint(1, 20), R.randint(1, 5), R.randint(1, 3)
            vals = [a]
            for i in range(4):
                vals.append(vals[-1] + d0 + dd * i)
            labs = [f"+{d0 + dd * i}" for i in range(4)]
            q = "다음 수의 배열에서 □에 알맞은 수는 얼마인가요?  " + ", ".join(map(str, vals[:4])) + ", □"
            lines = [L(f"차: {d0}, {d0 + dd}, {d0 + 2 * dd}", memo=f"차가 {dd}씩 커져요"), L(f"다음 차는 {d0 + 3 * dd}"), L(f"{vals[3]} + {d0 + 3 * dd} = {vals[4]}")]
            plan = "차를 구하고, 차가 어떻게 변하는지 살펴요"
        f = Fig()
        seq_fig(f, vals[:4] + [None], labs, 4)
        S.add(2, q, str(vals[4]), plan, lines, f.out(), key=q)
    fill(S, 2, 20, g2)

    def g3():
        k = S.count(3) % 3
        n = R.randint(6, 30)
        f = Fig()
        if k == 0:
            match_fig(f, 4)
            v = 2 * n + 1
            q = f"성냥개비로 삼각형을 한 줄로 이어 붙여 만들어요. 삼각형이 1개면 3개, 2개면 5개, 3개면 7개가 필요해요. 삼각형 {n}개를 만들려면 성냥개비가 몇 개 필요한가요?"
            lines = [L("처음 3개, 삼각형이 하나 늘 때마다 2개씩", memo="3, 5, 7, …"), L(f"3 + 2 × ({n} − 1) = {v}"), L(f"{v}개")]
            plan = "늘어나는 수가 일정하면 처음 수 + 늘어난 수 × (개수 − 1)"
        elif k == 1:
            v = 3 * n + 1
            for i in range(4):
                x = 120 + i * 110
                f.rect(x, 300, 110, 110, c="gold", sw=6, f="gold", fo=0.08, dl=i * 120)
            q = f"성냥개비로 정사각형을 한 줄로 이어 붙여 만들어요. 정사각형이 1개면 4개, 2개면 7개, 3개면 10개가 필요해요. 정사각형 {n}개를 만들려면 성냥개비가 몇 개 필요한가요?"
            lines = [L("처음 4개, 하나 늘 때마다 3개씩", memo="4, 7, 10, …"), L(f"4 + 3 × ({n} − 1) = {v}"), L(f"{v}개")]
            plan = "처음 수 + 늘어나는 수 × (개수 − 1)"
        else:
            n = R.randint(5, 12)
            v = n * n
            for i in range(4):
                for j in range(i + 1):
                    for jj in range(i + 1):
                        f.rect(60 + sum(range(1, i + 1)) * 34 + i * 30 + j * 30, 470 - jj * 30, 28, 28, c="ink", sw=2, f="teal", fo=0.4, dl=i * 200)
            q = f"바둑돌을 정사각형 모양으로 1개, 4개, 9개, 16개, …로 늘어놓아요. {n}번째에는 바둑돌이 몇 개인가요?"
            lines = [L("1 × 1, 2 × 2, 3 × 3, 4 × 4, …", memo="한 변의 개수 = 순서"), L(f"{n} × {n} = {v}"), L(f"{v}개")]
            plan = "순서와 개수 사이의 규칙 — 한 변에 순서만큼"
        S.add(3, q, f"{v}개", plan, lines, f.out(), ap=str(v), key=q)
    fill(S, 3, 20, g3)

    def g4():
        k = S.count(4) % 3
        a = R.randint(2, 12)
        b = R.randint(1, 15)
        xs = [1, 2, 3, 4]
        if k == 0:
            ys = [a * x for x in xs]
            rel, form = f"△ = □ × {a}", lambda x: a * x
        elif k == 1:
            ys = [x + b for x in xs]
            rel, form = f"△ = □ + {b}", lambda x: x + b
        else:
            ys = [a * x + b for x in xs]
            rel, form = f"△ = □ × {a} + {b}", lambda x: a * x + b
        N_ = R.randint(8, 40)
        f = Fig()
        table_fig(f, ("□", "△"), [xs + [N_], ys + ["?"]])
        q = f"□와 △ 사이의 대응 관계가 표와 같아요(□: 1, 2, 3, 4일 때 △: {', '.join(map(str, ys))}). □가 {N_}일 때 △는 얼마인가요?"
        if k == 2:
            lines = [L(f"차: {a}씩 커져요 → □ × {a}", memo="□가 1 커질 때 △는 몇 커지나"), L(f"1 × {a} + {b} = {ys[0]}", memo=f"나머지 {b}를 더해요" if not bat(b) else f"나머지 {b}을 더해요"), L(rel), L(f"{N_} × {a} + {b} = {form(N_)}")]
        elif k == 0:
            lines = [L(f"{ys[1]} ÷ 2 = {a}", memo="△는 □의 몇 배?"), L(rel), L(f"{N_} × {a} = {form(N_)}")]
        else:
            lines = [L(f"{ys[0]} − 1 = {b}", memo="△는 □보다 얼마 큰가?"), L(rel), L(f"{N_} + {b} = {form(N_)}")]
        S.add(4, q, str(form(N_)), "표에서 □와 △의 관계를 식으로 — 그 식에 넣어요", lines, f.out(), key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 4
        f = Fig()
        if k == 0:
            n = R.randint(5, 30)
            v = 2 * n + 2
            for i in range(3):
                f.rect(140 + i * 130, 300, 120, 80, c="ink", sw=3, f="gold", fo=0.15, dl=i * 120)
            q = f"정사각형 탁자를 한 줄로 이어 붙이고 둘레에 사람이 앉아요. 탁자 1개면 4명, 2개면 6명, 3개면 8명이 앉을 수 있어요. 탁자 {n}개를 이어 붙이면 몇 명이 앉을 수 있나요?"
            lines = [L("탁자 수(□)와 앉는 사람 수(△): 4, 6, 8, …", memo="2명씩 늘어요"), L("△ = □ × 2 + 2", memo="양 끝 2명"), L(f"{n} × 2 + 2 = {v}"), L(f"{v}명")]
            ans, ap = f"{v}명", str(v)
        elif k == 1:
            gap = R.randint(20, 35)
            age = R.randint(8, 13)
            yrs = R.randint(3, 20)
            n1 = R.choice(PEOPLE)
            q = f"{n1}의 나이를 □, {n1}보다 {gap}살 많은 어머니의 나이를 △라 할 때, □가 {age + yrs}이면 △는 얼마인가요?"
            lines = [L(f"△ = □ + {gap}", memo="나이 차는 늘 같아요"), L(f"{age + yrs} + {gap} = {age + yrs + gap}"), L(f"{age + yrs + gap}")]
            ans, ap = str(age + yrs + gap), str(age + yrs + gap)
            table_fig(f, ("□", "△"), [[age, age + 1, age + 2, age + yrs], [age + gap, age + gap + 1, age + gap + 2, "?"]])
        elif k == 2:
            p = R.randint(3, 12) * 100
            n = R.randint(6, 25)
            q = f"한 자루에 {p}원인 연필 □자루의 값을 △원이라 할 때, □가 {n}이면 △는 얼마인가요?"
            lines = [L(f"△ = □ × {p}", memo="한 자루 값 × 자루 수"), L(f"{n} × {p} = {n * p}"), L(f"{n * p}")]
            ans, ap = str(n * p), str(n * p)
            table_fig(f, ("□", "△"), [[1, 2, 3, n], [p, 2 * p, 3 * p, "?"]])
        else:
            c = R.randint(2, 6)
            n = R.randint(4, 15)
            v = n * (c - 1)
            q = f"통나무를 {c}도막으로 자르려면 {c - 1}번 잘라야 해요. 이런 통나무 {n}개를 모두 {c}도막씩으로 자르려면 모두 몇 번 잘라야 하나요?"
            lines = [L(f"한 개에 {c} − 1 = {c - 1}번", memo="도막 수 − 1"), L(f"{c - 1} × {n} = {v}"), L(f"{v}번")]
            ans, ap = f"{v}번", str(v)
            for i in range(c):
                f.rect(80 + i * 500 / c, 320, 500 / c - 8, 60, c="ink", sw=3, f="gold", fo=0.25)
        S.add(5, q, ans, "두 양을 □, △로 두고 표 → 식 → 계산", lines, f.out(), ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S


# ══════════ 어림과 평균 ══════════
def rnd(n, p, how):
    u = 10 ** p
    if how == "올림":
        return -(-n // u) * u
    if how == "버림":
        return n // u * u
    return (n + u // 2) // u * u

def avg():
    S = Set("avg", "어림과 평균 — 올림 · 버림 · 반올림, 고르게 하기", "어림과 평균",
            {1: "올림 · 버림 · 반올림", 2: "어림의 활용", 3: "평균 구하기", 4: "평균으로 모르는 값 구하기", 5: "평균의 변화"},
            pp=8,
            tips={1: "올림: 그 아랫자리를 모두 올려요 · 버림: 모두 버려요 · 반올림: 바로 아랫자리가 5 이상이면 올려요",
                  2: "남김없이 담아야 하면 올림, 꽉 찬 것만 세면 버림",
                  3: "평균 = 자료의 합 ÷ 자료의 수 — 막대를 고르게 맞춘 높이",
                  4: "자료의 합 = 평균 × 자료의 수 → 모르는 값 = 전체 합 − 아는 값의 합",
                  5: "자료가 하나 늘면 새 합 ÷ 새 개수. 평균이 오르려면 새 값이 평균보다 커야 해요"},
            note="어림은 ‘어느 자리까지’를 꼭 먼저 확인하게 하고, 평균은 막대를 고르게 맞추는 그림으로 뜻을 잡은 뒤 공식으로 옮겨 가게 해 주세요.")
    R = rng(344)
    PN = {1: "십", 2: "백", 3: "천"}

    def g1():
        how = ["올림", "버림", "반올림"][S.count(1) % 3]
        p = R.randint(1, 3)
        n = R.randint(10 ** p + 1, 10 ** (p + 2) * 3)
        if n % 10 ** p == 0:
            return
        r = rnd(n, p, how)
        lo, hi = n // 10 ** p * 10 ** p, n // 10 ** p * 10 ** p + 10 ** p
        f = Fig()
        N_ = NL(f, lo, hi, y=360, step=10 ** p / 10, lab_step=10 ** p, z=26)
        N_.pt(n, str(n), at="q", f_="gold")
        N_.pt(r, str(r), at=1, f_="coral", up=False)
        q = f"{n}{'을' if bat(n) else '를'} {how}하여 {PN[p]}의 자리까지 나타내면 얼마인가요?"
        below = str(n)[-p:]
        if how == "반올림":
            dgt = int(str(n)[-p])
            lines = [L(f"{PN[p]}의 자리 아래 숫자: {below}", memo="바로 아랫자리를 봐요"), L(f"바로 아랫자리 숫자 {dgt} → {'올려요' if dgt >= 5 else '버려요'}", memo="5 이상 올림 · 4 이하 버림"), L(f"{r}")]
        else:
            lines = [L(f"{PN[p]}의 자리 아래 숫자: {below}", memo=f"{how} — 아랫자리를 {'모두 올려요' if how == '올림' else '모두 버려요'}"), L(f"{lo} < {n} < {hi}", memo="어느 두 수 사이?"), L(f"{r}")]
        S.add(1, q, str(r), f"{PN[p]}의 자리 아래를 보고 — {how}", lines, f.out(), key=q)
    fill(S, 1, 20, g1)

    def g2():
        k = S.count(2) % 4
        if k == 0:
            per = R.choice([10, 100]); n = R.randint(per + 1, per * 30)
            if n % per == 0:
                return
            c = -(-n // per)
            q = f"사탕 {n}개를 한 봉지에 {per}개씩 남김없이 모두 담으려면 봉지는 적어도 몇 개 필요한가요?"
            lines = [L(f"{n} ÷ {per} = {n // per} … {n % per}", memo="남은 것도 담아야 해요"), L(f"{n // per} + 1 = {c}", memo="올림"), L(f"{c}개")]
            ans, ap, plan = f"{c}개", str(c), "남는 것까지 담으려면 올림"
        elif k == 1:
            n = R.randint(1001, 99999)
            if n % 1000 == 0:
                return
            c = n // 1000
            q = f"동전으로 {com(n)}원이 있어요. 1000원짜리 지폐로 바꾸면 최대 몇 장까지 바꿀 수 있나요?"
            lines = [L(f"{n} ÷ 1000 = {c} … {n % 1000}", memo="1000원이 안 되는 돈은 못 바꿔요"), L("버림으로 천의 자리까지"), L(f"{c}장")]
            ans, ap, plan = f"{c}장", str(c), "꽉 찬 것만 세면 버림"
        elif k == 2:
            n = R.randint(101, 999)
            q = f"상자 하나에 사과를 100개까지 담을 수 있어요. 사과 {n}개를 모두 담으려면 상자는 적어도 몇 개 필요한가요?"
            c = -(-n // 100)
            if n % 100 == 0:
                return
            lines = [L(f"{n} ÷ 100 = {n // 100} … {n % 100}", memo="남은 사과도 담아야"), L(f"{n // 100} + 1 = {c}"), L(f"{c}개")]
            ans, ap, plan = f"{c}개", str(c), "남김없이 → 올림"
        else:
            w = Fr(R.randint(1001, 9999), 100)
            if (w * 10).denominator == 1:
                return
            r = Fr(int(w * 10 + Fr(1, 2)), 10)
            q = f"키가 {DEC(w)} cm인 학생의 키를 반올림하여 소수 첫째 자리까지 나타내면 몇 cm인가요?"
            d2 = int(w * 100) % 10
            lines = [L(f"소수 둘째 자리 숫자 {d2}", memo="바로 아랫자리"), L(f"{d2}{'은' if bat(d2) else '는'} {'5 이상 → 올려요' if d2 >= 5 else '4 이하 → 버려요'}"), L(f"{DEC(r)} cm")]
            ans, ap, plan = f"{DEC(r)} cm", DEC(r), "소수도 바로 아랫자리를 보고 반올림"
        S.add(2, q, ans, plan, lines, None, ap=ap, key=q)
    fill(S, 2, 20, g2)

    def bars(f, vals, labs, avg_v=None, at_avg=0, unit=""):
        n = len(vals)
        M = max(vals) * 1.15
        bw = min(90, 460 / n)
        gap = (520 - bw * n) / (n + 1)
        y0, H = 560, 380
        for i, v in enumerate(vals):
            x = 80 + gap + i * (bw + gap)
            h = H * v / M
            f.rect(x, y0 - h, bw, h, c="ink", sw=2.5, f="teal", fo=0.35)
            f.text(x + bw / 2, y0 - h - 12, str(v), z=24, b=700)
            f.text(x + bw / 2, y0 + 34, labs[i], z=22, c="soft")
        f.line(70, y0, 620, y0, c="ink", w=3)
        if avg_v is not None:
            ya = y0 - H * float(avg_v) / M
            f.line(70, ya, 620, ya, c="coral", w=4, d=True, at=at_avg)
            f.text(72, ya - 12, f"평균 {avg_v}", z=24, c="coral", b=700, a="s", at=at_avg)

    def g3():
        n = R.randint(4, 6)
        k = S.count(3) % 3
        unit, who = [("개", "읽은 책 수(권)"), ("점", "수학 점수"), ("번", "줄넘기 횟수")][k]
        rng_ = {0: (2, 15), 1: (60, 100), 2: (20, 90)}[k]
        vals = [R.randint(*rng_) for _ in range(n)]
        if sum(vals) % n:
            return
        av = sum(vals) // n
        names = R.sample(PEOPLE, n)
        f = Fig()
        bars(f, vals, names, av, at_avg=1)
        u = "권" if k == 0 else unit
        q = f"{', '.join(names)}의 {who.split('(')[0]}가 차례로 {', '.join(map(str, vals))}{u}이에요. 평균은 몇 {u}인가요?" if k else f"{', '.join(names)}가 한 달 동안 읽은 책이 차례로 {', '.join(map(str, vals))}권이에요. 한 사람이 평균 몇 권을 읽었나요?"
        lines = [L(f"{' + '.join(map(str, vals))} = {sum(vals)}", pre="자료의 합"), L(f"{sum(vals)} ÷ {n} = {av}", pre="평균", memo=f"자료의 수 {n}"), L(f"{av}{u}")]
        S.add(3, q, f"{av}{u}", "평균 = 자료의 합 ÷ 자료의 수", lines, f.out(), ap=str(av), key=q)
    fill(S, 3, 20, g3)

    def g4():
        n = R.randint(4, 6)
        av = R.randint(60, 92)
        vals = [R.randint(av - 15, min(100, av + 15)) for _ in range(n - 1)]
        x = av * n - sum(vals)
        if not (40 <= x <= 100):
            return
        names = R.sample(PEOPLE, n)
        f = Fig()
        bars(f, vals + [x], names, av, at_avg="q")
        q = f"{', '.join(names[:-1])}, {names[-1]}의 수학 점수 평균이 {av}점이에요. {', '.join(names[:-1])}의 점수가 차례로 {', '.join(map(str, vals))}점이면 {names[-1]}의 점수는 몇 점인가요?"
        lines = [L(f"{av} × {n} = {av * n}", pre="전체 합", memo="평균 × 자료의 수"), L(f"{' + '.join(map(str, vals))} = {sum(vals)}", pre="아는 점수의 합"), L(f"{av * n} − {sum(vals)} = {x}"), L(f"{x}점")]
        S.add(4, q, f"{x}점", "전체 합 = 평균 × 자료의 수 → 모르는 값 = 전체 합 − 아는 값의 합", lines, f.out(), ap=str(x), key=q)
    fill(S, 4, 20, g4)

    def g5():
        k = S.count(5) % 3
        n = R.randint(4, 9)
        av = R.randint(30, 80)
        f = None
        if k == 0:
            new = R.randint(av - 20, av + 40)
            tot = av * n + new
            if tot % (n + 1):
                return
            na = tot // (n + 1)
            q = f"학생 {n}명의 몸무게 평균이 {av} kg이에요. 몸무게가 {new} kg인 학생 한 명이 더 들어오면 {n + 1}명의 몸무게 평균은 몇 kg인가요?"
            lines = [L(f"{av} × {n} = {av * n}", pre="처음 합"), L(f"{av * n} + {new} = {tot}", pre="새 합"), L(f"{tot} ÷ {n + 1} = {na}", pre="새 평균"), L(f"{na} kg")]
            ans, ap = f"{na} kg", str(na)
            plan = "새 평균 = (처음 합 + 새 값) ÷ 새 개수"
        elif k == 1:
            up = R.randint(1, 4)
            new = av + up * (n + 1)
            q = f"{n}번의 시험 점수 평균이 {av}점이에요. 다음 시험을 보고 {n + 1}번의 평균이 {av + up}점이 되려면 다음 시험에서 몇 점을 받아야 하나요?"
            if new > 100:
                return
            lines = [L(f"{av + up} × {n + 1} = {(av + up) * (n + 1)}", pre="필요한 합"), L(f"{av} × {n} = {av * n}", pre="지금까지 합"), L(f"{(av + up) * (n + 1)} − {av * n} = {new}"), L(f"{new}점")]
            ans, ap = f"{new}점", str(new)
            plan = "목표 평균 × 새 개수 − 지금까지의 합"
        else:
            n2 = R.randint(3, 8)
            av2 = R.randint(30, 80)
            tot = av * n + av2 * n2
            if tot % (n + n2):
                return
            na = tot // (n + n2)
            q = f"남학생 {n}명의 평균 키가 {av + 100} cm, 여학생 {n2}명의 평균 키가 {av2 + 100} cm예요. 전체 {n + n2}명의 평균 키는 몇 cm인가요?"
            A, B = (av + 100) * n, (av2 + 100) * n2
            na = (A + B) // (n + n2)
            if (A + B) % (n + n2):
                return
            lines = [L(f"{av + 100} × {n} = {A}", pre="남학생 합"), L(f"{av2 + 100} × {n2} = {B}", pre="여학생 합"), L(f"({A} + {B}) ÷ {n + n2} = {na}", memo="전체 합 ÷ 전체 수"), L(f"{na} cm")]
            ans, ap = f"{na} cm", str(na)
            plan = "평균끼리 평균 내지 말고 — 전체 합 ÷ 전체 수"
        S.add(5, q, ans, plan, lines, None, ap=ap, key=q)
    fill(S, 5, 20, g5)
    return S
