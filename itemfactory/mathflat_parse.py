# ashrain.out — 매쓰플랫 문제지 파서 (mathflat_parse.py, v1.0)
# 위치: itemfactory/mathflat_parse.py
#
# 매쓰플랫(MATH SQUARE) 출력 PDF의 고정 템플릿을 결정론으로 해체한다:
#   · 문항 번호·유형명·정답률 = 텍스트 레이어에서 정확 채집 (비전 오독 0)
#   · 문항 본문+도형 = 이미 문항 단위로 잘린 내장 이미지 그대로 추출
#   · 빠른정답 = 번호↔답 미니 이미지 페어링 → 번호 라벨 합성 1장 (러너 answer_sheet 경로 호환)
#   · 빠른정답 이후 페이지(해설)는 정책상 제외
# 결과를 기존 전사 큐에 "문항=페이지"로 적재 → 클라우드/로컬 러너가 그대로 처리.
#
# 사용:
#   python mathflat_parse.py 문제지.pdf --unit m2-2                # 큐 적재 (기본 클라우드)
#   python mathflat_parse.py 문제지.pdf --unit m2-2 --runner local --arb queue
#   python mathflat_parse.py 문제지.pdf --dry                      # DB 없이 ./mf_out/ 에 결과만
# 여러 파일: python mathflat_parse.py a.pdf b.pdf c.pdf --unit m2-2

import argparse, io, re, sys, time
from pathlib import Path

try:
    import pymupdf
except ImportError:
    sys.exit("pip install pymupdf 필요")
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
COL_SPLIT = 300          # 좌/우 열 경계 (pt)
BODY_W = (150, 360)      # 본문 이미지 폭 범위 (pt)


