import json
from z3 import Solver, BitVec, BitVecVal, LShR, Extract, sat, If

def solve_stage3():
    with open("trunc.json", "r") as f:
        data = json.load(f)

    high_bytes = data["high_bytes"]
    flag_ct = bytes.fromhex(data["flag_ct_hex"])

    print(f"[*] high_bytes soni: {len(high_bytes)}")
    print(f"[*] flag_ct uzunligi: {len(flag_ct)} bayt")

    solver = Solver()

    # Boshlang'ich 624 ta 32-bitli state
    S = [BitVec(f"s_{i}", 32) for i in range(624)]
    needed_outputs = 2600 + (len(flag_ct) + 3) // 4

    # MT19937 Twist
    for i in range(624, needed_outputs):
        s0 = S[i - 624]
        s1 = S[i - 623]
        sm = S[i - 624 + 397]
        y = (s0 & BitVecVal(0x80000000, 32)) | (s1 & BitVecVal(0x7FFFFFFF, 32))
        mag01 = If((y & 1) == 1, BitVecVal(0x9908B0DF, 32), BitVecVal(0, 32))
        next_s = sm ^ LShR(y, 1) ^ mag01
        S.append(next_s)

    # Tempering
    def temper(x):
        x = x ^ LShR(x, 11)
        x = x ^ ((x << 7) & BitVecVal(0x9D2C5680, 32))
        x = x ^ ((x << 15) & BitVecVal(0xEFC60000, 32))
        x = x ^ LShR(x, 18)
        return x

    print("[*] Z3 uchun cheklovlar qo'shilmoqda...")
    for i in range(2600):
        out = temper(S[i])
        solver.add(Extract(31, 24, out) == high_bytes[i])

    print("[*] Z3 tenglamani yechmoqda...")
    if solver.check() == sat:
        print("[+] Yechim topildi!")
        m = solver.model()

        keystream = bytearray()
        for i in range(2600, needed_outputs):
            val = m.eval(temper(S[i])).as_long()
            keystream.extend(val.to_bytes(4, 'big'))

        flag = bytes([b ^ k for b, k in zip(flag_ct, keystream)])
        print("\n" + "=" * 50)
        print(f"[🎉] FLAG: {flag.decode(errors='ignore')}")
        print("=" * 50 + "\n")
    else:
        print("[-] UNSAT: Yechim topilmadi.")

if __name__ == "__main__":
    solve_stage3()
