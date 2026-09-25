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
    def send(self, data):
        if isinstance(data, str):
            data = data.encode()
        self.s.sendall(data + b"\n")
    def close(self):
        self.s.close()

c = Conn()
out = c.recv(1.5)
print("BANNER:\n", out.decode(errors="replace"))

for opt, label in [("5", "cred"), ("8", "receipt"), ("7", "run")]:
    c.send(opt)
    r = c.recv(1.5)
    print(f"=== option {opt} ({label}) ===")
    print(r.decode(errors="replace"))

c.close()
