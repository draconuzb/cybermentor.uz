import re
import itertools

X = 12
Y = 34
MARGIN = 2
TOKEN_WIDTH = 8

rle = """12b$3bo4b2o2b$2bob2o4bob$2bo2bo6b$2bo2bo2bo3b$2b2o4bobob$2b2o8b$2b3obo2b2ob$2b4o2bobob$2b5o2bo2b$2bobob2o2bob$2bobo4bo2b$3b3ob2o3b$3b3o3b2ob$3b3obo2bob$3b2o3bo3b$3b3o3bo2b$3b4ob2o2b$4bobo3bob$2b6o4b$2bobo2bo4b$4bobo3bob$2bobob3o3b$3b4o5b$4bob3o3b$2bobob3o3b$3b3obo2bob$4bo2b3o2b$2bobob3o3b$3b3obob2ob$4b7ob$2bob3o2b2ob$12b$12b!"""

# parse RLE into grid Y x X
grid = [[0] * X for _ in range(Y)]
row = 0
col = 0
num = ""
for ch in rle:
    if ch.isdigit():
        num += ch
    elif ch in "bo":
        n = int(num) if num else 1
        num = ""
        val = 1 if ch == "o" else 0
        for _ in range(n):
            if col < X:
                grid[row][col] = val
            col += 1
    elif ch == "$":
        n = int(num) if num else 1
        num = ""
        row += n
        col = 0
    elif ch == "!":
        break

print("parsed grid rows:", len(grid), "cols:", len(grid[0]))
for r in grid:
    print("".join(str(v) for v in r))

def idx(r, c):
    return r * X + c

N = X * Y
final_vec = [0] * N
for r in range(Y):
    for c in range(X):
        final_vec[idx(r, c)] = grid[r][c]

NEIGHBORS = {
    "C": (0, 0),
    "N": (-1, 0),
    "S": (1, 0),
    "W": (0, -1),
    "E": (0, 1),
}
names = list(NEIGHBORS.keys())

def build_matrix(taps):
    # M rows as bitmask ints, M[i] has bit j set if cell j contributes to new cell i
    M = [0] * N
    for r in range(Y):
        for c in range(X):
            i = idx(r, c)
            rowmask = 0
            for t in taps:
                dr, dc = NEIGHBORS[t]
                rr, cc = r + dr, c + dc
                if 0 <= rr < Y and 0 <= cc < X:
                    rowmask |= (1 << idx(rr, cc))
            M[i] = rowmask
    return M

def solve(M, rhs):
    # augmented rows
    aug = [[M[i], rhs[i]] for i in range(N)]
    rank = 0
    pivot_col = {}
    for col_ in range(N):
        piv = None
        for r in range(rank, N):
            if (aug[r][0] >> col_) & 1:
                piv = r
                break
        if piv is None:
            continue
        aug[rank], aug[piv] = aug[piv], aug[rank]
        for r in range(N):
            if r != rank and ((aug[r][0] >> col_) & 1):
                aug[r][0] ^= aug[rank][0]
                aug[r][1] ^= aug[rank][1]
        pivot_col[rank] = col_
        rank += 1
        if rank == N:
            break
    # check consistency
    for r in range(rank, N):
        if aug[r][0] == 0 and aug[r][1] != 0:
            return None, rank
    sol = [0] * N
    for r in range(rank):
        sol[pivot_col[r]] = aug[r][1]
    return sol, rank

best = None
for k in range(1, 6):
    for taps in itertools.combinations(names, k):
        M = build_matrix(taps)
        sol, rank = solve(M, final_vec)
        if sol is None:
            continue
        if rank < N:
            continue  # need unique solution for now
        # extract interior
        bits = []
        for r in range(MARGIN, Y - MARGIN):
            for c in range(MARGIN, MARGIN + TOKEN_WIDTH):
                bits.append(sol[idx(r, c)])
        # pack bits MSB-first per byte, per row (8 bits/row = 1 byte/row)
        out = bytearray()
        for i in range(0, len(bits), 8):
            byte = 0
            for b in bits[i:i+8]:
                byte = (byte << 1) | b
            out.append(byte)
        m = re.search(rb"CTF\{[^}]*\}", bytes(out))
        if m:
            print("TAPS:", taps, "-> FLAG:", m.group(0))
            best = (taps, out)
        else:
            printable = sum(1 for b in out if 32 <= b < 127)
            if printable > len(out) * 0.6:
                print("TAPS:", taps, "rank", rank, "candidate:", bytes(out))

if not best:
    print("No exact-rank solution with flag found; trying underdetermined cases too")
