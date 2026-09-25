import base64

frags = {
    0x4b: "ZGQwNj",
    0x90: "E0NDJ9",
    0x2f: "vb3RfYz",
    0x12: "WY3OWRk",
    0x01: "Q1RGe3J",
    0xc5: "k5MTFkM",
}

order = [0x01, 0x2f, 0xc5, 0x12, 0x4b, 0x90]
s = "".join(frags[k] for k in order)
print("concatenated:", s)
try:
    print("decoded:", base64.b64decode(s + "==").decode(errors="replace"))
except Exception as e:
    print("err", e)

# also try reverse order just in case
order2 = list(reversed(order))
s2 = "".join(frags[k] for k in order2)
print("concatenated(rev):", s2)
try:
    print("decoded(rev):", base64.b64decode(s2 + "==").decode(errors="replace"))
except Exception as e:
    print("err", e)
