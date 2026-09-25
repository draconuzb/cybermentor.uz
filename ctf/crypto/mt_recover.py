import json
import re

d = json.load(open("generator_mt.json"))
outputs = d["outputs"]
ct = bytes.fromhex(d["flag_ct_hex"])
print("num outputs:", len(outputs), "ct len:", len(ct))

def undo_right(z, shift):
    result = z
    for _ in range((32 // shift) + 1):
        result = z ^ (result >> shift)
    return result & 0xFFFFFFFF

def undo_left_mask(z, shift, mask):
    result = z
    for _ in range((32 // shift) + 1):
        result = z ^ ((result << shift) & mask)
    return result & 0xFFFFFFFF

def untemper(y):
    y = undo_right(y, 18)
    y = undo_left_mask(y, 15, 0xEFC60000)
    y = undo_left_mask(y, 7, 0x9D2C5680)
    y = undo_right(y, 11)
    return y & 0xFFFFFFFF

state = [untemper(v) for v in outputs]
assert len(state) == 624

class MT19937:
    def __init__(self, state_array):
        self.mt = list(state_array)
        self.index = 624

    def generate(self):
        for i in range(624):
            y = (self.mt[i] & 0x80000000) + (self.mt[(i+1) % 624] & 0x7fffffff)
            self.mt[i] = self.mt[(i + 397) % 624] ^ (y >> 1)
            if y % 2 != 0:
                self.mt[i] ^= 2567483615
        self.index = 0

    def next(self):
        if self.index >= 624:
            self.generate()
        y = self.mt[self.index]
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        self.index += 1
        return y & 0xFFFFFFFF

mt = MT19937(state)

# verify: index=624 forces regenerate; first "next" call should reproduce output #624 (not in our list)
# sanity check: reconstruct state should reproduce KNOWN outputs if we regenerate from scratch differently.
# Instead let's verify by re-tempering the recovered (untempered) state and comparing to given outputs.
def temper(y):
    y ^= y >> 11
    y ^= (y << 7) & 0x9D2C5680
    y ^= (y << 15) & 0xEFC60000
    y ^= y >> 18
    return y & 0xFFFFFFFF

check = [temper(s) for s in state]
print("untemper/temper roundtrip matches outputs:", check == outputs)

n_needed = (len(ct) + 3) // 4
keystream = b""
for _ in range(n_needed):
    v = mt.next()
    keystream += v.to_bytes(4, 'big')

keystream = keystream[:len(ct)]
flag = bytes(x ^ y for x, y in zip(ct, keystream))
print("flag:", flag)
m = re.search(rb"CTF\{[^}]*\}", flag)
print("match:", m)
