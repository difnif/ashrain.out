# 세트 C — 사전식(알파벳 순) 나열 100제 · 영어 단어
from common import *
from math import factorial as fac

MEAN = {
    "CAT": "고양이", "DOG": "개", "SUN": "태양", "PEN": "펜", "BOX": "상자", "CUP": "컵", "MAP": "지도", "HAT": "모자",
    "RED": "빨간색", "BUS": "버스", "TOY": "장난감", "ARM": "팔", "ICE": "얼음", "ANT": "개미", "GOD": "신", "ACT": "행동",
    "STAR": "별", "BIRD": "새", "FISH": "물고기", "LION": "사자", "BOAT": "배", "MILK": "우유", "DESK": "책상", "RAIN": "비",
    "HOME": "집", "WIND": "바람", "GOLD": "금", "CAKE": "케이크", "SNOW": "눈", "KING": "왕", "FROG": "개구리", "WOLF": "늑대",
    "DUCK": "오리", "BEAR": "곰", "CORN": "옥수수", "SHIP": "배(큰 배)",
    "HEART": "마음", "BREAD": "빵", "PLANT": "식물", "HOUSE": "집", "WORLD": "세계", "TIGER": "호랑이", "MUSIC": "음악",
    "LIGHT": "빛", "WATER": "물", "MONEY": "돈", "CLOUD": "구름", "NIGHT": "밤", "BRAIN": "뇌", "CHAIR": "의자",
    "SMILE": "미소", "TRAIN": "기차", "HORSE": "말", "FRUIT": "과일", "PIANO": "피아노", "DREAM": "꿈", "OCEAN": "바다",
    "MAGIC": "마법", "BEACH": "해변", "STORY": "이야기", "EARTH": "지구", "LEMON": "레몬", "MELON": "멜론", "THING": "물건",
    "FRIEND": "친구", "MOTHER": "어머니", "FATHER": "아버지", "ORANGE": "오렌지", "SPRING": "봄", "GARDEN": "정원",
    "PLANET": "행성", "SILVER": "은", "FOREST": "숲", "ISLAND": "섬", "WINTER": "겨울", "CASTLE": "성", "MARKET": "시장",
    "SUNDAY": "일요일", "MONKEY": "원숭이", "POCKET": "주머니", "LISTEN": "듣다", "SILENT": "조용한",
    "BAT": "박쥐", "CAR": "자동차", "FAN": "선풍기", "JAM": "잼", "BAG": "가방", "RAT": "쥐", "SAD": "슬픈", "PAN": "프라이팬",
    "CAP": "모자", "LAMP": "램프", "HAND": "손", "FARM": "농장", "DARK": "어두운", "WAVE": "파도", "GAME": "게임",
    "NAME": "이름", "BEAN": "콩", "SALT": "소금", "KEY": "열쇠", "SKY": "하늘", "COAT": "외투", "DATE": "날짜",
    "LAKE": "호수", "WALK": "걷다",
    "CAB": "택시", "BAD": "나쁜", "BED": "침대", "ACE": "에이스(최고)", "BEAD": "구슬", "FACE": "얼굴", "CAFE": "카페",
    "FADE": "바래다", "DEAF": "귀가 먹은", "FED": "먹였다",
}


def lj(c, a, b):
    """알파벳 글자 읽기 받침: L(엘) M(엠) N(엔) R(알)"""
    return c + (a if c[-1] in "LMNR" else b)


def mj(w, a, b):
    return f"{w}({MEAN[w]})" + josa(MEAN[w], a, b)[len(MEAN[w]):]


def cards_txt(cs):
    return ", ".join(cs)


def all_strings(cards, k):
    return sorted("".join(p) for p in PERM(sorted(cards), k))


def nP(n, k):
    v = 1
    for i in range(k):
        v *= n - i
    return v


