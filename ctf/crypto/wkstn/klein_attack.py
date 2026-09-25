import json
import base64
import re
from collections import Counter

d = json.load(open("stage3.json"))
n = d["n"]
known_pt = base64.b64decode(d["known_plaintext_b64"])
print("known_pt:", known_pt.hex(), len(known_pt))
frames_raw = base64.b64decode(d["frames_b64"])
KEYLEN = d["keylen"]
RECLEN = 3 + 16
assert len(frames_raw) == n * RECLEN, (len(frames_raw), n * RECLEN)

frames = []
for i in range(n):
    rec = frames_raw[i*RECLEN:(i+1)*RECLEN]
    iv = rec[0:3]
    ct = rec[3:3+16]
    ks = bytes(c ^ p for c, p in zip(ct, known_pt))
    frames.append((iv, ks))

print("total frames:", len(frames))
import sys
SUBSET = int(sys.argv[1]) if len(sys.argv) > 1 else len(frames)
frames = frames[:SUBSET]
print("using subset:", len(frames))

def ksa_partial(key_bytes, rounds):
    S = list(range(256))
    j = 0
    keylen = len(key_bytes)
    for i in range(rounds):
        j = (j + S[i] + key_bytes[i % keylen]) % 256
        S[i], S[j] = S[j], S[i]
    return S, j

secret = []
for B in range(KEYLEN):
    A = 3 + B
    votes = Counter()
    for iv, ks in frames:
        ks0 = ks[0]
        full_known_key = list(iv) + secret
        S, j = ksa_partial(full_known_key, A)
        for guess in range(256):
            j2 = (j + S[A] + guess) % 256
            S2 = S.copy()
            S2[A], S2[j2] = S2[j2], S2[A]
            idx = (S2[1] + S2[S2[1]]) % 256
            pred = S2[idx]
            if pred == ks0:
                votes[guess] += 1
    top = votes.most_common(3)
    print(f"B={B} A={A} top={top}", flush=True)
    secret.append(top[0][0])

print("recovered secret:", bytes(secret).hex())

def rc4_keystream(key, nbytes):
    S = list(range(256))
    j = 0
    keylen = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % keylen]) % 256
        S[i], S[j] = S[j], S[i]
    out = bytearray()
    i = j = 0
    for _ in range(nbytes):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(S[(S[i] + S[j]) % 256])
    return bytes(out)

blob = base64.b64decode(d["blob_b64"])
prefix = base64.b64decode(d["blob_prefix_b64"])
print("prefix:", prefix)
ks = rc4_keystream(bytes(secret), len(blob))
pt = bytes(c ^ k for c, k in zip(blob, ks))
print("decrypted:", pt)
m = re.search(rb"CTF\{[^}]*\}", pt)
print("flag:", m.group(0) if m else None)
