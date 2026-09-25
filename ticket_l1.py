import socket

s = socket.create_connection(("10.13.37.10", 20512), timeout=10)
s.settimeout(2)

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

print(recv().decode(errors='replace'), flush=True)
s.sendall(b"1\n")
print(">>> 1", flush=True)
print(recv().decode(errors='replace'), flush=True)
s.close()
