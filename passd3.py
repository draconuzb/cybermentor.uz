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

def fresh_test(label, steps):
    c = Conn()
    print(f"\n########## {label} ##########")
    print(c.recv(1.0).decode(errors="replace"))
    for s in steps:
        r = c.cmd(s)
        print(f">> sent {s!r}")
        print(r.decode(errors="replace"))
    c.close()

fresh_test("new (option 1)", ["1", "8", "AAAAAAAA"])
fresh_test("show (option 4) on empty", ["4"])
fresh_test("receipt (option 8) with code", ["8", "TESTCODE"])
fresh_test("run (option 7) alone", ["7"])
fresh_test("login (option 6) alone, no cred", ["6"])
fresh_test("free (option 3) alone", ["3"])
fresh_test("edit (option 2) alone", ["2"])
