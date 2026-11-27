# 교실 모니터 「경우의 수와 확률 100제 해설」 — 단일 모드 오른쪽 그림(판서 줄과 맞물림)
#   seats  — 한 줄로 세우기: 자리 칸 · 묶음 · 고정된 사람 · 칸마다 가짓수(판서 줄에 맞춰 차례로) · 빈자리 ∨
#   grades — 학년별 선발: 학년마다 학생 점 · 이름 붙은 학생, 판서 줄에 나온 학년 · 학생이 빛난다
#   bag    — 주머니 공: 주머니 속 공(색 · 번호), 판서 줄에 나온 색 · 수가 빛난다
# 줄 번호(at)는 판서 줄 목록(lines)에서 찾는다: "neg" · "e0"(식 첫 줄) · 또는 그 줄에 들어 있는 글자.
import re
from math import factorial as fac


def fac_s(n):
    return " × ".join(str(i) for i in range(n, 0, -1)) if n > 1 else "1"


def anchor(lines, a):
    if a == "pos":
        return 0
    if a == "neg":
        return 1
    if isinstance(a, int):
        return a
    m = re.fullmatch(r"e(\d+)", a)
    if m:
        return min(2 + int(m.group(1)), len(lines) - 1)
    for i in range(2, len(lines)):
        if a in lines[i]["s"]:
            return i
    raise KeyError(f"판서 줄에 '{a}' 없음: " + " | ".join(l["s"] for l in lines))


# ───────── seats ─────────
def U(lab="", w=None, hi=False, cnt=None, inner=None, gap=False):
    labs = lab if isinstance(lab, list) else (lab.split() if (" " in lab and w != 1) else [lab])
    w = w or len(labs) or 1
    if len(labs) < w:
        labs = labs + [""] * (w - len(labs))
    u = {"w": w, "lab": labs}
    if hi:
        u["hi"] = True
    if cnt is not None:
        u["cnt"] = str(cnt)
    if inner:
        u["inner"] = inner
    if gap:
        u["gap"] = True
    return u


def R(cap, at, units, cntAt=None, innerAt=None, swaps=None, note=None, noteAt=None):
    return {"cap": cap, "at": at, "units": units, "cntAt": cntAt or at, "innerAt": innerAt or cntAt or at,
            "swaps": swaps or [], "note": note, "noteAt": noteAt or cntAt or at}


def blanks(k, start):
    """가짓수 start, start-1, … 를 단 빈칸 k개"""
    return [U("", cnt=start - i) for i in range(k)]


def counts(units, start):
    """가짓수가 없는 칸(고정 · 빈자리 제외)에 start 부터 차례로"""
    c = start
    for u in units:
        if "cnt" not in u and not u.get("hi") and not u.get("gap") and not u.get("keep"):
            u["cnt"] = str(c)
            c -= 1
    return units


L = lambda n: [chr(65 + i) for i in range(n)]


