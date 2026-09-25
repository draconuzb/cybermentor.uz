import socket, time

HOST = "10.13.37.10"
PORT = 21968

class Conn:
    def __init__(self):
        self.s = socket.create_connection((HOST, PORT), timeout=5)
        self.s.settimeout(2)
    def recv(self, t=1.0):
        buf = b""
        end = time.time() + t
        while time.time() < end:
            try:
                chunk = self.s.recv(4096)
                if chunk == b"":
                    break
                buf += chunk
            except socket.timeout:
                break
        return buf
    def cmd(self, data, t=1.0):
        if isinstance(data, str):
            data = data.encode()
        self.s.sendall(data + b"\n")
        return self.recv(t)
    def close(self):
        self.s.close()

c = Conn()
c.recv(1.0)

def new(slot, ln, data):
    c.cmd("1"); c.cmd(str(slot)); c.cmd(str(ln)); return c.cmd(data)

def show(slot):
    c.cmd("4")
    return c.cmd(str(slot))

r0 = new(0, 16, "A"*16)
r1 = new(1, 16, "C"*16)
s0 = show(0).decode(errors="replace")
s1 = show(1).decode(errors="replace")
print("slot0 show:\n", s0)
print("slot1 show:\n", s1)

import re
def extract_hex(s):
    m = re.search(r"raw:([0-9a-f]+)", s)
    return m.group(1) if m else None

h0 = extract_hex(s0)
h1 = extract_hex(s1)
if h0 and h1:
    print("slot0 offset32 bytes:", h0[64:80])
    print("slot1 offset32 bytes:", h1[64:80])

c.close()
