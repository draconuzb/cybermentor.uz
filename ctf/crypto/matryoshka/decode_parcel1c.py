import re

body_lines = [
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa""",
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG""",
]

def score(s):
    words = re.findall(r"[A-Za-z]{3,}", s)
    return sum(len(w) for w in words)

def xor_decode(text, start, reverse_in, reverse_out):
    s = text[::-1] if reverse_in else text
    out = []
    for i, ch in enumerate(s):
        out.append(chr(ord(ch) ^ (start + i)))
    r = "".join(out)
    return r[::-1] if reverse_out else r

candidates = []
for name, text in [("line1", body_lines[0]), ("line2", body_lines[1]), ("concat", body_lines[0]+body_lines[1])]:
    for start in [42, -42]:
        for rin in [False, True]:
            for rout in [False, True]:
                v = xor_decode(text, start, rin, rout)
                candidates.append((score(v), name, start, rin, rout, v))

candidates.sort(key=lambda x: -x[0])
for sc, name, start, rin, rout, v in candidates[:8]:
    print(sc, name, start, "revin" if rin else "-", "revout" if rout else "-", repr(v))
