import socket

HOST = "10.13.37.10"
PORT = 21869

s = socket.create_connection((HOST, PORT), timeout=10)
s.settimeout(5)

def recv_until_prompt(s):
    buf = b""
    while True:
        try:
            chunk = s.recv(4096)
        except socket.timeout:
            break
        if not chunk:
            break
        buf += chunk
        if buf.endswith(b"READY\n\n") or b"READY" in buf[-20:]:
            break
    return buf

banner = recv_until_prompt(s)
print("banner:", banner.decode(errors='replace')[-100:])

s.sendall(b"ORACLE 12345\n")
resp = recv_until_prompt(s)
print("resp:", resp.decode(errors='replace'))
s.close()
