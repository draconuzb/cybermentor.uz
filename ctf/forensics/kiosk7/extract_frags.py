data = open("kiosk7.img", "rb").read()

import re

for m in re.finditer(rb"K7FRG.{0,200}?\x00", data, re.DOTALL):
    chunk = m.group(0)
    off = m.start()
    print(off, chunk[:120])

print("=== K7IDX ===")
for m in re.finditer(rb"K7IDX.{0,200}?\x00", data, re.DOTALL):
    chunk = m.group(0)
    off = m.start()
    print(off, chunk[:120])
