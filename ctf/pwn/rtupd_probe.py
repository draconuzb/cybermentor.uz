import socket, sys, time, binascii

HOST = "10.13.37.10"
PORT = 21215

s = socket.create_connection((HOST, PORT), timeout=8)
s.settimeout(3)

data = b""
try:
    while True:
        chunk = s.recv(4096)
        if not chunk:
            break
        data += chunk
except socket.timeout:
    pass

print("recv len:", len(data))
print(binascii.hexlify(data[:200]))
print(repr(data[:500]))

with open("/tmp/rtupd_stage0.bin", "wb") as f:
    f.write(data)

s.close()
