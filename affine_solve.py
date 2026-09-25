crib_pt = bytes.fromhex("b2e3c05bee9a076f")
crib_ct = bytes.fromhex("3b2635ce8fb3f2ea")
ct = bytes.fromhex("46d1d72ecbf0a63a96a6375c374c4c96bb37a605377171bb027181dde4")

found = []
for a in range(1, 256, 2):  # a must be odd to be invertible mod 256
    for b in range(256):
        ok = True
        for p, c in zip(crib_pt, crib_ct):
            if (a * p + b) % 256 != c:
                ok = False
                break
        if ok:
            found.append((a, b))

print("candidates:", found)

for a, b in found:
    ainv = pow(a, -1, 256)
    pt = bytes(((c - b) * ainv) % 256 for c in ct)
    print(a, b, "->", pt)
