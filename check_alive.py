import socket
try:
    s = socket.create_connection(("10.13.37.10", 20550), timeout=5)
    s.settimeout(3)
    print(s.recv(4096).decode(errors="replace"))
except Exception as e:
    print("err:", e)
