import socket, time

HOST = "10.13.37.10"
PORT = 20199

def probe(build_input, badge_input=None, label=""):
    try:
        s = socket.create_connection((HOST, PORT), timeout=5)
    except Exception as e:
        print(label, "CONNECT FAIL", e)
        return
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
    try:
        s.sendall((build_input + "\n").encode())
    except BrokenPipeError:
        pass
    time.sleep(0.3)
    recv_all()
    if badge_input is not None:
        try:
            s.sendall((badge_input + "\n").encode())
        except BrokenPipeError:
            pass
        time.sleep(0.3)
        recv_all(2.0)
    s.close()
    print(f"=== {label} (build={build_input!r}) ===")
    print(buf.decode(errors="replace"))
    print()

for opt in ["0", "4", "-1", "99999999", "abc", "", "1e9", "  1", "01", "1 "]:
    probe(opt, badge_input="test", label=f"opt-{opt}")
