import socket, time

HOST = "10.13.37.10"
PORT = 20226

s = socket.create_connection((HOST, PORT), timeout=8)
s.settimeout(2)
buf = b""
end = time.time() + 4
while time.time() < end:
    try:
        chunk = s.recv(4096)
        if chunk == b"":
            break
        buf += chunk
    except socket.timeout:
        break
print(buf.decode(errors="replace"))
s.close()
