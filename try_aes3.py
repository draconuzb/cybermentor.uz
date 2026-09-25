import hashlib
import re
from Crypto.Cipher import AES, ChaCha20_Poly1305

h = "25ce410e82301085e1ab90aea558c0a06e4d3c81fb6668a750850e4e1b1243b8bba96edfff2dde26a24f28ae859861846982d2210f10a03c76e25008a6e9572d1197114324cef3c2b4fae829a0d5fd27838466d4deeab65575168660d118ec423ea40c2ae386cae2ea0dca67a4905144c39874a0ff85dbe3beb141dd5f6c0de07ac4c635e7164fa6863dfbf99d92ee995ec8d9aba354adeca412fb17"
blob = bytes.fromhex(h)
print("len", len(blob))

password = b"F3rg0na_M3sh_0TA_k3y"

keys = {
    "sha256": hashlib.sha256(password).digest(),
    "sha512_32": hashlib.sha512(password).digest()[:32],
    "sha512_16": hashlib.sha512(password).digest()[:16],
    "md5": hashlib.md5(password).digest(),
    "raw24": (password + b"\x00"*24)[:24],
    "raw32": (password + b"\x00"*32)[:32],
    "raw16": (password + b"\x00"*16)[:16],
    "sha256_of_sha256": hashlib.sha256(hashlib.sha256(password).digest()).digest(),
}

found = False
for klabel, key in keys.items():
    if len(key) not in (16, 24, 32):
        continue
    for nlen in (7, 8, 11, 12, 13, 16):
        for tagpos in ("end", "start"):
            if tagpos == "end":
                nonce = blob[:nlen]
                ct = blob[nlen:-16]
                tag = blob[-16:]
            else:
                tag = blob[:16]
                nonce = blob[16:16+nlen]
                ct = blob[16+nlen:]
            if len(ct) <= 0:
                continue
            try:
                c = AES.new(key, AES.MODE_GCM, nonce=nonce)
                pt = c.decrypt_and_verify(ct, tag)
                print("AES-GCM MATCH", klabel, nlen, tagpos, pt)
                found = True
            except Exception:
                pass
            if len(key) == 32:
                try:
                    c = ChaCha20_Poly1305.new(key=key, nonce=nonce[:12] if nlen>=12 else nonce.ljust(12,b'\x00'))
                    pt = c.decrypt_and_verify(ct, tag)
                    print("ChaCha20Poly1305 MATCH", klabel, nlen, tagpos, pt)
                    found = True
                except Exception:
                    pass

if not found:
    print("still no GCM/ChaChaPoly match")
