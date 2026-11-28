import json, re
import set_a, set_b, set_c, set_d
from common import josa
import figs
from fractions import Fraction as F
from common import fr

def clean(s, short=True):
    s = re.sub(r"\$([^$]+)\$", r"\1", s)
    return re.sub(r"남학생 (\d+)명·여학생 (\d+)명", r"남 \1 · 여 \2", s) if short else s

def steps(eq):
    parts = []
    for a in eq.split(" → "):
        for b in a.split(" / "):
            chunks, depth, cur0 = [], 0, ""      # 괄호 안의 「, 」에서는 나누지 않는다
            i = 0
            while i < len(b):
                ch = b[i]
                depth += ch == "("
                depth -= ch == ")"
                if depth == 0 and b.startswith(", ", i):
                    chunks.append(cur0); cur0 = ""; i += 2; continue
                cur0 += ch; i += 1
            chunks.append(cur0)
            cur = chunks[0]
            for c in chunks[1:]:
                if re.search(r"[가-힣]| = ", c):
                    parts.append(cur); cur = c
                else:
                    cur += ", " + c
            parts.append(cur)
    return parts

def ans(d):
    a = d["ans"]
    if isinstance(a, F):
        return fr(a)
    return str(a) + d.get("unit", "")

def items(S, figf=None):
    out = []
    for i, d in enumerate(S.build(), 1):
        assert d["ans"] == d["chk"]
        ln = [{"pre": "포지티브", "s": clean(d["pos"])}, {"pre": "네거티브", "s": clean(d["neg"])}]
        st = [clean(s) for s in (d["eq"] if isinstance(d["eq"], list) else steps(d["eq"]))]
        if len(st) > 1 and st[-1].strip() == ans(d):
            if isinstance(d["ans"], F) and d["ans"].denominator != 1:
                st[-1] = "확률 = " + st[-1]
            else:
                st = st[:-1]
        ln += [{"s": s} for s in st]
        it = {"no": i, "st": d["lv"], "q": clean(d["q"], False), "ans": ans(d), "plan": clean(d["plan"]), "lines": ln}
        if figf:
            f = figf(d, ln)
            if f:
                it["fig"] = f
        out.append(it)
    return out

# ── 사전식: 칠판 방식(숫자 분석 → 묶음 개수로 시작 글자 → 최종 묶음) · 오른쪽에 세로 나무 ──
lj = set_c.lj
ga = lambda n: josa(str(n), "이", "가")
ro = lambda c: c + ("으로" if c[-1] in "MN" else "로")      # 엠으로 · 엔으로 · 엘로 · 알로


