import socket
import sys

def try_ticket(n):
    s = socket.create_connection(("10.13.37.10", 20512), timeout=8)
    s.settimeout(3)
    def recv():
        buf = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                buf += chunk
        except socket.timeout:
            pass
        return buf
    recv()
    s.sendall(b"1\n")
    recv()
    s.sendall(b"A" * n + b"\n")
    r = recv()
    s.close()
    print(f"n={n} -> {r.decode(errors='replace')!r}", flush=True)

n = int(sys.argv[1])
try_ticket(n)
