import socket
import sys

HOST = "10.13.37.10"
PORT = 21869

def recv_all(s, timeout=2.0):
    s.settimeout(timeout)
    chunks = []
    try:
        while True:
            data = s.recv(65536)
            if not data:
                break
            chunks.append(data)
    except socket.timeout:
        pass
    return b"".join(chunks)

def session(commands, rawfile=None):
    s = socket.create_connection((HOST, PORT), timeout=5)
    banner = recv_all(s)
    print("--- banner ---")
    print(banner.decode(errors='replace'))
    all_resp = banner
    for cmd in commands:
        print(f">>> {cmd!r}")
        s.sendall((cmd + "\n").encode())
        resp = recv_all(s)
        all_resp += resp
        print(resp.decode(errors='replace'))
    s.close()
    if rawfile:
        with open(rawfile, "wb") as f:
            f.write(all_resp)
        print("raw saved to", rawfile, "len", len(all_resp))

if __name__ == "__main__":
    cmds = sys.argv[1:] if len(sys.argv) > 1 else ["HELP"]
    session(cmds, rawfile="/tmp/cert_raw.txt")
