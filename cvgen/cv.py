# ashrain.out — 개념 카드 「▶ 움직이는 예시」(components/ConceptAv.jsx) 학기 파일 생성기 공용 (cv.py)
# 개념 본문의 예를 시청각 해설과 같은 꼴(문제 → 방침 → 판서 줄 + 빨간 메모 → 답, 그림 DSL)로 만든다.
# 문항 글자 · 판서 검산 · 그림 DSL 은 기본기 해설 생성기(../avgen — core.py · fig.py · kit.py)를 그대로 쓴다.
#   예제 = { id, cid, q, plan, planTag?, lines:[{pre?, s, memo?}], ans, fig? } — export.py 가 카드 칸(title = 방침 평문 · tab = 「예제 n」 · no = "")을 더한다
#   자리(place) = { cid, bid, after } — 개념 blocks 에서 그 단락(bid)의 lines[after] 바로 뒤에 [[av:<id>]] 글줄을 넣는다(../cvgen/sql.py).
import os, sys, re

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.environ.get("ASHRAIN_REPO") or os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(REPO, "avgen"))

import core as avc                       # noqa: E402  (avgen/core.py)
from core import N, NP, SG, MX, DEC, L, J, RO, sup, mono, poly, lin, fixminus, chain_check, plain, MI   # noqa: E402,F401
from fig import Fig, fly, mv, Plane, NL, ang_pt, dir_deg, angle_mark, fbar, ffill, R1, FW, FH            # noqa: E402,F401

# 경우의 수와 확률(중2-2)은 다른 방에서 보완한다 — 이 생성기는 건드리지 않는다
SKIP = {"m2-2-12", "m2-2-13", "m2-2-14"}
CID = re.compile(r"^([mh][1-3]-[1-3])-(\d{2})$")
NO_ROOT = re.compile(r"^m[12]-")          # 중1 · 중2 개념은 √ 를 쓰지 않는다(중2 과정으로만)


def eun(w): return J(w, "은", "는")
def iga(w): return J(w, "이", "가")
def eul(w): return J(w, "을", "를")
def wa(w): return J(w, "과", "와")
def ro(w): return RO(w)


class Unit:
    """단원 하나의 예제 모음 — ex(...) 로 하나씩 더한다(더할 때 판서 「=」 줄을 sympy 로 검산)"""

    def __init__(self, unit):
        self.unit = unit
        self.items = {}
        self.places = {}
        self.checks = 0
        self.seq = {}

    def ex(self, cid, q, plan, lines, ans, fig=None, *, at, sub=None, ident=False, mixed=False, planTag=None, no="예제", key=None):
        """cid 개념 · q 문제 · plan 방침 · lines 판서 줄(L(...)) · ans 답 · fig 그림(Fig.out()) · at=(단락 id, 그 단락 lines 의 몇 번째 뒤)"""
        m = CID.match(cid)
        assert m and m.group(1) == self.unit, f"{self.unit}: 단원이 다른 개념 {cid}"
        assert cid not in SKIP, f"{cid}: 경우의 수와 확률(중2-2)은 이 생성기에서 다루지 않는다"
        k = self.seq.get(cid, 0) + 1
        self.seq[cid] = k
        iid = key or f"{cid}-{k}"
        assert iid not in self.items, f"{iid} 겹침"
        q, plan, ans = fixminus(q), fixminus(plan), fixminus(ans)
        lines = [{kk: fixminus(v) for kk, v in ln.items()} for ln in lines]
        it = {"id": iid, "cid": cid, "no": no, "q": q, "plan": plan, "lines": lines, "ans": ans}
        if planTag:
            it["planTag"] = planTag
        if fig:
            for el in fig.get("els", []):           # 옮기기 · 날아오기 값은 소수 한 자리(자료 크기)
                for k2 in ("mv", "fr"):
                    if k2 in el:
                        el[k2] = {kk: (R1(v) if isinstance(v, float) else v) for kk, v in el[k2].items()}
            it["fig"] = fig
        for ln in lines:
            c, bad = chain_check(ln["s"], mixed, sub, ident)
            assert not bad, f"{iid} 판서 계산 틀림: {ln['s']} → {bad}"
            self.checks += c
        c, bad = chain_check(plan, mixed, sub, ident)
        assert not bad, f"{iid} 방침 계산 틀림: {plan} → {bad}"
        self.checks += c
        txt = " ".join([q, plan, ans] + [ln["s"] + ln.get("pre", "") + ln.get("memo", "") for ln in lines])
        if NO_ROOT.match(cid):
            assert "√" not in txt and "√" not in str(fig), f"{iid}: 중1 · 중2 개념에 √"
        assert not re.search(r"(^|[^\w])-\d", txt), f"{iid}: 빼기 기호가 아닌 '-'"
        assert not re.search(r"undefined|NaN|None", txt), f"{iid}: 빈 값"
        bid, after = at
        assert re.fullmatch(r"b\d+", bid) and isinstance(after, int) and after >= -1, f"{iid}: 자리 {at}"
        self.items[iid] = it
        self.places[iid] = {"cid": cid, "bid": bid, "after": after}
        return it


# ── 자주 쓰는 그림 조각 ──────────────────────────────────────────────────────
def boxed(f, x, y, s, z=34, c="ink", at="q", dl=0, pad=12, fill=None, fo=0.18, b=700):
    """글자 + 둥근 칸(칸 폭은 글자 폭으로 어림)"""
    from figs import tw
    w = tw(s, z) + pad * 2
    f.rect(x - w / 2, y - z * 0.95, w, z * 1.35, c=c, sw=2.5, rx=10, f=fill, fo=fo if fill else None, at=at, dl=dl)
    f.text(x, y, s, z=z, c=c if c != "soft" else "ink", at=at, dl=dl, b=b)
    return w