def seats_fig(tpl, p, lines):
    n, b, g, k = p.get("n"), p.get("b"), p.get("g"), p.get("k")
    if b is not None and g is not None:
        n = b + g
    rows = []
    if tpl == "d_all":
        rows = [R("자리", "e0", blanks(n, n))]
    elif tpl == "d_choose":
        rows = [R(f"자리 {k}개", "e0", blanks(k, n))]
    elif tpl == "d_fixed_front":
        rows = [R("A는 맨 앞", "neg", counts([U("A", hi=True)] + [U() for _ in range(n - 1)], n - 1), cntAt="e0")]
    elif tpl == "d_fixed_mid":
        m = (n + 1) // 2
        us = [U() for _ in range(n)]
        us[m - 1] = U("C", hi=True)
        rows = [R(f"C는 {m}번째", "neg", counts(us, n - 1), cntAt="e0")]
    elif tpl == "d_front_back":
        rows = [R("A 맨 앞 · B 맨 뒤", "neg", counts([U("A", hi=True)] + [U() for _ in range(n - 2)] + [U("B", hi=True)], n - 2), cntAt="e0")]
    elif tpl in ("d_ends_AB", "p_ends"):
        rows = [R("A, B는 양 끝", "neg", counts([U("A", hi=True)] + [U() for _ in range(n - 2)] + [U("B", hi=True)], n - 2), cntAt="가운데",
                  swaps=[{"a": 0, "b": n - 1, "lab": "2 × 1", "at": "양 끝"}])]
    elif tpl == "d_A_an_end":
        rows = [R("A가 맨 앞", "A가 맨 앞", counts([U("A", hi=True)] + [U() for _ in range(n - 1)], n - 1)),
                R("A가 맨 뒤", "A가 맨 뒤", counts([U() for _ in range(n - 1)] + [U("A", hi=True)], n - 1))]
    elif tpl == "d_A_not_front":
        rows = [R("전체", "e0", blanks(n, n)),
                R("A가 맨 앞 → 뺀다", "A가 맨 앞", counts([U("A", hi=True)] + [U() for _ in range(n - 1)], n - 1))]
    elif tpl == "d_ends_boys":
        us = [U("남", hi=True, cnt=b)] + [U() for _ in range(n - 2)] + [U("남", hi=True, cnt=b - 1)]
        for i, u in enumerate(us[1:-1]):
            u["cnt"] = str(n - 2 - i); u["ca"] = "가운데"
        rows = [R("양 끝은 남학생", "neg", us, cntAt="양 끝")]
    elif tpl == "d_ends_girl_one":
        mid = lambda: [U("", cnt=n - 2 - i) for i in range(n - 2)]
        rows = [R("(남, 여)", "(남, 여)", [U("남", hi=True, cnt=b)] + mid() + [U("여", hi=True, cnt=g)]),
                R("(여, 남)", "(여, 남)", [U("여", hi=True, cnt=g)] + mid() + [U("남", hi=True, cnt=b)])]
    elif tpl in ("d_adj2", "p_adj"):
        at = "e0" if tpl == "d_adj2" else "이웃"
        rows = [R("A, B를 한 묶음으로", "neg", counts([U("A B", inner="× 2 × 1")] + [U() for _ in range(n - 2)], n - 1), cntAt=at, innerAt="묶음 안")]
    elif tpl == "d_adj3":
        rows = [R("A, B, C를 한 묶음으로", "neg", counts([U("A B C", inner="× 3 × 2 × 1")] + [U() for _ in range(n - 3)], n - 2), cntAt="e0", innerAt="묶음 안")]
    elif tpl == "d_not_adj":
        rows = [R("전체", "전체", blanks(n, n)),
                R("이웃하는 경우 → 뺀다", "이웃", counts([U("A B", inner="× 2 × 1")] + [U() for _ in range(n - 2)], n - 1), innerAt="묶음 안")]
    elif tpl == "d_adj_order":
        rows = [R("A 바로 뒤에 B — 순서가 정해진 묶음", "neg", counts([U("A B", inner="순서 고정")] + [U() for _ in range(n - 2)], n - 1), cntAt="e0")]
    elif tpl == "d_groups":
        rows = [R("남끼리 · 여끼리 한 묶음", "neg",
                  [U(" ".join(["남"] * b), inner=f"× {fac_s(b)}"), U(" ".join(["여"] * g), inner=f"× {fac_s(g)}")], cntAt="e0", innerAt="묶음 안",
                  swaps=[{"a": 0, "b": 1, "lab": "2 × 1"}])]
    elif tpl == "d_girls_together":
        rows = [R("여학생 묶음 + 남학생", "neg", counts([U(" ".join(["여"] * g), inner=f"× {fac_s(g)}")] + [U("남") for _ in range(b)], b + 1), cntAt="e0", innerAt="묶음 안")]
    elif tpl in ("d_ends_and_adj", "p_adj_and_end"):
        us = [U("A", hi=True)] + [U("C D", inner="× 2 × 1")] + [U() for _ in range(n - 4)] + [U("B", hi=True)]
        counts(us, n - 3)
        rows = [R("A, B 양 끝 · C, D 묶음", "neg", us, cntAt="가운데", innerAt="묶음 안", swaps=[{"a": 0, "b": len(us) - 1, "lab": "2 × 1", "at": "양 끝"}])]
    elif tpl in ("d_front_and_adj", "p_end_and_adj"):
        at = "e0" if tpl == "d_front_and_adj" else "e1"
        rows = [R("A 맨 앞 · B, C 묶음", "neg", counts([U("A", hi=True), U("B C", inner="× 2 × 1")] + [U() for _ in range(n - 3)], n - 2), cntAt=at, innerAt="묶음 안")]
    elif tpl == "d_pair_at_end":
        rows = [R("묶음이 앞쪽 끝", "e0", counts([U("A B", inner="× 2 × 1")] + [U() for _ in range(n - 2)], n - 2), cntAt="나머지", innerAt="묶음 안"),
                R("묶음이 뒤쪽 끝", "e0", counts([U() for _ in range(n - 2)] + [U("A B", inner="× 2 × 1")], n - 2), cntAt="나머지", innerAt="묶음 안")]
        rows[0]["units"][0].pop("cnt", None)
        rows[1]["units"][-1].pop("cnt", None)
        for r in rows:
            c = n - 2
            for u in r["units"]:
                if u["lab"][0] == "":
                    u["cnt"] = str(c); c -= 1
    elif tpl == "d_alt":
        def alt(first, cnt_on):
            seq = []
            nb = nm = 0
            for i in range(n):
                sx = first if i % 2 == 0 else ("여" if first == "남" else "남")
                if sx == "남":
                    seq.append(U("남", cnt=(b - nb) if cnt_on else None)); nb += 1
                else:
                    seq.append(U("여", cnt=(g - nm) if cnt_on else None)); nm += 1
            return seq
        if b == g:
            rows = [R("남이 앞", "e0", alt("남", True), cntAt="남학생"), R("여가 앞", "e0", alt("여", True), cntAt="남학생")]
        else:
            rows = [R("양 끝이 남학생인 꼴 하나", "e0", alt("남", True), cntAt="남학생")]
        for r in rows:
            r["mixed"] = True          # 남 · 여 가짓수가 섞여 있다(남 b! · 여 g! 로 따로 곱한다)
    elif tpl == "d_girls_ends_boys_adj":
        us = [U("여", hi=True, cnt=3), U("여"), U(" ".join(["남"] * b), inner=f"× {fac(b)}"), U("여", hi=True, cnt=2)]
        rows = [R("양 끝 여 · 가운데에 여 1명과 남 묶음", "neg", us, cntAt="양 끝", innerAt="묶음 안",
                  swaps=[{"a": 1, "b": 2, "lab": "2", "at": "가운데"}])]
    elif tpl in ("d_gap", "p_gap"):
        at1, at2 = "남학생", "빈자리"
        us = [U("∨", gap=True)]
        for i in range(b):
            us += [U("남", cnt=b - i), U("∨", gap=True)]
        gi = 0
        for u in us:
            if u.get("gap") and gi < g:
                u["cnt"] = str(b + 1 - gi); u["ca"] = at2; gi += 1
        rows = [R(f"남학생을 먼저 · 빈자리 {b + 1}곳에 여학생", "neg", us, cntAt=at1)]
    elif tpl == "d_adj_not_end":
        rows = [R("이웃", "이웃", counts([U("A B", inner="× 2 × 1")] + [U() for _ in range(n - 2)], n - 1), innerAt="묶음 안"),
                R("묶음이 끝에 닿음 → 뺀다", "끝에", [U("A B", inner="앞 · 뒤 2 × 2")] + [U("", cnt=n - 2 - i) for i in range(n - 2)])]
    elif tpl == "d_two_pairs":
        rows = [R("A·B 묶음 · C·D 묶음", "neg", counts([U("A B", inner="× 2 × 1"), U("C D", inner="× 2 × 1")] + [U() for _ in range(n - 4)], n - 2), cntAt="e0", innerAt="묶음 안")]
    elif tpl == "d_before":
        a = [U("A", hi=True), U(), U("B", hi=True)] + [U() for _ in range(n - 3)]
        bb = [U("B", hi=True), U(), U("A", hi=True)] + [U() for _ in range(n - 3)]
        rows = [R("A가 앞", "neg", a), R("B가 앞 — 자리만 바꾼 짝", "절반", bb, note=f"짝이 하나씩 → {fac(n)} ÷ 2")]
    elif tpl == "d_three_sep":
        rows = [R("B A C 묶음(가운데 A)", "neg", counts([U("B A C", inner="양옆 × 2 × 1")] + [U() for _ in range(n - 3)], n - 2), cntAt="e0", innerAt="양옆")]
        rows[0]["units"][0]["mid"] = True
    elif tpl == "p_end_girl":
        us = [U("남", hi=True, cnt=b)] + [U("", cnt=n - 2 - i) for i in range(n - 2)] + [U("남", hi=True, cnt=b - 1)]
        rows = [R("반대: 양 끝 모두 남 → 1에서 뺀다", "양 끝", us)]
    else:
        return None
    for r in rows:
        for key in ("at", "cntAt", "innerAt", "noteAt"):
            if key in r and r[key] is not None:
                r[key] = anchor(lines, r[key])
        for s in r["swaps"]:
            s["at"] = anchor(lines, s.get("at", r["cntAt"]))
        for u in r["units"]:
            if "ca" in u:
                u["ca"] = anchor(lines, u["ca"])
    return {"kind": "seats", "rows": rows}


