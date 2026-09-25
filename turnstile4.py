import socket, time, re

HOST = "10.13.37.10"
PORT = 20199
nonce_re = re.compile(rb"boot nonce:\s*([0-9a-f]+)")

def get_nonce_and_send_badge(badge_bytes, wait=2.0):
    s = socket.create_connection((HOST, PORT), timeout=5)
    s.settimeout(1.0)
    buf = b""
    def recv_some(t):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            try:
                chunk = s.recv(4096)
                if chunk == b"":
                    return
                buf += chunk
            except socket.timeout:
                continue
    recv_some(1.0)
    s.sendall(b"1\n")
    recv_some(1.0)
    m = nonce_re.search(buf)
    this_nonce = m.group(1) if m else None
    s.sendall(badge_bytes + b"\n")
    recv_some(wait)
    s.close()
    return this_nonce, buf

print("=== connection A (capture nonce, send garbage badge) ===")
nonceA, bufA = get_nonce_and_send_badge(b"garbage-first-conn")
print("nonceA:", nonceA)
print(bufA.decode(errors="replace"))

print("=== connection B (fresh nonce, but submit PREVIOUS connection's nonce A as badge) ===")
nonceB, bufB = get_nonce_and_send_badge(nonceA)
print("nonceB:", nonceB, " badge_sent(=nonceA):", nonceA)
print(bufB.decode(errors="replace"))
