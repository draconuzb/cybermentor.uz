import socket, time, re

HOST = "10.13.37.10"
PORT = 20199
nonce_re = re.compile(rb"boot nonce:\s*([0-9a-f]+)")

def test(badge_label, badge_fn, wait=4.0):
    s = socket.create_connection((HOST, PORT), timeout=5)
    s.settimeout(1.0)
    buf = b""
    closed = False
    def recv_some(t):
        nonlocal buf, closed
        end = time.time() + t
        while time.time() < end:
            try:
                chunk = s.recv(4096)
                if chunk == b"":
                    closed = True
                    return
                buf += chunk
            except socket.timeout:
                continue
    recv_some(1.0)
    s.sendall(b"1\n")
    recv_some(1.0)
    m = nonce_re.search(buf)
    nonce = m.group(1) if m else None
    badge = badge_fn(nonce)
    s.sendall(badge + b"\n")
    recv_some(wait)
    # probe: is socket still alive? try sending a harmless newline
    alive = True
    try:
        s.sendall(b"\n")
        recv_some(1.0)
    except (BrokenPipeError, OSError):
        alive = False
    s.close()
    print(f"--- {badge_label} --- nonce={nonce} badge={badge!r} closed_by_server={closed} still_alive_after_extra_send={alive}")
    print(buf.decode(errors="replace"))
    print()

test("empty",        lambda n: b"")
test("wrong-fixed",  lambda n: b"WRONGBADGE1234")
test("nonce-as-is",  lambda n: n)
test("nonce-upper",  lambda n: n.upper())
test("nonce-0x",     lambda n: b"0x"+n)
test("all-zero-8",   lambda n: b"00000000")
test("badge-admin",  lambda n: b"admin")
test("badge-debug",  lambda n: b"debug")
test("badge-master", lambda n: b"master")
