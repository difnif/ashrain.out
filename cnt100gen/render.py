import html, json, re, secrets, subprocess, sys, os
import pymupdf
from fractions import Fraction as F
import set_a, set_b, set_c, set_d
from common import fr

CODE_ALPHA = "23456789ABCDEFGHJKMNPQRSTUVWXYZ"


def new_code():
    return "".join(secrets.choice(CODE_ALPHA) for _ in range(6))


def fmt_code(c):
    return c[:3] + "-" + c[3:]


def rich(s):
    s = html.escape(s)
    s = re.sub(r"\{(-?\d+)/(\d+)\}", r'<span class="fr"><span class="n">\1</span><span class="d">\2</span></span>', s)
    s = re.sub(r"\$([^$]+)\$", r"<i>\1</i>", s)
    return s


def rich_line(x):
    """식 한 줄 — 「이름표: 식」이면 이름표를 옅게"""
    m = re.match(r"^([^:]*?):\s+(.*)$", x)
    if m and re.search(r"\d", m.group(2)):
        return f'<span class="lb">{rich(m.group(1))}:</span> {rich(m.group(2))}'
    return rich(x)


def rich_eq(eq):
    """식 — 줄 목록이면 줄마다(이름표 + 펼친 식), 글이면 그대로"""
    if isinstance(eq, list):
        return "".join(f'<span class="el">{rich_line(x)}</span>' for x in eq)
    return rich(eq)


def ans_str(d):
    if "ans_show" in d:
        return d["ans_show"]
    a = d["ans"]
    if isinstance(a, F):
        return fr(a) if a.denominator != 1 else str(a.numerator)
    return str(a) + d.get("unit", "")


def ans_plain(d):
    a = d["ans"]
    if isinstance(a, F):
        return f"{a.numerator}/{a.denominator}" if a.denominator != 1 else str(a.numerator)
    return str(a)


