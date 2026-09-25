import urllib.request
import urllib.parse

HOST = "http://01d78438-bd06-471f-aa3d-bdf294098503.red.cyberkent.uz"

def get(path):
    return urllib.request.urlopen(f"{HOST}{path}", timeout=10).read().decode().strip()

def post(path, data):
    req = urllib.request.Request(f"{HOST}{path}", data=data.encode(), method="POST",
                                  headers={"Content-Type": "application/x-www-form-urlencoded"})
    return urllib.request.urlopen(req, timeout=10).read().decode().strip()

# --- Layer 1 ---
ct1 = bytes.fromhex(get("/s1/ct"))
zero_hex = "00" * len(ct1)
ks1 = bytes.fromhex(post("/s1/enc", f"pt={zero_hex}"))
tok1 = bytes(c ^ k for c, k in zip(ct1, ks1)).decode()
print("tok1:", tok1)

# --- Layer 2 ---
def enc2(pt_hex):
    url = f"{HOST}/s2/enc?key={urllib.parse.quote(tok1)}&pt={pt_hex}"
    return urllib.request.urlopen(url, timeout=10).read().decode().strip()

ct2 = bytes.fromhex(get(f"/s2/ct?key={urllib.parse.quote(tok1)}"))
e0 = int(enc2("00"), 16)
e1 = int(enc2("01"), 16)
a2 = (e1 - e0) % 256
a2inv = pow(a2, -1, 256)
tok2 = bytes(((c - e0) * a2inv) % 256 for c in ct2).decode()
print("tok2:", tok2)

TOK2 = tok2

def enc3(pt_bytes):
    pt_hex = pt_bytes.hex()
    url = f"{HOST}/s3/enc?key={urllib.parse.quote(TOK2)}&pt={pt_hex}"
    return bytes.fromhex(urllib.request.urlopen(url, timeout=10).read().decode().strip())

ct_hex = get(f"/s3/ct?key={urllib.parse.quote(TOK2)}")
ct = bytes.fromhex(ct_hex)
print("ct len:", len(ct), "hex:", ct_hex)

# --- experiment 1: all zero block -> reveals B and parity of Perm ---
out0 = enc3(bytes(16))
print("out0:", out0.hex())
vals0 = set(out0)
print("distinct vals in out0:", vals0)
B = max(vals0)  # the nonzero one (assuming B != 0)
even_positions = [i for i in range(16) if out0[i] == B]
odd_positions = [i for i in range(16) if out0[i] == 0]
print("B=", B)
print("perm-even positions (output idx where Perm even):", even_positions)
print("perm-odd positions:", odd_positions)

# --- experiment 2: x0=1, rest 0 -> reveals A via V at an even-parity output position ---
pt2 = bytearray(16)
pt2[0] = 1
out1 = enc3(bytes(pt2))
print("out1:", out1.hex())
# pick any even_position, out1[i] should equal V = (A*1+B) mod 256
i0 = even_positions[0]
V = out1[i0]
A = (V - B) % 256
print("A=", A, "B=", B)

# sanity check with another even position and an odd position
for i in even_positions[:3]:
    assert out1[i] == V, f"mismatch at {i}"
for i in odd_positions[:3]:
    assert out1[i] == (V ^ B), f"mismatch odd at {i}"
print("A,B sanity check passed")

# --- experiment 3: distinct x[i] = i -> recover full Perm ---
pt3 = bytes(range(16))
y3 = [(A * x + B) % 256 for x in pt3]
z3 = [0] * 16
z3[0] = y3[0]
for i in range(1, 16):
    z3[i] = z3[i-1] ^ y3[i]
print("z3:", z3, "distinct:", len(set(z3)))

out3 = enc3(pt3)
print("out3:", out3.hex())

perm = [None] * 16
for i in range(16):
    val = out3[i]
    matches = [j for j in range(16) if z3[j] == val]
    perm[i] = matches
print("perm candidates:", perm)

# if unique matches, finalize
Perm = [m[0] for m in perm]
print("Perm:", Perm)

# --- now decrypt the actual ct token, per 16-byte block ---
Ainv = pow(A, -1, 256)

def decrypt_block(block, Perm, A, B, Ainv):
    n = len(block)
    z = [0] * n
    for i, p in enumerate(Perm):
        if p < n:
            z[p] = block[i]
    y = [0] * n
    y[0] = z[0]
    for i in range(1, n):
        y[i] = z[i] ^ z[i-1]
    x = bytes(((yy - B) * Ainv) % 256 for yy in y)
    return x

# process ct in 16-byte blocks (last block may be shorter)
pt_out = bytearray()
for start in range(0, len(ct), 16):
    block = ct[start:start+16]
    if len(block) == 16:
        pt_out += decrypt_block(block, Perm, A, B, Ainv)
    else:
        # partial last block - try truncated Perm/logic
        print("partial block len", len(block), "at", start)
        pt_out += block  # placeholder

print("decrypted:", bytes(pt_out))
