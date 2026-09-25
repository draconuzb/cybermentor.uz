import socket, time, sys

HOST = "10.13.37.10"
PORT = 20059

def recv_all(s, timeout=1.5):
    s.settimeout(timeout)
    chunks = b""
    try:
        while True:
            d = s.recv(65536)
            if not d:
                break
            chunks += d
    except socket.timeout:
        pass
    return chunks

def main():
    lines = sys.argv[1:]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((HOST, PORT))
    print(recv_all(s).decode(errors="replace"), end="")
    for line in lines:
        s.sendall((line + "\n").encode())
        time.sleep(0.3)
        out = recv_all(s)
        print(out.decode(errors="replace"), end="")
    s.close()

if __name__ == "__main__":
    main()
