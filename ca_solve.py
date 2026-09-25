import re

with open('/tmp/stream1.txt') as f:
    data = f.read()

ks_str = re.search(r'keystream_bits:\s*([01]+)', data).group(1)
mask_offset = int(re.search(r'mask_offset:\s*(\d+)', data).group(1))
ct_hex = re.search(r'ciphertext_hex:\s*([0-9a-fA-F]+)', data).group(1)

bits = [int(c) for c in ks_str]
print("len(keystream_bits) =", len(bits), "mask_offset =", mask_offset)

def berlekamp_massey(s):
    n = len(s)
    c = [1] + [0]*n
    b = [1] + [0]*n
    L, m = 0, 1
    for N in range(n):
        d = s[N]
        for i in range(1, L+1):
            d ^= c[i] & s[N-i]
        if d == 0:
            m += 1
        elif 2*L <= N:
            t = c[:]
            for i in range(len(b)):
                if i+m < len(c):
                    c[i+m] ^= b[i]
            L = N+1-L
            b = t
            m = 1
        else:
            for i in range(len(b)):
                if i+m < len(c):
                    c[i+m] ^= b[i]
            m += 1
    return c[:L+1], L

c, L = berlekamp_massey(bits)
print("linear complexity L =", L)
print("connection poly c =", c)

# extend sequence
seq = bits[:]
ct_bits_needed = len(ct_hex) * 4
target_len = mask_offset + ct_bits_needed
while len(seq) < target_len:
    N = len(seq)
    d = 0
    for i in range(1, L+1):
        d ^= c[i] & seq[N-i]
    seq.append(d)

ks_for_ct = seq[mask_offset:mask_offset+ct_bits_needed]

ct_bytes = bytes.fromhex(ct_hex)
ct_bits = []
for byte in ct_bytes:
    for i in range(7, -1, -1):
        ct_bits.append((byte >> i) & 1)

pt_bits = [c ^ k for c, k in zip(ct_bits, ks_for_ct)]
pt_bytes = bytearray()
for i in range(0, len(pt_bits), 8):
    byte = 0
    for b in pt_bits[i:i+8]:
        byte = (byte << 1) | b
    pt_bytes.append(byte)

print("plaintext bytes:", bytes(pt_bytes))
try:
    print("plaintext ascii:", bytes(pt_bytes).decode('utf-8', errors='replace'))
except Exception as e:
    print("decode err", e)
