import hashlib
import hmac as hmac_mod
import re
from Crypto.Cipher import AES

h = "25ce410e82301085e1ab90aea558c0a06e4d3c81fb6668a750850e4e1b1243b8bba96edfff2dde26a24f28ae859861846982d2210f10a03c76e25008a6e9572d1197114324cef3c2b4fae829a0d5fd27838466d4deeab65575168660d118ec423ea40c2ae386cae2ea0dca67a4905144c39874a0ff85dbe3beb141dd5f6c0de07ac4c635e7164fa6863dfbf99d92ee995ec8d9aba354adeca412fb17"
blob = bytes.fromhex(h)
print(len(blob))

password = b"F3rg0na_M3sh_0TA_k3y"
username = b"tech_provision"
clientid = b"thermostat-batch7-node"

def pbkdf2(pw, salt, n=1000, dklen=32):
    return hashlib.pbkdf2_hmac("sha256", pw, salt, n, dklen)

keys = {
    "sha256": hashlib.sha256(password).digest(),
    "sha256_16": hashlib.sha256(password).digest()[:16],
    "md5": hashlib.md5(password).digest(),
    "pbkdf2_client_salt_32": pbkdf2(password, clientid, 1000, 32),
    "pbkdf2_client_salt_16": pbkdf2(password, clientid, 1000, 16),
    "hmac_sha256_clientid": hmac_mod.new(password, clientid, hashlib.sha256).digest(),
    "hmac_sha256_key=client_msg=pw": hmac_mod.new(clientid, password, hashlib.sha256).digest(),
    "sha256_user_colon_pw": hashlib.sha256(username + b":" + password).digest(),
}

def try_cbc(key, iv, ct):
    try:
        c = AES.new(key, AES.MODE_CBC, iv)
        pt = c.decrypt(ct)
        return pt
    except Exception:
        return None

found = False
layouts = [
    ("iv16_ct128_tail12", blob[:16], blob[16:16+128]),
    ("iv16_ct140_notail", blob[:16], blob[16:]),  # won't work len%16 !=0 but try anyway guarded
    ("tail16_iv_ct_front", blob[-16:], blob[:-16] if len(blob[:-16])%16==0 else None),
]

for name, iv, ct in layouts:
    if ct is None or len(ct) % 16 != 0:
        continue
    for klabel, key in keys.items():
        if len(key) not in (16, 24, 32):
            continue
        pt = try_cbc(key, iv, ct)
        if pt is None:
            continue
        if re.search(rb"CTF\{", pt):
            print("MATCH", name, klabel, pt)
            found = True
        else:
            # check pkcs7 padding validity as weak signal
            padlen = pt[-1]
            if 1 <= padlen <= 16 and pt[-padlen:] == bytes([padlen])*padlen:
                printable = sum(1 for b in pt if 32<=b<127)
                if printable > len(pt)*0.7:
                    print("PKCS7-valid candidate", name, klabel, pt)

if not found:
    print("no CBC match in this layout batch")
