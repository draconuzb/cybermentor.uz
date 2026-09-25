import socket, sys, time, re

HOST = "10.13.37.10"
PORT = 20199

def session(badge, extra_after=None, sleep_between=0.3):
    s = socket.create_connection((HOST, PORT), timeout=5)
    s.settimeout(2)
    buf = b""
    def recv_all(t=1.5):
        nonlocal buf
        end = time.time() + t
        while time.time() < end:
            try:
                chunk = s.recv(4096)
                if not chunk:
                    break
                buf += chunk
            except socket.timeout:
                break
        return buf

    recv_all()
    s.sendall(b"1\n")
    time.sleep(sleep_between)
    recv_all()
    s.sendall(badge if isinstance(badge, bytes) else badge.encode())
    if not (isinstance(badge, bytes) and badge.endswith(b"\n")) and not (isinstance(badge, str) and badge.endswith("\n")):
        s.sendall(b"\n")
    time.sleep(sleep_between)
    recv_all()
    if extra_after:
        for line in extra_after:
            try:
                s.sendall(line if isinstance(line, bytes) else (line+"\n").encode())
            except BrokenPipeError:
                break
            time.sleep(sleep_between)
            recv_all()
    recv_all(1.0)
    s.close()
    return buf

if __name__ == "__main__":
    nonce_re = re.compile(rb"boot nonce:\s*([0-9a-f]+)")
    out = session("")
    print("=== empty badge ===")
    print(out.decode(errors="replace"))
    m = nonce_re.search(out)
    if m:
        nonce = m.group(1)
        print("=== nonce-as-badge (fresh connection) with extra menu probing ===")
        out2 = session(nonce, extra_after=["help", "status", "open", "2", "menu"])
        print(out2.decode(errors="replace"))
