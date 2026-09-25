import json
import base64
import re

with open("/home/ubuntu/ctf/crypto/wkstn/stage1.json") as f:
    d = json.load(f)

wordlist = d["wordlist"]
known_prefix = base64.b64decode(d["known_prefix_b64"])
ct = base64.b64decode(d["ciphertext_b64"])

print("known_prefix:", known_prefix)
print("ct len:", len(ct))

def rc4_keystream(key, n):
    S = list(range(256))
    j = 0
    keylen = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % keylen]) % 256
        S[i], S[j] = S[j], S[i]
    out = bytearray()
    i = j = 0
    for _ in range(n):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(S[(S[i] + S[j]) % 256])
    return bytes(out)

found = None
for w in wordlist:
    key = w.encode()
    ks = rc4_keystream(key, len(known_prefix))
    pt_prefix = bytes(c ^ k for c, k in zip(ct[:len(known_prefix)], ks))
    if pt_prefix == known_prefix:
        found = w
        break

print("found password:", found)

if found:
    ks = rc4_keystream(found.encode(), len(ct))
    pt = bytes(c ^ k for c, k in zip(ct, ks))
    print("full plaintext:", pt)
    m = re.search(rb"CTF\{[^}]*\}", pt)
    print("flag:", m.group(0) if m else None)
