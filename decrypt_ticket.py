import hashlib
import re
from Crypto.Cipher import AES

cert_hex = "30820242308201e7a003020102020f5aaa8597c11585e99bd446e3a2fe81300a06082a8648ce3d040302305b310b300906035504061302555331253023060355040a0c1c4d6567615465636820496e7465726e616c2049737375696e672043413125302306035504030c1c4d6567615465636820496e7465726e616c2049737375696e67204341301e170d3233303431313036313432325a170d3234303431303036313432325a305d31153013060355040a0c0c4d65676154656368204c4c433120301e060355040b0c1750726f766973696f6e696e67204175746f6d6174696f6e3122302006035504030c1970726f766973696f6e696e672e6d656761746563682e636f6d3059301306072a8648ce3d020106082a8648ce3d03010703420004897001a0373b974b64eeb5385d0b346e92db0c45343ff26aeb8190072b1d00b7b095bb82593ab2ea8f270da9f5203925a40887a8d1b911ebe127792637ca50a3a3818b30818830780603551d110471306f821970726f766973696f6e696e672e6d656761746563682e636f6d82523433353434363762363236313633356633363334363433363337333733363636333536323336333633383330363333312e333333333330363437642e6d676d742e6d656761746563682e696e7465726e616c300c0603551d130101ff04023000300a06082a8648ce3d0403020349003046022100860542b40b37ba7c4390ec8fa8c316a2153c112425b95aec40209308fda1d309022100cc1d7bdbb5edfbfc818dbf318f3c80ebadd9e5a1411d4d4c0b4fb72ea6e3c38a"
cert_der = bytes.fromhex(cert_hex)
print("cert der len:", len(cert_der))

ticket_hex = "ef52845eb74a18ef655291653aecf097480ff077d429eea9bae3480e5a6ad9cf477989d9be52a8a320cba2ac7e29469dd0297fad68930ad75bf7c1fda13b05933e6a568ca37e79beca41113d17890fb7782f37ed2435afa7f16449fc0815c8d37bb4c5cefb86a03f133d9bea62ffac5f152a035786890611012b619dc3ba589af9df6d7b1692fa195500ae7b670717f314f3cc60eff824fc51f5da0745e5c4bc7bc54a7183f430fa3be02f8a25263b477d26622b8929"
ticket = bytes.fromhex(ticket_hex)
print("ticket len:", len(ticket))

# public key raw bytes (EC point, from subjectPublicKeyInfo)
pubkey_hex = "04897001a0373b974b64eeb5385d0b346e92db0c45343ff26aeb8190072b1d00b7b095bb82593ab2ea8f270da9f5203925a40887a8d1b911ebe127792637ca50a3"
pubkey = bytes.fromhex(pubkey_hex)

serial_hex = "5aaa8597c11585e99bd446e3a2fe81"
serial = bytes.fromhex(serial_hex)

cn = b"provisioning.megatech.com"

candidates = {
    "sha256(cert_der)": hashlib.sha256(cert_der).digest(),
    "sha256(pubkey)": hashlib.sha256(pubkey).digest(),
    "sha256(serial)": hashlib.sha256(serial).digest(),
    "sha256(cn)": hashlib.sha256(cn).digest(),
    "sha256(serial+cn)": hashlib.sha256(serial + cn).digest(),
    "sha256(cn+serial)": hashlib.sha256(cn + serial).digest(),
    "md5(cert_der)": hashlib.md5(cert_der).digest(),
    "md5(pubkey)": hashlib.md5(pubkey).digest(),
    "sha1(cert_der)_16": hashlib.sha1(cert_der).digest()[:16],
    "sha1(pubkey)_16": hashlib.sha1(pubkey).digest()[:16],
}

def check(pt, label):
    if re.search(rb"CTF\{", pt):
        print("MATCH", label, pt)
        return True
    return False

found = False
for klabel, key in candidates.items():
    if len(key) not in (16, 24, 32):
        continue
    # GCM: nonce first12, tag last16
    nonce = ticket[:12]
    ct = ticket[12:-16]
    tag = ticket[-16:]
    try:
        c = AES.new(key, AES.MODE_GCM, nonce=nonce)
        pt = c.decrypt_and_verify(ct, tag)
        if check(pt, f"GCM12 {klabel}"):
            found = True
    except Exception:
        pass
    # GCM: nonce first16(non-standard), tag last16
    nonce16 = ticket[:16]
    ct2 = ticket[16:-16]
    try:
        c = AES.new(key, AES.MODE_GCM, nonce=nonce16)
        pt = c.decrypt_and_verify(ct2, tag)
        if check(pt, f"GCM16 {klabel}"):
            found = True
    except Exception:
        pass
    # CBC: iv first16, ct rest (if aligned)
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
    print("no match in this batch")
