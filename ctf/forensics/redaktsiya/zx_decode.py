import zxingcpp
from PIL import Image

candidates = [
    "thumb.jpg", "thumb_r90.jpg", "thumb_r270.jpg",
    "thumb_big.jpg", "thumb_nn.jpg", "thumb_nn_r90.jpg",
    "thumb_square.jpg", "thumb_nn_orig.jpg", "scan.jpg",
]

for name in candidates:
    try:
        img = Image.open(name)
    except FileNotFoundError:
        continue
    results = zxingcpp.read_barcodes(img)
    if results:
        for r in results:
            print(f"{name}: FORMAT={r.format} TEXT={r.text!r}")
    else:
        print(f"{name}: no result")
