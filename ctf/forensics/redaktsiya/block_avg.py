from PIL import Image

img = Image.open("thumb.jpg").convert("L")
w, h = img.size
px = img.load()

for cols, rows in [(9, 31), (9, 32), (10, 31), (10, 32)]:
    cw = w / cols
    ch = h / rows
    grid = []
    for r in range(rows):
        row = ""
        for c in range(cols):
            x0, x1 = int(c * cw), int((c + 1) * cw)
            y0, y1 = int(r * ch), int((r + 1) * ch)
            vals = [px[x, y] for y in range(y0, min(y1, h)) for x in range(x0, min(x1, w))]
            avg = sum(vals) / len(vals)
            row += "#" if avg < 128 else "."
        grid.append(row)
    print(f"\n=== {cols}x{rows} block-avg grid ===")
    for row in grid:
        print(row)
