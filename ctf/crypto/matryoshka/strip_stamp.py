import re

body = (
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa"""
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG"""
)

COMMON = re.compile(r"\b(the|and|is|of|to|in|it|you|that|was|for|on|are|with|as|this|be|at|have|from|or|one|had|by|word|but|not|what|all|were|we|when|your|can|said|there|use|an|each|carg|courier|actual|flag|ctf|package|cargo|route|drop|node)\b", re.I)

def score(s):
    return len(COMMON.findall(s)) * 10 + s.count(' ')

def decode(text, LO, HI, sign):
    RNG = HI - LO + 1
    out = []
    for i, ch in enumerate(text):
        code = ord(ch)
        shift = 42 + i
        newcode = (code - LO + sign * shift) % RNG + LO
        out.append(chr(newcode))
    return "".join(out)[::-1]

variants = {
    "full": body,
    "strip_first5": body[5:],
    "strip_last5": body[:-5],
    "strip_both_2_3": body[2:-3],
}

results = []
for name, t in variants.items():
    for LO, HI in [(33,126),(32,126),(32,127),(0,255)]:
        for sign in [1,-1]:
            v = decode(t, LO, HI, sign)
            results.append((score(v), name, LO, HI, sign, v))

results.sort(key=lambda x: -x[0])
for r in results[:8]:
    print(r[:5])
    print(repr(r[5]))
    print()
