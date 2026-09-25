import json, hashlib
from Crypto.Cipher import AES

data = json.loads(open('/tmp/vpn_export.json').read())
s1 = data["session1"]

shared = 1163866392143334801388988434493892403335622164933389768990993563980991954
nonce = bytes.fromhex(s1["payload_nonce"])
ct = bytes.fromhex(s1["payload"])

def shared_bytes(n):
    return shared.to_bytes(n, "big")

candidates_keys = []
for n in [16, 32]:
    sb = shared_bytes((shared.bit_length()+7)//8)
    candidates_keys.append(("raw-be-padded", shared.to_bytes(n, "big") if shared.bit_length() <= n*8 else None))
    candidates_keys.append(("sha256-full", hashlib.sha256(sb).digest()[:n]))
    candidates_keys.append(("sha256-str", hashlib.sha256(str(shared).encode()).digest()[:n]))
    candidates_keys.append(("md5x2", (hashlib.md5(sb).digest()*2)[:n]))

def try_all(key, label):
    if key is None:
        return
    results = []
    for mode_name, mode in [("CTR", None), ("CFB", AES.MODE_CFB), ("OFB", AES.MODE_OFB), ("GCM", AES.MODE_GCM)]:
        try:
            if mode_name == "CTR":
                from Crypto.Util import Counter
                ctr = Counter.new(128, initial_value=int.from_bytes(nonce, "big"))
                cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
                pt = cipher.decrypt(ct)
            elif mode_name == "GCM":
                if len(ct) <= 16:
                    continue
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce[:12])
                pt = cipher.decrypt(ct[:-16])
            else:
                cipher = AES.new(key, mode, iv=nonce)
                pt = cipher.decrypt(ct)
        except Exception as e:
            continue
        printable = all(32 <= b < 127 for b in pt)
        if printable or b"CTF" in pt or b"ctf" in pt:
            print(f"[{label} keylen={len(key)*8} mode={mode_name}] -> {pt}")

for label, key in candidates_keys:
    try_all(key, label)

print("done")
