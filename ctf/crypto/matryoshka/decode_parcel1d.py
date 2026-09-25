import re

body = (
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa"""
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG"""
)

LO, HI = 33, 126
RNG = HI - LO + 1  # 94, ROT47-style

def score(s):
    words = re.findall(r"[A-Za-z]{3,}", s)
    return sum(len(w) for w in words), s.count(' ')

def rot_rolling(text, start, sign, reverse_in, reverse_out):
    s = text[::-1] if reverse_in else text
    out = []
    for i, ch in enumerate(s):
        code = ord(ch)
        shift = start + i
        newcode = (code - LO + sign * shift) % RNG + LO
        out.append(chr(newcode))
    r = "".join(out)
    return r[::-1] if reverse_out else r

candidates = []
for sign in [-1, 1]:
    for rin in [False, True]:
        for rout in [False, True]:
            v = rot_rolling(body, 42, sign, rin, rout)
            sc = score(v)
            candidates.append((sc, sign, rin, rout, v))

candidates.sort(key=lambda x: (-x[0][0], -x[0][1]))
for sc, sign, rin, rout, v in candidates[:8]:
    print(sc, "sign", sign, "revin", rin, "revout", rout)
    print(repr(v))
    print()