def spans(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = s["text"].strip()
                if t:
                    out.append({"x": s["bbox"][0], "y": s["bbox"][1], "t": t})
    return out


def crop(page, bbox, zoom=2.7):
    """영역 렌더 — 임베디드 이미지의 투명 마스크·색공간 문제를 화면 합성 결과로 우회"""
    pix = page.get_pixmap(clip=pymupdf.Rect(bbox), matrix=pymupdf.Matrix(zoom, zoom))
    return Image.open(io.BytesIO(pix.tobytes("png")))


def parse_pdf(path):
    """PDF → items[{seq, src_tag, p_correct, png}], answers_png(합성), meta"""
    doc = pymupdf.open(path)
    ans_page = None
    for i, p in enumerate(doc):
        if any("빠른정답" in s["t"] for s in spans(p)):
            ans_page = i
            break
    if ans_page is None:
        raise RuntimeError("빠른정답 페이지를 못 찾음 — 매쓰플랫 출력이 맞는지 확인")

    items = []
    for pi in range(ans_page):
        p = doc[pi]
        sp = spans(p)
        nums = sorted([s for s in sp if re.fullmatch(r"\d{2}", s["t"])],
                      key=lambda s: (s["x"] > COL_SPLIT, s["y"]))
        heads = [s for s in sp if s["t"].startswith("|")]
        rates = [s for s in sp if s["t"].startswith("정답률")]
        imgs = [i2 for i2 in p.get_image_info(xrefs=True)
                if BODY_W[0] <= i2["bbox"][2] - i2["bbox"][0] <= BODY_W[1] and i2["bbox"][1] < 780]
        for k, n in enumerate(nums):
            col = n["x"] > COL_SPLIT
            nxt = next((m["y"] for m in nums[k + 1:] if (m["x"] > COL_SPLIT) == col), 9999)
            body = [i2 for i2 in imgs
                    if (i2["bbox"][0] > COL_SPLIT) == col and n["y"] - 6 < i2["bbox"][1] < nxt]
            if not body:
                print(f"  ⚠ 문항 {n['t']} 본문 이미지 없음 — 건너뜀"); continue
            body.sort(key=lambda i2: i2["bbox"][1])
            pil = [crop(p, b["bbox"]) for b in body]
            if len(pil) == 1:
                im = pil[0]
            else:                                   # 드물게 본문이 여러 조각이면 세로 합성
                w = max(x.width for x in pil)
                im = Image.new("RGB", (w, sum(x.height for x in pil) + 8 * len(pil)), "white")
                yy = 0
                for x in pil:
                    im.paste(x, (0, yy)); yy += x.height + 8
            head = min([h for h in heads if (h["x"] > COL_SPLIT) == col and h["y"] < n["y"]],
                       key=lambda h: n["y"] - h["y"], default=None)
            rate = min([r for r in rates if (r["x"] > COL_SPLIT) == col and abs(r["y"] - (head["y"] if head else n["y"])) < 8],
                       key=lambda r: abs(r["y"] - n["y"]), default=None)
            pc = None
            if rate:
                m = re.search(r"(\d+)\s*%", rate["t"])
                pc = int(m.group(1)) if m else None
            items.append({"seq": int(n["t"]),
                          "src_tag": head["t"].strip("| ").strip() if head else None,
                          "p_correct": pc, "img": im})

    # ── 빠른정답 합성
    ap = doc[ans_page]
    asp = spans(ap)
    anums = [s for s in asp if re.fullmatch(r"\d{2}", s["t"])]
    aimgs = [i2 for i2 in ap.get_image_info(xrefs=True)
             if i2["bbox"][2] - i2["bbox"][0] < 140 and i2["bbox"][1] > 150]
    pairs = []
    for n in anums:
        cand = [i2 for i2 in aimgs if abs(i2["bbox"][1] - n["y"]) < 26 and i2["bbox"][0] > n["x"]]
        if not cand: continue
        best = min(cand, key=lambda i2: i2["bbox"][0] - n["x"])
        pairs.append((int(n["t"]), best))
    pairs.sort()
    cell_h = 64
    canvas = Image.new("RGB", (520, cell_h * ((len(pairs) + 2) // 3) + 20), "white")
    dr = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except Exception:
        font = ImageFont.load_default()
    for idx, (seq, info) in enumerate(pairs):
        cx, cy = (idx % 3) * 172 + 8, (idx // 3) * cell_h + 10
        dr.text((cx, cy + 12), f"{seq:02d}", fill="black", font=font)
        aim = crop(ap, info["bbox"], zoom=3.2)
        r = min(1.0, 44 / aim.height, 110 / aim.width)
        aim = aim.resize((max(1, int(aim.width * r)), max(1, int(aim.height * r))))
        canvas.paste(aim, (cx + 44, cy + 4))
    skipped = len(doc) - ans_page - 1
    return items, canvas, {"title": Path(path).stem, "pages": ans_page,
                           "answers": len(pairs), "skipped_solution_pages": skipped}


def to_jpg(im, q=88):
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=q)
    return buf.getvalue()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("--unit", default=None, help="단원 힌트 (예: m2-2)")
    ap.add_argument("--runner", default="cloud", choices=["cloud", "local"])
    ap.add_argument("--arb", default="api", choices=["api", "queue"])
    ap.add_argument("--dry", action="store_true", help="DB 없이 ./mf_out/ 에 파일로만")
    a = ap.parse_args()

    sb = None
    if not a.dry:
        sys.path.insert(0, str(HERE))
        from transcribe_local import load_env, get_client
        load_env(); sb = get_client()

    for pdf in a.pdfs:
        print(f"\n== {pdf} ==")
        items, ans_img, meta = parse_pdf(pdf)
        got_pc = sum(1 for i in items if i["p_correct"] is not None)
        print(f"  문항 {len(items)} · 정답률 채집 {got_pc} · 답 {meta['answers']} · 해설 제외 {meta['skipped_solution_pages']}p")

        if a.dry:
            out = Path("mf_out") / meta["title"]
            out.mkdir(parents=True, exist_ok=True)
            for it in items:
                it["img"].save(out / f"q{it['seq']:02d}.png")
            ans_img.save(out / "answers.png")
            import json
            (out / "meta.json").write_text(json.dumps(
                [{k: v for k, v in it.items() if k != "img"} for it in items],
                ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"  → {out}/ 저장 (dry)")
            continue

        doc_row = sb.table("corpus_docs").insert({
            "title": meta["title"], "unit_hint": a.unit, "pages": len(items)}).execute().data[0]
        job = sb.table("transcribe_jobs").insert({
            "doc_id": doc_row["id"], "title": meta["title"], "unit_hint": a.unit,
            "total_pages": len(items) + 1, "runner": a.runner, "arb_mode": a.arb}).execute().data[0]
        rows = []
        for it in items:
            path = f"jobs/{job['id']}/q{it['seq']:02d}.jpg"
            sb.storage.from_("corpus").upload(path, to_jpg(it["img"]), {"content-type": "image/jpeg"})
            rows.append({"job_id": job["id"], "page": it["seq"], "storage_path": path,
                         "meta": {"src_tag": it["src_tag"], "p_correct": it["p_correct"]}})
        apath = f"jobs/{job['id']}/answers.jpg"
        sb.storage.from_("corpus").upload(apath, to_jpg(ans_img), {"content-type": "image/jpeg"})
        rows.append({"job_id": job["id"], "page": 900, "storage_path": apath, "meta": {"kind": "answers"}})
        sb.table("transcribe_job_pages").insert(rows).execute()
        print(f"  → 큐 적재 완료 (runner={a.runner}) — 클라우드면 코퍼스 화면 열어 점화, 로컬이면 워커가 집어감")


if __name__ == "__main__":
    main()
