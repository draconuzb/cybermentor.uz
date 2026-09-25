import hashlib

target = "87ddfc540437fb01931bb530e38af4a7"

with open("/home/ubuntu/wordlists/rockyou.txt", "rb") as f:
    for line in f:
        word = line.rstrip(b"\r\n")
        if hashlib.md5(word).hexdigest() == target:
            print("FOUND:", word)
            break
    else:
        print("not found in rockyou")
