data = open("kiosk7.img", "rb").read()
import re

for m in re.finditer(rb"K7FRG", data):
    off = m.start()
    window = data[off:off+220]
    print("offset", off)
    print(window)
    print("---")

print("=== K7IDX ===")
for m in re.finditer(rb"K7IDX", data):
    off = m.start()
    window = data[off:off+220]
    print("offset", off)
    print(window)
