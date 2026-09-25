import hashlib
import re
from Crypto.Cipher import AES, ChaCha20_Poly1305
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.primitives.hashes import SHA256

cert_hex = "30820242308201e7a003020102020f5aaa8597c11585e99bd446e3a2fe81300a06082a8648ce3d040302305b310b300906035504061302555331253023060355040a0c1c4d6567615465636820496e7465726e616c2049737375696e672043413125302306035504030c1c4d6567615465636820496e7465726e616c2049737375696e67204341301e170d3233303431313036313432325a170d3234303431303036313432325a305d31153013060355040a0c0c4d65676154656368204c4c433120301e060355040b0c1750726f766973696f6e696e67204175746f6d6174696f6e3122302006035504030c1970726f766973696f6e696e672e6d656761746563682e636f6d3059301306072a8648ce3d020106082a8648ce3d03010703420004897001a0373b974b64eeb5385d0b346e92db0c45343ff26aeb8190072b1d00b7b095bb82593ab2ea8f270da9f5203925a40887a8d1b911ebe127792637ca50a3a3818b30818830780603551d110471306f821970726f766973696f6e696e672e6d656761746563682e636f6d82523433353434363762363236313633356633363334363433363337333733363636333536323336333633383330363333312e333333333330363437642e6d676d742e6d656761746563682e696e7465726e616c300c0603551d130101ff04023000300a06082a8648ce3d0403020349003046022100860542b40b37ba7c4390ec8fa8c316a2153c112425b95aec40209308fda1d309022100cc1d7bdbb5edfbfc818dbf318f3c80ebadd9e5a1411d4d4c0b4fb72ea6e3c38a"
cert_der = bytes.fromhex(cert_hex)
cert = x509.load_der_x509_certificate(cert_der, default_backend())

print("Serial:", cert.serial_number, hex(cert.serial_number))
print("Subject:", cert.subject.rfc4514_string())
print("Issuer:", cert.issuer.rfc4514_string())
print("NotBefore:", cert.not_valid_before_utc)
print("NotAfter:", cert.not_valid_after_utc)
print("Fingerprint SHA256:", cert.fingerprint(SHA256()).hex())

pub_der = cert.public_key().public_bytes(Encoding.DER, PublicFormat.SubjectPublicKeyInfo)
pub_raw = cert.public_key().public_bytes(Encoding.X962, PublicFormat.UncompressedPoint)
tbs = cert.tbs_certificate_bytes

san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
san_names = [n.value for n in san.value]
print("SAN:", san_names)

ticket_hex = "ef52845eb74a18ef655291653aecf097480ff077d429eea9bae3480e5a6ad9cf477989d9be52a8a320cba2ac7e29469dd0297fad68930ad75bf7c1fda13b05933e6a568ca37e79beca41113d17890fb7782f37ed2435afa7f16449fc0815c8d37bb4c5cefb86a03f133d9bea62ffac5f152a035786890611012b619dc3ba589af9df6d7b1692fa195500ae7b670717f314f3cc60eff824fc51f5da0745e5c4bc7bc54a7183f430fa3be02f8a25263b477d26622b8929"
ticket = bytes.fromhex(ticket_hex)

serial_bytes = cert.serial_number.to_bytes((cert.serial_number.bit_length() + 7) // 8, "big")

materials = {
    "tbs": tbs,
    "pub_der": pub_der,
    "pub_raw": pub_raw,
    "fingerprint_sha256_bytes": cert.fingerprint(SHA256()),
    "serial_bytes": serial_bytes,
    "san0": san_names[0].encode(),
    "san1": san_names[1].encode() if len(san_names) > 1 else b"",
    "subject_str": cert.subject.rfc4514_string().encode(),
}

candidates = {}
for mlabel, m in materials.items():
    if not m:
        continue
    candidates[f"sha256({mlabel})"] = hashlib.sha256(m).digest()
    candidates[f"md5({mlabel})"] = hashlib.md5(m).digest()

# fingerprint itself IS sha256(cert_der) essentially (32 bytes) - use directly too
candidates["fingerprint_direct"] = cert.fingerprint(SHA256())

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
    # CBC iv16
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
    print("still no match")
