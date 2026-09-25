body = (
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa"""
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG"""
)

LO, HI = 33, 126
RNG = HI - LO + 1

for sign in [-1, 1]:
    out = []
    for j, ch in enumerate(body):
        code = ord(ch)
        shift = 42 + j
        newcode = (code - LO + sign * shift) % RNG + LO
        out.append(chr(newcode))
    X = "".join(out)
    P = X[::-1]
    print("sign", sign)
    print(P)
    print()
