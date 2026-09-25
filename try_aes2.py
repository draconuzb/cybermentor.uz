import hashlib
import re
from Crypto.Cipher import AES, ChaCha20_Poly1305, ChaCha20, Salsa20

h = "25ce410e82301085e1ab90aea558c0a06e4d3c81fb6668a750850e4e1b1243b8bba96edfff2dde26a24f28ae859861846982d2210f10a03c76e25008a6e9572d1197114324cef3c2b4fae829a0d5fd27838466d4deeab65575168660d118ec423ea40c2ae386cae2ea0dca67a4905144c39874a0ff85dbe3beb141dd5f6c0de07ac4c635e7164fa6863dfbf99d92ee995ec8d9aba354adeca412fb17"
blob = bytes.fromhex(h)

password = b"F3rg0na_M3sh_0TA_k3y"
username = b"tech_provision"
clientid = b"thermostat-batch7-node"

key_material = {
    "sha256(pw)": hashlib.sha256(password).digest(),
    "sha256(user+pw)": hashlib.sha256(username + password).digest(),
    "sha256(pw+user)": hashlib.sha256(password + username).digest(),
    "sha256(client+pw)": hashlib.sha256(clientid + password).digest(),
    "sha256(pw+client)": hashlib.sha256(password + clientid).digest(),
    "md5(pw)": hashlib.md5(password).digest(),
    "md5(user+pw)": hashlib.md5(username + password).digest(),
    "sha1(pw)_16": hashlib.sha1(password).digest()[:16],
    "raw_pw_32": (password + b"\x00" * 32)[:32],
    "raw_pw_16": (password + b"\x00" * 16)[:16],
}

def check(pt, label):
    if re.search(rb"CTF\{", pt):
        print("MATCH", label, pt)
        return True
    printable = sum(1 for b in pt if 32 <= b < 127)
    if printable > len(pt) * 0.85:
        print("CANDIDATE(ascii)", label, pt)
    return False

found = False

for klabel, key in key_material.items():
    if len(key) not in (16, 24, 32):
        continue
    # GCM variants: nonce first12/last12, tag last16/first16
    variants = [
        ("nonce_first12_tag_last16", blob[:12], blob[12:-16], blob[-16:]),
        ("nonce_last12_tag_first16", blob[-12:], blob[16:-12], blob[:16]),
    ]
    for vlabel, nonce, ct, tag in variants:
        try:
            c = AES.new(key, AES.MODE_GCM, nonce=nonce)
            pt = c.decrypt_and_verify(ct, tag)
            if check(pt, f"AES-GCM {klabel} {vlabel}"):
                found = True
        except Exception:
            pass
    # ChaCha20-Poly1305: nonce 12, tag 16 (needs 32-byte key)
    if len(key) == 32:
        for vlabel, nonce, ct, tag in variants:
            try:
                c = ChaCha20_Poly1305.new(key=key, nonce=nonce)
                pt = c.decrypt_and_verify(ct, tag)
                if check(pt, f"ChaCha20Poly1305 {klabel} {vlabel}"):
                    found = True
            except Exception:
                pass
    # AES-CTR with 16-byte IV prefix (no auth tag)
    if len(blob) > 16:
        iv = blob[:16]
        rest = blob[16:]
        try:
            from Crypto.Util import Counter
            ctr = Counter.new(128, initial_value=int.from_bytes(iv, "big"))
            c = AES.new(key, AES.MODE_CTR, counter=ctr)
            pt = c.decrypt(rest)
            check(pt, f"AES-CTR-iv16 {klabel}")
        except Exception:
            pass
        # also plain rest without IV split - CTR with zero IV over whole blob
        try:
            c = AES.new(key, AES.MODE_CTR, nonce=b"")
            pt = c.decrypt(blob)
            check(pt, f"AES-CTR-noiv {klabel}")
        except Exception:
            pass

# ChaCha20 stream (no poly, 32-byte key, 8 or 12-byte nonce) over whole blob variants
for klabel, key in key_material.items():
    if len(key) != 32:
        continue
    for nlen in (8, 12):
        nonce = blob[:nlen]
        ct = blob[nlen:]
        try:
            c = ChaCha20.new(key=key, nonce=nonce)
            pt = c.decrypt(ct)
            check(pt, f"ChaCha20-stream n{nlen} {klabel}")
        except Exception:
            pass

if not found:
    print("no confirmed CTF{ match found in this batch")
