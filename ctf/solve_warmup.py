import socket

host = "10.13.37.10"
port = 21136

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
s.connect((host, port))

# Menu matnini o'qish
menu = s.recv(4096).decode(errors='ignore')
print(menu, end="")

# 1-darajani tanlash
print("[+] '1' (warmup) yuborilmoqda...")
s.sendall(b"1\n")

# Warmup javobini olish
try:
    while True:
        data = s.recv(4096)
        if not data:
            break
        print(data.decode(errors='ignore'), end="")
except socket.timeout:
    pass

s.close()