# ───────── grades (학년별 선발) ─────────
NAMES = ["민준", "서연", "하준", "지우", "도윤", "수아", "예준", "하은", "시우", "유나", "주원", "채원"]


def grades_fig(q, lines):
    head = q.split("으로 이루어져 있다")[0]
    gg = re.findall(r"(\d)학년 남학생 (\d+)명·여학생 (\d+)명", head)
    groups = []
    if gg:
        for gr, m, f in gg:
            groups.append({"lab": f"{gr}학년", "key": gr, "m": int(m), "f": int(f)})
    else:
        gs = re.findall(r"(\d)학년 (\d+)명", head)
        if gs:
            for gr, c in gs:
                groups.append({"lab": f"{gr}학년", "key": gr, "n": int(c)})
        else:
            mf = re.search(r"남학생 (\d+)명, 여학생 (\d+)명", head)
            if not mf:
                return None
            groups = [{"lab": "남학생", "key": "남", "n": int(mf.group(1))}, {"lab": "여학생", "key": "여", "n": int(mf.group(2))}]
    rest = q[len(head):]
    named = []
    for mm in re.finditer(r"(\d)학년 (" + "|".join(NAMES) + r")", rest):
        gr, nm = mm.group(1), mm.group(2)
        idx = 1 if any(x["g"] == gr for x in named) else 0
        named.append({"g": gr, "i": idx, "name": nm})
    hl, spec = [None], None
    dflt = "all" if lines[0]["s"].startswith("모두") else None     # 전체에서 뽑는 문항은 모두를 가리킨 채로
    for i, ln in enumerate(lines[1:], 1):
        s = (ln.get("pre") or "") + " " + ln["s"]
        on = set()
        for mm in re.finditer(r"(\d)(?:[,·] ?(\d))?(?:[,·] ?(\d))?학년", s):
            on.update(x for x in mm.groups() if x)
        if groups[0]["key"] == "남":
            if "남" in s:
                on.add("남")
            if "여" in s:
                on.add("여")
        who = [x["name"] for x in named if x["name"] in s]
        on = sorted(x for x in on if any(gp["key"] == x for gp in groups))
        if on or who:
            st = spec = {"g": on, "w": who}
        elif re.match(r"\s*(모든 경우|전체|모두)", ln["s"]):
            st = "all"
        else:
            st = spec or dflt        # 앞 줄에서 가리킨 것을 이어서 센다
        hl.append(st)
    return {"kind": "grades", "groups": groups, "named": named, "hl": hl}


