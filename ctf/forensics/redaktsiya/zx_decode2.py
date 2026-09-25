import zxingcpp
from PIL import Image, ImageOps

candidates = [
    "thumb.jpg", "clean_mod2.png", "clean_mod4.png", "clean_mod8.png",
]

binarizers = [zxingcpp.Binarizer.LocalAverage, zxingcpp.Binarizer.GlobalHistogram, zxingcpp.Binarizer.FixedThreshold]

found_any = False
for name in candidates:
    try:
        img = Image.open(name).convert("L")
    except FileNotFoundError:
        continue
    # add white quiet zone border
    padded = ImageOps.expand(img, border=20, fill=255)
    for rot in [0, 90, 180, 270]:
        rimg = padded.rotate(rot, expand=True, fillcolor=255)
        for b in binarizers:
            for pure in [False, True]:
                try:
                    results = zxingcpp.read_barcodes(rimg, binarizer=b, is_pure=pure)
                except Exception as e:
                    continue
                if results:
                    found_any = True
                    for r in results:
                        print(f"{name} rot={rot} bin={b} pure={pure}: FORMAT={r.format} TEXT={r.text!r}")
if not found_any:
    print("NOTHING FOUND across all variants")
