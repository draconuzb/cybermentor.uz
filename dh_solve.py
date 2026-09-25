import json

data = json.loads(open('/tmp/vpn_export.json').read())
s1 = data["session1"]

p = int(s1["p"], 16)
g = int(s1["g"])
A = int(s1["our_public"], 16)
B = int(s1["peer_public"], 16)
nonce = bytes.fromhex(s1["payload_nonce"])
ct = bytes.fromhex(s1["payload"])

print("p =", p, "bitlen =", p.bit_length())
print("g =", g)
print("A =", A)
print("B =", B)
print("nonce len =", len(nonce), "ct len =", len(ct))

# factor p-1 for Pohlig-Hellman feasibility check
from sympy import factorint, discrete_log

fac = factorint(p-1)
print("p-1 factorization:", fac)

# try to solve discrete log a such that g^a = A mod p
try:
    a = discrete_log(p, A, g)
    print("recovered private exponent a (for A) =", a)
    shared = pow(B, a, p)
    print("shared secret =", shared, hex(shared))
except Exception as e:
    print("discrete_log on A failed:", e)
    a = None

if a is None:
    try:
        b = discrete_log(p, B, g)
        print("recovered private exponent b (for B) =", b)
        shared = pow(A, b, p)
        print("shared secret =", shared, hex(shared))
    except Exception as e:
        print("discrete_log on B failed:", e)