# ───────── bag (주머니 공) ─────────
COLORS = ["빨간", "파란", "노란", "흰", "검은", "초록"]


def _balls(txt):
    cs = re.findall(r"(" + "|".join(COLORS) + r") 공 (\d+)개", txt)
    return [{"c": c} for c, k in cs for _ in range(int(k))]


def bag_fig(q, lines):
    bags = []
    m2 = re.search(r"주머니 A에는 (.+?), 주머니 B에는 (.+?)가 들어 있다", q)
    mn2 = re.search(r"주머니 A에는 1부터 (\d+)까지, 주머니 B에는 1부터 (\d+)까지의 자연수", q)
    mn = re.search(r"주머니에 (\d)부터 (\d+)까지의 (?:자연수|정수)가 하나씩 적힌 공", q)
    mc = re.search(r"주머니에 (.+?)가 들어 있다", q)
    if mn2:
        bags = [{"lab": "A", "balls": [{"n": i} for i in range(1, int(mn2.group(1)) + 1)]},
                {"lab": "B", "balls": [{"n": i} for i in range(1, int(mn2.group(2)) + 1)]}]
    elif m2:
        bags = [{"lab": "A", "balls": _balls(m2.group(1))}, {"lab": "B", "balls": _balls(m2.group(2))}]
    elif mn:
        bags = [{"lab": "", "balls": [{"n": i} for i in range(int(mn.group(1)), int(mn.group(2)) + 1)]}]
    elif mc:
        bags = [{"lab": "", "balls": _balls(mc.group(1))}]
    if not bags or any(not b["balls"] for b in bags) or sum(len(b["balls"]) for b in bags) > 48:
        return None
    numbered = "n" in bags[0]["balls"][0]
    hl, spec = [None], None
    for i, ln in enumerate(lines[1:], 1):
        s = ln["s"]
        per = []
        for bi, bg in enumerate(bags):
            seg = s
            if len(bags) == 2:   # 「A 홀수 · B 짝수」처럼 주머니마다 나뉘어 있으면 그 쪽만
                parts = [x.strip() for x in re.split(r" · |, ", s)]
                mine = [x for x in parts if x.startswith(bg["lab"] + " ") or x.startswith(bg["lab"] + "의")]
                other = [x for x in parts if x.startswith(bags[1 - bi]["lab"] + " ") or x.startswith(bags[1 - bi]["lab"] + "의")]
                if mine or other:
                    seg = " ".join(mine)
            on = []
            if numbered:
                nums = [b["n"] for b in bg["balls"]]
                lst = re.findall(r"(?<![\d(/{])(\d+)(?=, \d)|(?<=, )(\d+)(?![\d/}])", seg)
                vals = [int(a or b) for a, b in lst]
                if "(" in seg and re.search(r"\(\d+, \d+\)", seg):
                    vals = []
                if len(vals) >= 2 and all(v in nums for v in vals):
                    on = sorted(set(vals))
                else:
                    for a, b in re.findall(r"(\d+) ~ (\d+)", seg):
                        on += [v for v in nums if int(a) <= v <= int(b)]
                    for kk in re.findall(r"(\d+)의 배수", seg):
                        on += [v for v in nums if v % int(kk) == 0]
                    if "짝수" in seg and "합" not in seg and "곱" not in seg:
                        on += [v for v in nums if v % 2 == 0]
                    if "홀수" in seg and "합" not in seg and "곱" not in seg:
                        on += [v for v in nums if v % 2 == 1]
                    if "소수" in seg:
                        on += [v for v in nums if v > 1 and all(v % d for d in range(2, v))]
                    on = sorted(set(on))
                    if len(on) == len(nums) and "~" in seg:
                        on = []           # 「1 ~ 20」처럼 모두면 빛낼 것 없음
                idx = [j for j, b in enumerate(bg["balls"]) if b["n"] in on]
            else:
                cols = [c for c in COLORS if re.search(c + r"(?: 공|\b| |$)", seg)]
                if len(cols) == len({b["c"] for b in bg["balls"]}) and len(cols) > 1:
                    cols = []             # 모든 색이 다 나오면(포지티브 줄) 빛낼 것 없음
                idx = [j for j, b in enumerate(bg["balls"]) if b["c"] in cols]
            per.append(idx)
        if len(bags) == 2 and numbered:      # 순서쌍 (A의 수, B의 수)
            prs = re.findall(r"\((\d+), (\d+)\)", s)
            if prs:
                per = [[j for j, b in enumerate(bags[0]["balls"]) if str(b["n"]) in {x for x, _ in prs}],
                       [j for j, b in enumerate(bags[1]["balls"]) if str(b["n"]) in {y for _, y in prs}]]
        if any(per):
            st = spec = per
        elif re.match(r"\s*(모든 경우|전체|모두)", s):
            st = "all"
        else:
            st = spec
        hl.append(st)
    return {"kind": "bag", "bags": bags, "hl": hl}
