import re

body_lines = [
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa""",
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG""",
]

def unshift_seq(text, start=42, sign=-1, lo=32, hi=126):
    rng = hi - lo + 1
    out = []
    for i, ch in enumerate(text):
        code = ord(ch)
        shift = start + i
        if lo <= code <= hi:
            newcode = (code - lo + sign*shift) % rng + lo
            out.append(chr(newcode))
        else:
            out.append(ch)
    return "".join(out)

def score(s):
    words = re.findall(r"[A-Za-z]{2,}", s)
    return len(words), sum(len(w) for w in words)

candidates = []
for name, text in [("line1", body_lines[0]), ("line2", body_lines[1]), ("concat", body_lines[0]+body_lines[1])]:
    for sign in [-1, 1]:
        # variant A: shift applied in original order, no reversal
        a = unshift_seq(text, sign=sign)
        # variant B: reverse input first, then shift
        b = unshift_seq(text[::-1], sign=sign)
        # variant C: shift in original order, then reverse output
        c = a[::-1]
        for vname, v in [("A_noRev", a), ("B_revIn", b), ("C_revOut", c)]:
            sc = score(v)
            candidates.append((sc[1], name, sign, vname, v))

candidates.sort(reverse=True)
for sc, name, sign, vname, v in candidates[:10]:
    print(sc, name, sign, vname, repr(v))
