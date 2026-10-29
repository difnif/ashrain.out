#!/usr/bin/env python3
"""서술형 평가 생성기 v1 (2026-10-14) — 채팅방 산출물: PDF(확인·인쇄용) + JSON(앱 등록용)

  (처음 한 번) cd assessgen && npm install          # 시험지 글꼴(@fontsource) — 앱 package.json 과 따로
  python3 assessgen/build_assess.py assessgen/specs/<회차>.py [--out assessgen/out] [--png]
  준비물: python3(segno·pymupdf·playwright), node, Chromium(playwright). 저장소의 src/lib/mathir.js·assess/*.js·omr/detect.js 를 그대로 쓴다.

쪽 구성: 1쪽 학생 확인 사항(안내) · 2쪽 강사 확인 사항(QR·학년·이름·필적 문장·닉네임) · 3쪽~ 한 쪽에 한 문제(①②③ 칸)
모든 쪽: 찰칵 채점(OMR) 카드와 같은 좌표계(1000×1414 단위, 1단위=0.19mm)·네 귀퉁이 마커·방향 막대 + 아래 가운데 쪽 번호 띠.
앱(src/lib/assess/sheet.js)이 같은 값으로 사진을 펴고 몇 쪽인지 읽는다 — 값을 바꾸면 양쪽을 함께.

검산(빌드 때 매번): 회차 스펙의 verify() · 필적 문장 자모/숫자 · MathIR 문법 · 앱 validateSpec(node) ·
PDF 각 쪽을 래스터로 떠서 앱의 마커 검출기(detect.js)로 펴고 쪽 번호 띠를 읽어 쪽 번호·확인값이 맞는지.
"""
import argparse, datetime, html, importlib.util, json, pathlib, subprocess, sys
import segno

ROOT = pathlib.Path(__file__).resolve().parent           # assessgen/
REPO = ROOT.parent                                        # 저장소 — 앱의 렌더러·검사기·검출기를 그대로 쓴다
FONTS = ROOT / "node_modules" / "@fontsource"
SITE = "https://ashrainout.com"

# ── 좌표계 (src/lib/assess/sheet.js 와 같은 값) ────────────────────────────────
U = 0.19
W_U, H_U = 1000, 1414
CARD_W, CARD_H = W_U * U, H_U * U            # 190 × 268.66 mm
MK, INSET = 60, 50
ORIENT = dict(x=122, y=50, w=24, h=60)
PAGECODE = dict(n=14, x0=308, y0=1324, size=20, pitch=28)   # 해밍(13,9)+전체 패리티 — sheet.js 와 같은 값
BODY_TOP_MM, BODY_BOT_MM = 27.0, 23.6        # 본문 영역: 위 27mm ~ 아래 23.6mm(=1289.8단위) — 마커 띠를 피한다

LEVELS = {"elem": "초등", "mid": "중등", "high": "고등"}


def check_of(code):
    """sheet.js checkOf 와 같은 계산 (FNV-1a 32 → 5비트 접기)"""
    h = 2166136261
    for ch in str(code):
        h ^= ord(ch)
        h = (h * 16777619) & 0xFFFFFFFF
    return ((h >> 27) ^ (h >> 22) ^ (h >> 17) ^ (h >> 12) ^ (h >> 7) ^ (h >> 2) ^ h) & 31


DATA_POS = [3, 5, 6, 7, 9, 10, 11, 12, 13]   # 해밍 위치 1~13 중 데이터 자리(쪽 4비트 → 확인 5비트, 낮은 자리부터)
PAR_POS = [1, 2, 4, 8]


def encode_page(page, check):
    """sheet.js encodePage 와 같은 계산 — 14칸(칸 0 = 해밍 위치 1, 칸 13 = 전체 패리티)"""
    assert 1 <= page <= 15 and 0 <= check <= 31
    d = [(page >> i) & 1 for i in range(4)] + [(check >> i) & 1 for i in range(5)]
    c = [0] * 15
    for pos, b in zip(DATA_POS, d):
        c[pos] = b
    for p in PAR_POS:
        x = 0
        for j in range(1, 14):
            if j != p and (j & p):
                x ^= c[j]
        c[p] = x
    a = 0
    for j in range(1, 14):
        a ^= c[j]
    c[14] = a
    return c[1:]


def decode_page(bits):
    """검산용 — sheet.js decodeBits 와 같은 판정 (고치지 않음)"""
    c = [0] + [1 if b else 0 for b in bits]
    syn = 0
    for p in PAR_POS:
        x = 0
        for j in range(1, 14):
            if j & p:
                x ^= c[j]
        if x:
            syn |= p
    a = 0
    for j in range(1, 15):
        a ^= c[j]
    page = sum(c[pos] << i for i, pos in enumerate(DATA_POS[:4]))
    check = sum(c[pos] << i for i, pos in enumerate(DATA_POS[4:]))
    return page, check, syn == 0 and a == 0 and page >= 1


def _selftest_code():
    """모든 (쪽, 확인값)에 대해: 그대로면 통과, 1~3칸 뒤집으면 모두 걸러진다"""
    import itertools
    valid = {}
    for pg in range(1, 16):
        for ck in range(32):
            bits = encode_page(pg, ck)
            assert len(bits) == PAGECODE["n"]
            assert decode_page(bits) == (pg, ck, True)
            valid[tuple(bits)] = (pg, ck)
    for bits, _ in valid.items():
        for k in (1, 2, 3):
            for idx in itertools.combinations(range(14), k):
                b = list(bits)
                for i in idx:
                    b[i] ^= 1
                assert not decode_page(b)[2], (bits, idx)
    return len(valid)


