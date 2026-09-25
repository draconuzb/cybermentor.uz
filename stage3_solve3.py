import base64

frames = {
    6: base64.b64decode("th70kQl9xkxtQ/hHqyBzJd5NtLBq9pNKMe7uJnML8t+mkmqCHXeM1e0gGrOQgOFI"),
    8: base64.b64decode("sZJm6xN6i6DtIHWuku7xU2R5ldpu3ivaHuc8qGc2ChPMpHcLRd1dscZdCGg37qRrLPaIm98znzRU9oPkMEXZRg=="),
    10: base64.b64decode("q7BxHUXCXLipOxR/Nuq4D0L2kP7ZM4hAN+yKyGJl/RJ2j62REEBgEU+83rEbFuzgOtxfPrsuDv6QKcA+9BJ57NYD26KPPwpfvjLOt7EX77+9WYD8ucnoMxTk5MD2RicQ"),
    12: base64.b64decode("e/jK9yUjSSkOnPOcezqAokmra07eB32RhCnARJFgFuywaq3Hj1d/MdpAq9Oxf4DKzyqAndqihlxjiIGkkSMnfw=="),
}

known_pt = {
    6: b"STATION SIX RELAYING WEATHER CONDITIONS ALONG THE",
    8: b"SIX ACTUAL SENDS RESUPPLY STATUS FOR THE FORWARD ELEMENT NOW OK",
    12: b"RESUPPLY CONVOY DEPARTS AT ZERO FIVE HUNDRED HOURS ACKNOWLEDGE OK",
}

B = 16
keystream = {}
for c in [6, 8, 12]:
    base_byte = c * B
    pt = known_pt[c]
    ct = frames[c]
    n = min(len(pt), len(ct))
    for i in range(n):
        keystream[base_byte + i] = pt[i] ^ ct[i]

target_ct = frames[10]
target_base = 10 * B
out = []
missing = []
for i, cb in enumerate(target_ct):
    gpos = target_base + i
    if gpos in keystream:
        out.append(cb ^ keystream[gpos])
    else:
        out.append(None)
        missing.append(i)

print("missing positions:", missing)
result = bytes(b if b is not None else 0x2A for b in out)
print("decrypted target:", result)
