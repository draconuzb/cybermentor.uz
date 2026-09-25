import re

body = (
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa"""
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG"""
)

alphabet = sorted(set(body))
n = len(alphabet)
idx = {c: i for i, c in enumerate(alphabet)}
print("alphabet size:", n)

COMMON = re.compile(r"\b(the|and|is|of|to|in|it|you|that|was|for|on|are|with|as|this|be|at|have|from|or|one|had|by|word|but|not|what|all|were|we|when|your|can|said|there|use|an|each|which|carg|courier|actual|flag|ctf)\b", re.I)

def score(s):
    return len(COMMON.findall(s)) * 10 + s.count(' ')

def apply(text, sign, step, revin, revout, start=42):
    s = text[::-1] if revin else text
    out = []
    for i, ch in enumerate(s):
        shift = start + step * i
        newidx = (idx[ch] + sign * shift) % n
        out.append(alphabet[newidx])
    r = "".join(out)
    return r[::-1] if revout else r

results = []
for sign in [1, -1]:
    for step in [1, -1]:
        for revin in [False, True]:
            for revout in [False, True]:
                v = apply(body, sign, step, revin, revout)
                results.append((score(v), sign, step, revin, revout, v))

results.sort(key=lambda x: -x[0])
for r in results[:8]:
    print(r[:5])
    print(repr(r[5]))
    print()
