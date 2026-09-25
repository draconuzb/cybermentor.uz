import base64

frames = {
    6: base64.b64decode("th70kQl9xkxtQ/hHqyBzJd5NtLBq9pNKMe7uJnML8t+mkmqCHXeM1e0gGrOQgOFI"),
    8: base64.b64decode("sZJm6xN6i6DtIHWuku7xU2R5ldpu3ivaHuc8qGc2ChPMpHcLRd1dscZdCGg37qRrLPaIm98znzRU9oPkMEXZRg=="),
    10: base64.b64decode("q7BxHUXCXLipOxR/Nuq4D0L2kP7ZM4hAN+yKyGJl/RJ2j62REEBgEU+83rEbFuzgOtxfPrsuDv6QKcA+9BJ57NYD26KPPwpfvjLOt7EX77+9WYD8ucnoMxTk5MD2RicQ"),
    12: base64.b64decode("e/jK9yUjSSkOnPOcezqAokmra07eB32RhCnARJFgFuywaq3Hj1d/MdpAq9Oxf4DKzyqAndqihlxjiIGkkSMnfw=="),
}

for c, ct in frames.items():
    print(c, len(ct))

known_pt = {
    6: b"STATION SIX RELAYING WEATHER CONDITIONS ALONG THE",
    8: b"SIX ACTUAL SENDS RESUPPLY STATUS FOR THE FORWARD ELEMENT NOW OK",
    12: b"RESUPPLY CONVOY DEPARTS AT ZERO FIVE HUNDRED HOURS ACKNOWLEDGE OK",
}
for c, pt in known_pt.items():
    print("known len", c, len(pt), "ct len", len(frames[c]))
