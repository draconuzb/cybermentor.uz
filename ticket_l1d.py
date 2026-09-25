import socket

def try_ticket(ticket_bytes):
    s = socket.create_connection(("10.13.37.10", 20512), timeout=8)
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
    s.sendall(b"1\n")
    recv()
    s.sendall(ticket_bytes + b"\n")
    r = recv()
    s.close()
    print(repr(ticket_bytes[:30]), "->", r.decode(errors='replace'), flush=True)

try_ticket(b"")
try_ticket(b"%x %x %x %x")
try_ticket(b"A" * 200)
try_ticket(b"{}")
try_ticket(b"flag")
try_ticket(b"warmup")
