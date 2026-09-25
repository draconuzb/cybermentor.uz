import json
import base64
from scapy.all import Dot11, Dot11WEP, RadioTap, wrpcap

d = json.load(open("stage3.json"))
n = d["n"]
frames_raw = base64.b64decode(d["frames_b64"])
RECLEN = 3 + 16

pkts = []
for i in range(n):
    rec = frames_raw[i*RECLEN:(i+1)*RECLEN]
    iv = rec[0:3]
    ct = rec[3:3+16]
    # WEP data: iv(3) + keyid(1) + encrypted_payload + icv(4, unknown, use zeros)
    wep_payload = ct + b"\x00\x00\x00\x00"  # fake ICV, aircrack PTW attack doesn't require valid ICV for key search
    dot11 = Dot11(
        type=2, subtype=0,  # data frame
        FCfield=0x40,  # protected bit (WEP) set
        addr1="ff:ff:ff:ff:ff:ff",
        addr2="00:11:22:33:44:55",
        addr3="00:11:22:33:44:66",
    )
    wep = Dot11WEP(iv=iv, keyid=0, wepdata=wep_payload[:-4], icv=int.from_bytes(wep_payload[-4:], 'little'))
    pkt = RadioTap() / dot11 / wep
    pkts.append(pkt)

wrpcap("stage3.pcap", pkts)
print("wrote", len(pkts), "packets")
