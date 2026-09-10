# itemfactory/tools/hwp5text.py — HWP 5.0(.hwp) 최소 텍스트·수식 추출기 (v1.0)
#
#   python itemfactory/tools/hwp5text.py 파일.hwp [파일2.hwp …]   → 표준 출력에 텍스트 (수식은 ⟦eq: …⟧ 로 스크립트 그대로)
#
# 외부 라이브러리 없이(olefile만) HWP 5.0 본문 레코드를 읽는다. 목적은 출판사 평가자료·답지의 문항·해설·배점 확인이라
# 서식은 버리고 문단 텍스트, 표 셀 텍스트, 수식 스크립트만 문서 순서대로 뽑는다.
#   · FileHeader 의 압축 플래그를 보고 BodyText/Section* 을 zlib(raw) 로 푼다
#   · 레코드 헤더 4바이트: tag(10) | level(10) | size(12), size==0xFFF 이면 뒤 4바이트가 실제 크기
#   · PARA_TEXT(67) 의 UTF-16LE 에서 제어문자(1~31)를 규칙대로 건너뛴다 (확장·인라인 제어는 8 WCHAR)
#   · EQEDIT(88) 의 수식 스크립트를 문단 뒤에 ⟦eq: …⟧ 로 붙인다
#   · 배포용(암호화) 문서는 지원하지 않는다
from __future__ import annotations

import struct
import sys
import zlib

import olefile

TAG_PARA_HEADER, TAG_PARA_TEXT, TAG_CTRL_HEADER, TAG_TABLE, TAG_EQEDIT = 66, 67, 71, 77, 88
_SINGLE = {0, 10, 13, 24, 25, 26, 27, 28, 29, 30, 31}          # 1 WCHAR 제어
_INLINE = {4, 5, 6, 7, 8, 9, 19, 20}                          # 8 WCHAR (자리 표시)
# 나머지 1~23 은 확장 제어(8 WCHAR) — 표·그림(11) 등은 뒤따르는 레코드에 내용이 있다


def records(buf: bytes):
    i, n = 0, len(buf)
    while i + 4 <= n:
        h = struct.unpack_from("<I", buf, i)[0]
        tag, level, size = h & 0x3FF, (h >> 10) & 0x3FF, (h >> 20) & 0xFFF
        i += 4
        if size == 0xFFF:
            size = struct.unpack_from("<I", buf, i)[0]
            i += 4
        yield tag, level, buf[i:i + size]
        i += size


def para_text(data: bytes) -> str:
    out, cu = [], []
    n = len(data) // 2
    j = 0
    while j < n:
        c = struct.unpack_from("<H", data, j * 2)[0]
        if c >= 32:
            out.append(chr(c) if not (0xD800 <= c <= 0xDFFF) else "")
            j += 1
        elif c in _SINGLE:
            if c in (10, 13):
                out.append("\n")
            j += 1
        elif c in _INLINE:
            if c == 9:
                out.append("\t")
            j += 8
        else:                                   # 확장 제어 — 표/그림/수식 자리
            if c == 11:
                out.append("⟨obj⟩")
            j += 8
    return "".join(out)


def eq_script(data: bytes) -> str:
    """EQEDIT: property(4) + WORD len + UTF-16LE script + …"""
    try:
        ln = struct.unpack_from("<H", data, 4)[0]
        return data[6:6 + ln * 2].decode("utf-16le", "replace")
    except Exception:                          # noqa: BLE001
        return ""


def extract(path: str) -> str:
    ole = olefile.OleFileIO(path)
    hdr = ole.openstream("FileHeader").read()
    flags = struct.unpack_from("<I", hdr, 36)[0]
    compressed, encrypted = bool(flags & 1), bool(flags & 2)
    if encrypted:
        return "⟪암호화/배포용 문서 — 지원하지 않음⟫"
    secs = sorted([e for e in ole.listdir() if e[0] == "BodyText"], key=lambda e: int(e[1].replace("Section", "")))
    out_lines = []
    for e in secs:
        raw = ole.openstream("/".join(e)).read()
        buf = zlib.decompress(raw, -15) if compressed else raw
        # 문단 = {"level", "text", "objs": [ctrl id …], "eqs": {ctrl index: script}}
        paras = []              # 문서 순서
        open_by_level = {}      # level → 그 문단 (자기 자식 컨트롤을 받는다)
        last_eq_target = None
        for tag, level, data in records(buf):
            if tag == TAG_PARA_HEADER:
                pp = {"level": level, "text": "", "objs": []}
                paras.append(pp)
                open_by_level[level] = pp
                for k in [k for k in open_by_level if k > level]:
                    del open_by_level[k]
            elif tag == TAG_PARA_TEXT:
                pp = open_by_level.get(level - 1)          # 본문 텍스트는 문단 헤더보다 한 단계 안
                if pp is not None:
                    pp["text"] += para_text(data)
            elif tag == TAG_CTRL_HEADER:
                cid = data[:4][::-1].decode("latin1", "replace") if len(data) >= 4 else "????"
                parent = open_by_level.get(level - 1)
                if parent is not None:
                    parent["objs"].append({"id": cid, "eq": None})
                    last_eq_target = parent["objs"][-1] if cid == "eqed" else None
            elif tag == TAG_EQEDIT and last_eq_target is not None:
                last_eq_target["eq"] = eq_script(data).strip()
                last_eq_target = None
        for pp in paras:
            t = pp["text"]
            for ob in pp["objs"]:
                if ob["id"] == "eqed":
                    rep = f"⟦{ob['eq'] or ''}⟧"
                elif ob["id"] == "tbl ":
                    rep = "[표]"
                elif ob["id"] in ("gso ", "$pic"):
                    rep = "[그림]"
                elif ob["id"] in ("secd", "cold", "head", "foot", "fn  ", "en  ", "atno", "nwno", "pgct", "pghd", "pgnp", "bokm", "tdut", "tcmt", "form"):
                    rep = ""
                else:
                    rep = f"[{ob['id'].strip()}]"
                t = t.replace("⟨obj⟩", rep, 1)
            t = t.replace("⟨obj⟩", "")
            if t.strip():
                out_lines.append(("  " * max(0, pp["level"] - 1)) + t.strip())
    return "\n".join(out_lines)


if __name__ == "__main__":
    for p in sys.argv[1:]:
        if len(sys.argv) > 2:
            print(f"\n===== {p}")
        print(extract(p))
