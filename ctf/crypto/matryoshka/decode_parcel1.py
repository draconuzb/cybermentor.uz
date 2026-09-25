body_lines = [
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa""",
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG""",
]

def try_decode(text, reverse_first, start=42, step=1, lo=32, hi=126):
    rng = hi - lo + 1
    s = text[::-1] if reverse_first else text
    out = []
    for i, ch in enumerate(s):
        code = ord(ch)
        shift = start + step * i
        if lo <= code <= hi:
            newcode = (code - lo - shift) % rng + lo
            out.append(chr(newcode))
        else:
            out.append(ch)
    result = "".join(out)
    if not reverse_first:
        pass
    return result

for joined_name, text in [
    ("line1", body_lines[0]),
    ("line2", body_lines[1]),
    ("both_concat", body_lines[0] + body_lines[1]),
    ("both_nl", body_lines[0] + "\n" + body_lines[1]),
]:
    for reverse_first in [True, False]:
        r = try_decode(text, reverse_first)
        printable_ratio = sum(1 for c in r if c.isalnum() or c.isspace()) / max(1, len(r))
        if printable_ratio > 0.5:
            print(f"[{joined_name} rev={reverse_first}] ratio={printable_ratio:.2f}")
            print(repr(r))
            print()
