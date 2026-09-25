import json
import base64
import re
import time
from collections import Counter

d = json.load(open("stage3.json"))
n = d["n"]
known_pt = base64.b64decode(d["known_plaintext_b64"])
frames_raw = base64.b64decode(d["frames_b64"])
KEYLEN = d["keylen"]
RECLEN = 3 + 16

ALL_FRAMES = []
for i in range(n):
    rec = frames_raw[i*RECLEN:(i+1)*RECLEN]
    iv = rec[0:3]
    ct0 = rec[3]
    ks0 = ct0 ^ known_pt[0]
    ALL_FRAMES.append((iv[0], iv[1], iv[2], ks0))

N_USE = 30000
frames = ALL_FRAMES[:N_USE]
print("using", len(frames), "frames", flush=True)

def ksa_partial(key_bytes, rounds):
    S = list(range(256))
    j = 0
    keylen = len(key_bytes)
    for i in range(rounds):
        j = (j + S[i] + key_bytes[i % keylen]) % 256
        S[i], S[j] = S[j], S[i]
    return S, j

def vote_for_byte(prefix, A, frames):
    votes = [0] * 256
    keylen = 3 + len(prefix)
    for iv0, iv1, iv2, ks0 in frames:
        full_key = (iv0, iv1, iv2) + tuple(prefix)
        S, j = ksa_partial(full_key, A)
        SA = S[A]
        S1 = S[1]
        SS1 = S[S1]
        for guess in range(256):
            j2 = (j + SA + guess) % 256
            if A == 1:
                v1 = guess
            elif j2 == 1:
                v1 = SA
            else:
                v1 = S1
            idx2 = v1
            if idx2 == A:
                v2 = guess
            elif idx2 == j2:
                v2 = SA
            else:
                v2 = S[idx2]
            outidx = (v1 + v2) % 256
            if outidx == A:
                pred = guess
            elif outidx == j2:
                pred = SA
            else:
                pred = S[outidx]
            if pred == ks0:
                votes[guess] += 1
    return votes

BEAM_WIDTH = 12
TOPK_PER_NODE = 6

beam = [((), 0)]
t0 = time.time()
for B in range(KEYLEN):
    A = 3 + B
    new_candidates = []
    for prefix, score in beam:
        votes = vote_for_byte(prefix, A, frames)
        ranked = sorted(range(256), key=lambda g: -votes[g])[:TOPK_PER_NODE]
        for g in ranked:
            new_candidates.append((prefix + (g,), score + votes[g]))
    new_candidates.sort(key=lambda x: -x[1])
    beam = new_candidates[:BEAM_WIDTH]
    print(f"B={B} A={A} elapsed={time.time()-t0:.1f}s top_score={beam[0][1]} beam_size={len(beam)}", flush=True)
    print("  best prefix so far:", bytes(beam[0][0]).hex(), flush=True)

print("FINAL BEAM (top 5):", flush=True)
for prefix, score in beam[:5]:
    print(" ", bytes(prefix).hex(), score, flush=True)

# verify against blob_prefix
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
prefix_known = base64.b64decode(d["blob_prefix_b64"])
print("blob_prefix:", prefix_known, flush=True)

found_key = None
for prefix, score in beam:
    key = bytes(prefix)
    ks = rc4_keystream(key, len(prefix_known))
    pt = bytes(c ^ k for c, k in zip(blob[:len(prefix_known)], ks))
    if pt == prefix_known:
        found_key = key
        break

if found_key:
    print("FOUND CORRECT KEY:", found_key.hex(), flush=True)
    ks = rc4_keystream(found_key, len(blob))
    full_pt = bytes(c ^ k for c, k in zip(blob, ks))
    print("decrypted:", full_pt, flush=True)
    m = re.search(rb"CTF\{[^}]*\}", full_pt)
    print("flag:", m.group(0) if m else None, flush=True)
else:
    print("NO beam candidate matched blob_prefix", flush=True)
