import hashlib
import re
from Crypto.Cipher import AES, ChaCha20_Poly1305

ticket_hex = "ef52845eb74a18ef655291653aecf097480ff077d429eea9bae3480e5a6ad9cf477989d9be52a8a320cba2ac7e29469dd0297fad68930ad75bf7c1fda13b05933e6a568ca37e79beca41113d17890fb7782f37ed2435afa7f16449fc0815c8d37bb4c5cefb86a03f133d9bea62ffac5f152a035786890611012b619dc3ba589af9df6d7b1692fa195500ae7b670717f314f3cc60eff824fc51f5da0745e5c4bc7bc54a7183f430fa3be02f8a25263b477d26622b8929"
ticket = bytes.fromhex(ticket_hex)

flag1 = b"CTF{bac_64d6776f5b6680c1330d}"
san_hex_part = b"4354467b6261635f36346436373736663562363638306331333330647d"  # the hex string without dots
san_full = b"4354467b6261635f36346436373736663562363638306331.333330647d.mgmt.megatech.internal"

materials = {
    "flag1": flag1,
    "san_hex_part": san_hex_part,
    "san_full": san_full,
    "flag1_inner": b"bac_64d6776f5b6680c1330d",
}

candidates = {}
for mlabel, m in materials.items():
    candidates[f"sha256({mlabel})"] = hashlib.sha256(m).digest()
    candidates[f"md5({mlabel})"] = hashlib.md5(m).digest()
    candidates[f"raw32({mlabel})"] = (m + b"\x00"*32)[:32]
    candidates[f"raw16({mlabel})"] = (m + b"\x00"*16)[:16]

def check(pt, label):
    if re.search(rb"CTF\{", pt):
        print("MATCH", label, pt)
        return True
    return False

found = False
for klabel, key in candidates.items():
    if len(key) not in (16, 24, 32):
        continue
    for nlen in (8, 12, 16):
        nonce = ticket[:nlen]
        ct = ticket[nlen:-16]
        tag = ticket[-16:]
        try:
            c = AES.new(key, AES.MODE_GCM, nonce=nonce)
            pt = c.decrypt_and_verify(ct, tag)
            if check(pt, f"AESGCM n{nlen} {klabel}"):
                found = True
        except Exception:
            pass
        if len(key) == 32:
            try:
                c = ChaCha20_Poly1305.new(key=key, nonce=nonce[:12].ljust(12, b'\x00'))
                pt = c.decrypt_and_verify(ct, tag)
                if check(pt, f"ChaChaPoly n{nlen} {klabel}"):
                    found = True
            except Exception:
                pass
    iv = ticket[:16]
    rest = ticket[16:]
    if len(rest) % 16 == 0:
        try:
            c = AES.new(key, AES.MODE_CBC, iv)
            pt = c.decrypt(rest)
            if check(pt, f"CBC {klabel}"):
                found = True
        except Exception:
            pass

if not found:
    print("no match with flag-based keys either")
