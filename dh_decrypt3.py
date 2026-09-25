import json, hashlib, hmac
from sympy import discrete_log

data = json.loads(open('/tmp/vpn_export.json').read())
s1 = data["session1"]

p = int(s1["p"], 16)
g = int(s1["g"])
A = int(s1["our_public"], 16)
B = int(s1["peer_public"], 16)
nonce = bytes.fromhex(s1["payload_nonce"])
ct = bytes.fromhex(s1["payload"])

a = discrete_log(p, A, g)
b = discrete_log(p, B, g)
shared_from_a = pow(B, a, p)
shared_from_b = pow(A, b, p)
print("a=",a,"b=",b)
print("shared via a:", shared_from_a)
print("shared via b:", shared_from_b)
print("match:", shared_from_a == shared_from_b)

shared = shared_from_a
nbytes = (shared.bit_length()+7)//8
sb_be = shared.to_bytes(max(nbytes,1), "big")
print("shared bytes (be):", sb_be.hex())

def xor(a,b):
    return bytes(x^y for x,y in zip(a, (b*(len(a)//len(b)+1))[:len(a)]))

def try_stream(keystream, label):
    if len(keystream) < len(ct):
        return
    pt = xor(ct, keystream)
    printable = sum(1 for c in pt if 32 <= c < 127) / len(pt)
    if printable > 0.8 or b"CTF" in pt or b"ctf" in pt:
        print(f"[{label}] -> {pt}")

candidates = {
  "sha256(sb)": hashlib.sha256(sb_be).digest(),
  "sha256(sb+nonce)": hashlib.sha256(sb_be+nonce).digest(),
  "sha256(nonce+sb)": hashlib.sha256(nonce+sb_be).digest(),
  "sha512(sb)": hashlib.sha512(sb_be).digest(),
  "hmac(nonce,sb)": hmac.new(nonce, sb_be, hashlib.sha256).digest(),
  "hmac(sb,nonce)": hmac.new(sb_be, nonce, hashlib.sha256).digest(),
  "md5(sb)x3": hashlib.md5(sb_be).digest()*3,
  "sha256(str(shared))": hashlib.sha256(str(shared).encode()).digest(),
  "sha256(str(shared)+nonce.hex())": hashlib.sha256((str(shared)+nonce.hex()).encode()).digest(),
  "raw_shared_bytes_repeated": sb_be * 3,
}

for label, ks in candidates.items():
    try_stream(ks, label)

# also try plain "shared secret bytes directly ct XOR sb_be repeated" already covered above as raw
print("done. ct hex:", ct.hex())
