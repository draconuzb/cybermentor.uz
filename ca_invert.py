import re

WIDTH = 232
GENERATIONS = 12
TAPS = [-2, -1, 0]
FINAL_HEX = "4765332eb2d3b96892e49b76745066672ae1c2d794b49e11350717070a"

final_bytes = bytes.fromhex(FINAL_HEX)
print("final_bytes len (bits):", len(final_bytes) * 8, "expected width:", WIDTH)

# bit j (0..WIDTH-1) corresponds to array index j, MSB-first per byte per spec
def bytes_to_bits(b, width):
    bits = []
    for byte in b:
        for k in range(7, -1, -1):
            bits.append((byte >> k) & 1)
    return bits[:width]

def bits_to_bytes(bits):
    # pad to full bytes, MSB-first
    n = len(bits)
    pad = (-n) % 8
    bits2 = bits + [0] * pad
    out = bytearray()
    for i in range(0, len(bits2), 8):
        v = 0
        for k in range(8):
            v = (v << 1) | bits2[i + k]
        out.append(v)
    return bytes(out)

final_bits = bytes_to_bits(final_bytes, WIDTH)
print("final_bits len:", len(final_bits))

# Build one-step matrix M as list of row-bitmasks (bit j set => M[i][j]=1)
M_rows = []
for i in range(WIDTH):
    row = 0
    for d in TAPS:
        j = i + d
        if 0 <= j < WIDTH:
            row |= (1 << j)
    M_rows.append(row)

def mat_mult(A_rows, B_rows, width):
    # (A*B)[i] row = XOR over k where A[i] has bit k set, of B_rows[k]
    C_rows = []
    for i in range(width):
        a = A_rows[i]
        c = 0
        k = 0
        aa = a
        while aa:
            if aa & 1:
                c ^= B_rows[k]
            aa >>= 1
            k += 1
        C_rows.append(c)
    return C_rows

# compute M^GENERATIONS via repeated multiplication
Mp = M_rows
result = None
# identity matrix
I_rows = [1 << i for i in range(WIDTH)]
P = I_rows
base = M_rows
e = GENERATIONS
while e > 0:
    if e & 1:
        P = mat_mult(P, base, WIDTH)
    base = mat_mult(base, base, WIDTH)
    e >>= 1

Mn_rows = P  # M^GENERATIONS

# Now solve Mn_rows @ seed = final_bits (over GF2) for seed, via Gaussian elimination
# Build augmented matrix: rows as (row_bitmask, rhs_bit)
aug = []
for i in range(WIDTH):
    aug.append([Mn_rows[i], final_bits[i]])

# Gaussian elimination over GF(2)
rank = 0
pivot_col_for_row = {}
for col in range(WIDTH):
    pivot_row = None
    for r in range(rank, WIDTH):
        if (aug[r][0] >> col) & 1:
            pivot_row = r
            break
    if pivot_row is None:
        continue
    aug[rank], aug[pivot_row] = aug[pivot_row], aug[rank]
    for r in range(WIDTH):
        if r != rank and ((aug[r][0] >> col) & 1):
            aug[r][0] ^= aug[rank][0]
            aug[r][1] ^= aug[rank][1]
    pivot_col_for_row[rank] = col
    rank += 1
    if rank == WIDTH:
        break

print("rank:", rank, "of", WIDTH)

# check consistency for rows beyond rank
consistent = True
for r in range(rank, WIDTH):
    if aug[r][0] == 0 and aug[r][1] != 0:
        consistent = False
print("consistent:", consistent)

seed = [0] * WIDTH
for r in range(rank):
    col = pivot_col_for_row[r]
    seed[col] = aug[r][1]

seed_bytes = bits_to_bytes(seed)
print("seed_bytes:", seed_bytes)

m = re.search(rb"CTF\{[^}]*\}", seed_bytes)
print("flag:", m.group(0) if m else None)
