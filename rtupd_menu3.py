import socket

def try_opt(opt):
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
    banner = recv()
    s.sendall((opt + "\n").encode())
    r = recv()
    s.close()
    print(f"opt={opt!r}:", banner.decode(errors='replace') + r.decode(errors='replace'), flush=True)

for opt in ["0", "4", "help", "download", "info", "binary", "elf", "?"]:
    try_opt(opt)