def _crosscheck_code():
    """앱(sheet.js)과 같은 칸을 그리는지 — 480가지 전부 node 로 대조"""
    want = {f"{pg},{ck}": encode_page(pg, ck) for pg in range(1, 16) for ck in range(32)}
    r = subprocess.run(["node", "-e", f"""
      import('{(REPO / "src/lib/assess/sheet.js").as_uri()}').then(m => {{
        const o = {{}};
        for (let p = 1; p <= 15; p++) for (let c = 0; c < 32; c++) o[p + ',' + c] = m.encodePage(p, c);
        console.log(JSON.stringify({{ o, pc: m.PAGECODE, checks: ['SAMPLE01','SAMPLE02','M1014A','E1015B','ABCD','ZZZZZZZZZZZZ'].map(m.checkOf) }}));
      }});"""], capture_output=True, text=True)
    got = json.loads(r.stdout)
    assert got["o"] == want, "sheet.js encodePage 와 다름"
    assert got["pc"] == PAGECODE, (got["pc"], PAGECODE)
    assert got["checks"] == [check_of(c) for c in ("SAMPLE01", "SAMPLE02", "M1014A", "E1015B", "ABCD", "ZZZZZZZZZZZZ")]
    return True


# ── 필적 확인 문장 (매일 같은 문장 · 같은 줄바꿈) ─────────────────────────────
PHRASE = [
    ("여름에 코끼리와 해마가 빨간 딸기 팥빙수를", None),
    ("짝꿍처럼 사이좋게 나눠 먹었다.", None),
    ("(41 + 59) × 30 − 78 ÷ 6 = 2987", None),
]
PHRASE_MID = ("y = −2x + 5,  a² ≥ 3b,  x = 3/4 = 0.75,  △ABC ∽ △DEF,  ∠A = 90°",
              'y = −2x + 5,&ensp; a² ≥ 3b,&ensp; x = <span class="fr"><i>3</i><i>4</i></span> = 0.75,&ensp; △ABC ∽ △DEF,&ensp; ∠A = 90°')


def phrase_lines(level):
    rows = list(PHRASE)
    if level in ("mid", "high"):
        rows.append(PHRASE_MID)
    return rows


# ── 1쪽 풀이 작성 예시 ────────────────────────────────────────────────────────
EXAMPLES = {
    "elem": {
        "problem": "색종이가 52장 있었습니다. 미술 시간에 18장을 쓰고, 선생님께 25장을 더 받았습니다. 지금 색종이는 몇 장인가요?",
        "s1": ["(지금 색종이) = (처음) − (쓴 것) + (받은 것)", "52 − 18 + 25"],
        "s2": [["52 − 18 = ", ("x", "44"), " 34"], ["34 + 25 = 59"]],
        "s2_right": None,
        "s3": "59장",
        "notes": {
            "q": "문제를 읽고 아래처럼 세 칸에 나누어 써요.",
            "s1": "문장을 식으로 바꿔요. 말로 된 식부터 써도 좋아요.",
            "s2": "한 줄에 한 단계씩. 틀린 곳은 <b>줄 하나 긋고</b> 옆에 다시 — 지우개는 쓰지 않아요.",
            "s3": "답은 <b>단위까지</b> 써요.",
        },
    },
    "mid": {
        "problem": "사탕은 한 개에 300원, 초콜릿은 한 개에 500원입니다. 사탕과 초콜릿을 합하여 12개를 사고 4400원을 냈을 때, 초콜릿은 몇 개를 샀는지 구하시오.",
        "s1": ["초콜릿을 x개 샀다고 하면 사탕은 (12 − x)개", "300(12 − x) + 500x = 4400"],
        "s2": [["3600 − 300x + 500x = 4400"], [("x", "200x = 4400 + 3600")], ["200x = 4400 − 3600"], ["200x = 800,  x = 4"]],
        "s2_right": [["(확인) 300 × 8"], ["+ 500 × 4"], ["= 2400 + 2000"], ["= 4400"]],
        "s3": "4개",
        "notes": {
            "q": "문제를 읽고 아래처럼 세 칸에 나누어 써요.",
            "s1": "<b>무엇을 x로 놓았는지</b> 먼저 쓰고 식을 세워요.",
            "s2": "한 줄에 한 단계씩. 틀린 곳은 <b>줄 하나 긋고</b> 아래에 다시 — 지우개는 쓰지 않아요. 칸 안에서 자리를 옮기면 <b>→</b>로 이어요.",
            "s3": "답은 <b>단위까지</b> 써요.",
        },
    },
}
EXAMPLES["high"] = EXAMPLES["mid"]


def rules(total_pages):
    return [
        ("시작과 끝", [
            ("2쪽부터 채워요.", "학년·이름은 꼭, 필적 확인 문장은 평소 글씨로 따라 써요. 닉네임은 쓰고 싶을 때만."),
            ("다 풀면 찍어서 채점받아요.", "앱 알림이나 2쪽 QR로 들어가, 안내에 따라 1쪽부터 한 장씩 찍어요."),
        ]),
        ("쓰는 법", [
            ("글씨는 평소 그대로.", "시험이라고 일부러 꾸미거나 바꿔 쓰지 않아요."),
            ("칸마다 할 일이 있어요.", "① 식 세우기 → ② 식 풀기 → ③ 구하는 것 순서로 써요."),
            ("한 줄에 한 단계씩,", "위에서 아래로 써요."),
            ("모르는 문제도 아는 데까지.", "비워 두지 말아요. 식만 맞게 세워도 ①의 점수를 받아요."),
        ]),
        ("고치는 법", [
            ("지우지 않아요.", "틀린 곳은 줄을 하나 긋고 옆이나 아래에 다시 써요. 그은 곳은 채점하지 않으니 감점도 없어요. 덮어 칠하지 않아요."),
            ("연습 계산도 남겨요.", "따로 하는 계산(세로셈 등)도 ② 칸 빈 곳에 하고 지우지 않아요."),
            ("자리를 옮기면 → 표시.", "② 칸 안에서 다른 자리로 옮겨 이어 쓰면 →로 이어지는 곳을 표시해요."),
        ]),
        ("지킬 것", [
            ("진한 연필이나 검은 펜.", "사진으로 찍어 채점해서 흐린 글씨는 읽히지 않아요."),
            ("가리지 않는 곳:", "네 귀퉁이 ■와 아래 가운데 작은 네모 줄 — 사진이 몇 쪽인지 이것으로 알아봐요. 칸 밖·뒷면에도 쓰지 않아요."),
            ("오픈북의 범위:", "교과서·개념서·노트는 봐도 돼요. 휴대폰·계산기는 쓰지 않고, 친구와 상의하지 않아요."),
        ]),
    ]


