import hashlib
import hmac
import random
import struct
import sympy
from Crypto.Cipher import AES, ChaCha20, Salsa20, ARC4
from Crypto.Util import Counter
from Crypto.Protocol.KDF import HKDF

# 1. Ma'lumotlar
p = int("e6c7aed5eb64deb4c600ead2c32b6ebeb5368c30e43e4fd5077a17280ef3", 16)
g = 2
A = int("824ad89131a5b01f3d56ddeeb639ecfc847b0e5eeea8b84ee789880ab57", 16)
B = int("e3c48bf2e73afc85b90da56d358bd36e29d96e4a592f54fca66c37db4b2c", 16)

nonce = bytes.fromhex("b9bdd230e9fc09561fdad1b6cc1e07f7")
payload = bytes.fromhex("6b2b7ddb7206b864ea6d370851f204071c47479f11e4facb90db9d5d22")

# Discrete Log
a = sympy.discrete_log(p, A, g)
S = pow(B, a, p)

# S variantlari (O'nlik matn va Hex ham kiritildi)
p_len = (p.bit_length() + 7) // 8
s_sources = [
    ("S_bytes_be", S.to_bytes(p_len, 'big')),
    ("S_bytes_le", S.to_bytes(p_len, 'little')),
    ("S_bytes_32_be", S.to_bytes(32, 'big')),
    ("S_bytes_32_le", S.to_bytes(32, 'little')),
    ("S_hex", f"{S:x}".encode()),
    ("S_dec_str", str(S).encode()), # CTF larda juda ko'p uchraydi: str(S)
]

keys = []
for label, sb in s_sources:
    keys.append((f"{label}_RAW", sb))
    keys.append((f"{label}_SHA256", hashlib.sha256(sb).digest()))
    keys.append((f"{label}_SHA512", hashlib.sha512(sb).digest()))
    keys.append((f"{label}_SHA1", hashlib.sha1(sb).digest()))
    keys.append((f"{label}_MD5", hashlib.md5(sb).digest()))
    keys.append((f"{label}_SHA256(S+nonce)", hashlib.sha256(sb + nonce).digest()))
    keys.append((f"{label}_SHA256(nonce+S)", hashlib.sha256(nonce + sb).digest()))
    keys.append((f"{label}_HMAC(nonce,S)", hmac.new(nonce, sb, hashlib.sha256).digest()))
    keys.append((f"{label}_HMAC(S,nonce)", hmac.new(sb, nonce, hashlib.sha256).digest()))

    for ctx in [b"", b"vpn", b"key", b"session1", b"handshake", b"ffdhe-legacy-1"]:
        try:
            keys.append((f"{label}_HKDF({ctx!r})", HKDF(sb, 32, nonce, hashlib.sha256, context=ctx)))
        except Exception: pass

# HAQIQIY FLAGNI ANIQLASH (Qat'iy shartlar)
def is_real_flag(pt):
    if not pt or len(pt) != len(payload):
        return False
    
    # 1. BARCHA baytlar mutlaqo o'qilishi mumkin bo'lgan ASCII belgilar bo'lishi shart!
    if not all(32 <= b <= 126 for b in pt):
        return False
    
    # 2. Flag '}' bilan tugashi YOKI 'c4', 'flag', 'ctf', 'uz' kabi prefiks bilan boshlanishi kerak
    text = pt.decode('ascii', errors='ignore')
    if text.endswith('}') or any(text.lower().startswith(pfx) for pfx in ['c4{', 'flag{', 'ctf{', 'uz{', 'c4_']):
        return True
    
    # Agar 100% toza inglizcha matn bo'lsa
    if sum(1 for c in text if c.isalnum() or c in "_{}-!@#$") == len(text):
        return True

    return False

def print_flag(alg_name, pt):
    print("\n" + "🔥" * 35)
    print(f"[🎉] HAQIQIY FLAG TOPILDI!")
    print(f"     Algoritm: {alg_name}")
    print(f"     FLAG:     {pt.decode()}")
    print("🔥" * 35 + "\n")

print("[*] Qat'iy saralash boshlandi...")
found = False

# 1. Standart shifrlar
for label, k in keys:
    subkeys = [k[:16], k[:24], k[:32]] if len(k) >= 32 else [k[:16]]
    
    for key in subkeys:
        if len(key) not in (16, 24, 32): continue
        kbits = len(key) * 8

        # AES-CTR (Har xil IV / Counter sozlamalari bilan)
        for nl in [8, 12, 16]:
            try:
                c = AES.new(key, AES.MODE_CTR, nonce=nonce[:nl])
                pt = c.decrypt(payload)
                if is_real_flag(pt):
                    print_flag(f"AES-{kbits}-CTR ({label}, nonce_len={nl})", pt)
                    found = True
            except Exception: pass

        # AES-CBC / CFB / OFB / ECB
        for mode_name, mode in [("CBC", AES.MODE_CBC), ("CFB", AES.MODE_CFB), ("OFB", AES.MODE_OFB), ("ECB", AES.MODE_ECB)]:
            try:
                c = AES.new(key, mode) if mode == AES.MODE_ECB else AES.new(key, mode, iv=nonce[:16])
                pt = c.decrypt(payload)
                if is_real_flag(pt):
                    print_flag(f"AES-{kbits}-{mode_name} ({label})", pt)
                    found = True
            except Exception: pass

        # ChaCha20 / Salsa20 / ARC4
        if len(key) == 32:
            try:
                c = ChaCha20.new(key=key, nonce=nonce[:12])
                pt = c.decrypt(payload)
                if is_real_flag(pt): print_flag(f"ChaCha20 ({label})", pt); found = True
            except Exception: pass

        if len(key) in (16, 32):
            try:
                c = Salsa20.new(key=key, nonce=nonce[:8])
                pt = c.decrypt(payload)
                if is_real_flag(pt): print_flag(f"Salsa20 ({label})", pt); found = True
            except Exception: pass

        try:
            c = ARC4.new(key)
            pt = c.decrypt(payload)
            if is_real_flag(pt): print_flag(f"ARC4 ({label})", pt); found = True
        except Exception: pass

# 2. Maxsus CTF Hash Stream (SHA256 Keystream: SHA256(key + 0), SHA256(key + 1)...)
for label, k in keys:
    keystream = b""
    counter = 0
    while len(keystream) < len(payload):
        keystream += hashlib.sha256(k + struct.pack(">I", counter)).digest()
        counter += 1
    pt = bytes([p ^ ks for p, ks in zip(payload, keystream)])
    if is_real_flag(pt):
        print_flag(f"Hash-Stream-SHA256 ({label})", pt)
        found = True

# 3. MT19937 (Python Random Seed)
try:
    random.seed(S & 0xffffffff)
    rand_ks = bytes([random.randint(0, 255) for _ in range(len(payload))])
    pt = bytes([p ^ ks for p, ks in zip(payload, rand_ks)])
    if is_real_flag(pt):
        print_flag("MT19937 PRNG Stream (S_seed)", pt)
        found = True
except Exception: pass

if not found:
    print("[-] Hali ham topilmadi. Flagni topish uchun xabardan 'known prefix' orqali kalit qidirib ko'ramiz...")
