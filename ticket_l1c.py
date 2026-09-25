import socket
import time

s = socket.create_connection(("10.13.37.10", 20512), timeout=10)
s.settimeout(3)

def recv(t=3):
    s.settimeout(t)
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
s.sendall(b"test-ticket-123\n")
r = recv()
print("after submit:", r.decode(errors='replace'), flush=True)
time.sleep(2)
r2 = recv(5)
print("after wait:", r2.decode(errors='replace'), flush=True)
s.close()
