import bz2
import re

frames = [
    ["40c181000046055b01010a0000000000", "00425a6839314159265359a1830aa600", "0049df80001040627fb03bad9f10bfff", "ff"],
    ["010a3000cd306a99a93321189e534640", "3134cd134d1a69a08a9f9341aa3c93d4", "1a68c2001a01a03412a2795320341880", "7a"],
    ["0280189b48000a9d3fbc6d6fce2be27e", "b1d22a756e4b6385e88140732b294098", "09f14c204404c09048185d4d4d05730d", "00"],
    ["0391a2b82b6826f57b4106283f2d9b8b", "13aa2e72134d80611a05c607b0cc22ad", "8cd962285816db45d040a5aa4e18733d", "58"],
    ["04761df73e9413ba284b5599a7ef3db9", "61383247b8b319a59913c77b2bd0fc30", "a82a271810fb16c9cf24a105de321c46", "2b"],
    ["853704a452314a38bcda84800436be6f", "d81ec4720c0a312271aa616b996a90c5", "7678fe2ee48a70a1214306154c"],
]

app_data = b""
for chunks in frames:
    raw = bytes.fromhex("".join(chunks))
    app_data += raw[1:]  # strip 1-byte transport control header

print("total app_data len:", len(app_data))
print(app_data.hex())

idx = app_data.find(b"BZh")
print("BZh found at offset:", idx)

bz_stream = app_data[idx:]
print("bz_stream len:", len(bz_stream))
print("bz_stream hex tail:", bz_stream[-20:].hex())

try:
    decompressed = bz2.decompress(bz_stream)
    print("decompressed:", decompressed)
except Exception as e:
    print("bz2 error:", e)
    # try trimming trailing bytes progressively
    for trim in range(0, 10):
        try:
            d = bz2.decompress(bz_stream[:len(bz_stream)-trim] if trim else bz_stream)
            print("worked with trim", trim, d)
            break
        except Exception as e2:
            pass
