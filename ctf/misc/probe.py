import socket, sys, time

HOST = "10.13.37.10"
PORT = 21856

def connect():
    s = socket.create_connection((HOST, PORT), timeout=5)
    s.settimeout(3)
    return s

def recv_all(s, t=0.4):
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

def host_call(s, idx, arg):
    s.sendall(b"3\n")
    recv_all(s, 0.2)
    s.sendall(str(idx).encode() + b"\n")
    recv_all(s, 0.2)
    s.sendall(str(arg).encode() + b"\n")
    return recv_all(s, 0.3)

def main():
    s = connect()
    banner = recv_all(s, 0.5)
    print("BANNER:\n", banner.decode(errors="replace"))

    # probe idx 0..30 with arg 0
    for idx in range(0, 40):
        try:
            out = host_call(s, idx, 0)
        except Exception as e:
            print(idx, "EXC", e)
            s.close()
            s = connect()
            recv_all(s, 0.3)
            continue
        text = out.decode(errors="replace").strip().replace("\n", " | ")
        print(f"idx={idx:3d} -> {text}")

    s.close()

if __name__ == "__main__":
    main()
