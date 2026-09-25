import json
import base64
import re
from collections import Counter

d = json.load(open("stage2.json"))
n = d["n"]
known_pt0 = d["known_plaintext_first_byte"]
frames_raw = base64.b64decode(d["frames_b64"])
assert len(frames_raw) == n * 4, (len(frames_raw), n * 4)

frames = []
for i in range(n):
    rec = frames_raw[i*4:(i+1)*4]
    iv = rec[0:3]
    ct0 = rec[3]
    ks0 = ct0 ^ known_pt0
    frames.append((iv, ks0))

print("total frames:", len(frames))
print("sample:", frames[:5])

from collections import Counter as _C
iv0_counts = _C(f[0][0] for f in frames)
iv1_counts = _C(f[0][1] for f in frames)
print("iv0 distribution:", sorted(iv0_counts.items())[:20])
print("iv1 distribution (top 5):", iv1_counts.most_common(5))

KEYLEN = d["keylen"]  # 5
secret = []

def ksa_partial(key_bytes, rounds):
    S = list(range(256))
    j = 0
    keylen = len(key_bytes)
    for i in range(rounds):
        j = (j + S[i] + key_bytes[i % keylen]) % 256
        S[i], S[j] = S[j], S[i]
    return S, j

for B in range(KEYLEN):
    A = 3 + B  # absolute key index being solved
    votes = Counter()
    used = 0
    checked = 0
    debug_printed = 0
    for iv, ks0 in frames:
        # weak IV condition: iv[0] == A+3, iv[1] == 255
        if iv[0] != A or iv[1] != 255:
            continue
        checked += 1
        full_known_key = list(iv) + secret  # length A (3 + B known secret bytes)
        S, j = ksa_partial(full_known_key, A)  # simulate rounds 0..A-1
        used += 1
        for guess in range(256):
            j2 = (j + S[A] + guess) % 256
            S2 = S.copy()
            S2[A], S2[j2] = S2[j2], S2[A]
            # predicted output using standard RC4 first-output formula on S2 as if final
            idx = (S2[1] + S2[S2[1]]) % 256
            pred = S2[idx]
            if pred == ks0:
                votes[guess] += 1
    if votes:
        best = votes.most_common(3)
        print(f"B={B} A={A} used_frames={used} top_votes={best}")
        secret.append(best[0][0])
    else:
        print(f"B={B} A={A} used_frames={used} NO VOTES")
        secret.append(0)

print("recovered secret:", bytes(secret))

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
print("decrypted blob:", pt)
m = re.search(rb"CTF\{[^}]*\}", pt)
print("flag:", m.group(0) if m else None)
