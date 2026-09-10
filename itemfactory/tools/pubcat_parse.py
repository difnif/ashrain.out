# 출판사 평가자료 문항 카탈로그 (유형·배점 참고 전용 — 복제·서비스 노출 금지)
import glob, os, re, json, collections
ROMAN = {"Ⅰ": 1, "Ⅱ": 2, "Ⅲ": 3, "Ⅳ": 4, "Ⅴ": 5, "Ⅵ": 6}
NUM = re.compile(r"^(?:\[그림\]\s*)*(\d{1,2})(?:\s*\[그림\])*\s*$")
CHOICE = re.compile(r"^[①②③④⑤]")
SUBQ = re.compile(r"^(?:\(\d\)|[⑴⑵⑶⑷⑸])")

def meta(b):
    pub = "chunjae" if b.startswith("chunjae") else "donga"
    grade = int(b[b.index("_m") + 2])
    kind = b.split("__")[0].split("_", 2)[2]
    rest = b.split("__", 1)[1]
    level = ""
    if pub == "donga":
        m = re.search(r"해결해요_(\d)_(\d)_(기본|발전|쌍둥이)", rest)
        if m: unit, sub, level = int(m.group(1)), int(m.group(2)), m.group(3)
        else:
            m = re.search(r"_(\d)단원_(기본|발전|\d회)", rest) or re.search(r"_(\d)단원", rest)
            unit = int(m.group(1)) if m else 0; sub = 0
            level = (m.group(2) if m and m.lastindex and m.lastindex >= 2 else "")
            if "중간대비" in rest or "기말대비" in rest:
                unit = 0; level = re.search(r"(\d학기_(?:중간|기말)대비)", rest).group(1)
    else:
        m = re.search(r"^([ⅠⅡⅢⅣⅤⅥ])-(\d)_(.+?)\.txt$", rest) or re.search(r"^([ⅠⅡⅢⅣⅤⅥ])_(.+?)\.txt$", rest)
        unit = ROMAN[m.group(1)]
        if m.lastindex == 3: sub, level = int(m.group(2)), m.group(3)
        else: sub, level = 0, m.group(2)
    return pub, grade, kind, unit, sub, level

def split_items(txt):
    lines = txt.splitlines()
    items, cur = [], None
    for l in lines:
        s = l.strip()
        m = NUM.match(s)
        if m and 1 <= int(m.group(1)) <= 40:
            n = int(m.group(1))
            if cur is None or n == cur["no"] + 1 or (n == 1 and cur["no"] > 1) or (n <= 2 and cur["no"] >= 10):
                cur = {"no": n, "lines": []}; items.append(cur); continue
        if cur is not None and s and s not in ("[그림]", "[표]", "●○○", "●●○", "●●●"):
            cur["lines"].append(s)
    out = []
    for it in items:
        stem, choices, sub = [], [], []
        for s in it["lines"]:
            if CHOICE.match(s): choices.append(s)
            elif SUBQ.match(s): sub.append(s)
            elif not choices: stem.append(s)
        st = " ".join(stem)
        st = re.sub(r"\s+", " ", st).strip()
        if len(st) < 6: continue
        out.append({"no": it["no"], "stem": st[:400], "choices": len(choices), "subq": len(sub)})
    return out

cat = []
for f in sorted(glob.glob("txt/*.txt")):
    b = os.path.basename(f)
    if "해설" in b: continue
    pub, grade, kind, unit, sub, level = meta(b)
    txt = open(f, encoding="utf-8").read()
    if pub == "chunjae":                       # 천재 파일은 뒤에 '정답과 풀이'가 붙어 있다 — 문항부만
        cut = txt.find("정답과 풀이")
        if cut > 0: txt = txt[:cut]
    head = [l.strip() for l in txt[:500].splitlines() if l.strip()]
    for it in split_items(txt):
        it.update({"pub": pub, "grade": grade, "kind": kind, "unit": unit, "sub": sub, "level": level, "file": b})
        cat.append(it)
json.dump(cat, open("catalog.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
c = collections.Counter((it["pub"], it["grade"]) for it in cat)
print(len(cat), c)
print(collections.Counter((it["pub"], it["grade"], it["unit"]) for it in cat))
