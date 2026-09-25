import socket

def session(cmds):
    s = socket.create_connection(("10.13.37.10", 20752), timeout=10)
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
    print(recv().decode(errors='replace'))
    for c in cmds:
        s.sendall((c + "\n").encode())
        print(f">>> {c}")
        print(recv().decode(errors='replace'))
    s.close()

session(["PEEK 0 16", "PEEK 0 64", "PEEK 0 256", "PEEK 16 64"])