def rank_lines(cards, w):
    """w 의 순번을 앞 글자부터 덩어리로 세는 줄들, 순번"""
    n, k = len(cards), len(w)
    rem = sorted(cards)
    lines = []
    tot = 0
    terms = []
    for i, ch in enumerate(w):
        smaller = [c for c in rem if c < ch]
        blk = nP(n - i - 1, k - i - 1)
        if smaller:
            pre = w[:i]
            boxes = "□" * (k - i - 1)
            heads = ", ".join(pre + c + boxes for c in smaller)
            v = len(smaller) * blk
            lines.append(f"{heads} → {len(smaller)} × {blk} = {v}" if blk > 1 or len(smaller) > 1 else f"{heads} → {v}")
            tot += v
            terms.append(v)
        rem.remove(ch)
    r = tot + 1
    if terms:
        lines.append(" + ".join(map(str, terms)) + f" + 1 = {r}")
    else:
        lines.append(f"{w}보다 앞선 문자열이 없다 → 1")
    return lines, r


def kth_lines(cards, k_len, kk):
    """kk 번째 문자열을 덩어리로 찾아가는 줄들"""
    n = len(cards)
    rem = sorted(cards)
    pre = ""
    left = kk
    lines = []
    cum = kk - left
    for i in range(k_len):
        blk = nP(n - i - 1, k_len - i - 1)
        for c in rem:
            if left > blk:
                left -= blk
                cum += blk
                lines.append(f"{pre + c + '□' * (k_len - i - 1)} {blk}개 → {cum}번째까지")
            else:
                pre += c
                rem.remove(c)
                break
    return lines, pre


def intro(cards, k=None):
    s = f"알파벳 카드 {lj(cards_txt(cards), '이', '가')} 한 장씩 있다. "
    if k is None or k == len(cards):
        s += f"{len(cards)}장을 모두 한 줄로 늘어놓아 만든 문자열을 사전식(알파벳 순서)으로 나열할 때,"
    else:
        s += f"이 중 {k}장을 골라 한 줄로 늘어놓아 만든 문자열을 사전식(알파벳 순서)으로 나열할 때,"
    return s


def neg_txt(cards, k):
    n = len(cards)
    return ("카드 " + (f"{n}장 모두" if k == n else f"{k}장") + " · 같은 카드는 한 번 · 알파벳 순")


def tree(cards, k_len, kk):
    """칠판 방식: 번호를 덩어리 크기의 합으로 쪼개며 세로 나무로 내려간다.
    남은 수가 덩어리 크기와 같으면 그 덩어리의 마지막(남은 글자를 큰 것부터),
    1이면 그 덩어리의 첫째(남은 글자를 작은 것부터)로 끝낸다."""
    n = len(cards)
    rem = sorted(cards)
    left = kk
    pre = ""
    cols, terms = [], []
    row = 0
    mode, tail = None, ""
    for i in range(k_len):
        blk = nP(n - i - 1, k_len - i - 1)
        items = []
        chosen = None
        for c in rem:
            if left > blk:
                items.append((c, blk, False))
                terms.append(blk)
                left -= blk
            else:
                chosen = c
                items.append((c, blk, True))
                break
        cols.append(dict(start=row, items=items))
        row = row + len(items) - 1
        rem.remove(chosen)
        pre += chosen
        m = k_len - i - 1
        if left == blk:
            terms.append(blk)
            mode = "last" if blk > 1 else "one"
            tail = "".join(sorted(rem)[::-1][:m])
            break
        if left == 1:
            terms.append(1)
            mode = "first"
            tail = "".join(sorted(rem)[:m])
            break
    word = pre + tail
    assert sum(terms) == kk and len(word) == k_len
    sizes = [nP(n - i - 1, k_len - i - 1) for i in range(k_len - 1)]
    return dict(cols=cols, tail=tail, terms=terms, mode=mode, word=word, kk=kk,
                sizes=sorted({x for x in sizes if x > 1}))


