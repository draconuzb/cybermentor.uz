from PIL import Image

img = Image.open("thumb.jpg").convert("L")
h = img.histogram()
nz = [(i, c) for i, c in enumerate(h) if c > 0]
total = sum(c for _, c in nz)
mid = sum(c for i, c in nz if 60 < i < 200)
print("distinct nonzero levels:", len(nz))
print("min/max level:", nz[0][0], nz[-1][0])
print("fraction in mid-gray 60-200:", mid / total)
print("sample low:", nz[:10])
print("sample high:", nz[-10:])
