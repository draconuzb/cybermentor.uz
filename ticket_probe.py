import socket

s = socket.create_connection(("10.13.37.10", 20512), timeout=10)
s.settimeout(2)
buf = b""
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        buf += chunk
except socket.timeout:
    pass
print(buf.decode(errors='replace'))
s.close()
