import socket

HOST = "10.13.37.10"
PORT = 21869

s = socket.create_connection((HOST, PORT), timeout=10)
f = s.makefile('rwb', buffering=0)

# drain banner
s.settimeout(1.5)
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
except socket.timeout:
    pass

s.settimeout(5)
for val in [12345, 1, 2, 999999]:
    s.sendall(f"ORACLE {val}\n".encode())
    data = s.recv(100)
    print(repr(val), "->", repr(data))
s.close()
