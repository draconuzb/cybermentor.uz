import base64
import gzip
import re

chunks_hex = {
    0: "4834734941414141414141434178334c515172434d42434634617545575775",
    1: "5a564e4d517434496e4546784b4f356c434d475167452b6969394f34616c2b",
    2: "2f6a2f547551354d7a55704d4c4e775062525673374f77636d41736d715330",
    3: "686c786a72684f76724e6f6c3163715554593146676363624d447250366c4d",
    4: "556d4d2f5848364c4b6b63754c633235462f666e59362f4537355669734859",
    5: "4d6276487348664d30346e4c4138515556585869376951414141413d3d",
}

payload_b64 = "".join(bytes.fromhex(chunks_hex[i]).decode() for i in sorted(chunks_hex))
print("base64 payload:", payload_b64)

raw = base64.b64decode(payload_b64)
print("raw bytes len:", len(raw), "magic:", raw[:4])

decompressed = gzip.decompress(raw)
print("decompressed:", decompressed)

m = re.search(rb"CTF\{[^}]*\}", decompressed)
print("flag:", m.group(0) if m else None)
