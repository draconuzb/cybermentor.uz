import urllib.request

ct_hex = "3cf93a079281a220cf4d4fc484f946cb1e4ac3d0f71c984845c485a402"
ct = bytes.fromhex(ct_hex)
n = len(ct)
print("token ct length:", n)

zero_hex = "00" * n
url = "http://f903813e-ffba-4893-b477-3fcc094e2046.red.cyberkent.uz/s1/enc"
req = urllib.request.Request(url, data=f"pt={zero_hex}".encode(), method="POST",
                              headers={"Content-Type": "application/x-www-form-urlencoded"})
resp = urllib.request.urlopen(req, timeout=10).read().decode()
print("enc(zero) response:", resp)

keystream = bytes.fromhex(resp.strip())
print("keystream len:", len(keystream))

pt = bytes(c ^ k for c, k in zip(ct, keystream))
print("token plaintext:", pt)
