import urllib.request
import urllib.parse

HOST = "http://a98bf0cb-ab57-449c-bd24-be94755d533f.red.cyberkent.uz"

def get(path):
    return urllib.request.urlopen(f"{HOST}{path}", timeout=10).read().decode()

# --- Layer 1: repeating-key XOR, recover via zero-plaintext oracle ---
ct1_hex = get("/s1/ct").strip()
ct1 = bytes.fromhex(ct1_hex)
n1 = len(ct1)
zero_hex = "00" * n1
req = urllib.request.Request(f"{HOST}/s1/enc", data=f"pt={zero_hex}".encode(), method="POST",
                              headers={"Content-Type": "application/x-www-form-urlencoded"})
ks1 = bytes.fromhex(urllib.request.urlopen(req, timeout=10).read().decode().strip())
tok1 = bytes(c ^ k for c, k in zip(ct1, ks1))
print("tok1:", tok1)
KEY = tok1.decode()

# --- Layer 2: affine cipher, recover a,b via enc(0), enc(1) ---
def enc2(pt_hex):
    url = f"{HOST}/s2/enc?key={urllib.parse.quote(KEY)}&pt={pt_hex}"
    return urllib.request.urlopen(url, timeout=10).read().decode().strip()

ct2_hex = get(f"/s2/ct?key={urllib.parse.quote(KEY)}").strip()
ct2 = bytes.fromhex(ct2_hex)
print("s2 ct:", ct2_hex, "len:", len(ct2))

e0 = enc2("00")
e1 = enc2("01")
print("enc(0)=", e0, "enc(1)=", e1)
b = int(e0, 16)
a = (int(e1, 16) - b) % 256
print("a=", a, "b=", b)
ainv = pow(a, -1, 256)
tok2 = bytes(((c - b) * ainv) % 256 for c in ct2)
print("tok2:", tok2)