def blocks_lines(n, k_len):
    """덩어리 크기를 공식대로 — 앞 j글자를 정하면 남은 (n − j)장으로 남은 (k_len − j)자리를 채운다(작은 덩어리부터).
    다 쓰면 「남은 4장을 한 줄로: 4 × 3 × 2 × 1 = 24」, 남으면 「남은 4장 중 2장을 차례로: 4 × 3 = 12」"""
    out = []
    for j in range(k_len - 1, 0, -1):
        m, slots = n - j, k_len - j
        v = nP(m, slots)
        if v <= 1:
            continue
        how = f"남은 {m}장 한 줄로" if m == slots else f"남은 {m}장 중 {slots}장 차례로"
        out.append(L(f"덩어리({how})", chain(m, slots), v))
    return out


def ga(n):
    return josa(str(n), "이", "가")


def lst(xs):
    return ", ".join(xs)


def ro(c):
    return c + ("으로" if c[-1] in "MN" else "로")


def steps_kth(t, cards):
    """칠판 말풀이: 숫자 분석 다음, 묶음을 다 쓴 글자 → 시작 글자(소모) → 최종 묶음"""
    rem = sorted(cards)
    pre = ""
    out = []
    ncol = len(t["cols"])
    for li, c in enumerate(t["cols"]):
        sk = [L for (L, b, ch) in c["items"] if not ch]
        ch = [L for (L, b, h) in c["items"] if h][0]
        blk = c["items"][-1][1]
        final = li == ncol - 1
        head = f"{pre}□" if pre else ""
        if not final:
            if sk:
                s = f"{ga(blk)} {len(sk)}개 → {lst([pre + L for L in sk])} 묶음 다 씀 → "
            else:
                s = f"{blk} 묶음은 0개 → 남은 {lst(rem)} 중 맨 앞 → "
            s += (f"{ro(ch)} 시작" if not pre else f"{pre} 다음은 {ch}") + f" ({ch} 소모)"
            out.append(s)
        else:
            rest = [x for x in rem if x != ch]
            if t["mode"] in ("last", "one") and blk > 1:
                if sk:
                    s = f"{ga(blk)} {len(sk) + 1}개 → 앞의 {len(sk)}개는 {lst([pre + L for L in sk])} 묶음 다 씀, 마지막 {josa(str(blk), '은', '는')} 최종 묶음"
                else:
                    s = f"마지막 {ga(blk)} 최종 묶음"
                s += f" → {pre + ch} 묶음({ch} 소모)의 맨 끝 → {('남은 ' + lj(lst(rest), '을', '를') + ' 큰 것부터') if len(rest) == len(t['tail']) else ('남은 ' + lst(rest) + ' 중 큰 것부터 ' + str(len(t['tail'])) + '장')} → {t['tail']}"
            elif t["mode"] == "first":
                s = (f"{ga(blk)} {len(sk)}개 → {lst([pre + L for L in sk])} 묶음 다 씀, " if sk else "")
                s += f"남은 1 → {pre + ch} 묶음({ch} 소모)의 맨 처음 → {('남은 ' + lj(lst(rest), '을', '를') + ' 작은 것부터') if len(rest) == len(t['tail']) else ('남은 ' + lst(rest) + ' 중 작은 것부터 ' + str(len(t['tail'])) + '장')} → {t['tail']}"
            else:  # 마지막 자리
                s = (f"1이 {len(sk)}개 → {lst([pre + L for L in sk])} 지나고, " if sk else "")
                s += f"마지막 1 → {pre + ch}"
            out.append(s)
        rem.remove(ch)
        pre += ch
    out.append(f"→ {t['word']}")
    return out


def steps_rank(t, cards):
    """단어를 따라가며 앞서는 묶음을 세고, 끝에 숫자 정리"""
    rem = sorted(cards)
    pre = ""
    out = []
    ncol = len(t["cols"])
    for li, c in enumerate(t["cols"]):
        sk = [L for (L, b, ch) in c["items"] if not ch]
        ch = [L for (L, b, h) in c["items"] if h][0]
        blk = c["items"][-1][1]
        final = li == ncol - 1
        lead = f"{ro(ch)} 시작" if not pre else f"{pre} 다음은 {ch}"
        s = lead + (f" → 앞에 {lst([pre + L for L in sk])} 묶음 → {blk} × {len(sk)}" if sk else " → 앞선 묶음 없음")
        if final:
            rest = [x for x in rem if x != ch]
            if t["mode"] == "last" and blk > 1:
                s += f" / 남은 {lj(t['tail'], '이', '가')} 큰 것부터 → {pre + ch} 묶음의 맨 끝 → {blk} 통째로"
            elif t["mode"] == "first":
                s += f" / 남은 {lj(t['tail'], '이', '가')} 작은 것부터 → {pre + ch} 묶음의 맨 처음 → 1"
            else:
                s += " / 마지막 글자 → 1"
        out.append(s)
        rem.remove(ch)
        pre += ch
    return out


