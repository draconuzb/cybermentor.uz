import re
from Crypto.Cipher import AES, ChaCha20_Poly1305

ticket_hex = "ef52845eb74a18ef655291653aecf097480ff077d429eea9bae3480e5a6ad9cf477989d9be52a8a320cba2ac7e29469dd0297fad68930ad75bf7c1fda13b05933e6a568ca37e79beca41113d17890fb7782f37ed2435afa7f16449fc0815c8d37bb4c5cefb86a03f133d9bea62ffac5f152a035786890611012b619dc3ba589af9df6d7b1692fa195500ae7b670717f314f3cc60eff824fc51f5da0745e5c4bc7bc54a7183f430fa3be02f8a25263b477d26622b8929"
ticket = bytes.fromhex(ticket_hex)

pubkey_hex = "04897001a0373b974b64eeb5385d0b346e92db0c45343ff26aeb8190072b1d00b7b095bb82593ab2ea8f270da9f5203925a40887a8d1b911ebe127792637ca50a3"
pubkey = bytes.fromhex(pubkey_hex)
print("pubkey total len:", len(pubkey))
x = pubkey[1:33]
y = pubkey[33:65]
print("x:", x.hex(), len(x))
print("y:", y.hex(), len(y))

candidates = {
    "x_coord": x,
    "y_coord": y,
    "x_plus_y": bytes(a ^ b for a, b in zip(x, y)),
}

def check(pt, label):
    if re.search(rb"CTF\{", pt):
        print("MATCH", label, pt)
        return True
    return False

found = False
for klabel, key in candidates.items():
    if len(key) not in (16, 24, 32):
        print(klabel, "bad len", len(key))
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
    print("no match with raw EC coordinate keys")
