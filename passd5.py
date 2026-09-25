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

def test_show(slot):
    c = Conn()
    c.recv(1.0)
    c.cmd("5", 1.0)  # issue cred first
    r = c.cmd("4", 0.8)  # show
    r2 = c.cmd(str(slot), 1.2)
    print(f"--- show slot={slot} ---")
    print((r+r2).decode(errors="replace"))
    c.close()

for slot in [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 16, 100]:
    test_show(slot)
