from cryptography import x509
from cryptography.hazmat.backends import default_backend

with open("cert_beta.pem", "rb") as f:
    cert = x509.load_pem_x509_certificate(f.read(), default_backend())

pub = cert.public_key()
nums = pub.public_numbers()
print("N =", nums.n)
print("e =", nums.e)
print("N bits:", nums.n.bit_length())
print("e bits:", nums.e.bit_length())
