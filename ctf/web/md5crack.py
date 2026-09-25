import hashlib

target = "0571749e2ac330a7455809c6b0e7af90"

with open("/home/ubuntu/wordlists/rockyou.txt", "rb") as f:
    for line in f:
        word = line.rstrip(b"\r\n")
        if hashlib.md5(word).hexdigest() == target:
            print("FOUND:", word)
            break
    else:
        print("not found in rockyou")
