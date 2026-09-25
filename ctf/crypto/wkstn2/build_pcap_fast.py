import json
import base64
import struct

d = json.load(open("stage3.json"))
n = d["n"]
frames_raw = base64.b64decode(d["frames_b64"])
RECLEN = 3 + 16

PCAP_MAGIC = 0xa1b2c3d4
LINKTYPE_IEEE802_11 = 105

out = bytearray()
out += struct.pack("<IHHiIII", PCAP_MAGIC, 2, 4, 0, 0, 65535, LINKTYPE_IEEE802_11)

addr1 = bytes.fromhex("ffffffffffff")
addr2 = bytes.fromhex("001122334455")
addr3 = bytes.fromhex("001122334466")
fc = bytes([0x08, 0x40])  # data frame, protected bit set
dur = bytes([0x00, 0x00])

for i in range(n):
    rec = frames_raw[i*RECLEN:(i+1)*RECLEN]
    iv = rec[0:3]
    ct = rec[3:3+16]
    seq = struct.pack("<H", i & 0xFFFF)
    dot11_hdr = fc + dur + addr1 + addr2 + addr3 + seq
    wep_iv_hdr = iv + b"\x00"  # keyid byte
    icv = b"\x00\x00\x00\x00"
    payload = dot11_hdr + wep_iv_hdr + ct + icv
    ts_sec = i // 1000
    ts_usec = (i % 1000) * 1000
    out += struct.pack("<IIII", ts_sec, ts_usec, len(payload), len(payload))
    out += payload

with open("stage3.pcap", "wb") as f:
    f.write(out)

print("wrote", n, "packets,", len(out), "bytes")
