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

for c in [6, 8, 12]:
    print(c, "crib_len", len(known_pt[c]), "ct_len", len(frames[c]))

# recover partial keystream per frame (global position = counter*BLOCK + offset within frame...
# but actually we don't know block size yet; instead build a GLOBAL byte-indexed keystream
# under the hypothesis that "counter" units directly correspond to BYTES divided by some block size B.
# We'll try several B and see which gives consistent overlaps.

for B in [8, 16, 32, 64]:
    keystream = {}  # global_byte_index -> byte
    consistent = True
    for c in [6, 8, 12]:
        base_byte = c * B
        pt = known_pt[c]
        ct = frames[c]
        n = min(len(pt), len(ct))
        for i in range(n):
            gpos = base_byte + i
            kb = pt[i] ^ ct[i]
            if gpos in keystream and keystream[gpos] != kb:
                consistent = False
            keystream[gpos] = kb
    print(f"B={B} consistent={consistent} keystream_positions={len(keystream)}")
