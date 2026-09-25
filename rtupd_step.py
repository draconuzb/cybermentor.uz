import socket
import time

s = socket.create_connection(("10.13.37.10", 21612), timeout=8)
s.settimeout(2)

def recv():
    buf = b""
    try:
        while True:
            chunk = s.recv(65536)
            if not chunk:
                break
            buf += chunk
    except socket.timeout:
        pass
    return buf

def send(x):
    print(f">>> {x!r}", flush=True)
    s.sendall((x + "\n").encode())
    time.sleep(0.3)
    r = recv()
    print(repr(r.decode(errors='replace')), flush=True)
    return r

r0 = recv()
print("BANNER:", repr(r0.decode(errors='replace')), flush=True)
send("1")
send("1")   # peek prompt - try a small numeric value
send("16")  # len prompt guess
send("00" * 16)  # data prompt - 16 zero bytes
s.close()
