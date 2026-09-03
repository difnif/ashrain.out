# -*- coding: utf-8 -*-
# zip 해제(UTF-8/cp437 파일명 보정) + manifest 요약
import zipfile, json, os, sys
from PIL import Image

def extract(zipname):
    src = f"/mnt/user-data/uploads/esc files/{zipname}.zip"
    dst = f"/root/esc/work/{zipname}"
    z = zipfile.ZipFile(src)
    os.makedirs(dst, exist_ok=True)
    for info in z.infolist():
        name = info.filename
        if not (info.flag_bits & 0x800):
            try: name = info.filename.encode("cp437").decode("utf-8")
            except Exception: pass
        target = os.path.join(dst, name)
        if info.is_dir():
            os.makedirs(target, exist_ok=True); continue
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f: f.write(z.read(info))
    return dst

def summary(zipname):
    dst = f"/root/esc/work/{zipname}"
    m = json.load(open(f"{dst}/manifest.json", encoding="utf-8"))
    print(zipname, m["chunk"])
    for it in m["items"]:
        img = it["image"]
        p = os.path.join(dst, img)
        size = Image.open(p).size if os.path.exists(p) else "MISSING"
        print(f"  {it['id'][:8]} | {img.split('/')[-1]} | {size} | seq {it['seq']} | {it['unit_id']} | {it['src_tag']} | {it['esc_triage']} | qa={it.get('quick_answer')!r} | diff={sorted(set(it['diff']))}")

if __name__ == "__main__":
    for zn in sys.argv[1:]:
        extract(zn); summary(zn)
