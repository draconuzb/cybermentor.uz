data = open("scan.jpg", "rb").read()
print("len", len(data))
i = 2
while i < len(data) - 1:
    if data[i] != 0xFF:
        i += 1
        continue
    marker = data[i + 1]
    if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
        i += 2
        continue
    if marker == 0xDA:
        print(hex(i), "SOS - start of scan, stopping marker walk")
        break
    if i + 3 >= len(data):
        break
    seglen = (data[i + 2] << 8) + data[i + 3]
    print(hex(i), hex(marker), "len=", seglen)
    if marker == 0xFE:
        print("  COMMENT:", data[i + 4:i + 2 + seglen])
    i += 2 + seglen
