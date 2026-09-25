import socket

s = socket.create_connection(("10.13.37.10", 21327), timeout=10)
s.settimeout(3)
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
