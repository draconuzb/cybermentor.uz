import socket

def session(cmds, initial="1"):
    s = socket.create_connection(("10.13.37.10", 21612), timeout=8)
    s.settimeout(1.5)
    def recv():
        buf = b""
        try:
            while True:
                chunk = s.recv(65536)
                if not chunk:
                    break
                buf += chunk
        except socket.timeout:
            pass
        return buf
    print("banner:", recv().decode(errors='replace'), flush=True)
    s.sendall((initial + "\n").encode())
    print(">>>", initial)
    print(recv().decode(errors='replace'), flush=True)
    for c in cmds:
        s.sendall((c + "\n").encode())
        print(">>>", c, flush=True)
        print(recv().decode(errors='replace'), flush=True)
    s.close()

session(["x", "16", "4142434445464748"])