def tree_note(t):
    if t["mode"] == "last" and t["tail"]:
        return f"마지막 {josa(str(t['terms'][-1]), '은', '는')} 덩어리 하나를 다 채운 것 → 그 덩어리의 맨 끝 → 남은 글자를 큰 것부터 {t['tail']}"
    if t["mode"] == "first" and t["tail"]:
        return f"마지막 1은 덩어리의 맨 처음 → 남은 글자를 작은 것부터 {t['tail']}"
    return ""


def tree_eq_kth(t):
    s = f"{t['kk']} = " + " + ".join(map(str, t["terms"]))
    n = tree_note(t)
    return s + (f" / {n}" if n else "") + f" / {t['kk']}번째 = {t['word']}"


def tree_eq_rank(t):
    s = " + ".join(map(str, t["terms"])) + f" = {t['kk']}"
    n = tree_note(t)
    return (f"{n.replace('→ 남은 글자를 큰 것부터', '— 남은 글자가 큰 것부터').replace('→ 남은 글자를 작은 것부터', '— 남은 글자가 작은 것부터')} / " if n else "") + s


PLAN_K = "덩어리 크기({sz})를 공식대로 먼저 구해 옆에 적어 두고, 번호를 큰 덩어리부터 쪼갠다(숫자 분석). 세로로 글자를 내려 적으며 다 쓴 카드는 지운다."
PLAN_R = "덩어리 크기를 공식대로 먼저 구해 두고, 단어를 따라 세로로 내려가며 앞서는 덩어리를 더한다. 남은 글자가 큰 것부터 놓여 있으면 그 덩어리를 통째로 더한다(맨 끝이니까)."


def q_rank(cards, w):
    k = len(w)
    ls, r = rank_lines(cards, w)
    S = all_strings(cards, k)
    t = tree(cards, k, r)
    assert t["word"] == w
    return dict(q=f"{intro(cards, k)} 단어 {mj(w, '은', '는')} 몇 번째인지 구하시오.",
                ans=r, chk=S.index(w) + 1, unit="번째", tree=t, blocks=blocks_lines(len(cards), k),
                steps=steps_rank(t, cards), numlast=" + ".join(map(str, t["terms"])) + f" = {r}",
                pos="카드 " + cards_txt(sorted(cards)), neg=neg_txt(cards, k),
                plan=PLAN_R, eq=tree_eq_rank(t))


def q_kth(cards, w):
    k = len(w)
    S = all_strings(cards, k)
    kk = S.index(w) + 1
    t = tree(cards, k, kk)
    assert t["word"] == w
    return dict(q=f"{intro(cards, k)} {kk}번째에 오는 문자열을 구하고, 그 단어의 뜻을 쓰시오.",
                ans=w, chk=S[kk - 1], ans_show=f"{w} ({MEAN[w]})", tree=t, blocks=blocks_lines(len(cards), k),
                num=f"{kk} = " + " + ".join(map(str, t["terms"])), steps=steps_kth(t, cards)[:-1] + [f"→ {w} ({MEAN[w]})"],
                pos="카드 " + cards_txt(sorted(cards)), neg=neg_txt(cards, k),
                plan=PLAN_K.format(sz=" · ".join(map(str, t["sizes"])) or "1"),
                eq=tree_eq_kth(t) + f" ({MEAN[w]})")


