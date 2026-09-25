import socket

host = "10.13.37.10"
port = 21136  # Agar 9401 bo'lsa, shu yerga 9401 yozing

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((host, port))
    
    # Server bergan birinchi xabarni o'qish
    data = s.recv(4096)
    print("=== SERVER JAVOBI ===")
    print(data.decode(errors='ignore'))
    print("=====================")

    s.close()
except Exception as e:
    print(f"Xatolik: {e}")
