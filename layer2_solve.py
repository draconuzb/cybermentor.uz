import urllib.request
import urllib.parse

HOST = "http://a98bf0cb-ab57-449c-bd24-be94755d533f.red.cyberkent.uz"
KEY = "CTF{bac_b134d89fb6306c5494ee}"

def get(path):
    url = f"{HOST}{path}"
    return urllib.request.urlopen(url, timeout=10).read().decode()

def enc(pt_hex):
    url = f"{HOST}/s2/enc?key={urllib.parse.quote(KEY)}&pt={pt_hex}"
    return urllib.request.urlopen(url, timeout=10).read().decode().strip()

ct_hex = get(f"/s2/ct?key={urllib.parse.quote(KEY)}").strip()
print("s2 ct:", ct_hex)
ct = bytes.fromhex(ct_hex)
print("len:", len(ct))

e0 = enc("00")
e1 = enc("01")
print("enc(0)=", e0, "enc(1)=", e1)

b = int(e0, 16)
a = (int(e1, 16) - b) % 256
print("a=", a, "b=", b)

ainv = pow(a, -1, 256)
pt = bytes(((c - b) * ainv) % 256 for c in ct)
print("token:", pt)