def q_kth_gen(cards, k, kk):
    """연속 알파벳 카드 — kk 번째 문자열(뜻이 있는 단어면 뜻도)"""
    S = all_strings(cards, k)
    t = tree(cards, k, kk)
    found = t["word"]
    assert found == S[kk - 1]
    word = found in MEAN
    tail = " 이 문자열은 영어 단어이다. 그 뜻도 쓰시오." if word else ""
    return dict(q=f"{intro(cards, k)} {kk}번째에 오는 문자열을 구하시오.{tail}",
                ans=found, chk=S[kk - 1], ans_show=(f"{found} ({MEAN[found]})" if word else found), tree=t, blocks=blocks_lines(len(cards), k),
                num=f"{kk} = " + " + ".join(map(str, t["terms"])), steps=steps_kth(t, cards),
                pos="카드 " + cards_txt(sorted(cards)) + " (알파벳 순서대로 연속)", neg=neg_txt(cards, k),
                plan=PLAN_K.format(sz=" · ".join(map(str, t["sizes"])) or "1"),
                eq=tree_eq_kth(t) + (f" ({MEAN[found]})" if word else ""))


def q_from_end(cards, w):
    k = len(w)
    S = all_strings(cards, k)
    ls, r = rank_lines(cards, w)
    t = tree(cards, k, r)
    tot = len(S)
    v = tot - r + 1
    return dict(q=f"{intro(cards, k)} 단어 {mj(w, '은', '는')} 뒤에서 몇 번째인지 구하시오.",
                ans=v, chk=len(S) - S.index(w), unit="번째", tree=t, blocks=blocks_lines(len(cards), k),
                steps=steps_rank(t, cards), numlast=" + ".join(map(str, t["terms"])) + f" = {r} (앞에서)",
                extra=[L(f"전체 문자열({len(cards)}장을 한 줄로)" if k == len(cards) else f"전체 문자열({len(cards)}장 중 {k}장을 차례로)", chain(len(cards), k), tot),
                       L("뒤에서(전체 − 앞에서 순번 + 1)", f"{tot} − {r} + 1", v)],
                pos="카드 " + cards_txt(sorted(cards)), neg=neg_txt(cards, k) + " · '뒤에서'",
                plan=PLAN_R + " 앞에서 순번을 구한 뒤 (전체) − (앞에서 순번) + 1.",
                eq=" / ".join([tree_eq_rank(t), f"전체 {chain(len(cards), k)} = {tot}", f"{tot} − {r} + 1 = {v}"]))


def q_between(w1, w2):
    cards = sorted(w1)
    assert sorted(w2) == cards
    S = all_strings(cards, len(w1))
    l1, r1 = rank_lines(cards, w1)
    l2, r2 = rank_lines(cards, w2)
    a, b = sorted([(r1, w1), (r2, w2)])
    v = b[0] - a[0] - 1
    return dict(q=f"{intro(cards, len(cards))} 두 단어 {mj(w1, '과', '와')} {w2}({MEAN[w2]}) 사이에 있는 문자열은 몇 개인지 구하시오.",
                ans=v, chk=abs(S.index(w1) - S.index(w2)) - 1, unit="개",
                pos="카드 " + cards_txt(cards) + f" · 두 단어는 같은 글자로 되어 있다", neg=neg_txt(cards, len(cards)) + " · '사이' = 두 단어는 빼고",
                plan="두 단어의 순번을 각각 구한 뒤 (큰 순번) − (작은 순번) − 1.",
                trees=[tree(cards, len(w1), r1), tree(cards, len(w2), r2)], blocks=blocks_lines(len(cards), len(cards)),
                eq=[f"{w1}: " + " + ".join(map(str, tree(cards, len(w1), r1)["terms"])) + f" = {r1}",
                    f"{w2}: " + " + ".join(map(str, tree(cards, len(w2), r2)["terms"])) + f" = {r2}",
                    L("사이(큰 순번 − 작은 순번 − 1)", f"{b[0]} − {a[0]} − 1", v)])


