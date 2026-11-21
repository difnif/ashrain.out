import sys
from PIL import Image
out = sys.argv[1]; files = sys.argv[2:]
W, H = 800, 450
cols = 2
rows = (len(files) + cols - 1) // cols
M = Image.new("RGB", (W * cols, H * rows), "white")
for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((W, H))
    M.paste(im, ((i % cols) * W, (i // cols) * H))
M.save(out)
print(out)