LVNAME = {1: "1단계", 2: "2단계", 3: "3단계", 4: "4단계", 5: "5단계"}

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Noto Sans CJK KR', sans-serif; color: #000; font-size: 10.6pt; line-height: 1.62; }
.code { position: fixed; top: 4.5mm; right: 6mm; font-size: 8pt; color: #595959; }
.page { width: 210mm; height: 297mm; padding: 12mm 12mm 10mm; page-break-after: always; position: relative; overflow: hidden; }
.page:last-child { page-break-after: auto; }
.hd { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 1.6pt solid #000; padding-bottom: 1.6mm; }
.hd .t { font-size: 13pt; font-weight: 700; }
.hd .nm { font-size: 9.5pt; }
.hd .nm span { display: inline-block; width: 30mm; border-bottom: 0.6pt solid #000; margin-left: 2mm; }
.note { font-size: 8.6pt; color: #333; margin: 1.4mm 0 2mm; }
.grid { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(3, 1fr); height: 250mm; border-top: 0.5pt solid #999; }
.cell { border-bottom: 0.5pt solid #999; padding: 3mm 3.5mm 2.5mm; position: relative; }
.cell:nth-child(odd) { border-right: 0.5pt solid #999; }
.no { font-weight: 700; font-size: 12pt; margin-right: 1.2mm; }
.lv { font-size: 7.6pt; border: 0.6pt solid #000; border-radius: 1mm; padding: 0 1.2mm; margin-right: 1.5mm; vertical-align: 1.5pt; }
.q { text-align: justify; word-break: keep-all; }
.sum { border-right: none !important; padding: 5mm 8mm; }
.sumt { font-weight: 700; font-size: 11pt; margin-bottom: 2mm; }
table.sumtb { border-collapse: collapse; width: 100%; font-size: 9.6pt; }
table.sumtb td { border: 0.5pt solid #777; padding: 1.4mm 2.5mm; }
table.sumtb td:first-child { width: 42%; font-weight: 500; }
.ab { position: absolute; right: 3.5mm; bottom: 3mm; font-size: 9.5pt; }
.ab span { display: inline-block; width: 26mm; height: 9mm; border: 0.7pt solid #000; vertical-align: middle; margin-left: 1.5mm; }
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; line-height: 1.05; margin: 0 0.6mm; font-size: 0.9em; }
.fr .n { border-bottom: 0.7pt solid #000; padding: 0 0.6mm; }
.fr .d { padding: 0 0.6mm; }
/* 해설지 */
.sol { width: 210mm; padding: 12mm 12mm 10mm; }
.sol .hd { margin-bottom: 2mm; }
table.qa { border-collapse: collapse; width: 100%; font-size: 8.8pt; margin: 2mm 0 4mm; }
table.qa td { border: 0.5pt solid #777; text-align: center; padding: 0.6mm 0.4mm; height: 9mm; }
table.qa td b { display: block; font-size: 7pt; color: #444; font-weight: 400; line-height: 1.1; }
.cols { column-count: 2; column-gap: 7mm; column-rule: 0.5pt solid #999; }
.it { break-inside: avoid; padding: 1.6mm 0 2.2mm; border-bottom: 0.4pt dashed #999; font-size: 9.3pt; line-height: 1.55; }
.it .top { font-weight: 700; margin-bottom: 0.6mm; }
.it .top .a { float: right; font-weight: 700; }
.it .r { display: flex; gap: 1.5mm; word-break: keep-all; }
.it .r .k { flex: none; width: 13mm; font-size: 8pt; border: 0.5pt solid #000; text-align: center; height: 4.6mm; line-height: 4.6mm; margin-top: 0.6mm; }
.it .r.eq .k { background: #000; color: #fff; }
.el { display: block; }
.lb { color: #4a4a4a; font-size: 0.9em; }
.tree { display: flex; gap: 4mm; align-items: flex-start; flex-wrap: wrap; margin: 0.6mm 0 0.8mm; }
.tdeck { flex-basis: 100%; font-size: 9pt; letter-spacing: 0.6mm; }
.tdeck span { display: inline-block; width: 4mm; text-align: center; }
.tdeck span.x { background: linear-gradient(to top right, transparent 46%, #000 47%, #000 53%, transparent 54%); }
.tgrid { display: inline-grid; grid-auto-columns: minmax(8mm, auto); column-gap: 1.2mm; font-size: 9.6pt; line-height: 4.3mm; }
.tc { white-space: nowrap; }
.tc.on { font-weight: 700; text-decoration: underline; text-underline-offset: 0.6mm; }
.tc.tail { font-weight: 700; letter-spacing: 0.4mm; }
.tb { font-size: 6.6pt; color: #444; margin-left: 0.6mm; vertical-align: 0.4mm; }
.tsz { display: flex; flex-direction: column; font-size: 8pt; line-height: 4.3mm; border-left: 0.5pt solid #999; padding-left: 2mm; text-align: right; }
.tsz b { font-weight: 500; font-size: 7pt; }
.num { font-weight: 700; font-size: 10.4pt; }
.lvh { column-span: all; font-weight: 700; font-size: 10.5pt; border-bottom: 1pt solid #000; margin: 3mm 0 1mm; padding-bottom: 0.6mm; }
.cover-note { font-size: 8.8pt; color: #222; margin: 1mm 0 0; }
"""


SUM_AB = (
    '<div class="sumt">한눈에 정리 — 셀 전략 고르기</div><table class="sumtb">'
    '<tr><td>둘 중 하나만 일어난다 (또는)</td><td>더한다 — 합의 법칙</td></tr>'
    '<tr><td>이어서·함께 일어난다 (그리고)</td><td>곱한다 — 곱의 법칙</td></tr>'
    '<tr><td>자격(차례)이 다른 2명·3명</td><td><i>n</i> × (<i>n</i> − 1), <i>n</i> × (<i>n</i> − 1) × (<i>n</i> − 2)</td></tr>'
    '<tr><td>자격이 같은 2명 · 동시에 2개</td><td><i>n</i> × (<i>n</i> − 1) ÷ 2</td></tr>'
    '<tr><td>자격이 같은 3명 · 동시에 3개</td><td><i>n</i> × (<i>n</i> − 1) × (<i>n</i> − 2) ÷ (3 × 2 × 1)</td></tr>'
    '<tr><td>꺼낸 공을 다시 넣는다 / 넣지 않는다</td><td>매번 그대로 / 한 개씩 줄어든다</td></tr>'
    '<tr><td>확률</td><td>(일어나는 경우의 수) ÷ (모든 경우의 수) — 둘을 같은 방법(차례 있음·없음)으로 센다</td></tr>'
    '<tr><td>\'적어도\' · \'아닐\'</td><td>1 − (반대 경우의 확률)</td></tr>'
    '<tr><td>절대 안 일어남 / 반드시 일어남</td><td>확률 0 / 확률 1</td></tr></table>')


SUM_C = (
    '<div class="sumt">한눈에 정리 — 사전식으로 몇 번째인지 세기</div><table class="sumtb">'
    '<tr><td>사전식(알파벳 순)</td><td>첫 글자가 빠른 것부터, 첫 글자가 같으면 둘째 글자로 비교</td></tr>'
    '<tr><td>한 덩어리의 크기</td><td>첫 글자를 정하면 남은 자리를 남은 카드로 채우는 수 — 예: 5장 모두 쓰면 4 × 3 × 2 × 1 = 24</td></tr>'
    '<tr><td>□번째인가?</td><td>목표 단어보다 앞서는 덩어리를 앞 글자부터 모두 더하고 + 1(그 단어 자신)</td></tr>'
    '<tr><td>□번째는 무엇?</td><td>덩어리 크기를 쌓아 가며 그 번호가 들어 있는 덩어리로 좁혀 간다</td></tr>'
    '<tr><td>뒤에서 몇 번째</td><td>(전체 개수) − (앞에서 순번) + 1</td></tr>'
    '<tr><td>두 단어 사이</td><td>(큰 순번) − (작은 순번) − 1</td></tr>'
    '<tr><td>카드가 남을 때</td><td>덩어리 크기 = 남은 카드에서 남은 자리만큼 차례로 곱한다 — 예: 6장 중 4장이면 첫 글자 뒤 5 × 4 × 3 = 60</td></tr></table>')
SUM_D = (
    '<div class="sumt">한눈에 정리 — 한 줄로 세우기</div><table class="sumtb">'
    '<tr><td><i>n</i>명을 한 줄로</td><td><i>n</i> × (<i>n</i> − 1) × … × 1</td></tr>'
    '<tr><td><i>n</i>명 중 <i>k</i>명을 한 줄로</td><td><i>n</i>부터 <i>k</i>개를 차례로 곱한다</td></tr>'
    '<tr><td>자리가 정해진 사람</td><td>먼저 세워 두고 나머지만 센다</td></tr>'
    '<tr><td>양 끝 조건</td><td>양 끝을 먼저 채우고 가운데를 센다</td></tr>'
    '<tr><td>이웃한다</td><td>한 묶음으로 보고 세운 뒤 × (묶음 안 순서)</td></tr>'
    '<tr><td>이웃하지 않는다</td><td>전체 − 이웃 / 여럿이면 나머지를 먼저 세우고 빈자리(사이와 양 끝)에 넣는다</td></tr>'
    '<tr><td>순서가 정해진 이웃 (A 바로 뒤에 B)</td><td>묶음 안 순서를 곱하지 않는다</td></tr>'
    '<tr><td>확률</td><td>(조건에 맞는 줄의 수) ÷ (모든 줄의 수)</td></tr></table>')
SUMMARY = {"AB": SUM_AB, "C": SUM_C, "D": SUM_D}


def tree_html(t, cards=None):
    cols = t["cols"]
    rows = max(c["start"] + len(c["items"]) for c in cols)
    cells = []
    for ci, c in enumerate(cols):
        for j, (L, blk, ch) in enumerate(c["items"]):
            num = "" if ch or blk == 1 else f'<span class="tb">{blk}</span>'
            cells.append(f'<span class="tc{" on" if ch else ""}" style="grid-column:{ci + 1};grid-row:{c["start"] + j + 1}">{L}{num}</span>')
    last = cols[-1]
    if t["tail"]:
        cells.append(f'<span class="tc tail" style="grid-column:{len(cols) + 1};grid-row:{last["start"] + len(last["items"])}">{t["tail"]}</span>')
    used = set("".join(L for c in cols for (L, b, ch) in c["items"] if ch))
    deck = ""
    if cards:
        deck = '<div class="tdeck">' + "".join(f'<span class="{"x" if L in used else ""}">{L}</span>' for L in cards) + "</div>"
    sizes = "".join(f"<span>{x}</span>" for x in t["sizes"]) or "<span>1</span>"
    return (f'<div class="tree">{deck}<div class="tgrid" style="grid-template-rows:repeat({rows},4.3mm)">{"".join(cells)}</div>'
            f'<div class="tsz"><b>덩어리</b>{sizes}</div></div>')


def problem_html(items, title, note, code, summ):
    pages = []
    for p in range(0, len(items), 6):
        cells = []
        for j, d in enumerate(items[p:p + 6]):
            no = p + j + 1
            cells.append(f'<div class="cell"><div class="q"><span class="no">{no}</span><span class="lv">{LVNAME[d["lv"]]}</span>{rich(d["q"])}</div>'
                         f'<div class="ab">답<span></span></div></div>')
        if len(cells) < 6:
            span = 6 - len(cells)
            cells.append(f'<div class="cell sum" style="grid-column: 1 / 3; grid-row: span {span // 2}">{summ}</div>')
        pages.append(f'<div class="page"><div class="hd"><div class="t">{html.escape(title)}</div>'
                     f'<div class="nm">이름<span></span></div></div><div class="note">{note}</div>'
                     f'<div class="grid">{"".join(cells)}</div></div>')
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body><div class="code">코드 {fmt_code(code)}</div>{"".join(pages)}</body></html>'


def solution_html(items, title, note, code, summ=None):
    rows = []
    for r in range(0, len(items), 10):
        tds = "".join(f'<td><b>{r + k + 1}</b>{rich(str(items[r + k]["ans"]) if "ans_show" in items[r + k] else ans_str(items[r + k]))}</td>' for k in range(10) if r + k < len(items))
        rows.append(f"<tr>{tds}</tr>")
    its = []
    cur = None
    for i, d in enumerate(items, 1):
        if d["lv"] != cur:
            cur = d["lv"]
            its.append(f'<div class="lvh">{LVNAME[cur]}</div>')
        if "steps" in d:
            rows = [f'<div class="r"><span class="k">포지티브</span><span>{rich(d["pos"])}</span></div>',
                    f'<div class="r"><span class="k">네거티브</span><span>{rich(d["neg"])}</span></div>']
            if d.get("blocks"):
                rows.append(f'<div class="r"><span class="k">덩어리</span><span>{rich_eq(d["blocks"])}</span></div>')
            if "num" in d:
                rows.append(f'<div class="r eq"><span class="k">숫자 분석</span><span class="num">{rich(d["num"])}</span></div>')
            rows.append('<div class="r"><span class="k">풀이</span><span>' + "<br>".join(rich(x) for x in d["steps"]) + "</span></div>")
            rows.append(f'<div class="r"><span class="k">세로 나무</span>{tree_html(d["tree"], d.get("cards"))}</div>')
            if "numlast" in d:
                rows.append(f'<div class="r eq"><span class="k">숫자 정리</span><span class="num">{rich(d["numlast"])}</span></div>')
            if "extra" in d:
                rows.append(f'<div class="r"><span class="k">뒤에서</span><span>{rich_eq(d["extra"])}</span></div>')
            its.append(f'<div class="it"><div class="top">{i}<span class="a">답 {rich(ans_str(d))}</span></div>' + "".join(rows) + "</div>")
            continue
        its.append(
            f'<div class="it"><div class="top">{i}<span class="a">답 {rich(ans_str(d))}</span></div>'
            f'<div class="r"><span class="k">포지티브</span><span>{rich(d["pos"])}</span></div>'
            f'<div class="r"><span class="k">네거티브</span><span>{rich(d["neg"])}</span></div>'
            f'<div class="r"><span class="k">전략</span><span>{rich(d["plan"])}</span></div>'
            + (f'<div class="r"><span class="k">세로 나무</span>{tree_html(d["tree"], d.get("cards"))}</div>' if "tree" in d else "")
            + "".join(f'<div class="r"><span class="k">{"나무 " + str(j + 1)}</span>{tree_html(t, d.get("cards"))}</div>' for j, t in enumerate(d.get("trees", [])))
            + (f'<div class="r"><span class="k">덩어리</span><span>{rich_eq(d["blocks"])}</span></div>' if d.get("blocks") else "")
            + f'<div class="r eq"><span class="k">식</span><span>{rich_eq(d["eq"])}</span></div></div>')
    body = (f'<div class="sol"><div class="hd"><div class="t">{html.escape(title)} · 해설</div><div class="nm"></div></div>'
            f'<div class="cover-note">{note} 포지티브 = 해도 되는 것(주어진 것), 네거티브 = 막는 제약 · 식 세우기 = 셀 전략.</div>'
            f'<div class="lvh" style="column-span:none">빠른 정답</div><table class="qa">{"".join(rows)}</table>'
            f'<div class="cols">{"".join(its)}</div></div>')
    css = CSS.replace("@page { size: A4; margin: 0; }", "@page { size: A4; margin: 12mm 0 10mm; @top-right { content: '코드 %s'; font-family: 'Noto Sans CJK KR'; font-size: 8pt; color: #595959; padding-right: 6mm; vertical-align: middle; } }" % fmt_code(code))
    css = css.replace(".sol { width: 210mm; padding: 12mm 12mm 10mm; }", ".sol { width: 210mm; padding: 0 12mm; } .sol > .hd { margin-top: 0; }")
    return f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{body}</body></html>'


def to_pdf(html_path, pdf_path):
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf_path}", "file://" + os.path.abspath(html_path)],
                   check=True, capture_output=True)


FIXED = {"선발": "SQ9HWR", "공꺼내기": "QS73DF", "사전식": "QHDWUB", "한줄세우기": "Z2W3KQ"}
FNAME = {"선발": "선발-경우의수확률100제", "공꺼내기": "공꺼내기-경우의수확률100제", "사전식": "사전식나열-영어단어100제", "한줄세우기": "한줄세우기-이웃양끝100제"}


def main():
    os.makedirs("out", exist_ok=True)
    ALL = {
        "선발": (set_a.build, "학년별 선발로 익히는 경우의 수와 확률 100제",
               "중2-2 · 1단계 → 5단계로 갈수록 어려워져요 · 확률은 기약분수로 답해요.", "학년별 선발", "AB"),
        "공꺼내기": (set_b.build, "주머니 속 공으로 익히는 경우의 수와 확률 100제",
                 "중2-2 · 1단계 → 5단계로 갈수록 어려워져요 · 확률은 기약분수로 답해요 · 공은 모두 서로 다른 공으로 봐요.", "주머니에서 공 꺼내기", "AB"),
        "사전식": (set_c.build, "영어 단어로 익히는 사전식 나열 100제",
                "중2-2 경우의 수 · 1단계 → 5단계 · 뜻이 없는 문자열도 모두 세요 · 단어 뜻은 덤으로 익혀요.", "사전식 나열(영어 단어)", "C"),
        "한줄세우기": (set_d.build, "한 줄로 세우기 100제 — 이웃 · 양 끝",
                  "중2-2 경우의 수 · 1단계 → 5단계 · 사람은 모두 서로 다른 사람으로 봐요 · 확률은 기약분수로 답해요.", "한 줄로 세우기", "D"),
    }
    keys = sys.argv[1:] or list(ALL)
    sets = [(k, ALL[k][0](), ALL[k][1], ALL[k][2], ALL[k][3], ALL[k][4]) for k in keys]
    codes = {}
    for key, items, title, note, sub, sk in sets:
        summ = SUMMARY[sk]
        for i, d in enumerate(items, 1):
            assert d["ans"] == d["chk"], (key, i)
        code = FIXED.get(key) or new_code()
        codes[key] = code
        for kind, fn in (("문제지", problem_html), ("해설지", solution_html)):
            h = f"out/{key}.{kind}.html"
            open(h, "w").write(fn(items, title, note, code, summ))
            raw = f"out/{key}.{kind}.raw.pdf"
            to_pdf(h, raw)
            final = f"out/{FNAME[key]}-{kind}.pdf"
            doc = pymupdf.open(raw)
            if kind == "문제지":
                manifest = {"kind": "ashrain.print", "version": 1, "code": code, "title": title,
                            "sub": f"중2-2 경우의 수와 확률 · {sub} · 단답형 100제", "label": "단답형",
                            "items": [{"no": str(i), "answer": ans_plain(d), "choice": False, "points": 1,
                                       "topic": f"{sub} · {LVNAME[d['lv']]}", "key": f"m2-2-{key}100-{i:03d}",
                                       "page": (i - 1) // 6 + 1} for i, d in enumerate(items, 1)]}
                data = json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8")
                doc.embfile_add("ashrain-print.json", data, filename="ashrain-print.json", desc="ashrain.print 등록 정보")
            doc.save(final, garbage=3, deflate=True)
            doc.close()
            os.remove(raw)
            d2 = pymupdf.open(final)
            t0 = d2[0].get_text()
            print(final, "pages", d2.page_count, "code on p1:", fmt_code(code) in t0,
                  "code on last:", fmt_code(code) in d2[-1].get_text(), "emb:", d2.embfile_count())
    print(codes)


if __name__ == "__main__":
    main()
