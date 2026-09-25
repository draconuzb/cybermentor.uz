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
    def read_until_prompt(self, timeout=3.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.buf.rstrip(b" ").endswith(b">") or self.buf.endswith(b": "):
                out, self.buf = self.buf, b""
                return out
            self._fill(min(time.time() + 0.3, deadline))
        out, self.buf = self.buf, b""
        return out
    def cmd(self, data, timeout=3.0):
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

def fresh():
    c = Conn()
    c.read_until_prompt(2.0)
    return c

def new(c, slot, ln, data):
    c.cmd("1"); c.cmd(str(slot)); c.cmd(str(ln)); return c.cmd(data)

# 1) explore 'run' with a valid pass, and various idx
c = fresh()
new(c, 0, 16, "A"*16)
for idx in ["0", "1", "-1", "999", "cred", ""]:
    c.cmd("7")
    r = c.cmd(idx)
    print(f"run idx={idx!r}:", r.decode(errors="replace"))
c.close()

# 2) explore 'receipt' with various codes after creating cred
c = fresh()
c.cmd("5")  # cred
for code in ["0", "admin", "1"*8, "%x"*4, "A"*40]:
    c.cmd("8")
    r = c.cmd(code)
    print(f"receipt code={code!r}:", r.decode(errors="replace"))
c.close()

# 3) run idx pointing at cred after issuing cred
c = fresh()
c.cmd("5")
c.cmd("7")
r = c.cmd("0")
print("run idx=0 after cred:", r.decode(errors="replace"))
c.close()
