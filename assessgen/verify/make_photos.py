# SAMPLE01 PDF → 사진처럼 만든 회색조 raw (원근·회전·그림자·흐림·잡음·손글씨 흉내) — 앱 파이프라인(pipeline.js) 시험용
#   python3 assessgen/verify/make_photos.py <출력폴더> [<생성기 out 폴더>]   (SAMPLE01·SAMPLE02 를 먼저 빌드)
#   node assessgen/verify/run_pipeline.mjs . <출력폴더> assessgen/out/SAMPLE01/SAMPLE01.json
import json, sys, pathlib, numpy as np, cv2, pymupdf
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
OUTDIR = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else pathlib.Path(__file__).resolve().parents[1] / "out"
rng = np.random.default_rng(11)
J = json.loads((OUTDIR / "SAMPLE01" / "SAMPLE01.json").read_text())
def page_img(pdf, i, dpi=200):
    d = pymupdf.open(pdf); pix = d[i].get_pixmap(dpi=dpi, colorspace=pymupdf.csGRAY)
    return np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width).copy()
def scribble(img, regions, dpi=200):
    # 단위 → px: 카드 원점 10mm, 1단위 0.19mm
    k = dpi / 25.4
    for b in regions:
        x0, y0, x1, y1 = [(v * 0.19 + 10) * k for v in b]
        for line in range(int((y1 - y0) // (9 * k))):
            y = y0 + 8 * k + line * 9 * k
            x = x0 + 6 * k
            pts = []
            while x < x0 + (x1 - x0) * rng.uniform(0.35, 0.9):
                pts.append((x, y + rng.normal(0, 1.2 * k)))
                x += rng.uniform(1.0, 2.2) * k
            if len(pts) > 2:
                cv2.polylines(img, [np.int32(pts)], False, int(rng.integers(20, 70)), max(1, int(0.45 * k)), cv2.LINE_AA)
    return img
def photo(img, rot=6.5, persp=True, shade=0.32, blur=1.1, noise=6, flip=0):
    h, w = img.shape; pad = int(0.08 * max(h, w))
    canvas = np.full((h + 2 * pad, w + 2 * pad), 95, np.uint8); canvas[pad:pad + h, pad:pad + w] = img
    H, W = canvas.shape
    if persp:
        src = np.float32([[pad, pad], [pad + w, pad], [pad + w, pad + h], [pad, pad + h]])
        j = 0.025 * w
        dst = np.float32([[pad + 2.2 * j, pad + j], [pad + w - j, pad + 3 * j], [pad + w + j, pad + h - j], [pad - 1.3 * j, pad + h - 2.5 * j]])
        canvas = cv2.warpPerspective(canvas, cv2.getPerspectiveTransform(src, dst), (W, H), borderValue=95)
    canvas = cv2.warpAffine(canvas, cv2.getRotationMatrix2D((W / 2, H / 2), rot, 1.0), (W, H), borderValue=95)
    yy, xx = np.mgrid[0:H, 0:W]
    f = canvas.astype(np.float32) * (1.0 - shade * np.clip((xx / W) * 0.9 + (yy / H) * 0.5 - 0.35, 0, 1))
    if blur: f = cv2.GaussianBlur(f, (0, 0), blur)
    f += rng.normal(0, noise, f.shape)
    f = np.clip(f, 0, 255).astype(np.uint8)
    if flip == 180: f = cv2.rotate(f, cv2.ROTATE_180)
    if flip == 90: f = cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)
    s = 2400 / max(f.shape)
    return cv2.resize(f, (round(f.shape[1] * s), round(f.shape[0] * s)), interpolation=cv2.INTER_AREA)
pdf = str(OUTDIR / "SAMPLE01" / "SAMPLE01.pdf")
cases = {}
for i, pg in enumerate(J["pages"]):
    img = page_img(pdf, i)
    if pg["kind"] == "item": img = scribble(img, [pg["regions"][k] for k in ("s1", "s2", "s3")])
    if pg["kind"] == "info": img = scribble(img, [pg["regions"][k] for k in pg["regions"] if k != "grade"])
    cases[f"p{pg['no']}_photo"] = (photo(img), {"expect": "ok", "page": pg["no"]})
    if pg["kind"] == "item":
        cv2.imwrite(str(out / f"p{pg['no']}_photo.jpg"), cases[f"p{pg['no']}_photo"][0], [cv2.IMWRITE_JPEG_QUALITY, 88])
img3 = scribble(page_img(pdf, 2), [J["pages"][2]["regions"][k] for k in ("s1", "s2", "s3")])
cases["p3_rot180"] = (photo(img3, rot=-4, flip=180), {"expect": "ok", "page": 3})
cases["p3_rot90"] = (photo(img3, rot=3, flip=90), {"expect": "ok", "page": 3})
cases["p3_blur"] = (photo(img3, blur=7.0), {"expect": "fail"})
cases["p3_dark"] = (np.clip(photo(img3).astype(np.float32) * 0.28, 0, 255).astype(np.uint8), {"expect": "fail"})
other = page_img(str(OUTDIR / "SAMPLE02" / "SAMPLE02.pdf"), 2)
cases["other_set"] = (photo(other), {"expect": "other"})
crop = photo(img3)[300:1700, :]
cases["cut_off"] = (crop, {"expect": "fail"})
meta = {}
for k, (im, exp) in cases.items():
    (out / f"{k}.gray").write_bytes(im.tobytes())
    meta[k] = {"width": im.shape[1], "height": im.shape[0], **exp}
    cv2.imwrite(str(out / f"{k}.png"), cv2.resize(im, (im.shape[1] // 4, im.shape[0] // 4)))
(out / "meta.json").write_text(json.dumps(meta))
print(len(meta), "cases")
