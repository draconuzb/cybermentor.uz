from PIL import Image
import sys

img = Image.open("thumb.jpg").convert("L")
w, h = img.size
px = img.load()

# Otsu-like simple threshold using mean
pixels = [px[x, y] for y in range(h) for x in range(w)]
mean = sum(pixels) / len(pixels)
thresh = mean

def bit(x, y):
    return 1 if px[x, y] < thresh else 0

# Try to detect module size by finding shortest run length in first few rows/cols
def shortest_run(seq):
    runs = []
    cur = seq[0]
    count = 1
    for v in seq[1:]:
        if v == cur:
            count += 1
        else:
            runs.append(count)
            cur = v
            count = 1
    runs.append(count)
    return runs

row_bits = [bit(x, h // 2) for x in range(w)]
col_bits = [bit(w // 2, y) for y in range(h)]
print("W,H:", w, h, "thresh:", thresh)
print("row runs sample:", shortest_run(row_bits)[:20])
print("col runs sample:", shortest_run(col_bits)[:30])

# print full binary grid at native resolution downsampled by candidate module sizes
# (capped to avoid huge output)
for mod in [4, 6, 8]:
    mw, mh = w // mod, h // mod
    if mw < 1 or mh < 1:
        continue
    grid = []
    for gy in range(mh):
        row = ""
        for gx in range(mw):
            # sample center pixel of the module
            sx = min(w - 1, gx * mod + mod // 2)
            sy = min(h - 1, gy * mod + mod // 2)
            row += "#" if bit(sx, sy) else "."
        grid.append(row)
    print(f"\n=== module={mod} grid {mw}x{mh} ===")
    for r in grid:
        print(r)
