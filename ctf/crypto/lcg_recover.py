import json
import math
import re

d = json.load(open("generator_lcg.json"))
outputs = d["outputs"]
ct = bytes.fromhex(d["flag_ct_hex"])
print("num outputs:", len(outputs))
print("ct len:", len(ct))

diffs = [outputs[i+1] - outputs[i] for i in range(len(outputs) - 1)]

# compute candidate multiples of m
zeroes = [diffs[i+1]*diffs[i-1] - diffs[i]**2 for i in range(1, len(diffs) - 1)]

m = 0
for z in zeroes:
    m = math.gcd(m, abs(z))

print("recovered m:", m)

a = (diffs[1] * pow(diffs[0], -1, m)) % m
c = (outputs[1] - a * outputs[0]) % m
print("recovered a:", a)
print("recovered c:", c)

# verify
ok = True
for i in range(len(outputs) - 1):
    pred = (a * outputs[i] + c) % m
    if pred != outputs[i+1]:
        ok = False
        break
print("verification:", ok)

# generate next outputs after the last logged one
n_needed = (len(ct) + 5) // 6
state = outputs[-1]
keystream = b""
for _ in range(n_needed):
    state = (a * state + c) % m
    keystream += state.to_bytes(6, 'big')

keystream = keystream[:len(ct)]
flag = bytes(x ^ y for x, y in zip(ct, keystream))
print("flag:", flag)
m2 = re.search(rb"CTF\{[^}]*\}", flag)
print("match:", m2)