# ── 공용 CSS ──────────────────────────────────────────────────────────────────
CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #fff; }
body { font-family: 'Noto Sans KR', 'Noto Sans CJK KR', sans-serif; color: #111; font-size: 9pt;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; word-break: keep-all; }
.page { position: relative; width: 210mm; height: 297mm; overflow: hidden; break-after: page; page-break-after: always; }
.page:last-child { break-after: auto; page-break-after: auto; }
.card { position: absolute; left: 10mm; top: 10mm; width: 190mm; height: 268.66mm; }
.mk { position: absolute; background: #000; }
.pc { position: absolute; background: #000; }
.pc.z { background: #fff; outline: .18mm solid #b5b5b5; outline-offset: -.18mm; }
.foot { position: absolute; left: 10mm; right: 10mm; top: 284mm; display: flex; justify-content: space-between;
        font-size: 7.5pt; color: #555; letter-spacing: .02em; }
.hw { font-family: 'Gaegu', 'Noto Sans KR', sans-serif; font-weight: 700; color: #1a1a1a; }
.kick { font-size: 8pt; letter-spacing: .12em; color: #444; font-weight: 500; }
b { font-weight: 700; }
.fr { display: inline-flex; flex-direction: column; vertical-align: middle; text-align: center; line-height: 1.05;
      font-size: .82em; margin: 0 .1em; }
.fr i { font-style: normal; padding: 0 .15em; }
.fr i:first-child { border-bottom: .25mm solid currentColor; }
.tband { position: absolute; left: 32mm; right: 32mm; top: 6.2mm; text-align: center; }
.tband h1 { margin: .6mm 0 0; font-size: 21pt; font-weight: 900; line-height: 1.1; }
.body { position: absolute; left: 0; right: 0; top: 27mm; bottom: 23.6mm; }

/* ── 1쪽 ── */
.p1 .body { display: flex; flex-direction: column; justify-content: space-between; }
.p1 .blk { display: block; }
.p1 .tag { position: absolute; right: 32mm; top: 15.4mm; font-size: 8pt; border: .3mm solid #111; border-radius: 1.4mm; padding: .6mm 2mm; }
.ov { display: grid; grid-template-columns: 1fr 1fr 1.45fr; gap: 2.5mm; }
.ov div { border: .3mm solid #999; border-radius: 1.8mm; padding: 1.5mm 3mm; }
.ov b { display: block; font-size: 11.5pt; font-weight: 900; margin-bottom: .5mm; }
.ov span { display: block; font-size: 8.9pt; line-height: 1.5; color: #333; }
.p1 h2 { display: flex; align-items: center; gap: 2.5mm; margin: 0 0 2.2mm; font-size: 11.5pt; font-weight: 900; }
.p1 h2::after { content: ""; flex: 1; border-top: .3mm solid #111; }
.ex { display: grid; grid-template-columns: minmax(0, 1fr) 54mm; column-gap: 5mm; row-gap: 1.5mm; align-items: stretch; }
.exq { border: .35mm solid #111; border-radius: 1.6mm; padding: 1.7mm 3mm; display: flex; gap: 2.5mm; align-items: flex-start; }
.exq .no { flex: none; background: #111; color: #fff; font-weight: 700; font-size: 8pt; border-radius: 1mm; padding: .4mm 1.8mm; margin-top: .3mm; }
.exq p { margin: 0; font-size: 9.8pt; line-height: 1.55; }
.bx { border: .35mm solid #111; border-radius: 1.6mm; padding: 1.2mm 3.2mm 1.8mm; }
.lb { display: flex; justify-content: space-between; align-items: baseline; font-size: 8pt; font-weight: 700;
      border-bottom: .2mm dashed #888; padding-bottom: .6mm; margin-bottom: 1mm; }
.lb i { font-style: normal; font-weight: 500; color: #555; }
.w { font-size: 15pt; line-height: 1.28; }
.lv-mid .w, .lv-high .w { font-size: 13.4pt; line-height: 1.25; }
.w .ln { white-space: nowrap; }
.x { position: relative; display: inline-block; }
.x::after { content: ""; position: absolute; left: -1.2mm; right: -1.2mm; top: 52%; border-top: .5mm solid #111; transform: rotate(-5deg); }
.cols { display: grid; grid-template-columns: auto 13mm 1fr; align-items: stretch; }
.cols .arw { position: relative; width: 13mm; }
.cols .arw svg { position: absolute; inset: 0; width: 100%; height: 100%; }
.cols .right { align-self: start; }
.op { font-family: 'Noto Sans KR', sans-serif; font-weight: 500; font-size: .78em; padding: 0 .08em; }
.nt { position: relative; align-self: center; background: #ececec; border-radius: 1.6mm; padding: 2.2mm 3mm; font-size: 9pt; line-height: 1.55; }
.nt::before { content: ""; position: absolute; left: -2.3mm; top: 50%; margin-top: -2.2mm;
              border-top: 2.2mm solid transparent; border-bottom: 2.2mm solid transparent; border-right: 2.4mm solid #ececec; }
.nt .k { display: inline-block; font-weight: 900; margin-right: 1mm; }
.nt.q { background: none; border: .3mm dashed #888; color: #333; }
.nt.q::before { display: none; }
.rules { display: grid; grid-template-columns: 1fr 1fr; column-gap: 6mm; }
.grp { margin-bottom: 2.3mm; break-inside: avoid; }
.grp h3 { display: inline-block; margin: 0 0 1.3mm; font-size: 8pt; font-weight: 700; color: #fff; background: #111;
          border-radius: 1mm; padding: .4mm 2mm; letter-spacing: .06em; }
.r { display: grid; grid-template-columns: 5.8mm 1fr; margin-bottom: 1.5mm; font-size: 9.2pt; line-height: 1.52; }
.r .n { width: 4.4mm; height: 4.4mm; border-radius: 50%; border: .3mm solid #111; font-size: 6.8pt; font-weight: 700;
        display: flex; align-items: center; justify-content: center; margin-top: .45mm; }
.r p { margin: 0; color: #222; }
.r p b { color: #000; }

/* ── 2쪽 ── */
.p2 .sub { position: absolute; left: 9.5mm; right: 9.5mm; top: 26mm; display: flex; justify-content: space-between;
           align-items: baseline; font-size: 8.6pt; color: #333; border-bottom: .5mm solid #111; padding-bottom: 1.8mm; }
.p2 .sub .date { font-size: 9.5pt; color: #111; letter-spacing: .02em; }
.p2 .flow { position: absolute; left: 9.5mm; right: 9.5mm; top: 36mm; bottom: 26mm; display: flex; flex-direction: column;
            justify-content: space-between; gap: 3.5mm; }
.qrb { display: flex; justify-content: center; align-items: center; gap: 7mm; }
.qr { width: 40mm; height: 40mm; flex: none; }
.qr svg { width: 100%; height: 100%; display: block; }
.qrc { width: 78mm; }
.qrc b { display: block; font-size: 13pt; font-weight: 900; margin-bottom: 1.2mm; }
.qrc span { display: block; font-size: 8.8pt; line-height: 1.5; color: #333; }
.qrc code { display: block; margin-top: 2.2mm; font-family: 'Noto Sans KR', monospace; font-size: 8pt; color: #333;
            border-top: .25mm solid #bbb; padding-top: 1.5mm; letter-spacing: .01em; }
.qrc code em { font-style: normal; font-weight: 900; color: #111; letter-spacing: .08em; }
.fld { border: .35mm solid #111; border-radius: 1.6mm; display: flex; align-items: stretch; min-height: 15mm; }
.fld label { flex: none; display: flex; align-items: center; padding: 0 3.2mm; font-size: 10pt; font-weight: 900;
             border-right: .3mm solid #111; background: #efefef; border-radius: 1.4mm 0 0 1.4mm; }
.fld label em { font-style: normal; font-weight: 500; font-size: 8pt; color: #444; margin-left: 1mm; }
.fld .val { flex: 1; display: flex; align-items: center; padding: 0 3.5mm; font-size: 10.5pt; gap: 2mm; }
.fld .bl { display: inline-block; width: 12mm; height: 9mm; border-bottom: .3mm solid #555; }
.fld .hint { align-self: center; padding: 0 3.5mm; font-size: 7.8pt; color: #555; }
.row2 { display: grid; grid-template-columns: 54mm 1fr; gap: 4mm; }
.ph { border: .35mm solid #111; border-radius: 1.6mm; padding: 2.4mm 3.2mm 3mm; }
.phh { display: flex; align-items: baseline; gap: 3mm; margin-bottom: 2mm; }
.phh b { font-size: 10.5pt; font-weight: 900; }
.phh span { font-size: 8.4pt; color: #333; }
.pl { margin-top: 1.8mm; }
.pl .model { display: flex; align-items: center; gap: 2.4mm; background: #efefef; border-radius: 1mm; padding: .9mm 2.4mm;
             font-size: 11.5pt; color: #222; letter-spacing: .01em; min-height: 7mm; }
.pl .model .n { flex: none; font-size: 7.5pt; font-weight: 700; color: #555; }
.pl .wr { position: relative; border-bottom: .3mm solid #666; }
.chk { display: flex; align-items: center; gap: 5mm; border-top: .3mm solid #111; padding-top: 2.6mm; font-size: 9pt; }
.chk b { font-size: 9.5pt; font-weight: 900; margin-right: 1mm; }
.chk .bx2 { display: inline-flex; align-items: center; gap: 1.4mm; }
.chk .bx2 i { display: inline-block; width: 3.6mm; height: 3.6mm; border: .3mm solid #111; }
.chk .sig { margin-left: auto; display: inline-flex; align-items: flex-end; gap: 1.5mm; }
.chk .sig i { display: inline-block; width: 30mm; border-bottom: .3mm solid #555; height: 5mm; }

/* ── 문제 쪽 ── */
.pi .tband .topic { display: inline-block; margin-top: 1mm; font-size: 8.5pt; font-weight: 700; border: .3mm solid #111;
                    border-radius: 999px; padding: .3mm 3mm; }
.pi .body { display: flex; flex-direction: column; gap: 3mm; }
.prob { border: .45mm solid #111; border-radius: 2mm; padding: 3mm 4mm 3.2mm; display: grid; grid-template-columns: minmax(0, 1fr) auto;
        column-gap: 5mm; align-items: start; }
.prob.nofig { grid-template-columns: minmax(0, 1fr); }
.prob .txt { font-size: 10.8pt; line-height: 1.75; }
.lv-elem .prob .txt { font-size: 12.2pt; line-height: 1.8; }
.prob .story { margin: 0; }
.prob .conds { list-style: none; margin: 2mm 0 0; padding: 1.6mm 3mm; border: .25mm solid #999; border-radius: 1.4mm; background: #f6f6f6; }
.prob .conds li { margin: .4mm 0; }
.prob .ask { margin: 2.2mm 0 0; font-weight: 700; }
.prob .fig { width: 58mm; display: flex; justify-content: center; align-items: center; }
.prob .fig svg { width: 100%; height: auto; display: block; }
.ans { flex: 1; display: flex; flex-direction: column; gap: 2.4mm; min-height: 0; }
.abox { border: .4mm solid #111; border-radius: 1.8mm; display: flex; flex-direction: column; min-height: 0; }
.abox .ah { flex: none; display: flex; justify-content: space-between; align-items: baseline; padding: 1mm 3mm .9mm;
            border-bottom: .25mm dashed #888; font-size: 8.4pt; font-weight: 800; }
.abox .ah i { font-style: normal; font-weight: 500; color: #555; font-size: 8pt; }
.abox .aw { flex: 1; min-height: 0; }
"""


def font_links():
    files = [("noto-sans-kr", w) for w in ("400.css", "500.css", "700.css", "900.css")] + [("gaegu", "700.css")]
    return "".join(f'<link rel="stylesheet" href="{(FONTS / fam / w).as_uri()}">' for fam, w in files)


def marks_html(page_no, check):
    s = [(INSET, INSET), (W_U - INSET - MK, INSET), (W_U - INSET - MK, H_U - INSET - MK), (INSET, H_U - INSET - MK)]
    out = [f'<div class="mk" style="left:{x * U:.3f}mm;top:{y * U:.3f}mm;width:{MK * U:.3f}mm;height:{MK * U:.3f}mm"></div>' for x, y in s]
    o = ORIENT
    out.append(f'<div class="mk" style="left:{o["x"] * U:.3f}mm;top:{o["y"] * U:.3f}mm;width:{o["w"] * U:.3f}mm;height:{o["h"] * U:.3f}mm"></div>')
    pc = PAGECODE
    for i, b in enumerate(encode_page(page_no, check)):
        x = pc["x0"] + pc["pitch"] * i
        out.append(f'<div class="pc{"" if b else " z"}" style="left:{x * U:.3f}mm;top:{pc["y0"] * U:.3f}mm;width:{pc["size"] * U:.3f}mm;height:{pc["size"] * U:.3f}mm"></div>')
    return "".join(out)


def hw_line(parts):
    if isinstance(parts, str):
        parts = [parts]
    out = []
    for p in parts:
        if isinstance(p, tuple) and p[0] == "x":
            out.append(f'<span class="x">{html.escape(p[1])}</span>')
        else:
            t = html.escape(p)
            for op in ("×", "÷"):
                t = t.replace(op, f'<span class="op">{op}</span>')
            out.append(t)
    return f'<div class="ln">{"".join(out)}</div>'


ARROW_SVG = ('<div class="arw"><svg viewBox="0 0 13 30" preserveAspectRatio="none" aria-hidden="true">'
             '<path d="M2 27 C 7.5 26, 4.5 8.5, 10.2 4.6" fill="none" stroke="#111" stroke-width="1.7" stroke-linecap="round" vector-effect="non-scaling-stroke"/>'
             '<path d="M7.1 3.9 L10.6 4.4 L9.8 7.6" fill="none" stroke="#111" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>'
             '</svg></div>')


def kicker(spec):
    d = spec.get("date")
    ds = ""
    if d:
        y, m, dd = (int(x) for x in d.split("-"))
        ds = f" · {m}월 {dd}일"
    g = spec.get("grade_label") or LEVELS.get(spec.get("level"), "")
    return f"애쉬레인 서술형 평가{ds}{' · ' + html.escape(g) if g else ''}"


def foot(spec, label, page_no, total):
    return (f'<div class="foot"><span>애쉬레인 서술형 평가 · {html.escape(spec["code"])} · {html.escape(label)}</span>'
            f'<span>{page_no} / {total}</span></div>')


def page1_html(spec, total, check):
    level = spec.get("level") or "mid"
    ex = EXAMPLES[level]
    nt = ex["notes"]
    s1 = "".join(hw_line(l) for l in ex["s1"])
    s2_left = "".join(hw_line(l) for l in ex["s2"])
    if ex["s2_right"]:
        s2 = f'<div class="cols"><div>{s2_left}</div>{ARROW_SVG}<div class="right">{"".join(hw_line(l) for l in ex["s2_right"])}</div></div>'
    else:
        s2 = s2_left
    groups, n = [], 0
    for name, items in rules(total):
        rs = []
        for lead, body in items:
            n += 1
            rs.append(f'<div class="r"><span class="n">{n}</span><p><b>{html.escape(lead)}</b> {html.escape(body)}</p></div>')
        groups.append(f'<div class="grp"><h3>{name}</h3>{"".join(rs)}</div>')
    n_items = len(spec["items"])
    pts = sum(sum(r["points"] for r in it["rubric"]) for it in spec["items"])
    el = spec["items"][0]["rubric"]
    el_txt = " · ".join(f'{"①②③④⑤"[k]} {html.escape(r["element"])} {r["points"]}점' for k, r in enumerate(el))
    return f"""
<section class="page p1 lv-{level}"><div class="card">
  {marks_html(1, check)}
  <div class="tband"><div class="kick">{kicker(spec)}</div><h1>학생 확인 사항</h1></div>
  <div class="body">
    <div class="ov">
      <div><b>{n_items}문제 · {pts}점</b><span>한 쪽에 한 문제,<br>문제마다 {el and sum(r["points"] for r in el)}점이에요.</span></div>
      <div><b>오픈북</b><span>교과서·개념서·노트를<br>펴 놓고 풀어도 돼요.</span></div>
      <div><b>과정이 점수</b><span>{el_txt}.<br>답만 쓰면 {spec.get("policy", {}).get("answer_only_max", 3)}점까지만 받아요.</span></div>
    </div>
    <div class="blk"><h2>풀이 작성 예시</h2>
    <div class="ex">
      <div class="exq"><span class="no">예시</span><p>{html.escape(ex["problem"])}</p></div>
      <div class="nt q">{nt["q"]}</div>
      <div class="bx"><div class="lb">① 식 세우기<i>4점</i></div><div class="w hw">{s1}</div></div>
      <div class="nt"><span class="k">①</span>{nt["s1"]}</div>
      <div class="bx"><div class="lb">② 식 풀기<i>3점</i></div><div class="w hw">{s2}</div></div>
      <div class="nt"><span class="k">②</span>{nt["s2"]}</div>
      <div class="bx"><div class="lb">③ 구하는 것<i>3점</i></div><div class="w hw">{hw_line(ex["s3"])}</div></div>
      <div class="nt"><span class="k">③</span>{nt["s3"]}</div>
    </div></div>
    <div class="blk"><h2>주의 사항</h2>
    <div class="rules"><div>{"".join(groups[:2])}</div><div>{"".join(groups[2:])}</div></div></div>
  </div>
</div>
{foot(spec, "학생 확인 사항", 1, total)}
</section>"""


def date_text(date):
    if not date:
        return "20&emsp;&ensp;년&emsp;&emsp;월&emsp;&emsp;일"
    y, m, d = (int(x) for x in date.split("-"))
    wd = "월화수목금토일"[datetime.date(y, m, d).weekday()]
    return f"{y}년 {m}월 {d}일 ({wd})"


def qr_svg(url):
    q = segno.make(url, error="q", micro=False)
    return q.svg_inline(scale=1, border=4, dark="#000", light="#fff", omitsize=True), q.version


def page2_html(spec, total, check):
    level = spec.get("level") or "mid"
    url = f"{SITE}/e/{spec['code']}"
    svg, _ = qr_svg(url)
    grade = {"elem": "초등", "mid": "중학교", "high": "고등학교"}[level]
    wr_h = 20 if level == "elem" else 14.5
    pls = []
    for i, (txt, rich) in enumerate(phrase_lines(level), 1):
        pls.append(f'<div class="pl"><div class="model"><span class="n">{i}</span><span>{rich or html.escape(txt)}</span></div>'
                   f'<div class="wr" data-region="phrase_{i}" style="height:{wr_h}mm"></div></div>')
    return f"""
<section class="page p2 lv-{level}"><div class="card">
  {marks_html(2, check)}
  <div class="tband"><div class="kick">{kicker(spec)}</div><h1>강사 확인 사항</h1></div>
  <div class="sub"><span>학년·이름·필적 확인 문장은 <b>학생이 직접</b> 써요. 닉네임은 선택이에요.</span>
       <span class="date">{date_text(spec.get("date"))}</span></div>
  <div class="flow">
    <div class="qrb">
      <div class="qr">{svg}</div>
      <div class="qrc"><b>찍어서 채점받기</b>
        <span>다 풀었으면 휴대폰 카메라로 이 QR을 찍어요.<br>앱을 쓰면 「서술형 평가」 알림에서 바로 열어도 돼요.<br>안내에 따라 1쪽부터 한 장씩 찍으면 채점돼요.</span>
        <code>{html.escape(url.replace("https://", ""))} · 평가 코드 <em>{html.escape(spec["code"])}</em></code></div>
    </div>
    <div class="row2">
      <div class="fld"><label>학년</label><div class="val">{grade}<span class="bl" data-region="grade"></span>학년</div></div>
      <div class="fld"><label>이름</label><div class="val" data-region="name"></div></div>
    </div>
    <div class="ph">
      <div class="phh"><b>필적 확인</b><span>아래 문장을 평소 글씨로 그대로 따라 써요. 매번 같은 문장이에요.</span></div>
      {"".join(pls)}
    </div>
    <div class="fld"><label>닉네임<em>(선택)</em></label><div class="val" data-region="nickname"></div>
      <span class="hint">쓰고 싶을 때만 써요</span></div>
    <div class="chk">
      <b>강사 확인</b>
      <span class="bx2"><i></i>학년·이름</span><span class="bx2"><i></i>필적 문장</span><span class="bx2"><i></i>채점 완료</span>
      <span class="sig">확인<i></i></span>
    </div>
  </div>
</div>
{foot(spec, "강사 확인 사항", 2, total)}
</section>"""


def item_html(spec, it, rendered, total, check):
    level = spec.get("level") or "mid"
    pno = it["page"]
    story = rendered[it["story"]] if it.get("story") else ""
    ask = rendered[it["ask"]] if it.get("ask") else ""
    conds = "".join(f"<li>{rendered[c]}</li>" for c in it.get("conditions") or [])
    fig = it.get("figure_svg")
    boxes = []
    flex = {1: 3, 2: 5, 3: 2}
    for k, r in enumerate(it["rubric"], 1):
        hint = " — 답은 단위까지" if r["element"] == "구하는 것" else ""
        boxes.append(f'<div class="abox" style="flex:{flex.get(k, 3)}"><div class="ah"><span>{"①②③④⑤"[k - 1]} {html.escape(r["element"])}{hint}</span>'
                     f'<i>{r["points"]}점</i></div><div class="aw" data-region="s{k}"></div></div>')
    return f"""
<section class="page pi lv-{level}"><div class="card">
  {marks_html(pno, check)}
  <div class="tband"><div class="kick">{kicker(spec)}</div><h1>문제 {it["no"]}</h1>
    {f'<span class="topic">{html.escape(it["topic"])}</span>' if it.get("topic") else ""}</div>
  <div class="body">
    <div class="prob{"" if fig else " nofig"}" data-region="q">
      <div class="txt">
        {f'<p class="story">{story}</p>' if story else ""}
        {f'<ul class="conds">{conds}</ul>' if conds else ""}
        {f'<p class="ask">{ask}</p>' if ask else ""}
      </div>
      {f'<div class="fig">{fig}</div>' if fig else ""}
    </div>
    <div class="ans">{"".join(boxes)}</div>
  </div>
</div>
{foot(spec, f"문제 {it['no']}", pno, total)}
</section>"""


MEASURE_JS = """
() => [...document.querySelectorAll('.page')].map((pg) => {
  const card = pg.querySelector('.card');
  const c = card.getBoundingClientRect();
  const pxPerMm = c.width / 190;
  const u = (v) => Math.round(v / pxPerMm / 0.19);
  const regions = {};
  for (const el of card.querySelectorAll('[data-region]')) {
    const r = el.getBoundingClientRect();
    regions[el.dataset.region] = [u(r.left - c.left), u(r.top - c.top), u(r.right - c.left), u(r.bottom - c.top)];
  }
  let worst = 0;
  for (const el of card.querySelectorAll('*')) {
    const e = el.getBoundingClientRect();
    if (e.width && e.height) worst = Math.max(worst, e.bottom - c.bottom, e.right - c.right);
  }
  const body = card.querySelector('.body');
  let bodyOver = 0;
  if (body) {
    const b = body.getBoundingClientRect();
    for (const el of body.querySelectorAll('*')) { const e = el.getBoundingClientRect(); if (e.width && e.height) bodyOver = Math.max(bodyOver, e.bottom - b.bottom); }
  }
  return { regions, overflow: Math.round(worst), bodyOver: Math.round(bodyOver) };
})
"""


def load_spec(path):
    p = pathlib.Path(path)
    if p.suffix == ".json":
        return json.loads(p.read_text(encoding="utf-8")), None
    sp = importlib.util.spec_from_file_location("assess_spec", p)
    mod = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(mod)
    return mod.SPEC, getattr(mod, "verify", None)


def mathir_batch(texts):
    r = subprocess.run(["node", str(ROOT / "lib" / "mathir_render.mjs"), str(REPO)], input=json.dumps({"texts": texts}),
                       capture_output=True, text=True, check=True)
    out = json.loads(r.stdout)
    return out["html"], out["css"], out["errs"]


def verify_phrase():
    CHO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
    JONG = ["", "ㄱ", "ㄲ", "ㄳ", "ㄴ", "ㄵ", "ㄶ", "ㄷ", "ㄹ", "ㄺ", "ㄻ", "ㄼ", "ㄽ", "ㄾ", "ㄿ", "ㅀ", "ㅁ", "ㅂ", "ㅄ", "ㅅ", "ㅆ", "ㅇ", "ㅈ", "ㅊ", "ㅋ", "ㅌ", "ㅍ", "ㅎ"]
    cho, jong = set(), set()
    for ch in " ".join(t for t, _ in PHRASE):
        c = ord(ch) - 0xAC00
        if 0 <= c < 11172:
            cho.add(CHO[c // 588])
            if c % 28:
                jong.add(JONG[c % 28])
    assert set(CHO) <= cho | {j for j in jong if j in CHO}
    expr = PHRASE[2][0]
    assert set("0123456789") <= set(expr) and all(op in expr for op in "+−×÷=()")
    assert (41 + 59) * 30 - 78 // 6 == 2987 and 78 % 6 == 0


def normalize_spec(spec):
    """스펙 → 문항 번호·쪽 번호·배점 채우기"""
    s = dict(spec)
    assert s.get("code") and s["code"].isalnum() and s["code"].upper() == s["code"] and 4 <= len(s["code"]) <= 12, "code"
    items = []
    for i, it in enumerate(s["items"], 1):
        x = dict(it)
        x["no"] = i
        x["page"] = i + 2
        x["points"] = sum(r["points"] for r in x["rubric"])
        for k, r in enumerate(x["rubric"], 1):
            r.setdefault("no", k)
        items.append(x)
    assert 1 <= len(items) <= 13
    s["items"] = items
    return s


def build(spec_path, out_root, png=False):
    from playwright.sync_api import sync_playwright
    assert (FONTS / "noto-sans-kr").exists() and (FONTS / "gaegu").exists(), f"글꼴이 없어요 — 먼저: cd {ROOT} && npm install"
    spec, verify_fn = load_spec(spec_path)
    checks = {"code_words": _selftest_code(), "code_same_as_app": _crosscheck_code()}
    if verify_fn:
        checks["spec"] = verify_fn()
    verify_phrase()
    spec = normalize_spec(spec)
    code = spec["code"]
    check = check_of(code)
    total = 2 + len(spec["items"])

    # MathIR → HTML (앱과 같은 렌더러)
    texts = []
    for it in spec["items"]:
        texts += [t for t in [it.get("story"), it.get("ask")] if t] + list(it.get("conditions") or []) + list(it.get("solution") or []) + [it["answer"]]
    htmls, math_css, errs = mathir_batch(texts)
    bad = [(t, e) for t, e in zip(texts, errs) if e]
    assert not bad, f"MathIR 문법 오류: {bad}"
    rendered = dict(zip(texts, htmls))

    pages_html = [page1_html(spec, total, check), page2_html(spec, total, check)] + [item_html(spec, it, rendered, total, check) for it in spec["items"]]
    doc = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{html.escape(spec["title"])}</title>{font_links()}'
           f'<style>{CSS}{math_css}</style></head><body>{"".join(pages_html)}</body></html>')
    out = pathlib.Path(out_root) / code
    out.mkdir(parents=True, exist_ok=True)
    src = out / f"{code}.html"
    src.write_text(doc, encoding="utf-8")
    pdf = out / f"{code}.pdf"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        pg = b.new_page(viewport={"width": 1240, "height": 1754})
        pg.goto(src.as_uri())
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(500)
        meas = pg.evaluate(MEASURE_JS)
        pg.pdf(path=str(pdf), format="A4", print_background=True, prefer_css_page_size=True,
               margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
        b.close()
    assert len(meas) == total, (len(meas), total)
    for i, m in enumerate(meas, 1):
        assert m["overflow"] <= 0, f"{i}쪽 내용이 카드 밖으로 {m['overflow']}px 넘침"
        assert m["bodyOver"] <= 0, f"{i}쪽 본문이 마커 띠까지 {m['bodyOver']}px 내려옴"

    # 쪽 목록 + 영역
    pages = [{"no": 1, "kind": "guide"},
             {"no": 2, "kind": "info", "regions": {k: v for k, v in meas[1]["regions"].items()}}]
    for it in spec["items"]:
        reg = meas[it["page"] - 1]["regions"]
        r = {k: reg[k] for k in ("q", "s1", "s2", "s3") if k in reg}
        # 답안 칸 최소 높이(단위) — 너무 좁으면 생성기에서 막는다
        for k, mn in (("s1", 120), ("s2", 230), ("s3", 70)):
            assert r[k][3] - r[k][1] >= mn, f"문제 {it['no']} {k} 칸이 너무 좁아요 ({r[k][3] - r[k][1]}단위) — 문장·그림을 줄이세요"
        pages.append({"no": it["page"], "kind": "item", "item": it["no"], "regions": r})

    J = {
        "kind": "ashrain.assess", "version": 1,
        "code": code, "title": spec["title"], "level": spec.get("level", "mid"), "grade_label": spec.get("grade_label"),
        "date": spec.get("date"), "open_book": spec.get("open_book", True),
        "reveal": spec.get("reveal", "after_close"), "opens_at": spec.get("opens_at"), "closes_at": spec.get("closes_at"),
        "policy": spec.get("policy", {"carry": "half", "alt_method": "accept", "answer_only_max": 3}),
        "sheet": {"w": W_U, "h": H_U, "mm_per_unit": U, "markers": {"size": MK, "inset": INSET}, "orient": ORIENT,
                  "pagecode": {**PAGECODE, "check": check}},
        "pages": pages,
        "phrase": [t for t, _ in phrase_lines(spec.get("level", "mid"))],
        "items": [{
            "no": it["no"], "page": it["page"], "topic": it.get("topic", ""), "story": it.get("story", ""),
            "figure_svg": it.get("figure_svg"), "conditions": it.get("conditions") or [], "ask": it.get("ask", ""),
            "points": it["points"], "rubric": it["rubric"], "answer": it["answer"], "solution": it.get("solution") or [],
            "accept": it.get("accept") or [], "misses": it.get("misses") or [], "deductions": it.get("deductions") or [],
        } for it in spec["items"]],
        "meta": {"generator": "build_assess.py v1", "built_at": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(timespec="seconds"),
                 "qr": f"{SITE}/e/{code}"},
    }
    jpath = out / f"{code}.json"
    jpath.write_text(json.dumps(J, ensure_ascii=False, indent=1), encoding="utf-8")

    # 앱 검사기(spec.js)로 한 번 더
    r = subprocess.run(["node", "-e", f"""
      import('{(REPO / "src/lib/assess/spec.js").as_uri()}').then(m => {{
        const fs = require('fs'); const raw = fs.readFileSync('{jpath}', 'utf8');
        const v = m.validateSpec(JSON.parse(raw), {{ bytes: Buffer.byteLength(raw) }});
        console.log(JSON.stringify(v)); process.exit(v.ok ? 0 : 1);
      }});"""], capture_output=True, text=True)
    v = json.loads(r.stdout or "{}")
    assert r.returncode == 0 and v.get("ok"), f"앱 검사 실패: {v.get('errors')} {r.stderr[-500:]}"
    checks["validate"] = {"warnings": v.get("warnings"), "summary": v.get("summary")}

    # 쪽 번호 띠 · 마커 — 래스터로 떠서 앱 검출기로 읽어 본다
    import pymupdf
    d = pymupdf.open(str(pdf))
    rasters = out / "_ras"
    rasters.mkdir(exist_ok=True)
    meta = {}
    for i, p in enumerate(d, 1):
        pix = p.get_pixmap(dpi=150, colorspace=pymupdf.csGRAY)
        (rasters / f"p{i}.gray").write_bytes(pix.samples)
        meta[f"p{i}"] = {"width": pix.width, "height": pix.height}
        if png:
            p.get_pixmap(dpi=110).save(str(out / f"p{i}.png"))
    (rasters / "meta.json").write_text(json.dumps(meta))
    r = subprocess.run(["node", str(ROOT / "lib" / "read_pages.mjs"), str(REPO), str(rasters), str(jpath)], capture_output=True, text=True)
    res = json.loads(r.stdout or "{}")
    for i in range(1, total + 1):
        x = res.get(f"p{i}", {})
        assert x.get("ok") and x.get("page") == i and x.get("check") == check, f"{i}쪽 띠 판독 실패: {x} {r.stderr[-400:]}"
    checks["pagecode"] = {k: {kk: v[kk] for kk in ("page", "contrast", "margin")} for k, v in res.items()}
    for f in rasters.iterdir():
        f.unlink()
    rasters.rmdir()
    return {"pdf": str(pdf), "json": str(jpath), "pages": total, "check": check, "checks": checks}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("spec")
    ap.add_argument("--out", default=str(ROOT / "out"))
    ap.add_argument("--png", action="store_true")
    a = ap.parse_args()
    print(json.dumps(build(a.spec, a.out, a.png), ensure_ascii=False, indent=1))
