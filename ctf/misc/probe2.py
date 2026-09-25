import socket

HOST = "10.13.37.10"
PORT = 21856

def connect():
    s = socket.create_connection((HOST, PORT), timeout=5)
    s.settimeout(3)
    return s

def recv_all(s, t=0.3):
    data = b""
    s.settimeout(t)
    try:
        while True:
            chunk = s.recv(4096)
            if not chunk:
                break
            data += chunk
    except socket.timeout:
        pass
    return data

def send(s, line):
    s.sendall((str(line) + "\n").encode())
    return recv_all(s, 0.25)

def host_call(s, idx, arg):
    send(s, 3)
    send(s, idx)
    return send(s, arg)

def fresh():
    s = connect()
    recv_all(s, 0.4)
    return s

def show(label, out):
    print(f"--- {label} ---")
    print(out.decode(errors="replace"))

s = fresh()
# try mem.write then mem.read to understand memory layout / format
out = send(s, 1)  # mem.write
show("mem.write menu", out)
out = send(s, 0)  # offset
show("offset0", out)
out = send(s, "AAAAAAAA")
show("data", out)
s.close()

# try negative idx
s = fresh()
for idx in [-1, -2, -16, 16, 65535, 65536, 4294967295, 2147483647, 2147483648]:
    out = host_call(s, idx, 0)
    txt = out.decode(errors="replace").strip().replace("\n"," | ")
    print(f"idx={idx} -> {txt}")
s.close()

# try idx with various nonzero args across full range
s = fresh()
for idx in range(0,16):
    for arg in [1, 0x41414141, -1]:
        out = host_call(s, idx, arg)
        txt = out.decode(errors="replace").strip().replace("\n"," | ")
        print(f"idx={idx} arg={arg} -> {txt}")
s.close()
