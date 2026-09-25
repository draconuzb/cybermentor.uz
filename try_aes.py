import hashlib
import re
from Crypto.Cipher import AES

h = "25ce410e82301085e1ab90aea558c0a06e4d3c81fb6668a750850e4e1b1243b8bba96edfff2dde26a24f28ae859861846982d2210f10a03c76e25008a6e9572d1197114324cef3c2b4fae829a0d5fd27838466d4deeab65575168660d118ec423ea40c2ae386cae2ea0dca67a4905144c39874a0ff85dbe3beb141dd5f6c0de07ac4c635e7164fa6863dfbf99d92ee995ec8d9aba354adeca412fb17"
blob = bytes.fromhex(h)
print("blob len:", len(blob))

passphrase = b"F3rg0na_M3sh_0TA_k3y"

candidates_keys = {
    "sha256": hashlib.sha256(passphrase).digest(),
    "md5": hashlib.md5(passphrase).digest(),
    "raw_padded32": (passphrase + b"\x00"*32)[:32],
    "raw_padded16": (passphrase + b"\x00"*16)[:16],
    "sha1_16": hashlib.sha1(passphrase).digest()[:16],
}

nonce = blob[:12]
ct = blob[12:-16]
tag = blob[-16:]
print("nonce len", len(nonce), "ct len", len(ct), "tag len", len(tag))

for name, key in candidates_keys.items():
    try:
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        pt = cipher.decrypt_and_verify(ct, tag)
        print(f"[{name}] SUCCESS:", pt)
    except Exception as e:
        pass

# also try IV=16 bytes variants for CBC even if not perfectly aligned, and CTR mode
for name, key in candidates_keys.items():
    if len(key) not in (16, 24, 32):
        continue
    try:
        iv = blob[:16]
        rest = blob[16:]
        cipher = AES.new(key, AES.MODE_CTR, nonce=b"", initial_value=iv)
    except Exception:
        pass

print("done trying GCM; now trying CBC/CTR with 16-byte IV prefix")
for name, key in candidates_keys.items():
    if len(key) not in (16, 24, 32):
        continue
    iv = blob[:16]
    rest = blob[16:]
    if len(rest) % 16 == 0:
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = cipher.decrypt(rest)
            if re.search(rb"CTF\{", pt):
                print(f"[{name} CBC] SUCCESS:", pt)
        except Exception:
            pass
    # CTR doesn't need alignment
    try:
        from Crypto.Util import Counter
        ctr = Counter.new(128, initial_value=int.from_bytes(iv, 'big'))
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        pt = cipher.decrypt(rest)
        if re.search(rb"CTF\{", pt) or sum(32 <= b < 127 for b in pt) > len(pt)*0.8:
            print(f"[{name} CTR iv16] candidate:", pt)
    except Exception as e:
        pass
