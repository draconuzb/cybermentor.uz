import itertools

ct = bytes.fromhex("6e180367acb27c0e679840649a2b6ffed82f43522e57c7c848c78653d1f4d9c3")
A = 123
B = 15
Ainv = pow(A, -1, 256)

# ambiguous pairs: output positions -> two candidate z-indices
ambiguous = [
    ([0, 4], [7, 11]),
    ([5, 6], [3, 15]),
    ([2, 9], [5, 13]),
]

base_perm = {1: 8, 3: 6, 7: 14, 8: 4, 10: 0, 11: 9, 12: 2, 13: 1, 14: 12, 15: 10}

def decrypt_block(block, Perm):
    n = len(block)
    z = [0] * n
    for i in range(n):
        z[Perm[i]] = block[i]
    y = [0] * n
    y[0] = z[0]
    for i in range(1, n):
        y[i] = z[i] ^ z[i-1]
    return bytes(((yy - B) * Ainv) % 256 for yy in y)

best = None
for assign in itertools.product([0, 1], repeat=3):
    perm = dict(base_perm)
    for (outs, zs), a in zip(ambiguous, assign):
        perm[outs[0]] = zs[a]
        perm[outs[1]] = zs[1 - a]
    Perm = [perm[i] for i in range(16)]
    if sorted(Perm) != list(range(16)):
        continue
    out = b""
    for start in range(0, len(ct), 16):
        blk = ct[start:start+16]
        if len(blk) == 16:
            out += decrypt_block(blk, Perm)
        else:
            out += blk
    print(assign, Perm, "->", out)
