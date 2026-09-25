from PIL import Image

img = Image.open("thumb.jpg").convert("L")
w, h = img.size
px = img.load()

pixels = [px[x, y] for y in range(h) for x in range(w)]
mean = sum(pixels) / len(pixels)
thresh = mean

def bit(x, y):
    return 1 if px[x, y] < thresh else 0

for mod in [2, 4, 8]:
    mw, mh = w // mod, h // mod
    scale = 10
    out = Image.new("L", (mw * scale, mh * scale), 255)
    opx = out.load()
    for gy in range(mh):
        for gx in range(mw):
            sx = min(w - 1, gx * mod + mod // 2)
            sy = min(h - 1, gy * mod + mod // 2)
            val = 0 if bit(sx, sy) else 255
            for yy in range(scale):
                for xx in range(scale):
                    opx[gx * scale + xx, gy * scale + yy] = val
    out.save(f"clean_mod{mod}.png")
    print(f"saved clean_mod{mod}.png size={out.size}")