def build():
    I = []

    def add(lv, d):
        d["lv"] = lv
        d["cards"] = d["pos"].split("카드 ")[1].split(" (")[0].split(" · ")[0].split(", ")
        I.append(d)

    W = lambda w: sorted(w)
    AB = lambda n: [chr(65 + i) for i in range(n)]
    S_ = lambda n, k: all_strings(AB(n), k)
    idx = lambda n, k, w: S_(n, k).index(w) + 1
    # ── 앞 50문항: A부터 연속한 카드, ○번째 문자열 찾기 ──
    # 1단계 (10): A, B, C 모두 · A, B, C, D 중 2장
    for kk in (2, 5, 3, 6, 1, 4):
        add(1, q_kth_gen(AB(3), 3, kk))
    for kk in (3, 7, 10, 12):
        add(1, q_kth_gen(AB(4), 2, kk))
    # 2단계 (16): A ~ D 모두 · A ~ D 중 3장(뜻 있는 단어 섞기)
    for kk in (4, 7, 9, 12, 14, 16, 19, 21, 23, 24):
        add(2, q_kth_gen(AB(4), 4, kk))
    for kk in (5, 11, idx(4, 3, "CAB"), idx(4, 3, "BAD"), 17, 22):
        add(2, q_kth_gen(AB(4), 3, kk))
    # 3단계 (24): A ~ E 모두 · A ~ E 중 3장 · 4장 · A ~ F 중 3장 · 4장
    for kk in (10, 27, 33, 50, 58, 64, 75, 86, 97, 101, 113, 120):
        add(3, q_kth_gen(AB(5), 5, kk))
    for kk in (idx(5, 3, "ACE"), idx(5, 3, "BED"), 41):
        add(3, q_kth_gen(AB(5), 3, kk))
    for kk in (idx(5, 4, "BEAD"), 66, 103):
        add(3, q_kth_gen(AB(5), 4, kk))
    add(3, q_kth_gen(AB(6), 3, idx(6, 3, "FED")))
    for w in ("CAFE", "FACE", "FADE", "DEAF", "BEAD"):
        add(3, q_kth_gen(AB(6), 4, idx(6, 4, w)))
    # ── 뒤 50문항: 영어 단어 카드 ──
    # 4단계 (25): ○번째 문자열 찾기 — 3장 · 4장 · 5장 · 남는 카드
    for w in ["CAT", "ARM", "MAP", "BAG", "HAT", "DOG", "SUN", "PEN", "TOY", "STAR", "CAKE", "LAMP", "BIRD", "FISH", "LION",
              "HEART", "PIANO", "HORSE", "FRUIT", "OCEAN"]:
        add(4, q_kth(W(w), w))
    for w, ex in [("CUP", "AS"), ("BOX", "ER"), ("SNOW", "AE"), ("WOLF", "AE"), ("MILK", "AS")]:
        add(4, q_kth(sorted(w + ex), w))
    # 5단계 (25): 몇 번째인가 · 뒤에서 몇 번째 · 두 단어 사이
    for w in ["BUS", "RED", "ICE", "KEY", "COAT", "LAKE", "WIND", "GOLD", "FROG", "KING", "HOUSE", "TIGER", "MUSIC", "WATER", "CLOUD"]:
        add(5, q_rank(W(w), w))
    for w in ["DUCK", "BRAIN"]:
        add(5, q_from_end(W(w), w))
    for w in ["FRIEND", "MOTHER", "ORANGE"]:
        add(5, q_rank(W(w), w))
    for w, ex in [("CAT", "BO"), ("STAR", "EP"), ("HEART", "BS")]:
        add(5, q_rank(sorted(w + ex), w))
    for a, b in [("HEART", "EARTH"), ("LEMON", "MELON")]:
        add(5, q_between(a, b))
    return I


if __name__ == "__main__":
    I = build()
    from collections import Counter
    print(len(I), Counter(d["lv"] for d in I))
    for i, d in enumerate(I, 1):
        assert d["ans"] == d["chk"], (i, d["q"], d["ans"], d["chk"])
    print("all ok")
    for d in I[::9]:
        print(d["lv"], d["ans"], d["q"][-50:], "|", d["eq"])