def lex_lines(d):
    t = d.get("tree")
    cards = d["cards"]
    n = len(cards)
    k = len(t["word"]) if t else None
    lines = [{"pre": "포지티브", "s": "카드 " + ", ".join(cards)},
             {"pre": "네거티브", "s": (f"{k}장 모두" if k == n else f"{n}장 중 {k}장") + " · 한 번씩 · 알파벳 순"}]
    lines += [{"s": b} for b in d.get("blocks", [])]          # 덩어리 크기를 공식대로(작은 덩어리부터)
    if "num" in d:
        lines.append({"pre": "숫자 분석", "s": d["num"]})
    at = []          # 단(세로 줄)마다 (나타나는 줄, 고르는 줄)
    rem = sorted(cards)
    pre = ""
    kth = "num" in d
    ncol = len(t["cols"])
    tail_at = None
    for li, c in enumerate(t["cols"]):
        sk = [L for (L, b, h) in c["items"] if not h]
        ch = [L for (L, b, h) in c["items"] if h][0]
        blk = c["items"][-1][1]
        final = li == ncol - 1
        rest = [x for x in rem if x != ch]
        show = len(lines)
        if kth:
            if final and blk == 1:   # 마지막 자리 — 한 줄로
                lines.append({"s": (f"1 × {len(sk)} → " + ", ".join(pre + L for L in sk) + " 지나고 → 마지막 1") if sk else "마지막 1"})
            elif sk:
                lines.append({"s": f"{blk} × {len(sk)} → " + ", ".join(pre + L for L in sk) + " 묶음 다 씀"})
            if not final:
                lead = f"{ro(ch)} 시작" if not pre else f"{pre} 다음은 {ch}"
                if sk:
                    lines.append({"s": lead, "memo": f"{ch} 소모"})
                else:          # 다 쓴 묶음이 없으면 한 줄로
                    show = len(lines)
                    lines.append({"s": f"{blk} 묶음 0개 → 맨 앞 → {lead}", "memo": f"{ch} 소모"})
            else:
                many = len(rest) > len(t["tail"])
                if t["mode"] == "last" and blk > 1:
                    lines.append({"s": f"마지막 {blk} = 최종 묶음 {pre + ch}", "memo": f"{ch} 소모"})
                    tail_at = len(lines)
                    lines.append({"s": f"남은 {', '.join(rest)} → " + (f"큰 것부터 {len(t['tail'])}장 " if many else "큰 것부터 ") + t["tail"], "memo": "묶음의 맨 끝"})
                elif t["mode"] == "first":
                    lines.append({"s": f"남은 1 → 묶음 {pre + ch}의 맨 처음", "memo": f"{ch} 소모"})
                    tail_at = len(lines)
                    lines.append({"s": f"남은 {', '.join(rest)} → " + (f"작은 것부터 {len(t['tail'])}장 " if many else "작은 것부터 ") + t["tail"]})
                else:
                    pass
        else:
            lead = f"{ro(ch)} 시작" if not pre else f"{pre} 다음은 {ch}"
            if sk:
                lines.append({"s": f"{lead} → 앞에 " + ", ".join(pre + L for L in sk) + " 묶음", "memo": f"{blk} × {len(sk)}"})
            else:
                lines.append({"s": f"{lead} → 앞선 묶음 없음"})
            if final and t["tail"]:
                tail_at = len(lines)
                if t["mode"] == "last" and blk > 1:
                    lines.append({"s": f"남은 {t['tail']} → 큰 것부터 → 맨 끝", "memo": f"{blk} 통째로"})
                elif t["mode"] == "first":
                    lines.append({"s": f"남은 {t['tail']} → 작은 것부터 → 맨 처음", "memo": "+ 1"})
        pick = len(lines) - 1 if kth and not final else (tail_at - 1 if tail_at else len(lines) - 1)
        if not kth:
            pick = show
        at.append([show, max(show, pick)])
        rem.remove(ch)
        pre += ch
    if kth:
        lines.append({"s": f"→ {t['word']}"})
    else:
        lines.append({"pre": "숫자 정리", "s": " + ".join(map(str, t["terms"])) + f" = {t['kk']}"})
        for x in d.get("extra", []):
            lines.append({"s": x})
    fig = {"kind": "tree", "cards": cards, "cols": [{"start": c["start"], "items": [[L, b, h] for (L, b, h) in c["items"]]} for c in t["cols"]],
           "tail": t["tail"], "tailAt": tail_at if tail_at is not None else len(lines) - 1, "at": at, "sizes": t["sizes"]}
    return lines, fig


def lex_items():
    out = []
    for i, d in enumerate(set_c.build(), 1):
        assert d["ans"] == d["chk"]
        if "trees" in d:          # 두 단어 사이 — 그림 없이 숫자만
            t1, t2 = d["trees"]
            lines = [{"pre": "포지티브", "s": "카드 " + ", ".join(d["cards"]) + " · 두 단어는 같은 글자"},
                     {"pre": "네거티브", "s": "'사이' = 두 단어는 빼고"}]
            lines += [{"s": b} for b in d.get("blocks", [])]
            for t in (t1, t2):
                lines.append({"pre": t["word"], "s": " + ".join(map(str, t["terms"])) + f" = {t['kk']}"})
            hi, lo = max(t1["kk"], t2["kk"]), min(t1["kk"], t2["kk"])
            lines.append({"s": f"사이(큰 순번 − 작은 순번 − 1): {hi} − {lo} − 1 = {hi - lo - 1}"})
            out.append({"no": i, "st": d["lv"], "q": d["q"], "ans": ans(d), "plan": "덩어리 크기를 구하고, 두 단어의 순번을 각각 숫자로 정리한 뒤 (큰 순번) − (작은 순번) − 1", "lines": lines})
            continue
        lines, fig = lex_lines(d)
        it = {"no": i, "st": d["lv"], "q": d["q"], "ans": d.get("ans_show") or ans(d), "lines": lines, "fig": fig}
        if "num" in d:
            it["plan"] = "덩어리 크기 → 숫자 분석(번호를 큰 덩어리부터 쪼개기) → 세로로 글자 내려 적기"
        else:
            it["plan"] = "덩어리 크기 → 단어를 따라 앞선 묶음을 센다 → 숫자 정리"
        out.append(it)
    return out


