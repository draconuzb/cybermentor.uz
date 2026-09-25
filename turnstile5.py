import socket, time, re
HOST="10.13.37.10"; PORT=20199
nonce_re = re.compile(rb"boot nonce:\s*([0-9a-f]+)")

def test(label, badge_fn, wait=2.0):
    s = socket.create_connection((HOST, PORT), timeout=5)
    s.settimeout(1.0)
    buf=b""
    def recv_some(t):
        nonlocal buf
        end=time.time()+t
        while time.time()<end:
            try:
                c=s.recv(4096)
                if c==b"": return
                buf+=c
            except socket.timeout: continue
    recv_some(1.0)
    s.sendall(b"1\n"); recv_some(1.0)
    m=nonce_re.search(buf)
    nonce=m.group(1) if m else None
    badge=badge_fn(nonce)
    s.sendall(badge); recv_some(wait)
    s.close()
    print(f"--- {label} nonce={nonce} badge={badge!r} ---")
    print(buf.decode(errors="replace")); print()

test("raw-bytes-of-nonce-no-newline", lambda n: bytes.fromhex(n.decode()))
test("raw-bytes-of-nonce-with-newline", lambda n: bytes.fromhex(n.decode())+b"\n")
test("raw-bytes-reversed", lambda n: bytes.fromhex(n.decode())[::-1]+b"\n")
