import socket, time

HOST = "10.13.37.10"
PORT = 21968

def connect():
    s = socket.create_connection((HOST, PORT), timeout=5)
    s.settimeout(2)
    return s

def recv_all(s, t=1.5):
    buf = b""
    end = time.time() + t
    while time.time() < end:
        try:
            chunk = s.recv(4096)
            if chunk == b"":
                break
            buf += chunk
        except socket.timeout:
            break
    return buf

s = connect()
print(recv_all(s, 2.0).decode(errors="replace"))
s.close()
