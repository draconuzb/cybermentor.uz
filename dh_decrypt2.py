import json, hashlib, hmac, itertools
from Crypto.Cipher import AES
from Crypto.Util import Counter

data = json.loads(open('/tmp/vpn_export.json').read())
s1 = data["session1"]

shared = 1163866392143334801388988434493892403335622164933389768990993563980991954
nonce = bytes.fromhex(s1["payload_nonce"])
ct = bytes.fromhex(s1["payload"])
CTX = b"vpn-key-confirmation-v1"

def be(n):
    return shared.to_bytes(n, "big")
def le(n):
    return shared.to_bytes(n, "little")

nbytes = (shared.bit_length()+7)//8

key_candidates = {}
key_candidates["sha256(be_min)"] = hashlib.sha256(be(nbytes)).digest()
key_candidates["sha256(be_min+ctx)"] = hashlib.sha256(be(nbytes)+CTX).digest()
key_candidates["sha256(ctx+be_min)"] = hashlib.sha256(CTX+be(nbytes)).digest()
key_candidates["hmac(ctx,be_min)"] = hmac.new(CTX, be(nbytes), hashlib.sha256).digest()
key_candidates["hmac(be_min,ctx)"] = hmac.new(be(nbytes), CTX, hashlib.sha256).digest()
key_candidates["sha256(le_min)"] = hashlib.sha256(le(nbytes)).digest()
key_candidates["sha256(be_min+ctx)_16"] = hashlib.sha256(be(nbytes)+CTX).digest()[:16]
key_candidates["md5(be_min)"] = hashlib.md5(be(nbytes)).digest()
key_candidates["sha1(be_min)[:16]"] = hashlib.sha1(be(nbytes)).digest()[:16]
key_candidates["sha1(be_min)[:32pad]"] = (hashlib.sha1(be(nbytes)).digest()+b"\x00"*12)
key_candidates["str(shared)_sha256"] = hashlib.sha256(str(shared).encode()).digest()
key_candidates["hex(shared)_sha256"] = hashlib.sha256(format(shared,'x').encode()).digest()

def attempts(key, label):
    out = []
    try:
        ctr = Counter.new(128, initial_value=int.from_bytes(nonce, "big"))
        pt = AES.new(key, AES.MODE_CTR, counter=ctr).decrypt(ct)
        out.append(("CTR", pt))
    except Exception: pass
    try:
        pt = AES.new(key, AES.MODE_CFB, iv=nonce).decrypt(ct)
        out.append(("CFB", pt))
    except Exception: pass
    try:
        pt = AES.new(key, AES.MODE_OFB, iv=nonce).decrypt(ct)
        out.append(("OFB", pt))
    except Exception: pass
    if len(ct) > 16:
        for nl in (16, 12):
            try:
                cipher = AES.new(key, AES.MODE_GCM, nonce=nonce[:nl])
                pt = cipher.decrypt(ct[:-16])
                out.append((f"GCM-noncelen{nl}", pt))
            except Exception: pass
    for mode_name, mode in out:
        printable = sum(1 for b in mode if 32 <= b < 127) / max(1,len(mode))
        if printable > 0.85 or b"CTF" in mode or b"ctf" in mode:
            print(f"[{label} keylen={len(key)} mode={mode_name}] -> {mode}")

for label, key in key_candidates.items():
    for kl in (16, 24, 32):
        k = key[:kl] if len(key) >= kl else None
        if k:
            attempts(k, f"{label}[:{kl}]")

print("done")
