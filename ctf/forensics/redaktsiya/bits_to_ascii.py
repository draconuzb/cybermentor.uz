from PIL import Image
import re

img = Image.open("thumb.jpg").convert("L")
w, h = img.size
px = img.load()

def block_bits(cols, rows):
    cw = w / cols
    ch = h / rows
    bits = []
    for r in range(rows):
        for c in range(cols):
            x0, x1 = int(c * cw), int((c + 1) * cw)
            y0, y1 = int(r * ch), int((r + 1) * ch)
            vals = [px[x, y] for y in range(y0, min(y1, h)) for x in range(x0, min(x1, w))]
            avg = sum(vals) / len(vals)
            bits.append(1 if avg < 128 else 0)
    return bits

def bits_to_bytes(bits):
    n = len(bits) - (len(bits) % 8)
    out = bytearray()
    for i in range(0, n, 8):
        b = 0
        for j in range(8):
            b = (b << 1) | bits[i + j]
        out.append(b)
    return bytes(out)

printable = re.compile(rb'[\x20-\x7e]{3,}')

configs = [(9,31),(9,32),(10,31),(10,32),(24,79),(12,39),(16,52)]
for cols, rows in configs:
    bits = block_bits(cols, rows)
    for invert in [False, True]:
        b = [1-x for x in bits] if invert else bits
        data = bits_to_bytes(b)
        matches = printable.findall(data)
        if matches:
            print(f"{cols}x{rows} invert={invert}: MATCHES {matches}")
    # also column-major
    bits2d = [bits[r*cols:(r+1)*cols] for r in range(rows)]
    colmajor = [bits2d[r][c] for c in range(cols) for r in range(rows)]
    for invert in [False, True]:
        b = [1-x for x in colmajor] if invert else colmajor
        data = bits_to_bytes(b)
        matches = printable.findall(data)
        if matches:
            print(f"{cols}x{rows} COLMAJOR invert={invert}: MATCHES {matches}")

print("done")