A = items(set_a, lambda d, ln: figs.grades_fig(d["q"], ln))
B = items(set_b, lambda d, ln: figs.bag_fig(d["q"], ln))
C_ = lex_items()
D_ = items(set_d, lambda d, ln: figs.seats_fig(d["tpl"], d["prm"], ln))
def js(a):
    return "[\n" + ",\n".join("  " + json.dumps(x, ensure_ascii=False, separators=(", ", ": ")) for x in a) + ",\n]"
src = f'''// ashrain.out — 교실 모니터 「경우의 수와 확률 100제 해설」 문항 (cnt100-items.js)
// 학원 프린트 네 세트(중2-2, 1~5단계)와 같은 문항 · 같은 번호 · 같은 답:
//   「학년별 선발로 익히는 경우의 수와 확률 100제」 · 「주머니 속 공으로 익히는 경우의 수와 확률 100제」 ·
//   「영어 단어로 익히는 사전식 나열 100제」 · 「한 줄로 세우기 100제 — 이웃 · 양 끝」
// 한 문항: no 번호(1~100) · st 단계(1~5) · q 발문 · ans 답 · plan 방침 한 줄 ·
//   lines 판서 줄 [{{ pre? 머리말, s 식, memo? 빨간 메모 }}] · fig?(사전식) 세로 나무:
//   {{ kind: "tree", cards 카드, cols [{{ start 시작 줄, items [[글자, 덩어리, 고름]] }}], tail 남은 글자, tailAt · at[[나타나는 판서 줄, 고르는 판서 줄]], sizes 덩어리 크기 }}
// 판서 식은 공식을 다 펼치고(4 × 3 ÷ 2 · 5 × 4 × 3 ÷ (3 × 2 × 1) · 3 × 2 × 1) 줄마다 무엇을 센 식인지 이름표를 붙인다
//   (「빨간 공 4개 중 2개: 4 × 3 ÷ 2 = 6」 → 「같은 색(합의 법칙): 6 + 3 = 9」). 앞 줄에서 구하지 않은 수는 쓰지 않는다.
// 사전식 해설은 강사 판서 방식 — 덩어리 크기를 공식대로 먼저 구하고(「덩어리(남은 4장 한 줄로): 4 × 3 × 2 × 1 = 24」),
//   「숫자 분석」 줄에서 번호를 덩어리 합으로 쪼갠 뒤(70 = 24 + 24 + 6 + 6 + 6 + 2 + 2),
//   「24 × 2 → A, B 묶음 다 씀 → C로 시작(C 소모)」처럼 내려가 최종 묶음에서 남은 글자로 끝낸다.
// 정답은 학생 · 공 · 문자열 · 줄을 하나하나 늘어놓고 직접 세어 확인해 만들었고(생성기 cnt100gen/ — 문항마다 직접 센 chk와 맞춰 봄),
// 저장소 안에서는 tests/display-cnt100.test.mjs 가 판서의 「=」 계산 · 답 · 나무를 다시 본다.
export const CNT100_SEL = {js(A)};

export const CNT100_BALL = {js(B)};

export const CNT100_LEX = {js(C_)};

export const CNT100_LINE = {js(D_)};
'''
import sys
open(sys.argv[1] if len(sys.argv) > 1 else "/tmp/cnt100-items.gen.js", "w").write(src)
print(len(src))
for it in (C_[0], C_[30], C_[80], C_[90], D_[60]):
    print(it['q'][-40:], '|', it['ans'], '|', it['plan']); [print('   ', l.get('pre',''), l['s'], '//', l.get('memo','')) for l in it['lines']]; print('   fig', it.get('fig', {}).get('at'), it.get('fig', {}).get('tailAt'))
